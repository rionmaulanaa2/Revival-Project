# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/charge_ui/ChargeUINew.py
from __future__ import absolute_import
import six
from common.uisys.basepanel import BasePanel
from common.const.uiconst import DIALOG_LAYER_ZORDER, UI_VKB_CLOSE
from logic.comsys.mall_ui.PriceUIWidget import PriceUIWidget
from logic.gutils import template_utils
from logic.gutils import mall_utils
from logic.gutils import task_utils
from common.cfg import confmgr
import logic.gcommon.time_utility as tutil
from logic.comsys.charge_ui.ChargeWidget import ChargeWidget
from logic.comsys.charge_ui.LimitChargeWidget import LimitChargeWidget
from logic.comsys.charge_ui.KizunaAIChargeWidget import KizunaAIChargeWidget
from logic.comsys.charge_ui.NewRoleChargeWidget import NewRoleChargeWidget
from logic.comsys.charge_ui.NewRoleChargeWidgetNew import NewRoleChargeWidgetNew
from logic.comsys.charge_ui.GrowthFundWidget import GrowthFundWidget
from logic.comsys.charge_ui.PrivilegeChargeWidget import PrivilegeChargeWidget
from logic.gutils import activity_utils
from logic.gcommon.common_const import activity_const
from logic.gutils import jump_to_ui_utils
from common.platform import is_ios
import copy
ACTIVITY_CHARGE_TYPE = 0
ACTIVITY_LIMIT_GIFTS_WEEK_TYPE = 1
ACTIVITY_NEW_ROLE_TYPE = 2
ACTIVITY_YUEKA_NEW_TYPE = activity_const.ACTIVITY_YUEKA_NEW
ACTIVITY_GROWTH_FUND = 3
ACTIVITY_KIZUNA_AI_GIFT = 4
ACTIVITY_PRIVILEGE_TYPE = 5
ACCUMULATE_CHARGE_TASK = '1301000'

class ChargeUINew(BasePanel):
    PANEL_CONFIG_NAME = 'charge/charge_main_new'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'temp_btn_close.btn_back.OnClick': 'on_click_back_btn',
       'btn_refund.OnClick': 'on_click_btn_refund'
       }
    GLOBAL_EVENT = {'buy_good_success': 'refresh_red_point',
       'update_weekly_card_info': 'refresh_red_point',
       'update_month_card_info': 'refresh_red_point',
       'receive_task_reward_succ_event': 'refresh_red_point',
       'refresh_activity_redpoint': 'refresh_red_point',
       'receive_privilege_level_reward_succ': 'refresh_red_point',
       'receive_task_prog_reward_succ_event': 'refresh_red_point'
       }

    def on_init_panel(self, default_page=None, come_from=''):
        self.come_from = come_from
        self.is_pc_global_pay = mall_utils.is_pc_global_pay()
        self._menu_conf = []
        if default_page == None:
            if mall_utils.has_new_role_page():
                self._default_page = ACTIVITY_NEW_ROLE_TYPE
            else:
                self._default_page = ACTIVITY_CHARGE_TYPE
        else:
            self._default_page = default_page
        self._cur_view_page_widget = None
        self._cur_selected_activity_type = None
        self._accumulate_charge_entry_wgt = None
        self.task_conf = task_utils.get_task_conf_by_id(ACCUMULATE_CHARGE_TASK)
        self.prog_rewards = self.task_conf.get('prog_rewards', [])
        for ani_name in ['loop_light', 'loop_box', 'open', 'loop_light_open', 'loop_cycle']:
            self.panel.RecordAnimationNodeState(ani_name)

        self.init_widget()
        self.init_tab_list()
        self.hide_main_ui()
        self.init_rebate_btn()
        return

    def can_show_rebate(self):
        return False

    def init_rebate_btn(self):
        self.panel.btn_refund.setVisible(self.can_show_rebate())
        date = tutil.get_date_str(timestamp=tutil.get_server_time())
        is_open_rebate_ui = (global_data.message_data.get_seting_inf('OPEN_REBATE_UI') or '') == date
        if self.can_show_rebate() and (not is_open_rebate_ui or self.come_from == 'banner'):
            self.on_click_btn_refund()
            global_data.message_data.set_seting_inf('OPEN_REBATE_UI', date)

    def on_finalize_panel(self):
        self.price_top_widget and self.price_top_widget.on_finalize_panel()
        self.price_top_widget = None
        self._cur_view_page_widget and self._cur_view_page_widget.set_show(False)
        self._cur_view_page_widget and self._cur_view_page_widget.on_finalize_panel()
        self._cur_view_page_widget = None
        self._cur_selected_activity_type = None
        self.activity_data = {}
        self.show_main_ui()
        return

    def init_widget--- This code section failed: ---

 169       0  LOAD_GLOBAL           0  'PriceUIWidget'
           3  LOAD_GLOBAL           1  'panel'
           6  LOAD_FAST             0  'self'
           9  LOAD_ATTR             1  'panel'
          12  LOAD_ATTR             2  'list_price'
          15  CALL_FUNCTION_257   257 
          18  LOAD_FAST             0  'self'
          21  STORE_ATTR            3  'price_top_widget'

 170      24  LOAD_FAST             0  'self'
          27  LOAD_ATTR             3  'price_top_widget'
          30  LOAD_ATTR             4  'show_money_types'
          33  LOAD_GLOBAL           5  'mall_utils'
          36  LOAD_ATTR             6  'get_default_money_types'
          39  CALL_FUNCTION_0       0 
          42  CALL_FUNCTION_1       1 
          45  POP_TOP          

