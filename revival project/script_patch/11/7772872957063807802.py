# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEMainUIWidgetUI/PVETalentWidgetUI.py
from __future__ import absolute_import
import six_ex
from six.moves import range
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_1, UI_VKB_CLOSE
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.pve_utils import init_talent_item, get_attr_desc_text
from logic.gutils.template_utils import splice_price, FrameLoaderTemplate
from logic.comsys.mall_ui.PriceUIWidget import PriceUIWidget
from logic.gcommon.const import SHOP_PAYMENT_ITEM_PVE_KEY, SHOP_PAYMENT_PVE_COIN, SHOP_PAYMENT_ITEM_PVE_COIN
from common.cfg import confmgr
import time
import cc

class PVETalentWidgetUI(BasePanel):
    LEVEL_UP_TAG = 20231106
    DELAY_CLOSE_TAG = 20231129
    PANEL_CONFIG_NAME = 'pve/open_pve_talent'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'nd_content.nd_mid.btn_close.OnClick': '_on_click_back'
       }

    def on_init_panel(self, *args, **kwargs):
        super(PVETalentWidgetUI, self).on_init_panel()
        self.init_params()
        self.process_events(True)
        self.init_ui()

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'player_item_update_event': self.on_player_item_update_event,
           'refresh_pve_talent_event': self.refresh_pve_talent_event
           }
        emgr.bind_events(econf) if is_bind else emgr.unbind_events(econf)

    def play_anim(self):
        self.show()
        self.panel.PlayAnimation('appear')
        self.hide_main_ui()

    def init_params(self):
        self._disappearing = False
        self._is_first_init = True
        self._talent_conf = confmgr.get('talent_data', default={})
        self._talent_effect_conf = confmgr.get('talent_effect_data', default={})
        self._talent_id_list = six_ex.keys(self._talent_conf)
        self._current_select_talent = None
        self._current_select_talent_id = None
        self._talent_item_dict = {}
        self._price_top_widget = None
        self._async_action = None
        return

    def init_ui(self):
        self.panel.PlayAnimation('loop')
        self.init_talent_list()
        self.init_pnl_describe()
        self.init_money_widget()

    def on_resolution_changed(self):
        super(PVETalentWidgetUI, self).on_resolution_changed()

    def _on_click_back(self, *args):
        self.play_disappear_anim()

    def init_talent_list(self):
        self._frame_loader_template = FrameLoaderTemplate(self.nd_content.pnl_content.list_item, len(self._talent_conf), self.init_list_item)

    def init_list_item(self, item, cur_index):
        talent_id = self._talent_id_list[cur_index]
        self._talent_item_dict[talent_id] = item
        self._update_talent_item(talent_id)
        btn_item = item.btn_item
        btn_item.EnableCustomState(True)
        btn_choose = btn_item.btn_choose
        btn_choose.EnableCustomState(True)
        if cur_index == 0:
            self._current_select_talent = btn_item
            self._current_select_talent_id = talent_id
            btn_item.SetSelect(True)
            btn_item.btn_choose.SetSelect(True)
            self._update_talent(talent_id)

        @btn_choose.unique_callback()
        def OnClick(btn, touch):
            if self._current_select_talent == btn_item:
                return
            else:
                if self._current_select_talent != None:
                    self._current_select_talent.SetSelect(False)
                    self._current_select_talent.btn_choose.SetSelect(False)
                self._current_select_talent = btn_item
                self._current_select_talent_id = talent_id
                btn_item.SetSelect(True)
                btn_item.btn_choose.SetSelect(True)
                self._update_talent(talent_id)
                return

    def init_pnl_describe(self):
        pnl_describe = self.nd_content.pnl_content.pnl_describe
        pnl_describe.setVisible(False)

        @pnl_describe.btn_upgrade.unique_callback()
        def OnClick(btn, touch):
            if not global_data.player:
                return

            def cb():
                global_data.player.up_talent_level(self._current_select_talent_id)

            have_item_counts = global_data.player.get_item_num_by_no(SHOP_PAYMENT_PVE_COIN)
            cost_price = global_data.player.get_talent_cost(self._current_select_talent_id)
            if have_item_counts >= cost_price:
                cb()
            else:
                ui = global_data.ui_mgr.show_ui('PVEItemExchangeUI', 'logic.comsys.battle.pve.PVEMainUIWidgetUI')
                ui and ui.init_widget(cost_price, have_item_counts, cb=cb)

    def on_player_item_update_event(self):
        self.init_money_widget()

    def init_money_widget--- This code section failed: ---

 137       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  '_price_top_widget'
           6  POP_JUMP_IF_TRUE     64  'to 64'

 138       9  LOAD_GLOBAL           1  'PriceUIWidget'
          12  LOAD_GLOBAL           1  'PriceUIWidget'
          15  LOAD_FAST             0  'self'
          18  LOAD_ATTR             2  'panel'
          21  LOAD_ATTR             3  'list_money'
          24  LOAD_CONST            2  'pnl_title'
          27  LOAD_GLOBAL           4  'False'
          30  CALL_FUNCTION_513   513 
          33  LOAD_FAST             0  'self'
          36  STORE_ATTR            0  '_price_top_widget'

 139      39  LOAD_FAST             0  'self'
          42  LOAD_ATTR             0  '_price_top_widget'
          45  LOAD_ATTR             5  'show_money_types'
          48  LOAD_GLOBAL           6  'SHOP_PAYMENT_ITEM_PVE_KEY'
          51  LOAD_GLOBAL           7  'SHOP_PAYMENT_ITEM_PVE_COIN'
          54  BUILD_LIST_2          2 
          57  CALL_FUNCTION_1       1 
          60  POP_TOP          
          61  JUMP_FORWARD         13  'to 77'

 141      64  LOAD_FAST             0  'self'
          67  LOAD_ATTR             0  '_price_top_widget'
          70  LOAD_ATTR             8  '_on_player_info_update'
          73  CALL_FUNCTION_0       0 
          76  POP_TOP          
        77_0  COME_FROM                '61'

