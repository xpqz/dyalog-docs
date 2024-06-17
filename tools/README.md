# Docker tools for Dyalog documentation authors

The `tools/` directory contains Docker-based tools for Dyalog's documentation authors. You will need a working installation of [Docker](https://www.docker.com/products/docker-desktop/). We use the `docker-compose` orchestration tool to bundle up a set of containers that are useful for documentation authors who do not wish to keep a local Python environmment.

Note: the directory settings can be stashed in a `.env` file; see [below](#the-env-file).

## Live preview

To preview a mkdocs site, do:

```shell
export DOCS_DIR=path-to-dir-containing-docs  # or use a .env file; see below
docker-compose up [--build][--remove-orphans] mkdocs-server
```

for example, for the whole lot, do:
```shell
export DOCS_DIR=/Users/stefan/work/dyalog-docs/documentation
docker-compose up mkdocs-server
```
and for a particular set,
```shell
export DOCS_DIR=/Users/stefan/work/dyalog-docs/documentation/language-reference-guide/
docker-compose up mkdocs-server
```

Visit [the preview page](http://0.0.0.0:8000/) on http://0.0.0.0:8000/

For individual documents, this is pretty swift, and subsequent source changes will be reflected live.

Note that building the complete set takes several minutes. Consider previewing the specific document you're working on for the best experience.

Note also that you'll see many screens of warnings about links referencing files that do not exist -- this is expected, and a consequence of the [monorepo plugin](https://backstage.github.io/mkdocs-monorepo-plugin/). Links referencing pages across sub-sites will only be valid _after_ the final rendering is complete.

Quit with <kbd>Ctrl</kbd>-<kbd>c</kbd>, and tidy up with 
```shell
docker-compose down
```

## Making the CHM file

Note: this is normally a job for the build pipeline and final testing.

[CHM](https://en.wikipedia.org/wiki/Microsoft_Compiled_HTML_Help) is the long deprecated, but still widely used, Microsoft format for off-line help. We bundle our documentation as a CHM-file with the Windows build of the interpreter.

To render the CHM file, do:
```shell
export DOCS_DIR=/Users/stefan/work/dyalog-docs/documentation
export CHM_OUTPUT_DIR=/Users/stefan/work/dyalog-docs/documentation/tools/project
docker-compose run [--build]  mkdocs2chm
```
which produces `$CHM_OUTPUT_DIR/dyalog.chm` (and several other build artefacts useful for troubleshooting).

NOTE: you want the `DOCS_DIR` variable to point to the top level documentation directory, not a sub-directory for one of the constituent parts (making a CHM-file for a single document makes no sense). 

## Rendering PDFs (experimental)

To render a document as PDF, use the command

```shell
docker-compose run [--build] mkdocs2pdf --document document-name-here
```
where `document-name-here` is the name of a sub-directory of the top-level documentation source directory, for example
```shell
docker-compose run mkdocs2pdf --document language-reference-guide
```

It relies on the two variables `DOCS_DIR` and `PDF_OUTPUT_DIR` to be set. Consider using the `.env` approach. Note also that `mkdocs2chm` and `mkdocs2pdf` can use the same output directory if you so wish.

A successful run will create two files: the .pdf-file and also the merged .htm-file from which it was derived. 

## The .env file

You can gather the environment variable settings into a `.env` file which will be read by `docker-compose`. Create a file called `.env` in the `tools/` directory. There is a file `.env.template` included in the reposiory. Here's mine:

```
DOCS_DIR=/Users/stefan/work/dyalog-docs/documentation
CHM_OUTPUT_DIR=/Users/stefan/work/dyalog-docs/documentation/tools/project
PDF_OUTPUT_DIR=/Users/stefan/work/dyalog-docs/documentation/tools/project
```
