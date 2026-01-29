# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/task/TaskMainUI.py
from __future__ import absolute_import
import six
from six.moves import range
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, BG_ZORDER, UI_VKB_CUSTOM
from logic.gcommon.common_const.task_const import TASK_TYPE_DAYLY, TASK_TYPE_WEEKLY, TASK_TYPE_ASSESS, TASK_TYPE_SEASON, TASK_TYPE_CORP, TASK_TYPE_GROWTH, TASK_TYPE_WEEKLY_PVE, TASK_TYPE_CLAN_DAILY
from .DayTaskWidget import DayTaskWidget
from .ClanTaskWidget import ClanTaskWidget
from .WeekTaskWidget import WeekTaskWidget
from .AssessTaskWidget import AssessTaskWidget
from .SeasonTaskWidget import SeasonTaskWidget
from .CorpTaskWidget import CorpTaskWidget
from .GrowthTaskWidget import GrowthTaskWidget
from .PVEWeekTaskWidget import PVEWeekTaskWidget
from logic.gutils.new_template_utils import CommonLeftTabList
from data.newbiepass_data import NEWBIEPASS_LV_CAP
import copy
from logic.gutils import mouse_scroll_utils
from logic.gcommon.common_const import ui_operation_const as uoc
from common.platform.dctool.interface import is_mainland_package
from logic.gutils.system_unlock_utils import is_sys_unlocked, show_sys_unlock_tips, SYSTEM_ASSESS_TASK, SYSTEM_SEASON_TASK, SYSTEM_CORP_TASK, SYSTEM_CLAN

