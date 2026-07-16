

def judge_color(ha):

    colors = []

    for _, row in ha.iterrows():

        if row["HA_Close"] > row["HA_Open"]:
            colors.append("青")
        else:
            colors.append("赤")

    return colors

