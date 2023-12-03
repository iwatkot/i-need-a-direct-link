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


logger = Logger(__name__)

UPLOADS_DIR = os.path.join(PARENT_DIR, "uploads")
os.makedirs(UPLOADS_DIR, exist_ok=True)

MAX_FILE_SIZE = 50000000
MAX_FILE_SIZE_MB = f"{MAX_FILE_SIZE / 1000000} MB"

IDS_FILEPATH = os.path.join(PARENT_DIR, "file_ids.json")
if not os.path.isfile(IDS_FILEPATH):
    logger.info(f"Can't find {IDS_FILEPATH}. Creating new file...")
    with open(IDS_FILEPATH, "w") as f:
        json.dump({}, f, indent=4)
    logger.info(f"Created {IDS_FILEPATH} successfully.")
else:
    logger.info(f"Found {IDS_FILEPATH} successfully.")


def get_file_number() -> str:
    """Get the next file number for the filename.

    Returns:
        str: next file number
    """
    files = os.listdir(UPLOADS_DIR) or []
    file_number = len(files) + 1
    logger.info(f"Next file number is {file_number}.")
    return str(file_number).zfill(5)


def save_file_id(filename: str):
    """Save file_id to ids.json.

    Args:
        filename (str): filename of the file

    Returns:
        str: file_id of the file
    """
    file_id = str(uuid.uuid4())
    logger.info(f"Generated file_id: {file_id}.")

    with open(IDS_FILEPATH, "r") as f:
        data = json.load(f)
    data[file_id] = filename
    with open(IDS_FILEPATH, "w") as f:
        json.dump(data, f, indent=4)

    logger.info(f"Saved file_id: {file_id} to {IDS_FILEPATH}.")
    return file_id


def delete_file_id(file_id: str) -> bool:
    """Delete file from uploads directory and delete file_id from ids.json.
    Return True if file was deleted, False if file was not deleted.

    Args:
        file_id (str): unique uuid4 string of the file

    Returns:
        bool: True if file was deleted, False if file was not deleted
    """
    logger.info(f"Deleting file with file_id: {file_id}...")
    with open(IDS_FILEPATH, "r") as f:
        data = json.load(f)

    filename = data.pop(file_id)
    logger.info(f"Filename of file_id: {file_id} is {filename}.")
    if filename:
        try:
            os.remove(os.path.join(UPLOADS_DIR, filename))
        except OSError:
            pass
        with open(IDS_FILEPATH, "w") as f:
            json.dump(data, f, indent=4)

        logger.info(f"Deleted file with file_id: {file_id} successfully.")
        return True
    logger.info(f"File with file_id: {file_id} was not deleted.")
    return False