class TaskMainUI(BasePanel):
    PANEL_CONFIG_NAME = 'task/task_main'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    OPEN_SOUND_NAME = 'leaderboard'
    SUB_RANK_NUM = 3
    DELAY_TIME = 1
    UI_VKB_TYPE = UI_VKB_CUSTOM
    HOT_KEY_NEED_SCROLL_SUPPORT = True
    UI_ACTION_EVENT = {'temp_btn_close.btn_back.OnClick': 'on_click_back_btn'
       }
    GLOBAL_EVENT = {'start_new_season_event': 'start_new_season_task',
       'player_info_update_event': 'refresh_red_point',
       'season_pass_open_type': 'refresh_red_point',
       'task_prog_changed': 'refresh_red_point',
       'receive_task_reward_succ_event': 'refresh_red_point',
       'update_day_vitality_event': 'refresh_red_point',
       'update_day_vitality_reward_event': 'refresh_red_point',
       'update_week_vitality_event': 'refresh_red_point',
       'update_week_vitality_reward_event': 'refresh_red_point',
       'corp_task_changed_event': 'refresh_red_point',
       'receive_task_prog_reward_succ_event': 'refresh_red_point',
       'refresh_task_main_redpoint': 'refresh_red_point'
       }
    ALL_TASK_WIDGET_DICT = {TASK_TYPE_DAYLY: (
                       602005, DayTaskWidget),
       TASK_TYPE_CLAN_DAILY: (
                            635670, ClanTaskWidget),
       TASK_TYPE_SEASON: (
                        602021, SeasonTaskWidget),
       TASK_TYPE_CORP: (
                      602034, CorpTaskWidget),
       TASK_TYPE_GROWTH: (
                        82089, GrowthTaskWidget),
       TASK_TYPE_WEEKLY_PVE: (
                            709132, PVEWeekTaskWidget)
       }
    TAG_LOCK_DICT = {TASK_TYPE_CLAN_DAILY: {'is_unlock': lambda : is_sys_unlocked(SYSTEM_CLAN),
                              'lock_tips': lambda : show_sys_unlock_tips(SYSTEM_CLAN),
                              'can_click': lambda : TaskMainUI.check_can_click(TASK_TYPE_CLAN_DAILY)
                              },
       TASK_TYPE_CORP: {'is_unlock': lambda : is_sys_unlocked(SYSTEM_CORP_TASK),
                        'lock_tips': lambda : show_sys_unlock_tips(SYSTEM_CORP_TASK)
                        },
       TASK_TYPE_SEASON: {'is_unlock': lambda : is_sys_unlocked(SYSTEM_SEASON_TASK),
                          'lock_tips': lambda : show_sys_unlock_tips(SYSTEM_SEASON_TASK)
                          }
       }

    def on_init_panel(self, *args, **kargs):
        self.init_parameters()
        self.init_widget()
        self.init_scroll()

    def show(self):
        self.clear_show_count_dict()
        self.hide_main_ui()
        self.get_bg_ui() and self.get_bg_ui().img_right.setVisible(False)
        super(TaskMainUI, self).show()
        self.panel.PlayAnimation('appear')

    def hide(self):
        super(TaskMainUI, self).hide()
        self.show_main_ui()

    def do_show_panel(self):
        super(TaskMainUI, self).do_show_panel()
        self.get_bg_ui() and self.get_bg_ui().setVisible(True)

    def do_hide_panel(self):
        super(TaskMainUI, self).do_hide_panel()
        self.get_bg_ui() and self.get_bg_ui().setVisible(False)

    def init_parameters(self):
        self.task_type_list = [
         TASK_TYPE_DAYLY, TASK_TYPE_CLAN_DAILY,
         TASK_TYPE_SEASON, TASK_TYPE_CORP,
         TASK_TYPE_GROWTH, TASK_TYPE_WEEKLY_PVE]
        self.cur_task_type = TASK_TYPE_DAYLY
        self.widget_dict = {}
        self.red_point_dict = {}
        self.type_2_idx = {}

    def reset_type_2_idx(self):
        self.type_2_idx = {}
        for idx in range(len(self.task_type_list)):
            task_type = self.task_type_list[idx]
            self.type_2_idx[task_type] = idx

    def init_widget(self):
        self.bg_ui = global_data.ui_mgr.create_simple_dialog('common/bg_full_screen_bg', BG_ZORDER)
        tab_list = []
        if G_IS_NA_PROJECT:
            self.task_type_list.remove(TASK_TYPE_GROWTH)
        self.reset_type_2_idx()
        for task_type in self.task_type_list:
            text_id = self.ALL_TASK_WIDGET_DICT[task_type][0]
            tab_list.append({'text': text_id})
            from logic.gcommon.common_utils.local_text import get_text_by_id
            print (
             'arrrrrrrrrrrrrr__', get_text_by_id(text_id))

        self.left_tab_list = CommonLeftTabList(self.panel.temp_left_tab, tab_list, None, self.on_click_tab)
        self.select_task_type(TASK_TYPE_DAYLY)
        self.refresh_red_point()
        return

    def get_bg_ui(self):
        if self.bg_ui and self.bg_ui.is_valid():
            return self.bg_ui

    def init_task_by_type(self, task_type, need_hide=True):
        if task_type in self.widget_dict:
            return
        widget_cls = self.ALL_TASK_WIDGET_DICT[task_type][1]
        task_widget = widget_cls(self, self.panel, task_type)
        task_widget.init_widget(need_hide)
        self.widget_dict[task_type] = task_widget

    def select_task_type(self, task_type):
        idx = self.type_2_idx[task_type]
        self.left_tab_list.select_tab_btn(idx)

    @staticmethod
    def check_can_click(task_type):
        if task_type == TASK_TYPE_CLAN_DAILY:
            is_in_clan = bool(global_data.player and global_data.player.is_in_clan())
            if is_in_clan:
                return True
            else:
                global_data.ui_mgr.show_ui('ClanJoinMainUI', 'logic.comsys.clan')
                return False

        return False

    def on_click_tab(self, idx):
        task_type = self.task_type_list[idx]
        if task_type in self.TAG_LOCK_DICT:
            lockinfo = self.TAG_LOCK_DICT.get(task_type, {})
            is_unlock = lockinfo.get('is_unlock', None)
            if is_unlock and not is_unlock():
                lock_tips = lockinfo.get('lock_tips', None)
                lock_tips and lock_tips()
                return False
            can_click = lockinfo.get('can_click')
            if can_click and callable(can_click):
                if not can_click():
                    return False
        last_widget = self.widget_dict.get(self.cur_task_type, None)
        if last_widget:
            last_widget.set_visible(False)
        cur_widget = self.widget_dict.get(task_type, None)
        if cur_widget:
            cur_widget.set_visible(True)
        else:
            self.init_task_by_type(task_type, False)
        self.cur_task_type = task_type
        if task_type == TASK_TYPE_CORP:
            self.panel.nd_top.setVisible(True)
            self.bg_ui.img_bg.SetDisplayFrameByPath('', 'gui/ui_res_2/task/contrast_task/img_contrast_bg.png')
        else:
            self.panel.nd_top.setVisible(False)
            self.bg_ui.img_bg.SetDisplayFrameByPath('', 'gui/ui_res_2/common/bg/img_info_bg.png')
        return True

    def start_new_season_task(self):
        season_task_widget = self.widget_dict.get(TASK_TYPE_SEASON, None)
        if season_task_widget:
            self.widget_dict.pop(TASK_TYPE_SEASON)
            season_task_widget.destroy()
        return

    def refresh_red_point(self, *args):
        for task_type in self.task_type_list:
            task_widget_cls = self.ALL_TASK_WIDGET_DICT[task_type][1]
            redpoint = task_widget_cls.check_red_point()
            idx = self.type_2_idx[task_type]
            tag_btn = self.panel.temp_left_tab.tab_list.GetItem(idx)
            tag_btn.img_red.setVisible(redpoint)
            if task_type in self.TAG_LOCK_DICT:
                text_id = self.ALL_TASK_WIDGET_DICT[task_type][0]
                is_unlock = self.TAG_LOCK_DICT.get(task_type, {}).get('is_unlock', None)
                locked = is_unlock and not is_unlock()
                tag_btn.img_lock.setVisible(locked)
                hide_text = ''
                if locked:
                    tag_btn.lab_lock.SetString(text_id)
                else:
                    hide_text = text_id
                if tag_btn.lab_main:
                    tag_btn.lab_main.SetString(hide_text)
                else:
                    tag_btn.btn.SetText(hide_text)

        return

    @staticmethod
    def check_red_point():
        for task_type, task_cls_conf in six.iteritems(TaskMainUI.ALL_TASK_WIDGET_DICT):
            is_unlock = TaskMainUI.TAG_LOCK_DICT.get(task_type, {}).get('is_unlock', None)
            if is_unlock and not is_unlock():
                continue
            task_widget = task_cls_conf[1]
            if task_widget.check_red_point():
                return True

        return False

    def on_finalize_panel(self):
        for task_widget in six.itervalues(self.widget_dict):
            task_widget.destroy()

        self.get_bg_ui() and self.get_bg_ui().close()
        self.widget_dict = None
        global_data.emgr.show_lobby_common_bg_event.emit(False)
        self.show_main_ui()
        if self.left_tab_list:
            self.left_tab_list.destroy()
            self.left_tab_list = None
        return

    def on_before_close(self, callback):
        self.get_bg_ui() and self.get_bg_ui().setVisible(False)
        if callback:
            callback()

    def on_resolution_changed(self):
        import game3d
        game3d.delay_exec(1, self.close)

    def on_click_back_btn(self, *args):
        self.close(*args)

    def close_task(self, task_type):
        idx = self.type_2_idx[task_type]
        self.left_tab_list.delete_one_tab(idx)
        task_widget = self.widget_dict.get(task_type, None)
        if task_widget:
            self.task_type_list.pop(idx)
            self.widget_dict.pop(task_type)
            task_widget.destroy()
            self.reset_type_2_idx()
            self.select_task_type(TASK_TYPE_DAYLY)
        return

    def ui_vkb_custom_func(self):
        self.on_click_back_btn()
        return True

    def init_scroll(self):
        if global_data.is_pc_mode:
            self.register_mouse_scroll_event()

    def on_hot_key_mouse_scroll(self, msg, delta, key_state):
        cur_widget = self.widget_dict[self.cur_task_type]
        if not cur_widget:
            return
        task_list = cur_widget.ui_view_list
        if not task_list:
            return
        mouse_scroll_utils.sview_scroll_by_mouse_wheel_dynamic(cur_widget, task_list, delta, uoc.SST_TASK_MAIN_MOUSE_WHEEL)

    def check_can_mouse_scroll(self):
        if global_data.is_pc_mode and self.HOT_KEY_NEED_SCROLL_SUPPORT and global_data.player:
            return True
        return False