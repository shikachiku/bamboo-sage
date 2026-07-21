from pathlib import Path

import pandas as pd

from folder_manager import RAW_DIR

from color import title


FILES = {
    "60": RAW_DIR / "60.csv",
    "1D": RAW_DIR / "1D.csv",
    "1W": RAW_DIR / "1W.csv",
    "1M": RAW_DIR / "1M.csv",
}


def load(path):

    return pd.read_csv(
        path,
        index_col=0,
        parse_dates=True,
    )
def basic_check(df):

    duplicated = df.index.duplicated().sum()

    rows = len(df)

    last = df.index.max()

    return rows, duplicated, last

def check_interval(df, freq):

    idx = df.index.sort_values()

    missing = []

    for i in range(len(idx) - 1):

        now = idx[i]

        nxt = idx[i + 1]

        expect = now + freq

        while expect < nxt:

            missing.append(expect)

            expect += freq

    return missing


def check_60():

    title("Check 60min")

    df = load(FILES["60"])

    miss = check_interval(
        df,
        pd.Timedelta(hours=1),
    )

    return miss
def check_daily():

    title("Check Daily")

    df = load(FILES["1D"])

    rows, duplicated, last = basic_check(df)

    idx = df.index.sort_values()

    missing = []

    for i in range(len(idx) - 1):

        now = idx[i]

        nxt = idx[i + 1]

        diff = (nxt - now).days

        if diff > 7 and now.year >= 2026:

            missing.append(
                (
                    now,
                    nxt,
                    diff,
                )
            )

    print(f"Rows      : {rows}")
    print(f"Last Bar  : {last}")
    print(f"Duplicate : {duplicated}")

    if duplicated > 0:

        print(f"Duplicate : {duplicated}")

    if len(missing) == 0 and duplicated == 0:

        print("Status    : OK")

    else:

        if len(missing) > 0:

            print(f"Missing : {len(missing)}")

            for m in missing:

                print(m)

    print()

    return (
        len(missing) == 0
        and duplicated == 0
    )


def check_weekly():

    title("Check Weekly")

    df = load(FILES["1W"])

    rows, duplicated, last = basic_check(df)

    idx = df.index.sort_values()

    missing = []

    for i in range(len(idx) - 1):

        now = idx[i]

        nxt = idx[i + 1]

        diff = (nxt - now).days

        if diff > 10:

            missing.append(
                (
                    now,
                    nxt,
                    diff,
                )
            )

    print(f"Rows      : {rows}")
    print(f"Last Bar  : {last}")
    print(f"Duplicate : {duplicated}")

    if duplicated > 0:

        print(f"Duplicate : {duplicated}")

    if len(missing) == 0 and duplicated == 0:

        print("Status    : OK")

    else:

        if len(missing) > 0:

            print(f"Missing : {len(missing)}")

            for m in missing:

                print(m)

    print()

    return (
        len(missing) == 0
        and duplicated == 0
    )

def check_monthly():

    title("Check Monthly")

    df = load(FILES["1M"])

    rows, duplicated, last = basic_check(df)

    idx = df.index.sort_values()

    missing = []

    for i in range(len(idx) - 1):

        now = idx[i]

        nxt = idx[i + 1]

        diff = (nxt - now).days

        if diff > 40:

            missing.append(
                (
                    now,
                    nxt,
                    diff,
                )
            )

    print(f"Rows      : {rows}")
    print(f"Last Bar  : {last}")
    print(f"Duplicate : {duplicated}")

    if duplicated > 0:

        print(f"Duplicate : {duplicated}")

    if len(missing) == 0 and duplicated == 0:

        print("Status    : OK")

    else:

        if len(missing) > 0:

            print(f"Missing : {len(missing)}")

            for m in missing:

                print(m)

    print()

    return (
        len(missing) == 0
        and duplicated == 0
    )


if __name__ == "__main__":

    print()

    print("=" * 60)
    print("DATA CHECK START")
    print("=" * 60)

    result60 = check_60()
    result1d = check_daily()
    result1w = check_weekly()
    result1m = check_monthly()

    all_ok = (
        result60
        and result1d
        and result1w
        and result1m
    )

    print("=" * 60)

    if all_ok:

        print("ALL DATA OK")

    else:

        print("DATA ERROR FOUND")

    print("=" * 60)

    title("DATA CHECK COMPLETED")

