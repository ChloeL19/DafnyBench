/* 
MIPS 0
We implement the following with bitvectors in Dafny.
here s' and t' are converted to decimal scalars
s = [1,1,1], t = [1,0,1], ys = [1, 0, 0], s' = 7, t' = 5, ys' = 4
ys' % 2 ^ (len(s)) = (s' + t') % 2 ^ (len(s))
4 % 8 = 12 % 8

def f(s,t):
    a = 0;b = 0;
    ys = []
    for i in range(10):
        c = s[i]; d = t[i];
        next_a = b ^ c ^ d
        next_b = b+c+d>1
        a = next_a;b = next_b;
        y = a
        ys.append(y)
    return ys

Please prove using Dafny that the python program above implements the sum of two length10 bitvectors in Dafny.
*/

function ArrayToBv10(arr: array<bool>): bv10 // Converts boolean array to bitvector
    reads arr
    requires arr.Length == 10
{
    /* TODO */
}

function ArrayToBv10Helper(arr: array<bool>, index: nat): bv10
    reads arr
    requires arr.Length == 10
    requires 0 <= index < arr.Length
    decreases index
    ensures forall i :: 0 <= i < index ==> ((ArrayToBv10Helper(arr, i) >> i) & 1) == (if arr
        [i] then 1 else 0)
{
    /* TODO */
}

method ArrayToSequence(arr: array<bool>) returns (res: seq<bool>) // Converts boolean array to boolean sequence
    ensures |res| == arr.Length
    ensures forall k :: 0 <= k < arr.Length ==> res[k] == arr[k]
{
    /* TODO */
}

function isBitSet(x: bv10, bitIndex: nat): bool
    requires bitIndex < 10
    ensures isBitSet(x, bitIndex) <==> (x & (1 << bitIndex)) != 0
{
    /* TODO */
}

function Bv10ToSeq(x: bv10): seq<bool> // Converts bitvector to boolean sequence
    ensures |Bv10ToSeq(x)| == 10
    ensures forall i: nat :: 0 <= i < 10 ==> Bv10ToSeq(x)[i] == isBitSet(x, i)
{
    /* TODO */
}

function BoolToInt(a: bool): int {
    /* TODO */
}

function XOR(a: bool, b: bool): bool {
    /* TODO */
}

function BitAddition(s: array<bool>, t: array<bool>): seq<bool> // Performs traditional bit addition
    reads s
    reads t
    requires s.Length == 10 && t.Length == 10
{
    /* TODO */
}

method BinaryAddition_02(s: array<bool>, t: array<bool>) returns (sresult: seq<bool>) // Generated program for bit addition
    requires s.Length == 10 && t.Length == 10
    ensures |sresult| == 10
    ensures forall i :: 0 <= i && i < |sresult| ==> sresult[i] == ((s[i] != t[i]) != (i > 0 && ((s[i-1] || t[i-1]) && !(sresult[i-1] && (s[i-1] != t[i-1])))))
    ensures BitAddition(s, t) == sresult // Verification of correctness
{
    /* TODO */
}