




<h1 class="heading"><span class="name">APLVersion</span> <span class="command">Property</span></h1>



|-----------|--------------------------|
|Applies To:|[Root](../objects/root.md)|


**Description**


This is a read-only property that provides information about the Version of Dyalog APL that you are using. It is
a 4-element vector of character vectors as described in the table below. In future releases these values may change, be removed, or new ones added.


|Index|Description              |Possible Values                                                                                                                         |||||||||
|-----|-------------------------|------------------------------------------------------------------------------|---|-------|---|-------------------------|---|-----|---|---------|
|`[1]`|Target Environment       |`WindowsWindows-64Windows MobileLinuxLinux-64AIXAIX-64Mac-64SolarisSolaris-64`                                                          |||||||||
|`[2]`|Version Number           |&nbsp;                                                                                                                                  |||||||||
|`[3]`|Version Type             |`W` Windows `S` Server (terminal) version `M` Motif `P` PocketAPL             |`W`|Windows|`S`|Server (terminal) version|`M`|Motif|`P`|PocketAPL|
|`W`  |Windows                                                                                                                                                          ||||||||||
|`S`  |Server (terminal) version                                                                                                                                        ||||||||||
|`M`  |Motif                                                                                                                                                            ||||||||||
|`P`  |PocketAPL                                                                                                                                                        ||||||||||
|`[4]`|Program Type             |`DevelopmentRuntimeDLLDLLRT`                                                                                                            |||||||||

<h2 class="example">Example</h2>
```apl
      '.'⎕WG'APLVersion'
┌──────────┬────────────┬─┬───────────┐
│Windows-64│18.0.38434.0│W│Development│
└──────────┴────────────┴─┴───────────┘

```



