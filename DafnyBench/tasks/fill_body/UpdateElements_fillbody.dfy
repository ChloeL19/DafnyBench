/*
Adapted from Clover_update_array_strong.dfy
Ensure the array value is increased by 3 in the fourth position, and the array value is set to 516 in the 7th position.
*/

method UpdateElements(a: array<int>)
  requires a.Length >= 8
  modifies a
  ensures old(a[4]) +3 == a[4]
  ensures a[7]==516
  ensures forall i::0 <= i<a.Length ==> i != 7 && i != 4 ==> a[i] == old(a[i])
{
  /* TODO */
}