Parse error at or near `CALL_FUNCTION_513' instruction at offset 30

    def _show_talent_confirm_ui(self):
        from logic.comsys.battle.pve.PVEMainUIWidgetUI.PVETalentConfirmUI import PVETalentConfirmUI
        PVETalentConfirmUI(talent_id=self._current_select_talent_id)

    def _update_talent(self, talent_id):
        self._update_talent_item(talent_id)
        self._update_talent_data(talent_id)

    def _update_talent_item(self, talent_id):
        talent_item = self._talent_item_dict[talent_id]
        if talent_item and talent_item.isValid():
            init_talent_item(talent_item, talent_id)
            talent_level = global_data.player.get_talent_level_by_id(talent_id) if global_data.player else 0
            talent_conf = self._talent_conf.get(talent_id)
            max_level = talent_conf.get('max_level', 1)
            if talent_level == max_level:
                talent_item.PlayAnimation('loop_level_full')
            else:
                talent_item.StopAnimation('loop_level_full')

    def _update_talent_data(self, talent_id):
        talent_level = global_data.player.get_talent_level_by_id(talent_id) if global_data.player else 0
        talent_conf = self._talent_conf.get(talent_id)
        talend_effect_conf = self._talent_effect_conf.get(talent_id)
        pnl_describe = self.nd_content.pnl_content.pnl_describe
        pnl_describe.setVisible(True)
        btn_upgrade = pnl_describe.btn_upgrade
        pnl_describe.lab_name.SetString(get_text_by_id(talent_conf['name_id']))
        show_level = talent_level if talent_level > 0 else 1
        talent_text = get_attr_desc_text(talend_effect_conf.get('desc_id'), talend_effect_conf.get('desc_params'), show_level)
        pnl_describe.lab_describe.SetString(talent_text)
        pnl_describe.img_item.SetDisplayFrameByPath('', talent_conf.get('icon'))
        lab_level = pnl_describe.lab_level
        max_level = talent_conf.get('max_level', 1)
        if talent_level < max_level:
            pnl_describe.SetDisplayFrameByPath('', 'gui/ui_res_2/pve/talent/bar_pve_talent_describe_3.png')
            btn_upgrade.setVisible(True)
            lab_level.setVisible(False)
        else:
            pnl_describe.SetDisplayFrameByPath('', 'gui/ui_res_2/pve/talent/bar_pve_talent_describe_2.png')
            btn_upgrade.setVisible(False)
            lab_level.setVisible(True)
        if talent_level == max_level:
            self.panel.PlayAnimation('loop_level_full')
        else:
            self.panel.StopAnimation('loop_level_full')
        bar_title = pnl_describe.bar_title
        lab_level = bar_title.lab_level
        list_prog = lab_level.list_prog
        list_prog.DeleteAllSubItem()
        for level in range(max_level):
            item = list_prog.AddTemplateItem()
            item.EnableCustomState(True)
            if level < talent_level:
                if level == talent_level - 1:
                    self._play_anim(item)
                else:
                    item.SetSelect(True)
            else:
                item.SetSelect(False)

        cost_price = global_data.player.get_talent_cost(talent_id) if global_data.player else 0
        price_info = [{'original_price': cost_price,'goods_payment': SHOP_PAYMENT_ITEM_PVE_COIN,'discount_price': cost_price}]
        color = [
         '#SR', '#BC']
        splice_price(btn_upgrade.temp_price, price_info, color)

    def _play_anim(self, item):

        def delay_call(*args):
            if item and item.isValid():
                item.SetSelect(True)

        if self._is_first_init:
            delay_call()
        else:
            anim_time = item.GetAnimationMaxRunTime('level_up_tips')
            self.panel.DelayCallWithTag(anim_time, delay_call, self.LEVEL_UP_TAG)
            item.PlayAnimation('level_up_tips')
            self._is_first_init = True

    def refresh_pve_talent_event(self, talent_id):
        self._is_first_init = False
        self.panel.PlayAnimation('level_up')
        self._update_talent(talent_id)

    @staticmethod
    def check_red_point():
        return False

    def play_disappear_anim(self):
        if self._disappearing:
            return
        self._disappearing = True
        anim_time = self.panel.GetAnimationMaxRunTime('disappear')

        def delay_call(*args):
            self._disappearing = False
            self.close()

        self.panel.StopAnimation('disappear')
        self.panel.DelayCallWithTag(anim_time, delay_call, self.DELAY_CLOSE_TAG)
        self.panel.PlayAnimation('disappear')

    def on_finalize_panel(self):
        self.process_events(False)
        self._disappearing = None
        self._is_first_init = None
        self._talent_conf = None
        self._talent_effect_conf = None
        self._talent_id_list = None
        self._current_select_talent = None
        self._current_select_talent_id = None
        self._talent_item_dict = None
        if self._price_top_widget:
            self._price_top_widget.destroy()
            self._price_top_widget = None
        if self._frame_loader_template:
            self._frame_loader_template.destroy()
            self._frame_loader_template = None
        self.show_main_ui()
        super(PVETalentWidgetUI, self).on_finalize_panel()
        return