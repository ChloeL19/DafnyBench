method rando(){
    var s := "hello";
    assert s[0] == 'h';
    assert exists k :: 0 <= k < |s| - 2 ==> s[k] + s[k+1] + s[k+2] == "hell";
}