# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEBlessUpgradeWidget.py
from __future__ import absolute_import
from common.cfg import confmgr
from logic.gutils.pve_utils import get_effect_desc_text, get_bless_elem_desc, get_bless_elem_attr_conf, get_bless_elem_res, DEFAULT_BLESS_PANEL

class PVEBlessUpgradeWidget(object):
    TEMPLATE = 'pve/energy/pve_energy_upgrade'

    def __init__(self, panel):
        self.panel = panel
        self.init_params()
        self.init_widget()
        self.init_ui_nds()
        self.process_events(True)

    def init_params(self):
        self.random_tag = False

    def init_widget(self):
        self.widget = global_data.uisystem.load_template_create(self.TEMPLATE, self.panel)
        self.widget.setVisible(False)

    def init_ui_nds(self):
        if not self.widget:
            return

        @self.widget.nd_content.unique_callback()
        def OnClick(*args):
            if self.widget.IsPlayingAnimation('appear') or self.widget.IsPlayingAnimation('disappear'):
                return
            self.widget.PlayAnimation('disappear')
            self.random_tag = False

    def process_events(self, is_bind):
        econf = {'pve_update_bless_event': self.update_bless,
           'pve_random_choose_bless': self.random_choose_bless
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

    def random_choose_bless(self, bless_id):
        self.random_tag = True

    def update_bless(self, bless_id):
        if not self.random_tag:
            return
        else:
            bless_conf = confmgr.get('bless_data', str(bless_id), default=None)
            if not bless_conf:
                return
            ori_nd = self.widget.temp_item_0
            cur_nd = self.widget.temp_item_1
            ui_items = (
             ori_nd, cur_nd)
            cur_level = global_data.cam_lplayer.ev_g_bless_level(bless_id) - 1
            ori_level = cur_level - 1
            for idx, ui_item in enumerate(ui_items):
                level = ori_level if idx == 0 else cur_level
                ui_item.lab_name.SetString(bless_conf['name_id'])
                ui_item.img_item.SetDisplayFrameByPath('', bless_conf.get('icon', ''))
                desc_id = bless_conf['desc_id']
                attr_conf = bless_conf.get('attr_text_conf', [])
                ui_item.lab_introduce.SetString(get_effect_desc_text(desc_id, attr_conf, level + 1))
                max_level = bless_conf.get('max_level', 1)
                if max_level == 1:
                    ui_item.list_dot.setVisible(False)
                else:
                    ui_item.list_dot.setVisible(True)
                    ui_item.list_dot.DeleteAllSubItem()
                    ui_item.list_dot.SetInitCount(max_level)
                    for i, btn in enumerate(ui_item.list_dot.GetAllItem()):
                        if i <= level:
                            btn.btn_dot.SetEnable(True)
                            btn.btn_dot.SetSelect(True)
                        else:
                            btn.btn_dot.SetEnable(True)
                            btn.btn_dot.SetSelect(False)

                elem_id = bless_conf.get('elem_id', None)
                if elem_id:
                    ui_item.bar_describe.setVisible(True)
                    elem_desc_id = get_bless_elem_desc(elem_id)
                    elem_attr_conf = get_bless_elem_attr_conf(elem_id)
                    ui_item.bar_describe.lab_describe.SetString(get_effect_desc_text(elem_desc_id, elem_attr_conf, 1))
                    elem_icon, elem_pnl_icon = get_bless_elem_res(elem_id, ['icon', 'panel'])
                    ui_item.icon_type.SetDisplayFrameByPath('', elem_icon)
                    ui_item.bar.SetFrames('', [elem_pnl_icon, elem_pnl_icon, elem_pnl_icon])
                    ui_item.icon_type.setVisible(True)
                else:
                    ui_item.bar_describe.setVisible(False)
                    ui_item.icon_type.setVisible(False)
                    pic = DEFAULT_BLESS_PANEL
                    ui_item.bar.SetFrames('', [pic, pic, pic])

            self.play_show_anim()
            return

    def play_show_anim(self):
        self.widget.PlayAnimation('appear')