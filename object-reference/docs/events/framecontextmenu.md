




<h1 class="heading"><span class="name">FrameContextMenu</span> <span class="command">Event 411</span></h1>



|-----------|--------------------------|--------------------------------|
|Applies To:|[Form](../objects/form.md)|[SubForm](../objects/subform.md)|


**Description**


If enabled, this event is reported when the user clicks and releases the right mouse button over the non-client area of an object, e.g. the title bar in a Form.


The event message reported as the result of `⎕DQ`, or supplied as the right argument to your callback function, is a 4-element vector as follows :


|-----|------|--------------------------------|
|`[1]`|Object|ref or character vector         |
|`[2]`|Event |`'FrameContextMenu'` or 411     |
|`[3]`|Y     |y-position of the mouse (number)|
|`[4]`|X     |x-position of the mouse (number)|


For further details, see [ContextMenu Event](../methodorevents/contextmenu.md).



