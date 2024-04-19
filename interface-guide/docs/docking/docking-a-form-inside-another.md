<h1 class="heading"><span class="name"> Docking a Form inside another</span></h1>

The following example illustrates the effect of docking one Form in another.
```apl
      'Host' ⎕WC 'Form' 'Host'
      Host.DockChildren←'Client'
```

![docking_form_host 0](../img/docking-form-host-0.png)

```apl
      
      'Client' ⎕WC 'Form' 'Client'
      Client.Dockable←'Always'
```

![docking_form_client 0](../img/docking-form-client-0.png)

Notice that a dockable Form is indistinguishable in appearance between any other top-level Form except that it has additional items in its pop-up context (right mouse button) menu as shown.

The following picture shows the effect of dragging the `Client` Form to the top edge of the `Host`, just before the mouse button is released.

![docking_form_host 1](../img/docking-form-host-1.png)

The next picture shows the result after docking. The `Client` Form has become a SubForm (white is the default background colour for a SubForm) called `Host.Client`.

![docking_form_host 2](../img/docking-form-host-2.png)

The third picture illustrates the effect of docking the `Client` on the left-hand edge.

![docking_form_host 3](../img/docking-form-host-3.png)

The following picture shows the `Client` Form docked as a SubForm along the right edge of the `Host` Form.

![docking_form_host 4](../img/docking-form-host-4.png)

It is also possible to dock a Form into an already docked Form.
```apl
      'Client2' ⎕WC 'Form' 'Second Client'
      Client2.Dockable←'Always'
```

![docking_form_client 1](../img/docking-form-client-1.png)

which we can make dockable in both the `Host` Form and the `Host.Client` SubForm:
```apl
Host.DockChildren Host.Client.DockChildren←⊂'Client2'
```

The next picture shows `Client2` about to be docked in the `Client` SubForm:

![docking_form_host 5](../img/docking-form-host-5.png)

And finally, after it has been docked.

![docking_form_host 6](../img/docking-form-host-6.png)
