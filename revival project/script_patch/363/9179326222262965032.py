# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/role_profile/VoiceWidget.py
from __future__ import absolute_import
import six
import six_ex
from common.uisys.BaseUIWidget import BaseUIWidget
from common.cfg import confmgr
from logic.gcommon.common_utils.local_text import get_text_by_id
import cc
from logic.gutils import item_utils

class VoiceWidget(BaseUIWidget):

    def __init__(self, parent, panel, *args, **kwargs):
        self.global_events = {'player_item_update_event': self.on_buy_good_success
           }
        super(VoiceWidget, self).__init__(parent, panel)
        self.role_id = 0
        self._ui_role_id = 0
        self.voice_config = {}
        self.all_voice_text = confmgr.get('game_voice_conf', 'VoiceText', 'Content')
        self.item_dict = {}
        self.role_id = 0
        self.playing_item = None
        self.selected_item = None
        self.own_items = set()

        @self.panel.btn_describe.callback()
        def OnClick(*args):
            from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
            dlg = GameRuleDescUI()
            dlg.set_show_rule(get_text_local_content(81253), get_text_local_content(81251))

        return

    def show_panel(self, flag):
        if self.panel:
            self.panel.setVisible(flag)
        if not flag:
            self.stop_voice()

    def on_parent_hide(self):
        self.stop_voice()

    def destroy(self):
        self.item_dict = {}
        self.panel.list_voice.DeleteAllSubItem()
        super(VoiceWidget, self).destroy()

    def set_role_id(self, role_id):
        self.role_id = role_id
        self.stop_voice()

    def refresh_all_content(self):
        if self._ui_role_id == self.role_id:
            return
        else:
            self._ui_role_id = self.role_id
            self.voice_config = confmgr.get('game_voice_conf', str(self.role_id), 'Content', default={})
            id_list = six_ex.keys(self.voice_config)
            id_list.sort(key=lambda x: self.voice_config[x].get('type_text_id', 0))
            self.item_dict = {}
            self.own_items = set()
            self.panel.list_voice.SetInitCount(len(id_list))
            has = global_data.player.has_item_by_no if global_data.player else (lambda : False)
            for i, item_no in enumerate(id_list):
                voice_item = self.panel.list_voice.GetItem(i)
                self.item_dict[item_no] = voice_item
                own = has(int(item_no))
                self.set_item_status(item_no, voice_item, own)
                voice_item.btn_choose.BindMethod('OnClick', lambda b, t, id=item_no: self.on_click_select(id))

            self.panel.lab_title.SetString('%s  %d/%d' % (get_text_by_id(81231), len(self.own_items), len(self.voice_config)))
            self.on_click_select(None, True)
            return

    def set_item_status(self, item_no, voice_item, own):
        voice_info = self.voice_config[item_no]
        voice_type_text = get_text_by_id(voice_info.get('type_text_id', 0))
        switch = voice_info.get('switch', '')
        voice_text_id = self.all_voice_text.get(switch, {}).get('text_id', 0)
        voice_text = get_text_by_id(voice_text_id)
        voice_item.lab_voice.SetString('[%s] %s' % (voice_type_text, voice_text))
        if own:
            voice_item.nd_cut.setOpacity(255)
            voice_item.nd_cut.SetEnableCascadeOpacityRecursion(True)
            voice_item.btn_play.setVisible(True)
            voice_item.btn_play.BindMethod('OnClick', lambda b, t, id=item_no: self.play_voice(id))
            self.own_items.add(item_no)
        else:
            voice_item.nd_cut.setOpacity(128)
            voice_item.btn_play.setVisible(False)
            voice_item.nd_cut.SetEnableCascadeOpacityRecursion(True)

    def on_click_select(self, item_id, force_update=False):
        if self.selected_item == item_id and not force_update:
            return
        for item_no, item in six.iteritems(self.item_dict):
            item.btn_choose.SetSelect(item_no == item_id)

        if item_id:
            btn = self.panel.temp_btn_go.btn_common
            if item_id in self.own_items:
                btn.SetText(get_text_by_id(80451))
                btn.SetEnable(False)
            else:
                self.panel.lab_get_method.SetString(item_utils.get_item_access(item_id))
                btn.SetText(2222)
                btn.SetEnable(True)
                btn.BindMethod('OnClick', lambda b, t, id=item_id: item_utils.jump_to_ui(id))
        self.panel.lab_get_method.setVisible(bool(item_id) and item_id not in self.own_items)
        self.panel.temp_btn_go.setVisible(bool(item_id))
        self.selected_item = item_id

    def play_voice(self, item_id):
        if item_id == self.playing_item:
            return
        self.stop_voice(False)
        global_data.emgr.play_human_voice_trial.emit(self.role_id, item_id, lambda : self.start_roll(item_id), lambda : self.stop_roll(item_id))

    def stop_voice(self, emit=True):
        if self.playing_item:
            if emit:
                global_data.emgr.stop_human_voice_trial.emit()
            self.stop_roll(self.playing_item)

    def start_roll(self, item_id):
        item = self.item_dict.get(item_id)
        if not item:
            return
        text_size = item.lab_voice.getTextContentSize().width
        delta = text_size - item.nd_cut.GetContentSize()[0]
        if delta > 0:
            cur_pos = item.lab_voice.GetPosition()
            target_pos = cc.Vec2(cur_pos[0] - delta, cur_pos[1])
            item.lab_voice.runAction(cc.MoveTo.create(delta / 100.0, target_pos))
        self.playing_item = item_id
        btn = item.btn_play
        btn.SetSelect(True)
        btn.BindMethod('OnClick', lambda *args: self.stop_voice())

    def stop_roll(self, item_id):
        if item_id != self.playing_item:
            return
        else:
            item = self.item_dict.get(item_id)
            if not item:
                return
            item.lab_voice.stopAllActions()
            item.ResizeAndPosition(False)
            self.playing_item = None
            btn = item.btn_play
            btn.SetSelect(False)
            btn.BindMethod('OnClick', lambda b, t, id=item_id: self.play_voice(id))
            return

    def on_buy_good_success(self):
        has = global_data.player.has_item_by_no if global_data.player else (lambda : False)
        for item_no, voice_item in six.iteritems(self.item_dict):
            if has(int(item_no)) and item_no not in self.own_items:
                self.set_item_status(item_no, voice_item, True)

        self.panel.lab_title.SetString('%s  %d/%d' % (get_text_by_id(81231), len(self.own_items), len(self.voice_config)))
        self.on_click_select(self.selected_item, True)