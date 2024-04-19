




<h1 class="heading"><span class="name">Continue Autosave</span><span class="command">{R}←2704⌶Y</span></h1>



This function enables or disables the automatic saving of a `CONTINUE` workspace when Dyalog exits. By default this is disabled when Dyalog starts and must be explicitly enabled using this function.


`Y` is an integer defined as follows:


| Value | Description |
| --- | ---  |
| 0 | Disable the automatic saving of a `CONTINUE` workspace. |
| 1 | Enable the automatic saving of a `CONTINUE` workspace. This setting applies only to the current session or until disabled by `2704⌶0` . |



The shy result `R` is the previous value of this setting.



Circumstances when Dyalog automatically saves a `CONTINUE` workspace include:

- a run-time violation. This is most frequently caused by an untrapped APL error which causes Dyalog to return to session-input mode (i.e. an application programming fault).
- a hang-up signal.



