# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/item/client_item_use_handler.py
from __future__ import absolute_import
import logic.gcommon.time_utility as t_util
import logic.gcommon.common_const.mecha_const as mconst
if G_IS_CLIENT:

    def client_on_use_fireworks_item(unit_obj, item_id, args):
        from logic.gcommon.common_const.character_anim_const import UP_BODY, LOW_BODY
        from common.cfg import confmgr
        from logic.gcommon.cdata import status_config
        fireworks_data = confmgr.get('ai_concert_conf', 'FireworkSetting', 'Content', str(item_id), default={})
        sfx_path = fireworks_data.get('firework_sfx', '')
        timeline_action = fireworks_data.get('action', [])
        sfx_timeline_action = []
        for t, action_info in timeline_action:
            key_named_sfx_path_info = action_info.get('res_effect', {}).get('sfx_path')
            if not key_named_sfx_path_info:
                sfx_timeline_action.append([t, action_info])
            else:
                new_action_info = dict(action_info)
                new_action_info['res_effect'] = dict(action_info['res_effect'])
                new_action_info['res_effect'][sfx_path] = key_named_sfx_path_info
                del new_action_info['res_effect']['sfx_path']
                sfx_timeline_action.append([t, new_action_info])

        if not unit_obj.ev_g_status_check_pass(status_config.ST_CUSTOM_ACTIONS):
            return False
        if fireworks_data.get('trigger_chat_msg') and global_data.player:
            avoid_circle = global_data.game_mode.get_cfg_data('play_data').get('far_fireworks_avoid_area', {}).get('circle', [0, 0, 0])

            def send_firework_msg():
                import math3d
                import random
                pos = unit_obj.ev_g_position()
                forward = unit_obj.ev_g_forward()
                radius = avoid_circle[2] + random.randint(0, 100)
                firework_pos = math3d.vector(avoid_circle[0], pos.y + 100, avoid_circle[1]) + forward * radius
                from logic.gcommon.common_const import chat_const
                extra_data = {'type': chat_const.MSG_TYPE_CONCERT_FIREWORK,
                   'player_name': global_data.player.char_name,
                   'firework_pos': [
                                  firework_pos.x, firework_pos.y, firework_pos.z],
                   'entity_id': str(unit_obj.id),
                   'firework_id': item_id
                   }
                global_data.player.send_msg(chat_const.CHAT_BATTLE_WORLD, '', extra=extra_data)

            send_firework_msg()
        unit_obj.send_event('E_PERFORM_UNMOVABLE_ACTION_START', str(item_id), sfx_timeline_action, {'need_cache_anim': True}, fireworks_data.get('firework_camera'))
        return True


    def client_on_use_concert_light_stick_item(unit_obj, item_id, *args):
        return True


    def client_on_anniversary_salute(unit_obj, item_id, *args):
        return True


    def pve_get_story_debris(unit_obj, item_id, *args):
        global_data.emgr.pve_get_story_debris.emit()


    def pve_get_mecha_debris(unit_obj, item_id, *args):
        global_data.emgr.pve_get_mecha_debris.emit(item_id)


    last_get_coin_time = 0
    last_get_shield_time = 0
    last_get_crystal_time = 0

    def pve_get_coin(unit_obj, item_id, *args):
        global last_get_coin_time
        if global_data.mecha and global_data.mecha.logic:
            model = global_data.mecha.logic.ev_g_model()
            if model and model.valid:
                if global_data.game_time - last_get_coin_time > 0.5:
                    last_get_coin_time = global_data.game_time
                    global_data.sfx_mgr.create_sfx_on_model('effect/fx/monster/pve/pve_dl_huobi_huoqu.sfx', model, 'fx_buff')
                global_data.sound_mgr.post_event_2d_with_opt('Play_ui_pve_get', None, 1.0)
        return


    def pve_get_shield(unit_obj, item_id, *args):
        global last_get_shield_time
        if global_data.mecha and global_data.mecha.logic:
            model = global_data.mecha.logic.ev_g_model()
            if model and model.valid:
                if global_data.game_time - last_get_shield_time > 0.6:
                    last_get_shield_time = global_data.game_time
                    global_data.sfx_mgr.create_sfx_on_model('effect/fx/monster/pve/pve_dl_hundun_huoqu.sfx', model, 'fx_buff')
                global_data.sound_mgr.post_event_2d_with_opt('Play_ui_pve_get', None, 1.0)
        return


    def pve_get_crystal(unit_obj, item_id, *args):
        global last_get_crystal_time
        if global_data.mecha and global_data.mecha.logic:
            model = global_data.mecha.logic.ev_g_model()
            if model and model.valid:
                if global_data.game_time - last_get_crystal_time > 0.3:
                    last_get_crystal_time = global_data.game_time
                    global_data.sfx_mgr.create_sfx_on_model('effect/fx/monster/pve/pve_dl_jinbi_huoqu.sfx', model, 'fx_buff')
                global_data.sound_mgr.post_event_2d_with_opt('Play_ui_pve_get', None, 1.0)
        return