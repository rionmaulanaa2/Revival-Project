# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/TeammateWidget/LobbyTeamateMechaTipUI.py
from __future__ import absolute_import
from six.moves import range
from common.uisys.basepanel import BasePanel
import common.const.uiconst as ui_const
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.item import item_const as iconst
from common.cfg import confmgr
from common.utils.cocos_utils import getScreenSize
from logic.gcommon.const import NEOX_UNIT_SCALE
from common.utils.ui_utils import get_scale
import time
import cc
import math3d
import math
import world
import weakref
from logic.gcommon.common_const import scene_const
from logic.gutils.dress_utils import mecha_lobby_id_2_battle_id

class LobbyTeamateMechaTipUI(object):
    screen_size = getScreenSize()
    screen_angle_limit = math.atan(getScreenSize().height / 2.0 / (getScreenSize().width / 2.0)) * 180 / math.pi
    MODEL_HEIGHT = 1.9 * NEOX_UNIT_SCALE
    SCREEN_MARGIN = get_scale('40w')

    def __init__(self, tip_nd, teamate_uid, interact_model):
        self._teamate_uid = teamate_uid
        self._interact_model = interact_model
        self._nd = tip_nd
        self._teamate_name = None
        self._space_node = None
        self.init_event()
        self.init_panel()
        return

    def init_panel(self):
        from common.uisys.uielment.CCUISpaceNode import CCUISpaceNode
        space_node = CCUISpaceNode.Create()
        space_node.setLocalZOrder(0)
        space_node.AddChild('', self._nd)

        def vis_callback(last_need_draw, cur_need_draw):
            cnt_scene = global_data.game_mgr.scene
            if not cnt_scene:
                return
            if self._nd and self._nd.isValid() and cnt_scene.scene_type == scene_const.SCENE_LOBBY:
                self._nd.setVisible(True if cur_need_draw else False)
            else:
                self._nd.setVisible(False)

        space_node.set_visible_callback(vis_callback)
        self._nd.setPosition(0, 0)
        self._space_node = space_node
        xuetiao_pos = self._interact_model.get_socket_matrix('xuetiao', world.SPACE_TYPE_WORLD)
        space_node.set_assigned_world_pos(xuetiao_pos.translation)
        if global_data.player:
            if global_data.player.uid == self._teamate_uid:
                self.update_self_team_info()
            else:
                teamate_uinfo = self.get_teamate_info()
                teamate_name = teamate_uinfo.get('char_name', None)
                self._teamate_name = teamate_name
                self.update_other_team_info(teamate_uinfo)
        return

    def on_change_name(self, cname):
        if self._teamate_uid == global_data.player.uid:
            self._nd.name.SetString(cname)

    def on_update_proficiency(self, *args):
        if self._teamate_uid == global_data.player.uid:
            self.update_self_team_info()

    def update_self_team_info(self):
        player = global_data.player
        if not player:
            return
        self._nd.name.SetString(player.get_name())
        mecha_item_no = global_data.player.get_lobby_selected_mecha_item_id()
        mecha_id = mecha_lobby_id_2_battle_id(mecha_item_no)
        level, proficiency = player.get_proficiency(mecha_id)
        proficiency_level = self.get_dan_lv(level)
        dan_conf = confmgr.get('proficiency_config', 'ProficiencyDan', str(proficiency_level), default={})
        mecha_conf = confmgr.get('mecha_display', 'HangarConfig', 'Content', str(mecha_id))
        mecha_name = get_text_by_id(dan_conf.get('name', '')) + '\xc2\xb7' + get_text_by_id(mecha_conf.get('name_mecha_text_id', ''))
        self._nd.lab_mecha.SetString(mecha_name)
        icon_path = dan_conf.get('icon_path', '')
        if icon_path:
            self._nd.img_proficiency.SetDisplayFrameByPath('', icon_path)
        if global_data.ui_mgr.get_ui('PVEMainUI'):
            self.hide()

    def get_dan_lv(self, level):
        _dan_conf = confmgr.get('proficiency_config', 'ProficiencyDan')
        _max_dan_lv = len(_dan_conf)
        dan_lv = 1
        for dan_lv in range(1, _max_dan_lv + 1):
            max_level = _dan_conf[str(dan_lv)]['max_level']
            if level < max_level:
                break

        return dan_lv

    def update_other_team_info(self, teamate_uinfo):
        teamate_name = teamate_uinfo.get('char_name', None)
        if teamate_name:
            self._nd.name.setVisible(True)
            self._nd.name.SetString(teamate_name)
        else:
            self._nd.name.setVisible(False)
        lobby_mecha_info = teamate_uinfo.get('lobby_mecha_info', None)
        if lobby_mecha_info:
            lobby_mecha_proficiency = lobby_mecha_info.get('lobby_mecha_proficiency', {})
            level = lobby_mecha_proficiency.get('level', 1)
            proficiency_level = self.get_dan_lv(level)
            dan_conf = confmgr.get('proficiency_config', 'ProficiencyDan', str(proficiency_level), default={})
            mecha_id = mecha_lobby_id_2_battle_id(lobby_mecha_info['lobby_mecha_id'])
            mecha_conf = confmgr.get('mecha_display', 'HangarConfig', 'Content', str(mecha_id))
            mecha_name = get_text_by_id(dan_conf.get('name', '')) + '\xc2\xb7' + get_text_by_id(mecha_conf.get('name_mecha_text_id', ''))
            self._nd.lab_mecha.setVisible(True)
            self._nd.lab_mecha.SetString(mecha_name)
            icon_path = dan_conf.get('icon_path', '')
            if icon_path:
                self._nd.img_proficiency.setVisible(True)
                self._nd.img_proficiency.SetDisplayFrameByPath('', icon_path)
            else:
                self._nd.img_proficiency.setVisible(False)
        else:
            self._nd.lab_mecha.setVisible(False)
            self._nd.img_proficiency.setVisible(False)
        if global_data.ui_mgr.get_ui('PVEMainUI'):
            self.hide()
        return

    def init_event(self):
        global_data.emgr.player_teammate_info_update_event += self.on_player_teammate_info_update
        global_data.emgr.visit_player_teammate_info_update_event += self.on_player_teammate_info_update
        global_data.emgr.player_on_change_name += self.on_change_name
        global_data.emgr.update_proficiency_event += self.on_update_proficiency
        global_data.emgr.lobby_ui_visible += self.on_lobby_ui_visible_update
        global_data.emgr.on_open_pve_main_ui += self.hide
        global_data.emgr.on_close_pve_main_ui += self.show

    def get_teamate_info(self):
        teammate_info = None
        teammate_info = global_data.player.get_teamate_info(self._teamate_uid) or {}
        if not teammate_info and global_data.player.get_visit_uid() == self._teamate_uid:
            teammate_info = {'char_name': global_data.player.get_visit_name(),
               'lobby_mecha_info': global_data.player.get_visit_mecha_info()
               }
        if not teammate_info:
            teammate_info = global_data.player.get_visit_teammate_info(self._teamate_uid) or {}
        return teammate_info

    def destroy(self):
        if self._space_node:
            self._space_node.Destroy()
        self._space_node = None
        self._nd = None
        self._teamate_uid = None
        self._teamate_name = None
        self._interact_model = None
        global_data.emgr.player_teammate_info_update_event -= self.on_player_teammate_info_update
        global_data.emgr.visit_player_teammate_info_update_event -= self.on_player_teammate_info_update
        global_data.emgr.player_on_change_name -= self.on_change_name
        global_data.emgr.update_proficiency_event -= self.on_update_proficiency
        global_data.emgr.lobby_ui_visible -= self.on_lobby_ui_visible_update
        global_data.emgr.on_open_pve_main_ui -= self.hide
        global_data.emgr.on_close_pve_main_ui -= self.show
        return

    def on_player_teammate_info_update(self, uid, teamate_uinfo):
        if self._teamate_uid == uid:
            self.update_other_team_info(teamate_uinfo)

    def update_ui(self):
        if global_data.player:
            teamate_uinfo = self.get_teamate_info()
            teamate_name = teamate_uinfo.get('char_name', None)
            if teamate_name and teamate_name != self._teamate_name:
                self._teamate_name = teamate_name
                self.update_other_team_info(teamate_uinfo)
        return

    def hide(self):
        if self._space_node:
            self._space_node.setVisible(False)
        self._nd.setVisible(False)

    def show(self):
        if self._space_node:
            self._space_node.setVisible(True)
        self._nd.setVisible(True)

    def on_main_ui_change(self, visible):
        if not visible:
            self.hide()
        else:
            self.show()

    def on_lobby_ui_visible_update(self, is_visible):
        if is_visible:
            self.show()
        elif not global_data.ui_mgr.get_ui('LobbySceneOnlyUI'):
            self.hide()