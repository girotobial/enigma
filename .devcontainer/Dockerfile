FROM mcr.microsoft.com/vscode/devcontainers/python:3.9 as python-base

ENV POETRY_VERSION=1.1.12 \
    POETRY_HOME="/home/vscode/.poetry/"

FROM python-base as builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    curl \
    build-essential
RUN apt-get install gnupg

# install poetry - respects $POETRY_VERSION & $POETRY_HOME
USER vscode
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
ENV PATH="$POETRY_HOME/bin:$PATH"
