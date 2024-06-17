#!/usr/bin/env python3

"""
python mkdocs2pdf.py [--mkdocs-yml ../documentation/mkdocs.yml][--project-dir project] --document language-reference-guide
"""

import argparse
import json
import os
import re
import shutil
import sys
from typing import Callable, Dict, Generator, Iterator, List, Tuple, Union

from bs4 import BeautifulSoup
import markdown
from caption import CaptionExtension, TableCaptionExtension
from ruamel.yaml import YAML

from weasyprint import CSS, HTML
from weasyprint.text.fonts import FontConfiguration

NavItem = Union[str, List['NavItem']]
NavDict = Dict[str, NavItem]
NavType = Union[List[NavDict], NavDict]


def shift_headings(body: str, n: int) -> str:
    soup = BeautifulSoup(body, 'html.parser')

    # Find all heading tags
    headings = soup.find_all(re.compile('^h[1-6]$'))

    # Modify each heading tag
    for tag in headings:
        current_level = int(tag.name[1])  # Extract the current heading level
        new_level = min(max(current_level + n, 1), 6)  # Ensure new level is between 1 and 6
        tag.name = f'h{new_level}'

    return str(soup)


def remove_paths(data: Union[dict, list], paths: List[List[str]]) -> Union[dict, list]:
    if isinstance(data, dict):
        for key in list(data.keys()):  # Clone to avoid problems with mutation during iteration
            # Check if this key matches any of the first keys in paths
            matching_paths = [path for path in paths if path and path[0] == key]
            if matching_paths:
                if len(matching_paths[0]) == 1:
                    del data[key]  # Full path matches, remove this key
                else:  # Recurse into the value
                    data[key] = remove_paths(data[key], [path[1:] for path in matching_paths])
                    if not data[key]:  # If the value is now empty, remove the key
                        del data[key]
    elif isinstance(data, list):
        for item in data:
            remove_paths(item, paths)
        data = [item for item in data if item]  # Remove any empty dictionaries from the list
    return data


def parse_mkdocs_yml(yml_file: str, remove: List[List[str]]) -> dict:
    """
    Read and parse the mkdocs.yml files, with options to exclude
    elements from the nav-section based on key paths.
    """
    yaml = YAML()
    with (open(yml_file, 'r', encoding='utf-8')) as f:
        data = yaml.load(f)

    if 'nav' in data and remove:
        data['nav'] = remove_paths(data['nav'], remove)

    return data


def extract_html_h1(data: str) -> str:
    """
    Some files will have a raw HTML <h1> for styling reasons.
    """
    soup = BeautifulSoup(data, 'html.parser')
    if h1 := soup.find('h1'):
        if name_span := h1.find('span', class_='name'):
            name = name_span.get_text() if name_span else None
            if name:
                return name.strip().replace('"', '').replace('`', '')
        else:
            return h1.get_text().strip().replace('"', '').replace('`', '')
    return ''


def extract_h1(filename: str) -> str:
    """
    Find the H1, either markdown or HTML-style
    """
    with open(filename, 'r', encoding='utf-8') as f:
        data = f.read()

    if h1 := extract_html_h1(data):
        return h1

    if h1 := re.findall(r'^#\s+(.+)$', data):
        return h1[0]

    return ''


def find_source_files(prefix: str, nav: NavType, path: List[str] = None) -> Generator[Tuple[List[str], str], None, None]:
    if path is None:
        path = []

    if isinstance(nav, dict):
        for key, value in nav.items():
            current_path = path + [key]
            if isinstance(value, str):
                yield current_path, value
            else:
                yield current_path, ''  # Represent the key-path to an empty string
                yield from find_source_files(prefix, value, current_path)
    elif isinstance(nav, list):
        for item in nav:
            yield from find_source_files(prefix, item, path)
    elif isinstance(nav, str):
        # No key. Pick the H1.
        key = extract_h1(os.path.join(prefix, 'docs', nav))
        current_path = path + [key]
        yield current_path, nav


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


