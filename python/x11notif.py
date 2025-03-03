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
import shutil


SCRIPT_NAME = "x11notif"
SCRIPT_AUTHOR = "Tomteipl"
SCRIPT_VERSION = "1.0"
SCRIPT_LICENSE = "GPL3"
SCRIPT_DESC = "Sends notifications to your desktop when you are mentioned in a channel"


weechat.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, SCRIPT_LICENSE, SCRIPT_DESC, "", "")

help = """
    x11Notif will work if:

        * You are using X11
        * You have /notify-send/ that comes with /libnotify/
        * You are running notification daemon for example /GNOME/KDE's/mako/dunst/ etc.

    So basically it should work on most of the desktop environments.
        """

# Check if libnotify is installed
def check_libnotify():
    return shutil.which("notify-send") is not None

# Send notification function
def smart_notif(data, buffer, date, tags, displayed, highlight, prefix, message):
    if int(highlight) and check_libnotify():
        channel = weechat.buffer_get_string(buffer, "localvar_channel")
        send_notif = "notify-send -i dialog-information 'Mentioned in {}' '{}'".format(channel, message)
        weechat.hook_process(send_notif, 0, "", "")
    return weechat.WEECHAT_RC_OK

# Commands
def commands_cb(data, buffer, args):
    if args.startswith("help"):
        weechat.prnt("", f"{help}")
        return weechat.WEECHAT_RC_OK

    else:
        weechat.prnt("", f"{help}")
        return weechat.WEECHAT_RC_OK

# Hooks
weechat.hook_command(
    "xnotif",
    "Sends notifications to your desktop when you are mentioned in a channel",
    "",
    "",
    "help",
    "commands_cb",
    "",
)
weechat.hook_print("", "", "", 1, "smart_notif", "")

if not check_libnotify():
    weechat.prnt("", "You don't have notify-send installed. X11Notif will not work.")
    weechat.prnt("", "Please install libnotify and try again.")
    weechat.prnt("", "Exiting...")
    weechat.command("", "/script unload X11notif")
    exit(1)
