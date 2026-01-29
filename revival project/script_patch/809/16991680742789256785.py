# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/Calendar/CalendarUI.py
from __future__ import absolute_import
import six
from six.moves import range
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_1, UI_VKB_CLOSE_BY_DEFAULT_FUNC_NAME
from logic.gcommon import time_utility as tutil
from common.cfg import confmgr
from common.const import uiconst
import datetime
import cc
from logic.gcommon.common_const.activity_const import ACTIVITY_TIME_NOTICE_DATE_KEY
from common.framework import Functor
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_const.activity_const import ACTIVITY_ID_3, ACTIVITY_ID_2
from logic.gcommon.time_utility import UTC
ACTIVITY_STATUS_END = 1
ACTIVITY_STATUS_UNSTART = 2
ACTIVITY_STATUS_GOING = 3
ACTIVITY_STATUS_STR = {ACTIVITY_STATUS_UNSTART: 19863,
   ACTIVITY_STATUS_GOING: 19864,
   ACTIVITY_STATUS_END: 19865
   }
ACTIVITY_STATUS_FONT_CFG = {ACTIVITY_STATUS_UNSTART: (16, 4291546367L),
   ACTIVITY_STATUS_GOING: (18, 4280556845L),
   ACTIVITY_STATUS_END: (18, 4289835441L)
   }
ACTIVITY_STATUS_FONT_CFG2 = {ACTIVITY_STATUS_UNSTART: 4291546367L,
   ACTIVITY_STATUS_GOING: 4294967295L,
   ACTIVITY_STATUS_END: 4289835441L
   }

