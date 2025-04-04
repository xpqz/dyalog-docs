<h1 class="heading"><span class="name">Menus in MDI Applications</span></h1>

A feature of MDI behaviour is that SubForms do not display menu bars. However, if you create a MenuBar object for a SubForm, that object will be displayed as the menu bar of the parent Form whenever the SubForm has the focus. If there are no SubForms or if the SubForm with the focus does not own a MenuBar, the MenuBar of the parent Form is displayed. This mechanism provides one way of achieving the desired effect, namely that the menu bar displayed is appropriate for the type of document represented by the SubForm that has the focus. However, if you have a  large number of SubForms of the same type (that is, which share the same menu bar) you must defined identical MenuBar objects for all of them.

An alternative approach is to define separate MenuBar objects as children of the parent Form, only one of which is visible. Then you simply attach a callback function to the GotFocus event for each SubForm that makes the appropriate MenuBar visible. This approach means that you need only define MenuBar objects for each different *type* of SubForm, rather than for every one.

It is possible to mix these techniques, so that the MenuBar displayed is either the result of your callback function making it visible, or because a SubForm has its own MenuBar object defined and received the focus.

Note that when the user maximises a SubForm, its system menu button and restore button are displayed in the parent Form's menu bar. It is therefore essential that you ensure that your application provides such a menu bar at all times. Otherwise, when your user maximises a SubForm there is no way to reverse it.
