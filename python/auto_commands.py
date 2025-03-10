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
#[Change Log]
# 0.5   : Added suspend/unsuspend function.
# 0.4   : Removed buffers sending text to channels.
#
# 0.3   : Implemented the hook_completion_cb to provide autocompletion for stored commands.
#       : Added Guides.
#       : Added <del> by Index or String values.
#       : Added "time" command to set timer for sending commands after start.
#
# 0.2   : added list, add, delete, clear commands
#       : added save and load commands functions
#
# 0.1   : Initial release

import weechat


SCRIPT_NAME = "auto_commands"
SCRIPT_AUTHOR = "Tomteipl"
SCRIPT_VERSION = "0.5"
SCRIPT_LICENSE = "GPL3"
SCRIPT_DESC = "Send auto commands on start"

weechat.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, SCRIPT_LICENSE, SCRIPT_DESC, "", "")


#   Guides
help = """
    Usage:

    IMPORTANT: Commands are sent on client start only once !
    /autocommands add <command> - adds command to the list. You can use spaces and special signs.
    /autocommands del <number/string> - deletes command from the list. You can use /autocommands list to see the numbers or tap TAB for auto completion.
    /autocommands list - shows the list of commands with index.
    /autocommands clear - clears the list of commands.
    /autocommands suspend <number> - suspends selected commands. The command will not be exectuted on start.
    /autocommands time <miliseconds> - 1sec = 1000ms, sets the timer for hook in miliseconds. Default value 10000ms = 10 sec.
    """



commands = []   # Commands are stored here

suspends = []    # Suspended commands are stored here

def load_commands():
    global commands
    global suspends

    # commands
    saved_commands = weechat.config_get_plugin("commands")
    commands = saved_commands.split(",") if saved_commands else []

    # suspends
    saved_suspends = weechat.config_get_plugin("suspends")
    suspends = saved_suspends.split(",") if saved_suspends else []

def save_commands():
    weechat.config_set_plugin("commands", ",".join(commands))
    weechat.config_set_plugin("suspends", ",".join(suspends))

# adds commands to the list
def add_command(data, buffer, args):
    commands.append(args)
    save_commands()
    weechat.prnt("", f"Command '{args}' added!")
    return weechat.WEECHAT_RC_OK

def send_auto_commands(data, buffer):
    for command in commands:
        weechat.command("", command)
        weechat.prnt("", f"Command '{command}' sent!")
    return weechat.WEECHAT_RC_OK

def suspend_commands(commands, suspends, index):
    if 0 <= index < len(commands):
        suspends.append(commands.pop(index))
        weechat.prnt("", f"Command '{suspends[-1]}' suspended!")
        return weechat.WEECHAT_RC_OK

def unsuspend_commands(commands, suspends, index):
    if 0 <= index < len(suspends):
        commands.append(suspends.pop(index))
        weechat.prnt("", f"Command '{commands[-1]}' unsuspended!")
        return weechat.WEECHAT_RC_OK


# [ ---COMMANDS--- ]
def commands_cb(data, buffer, args):
    if args.startswith("list"):

        # commands table
        weechat.prnt("", "\nActive commands: \n")
        for i, command in enumerate(commands):
            weechat.prnt("", f"{i + 1}. {command}")

        # suspends table
        weechat.prnt("", "\nSuspended commands: \n")
        for i, suspend in enumerate(suspends):
            weechat.prnt("", f"{i + 1}. {suspend}")

        return weechat.WEECHAT_RC_OK

# ---------------------------------------------------

    elif args.startswith("add"):
        add_command(data, "", args[len("add "):])
        return weechat.WEECHAT_RC_OK

# ---------------------------------------------------
    # Suspends
    if args.startswith("suspend"):
        try:
            suspend_commands(commands, suspends, int(args.split()[1]) - 1)
            save_commands()
            return weechat.WEECHAT_RC_OK

        except (ValueError, IndexError):
            weechat.prnt("", "Use only numbers! '/autocommands suspend <number>'")
            return weechat.WEECHAT_RC_OK

    if args.startswith("unsuspend"):
        try:
            unsuspend_commands(commands, suspends, int(args.split()[1]) - 1)
            save_commands()
            return weechat.WEECHAT_RC_OK

        except (ValueError, IndexError):
            weechat.prnt("", "Use only numbers! '/autocommands unsuspend <number>'")
            return weechat.WEECHAT_RC_OK

# ---------------------------------------------------

    elif args.startswith("del"):
        try:
            arg_value = " ".join(args.split()[1:])

            if arg_value.isdigit():         # delete command by index (example: /autocommands del 1)
                index = int(args.split()[1]) -1

                if 0 <= index < len(commands):
                    del_command = commands.pop(index)
                    save_commands()
                    weechat.prnt("", f"Command '{del_command}' deleted!")
                    return weechat.WEECHAT_RC_OK

                else:
                    weechat.prnt("", "Invalid command number!")
                    return weechat.WEECHAT_RC_OK

            elif arg_value in commands:          # delete command by string, you can use autocomplete (example: /autocommands del /join #channel)
                commands.remove(arg_value)
                save_commands()
                weechat.prnt("", f"Command '{arg_value}' deleted!")
                return weechat.WEECHAT_RC_OK

            else:
                weechat.prnt("", "Invalid command number or string!")
                return weechat.WEECHAT_RC_OK

        except (ValueError, IndexError):
                weechat.prnt("", "Invalid command number!")
                return weechat.WEECHAT_RC_OK

# ---------------------------------------------------

    elif args.startswith("time"):           # set timer for hook
        try:
            new_time = int(args.split()[1])
            weechat.config_set_plugin("timer", str(new_time))
            weechat.prnt("", f"Timer set to {new_time} ms!")

        except (ValueError, IndexError):
            weechat.prnt("", "Invalid time value! /autocommands time <miliseconds>")

        return weechat.WEECHAT_RC_OK

# ---------------------------------------------------

    elif args.startswith("clear"):
        commands.clear()
        suspends.clear()
        save_commands()
        weechat.prnt("", "Commands cleared!")
        return weechat.WEECHAT_RC_OK

# ---------------------------------------------------

    else:
        weechat.prnt("", f"{help}")
        return weechat.WEECHAT_RC_OK



# Commands completion when using <del>
def hook_completion_cb(data, completion, buffer, completion_item):
    for command in commands:
        weechat.completion_list_add(completion_item, command, 0, weechat.WEECHAT_LIST_POS_SORT)
    return weechat.WEECHAT_RC_OK



load_commands()

weechat.hook_completion("autocommands_cmds", "List auto commands", "hook_completion_cb", "")
weechat.hook_command(
    "autocommands",
    "List auto commands",
    "",
    "",
    "list || add  || del %(autocommands_cmds) || clear || time || suspend || unsuspend",
    "commands_cb",
    "",
)

timer = int(weechat.config_get_plugin("timer") or 10000)
weechat.hook_timer(timer, 0, 1, "send_auto_commands", "")
