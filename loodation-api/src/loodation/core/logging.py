import logging


class InterceptHandler(logging.Handler):  # TODO: intercept uvicorn logs
    def emit(self, record):
        pass
