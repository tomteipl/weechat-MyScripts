# Copyright (c) 2025 by Kamil Wiśniewski <tomteipl@gmail.com>
#
# This script shows unread messages count in the buffer title
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
# 1.0   : Initial release

import weechat
import subprocess

SCRIPT_NAME = "Macnotif"
SCRIPT_AUTHOR = "Tomteipl"
SCRIPT_VERSION = "1.0"
SCRIPT_LICENSE = "GPL3"
SCRIPT_DESC = "Sends notifications to your desktop when you are mentioned in a channel"


weechat.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, SCRIPT_LICENSE, SCRIPT_DESC, "", "")

help = """
        Macnotif works only on MacOS systems!
    """

def smart_notif(data, buffer, date, tags, displayed, highlight, prefix, message):
    if int(highlight):
        channel = weechat.buffer_get_string(buffer, "localvar_channel")
        send_notification(channel, message)
    return weechat.WEECHAT_RC_OK


# Send notif using osascript and send sound using afplay that are built in MacOS
def send_notification(title, message):
    script = f'display notification "{message}" with title "{title}"'
    subprocess.run(["osascript", "-e", script])
    subprocess.run(["afplay", "/System/Library/Sounds/Ping.aiff"])


# Commands
def commands_cb(data, buffer, args):
    if args.startswith("help"):
        weechat.prnt("", f"{help}")
        return weechat.WEECHAT_RC_OK

    else:
        weechat.prnt("", f"{help}")
        return weechat.WEECHAT_RC_ERROR

# Hooks
weechat.hook_command(
    "macnotif",
    "Shows help",
    "",
    "",
    "help",
    "commands_cb",
    "",
)
weechat.hook_print("", "", "", 1, "smart_notif", "")