class CalendarUI(BasePanel):
    PANEL_CONFIG_NAME = 'lobby/mode_calendar'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = UI_VKB_CLOSE_BY_DEFAULT_FUNC_NAME
    UI_ACTION_EVENT = {'temp_close.btn_back.OnClick': 'on_click_close_btn',
       'btn_tips.OnClick': 'on_tips_click'
       }
    GLOBAL_EVENT = {'reserve_activity_changed': 'on_reserve_activity_changed'
       }
    WEEK_STR_MAP = {0: 19856,
       1: 19857,
       2: 19858,
       3: 19859,
       4: 19860,
       5: 19861,
       6: 19862
       }

    def on_init_panel(self):
        self.date_item_list = []
        self.datetime_list = []
        self.activity_map = {}
        self.show_item_dict = {}
        self.init_calendar_date()
        self.init_activity_date()
        self.hide_main_ui()
        self.init_date_items()
        self.refresh_activity_status()
        self.panel.lab_tips.SetString(get_text_by_id(19848))
        self.on_reserve_activity_changed()
        self.on_refresh_activity_img()
        self.panel.PlayAnimation('show')
        self.panel.SetTimeOut(0.5, self.begin_show_animate)
        show_time_second = self.panel.GetAnimationMaxRunTime('show')
        self.panel.SetTimeOut(show_time_second, lambda : self.panel.PlayAnimation('loop'))
        global_data.display_agent.set_longtime_post_process_active('gaussian_blur', True)

    def begin_show_animate(self, *args):
        ani_show3_second = 0
        for battle_type, info_dicts in six.iteritems(self.show_item_dict):
            for info_dict in info_dicts:
                if info_dict['ui_ac_type'] == 1:
                    items = info_dict['item_list']
                    status = info_dict['ac_status']
                    for item in items:
                        if status == ACTIVITY_STATUS_GOING:
                            ani_show3_second = item.GetAnimationMaxRunTime('show3')
                            item.PlayAnimation('show3')

                else:
                    items = info_dict['item_list']
                    status = info_dict['ac_status']
                    if items:
                        if status == ACTIVITY_STATUS_GOING:
                            item = items[0]
                            item.PlayAnimation('show2')

        def show_lab_show_ani():
            for battle_type, info_dicts in six.iteritems(self.show_item_dict):
                for info_dict in info_dicts:
                    if info_dict['ui_ac_type'] == 1:
                        item = info_dict['item_list'][0]
                        if item and item.isValid():
                            item.PlayAnimation('lab_show')

        self.panel.SetTimeOut(ani_show3_second, show_lab_show_ani)

    def on_finalize_panel(self):
        self.date_item_list = []
        self.datetime_list = {}
        self.activity_map = {}
        self.show_item_dict = {}
        self.show_main_ui()
        global_data.display_agent.set_longtime_post_process_active('gaussian_blur', False)

    def on_click_close_btn(self, *args):
        self.panel.PlayAnimation('exit')
        exit_time = self.panel.GetAnimationMaxRunTime('exit')
        self.panel.SetTimeOut(exit_time, self.close)

    def on_tips_click(self, *args):
        from logic.comsys.lobby.Calendar.CalendarModeTipsUI import CalendarModeTipsUI
        self.panel.PlayAnimation('remind')
        ani_time = self.panel.GetAnimationMaxRunTime('remind')
        self.panel.SetTimeOut(ani_time, lambda : CalendarModeTipsUI())

    def on_reserve_activity_changed(self, *args):
        archive_date = global_data.achi_mgr.get_general_archive_data()
        notice_dict = archive_date.get_field(ACTIVITY_TIME_NOTICE_DATE_KEY, {})
        for battle_type, flag in six.iteritems(notice_dict):
            if battle_type in self.show_item_dict:
                info_dicts = self.show_item_dict[battle_type]
                for info_dict in info_dicts:
                    item = info_dict['item_list'][0]
                    ac_status = info_dict['ac_status']
                    if ac_status == ACTIVITY_STATUS_UNSTART:
                        item.img_clock.setVisible(flag)

    def on_refresh_activity_img(self):
        from logic.gutils.mode_utils import get_sub_modes_by_show_type
        for battle_type, info_dicts in six.iteritems(self.show_item_dict):
            for info_dict in info_dicts:
                ac = info_dict['ac_info']
                item = info_dict['item_list'][0]
                _, _, _, _, _, mode_id = ac
                conf = confmgr.get('c_battle_mode_show_config', str(mode_id))
                if conf:
                    sub_modes = get_sub_modes_by_show_type(str(mode_id))
                    if len(sub_modes) > 1:
                        sub_conf = confmgr.get('c_battle_mode_show_config', str(sub_modes[0]))
                        mode_pic = sub_conf.get('cModeImgs', '')
                    else:
                        mode_pic = conf.get('cModeImgs', '')
                    if mode_pic:
                        item.img_cut.SetDisplayFrameByPath('', mode_pic[0])

    def init_calendar_date(self):
        now = datetime.datetime.fromtimestamp(tutil.time())
        now = datetime.datetime(year=now.year, month=now.month, day=now.day, tzinfo=UTC(8))
        self.now = now
        now_weekday = now.weekday()
        for i in range(14):
            if i == now_weekday:
                self.datetime_list.append(now)
                continue
            day_ofs = i - now_weekday
            day = now + datetime.timedelta(days=day_ofs)
            self.datetime_list.append(day)

    def init_activity_date(self):
        ac_conf = confmgr.get('battle_opentime_config')
        self.activity_map[ACTIVITY_ID_2] = []
        self.activity_map[ACTIVITY_ID_3] = []
        activity_2_list = ac_conf.get(ACTIVITY_ID_2, [])
        activity_3_list = ac_conf.get(ACTIVITY_ID_3, [])
        activity_list = [
         [
          ACTIVITY_ID_2, activity_2_list],
         [
          ACTIVITY_ID_3, activity_3_list]]
        for aid, acs in activity_list:
            for ac in acs:
                start_date = datetime.datetime(tzinfo=UTC(8), *[ int(x) for x in ac['start_date'] ])
                end_date = datetime.datetime(tzinfo=UTC(8), *[ int(x) for x in ac['end_date'] ])
                ac_time = ac['time']
                battle_desc = ac['battle_desc']
                battle_type = ac['battle_type']
                mode_id = ac['mode_id']
                self.activity_map[aid].append([start_date, end_date, ac_time, battle_desc, battle_type, mode_id])

    def refresh_activity_status(self):
        date_list = self.datetime_list
        show_start_date = date_list[0]
        show_end_date = date_list[-1]
        now = self.now
        for aid, acs in six.iteritems(self.activity_map):
            show_acs = []
            for ac in acs:
                show_flag = False
                if self._is_between_dates(show_start_date, show_end_date, ac[0]):
                    show_flag = True
                elif self._is_between_dates(show_start_date, show_end_date, ac[1]):
                    show_flag = True
                elif self._is_between_dates(ac[0], ac[1], show_start_date) and self._is_between_dates(ac[0], ac[1], show_end_date):
                    show_flag = True
                if show_flag:
                    show_acs.append(ac)

            for sac in show_acs:
                ac_start_time = sac[0]
                ac_end_time = sac[1]
                ac_start, ac_end, ac_time, ac_desc, ac_type, mode_id = sac
                ac_start_time = show_start_date if ac_start_time < show_start_date else ac_start_time
                if ac_end_time > show_end_date:
                    ac_end_time = show_end_date if 1 else ac_end_time
                    ac_status = None
                    if ac_end_time < now:
                        ac_status = ACTIVITY_STATUS_END
                    elif ac_start_time > now:
                        ac_status = ACTIVITY_STATUS_UNSTART
                    else:
                        ac_status = ACTIVITY_STATUS_GOING
                    ui_ac_type = None
                    if ac_start_time == ac_end_time:
                        ui_ac_type = 1
                    elif ac_end_time < date_list[7] or ac_start_time >= date_list[7]:
                        ui_ac_type = 2
                    else:
                        ui_ac_type = 3
                        line_1_offset = (date_list[6] - ac_start_time).days + 1
                        line_2_offset = (ac_end_time - date_list[7]).days + 1
                        if line_1_offset > 2 or line_2_offset > 2:
                            ui_1_ac_type = 1 if line_1_offset == 1 else 2
                            ui_2_ac_type = 1 if line_2_offset == 1 else 2
                            ac1 = [
                             ac_start_time, date_list[6], ac_time, ac_desc, ac_type, mode_id]
                            ac2 = [date_list[7], ac_end_time, ac_time, ac_desc, ac_type, mode_id]
                            self.show_single_activity_item(ac1, ui_1_ac_type, aid, ac_status)
                            self.show_single_activity_item(ac2, ui_2_ac_type, aid, ac_status)
                            continue
                    self.show_single_activity_item(sac, ui_ac_type, aid, ac_status)

        return

    def show_single_activity_item(self, ac, ui_ac_type, aid, ac_status):
        datelist = self.datetime_list
        date_item_list = self.date_item_list
        start_ac_time_index = None
        end_ac_time_index = None
        show_start_date = datelist[0]
        show_end_date = datelist[-1]
        ac_start, ac_end, ac_time, ac_desc, ac_type, mode_id = ac
        battle_config = confmgr.get('battle_config')
        bconf = battle_config.get(ac_type)
        if bconf:
            cnameId = bconf['cNameTID']
            ac_desc = get_text_by_id(cnameId)
        now = self.now
        ac_start = show_start_date if ac_start < show_start_date else ac_start
        ac_end = show_end_date if ac_end > show_end_date else ac_end
        for idx, date in enumerate(datelist):
            if date == ac_start:
                start_ac_time_index = idx
            if date == ac_end:
                end_ac_time_index = idx

        if start_ac_time_index is None or end_ac_time_index is None:
            return
        else:
            if ui_ac_type in (1, 2):
                ui_item = date_item_list[start_ac_time_index]
                parent_item = ui_item.nd_mode_1 if aid == ACTIVITY_ID_2 else ui_item.nd_mode_2
                ui_activity_name = 'ui_activity{}'.format(aid)
                ui_template_name = 'lobby/i_mode_calendar_3' if ui_ac_type == 1 else 'lobby/i_mode_calendar_2'
                ac_item = global_data.uisystem.load_template_create(ui_template_name, parent=parent_item, name=ui_activity_name)
                ac_item.lab_mode.SetString(ac_desc)
                time_str = ac_time[:2] + ':' + ac_time[2:4] + ' - ' + ac_time[5:7] + ':' + ac_time[7:9]
                ac_item.lab_mode_time.SetString(time_str)
                ac_item.lab_mode_1.SetString(get_text_by_id(ACTIVITY_STATUS_STR[ac_status]))
                ac_item.lab_mode_1.SetFontSize(ACTIVITY_STATUS_FONT_CFG[ac_status][0])
                ac_item.lab_mode_1.SetColor(ACTIVITY_STATUS_FONT_CFG[ac_status][1])
                ac_item.lab_mode.SetColor(ACTIVITY_STATUS_FONT_CFG2[ac_status])
                ac_item.lab_mode_time.SetColor(ACTIVITY_STATUS_FONT_CFG2[ac_status])
                ac_item.nd_mode_bg_2.setVisible(ac_status == ACTIVITY_STATUS_UNSTART)
                ac_item.nd_mode_bg_3.setVisible(ac_status == ACTIVITY_STATUS_GOING)
                ac_item.nd_mode_bg_2.OnClick = Functor(self.on_click_calendar_activity, ac_type, mode_id)
                ac_item.nd_mode_bg_3.OnClick = Functor(self.on_click_calendar_activity, ac_type, mode_id)
                for i in range(1, 4):
                    img_mode = getattr(ac_item, 'img_mode_{}'.format(i))
                    img_mode.setVisible(i == ac_status)

                if ui_ac_type == 1:
                    ac_item.nd_real.OnClick = Functor(self.on_click_calendar_activity, ac_type, mode_id)
                if ui_ac_type == 2:
                    ac_item.nd_mode_bg_2.setAnchorPoint(cc.Vec2(0.5, 0.5))
                    ac_item.nd_mode_bg_2.SetPosition('50%', '50%')
                    ac_item.nd_mode_bg_3.setAnchorPoint(cc.Vec2(0.5, 0.5))
                    ac_item.nd_mode_bg_3.SetPosition('50%', '50%')
                    ac_item.nd_mode_bg_2.OnClick = Functor(self.on_click_calendar_activity, ac_type, mode_id)
                    ac_item.nd_mode_bg_3.OnClick = Functor(self.on_click_calendar_activity, ac_type, mode_id)
                    days = end_ac_time_index - start_ac_time_index
                    x_percent = 100 * (days + 1) / 2.0
                    scale = 1.0 + (days - 1) * 0.5
                    ac_item.SetPosition('{}%'.format(int(x_percent)), '50%')
                    if ac_status == ACTIVITY_STATUS_GOING:
                        size = ac_item.nd_mode_bg_3.getContentSize()
                        ac_item.nd_mode_bg_3.SetContentSize(size.width * scale, size.height)
                        ac_item.nd_mode_bg_3.ChildResizeAndPosition()
                        ac_item.img_bar_2.setAnchorPoint(cc.Vec2(0.5, 0.5))
                        ac_item.img_bar_2.SetPosition('50%2', '50%-7')
                    elif ac_status == ACTIVITY_STATUS_UNSTART:
                        size = ac_item.nd_mode_bg_2.getContentSize()
                        ac_item.nd_mode_bg_2.SetContentSize(size.width * scale, size.height)
                        ac_item.nd_mode_bg_2.ChildResizeAndPosition()
                if ac_type not in self.show_item_dict:
                    self.show_item_dict[ac_type] = []
                self.show_item_dict[ac_type].append({'ac_info': ac,
                   'item_list': [
                               ac_item],
                   'ac_status': ac_status,
                   'ui_ac_type': ui_ac_type
                   })
            elif ui_ac_type == 3:
                ui_items = [date_item_list[start_ac_time_index], date_item_list[7]]
                ui_template_name = 'lobby/i_mode_calendar_2'
                ui_activity_name = 'ui_activity{}'.format(aid)
                ac_items = []
                for ui_item in ui_items:
                    if aid == ACTIVITY_ID_2:
                        parent_item = ui_item.nd_mode_1 if 1 else ui_item.nd_mode_2
                        ac_item = global_data.uisystem.load_template_create(ui_template_name, parent=parent_item, name=ui_activity_name)
                        ac_items.append(ac_item)
                        ac_item.lab_mode_1.SetString(get_text_by_id(ACTIVITY_STATUS_STR[ac_status]))
                        ac_item.lab_mode_1.SetColor(ACTIVITY_STATUS_FONT_CFG[ac_status][1])
                        ac_item.lab_mode.SetColor(ACTIVITY_STATUS_FONT_CFG2[ac_status])
                        ac_item.lab_mode_time.SetColor(ACTIVITY_STATUS_FONT_CFG2[ac_status])
                        ac_item.nd_mode_bg_2.setVisible(ac_status == ACTIVITY_STATUS_UNSTART)
                        ac_item.nd_mode_bg_3.setVisible(ac_status == ACTIVITY_STATUS_GOING)
                        ac_item.nd_mode_bg_2.OnClick = Functor(self.on_click_calendar_activity, ac_type, mode_id)
                        ac_item.nd_mode_bg_3.OnClick = Functor(self.on_click_calendar_activity, ac_type, mode_id)
                        for i in range(1, 4):
                            img_mode = getattr(ac_item, 'img_mode_{}'.format(i))
                            img_mode.setVisible(i == ac_status)

                ac_items[0].lab_mode.setVisible(False)
                ac_items[0].lab_mode_time.setVisible(False)
                ac_items[0].setAnchorPoint(cc.Vec2(0, 0.5))
                ac_items[0].SetPosition('0%', '50%')
                scale = 0.5 + (6 - start_ac_time_index) * 0.5
                mode_bg = ac_items[0].nd_mode_bg_2 if ac_status == ACTIVITY_STATUS_UNSTART else ac_items[0].nd_mode_bg_3
                size = mode_bg.getContentSize()
                mode_bg.SetContentSize(size.width * scale, size.height)
                mode_bg.ChildResizeAndPosition()
                if ac_status == ACTIVITY_STATUS_UNSTART:
                    size = mode_bg.img_bar_will_start.img_line_1.getContentSize()
                mode_bg.setAnchorPoint(cc.Vec2(0, 0))
                x, y = mode_bg.CalcPosition('0%', '0%')
                mode_bg.setPosition(cc.Vec2(x, y))
                percent_x = '{}%'.format(50 + (6 - start_ac_time_index) * 50)
                ac_items[0].nd_cut.setAnchorPoint(cc.Vec2(1, 0.5))
                x, y = ac_items[0].nd_cut.CalcPosition(percent_x, '50%')
                ac_items[0].nd_cut.setPosition(cc.Vec2(x, y))
                percent_x = '{}%+5'.format(50 + (6 - start_ac_time_index) * 50)
                ac_items[0].img_mode_bar.setAnchorPoint(cc.Vec2(1, 0.5))
                x, y = ac_items[0].img_mode_bar.CalcPosition(percent_x, '50%-5')
                ac_items[0].img_mode_bar.setPosition(cc.Vec2(x, y))
                if ac_status == ACTIVITY_STATUS_UNSTART:
                    ac_items[0].img_line_2.setVisible(False)
                ac_items[1].setAnchorPoint(cc.Vec2(0, 0.5))
                x, y = ac_items[1].CalcPosition('0%', '50%')
                ac_items[1].setPosition(x, y)
                ac_items[1].nd_cut.setVisible(False)
                ac_items[1].img_mode_bar.setVisible(False)
                scale = 0.5 + (end_ac_time_index - 7) * 0.5
                mode_bg = ac_items[1].nd_mode_bg_2 if ac_status == ACTIVITY_STATUS_UNSTART else ac_items[1].nd_mode_bg_3
                size = mode_bg.getContentSize()
                mode_bg.SetContentSize(size.width * scale, size.height)
                mode_bg.ChildResizeAndPosition()
                if ac_status == ACTIVITY_STATUS_UNSTART:
                    size = mode_bg.img_bar_will_start.img_line_1.getContentSize()
                mode_bg.setAnchorPoint(cc.Vec2(0, 0))
                x, y = mode_bg.CalcPosition('0%', '0%')
                mode_bg.setPosition(cc.Vec2(x, y))
                x, y = ac_items[1].lab_mode.CalcPosition('4%', '50%11')
                ac_items[1].lab_mode.setPosition(x, y)
                x, y = ac_items[1].lab_mode_time.CalcPosition('4%', '50%-18')
                ac_items[1].lab_mode_time.setPosition(x, y)
                ac_items[1].lab_mode.SetString(ac_desc)
                time_str = ac_time[:2] + ':' + ac_time[2:4] + ' - ' + ac_time[5:7] + ':' + ac_time[7:9]
                ac_items[1].lab_mode_time.SetString(time_str)
                if ac_status == ACTIVITY_STATUS_UNSTART:
                    ac_items[1].img_line_1.setVisible(False)
                if ac_type not in self.show_item_dict:
                    self.show_item_dict[ac_type] = []
                self.show_item_dict[ac_type].append({'ac_info': ac,
                   'item_list': [
                               ac_items[0], ac_items[1]],
                   'ac_status': ac_status,
                   'ui_ac_type': ui_ac_type
                   })
            return

    def _is_between_dates(self, st_date, ed_date, date):
        start_delta = date - st_date
        end_delta = date - ed_date
        if start_delta.total_seconds() >= 0 and end_delta.total_seconds() <= 0:
            return True
        return False

    def init_date_items(self):
        for i in range(14):
            if i <= 6:
                item = self.panel.list_mode_1.AddTemplateItem()
            else:
                item = self.panel.list_mode_2.AddTemplateItem()
            if i == self.now.weekday():
                item.img_circle.setVisible(True)
                item.lab_day.SetColor(4294642083L)
                item.lab_week.SetColor(4294642083L)
            dtime = self.datetime_list[i]
            item.lab_week.SetString(get_text_by_id(self.WEEK_STR_MAP.get(i % 7)))
            item.lab_day.SetString('{}/{}'.format(dtime.month, dtime.day))
            self.date_item_list.append(item)

    def on_click_calendar_activity(self, *args):
        battle_type, mode_id, _ = args
        from logic.comsys.lobby.Calendar.CalendarModeIntroUI import CalendarModeIntroUI
        ui = CalendarModeIntroUI()
        ui.init_intro_panel(mode_id, battle_type)