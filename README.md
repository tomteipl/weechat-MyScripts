# weechat-MyScripts

**Current scripts:**

* ***X11notify.py*** - sends a notification to the X11 desktop using
`notify-send` when a highlighted message is received.

* ***auto_commands.py*** - you can set commands to be executed
automatically on client startup.

## X11notif.py usage

Type `/xnotif help` to see help in client.
X11notify.py requires `libnotify` to work. Most **DE** has it installed by default.
It works out of the box, so all you need to do is to copy it to
the **Weechat** scripts directory and load it with `/script load X11notify.py`.
Or `/script load PATH/TO/SCRIPT`.

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
