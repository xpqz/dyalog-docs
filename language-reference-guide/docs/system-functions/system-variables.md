<h1 class="heading"><span class="name"> System Variables</span></h1>

System variables retain information used by the system in some way. Many system variables affect the behaviour of primitive functions and operators to which they act as *implicit arguments* For further information, see [System Settings](system-settings.md).

System variables may be localised by inclusion in the header line of a defined function or in the argument list of the system function `⎕SHADOW`. When a system variable is localised, it retains its previous value until it is assigned a new one. This feature is known as "pass-through localisation".  The exception to this rule is `⎕TRAP`.

A system variable can never be undefined. Default values are assigned to all system variables in a clear workspace.

| Name | Description | Scope |
| --- | --- | ---  |
| [⎕AVU](./avu.md) | Atomic Vector – Unicode | Namespace |
| [⎕CT](../primitive-functions/subtract.md) | Comparison Tolerance | Namespace |
| [⎕DCT](./dct.md) | Decimal Comp Tolerance | Namespace |
| [⎕DIV](./div.md) | Division Method | Namespace |
| [⎕FR](./fr.md) | Floating-Point Representation | Namespace |
| [⎕IO](./io.md) | Index Origin | Namespace |
| [⎕LX](./lx.md) | Latent Expression | Workspace |
| [⎕ML](./ml.md) | Migration Level | Namespace |
| [⎕PATH](./path.md) | Search Path | Session |
| [⎕PP](./pp.md) | Print Precision | Namespace |
| [⎕PW](./pw.md) | Print Width | Session |
| [⎕RL](./rl.md) | Random Link | Namespace |
| [⎕RTL](./rtl.md) | Response Time Limit | Namespace |
| [⎕SM](./sm.md) | Screen Map | Workspace |
| [⎕TNAME](./tname.md) | Thread Name | Workspace |
| [⎕TRAP](./trap.md) | Event Trap | Workspace |
| [⎕USING](./using.md) | Microsoft .NET Search Path | Namespace |
| [⎕WSID](./wsid.md) | Workspace ID | Workspace |
| [⎕WX](./wx.md) | Window Expose | Namespace |

In other words,  `⎕PATH` and `⎕PW` relate to the session.  `⎕LX`, `⎕SM`, `⎕TRAP` and `⎕WSID` relate to the active workspace.  All the other system variables relate to the current namespace.

| Session | Workspace | Namespace |
| --- | --- | ---  |
| [⎕PATH](./path.md) | [⎕LX](./lx.md) | [⎕AVU](./avu.md) |
| [⎕PW](./pw.md) | [⎕SM](./sm.md) | [⎕CT](../primitive-functions/subtract.md) |
|  | [⎕TRAP](./trap.md) | [⎕DCT](./dct.md) |
|  | [⎕WSID](./wsid.md) | [⎕DIV](./div.md) |
|  |  | [⎕FR](./fr.md) |
|  |  | [⎕IO](./io.md) |
|  |  | [⎕ML](./ml.md) |
|  |  | [⎕PP](./pp.md) |
|  |  | [⎕RL](./rl.md) |
|  |  | [⎕RTL](./rtl.md) |
|  |  | [⎕USING](./using.md) |
|  |  | [⎕WX](./wx.md) |

Note that the value assigned to a system variable must be appropriate; otherwise an error will be reported immediately.

**Example**

```apl
      ⎕IO←3
DOMAIN ERROR
      ⎕IO←3
      ^
```
