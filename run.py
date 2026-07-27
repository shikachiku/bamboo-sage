from indicators.heikin_ashi import main as heikin_ashi_main
from indicators.adx import main as adx_main
from indicators.highlow import main as highlow_main
from indicators.highlow5 import main as highlow5_main

from indicators.adx_profile import main as adx_profile_main
from indicators.highlow_profile import main as highlow_profile_main
from indicators.highlow5_profile import main as highlow5_profile_main

from indicators.history import main as history_main
from indicators.master import main as master_main
from indicators.strategy import main as strategy_main


def main():

    print("\n==============================")
    print(" Bamboo Sage")
    print("==============================")

    print("\n[1] Heikin Ashi")
    heikin_ashi_main()

    print("\n[2] ADX")
    adx_main()

    print("\n[3] High Low")
    highlow_main()

    print("\n[4] High Low5")
    highlow5_main()

    print("\n[5] ADX Profile")
    adx_profile_main()

    print("\n[6] HighLow Profile")
    highlow_profile_main()

    print("\n[7] HighLow5 Profile")
    highlow5_profile_main()

    print("\n[8] History")
    history_main()

    print("\n[9] MASTER")
    master_main()

    print("\n[10] STRATEGY")
    strategy_main()

    print("\n==============================")
    print(" Bamboo Sage Complete")
    print("==============================")


if __name__ == "__main__":
    main()