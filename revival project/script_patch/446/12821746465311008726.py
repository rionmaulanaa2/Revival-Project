# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/TeammateWidget/LobbyTeammateTipUI.py
from __future__ import absolute_import
from common.utils.cocos_utils import getScreenSize
from logic.gcommon.const import NEOX_UNIT_SCALE
from common.utils.ui_utils import get_scale
import cc
import math
import world
from logic.gutils import role_head_utils
from logic.gcommon.cdata import dan_data
from logic.gutils.lv_template_utils import init_lv_template
from logic.gutils import season_utils
import weakref
from mobile.common.EntityManager import EntityManager
from logic.gutils.intimacy_utils import get_relation_by_uid, get_intimacy_level_by_uid, init_intimacy_icon_with_uid
from logic.gcommon.common_const.battle_const import DEFAULT_PVE_TID
UPDATE_POS_ACTION_TAG = 10000
MAX_DIST = 30 * NEOX_UNIT_SCALE
MIN_DIST = 2 * NEOX_UNIT_SCALE
MIN_SCALE = 0.1

class LobbyTeammateTipUI(object):
    screen_size = getScreenSize()
    screen_angle_limit = math.atan(getScreenSize().height / 2.0 / (getScreenSize().width / 2.0)) * 180 / math.pi
    MODEL_HEIGHT = 1.9 * NEOX_UNIT_SCALE
    SCREEN_MARGIN = get_scale('40w')
    UI_DICT = {}

    @classmethod
    def cls_update_tips(cls, unit_obj, user_data):
        model = unit_obj.ev_g_model()
        if not model:
            return
        else:
            uid = unit_obj.id
            ui = cls.UI_DICT.get(uid, None)
            if not ui:
                nd = global_data.uisystem.load_template_create('lobby/lobby_teammate_scene')
                ui = LobbyTeammateTipUI(nd, unit_obj)
                cls.UI_DICT[uid] = ui
            ui.update_team_info(user_data)
            ui.follow_model(model)
            return

    @classmethod
    def cls_destroy_ui(cls, unit_obj):
        ui = cls.UI_DICT.get(unit_obj.id, None)
        if ui:
            ui.destroy()
            del cls.UI_DICT[unit_obj.id]
        return

    def __init__(self, tip_nd, unit_obj):
        self._nd = tip_nd
        self._space_node = None
        self._scale = 1
        self._unit_obj = unit_obj
        self._uid = unit_obj.id
        scn = global_data.game_mgr.scene
        self.scene = weakref.ref(scn)
        self._lobbyui_vis = True
        self.process_event()
        self.init_panel(unit_obj)
        return

    def init_panel(self, unit_obj):
        from common.uisys.uielment.CCUISpaceNode import CCUISpaceNode
        space_node = CCUISpaceNode.Create()
        space_node.AddChild('', self._nd)

        def vis_callback(last_need_draw, cur_need_draw):
            scn = self.scene()
            if not scn:
                return
            if self._nd and self._nd.isValid() and scn == world.get_active_scene():
                is_visible = True if cur_need_draw else False
                self._nd.setVisible(is_visible)
            else:
                self._nd.setVisible(False)

        space_node.set_visible_callback(vis_callback)
        self._nd.setPosition(0, 0)
        self._space_node = space_node

    def follow_model(self, model):
        xuetiao_pos = model.get_socket_matrix('team_info', world.SPACE_TYPE_WORLD)
        self._space_node.set_assigned_world_pos(xuetiao_pos.translation)
        self._space_node.bind_model(model, 'team_info')

    def start_update_ui_pos(self):
        repeat_action = cc.RepeatForever.create(cc.Sequence.create([
         cc.DelayTime.create(0.04),
         cc.CallFunc.create(self.update_nd_pos)]))
        update_pos_action = self._nd.runAction(repeat_action)
        update_pos_action.setTag(UPDATE_POS_ACTION_TAG)

    def update_team_info(self, user_data=None):
        if user_data is None:
            user_data = self._unit_obj.ev_g_lobby_user_data()
        self.update_other_team_info(user_data)
        return

    def update_other_team_info(self, user_data):
        teamate_name = user_data.get('char_name', None)
        if teamate_name:
            self._nd.name.SetString(teamate_name)
        dan_info = user_data.get('dan_info', {})
        role_head_utils.set_role_dan(self._nd.temp_tier, dan_info)
        level = user_data.get('lv', 1)
        init_lv_template(self._nd.temp_level, level)
        survival_dan = dan_info.get('survival_dan', {})
        cur_dan = survival_dan.get('dan', dan_data.BROZE)
        cur_dan_lv = survival_dan.get('lv', dan_data.get_lv_num(dan_data.BROZE))
        dan_lv_name = season_utils.get_dan_lv_name(cur_dan, cur_dan_lv)
        self._nd.lab_tier.SetString(dan_lv_name)
        uid = user_data.get('uid', 0)
        teamate_info = global_data.player.get_teamate_info(uid)
        if teamate_info:
            is_ready = teamate_info.get('ready', False)
            battle_type = teamate_info.get('battle_type', None)
            self.on_ready_state_update(uid, is_ready, battle_type)
        rank_use_title_dict = user_data.get('rank_use_title_dict', {})
        if rank_use_title_dict:
            if not self._nd.title.nd_title:
                global_data.uisystem.load_template_create('title/i_title_normal_2', parent=self._nd.title, name='nd_title')
            if self._nd.title.nd_title:
                self._nd.title.nd_title.setVisible(True)
                from logic.gutils import template_utils
                from logic.gcommon.common_const import rank_const
                title_type = rank_const.get_rank_use_title_type(rank_use_title_dict)
                title_dict = rank_const.get_rank_use_title(rank_use_title_dict)
                template_utils.init_rank_title(self._nd.title.nd_title, title_type, title_dict, icon_scale=0.85)
        elif self._nd.title.nd_title:
            self._nd.title.nd_title.setVisible(False)
        init_intimacy_icon_with_uid(self._nd.temp_intimacy, uid)
        if global_data.ui_mgr.get_ui('PVEMainUI'):
            self.hide()
        return

    def on_show_emoji_event(self, pid, emoji_item_id, is_show):
        if pid in LobbyTeammateTipUI.UI_DICT:
            ui = LobbyTeammateTipUI.UI_DICT[pid]
            if ui:
                if is_show:
                    ui.hide()
                elif not self._lobbyui_vis:
                    if global_data.ui_mgr.get_ui('LobbySceneOnlyUI'):
                        self.show()
                else:
                    self.show()

    def update_nd_pos(self):
        scene = self.scene()
        if not (scene and scene.valid):
            return
        cam_lplayer = global_data.lobby_player
        if not cam_lplayer:
            return
        lplayer_pos = cam_lplayer.ev_g_position()
        if not lplayer_pos:
            return
        unit_obj = EntityManager.getentity(self._uid)
        if not (unit_obj and unit_obj.logic):
            return
        unit_obj = unit_obj.logic
        self_position = unit_obj.ev_g_position()
        if not self_position:
            return
        self.update_scale(self_position, lplayer_pos)

    def update_scale(self, self_position, lplayer_pos):
        if not self._space_node:
            return
        if not self_position or not lplayer_pos:
            return
        diff_vec = self_position - lplayer_pos
        dist = diff_vec.length
        scale = 1
        if dist >= MAX_DIST:
            scale = MIN_SCALE
        elif dist <= MIN_DIST:
            scale = 1
        else:
            scale = (MAX_DIST - dist) / (MAX_DIST - MIN_DIST) * (1 - MIN_SCALE) + MIN_SCALE
        self._space_node.setScale(scale)

    def process_event(self, is_init=True):
        event_list = [
         (
          global_data.emgr.player_set_ready_event, self.on_ready_state_update),
         (
          global_data.emgr.lobby_ui_visible, self.on_lobby_ui_visible_update),
         (
          global_data.emgr.message_refresh_intimacy_data, self.update_team_info),
         (
          global_data.emgr.show_emoji_event, self.on_show_emoji_event),
         (
          global_data.emgr.on_open_pve_main_ui, self.hide),
         (
          global_data.emgr.on_close_pve_main_ui, self.show)]
        for hook, handle in event_list:
            if is_init:
                hook += handle
            else:
                hook -= handle

    def on_lobby_ui_visible_update(self, is_visible):
        self._lobbyui_vis = is_visible
        if is_visible:
            self.show()
        elif not global_data.ui_mgr.get_ui('LobbySceneOnlyUI'):
            self.hide()

    def on_ready_state_update(self, uid, is_ready, battle_type):
        if uid != self._uid:
            return
        self._nd.img_ready.setVisible(is_ready and battle_type != DEFAULT_PVE_TID)

    def destroy(self):
        self.process_event(False)
        if self._space_node:
            self._space_node.Destroy()
        self._space_node = None
        self._nd = None
        return

    def hide(self):
        if self._space_node:
            self._space_node.setVisible(False)
        self._nd.setVisible(False)
        self._nd.stopActionByTag(UPDATE_POS_ACTION_TAG)

    def show(self):
        if self._space_node:
            self._space_node.setVisible(True)
        self._nd.setVisible(True)
        self.start_update_ui_pos()