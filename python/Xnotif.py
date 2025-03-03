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
# 1.1   : Merged Macnotif.py and X11notif.py into one
#       : Added system checks to get what OS is running
#       : Changed name to Xnotif
# 1.0   : Initial release

import weechat
import subprocess
import platform
import shutil

SCRIPT_NAME = "Xnotif"
SCRIPT_AUTHOR = "Tomteipl"
SCRIPT_VERSION = "1.1"
SCRIPT_LICENSE = "GPL3"
SCRIPT_DESC = "Sends notifications to your desktop when you are mentioned in a channels"

weechat.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, SCRIPT_LICENSE, SCRIPT_DESC, "", "")

help = """
        Xnotif sends desktop notifications when you are pinged on a channels or message is highlighted.
        Script works on Linux distros with desktop notifications (libnotify)
        and MacOS (with sound).

        /xnotif sys - to see if you OS is supported.
        /xnotif or /xnotif help - to see this help.
    """

# -----[]-----[ System Checks ]-----[]----- #
def check_system():
    os_name = platform.system()
    if os_name == "Darwin":
        weechat.prnt("", "MacOS detected")
        return "macos"

    elif os_name == "Linux":
        weechat.prnt("", "Linux detected")
        return "linux"

    else:
        weechat.prnt("", "OS not detected!")
        return None

def check_libnotify():
    return shutil.which("notify-send") is not None
# -----[]-----[ End of Checks ]-----[]----- #

# -----[]-----[ Functions ]-----[]----- #
def get_notif(data, buffer, date, tags, displayed, highlight, prefix, message):
    if int(highlight):
        channel = weechat.buffer_get_string(buffer, "localvar_channel")
        send_notification(system_type, channel, message)
    return weechat.WEECHAT_RC_OK

#def linux_notif(data, buffer, date, tags, displayed, highlight, prefix, message):
#    if int(highlight):
#        channel = weechat.buffer_get_string(buffer, "localvar_channel")
#        send_notification("linux", channel, message)
#    return weechat.WEECHAT_RC_OK

def send_notification(system_type, title, message):
    if system_type == "macos":
        script = f'display notification "{message}" with title "{title}"'
        subprocess.run(["osascript", "-e", script])
        subprocess.run(["afplay", "/System/Library/Sounds/Ping.aiff"])

    elif system_type == "linux" and check_libnotify():
        subprocess.run(["notify-send", "-i", "dialog-information", f"Mentioned in {title}", message])
# -----[]-----[ End of Functions ]-----[]----- #

# -----[]-----[ Commands ]-----[]----- #
def commands_cb(data, buffer, args):
    if args.startswith("help"):
        weechat.prnt("", help)
        return weechat.WEECHAT_RC_OK

    elif args.startswith("sys"):
        check_system()
        return weechat.WEECHAT_RC_OK

    else:
        weechat.prnt("", help)
        return weechat.WEECHAT_RC_ERROR
# -----[]-----[ End of Commands ]-----[]----- #

# Hooks
weechat.hook_command(
    "xnotif",
    "Shows help",
    "",
    "",
    "help || sys",
    "commands_cb",
    "",
)

system_type = check_system()
if system_type == "macos" or "linux":
    weechat.hook_print("", "", "", 1, "get_notif", "")

else:
    weechat.prnt("", "Wrong OS. Notifications won't work.")
    weechat.command("", "/script unload Xnotif")

