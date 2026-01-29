# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/item/client_item_check_handler.py
from __future__ import absolute_import
import logic.gcommon.time_utility as t_util
import logic.gcommon.common_const.mecha_const as mconst
if G_IS_CLIENT:
    from logic.client.const import game_mode_const

    def client_check_use_reset_mecha_item(unit_obj, item_id, args):
        if not unit_obj.ev_g_below_use_item_limit(item_id):
            return (False, 17021)
        if not unit_obj.ev_g_get_bind_mecha_type():
            return (False, 17023)
        if unit_obj.ev_g_is_in_mecha():
            return (False, 17022)
        cd_type, total_cd, left_time = unit_obj.ev_g_get_change_state()
        battle = unit_obj.get_battle()
        if battle.is_in_ace_state and cd_type == mconst.RECOVER_CD_TYPE_DISABLE:
            return (False, 17024)
        return (
         True, '')


    def client_check_use_reset_mecha_item_in_exercise(unit_obj, item_id, *args):
        if not unit_obj.ev_g_below_use_item_limit(item_id):
            in_exercise = global_data.game_mode.get_mode_type() == game_mode_const.GAME_MODE_EXERCISE
            if not in_exercise:
                return (False, 17021)
        if not unit_obj.ev_g_get_bind_mecha_type():
            return (False, 17023)
        if unit_obj.ev_g_is_in_mecha():
            return (False, 17022)
        cd_type, total_cd, left_time = unit_obj.ev_g_get_change_state()
        battle = unit_obj.get_battle()
        if battle.is_in_ace_state and cd_type == mconst.RECOVER_CD_TYPE_DISABLE:
            return (False, 17024)
        return (
         True, '')


    def client_check_use_in_concert(unit_obj, item_id, args):
        from logic.client.const import game_mode_const
        if unit_obj.ev_g_is_in_mecha():
            return (False, 1600085)
        if global_data.game_mode and global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_CONCERT):
            if global_data.battle.is_duel_player(unit_obj.id):
                return (False, 18144)
        return (
         True, '')


    def check_not_in_water(unit_obj, item_id, args):
        from logic.gcommon.common_const.water_const import WATER_NONE
        if unit_obj.sd.ref_water_status == WATER_NONE:
            return (True, '')
        return (False, 18295)