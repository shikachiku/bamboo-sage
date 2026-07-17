
def judge_strategy(month_trend, week_trend, day_trend):

    # 基本は待機
    strategy = "待機"

    # 最強パターン
    if month_trend == "青継続":
        if week_trend in ["青継続", "青転"]:
            if day_trend == "青転":
                strategy = "買い準備"

    # 押し目候補
    if month_trend == "青継続":
        if week_trend.startswith("赤"):
            if day_trend.startswith("赤"):
                strategy = "押し目待ち"

    # 利益確定警戒
    if month_trend.startswith("赤"):
        strategy = "利益確定警戒"

    return strategy
