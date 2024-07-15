




<h1 class="heading"><span class="name">Encoding</span> <span class="command">Property</span></h1>



|-----------|------------------------------------|
|Applies To:|[TCPSocket](../objects/tcpsocket.md)|


**Description**


The Encoding property is a character vector that specifies how character data
are encoded or translated.



The possible values are `'None'`,
`'UTF-8'`, `'Classic'`, or `'Unicode'`, depending upon the value of the [Style](style.md) property.



Table: Unicode Edition


|Style|Encoding|Description|
|---|---|---|
|`'Raw'`|'None'|Not applicable. Only integer data may be transmitted/received.|
|`'Char'`|'None'|Transmission is limited to characters with Unicode code points in the         range 0-255. Attempting to transmit (or receive) a character outside         this range will cause `DOMAIN ERROR` .|
|`'UTF-8'`|Characters are transmitted/received using the UTF-8 encoding scheme.||
|`'APL'`|'Classic'|Characters are transmitted/received as indices of `⎕AV` ,         and translated according to the current value of `⎕AVU` .         An attempt to transmit or receive a characters not present in `⎕AVU` will cause `TRANSLATION ERROR`|
|`'Unicode'`|Characters are transmitted/received *as is* (as Unicode code         points).||




Table: Classic Edition


|Style|Encoding|Description|
|---|---|---|
|`'Raw'`|'None'|Not applicable. Only integer data may be transmitted/received.|
|`'Char'`|'None'|Characters (which are represented internally as indices of `⎕AV` ) are         translated to and from ASCII using the Output Translate Table win.dot.|
|`'UTF-8'`|Characters are converted to/from Unicode using `⎕AVU` and transmitted/received using the UTF-8 encoding scheme. An attempt to         transmit or receive a characters not present in `⎕AVU` will cause `TRANSLATION ERROR` .||
|`'Raw'`|'Classic'|Characters are transmitted/received as indices of `⎕AV` .|
|`'Unicode'`|Characters are converted to/from Unicode using `⎕AVU` and transmitted/received as Unicode code points. An attempt to transmit         or receive a characters not present in `⎕AVU` will cause `TRANSLATION ERROR` .||



The default value of Encoding depends upon the value of [Style](style.md) as indicated.  Default values are highlighted thus.  in the above tables.


An attempt to set the value of Encoding to a value not valid for the current [Style](style.md),
as implied by the above tables, will cause `DOMAIN ERROR`.


If you change the value of the [Style](style.md) property, the value of Encoding will remain unchanged if it is valid for the new
Style. Otherwise it will revert to the default value for the new value of [Style](style.md).
```apl
      's0'⎕WC'TCPSocket' ('LocalPort' 2001)
      s0.(Style Encoding)
Char  None 

      s0.Style←'APL'
      s0.(Style Encoding)
Apl  Classic
```


