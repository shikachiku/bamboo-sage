

def judge_strategy(month_trend, week_trend, day_trend, position):

    strategy = "待機"
    reasons = []

    if month_trend == "青継続":
        reasons.append("✓ 月足 青継続")

    if week_trend.startswith("赤"):
        reasons.append("✓ 週足 赤継続")

    if day_trend.startswith("赤"):
        reasons.append("✓ 日足 赤継続")

    if position == "LOW":
        reasons.append("✓ Low5MAより下")

    if month_trend == "青継続":
        if week_trend.startswith("赤"):
            if day_trend.startswith("赤"):
                strategy = "押し目待ち"

    if month_trend == "青継続":
        if week_trend.startswith("青"):
            if day_trend == "青転":
                strategy = "買い準備"

    if month_trend.startswith("赤"):
        strategy = "利益確定警戒"

    return strategy, reasons
