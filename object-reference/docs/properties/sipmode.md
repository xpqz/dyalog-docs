<h1 class="heading"><span class="name">SIPMode</span> <span class="right">Property</span></h1>



**Applies To:** [Form](../objects/form.md)

**Description**


**SIPMode applies only to PocketAPL. In versions of Dyalog for other platforms, it has no effect.**


This is a Boolean property that specifies the behaviour of the Input Panel with respect to the Pocket APL GUI.


If SIPMode is 1, the Input Panel is automatically displayed when a GUI control that may receive character input (for example, an Edit object) receives the input focus. The Input Panel is automatically hidden when the input focus moves to a control that does not receive character input.


If SIPMode is 0 (the default), the display of the Input Panel is not handled automatically, but may be controlled using the ShowSIP method.


Note that the user may display and hide the Input Panel manually, regardless of the value of SIPMode.



