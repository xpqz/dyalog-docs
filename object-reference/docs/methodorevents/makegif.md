<h1 class="heading"><span class="name">MakeGIF</span> <span class="right">Method 261</span></h1>



**Applies To:** [Bitmap](../objects/bitmap.md)

**Description**


This method is used to generate a  GIF representation of a picture from a Bitmap object suitable for display by a Web browser.


The MakeGIF method is niladic.


The result is an integer vector containing the encoded GIF image.

<h2 class="example">Example</h2>
```apl
      ⍴GIF←BM.MakeGIF
19620
```



