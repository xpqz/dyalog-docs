<h1> Vector Notation</h1>

A series of two or more adjacent expressions results in a vector whose elements are the enclosed arrays resulting from each expression.  This is known as vector (or strand) notation. Each expression in the series may consist of one of the following:

1. a single numeric value
2. single character, within a pair of quotes
3. more than one character, within a pair of quotes
4. the name of a variable
5. the evaluated input symbol `⎕`
6. the quote-quad symbol `⍞`
7. the name of a niladic, defined function yielding a result
8. any other APL expression which yields a result, within parentheses

<h2 class="example">Examples</h2>
```apl
      ⍴A←2 4 10
3
      ⍴TEXT←'ONE' 'TWO'
2
```

Numbers and characters may be mixed:
```apl
      ⍴X←'THE ANSWER IS ' 10
2
      X[1]
 THE ANSWER IS
      X[2] + 32
42
```

Blanks, quotes or parentheses must separate adjacent items in vector notation.  Redundant blanks and parentheses are permitted.  In this manual, the symbol pair '`←→`' indicates the phrase 'is equivalent to'.
```apl
      1  2  ←→ (1)(2) ←→ 1  (2)  ←→ (1)  2
      2'X'3 ←→ 2 'X' 3 ←→ (2) ('X') (3)
      1  (2+2) ←→ (1) ((2+2)) ←→ ((1))  (2+2)
```

Vector notation may be used to define an item in vector notation:
```apl
       ⍴X ← 1 (2 3 4) ('THIS' 'AND' 'THAT')
3
      X[2]
 2 3 4
      X[3]
  THIS  AND  THAT
```

Expressions within parentheses are evaluated to produce an item in the vector:
```apl
      Y ← (2+2) 'IS' 4
      Y
4  IS  4
```

The following identity holds:
```apl
      A  B  C  ←→ (⊂A), (⊂B), ⊂C
```
