<h1 class="heading"><span class="name">JSON Import</span> <span class="command">R←0⎕JSON Y</span></h1>

`Y` is a character vector or matrix in JSON format. There is an implied newline character between each row of a matrix.
                    
The content of the result `R` depends upon the `Format` variant, which can be`'D'` (the default) or`'M'`. 
                        
If `Format` is`'D'` (which stands for "data") the JSON described by `Y` is converted to APL object(s) and `R` is an array or a namespace containing arrays and sub-namespaces.

- JSON objects are created as APL namespaces.
- JSON null is converted to  the value specified by the `Null` variant, which may be either `⊂'null'` (the default) or `⎕NULL`.
- JSON true and false and the JSON5 numeric constants `Infinity`, `-Infinity`, `NaN` and `-NaN` are converted to enclosed character vectors `⊂'true'`,`⊂'false'` and so forth.
- If the JSON source contains object names which are not valid APL names they are converted to APL objects with mangled names. See [JSON Name Mangling](name-mangling.md). `7162⌶` can be used to obtain the original name. See [JSON Translate Name](../../../the-i-beam-operator/json-translate-name)
                        
If `Format` is`'M'` (which stands for "matrix") the result `R` is a matrix whose columns contain the following:

|------|-------------------------------|
| [;1] | depth                         |
| [;2] | name (for JSON object members)|
| [;3] | value                         |
| [;4] | JSON type (integer: see below)|

- The representation of null, true and false are the same as for `Format 'D'`.
- Object names are reported as specified in the JSON text; they are not mangled as they are for `Format 'D'`.

| Type | Description                                           |
|------|-------------------------------------------------------|
| 1    | Object                                                |
| 2    | Array                                                 |
| 3    | Numeric                                               |
| 4    | String                                                |
| 5    | Null                                                  |
| 6    | No APL equivalent (represented by character string)   |
| 7    | JavaScript Object (export only)                       |

**Duplicate Names**
                        
The JSON standard says that members of a JSON object should have unique names and that different implementations behave differently when there are duplicates. Dyalog handles duplicate names as follows:

- No error is generated.
- For `Format 'D'`, the last member encountered is used and all previous members with the same name are discarded.
- For `Format 'M'` all duplicate members are recorded in the result matrix.
                        
**Examples**

```apl
18 19
        JSON
{                  
    "a": {           
        "b": [         
            "string 1",
            "string 2"
        ],
        "c": true,     
        "d": {         
            "e": false,  
            "f⍺": [       
                "string 3",
                123,       
                1000.2,    
                null       
            ]            
        }              
    }                
}
```

## Import as Data (`Format 'D'`)
```apl
        j←0 ⎕JSON JSON
        j
#.[JSON object]
        j.⎕NL 9
a
        j.a.⎕NL 2
b
c
        j.a.b
┌────────┬────────┐
│string 1│string 2│
└────────┴────────┘
        j.a.c
┌────┐
│true│
└────┘
        j.a.⎕NL 9
d
        j.a.d.⎕NL 2 ⍝ Note that f⍺ is an invalid APL name
e       
⍙f⍙9082⍙
        j.a.d.e
┌─────┐
│false│
└─────┘
        j.a.d.⍙f⍙9082⍙
┌────────┬───┬──────┬──────┐
│string 3│123│1000.2│┌────┐│
│        │   │      ││null││
│        │   │      │└────┘│
└────────┴───┴──────┴──────┘
```

**Performance Warning**
                            
Extracting part of a namespace created by `⎕JSON` can lead to poor application performance. For example, if you are only interested in an array of records contained as child namespaces that are nested within data that you receive via `⎕JSON`, you might write something like:

```apl
data←(0 ⎕JSON ⊃⎕NGET filename).records
```
                            
This expression actually creates a temporary namespace `(0 ⎕JSON ⊃⎕NGET filename)` (lets call it `temp` for now), extracts the sub-namespace `records`, and then discards its parent namespace `temp`. The result `data` however contains pointers to `temp`, so although it is not visible (it is unnamed), it is retained internally in the workspace. This can lead to poor performance due to the behaviour of the memory manager in this situation. This issue will be resolved in the next release of Dyalog. In the meantime, the situation can be avoided by assigning a name to the  top-level namespace. Instead of the expression above, you could write:

```apl
dataset←0 ⎕JSON ⊃⎕NGET filename
data←dataset.records
```
                        
Giving a name to the top-level namespace effectively avoids the performance issue.

## Import as Matrix (`Format 'M'`)

```apl
    (⎕JSON⍠'M')JSON
┌─┬──┬────────┬─┐
│0│  │        │1│
├─┼──┼────────┼─┤
│1│a │        │1│
├─┼──┼────────┼─┤
│2│b │        │2│
├─┼──┼────────┼─┤
│3│  │string 1│4│
├─┼──┼────────┼─┤
│3│  │string 2│4│
├─┼──┼────────┼─┤
│2│c │┌────┐  │6│
│ │  ││true│  │ │
│ │  │└────┘  │ │
├─┼──┼────────┼─┤
│2│d │        │1│
├─┼──┼────────┼─┤
│3│e │┌─────┐ │6│
│ │  ││false│ │ │
│ │  │└─────┘ │ │
├─┼──┼────────┼─┤
│3│f⍺│        │2│
├─┼──┼────────┼─┤
│4│  │string 3│4│
├─┼──┼────────┼─┤
│4│  │123     │3│
├─┼──┼────────┼─┤
│4│  │1000.2  │3│
├─┼──┼────────┼─┤
│4│  │┌────┐  │5│
│ │  ││null│  │ │
│ │  │└────┘  │ │
└─┴──┴────────┴─┘
```
