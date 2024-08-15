# Template for Fastapi projects

TODOs:
- [ ] connection handling for repositories
- [ ] create a schema with mermaid to show a structure as whole
- [ ] fix mypy in github-ci
- [ ] fix pytest in github-ci
- [ ] fix integration with test case and pytest

TODO(maybe):

- Paginator
- caching
- admin panel
- soft delete

## start project

requirements:

- need python version 3.12+
- need [poetry](https://python-poetry.org/) version 1.7.1+

### Docker

to start the project quickly:

```bash
docker compose up -d --build backend
```

### if you have a Windows machine need to copy this into the begging of the main.py module

```python
import asyncio

if hasattr(asyncio, 'WindowsSelectorEventLoopPolicy'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def set_multiproc_dir() -> None:
    ...
```

### command will install main packages with packages used for development.

```bash
poetry install --with dev
```

### before any commit please run this

```bash
pre-commit install --hook-type commit-msg --hook-type pre-push
```

### running linter manually ([Ruff](https://docs.astral.sh/ruff/linter/))

```bash
poetry run ruff check                  # Lint all files in the current directory.
poetry run ruff check --fix
```

### running formatter manually ([black](https://black.readthedocs.io/en/stable/))

```bash
poetry run black . 
```

#### project uses mypy see the typehint [cheatsheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html)

running mypy manually

```bash
poetry run mypy .
```

## increase the project version via [commitizen](https://commitizen-tools.github.io/commitizen/commands/bump/)

```bash
cz bump
cz bump --check-consistency # Check if the version in your configuration file matches the latest tag.
cz bump --increment minor #  Manually specify the version increment (patch, minor, major).
git push && git push --tags #  Push the changes and the new tag to your repository.
```

## App setting([pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/))

for local development create a `.env` file in the root directory and add the variables from .`.env.sample` file
in `app/settings.py` you can find the settings for the app if you want to change the default value for them
also you can add prefix for variable used in `.env` in code blow.

```python
model_config = SettingsConfigDict(
    env_file=".env",
    env_prefix="",  # change here
    env_file_encoding="utf-8",
)
```

### Adding logger
the `loguru` package is used for logging in the project. you can add a logger in the module like this:
```python
from loguru import logger

def filter_dummy_logs(record: dict) -> bool:
    ...

def configure_logging() -> None:  # pragma: no cover
    ...
    # add other loggers to use in the project
    logger.add("dummy_error.log", level="ERROR", filter=filter_dummy_logs) # add your handler like this in here
```
and to use them 
```python
from loguru import logger

logger.bind(type="DUMMY").error("Dummy error") # bind for specifying handler
```

### running tests
```bash
poetry run pytest
```