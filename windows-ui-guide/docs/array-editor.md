<h1 class="heading"><span class="name"> Array Editor</span></h1>

The Array Editor[^1]  allows you to edit arbitrary arrays. It is invoked by either:

- Clicking the ![edit numbers icon](img/edit-numbers-icon.png) icon in the Session toolbar when the mouse pointer is over the name of a suitable variable.
- Calling the user command `]array.edit`, specifying the name of a suitable variable as its argument.
- Calling it directly via `⎕NA`

The Array Editor draws data using a format that is similar to the output of the `DISPLAY` function. For example:

![array editor](img/array-editor.png)

### Documentation

Full documentation for the Array Editor, including a list of the keystrokes it uses, is available from the Help menu in the Array Editor's window.

### Supported Arrays

The Array Editor supports arrays that  consist solely of characters and/or numbers. You may not use it to edit an array that contains an object reference or a `⎕OR`.

#### Reject unsupported data

The way that the Arrays Editor reacts to unsupported arrays is determined by the value of the **Reject unsupported data** option which is accessed by the *Options/Reject unsupported data* menu item on the Array Editor menubar.

If this is set to true (the default), and you try to edit an array containing an object reference, the Array Editor will refuse to start and the system will generate an error message.
```apl
      ⎕SE.NumEd.numed: Unexpected error in array editor:
	DOMAIN ERROR  Argument contained data that is 
       neither simple or nested.
```

If this option is cleared, the Array editor will start but you will not be able to do anything. It is therefore advisable that you leave this option set.

### Notes

- The Array Editor is supplied only with Unicode Editions of Dyalog APL/W. Please visit www.davidliebtag.com for details about availability and support for Classic Editions of Dyalog APL/W.
- Namespaces are not supported.
- Internal representations returned by `⎕OR` are not supported.
- Only one instance of the Array Editor may be executed at a time.
- All calls to interpreter primitives use a value of 3 for `⎕ML`.
- Negative numbers must be represented using high minus signs. For example, `¯3` not `-3`.

### Implementation

The Array Editor is implemented by a DLL named `dlaedit.dll` (32-bit) or      `dlaedit64.dll` (64-bit).

The DLL exports two functions:  `DyalogEditArray` and `DyalogEditArrayTitle`. The latter is used when you click  the ![edit numbers icon](img/edit-numbers-icon.png) icon in the Session toolbar (via the APL function `⎕SE.NumEd.numed`)  and by the user command `]array.edit`

### Calling the Array Editor Directly

If you wish to use the Array Editor directly, you may do so as follows using `⎕NA`[^2].

For both `DyalogEditArray` and `DyalogEditArrayTitle` the first argument is the array to be edited, while the second argument is a place holder and should always be 0

For `DyalogEditArrayTitle` the 3rd argument is a character vector whose contents are displayed in the caption of the array editor window.

The result is the newly altered array.

**Examples**

```apl

⎕NA'dlaedit.dll|DyalogEditArray <pp >pp'              ⍝ 32-bit
⎕NA'dlaedit.dll|DyalogEditArrayTitle <pp >pp <0C2[]'  ⍝ 32-bit
			
⎕NA'dlaedit64.dll|DyalogEditArray <pp >pp'            ⍝ 64-bit
⎕NA'dlaedit64.dll|DyalogEditArrayTitle <pp >pp <0C2[]'⍝ 64-bit
			
New←DyalogEditArray Old 0
New←DyalogEditArrayTitle Old 0 Name

```

[^1]: Array Editor Version 1 Release 1 © Copyright davidliebtag.com 2012, 2015
[^2]: Note that these are not standard ⎕NA calls, but rather use an extension to ⎕NA , called Direct Workspace Access . Dyalog does not intend to make this feature generally available at present: if you are interested in this feature please contact sales@dyalog.com.
