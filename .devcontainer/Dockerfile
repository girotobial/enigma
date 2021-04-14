FROM mcr.microsoft.com/vscode/devcontainers/python as python-base

ENV POETRY_VERSION=1.1.4 \
    POETRY_HOME="/home/vscode/.poetry/"

FROM python-base as builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    curl \
    build-essential

# install poetry - respects $POETRY_VERSION & $POETRY_HOME
USER vscode
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
ENV PATH="$POETRY_HOME/bin:$PATH"
