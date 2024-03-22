/*
HumanEvalX 158
Write a function that accepts a list of strings. The list contains different words. 
Return the word with maximum number of unique characters. If multiple strings have maximum number of unique 
characters, return the one which comes first in lexicographical order.
*/

function numUniqueChars(s: string): nat {
    |set c | c in s|
}

method FindMaxWord(words: seq<string>) returns (maxWord: string)
    ensures maxWord in words || |words| == 0
    ensures forall w :: w in words ==> numUniqueChars(w) <= numUniqueChars(maxWord)
{
    /* TODO */
}