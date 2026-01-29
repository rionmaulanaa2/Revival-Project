# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/control_ui/BagPVEBlessWidget.py
from __future__ import absolute_import
import six
from six.moves import range
from common.cfg import confmgr
from logic.gcommon.common_const.pve_const import BLESS_TRIGGER_TYPE_MAIN_WP, BLESS_TRIGGER_TYPE_SEC_WP, BLESS_TRIGGER_TYPE_SKILL, BLESS_TRIGGER_TYPE_HIT
from logic.gcommon.common_const import mecha_const
from logic.gutils import template_utils

class BagPVEBlessWidget(object):

    def __init__(self, panel, click_method):
        self._panel = panel
        self._on_click_bless = click_method
        self.init_widget()
        self.process_event(True)

    def init_widget(self):
        if not global_data.cam_lplayer:
            return None
        else:
            bless_conf = confmgr.get('bless_data')
            skill_bless = global_data.cam_lplayer.ev_g_skill_bless()
            cur_skill_bless = {}
            for bless_id, level in six.iteritems(skill_bless):
                cur_skill_bless[bless_conf[str(bless_id)]['trigger_type']] = (
                 bless_id, level)

            for bless_no in range(1, 5):
                bless_id, level = cur_skill_bless.get(bless_no, (None, None))
                ui_item = self._panel.nd_skill.list_item_skill.GetItem(bless_no - 1)
                if bless_id:
                    ui_item.btn_frame.SetEnable(True)
                    ui_item.nd_cut.setVisible(True)
                    icon = bless_conf[str(bless_id)]['icon']
                    ui_item.img_item.SetDisplayFrameByPath('', icon)
                    ui_item.lab_level.SetString(get_text_by_id(80100) + str(level))
                    item_data = {'is_bless': True,
                       'bless_id': bless_id,
                       'level': level,
                       'name_text': bless_conf[str(bless_id)]['name_id'],
                       'desc_text': bless_conf[str(bless_id)]['desc_id'],
                       'icon': icon
                       }

                    @ui_item.btn_frame.unique_callback()
                    def OnClick(layer, touch, idata=item_data):
                        if not self._on_click_bless or not idata:
                            return
                        self._on_click_bless(layer, touch, idata)

                else:
                    ui_item.btn_frame.SetEnable(False)
                    ui_item.nd_cut.setVisible(False)

            cur_addition_bless = {}
            cur_addition_bless.update(global_data.cam_lplayer.ev_g_addition_blesses() or {})
            cur_addition_bless.update(global_data.cam_lplayer.ev_g_common_blesses() or {})
            self._panel.list_item_blessing.setVisible(bool(cur_addition_bless))
            self._panel.empty_blessing.setVisible(not bool(cur_addition_bless))
            if cur_addition_bless:
                self._panel.list_item_blessing.SetInitCount(len(cur_addition_bless))
                for idx, (bless_id, level) in enumerate(six.iteritems(cur_addition_bless)):
                    ui_item = self._panel.list_item_blessing.GetItem(idx)
                    ui_item.btn_frame.SetEnable(True)
                    ui_item.nd_cut.setVisible(True)
                    ui_item.img_item.SetDisplayFrameByPath('', bless_conf[str(bless_id)]['icon'])
                    ui_item.lab_level.SetString(get_text_by_id(80100) + str(level))
                    item_data = {'is_bless': True,
                       'bless_id': bless_id,
                       'level': level,
                       'name_text': bless_conf[str(bless_id)]['name_id'],
                       'desc_text': bless_conf[str(bless_id)]['desc_id']
                       }

                    @ui_item.btn_frame.unique_callback()
                    def OnClick(layer, touch, idata=item_data):
                        if not self._on_click_bless or not idata:
                            return
                        self._on_click_bless(layer, touch, idata)

            return None

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'observer_bless_changed_event': self.init_widget
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def destroy(self):
        self._panel = None
        self._nd_bless = None
        self.process_event(False)
        return