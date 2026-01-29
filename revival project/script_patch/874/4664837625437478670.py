# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mall_ui/PurchaseAgeCheckUI.py
from __future__ import absolute_import
from six.moves import range
from common.uisys.basepanel import BasePanel
from common.const.uiconst import DIALOG_LAYER_ZORDER
import datetime
from logic.gutils.InfiniteScrollWidget import InfiniteScrollWidget
from logic.gcommon.time_utility import get_age
from logic.gcommon.cdata.law_config import get_japan_month_pay_limit
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase

class Birthday(object):

    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def has_all_set(self):
        if self.year != '' and self.month != '' and self.day != '':
            if self.is_valid_date():
                return True
        return False

    def is_valid_date(self):
        try:
            date = datetime.date(self.year, self.month, self.day)
        except:
            return False

        return True

    def isoformat(self):
        return '%d-%02d-%02d' % (self.year, self.month, self.day)


class PurchaseAgeCheckUI(WindowMediumBase):
    PANEL_CONFIG_NAME = 'common/purchase_limited'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    TEMPLATE_NODE_NAME = 'bg'
    UI_ACTION_EVENT = {'btn_year.OnClick': 'on_click_year_btn',
       'btn_month.OnClick': 'on_click_month_btn',
       'btn_day.OnClick': 'on_click_day_btn',
       'btn_confirm.btn_major.OnClick': 'on_click_confirm_btn',
       'bg.OnClick': 'on_click_bg_btn'
       }

    def on_init_panel(self):
        super(PurchaseAgeCheckUI, self).on_init_panel()
        self._birthday = Birthday('', '', '')
        self._cur_sel_index = None
        self.init_age_limit_show()
        self.update_birthday_show()
        self.init_year_list()
        self.init_month_list()
        self.init_day_list()
        return

    def on_click_confirm_btn(self, btn, touch):
        if not self._birthday.has_all_set():
            global_data.game_mgr.show_tip(get_text_by_id(81141))
            return
        else:
            from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2

            def confirm_callback():
                if global_data.player:
                    global_data.player.set_born_date(self._birthday.isoformat())
                self.close()

            ok_index = self.get_limit_index()
            if ok_index < 0:
                global_data.game_mgr.show_tip(get_text_by_id(81141))
                return
            limit_data = get_japan_month_pay_limit()
            age_limit_data = limit_data[ok_index]
            pay_limit = age_limit_data.get('pay_jp_limit', None)
            content = get_text_by_id(81113, {'birthday': self._birthday.isoformat(),'limit': pay_limit if pay_limit else get_text_by_id(81119)})
            SecondConfirmDlg2().confirm(content=content, confirm_callback=confirm_callback)
            return

    def init_year_list(self):
        self._year_data_list = range(max(datetime.datetime.now().year, 2019) + 1, 1900, -1)
        self._year_list_sview = InfiniteScrollWidget(self.panel.year_list.option_list, self.panel.btn_year)
        self._year_list_sview.set_template_init_callback(self.init_year_button)
        self._year_list_sview.update_data_list(self._year_data_list)
        self._year_list_sview.update_scroll_view()

        @self.panel.year_list.nd_close.callback()
        def OnClick(*args):
            self.set_list_vis(self.panel.btn_year, self.panel.year_list, False)

    def init_year_button(self, ui_item, year):
        ui_item.button.SetText(str(year))

        @ui_item.button.callback()
        def OnClick(btn, touch):
            self.set_list_vis(self.panel.btn_year, self.panel.year_list, False)
            self.chose_year(year)

    def chose_year(self, year):
        self.update_birthday(year, None, None)
        return

    def chose_month(self, month):
        self.update_birthday(None, month, None)
        return

    def chose_day(self, day):
        self.update_birthday(None, None, day)
        return

    def update_birthday(self, new_year, new_month, new_day):
        self._birthday.year = new_year or self._birthday.year
        self._birthday.month = new_month or self._birthday.month
        self._birthday.day = new_day or self._birthday.day
        self.update_birthday_show()

    def update_birthday_show(self):
        self.panel.btn_year.SetText(str(self._birthday.year))
        self.panel.btn_month.SetText(str(self._birthday.month))
        self.panel.btn_day.SetText(str(self._birthday.day))
        self.update_limit_show()

    def init_month_list(self):
        month_list = range(1, 13)
        from logic.gutils import template_utils
        mode_option = [ {'name': str(mon),'mode': mon} for mon in month_list
                      ]

        def call_back(index):
            option = mode_option[index]
            self.chose_month(option['mode'])
            self.set_list_vis(self.panel.btn_month, self.panel.month_list, False)

        template_utils.init_common_choose_list(self.panel.month_list, mode_option, call_back, self.panel.month_list.getContentSize().height)

    def init_day_list(self):
        import calendar
        try:
            day_num = 31
            if self._birthday.year and self._birthday.month:
                _, day_num = calendar.monthrange(self._birthday.year, self._birthday.month)
        except:
            day_num = 31

        from logic.gutils import template_utils
        mode_option = [ {'name': str(day),'mode': day} for day in range(1, day_num + 1) ]

        def call_back(index):
            option = mode_option[index]
            self.chose_day(option['mode'])
            self.set_list_vis(self.panel.btn_day, self.panel.day_list, False)

        template_utils.init_common_choose_list(self.panel.day_list, mode_option, call_back, self.panel.day_list.getContentSize().height)

    def on_click_year_btn(self, btn, touch):
        self.set_list_vis(self.panel.btn_year, self.panel.year_list, not self.panel.year_list.isVisible())

    def on_click_month_btn(self, btn, touch):
        self.set_list_vis(self.panel.btn_month, self.panel.month_list, not self.panel.month_list.isVisible())

    def on_click_day_btn(self, btn, touch):
        self.init_day_list()
        self.set_list_vis(self.panel.btn_day, self.panel.day_list, not self.panel.day_list.isVisible())

    def set_list_vis(self, btn, list, vis):
        if vis:
            btn.img_icon.setRotation(180)
            list.setVisible(True)
        else:
            btn.img_icon.setRotation(0)
            list.setVisible(False)

    def on_click_close_btn(self, btn, touch):
        self.close()

    def init_age_limit_show(self):
        age_limits = get_japan_month_pay_limit()
        self.panel.list_rule.SetInitCount(len(age_limits))
        for idx, age_info in enumerate(age_limits):
            ui_item = self.panel.list_rule.GetItem(idx)
            ui_item.lab_age.SetString(age_info.get('text_id1', ''))
            ui_item.lab_money_limited.SetString(age_info.get('text_id2', ''))
            ui_item.lab_age.SetColor('#BH')
            ui_item.lab_money_limited.SetColor('#BH')

    def get_limit_index(self):
        if not self._birthday.has_all_set():
            return -1
        age = get_age(self._birthday)
        age_limits = get_japan_month_pay_limit()
        ok_index = 0
        for idx, age_info in enumerate(age_limits):
            func = age_info.get('age_range', lambda age: None)
            if func(age):
                ok_index = idx
                break

        return ok_index

    def update_limit_show(self):
        if not self._birthday.has_all_set():
            self.panel.btn_confirm.btn_major.SetShowEnable(False)
        else:
            self.panel.btn_confirm.btn_major.SetShowEnable(True)
        ok_index = self.get_limit_index()
        all_item = self.panel.list_rule.GetAllItem()
        for idx, ui_item in enumerate(all_item):
            ui_item.icon_tick.setVisible(idx == ok_index)

        if self._cur_sel_index is not None:
            ui_item = self.panel.list_rule.GetItem(self._cur_sel_index)
            if ui_item:
                ui_item.lab_age.SetFontName('gui/fonts/fzy4jw.ttf')
                ui_item.lab_money_limited.SetFontName('gui/fonts/fzy4jw.ttf')
                ui_item.lab_age.SetColor('#BH')
                ui_item.lab_money_limited.SetColor('#BH')
        self._cur_sel_index = ok_index
        if self._cur_sel_index >= 0:
            ui_item = self.panel.list_rule.GetItem(ok_index)
            if ui_item:
                ui_item.lab_age.SetFontName('gui/fonts/fzdys.ttf')
                ui_item.lab_money_limited.SetFontName('gui/fonts/fzdys.ttf')
                ui_item.lab_age.SetColor('#SK')
                ui_item.lab_money_limited.SetColor('#SK')
        return

    def on_click_bg_btn(self, btn, touch):
        self.set_list_vis(self.panel.btn_year, self.panel.year_list, False)
        self.set_list_vis(self.panel.btn_month, self.panel.month_list, False)
        self.set_list_vis(self.panel.btn_day, self.panel.day_list, False)