Parse error at or near `CALL_FUNCTION_257' instruction at offset 15

    def init_tab_list(self):
        self.activity_data = {ACTIVITY_NEW_ROLE_TYPE: (
                                  NewRoleChargeWidget, 'charge/i_charge_gifts_new'),
           ACTIVITY_CHARGE_TYPE: (ChargeWidget, 'activity/activity/i_pc_charge') if self.is_pc_global_pay else (ChargeWidget, 'charge/i_charge_common'),
           ACTIVITY_LIMIT_GIFTS_WEEK_TYPE: (
                                          LimitChargeWidget, 'charge/i_charge_gifts_week'),
           ACTIVITY_YUEKA_NEW_TYPE: activity_const.ACTIVITY_YUEKA_NEW,
           ACTIVITY_GROWTH_FUND: (
                                GrowthFundWidget, 'activity/activity_new_domestic/i_activity_growth_fund'),
           ACTIVITY_KIZUNA_AI_GIFT: (
                                   KizunaAIChargeWidget, 'activity/activity_202103/kizunaai/i_charge_kizunaai'),
           ACTIVITY_PRIVILEGE_TYPE: (
                                   PrivilegeChargeWidget, 'charge/i_charge_reward')
           }
        if not G_IS_NA_PROJECT and not global_data.channel.is_steam_channel():
            self.activity_data[ACTIVITY_NEW_ROLE_TYPE] = (NewRoleChargeWidgetNew, 'charge/i_charge_newplayer_gifts')

        def init_func(item_widget, conf):
            text = conf.get('data', {}).get('text', '')
            if text:
                item_widget.btn.SetText(text)
            menu_list_widget = conf.get('menu_list_widget', None)
            if menu_list_widget:
                menu_list_widget.img_bar.setVisible(False)
            return

        def init_sub_func(item_widget, conf):
            item_widget.button.SetSelect(False)
            item_widget.button.SetText(conf['data']['text'])

        def select_cb(item_widget, conf):
            item_widget.btn.SetSelect(True)
            item_widget.PlayAnimation('click')
            item_widget.RecordAnimationNodeState('continue')
            item_widget.PlayAnimation('continue')
            menu_list = conf.get('menu_list', [])
            if menu_list:
                sub_conf = menu_list[0]
                sub_conf['button.OnClick']()
            else:
                a_id = conf.get('data', {}).get('a_id', None)
                self.list_tab_btn_click_func(a_id)
            return

        def unselect_cb(item_widget, conf):
            item_widget.btn.SetSelect(False)
            item_widget.StopAnimation('continue')
            item_widget.RecoverAnimationNodeState('continue')

        def sub_select_cb(item_widget, conf):
            item_widget.button.SetSelect(True)
            a_id = conf.get('data', {}).get('a_id', None)
            self.list_tab_btn_click_func(a_id)
            return

        def sub_unselect_cb(item_widget, conf):
            item_widget.button.SetSelect(False)

        menu_conf = copy.deepcopy(mall_utils.get_charge_menu_conf())
        select_act = None
        on_clicks = []
        for conf in menu_conf:
            conf['init_func'] = init_func
            conf['select_cb'] = select_cb
            conf['unselect_cb'] = unselect_cb
            conf['btn.OnClick'] = 1
            conf['btn.OnClick'] = 1
            for sub_conf in conf.get('menu_list', []):
                sub_conf['init_func'] = init_sub_func
                sub_conf['select_cb'] = sub_select_cb
                sub_conf['unselect_cb'] = sub_unselect_cb
                sub_conf['button.OnClick'] = 1

        self._menu_conf = menu_conf
        self.panel.temp_left_tab.tab_list.DeleteAllSubItem()
        template_utils.init_foldable_menu(self.panel.temp_left_tab.tab_list, menu_conf)
        self.switch_to_activity_page(self._default_page)
        self.refresh_red_point()
        return

    def switch_to_activity_page(self, activity_type=None):
        if not self._menu_conf:
            return
        else:
            if activity_type != None and activity_type == self._cur_selected_activity_type:
                return
            if activity_type == None:
                activity_type = self._default_page
            for conf in self._menu_conf:
                data = conf['data']
                a_id = data.get('a_id', None)
                if a_id == activity_type:
                    conf['btn.OnClick']()
                    return
                for sub_conf in conf.get('menu_list', []):
                    sub_data = sub_conf['data']
                    sub_a_id = sub_data.get('a_id', None)
                    if sub_a_id == activity_type:
                        conf['btn.OnClick']()
                        sub_conf['button.OnClick']()
                        return

            if mall_utils.has_new_role_page():
                self._default_page = ACTIVITY_NEW_ROLE_TYPE
            else:
                self._default_page = ACTIVITY_CHARGE_TYPE
                self.switch_to_activity_page(self._default_page)
            return

    def list_tab_btn_click_func(self, activity_type):
        self.panel.nd_charge_bones.setVisible(False)
        if activity_type == None or self._cur_selected_activity_type == activity_type:
            return
        else:
            self._cur_selected_activity_type = activity_type
            activity_data = self.activity_data.get(activity_type, None)
            if not activity_data:
                return
            self._cur_view_page_widget and self._cur_view_page_widget.set_show(False)
            self._cur_view_page_widget and self._cur_view_page_widget.on_finalize_panel()
            from logic.gutils import activity_utils
            unique_nodename = 'a_template_{}'.format(activity_type)
            if type(activity_data) in [str, six.text_type]:
                activity_type = activity_data
                ui_template = confmgr.get('c_activity_config', activity_type, 'cUiTemplate', default='').strip()
                ui_class = confmgr.get('c_activity_config', activity_type, 'cUiClass', default='')
                cls = activity_utils.get_activity_cls(ui_class)
                dlg = getattr(self.panel.temp_content, unique_nodename)
                if not dlg:
                    dlg = global_data.uisystem.load_template_create(ui_template, parent=self.panel.temp_content, name=unique_nodename)
                self._cur_view_page_widget = cls(dlg, activity_type)
                self._cur_view_page_widget.on_init_panel()
                self._cur_view_page_widget.set_show(True)
            else:
                cls, ui_template = activity_data
                dlg = getattr(self.panel.temp_content, unique_nodename)
                if not dlg:
                    dlg = global_data.uisystem.load_template_create(ui_template, parent=self.panel.temp_content, name=unique_nodename)
                self._cur_view_page_widget = cls()
                self._cur_view_page_widget.on_init_panel(dlg)
                self._cur_view_page_widget.set_show(True)
            return

    def on_click_back_btn(self, *args):
        self.close()

    def on_click_btn_refund(self, *args):
        pass

    def refresh_red_point(self, *args):
        mall_utils.refresh_charge_red_point(menu_conf=self._menu_conf)

    def extra_jump_parameters(self, func_name, *args):
        if self._cur_view_page_widget:
            func = getattr(self._cur_view_page_widget, func_name)
            if func:
                func(*args)

    def do_show_panel(self):
        super(ChargeUINew, self).do_show_panel()
        self.refresh_red_point()