import csv


def load_symbols(filename="symbols.csv"):

    symbols = []

    with open(
        filename,
        newline="",
        encoding="utf-8",
    ) as f:

        reader = csv.DictReader(f)

        for row in reader:

            if row["Enable"] == "1":

                symbols.append(row)

    return symbols
