# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/TeammateUI.py
from __future__ import absolute_import
import six_ex
import six
from six.moves import range
import weakref
import copy
from common.uisys.basepanel import BasePanel
from common.const.uiconst import SMALL_MAP_ZORDER
from common.utils.cocos_utils import getScreenSize
import cc
import math3d
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gutils.team_utils import get_teammate_colors, get_teammate_num
from logic.comsys.battle.TeammateWidget.TeammateLocateUI import TeammateLocateUI
from common.const import uiconst
from logic.entities.Battle import Battle
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode
from logic.client.const import game_mode_const
from mobile.common.EntityManager import EntityManager

class TeammateUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/empty'
    DLG_ZORDER = SMALL_MAP_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    NAME_PIC = ['icon_blue.png', 'icon_green.png', 'icon_yellow.png', 'icon_red.png']
    GLOBAL_EVENT = {'ccmini_team_speaking_list': 'refresh_team_speak',
       'on_player_inited_event': 'add_teammate',
       'add_follow_player_event': 'add_player',
       'del_follow_player_event': 'del_player',
       'battle_people_get_hurt': 'on_people_get_hurt',
       'scene_camera_player_setted_event': 'init_observe_player',
       'scene_on_teammate_change': 'on_teammate_change',
       'update_teammate_info_event': 'on_update_teammate_info',
       'on_battle_status_changed': 'on_battle_status_changed',
       'death_count_down_start': 'on_death_count_down_start',
       'death_count_down_over': 'on_death_count_down_over',
       'on_teammate_global_add_emoji': 'on_teammate_show_emoji',
       'on_teammate_global_remove_emoji': 'on_teammate_remove_emoji',
       'cam_lplayer_gulag_state_changed': 'on_cam_lplayer_gulag_state_changed'
       }

    def on_init_panel(self):
        self.observe_player_id = None
        self.player_map = {}
        self.teammate_ids = []
        self._need_check_title = global_data.battle.battle_status <= Battle.BATTLE_STATUS_PREPARE
        self.init_event()
        self.panel.setLocalZOrder(1)
        self.screen_height = getScreenSize().height
        self.screen_size = getScreenSize()
        scn = global_data.game_mgr.scene
        self.cam = weakref.ref(scn.active_camera)
        self.panel.runAction(cc.RepeatForever.create(cc.Sequence.create([
         cc.CallFunc.create(self._update_pos),
         cc.DelayTime.create(0.1)])))
        self.panel.runAction(cc.RepeatForever.create(cc.Sequence.create([
         cc.CallFunc.create(self.update_teammate_status),
         cc.DelayTime.create(1.0)])))
        self.init_observe_player()
        return

    def init_observe_player(self):
        observe_player = global_data.cam_lplayer
        if not observe_player:
            self.clear_all_players()
            return
        if observe_player.id != self.observe_player_id:
            self.clear_all_players()
            self.observe_player_id = observe_player.id
        else:
            return
        teammates = observe_player.ev_g_groupmate()
        teammate_infos = observe_player.ev_g_teammate_infos()
        self.teammate_ids = copy.deepcopy(teammates) if teammates else []
        for tid in teammates:
            is_dead = teammate_infos.get(tid, {}).get('dead', False)
            if is_dead:
                self.teammate_ids.remove(tid)

        self.set_teammates(self.teammate_ids, teammate_infos)

    def do_hide_panel(self):
        super(TeammateUI, self).do_hide_panel()
        for k, v in six.iteritems(self.player_map):
            v.hide()

    def do_show_panel(self):
        super(TeammateUI, self).do_show_panel()
        for k, v in six.iteritems(self.player_map):
            v.show()

    def update_teammate_status(self):
        bat = global_data.battle
        is_in_celebrate = bat.is_in_settle_celebrate_stage() if bat else False
        del_players = []
        for k, v in six.iteritems(self.player_map):
            if not global_data.cam_lplayer:
                break
            teammate_infos = global_data.cam_lplayer.ev_g_teammate_infos()
            if teammate_infos and not is_in_celebrate:
                is_dead = teammate_infos.get(k, {}).get('dead', False)
                if is_dead:
                    del_players.append(k)
            v.update_teammate()

        for player_id in del_players:
            self.del_player_by_id(player_id)

    def on_teammate_change(self, player_id):
        if player_id != self.observe_player_id:
            return
        else:
            self.observe_player_id = None
            self.init_observe_player()
            return

    def init_event(self):
        pass

    def on_people_get_hurt(self, people_id):
        if people_id in self.player_map:
            self.player_map[people_id].on_teammate_hurted()

    def on_finalize_panel(self):
        self.clear_all_players()

    def clear_all_players(self):
        for locate in six.itervalues(self.player_map):
            locate.destroy()

        self.player_map = {}
        self.teammate_ids = []
        self.observe_player_id = None
        return

    def set_teammates(self, teammate_ids, teammate_infos):
        if teammate_ids:
            self.teammate_ids = teammate_ids
            self.teammate_ids.sort()
            for pid in teammate_ids:
                ent = EntityManager.getentity(pid)
                if ent and ent.logic and not ent.logic.ev_g_death():
                    self.add_player(ent.logic)

    def add_teammate(self, player, *args):
        if player.id not in self.teammate_ids:
            return
        self.add_player(player)

    def add_player(self, player):
        if player.id in self.player_map or not global_data.is_judge_ob and global_data.cam_lplayer and player.id == global_data.cam_lplayer.id:
            if player.id in self.player_map:
                locate_wrapper = self.player_map[player.id]
                locate_wrapper.set_teammate(player)
            return
        is_teammate = player.id in self.teammate_ids
        self._add_player(player.id, player, is_teammate)

    def add_empty_player(self, player_id, player_info):
        if player_id in self.player_map or not global_data.is_judge_ob and global_data.cam_lplayer and player_id == global_data.cam_lplayer.id:
            return
        else:
            is_teammate = player_id in self.teammate_ids
            self._add_player(player_id, None, is_teammate)
            if player_id in self.player_map:
                locate_wrapper = self.player_map[player_id]
                locate_wrapper.init_by_teammate_info(player_info)
            return

    def _add_player(self, player_id, player, is_teammate=True):
        color_info = get_teammate_colors(self.teammate_ids)[player_id]
        player_num = get_teammate_num(self.teammate_ids)[player_id]
        locate_wrapper = TeammateLocateUI(color_info, player_num, self.panel)
        if player:
            locate_wrapper.set_teammate(player)
        if is_teammate and self._need_check_title:
            if global_data.cam_lplayer:
                teammate_infos = global_data.cam_lplayer.ev_g_teammate_infos()
                teammate_info = teammate_infos.get(player_id)
                if teammate_info:
                    rank_use_title_dict = teammate_info.get('rank_use_title_dict', {})
                    locate_wrapper.check_title(rank_use_title_dict)
        self.player_map[player_id] = locate_wrapper
        if global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_SURVIVALS):
            if len(self.player_map) >= 4:
                raise ValueError('Num of teammate player error!!!!', self.player_map, [ type(k) for k in six.iterkeys(self.player_map) ], [global_data.cam_lplayer.id, global_data.cam_lplayer.ev_g_teammate_infos()] if global_data.cam_lplayer else (None,
                                                                                                                                                                                                                                                       None), global_data.player.id if global_data.player else None)
        return

    def del_player(self, player):
        if player:
            self.del_player_by_id(player.id)

    def del_player_by_id(self, player_id):
        if player_id in self.player_map:
            self.player_map[player_id].destroy()
            del self.player_map[player_id]

    def _update_pos(self):
        cam = self.cam()
        if not cam:
            return
        cam_lplayer = global_data.cam_lplayer
        if cam and cam_lplayer:
            del_ids = []
            lplayer_pos = self.get_target_pos(cam_lplayer)
            for pid, locate in six.iteritems(self.player_map):
                ret = locate.update_nd_pos(cam, cam_lplayer, lplayer_pos)

    def refresh_team_speak(self, session_id, all_list, all_energy):
        from logic.gcommon.common_utils import ui_gameplay_utils as ui_utils
        if all_list:
            for index, eid in enumerate(all_list):
                entity_id = global_data.ccmini_mgr.get_entity_id_by_eid(eid, session_id)
                player_top_ui = self.player_map.get(entity_id, None)
                if player_top_ui:
                    voice = player_top_ui._nd.voice
                    energy_level = ui_utils.get_energy_level(all_energy[index])
                    voice.setVisible(True)
                    for i in range(3):
                        img_voice = getattr(voice, 'voice_%d' % (i + 1), None)
                        if img_voice:
                            if i + 1 <= energy_level:
                                img_voice.setVisible(True)
                            else:
                                img_voice.setVisible(False)

        else:
            for player_top_ui in six_ex.values(self.player_map):
                if player_top_ui:
                    voice = player_top_ui._nd.voice
                    voice and voice.setVisible(False)

        return

    def on_update_teammate_info(self, teammate_id, info):
        if teammate_id in self.player_map:
            if teammate_id in self.teammate_ids:
                if teammate_id in self.player_map:
                    locate_wrapper = self.player_map[teammate_id]
                    locate_wrapper.init_by_teammate_info(info)

    @execute_by_mode(False, (game_mode_const.GAME_MODE_DEATHS,))
    def on_battle_status_changed(self, status):
        if status <= Battle.BATTLE_STATUS_PREPARE:
            self.set_need_check_title(True)
        else:
            self.set_need_check_title(False)

    def set_need_check_title(self, value):
        if self._need_check_title != value:
            self._need_check_title = value
            if self._need_check_title:
                if not global_data.cam_lplayer:
                    return
                teammate_infos = global_data.cam_lplayer.ev_g_teammate_infos()
                for k, v in six.iteritems(self.player_map):
                    if global_data.player and k == global_data.player.id:
                        rank_use_title_dict = global_data.player.rank_use_title_dict
                    else:
                        teammate_info = teammate_infos.get(k, {})
                        rank_use_title_dict = teammate_info.get('rank_use_title_dict', {})
                    v.check_title(rank_use_title_dict)

            else:
                for k, v in six.iteritems(self.player_map):
                    v.check_title({})

    def on_death_count_down_start(self):
        self.set_need_check_title(True)

    def on_death_count_down_over(self):
        self.set_need_check_title(False)

    def get_target_pos(self, ltarget):
        if ltarget:
            control_target = ltarget.sd.ref_ctrl_target
            if control_target and control_target.logic:
                pos = control_target.logic.ev_g_model_position()
                return pos
        return None

    def on_teammate_show_emoji(self, pid):
        if pid in self.player_map:
            if pid in self.teammate_ids:
                locate_wrapper = self.player_map[pid]
                locate_wrapper.add_hide_reason_set('emoji')

    def on_teammate_remove_emoji(self, pid):
        if pid in self.player_map:
            if pid in self.teammate_ids:
                locate_wrapper = self.player_map[pid]
                locate_wrapper.remove_hide_reason_set('emoji')

    def on_cam_lplayer_gulag_state_changed(self, gulag_state, **kwargs):
        if not self.player_map:
            return
        from logic.gcommon.common_const.battle_const import ST_IDLE
        show_space_node = gulag_state == ST_IDLE
        for player_locate in six.itervalues(self.player_map):
            if show_space_node:
                player_locate.remove_hide_reason_set('self_gulag')
            else:
                player_locate.add_hide_reason_set('self_gulag')

    def on_teammate_enter_gulag(self, pid, enter):
        if pid not in self.player_map or pid not in self.teammate_ids:
            return
        if enter:
            self.player_map[pid].add_hide_reason_set('teammate_gulag')
        else:
            self.player_map[pid].remove_hide_reason_set('teammate_gulag')