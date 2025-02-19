<h1 class="heading"><span class="name">Timer</span> <span class="right">Event 140</span></h1>



**Applies To:** [Timer](../objects/timer.md)

**Description**


This event is generated at regular intervals by a [Timer](../objects/timer.md) object and is typically used to fire a callback function to perform a task repeatedly. Returning a 0 from a callback function attached to a Timer event has no effect. The event message reported as the result of [`⎕DQ`](../../../language-reference-guide/system-functions/dq), or supplied as the right argument to your callback function, is a 2 element vector as follows :


|-----|------|-----------------------|
|`[1]`|Object|ref or character vector|
|`[2]`|Event |`'Timer'` or 140       |



