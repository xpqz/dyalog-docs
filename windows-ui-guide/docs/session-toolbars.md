<h1 class="heading"><span class="name"> The Session Toolbars</span></h1>

The Session toolbars are contained by four separate CoolBand objects, allowing you to configure their order in whichever way you choose. The tool buttons appear differently according to whether or not Native Look and Feel is enabled.

The bitmaps for the buttons displayed on the session tool bar are implemented by three ImageList objects owned by the CoolBar `⎕SE.cbtop`. These represent the ToolButton images in their normal, highlighted and inactive states and are named `iln`, `ilh` and `ili` respectively. These images derive from three bitmap resources contained in `dyalog.exe` named `tb_normal`, `tb_hot` and `tb_inactive`.

If Native Look and Feel is enabled all three bitmap resources are mapped to a different set of images which are capable of  reflecting the *Visual Styles* in use.

## Native Look and Feel Enabled

![ws session toolbar](img/ws-session-toolbar.png)

![object session toolbar](img/object-session-toolbar.png)

![tool session toolbar](img/tool-session-toolbar.png)

![edit session toolbar](img/edit-session-toolbar.png)

![session session toolbar](img/session-session-toolbar.png)

## Native Look and Feel Disabled

![ws session toolbar](img/nlf-disabled/ws-session-toolbar.png)

![object session toolbar](img/nlf-disabled/object-session-toolbar.png)

![tool session toolbar](img/nlf-disabled/tool-session-toolbar.png)

![edit session toolbar](img/nlf-disabled/edit-session-toolbar.png)

![session session toolbar](img/nlf-disabled/session-session-toolbar.png)

## Workspace (WS) Operations

| Button | Operation  | Description |
|--------|-------| --- |
| ![clear workspace icon](img/clear-workspace-icon.png) ![clear workspace icon](img/nlf-disabled/clear-workspace-icon.png) | Clear Workspace  | Executes the system operation `[WSClear]` which asks for confirmation, then clears the workspace |
| ![load workspace icon](img/load-workspace-icon.png) ![load workspace icon](img/nlf-disabled/load-workspace-icon.png) | Load Workspace   | Executes the system operation `[WSLoad]` which displays a file selection dialog box and loads the selected workspace |
| ![copy workspace icon](img/copy-workspace-icon.png) ![copy workspace icon](img/nlf-disabled/copy-workspace-icon.png) | Copy Workspace   | Executes the system operation `[WSCopy]` which displays a file selection dialog box and copies the (entire) selected workspace |
| ![save workspace icon](img/save-workspace-icon.png) ![save workspace icon](img/nlf-disabled/save-workspace-icon.png) | Save Workspace   | Executes the system operation `[WSSaveas]` which displays a file selection dialog box and saves the workspace in the selected file |
| ![export workspace icon](img/export-workspace-icon.png) ![reexport workspace icon](img/nlf-disabled/reexport-workspace-icon.png) | Export Workspace | Executes the system operation `[MakeExe]` which re-exports the workspace using the settings, parameters and options that were previously selected using the *Create Bound File* dialog |
| ![print functions icon](img/print-functions-icon.png) ![print workspace icon](img/nlf-disabled/print-workspace-icon.png) | Print Functions  | Executes the system operation `[PrintFnsInNS]` that prints all the functions and operators in the current namespace |

## Object Operations

