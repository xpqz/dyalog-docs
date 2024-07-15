<h1> Structuring of Arrays</h1>

A class of primitive functions re-structures arrays in some way. Arrays may be input only in scalar or vector form. Structural functions may produce arrays with a higher rank. The Structural functions are [reshape](../../../../language-reference-guide/primitive-functions/reshape) (`⍴`), [ravel](../../../../language-reference-guide/primitive-functions/ravel), [laminate and catenate](../../../../language-reference-guide/primitive-functions/catenate-laminate) (`,`), [reverse](../../../../language-reference-guide/primitive-functions/reverse) and [rotate](../../../../language-reference-guide/primitive-functions/rotate) (`⌽`), [transpose](../../../../language-reference-guide/primitive-functions/transpose-monadic) (`⍉`), [mix](../../../../language-reference-guide/primitive-functions/mix) and [take](../../../../language-reference-guide/primitive-functions/take) (`↑`), [split](../../../../language-reference-guide/primitive-functions/split) and [drop](../../../../language-reference-guide/primitive-functions/drop) (`↓`), [enlist](../../../../language-reference-guide/primitive-functions/enlist) (`∊`), and [enclose](../../../../language-reference-guide/primitive-functions/enclose) (`⊂`).

<h2 class="example">Examples</h2>
```apl
      2 2⍴1 2 3 4
1 2
3 4
 
      2 2 4⍴'ABCDEFGHIJKLMNOP'
ABCD
EFGH
 
IJKL
MNOP
         ↓2 4⍴'COWSHENS'
 COWS  HENS
```
