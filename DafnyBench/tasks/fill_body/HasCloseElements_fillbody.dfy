/*
HumanEvalX 0
Check if in given list of numbers, are any two numbers closer to each other than given threshold.
*/

function abs(x: real): real
{
  if x < 0.0 then -x else x
}

method HasCloseElements(numbers: seq<real>, threshold: real) returns (result: bool)
    ensures result <==> exists i, j ::
      0 <= i < |numbers| &&
      0 <= j < |numbers| &&
      i != j &&
      abs(numbers[i] - numbers[j]) < threshold
    ensures result ==> |numbers| > 1
{
    /* TODO */
}