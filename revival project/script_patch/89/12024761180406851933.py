# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/units/LLobbyPuppet.py
from __future__ import absolute_import
from logic.gcommon.component.Unit import Unit
from logic.gcommon.component.com_factory import component

@component(client=('com_lobby_char.ComLobbyPuppetUserData', 'com_lobby_char.com_lobby_appearance.ComPuppetTeamateTips',
                   'com_lobby_char.com_lobby_appearance.ComLobbyEmoji', 'com_lobby_char.com_lobby_appearance.ComLobbyMoveAppr',
                   'com_lobby_char.com_lobby_appearance.ComLobbySoundEffect', 'com_lobby_char.com_lobby_appearance.ComLobbyCelebrate',
                   'com_lobby_char.com_lobby_appearance.ComLobbyChatUI', 'com_lobby_char.ComLobbyModel',
                   'com_global_sync.ComLobbyPlayerSender', 'com_character_ctrl.ComSpringAnim',
                   'com_simple_sync.ComSimpleMoveSyncReceiver', 'com_simple_sync.ComSimpleJumpSyncReceiver',
                   'com_lobby_char.ComWeaponLobby', 'com_lobby_char.ComJumpLobby',
                   'com_lobby_char.ComClimbLobby', 'ComHairLogic'))
class LLobbyPuppet(Unit):
    pass