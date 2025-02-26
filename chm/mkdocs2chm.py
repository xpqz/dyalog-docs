"""
mkdocs2chm.py

Convert a mkdocs site to a Windows CHM help file bundle.

Stefan Kruger <stefan@dyalog.com>

python mkdocs2chm.py \
    --mkdocs-yml ../mkdocs.yml \
    --project-dir project \
    --assets-dir assets \
    --config config.json

with a config.json:

{
    "exclude": [
        "UNIX Installation",
        "UNIX User Guide"
    ]
}

will read the top-level "mkdocs.yml" file and make a CHM file

    dyalog.chm

in the ./project/ directory.

Notes:

You need the tool "chmcmd" installed, which is part of Free Pascal. See

    https://wiki.freepascal.org/htmlhelp_compiler

You also need 'pygments' to highlight code.

If a directory 'assets' is found, any .css and .ttf files discovered will be included.
"""

import argparse
from dataclasses import dataclass, field
import itertools
import json
import logging
import os
from csscompressor import compress as css_compress
import cssutils
from htmlmin import minify as html_minify
import re
import shutil
from subprocess import Popen
import sys
from typing import Callable, IO, List, Tuple
import warnings
from xml.dom.minidom import getDOMImplementation

from caption import TableCaptionExtension
from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning
import markdown
from ruamel.yaml import YAML

warnings.filterwarnings('ignore', category=MarkupResemblesLocatorWarning)

cssutils.log.setLevel(logging.CRITICAL)


HEADER = """
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN">
<html>
<head>
<meta name="GENERATOR" content="Microsoft&reg; HTML Help Workshop 4.1">
</head><body>
<object type="text/site properties">
    <param name="SiteType" value="toc">
    <param name="Window Styles" value="0x800401">
    <param name="ExWindow Styles" value="0x200">
</object>
"""

DIR_ENTRY = """<li><object type="text/sitemap">
        <param name="Name" value="{name}">
    </object>
"""

FILE_ENTRY = """<li><object type="text/sitemap">
        <param name="Name" value="{name}">
        <param name="Local" value="{file}">
    </object>
"""

@dataclass
class Node:
    name: str = ''
    value: str | List[str] = None
    depth: int = 0
    parent: 'Node' = None
    children: List['Node'] = field(default_factory=list)
    html_name: str = field(default=None, init=False)

    def __post_init__(self):
        if isinstance(self.value, str) and self.value.endswith('.md'):
            self.html_name = self.value.replace('.md', '.htm')

    def isdir(self):
        return len(self.children) > 0


def _process_nav_item(item: dict | str, parent: Node, project='project') -> None:
    """
    Process a single nav item -- either a dict, which has either a string
    value (leaf node), or a list value -- of other nav items, or a string
    referencing a file, from which the name needs to be picked up from the
    H1 later.
    """
    if isinstance(item, dict):
        (key, value), = item.items()
    else:  # No name in the yml -- name should be picked up from the H1 in the file
        key = ''
        value = item  # item is the filename -- swap to .htm to parse
        if item.endswith('.md'):
            html_file = os.path.join(project, item.replace('.md', '.htm'))
            with open(html_file, "r", encoding="utf-8") as f:
                data = f.read()
            if h1 := extract_h1(data):
                key = h1

            # Special case for welcome.md - override the H1 title
            if item == 'welcome.md':
                key = 'Welcome'

    node = Node(key, value, parent.depth + 1, parent)
    parent.children.append(node)

    if isinstance(value, list):
        for sub_item in value:
            _process_nav_item(sub_item, node, project)


def _traverse(node: Node, toc: IO[str]) -> None:
    title = node.name.replace('`', '').replace('"', '')
    toc.write(DIR_ENTRY.format(name=title))
    if node.children:  # Only write <ul> if there are children
        toc.write("<ul>\n")
        for child in node.children:
            if child.isdir():
                _traverse(child, toc)
            else:
                toc.write(FILE_ENTRY.format(name=child.name.replace('`', '').replace('"', ''), file=child.html_name))
        toc.write("</ul>\n")

def modify_paths(navdata, base_path: str):
    """
    In the monorepo, included documents must have the
    top-level prepended (here known as the `base_path`)
    """
    if isinstance(navdata, dict):
        for key, value in navdata.items():
            if isinstance(value, (dict, list)):
                navdata[key] = modify_paths(value, base_path)
            elif isinstance(value, str) and value.endswith('.md'):
                navdata[key] = os.path.join(base_path, value)
    elif isinstance(navdata, list):
        navdata = [modify_paths(item, base_path) for item in navdata]
    elif isinstance(navdata, str):
        navdata = os.path.join(base_path, navdata)
    return navdata


