<h1 class="heading"><span class="name">Entering the Stencil and Nest Characters</span></h1>

As of April 2017 it is not possible by default to enter the Stencil or Nest character as a single key-chord under windows managers under Linux; the updated keyboard mapping file is not yet included in Linux distributions.

Dyalog expects that future Linux distributions will have an updated mapping file, but until that time, and for existing versions of Linux distributions the methods available are:

- Update the mapping file. See below for more details
- Define the *Compose* key and enter *Stencil* by pressing *Compose Quad Diamond* and *Nest* by pressing *Compose Enclose Underbar*
- In APL, use *APL i* to swap into overstrike mode, and for *Stencil* enter *Quad <Cursor left> Diamond* for or *Diamond <Cursor Left> Quad* and use *APL i* to swap back to insert mode. For Nest use *Enclose <Cursor left> Underbar* or *Underbar <Cursor left> Enclose*

To update the mapping file, edit */usr/share/X11/xkb/symbols/apl*:

- Search for the text **xkb_symbols "dyalog_base"**
- Look for the line
- *key <AB01> { [ U2282                    ] };    // subset of*

- and replace with
- *key <AB01> { [ U2282,           U2286   ] };    // subset of, enclose if simple*

- Look for the line
- *key <TLDE> { [ U22c4                    ] };    // diamond*

- and replace with
- *key <TLDE> { [ U22c4,           U233a   ] };    // diamond, quad diamond*

Be aware that there are multiple occurrences of AB01 and TLDE; please ensure that you are editing the Dyalog APL section !

Logout and log back in again.

Be aware that these changes may be lost if you update the operating system.
