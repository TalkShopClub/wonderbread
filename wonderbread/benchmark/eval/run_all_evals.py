#!/usr/bin/env python3
"""
Master script to run all WONDERBREAD benchmark evaluations sequentially.

Usage:
    python run_all_evals.py
    python run_all_evals.py --skip sop_generation
    python run_all_evals.py --skip sop_generation --skip demo_segmentation
"""

import argparse
import subprocess
import sys
from pathlib import Path


EVAL_SCRIPTS = {
    "sop_generation": "run_sop_generation.py",
    "demo_segmentation": "run_demo_segmentation.py",
    "sop_improvement": "run_sop_improvement.py",
    "sop_ranking": "run_sop_ranking.py",
    "demo_validation": "run_demo_validation.py",
    "question_answering": "run_question_answering.py",
}


def main():
    parser = argparse.ArgumentParser(description="Run all WONDERBREAD benchmark evaluations sequentially")
    parser.add_argument(
        "--path_to_experimental_results_dir",
        type=str,
        default=None,
        help="Path to experimental results directory (optional, defaults to data/experimental_results)"
    )
    parser.add_argument(
        "--path_to_data_dir",
        type=str,
        default=None,
        help="Path to gold demos directory (optional, only needed for SOP generation eval)"
    )
    parser.add_argument(
        "--skip",
        type=str,
        action="append",
        default=[],
        help="Tasks to skip (can be specified multiple times). Options: " + ", ".join(EVAL_SCRIPTS.keys())
    )
    args = parser.parse_args()

    script_dir = Path(__file__).parent.resolve()

    for task_name, eval_script in EVAL_SCRIPTS.items():
        if task_name in args.skip:
            print(f"Skipping {task_name}")
            continue

        cmd = [sys.executable, str(script_dir / eval_script)]

        if args.path_to_experimental_results_dir:
            cmd.extend(["--path_to_experimental_results_dir", args.path_to_experimental_results_dir])

        if args.path_to_data_dir and eval_script == "run_sop_generation.py":
            cmd.extend(["--path_to_data_dir", args.path_to_data_dir])

        result = subprocess.run(cmd, cwd=str(script_dir))
        if result.returncode != 0:
            sys.exit(result.returncode)


if __name__ == "__main__":
    main()
