# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/control_ui/SceneInteractionUIPC.py
from __future__ import absolute_import
import six
import six_ex
from .SceneInteractionUI import SceneInteractionBaseUI
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.hot_key_utils import set_hot_key_common_tip_multiple_version
from data.hot_key_def import SWITCH_PC_MODE
from common.cfg import confmgr
from logic.comsys.control_ui.PcKeyHintWidget import HINT_TEXT_FUNC_DICT

class SceneInteractionUIPC(SceneInteractionBaseUI):
    PANEL_CONFIG_NAME = 'battle/fight_temporary_pc'
    GLOBAL_EVENT = dict(SceneInteractionBaseUI.GLOBAL_EVENT)
    GLOBAL_EVENT.update({'hot_key_conf_refresh_event': '_on_refresh_hot_key'
       })
    GLOBAL_EVENT.update()

    def on_init_panel(self):
        super(SceneInteractionUIPC, self).on_init_panel()
        self.hide_all_btns()
        self.refresh_tilde_key_hint()

    def leave_screen(self):
        super(SceneInteractionUIPC, self).leave_screen()
        global_data.ui_mgr.close_ui('SceneInteractionUIPC')

    def on_switch_on_hot_key(self):
        super(SceneInteractionUIPC, self).on_switch_on_hot_key()
        self.panel.list_pc_2.setVisible(False)
        if self.pc_key_hint_widget:
            self.pc_key_hint_widget.update_cur_status()
            self.pc_key_hint_widget.refresh_list()

    def on_switch_off_hot_key(self):
        super(SceneInteractionUIPC, self).on_switch_off_hot_key()
        self.panel.list_pc_2.setVisible(True)

    def refresh_tilde_key_hint(self):
        hint_conf = confmgr.get('hint_custom_show')
        if not hint_conf:
            return
        else:
            resident_hint_set = []
            hint_items = sorted(six_ex.values(hint_conf), key=lambda v: v.get('cSortID'))
            mode_type = global_data.game_mode.get_mode_type()
            for cur_hint in hint_items:
                cResidentModeList = cur_hint.get('cResidentModeList', [])
                if not cResidentModeList:
                    continue
                elif isinstance(cResidentModeList, six.string_types) and cResidentModeList == 'all':
                    pass
                elif isinstance(cResidentModeList, list) and mode_type in cResidentModeList:
                    pass
                else:
                    continue
                hint_text_or_func = cur_hint.get('cHintDesc') or cur_hint.get('cHintDescFunc')
                resident_hint_set.append((hint_text_or_func, cur_hint.get('cHotKeyFuncCodeList', [])))

            if not resident_hint_set:
                return
            self.panel.list_pc_2.DeleteAllSubItem()
            self.panel.list_pc_2.SetInitCount(len(resident_hint_set))
            for idx, hint in enumerate(resident_hint_set):
                desc_text_id_or_func = hint[0]
                shortcuts = hint[1]
                node = self.list_pc_2.GetItem(idx)
                if type(desc_text_id_or_func) == int:
                    node.lab_desc.SetString(get_text_by_id(desc_text_id_or_func))
                else:
                    func = HINT_TEXT_FUNC_DICT.get(desc_text_id_or_func, None)
                    if func:
                        node.lab_desc.SetString(func())
                set_hot_key_common_tip_multiple_version(node.nd_key_pc, shortcuts, force_set=True)
                node.lab_desc.ResizeAndPositionSelf()

            return

    def _on_refresh_hot_key(self):
        self.refresh_tilde_key_hint()

    def set_common_button_frame(self, btn_path):
        pass