import logging

logging.basicConfig(level=logging.INFO)


def set_logger(name: str):
    """uvicornのログに合わせる"""
    if not name.startswith("uvicorn"):
        name = "uvicorn." + name
    logger = logging.getLogger(name=name)
    logger.info(f"Set logger {name}")
    return logger