| Button  | Operation  | Description |
| --- | ---  | --- |
| ![copy object icon](img/copy-object-icon.png) ![copy object icon](img/nlf-disabled/copy-object-icon.png)     | Copy Object  | Executes the system operation `[ObjCopy]` which copies the contents of the current object to the clipboard |
| ![paste object icon](img/paste-object-icon.png) ![paste object icon](img/nlf-disabled/paste-object-icon.png) | Paste Object | Executes the system operation `[ObjPaste]` which copies the contents of the clipboard into the current object, replacing its previous value |
| ![print object icon](img/print-object-icon.png) ![print object icon](img/nlf-disabled/print-object-icon.png) | Print Object | Executes the system operation `[ObjPrint]` . Prints the current object. Note that if the object is being edited, the version of the object displayed in the edit window is printed. |
| ![edit object icon](img/edit-object-icon.png) ![edit object icon](img/nlf-disabled/edit-object-icon.png)     | Edit Object  | Executes the system operation `[Edit]` which edits the current object using the standard system editor |
| ![edit numbers icon](img/edit-numbers-icon.png) ![edit numbers icon](img/nlf-disabled/edit-numbers-icon.png) | Edit Array   | Executes a defined function in `⎕SE` that edits the current object using the Array Editor (Unicode Edition) or a spreadsheet-like interface based upon the Grid object (Classic Edition). See [Array Editor](array-editor.md) |
| ![sharpplot icon](img/sharpplot-icon.png) ![sharpplot icon](img/nlf-disabled/sharpplot-icon.jpg)             | SharpPlot    | Executes a defined function in `⎕SE` that runs the Chart Wizard to plot the current object using the `]chart` User Command. |


## Tools

| Button  | Operation  | Description |
| --- | ---  | --- |
| ![explorer icon](img/explorer-icon.png) ![explorer icon](img/nlf-disabled/explorer-icon.png) | Explorer | Executes the system operation `[Explorer]` which displays the *Workspace Explorer* tool |
| ![search icon](img/search-icon.png) ![search icon](img/nlf-disabled/search-icon.png) | Search | Executes the system operation `[WSSearch]` which displays the *Workspace Search* tool |
| ![line numbers icon](img/line-numbers-icon.png) ![line numbers icon](img/nlf-disabled/line-numbers-icon.png) | Line Numbers | Executes the system operation `[LineNumbers]` which toggles the display of line numbers in edit and trace windows on and off |
| ![clear all stops icon](img/clear-all-stops-icon.png) ![clear all stops icon](img/nlf-disabled/clear-all-stops-icon.png) | Clear all Stops | Executes the system operation `[ClearTSM]` which clears all `⎕STOP` , `⎕MONITOR` and `⎕TRACE` settings |

## Edit Operations

| Button  | Operation  | Description |
| --- | ---  | --- |
| ![copy selection icon](img/copy-selection-icon.png) ![copy selection icon](img/nlf-disabled/copy-selection-icon.png) | Copy Selection | Executes the system operation `[Copy]` which copies the selected text to the clipboard |
| ![paste selection icon](img/paste-selection-icon.png) ![paste selection icon](img/nlf-disabled/paste-selection-icon.png) |  Paste Selection | Executes the system operation `[Paste]` which pastes the text in the clipboard into the current window at the insertion point |
| ![recall last icon](img/recall-last-icon.png) ![recall last icon](img/nlf-disabled/recall-last-icon.png) | Recall Last | Executes the system operation `[Undo]` which recalls the previous input line from the input history stack |
| ![recall next icon](img/recall-next-icon.png) ![recall next icon](img/nlf-disabled/recall-next-icon.png) | Recall Next | Executes the system operation `[Redo]` which recalls the next input line from the input history stack |

## Session Operations

| Button  | Operation  | Description |
| --- | ---  | --- |
| ![load workspace icon](img/load-workspace-icon.png) ![load session icon](img/nlf-disabled/load-session-icon.png) | Load Session | Executes the system operation `[SELoad]` which displays a file selection dialog box and loads the selected Session File |
| ![boxing icon](img/boxing-icon.png) ![boxing icon](img/nlf-disabled/boxing-icon.png) | Boxing On/Off | Executes the user command `]boxing` to toggle boxing on/off. |
| ![select font combo](img/select-font-combo.png) | Select Font | Selects the font to be used in the Session window |
| ![select fontsize spinner](img/select-fontsize-spinner.png) | Select Font Size | Selects the size of the font to be used in the Session window |
