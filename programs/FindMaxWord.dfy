/*
HumanEvalX 158
Write a function that accepts a list of strings. The list contains different words. 
Return the word with maximum number of unique characters. If multiple strings have maximum number of unique 
characters, return the one which comes first in lexicographical order.
*/

function numUniqueChars(s: string): nat {
    |set c | c in s|
}

method findMax(words: seq<string>) returns (maxWord: string)
    ensures maxWord in words || |words| == 0
    ensures forall w :: w in words ==> numUniqueChars(w) <= numUniqueChars(maxWord)
{
    if |words| == 0 {
        maxWord := "";
        return;
    }
    var word := words[0];
    maxWord := words[0];
    var maxUniqueChars := |set c | c in maxWord|;
    assert maxUniqueChars == numUniqueChars(maxWord);
    for i := 0 to |words|
        invariant maxWord in words
        invariant maxUniqueChars == numUniqueChars(maxWord)
        invariant numUniqueChars(word) <= numUniqueChars(maxWord)
        invariant (forall w :: 0 <= w < i ==> numUniqueChars(words[w]) <= numUniqueChars(maxWord))
    {
        word := words[i];
        var uniqueChars := set c | c in word; 
        var count := |uniqueChars|; 
        assert count == numUniqueChars(word);
        if count > maxUniqueChars || (count == maxUniqueChars && word < maxWord) {
            maxUniqueChars := count;
            maxWord := word;
            assert maxWord == word;
        }
        assert maxUniqueChars >= count;
        assert maxUniqueChars == numUniqueChars(maxWord);
    }
    assert forall w :: w in words ==> numUniqueChars(w) <= numUniqueChars(maxWord);
}