def slug(text: str) -> str:
    return re.sub(r'\W+', '-', text).lower()


def print_footnotes(body: str) -> str:
    """
    Convert to CSS-only footnotes style.
    """
    soup = BeautifulSoup(body, 'html.parser')
    footnote_defs = {}

    # Find all footnote definitions
    for footnote in soup.select('div.footnote ol li'):
        footnote_id = footnote.get('id')
        if footnote_id and footnote_id.startswith('fn:'):
            # Extract the text from the footnote definition
            p_tag = footnote.find('p')
            footnote_text = ''.join(
                str(c) for c in p_tag.contents if not (c.name == 'a' and 'footnote-backref' in c.get('class', [])))
            footnote_defs[footnote_id] = footnote_text.strip()

    # Find all footnote references
    footnote_refs = soup.find_all('sup', id=lambda x: x and x.startswith('fnref:'))

    # Replace footnote references with inlined footnotes
    for ref in footnote_refs:
        footnote_id = ref.find('a').get('href', '').lstrip('#')
        if footnote_id in footnote_defs:
            new_span = soup.new_tag('span', **{'class': 'footnote'})
            new_span.string = footnote_defs[footnote_id]
            ref.replace_with(new_span)

    # Remove the original footnote definitions section
    footnote_div = soup.find('div', class_='footnote')
    if footnote_div:
        footnote_div.decompose()

    # Return the modified HTML content as a string
    return str(soup)


def convert_to_html(filenames: Iterator[str], prefix: str, title: str, macros: dict,
                    transforms: List[Callable[[str], str]]) -> str:
    toc = """
<article id="contents">
    <h2>Contents</h2>
    <ul>
"""
    articles = ""
    section_stack = []
    chapter_number = 0

    for keypath, file in filenames:
        if file == '':  # New Section
            while section_stack and len(section_stack[-1]) >= len(keypath):
                section_stack.pop()
                toc += "</ul></li>\n"
                articles += "</section>\n"

            section_stack.append(keypath)
            heading_level = len(section_stack)
            heading_text = keypath[-1]
            section_id = '-'.join(slug(part) for part in keypath)

            if heading_level == 1:
                chapter_number += 1
                articles += f'<section id="{section_id}">\n<h1 class="chapter">Chapter {chapter_number}: {heading_text}</h1>\n'
                toc += f'<li><strong><a href="#{section_id}">Chapter {chapter_number}: {heading_text}</a></strong><ul class="first-level">\n'
            else:
                articles += f'<section id="{section_id}">\n<h{heading_level}>{heading_text}</h{heading_level}>\n'
                toc += f'<li><a href="#{section_id}">{heading_text}</a><ul>\n'
            continue

        # This represents the start of a new article
        section_id = '-'.join(slug(part) for part in keypath)
        toc += f'<li><a href="#{section_id}">{keypath[-1]}</a></li>\n'
        articles += f'<article id="{section_id}">\n'

        with open(os.path.join(prefix, file), "r", encoding="utf-8") as f:
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
            'admonition',  # https://python-markdown.github.io/extensions/admonition/
            'attr_list',  # https://python-markdown.github.io/extensions/attr_list/
            'footnotes',  # https://python-markdown.github.io/extensions/footnotes/
            'markdown_tables_extended',  # https://github.com/fumbles/tables_extended
            'pymdownx.details',  # https://facelessuser.github.io/pymdown-extensions/extensions/details/
            'pymdownx.superfences',  # https://facelessuser.github.io/pymdown-extensions/extensions/superfences/
            CaptionExtension(numbering=True),
            TableCaptionExtension(),
        ])

        body = shift_headings(body, len(section_stack))
        body = print_footnotes(body)

        articles += body.replace('``', '')  # Empty code blocks aren't rendered correctly
        articles += "\n</article>\n"

    while section_stack:
        section_stack.pop()
        toc += "</ul></li>\n"
        articles += "</section>\n"

    toc += """
    </ul>
</article>
"""

    result = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="assets/main.css">
    <title>{title}</title>
