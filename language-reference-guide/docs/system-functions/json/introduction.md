<h1 class="heading"><span class="name">JSON Convert</span> <span class="command">R←{X}⎕JSON Y</span></h1>

This function imports and exports data in [JavaScript Object Notation](https://www.json.org/json-en.html) (JSON) Data Interchange Format[^1].

JSON supports a limited number of data types and there is not a direct correspondence between JSON and APL data structures. In particular:

- JSON does not support arrays with rank &gt;1.
- JSON standard includes Boolean values true and false which are distinct from numeric values 1 and 0, and have no direct APL equivalent.
- The [JSON5](https://json5.org/) standard includes numeric constants `Infinity`, `-Infinity`, `NaN` and `-NaN` which have no direct APL equivalent.
- JSON object members are named and these names might not be valid names in APL.
                
These differences are catered for in various ways as discussed below.

If specified, `X` must be a numeric scalar with the value `0` (import JSON) or `1` (export JSON). If `X` is not specified and `Y` is a character array, `X` is assumed to be `0` (import); otherwise it is assumed to be 1 (export).
                
Although this system function was designed with an optional left argument, it is strongly recommended that the argument should always be used.
                
Other options for `⎕JSON` are `Format`, `Compact`, `Null`, `HighRank`, `Charset` and `Dialect` which are specified using the [Variant operator](../../../primitive-operators/variant), `⍠`. The Principal Option is `Format`.
                
The `Dialect` Variant option is either `'JSON'` (the default) or `'JSON5'`. The latter enables [JSON5](https://json5.org/) extensions on import and export[^2].
                
See also: [JSON Name Mangling](name-mangling.md).


- [JSON Import (X is 0)](import.md)
- [JSON Export (X is 0)](export.md)


[^1]: IETF RFC 7159. The JavaScript Object Notation (JSON) Data Interchange Format is a widely supported, text based data interchange format for the portable representation of structured data; any application which conforms to the standard may exchange data with any other.

[^2]: JSON5 (JSON5 Data Interchange Format) is an extension of JSON that extends the subset of JavaScript syntax to include
optional trailing commas, unquoted object keys, single quoted and multiline strings, additional number formats, and
comments.