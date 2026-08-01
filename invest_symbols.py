import csv


def load_investing_symbols(
    filename="invest_symbols.csv"
):

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


if __name__ == "__main__":

    symbols = load_investing_symbols()


    for symbol in symbols:

        print(
            symbol["Folder"],
            symbol["Investing"],
            symbol["Name"],
        )