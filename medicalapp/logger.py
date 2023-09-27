import logging

logger = logging.getLogger("medicalapp")

stream_handler = logging.StreamHandler()
file_handler = logging.FileHandler("./logs/error.log")
stream_handler.setLevel(logging.DEBUG)
file_handler.setLevel(logging.DEBUG)

stream_format = logging.Formatter(
    "%(name)s - %(asctime)s - %(levelname)s - %(message)s"
)
file_format = logging.Formatter("%(name)s - %(asctime)s - %(levelname)s - %(message)s")
stream_handler.setFormatter(stream_format)
file_handler.setFormatter(file_format)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)

logging.basicConfig(
    filename="./logs/error.log",
    level=logging.DEBUG,
    format="%(name)s - %(asctime)s - %(levelname)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
)
