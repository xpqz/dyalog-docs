<h1 class="heading"><span class="name"> Display of Arrays</span></h1>

Simple scalars and vectors are displayed in a single line beginning at the left margin.  A number is separated from the next adjacent element by a single space.  The number of significant digits to be printed is determined by the system variable `⎕PP` whose default value is 10.  The fractional part of the number will be rounded in the last digit if it cannot be represented within the print precision.  Trailing zeros after a decimal point and leading zeros will not be printed.  An integer number will display without a decimal point.

**Examples**

```apl
      0.1 1.0 1.12
0.1 1 1.12
 
      'A' 2 'B' 'C'
A 2 BC
 
      ÷3 2 6
0.3333333333 0.5 0.1666666667
```

If a number cannot be fully represented in `⎕PP` significant digits, or if the number requires more than five leading zeros after the decimal point, the number is represented in scaled form.  The mantissa will display up to `⎕PP` significant digits, but trailing zeros will not be displayed.

**Examples**

```apl
      ⎕PP←3
 
      123 1234 12345 0.12345 0.00012345 0.00000012345
123 1.23E3 1.23E4 0.123 0.000123 1.23E¯7
```

Simple matrices are displayed in rectangular form, with one line per matrix row.  All elements in a given column are displayed in the same format, but the format and width for each column is determined independently of other columns.  A column is treated as numeric if it contains any numeric elements.  The width of a numeric column is determined such that the decimal points (if any) are aligned; that the `E` characters for scaled formats are aligned, with trailing zeros added to the mantissae if necessary, and that integer forms are right-adjusted one place to the left of the decimal point column (if any).  Numeric columns are right-justified; a column which contains no numeric elements is left-justified.  Numeric columns are separated from their neighbours by a single column of blanks.

**Examples**

```apl
      2 4⍴'HANDFIST'
HAND
FIST
 
      1 2 3 ∘.× 6 2 5
 6 2  5
12 4 10
18 6 15
 
      2 3⍴2 4 6.1 8 10.24 12
2  4     6.1
8 10.24 12
 
      2 4⍴4 'A' 'B' 5 ¯0.000000003 'C' 'D' 123.56
 4E0  AB   5
¯3E¯9 CD 123.56
```

In the display of non-simple arrays, each element is displayed within a rectangle such that the rows and columns of the array are aligned.  Simple items within the array are displayed as above.  For non-simple items, this rule is applied recursively, with one space added on each side of the enclosed element for each level of nesting.

**Examples**

```apl
      ⍳3
1 2 3
 
      ⊂⍳3
 1 2 3
 
      ⊂⊂⍳3
  1 2 3
 
      ('ONE' 1) ('TWO' 2) ('THREE' 3) ('FOUR' 4)
  ONE  1   TWO  2   THREE  3   FOUR  4
 
      2 4⍴'ONE' 1 'TWO' 2 'THREE' 3 'FOUR' 4
 ONE    1  TWO   2
 THREE  3  FOUR  4
```

Multi-dimensional arrays are displayed in rectangular planes.  Planes are separated by one blank line, and hyper-planes of higher dimensions are separated by increasing numbers of blank lines.  In all other respects, multi-dimensional arrays are displayed in the same manner as matrices.

**Examples**

```apl
      2 3 4⍴⍳24
 1  2  3  4
 5  6  7  8
 9 10 11 12
 
13 14 15 16
17 18 19 20
21 22 23 24
 
      3 1 1 3⍴'THEREDFOX'
THE
 
 
RED
 
 
FOX
```

The power of this form of display is made apparent when formatting informal reports.

**Examples**

```apl
      +AREAS←'West' 'Central' 'East'
 West  Central  East
 
      +PRODUCTS←'Biscuits' 'Cakes' 'Buns' 'Rolls'
 Biscuits  Cakes  Buns  Rolls
 
      SALES←50 5.25 75 250 20.15 900 500
      SALES,←80.98 650 1000 90.03 1200
      +SALES←4 3⍴SALES
  50  5.25   75
 250 20.15  900
 500 80.98  650
1000 90.03 1200
 
      ' ' PRODUCTS ⍪., AREAS SALES
            West  Central  East
 Biscuits     50     5.25    75
 Cakes       250    20.15   900
 Buns        500    80.98   650
 Rolls      1000    90.03  1200
```

