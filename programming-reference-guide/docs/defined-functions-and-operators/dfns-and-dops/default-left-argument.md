<h1> Default Left Argument</h1>

The special  syntax: `⍺←expr` is used to give a default value to the left argument if a dfn is called monadically. For example:
```apl
      root←{      ⍝ ⍺th root
          ⍺←2     ⍝ default to sqrt
          ⍵*÷⍺
      }
```

The expression to the right of  `⍺←` is evaluated *only* if its dfn is called with no left argument.

Note that the assignment `⍺←⊢` allows an ambivalent function to call an ambivalent sub-function. For example in:
```apl
      foo←{
         ⍺←⊢
         ⍺ goo ⍵
      }
```

If `foo` is given a left argument, this is passed to `goo`. Otherwise, `⍺` is assigned `⊢` and the last line is `⊢ goo ⍵`, which is a monadic call on `goo` followed by the `⊢` (Right) of the result of `goo`, which is the same value.
