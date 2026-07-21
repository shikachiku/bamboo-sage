from pathlib import Path

from config import SYMBOL


BASE_DIR = Path("data")

# TradingViewシンボルをフォルダ名へ変換
DATA_NAME = SYMBOL.replace(":", "_")

SYMBOL_DIR = BASE_DIR / DATA_NAME

RAW_DIR = SYMBOL_DIR / "raw"
LIVE_DIR = SYMBOL_DIR / "live"
BACKTEST_DIR = SYMBOL_DIR / "backtest"


def create_data_folders():

    for folder in (
        RAW_DIR,
        LIVE_DIR,
        BACKTEST_DIR,
    ):
        folder.mkdir(
            parents=True,
            exist_ok=True,
        )


if __name__ == "__main__":

    create_data_folders()

    print("===================================")
    print("Data folders ready")
    print("SYMBOL    :", SYMBOL)
    print("DATA_NAME :", DATA_NAME)
    print(RAW_DIR)
    print(LIVE_DIR)
    print(BACKTEST_DIR)
    print("===================================")