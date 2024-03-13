from execute import execute
import requests
import re
from typing import Optional, Tuple, List

def short_verifier_feedback(ok: str, not_ok: str) -> Optional[Tuple[str,str]]:
    _, err = calculateScoreHelper(not_ok)
    if err:
        err = err.strip()
        return (None, err)
    return None

def verifier_feedback(ok: str, not_ok: str) -> Optional[str]:
    msg = "Consider previous issue"
    if msg in ok:
        return None
    _, err = calculateScoreHelper(not_ok)
    if err:
        err = err.strip()
        hint = f"\n/* {msg}: {err} */\n"
        text = ok + hint
        return text
    return None

## Helper functions for checking if model output verifies
def calculateScore(msg: str) -> Optional[float]:
    score, _ = calculateScoreHelper(msg)
    return score

def calculateScoreHelper(msg: str) -> (Optional[float], Optional[str]):
    v = filterDafny(msg + "```").strip()
    if v == "":
        return None, None
    r = checkDafny(v)
    if r["status"] == 0:
        return 1.0, None
    log = r["out"]
    print(log)
    try:
        first = log[log.index("ex.dfy(") + 7 :]
    except ValueError:
        # might be a timeout
        return -1.0, ""
    num_line_first = int(first[0 : first.index(",")])
    if filterDafny(msg).strip() != v and num_line_first >= v.count("\n"):
        return None, None
    else:
        err = first[first.index(":") :]
        try:
            err = err[: err.index("ex.dfy")]
        except ValueError:
            pass
        return -1.0, err


def score_func(sentence: str) -> Optional[float]:
    score = calculateScore(sentence)
    return score

def filterDafny(msg: str) -> str:
    m = re.findall("```([Dd]afny)?(.*?)```", msg, re.MULTILINE | re.DOTALL)
    r = "\n".join([x[1] for x in m])
    return r


def checkDafny(v: str) -> dict:
    return execute("dafny verify", "dfy", v)

### Functions to work with generalized model output

def calculateScore_whole(msg: str) -> Optional[float]:
    score_whole, _ = calculateScoreHelper_whole(msg)
    score, _ = calculateScoreHelper(msg)
    print("SCORE")
    print(score)
    print("SCORE_WHOLE")
    print(score_whole)
    # always return the better of the two scores
    if score_whole == 1.0 and score == -1.0:
        return 1.0
    elif score_whole == 1.0 and score == 1.0:
        return 1.0
    elif score_whole == 1.0 and score == None:
        return 1.0
    elif score_whole == -1.0 and score == -1.0:
        return -1.0
    elif score_whole == -1.0 and score == 1.0:
        return 1.0
    elif score_whole == -1.0 and score == None:
        return None
    elif score_whole == None and score == -1.0:
        return None
    elif score_whole == None and score == 1.0:
        return 1.0
    else:
        return None

def calculateScoreHelper_whole(msg: str) -> (Optional[float], Optional[str]):
    v = [s.strip() for s in filterDafny_whole(msg + "```")]
    for vs in v:
        if vs == "":
            return None, None
        r = checkDafny(vs)
        if r["status"] == 0:
            return 1.0, None
        log = r["out"]
        print(log)
        try:
            first = log[log.index("ex.dfy(") + 7 :]
        except ValueError:
            pass
        num_line_first = int(first[0 : first.index(",")])
        err = first[first.index(":") :]
        try:
            err = err[: err.index("ex.dfy")]
        except ValueError:
            pass
    # return error sign only if all attempts fail
    return -1.0, err

def score_func_whole(sentence: str) -> Optional[float]:
    print("TEXT")
    print(sentence)
    score = calculateScore_whole(sentence)
    print("SCORE_FINAL")
    print(score)
    return score


def filterDafny_whole(msg: str) -> List[str]:
    m = re.findall("```([Dd]afny)?(.*?)```", msg, re.MULTILINE | re.DOTALL)
    r = [x[1] for x in m]
    return r

def check_cheat(code: str) -> bool:
    '''
    Checks if the code, which is assumed to be Dafny code, contains any {:verify false} or assume statements.
    '''
    lines = code.split('\n')
    for line in lines:
        line = line.strip()
        if '{:verify false}' in line:
            return True
        if line.startswith('assume'):
            return True
    return False

