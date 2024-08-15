import json
from typing import Any, Dict

from gunicorn.app.base import BaseApplication
from gunicorn.util import import_app
from gunicorn.glogging import Logger
from gunicorn.http.wsgi import Response
from gunicorn.http.message import Request
from uvicorn_worker import UvicornWorker as BaseUvicornWorker


class JSONLogger(Logger):
    """
    JSON logger for gunicorn.

    This class is used to log access logs in JSON format.
    """

    def access(self, resp: Response, req: Request, environ: Dict[str, Any], request_time: float):
        log_data = {
            "method": req.method,
            "path": req.path,
            "status": resp.status,
            "request_time": request_time,
            "client_ip": req.headers.get("X-Forwarded-For", req.remote_addr),
            "user_agent": req.headers.get("User-Agent"),
        }
        log_message = json.dumps(log_data)
        self.access_log.info(log_message)


class UvicornWorker(BaseUvicornWorker):
    """
    Configuration for uvicorn workers.

    This class is subclassing UvicornWorker and defines
    some parameters class-wide, because it's impossible,
    to pass these parameters through gunicorn.
    """

    CONFIG_KWARGS = {  # noqa: WPS115 (upper-case constant in a class)
        "loop": "asyncio",
        # Uses httptools for HTTP parsing, which is a high-performance HTTP parser.
        "http": "httptools",
        "lifespan": "on",
        # Enables the lifespan protocol,
        # which is used to manage the startup and shutdown of the application.
        "factory": True,  # Indicates that the application factory pattern is used.
        "proxy_headers": False,  # Disables the handling of proxy headers.
    }


class GunicornApplication(BaseApplication):
    """
    Custom gunicorn application.

    This class is used to start guncicorn
    with custom uvicorn workers.
    """

    def __init__(  # noqa: WPS211 (Too many args)
        self,
        app: str,
        host: str,
        port: int,
        workers: int,
        **kwargs: Any,
    ):
        self.options = {
            "bind": f"{host}:{port}",
            "workers": workers,
            "worker_class": "app.gunicorn_web_server.UvicornWorker",
            "logger_class": JSONLogger,
            **kwargs,
        }
        self.app = app
        super().__init__()

    def load_config(self) -> None:
        """
        Load config for web server.

        This function is used to set parameters to gunicorn
        main process. It only sets parameters that
        gunicorn can handle. If you pass unknown
        parameter to it, it crash with error.
        """
        for key, value in self.options.items():
            if key in self.cfg.settings and value is not None:
                self.cfg.set(key.lower(), value)

    def load(self) -> str:
        """
        Load actual application.

        Gunicorn loads application based on this
        function's returns. We return python's path to
        the app's factory.

        :returns: python path to app factory.
        """
        app: str = import_app(self.app)
        return app
