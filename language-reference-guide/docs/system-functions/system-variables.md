<h1 class="heading"><span class="name">System Variables</span></h1>

System variables retain information used by the system in some way. Many system variables affect the behaviour of primitive functions and operators to which they act as *implicit arguments* For further information, see [System Settings](system-settings.md).

System variables may be localised by inclusion in the header line of a defined function or in the argument list of the system function `⎕SHADOW`. When a system variable is localised, it retains its previous value until it is assigned a new one. This feature is known as "pass-through localisation".  The exception to this rule is `⎕TRAP`.

A system variable can never be undefined. Default values are assigned to all system variables in a clear workspace.

|Name    |Description                  |Scope    |
|--------|-----------------------------|---------|
|`⎕AVU`  |Atomic Vector – Unicode      |Namespace|
|`⎕CT`   |Comparison Tolerance         |Namespace|
|`⎕DCT`  |Decimal Comp Tolerance       |Namespace|
|`⎕DIV`  |Division Method              |Namespace|
|`⎕FR`   |Floating-Point Representation|Namespace|
|`⎕IO`   |Index Origin                 |Namespace|
|`⎕LX`   |Latent Expression            |Workspace|
|`⎕ML`   |Migration Level              |Namespace|
|`⎕PATH` |Search Path                  |Session  |
|`⎕PP`   |Print Precision              |Namespace|
|`⎕PW`   |Print Width                  |Session  |
|`⎕RL`   |Random Link                  |Namespace|
|`⎕RTL`  |Response Time Limit          |Namespace|
|`⎕SM`   |Screen Map                   |Workspace|
|`⎕TNAME`|Thread Name                  |Workspace|
|`⎕TRAP` |Event Trap                   |Workspace|
|`⎕USING`|Microsoft .NET Search Path   |Namespace|
|`⎕WSID` |Workspace ID                 |Workspace|
|`⎕WX`   |Window Expose                |Namespace|

In other words,  `⎕PATH` and `⎕PW` relate to the session.  `⎕LX`, `⎕SM`, `⎕TRAP` and `⎕WSID` relate to the active workspace.  All the other system variables relate to the current namespace.

|Session|Workspace|Namespace|
|-------|---------|---------|
|`⎕PATH`|`⎕LX`    |`⎕AVU`   |
|`⎕PW`  |`⎕SM`    |`⎕CT`    |
|&nbsp; |`⎕TRAP`  |`⎕DCT`   |
|&nbsp; |`⎕WSID`  |`⎕DIV`   |
|&nbsp; |&nbsp;   |`⎕FR`    |
|&nbsp; |&nbsp;   |`⎕IO`    |
|&nbsp; |&nbsp;   |`⎕ML`    |
|&nbsp; |&nbsp;   |`⎕PP`    |
|&nbsp; |&nbsp;   |`⎕RL`    |
|&nbsp; |&nbsp;   |`⎕RTL`   |
|&nbsp; |&nbsp;   |`⎕USING` |
|&nbsp; |&nbsp;   |`⎕WX`    |

Note that the value assigned to a system variable must be appropriate; otherwise an error will be reported immediately.

<h2 class="example">Example</h2>
```apl
      ⎕IO←3
DOMAIN ERROR
      ⎕IO←3
      ^
```
