from pathlib import Path
import subprocess
import sys
import time
from datetime import datetime


# =====================================
# Project Root
# =====================================

PROJECT_ROOT = Path(__file__).resolve().parent

# =====================================
# Update Tasks
# =====================================

TASKS = [
    (
        "Investing Download",
        PROJECT_ROOT / "invest_download_history.py"
    ),
    (
        "Make 4H Data",
        PROJECT_ROOT / "invest_make4Hdata.py"
    ),
    (
        "Analysis Engine",
        PROJECT_ROOT / "analysis_engine.py"
    ),
    (
        "Summary Report",
        PROJECT_ROOT / "report" / "summary_report.py"
    ),
]


# =====================================
# Execute Task
# =====================================

def run_task(name, script):

    print()
    print("=" * 60)
    print(name)
    print(script)
    print("=" * 60)

    start = time.time()

    result = subprocess.run(
        [
            sys.executable,
            str(script)
        ],
        cwd=PROJECT_ROOT
    )

    elapsed = time.time() - start


    if result.returncode != 0:

        print()
        print("=" * 60)
        print("ERROR")
        print(name)
        print(f"TIME : {elapsed:.1f} sec")
        print("=" * 60)

        return False


    print()
    print("OK")
    print(f"TIME : {elapsed:.1f} sec")

    return True



# =====================================
# Main
# =====================================

def main():

    print()
    print("=" * 60)
    print("BambooSage UPDATE START")
    print(datetime.now())
    print("=" * 60)


    for name, script in TASKS:

        if not script.exists():

            print()
            print("FILE NOT FOUND")
            print(script)

            return


        success = run_task(
            name,
            script
        )


        if not success:

            print()
            print("=" * 60)
            print("UPDATE STOPPED")
            print("=" * 60)

            return


    print()
    print("=" * 60)
    print("BambooSage UPDATE COMPLETE")
    print(datetime.now())
    print("=" * 60)



if __name__ == "__main__":
    main()