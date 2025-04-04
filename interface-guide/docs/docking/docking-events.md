<h1 class="heading"><span class="name">Docking Events</span></h1>

An object (the client) may be docked in another object (the host) if the Dockable property of the client is set to `'Always'` and the name of the client is included in the host object's DockChildren property. This property defines the list of names that the host will accept. Docking a Form or re-docking an already docked object behave in essentially the same way.

## DockStart Event

The user picks up a client object by depressing the left mouse button over its title bar or client area and dragging. As soon as the mouse is moved, the object generates a DockStart event At this stage, the entire operation may be cancelled by a callback function on DockStart that returns 0.

Once a docking operation has begun, the outline of the object is displayed as a rectangle that moves with the mouse.

## DockMove Event

When the client object is dragged over a suitable host object (one that will accept it as a child), the host object generates a series of DockMove events. Each DockMove event reports the edge along which the client object will be docked, namely Top, Bottom, Left, Right or None, and a corresponding rectangle

When the mouse pointer approaches an edge of the host, the rectangle changes to describe a docking zone indicating where the object will be docked in the host.

A callback function on DockMove that returns 0 will prevent the outline rectangle changing to indicating a docking zone and will prevent the client from being docked.

A callback function on DockMove can also return a result that modifies the position and size of the rectangle that is actually displayed for the user. This in turn will affect the zone occupied by the client when it becomes docked. For example, you can use this to control its size.

## DockRequest Event

When the user releases the mouse pointer, the client object generates a DockRequest event. A callback function on DockRequest may return 0 to abort the operation, or may modify the requested docking zone in the host. In the case of a ToolControl, the callback is used to action the docking operation.

## DockAccept Event

In response to a successful DockRequest event, the host object generates a DockAccept event. A callback on DockAccept may also be used to abort the operation or to modify the docking zone. The DockAccept event reports the new name for the client object which it will assume as a child of the host.

Furthermore, if the DockAccept callback actions the event before completing, the docking operation will take place immediately, rather than being deferred until the callback has completed. This allows you to set properties on the newly docked object.

## DockEnd Event

Finally, the docked client object (whose name has now changed) will generate a DockEnd event. This is reported for information only and a DockEnd callback function cannot cancel or modify the docking operation. The DockEnd event may however be used to set properties for the newly docked client.

If the user releases the mouse elsewhere than over an accepting host object, the DockEnd event is reported by the client object itself. If appropriate, this will be followed by a Configure event and the client will simply move to a new location without changing its docking status.

## DockCancel Event

If at any stage the user presses the Esc key, the operation is aborted and the client object generates a DockCancel event.
