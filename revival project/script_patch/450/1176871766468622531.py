# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/ui_salog_utils.py
from __future__ import absolute_import

def add_uiclick_salog(click_type, click_desc=None):
    from logic.comsys.feedback import echoes
    if not global_data.player:
        return
    player = global_data.player
    battle = global_data.player.get_battle()
    if not battle:
        return
    from logic.gcommon import time_utility as tutil
    if not click_desc:
        click_desc = ''
    json_paras = [
     str(echoes.server_info['server_name']),
     str(player.id),
     str(battle.id),
     str(battle.get_battle_tid()),
     str(tutil.get_server_time() - battle.init_timestamp),
     str(click_type),
     str(click_desc)]
    from logic.gutils.salog import SALog
    salog_writer = SALog.get_instance()
    salog_writer.write_battle_log(SALog.UICLICK, json_paras)


def add_uiclick_salog_lobby(click_type):
    if not global_data.player:
        return
    player = global_data.player
    json_paras = [
     str(player.uid), str(click_type)]
    from logic.gutils.salog import SALog
    salog_writer = SALog.get_instance()
    salog_writer.write(SALog.APP_COMMENT_UI, json_paras)


def add_uiclick_add_up_salog(click_store_key_1, click_store_key_2):
    from logic.comsys.feedback import echoes
    if not global_data.player:
        return
    player = global_data.player
    battle = global_data.player.get_battle()
    if not battle:
        return
    json_paras = [
     str(echoes.server_info['server_name']),
     str(player.id),
     str(battle.id),
     str(battle.get_battle_tid()),
     str(battle.init_timestamp),
     str(click_store_key_1),
     str(click_store_key_2),
     str(battle.id),
     1]
    from logic.gutils.salog import SALog
    salog_writer = SALog.get_instance()
    salog_writer.write_battle_log(SALog.UICLICK_ADD_UP, json_paras)


def ui_operaion_salog_wrapper(func, click_type):

    def func_with_record(*args, **kwargs):
        add_uiclick_salog(click_type)
        func(*args, **kwargs)

    return func_with_record


def add_lobby_uiclick_salog(click_type, click_desc=None):
    if not global_data.player:
        return
    player = global_data.player
    if not click_desc:
        click_desc = ''
    json_paras = [
     str(player.id),
     str(click_type),
     str(click_desc)]
    from logic.gutils.salog import SALog
    salog_writer = SALog.get_instance()
    salog_writer.write(SALog.UICLICK, json_paras)