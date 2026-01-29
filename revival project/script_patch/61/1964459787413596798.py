# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/role_profile/BondWidget.py
from __future__ import absolute_import
import six
import time
import common.utilities
from common.uisys.BaseUIWidget import BaseUIWidget
from common.cfg import confmgr
from common.utils import ui_utils
from logic.gutils import bond_utils
from logic.gutils import template_utils
from logic.comsys.effect import ui_effect
from logic.gcommon.cdata import bond_config
from logic.gcommon.cdata import bond_gift_config
from logic.gcommon.item import lobby_item_type
from logic.entities.avatarmembers.impBond import impBond
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no, get_lobby_item_name, get_lobby_item_desc
from logic.gutils import item_utils, role_utils

class BondWidget(BaseUIWidget):

    def __init__(self, parent, panel):
        self.global_events = {'bond_update_role_level': self.on_bond_udpate,
           'bond_role_reward': self.on_bond_reward,
           'bond_role_gift': self.on_bond_gift_update,
           'refresh_item_red_point': self.on_refresh_item_red_point,
           'on_check_bond_exchange_driver_gift': self.on_refresh_item_red_point,
           'player_item_update_event_with_id': self.on_buy_good_success,
           'on_lobby_bag_item_changed_event': self.on_bag_item_changed,
           'ret_bond_keepsake_oper': self.on_ret_bond_keepsake_oper,
           'ret_bond_replace_driver_gift': self.on_bond_driver_gift_change,
           'ret_bond_refresh_driver_gifts': self.on_bond_driver_gift_change
           }
        super(BondWidget, self).__init__(parent, panel)
        self.role_id = 0
        self._ui_role_id = 0
        self.selected_item = None
        self.selected_item_id = None
        self.dont_show_item_desc_count = 0
        self._items_refresh_cb = {}
        self._items_click_cb = {}
        self._pnl_bond_exp_up = None
        self._bond_exp_ani_finished = True
        self._is_gift_opened = False

        @self.panel.unique_callback()
        def OnClick(layer, touch, *args):
            self.on_click_empty()

        @self.panel.btn_tips.unique_callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(870020, 870021)

        @self.panel.btn_level.unique_callback()
        def OnClick(btn, touch):
            if self.role_id:
                self.open_bond_reward_ui()

        @self.panel.btn_gift.unique_callback()
        def OnClick(btn, touch):
            self.show_gift_panel(True)

        @self.panel.btn_close.unique_callback()
        def OnClick(btn, touch):
            self.show_gift_panel(False)

        self.show_gift_panel(False)
        return

    def show_panel(self, flag):
        self.panel.setVisible(flag)
        self.parent.enable_bond_cam(flag)
        if flag:
            self.show_guide()

    def on_hide(self):
        self.parent.enable_bond_cam(False)

    def destroy(self):
        super(BondWidget, self).destroy()

    def on_focus(self, flag):
        if not flag:
            self.on_click_empty()

    def set_role_id(self, role_id):
        self.role_id = role_id

    def show_guide(self):
        if not bond_utils.need_bond_guided():
            return
        else:
            if global_data.player.get_item_by_no(self.role_id) is None:
                return
            lobby = global_data.ui_mgr.get_ui('LobbyUI')
            if not lobby:
                return
            bond_utils.set_bond_guided()
            lobby.show_bond_guide()
            global_data.ui_mgr.show_ui('GuideBondUI', 'logic.comsys.role_profile')
            return

    def show_gift_panel(self, flag):
        self._is_gift_opened = flag
        self.panel.nd_gift.setVisible(flag)
        self.panel.btn_gift.setVisible(not flag)
        self.panel.btn_close.setVisible(flag)
        self.panel.btn_close.setRotation(0 if flag else 180)
        self.panel.btn_gift.setRotation(0 if flag else 180)
        has_role = global_data.player.get_item_by_no(self.role_id) is not None
        if flag and has_role:
            if self.selected_item_id and self.selected_item_id > 0:
                self.select_item(self.selected_item_id)
        else:
            self.show_preview_exp(0, visible=False)
        return

    def refresh_all_content(self):
        if self._ui_role_id == self.role_id:
            return
        else:
            self._ui_role_id = self.role_id
            self.selected_item = None
            self.selected_item_id = None
            item_data = global_data.player.get_item_by_no(self.role_id)
            self.on_click_empty()
            self.show_exp()
            if item_data:
                self.show_items()
                self.show_empty_detail(False)
            else:
                self.show_empty_detail(True)
            self.show_gift_panel(self._is_gift_opened)
            self.show_skills()
            return

    def on_click_empty(self):
        pass

    def on_dress_change(self, new_skin_id):
        pass

    def on_bond_udpate(self, role_id, event_info):
        if self.role_id == role_id:
            self.show_bond_exp_up(event_info)
            self.show_skills()
            self.show_preview_exp(0, visible=False)

    def on_bond_reward(self, role_id):
        if self.role_id == role_id:
            self.refresh_bond_redpoint()
            self.show_skills()

    def on_bond_gift_update(self, role_id):
        if self.role_id == role_id:
            self.show_skills()

    def on_buy_good_success(self, item_no):
        self.refresh_items()

    def on_bag_item_changed(self):
        self.refresh_items()

    def on_ret_bond_keepsake_oper(self, oper_type, role_id, role_keepsakes):
        role_id = int(role_id)
        if self.role_id == role_id:
            self.refresh_bond_redpoint()
            self.show_skills()

    def on_bond_driver_gift_change(self, *args):
        self.refresh_bond_redpoint()
        self.show_skills()

    def on_refresh_item_red_point(self):
        self.show_skills()

    def show_bond_exp_up(self, event_info):
        from logic.gcommon.const import SEX_FEMALE
        if not self._bond_exp_ani_finished:
            return
        if not self._pnl_bond_exp_up:
            item_conf = global_data.uisystem.load_template('role_profile/i_vx_gift')
            self._pnl_bond_exp_up = global_data.uisystem.create_item(item_conf, parent=self.parent.panel)
        role_sex = confmgr.get('role_info', 'RoleInfo', 'Content', str(self.role_id), 'sex')
        anim_name = 'show'
        anim_level_up = 'level_up'
        if role_sex != SEX_FEMALE:
            anim_name = 'show2'
            anim_level_up = 'level_up2'
        max_time = self._pnl_bond_exp_up.GetAnimationMaxRunTime(anim_name)
        self._pnl_bond_exp_up.PlayAnimation(anim_name)
        if global_data.sound_mgr:
            global_data.sound_mgr.play_ui_sound('ui_fetters_send_gifts')

        def first_cb():
            add_exp = bond_config.get_added_strength(event_info[impBond.BOND_LEVEL][0], event_info[impBond.BOND_STRENGTH][0], event_info[impBond.BOND_LEVEL][1], event_info[impBond.BOND_STRENGTH][1])
            dialog_id = bond_utils.get_gift_dialog_id(self.role_id, bond_exp=add_exp)
            if dialog_id:
                global_data.emgr.role_show_chat.emit(self.role_id, dialog_id)

        self._pnl_bond_exp_up.DelayCall(14.0 / 30, first_cb)

        def second_cb():
            self.panel.PlayAnimation(anim_level_up)

        self._pnl_bond_exp_up.DelayCall(18.0 / 30, second_cb)

        def third_cb():
            self.show_exp(event_info=event_info)

        self._pnl_bond_exp_up.DelayCall(25.0 / 30, third_cb)

        def forth_cb():
            self._bond_exp_ani_finished = True

        self._pnl_bond_exp_up.DelayCall(max_time, forth_cb)
        self._bond_exp_ani_finished = False

    def show_percent_action(self, pg_bar, event_info):
        unit_time = 1.0
        _cur_exp = event_info[impBond.BOND_STRENGTH][0]
        _, cur_nxt_exp = bond_config.get_nxt_bond_level_strength(event_info[impBond.BOND_LEVEL][0])
        cur_percent = common.utilities.safe_percent(_cur_exp, cur_nxt_exp)
        new_lv = event_info[impBond.BOND_LEVEL][1]
        _nxt_exp = event_info[impBond.BOND_STRENGTH][1]
        _, nxt_nxt_exp = bond_config.get_nxt_bond_level_strength(new_lv)
        nxt_percent = common.utilities.safe_percent(_nxt_exp, nxt_nxt_exp)
        is_max_level = new_lv >= bond_config.get_bond_max_level()

        def reset():
            level, cur_exp = global_data.player.get_bond_data(self.role_id)
            _, nxt_exp = bond_config.get_nxt_bond_level_strength(event_info[impBond.BOND_LEVEL][0])
            self.panel.lab_level.SetString('LV.{}'.format(level))
            self.panel.lab_num.SetString('{}/{}'.format(cur_exp, nxt_exp))

        def finish():
            if self.panel.nd_give.isVisible() and self.selected_item_id:
                self.show_give_panel(self.selected_item_id)

        if nxt_percent > cur_percent:
            pg_bar.SetPercent(nxt_percent, time=(nxt_percent - cur_percent) / 100.0 * unit_time, end_cb=finish)
            reset()
        else:

            def end_cb():
                reset()
                pg_bar.setPercent(0.0)
                if not is_max_level:
                    pg_bar.SetPercent(nxt_percent, time=(nxt_percent - 0.0) / 100.0 * unit_time, end_cb=finish)
                else:
                    pg_bar.SetPercent(100, time=0, end_cb=finish)

            pg_bar.SetPercent(100.0, time=(100.0 - cur_percent) / 100.0 * unit_time, end_cb=end_cb)

    def show_exp(self, event_info=None):
        if not global_data.player:
            return
        level, cur_exp = global_data.player.get_bond_data(self.role_id)
        is_max_lv = False
        if level >= bond_config.get_bond_max_level():
            is_max_lv = True
        self.panel.lab_top.setVisible(is_max_lv)
        self.panel.lab_num.setVisible(not is_max_lv)
        _, nxt_exp = bond_config.get_nxt_bond_level_strength(level)
        self.panel.lab_num.SetString('{}/{}'.format(cur_exp, nxt_exp))
        if not is_max_lv:
            update_percent = common.utilities.safe_percent(cur_exp, nxt_exp) if 1 else 100
            if event_info:
                self.show_percent_action(self.panel.progress_exp, event_info)
            else:
                self.panel.progress_exp.SetPercent(update_percent)
            global_data.player.get_item_by_no(self.role_id) or self.panel.lab_level.SetString(870022)
        else:
            self.panel.lab_level.SetString('LV.{}'.format(level))
        self.refresh_bond_redpoint()

    def show_preview_exp(self, add_exp, visible=True):
        self.panel.progress_preview.setVisible(visible)
        level, cur_exp = global_data.player.get_bond_data(self.role_id)
        new_lv, new_exp = bond_config.get_new_bond_level_strength(level, cur_exp, add_exp)
        nxt_level, nxt_exp = bond_config.get_nxt_bond_level_strength(new_lv)
        if new_lv >= bond_config.get_bond_max_level():
            new_exp = bond_config.get_cur_bond_level_strength(nxt_level)
            nxt_exp = bond_config.get_cur_bond_level_strength(nxt_level)
        if level != new_lv:
            str_exp = '#SY{}#n/#SY{}#n'.format(new_exp, nxt_exp)
        elif cur_exp != new_exp:
            str_exp = '#SY{}#n/{}'.format(new_exp, nxt_exp)
        else:
            str_exp = '{}/{}'.format(new_exp, nxt_exp)
        self.panel.lab_num.SetString(str_exp)
        self.panel.progress_preview.setVisible(level < bond_config.get_bond_max_level())
        self.panel.progress_preview.SetPercent(common.utilities.safe_percent(new_exp, nxt_exp))
        preview_parent = self.panel.progress_preview.GetParent()
        lv_clr = '#SW'
        if level != new_lv:
            lv_clr = '#SY'
            preview_parent.ReorderChild(self.panel.progress_preview, 2)
        else:
            preview_parent.ReorderChild(self.panel.progress_preview, 0)
        if not global_data.player.get_item_by_no(self.role_id):
            self.panel.lab_level.SetString(870022)
        else:
            self.panel.lab_level.SetString('#SWLV.#n{}{}#n'.format(lv_clr, new_lv))

    def refresh_items(self):
        if not self._items_refresh_cb:
            return
        for item_id, cb in six.iteritems(self._items_refresh_cb):
            cb()

    def show_items(self):
        from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_BOND
        self.panel.nd_empty.setVisible(False)
        item_list = bond_utils.get_ordered_bond_items(self.role_id)
        self._items_refresh_cb = {}
        self._items_click_cb = {}
        tpl_path = self.panel.list_gift.GetTemplatePath()
        self.panel.list_gift.SetInitCount(len(item_list))
        for i, item_info in enumerate(item_list):
            one_item = self.panel.list_gift.GetItem(i)
            self.init_one_item(tpl_path, one_item, item_info)
            if i == 0:
                self.selected_item_id = item_info['itemno']

        self.show_give_panel(None)
        return

    def locate_selected_item(self):
        if not self.selected_item_id:
            return
        item_list = bond_utils.get_ordered_bond_items(self.role_id)
        for i, item_info in enumerate(item_list):
            if self.selected_item_id == item_info['itemno']:
                self.panel.list_gift.LocatePosByItem(i, duration=1)
                return

    def _select_item(self, item, item_id):
        if self.selected_item and self.selected_item.isValid():
            self.selected_item.temp_item.btn_choose.SetSelect(False)
        item.temp_item.btn_choose.SetSelect(True)
        self.selected_item = item
        self.selected_item_id = item_id

    def set_select_item_id(self, item_id):
        self.selected_item_id = item_id
        self.dont_show_item_desc_count = 1

    def select_item(self, item_id):
        if item_id not in self._items_click_cb:
            return
        self._items_click_cb[item_id]()

    def refresh_one_item(self, item_id):
        if item_id in self._items_refresh_cb:
            self._items_refresh_cb[item_id]()

    def _refresh_one_item(self, item, item_id):
        item_tpl = item.temp_item
        own_num = global_data.player.get_item_num_by_no(item_id)
        is_gray = own_num <= 0
        ui_effect.set_gray(item_tpl.item, is_gray)
        if item_id == self.selected_item_id:
            if own_num > 0:
                self.show_give_panel(item_id)
            else:
                self.show_access_panel(item_id)
        item_tpl.lab_quantity.setVisible(True)
        item_tpl.lab_quantity.SetString(str(own_num))

    def init_one_item(self, tpl_path, item, item_info):
        item_tpl = item.temp_item
        item_id = item_info['itemno']
        template_utils.init_tempate_mall_i_item(item_tpl, item_id, templatePath=item_tpl.GetTemplatePath())
        self._refresh_one_item(item, item_id)
        self._items_refresh_cb[item_id] = lambda : self._refresh_one_item(item, item_id)
        effect_add = item_info['effect_add']
        item.img_up.setVisible(effect_add > 1)
        if effect_add > 1:
            item.PlayAnimation('show')
        if item_id == self.selected_item_id:
            item_tpl.btn_choose.SetSelect(True)
            self.selected_item = item
        else:
            item_tpl.btn_choose.SetSelect(False)

        def OnClick(*args):
            self._select_item(item, item_id)
            self.show_common_detail(item_id)
            self.show_gift_item_desc(item_id)
            self.show_give_panel(item_id)
            if global_data.player.get_item_num_by_no(item_id) <= 0:
                self.show_access_panel(item_id)
            else:
                self.show_give_panel(item_id)

        item.OnClick = OnClick
        self._items_click_cb[item_id] = OnClick

    def show_give_panel(self, item_id):
        self.panel.nd_control.setVisible(True)
        self.panel.nd_obtain.setVisible(False)
        nd_give = self.panel.nd_give
        nd_control = self.panel.nd_control
        slider = nd_control.nd_slider.slider
        if not item_id:
            nd_give.lab_name.SetString('')
            nd_give.lab_up.SetString('')
            slider.setPercent(0)
            nd_control.nd_slider.name.SetString('')
            nd_control.lab_tips.SetString('')
            nd_control.nd_slider.minute.SetEnable(False)
            nd_control.nd_slider.plus.SetEnable(False)
            nd_give.btn_give.SetEnable(False)
            nd_give.btn_obtain.SetEnable(False)
            return
        limit = global_data.player.get_item_num_by_no(item_id)
        min_num = 0 if limit > 0 else 0
        unit_num = bond_config.get_bond_gain_effect(item_id, self.role_id)
        count = [1 if limit > 0 else 0]

        def set_count--- This code section failed: ---

 486       0  LOAD_FAST             0  'new_count'
           3  LOAD_DEREF            0  'count'
           6  LOAD_CONST            1  ''
           9  BINARY_SUBSCR    
          10  COMPARE_OP            2  '=='
          13  POP_JUMP_IF_FALSE    27  'to 27'
          16  LOAD_FAST             1  'force'
          19  UNARY_NOT        
        20_0  COME_FROM                '13'
          20  POP_JUMP_IF_FALSE    27  'to 27'

 487      23  LOAD_CONST            0  ''
          26  RETURN_END_IF    
        27_0  COME_FROM                '20'

 488      27  LOAD_GLOBAL           0  'max'
          30  LOAD_DEREF            1  'min_num'
          33  LOAD_GLOBAL           1  'min'
          36  LOAD_FAST             0  'new_count'
          39  LOAD_DEREF            2  'limit'
          42  CALL_FUNCTION_2       2 
          45  CALL_FUNCTION_2       2 
          48  STORE_FAST            0  'new_count'

 490      51  LOAD_FAST             0  'new_count'
          54  LOAD_DEREF            0  'count'
          57  LOAD_CONST            1  ''
          60  STORE_SUBSCR     

 491      61  LOAD_DEREF            3  'unit_num'
          64  LOAD_FAST             0  'new_count'
          67  BINARY_MULTIPLY  
          68  STORE_FAST            2  'add_num'

 492      71  LOAD_DEREF            4  'nd_control'
          74  LOAD_ATTR             2  'lab_tips'
          77  LOAD_ATTR             3  'setVisible'
          80  LOAD_DEREF            2  'limit'
          83  LOAD_CONST            1  ''
          86  COMPARE_OP            4  '>'
          89  CALL_FUNCTION_1       1 
          92  POP_TOP          

 493      93  LOAD_DEREF            4  'nd_control'
          96  LOAD_ATTR             2  'lab_tips'
          99  LOAD_ATTR             4  'SetString'
         102  LOAD_GLOBAL           5  'get_text_by_id'
         105  LOAD_CONST            2  870041
         108  LOAD_CONST            3  'args'
         111  LOAD_FAST             2  'add_num'
         114  BUILD_LIST_1          1 
         117  CALL_FUNCTION_257   257 
         120  CALL_FUNCTION_1       1 
         123  POP_TOP          

 494     124  LOAD_DEREF            4  'nd_control'
         127  LOAD_ATTR             6  'nd_slider'
         130  LOAD_ATTR             7  'name'
         133  LOAD_ATTR             4  'SetString'
         136  LOAD_CONST            4  '#SY{}#n/{}'
         139  LOAD_ATTR             8  'format'
         142  LOAD_FAST             0  'new_count'
         145  LOAD_DEREF            2  'limit'
         148  CALL_FUNCTION_2       2 
         151  CALL_FUNCTION_1       1 
         154  POP_TOP          

 496     155  LOAD_DEREF            5  'slider'
         158  LOAD_ATTR             3  'setVisible'
         161  LOAD_DEREF            2  'limit'
         164  LOAD_CONST            1  ''
         167  COMPARE_OP            4  '>'
         170  CALL_FUNCTION_1       1 
         173  POP_TOP          

 497     174  LOAD_DEREF            5  'slider'
         177  LOAD_ATTR             9  'setPercent'
         180  LOAD_GLOBAL          10  'common'
         183  LOAD_ATTR            11  'utilities'
         186  LOAD_ATTR            12  'safe_percent'
         189  LOAD_FAST             0  'new_count'
         192  LOAD_DEREF            2  'limit'
         195  CALL_FUNCTION_2       2 
         198  CALL_FUNCTION_1       1 
         201  POP_TOP          

 499     202  LOAD_DEREF            4  'nd_control'
         205  LOAD_ATTR             6  'nd_slider'
         208  LOAD_ATTR            13  'minute'
         211  LOAD_ATTR            14  'SetEnable'
         214  LOAD_FAST             0  'new_count'
         217  LOAD_DEREF            1  'min_num'
         220  COMPARE_OP            4  '>'
         223  CALL_FUNCTION_1       1 
         226  POP_TOP          

 500     227  LOAD_DEREF            4  'nd_control'
         230  LOAD_ATTR             6  'nd_slider'
         233  LOAD_ATTR            15  'plus'
         236  LOAD_ATTR            14  'SetEnable'
         239  LOAD_FAST             0  'new_count'
         242  LOAD_DEREF            2  'limit'
         245  COMPARE_OP            0  '<'
         248  CALL_FUNCTION_1       1 
         251  POP_TOP          

 501     252  LOAD_DEREF            6  'nd_give'
         255  LOAD_ATTR            16  'btn_give'
         258  LOAD_ATTR            14  'SetEnable'
         261  LOAD_ATTR             1  'min'
         264  COMPARE_OP            4  '>'
         267  CALL_FUNCTION_1       1 
         270  POP_TOP          

 503     271  LOAD_DEREF            7  'self'
         274  LOAD_ATTR            17  'show_preview_exp'
         277  LOAD_FAST             2  'add_num'
         280  CALL_FUNCTION_1       1 
         283  POP_TOP          

