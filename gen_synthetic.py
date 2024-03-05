'''
First define a list of string properties that one could have. 
Phrase these as strings that can be slotted into requires/ensures clauses in Dafny.
Then select a random group of these properties, and randomly choose pairs to create directional connections between.
'''

# assume the string is always called s
# TODO: make sure these properties will all work in Dafny, may need to implement helper functions
properties = [
    "s[0] != 'a'",  # The first character is not 'a'
    "s[0] == 'a' || s[0] == 'e' || s[0] == 'i' || s[0] == 'o' || s[0] == 'u'",  # The first character is a vowel
    "|s| == 3",  # The string length is exactly 3
    "forall k :: 0 <= k < |s| - 2 ==> s[k] + s[k+1] + s[k+2] != \"nan\"",  # "nan" does not appear as a substring
    "|s| > 0 ==> s[0] == s[|s|-1]",  # The first and last characters are the same (non-empty string)
    "exists k :: 0 <= k < |s| && s[k] == ' '",  # There is at least one space in the string
    "forall k :: 0 <= k < |s| ==> s[k] in {'0', '1'}",  # The string is binary (consists only of '0' and '1')
    "|s| % 2 == 0",  # The string length is even
    "forall k :: 0 <= k < |s| ==> s[k] in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}",  # The string consists only of digits
    "exists k :: 0 <= k < |s| - 2 ==> s[k] + s[k+1] + s[k+2] == \"abc\"", # The string contains the substring "abc"
    "forall k :: 0 <= k < |s| - 1 ==> s[k] <= s[k+1]",  # The string's characters are in non-decreasing order
    "forall k :: 0 <= k < |s| ==> s[k] != 'z'",  # The string does not contain the character 'z'
    "0 <= 0 < |s| - 3 ==> s[0..0+5] == \"http\"", # The string starts with "http"
    "exists k :: 0 <= k < |s| && s[k] == 'a'",  # The string contains at least one 'a'
    
    # TODO: these properties require defining helper functions
    "forall k :: 0 <= k < |s| ==> char.IsUpper(s[k])",  # The string consists only of uppercase letters
    "exists k :: 0 <= k < |s| && char.IsLetter(s[k]) && char.IsLower(s[k])",  # There is at least one lowercase letter in the string
    "s == s.Reverse()",  # The string is a palindrome
    "|s| >= 5 && s.Substring(1, 3) == '123'",  # The substring starting at index 1 and of length 3 is "123" (for strings of length at least 5)
    "count(s, 'x') == 2",  # The character 'x' appears exactly twice in the string
    "s.ToUpper() == s",  # The string is identical to its uppercase version (implies it's already in uppercase)
    "exists k :: 0 <= k < |s| - 1 && s[k] == 'q' && s[k+1] == 'u'",  # The string contains the substring "qu"
    "|s.Trim().Length| == |s|",  # The string does not start or end with whitespace
    "s.Intersect('aeiou').Any()",  # The string contains at least one vowel
    "s.Distinct().Count() == |s|",  # All characters in the string are unique
    "exists k :: 0 <= k < |s| && char.IsPunctuation(s[k])",  # There is at least one punctuation mark in the string
]