from fastapi import FastAPI
from prometheus_fastapi_instrumentator.instrumentation import PrometheusFastApiInstrumentator


def setup_prometheus(app: FastAPI) -> None:
    """
    Enables prometheus integration.

    :param app: current application.
    """
    PrometheusFastApiInstrumentator(should_group_status_codes=False).instrument(
        app,
    ).expose(app, should_gzip=True, name="metrics")
