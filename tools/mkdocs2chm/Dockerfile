FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    libffi-dev \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    weasyprint \
    fpc \
    && rm -rf /var/lib/apt/lists/*

RUN pip install \
    mkdocs-material \
    mkdocs-macros-plugin \
    mkdocs-monorepo-plugin \
    mkdocs-site-urls \
    mkdocs-caption \
    beautifulsoup4 \
    markdown \
    ruamel.yaml \
    pygments \
    markdown-tables-extended \
    git+https://github.com/flywire/caption

# Set the working directory
WORKDIR /app

COPY mkdocs2chm/mkdocs2chm.py /usr/local/bin/mkdocs2chm.py
COPY mkdocs2chm/assets /opt/mkdocs2chm/assets

# Make the script executable
RUN chmod +x /usr/local/bin/mkdocs2chm.py

# Set the entrypoint to the script
ENTRYPOINT ["/usr/local/bin/mkdocs2chm.py"]