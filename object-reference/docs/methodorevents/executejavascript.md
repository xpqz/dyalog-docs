




<h1 class="heading"><span class="name">ExecuteJavaScript</span><span class="command">Method 839</span></h1>



|-----------|------------------------------------------|
|Applies To:|[HTMLRenderer](../objects/htmlrenderer.md)|


**Description**


This method is used to execute JavaScript in an [HTMLRenderer](../objects/htmlrenderer.md) object.


The argument to ExecuteJavaScript is a single item as follows:


|-----|----|-------------------------------------------|
|`[1]`|Code|character vector containing JavaScript code|


The shy result of ExecuteJavaScript is currently 1; this may change.



**Example**

```apl
      hr.ExecuteJavaScript 'alert("Hello")'
```



