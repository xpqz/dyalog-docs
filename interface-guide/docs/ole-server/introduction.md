<h1 class="heading"><span class="name">Introduction</span></h1>

This chapter describes how you can write an OLE Automation Server in Dyalog APL.

OLE objects are represented in Dyalog APL by namespaces. There is a direct correspondence between the object model and Dyalog APL namespace technology, a correspondence that is thoroughly exploited in the implementation of OLE Automation.

An OLE object is simply a collection of methods (code that performs tasks) and properties (data that affects behaviour). An object corresponds directly to a Dyalog APL namespace which contains functions that do things and variables that affect things. Furthermore, OLE objects are hierarchical in nature; objects may contain sub-objects just as namespaces may contain sub-namespaces. To complete the picture, an OLE Server is an application that provides (exposes) one or more OLE objects. Thus an OLE Server corresponds directly to a workspace that contains one or more namespaces.

However, when you access an OLE object, you do so by creating an instance of its class and you may work with several instances at the same time. Furthermore, several applications may access the same OLE object at the same time, each with its own set of instances. Each instance inherits its methods (functions) and the initial values of its properties from the class. However, different property values will soon be established in different instances so they must be maintained separately.

Dyalog APL/W includes the capability for a namespace to spawn instances of itself. Initially, a new instance is simply a pointer to the original namespace (not a copy), but as soon as anything in it is changed, the new value is recorded separately. Thus instance namespaces will typically share functions but maintain separate sets of data.

## Out-of-Process and In-Process OLE Servers

Dyalog APL allows you to create both out-of-process OLE Servers and in-process OLE Servers. An out-of-process OLE Server runs as a completely separate Windows program that communicates with one or more client programs. An in-process OLE Server is implemented as a Dynamic Link Library (DLL) that is loaded into the client process and becomes part of its address space.

## Writing an APL OLE Server

The following steps are required to create an OLE Automation Server in Dyalog APL/W:

1. **On Windows 7 or later, you must start Dyalog APL with Administrator privileges (right-click the desktop icon and choose Run as administrator). This is necessary to register an OLE server.**

2. Create a workspace containing an OLEServer namespace. This namespace represents an OLE Object and may contain as many functions and variables as you want to provide the functionality you require. It may also contain other OLEServer namespaces to represent sub-objects in an object hierarchy.
3. For each of the functions and variables that you wish to expose as methods and properties of your object, you must declare the data types of their parameters and results. You can do this manually, using the COM Properties tab of the Object Properties dialog box, or by invoking the SetFnInfo and SetVarInfo methods. Note that non-exported functions and variables, sub-namespaces and defined operators may be used internally, but are not available directly to an OLE Automation client. It is also possible to generate events from an OLEServer. The mechanism is the same as for an ActiveXControl and is described in the next chapter.
4. Select Export from the Session File menu and choose in-process or out-of-process COM Server as you prefer.

## Deploying an APL OLE Server

An in-process Dyalog COM Server uses  the dynamic-link library version of the Dyalog interpreter  which must be present in the same directory as your .dll, so you must copy the appropriate version there. You may use either the Development DLL or the Run-Time DLL. If you choose to use the Development DLL, you will also need to copy the DyaRes DLL which it uses.

An out-of-process Dyalog COM Server consists of your workspace and the associated type library (.tlb) file which is created when you export it. The workspace requires the  Development EXE or the  Run-Time EXE, which must be in the same directory as your workspace and type library file.

## Rules for Exported Functions

There are certain fundamental differences between OLE syntax and APL syntax.

For example, OLE methods may take any number of arguments whereas APL is confined to two; a left and a right.

Secondly, some of the arguments or even all of the arguments to an OLE method may be optional. You cannot however call a monadic APL function with no arguments; in APL there is a clear distinction between niladic functions and functions that take an argument.

Furthermore, the number and type of the arguments for each OLE method must be registered in advance so that OLE knows how to call it.

These factors mean that certain rules must be adopted so that APL can register your APL functions as OLE methods.

1. Exported APL functions must be niladic or monadic defined functions; dyadic functions, dfns, derived functions and operators are not allowed. However, ambivalent functions may be called (monadically) by OLE.
2. Character arrays whose rank is greater than 1 are passed as 1-byte integer arrays. This means that 1-byte integer matrices and higher-rank arrays will always be converted to character arrays.
3. An exported APL function may not be called with an empty numeric vector (zilde) as its single argument. Zilde is used by an APL client to call a non-niladic OLE method with no arguments.
4. If an exported APL function is called with more than one parameter, its argument will be a nested vector. If it is called with a single parameter that is a character vector or an array whose rank is greater than 1, the argument supplied to the APL function will be a simple array. Effectively, a 1-element nested array received from an OLE Client is disclosed.

The main advantage of an in-process OLE Server is that communication between the client application and the OLE Server is fast. Communication between clients and out-of-process OLE Servers has to go through a separate OLE layer in Windows that incurs a certain overhead. Another advantage is that in-process OLE Servers are simpler to administer and simpler to install.

The main disadvantages of in-process OLE Servers is that there can only be one client per server and they do not support DCOM directly.

## ClassID, TypeLibID and other properties

Windows COM objects are identified using a system of Globally Unique Identifiers (GUIDs). When you create an OLEServer object using `⎕WC`, APL creates a number of GUIDs and allocates them to the OLE Server. One of these is a Class Identifier (often abbreviated to CLSID) that will uniquely identify your OLE object. This is stored in the ClassID property of the OLEServer. Another GUID identifies the Dispatch interface of the object but is not available via a property.

An out-of-process COM server requires a separate Type Library file. This is a binary file that describes the methods (functions) and properties (variables) exposed by the OLEServer namespace(s) in the workspace. The Type Library is identified by a GUID and by its file name. The file name (which is constructed from the workspace name with a .TLB extension) is stored in the TypeLibFile property of the OLEServer namespace. The GUID is generated when it is first needed and is stored in the TypeLibFileID property of the OLEServer namespace. Note that if the workspace contains several OLEServer objects, their TypeLibFile and TypelLibID properties all have the same values.