def can_be_solution(msg: str, formal_spec: List[str]) -> (bool, str):
    '''
    Checks if the parts of the model's response that compile account for the full original 
    formal specification.
    '''
    candidates = [s.strip() for s in filterDafny_whole(msg + "```")+[filterDafny(msg + "```")]]
    solutions = []
    formal_spec = [re.sub(r'\s', '', s) for s in formal_spec]
    for candidate in candidates:
        uncovered_spec = formal_spec
        print("THE FORMAL SPEC:")
        print(formal_spec)
        print("LENGTH OF FORMAL SPEC:")
        print(len(formal_spec))
        if candidate == "":
            continue
        r = checkDafny(candidate)
        if r["status"] == 0: # if the candidate verifies
            while len(uncovered_spec) > 0:
                spec = uncovered_spec[0]
                print("THE SPEC:")
                print(spec)
                print("THE CANDIDATE:")
                print(candidate)
                if spec in re.sub(r'\s', '', candidate):
                    print("SPEC MATCH!")
                    uncovered_spec.remove(spec)
                else:
                    break
            if len(uncovered_spec) == 0: # if the whole formal spec is accounted for
                if not check_cheat(candidate): 
                    solutions.append(candidate)
            else:
                pass # otherwise this does not count as a potential solution
    if len(solutions) > 0:
        print("THE NUMBER OF SOLUTIONS")
        print(len(solutions))
        return True, solutions[0]
    return False, ""
        
# TODO: do I need these below?
filter_code = filterDafny
filter_code_whole = filterDafny_whole
check_code = checkDafny

if __name__ == "__main__":
    formal_spec = [
        """function numUniqueChars(s: string): nat {
            |set c | c in s|
        }""",
        """method FindMaxWord(words: seq<string>) returns (maxWord: string)
            ensures maxWord in words || |words| == 0
            ensures forall w :: w in words ==> numUniqueChars(w) <= numUniqueChars(maxWord)
        {"""]

    ground_truth = """
```dafny
function numUniqueChars(s: string): nat {
    |set c | c in s|
}

method FindMaxWord(words: seq<string>) returns (maxWord: string)
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
}```
    """

    ground_truth_w_rand_split = """
```dafny
function numUniqueChars(s: string): nat {
    |set c | c in s|
}

method FindMaxWord(words: seq<string>) returns (maxWord: string)
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
}```

Now I will write random stuff in another split:
    ```dafny
    Random stuff that shouldn't compile LOL.
    ```
    """
    ground_truth_duplicated = """
```dafny
function numUniqueChars(s: string): nat {
    |set c | c in s|
}

method FindMaxWord(words: seq<string>) returns (maxWord: string)
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
}```
Here we go again.
```dafny
function numUniqueChars(s: string): nat {
    |set c | c in s|
}

method FindMaxWord(words: seq<string>) returns (maxWord: string)
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
}```
    """

    incorrect_body = """
```dafny
function numUniqueChars(s: string): nat {
    |set c | c in s|
}

method FindMaxWord(words: seq<string>) returns (maxWord: string)
    ensures maxWord in words || |words| == 0
    ensures forall w :: w in words ==> numUniqueChars(w) <= numUniqueChars(maxWord)
{
    if |words| == 0 {
        maxWord := "";
        return;
    }
    var word := words[0];
    var maxUniqueChars := |set c | c in maxWord|;
        var count := |uniqueChars|; 
        assert count == numUniqueChars(word);
        if count > maxUniqueChars || (count == maxUniqueChars && word < maxWord) {
            maxUniqueChars := count;
            maxWord := word;
            assert maxWord == word;
        }
    }
    assert forall w :: w in words ==> numUniqueChars(w) <= numUniqueChars(maxWord);
}```
    """

    modified_spec = """
```dafny
function numUniqueChars(s: string): nat {
    |set c | c in s|
}

method FindMaxWord(words: seq<string>) returns (maxWord: string)
    ensures maxWord in words || |words| == 0
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
}```
    """
    
    cheat = """
```dafny
function numUniqueChars(s: string): nat {
    |set c | c in s|
}

method {:verify false} FindMaxWord(words: seq<string>) returns (maxWord: string)
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
}```
    """

    cheat_assume = """
```dafny
function numUniqueChars(s: string): nat {
    |set c | c in s|
}

method FindMaxWord(words: seq<string>) returns (maxWord: string)
    ensures maxWord in words || |words| == 0
    ensures forall w :: w in words ==> numUniqueChars(w) <= numUniqueChars(maxWord)
{
    if |words| == 0 {
        maxWord := "";
        return;
    }
    assume false;
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
```
    """
    print(f"TEST FORMAL SPEC: {formal_spec}")
    print("---Test 1---")
    print(can_be_solution(ground_truth, formal_spec)) # should be true, this is the ground truth
    print("---Test 2---")
    print(can_be_solution(ground_truth_w_rand_split, formal_spec)) # should be true, this is the ground truth with random stuff in another split
    print("---Test 3---")
    print(can_be_solution(ground_truth_duplicated, formal_spec)) # should be true, this is the split and duplicated ground truth
    print("---Test 4---")
    print(can_be_solution(incorrect_body, formal_spec)) # should be false, this is an incorrect body
    print("---Test 5---")
    print(can_be_solution(modified_spec, formal_spec)) # should be false, this is a modified specification
    print("---Test 6---")
    print(can_be_solution(cheat, formal_spec)) # should be false, this is a cheat with {:verify false}
    print("---Test 7---")
    print(can_be_solution(cheat_assume, formal_spec)) # should be false, this is a cheat with assume false
