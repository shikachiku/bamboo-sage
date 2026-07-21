import time
import subprocess
import sys
import os
from logger import log
from pathlib import Path

from color import title

from config import SYMBOL

from folder_manager import (
    RAW_DIR,
    LIVE_DIR,
)

from merge_update import (
    load_existing,
    save,
    get_last_datetime,
    calculate_missing_bars,
    merge_data,
    history_too_old,
    has_new_data,
)

from tv_update import (
    download_from_tv,
)

from tv_dataframe import (
    tv_to_dataframe,
)


TIMEFRAMES = [
    "60",
    "1D",
    "1W",
    "1M",
]


def update_one(timeframe):
    
    start = time.perf_counter()

    raw_file = RAW_DIR / f"{timeframe}.csv"
    live_file = LIVE_DIR / f"{timeframe}.csv"

    old_df = load_existing(raw_file)

    last_datetime = get_last_datetime(old_df)

    if last_datetime is None:

        print("No existing history")

    else:

        print("Last history :", last_datetime)

    # 履歴が古い場合はフルダウンロード
    if history_too_old(
        timeframe,
        last_datetime,
    ):

        print("History too old -> Full Download")

        subprocess.run(
            [
                sys.executable,
                "download_history.py",
            ]
        )

        old_df = load_existing(raw_file)

        last_datetime = get_last_datetime(old_df)

    bars = calculate_missing_bars(
        timeframe,
        last_datetime,
    )

    print("Request bars :", bars)

    try:

        title(f"{timeframe} Update Start")
        log(f"{timeframe} Update Start")




        for attempt in range(3):

            try:

                message = download_from_tv(
                    timeframe,
                    bars,
                )

                break

            except TimeoutError:

                print(
                    f"Reconnect {attempt + 1}/3"
                )

                log(
                    f"{timeframe} Reconnect {attempt + 1}/3"
                )

                if attempt == 2:
                    raise

        new_df = tv_to_dataframe(
            message
        )

        if has_new_data(
            old_df,
            new_df,
        ):

            merged = merge_data(
                old_df,
                new_df,
            )

            save(
                merged,
                raw_file,
            )

            save(
                merged,
                live_file,
            )

            print("CSV Updated")
            log(f"{timeframe} CSV Updated")

        else:

            print("No Update")
            log(f"{timeframe} No Update")

        title(f"{timeframe} Update Finished")

    except Exception as e:

        print()
        print("UPDATE ERROR")
        print(e)
        log(f"{timeframe} ERROR : {e}")

    finally:

        elapsed = time.perf_counter() - start

        print(
            f"Elapsed : {elapsed:.2f} sec"
        )

        log(
            f"{timeframe} Elapsed : {elapsed:.2f} sec"
        )

        title(f"{timeframe} Disconnected")


def main():

    print()
    print("=" * 60)
    print("UPDATE ENGINE START")
    print("=" * 60)
    log("========================================")
    log("UPDATE ENGINE START")
    log("========================================")

    for tf in TIMEFRAMES:

        print()
        print("-" * 60)
        print(f"{tf} Updating")
        print("-" * 60)

        update_one(tf)

    print()
    print("=" * 40)
    print("UPDATE ENGINE COMPLETED")
    log("UPDATE ENGINE COMPLETED")
    print("=" * 40)

    print()
    print("Running Data Checker...")
    log("Running Data Checker...")

    os.system(
        f"{sys.executable} data_checker.py"
    )

if __name__ == "__main__":

    main()