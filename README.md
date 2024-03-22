## Contributions
This project aims to create the largest Dafny benchmark (with >1000 different Dafny challenges) to date and set a tone for the core types of formal verification challenges required for properly evaluating the abilities of Large Language Models.

This repo introduces the benchmark `DafnyBench/` and corresponding infrastructure for loading and evaluating the tasks within it.

#### DafnyBench
Within DafnyBench, `programs/` contains ground-truth implementations of the benchmark problems (we have ground truth implementations for >1000 problems). `tasks/` contains the problem setup of each benchmark task. We also include evaluate scripts and loader scripts for running models on the benchmark tasks.

See key characteristics of each implemented program in the `programs/characteristics.csv` file. This can help researchers categorize their model's results. For example, it may be interesting to measure how pretraining on Category 1 programs affects performance on Category 2 program tasks.

## Getting Started
Install Dafny locally and the corresponding z3 solver. Make sure these are in your PYTHONPATH.

Generate attempted solutions to each task example, and store these in some output subdirectory.

Within the DafnyBench directory, modify the appropriate fields of the `config.py` file if necessary, so the benchmark evaluator knows where to find all of your generated solution files.

Then run `run_eval.sh` to launch a bash script that will print the number of your solution files that meet our benchmark acceptance criteria.

## Call for Contributions

