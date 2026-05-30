# common/logger.py

import logging
import sys
from pathlib import Path
from datetime import datetime

# Для корректных цветов в Windows
try:
    from colorama import just_fix_windows_console
    just_fix_windows_console()
except ImportError:
    pass

# Создаем папку logs
Path("logs").mkdir(exist_ok=True)

# Новый лог-файл при каждом запуске
log_file = f"logs/internal_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"


class ColoredFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[36m",      # Cyan
        "INFO": "\033[32m",       # Green
        "WARNING": "\033[33m",    # Yellow
        "ERROR": "\033[31m",      # Red
        "CRITICAL": "\033[41m",   # Red background
    }

    RESET = "\033[0m"

    def format(self, record):
        original = record.levelname

        color = self.COLORS.get(record.levelname, "")
        record.levelname = f"{color}{record.levelname.lower()}{self.RESET}"

        result = super().format(record)

        record.levelname = original
        return result


class PlainFormatter(logging.Formatter):
    def format(self, record):
        original = record.levelname

        record.levelname = record.levelname.lower()

        result = super().format(record)

        record.levelname = original
        return result


logger = logging.getLogger("internal")
logger.setLevel(logging.DEBUG)
logger.propagate = False

if not logger.handlers:

    # Цветной вывод в консоль
    console_formatter = ColoredFormatter(
        "%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y/%m/%d %H:%M:%S"
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # Обычный вывод в файл
    file_formatter = PlainFormatter(
        "%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y/%m/%d %H:%M:%S"
    )

    file_handler = logging.FileHandler(
        log_file,
        encoding="utf-8"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Перехватываем логи uvicorn / fastapi
    for name in (
        "uvicorn",
        "uvicorn.error",
        "uvicorn.access",
        "fastapi"
    ):
        uv_logger = logging.getLogger(name)
        uv_logger.handlers.clear()
        uv_logger.handlers.extend(logger.handlers)
        uv_logger.setLevel(logging.DEBUG)
        uv_logger.propagate = False