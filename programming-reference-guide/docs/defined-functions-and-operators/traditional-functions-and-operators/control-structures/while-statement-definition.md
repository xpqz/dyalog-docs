<h1 class="heading"><span class="name"> :While Statement</span></h1>

```apl
 
       |
       :While bexp
       |
       .-------.
       |       |
       |       andor
       |       |
       |<------'
       |
       code
       |
       .---------------.
       |               |
       :End[While]     :Until bexp
       |               |
       |               .-------.
       |               |       |
       |               |       andor
       |               |       |
       |               |<------'
       |               |
       |<--------------'
       |
```
