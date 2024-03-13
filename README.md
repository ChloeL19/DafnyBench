Get setup quickly by chatting here: https://chat.openai.com/g/g-cDrCHBx9Y-repo-research-assistant 

## Contributions
This project aims to create the largest Dafny benchmark (with >1000 different Dafny challenges) to date and set a tone for the core types of formal verification challenges required for properly evaluating the abilities of Large Language Models. 

This repo introduces the benchmark `DafnyBench/` and corresponding infrastructure for loading and evaluating the tasks within it. Additionally, this repo contains `Baselines/` with baseline algorithms for solving the the `DafnyBench/` benchmark tasks.

#### DafnyBench
Within `DafnyBench`, `programs/` contains ground-truth implementations of the benchmark problems (we have ground truth implementations for >1000 of the problems in this benchmark). `tasks/` contains the problem setup of each benchmark task. We also include `evaluate` scripts and `loader` scripts for running models on the benchmark tasks.

See key characteristics of each implemented program in the `programs/characteristics.csv` file.
Likewise, each task directory has a `characteristics.csv` file describing the characteristics of each task example. This can help researchers categorize their model's results. For example, it may be interesting to measure how pretraining on `Category 1` tasks affects performance on `Category 2` tasks.

#### Baselines
Within `Baselines`, the `experiment.py` script and associated `cmdline` arguments allow researchers to run the following baseline algorithms on DafnyBench out of the box:
* Strict sampling from `code-phind-llama`
* Strict sampling from `GPT3.5`
* Strict sampling from `GPT4`
* Strict sampling from `Claude 3`
* Verified monte-carlo tree search sampling with `code-phind-llama`, dubbed `VMCTS`

## Getting Started
Install Dafny locally and the corresponding z3 solver. Make sure these are in your PYTHONPATH.

Install necessary Python requirements by running `pip install requirements.txt`.

To run one of the pre-established baselines on DafnyBench, run the following:

`./Baselines/log.sh Baselines/your_log_filename.txt python Baselines/experiment.py --experiment_name run.py --task fill_body`

Solution `.dfy` files will be saved to the `Baselines/outputs/fill_body/` directory.

To evaluate the solutions to the DafnyBench task (which is in this case `fill_body`), run:

`python DafnyBench/evaluate.py --outputs_dir Baselines/outputs/fill_body/`


## Benchmark Tasks
* *fill_body*: fill in missing method and function bodies in a file of Dafny code. We have X problems under this task.
The `fill_body` task has problems that fall into two main categories:
    * Category 1: fill in the body of a single core method based on a self-contained formal specification and docstring.
    * Category 2: fill in the body of a core method and possibly one or more helper functions/methods. the formal specification for the core method(s) may rely on helper functions and/or lemmas. this serves as a more realistic multi-step type of formal verification task.

* *fill_annotations*: fill in the missing compiler hints (excluding the formal specification) for code in a Dafny file. We have X problems for this task.

We welcome contributions for future tasks. These may include synthesizing docstrings for each piece of Dafny code, and/or synthesizing formal specifications for each docstring. It would be great to migrate more of the Clover tasks to here.

## Citations

@misc{sun2023clover,
      title={Clover: Closed-Loop Verifiable Code Generation}, 
      author={Chuyue Sun and Ying Sheng and Oded Padon and Clark Barrett},
      year={2023},
      eprint={2310.17807},
      archivePrefix={arXiv},
      primaryClass={cs.SE}
}

@misc{brandfonbrener2024verified,
      title={Verified Multi-Step Synthesis using Large Language Models and Monte Carlo Tree Search}, 
      author={David Brandfonbrener and Sibi Raja and Tarun Prasad and Chloe Loughridge and Jianang Yang and Simon Henniger and William E. Byrd and Robert Zinkov and Nada Amin},
      year={2024},
      eprint={2402.08147},
      archivePrefix={arXiv},
      primaryClass={cs.SE}
}

For now rest assured that GPT4 with reflection can solve at least one problem (DoAlgebra.dfy): https://chat.openai.com/share/9a250315-1ef2-460b-9fd2-a941e7e64141