If the display of an array is wider than the page width, as set by the system variable `⎕PW`, it will be folded at or before `⎕PW` and the folded portions indented six spaces.  The display of a simple numeric or mixed array may be folded at a width less than `⎕PW` so that individual numbers are not split across a page boundary.

**Example**

```apl
      ⎕PW←40
 
      ?3 20⍴100
54 22  5 68 68 94 39 52 84  4  6 53 68
85 53 10 66 42 71 92 77 27  5 74 33 64
66  8 64 89 28 44 77 48 24 28 36 17 49
       1  39  7 42 69 49 94
      76 100 37 25 99 73 76
      90  91  7 91 51 52 32
```

## The ]display User Command

The user command `]display`   illustrates the structure of an array.

**Examples**

```apl
      ]display 'ABC' (1 4⍴1 2 3 4)
┌→────────────────┐
│ ┌→──┐ ┌→──────┐ │
│ │ABC│ ↓1 2 3 4│ │
│ └───┘ └~──────┘ │
└∊────────────────┘

```
```apl
      ]display ' 'PRODUCTS⍪.,AREAS SALES ⍝ see above
┌────────────────────────────────────────┐
│ ┌→───────────────────────────────────┐ │
│ ↓            ┌→───┐ ┌→──────┐ ┌→───┐ │ │
│ │            │West│ │Central│ │East│ │ │
│ │ -          └────┘ └───────┘ └────┘ │ │
│ │ ┌→───────┐                         │ │
│ │ │Biscuits│ 50     5.25      75     │ │
│ │ └────────┘                         │ │
│ │ ┌→────┐                            │ │
│ │ │Cakes│    250    20.15     900    │ │
│ │ └─────┘                            │ │
│ │ ┌→───┐                             │ │
│ │ │Buns│     500    80.98     650    │ │
│ │ └────┘                             │ │
│ │ ┌→────┐                            │ │
│ │ │Rolls│    1000   90.03     1200   │ │
│ │ └─────┘                            │ │
│ └∊───────────────────────────────────┘ │
└∊───────────────────────────────────────┘

```

An explanation of the symbols that appear in the borders can be seen by running `]display -?`

## The ]boxing User Command

The user command `]boxing` changes the way in which nested arrays are the displayed in the Session. The following examples show different settings.

Examples
```apl
      ]boxing on -style=min
Was OFF -style=min

      'ABC' (1 4⍴1 2 3 4)
┌───┬───────┐
│ABC│1 2 3 4│
└───┴───────┘

      ]boxing on -style=mid
Was ON -style=min

      'ABC' (1 4⍴1 2 3 4)
┌→──┬───────┐
│ABC│1 2 3 4↓
└──→┴~─────→┘

      ]boxing on -style=max
┌→────────────────┐
│Was ON -style=mid│
└─────────────────┘

      'ABC' (1 4⍴1 2 3 4)
┌→────────────────┐
│ ┌→──┐ ┌→──────┐ │
│ │ABC│ ↓1 2 3 4│ │
│ └───┘ └~──────┘ │
└∊────────────────┘

      ]boxing on -style=min
Was ON -style=max
      ]boxing off
Was ON

      'ABC' (1 4⍴1 2 3 4)
 ABC  1 2 3 4 

```

## Shy Results

Functions may return shy results.

A shy  or suppressed result is a result that is not automatically displayed in the Session, but is suppressed. A shy result of an expression may be displayed by using it as an argument to a function that returns its argument unchanged, by enclosing the expression in parentheses or by assigning it to `⎕`.

**Examples**

```apl
      A←10 ⍝ Result of assignment is shy
      (A←10)
10
      ⎕DL 2 ⍝ Result of delay is shy
      ⎕←⎕DL
1.994
      foo&88  ⍝ Result of Spawn (thread number) is shy
      ⊣foo&88
6

```

See also:

- [Model Syntax.](../../defined-functions-and-operators/traditional-functions-and-operators/model-syntax.md)

- [Shy Result.](../../defined-functions-and-operators/dfns-and-dops/shy-result.md)

- [Execute Expression](../../../../language-reference-guide/the-i-beam-operator/execute-expression)
.
