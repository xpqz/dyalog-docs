<h1 class="heading"><span class="name">Shell Process Control</span> <span class="command">R←{X}(8373⌶)Y</span></h1>

This function provides a way to determine the process IDs of processes started by [`⎕SHELL`](../system-functions/shell.md), as well as a way to send signals to any of those processes.

## Query Process IDs
If the I-beam is run monadically with `⍬` as its right argument, it returns a numeric vector containing all the process IDs of the processes that were left behind by [`⎕SHELL`](../system-functions/shell.md) (due to timeouts or interrupts for example). The list of process IDs are in a wait-able state, which means their ID will not be reused by the operating system before they have been waited for. Any call to 8373 I-Beam will start by removing the dead processes from the list.

When the I-beam is run with a positive integer as the right argument, it interprets that integer as an APL thread number, and if that thread is currently running [`⎕SHELL`](../system-functions/shell.md), the child process ID is returned.

<h2 class="example">Example</h2>
```apl
	tid←{
        ...
        r←⎕SHELL ...
        ...
    }&⍬

    (8373⌶)tid
84093 ⍝ the process ID
```

## Signal Child Process

If the I-beam is run dyadically, the left argument must be a integer scalar representing a signal number, which is to be sent to the child process. The child process is identified by the right argument, which must also be an integer scalar. Non-negative right arguments are interpreted as APL thread numbers, and identifies the child process of any currently running [`⎕SHELL`](../system-functions/shell.md) call on that thread. Negative numbers are negated and treated as process IDs. The process ID **must** be one of the processes left behind by a finished call to [`⎕SHELL`](../system-functions/shell.md).

The return value is a Boolean scalar, indicating if the signal was successfully sent, as reported by the operating-system.

!!! note
	On Windows, the only valid signal number is 9, which makes the I-beam call `TerminateProcess()` on the child process.
