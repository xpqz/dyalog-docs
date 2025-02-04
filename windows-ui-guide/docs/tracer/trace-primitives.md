# Trace Primitives

_Trace Primitive_ (TP) is an extension to the tracer that allows the developer to step through the execution of individual primitives of expressions, examining intermediate results and left and right arguments of sub-expressions. It's a powerful addition to the developer's toolbox: it enables the introspection of complex expressions typed directly into the session, and can be used in conjunction with the traditional tracing mode to skip over lines you're not interested in, and step through primitive by primitive in complex expressions where you need to.

!!! note
    _Trace Primitives_ is not an entirely accurate name: it is tracing with the (approximate) granularity of primitives, though it does stop on non-primitives.

## Getting started

There is a command **&lt;TP&gt;** called *Trace Primitive* with the default keyboard shortcut <kbd>shift</kbd>+<kbd>alt</kbd>+<kbd>enter</kbd> which is used to trace primitives.

There are four primary means of starting a TP session:

1. Issue the command **&lt;TP&gt;** directly in the session.
2. Select **Trace Primitives…** from the _Action_ menu.
3. Select **Action > Trace Primitives…** from the context menu.
4. Click the **Next Primitive** icon in the tracer's toolbar, showing as a downward arrow over three dots:

    ![](../../img/next-primitive.png)

If you enter an expression in the session such as:
```apl
(+/÷≢)⍳10
```
and hit <kbd>shift</kbd>+<kbd>alt</kbd>+<kbd>enter</kbd>, you should see:

![](../../img/start-tbt.png)

The little red box surrounding the `⍳` in the tracer pane is showing the next primitive to be executed. Keep hitting <kbd>shift</kbd>+<kbd>alt</kbd>+<kbd>enter</kbd> a few times to see how the execution progresses through the expression. 

The **Next Primitive** icon is always present in the tracer. The new **&lt;TP&gt;** command lets you open a tracer on an expression typed directly in the session that previously could not be traced into. 

## Anatomy of the TP Interface

There are three available layout modes (each of which can be adjusted and configured to taste). They are available under the **Layout** menu:

- **Classic**
- **Debugger at the bottom**
- **Debugger on the left**

The layout is a matter of preference; the functionality is the same. The default behaviour is **Debugger at the bottom**. 

The **Classic** layout mode detaches the tracer window, allowing it to be placed on a second monitor. 

![](../../img/tbt-classic.png)

The **Debugger at the bottom** layout mode:

![](../../img/tbt-debugger-bottom.png)

The **Debugger to the left** layout mode:

![](../../img/tbt-debugger-left.png)

In the last two layout modes, the tracer panes are docked into the main window. In all three modes, by default, there are two docked, but minimised panes, named **Left Argument** and **Right Argument**. They will open up automatically as you trace through an expression.

### Aspect Panes

There are several more aspects of an expression that can be inspected in TP mode beyond the left and right arguments. These are available under the **Windows** menu when in tracing mode.

The aspect pane options are divided into two groups: 1-4, which apply to the *current* function, and 5-9, which apply to the *previously* executed function. They are:

1. **Left Argument**

    The **Left Argument** pane is enabled (but minimised) by default. As you step through an expression, it will display the left argument about to be passed to the highlighted function. 

2. **Current Function**

    The **Current Function** is the one highlighted with the red box in the tracer. Opening a dedicated aspect pane allows you to select different presentation modes, see the section [Aspect Pane Options](#aspect-pane-options) below.

3. **Right Argument**

    The **Right Argument** pane is enabled (but minimised) by default. As you step through an expression, it will display the right argument about to be passed to the highlighted function. 
    
4. **Axis Specification**

    The bracket axis applied to the current function (if any).

5. **Previous Result**
    
    The result of the function evaluation immediately before the one highlighted with the red box. 
    
6. **Previous Left**

    The left argument of the function evaluation immediately before the one highlighted with the red box.

7. **Previous Function**

    The function that was evaluated immediately before the one highlighted with the red box. 

8. **Previous Right**

    The right argument of the function evaluation immediately before the one highlighted with the red box.

9. **Previous Axis**

    The bracket axis applied to the function evaluation immediately before the one highlighted with the red box (if any).

The relationship between these panes can be illustrated as

```other
Left Argument  ┐     ┌─  Axis Specification
               │ ┌─┐ │  ┌──────┬─  Right Argument / Previous Result
               a │B│[1] c D[2] e
                 └┬┘    │ │ │  └  Previous Right
Current Function  ┘     │ │ └  Previous Axis
         Previous Left  ┘ └  Previous Function
```

!!! note 
    Each of these options correspond to a new pane in the tracer. With every such pane enabled and visible, the interface will become busy. A good strategy is to enable these on a case by case basis.

### Aspect Pane Options

The settings available under the **Options** menu can be used to configure the behaviour of the aspect panes. They are:

1. **Show Status Bars**

    This controls the appearance of status bars at the bottom of TP windows.

2. **Minimise until first use**
    
    This means that if you have saved a tracer layout, the panes should remain minimised until they're activated. This is the default setting. For complex tracer layouts, this can often mean a better use of the screen real estate.

3. **Show functions as trees**

    When using the **Current/Previous Function** panes, **Show functions as trees** uses the same display mode as `]box on -trains=tree`. Default is `]box on -trains=box`. This option can be helpful when dealing with tacit expressions. 

4. **Trace idioms**

    When selected, the TP tracer will trace _into_ any expression that the interpreter might otherwise optimise out. If not selected, the tracer will instead treat such expressions as atomic functions.
 
5. **Use Array Notation**

    Use APL array notation in the panes for arguments and results, instead of the traditional APL array display.

Here is an illustration of the effect of choosing **Show functions as trees** on the **Current Function** pane:

![](../../img/tbt-current-fn-options-menu.png)

## Tracing Diamond-Separated Expressions

Sometimes you encounter a line of code which is a set of expressions separated by diamonds, but you might only want to TP into some of them. Consider three diamond-separated expressions, but we want to skip the first two, and TP-trace into the last expression only:

```apl
a ← 3 3⍴⍳9 ⋄ b ← ⍉a ⋄ a + b
```

Enter the expressions in the session, and commence TP by hitting <kbd>alt</kbd>+<kbd>shift</kbd>+<kbd>enter</kbd>. You should see:

![](../../img/tbt-diamond1.png)

with the first expression highlighted. Now hit <kbd>enter</kbd> to execute single expression:

![](../../img/tbt-diamond2.png)

and hit <kbd>enter</kbd> again to skip the middle expression, and then <kbd>alt</kbd>+<kbd>shift</kbd>+<kbd>enter</kbd> to TP into the final expression:

![](../../img/tbt-diamond3.png)

