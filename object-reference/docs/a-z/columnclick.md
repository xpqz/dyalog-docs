




<h1 class="heading"><span class="name">ColumnClick</span><span class="command">Event 320</span></h1>



Applies To: [ListView](../objects/listview.md)


**Description**


If enabled, this event is reported when the user clicks on the column heading in a [ListView](../objects/listview.md) object. This event may not be disabled or affected by a callback function in any way.


The event message reported as the result of `⎕DQ`, or supplied as the right argument to your callback function, is a 5-element vector as follows :


| [1] | Object | ref or character vector |
| --- | --- | ---  |
| [2] | Event | `'ColumnClick'` or 320 |
| [3] | Column number | Integer |
| [4] | Button | button pressed (number) 1 = left button 2 =        right button 4 = middle button |
| [5] | Shift State | sum of shift key codes (number) 1 = Shift key        is down 2 =  Ctrl key is down |



