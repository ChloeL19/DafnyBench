Each program in this list represents one way the formal specification and docstring at the top of the .dfy file can be satisfied in Dafny. We note that sometimes there is more than way to implement a program satisfying the same docstring and formal spec. We denote such equivalences using the `_variantX` naming convention. For example, `HasCloseElements_variant01.dfy` is another way to solve `HasCloseElements.dfy`. 

`characteristics.csv` contains useful statistics about each program we've implemented in this benchmark. The statistics include:
- category of the program (this indicates the complexity of the implementation, which is a proxy for the complexity of satisfying the docstring and formal specification)
- the number of helper functions required by the implementation
- the number of lemmas required to verify the implementation
- domain of the method that is implemented (i.e. does it operate on floats, strings, or objects more generally?)
- the source from which the problem framing originated (we adopt many problems from pre-existing python benchmarks)

We plan to provide scripts for filtering the Dafny programs and benchmark tasks based on these characeristics. Hopefully this will help researchers better target specific model capabilities that they want to test with this benchmark.
