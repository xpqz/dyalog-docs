<h1 class="heading"><span class="name"> State and Access Control</span></h1>

Earlier, we have seen how shared variable state and access controls are used to ensure effective communication between two APL tasks. How do these concepts apply in the DDE environment when APL is using shared variables to communicate via DDE with both other APL workspaces, and with non-APL applications?

The initial state of a shared variable on the completion of sharing depends upon whether your variable is a server or a client. If it is a server, the initial state vector is (1 0 1 0) which means that you have set (and know) the value, but your partner has yet to use it. If the variable is acting as a client, the initial state vector is (0 1 0 1). This implies that your partner has set the value but you have yet to use it.

As your partner can be a non-APL application which does not share the concepts of **set** and **use**, it is necessary to define a rule or set of rules from which APL can reasonably infer such actions.

During a DDE conversation, the physical transfer of data from one application to another is achieved using DDE DATA messages. When a DATA message is sent, the receiving task normally returns an ACK (acknowledgement) message. APL uses the DATA and ACK messages to control Shared Variable access.

When an assignment is made to a shared variable, APL sends a DATA message to the second process. When it receives back an ACK message, APL infers that this means that the partner has **used** the variable. When APL receives a DATA message from the other process it infers that the partner has **set** the variable. However, it only responds with an ACK message when the new value of the variable is referenced by the workspace.

Let's see what this means if two APL workspaces are involved.

| Server Workspace | Client Workspace |
| --- | ---  |
|  |  |
| Make general offer |  |
| X←42 |  |
| 'DDE:' ⎕SVO 'X' |  |
| 1 |  |
| ⎕SVS 'X' |  |
| 0 0 0 0 ⍝ No partner |  |
| ⎕SVC 'X' |  |
| 0 0 0 0 ⍝ No access ctl |  |
|  |  |
|  | Make specific offer |
|  | 'DDE:DYALOG|SERVER'⎕SVO'X' |
|  | <--- initiate --- |
| ack ---> |  |
|  | <--- please advise on change |
| ack ---> |  |
|  | 2  ⍝ Offer accepted |
| ⎕SVS 'X' | ⎕SVS 'X' |
| 1 0 1 0⍝ I know, not he | 0 1 0 1⍝ He knows, I don't |
|  | Client requests data |
|  | Y ← X |
|  | <--- req --- |
| --- data (42) ---> |  |
|  | <--- ack --- |
| ⎕SVS 'X' | ⎕SVS 'X' |
| 0 0 1 1⍝ We both know | 0 0 1 1⍝ We both know |
| Server changes data |  |
| X ← 20 |  |
| --- data has changed --> |  |
|  | <--- ack --- |
| ⎕SVS 'X' | ⎕SVS 'X' |
| 1 0 1 0⍝ I know, not he | 0 1 0 1⍝ He knows, I don't |
|  | Client requests data |
|  | Y ← X |
|  | <--- req --- |
| --- data (20) ---> |  |
|  | <--- ack --- |
| ⎕SVS 'X' | ⎕SVS 'X' |
| 0 0 1 1⍝ We both know | 0 0 1 1⍝ We both know |

As you can see, this has the desired effect, namely that an APL workspace sets the value of a shared variable by assignment to it and **uses** it by reference to it. The mechanism of using the DATA and ACK messages to imply **set** and **use** also works with non-APL applications which do not (in general) support these concepts.

Access control between two APL workspaces is imposed by each workspace acting independently. Whenever either workspace changes its `⎕SVC`, the information is transmitted to the other. Thus both workspaces maintain their own copy of the **effective** access control vector upon which to base decisions.

