# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/control_ui/BagMechaModuleWidget.py
from __future__ import absolute_import
from six.moves import range
from logic.gcommon.common_const import mecha_const
from logic.gutils.mecha_module_utils import get_module_item_bar_pic
from logic.gutils import template_utils

class BagMechaModuleWidget(object):

    def __init__(self, panel, nd_module, click_method, drag_method, end_method):
        self._panel = panel
        self._nd_module = nd_module
        self._on_click_module = click_method
        self._on_drag_module = drag_method
        self._on_end_module = end_method
        self.init_widget()
        self.process_event(True)

    def init_widget(self):
        if not global_data.cam_lplayer:
            return None
        else:
            cur_module_config = global_data.cam_lplayer.ev_g_mecha_all_installed_module()
            max_module_num = mecha_const.MODULE_MAX_SLOT_COUNT
            for slot_no in range(1, max_module_num + 1):
                card_id, module_id = cur_module_config.get(slot_no, (None, None))
                _, card_lv = global_data.cam_lplayer.ev_g_module_item_slot_lv(module_id)
                ui_item = getattr(self._nd_module, 'module_{}'.format(slot_no))
                self.init_module_item(ui_item, slot_no, card_lv, card_id, module_id)

            return None

    def init_module_item(self, ui_item, slot_no, card_lv, card_id, module_id):
        module_icon_path = get_module_item_bar_pic(slot_no, card_lv, 'big_')
        card_icon_path = template_utils.get_module_show_slot_pic(slot_no, card_id, card_lv)
        ui_item.module_bar.SetDisplayFrameByPath('', module_icon_path)
        ui_item.module_bar_vx.SetDisplayFrameByPath('', module_icon_path)
        ui_item.icon_skill.SetDisplayFrameByPath('', card_icon_path)
        if slot_no and slot_no == mecha_const.SP_MODULE_SLOT:
            if module_id and module_id in mecha_const.SP_MODULE_NO_CHOOSE_ITEM_IDS:
                card_index = mecha_const.SP_MODULE_NO_CHOOSE_ITEM_IDS.index(module_id)
                ui_item.img_sp_num.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/mech_module/icon_module_sp_%d.png' % (card_index + 1))
                ui_item.img_sp_num.setVisible(True)
            else:
                ui_item.img_sp_num.setVisible(False)

        @ui_item.unique_callback()
        def OnClick(layer, touch):
            if not self._on_click_module:
                return
            self._on_click_module(layer, touch, module_id, card_id, card_lv, slot_no)

        @ui_item.unique_callback()
        def OnDrag(layer, touch):
            if not self._on_drag_module:
                return
            self._on_drag_module(layer, touch, module_id, slot_no)

        @ui_item.unique_callback()
        def OnEnd(layer, touch):
            if not self._on_end_module:
                return
            self._on_end_module(layer, touch, module_id, slot_no)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'observer_module_changed_event': self.init_widget,
           'on_player_rechoose_mecha_event': self.init_widget
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def destroy(self):
        self._panel = None
        self._nd_module = None
        self.process_event(False)
        return