<h1> :Select Statement</h1>

```
 
       |
       :Select aexp
       |
       |<----------------------------------------------.
       |                                               |
       .-------.-------.---------------.               |
       |       |       |               |               |
       |       :Else   :Case aexp      :CaseList aexp  |
       |       |       |               |               |
       |       |       |<--------------'               |
       |       |       |                               |
       |       code    code                            |
       |       |       |                               |
       |<------'       `-------------------------------'
       |
       :End[Select]
```