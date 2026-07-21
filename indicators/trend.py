
def judge_trend(colors):

    trends = []

    for i, color in enumerate(colors):

        if i == 0:
            trends.append("開始")
            continue

        previous = colors[i - 1]

        if previous == "赤" and color == "青":
            trends.append("青転")

        elif previous == "青" and color == "赤":
            trends.append("赤転")

        elif color == "青":
            trends.append("青継続")

        else:
            trends.append("赤継続")

    return trends
