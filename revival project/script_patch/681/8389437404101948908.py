# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/housesys/ModelArrowUI.py
from __future__ import absolute_import
import six
import six_ex
from six.moves import range
import world
from common.uisys.basepanel import BasePanel
import time
import common.const.uiconst
from cocosui import cc, ccui, ccs
from common.const.property_const import *
from common.cfg import confmgr
import logic.comsys.message.message_data as message_data
from common.uisys.uielment.CCRichText import CCRichText
from logic.gutils import locate_utils
from logic.gutils import template_utils
from logic.gcommon.common_const import rank_const
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_const.team_const import TEAM_SUMMON_VALID_TIME
import render
from logic.gcommon.item import item_const as iconst
from logic.gutils.item_utils import jump_to_ui
import collision
from common.utils.cocos_utils import neox_pos_to_cocos, cocos_pos_to_neox
from logic.gcommon.const import LOBBY_MODEL_TOUCH_MAX_DISTANCE, LOBBY_TV_TOUCH_MAX_DISTANCE, LOBBY_MECHA_RANK_MAX_DISTANCE, LOBBY_COMPUTER_TOUCH_MAX_DISTANCE
import common.utils.timer as timer
from common.platform.dctool import interface
from common.const import uiconst
MODEL_ARROW_DICT = {'box_mecha': {'ui_node': 'nd_scene_ui0',
                 'check_func': None,
                 'interactui_update_enabled': True,
                 'hide_when_visiting': True,
                 'touch_distance': LOBBY_MODEL_TOUCH_MAX_DISTANCE,
                 'model_offset': 0
                 },
   'box_computer_3': {'ui_node': 'nd_scene_ui2',
                      'check_func': None,
                      'interactui_update_enabled': True,
                      'hide_when_visiting': True,
                      'touch_distance': LOBBY_COMPUTER_TOUCH_MAX_DISTANCE,
                      'model_offset': 0
                      },
   'box_computer_5': {'ui_node': 'nd_scene_ui3',
                      'check_func': None,
                      'interactui_update_enabled': True,
                      'hide_when_visiting': False,
                      'touch_distance': LOBBY_COMPUTER_TOUCH_MAX_DISTANCE * 2,
                      'model_offset': 0
                      },
   'dt_prop_xianshiqi_02': {'ui_node': 'nd_scene_ui1',
                            'check_func': None,
                            'interactui_update_enabled': True,
                            'hide_when_visiting': False,
                            'touch_distance': LOBBY_TV_TOUCH_MAX_DISTANCE,
                            'model_offset': 0
                            }
   }

