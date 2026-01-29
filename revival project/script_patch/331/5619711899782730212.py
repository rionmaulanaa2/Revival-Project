# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/control_ui/PcKeyHintWidget.py
from __future__ import absolute_import
import six_ex
from data import hot_key_def
from logic.gutils.hot_key_utils import set_hot_key_common_tip_multiple_version
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.cfg import confmgr
from logic.gutils.newbie_stage_utils import is_in_newbie_local_battle
from logic.gutils import hotkey_hint_check_handler
status_none = 0
status_human = 1
status_mecha = 2
status_mecha_trans = 3

def get_run_hint_text():
    is_run = global_data.moveKeyboardMgr.get_run_switch_state()
    if is_run:
        return 17990
    return 17991


HINT_TEXT_FUNC_DICT = {'get_run_hint_text': get_run_hint_text
   }

class PcKeyHintWidget(object):

    def __init__(self, root_list_node):
        self.root_list_node = root_list_node
        self.root_list_node.EnableItemAutoPool(True)
        self.root_list_node.setVisible(True)
        self._cur_status = status_none
        self.unit = None
        self.hints = {}
        self.init_hint_list()
        if global_data.player and global_data.player.logic:
            self.unit = global_data.player.logic
            self.bind_ui_event(self.unit, True)
        self.process_event(True)
        self.update_cur_status()
        self.refresh_list()
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'scene_player_setted_event': self._scene_player_setted,
           'hot_key_conf_refresh_event': self._on_refresh_hot_key,
           'run_switch_state_changed_event': self._on_run_switch_state_changed
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def _scene_player_setted(self, unit):
        if unit is None:
            return
        else:
            if global_data.player and global_data.player.logic and unit and global_data.player.logic.id == unit.id:
                if self.unit is not None:
                    self.bind_ui_event(self.unit, False)
                self.unit = unit
                self.bind_ui_event(self.unit, True)
                self.update_cur_status()
                self.refresh_list()
            return

    def _on_refresh_hot_key(self):
        self.update_cur_status()
        self.refresh_list()

    def _on_run_switch_state_changed(self, new_val):
        self.refresh_list()

    def show(self):
        if not self.root_list_node or not self.root_list_node.isValid():
            return
        self.root_list_node.setVisible(True)

    def hide(self):
        if not self.root_list_node or not self.root_list_node.isValid():
            return
        self.root_list_node.setVisible(False)

    def destroy(self):
        self.root_list_node = None
        self.process_event(False)
        if self.unit is not None:
            self.bind_ui_event(self.unit, False)
        return

    def update_cur_status(self):
        self._cur_status = status_none
        if self.unit is not None:
            if self.unit.ev_g_in_mecha_only():
                self._cur_status = status_mecha
            elif self.unit.ev_g_in_mecha_trans_only():
                self._cur_status = status_mecha_trans
            else:
                self._cur_status = status_human
        return

    def refresh_list(self):
        cur_hints = self._get_hint_list(self._cur_status)
        self.root_list_node.DeleteAllSubItem()
        self.root_list_node.SetInitCount(len(cur_hints))
        for idx, hint in enumerate(cur_hints):
            desc_text_id_or_func = hint[0]
            shortcuts = hint[1]
            node = self.root_list_node.GetItem(idx)
            self.refresh_hint_ui_item(node, desc_text_id_or_func, shortcuts)

    @staticmethod
    def refresh_hint_ui_item(node, desc_text_id_or_func, shortcuts):
        if type(desc_text_id_or_func) == int:
            node.lab_desc.SetString(get_text_by_id(desc_text_id_or_func))
        else:
            func = HINT_TEXT_FUNC_DICT.get(desc_text_id_or_func, None)
            if func:
                node.lab_desc.SetString(func())
        set_hot_key_common_tip_multiple_version(node.nd_key_pc, shortcuts)
        node.lab_desc.ResizeAndPositionSelf()
        return

    def _get_hint_list(self, status):
        return self.hints.get(status, ())

    def init_hint_list(self):
        if is_in_newbie_local_battle():
            hint_conf = confmgr.get('newbie_hint_custom_show')
        else:
            hint_conf = confmgr.get('hint_custom_show')
        if not hint_conf:
            return
        hint_items = sorted(six_ex.values(hint_conf), key=lambda v: v.get('cSortID'))
        human_hint_set = []
        mecha_hint_set = []
        mecha_trans_hint_set = []
        mode_type = global_data.game_mode.get_mode_type()
        for cur_hint in hint_items:
            cShowModeList = cur_hint.get('cShowModeList', [])
            if not cShowModeList:
                if mode_type in cur_hint.get('cNotShowModeList', []):
                    continue
            elif mode_type not in cShowModeList:
                continue
            check_handler_name = cur_hint.get('cCustomCheck')
            if check_handler_name:
                check_handler = getattr(hotkey_hint_check_handler, check_handler_name)
                if check_handler and callable(check_handler):
                    if not check_handler():
                        continue
            hint_text_or_func = cur_hint.get('cHintDesc') or cur_hint.get('cHintDescFunc')
            if cur_hint.get('cIsHumanShow', 0) != 0:
                human_hint_set.append((hint_text_or_func, cur_hint.get('cHotKeyFuncCodeList', [])))
            if cur_hint.get('cIsMechaShow', 0) != 0:
                mecha_hint_set.append((hint_text_or_func, cur_hint.get('cHotKeyFuncCodeList', [])))
            if cur_hint.get('cIsMechaTransShow', 0) != 0:
                mecha_trans_hint_set.append((hint_text_or_func, cur_hint.get('cHotKeyFuncCodeList', [])))

        self.hints = {status_human: human_hint_set,status_mecha: mecha_hint_set,
           status_mecha_trans: mecha_trans_hint_set
           }

    def bind_ui_event(self, target, bind):
        if target and target.is_valid():
            if bind:
                func = target.regist_event
            else:
                func = target.unregist_event
            func('E_ON_CONTROL_TARGET_CHANGE', self._on_ct_changed)

    def _on_ct_changed(self, *args, **kwargs):
        self.update_cur_status()
        self.refresh_list()