<h1> :If Statement</h1>

```
 
       |
       :If bexp
       |
       .-------.
       |       |
       |       andor
       |       |
       |<------'
       |
       code
       |
       |<------------------------------.
       |                               |
       .-------.-------.               |
       |       |       |               |
       |       :Else   :ElseIf bexp    |
       |       |       |               |
       |       |       .-------.       |
       |       |       |       |       |
       |       |       |       andor   |
       |       |       |       |       |
       |       |       |<------'       |
       |       |       |               |
       |       code    code            |
       |       |       |               |
       |<------'       `---------------'
       |
       :End[If]
       |
```
