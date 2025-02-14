<h1 class="heading"><span class="name">Value Get</span> <span class="command">R←{X}⎕VGET Y</span></h1>

`⎕VGET` is a system function that allows reading the values of variables in a source namespace or source namespaces, optionally with a fallback value for the cases where the variable requested is undefined.

`Y` is either a specification of variable names, variable names with fallback values, or nameclasses. Each of those three cases are described in the sections below. In all cases, the values requested must have nameclass 0, 1, 2, 8 or 9 in the source namespace.

If `X` is specified, it must be an array that references one or more source namespaces. The possible values are the same as those allowed for [`⎕NS`](ns.md). The namespace(s) referenced must already exist, or a `VALUE ERROR` is produced. If `X` is not specified, the source namespace is the current namespace.

The result `R` depends on the format of `Y`.

See also [`⎕VSET`](vset.md).

## Nested `X`

When `X` is nested, the system function processes each item of `X` in ravel order, using the entire right argument `Y`. That means that when `X` is nested, the system function is equivalent to `R←X ⎕VGET¨⊂Y`.

The rest of this document describes `⎕VGET` using a single source namespace, as if the left argument is not specified, or it is not nested.

## Case 1: Values without Fallback

In the first case, `Y` must be either:

* a simple character vector or scalar, representing a single variable name. `R` is the value of the variable with that name.
* a nested vector or scalar, where each item is one of the above. `R` is a nested array with the same shape as `Y`, where each item is the value of the variable with the corresponding name.
* a character matrix, where each row represents a variable name. `R` is a vector of the values of the variables with the corresponding names from the matrix, one item for each row of the name matrix.

<h3 class="example">Examples</h3>
Single name:

```apl
      (ns1 ns2)←⎕NS¨⍬⍬
      (ns1 ns2).name1←'ABC' 'DEF'

      ns1 ⎕VGET 'name1'
ABC
      ns1 'ns2' ⎕VGET 'name1'
 ABC  DEF
```

Single name enclosed:

```apl
      name1←'APL'
      ⎕VGET ⊂'name1'
 APL
      ≢⍴⎕VGET ⊂'name1'
0
```

Multiple names as a vector:

```apl
      (name1 name2 name3)←(1 2 3) (⎕NS⍬) 'APL'

      ⎕VGET 'name1' 'name2' 'name3'
 1 2 3  #.[Namespace]  APL
```

Multiple names as a matrix:

```apl
      (name1 name2 name3 longer_name)←(1 2 3) (⎕NS⍬) 'APL' 42
      names←↑'name1' 'name2' 'name3' 'longer_name'
      names
name1
name2
name3
longer_name
      ⎕VGET names
 1 2 3  #.[Namespace]  APL  42
```

## Case 2: Values with Fallback

In the second case, `Y` must be either:

* a vector or scalar of name-value pairs. The values are the default values for the corresponding names.
* a vector of a combination of names and name-value pairs. Only the names with a corresponding value will have a default value associated with them.
* a two element vector, where the first item is a character matrix of names, and the second item is either a vector or scalar of default value(s). In the scalar case, all names have the same default value, and otherwise each item of the vector is a default value for the name in the matrix where the row is equal to the vector index.

The name lookup and result `R` structure is the same as in [case 1](#case-1-values-without-fallback), but when a name refers to a variable with nameclass 0, the default value is used instead of producing a `VALUE ERROR`.

<h3 class="example">Examples</h3>

Single name with fallback:
```apl
      ns←⎕NS⍬
      ns ⎕VGET ⊂'name1' 'default'
default
```

Multiple names with fallback for some:

```apl
      (name1 name2)←'APL' 123
      ⎕vget ('name1' 1) 'name2' ('name3' 3)
 APL  123 3
      ⎕EX'name1'
      ⎕vget ('name1' 1) 'name2' ('name3' 3)
1 123 3
```

Multiple names with different fallback for each of them:
```apl
      name2←100
      ⎕VGET ('name1' 1) ('name2' 2) ('name3' 3)
1 100 3

      names←↑'name1' 'name2' 'name3'
      names
name1
name2
name3
      defaults←1 2 3
      ⎕vget names defaults
1 100 3
```

Multiple names with the same fallback for all of them:

```apl
      persons←(
        (name: 'Jack' ⋄ age: 36)
        (name: 'Peter' ⋄ email: 'peter@example.com')
        (phone: 12345678 ⋄ email: 'susan@example.com')
      )
      persons
 #.[Namespace]  #.[Namespace]  #.[Namespace]
      names←↑'name' 'age' 'email' 'phone'
      names
name
age
email
phone

      ⍝ Lookup information about each person, with a default for missing data
      ↑persons ⎕VGET names (⊂'<no data>')
 Jack              36  <no data>          <no data>
 Peter      <no data>  peter@example.com  <no data>
 <no data>  <no data>  susan@example.com   12345678
```

## Case 3: Names with Values

In the third case, `Y` must be a numeric scalar or vector, where each item is a nameclass (see [Name Classification](nc.md)).

If any of the numbers in `Y` are negative, the result `R` is a vector of name-value pairs, one per existing name in the source namespace with a nameclass from `Y`. Otherwise, the result is a two-element nested vector, where the first element is a character matrix of names, and the second element is a vector of values.

<h3 class="example">Examples</h3>
Name value pairs:

```apl
      ns←⎕NS⍬
      ns.ns1←⎕SE
      ns.ns2←#
      ns.a1←1 2 3
      ns.a2←'APL'
      ns ⎕VGET ¯2
  a1  1 2 3    a2  APL
      ns ⎕VGET ¯2 ¯9
  a1  1 2 3    a2  APL    ns1  ⎕SE    ns2  #
      ↑⎕SE ⎕VGET ¯8
 onClose            0
 onCreate            Dyalog.Callbacks.SECreate
 onFontOK           0
 onFontCancel       0
 onWorkspaceLoaded   Dyalog.Callbacks.WSLoaded
 onSessionPrint     0
 onSessionTrace     0


      ÷0
DOMAIN ERROR: Divide by zero
      ÷0
      ∧
      ↑⎕DMX ⎕VGET ¯2
 Category                                             General
 DM                          DOMAIN ERROR        ÷0        ∧
 EM                                              DOMAIN ERROR
 EN                                                        11
 ENX                                                        1
 HelpURL           https://help.dyalog.com/dmx/20.0/General/1
 InternalLocation                              scalm.cpp  356
 Message                                       Divide by zero
 OSError                                               0 0
 Vendor                                                Dyalog
```

Name matrix and value vector:

```apl
      ]box on
Was OFF
      (name1 name2 name3)←'APL' (1 2 3) ⎕SE
      ⎕VGET 2 9
┌─────┬─────────────────┐
│name1│┌───┬─────┬─────┐│
│name2││APL│1 2 3│ ⎕SE ││
│name3│└───┴─────┴─────┘│
└─────┴─────────────────┘
```
