<h1 class="heading"><span class="name">Caption</span> <span class="right">Property</span></h1>

[**Applies To**](../propertyapplies/caption.md)

**Description**


The Caption property is a character vector specifying fixed text associated with the object. For example, Caption defines the label on a [Button](../objects/button.md), the title of a [Form](../objects/form.md), [SubForm](../objects/subform.md) or [MsgBox](../objects/msgbox.md), the heading in a [Group](../objects/group.md), and the text of a [Menu](../objects/menu.md) or a [MenuItem](../objects/menuitem.md).


For the [Root](../objects/root.md) object, Caption specifies the text displayed when Alt+Tab is used to switch to the Dyalog APL/W application. It may be used in conjunction with the [IconObj](iconobj.md) property which specifies the name of an [Icon](../objects/icon.md) object to be displayed alongside this text.


Its default value is an empty vector.


For a [Button](../objects/button.md) or [Label](../objects/label.md), if the Caption property  contains one or more linefeed characters (`⎕UCS 10`) the text is top-left justified or, for a [Button](../objects/button.md) with [Style](style.md)`'Push'`, centre-justifed ;  and automatically wraps on white-space characters (such as space and tab) to fit in the width provided.


For controls that support this feature, a single ampersand (&) is used to designate that the following character (if present) is an access key or an accelerator key and that character is underlined. The ampersand is not itself displayed. To negate this feature and cause an ampersand to be displayed, it is necessary to specify "&&".