def parse_mkdocs_yml(yml_file: str, remove: List[str]) -> dict:
    """
    Read and parse the mkdocs.yml files. The monorepo plugin references
    the sub-document mkdocs.yml files, which we expand in place to produce
    the complete state.
    """

    yaml = YAML()
    with (open(yml_file, 'r', encoding='utf-8')) as f:
        data = yaml.load(f)

    if remove:
        data['nav'] = [item for item in data['nav'] if not any(key in item for key in remove)]

    def resolve_includes(data: dict, base_path: str) -> dict:
        if isinstance(data, dict):
            for key, value in data.items():
                data[key] = resolve_includes(value, base_path)
        elif isinstance(data, list):
            for i in range(len(data)):
                data[i] = resolve_includes(data[i], base_path)
        elif isinstance(data, str) and data.startswith("!include"):
            include_path = data.split(' ')[1]
            full_path = os.path.normpath(os.path.join(base_path, include_path))
            navdata = parse_mkdocs_yml(full_path, remove=[])['nav']
            subdir = os.path.basename(os.path.dirname(include_path))
            return modify_paths(navdata, subdir)
        return data

    base_path = os.path.dirname(yml_file)
    return resolve_includes(data, base_path)

def generate_toc(yml_data: dict, project='project'):
    """
    Given the parsed and expanded mkdocs.yml -- specifically its "nav"
    section -- write out the corresponding CHM TOC XML with top-level items
    directly under the root <ul>.
    """
    root = Node()  # Still used to build the hierarchy
    nav = yml_data.get('nav', [])
    for item in nav:
        _process_nav_item(item, root, project)

    toc = open(os.path.join(project, '_table_of_contents.hhc'), "w", encoding="utf-8")
    toc.write(HEADER)
    toc.write("<ul>\n")
    
    # Write top-level children directly, skipping the empty root
    for child in root.children:
        if child.isdir():
            _traverse(child, toc)
        else:
            toc.write(FILE_ENTRY.format(name=child.name.replace('`', '').replace('"', ''), file=child.html_name))
    
    toc.write("</ul>\n")
    toc.write("</body></html>\n")
    toc.close()

def find_source_files(topdir: str, subdirs: List[str]) -> Tuple[List[str], List[str]]:
    """
    Under `topdir`, recursively scan the subdirs defined by `subdirs`,
    and return full paths to all Markdown and image files.
    """
    markdown_files = []
    image_files = []

    for subdir in subdirs:
        incldir = os.path.join(topdir, re.sub(r'^[./]+', '', os.path.dirname(subdir)))
        if not os.path.isdir(incldir):
            raise NotADirectoryError(f'Not a directory: {incldir}')
        for root, _, files in os.walk(incldir):
            for file in files:
                full_path = os.path.abspath(os.path.join(root, file))
                # If the markdown source has been used to build a site already, we need to
                # ensure we skip the target files
                if '/site/' in full_path:
                    continue
                extension = os.path.splitext(full_path)[-1]
                if extension == '.md':
                    markdown_files.append(full_path)
                elif extension in {'.png', '.gif', '.jpg', '.bmp', '.jpeg'}:
                    image_files.append(full_path)

    return markdown_files, image_files


def expand_macros(data: str, macros: dict) -> str:
    """
    The mkdocs macro extension makes use of templates of the type {{ macro-id }} where
    the substitution value is stored in the "extra:" section in the mkdocs.yml file.
    """
    def replace(match):
        key = match.group(1).strip()
        value = macros.get(key)
        return str(value) if not isinstance(value, dict) else match.group(0)
    return re.sub(r'\{\{\s*(.*?)\s*}}', replace, data)


