<h1 class="heading"><span class="name">Monadic Operator Generator</span> <span class="command">R←43⌶Y</span></h1>

Returns a monadic operator, selected by the right argument `Y`.

`Y` is a scalar integer from the following table.
Running 43⌶ with a right argument not in the table below results in a `DOMAIN ERROR`.

`R` is a monadic operator, chosen by the value of `Y`. Its functionality is described in the following table. Since the result is a monadic operator, it is recommended that the evaluation of this I-Beam is either parenthesised or named.

| Y | Returned Operator | Notes |
|---|---                |---|
|632|[Generics Operator](#632-generics-operator)| Requires .NET. |


!!! warning
	The set of supported values for `Y` might change from one release to the next. Saving the resulting operator in a workspace and attempting to run in in a later release might therefore cause a `DOMAIN ERROR`, if support has been withdrawn. It is guaranteed that documented `Y` values will not be repurposed for other operators once they are withdrawn.

### Example
The following example demonstrates the calling syntax.

```apl
      ⎕USING←''

      ⍝ I-Beam call is parenthesised
      IntList←System.Collections.Generic.List (43⌶632) System.Int32

      ⍝ Result of I-Beam call is named
      GenOp←43⌶632
      CharList←System.Collections.Generic.List GenOp System.Char
```

### 632 - Generics Operator
The generics operator is used to deal with generic .NET classes and methods. It can create concrete versions of generic classes, and execute generic methods.

For more information, see the .NET interface guide.
