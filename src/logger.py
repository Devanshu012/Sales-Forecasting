import logging
import os
import sys
from datetime import datetime


def setup_logging(log_level: int = logging.INFO, log_dir: str = None) -> None:
    """
    Configure the root logger for the project.

    Call this once at the entry point of each notebook or script.
    Handlers are cleared on every call so re-running a notebook cell
    does not duplicate log lines.
    """
    fmt = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(fmt, datefmt=datefmt)

    root = logging.getLogger()
    root.setLevel(log_level)
    root.handlers.clear()

    # Console — use stdout so Jupyter shows output inline
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)
    root.addHandler(console)

    # Optional rotating file handler
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(
            log_dir,
            f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        )
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        root.addHandler(file_handler)
        logging.getLogger(__name__).info("Logging to file: %s", log_file)
