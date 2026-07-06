from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(ROOT / "solution"))

from solve import main


def run_reference_pipeline():
    main()


if __name__ == "__main__":
    run_reference_pipeline()