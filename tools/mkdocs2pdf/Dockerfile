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
    beautifulsoup4 \
    markdown \
    ruamel.yaml \
    pygments \
    weasyprint \
    pymdown-extensions \
    markdown-tables-extended \
    git+https://github.com/flywire/caption

# Set the working directory
WORKDIR /app

COPY mkdocs2pdf/mkdocs2pdf.py /usr/local/bin/mkdocs2pdf.py
COPY mkdocs2pdf/assets /opt/mkdocs2pdf/assets

# Make the script executable
RUN chmod +x /usr/local/bin/mkdocs2pdf.py

# Set the entrypoint to the script
ENTRYPOINT ["/usr/local/bin/mkdocs2pdf.py"]