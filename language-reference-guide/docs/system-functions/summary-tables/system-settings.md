<h1 class="heading"><span class="name"> System Settings</span></h1>

### Settings Affecting Behaviour of Primitive Functions

|Name  |Description                  |
|------|-----------------------------|
|`⎕CT` |Comparison Tolerance         |
|`⎕DCT`|Decimal Comp Tolerance       |
|`⎕DIV`|Division Method              |
|`⎕FR` |Floating-Point Representation|
|`⎕IO` |Index Origin                 |
|`⎕ML` |Migration Level              |
|`⎕PP` |Print Precision              |
|`⎕RL` |Random Link                  |

The following table describes the dependencies that exist between functions, operators and these system variables.

Implicit Arguments

|System Variable|Monadic Functions|Dyadic Functions|Operators|
|---|---|---|---|
|`⎕CT, ⎕DCT`|`⌈ ⌊ ∪`|`~ < ≤ = ≥ > ≠ ≡ ≢ ⍳ ∊ ∪ ∩ ⍷ | ∨ ∧`|`⌸`|
|`⎕DIV`|`÷`|`÷`|&nbsp;|
|`⎕FR   ⍝ 1`|`÷ * ⍟ ! ○ ⌹`|`+ - × ÷ * ⍟ | ! ○ ∨ ∧ ⊥ ⊤ ⌹`|&nbsp;|
|`⎕FR   ⍝ 2`|`⌈ ⌊ ∪`|`~ < ≤ = ≥ > ≠ ≡ ≢ ⍳ ∊ ∪ ∩ ⍷`|`⌸`|
|`⎕FR   ⍝ 3`|`⍒ ⍋`|`⌈ ⌊ ⍒ ⍋ ⍸`|&nbsp;|
|`⎕IO`|`⍳ ? ⍒ ⍋ ⍸`|`⍳ ? ⍒ ⍋ ⍉ ⊃ ⌷ ⍸`|`⌸ @ []`|
|`⎕ML`|`∊ ↑ ⊃ ≡`|&nbsp;|&nbsp;|
|`⎕PP`|`⍕`|&nbsp;|&nbsp;|
|`⎕RL`|`?`|`?`|&nbsp;|

where, for `⎕FR`, `1` indicates functions that compute real numbers and whose precision depends on `⎕FR`, `2` indicates functions that perform tolerant comparisons and `3` indicates functions that perform tolerant comparisons.

NOTE: Tolerant comparisons depend on `⎕FR` to select which of `⎕CT` and `⎕DCT` is used; `⎕FR` also determines the precision of the comparison computation that can affect results. However, even primitives involving intolerant comparison (including the tolerant ones with all comparison tolerances set to 0) can depend on `⎕FR` if the argument contains DECFs. This is because DECFs must be converted to doubles for comparison. If two DECFs are different but correspond to the same double, then they will be treated as intolerantly unequal when `⎕FR` is `1287` but equal when it is `645`.