class ModelArrowUI(BasePanel):
    DLG_ZORDER = common.const.uiconst.LOW_MESSAGE_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    PANEL_CONFIG_NAME = 'lobby/i_scene_ui_arrow'

    def on_init_panel(self, *args, **kargs):
        self.init_params()
        self.init_ui()
        self.process_event(True)

    def init_params(self):
        self.lobby_mechas = {}
        self.rank_widgets = [
         self.panel.temp_title]
        self._node_data_dict = {}
        self._model_interactui_update_enabled = {}
        for model_name, node_data in six_ex.items(MODEL_ARROW_DICT):
            check_func = node_data.get('check_func')
            if check_func and callable(check_func) and not check_func():
                continue
            self._node_data_dict[model_name] = node_data
            self._model_interactui_update_enabled[model_name] = node_data.get('interactui_update_enabled')

        self.timer = global_data.game_mgr.register_logic_timer(self.update_interact_ui, interval=1, times=-1, mode=timer.LOGIC)

    def init_ui(self):
        self.panel.temp_title.setVisible(False)
        self.panel.PlayAnimation('scene_tips')
        self._check_model_interactui_update_enabled(True)
        self.refresh_message_board_new()
        self.refresh_tv_new()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'player_enter_visit_scene_event': self._on_player_enter_visit_scene_event,
           'player_leave_visit_scene_event': self._on_player_leave_visit_scene_event,
           'net_login_reconnect_event': self.on_login_reconnect,
           'show_lobby_mecha_model': self.on_show_lobby_mecha_model,
           'message_on_players_detail_inf': self.refresh_mecha_titles,
           'message_on_set_rank_title': self.refresh_mecha_titles,
           'refresh_message_board_new': self.refresh_message_board_new,
           'visit_place_change_event': self.on_visit_place_change,
           'refresh_tv_new': self.refresh_tv_new
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_login_reconnect(self, *args):
        if self.timer:
            global_data.game_mgr.unregister_logic_timer(self.timer)
        self.timer = global_data.game_mgr.register_logic_timer(self.update_interact_ui, interval=1, times=-1, mode=timer.LOGIC)

    def _check_model_interactui_update_enabled(self, hideWhenDisabled):
        show_interact = False if not global_data.player or global_data.player.is_visit_others() else True
        for model_name, node_data in six_ex.items(self._node_data_dict):
            if node_data.get('hide_when_visiting') == True:
                self._model_interactui_update_enabled[model_name] = show_interact
                ui_node = getattr(self, node_data.get('ui_node'))
                ui_node and hideWhenDisabled and not show_interact and ui_node.setVisible(show_interact)

    def _on_player_enter_visit_scene_event(self, *args):
        self._check_model_interactui_update_enabled(True)

    def _on_player_leave_visit_scene_event(self):
        self._check_model_interactui_update_enabled(True)

    def on_show_lobby_mecha_model(self, uid, model):
        pass

    def _get_rank_info(self, uid):
        rank_info = None
        if global_data.player.uid == uid:
            rank_info = (
             global_data.player.rank_use_title_type, global_data.player.rank_use_title_dict.get(global_data.player.rank_use_title_type, None))
        else:
            player_data = global_data.message_data.get_player_detail_inf(uid)
            player_data = player_data if player_data else {}
            title_type = rank_const.get_rank_use_title_type(player_data.get('rank_use_title_dict', {}))
            rank_info = rank_const.get_rank_use_title(player_data.get('rank_use_title_dict', {}))
        return (
         title_type, rank_info)

    def refresh_mecha_title(self, uid):
        info = self.lobby_mechas[uid]
        title_type, rank_info = self._get_rank_info(uid)
        if global_data.player.uid != uid:
            player_data = global_data.message_data.get_player_detail_inf(uid)
            if not player_data:
                global_data.player.request_players_detail_inf([uid])
        info['rank_info'] = rank_info
        template_utils.init_rank_title(info['widget'], title_type, rank_info)

    def refresh_mecha_titles(self, *argv):
        for uid, info in six.iteritems(self.lobby_mechas):
            title_type, rank_info = self._get_rank_info(uid)
            info['rank_info'] = rank_info
            template_utils.init_rank_title(info['widget'], title_type, rank_info)

    def _get_rank_widget_cache(self):
        count = len(self.lobby_mechas)
        if count < len(self.rank_widgets):
            pending_widget = None
            used_widget_list = [ info['widget'] for info in six_ex.items(self.lobby_mechas) ]
            for widget in self.rank_widgets:
                if widget not in used_widget_list:
                    return widget

        else:
            widget = global_data.uisystem.load_template_create('title/i_title_normal_2')
            self.panel.AddChild('rank_widget_{}'.format(count), widget)
            widget.setVisible(False)
            return widget
        return

    def update_interact_ui(self, *args):
        scene = global_data.game_mgr.scene
        if scene and scene.valid:
            cam = scene.active_camera
            for model_name, node_data in six_ex.items(self._node_data_dict):
                enabled = self._model_interactui_update_enabled[model_name]
                if not enabled:
                    continue
                ui_node = getattr(self, node_data.get('ui_node'))
                if not ui_node:
                    continue
                model = scene.get_model(model_name)
                if not model:
                    continue
                mpos = model.center_w
                model_offset = node_data.get('model_offset')
                mpos.y = mpos.y - model.bounding_box_w.y + model_offset
                x, y = cam.world_to_screen(mpos)
                distance = (cam.position - mpos).length
                touch_distance = node_data.get('touch_distance')
                ignore_dis_show = model_name == 'box_computer_5' and global_data.message_board_mgr.has_new
                if self._is_in_screen(x, y) and distance < touch_distance or ignore_dis_show:
                    x, y = self._to_screen_pos(x, y)
                    lpos = ui_node.getParent().convertToNodeSpace(cc.Vec2(x, y))
                    ui_node.setPosition(lpos)
                    if not ignore_dis_show:
                        scale = -0.002 * distance + 1.2
                        ui_node.setScale(scale)
                    ui_node.setVisible(True)
                else:
                    ui_node.setVisible(False)

            remove_uids = []
            for uid, info in six.iteritems(self.lobby_mechas):
                model = info['model']
                ui_node = info['widget']
                rank_info = info['rank_info']
                if not model or not model.valid:
                    remove_uids.append(uid)
                    continue
                if not rank_info:
                    ui_node.setVisible(False)
                    continue
                offset = info['offset']
                mpos = model.center_w
                mpos.y = mpos.y - model.bounding_box_w.y + offset
                x, y = cam.world_to_screen(mpos)
                distance = (cam.position - mpos).length
                if self._is_in_screen(x, y) and distance < LOBBY_MECHA_RANK_MAX_DISTANCE:
                    x, y = self._to_screen_pos(x, y)
                    lpos = ui_node.getParent().convertToNodeSpace(cc.Vec2(x, y))
                    ui_node.setPosition(lpos)
                    scale = -0.002 * distance + 1.2
                    ui_node.setScale(scale)
                    ui_node.setVisible(True)
                else:
                    ui_node.setVisible(False)

            for uid in remove_uids:
                del self.lobby_mechas[uid]

    def _is_in_screen(self, x, y):
        screen_width = global_data.ui_mgr.screen_size.width
        screen_height = global_data.ui_mgr.screen_size.height
        if x >= 0 and x <= screen_width and y >= 0 and y <= screen_height:
            return True
        return False

    def _to_screen_pos(self, x, y):
        return neox_pos_to_cocos(x, y)

    def on_finalize_panel(self):
        self.process_event(False)
        global_data.game_mgr.unregister_logic_timer(self.timer)
        self.timer = None
        return

    def refresh_message_board_new(self):
        has_new = global_data.message_board_mgr.has_new
        img_path = 'gui\\ui_res_2\\main\\icon_main_msg_3.png' if has_new else 'gui\\ui_res_2\\main\\icon_main_msg_2.png'
        nd = self.panel.nd_scene_ui3
        nd.icon_msg and nd.icon_msg.SetDisplayFrameByPath('', img_path)

    def on_visit_place_change(self):
        is_landlord = global_data.message_board_mgr.is_landlord()
        if not is_landlord:
            nd = self.panel.nd_scene_ui3
            nd.icon_msg and nd.icon_msg.SetDisplayFrameByPath('', 'gui\\ui_res_2\\main\\icon_main_msg_2.png')
        else:
            self.refresh_message_board_new()
        self.refresh_tv_new()

    def refresh_tv_new(self):
        if G_IS_NA_PROJECT:
            return
        icon = self.panel.nd_scene_ui1.icon_1
        if not icon:
            return
        if global_data.player and global_data.player.is_visit_others():
            icon.SetColor('#SW')
            return
        from logic.gutils.tv_panel_utils import get_tv_texture_path
        tex_path = get_tv_texture_path()
        from logic.gcommon.const import LOBBY_TV_TEXTURE_KEY
        local_cache_tex_path = global_data.achi_mgr.get_general_archive_data().get_field(LOBBY_TV_TEXTURE_KEY, '')
        has_new = tex_path != local_cache_tex_path
        if has_new:
            icon.SetColor('#SY')
        else:
            icon.SetColor('#SW')