def purge_css(css: str, html_content: str) -> str:
    """
    Simple CSS purger that removes unused selectors.
    Uses cssutils for parsing CSS and BeautifulSoup for HTML.
    Preserves selectors for important HTML structure elements.
    """
    # Parse the HTML to find all class names and IDs
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all class names in use
    classes_in_use = set()
    for tag in soup.find_all(class_=True):
        classes_in_use.update(tag.get('class'))
    
    # Find all IDs in use
    ids_in_use = {tag.get('id') for tag in soup.find_all(id=True)}
    
    # Find all tag names in use
    tags_in_use = {tag.name for tag in soup.find_all()}
    
    # Add essential HTML structure elements that might not appear in the parsed HTML
    # but are still needed for proper styling
    essential_tags = {'html', 'head', 'body', 'main', 'article', 'section', 'header', 'footer'}
    tags_in_use.update(essential_tags)
    
    # Parse the CSS
    stylesheet = cssutils.parseString(css)
    
    # Track which rules to keep
    rules_to_keep = []
    
    # Process each rule
    for rule in stylesheet:
        if rule.type == rule.STYLE_RULE:
            selectors = rule.selectorText.split(',')
            matched_selectors = []
            
            for selector in selectors:
                selector = selector.strip()
                should_keep = False
                
                # Always keep essential structure selectors and their variants
                for tag in essential_tags:
                    if re.search(r'\b' + re.escape(tag) + r'\b', selector):
                        should_keep = True
                        break
                
                if not should_keep:
                    # Simple tag selectors like "div" or "p"
                    if selector in tags_in_use:
                        should_keep = True
                    # Class selectors like ".my-class"
                    elif selector.startswith('.') and selector[1:] in classes_in_use:
                        should_keep = True
                    # ID selectors like "#my-id"
                    elif selector.startswith('#') and selector[1:] in ids_in_use:
                        should_keep = True
                    # Universal selector
                    elif selector == '*':
                        should_keep = True
                    # Complex selectors - more conservative, keep these to avoid breaking things
                    elif any(c in selector for c in (':', '>', '+', '~', '[', ']')):
                        should_keep = True
                    # Selectors with tags, classes, or IDs that might be used
                    else:
                        # Check for tag names
                        for tag in tags_in_use:
                            if re.search(r'\b' + re.escape(tag) + r'\b', selector):
                                should_keep = True
                                break
                        
                        # Check for class names
                        if not should_keep:
                            for cls in classes_in_use:
                                if re.search(r'\.' + re.escape(cls) + r'\b', selector):
                                    should_keep = True
                                    break
                        
                        # Check for IDs
                        if not should_keep:
                            for id_val in ids_in_use:
                                if re.search(r'#' + re.escape(id_val) + r'\b', selector):
                                    should_keep = True
                                    break
                
                if should_keep:
                    matched_selectors.append(selector)
            
            # If any selectors matched, keep this rule with only the matched selectors
            if matched_selectors:
                rule.selectorText = ', '.join(matched_selectors)
                rules_to_keep.append(rule)
        
        # Keep other types of rules (like @media, @keyframes, etc.)
        elif rule.type != rule.COMMENT:
            rules_to_keep.append(rule)
    
    # Create a new stylesheet with only the retained rules
    new_stylesheet = cssutils.css.CSSStyleSheet()
    for rule in rules_to_keep:
        new_stylesheet.add(rule)
    
    # Serialise the new stylesheet    
    return new_stylesheet.cssText.decode('utf-8')

def convert_to_html(filenames: List[str], css: str, macros: dict, transforms: List[Callable[[str], str]], project) -> List[str]:
    """
    Convert each Markdown file and convert to HTML, using the same rendering library as
    mkdocs, with the same set of extensions. We expand the mkdocs-macro {{ templates }}
    and optionally provide means for applying a set of transformations. Currently, we add
    all the CSS in the header - this is required as the HTML engine in the Windows CHM
    viewer does not understand <link ...>.

    As a mitigation, take steps to only add the actually used CSS bits.
    """
    converted: List[str] = []

    head = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
