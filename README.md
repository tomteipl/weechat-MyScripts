# weechat-MyScripts

**Current scripts:**

* ***Xnotif.py*** - sends a notification to the MacOS or X11 desktop using
`notify-send` when a highlighted message is received.

* ***X11notif.py*** - does the same as `xnotif.py` but its only for linux DE.
It was made eariler and merged with `xnotif.py` to make it more universal.

* ***auto_commands.py*** - you can set commands to be executed
automatically on client startup.

## Xnotify.py usage

Type `/xnotif help` to see help in client.
On Linux Xnotif.py requires `libnotify` to work.
Most **DE** has it installed by default.  
On MacOS it doesn't require any additional software.
It works out of the box, so all you need to do is to copy it to
the **Weechat** scripts directory and load it with `/script load Xnotif.py`.
Or `/script load PATH/TO/SCRIPT`.

*You can use `/xnotif sys` to check if your OS is correctly detected.*

## auto_commands.py usage

1. **/autocommands add <command>** - adds command to the list. You can use spaces and special signs.

2. **/autocommands del <number/string>** - deletes command from the list.
You can use /autocommands list to see the numbers or tap TAB for auto completion.

3. **/autocommands list** - shows the list of commands with index.
4. **/autocommands clear** - clears the list of commands.

5. **/autocommands time <miliseconds>** - 1sec = 1000ms, sets the timer for hook
in miliseconds. Default value 10000ms = 10 sec.

6. **/autocommands** - Shows guides.

*You can achieve similar effect by using `weechat.startup.command_after_plugins`
and `weechat.startup.command_before_plugins`, that are built in **Weechat**.*
