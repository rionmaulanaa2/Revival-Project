# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEBreakUpgradeWidget.py
from __future__ import absolute_import
from common.cfg import confmgr
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.pve_utils import get_effect_desc_text

class PVEBreakUpgradeWidget(object):
    TEMPLATE = 'pve/breakthrough/pve_breakthrough_upgrade'

    def __init__(self, panel):
        self.panel = panel
        self.init_params()
        self.init_conf()
        self.init_widget()
        self.init_ui_nds()
        self.process_events(True)

    def init_params(self):
        self.random_tag = False
        self.mecha_id = None
        self.mecha_item_id = None
        self.skin_id = None
        return

    def init_conf(self):
        self.mecha_id = global_data.player.get_pve_select_mecha_id()
        self.mecha_item_id = global_data.player.get_pve_selected_mecha_item_id()
        self.skin_id = global_data.player.get_mecha_fashion(self.mecha_item_id)
        self.break_conf = confmgr.get('mecha_breakthrough_data', str(self.mecha_id), default=None)
        return

    def init_widget(self):
        self.widget = global_data.uisystem.load_template_create(self.TEMPLATE, self.panel)
        self.widget.setVisible(False)

    def init_ui_nds(self):
        if not self.widget:
            return

        @self.widget.nd_content.unique_callback()
        def OnClick(*args):
            self.widget.PlayAnimation('disappear')
            self.random_tag = False

    def process_events(self, is_bind):
        econf = {'pve_update_break_event': self.update_break
           }
        global_data.emgr.bind_events(econf) if is_bind else global_data.emgr.unbind_events(econf)

    def clear(self):
        self.widget and self.widget.Destroy()
        self.widget = None
        return

    def destroy(self):
        self.clear()
        self.init_params()
        self.process_events(False)
        self.panel = None
        return

    def random_choose_break(self):
        self.random_tag = True

    def update_break(self, state_dict):
        if not self.random_tag:
            return
        if state_dict:
            slot = list(state_dict.keys())[0]
            cur_level = state_dict[slot]
            ori_level = cur_level - 1
            ori_nd = self.widget.temp_item_0
            cur_nd = self.widget.temp_item_1
            conf = self.break_conf.get(str(slot), {})
            ori_conf = conf.get(str(ori_level), {})
            cur_conf = conf.get(str(cur_level), {})
            name_text = get_text_by_id(ori_conf['name_id'])
            desc_text = get_effect_desc_text(ori_conf['desc_id'], ori_conf.get('attr_text_conf', []))
            type_text = get_text_by_id(ori_conf['type_text_id'])
            ori_nd.lab_name.SetString(name_text)
            ori_nd.lab_describe.SetString(desc_text)
            ori_nd.lab_type.SetString(type_text)
            ori_nd.list_dot.DeleteAllSubItem()
            ori_nd.list_dot.SetInitCount(len(conf))
            for i, btn in enumerate(ori_nd.list_dot.GetAllItem()):
                if i + 1 <= ori_level:
                    btn.btn_dot.SetEnable(True)
                    btn.btn_dot.SetSelect(True)
                else:
                    btn.btn_dot.SetEnable(True)
                    btn.btn_dot.SetSelect(False)

            ori_nd.img_item.SetDisplayFrameByPath('', ori_conf['icon'])
            name_text = get_text_by_id(cur_conf['name_id'])
            desc_text = get_effect_desc_text(cur_conf['desc_id'], cur_conf.get('attr_text_conf', []))
            type_text = get_text_by_id(cur_conf['type_text_id'])
            cur_nd.lab_name.SetString(name_text)
            cur_nd.lab_describe.SetString(desc_text)
            cur_nd.lab_type.SetString(type_text)
            cur_nd.list_dot.DeleteAllSubItem()
            cur_nd.list_dot.SetInitCount(len(conf))
            for i, btn in enumerate(cur_nd.list_dot.GetAllItem()):
                if i + 1 <= cur_level:
                    btn.btn_dot.SetEnable(True)
                    btn.btn_dot.SetSelect(True)
                else:
                    btn.btn_dot.SetEnable(True)
                    btn.btn_dot.SetSelect(False)

            cur_nd.img_item.SetDisplayFrameByPath('', cur_conf['icon'])
            self.play_show_anim()

    def play_show_anim(self):
        self.widget.PlayAnimation('appear')