"""
    
    converted: List[str] = []    

    for file in filenames:
        # Handle both root-level files and files in docs subdirectories
        if '/docs/' in file:
            path, oldname = file.split('/docs/', maxsplit=1)
            newname = str(os.path.join(os.path.basename(path), oldname.replace('.md', '.htm')))
        else:
            # For root-level files, just use the basename
            newname = os.path.basename(file).replace('.md', '.htm')
            
        realpath_newname = str(os.path.join(project, newname))
        os.makedirs(os.path.dirname(realpath_newname), exist_ok=True)

        with open(file, "r", encoding="utf-8") as f:
            md = f.read()

        # Macros are defined in the "extra:" section in the mkdocs.yml file. In the Markdown
        # source, they are templates of the type
        #
        #    {{ macro-name }}
        md = expand_macros(md, macros)

        # Hook point for transforms we may want to apply to the source Markdown before it's
        # converted to HTML.
        for fun in transforms:
            md = fun(md)

        # Convert Markdown to HTML, using the same extensions as used by our mkdocs setup.
        body = markdown.markdown(md, extensions=[
            'admonition',                # https://python-markdown.github.io/extensions/admonition/
            'attr_list',                 # https://python-markdown.github.io/extensions/attr_list/
            'footnotes',                 # https://python-markdown.github.io/extensions/footnotes/
            'markdown_tables_extended',  # https://github.com/fumbles/tables_extended
            'pymdownx.details',          # https://facelessuser.github.io/pymdown-extensions/extensions/details/
            'pymdownx.superfences',      # https://facelessuser.github.io/pymdown-extensions/extensions/superfences/
            TableCaptionExtension(),     # https://github.com/flywire/caption
        ])

        body = body.replace('``', '')  # Empty code blocks aren't rendered correctly

        body = fix_links_html(body)

        # Optimise CSS specifically for this page: only use selectors referring to 
        # ids, classes and tags on the actual page.
        optimised_css = purge_css(css, body)
        
        # Minimise the CSS
        optimised_css = css_compress(optimised_css)

        # Construct and minimise the HTML
        final_html = f"{head}<style>{optimised_css}</style></head><body>{body}</body></html>"
        final_html = html_minify(
            final_html, 
            remove_comments=True,
            remove_empty_space=True, 
            remove_all_empty_space=False,
            reduce_boolean_attributes=True
        )

        with open(realpath_newname, "w", encoding="utf-8") as f:
            f.write(final_html)
            
        converted.append(str(newname))
    return converted

def copy_images(filenames: List[str], project='project') -> List[str]:
    copied: List[str] = []
    for file in filenames:
        path, oldname = file.split('/docs/', maxsplit=1)
        newname = str(os.path.join(os.path.basename(path), oldname))
        realpath_newname = str(os.path.join(project, newname))
        os.makedirs(os.path.dirname(realpath_newname), exist_ok=True)
        shutil.copy(file, realpath_newname)
        copied.append(newname)
    return copied


def static_assets(src_dir='assets', project='project') -> Tuple[List[str], str, List[str]]:
    """
    Copy the items in the assets dir. There is no supported way to
    bundle css via a <link> tag in a CHM file, so we concatenate
    the css files we can find and return this as a string for
    injection into each page.
    """
    assets = []
    css_files = []  # Keep track of CSS files
    css = ''
    
    if not os.path.exists(src_dir):
        return assets, css, css_files
        
    os.makedirs(os.path.join(project, 'assets'), exist_ok=True)
    
    for root, _, files in os.walk(src_dir):
        for file in files:
            src_path = os.path.join(root, file)
            rel_path = os.path.relpath(src_path, src_dir)
            dst_path = os.path.join(project, 'assets', rel_path)
            
            # Ensure destination directory exists
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)

            if file.endswith('.css'):
                with open(src_path, 'r', encoding='utf-8') as f:
                    data = f.read()
                css = css + data
                css_files.append(src_path)  # Add to list of CSS files
            else:
                shutil.copy(src_path, dst_path)
                assets.append(os.path.join('assets', rel_path))
                
    return assets, css, css_files


def extract_h1(data: str) -> str:
    """
    Some files will have a raw HTML <h1> for styling reasons.
    """
    soup = BeautifulSoup(data, 'html.parser')
    if h1 := soup.find('h1'):
        if name_span := h1.find('span', class_='name'):
            command_span = h1.find('span', class_='command')
            name = name_span.get_text() if name_span else None
            command = command_span.get_text() if command_span else None
            if name and command:
                return f"{name} {command}".strip()
            elif name:
                return name.strip().replace('"', '').replace('`', '')
        else:
            return h1.get_text().strip().replace('"', '').replace('`', '')
    return ''


def extract_headers(filename: str) -> List[str]:
    """
    Find all headers -- Markdown headers are lines that start with one or more '#'.
    Some files will also have a raw HTML <h1> for styling reasons. The headers will
    be used as entries in the CHM index file.
    """
    results: List[str] = []

    with open(filename, 'r', encoding='utf-8') as f:
        data = f.read()

    h1 = extract_h1(data)
    if h1:
        results.append(h1)

    headers = re.findall(r'^#+\s+(.+)$', data)
    results.extend(headers)

    return results


def generate_index_data(files: List[str]) -> List[Tuple[str, str]]:
    """
    Note: we're generating the index data from the source Markdown, but we
    need to ensure that filenames refer to the converted HTML files.
    """
    entries = []
    for filename in files:
        headings = extract_headers(filename)
        if '/docs/' in filename:
            a, b = filename.split('/docs/', maxsplit=1)
            newname = f"{os.path.basename(a)}/{b.replace('.md', '.htm')}"
        else:
            # For root-level files, just use the basename
            newname = os.path.basename(filename).replace('.md', '.htm')
            
        for heading in headings:
            entries.append((heading, newname))

    # Sort the index alphabetically by entry (not filename!)
    entries.sort(key=lambda w: w[0])

    return entries


def write_index_data(entries: List[Tuple[str, str]], filename: str) -> None:
    """
    Write out the CHM index file.
    """
    with open(filename, "w", encoding="utf-8") as idxfh:
        idxfh.write(HEADER)
        idxfh.write("<ul>\n")
        for x in entries:
            idxfh.write(FILE_ENTRY.format(name=x[0], file=x[1]))
        idxfh.write("</ul>\n")
        idxfh.write("</body></html>\n")


def find_toplevel_dirs(filename: str, remove: List[str]) -> List[str]:
    """
    Find the toplevel document dirs -- these are the ones that are
    pulled into the main mkdocs.yml file via !include
    """
    yaml = YAML()
    with (open(filename, 'r', encoding='utf-8')) as f:
        data = yaml.load(f)
    tlds = []
    for d in data['nav']:
        key, value = next(iter(d.items()))
        if key not in remove:
            if m := re.match(r'!include\s+([^"]+)', value):
                tlds.append(m.group(1))

    return tlds


def generate_hfp(project: str, chmfile: str, files: List[str], images: List[str], assets: List[str], title: str) -> None:
    """
    Generates a project .hfp file for the chmcmd chm compiler, listing all .htm-files
    in the directory tree, plus the _index.hhk and _table_of_contents.hhc files.
    """
    start_page = None
    base, chmext = os.path.splitext(chmfile)
    hfp = base + '.hfp'
    outfile = os.path.join(project, hfp)

    impl = getDOMImplementation()

    doc = impl.createDocument(None, "CONFIG", None)

    # Create the <CONFIG> base element
    cfg = doc.documentElement

    # Files section
    filegroup = doc.createElement("Files")
    cfg.appendChild(filegroup)

    count = doc.createElement("Count")
    count.setAttribute("Value", str(len(files) + len(images)))
    filegroup.appendChild(count)

    fcount = 0

    for file in itertools.chain(files, images, assets):
        f = doc.createElement("FileName" + str(fcount))
        f.setAttribute("Value", file)
        filegroup.appendChild(f)
        if start_page is None:
            _, ext = os.path.splitext(file)
            if ext == '.htm':
                start_page = file
        fcount = fcount + 1

    tcf = doc.createElement("IndexFile")
    tcf.setAttribute("Value", "_index.hhk")
    filegroup.appendChild(tcf)

    tcf = doc.createElement("TOCFile")
    tcf.setAttribute("Value", "_table_of_contents.hhc")
    filegroup.appendChild(tcf)

    settings = doc.createElement("Settings")
    cfg.appendChild(settings)

    searchable = doc.createElement("MakeSearchable")
    searchable.setAttribute("Value", "True")
    settings.appendChild(searchable)

    if start_page is None:
        start_page = 'index.htm'
    dflt = doc.createElement("DefaultPage")
    dflt.setAttribute("Value", start_page)
    settings.appendChild(dflt)

    te = doc.createElement("Title")
    te.setAttribute("Value", title)
    settings.appendChild(te)

    ofn = doc.createElement("OutputFileName")
    ofn.setAttribute("Value", chmfile)
    settings.appendChild(ofn)

    fnt = doc.createElement("DefaultFont")
    fnt.setAttribute("Value", "")
    settings.appendChild(fnt)

    with open(outfile, 'w', encoding="utf-8") as f:
        f.write(doc.toprettyxml(indent="  "))


def table_captions(body: str) -> str:
    """
    Find table captions and references. Adapt for use with

        https://github.com/flywire/caption

    Captions will have the format

        Table: caption_text {: #anchor_name }

    References are links to the anchor name, but without a link text:

        [](#anchor_name)

    The flywire/caption Markdown extension uses its own ids of the form

        _table-X

    so we need to rewrite our ids to theirs. Also, flywire/caption has
    no automatic renumbering of table _references_, so fill that out.
    """
    anchors = {}
    idx_list = []

    def replace_table_captions(match, idx_list):
        idx = len(idx_list) + 1  # ⎕IO ← 1
        caption_text, anchor_name = match.groups()
        idx_list.append(idx)
        anchors[anchor_name] = idx
        return f"Table: {caption_text}"

    # Update table references
    def replace_table_refs(match):
        anchor_name = match.group(1)
        if anchor_name in anchors:
            idx = anchors[anchor_name]
            return f"[Table {idx}](#_table-{idx})"
        return match.group(0)  # Return the original match if not in anchors

    # Rework caption ids.
    body = re.sub(r"Table:\s*(.*?)\s*\{:\s*#(\S+)\s*\}", lambda match: replace_table_captions(match, idx_list), body)
    return re.sub(r"\[\]\(#(\S+)\)", replace_table_refs, body)  # Update table references

def fix_links_html(html: str) -> str:
    """
    Applies the link transformations to an HTML document:
    1. Links with targets ending in ".md" are changed to ".htm".
    2. Links without extensions and leading "../" are lifted one relative level, and suffixed with ".htm".
    3. Off-site links starting with "http" remain unchanged.

    Parameters:
        html (str): The HTML content as a string.

    Returns:
        str: The modified HTML content.
    """

    def transform_link(href: str) -> str:
        """
        Transforms an individual href link according to the rules.
        """
        if href.startswith('http'):  # Off-site link: leave unchanged
            return href

        path, name = os.path.split(href)
        base, ext = os.path.splitext(name)

        if ext == '.md':  # Link to another sub-site: change ".md" to ".htm"
            return os.path.join(path, f'{base}.htm')

        if ext == '':  # Link within the same side -- lift one relative level, and add .htm
            target = re.sub(r'^\.\.\/', '', href, count=1)
            return f'{target}.htm'

        # Something else; leave unchanged
        return href

    # Parse the HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Find and transform all <a> tags with href attributes
    for a_tag in soup.find_all('a', href=True):
        original_href = a_tag['href']
        a_tag['href'] = transform_link(original_href)

    # Return the modified HTML as a string
    return str(soup)

def find_image_references_in_markdown(md_files: List[str]) -> set:
    """
    Find all image references in Markdown files.
    Returns set of image filenames.
    """
    image_refs = set()
    
    # Regular expression for Markdown image syntax: ![alt](path/image.png)
    md_img_pattern = r'!\[.*?\]\((.*?)\)'
    
    # Regular expression for HTML image tags in Markdown: <img src="path/image.png">
    html_img_pattern = r'<img[^>]*src=[\'"]([^\'"]+)[\'"][^>]*>'
    
    for file in md_files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Find Markdown-style image references
                for match in re.findall(md_img_pattern, content):
                    if not match.startswith(('http:', 'https:', 'data:')):
                        image_refs.add(os.path.basename(match))
                
                # Find HTML-style image references
                for match in re.findall(html_img_pattern, content):
                    if not match.startswith(('http:', 'https:', 'data:')):
                        image_refs.add(os.path.basename(match))
        except Exception as e:
            print(f"Warning: Could not check images in {file}: {e}")
    
    return image_refs

def find_image_references_in_css(css_files: List[str]) -> set:
    """
    Find all image references in CSS files.
    Returns set of image filenames.
    """
    image_refs = set()
    
    # Regular expression for CSS url() syntax: url('/path/image.png')
    css_img_pattern = r'url\([\'"]?([^\'"()]+)[\'"]?\)'
    
    for file in css_files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Find CSS url() references
                for match in re.findall(css_img_pattern, content):
                    if not match.startswith(('http:', 'https:', 'data:')):
                        # Extract just the filename from the path
                        image_refs.add(os.path.basename(match))
        except Exception as e:
            print(f"Warning: Could not check images in CSS file {file}: {e}")
    
    return image_refs

def filter_unused_images(md_files: List[str], css_files: List[str], image_files: List[str]) -> List[str]:
    """
    Filter out images that are not referenced in any Markdown or CSS files.
    Returns filtered list of image files to include.
    """
    # Find all image references from Markdown and CSS
    md_referenced_images = find_image_references_in_markdown(md_files)
    css_referenced_images = find_image_references_in_css(css_files)
    
    referenced_images = md_referenced_images.union(css_referenced_images)
    
    # Filter image_files to only include referenced images
    used_images = []
    unused_images = []
    
    for img in image_files:
        if os.path.basename(img) in referenced_images:
            used_images.append(img)
        else:
            unused_images.append(img)
    
    # Report findings
    if unused_images:
        print("\nExcluding unused images:")
        for img in sorted(unused_images):
            print(f"  {os.path.basename(img)}")
        print(f"\nTotal: {len(unused_images)} unused images removed, keeping {len(used_images)} used images")
    else:
        print("\nAll images are referenced in the documentation or CSS.")
    
    if css_referenced_images:
        print("\nImages referenced in CSS:")
        for img in sorted(css_referenced_images):
            print(f"  {img}")
    
    return used_images

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a CHM bundle from a mkdocs site')
    parser.add_argument('--mkdocs-yml', type=str, required=True, help='Path to the mkdocs.yml file')
    parser.add_argument('--project-dir', type=str, required=True, help='Name of output directory')
    parser.add_argument('--assets-dir', type=str, default='assets', help='Name of assets directory')
    parser.add_argument('--welcome', type=str, default='welcome.md', help='Path to welcome.md file')
    parser.add_argument('--config', type=str, help='JSON config file for additional options')
    parser.add_argument('--git-info', type=str, help='Git branch and commit info')
    parser.add_argument('--build-date', type=str, help='Build date')

    args = parser.parse_args()

    if not args.mkdocs_yml.endswith('mkdocs.yml'):
        sys.exit('--> expected a "mkdocs.yml" file')

    if not os.path.isfile(args.mkdocs_yml):
        sys.exit(f'--> file {args.mkdocs_yml} not found.')

    if not os.path.isfile(args.welcome):
        sys.exit(f'--> welcome file {args.welcome} not found.')

    os.makedirs(args.project_dir, exist_ok=True)

    # Parse the nav section. If this is a monorepo (in 99% of the cases it will be),
    # macro-expand any !include directives

    excludes = []
    if args.config:
        try:
            with open(args.config, 'r', encoding='utf-8') as f:
                config = json.load(f)
                excludes = config.get('exclude', [])
        except (json.JSONDecodeError, FileNotFoundError) as e:
            sys.exit(f'--> Error reading config file: {e}')

    yml_data = parse_mkdocs_yml(args.mkdocs_yml, remove=excludes)
    includes = find_toplevel_dirs(args.mkdocs_yml, remove=excludes)

    version = yml_data["extra"].get("version_majmin")
    if not version:
        sys.exit(f'--> source mkdocs.yml has no Dyalog version set')

    # Find all source Markdown files and images
    md_files, image_files = find_source_files(os.path.dirname(args.mkdocs_yml), includes)

    # Add welcome.md to the start of the files list
    md_files.insert(0, os.path.abspath(args.welcome))
    
    # Modify nav to include welcome page at the start
    yml_data['nav'].insert(0, 'welcome.md')

    # Copy images and other static assets into the project
    assets, css, css_files = static_assets(args.assets_dir, args.project_dir)
    
    # Filter out unused images, considering both MD and CSS references
    image_files = filter_unused_images(md_files, css_files, image_files)
    copied_images = copy_images(image_files, project=args.project_dir)
    
    # Add git info and build date to macros
    macros = yml_data.get('extra', {})
    if args.git_info:
        macros['git_info'] = args.git_info
    if args.build_date:
        macros['build_date'] = args.build_date

    # Convert to HTML
    html_files = convert_to_html(
        md_files,
        css,
        macros=macros,
        transforms=[
            table_captions
        ],
        project=args.project_dir
    )

    # Generate the CHM ToC
    generate_toc(yml_data, project=args.project_dir)

    # Generate the index
    idx = generate_index_data(md_files)
    write_index_data(idx, f'{args.project_dir}/_index.hhk')

    print(f'Converted {len(md_files)} Markdown files to HTML.')

    # Generate the CHM project config file
    chm_name = "dyalog.chm"

    generate_hfp(args.project_dir, chm_name, html_files, copied_images, assets, title=f'Dyalog version {version}')

    # Run the compiler
    output = Popen(['chmcmd', 'dyalog.hfp'], cwd=args.project_dir)
    output.wait()