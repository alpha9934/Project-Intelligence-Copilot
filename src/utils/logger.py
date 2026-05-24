import logging
import sys

def setup_logger(name: str) -> logging.Logger:
    """
            Outputs structured logs to stdout so they can be captured by Docker/Kubernetes observability tools.
    """
    logger = logging.getLogger(name)
    
    # Prevent duplicate log entries if called multiple times
    if logger.hasHandlers():
        return logger

    # Set default level to INFO. (In a real production app, this could pull from config)
    logger.setLevel(logging.INFO)

    # Standard enterprise format: [Time] | [Level] | [Module] | Message
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console handler for containerized environments
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    
    return logger