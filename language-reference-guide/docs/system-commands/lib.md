




<h1 class="heading"><span class="name">List Workspace Library</span><span class="command">)LIB {dir}</span></h1>



This command lists the names of Dyalog APL workspaces contained in the given directory.



**Example**

```apl
      )LIB WS
MYWORK TEMP
```


If a directory is not given, the workspaces on the user's APL workspace path (**WSPATH**) are listed.  In this case, the listing is divided into sections identifying the directories concerned.  The current directory is identified as "`.`".



**Example**

```apl
      )LIB
.
        PDTEMP  WORK   GRAPHICS
```
```apl
c:\Dyalog\ws
        display groups
```



