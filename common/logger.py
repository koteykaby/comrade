import logging
from logging.handlers import RotatingFileHandler
import sys

logger = logging.getLogger("internal")
logger.setLevel(logging.DEBUG) 

formatter = logging.Formatter("[%(levelname)s:%(name)s.%(funcName)s]: %(message)s")

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

file_handler = RotatingFileHandler("logs/internal.log", maxBytes=5_000_000, backupCount=3)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)