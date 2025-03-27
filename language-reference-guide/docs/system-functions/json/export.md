<h1 class="heading"><span class="name">JSON Import</span> <span class="command">R←1⎕JSON Y</span></h1>
                        
`Y` is the data to be exported as JSON and may be an array, a namespace or a matrix representation of JSON such as would have been produced by JSON Import with `Format 'M'`.`Y` is interpreted according to the `Format` variant which may be`'D'` (the default) or`'M'`.
                    
`⎕JSON` will signal `DOMAIN ERROR` if `Y` is incompatible with the specified (or implied) value of `Format`.
                        
If `Format` is`M`, the data values in `Y[;3]` must correspond precisely with the JSON types specified in`Y[;4] `as specified in the following table.

| `Y[;4]` (Type) | `Y[;3]` (Value)             |
|----------------|-----------------------------|
| 1              | Empty array                 |
| 2              | Empty array                 |
| 3              | Numeric scalar              |
| 4              | Character vector            |
| 5              | Null                        |
| 6              | Enclosed character vector   |
| 7              | Enclose character vector    |

                    
`R` is a character vector whose content depends upon the value of the `Compact` variant.

| Compact | Description                                                      |
|---------|------------------------------------------------------------------|
| 0       | The JSON text is padded with spaces and new lines for readability. |
| 1       | The JSON text is compacted into its minimal form.                |

The `Charset` variant option may be used to restrict the output to ASCII characters. 
                    
| Charset    | Description |
|------------|-----------------|
| 'Unicode' | All Unicode characters in `Y` are passed unchanged in the result `R`. |
| 'ASCII' | Non-ASCII characters are converted to an encoded string of the form "\uNNNN" where "NNNN" is the upper-case hexadecimal value of the character in the Unicode system. For example, é (e-acute) is converted to "\u00E9". Furthermore, if the Dialect is JSON5, values less than hex 100 are converted to the form \xNN. |

The `HighRank` variant option may be used to instruct `⎕JSON` to pre-process higher rank arrays into a form that can be represented by JSON. Note that if necessary, the transformation is applied recursively throughout the high-rank array(s) specified by `Y`.

| HighRank | Description                                        |
|----------|----------------------------------------------------|
| 'Split'  | High rank data is split into nested vectors.       |
| 'Error'  | Higher rank data is rejected (`DOMAIN ERROR`)      |

The name of any namespace member that begins with `⍙` and otherwise conforms to the conversion format used for JSON object names will be demangled.
                    
**Example**

```apl
        j             ⍝ See above
#.[JSON object]
        ⍴JS←1 ⎕JSON j
94
        JS
{"a":{"b":["string 1","string 2"],"c":true,"d":{"e":false,"f⍺":["string 3",123,1000.2,null]}}}

        1(⎕JSON⍠'Compact' 0) j

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

If there are any mis-matches between the values in `Y[;3]` and the types in `Y[;4]`, `⎕JSON` will signal `DOMAIN ERROR` and report the first row where there is a mis-match (`⎕IO` sensitive) as illustrated in the following example.

**Example**

```apl      
        M←(⎕JSON⍠'Format' 'M')'{"values": [ 75, 300 ]}'
        M
┌─┬──────┬───┬─┐
│0│      │   │1│
├─┼──────┼───┼─┤
│1│values│   │2│
├─┼──────┼───┼─┤
│2│      │75 │3│
├─┼──────┼───┼─┤
│2│      │300│3│
└─┴──────┴───┴─┘

        M[3;3]←⊂'75' ⍝ character not numeric

        M            ⍝ but looks the same as before

┌─┬──────┬───┬─┐
│0│      │   │1│
├─┼──────┼───┼─┤
│1│values│   │2│
├─┼──────┼───┼─┤
│2│      │75 │3│
├─┼──────┼───┼─┤
│2│      │300│3│
└─┴──────┴───┴─┘

        1 (⎕JSON⍠ 'Format' 'M')M
DOMAIN ERROR: JSON export: value does not match the specified type in row 3 (⎕IO=1)
        1(⎕JSON⍠'Format' 'M')M
        ∧
```

**Charset Example**

```apl
        ns←⎕NS ''
        ns.dé←'DÉ'
        ns.dé
