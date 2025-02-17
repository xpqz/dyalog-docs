"""
mkdocs2chm.py

Convert a mkdocs site to a Windows CHM help file bundle.

Stefan Kruger <stefan@dyalog.com>

python mkdocs2chm.py \
    --mkdocs-yml ../mkdocs.yml \
    --project-dir project \
    --assets-dir assets \
    --exclude "UNIX Installation" "UNIX User Guide"

will read the top-level "mkdocs.yml" file and make a CHM file

    dyaloghlp.chm

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
import os
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

HEADER = """
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN">
<html>
<head>
<meta name="GENERATOR" content="Microsoft&reg; HTML Help Workshop 4.1">
</head><body>
<object type="text/site properties">
</object>
"""

DIR_ENTRY = """<li><object type="text/sitemap">
        <param name="Name" value="{name}">
        <param name="ImageNumber" value="0">
    </object>
"""

FILE_ENTRY = """<li><object type="text/sitemap">
        <param name="Name" value="{name}">
        <param name="Local" value="{file}">
        <param name="ImageNumber" value="0">
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

    node = Node(key, value, parent.depth + 1, parent)
    parent.children.append(node)

    if isinstance(value, list):
        for sub_item in value:
            _process_nav_item(sub_item, node, project)


def _traverse(node: Node, toc: IO[str]) -> None:
    title = node.name.replace('`', '').replace('"', '')
    toc.write(DIR_ENTRY.format(name=title))
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
    section -- write out the corresponding CHM TOC XML.
    """
    root = Node()
    nav = yml_data.get('nav', [])
    for item in nav:
        _process_nav_item(item, root, project)

    toc = open(os.path.join(project, '_table_of_contents.hhc'), "w", encoding="utf-8")
    toc.write(HEADER)
    toc.write("<ul>\n")
    _traverse(root, toc)
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


def convert_to_html(filenames: List[str], css: str, macros: dict, transforms: List[Callable[[str], str]], project) -> List[str]:
    """
    Convert each Markdown file and convert to HTML, using the same rendering library as
    mkdocs, with the same set of extensions. We expand the mkdocs-macro {{ templates }}
    and optionally provide means for applying a set of transformations. Currently, add
    all the CSS in the header - not ideal, but convenient.
    """
    converted: List[str] = []

    head = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
"""
    for file in filenames:
        path, oldname = file.split('/docs/', maxsplit=1)
        newname = str(os.path.join(os.path.basename(path), oldname.replace('.md', '.htm')))
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

        with open(realpath_newname, "w", encoding="utf-8") as f:
            f.write(f"{head}<style>\n{css}\n</style></head><body>\n{body}\n</body></html>")
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


def static_assets(src_dir='assets', project='project') -> Tuple[List[str], str]:
    """
    Copy the items in the assets dir. There seem to be no way to
    bundle css via a <link> tag in a CHM file, so we concatenate
    the css files we can find and return this as a string for
    injection into each page. Ugly, but effective.
    """
    assets = []
    css = ''
    
    if not os.path.exists(src_dir):
        return assets, css
        
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
            else:
                shutil.copy(src_path, dst_path)
                assets.append(os.path.join('assets', rel_path))
                
    return assets, css


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
        a, b = filename.split('/docs/', maxsplit=1)
        newname = f"{os.path.basename(a)}/{b.replace('.md', '.htm')}"
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
    searchable.setAttribute("Value", "False")
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a CHM bundle from a mkdocs site')
    parser.add_argument('--mkdocs-yml', type=str, required=True, help='Path to the mkdocs.yml file')
    parser.add_argument('--project-dir', type=str, required=True, help='Name of output directory')
    parser.add_argument('--assets-dir', type=str, default='assets', help='Name of assets directory')
    parser.add_argument('--exclude', nargs='+', help='Names of documents to exclude')

    args = parser.parse_args()

    if not args.mkdocs_yml.endswith('mkdocs.yml'):
        sys.exit('--> expected a "mkdocs.yml" file')

    if not os.path.isfile(args.mkdocs_yml):
        sys.exit(f'--> file {args.mkdocs_yml} not found.')

    # if os.path.exists(args.project_dir):
    #     sys.exit(f'--> project directory "{args.project_dir}" exists. Will not overwrite!')

    # os.makedirs(args.project_dir)

    # Parse the nav section. If this is a monorepo (in 99% of the cases it will be),
    # macro-expand any !include directives
    yml_data = parse_mkdocs_yml(args.mkdocs_yml, remove=args.exclude)
    includes = find_toplevel_dirs(args.mkdocs_yml, remove=args.exclude)

    version = yml_data["extra"].get("version_majmin")
    if not version:
        sys.exit(f'--> source mkdocs.yml has no Dyalog version set')

    # Find all source Markdown files and images
    md_files, image_files = find_source_files(os.path.dirname(args.mkdocs_yml), includes)

    # Copy images and other static assets into the project
    copied_images = copy_images(image_files, project=args.project_dir)
    assets, css = static_assets(args.assets_dir, args.project_dir)

    # Convert to HTML
    html_files = convert_to_html(
        md_files,
        css,
        macros=yml_data.get('extra', {}),
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