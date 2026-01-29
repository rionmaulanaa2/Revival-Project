# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/Calendar/CalendarModeTipsUI.py
from __future__ import absolute_import
import six
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_1, UI_VKB_CLOSE
from logic.gcommon import time_utility as tutil
from common.cfg import confmgr
from common.const import uiconst
import datetime
import cc
from common.framework import Functor
from logic.gcommon.common_const.activity_const import ACTIVITY_TIME_NOTICE_DATE_KEY
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.time_utility import UTC

class CalendarModeTipsUI(BasePanel):
    PANEL_CONFIG_NAME = 'lobby/mode_tips'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'temp_mode_tip.btn_close.OnClick': 'on_click_close'
       }
    GLOBAL_EVENT = {'reserve_activity_changed': 'on_reserve_activity_changed'
       }

    def on_init_panel(self):
        self.mode_item_dict = {}
        self.mode_notice_dict = {}
        self.panel.temp_mode_tip.lab_title.SetString(get_text_by_id(19867))
        self.panel.lab_tips.SetString(get_text_by_id(19866))
        self.init_notice_dict()
        self.init_mode_items()

    def on_finalize_panel(self):
        self.check_mode_save_date()
        global_data.emgr.reserve_activity_changed.emit()

    def on_click_close(self, *args):
        self.close()

    def on_reserve_activity_changed(self, *args):
        self.init_notice_dict()
        for battle_type, item in six.iteritems(self.mode_item_dict):
            if self.mode_notice_dict.get(battle_type):
                item.img_choose.setVisible(True)
            else:
                item.img_choose.setVisible(False)

    def init_mode_items(self):
        ac_conf = confmgr.get('battle_opentime_config')
        activity_2_list = ac_conf.get('2')
        activity_3_list = ac_conf.get('3')
        ac_list = []
        ac_list.extend(activity_2_list)
        ac_list.extend(activity_3_list)
        notice_dict = self.mode_notice_dict
        mode_item_dict = self.mode_item_dict
        battle_config = confmgr.get('battle_config')
        for ac in ac_list:
            battle_type, battle_desc, mode_id = ac['battle_type'], ac['battle_desc'], ac['mode_id']
            if battle_type in mode_item_dict:
                continue
            bconf = battle_config.get(battle_type, None)
            if not bconf:
                continue
            cNameId = bconf['cNameTID']
            item = self.panel.list_mode_tips.AddTemplateItem()
            mode_item_dict[battle_type] = item
            item.img_choose.setVisible(notice_dict.get(battle_type, False))
            item.lab_mode.SetString(get_text_by_id(cNameId))
            item.btn_choose.OnClick = Functor(self.on_click_mode, battle_type, item)
            item.btn_mode_introduce.OnClick = Functor(self.on_click_intro, battle_type, mode_id, item)

        return

    def on_click_mode(self, *args):
        battle_type, item, _ = args
        visible = item.img_choose.IsVisible()
        item.img_choose.setVisible(not visible)

    def on_click_intro(self, *args):
        self.check_mode_save_date()
        battle_type, mode_id, item, _ = args
        from logic.comsys.lobby.Calendar.CalendarModeIntroUI import CalendarModeIntroUI
        ui = CalendarModeIntroUI()
        ui.init_intro_panel(mode_id, battle_type)

    def check_mode_save_date(self):
        battle_time_notice_dict = {}
        for battle_type, item in six.iteritems(self.mode_item_dict):
            if item.img_choose.IsVisible():
                battle_time_notice_dict[battle_type] = True
            else:
                battle_time_notice_dict[battle_type] = False

        archive_data = global_data.achi_mgr.get_general_archive_data()
        archive_data.set_field(ACTIVITY_TIME_NOTICE_DATE_KEY, battle_time_notice_dict)

    def init_notice_dict(self):
        archive_date = global_data.achi_mgr.get_general_archive_data()
        self.mode_notice_dict = archive_date.get_field(ACTIVITY_TIME_NOTICE_DATE_KEY, {})