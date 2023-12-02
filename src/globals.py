import os
import json
import uuid
import logging
import sys
from datetime import datetime
from dotenv import load_dotenv

load_dotenv("key.env")
FLASK_KEY = os.getenv("FLASK_KEY")

LOG_FORMATTER = "%(name)s | %(asctime)s | %(levelname)s | %(message)s"
ABSOLUTE_PATH = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(ABSOLUTE_PATH)
LOG_DIR = os.path.join(PARENT_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

UPLOADS_DIR = os.path.join(PARENT_DIR, "uploads")
os.makedirs(UPLOADS_DIR, exist_ok=True)

IDS_FILEPATH = os.path.join(PARENT_DIR, "ids.json")
if not os.path.isfile(IDS_FILEPATH):
    with open(IDS_FILEPATH, "w") as f:
        json.dump({}, f, indent=4)


class Logger(logging.getLoggerClass()):
    def __init__(self, name: str):
        super().__init__(name)
        self.setLevel(logging.DEBUG)
        self.stdout_handler = logging.StreamHandler(sys.stdout)
        self.file_handler = logging.FileHandler(
            filename=self.log_file(), mode="a", encoding="utf-8"
        )
        self.fmt = LOG_FORMATTER
        self.stdout_handler.setFormatter(logging.Formatter(LOG_FORMATTER))
        self.file_handler.setFormatter(logging.Formatter(LOG_FORMATTER))
        self.addHandler(self.stdout_handler)
        self.addHandler(self.file_handler)

    def log_file(self):
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = os.path.join(LOG_DIR, f"{today}.txt")
        return log_file


def get_file_number() -> str:
    files = os.listdir(UPLOADS_DIR) or []
    file_number = len(files) + 1
    return str(file_number).zfill(5)


def generate_uuid():
    return str(uuid.uuid4())


def save_id(filename: str):
    file_id = generate_uuid()
    with open(IDS_FILEPATH, "r") as f:
        data = json.load(f)
    data[file_id] = filename
    with open(IDS_FILEPATH, "w") as f:
        json.dump(data, f, indent=4)

    return file_id


def delete_id(file_id: str):
    with open(IDS_FILEPATH, "r") as f:
        data = json.load(f)

    filename = data.pop(file_id)
    if filename:
        try:
            os.remove(os.path.join(UPLOADS_DIR, filename))
        except OSError:
            pass
        with open(IDS_FILEPATH, "w") as f:
            json.dump(data, f, indent=4)
