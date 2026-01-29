# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/setting_ui/SensitySettingUI.py
from __future__ import absolute_import
from six.moves import range
from common.uisys.basepanel import BasePanel
from logic.gcommon.common_const import ui_operation_const as uoc
from common.const.uiconst import TOP_ZORDER
from logic.gcommon.common_utils.local_text import get_text_by_id

class SensitySettingUI(BasePanel):
    PANEL_CONFIG_NAME = 'test/sensity_setting'
    DLG_ZORDER = TOP_ZORDER

    def on_init_panel(self):
        self.init_event()

    def init_event(self):
        frocker_setting = {'key': uoc.SST_FROCKER_KEY,'sliders': [
                     'sl_base', 'sl_up', 'sl_down', 'sl_left', 'sl_right'],
           'texts': [
                   get_text_by_id(2152), get_text_by_id(2153), get_text_by_id(2154), get_text_by_id(2155), get_text_by_id(2156)],
           'event': 'sst_frock_changed_event',
           'title': get_text_by_id(2159)
           }
        scr_setting = {'key': uoc.SST_SCR_KEY,'sliders': [
                     'sl_base', 'sl_up', 'sl_down', 'sl_left', 'sl_right'],
           'texts': [
                   get_text_by_id(2152), get_text_by_id(2153), get_text_by_id(2154), get_text_by_id(2157), get_text_by_id(2158)],
           'event': 'sst_scr_changed_event',
           'title': get_text_by_id(2160)
           }
        aim_scr_setting = {'key': uoc.SST_FS_ROCKER_KEY,'sliders': [
                     'sl_base', 'sl_up', 'sl_down', 'sl_left', 'sl_right'],
           'texts': [
                   get_text_by_id(2152), get_text_by_id(2153), get_text_by_id(2154), get_text_by_id(2155), get_text_by_id(2156)],
           'event': 'sst_free_sight_changed_event',
           'title': get_text_by_id(2161)
           }
        aim_rd_setting = {'key': uoc.SST_AIM_RD_KEY,'sliders': [
                     'sl_base', 'sl_up', 'sl_down', 'sl_left', 'sl_right'],
           'texts': [
                   get_text_by_id(2152), get_text_by_id(2153), get_text_by_id(2154), get_text_by_id(2155), get_text_by_id(2156)],
           'event': 'sst_aim_rd_changed_event',
           'title': get_text_by_id(2162)
           }
        aim_2m_setting = {'key': uoc.SST_AIM_2M_KEY,'sliders': [
                     'sl_base', 'sl_up', 'sl_down', 'sl_left', 'sl_right'],
           'texts': [
                   get_text_by_id(2152), get_text_by_id(2153), get_text_by_id(2154), get_text_by_id(2155), get_text_by_id(2156)],
           'event': 'sst_aim_2m_changed_event',
           'title': get_text_by_id(2163)
           }
        aim_4m_setting = {'key': uoc.SST_AIM_4M_KEY,'sliders': [
                     'sl_base', 'sl_up', 'sl_down', 'sl_left', 'sl_right'],
           'texts': [
                   get_text_by_id(2152), get_text_by_id(2153), get_text_by_id(2154), get_text_by_id(2155), get_text_by_id(2156)],
           'event': 'sst_aim_4m_changed_event',
           'title': get_text_by_id(2164)
           }
        sliders_list = [
         frocker_setting, scr_setting, aim_scr_setting, aim_rd_setting, aim_2m_setting, aim_4m_setting]
        self.panel.lv_sensity_setting.SetInitCount(len(sliders_list))
        all_items = self.panel.lv_sensity_setting.GetAllItem()
        for idx, ui_item in enumerate(all_items):
            ui_setting = sliders_list[idx]
            self._bind_sliders(ui_item, ui_setting)

    def _bind_sliders(self, node, ui_setting):
        import world
        scn = world.get_active_scene()
        player = scn.get_player()
        if not player:
            return
        else:
            key = ui_setting['key']
            val_list = player.get_owner().get_setting(key)
            slider_names = ui_setting['sliders']
            slider_texts = ui_setting['texts']
            event_name = ui_setting['event']
            title = ui_setting['title']
            node.tf_label.SetString(title)
            for idx in range(0, len(val_list)):
                node_name = slider_names[idx]
                node_text = slider_texts[idx]
                cur_val = val_list[idx]
                slider_ccb = getattr(node, node_name, None)
                if not slider_ccb:
                    continue
                slider_ccb.tf_name.SetString(node_text)
                slider_ccb.tf_value.SetString(str(cur_val))
                min_val, max_val = uoc.SST_RANGE
                percent = self._cal_percent(cur_val, uoc.SST_RANGE)
                slider_ccb.slider.setPercent(percent * 100)

                @slider_ccb.slider.callback()
                def OnPercentageChanged(ctrl, sl, idx=idx, slider_ccb=slider_ccb, val_list=val_list):
                    val = sl.getPercent() / 100.0 * (max_val - min_val) + min_val
                    slider_ccb.tf_value.SetString(str(val))
                    if idx < len(val_list):
                        val_list[idx] = val
                        global_data.emgr.fireEvent(event_name, val_list)

            return

    def _cal_percent(self, val, range):
        return (val - range[0]) / (range[1] - range[0])