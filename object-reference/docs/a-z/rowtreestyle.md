




<h1 class="heading"><span class="name">RowTreeStyle</span> <span class="command">Property</span></h1>



|-----------|--------------------------|
|Applies To:|[Grid](../objects/grid.md)|


**Description**


RowTreeStyle specifies the visible attributes of the tree displayed in the Row titles of a [Grid](../objects/grid.md).


The value of the RowTreeStyle property is a character vector chosen from the following :


|---------------------|--------------------------------------------------------|
|`'LinesOnly'`        |Only the lines of the tree structure are drawn.         |
|`'ImagesOnly'`       |Only the images of nodes with children are drawn.       |
|`'ImagesAndLines'`   |Both lines and images for nodes with children are drawn.|
|`'AllImagesOnly'`    |Images for all nodes are drawn.                         |
|`'AllImagesAndLines'`|Both lines and images for all nodes are drawn.          |




The default value, `'ImagesAndLines'`, is illustrated in the first picture below. Other values are displayed in subsequent pictures.


![gridtree3](../img/gridtree3.gif)


```apl
F.G.RowTreeStyle←'LinesOnly'
```


![gridtree4](../img/gridtree4.gif)


```apl
      

f.g.RowTreeStyle←'ImagesOnly'

```


![gridtree5](../img/gridtree5.gif)


```apl

f.g.RowTreeStyle←'AllImagesOnly'

```


![gridtree6](../img/gridtree6.gif)


```apl
      

f.g.RowTreeStyle←'AllImagesAndLines'

```


![gridtree7](../img/gridtree7.gif)



