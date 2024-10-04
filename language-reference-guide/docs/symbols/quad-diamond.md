



<h1 class="heading"><span class="name">Quad Diamond</span> <span class="command">⌺</span></h1>


## Quad Diamond is a Dyadic operator

## Operator Quad Diamond means


[Stencil](../primitive-operators/stencil.md)
```apl
Dyadic operator:  Stencil

      mat
 1  2  3  4
 5  6  7  8
 9 10 11 12
13 14 15 16
      
      ({⊂⍵}⌺3 3) mat
┌───────┬────────┬────────┬───────┐
│0 0 0  │0 0 0   │0 0 0   │0 0 0  │
│0 1 2  │1 2 3   │2 3 4   │3 4 0  │
│0 5 6  │5 6 7   │6 7 8   │7 8 0  │
├───────┼────────┼────────┼───────┤
│0 1  2 │1  2  3 │ 2  3  4│ 3  4 0│
│0 5  6 │5  6  7 │ 6  7  8│ 7  8 0│
│0 9 10 │9 10 11 │10 11 12│11 12 0│
├───────┼────────┼────────┼───────┤
│0  5  6│ 5  6  7│ 6  7  8│ 7  8 0│
│0  9 10│ 9 10 11│10 11 12│11 12 0│
│0 13 14│13 14 15│14 15 16│15 16 0│
├───────┼────────┼────────┼───────┤
│0  9 10│ 9 10 11│10 11 12│11 12 0│
│0 13 14│13 14 15│14 15 16│15 16 0│
│0  0  0│ 0  0  0│ 0  0  0│ 0  0 0│
└───────┴────────┴────────┴───────┘

      ({+/,⍵}⌺3 3) mat
14 24 30 22
33 54 63 45
57 90 99 69
46 72 78 54

```


[Language Elements](./language-elements.md)

