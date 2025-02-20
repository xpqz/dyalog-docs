<h1 class="heading"><span class="name">Value Get</span> <span class="command">R←{X}⎕VGET Y</span></h1>

`⎕VGET` is a system function that allows reading the values of names in a source namespace or source namespaces, optionally with a fallback value for the cases where the name requested is undefined.

`Y` is either a specification of names in a name matrix, a vector of names, or nameclasses. In the first two cases, `Y` can contain fallback values as well, which is used when the name has nameclass 0, instead of producing a `VALUE ERROR`. Each of the three cases are described in the sections below. In all cases, the values requested must have nameclass 0, 1, 2, 8 or 9 in the source namespace.

If `X` is specified, it must be an array that references one or more source namespaces. The possible values are the same as those allowed for [`⎕NS`](ns.md). The namespace(s) referenced must already exist, or a `VALUE ERROR` is produced. If `X` is not specified, the source namespace is the current namespace.

The result `R` depends on the format of `Y`.

See also [`⎕VSET`](vset.md).

## Multiple namespace `X`

When `X` refers to multiple namespaces, the system function processes each item of `X` in ravel order, using the entire right argument `Y`.
Except when `X` is empty, this is equivalent to `R←X ⎕VGET¨⊂Y`.

The rest of this document describes `⎕VGET` using a single source namespace, as if the left argument is not specified, or contains a single namespace name or reference.

## Case 1: Name matrix

Names are specified as rows in a character matrix.
`Y` must be either:

* a character matrix, where each row is a name.
* a two element vector, where the first item is a character matrix of names, and the second item is a specification of fallback values.

The fallback values must either be a vector with as many elements as there are names in the matrix, or it must be a scalar value which is used as the fallback value for all names.

The result `R` is a vector of the values from the corresponding names or fallback values.

<h3 class="example">Examples</h3>

Names without fallback:

```apl
      (name1 name2 name3 longer_name)←(1 2 3) () 'APL' 42
      names←↑'name1' 'name2' 'name3' 'longer_name'
      names
name1
name2
name3
longer_name
      ⎕VGET names
 1 2 3  #.[Namespace]  APL  42
```

Names with different fallback for each name:

```apl
      name2←100
      names←↑'name1' 'name2' 'name3'
      names
name1
name2
name3
      defaults←1 2 3
      ⎕vget names defaults
1 100 3
```

Names with the same fallback for all of them:

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

## Case 2: Vector of names

Names are specified as character vectors or scalars. `Y` must be either:

* a single name. In this case, the result `R` is the value of that name in the source namespace.
* a single enclosed name. In this case, the result `R` is also the value of the name, but enclosed.
* a single enclosed name-value pair, which is a two-element vector consisting of a character vector name and a fallback value for that name. In this case, the result `R` is the value of the name, or the fallback value in case the name has nameclass 0.
* a nested vector where each item is either a name, or a name value pair. In this case, the result `R` is a vector with the same length as `Y`, with the values from the corresponding names, or fallback values.

<h3 class="example">Examples</h3>

Single name:
```apl
      (ns1 ns2)←()()
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

Multiple names without fallback:
```apl
      (name1 name2 name3)←(1 2 3) () 'APL'

      ⎕VGET 'name1' 'name2' 'name3'
 1 2 3  #.[Namespace]  APL
```

Single name with fallback:
```apl
      ns←()
      ns ⎕VGET ⊂'name1' 'default'
default
```

Multiple names with fallback for some:
```apl
      (name1 name2)←'APL' 123
      ⎕VGET ('name1' 1) 'name2' ('name3' 3)
 APL  123 3
      ⎕EX'name1'
      ⎕VGET ('name1' 1) 'name2' ('name3' 3)
1 123 3
```

Multiple names with different fallback for each of them:
```apl
      name2←100
      ⎕VGET ('name1' 1) ('name2' 2) ('name3' 3)
1 100 3
```

## Case 3: Nameclasses

`Y` must be a numeric scalar or vector, where each item is a nameclass (see [Name Classification](nc.md)).

If any of the numbers in `Y` are negative, the result `R` is a vector of name-value pairs, one per existing name in the source namespace with a nameclass from `Y`. Otherwise, the result is a two-element nested vector, where the first element is a character matrix of names, and the second element is a vector of values. Both of the result formats are suitable as arguments for [`⎕VGET`](vget.md) and [`⎕VSET`](vset.md).

<h3 class="example">Examples</h3>
Name value pairs:

```apl
      ns←()
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
