/*
HumanEvalX 10
Test if given string is a palindrome.
Find the shortest palindrome that begins with a supplied string. Algorithm idea is simple: 
- Find the longest postfix of supplied string that is a palindrome. 
- Append to the end of the string reverse of a string prefix that comes before the palindromic suffix.
*/

//TODO: unsure whether to include because times out, but lots of rich helper functions here

function reverse(s: string): string {
    if (|s| == 0) then "" else reverse(s[1..]) + s[0..1]
}

lemma reverse_length(s: string)
ensures |reverse(s)| == |s|
{
}

lemma reverse_assoc(s1: string, s2: string, s3: string)
ensures reverse(s1 + s2 + s3) == reverse(s1 + (s2 + s3))
{
    assert s1 + s2 + s3 == s1 + (s2 + s3);
}

lemma reverse_concat_empty(s: string)
ensures "" + reverse(s) == reverse(s + "")
{
    assert "" + reverse(s) == reverse(s);
    assert s + "" == s;
}

lemma reverse_step(s: string, x: char)
requires |s| > 0
ensures reverse(s[1..] + [x]) + [s[0]] == reverse(s + [x])
{
    var t := s + [x];
    assert reverse(t) == reverse(t[1..]) + t[0..1];
    assert t[1..] == s[1..] + [x];
    assert t[0..1] == [s[0]];
    assert reverse(t) == reverse(s[1..] + [x]) + [s[0]];
}

lemma reverse_concat1(s: string, x: char)
ensures [x] + reverse(s) == reverse(s + [x])
{
    if |s| == 0 {
        assert "" + [x] == [x];
        assert [x] == reverse([x]);
    } else {
        reverse_concat1(s[1..], x);
        assert [x] + reverse(s[1..]) == reverse(s[1..] + [x]);
        assert [x] + reverse(s[1..]) + [s[0]] == reverse(s[1..] + [x]) + [s[0]];
        assert reverse(s[1..]) + [s[0]] == reverse(s);
        reverse_step(s, x);
        assert reverse(s[1..] + [x]) + [s[0]] == reverse(s + [x]);
        assert [x] + reverse(s) == reverse(s + [x]);
    }
}

lemma reverse_parts(s1: string, s2: string)
ensures s1 + reverse(s2) == reverse(s2 + reverse(s1))
{
    if |s1| == 0 {
        reverse_concat_empty(s2);
    } else {
        reverse_parts(s1[1..], s2);
        assert s1[0..1] + s1[1..] + reverse(s2) == s1[0..1] + reverse(s2 + reverse(s1[1..]));
        assert s1[0..1] + s1[1..] + reverse(s2) == s1 + reverse(s2);
        assert s1 + reverse(s2) == s1[0..1] + reverse(s2 + reverse(s1[1..]));
        reverse_concat1(s2 + reverse(s1[1..]), s1[0]);
        assert s1[0..1] + reverse(s2 + reverse(s1[1..])) == reverse(s2 + reverse(s1[1..]) + [s1[0]]);
        assert s1 + reverse(s2) == reverse(s2 + reverse(s1[1..]) + [s1[0]]);
        assert reverse(s1[1..]) + [s1[0]] == reverse(s1);
        reverse_assoc(s2, reverse(s1[1..]), [s1[0]]);
        assert reverse(s2 + reverse(s1[1..]) + [s1[0]]) == reverse(s2 + (reverse(s1[1..]) + [s1[0]]));
        assert reverse(s2 + reverse(s1[1..]) + [s1[0]]) == reverse(s2 + reverse(s1));
        assert s1[0..1] + s1[1..] + reverse(s2) == s1 + reverse(s2);
        assert s1 + reverse(s2) == reverse(s2 + reverse(s1));
    }
}

function is_palindrome(s: string): bool {
    s == reverse(s)
}

lemma is_palindrome_palindrome_reverse(s: string, i: int)
requires 0 <= i <= |s|
requires is_palindrome(s[i..])
ensures is_palindrome(s + reverse(s[0..i]))
{
    var p := s + reverse(s[0..i]);
    reverse_length(s[0..i]);
    assert |p| == |s| + i;
    var rp := reverse(p);
    reverse_length(p);
    reverse_parts(s[0..i], s);
    assert rp == s[0..i] + reverse(s);
    reverse_parts(s[i..], s[0..i]);
    assert s[i..] + reverse(s[0..i]) == reverse(s[0..i] + reverse(s[i..]));
    assert s[i..] + reverse(s[0..i]) == reverse(s[0..i] + s[i..]);
    assert reverse(s[0..i] + s[i..]) == s[i..] + reverse(s[0..i]);
    assert s == s[0..i] + s[i..];
    assert rp == s + reverse(s[0..i]);
    assert p == rp;
}

method make_palindrome(s: string) returns (result: string)
    ensures is_palindrome(result)
{
    for i := 0 to |s|
    {
        if is_palindrome(s[i..]) {
            result := s + reverse(s[0..i]);
            is_palindrome_palindrome_reverse(s, i);
            assert is_palindrome(s + reverse(s[0..i]));
            return;
        }
    }
    result := s + reverse(s);
    is_palindrome_palindrome_reverse(s, |s|);
    assert s == s[0..|s|];
    assert is_palindrome(s + reverse(s));
}