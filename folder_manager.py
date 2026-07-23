from pathlib import Path

from symbol_loader import load_symbols

BASE_DIR = Path("data")


def create_data_folders():

    symbols = load_symbols()

    for symbol in symbols:

        base = BASE_DIR / symbol["Folder"]

        (base / "raw").mkdir(
            parents=True,
            exist_ok=True,
        )

        (base / "live").mkdir(
            parents=True,
            exist_ok=True,
        )

        (base / "backtest").mkdir(
            parents=True,
            exist_ok=True,
        )


if __name__ == "__main__":

    create_data_folders()

    print("=" * 40)
    print("Folder Ready")
    print("=" * 40)