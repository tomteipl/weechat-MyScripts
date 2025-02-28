# Copyright (c) 2025 by Kamil Wiśniewski <tomteipl@gmail.com>
#
# This script sends auto commands on start
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# 0.1 - Initial release

import weechat
from time import sleep


weechat.register("auto_commands", "Tomtei", "0.1", "GPL3", "Send auto commands on start", "", "")

commands = []   # Add commands here


# adds commands to the list
def add_command(_, buffer, args):
    commands.append(args)
    weechat.prnt(buffer, f"Command '{args}' added!")
    return weechat.WEECHAT_RC_OK

def send_auto_commands():
    for command in commands:
        weechat.command("", command)
        weechat.prnt("", f"Command '{command}' sent!")
        sleep(2)
    return weechat.WEECHAT_RC_OK

def commands_cb(_, buffer, args):
    if args.startswith("list"):
        weechat.prnt(buffer, "Current commands: \n")
        for i, command in enumerate(commands):
            weechat.prnt(buffer, f"{i + 1}. {command}")
        return weechat.WEECHAT_RC_OK

    elif args.startswith("add"):
        add_command(_, buffer, args[len("add"):])
        return weechat.WEECHAT_RC_OK

    elif args.startswith("del"):
        del_command = args[len("del"):]
        if del_command in commands:
            commands.remove(del_command)
            weechat.prnt(buffer, f"Command '{del_command}' removed!")
        else:
            weechat.prnt(buffer, f"Command '{del_command}' not found!")
        return weechat.WEECHAT_RC_OK

    else:
        weechat.prnt(buffer, "Usage: /autocommands list|add|del")
        return weechat.WEECHAT_RC_OK

weechat.hook_command("autocommands", "List auto commands", "", "", "list|add|del", "commands_cb", "")
weechat.hook_timer(10000, 0, 1, "send_auto_commands", "")
