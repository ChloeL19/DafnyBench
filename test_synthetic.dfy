method rando(){
    var s := "hello";
    assert s[0] == 'h';

    // assert exists k :: 0 <= k < |s| - 1 && s[k] == 'h';
    // assert exists k :: 0 <= k < |s| - 1 && s[k] == 'h' && s[k+1] == 'e';

    assert 0 <= 0 < |s| - 2 && s[0..0+3] == "hel";
    assert 0 <= 0 < |s| - 2 && s[0] == 'h' && s[0+1] == 'e' && s[0+2] == 'l';
    assert exists k: int :: 0 <= k < |s| - 2 && s[k] == 'h' && s[k+1] == 'e' && s[k+2] == 'l';
}