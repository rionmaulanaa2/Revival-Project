# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/exercise_ui/ExerciseEquipmentUI.py
from __future__ import absolute_import
from six.moves import range
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_2, BASE_LAYER_ZORDER
from logic.comsys.common_ui.WidgetCommonComponent import WidgetCommonComponent
from common.const import uiconst
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.cfg import confmgr

class ExerciseEquipmentUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_train/fight_change_main'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {}
    HOT_KEY_FUNC_MAP = {'exercise_weapon_config_close': '_on_click_close_PC',
       'cancel_action': '_on_click_close_PC'
       }
    LEFT_TAB = ('weapon', 'item', 'armor')

    def on_init_panel(self, *args, **kwargs):
        super(ExerciseEquipmentUI, self).on_init_panel()
        self.hide_main_ui()
        self.panel.temp_bg.PlayAnimation('in')
        global_data.display_agent.set_longtime_post_process_active('gaussian_blur', True)
        self.widgets_helper = None
        self.process_events(True)
        self.init_widget()
        self.init_ui_events()
        self.cur_index = 0
        select_tab_idx = global_data.emgr.exercise_get_eq_tab.emit()[0]
        if select_tab_idx:
            self.widgets_helper.on_switch_to_widget(select_tab_idx)
        else:
            self.widgets_helper.on_switch_to_widget(0)
        return

    def init_params(self):
        self.weapon_widget = None
        self.item_widget = None
        self.armor_widget = None
        self.list_tab = []
        self.tag_btn_dict = {}
        return

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {}
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_widget(self):
        self.widget_data = [
         {'text': 18201,
            'widget_func': self.init_weapon_widget,
            'widget_template': 'battle_train/i_change_weapon',
            'icon': 'gui/ui_res_2/common/icon/icon_common_gun.png',
            'icon_dark': 'gui/ui_res_2/common/icon/icon_common_gun_dark.png'
            },
         {'text': 920735,
            'widget_func': self.init_item_widget,
            'widget_template': 'battle_train/i_change_item',
            'icon': 'gui/ui_res_2/common/icon/icon_common_item.png',
            'icon_dark': 'gui/ui_res_2/common/icon/icon_common_item_dark.png'
            },
         {'text': 80587,
            'widget_func': self.init_armor_widget,
            'widget_template': 'battle_train/i_change_armor',
            'icon': 'gui/ui_res_2/common/icon/icon_common_armor.png',
            'icon_dark': 'gui/ui_res_2/common/icon/icon_common_armor_dark.png'
            }]
        self.widgets_helper = WidgetCommonComponent(self.panel.nd_content, self.widget_data)
        self.widgets_helper.set_widget_switch_func(self.on_switch_widget)
        self.panel.temp_bg.lab_title.SetString(get_text_by_id(861002))
        self.panel.temp_bg.icon_title.SetDisplayFrameByPath('', 'gui/ui_res_2/battle_train/icon_peizhirukou2.png')
        self.panel.temp_bg.list_tab.SetInitCount(1)
        self.panel.temp_bg.list_tab.GetItem(0).list_btn_left.SetInitCount(len(self.widget_data))
        self.list_tab = [ self.panel.temp_bg.list_tab.GetItem(0).list_btn_left.GetItem(i) for i in range(len(self.widget_data)) ]
        self.tag_btn_dict = {}
        for idx, tag in enumerate(self.LEFT_TAB):
            tag_name = self.widget_data[idx].get('text')
            icon_dark = self.widget_data[idx].get('icon_dark')
            tag_btn = self.list_tab[idx]
            self.tag_btn_dict[tag] = tag_btn
            tag_btn.btn_window_tab.SetText(tag_name)
            tag_btn.icon.SetDisplayFrameByPath('', icon_dark)

            @tag_btn.btn_window_tab.unique_callback()
            def OnClick(_btn, _touch, _idx=idx, *args):
                if global_data.player and global_data.player.logic:
                    self.widgets_helper.on_switch_to_widget(_idx)

    def init_weapon_widget(self, nd):
        from logic.comsys.exercise_ui.ExerciseWeaponWidget import ExerciseWeaponWidget
        self.panel.temp_bg.list_tab.GetItem(0).list_btn_left.SetInitCount(len(self.widget_data))
        return ExerciseWeaponWidget(self, nd)

    def init_item_widget(self, nd):
        from logic.comsys.exercise_ui.ExerciseItemWidget import ExerciseItemWidget
        return ExerciseItemWidget(self, nd)

    def init_armor_widget(self, nd):
        from logic.comsys.exercise_ui.ExerciseArmorWidget import ExerciseArmorWidget
        return ExerciseArmorWidget(self, nd)

    def on_switch_widget(self, index, widget, is_show):
        btn_nd = self.tag_btn_dict[self.LEFT_TAB[index]]
        btn_nd.btn_window_tab.SetSelect(is_show)
        icon_dark = self.widget_data[self.cur_index].get('icon_dark')
        tag_btn = self.list_tab[self.cur_index]
        tag_btn.icon.SetDisplayFrameByPath('', icon_dark)
        icon = self.widget_data[index].get('icon')
        tag_btn = self.list_tab[index]
        tag_btn.icon.SetDisplayFrameByPath('', icon)
        self.cur_index = index
        if is_show:
            btn_nd.PlayAnimation('click')
            btn_nd.RecordAnimationNodeState('continue')
            btn_nd.PlayAnimation('continue')
            global_data.emgr.exercise_set_eq_tab.emit(index)
        else:
            btn_nd.StopAnimation('continue')
            btn_nd.RecoverAnimationNodeState('continue')
        widget.on_switch_widget()
        widget.on_switch_tab(0)

    def init_ui_events(self):

        @self.temp_bg.btn_close.callback()
        def OnClick(*args):
            self.close()
            if global_data.mouse_mgr:
                global_data.mouse_mgr.add_cursor_hide_count('ExerciseWeaponConfUI')

    def _on_click_close_PC(self, *args, **kwargs):
        from logic.vscene.parts.ctrl.InputMockHelper import trigger_ui_btn_event
        trigger_ui_btn_event('ExerciseEquipmentUI', 'temp_bg.btn_close', need_check_vis=True)

    def on_finalize_panel(self):
        self.process_events(False)
        self.destroy_widget('widgets_helper')
        self.init_params()
        global_data.display_agent.set_longtime_post_process_active('gaussian_blur', False)
        self.show_main_ui()
        self.widget_data = None
        super(ExerciseEquipmentUI, self).on_finalize_panel()
        return