# Stage 1: Build
FROM python:3.12.4-slim-bullseye AS build

# Set environment variables to ensure poetry installs to the right location
ENV PIP_DEFAULT_TIMEOUT=1000
# Allow statements and log messages to immediately appear
ENV PYTHONUNBUFFERED=1
# prevents python creating .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

ENV POETRY_VERSION=1.7.1
# make poetry install to this location
ENV POETRY_HOME="/opt/poetry"
# make poetry create the virtual environment in the project's root it gets named `.venv`
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV POETRY_VIRTUALENVS_CREATE=1


# Set the working directory in the container
WORKDIR /usr/src/app

# Copy dependencies
COPY pyproject.toml poetry.lock ./

# install poetry and it's packages
RUN python -m venv $POETRY_HOME \
    && $POETRY_HOME/bin/pip install poetry==$POETRY_VERSION  \
    && $POETRY_HOME/bin/poetry install --only main  --no-root --no-ansi --no-interaction

# Stage 2: Runtime
FROM python:3.12.4-slim-bullseye AS runtime

RUN apt-get update && apt upgrade -y


# Set the working directory
WORKDIR /usr/src/app

# Set environment variables for the virtual environment
ENV VIRTUAL_ENV=/usr/src/app/.venv
ENV PATH="/usr/src/app/.venv/bin:$PATH"

# Copy the virtual environment from the build stage
COPY --from=build /usr/src/app/.venv /usr/src/app/.venv

# Copy the application code from the build stage
COPY . /usr/src/app

# Run the application
CMD ["python", "main.py"]
