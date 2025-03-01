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
#
#
#
# 0.2   : added list, add, delete, clear commands
#       : added save and load commands functions
#
# 0.1   : Initial release

import weechat


weechat.register("auto_commands", "Tomtei", "0.2", "GPL3", "Send auto commands on start", "", "")


commands = []   # Add commands here

def load_commands():
    global commands
    saved_commands = weechat.config_get_plugin("commands")
    commands = saved_commands.split(",") if saved_commands else []

def save_commands():
    weechat.config_set_plugin("commands", ",".join(commands))

# adds commands to the list
def add_command(_, buffer, args):
    commands.append(args)
    save_commands()
    weechat.prnt(buffer, f"Command '{args}' added!")
    return weechat.WEECHAT_RC_OK

def send_auto_commands(_, __):
    for command in commands:
        weechat.command("", command)
        weechat.prnt("", f"Command '{command}' sent!")
    return weechat.WEECHAT_RC_OK

def commands_cb(_, buffer, args):           # commands
    if args.startswith("list"):
        weechat.prnt(buffer, "Current commands: \n")
        for i, command in enumerate(commands):
            weechat.prnt(buffer, f"{i + 1}. {command}")
        return weechat.WEECHAT_RC_OK

    elif args.startswith("add"):
        add_command(_, buffer, args[len("add "):])
        return weechat.WEECHAT_RC_OK

    elif args.startswith("del"):
        try:
            index = int(args.split()[1]) -1
            if 0 <= index < len(commands):
                del_command = commands.pop(index)
                save_commands()
                weechat.prnt(buffer, f"Command '{del_command}' deleted!")
                return weechat.WEECHAT_RC_OK
            else:
                weechat.prnt(buffer, "Invalid command number!")
                return weechat.WEECHAT_RC_OK

        except (ValueError, IndexError):
                weechat.prnt(buffer, "Invalid command number!")
                return weechat.WEECHAT_RC_OK

    elif args.startswith("clear"):
        commands.clear()
        weechat.prnt(buffer, "Commands cleared!")
        return weechat.WEECHAT_RC_OK

    else:
        weechat.prnt(buffer, "Usage: /autocommands list|add|del (command number)")
        return weechat.WEECHAT_RC_OK

load_commands()

weechat.hook_command("autocommands", "List auto commands", "", "", "list || add  || del || clear", "commands_cb", "")
weechat.hook_timer(10000, 0, 1, "send_auto_commands", "")
