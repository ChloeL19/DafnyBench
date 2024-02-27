/*
HumanEvalX 160 
Given two lists operator, and operand. The first list has basic algebra operations, and the second list is a 
list of integers. Use the two given lists to build the algebric expression and return the evaluation of 
this expression. The basic algebra operations: Addition ( + ) Subtraction ( - ) Multiplication ( * ) 
Floor division ( // ) Exponentiation ( ** ) Example: operator['+', '*', '-'] array = [2, 3, 4, 5] 
result = 2 + 3 * 4 - 5 => result = 9 Note: The length of operator list is equal to the length of operand 
list minus one. Operand is a list of of non-negative integers. Operator list has at least one operator, 
and operand list has at least two operands.
*/

function pow(base: int, exponent: int): int
  requires exponent >= 0
  decreases exponent
{
  if exponent == 0 then 1
  else if exponent % 2 == 0 then pow(base * base, exponent / 2)
  else base * pow(base, exponent - 1)
}

method do_algebra(operators: seq<char>, operands: seq<int>) returns (result: int)
  requires operators != [] && operands != [] && |operators| + 1 == |operands|
  requires forall i :: 0 <= i < |operands| ==> operands[i] >= 0
{
  result := operands[0];
  var i := 0;
  while i < |operators|
    invariant 0 <= i <= |operators|
    decreases |operators| - i
  {
    var op := operators[i];
    i := i + 1;
    match op
    {
      case '+' =>
        result := result + operands[i];
      case '-' =>
        result := result - operands[i];
      case '*' =>
        result := result * operands[i];
      case '/' => 
        if operands[i] != 0 {
            result := result / operands[i];
        }
      case '^' => 
        result := pow(result, operands[i]);
      case _ =>
    }
  }
}