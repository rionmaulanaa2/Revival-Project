# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/gamemode/CNBombMode.py
from __future__ import absolute_import
from logic.gcommon.common_const import battle_const
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.comsys.battle.NBomb.NBombBattleDefines import POWER_CORE_ID, SPACE_CORE_ID, SPEED_CORE_ID, NBOMB_NEWBIE_GUIDE_KEY, CORE_ID_2_ICON
from logic.comsys.battle.NBomb import nbomb_utils
from logic.entities.Battle import Battle
from mobile.common.EntityManager import EntityManager
from logic.gcommon.common_utils import parachute_utils
from logic.vscene.parts.gamemode.CNormalMode import CNormalBase

class CNBombMode(CNormalBase):

    def __init__(self, map_id):
        self.map_id = map_id
        self.lst_complete = []
        self.real_game_over = False
        self.init_parameters()
        self.init_mgr()
        self.process_event(True)

    def on_finalize(self):
        super(CNBombMode, self).on_finalize()
        self.process_event(False)
        self.show_screen_sfx(False)
        self.clear_nbomb_defense_icon()
        self.destroy_ui()
        global_data.nbomb_battle_data and global_data.nbomb_battle_data.finalize()

    def init_parameters(self):
        pass

    def init_mgr(self):
        super(CNBombMode, self).init_mgr()
        self.init_battle_data()

    def init_battle_data(self):
        from logic.comsys.battle.NBomb.NBombBattleData import NBombBattleData
        NBombBattleData()

    def destroy_ui(self):
        global_data.ui_mgr.close_ui('NBombCoreCollectUI')
        global_data.ui_mgr.close_ui('NBombCountDownUI')
        global_data.ui_mgr.close_ui('PlayIntroduceUI')
        global_data.ui_mgr.close_ui('NBombRuleTipsUI')
        global_data.ui_mgr.close_ui('NBombStartReadyUI')

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'scene_add_entity_event': self.on_add_entity,
           'on_battle_status_changed': self.on_battle_status_changed,
           'nbomb_update_ui_show': self.on_update_ui_show,
           'nbomb_core_got_status': self.on_update_core_ownership,
           'nbomb_core_got_status_our_group': self.on_update_our_group_core_ownership,
           'nbomb_start_install': self.on_start_nbomb_install,
           'nbomb_stop_install': self.on_stop_nbomb_install,
           'nbomb_show_tips': self.on_show_nbomb_tips,
           'switch_control_target_event': self.on_switch_control_target,
           'nbomb_update_explosion': self.on_update_explosion,
           'nbomb_clear_war': self.on_finalize,
           'settle_stage_event': self.on_settle_stage,
           'fight_tips_finish_event': self.on_show_tips_finished,
           'on_observer_parachute_stage_changed': self.on_parachute_stage_changed,
           'on_player_parachute_stage_changed': self.on_parachute_stage_changed,
           'scene_camera_player_setted_event': self.on_scene_camera_player_setted,
           'stop_player_damage_event': self.show_settle_statistics,
           'spectate_battle_finish_event': self.on_spectate_battle_finish,
           'judge_ob_settle_event': self.on_spectate_battle_finish
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_spectate_battle_finish(self, *args):
        self.real_game_over = True
        self.destroy_ui()

    def show_settle_statistics(self):
        self.real_game_over = True
        self.destroy_ui()

    def on_settle_stage(self, *args):
        self.destroy_ui()

    def on_battle_status_changed(self, status):
        is_showed = global_data.achi_mgr.get_cur_user_archive_data(NBOMB_NEWBIE_GUIDE_KEY, False)
        if status == Battle.BATTLE_STATUS_PREPARE:
            if not is_showed and global_data.battle.is_in_island():
                self.show_newbie_guide(True)
                global_data.achi_mgr.set_cur_user_archive_data(NBOMB_NEWBIE_GUIDE_KEY, True)
                return
        self.show_newbie_guide(False)

    def on_parachute_stage_changed(self, stage):
        if self.real_game_over:
            return
        if stage in [parachute_utils.STAGE_ISLAND, parachute_utils.STAGE_PLANE, parachute_utils.STAGE_PRE_PARACHUTE]:
            global_data.nbomb_battle_data.is_ready_state = False
        elif stage == parachute_utils.STAGE_LAND:
            global_data.nbomb_battle_data.is_ready_state = True
            self.on_update_ui_show()

    def show_newbie_guide(self, is_show):
        if is_show:
            from logic.comsys.lobby.PlayIntroduceUI import PlayIntroduceUI
            PlayIntroduceUI(None, 51)
        else:
            global_data.ui_mgr.close_ui('PlayIntroduceUI')
        return

    def on_scene_camera_player_setted(self, *args):
        if not global_data.cam_lplayer:
            return
        self.on_update_ui_show()

    def on_update_ui_show(self, info=None):
        if self.real_game_over:
            return
        if not nbomb_utils.is_data_ready():
            return
        is_placed_nbomb_cb = (info or {}).get('is_placed_nbomb_cb', False)
        is_placed_nbomb = global_data.nbomb_battle_data.get_nbomb_cd_timestamp() > 0
        is_nbomb_core_spawned = global_data.nbomb_battle_data.is_nbomb_core_spawned
        if is_placed_nbomb:
            self.close_collect_ui()
            if not is_placed_nbomb_cb:
                self.show_count_down_ui()
        elif is_nbomb_core_spawned:
            self.show_collect_ui()
        else:
            self.close_collect_ui()
            global_data.ui_mgr.close_ui('NBombCountDownUI')

    def close_collect_ui(self):
        global_data.ui_mgr.close_ui('NBombCoreCollectUI')
        global_data.ui_mgr.close_ui('NBombStartReadyUI')

    def show_collect_ui(self, core_exchange_info=None):
        global_data.ui_mgr.close_ui('NBombCountDownUI')
        ui = global_data.ui_mgr.get_ui('NBombCoreCollectUI')
        if not ui:
            ui = global_data.ui_mgr.show_ui('NBombCoreCollectUI', 'logic.comsys.battle.NBomb')
        ui and ui.update_nbomb_core_btn(core_exchange_info)
        return ui

    def show_count_down_ui(self):
        self.close_collect_ui()
        nbomb_exploded = global_data.nbomb_battle_data.nbomb_exploded
        nbomb_destroyed = global_data.nbomb_battle_data.nbomb_destroyed
        if nbomb_exploded or nbomb_destroyed:
            return
        ui = global_data.ui_mgr.get_ui('NBombCountDownUI')
        if not ui:
            ui = global_data.ui_mgr.show_ui('NBombCountDownUI', 'logic.comsys.battle.NBomb')
        ui and ui.update_count_down()
        self.show_role_tips()
        return ui

    def is_nomb_exploded(self):
        if global_data.nbomb_battle_data:
            return global_data.nbomb_battle_data.nbomb_exploded
        return False

    def on_update_core_ownership(self):
        _core_soul_ids = global_data.nbomb_battle_data.get_nbomb_core_soul_ids()
        for entity_id in _core_soul_ids:
            self._update_nbomb_mark_show(entity_id)

    def on_update_our_group_core_ownership(self, core_exchange_info=None):
        if self.real_game_over:
            return
        is_placed_nbomb = global_data.nbomb_battle_data.get_nbomb_cd_timestamp() > 0
        is_nbomb_core_spawned = global_data.nbomb_battle_data.is_nbomb_core_spawned
        if is_nbomb_core_spawned and not is_placed_nbomb:
            self.show_collect_ui(core_exchange_info)
        else:
            self.close_collect_ui()

    def on_start_nbomb_install(self):
        ui = global_data.ui_mgr.get_ui('NBombCoreCollectUI')
        ui and ui.on_start_install_nbomb()

    def on_stop_nbomb_install(self):
        ui = global_data.ui_mgr.get_ui('NBombCoreCollectUI')
        ui and ui.on_stop_install_nbomb()

    def get_logic(self, entity_id):
        entity = EntityManager.getentity(entity_id)
        if not entity or not entity.logic:
            return None
        else:
            ctarget = entity.logic.ev_g_control_target()
            if ctarget and ctarget.logic:
                return ctarget.logic
            return None

    def _update_nbomb_mark_show(self, entity_id):
        entity_logic = self.get_logic(entity_id)
        entity_logic and entity_logic.send_event('E_NBOMB_SHOW_HEAD_MARK')

    def on_switch_control_target(self, control_target_id, pos, *args):
        self.on_update_ui_show()

    def on_add_entity(self, entity_id):
        self._update_nbomb_mark_show(entity_id)

    def on_update_explosion(self, explosion_time, group_id, player_ids):
        is_install_nbomb = global_data.nbomb_battle_data.is_install_nbomb()
        self.show_screen_sfx(is_install_nbomb)
        self.on_show_nbomb_defense_icon(player_ids)

    def on_show_nbomb_defense_icon(self, player_ids):
        _set_player_ids = list(set(self.lst_complete + player_ids))
        for player_id in _set_player_ids:
            entity_logic = self.get_logic(player_id)
            if not entity_logic:
                continue
            entity_logic.send_event('E_NBOMB_SHOW_HEAD_MARK')

        self.lst_complete = player_ids

    def clear_nbomb_defense_icon(self):
        for player_id in self.lst_complete:
            entity_logic = self.get_logic(player_id)
            if not entity_logic:
                continue
            entity_logic.send_event('E_NBOMB_CLEAR_MARK')

        self.lst_complete = []

    def show_screen_sfx(self, is_show):
        if is_show:
            global_data.emgr.show_screen_effect.emit('ScreenNBombPlaced', {})
        else:
            global_data.emgr.destroy_screen_effect.emit('ScreenNBombPlaced')

    def show_role_tips(self):
        ui = global_data.ui_mgr.get_ui('NBombRuleTipsUI')
        if not ui:
            ui = global_data.ui_mgr.show_ui('NBombRuleTipsUI', 'logic.comsys.battle.NBomb')
        ui and ui.update_display()

    def on_show_nbomb_tips(self, tips_type, tips_data=None):
        self_group_id = global_data.nbomb_battle_data.get_self_group_id()
        is_self_camp_installed = global_data.nbomb_battle_data.is_self_group_install_nbomb()
        message = {'in_anim': 'appear',
           'out_anim': 'disappear'
           }
        tips_align = 'top'
        if tips_type == battle_const.NBOMB_TIP_NBOMB_START:
            self_path = 'gui/ui_res_2/battle_bomb/bar_battle_bomb_tips_start_0.png'
            emeny_path = 'gui/ui_res_2/battle_bomb/bar_battle_bomb_tips_start_1.png'
            message.update({'i_type': battle_const.NBOMB_DEVICE_PLACE_SUCCEED,
               'bar_path': self_path if is_self_camp_installed else emeny_path,
               'lab_title2': get_text_by_id(18306) if is_self_camp_installed else get_text_by_id(18307)
               })
        elif tips_type == battle_const.NBOMB_TIP_NBOMB_EXPLODE:
            tips_align = 'middle'
            self_icon_path = 'gui/ui_res_2/battle_bomb/icon_battle_bomb_tips_warning_blue.png'
            emeny_icon_path = 'gui/ui_res_2/battle_bomb/icon_battle_bomb_tips_warning_red.png'
            self_path = 'gui/ui_res_2/battle_bomb/bar_battle_bomb_tips_end_0.png'
            emeny_path = 'gui/ui_res_2/battle_bomb/bar_battle_bomb_tips_end_1.png'
            message.update({'i_type': battle_const.NBOMB_DEVICE_EXPLOSION,
               'icon_path': self_icon_path if is_self_camp_installed else emeny_icon_path,
               'icon_path2': self_icon_path if is_self_camp_installed else emeny_icon_path,
               'bar_path': self_path if is_self_camp_installed else emeny_path,
               'lab_title2': get_text_by_id(18310) if is_self_camp_installed else get_text_by_id(18311)
               })
        elif tips_type == battle_const.NBOMB_TIP_NBOMB_ILLEGAL_AREA:
            message.update({'i_type': battle_const.NBOMB_DEVICE_PLACE_ERROR,
               'lab_title2': get_text_by_id(18315)
               })
        elif tips_type == battle_const.NBOMB_TIP_BLEED:
            message.update({'i_type': battle_const.NBOMB_DEVICE_STATUS_ERROR,
               'lab_title2': get_text_by_id(18333)
               })
        elif tips_type == battle_const.NBOMB_TIP_NBOMB_DESTROY:
            tips_align = 'middle'
            message.update({'i_type': battle_const.NBOMB_DEVICE_REMOVE})
        elif tips_type == battle_const.NBOMB_TIP_FIRST_HIT:
            message.update({'i_type': battle_const.NBOMB_DEVICE_BE_HIT})
        elif tips_type == battle_const.NBOMB_TIP_CORE_SPAWNED:
            message.update({'i_type': battle_const.NBOMB_CORE_APPEAR,
               'lab_title': get_text_by_id(18316),
               'lab_title2': get_text_by_id(18317)
               })
        elif tips_type == battle_const.NBOMB_TIP_CORE_MOVE:
            CONFIG_ID_2_TEXT_ID = {POWER_CORE_ID: 18334,
               SPACE_CORE_ID: 18335,
               SPEED_CORE_ID: 18336
               }
            core_config_id = tips_data['item_no']
            message.update({'i_type': battle_const.NBOMB_CORE_TRANSFER,
               'lab_title': get_text_by_id(CONFIG_ID_2_TEXT_ID[core_config_id]),
               'lab_title2': get_text_by_id(18317)
               })
            global_data.emgr.nbomb_show_map_overview.emit({'target_pos': tips_data.get('target_pos')})
        elif tips_type == battle_const.NBOMB_TIP_COLLECT_ALL_CORES:
            is_self_group_collect_all = self_group_id == tips_data['group_id']
            self_path = 'gui/ui_res_2/battle_bomb/bar_battle_bomb_tips_complete_0.png'
            emeny_path = 'gui/ui_res_2/battle_bomb/bar_battle_bomb_tips_complete_1.png'
            message.update({'i_type': battle_const.NBOMB_CORE_COLLECT_COMPLETE,
               'bar_path': self_path if is_self_group_collect_all else emeny_path,
               'lab_title': get_text_by_id(18318) if is_self_group_collect_all else get_text_by_id(18320),
               'lab_title2': get_text_by_id(18319) if is_self_group_collect_all else get_text_by_id(18321)
               })
        elif tips_type == battle_const.NBOMB_TIP_PICK_CORE:
            CONFIG_ID_2_TEXT_ID = {POWER_CORE_ID: [
                             18325, 18328],
               SPACE_CORE_ID: [
                             18326, 18329],
               SPEED_CORE_ID: [
                             18327, 18330]
               }
            CORE_EFFECT_TEXT_ID = {POWER_CORE_ID: 18350,
               SPACE_CORE_ID: 18351,
               SPEED_CORE_ID: 18352
               }
            self_path = 'gui/ui_res_2/battle_bomb/bar_battle_bomb_tips_common_0.png'
            emeny_path = 'gui/ui_res_2/battle_bomb/bar_battle_bomb_tips_common_1.png'
            core_config_id = tips_data['item_no']
            is_self_group = self_group_id == tips_data['group_id']
            content_txt_id = CONFIG_ID_2_TEXT_ID[core_config_id][0] if is_self_group else CONFIG_ID_2_TEXT_ID[core_config_id][1]
            effect_txt_id = CORE_EFFECT_TEXT_ID[core_config_id] if is_self_group else 18331
            message.update({'i_type': battle_const.NBOMB_CORE_PICKUP,
               'icon_path': CORE_ID_2_ICON[core_config_id],
               'bar_path': self_path if is_self_group else emeny_path,
               'lab_title': get_text_by_id(content_txt_id),
               'lab_title2': get_text_by_id(effect_txt_id)
               })
            global_data.emgr.nbomb_show_map_overview.emit({'target_pos': tips_data.get('target_pos')})
        elif tips_type == battle_const.NBOMB_TIP_LOST_CORE:
            CONFIG_ID_2_TEXT_ID = {POWER_CORE_ID: 18322,
               SPACE_CORE_ID: 18323,
               SPEED_CORE_ID: 18324
               }
            core_config_id = tips_data['item_no']
            message.update({'i_type': battle_const.NBOMB_CORE_DROP,
               'content_txt': get_text_by_id(CONFIG_ID_2_TEXT_ID[core_config_id])
               })
        if tips_align == 'middle':
            global_data.emgr.show_battle_med_message.emit((message,), battle_const.MED_NODE_RECRUIT_COMMON_INFO)
        else:
            global_data.emgr.show_battle_main_message.emit(message, battle_const.MAIN_NODE_COMMON_INFO)

    def on_show_tips_finished(self, t_message):
        message = t_message[0]
        tips_type = message.get('i_type', None)
        if tips_type == battle_const.NBOMB_DEVICE_PLACE_SUCCEED:
            self.show_count_down_ui()
        return