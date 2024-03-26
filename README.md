# Tools

The `tools/` directory contains a `docker compose` configuration that can be used to preview our documentation documents in their rendered form.

## Local preview

When working on a document, you can render the mkdocs site locally either directly (requires an up-to-date Python
installation -- if you wish to run it this way, talk to Stefan), or using the provided `docker compose` configuration (requires a running [Docker installation](https://docs.docker.com/desktop/install/windows-install/)):

1. Tell Docker which site you wish to render. Note: this needs to be an absolute path, for example:
    ```
    export DOCS_DIR=/Users/stefan/work/dyalog-docs/documentation/windows-installation-and-configuration
    ```
   or in Powershell,
    ```
    $env:DOCS_DIR="C:{YOUR PATH HERE}\dyalog-docs\documentation\windows-installation-and-configuration"
    ```
2. In the directory containing the `Dockerfile`, start `docker-compose`:
    ```
    docker-compose up
    ```
   First time you run this it might take a minute or two; subsequent runs should be quicker. Note: if you ever wish to
   rebuild the Docker image, append `--build` to the `docker-compose` command.
3. Open a web browser on `http://0.0.0.0:8000/` -- note that this is an `http` site, so your browser may complain about that.
4. Once you're done, terminate the docker stack:
    ```
    docker-compose down
   ```

## Running Docker on Windows

To run `docker-compose up` on Windows, you'll need to have `Docker Desktop` for Windows installed and
running. `Docker Desktop` includes both `Docker` and `Docker Compose`.

**Install Docker Desktop for Windows**

1. Download and run the [Docker Desktop installer](https://docs.docker.com/desktop/install/windows-install/) and follow
   the prompts to complete the installation.
2. `Docker Desktop` will require you to enable the [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install) feature
   and install a Linux kernel update package if you're on Windows 10. Follow the installation guide provided by
   the `Docker` installer.
3. After installation, run Docker Desktop. You might need to log in with your Docker account.

**Open a terminal**

1. You can use either Command Prompt (cmd) or PowerShell to run Docker commands on Windows.
2. Use the `cd` command to go to the directory containing the `docker-compose.yml` file.
3. Run `docker-compose up`. This command reads the docker-compose.yml file in the current directory, builds the images
   if they don't exist, and starts the containers as specified in the file.
4. If you've made changes to your Dockerfile or Docker Compose configuration and want to rebuild the images, you can
   use `docker-compose up --build`.