# Tools for Dyalog documentation authors

The `tools/` directory contains Docker-based tools for Dyalog's documentation authors. You will need a working installation of [Docker](https://www.docker.com/products/docker-desktop/). We use the `docker-compose` orchestration tool to bundle up a set of containers that are useful for documentation authors who do not wish to keep a local Python environment.

Note: the directory settings can be stashed in a `.env` file; see [below](#the-env-file).

## Live preview

A "sub-site" is one of the component documents as defined by the nav section in the top-level `mkdocs.yml` file, currently:

- release-notes-v19-0
- windows-installation-and-configuration-guide
- unix-installation-and-configuration-guide
- programming-reference-guide
- language-reference-guide
- object-reference
- windows-ui-guide
- interface-guide
- dotnet-interface
- unix-user-guide

> **Note:** When using the Docker-based tools, you need to give `docker-compose` the **full command name**, _not_ a bare `docker-compose up`. 

To preview a mkdocs site, do:

```shell
export DOCS_DIR=path-to-dir-containing-docs  # or use a .env file; see below
docker-compose up [--build][--remove-orphans] mkdocs-server
```
Note the full command name. For example, for the whole lot, do:
```shell
export DOCS_DIR=/Users/stefan/work/documentation
docker-compose up mkdocs-server
```
and for a particular sub-site, e.g the `language-reference-guide` (see list above):
```shell
export DOCS_DIR=/Users/stefan/work/documentation/language-reference-guide/
docker-compose up mkdocs-server
```

> **Note**: The first time you run `docker-compose`, the various containers will be built. Subsequent runs will reuse the containers, and will be quicker to start.

Visit [the preview page](http://localhost:8000/) on http://localhost:8000/

For individual documents, this is pretty swift, and subsequent source changes will be reflected live.

Note that building the complete set takes several minutes. Consider previewing the specific document you're working on for the best experience.

Note also that you'll see many screens of warnings about links referencing files that do not exist -- this is expected, and a consequence of the [monorepo plugin](https://backstage.github.io/mkdocs-monorepo-plugin/). Links referencing pages across sub-sites will only be valid _after_ the final rendering is complete.

The docker image will consume resources, so when you're finished, be sure to quit with <kbd>Ctrl</kbd>-<kbd>c</kbd>, and tidy up with 
```shell
docker-compose down
```

## Making the CHM file

Note: this is normally a job for the build pipeline and final testing.

[CHM](https://en.wikipedia.org/wiki/Microsoft_Compiled_HTML_Help) is the still widely used, Microsoft format for off-line help. We bundle our documentation as a CHM-file with the Windows build of the interpreter.

To render the CHM file, do:
```shell
export DOCS_DIR=/Users/stefan/work/documentation
export CHM_OUTPUT_DIR=/Users/stefan/work/documentation/tools/project
docker-compose run [--build] mkdocs2chm
```
which produces `$CHM_OUTPUT_DIR/dyalog.chm` (and several other build artefacts useful for troubleshooting).

> **Note** you want the `DOCS_DIR` variable to point to the top level documentation directory, not a sub-directory for one of the constituent parts (making a CHM-file for a single document makes no sense). 

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

## The `.env` file

You can gather the environment variable settings into a `.env` file which will be read by `docker-compose`. Create a file called `.env` in the `tools/` directory. There is a file `.env.template` included in the repository. It should look like this (for a complete render of _all_ docs):

```
DOCS_DIR={YOUR_REPO}
CHM_OUTPUT_DIR={YOUR_REPO}/tools/project
PDF_OUTPUT_DIR={YOUR_REPO}/tools/project
```

Here is mine:

```
DOCS_DIR=/Users/stefan/work/documentation
CHM_OUTPUT_DIR=/Users/stefan/work/documentation/tools/project
PDF_OUTPUT_DIR=/Users/stefan/work/documentation/tools/project
```

and for a specific sub-site, in this case `language-reference-guide`:

```
DOCS_DIR=/Users/stefan/work/documentation/language-reference-guide
CHM_OUTPUT_DIR=/Users/stefan/work/documentation/tools/project
PDF_OUTPUT_DIR=/Users/stefan/work/documentation/tools/project
```

> **Note**: the last two lines don't need to change.

If you're on Windows, you _must_ use backslashes:

```
DOCS_DIR=C:\devt\documentation
CHM_OUTPUT_DIR=C:\devt\documentation\tools\project
PDF_OUTPUT_DIR=C:\devt\documentation\tools\project
```

## Running Docker on Windows

To run `docker-compose up` on Windows, you'll need to have `Docker Desktop` for Windows installed and
running. `Docker Desktop` includes both `Docker` and `Docker Compose`.

**Install Docker Desktop for Windows**

> **Warning:** If you're using Microsoft Windows 10, you cannot use WSL2 with Docker. Choose HyperV instead during installation.

1. Download and run the [Docker Desktop installer](https://docs.docker.com/desktop/install/windows-install/) and follow
   the prompts to complete the installation.
2. `Docker Desktop` will recommend you to enable the [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install) feature
   and potentially install a Linux kernel update package. Follow the installation guide provided by
   the `Docker` installer. 
3. After installation, run `Docker Desktop`. You might need to log in with your Docker account.

**Open a terminal**

1. You can use either Command Prompt (cmd) or PowerShell to run Docker commands on Windows.
2. Use the `cd` command to go to the directory containing the `docker-compose.yml` file.
3. Run `docker-compose up`. This command reads the `docker-compose.yml` file in the current directory, builds the images
   if they don't exist, and starts the containers as specified in the file.
4. If you've made changes to your `Dockerfile` or Docker Compose configuration and want to rebuild the images, you can
   use `docker-compose up --build mkdocs-server`.
   
## APL-based tools

### BuildGUI

Note:

1. This code has been exported from the workspace `Core/ws/GUIMaint.dws`.
2. The code can only be run on Windows.

The main purpose of the code herein is to generate the cross-reference tables present in the `Object Reference Guide`. In
all likelihood, this is now fairly static, but changes do still occasionally happen. The code was written a long time ago, before Dyalog contained, for example, `⎕XML`. There are a few other, related functions in present, but only the cross-references generation has been ported to the new format for now.

The code has been left as-is, with the following exceptions:

1. The workspace has been exported to text, so that it can be versioned.
2. The function `WriteFile` now ensures that any directories not present in its path are created.

Additionally, two new functions have been added:

1. `NewBuildGUI`: the new entry point, serving the same purpose as `BuildGUI`, but not writing entries into a
   Table-of-Contents file, and not writing stubbed entries of new object.
2. `NewWriteMembers`: analogous to `WriteMembers`, creating the actual cross-reference tables, but writing
   Markdown instead of XML. This function will sort the tables it generates in col-major order. The old code generated
   tables that were occasionally not sorted at all.

To run this code, say

```apl
files ← NewBuildGUI '/some/path/to/your/chosen/dir/here'
```

Note that the old `BuildGUI` also takes a left arg 0 for "run" and 1 for "dry run". Write out the files to a fresh directory, do a diff against the existing, and integrate manually in the rare cases that something changed. 

We don't envisage that this will need doing as part of the day-to-day documentation authoring process, but something that will be run once per major version release. 
