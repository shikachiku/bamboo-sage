

def judge_color(ha):

    colors = []

    for _, row in ha.iterrows():

        if row["HA_Close"] > row["HA_Open"]:
            colors.append("Blue")
        else:
            colors.append("Red")

    return colors

