import hashlib
import os

def execute(cmd, ext, v):
    HOME = os.environ["HOME"]
    TMP_DIR = f"{HOME}/tmp/llm-verified/{ext}/"
    key = hashlib.md5(v.encode("utf-8")).hexdigest()
    dir = "%s%s/" % (TMP_DIR, key)
    old_dir = os.getcwd()
    if not os.path.exists(dir):
        os.makedirs(dir)
    os.chdir(dir)

    try:
        fn = f"ex.{ext}"
        outfn = "out.txt"
        errfn = "err.txt"

        f = open(fn, "w")
        f.write(v)
        f.close()

        status = os.system("timeout 10 %s %s >%s 2>%s" % (cmd, fn, outfn, errfn))

        f = open(outfn, "r")
        outlog = f.read()
        f.close()

        f = open(errfn, "r", encoding='utf-8')
        log = f.read()
        f.close()

        sys_error_prefix = "sh: line 1:"
        if log.startswith(sys_error_prefix):
            raise RuntimeError(
                log[len(sys_error_prefix) :]
                + " -- install tool locally or set livecode to True for lightweight testing"
            )
    finally:
        os.chdir(old_dir)

    return {"status": status, "log": log, "out": outlog}

if __name__ == "__main__":
    code = """
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
        //invariant maxWord in words
        //invariant maxUniqueChars == numUniqueChars(maxWord)
        //invariant numUniqueChars(word) <= numUniqueChars(maxWord)
        //invariant (forall w :: 0 <= w < i ==> numUniqueChars(words[w]) <= numUniqueChars(maxWord))
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
    """
    print(execute("dafny verify", ".dfy", code))
