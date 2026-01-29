# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/ctrl/VirtualCodeComplement.py
import game3d
VK_PAUSE = 19
VK_LBRACKET = 219
VK_RBRACKET = 221
VK_SEMICOLON = 186
VK_QUOTE = 222
VK_BACKSLASH = 220
VK_COMMA = 188
VK_PERIOD = 190
VK_SLASH = 191
VK_SCROLL_LOCK = 145
MOUSE_BUTTON_BACK = 5
MOUSE_BUTTON_FORWARD = 6
if game3d.get_platform() == game3d.PLATFORM_ANDROID:
    VK_PAUSE = 121
    VK_LBRACKET = 71
    VK_RBRACKET = 72
    VK_SEMICOLON = 74
    VK_QUOTE = 75
    VK_BACKSLASH = 73
    VK_COMMA = 55
    VK_PERIOD = 56
    VK_SLASH = 76
    VK_SCROLL_LOCK = 116
    VK_NUM_ENTER = 160
    MOUSE_BUTTON_BACK = 1008
    MOUSE_BUTTON_FORWARD = 10016