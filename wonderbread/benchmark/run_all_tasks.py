#!/usr/bin/env python3
"""
Master orchestration script to run all WONDERBREAD benchmark tasks sequentially.

Usage:
    python run_all_tasks.py --model GPT4 [--is_debug]
    python run_all_tasks.py --model openrouter/anthropic/claude-3.5-sonnet [--is_debug]
"""

import argparse
import subprocess
import sys
from pathlib import Path


BENCHMARK_TASKS = [
    "documentation/sop_generation/run_experiments.py",
    "documentation/demo_segmentation/run_experiments.py",
    "improvement/sop_improvement/run_experiments.py",
    "improvement/sop_ranking/run_experiments.py",
    "knowledge_transfer/demo_validation/run_experiments.py",
    "knowledge_transfer/question_answering/run_experiments.py",
]


def main():
    parser = argparse.ArgumentParser(description="Run all WONDERBREAD benchmark tasks sequentially")
    parser.add_argument("--model", type=str, required=True, help="Model to use")
    parser.add_argument("--is_debug", action="store_true", default=False, help="Run in debug mode")
    args = parser.parse_args()

    script_dir = Path(__file__).parent.resolve()
    tasks_dir = script_dir / "tasks"

    if not tasks_dir.exists():
        print(f"Error: Tasks directory not found at: {tasks_dir}", file=sys.stderr)
        sys.exit(1)

    for task_path in BENCHMARK_TASKS:
        cmd = [sys.executable, str(tasks_dir / task_path), "--model", args.model]
        if args.is_debug:
            cmd.append("--is_debug")

        result = subprocess.run(cmd, cwd=str(tasks_dir))
        if result.returncode != 0:
            sys.exit(result.returncode)


if __name__ == "__main__":
    main()
