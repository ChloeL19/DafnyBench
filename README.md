This project aims to create the largest Dafny benchmark to date and set a tone for the core types of formal verification challenges required for properly evaluating the abilities of Large Language Models. This benchmark will likely contain mostly problems from Category 1 and Category 2.

programs/ contains the ground-truth implementation of each problem. Each problem has a docstring description and is solved with a dafny method and possibly several helper functions and lemmas. tasks/ will contain the problem setup of each benchmark task. We will also include evaluation scripts for running models on this benchmark.

## Category Coding Scheme
##### What ability does each problem category test?
Category 1: relate formal specification to algorithm implementation (relate objects in logic world to objects in algorithm world)
Category 2: relate a logical property (which can be a subset of a full formal spec) to an algorithm implementation or a specification
Category 3: relate two separate logical specifications to each other
Category 4: some multi-step combination of all of the above
