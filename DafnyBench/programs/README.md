Each program in this list represents one way the formal specification and docstring at the top of the .dfy file can be satisfied in Dafny. We note that sometimes there is more than way to implement a program satisfying the same docstring and formal spec. We denote such equivalences using the `_variantX` naming convention. For example, `HasCloseElements_variant01.dfy` is another way to solve `HasCloseElements.dfy`. 

`characteristics.csv` contains useful statistics about each program we've implemented in this benchmark. The statistics include:
- the number of methods required by the implementation
- the number of functions required by the implementation
- the number of lemmas required to verify the implementation
- the source from which the problem framing originated (non-github link format means the problem was hand-crafted)

