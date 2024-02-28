## Contributions
This project aims to create the largest Dafny benchmark to date and set a tone for the core types of formal verification challenges required for properly evaluating the abilities of Large Language Models. It will do this by categorizing all presented problems into one of four categories representing the complexity of the formal verification task. This benchmark will likely contain mostly problems from Category 1 and Category 2.

`programs/` contains the ground-truth implementation of each problem. Each problem has a docstring description and is solved with a dafny method and possibly several helper functions and lemmas. `tasks/` will contain the problem setup of each benchmark task. We will also include evaluation scripts for running models on this benchmark.

See key characteristics of each implemented program in the characteristics.csv file.

## Category Coding Scheme
##### What ability does each problem category test?

[maybe nice to include diagram of difficulty spectrum, basically 1 should be the easiest and least meaningful/important for safety, and 4 should be the most difficult and more important for real safety]

* Category 1: relate formal specification to algorithm implementation (relate objects in logic world to objects in algorithm world)
* Category 1.5: Category 1 programs that require multiple helper functions and lemmas to prove
* Category 2: relate a logical property (which can be a subset of a full formal spec) to an algorithm implementation or a specification
* Category 3: relate two separate logical specifications to each other
* Category 4: some multi-step combination of all of the above

## References
I would really like to incorporate problems from Clover and MBPP-Dafny-- will be in touch with those authors.
Likely will translate problems from MBPP, HumanEval, Leetcode, and MIPS. May combinatorially combine these problem solutions to create more complex problems and solutions. 
May also experiment with creating synthetic problems.

## Collect Statistics on all Programs
- [ ] How many helper functions/methods does the program include?
- [ ] Does the verification involve extra lemmas?
- [ ] What is the category of the problem

## Development Questions
- [ ] All right to include multiple correct implementations of the same ground truth program? Should we be aiming for this?
- [ ] Is it okay for ground truth programs to involve multiple helper functions and lemmas? 
- [ ] Is it okay that some programs require helper functions for their formal specification? Also okay that some implementations of the same docstring may have different formal specifications?
- [ ] Note: locally some Dafny functions timeout in a way that doesn't happen on other peoples' devices I think. Not sure if this will bias the solutions I produce in any way.
- [ ] Can edits-based methods work with problems that have multiple moving parts? i.e. how to make sure edits only apply to the function that is wrong?
- [ ] should we expand number of categories to reflect different number of helper functions expected as well?

## Ideas for Tasks
- Code synthesis and annotations: basically implement an algorithm and a proof for that algorithm given a formal specification of what is wanted
- Annotations: given an algorithm, re-insert the formal specifications and all helper annotations
- Docstring to full implementation: given a natural language description of a task, write a formal specification for important properties of this task and also implement an algorithm for it and prove the algorithm upholds the chosen properties.

## Ideas for Future Tasks
- Synthesis of formal specs from natural language
- Synthesis of natural language from formal specs