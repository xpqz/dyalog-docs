




<h1 class="heading"><span class="name">HasClearButton</span><span class="command">Property</span></h1>



Applies To: [ButtonEdit](../objects/buttonedit.md) [Combo](../objects/combo.md) [ComboEx](../objects/comboex.md) [Edit](../objects/edit.md)


**Description**


Specifies whether or not an![clearbutton](../img/clearbutton.png)button is displayed in the right-hand end of an edit box. Clicking this button clears the text from the field.



**Note that this feature only applies if Native Look and Feel 

 is enabled.**


HasClearButton is Boolean. 1 means that an ![clearbutton](../img/clearbutton.png) button will be displayed; 0 (the default) means that the button will not be shown. It may only be specified when the object is created. If you subsequently attempt to change the value of HasClearButton, the operation will fail with `NONCE ERROR`.


HasClearButton is only effective for Edit objects with Style Single; it is silently ignored for other Styles of Edit objects.


![hasclearbutton](../img/hasclearbutton.png)


