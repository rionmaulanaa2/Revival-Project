# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityNewBieCharge.py
from __future__ import absolute_import
from logic.client.const import mall_const
from logic.gutils import template_utils
from logic.gutils import item_utils
from logic.gutils import activity_utils
from common.cfg import confmgr
from logic.comsys.activity.ActivityTemplate import ActivityTemplate
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no, get_lobby_item_name, get_lobby_item_desc
from logic.comsys.charge_ui.NewRoleChargeWidget import NewRoleChargeWidget
from logic.comsys.charge_ui.NewRoleChargeWidgetNew import NewRoleChargeWidgetNew
import logic.gcommon.common_const.activity_const as activity_const

class ActivityNewBieCharge(ActivityTemplate):

    def __init__(self, dlg, activity_type):
        ActivityTemplate.__init__(self, dlg, activity_type)
        group_b = not G_IS_NA_PROJECT and not global_data.channel.is_steam_channel()
        if group_b:
            self._charge_widget = NewRoleChargeWidgetNew()
            from logic.comsys.activity.NewAlphaPlan.AlphaPlanMainUI import AlphaPlanMainUI
            self._charge_widget.on_init_panel(dlg, parent_ui_cls_name=AlphaPlanMainUI.__name__)
        else:
            self._charge_widget = NewRoleChargeWidget()
            from logic.comsys.activity.NewAlphaPlan.AlphaPlanMainUI import AlphaPlanMainUI
            self._charge_widget.on_init_panel(dlg.temp_beginner, parent_ui_cls_name=AlphaPlanMainUI.__name__)

    def on_init_panel(self):
        ActivityTemplate.on_init_panel(self)
        if global_data.ui_lifetime_log_mgr:
            activity_type = activity_utils.get_activity_widget_type(self._activity_type)
            global_data.ui_lifetime_log_mgr.start_record_ui_page_life_time(activity_type, self.__class__.__name__)

    def on_finalize_panel(self):
        self._charge_widget and self._charge_widget.on_finalize_panel()
        ActivityTemplate.on_finalize_panel(self)
        if global_data.ui_lifetime_log_mgr:
            activity_type = activity_utils.get_activity_widget_type(self._activity_type)
            global_data.ui_lifetime_log_mgr.finish_record_ui_page_life_time(activity_type, self.__class__.__name__)

    def set_show(self, show, is_init=False):
        self._charge_widget and self._charge_widget.set_show(show)

    def init_event(self):
        ActivityTemplate.init_event(self)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'task_prog_changed': self._on_task_prog_changed,
           'receive_task_reward_succ_event': self._on_receive_task_reward_succ_event,
           'buy_good_success': self._on_buy_good_success
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def refresh_panel(self):
        pass

    def _on_task_prog_changed(self, *args, **kw):
        global_data.emgr.refresh_activity_redpoint.emit()

    def _on_receive_task_reward_succ_event(self, *args, **kw):
        global_data.emgr.refresh_activity_redpoint.emit()

    def _on_buy_good_success(self, *args, **kw):
        global_data.emgr.refresh_activity_redpoint.emit()