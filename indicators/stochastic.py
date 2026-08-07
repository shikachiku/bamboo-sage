from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(PROJECT_ROOT)
    )


import pandas as pd



# ===================================
# Parameter
# ===================================

INDICATOR = "stochastic"


# TradingView setting
LENGTH = 5

SMOOTH_K = 5

SMOOTH_D = 3



# ===================================
# Stochastic Calculation
# ===================================

def calculate(data):

    result = data.copy()

    high = result["High"]
    low = result["Low"]
    close = result["Close"]

    # ===================================
    # Lowest / Highest
    # ===================================

    lowest_low = (
        low
        .rolling(LENGTH)
        .min()
    )

    highest_high = (
        high
        .rolling(LENGTH)
        .max()
    )

    # ===================================
    # Raw %K
    # ===================================

    price_range = (
        highest_high
        -
        lowest_low
    )

    raw_k = (
        (
            close
            -
            lowest_low
        )
        /
        price_range
    ) * 100

    raw_k = raw_k.fillna(0)

    # ===================================
    # Smooth K
    # ===================================

    stoch_k = (
        raw_k
        .rolling(SMOOTH_K)
        .mean()
    )

    # ===================================
    # Smooth D
    # ===================================

    stoch_d = (
        stoch_k
        .rolling(SMOOTH_D)
        .mean()
    )

    result["STOCH_K"] = stoch_k

    result["STOCH_D"] = stoch_d

    # ===================================
    # State
    # ===================================

    result["STOCH_STATE"] = (
        pd.Series(
            "DOWN",
            index=result.index,
        )
    )

    result.loc[
        stoch_k > stoch_d,
        "STOCH_STATE"
    ] = "UP"

    # ===================================
    # Cross
    # ===================================

    cross = (
        ["NONE"]
        *
        len(result)
    )

    k_values = stoch_k.values

    d_values = stoch_d.values

    for i in range(1, len(result)):

        k_prev = k_values[i - 1]

        d_prev = d_values[i - 1]

        k_now = k_values[i]

        d_now = d_values[i]

        if (
            pd.isna(k_prev)
            or
            pd.isna(d_prev)
            or
            pd.isna(k_now)
            or
            pd.isna(d_now)
        ):

            continue

        # -----------------------------------
        # Golden Cross
        # -----------------------------------

        if (
            k_now > d_now
            and
            k_prev <= d_prev
        ):

            cross[i] = "GOLDEN"

        # -----------------------------------
        # Dead Cross
        # -----------------------------------

        elif (
            k_now < d_now
            and
            k_prev >= d_prev
        ):

            cross[i] = "DEAD"

    result["STOCH_CROSS"] = cross

    # ===================================
    # Zone
    # ===================================

    zone = []

    for value in k_values:

        if pd.isna(value):

            zone.append("MIDDLE")

        elif value >= 80:

            zone.append("OVERBOUGHT")

        elif value <= 20:

            zone.append("OVERSOLD")

        else:

            zone.append("MIDDLE")

    result["STOCH_ZONE"] = zone

    # ===================================
    # Wave State
    #
    # Initial:
    #
    # GOLDEN
    #   ↓
    # K >= 80
    #   ↓
    # SLOW >= 80
    #   ↓
    # WAVE CONFIRMED
    #
    # After confirmation:
    #
    # Pullback
    #   ↓
    # GOLDEN
    #   ↓
    # BUY
    #   ↓
    # K >= 80
    #   ↓
    # Continue
    #
    # K < 80
    #   ↓
    # DEAD
    #   ↓
    # BREAK
    # ===================================

    wave_state = []

    wave_break = []

    high_touch = []

    buy_signal = []

    # ===================================
    # State Variables
    # ===================================

    wave_active = False

    initial_waiting = False

    initial_k_touch = False

    initial_slow_touch = False

    pullback = False

    waiting_high = False

    # ===================================
    # Main State Machine
    # ===================================

    for i in range(len(result)):

        k = k_values[i]

        slow = d_values[i]

        signal = cross[i]

        current_state = "NONE"

        current_break = False

        current_buy = False

        # ===================================
        # Invalid Data
        # ===================================

        if (
            pd.isna(k)
            or
            pd.isna(slow)
        ):

            wave_state.append(
                current_state
            )

            wave_break.append(False)

            high_touch.append(False)

            buy_signal.append(False)

            continue

        # ===================================
        # Initial Wave
        # ===================================

        if not wave_active:

            # --------------------------------
            # Golden Cross starts Wave check
            # --------------------------------

            if signal == "GOLDEN":

                initial_waiting = True

                initial_k_touch = False

                initial_slow_touch = False

            # --------------------------------
            # Waiting for K / SLOW 80
            # --------------------------------

            if initial_waiting:

                if k >= 80:

                    initial_k_touch = True

                if slow >= 80:

                    initial_slow_touch = True

                # --------------------------------
                # Initial Wave Confirmed
                # --------------------------------

                if (
                    initial_k_touch
                    and
                    initial_slow_touch
                ):

                    wave_active = True

                    initial_waiting = False

                    initial_k_touch = False

                    initial_slow_touch = False

                    pullback = False

                    waiting_high = False

                    current_state = (
                        "WAVE_CONFIRMED"
                    )

                else:

                    current_state = (
                        "WAIT_WAVE"
                    )

            else:

                current_state = "NONE"

        # ===================================
        # Active Wave
        # ===================================

        else:

            # =================================
            # Normal Active State
            # =================================

            if not pullback and not waiting_high:

                # --------------------------------
                # K below 80 = Pullback
                # --------------------------------

                if k < 80:

                    pullback = True

                    current_state = (
                        "PULLBACK"
                    )

                else:

                    current_state = (
                        "WAVE_ACTIVE"
                    )

            # =================================
            # Pullback
            # =================================

            elif pullback:

                current_state = (
                    "PULLBACK"
                )

                # --------------------------------
                # Golden Cross after Pullback
                # --------------------------------

                if signal == "GOLDEN":

                    current_buy = True

                    pullback = False

                    waiting_high = True

                    current_state = "BUY"

            # =================================
            # After BUY
            # Waiting for K >= 80
            # =================================

            elif waiting_high:

                # --------------------------------
                # K returns to 80
                # --------------------------------

                if k >= 80:

                    waiting_high = False

                    current_state = (
                        "WAVE_CONTINUE"
                    )

                # --------------------------------
                # DEAD before K returns to 80
                # --------------------------------

                elif signal == "DEAD":

                    wave_active = False

                    initial_waiting = False

                    initial_k_touch = False

                    initial_slow_touch = False

                    pullback = False

                    waiting_high = False

                    current_break = True

                    current_state = "BREAK"

                else:

                    current_state = (
                        "WAIT_HIGH"
                    )

        # ===================================
        # Output
        # ===================================

        wave_state.append(
            current_state
        )

        wave_break.append(
            current_break
        )

        high_touch.append(
            k >= 80
        )

        buy_signal.append(
            current_buy
        )

    # ===================================
    # Result Columns
    # ===================================

    result["STOCH_HIGH_TOUCH"] = (
        high_touch
    )

    result["STOCH_WAVE_BREAK"] = (
        wave_break
    )

    result["STOCH_WAVE_STATE"] = (
        wave_state
    )

    result["STOCH_BUY"] = (
        buy_signal
    )

    return result