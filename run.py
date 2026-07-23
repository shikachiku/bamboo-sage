import subprocess
import sys

scripts = [

    "indicators/heikin_ashi.py",

    "indicators/adx.py",

    "indicators/highlow.py",

    "indicators/highlow5.py",

    "indicators/adx_profile.py",

    "indicators/highlow_profile.py",

    "indicators/highlow5_profile.py",

    "indicators/history.py",

    "indicators/master.py",

    "indicators/strategy.py",

]

print()
print("===================================")
print(" Bamboo Sage")
print("===================================")
print()

for script in scripts:

    print("-----------------------------------")
    print(script)
    print("-----------------------------------")

    result = subprocess.run(
        [sys.executable, script]
    )

    if result.returncode != 0:

        print()
        print(f"ERROR : {script}")
        sys.exit(1)

print()
print("===================================")
print(" Bamboo Sage Complete")
print("===================================")