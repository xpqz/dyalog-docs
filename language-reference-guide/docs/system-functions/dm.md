




<h1 class="heading"><span class="name">Diagnostic Message</span><span class="command">R←⎕DM</span></h1>



This niladic function returns the last reported APL error as a three-element vector, giving error message, line in error and position of caret pointer.



**Example**

```apl

      2÷0
DOMAIN ERROR
      2÷0
     ^

      ⎕DM
 DOMAIN ERROR        2÷0       ^
```


Note: `⎕SIGNAL` can be used to reset the value of this system constant.



