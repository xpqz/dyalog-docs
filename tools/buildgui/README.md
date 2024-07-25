# BuildGUI

Note: 

1. This code has been exported from the workspace `Core/ws/GUIMaint.dws`.
2. The code can only be run on Windows.

The main purpose of the code herein is to generate the crossreference tables present in the `Object Reference Guide`. In all likelihood, this is now fairly static, but changes do still happen. The code was written a long time ago, before Dyalog contained, for example, `⎕XML`.

The code has been left as-is, with the following exceptions:

1. The workspace has been exported to text, so that it can be versioned. 
2. The function `WriteFile.aplf` now ensures that any directories not present in its path are created.

Additionally, two new functions have been added:

1. `NewBuildGUI.aplf`: the new entry point, serving the same purpose as `BuildGUI.aplf`, but not writing entries into a Table of Contents file, and not writing stubbed entries of new object.
2. `NewWriteMembers.aplf`: analogous to `WriteMembers.aplf`, creating the actual crossreference tables, but writing Markdown instead of XML. This function will sort the tables it generates in col-major order. The old code generated tables that were occasionally not sorted at all.

To run this code, say

```apl
files ← NewBuildGUI '/some/path/to/your/project/dir/here'
```

Note that the old `BuildGUI.aplf` also takes a left arg 0 for "run" and 1 for "dry run". The old version was intended to write straight to the documentation repository, but we probably don't need to do that with the new one: write out the files to a fresh directory, do a diff against the existing, and integrate manually in the rare cases that something changed. 