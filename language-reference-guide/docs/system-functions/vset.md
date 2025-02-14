<h1 class="heading"><span class="name">Value Set</span> <span class="command">{R}←{X}⎕VSET Y</span></h1>

`⎕VSET` is a system function that allows setting the values of variables in a target namespace or target namespaces.

`Y` is a specification of the variable names, and their values. Several formats are allowed. In all cases, the names are character arrays, and the values are arrays or references to namespaces. The possible formats for `Y` are listed below.

* A nested vector or scalar, where each element is a name-value pair. The name must be a simple character scalar or vector.
* A two-element nested array, where the first element is a matrix of names, and the second element is a vector or scalar of value(s). If multiple names are specified, and the value is a scalar, the same value is used for all names.

All names must have nameclass 0, 2, 8 or 9 in the target namespace(s).

If `X` is specified, it must be an array that references one or more target namespaces. The possible values are the same as those allowed for [`⎕NS`](ns.md). The namespace(s) referenced must already exist, or a `VALUE ERROR` is produced. If `X` is not specified, the target namespace is the current namespace.

The result `R` is a shy reference to the target namespace(s).

See also [`⎕VGET`](vget.md).

## Examples

Name value pairs:

```apl
      ⎕VSET ('name1' 123) ('name2' (1 2 'hello'))
      name1
123
      name2
1 2  hello

      (ns1 ns2 ns3)←⎕NS¨⍬⍬⍬
      ns1 'ns2' ns3⎕VSET ('X' 'X value') ('Y' 'Y value')
      (ns1 ns2 ns3).(X Y)
  X value  Y value    X value  Y value    X value  Y value
```

Name matrix and value vector:

```apl
      names←↑'name1' 'name2' 'name3'
      names
name1
name2
name3
      values←1 2 3
      ⎕VSET names values
      name1 name2 name3
1 2 3
```

Single name-value pair:

```apl
      ⎕VSET ⊂'name1' (10 20 30)
      ⎕VSET ,⊂'name2' (40 50 60)
      name1
10 20 30
      name2
40 50 60
```

Multiple names, with a single value:

```apl
      names←↑'name1' 'name2' 'name3'
      value←'APL'

      ⎕VSET names (⊂value)
      name1 name2 name3
 APL  APL  APL
```
## Variant Options

`⎕VSET` supports a single variant option `'Trigger'`.

### Trigger

For a description of the Trigger variant option, see [`⎕NS`](ns.md#trigger).

<h4 class="example">Example</h4>
```apl
      ⎕VR 'trigger'
     ∇trigger arg
[1]   :Implements Trigger X,Y
[2]   ⎕←'Running trigger for: ',arg.Name
     ∇

      ⍝ X has a trigger, Z does not
      X←1
Running trigger for: X
      Z←2

      ⍝ Without the trigger option, triggers are not run by ⎕VSET
      ⎕VSET ('X' 1) ('Z' 2) ('Y' 3)
      ⎕VSET⍠'Trigger' 0⊢('X' 1) ('Z' 2) ('Y' 3)

      ⍝ With the trigger option enabled, triggers are run
      ⎕VSET⍠'Trigger' 1⊢('X' 1) ('Z' 2) ('Y' 3)
Running trigger for: X
Running trigger for: Y
```