| Server Workspace | Client Workspace |
| --- | ---  |
| No access control | No access control |
| ⎕SVC 'X' | ⎕SVC 'X' |
| 0 0 0 0 ⍝ No access ctl | 0 0 0 0 ⍝ No access ctl |
|  | Client makes multiple requests for data |
|  | Y←X |
|  | Y←X |
| Server can set several times |  |
| X←30 |  |
| X←40 |  |
| Set access control |  |
| 1 0 0 1 ⎕SVC 'X' |  |
| --- change in ⎕SVC --> |  |
| ⎕SVC 'X' | ⎕SVC 'X' |
| ```apl 1 0 0 1⍝ I cannot set          until he has          used; he cannot          use untilI          have set ``` | ```apl 0 1 1 0⍝ He cannot set          until I have          used. I cannot          use until he          has set ``` |
|  | Client requests data |
|  | Y ← X |
|  | <--- req --- |
|  | (hangs waiting for data) |
| Server changes data |  |
| X ← 30 |  |
| --- data (30) ---> |  |
|  | <--- ack --- |
|  | Y⍝ data received |
|  | 30 |
| Server changes data |  |
| X ← 40 |  |
| --- data has changed ---> |  |
|  | <--- ack --- |
| Server tries to change data again |  |
| X ← 50 |  |
| --- data has changed ---> |  |
| (assignment hangs waiting for ack) |  |
|  | Y ← X⍝ use data |
|  | <--- req --- |
| --- data (40) ---> |  |
|  | <--- ack --- |
| X⍝ assignment done | Y⍝ data received |
| 50 | 40 |

Where the second process is a non-APL application, the effective access control vector is maintained only by the APL task and access control can only be imposed by APL. At first sight, it may seem impossible for APL to affect another application in this way, and indeed there are severe limitations in what APL can achieve. Nevertheless, effective access control is possible in the case when it is desirable to inhibit the partner from **setting** the value twice without an intervening **use** by the APL task.

This is simply achieved by withholding the ACK message. Thus if APL receives a DATA message from its partner at a time when a **set** by the partner is inhibited, APL registers the new value but withholds the acknowledgement. Only when the inhibitor is removed will APL respond with an ACK. (Users with DDESPY will observe that this is actually implemented by APL re-transmitting the DATA message to itself when the inhibitor is removed).

Assuming that the second application waits for the acknowledgement before proceeding, this will cause the desired synchronisation. Naturally, this cannot be entirely guaranteed because APL has no **direct** control over a non-APL program. Indeed, when an application transmits a DATA message, it can include a flag to indicate that an acknowledgement is neither expected nor required. In these circumstances, APL is powerless to impose any access control.

Note that APL does not (and cannot) have any control over successive internal references to the data by a non-APL application.

The rule for establishing your partner's initial `⎕SVC` is as follows:

- If the DDE link is a **warm** link, your partner's `⎕SVC` is initially (0 0 0 0).
- If the DDE link is instead a **hot** link, your partner's `⎕SVC` is initially (1 0 0 1).

This works in practice as follows:

#### Server = APL, Client = APL

You made a general offer which has been accepted by another APL workspace, e.g.
```apl
      'DDE:' ⎕SVO 'DATA'
```

Two APL tasks always use a warm DDE link. Therefore, initially, both `⎕SVC`s are (0 0 0 0). Control is (optionally) imposed by both partners subsequently setting `⎕SVC`.

#### Server = APL, Client = another application

You made a general offer which has been accepted by another application, e.g.
```apl
      'DDE:' ⎕SVO 'DATA'
```

The client application establishes the strength of the link (warm or hot). If it is a warm link, the initial value of the client's `⎕SVC` is (0 0 0 0) and, as the client has no means to change it itself, control may only be imposed by the server APL task. If the client establishes a hot link, its initial `⎕SVC` is (1 0 0 1). As it has no means to change it, and as the APL server task cannot (by definition) change it, the client's `⎕SVC` retains this setting for the duration of the conversation. (1 0 0 1) means that both partners are inhibited from setting the value of the shared variable twice in a row without an intervening use (or set) by the other. Given that the other application has requested a hot link (give me the value every time it changes) it is reasonable to assume that the application does not want to miss any values and will happily accept new data every time it is changed.

#### Server = another application, Client = APL

You made a **specific offer** to another application, e.g.
```apl
      'DDE:EXCEL|SHEET1' ⎕SVO 'DATA R1C1:R3C4'
```

In this case, APL as the client will request a warm DDE link. If the server fails to agree to this request, APL will ask for the current data value and, whether or not the server responds, will not establish a permanent link. Thus the only possibility for a permanent connection is a warm link. This in turn means that the server's `⎕SVC` will be (0 0 0 0). Furthermore, as the server has no means to change it, it's `⎕SVC` will remain (0 0 0 0) for the duration of the conversation. Control is therefore imposed solely by APL.

### Terminating a Conversation

A DDE conversation is terminated by "un-sharing" the variable. This can be done explicitly using `⎕EX` or `⎕SVR`. It is also done automatically when you exit a function in which a shared variable is localised.
