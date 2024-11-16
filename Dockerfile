# Use a Debian Slim base image
FROM python:3.8-slim-buster AS base

LABEL maintainer="Deep Dev dev@thedeep.io"

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /code

# Copy Poetry configuration files
COPY pyproject.toml poetry.lock /code/

# Basic System Setup
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends \
        iproute2 git vim \
        procps \
        wait-for-it binutils gdal-bin \
    && rm -rf /var/lib/apt/lists/*

# Install build tools and necessary libraries
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends \
        # Build essential packages
        gcc libc-dev libproj-dev \
        # WeasyPrint and Image processing requirements
        build-essential \
        libcairo2-dev \
        libpango1.0-dev \
        libgdk-pixbuf2.0-dev \
        libffi-dev \
        libjpeg-dev \
        zlib1g-dev \
        libfreetype6-dev \
        liblcms2-dev \
        libopenjp2-7-dev \
        libtiff5-dev \
        tk-dev \
        tcl-dev \
        ghostscript \
        poppler-utils \
        fontconfig \
        fonts-freefont-ttf \
        fonts-dejavu-core \
        fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Poetry for Python dependencies
RUN pip install --upgrade --no-cache-dir pip poetry \
    && poetry --version

# Configure Poetry to use the system environment
RUN poetry config virtualenvs.create false

# Install Python dependencies from Poetry
RUN poetry install --no-root

# Clean-up unnecessary build tools
RUN apt-get remove -y gcc libc-dev libproj-dev \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Install WeasyPrint via pip
RUN pip install weasyprint

# -------------------------- WEB ---------------------------------------
FROM base AS web

# Copy the project files
COPY . /code/


# -------------------------- WORKER ---------------------------------------
FROM base AS worker

# Additional installation for worker requirements
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends \
        libreoffice \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Copy the project files
COPY . /code/