</head>
<body>
{toc}
{articles}
</body>
</html>
"""

    return result


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


def static_assets(assets_dir: str, project='project') -> str:
    """
    Copy the items from the assets_dir to project, accumulating all CSS
    into a string.
    """
    css = ''
    for root, _, files in os.walk(assets_dir):
        for file in files:
            src_name = os.path.join(assets_dir, file)
            newname = os.path.join(project, file)
            os.makedirs(os.path.dirname(newname), exist_ok=True)

            if newname.endswith('.css'):
                with open(src_name, 'r', encoding='utf-8') as f:
                    data = f.read()
                css = css + data

            shutil.copy(src_name, newname)

    return css


def fix_links(b: str) -> str:
    """
    Links in the mkdocs source are "clean URLs" -- the renderer will remove the .md extensions
    on link targets. We have to do that transformation ourselves -- or rather, change to .htm.

    Three cases:

    1. Intra-doc links present with link targets ending in ".md" -- they go to other pages
    defined within the same mkdocs.yml sub-site. Fix those by changing suffix to ".htm".

    2. Inter-doc links have a target presenting with (potentially several) leading "../" and no
    extension. The first actual component (not "../") of the path will be the name of one of the other
    sub-sites. Make the link absolute, and add the ".htm" extension.

    3. Off-site links start with "http" -- return those unchanged.
    """

    def link_transform(match: re.Match) -> str:
        link_text = match.group(1)
        link_target = match.group(2)

        if link_target.startswith('http'):  # Off-site link: return unchanged
            return f'[{link_text}]({link_target})'

        path, name = os.path.split(link_target)
        base, ext = os.path.splitext(name)
        htm_target = f'{os.path.join(path, base)}.htm'

        if ext == '.md':  # Intra-doc link: change extension to ".htm"
            return f'[{link_text}]({htm_target})'

        if ext == '':  # Inter-doc link: make absolute, change extension
            # Replace any number of leading ../ with a single /
            no_slashdot = re.sub(r'^[/.]+', '/', htm_target)
            return f'[{link_text}]({no_slashdot})'

        # Something else; leave alone
        return f'[{link_text}]({link_target})'

    return re.sub(r'\[([^]]+)]\(([^)]+)\)', link_transform, b)


def normalise_links(html: str, documents: Dict[str, str]) -> str:
    soup = BeautifulSoup(html, 'html.parser')

    def extract_components(href):
        # Remove leading ../ and .htm or .html extension
        href = re.sub(r'^[/.]+', '', href)
        href = re.sub(r'\.html?$', '', href)
        return href.split('/')

    # Find all articles and their ids
    articles = soup.find_all('article')
    article_ids = {article['id'] for article in articles}

    # Process all <a> tags
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if not href.startswith('http') and not href.startswith('#'):
            components = extract_components(href)
            matched = False

            for article_id in article_ids:
                if all(component in article_id for component in components):
                    a_tag['href'] = f"#{article_id}"
                    matched = True
                    break

            if not matched:
                first_component = components[0]
                if first_component in documents:
                    # Replace the link with its text in italics
                    a_tag.replace_with(soup.new_tag('i'))
                    a_tag.string = a_tag.get_text()
                else:
                    print(f'--> Can\'t match "{href}" to an article id')

    return str(soup)


def toplevel_docs(nav: List[Dict[str, str]]) -> Dict[str, str]:
    result = {}
    for entry in nav:
        for doc_name, include_path in entry.items():
            path = include_path.split(' ')[1]
            first_component = path.split('/')[1]
            result[first_component] = doc_name
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a PDF-file from a mkdocs site')
    parser.add_argument('--mkdocs-yml', type=str, default='/app/documentation/mkdocs.yml', help='Path to the toplevel mkdocs.yml file')
    parser.add_argument('--document', type=str, required=True, help='Name of dir containing /docs to be converted to PDF')
    parser.add_argument('--project-dir', type=str, default='/app/mkdocs2pdf/project', help='Name of output directory')
    parser.add_argument('--assets-dir', type=str, default='/opt/mkdocs2pdf/assets', help='Name of assets directory')
    parser.add_argument('--exclude', type=str, help='Name of json file with ToC exclusions')

    args = parser.parse_args()

    if not args.mkdocs_yml.endswith('mkdocs.yml'):  # We're only picking out the macro definitions from here.
        sys.exit('--> expected a "mkdocs.yml" file')

    if not os.path.isfile(args.mkdocs_yml):
        sys.exit(f'--> toplevel mkdocs.yml file "{args.mkdocs_yml}" not found.')

    if args.document.endswith('/'):
        args.document = args.document[:-1]

    # If there is a print-specific yml file, use that. Otherwise, use the normal mkdocs.yml file.
    doc_mkdocs_file = str(os.path.join(os.path.abspath(os.path.dirname(args.mkdocs_yml)), args.document, 'print_mkdocs.yml'))
    if not os.path.isfile(doc_mkdocs_file):
        doc_mkdocs_file = str(os.path.join(os.path.abspath(os.path.dirname(args.mkdocs_yml)), args.document, 'mkdocs.yml'))
        if not os.path.isfile(doc_mkdocs_file):
            sys.exit(f'--> document mkdocs.yml file "{doc_mkdocs_file}" not found.')

    os.makedirs(args.project_dir, exist_ok=True)

    # Parse the top-level config
    top_mkdocs_data = parse_mkdocs_yml(args.mkdocs_yml, remove=args.exclude)

    version = top_mkdocs_data["extra"].get("version_majmin")
    if not version:
        sys.exit(f'--> source mkdocs.yml has no Dyalog version set')

    documents = toplevel_docs(top_mkdocs_data.get('nav', {}))

    excludes = []
    if args.exclude:
        with open(args.exclude, 'r', encoding='utf-8') as file:
            excludes = json.load(file)

    # Parse the mkdocs.yml file of our actual document
    yml_data = parse_mkdocs_yml(doc_mkdocs_file, remove=excludes)

    # Find all source Markdown files in depth-first traversal order
    md_files = find_source_files(os.path.dirname(doc_mkdocs_file), yml_data['nav'])

    # Copy static assets into the project
    css = static_assets(args.assets_dir, args.project_dir)

    print(f'--> loaded CSS from {args.assets_dir}: {css[:100]}....[truncated]')

    # Convert each Markdown file to HTML, and concatenate to a single string
    to_html = convert_to_html(md_files, prefix=os.path.join(os.path.dirname(doc_mkdocs_file), 'docs'),
                              title=yml_data['site_name'], macros=top_mkdocs_data.get('extra', {}),
                              transforms=[fix_links], )
    html_content = normalise_links(to_html, documents)

    soup = BeautifulSoup(html_content, 'html.parser')

    # Pretty-print the HTML
    pretty_html = soup.prettify()

    # Write out the combined HTML-file. If we want to switch to a different PDF converter, this can
    # be used to feed that.
    htm_file = f'{args.project_dir}/{args.document}.htm'
    print(f'--> Saving combined html-file "{htm_file}"')
    with (open(htm_file, 'w', encoding='utf-8')) as f:
        f.write(pretty_html)

    # Create a FontConfiguration object -- TODO: is this really needed?
    font_config = FontConfiguration()
    font_file = os.path.join(args.project_dir, 'apl385.ttf')

    # Read the CSS content and ensure the @font-face rule is correctly referencing the font file
    css_content = f"""
        @font-face {{
            font-family: 'APL';
            src: local("APL385 Unicode"), url('file://{font_file}');
        }}
    """ + css

    # Convert HTML to PDF
    target = os.path.abspath(os.path.join(args.project_dir, f'{args.document}.pdf'))
    html = HTML(string=html_content, base_url=f'file://{os.path.abspath(args.project_dir)}')
    stylesheet = CSS(string=css_content, font_config=font_config)
    html.write_pdf(target, stylesheets=[stylesheet], font_config=font_config)
    print(f'--> Saved pdf conversion "{target}"')