DÉ
        ⎕JSON ns
{"dé":"DÉ"}
        (⎕JSON⍠'Charset' 'ASCII')ns
{"d\u00E9":"D\u00C9"}
```

**High Rank Example**

```apl
        d
┌─────┬─────────────────────────┐
│1 2  │ABC                      │
│A B  │DEF                      │
├─────┼─────────────────────────┤
│1 2 3│1            0.5         │
│4 5 6│0.3333333333 0.25        │
│     │                         │
│     │0.2          0.1666666667│
│     │0.1428571429 0.125       │
└─────┴─────────────────────────┘
        1 ⎕JSON d
DOMAIN ERROR: JSON export: the right argument cannot be converted (⎕IO=1)
        1 ⎕JSON d
        ∧
        1 (⎕JSON⍠'HighRank' 'Split') d
[[[[1,2],"AB"],["ABC","DEF"]],[[[1,2,3],[4,5,6]],...
```

## Raw Text
An enclosed character vector is inserted into the result of JSON export as raw text. This feature may be used to export special JSON values such as `null`, `true` and `false`. Without the extra enclosure, the character vectors are exported as strings:

**Example**

```apl
        ⎕JSON 'null' 'true' 'false'
["null","true","false"]
        ⎕JSON ⊂¨'null' 'true' 'false'
[null,true,false]
```
                        
The same mechanism may be used to inject any raw text, although unless this is valid JSON it cannot then be re-imported.
                        
The following example illustrates how JavaScript objects may be exported. In the example, the object is a JavaScript function which is specified by the contents of an enclosed character vector.

**Example**

```apl
        'Slider' ⎕NS ''
        Slider.range←⊂'true'         ⍝ Note the ⊂
        Slider.min←0
        Slider.max←500
        Slider.values←75 300

        fn1←' function( event, ui ) {'
        fn2←'$( "#amount" ).val( "$" + ui.values[ 0 ] +'
        fn2,←' " - $" + ui.values[ 1 ] );}'
    
        Slider.slide←,/fn1 fn2 ⍝ Enclosed character vec
        ⍴JS←1 ⎕JSON Slider
159
        JS
{"max":500,"min":0,"range":true,"slide": function( event, ui ) {$( \"#amount\" ).val( \"$\" + ui.values[ 0 ] + \" - $\" + ui.values[ 1 ]);},"values":[75,300]}
```

## Wrappers

A wrapper is an enclosed vector of the form:

```apl
        ⊂code special
```
                        
The nature of the `special` data structure is identified within the wrapper by a leading numeric code. Code 1 is used to identify JSON values such as `null`, `true` and `false`. Codes 2, 3 and 4 are used to identify different forms of datasets.
                        
This wrapper mechanism has been chosen to identify special treatment because a scalar enclosure cannot be represented in JSON/JavaScript.
                        
A wrapper may be specified directly in the right argument to `⎕JSON` and/or as part of the array structure specified by the right argument, as a sub-array or in a namespace. This allows a special array to be processed appropriately as part of a general data structure that is to be rendered in JSON notation.

**Wrappers for special JSON values**
                            
Wrappers may be used to export JSON special values such as `null`, `true` and `false` using code 1. This mechanism is supplementary to the use of enclosed character vectors. See **RawText** above.
                            
**Example**

```apl
        ⎕JSON⊂¨(1 'null')(1 'true')(1 'false')
[null,true,false]
```

**Datasets**

The term dataset is used here to mean a collection of data, usually presented in tabular form. Each named column represents a particular variable. Each row corresponds to a given member of the dataset in question. It lists values for each of the variables, such as height and weight of an object.

Datasets are often represented in APL as a collection of variables.

```apl
        Fields←'Item' 'Price' 'Qty'
        Items←'Knife' 'Fork'
        Price←3 4
        Qty←23 45
```

As an aside, note that using this scheme each variable represents an inverted index into the dataset and enables rapid searches.

```apl
        (Price<4)/Items
┌─────┐
│Knife│
└─────┘
```

A conventional way to represent this dataset is as a matrix:

```apl
        Fields⍪⍉↑ Items Price Qty

┌─────┬─────┬───┐
│Item │Price│Qty│
├─────┼─────┼───┤
│Knife│   3 │23 │
├─────┼─────┼───┤
│Fork │   4 │45 │
└─────┴─────┴───┘
```

Another is as a 2-item vector containing the names of the fields and a matrix of their values:

```apl
        (Fields (⍉↑Items Price Qty))

┌────────────────┬────────────┐
│┌────┬─────┬───┐│┌─────┬─┬──┐│
││Item│Price│Qty│││Knife│3│23││
│└────┴─────┴───┘│├─────┼─┼──┤│
│                ││Fork │4│45││
│                │└─────┴─┴──┘│
└────────────────┴────────────┘
```

A third way retains the inverted nature of the data structure, storing the values as a vector. The advantage of this structure is that it consumes significantly less memory compared to the matrix forms, because numeric columns are stored as simple numeric vectors.

```apl
        (Fields (Items Price Qty))

┌────────────────┬────────────────────────┐
│┌────┬─────┬───┐│┌────────────┬───┬─────┐│
││Item│Price│Qty│││┌─────┬────┐│3 4│23 45││
│└────┴─────┴───┘│││Knife│Fork││   │     ││
│                ││└─────┴────┘│   │     ││
│                │└────────────┴───┴─────┘│
└────────────────┴────────────────────────┘
```

In JSON, these three data structures are all expressed as follows:

```json
[
    {
        "Item": "Knife",
        "Price": 3,
        "Qty": 23
    },
    {
        "Item": "Fork",
        "Price": 4,
        "Qty": 45
    }
]
```

<div markdown="1" class="example-block">
**Examples**

```apl
        Fields,[1]↑[1]Items Price Qty

┌─────┬─────┬───┐
│Item │Price│Qty│
├─────┼─────┼───┤
│Knife│3    │23 │
├─────┼─────┼───┤
│Fork │4    │45 │
└─────┴─────┴───┘
        ⎕JSON ⊂ 2 (Fields,[1]↑[1]Items Price Qty)
[{"Item":"Knife","Price":3,"Qty":23},{"Item":"Fork","Price":4,"Qty":45}]
```

Note that if you omit the wrapper the operation fails:

```apl
        ⎕JSON Fields,[1]↑[1]Items Price Qty)

DOMAIN ERROR: JSON export: the right argument cannot be converted (⎕IO=1)
⎕JSON Fields,[1]↑[1]Items Price Qty)
∧
```
</div>
<div markdown="1" class="example-block">
**Further Examples**

```apl
        ⎕JSON ⊂ 3 ((↑[1]Items Price Qty)Fields)
[{"Item":"Knife","Price":3,"Qty":23},{"Item":"Fork","Price":4,"Qty":45}]

        ⎕JSON ⊂ 4 ((Items Price Qty)Fields)
[{"Item":"Knife","Price":3,"Qty":23},{"Item":"Fork","Price":4,"Qty":45}]
```

Note that if you omit the wrapper, the operation generates a different result.

```apl
        ⎕JSON ((Items Price Qty)Fields)
[[["Knife","Fork"],[3,4],[23,45]],["Item","Price","Qty"]]
```
</div>

**Selection**

For codes 2, 3 and 4 the extension also provides the facility to optionally select elements of the dataset, so the array may contain 2, 3 or 4 items:

```apl
        ⊂(code dataset {records} {fields})
```

where records and fields are integer indices that select which fields and which records are to be exported. The following example selects the first record and the first and third fields (Items and Qty)

```apl
        ⎕JSON⊂4 ((Items Price Qty)Fields)1(1 3)
[{"Item":"Knife","Qty":23}]
```

**Namespaces and Sub-Arrays**

Wrappers in namespaces and sub-arrays are recognised for special treatment.

<div markdown="1" class="example-block">
**Example**

```apl
        ns.Items←'Fork' 'Knife'
        ns.Price←3 4
        ns.Qty←23 45
        ns.(ds←⊂4(⌽('Item' 'Price' 'Qty')(Items Price Qty)))
        ⎕JSON ns
{"Items":["Knife","Fork"],"Price":[3,4],"Qty":[23,45],"ds":[{"Item":"Knife","Price":3,"Qty":23},{"Item":"Fork","Price":4,"Qty":45}]}

        a←'the' 'answer' 'is' 42
        a[3]←⊂ns.ds
        ⎕JSON a
["the","answer",[{"Item":"Knife","Price":3,"Qty":23},{"Item":"Fork","Price":4,"Qty":45}],42]
```
</div>