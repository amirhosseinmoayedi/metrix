import os
import shutil

import uvicorn
from loguru import logger

from app.gunicorn_web_server import GunicornApplication
from app.settings import settings


def set_multiproc_dir() -> None:
    """
    Sets mutiproc_dir env variable.

    This function cleans up the multiprocess directory
    and recreates it. This actions are required by prometheus-client
    to share metrics between processes.

    After cleanup, it set variable.
    """
    shutil.rmtree(settings.prometheus_dir, ignore_errors=True)
    os.makedirs(settings.prometheus_dir, exist_ok=True)
    os.environ["PROMETHEUS_MULTIPROC_DIR"] = str(
        settings.prometheus_dir.expanduser().absolute(),
    )


@logger.catch
def main() -> None:
    """Entrypoint of the application."""
    set_multiproc_dir()
    if settings.reload:
        uvicorn.run(
            "app.presentation.application:get_app",
            host=settings.host,
            port=settings.port,
            workers=settings.workers_count,
            reload=settings.reload,
            log_level=settings.log_level.value.lower(),
            factory=True,
        )
    else:
        # We choose gunicorn only if reload
        # option is not used, because reload
        # feature doen't work with Uvicorn workers.
        GunicornApplication(
            "app.presentation.application:get_app",
            host=settings.host,
            port=settings.port,
            workers=settings.workers_count,
            factory=True,
            accesslog="-",
            loglevel=settings.log_level.value.lower(),
        ).run()


if __name__ == "__main__":
    main()
