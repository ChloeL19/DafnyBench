/*
HumanEvalX 4
For a given list of input numbers, calculate Mean Absolute Deviation around the mean of this dataset. 
Mean Absolute Deviation is the average absolute difference between each element and a centerpoint (mean in this case): 
MAD = average | x - x_mean |
*/
function abs(x: real): real
{
  /* TODO */
}

function sum(numbers: seq<real>): real
{
    if |numbers| == 0 then
        0.0
    else
        numbers[0] + sum(numbers[1..])
}

function mean(numbers: seq<real>): real
    requires numbers != []
{
    sum(numbers) / (|numbers| as real)
}

function mapf<A,B>(f: A -> B, xs: seq<A>): seq<B>
    ensures |xs| == |mapf(f, xs)|
    ensures forall i :: 0 <= i < |xs| ==> (mapf(f, xs))[i] == f(xs[i])
{
    /* TODO */
}

function mean_absolute_deviation(numbers: seq<real>):real
    requires numbers != []
{
    /* TODO */
}

lemma sum_nonnegative(numbers: seq<real>)
    requires forall i :: 0 <= i < |numbers| ==> numbers[i] >= 0.0
    ensures sum(numbers) >= 0.0
{
}

lemma mean_nonnegative(numbers: seq<real>)
    requires numbers != []
    requires forall i :: 0 <= i < |numbers| ==> numbers[i] >= 0.0
    ensures mean(numbers) >= 0.0
{
    /* TODO */
}

lemma MeanAbsoluteDeviationNonnegative(numbers: seq<real>)
    requires numbers != []
    ensures mean_absolute_deviation(numbers) >= 0.0
{
   /* TODO */
}