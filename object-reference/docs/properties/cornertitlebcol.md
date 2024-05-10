




<h1 class="heading"><span class="name">CornerTitleBCol</span><span class="command">Property</span></h1>



|-----------|--------------------------|
|Applies To:|[Grid](../objects/grid.md)|


**Description**


This property specifies the colour used to fill  the area in the left corner  a [Grid](../objects/grid.md) . This is the rectangle above the row titles and to the left of the column titles.


CornerTitleBCol may be a 3-element vector of integer values  in the range 0-255 which refer to the red, green and blue components of the colour respectively, or it may be a scalar that defines a standard Windows colour element (see [BCol](bcol.md) for details). Its default value is 0 which means that the colour derives from your current Windows colour scheme.



**Example**

```apl
      f.g.CornerTitleBCol←⊂255 0 0
```


![cornertitlebcol](../img/cornertitlebcol.png)



