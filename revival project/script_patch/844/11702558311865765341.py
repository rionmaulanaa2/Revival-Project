# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/TeammateWidget/LobbyChatHeadUI.py
from __future__ import absolute_import
import world
from logic.gcommon.common_const import scene_const
from logic.gcommon.common_utils.local_text import get_server_text

class LobbyChatHeadUI(object):
    UI_DICT = {}

    @classmethod
    def cls_show_chat_msg(cls, unit_obj, msg):
        model = unit_obj.ev_g_model()
        if not model:
            return
        if model.get_scene() != world.get_active_scene():
            return
        ui = cls.get_ui(unit_obj, True)
        ui.add_chat_message(msg)
        ui.update_follow_model(unit_obj)

    @classmethod
    def cls_hide_chat_msg(cls, unit_obj):
        ui = cls.get_ui(unit_obj, False)
        if ui:
            ui.hide_chat_message()

    @classmethod
    def get_ui(cls, unit_obj, create_if_not_exist):
        uid = unit_obj.id
        ui = cls.UI_DICT.get(uid, None)
        if not ui and create_if_not_exist:
            ui = LobbyChatHeadUI(unit_obj)
            cls.UI_DICT[uid] = ui
        return ui

    @classmethod
    def destroy_ui(cls, unit_obj):
        uid = unit_obj.id
        if uid in cls.UI_DICT:
            ui = cls.UI_DICT[uid]
            if ui:
                ui.destroy()
            del cls.UI_DICT[uid]

    def __init__(self, unit_obj):
        self._chat_ui_nd = global_data.uisystem.load_template_create('lobby/lobby_chat_pop')
        self._chat_ui_nd.lab.setVisible(False)
        self._chat_ui_nd.btn_speak.setVisible(False)
        self._space_node = None
        self._scale = 1
        self.process_event()
        self.init_panel(unit_obj)
        return

    def process_event(self, is_init=True):
        event_info_list = [
         (
          global_data.emgr.lobby_ui_visible, self.on_lobby_ui_visible_update),
         (
          global_data.emgr.chat_voice_empty, self.on_voice_empty)]
        for info in event_info_list:
            ev_hook, handle = info
            if is_init:
                ev_hook += handle
            else:
                ev_hook -= handle

    def init_panel(self, unit_obj):
        from common.uisys.uielment.CCUISpaceNode import CCUISpaceNode
        space_node = CCUISpaceNode.Create()
        space_node.setLocalZOrder(1)
        space_node.AddChild('', self._chat_ui_nd)
        if unit_obj.ev_g_is_avatar():
            self._chat_ui_nd.setPosition(0, -50)
        else:
            self._chat_ui_nd.setPosition(0, 11)

        def vis_callback(last_need_draw, cur_need_draw):
            cnt_scene = global_data.game_mgr.scene
            if not cnt_scene:
                return
            if self._chat_ui_nd and self._chat_ui_nd.isValid() and cnt_scene.scene_type == scene_const.SCENE_LOBBY:
                is_visible = True if cur_need_draw else False
                self._chat_ui_nd.setVisible(is_visible)
            else:
                self._chat_ui_nd.setVisible(False)

        space_node.set_visible_callback(vis_callback)
        self._space_node = space_node
        self.update_follow_model(unit_obj)

    def update_follow_model(self, unit_obj):
        model = unit_obj.ev_g_model()
        space_node = self._space_node
        if model and space_node:
            xuetiao_pos = model.get_socket_matrix('team_info', world.SPACE_TYPE_WORLD)
            if xuetiao_pos:
                space_node.set_assigned_world_pos(xuetiao_pos.translation)
                space_node.bind_model(model, 'team_info')
            else:
                self.hide()

    def add_chat_message(self, data):
        if 'notify_type' in data.get('sender_info', {}):
            return
        else:
            if data.get('voice', None):
                self._chat_ui_nd.btn_speak.setVisible(True)
                self._chat_ui_nd.lab.setVisible(False)
                self._chat_ui_nd.stopAllActions()
            else:
                chat_text = get_server_text(data['msg'])
                self._chat_ui_nd.btn_speak.setVisible(False)
                self._chat_ui_nd.lab.setVisible(True)

                def time_cb():
                    self._chat_ui_nd.lab.setVisible(False)

                self._chat_ui_nd.PlayAnimation('show_lab')
                self._chat_ui_nd.lab.SetStringWithAutoFitAdapt(chat_text, min_size=(150,
                                                                                    32))
                self._chat_ui_nd.stopAllActions()
                self._chat_ui_nd.SetTimeOut(5, time_cb)
            return

    def hide_chat_message(self):
        if self._chat_ui_nd:
            self._chat_ui_nd.lab.setVisible(False)
            self._chat_ui_nd.btn_speak.setVisible(False)
            self._chat_ui_nd.stopAllActions()

    def on_lobby_ui_visible_update(self, is_visible):
        if is_visible:
            self.show()
        else:
            self.hide()

    def on_voice_empty(self, *args):
        self._chat_ui_nd.btn_speak.setVisible(False)

    def destroy(self):
        if self._space_node:
            self._space_node.Destroy()
        self._space_node = None
        self._chat_ui_nd = None
        self.process_event(False)
        return

    def hide(self):
        self.toggle_visible(False)

    def show(self):
        self.toggle_visible(True)

    def toggle_visible(self, visible):
        if self._space_node:
            self._space_node.setVisible(visible)
        if self._chat_ui_nd:
            self._chat_ui_nd.setVisible(visible)