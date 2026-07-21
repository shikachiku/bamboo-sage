# ========================================
# Bamboo Sage 共通設定
# ========================================

# TradingView
SYMBOL = "WHSELFINVEST:JAPAN225CFD"
TIMEFRAME = "60"

# ===== 取得する時間足 =====
TIMEFRAMES = [
    "1M",
    "1W",
    "1D",
    "240",
]
BAR_COUNT = 500

# ========================================
# 保存ファイル名（自動生成）
# ========================================

SYMBOL_NAME = SYMBOL.split(":")[1]
BROKER_NAME = SYMBOL.split(":")[0]

CSV_FILE = f"{SYMBOL_NAME}_{BROKER_NAME}_{TIMEFRAME}.csv"

# ===== ADX =====
ADX_PERIOD = 10
ADX_THRESHOLD = 5

# ===== MACD =====
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

# ===== Stochastic =====
STOCH_K = 14
STOCH_D = 3
STOCH_SLOW = 3

# ===== Moving Average =====
HIGH_MA = 5
LOW_MA = 5

# ===== 通知 =====
SHOW_LOG = True