




<h1 class="heading"><span class="name">Grade Down (Monadic)</span> <span class="command">R←⍒Y</span></h1>



`Y` may be any array of rank greater than 0 but may not contain namespaces.  `R` is an integer vector being the permutation of `⍳1↑⍴Y` that places the sub-arrays along the first axis in descending order. For the rules for comparing items of `Y` with one another, see [Grade Up (Monadic)](grade-up-monadic.md).


`⎕IO` is an implicit argument of Grade Down.


<h2 class="example">Examples</h2>
```apl
      ⍒22.5 1 15 3 ¯4
1 3 4 2 5

```
```apl
      M
2 3 5
1 4 7
     
2 3 4
5 2 4
     
2 3 5
1 2 6
      ⍒M
1 3 2

```



**Note that character arrays sort differently in the Unicode and Classic Editions.**
```apl
      M
Goldilocks
porridge   
Porridge   
3 bears 
```


|Unicode Edition                                             |Classic Edition                                             |
|------------------------------------------------------------|------------------------------------------------------------|
|```apl       ⍒M 2 3 1 4 ```                                 |```apl       ⍒M 3 1 4 2 ```                                 |
|```apl       M[⍒M;] porridge Porridge Goldilocks 3 bears ```|```apl       M[⍒M;] Porridge Goldilocks 3 bears porridge ```|

```apl
      ⍴pb
6 3
      pb
┌────────┬─────┬───┐
│Rivers  │Jason│554│
├────────┼─────┼───┤
│Daintree│John │532│
├────────┼─────┼───┤
│Rivers  │Jason│543│
├────────┼─────┼───┤
│Foad    │Jay  │558│
├────────┼─────┼───┤
│Scholes │John │547│
├────────┼─────┼───┤
│Scholes │John │535│
└────────┴─────┴───┘
      ⍒pb
5 6 1 3 4 2

```


