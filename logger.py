from pathlib import Path
from datetime import datetime


LOG_DIR = Path("logs")


def _today_log():

    LOG_DIR.mkdir(
        exist_ok=True
    )

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )

    return LOG_DIR / f"{today}.log"


def log(text):

    path = _today_log()

    timestamp = datetime.now().strftime(
        "%H:%M:%S"
    )

    line = f"[{timestamp}] {text}"

    with open(
        path,
        "a",
        encoding="utf-8",
    ) as f:

        f.write(
            line + "\n"
        )