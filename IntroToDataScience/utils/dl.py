from functools import lru_cache
from pathlib import Path
from time import time, sleep

# Local imports
from utils.config import config


def data_exists(filename: str) -> bool:
    data = Path(config.DATA_DIR)
    matches = list(data.glob(filename + "*"))
    if matches:
        return True
    else:
        return False


@lru_cache
def get_abs_path() -> str:
    path = Path(config.DATA_DIR)
    return str(path.absolute())


def file_count() -> int:
    path = Path(config.DATA_DIR)
    return len(list(path.glob("*")))


def wait_for_download(initial_file_count: int, timeout: int = 60):
    downloaded = False
    end_time = time() + timeout
    while not downloaded and time() < end_time:
        current_count = file_count()
        if current_count > initial_file_count:
            sleep(2)
            downloaded = True
        else:
            sleep(1)

    if not downloaded:
        raise TimeoutError("Download timed out! ({} secs)".format(timeout))