Parse error at or near `COMPARE_OP' instruction at offset 264

        @slider.callback()
        def OnPercentageChanged(*args):
            percent = slider.getPercent()
            set_count(int(limit * percent / 100.0))

        set_count(count[0], force=True)

        @nd_control.nd_slider.minute.unique_callback()
        def OnClick(layer, touch, *args):
            set_count(count[0] - 1, force=True)

        @nd_control.nd_slider.plus.unique_callback()
        def OnClick(layer, touch, *args):
            set_count(count[0] + 1, force=True)

        @nd_give.btn_give.unique_callback()
        def OnClick(layer, touch, *args):
            level, cur_exp = global_data.player.get_bond_data(self.role_id)
            if level >= bond_config.get_bond_max_level():
                global_data.game_mgr.show_tip(get_text_by_id(870056))
                return
            if count[0] > 0:
                item = global_data.player.get_item_by_no(item_id)
                if not item:
                    return
                use_item_func = lambda : global_data.player.use_item(item.get_id(), count[0], {'role_id': self.role_id})
                role_id = bond_config.get_unlock_role_id_of_bond_item(item_id)
                if role_id and role_id != self.role_id and not global_data.player.get_item_by_no(role_id):
                    role_name_id = confmgr.get('role_info', 'RoleProfile', 'Content', str(role_id), 'role_name')
                    role_name = get_text_by_id(role_name_id)
                    SecondConfirmDlg2().confirm(content=get_text_by_id(870060, {'name': role_name}), confirm_callback=use_item_func)
                else:
                    use_item_func()

    def show_common_detail(self, item_id):
        nd_give = self.panel.nd_give
        nd_give.lab_name.SetString(item_utils.get_lobby_item_name(item_id))
        unit_num = bond_config.get_bond_gain_effect(item_id, self.role_id)
        nd_give.lab_up.SetString('+{}'.format(unit_num))
        can_jump = item_utils.can_jump_to_ui(item_id)
        jump_txt = item_utils.get_item_access(item_id)
        nd_give.lab_way.SetString(jump_txt or '')
        nd_give.lab_way.setVisible(not can_jump)
        nd_give.btn_obtain.SetEnable(can_jump)

        @nd_give.btn_obtain.unique_callback()
        def OnClick(layer, touch, *args):
            item_utils.jump_to_ui(item_id)

    def show_gift_item_desc(self, item_id):
        self.dont_show_item_desc_count -= 1
        if self.dont_show_item_desc_count >= 0:
            return
        wpos = self.panel.nd_gift.ConvertToWorldSpacePercentage(0, 50)
        descIDs = confmgr.get('lobby_item', str(item_id), 'desc_id', default='')
        tips = ''.join(get_text_by_id(descIDs[0], [bond_config.get_bond_gain_effect(item_id, self.role_id)]))
        effect_desc = bond_config.get_bond_effect_desc(item_id, self.role_id)
        if effect_desc > 1:
            role_name_id = confmgr.get('role_info', 'RoleProfile', 'Content', str(self.role_id), 'role_name')
            role_name = get_text_by_id(role_name_id)
            tips += '\n' + get_text_by_id(870059, {'name': role_name})
        extra_info = {'show_desc': tips,'btn_text': 2222}
        global_data.emgr.show_item_desc_ui_event.emit(item_id, wpos, extra_info=extra_info)

    def show_empty_detail(self, flag):
        self.panel.img_line.setVisible(not flag)
        self.panel.nd_give.setVisible(not flag)
        self.panel.list_gift.setVisible(not flag)
        self.panel.nd_empty.setVisible(flag)

    def show_access_panel(self, item_id):
        self.panel.nd_control.setVisible(False)
        self.panel.nd_obtain.setVisible(True)
        self.show_preview_exp(0, visible=False)

    def refresh_bond_redpoint(self):
        is_permanent = global_data.player.has_permanent_role(self.role_id)
        if not is_permanent:
            self.panel.img_new.setVisible(False)
            return
        can_get = bond_utils.can_get_gift_reward(self.role_id)
        self.panel.img_new.setVisible(can_get)
        if can_get:
            self.panel.PlayAnimation('reward_tips')
        else:
            self.panel.StopAnimation('reward_tips')

    def open_bond_reward_ui(self):
        from . import RoleBondRewardUI
        RoleBondRewardUI.RoleBondRewardUI(None, self.role_id)
        return

    def show_skills(self):
        nd_skill = self.panel.nd_skill
        template_utils.init_bond_skills(nd_skill, self.role_id)