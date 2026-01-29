# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/role_profile/BondSkillLevelUp.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
from six.moves import range
from . import RoleBondRewardUI
from . import BondSkillChange
from . import BondSkillUpgradeConfirm
import common.utilities
from common.cfg import confmgr
from common.const import uiconst
import logic.gcommon.const as gconst
from logic.comsys.effect import ui_effect
from logic.gcommon.item import item_const
from logic.gcommon.cdata import bond_config
from logic.gcommon.cdata import bond_gift_config
from logic.gcommon.item import lobby_item_type
from logic.gcommon.common_utils.local_text import get_text_by_id
import logic.gcommon.time_utility as tutil
from logic.gutils import bond_utils
from logic.gutils import mall_utils
from logic.gutils import role_utils
from logic.gutils import template_utils
from logic.gutils import lobby_model_display_utils
from logic.comsys.mall_ui.PriceUIWidget import PriceUIWidget
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no, get_lobby_item_name, get_lobby_item_desc, update_item_status
from common.uisys.basepanel import BasePanel

def get_last_id--- This code section failed: ---

  31       0  LOAD_FAST             0  'seq_list'
           3  LOAD_ATTR             0  'index'
           6  LOAD_FAST             1  'cur_id'
           9  CALL_FUNCTION_1       1 
          12  STORE_FAST            2  'cur_index'

  32      15  LOAD_FAST             2  'cur_index'
          18  LOAD_CONST            1  ''
          21  COMPARE_OP            2  '=='
          24  POP_JUMP_IF_FALSE    34  'to 34'
          27  POP_JUMP_IF_FALSE     2  'to 2'
          30  BINARY_SUBSCR    
          31  JUMP_FORWARD         11  'to 45'
          34  LOAD_FAST             0  'seq_list'
          37  LOAD_FAST             2  'cur_index'
          40  LOAD_CONST            3  1
          43  BINARY_SUBTRACT  
          44  BINARY_SUBSCR    
        45_0  COME_FROM                '31'
          45  STORE_FAST            3  'new_id'

  33      48  LOAD_FAST             3  'new_id'
          51  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `POP_JUMP_IF_FALSE' instruction at offset 27


def get_next_id--- This code section failed: ---

  36       0  LOAD_FAST             0  'seq_list'
           3  LOAD_ATTR             0  'index'
           6  LOAD_FAST             1  'cur_id'
           9  CALL_FUNCTION_1       1 
          12  STORE_FAST            2  'cur_index'

  37      15  LOAD_FAST             2  'cur_index'
          18  LOAD_GLOBAL           1  'len'
          21  LOAD_FAST             0  'seq_list'
          24  CALL_FUNCTION_1       1 
          27  LOAD_CONST            1  1
          30  BINARY_SUBTRACT  
          31  COMPARE_OP            2  '=='
          34  POP_JUMP_IF_FALSE    44  'to 44'
          37  POP_JUMP_IF_FALSE     2  'to 2'
          40  BINARY_SUBSCR    
          41  JUMP_FORWARD         11  'to 55'
          44  LOAD_FAST             0  'seq_list'
          47  LOAD_FAST             2  'cur_index'
          50  LOAD_CONST            1  1
          53  BINARY_ADD       
          54  BINARY_SUBSCR    
        55_0  COME_FROM                '41'
          55  STORE_FAST            3  'new_id'

  38      58  LOAD_FAST             3  'new_id'
          61  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `POP_JUMP_IF_FALSE' instruction at offset 37


ROLE_DEFAULT_POS = ('50%4', '50%-228')

class BondSkillLevelUp(BasePanel):
    PANEL_CONFIG_NAME = 'role_profile/skill_level_up'
    TEMPLATE_NODE_NAME = 'temp_window_small'
    DLG_ZORDER = uiconst.NORMAL_LAYER_ZORDER_2
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    GLOBAL_EVENT = {'bond_role_gift': 'on_bond_gift_update',
       'ret_bond_keepsake_oper': 'on_ret_bond_keepsake_oper',
       'ret_bond_replace_driver_gift': 'init_widget',
       'ret_bond_refresh_driver_gifts': 'init_widget',
       'refresh_item_red_point': 'refresh_red_point',
       'on_check_bond_exchange_driver_gift': 'refresh_red_point',
       'player_money_info_update_event': 'init_widget',
       'buy_good_success': 'init_widget'
       }
    UI_ACTION_EVENT = {'btn_close.OnClick': 'close',
       'temp_btn_get.btn_common.OnClick': 'on_get',
       'temp_btn_change.btn_common.OnClick': 'on_change_keepsake',
       'btn_change.OnClick': 'on_change_driver_gift',
       'btn_last.OnClick': 'on_click_btn_last',
       'btn_next.OnClick': 'on_click_btn_next',
       'btn_describe.OnClick': 'on_click_btn_describe'
       }

    def on_init_panel(self, role_id, select_index=-1):
        super(BondSkillLevelUp, self).on_init_panel()
        self.role_seq = []
        vaild_seq = lobby_model_display_utils.get_role_seq_show()
        for str_role_id in vaild_seq:
            role_goods_id = confmgr.get('role_info', 'RoleInfo', 'Content', str_role_id, 'goods_id')
            if role_goods_id:
                self.role_seq.append(role_goods_id)

        self.init_role_id = role_id
        self.role_id = role_id
        self._select_index = select_index
        self._select_keepsake_index = -1
        self._gift_infos = []
        self._last_select_keepsake_index = -1
        self._keepsake_items = []
        self._show_level_up_anim = False
        self.price_top_widget = None
        self.button_ui_price_nd = None
        self.sel_gift_type = None
        self.can_change = False
        self.init_widget()
        self.refresh_red_point()
        self.refresh_page_tips()
        return

    def on_finalize_panel(self):
        if self.button_ui_price_nd and self.button_ui_price_nd.isValid():
            self.button_ui_price_nd.setVisible(True)
        self.button_ui_price_nd = None
        if self.price_top_widget:
            self.price_top_widget.destroy()
        if self.init_role_id != self.role_id:
            global_data.emgr.role_id_chagne.emit(self.role_id)
        return

    def set_buttom_ui_price_nd(self, nd):
        self.button_ui_price_nd = nd
        if self.button_ui_price_nd.isValid():
            self.button_ui_price_nd.setVisible(False)

    def on_bond_gift_update(self, role_id):
        if self.role_id == role_id:
            self._show_level_up_anim = True
            self.show_skills()

    def on_ret_bond_keepsake_oper(self, oper_type, role_id, role_keepsakes):
        if self.role_id == role_id:
            self.show_skills()
            self.refresh_keepsakes()

    def on_click_btn_last(self, *args):
        new_role_id = get_last_id(self.role_seq, str(self.role_id))
        self.refresh_pages(new_role_id)

    def on_click_btn_next(self, *args):
        new_role_id = get_next_id(self.role_seq, str(self.role_id))
        self.refresh_pages(new_role_id)

    def on_click_btn_describe(self, *args):
        from cocosui import cc
        dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
        dlg.set_show_rule(get_text_by_id(875271), get_text_by_id(875272))
        x, y = self.panel.btn_describe.GetPosition()
        wpos = self.panel.btn_describe.GetParent().ConvertToWorldSpace(x, y)
        dlg.panel.nd_game_describe.setAnchorPoint(cc.Vec2(1.0, 1.0))
        template_utils.set_node_position_in_screen(dlg.panel.nd_game_describe, dlg.panel, wpos)

    def refresh_pages(self, new_role_id):
        self.role_id = int(new_role_id)
        self.init_widget()
        self.refresh_red_point()
        self.refresh_page_tips()

    def refresh_page_tips(self):
        new_role_id = str(self.role_id)
        last_id = get_last_id(self.role_seq, new_role_id)
        next_id = get_next_id(self.role_seq, new_role_id)
        img_role = confmgr.get('role_info', 'RoleInfo', 'Content', last_id, 'icon')
        self.panel.img_last.SetDisplayFrameByPath('', img_role)
        img_role = confmgr.get('role_info', 'RoleInfo', 'Content', next_id, 'icon')
        self.panel.img_next.SetDisplayFrameByPath('', img_role)

    def init_widget--- This code section failed: ---

 166       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  'show_skills'
           6  CALL_FUNCTION_0       0 
           9  POP_TOP          

 169      10  LOAD_FAST             0  'self'
          13  LOAD_ATTR             1  'price_top_widget'
          16  POP_JUMP_IF_FALSE    35  'to 35'

 170      19  LOAD_FAST             0  'self'
          22  LOAD_ATTR             1  'price_top_widget'
          25  LOAD_ATTR             2  'destroy'
          28  CALL_FUNCTION_0       0 
          31  POP_TOP          
          32  JUMP_FORWARD          0  'to 35'
        35_0  COME_FROM                '32'

 171      35  LOAD_GLOBAL           3  'PriceUIWidget'
          38  LOAD_GLOBAL           1  'price_top_widget'
          41  LOAD_FAST             0  'self'
          44  LOAD_ATTR             4  'panel'
          47  LOAD_ATTR             5  'list_price'
          50  LOAD_CONST            2  'pnl_title'
          53  LOAD_GLOBAL           6  'False'
          56  CALL_FUNCTION_513   513 
          59  LOAD_FAST             0  'self'
          62  STORE_ATTR            1  'price_top_widget'

 172      65  LOAD_FAST             0  'self'
          68  LOAD_ATTR             1  'price_top_widget'
          71  LOAD_ATTR             7  'show_money_types'
          74  LOAD_CONST            3  '%d_%d'
          77  LOAD_GLOBAL           8  'gconst'
          80  LOAD_ATTR             9  'SHOP_PAYMENT_ITEM'
          83  LOAD_GLOBAL           8  'gconst'
          86  LOAD_ATTR            10  'SHOP_PAYMENT_BOND_SKILL_BOOK'
          89  BUILD_TUPLE_2         2 
          92  BINARY_MODULO    
          93  BUILD_LIST_1          1 
          96  CALL_FUNCTION_1       1 
          99  POP_TOP          

Parse error at or near `CALL_FUNCTION_513' instruction at offset 56

    def refresh_red_point(self):
        self.show_skills(refresh=True)
        self.show_keepsakes(self._select_keepsake_index, refresh=True)

    def show_skills(self, refresh=False):
        from logic.gutils import dress_utils
        skin_id = dress_utils.get_role_dress_clothing_id(self.role_id)
        if not skin_id:
            default_skin = confmgr.get('role_info', 'RoleInfo', 'Content', str(self.role_id), 'default_skin')
            skin_id = default_skin[0]
        img_role = confmgr.get('role_info', 'RoleSkin', 'Content', str(skin_id), 'img_role')
        self.panel.img_role.SetDisplayFrameByPath('', img_role)
        special_pos_conf = confmgr.get('ui_display_conf', 'RoleSkinPicture', 'Content', default={})
        special_pos = special_pos_conf.get(str(skin_id), {})
        if special_pos and special_pos.get('BondLevelUpPic'):
            self.panel.img_role.SetPosition(*special_pos.get('BondLevelUpPic'))
        else:
            self.panel.img_role.SetPosition(*ROLE_DEFAULT_POS)
        bond_level, cur_exp = global_data.player.get_bond_data(self.role_id)
        has_role = True if global_data.player.get_item_by_no(self.role_id) else False
        gift_role_id = self.role_id
        if role_utils.is_crossover_role(self.role_id):
            gift_role_id = role_utils.get_crossover_role_id(self.role_id)
        gift_infos = bond_gift_config.get_role_bond_gift_info(str(gift_role_id), bond_config.get_bond_max_level())
        self._gift_infos = gift_infos

        def set_callback(index):

            def callback(*args):
                self.select_index(index)

            return callback

        rp_mgr = global_data.lobby_red_point_data
        for gift_info in gift_infos:
            base_gift_id = gift_info['gift_id']
            unlock_level = gift_info['level']
            gift_type = bond_utils.get_gift_type(base_gift_id)
            index = bond_utils.GIFT_TYPE_TO_INDEX.get(gift_type, 3)
            tpl_name = 'nd_skill_{}'.format(index)
            skill_tpl = getattr(self.panel, tpl_name)
            if not skill_tpl:
                return
            equipped_gift_id, lv = bond_utils.get_gift_id_level(self.role_id, gift_type)
            if equipped_gift_id <= 0:
                equipped_gift_id = base_gift_id
            gift_upgrade_conf = bond_gift_config.GetBondGiftDataConfig().get(equipped_gift_id, {})
            skill_tpl.lab_skill.SetString(gift_upgrade_conf['name_id'])
            skill_nd = skill_tpl.temp_skill
            is_lock = not has_role or bond_level < unlock_level
            skill_tpl.btn_skill.OnClick = set_callback(index)
            if gift_type == bond_gift_config.BOND_GIFT_TYPE_KEEPSAKE_GIFT:
                show_change = False if is_lock else True
                keepsake_rp = rp_mgr.get_rp_by_type(lobby_item_type.L_ITEM_TYPE_BOND_KEEPSAKE)
                template_utils.init_bond_skill(skill_nd, equipped_gift_id, level=0, redpoint=keepsake_rp, redpoint_temp='common/i_tips_red', show_lock=is_lock, black_scale=0.24, show_change=show_change, callback=set_callback(index))
            else:
                if is_lock:
                    template_utils.init_bond_skill(skill_nd, equipped_gift_id, level=0, show_lock=True, callback=set_callback(index))
                    continue
                show_rp = rp_mgr.get_rp_by_gift_type_and_belong(self.role_id, gift_type)
                if gift_type == bond_gift_config.BOND_GIFT_TYPE_DRIVER_GIFT:
                    show_rp = bond_utils.has_uncheck_exchangeable_driver_gift(self.role_id) or show_rp
                if show_rp:
                    template_utils.init_bond_skill(skill_nd, equipped_gift_id, lv, redpoint=show_rp, redpoint_temp='common/i_tips_red', callback=set_callback(index))
                    continue
                upgrade = bond_utils.is_gift_upgradable(equipped_gift_id)
                template_utils.init_bond_skill(skill_nd, equipped_gift_id, lv, redpoint=upgrade, callback=set_callback(index))

        if self._select_index < 0:
            self.select_index(0, refresh=refresh)
        else:
            self.select_index(self._select_index, refresh=refresh)

    def select_index(self, index, refresh=False):
        if self._select_index >= 0:
            last_skill_tpl = getattr(self.panel, 'nd_skill_{}'.format(self._select_index))
            last_skill_tpl.btn_skill.SetSelect(False)
            last_skill_tpl.img_arrow.setVisible(False)
        skill_tpl = getattr(self.panel, 'nd_skill_{}'.format(index))
        skill_tpl.btn_skill.SetSelect(True)
        skill_tpl.img_arrow.setVisible(True)
        self._select_index = index
        base_gift_id = self._gift_infos[index]['gift_id']
        gift_conf = bond_gift_config.GetBondGiftBaseDataConfig().get(base_gift_id, {})
        gift_type = gift_conf['gift_type']
        item_no = gift_conf['activate_item_no']
        if gift_type == bond_gift_config.BOND_GIFT_TYPE_KEEPSAKE_GIFT:
            self.show_keepsake_detail()
        else:
            if not refresh:
                global_data.lobby_red_point_data.del_item_rp(item_no)
                global_data.player.req_del_item_redpoint(item_no)
            self.show_skill_reset(gift_type)
            self.show_level_detail(self._gift_infos[index]['gift_id'])

    def show_level_detail(self, base_gift_id):
        self.can_change = False
        nd_upgrade_detail = self.panel.nd_upgrade_detail
        nd_change_detail = self.panel.nd_change_detail
        nd_skill_des = nd_upgrade_detail.nd_skill_des
        nd_upgrade_detail.setVisible(True)
        nd_change_detail.setVisible(False)
        bond_level, cur_exp = global_data.player.get_bond_data(self.role_id)
        base_gift_conf = bond_gift_config.GetBondGiftBaseDataConfig().get(base_gift_id, {})
        gift_type = base_gift_conf.get('gift_type')
        self.sel_gift_type = gift_type
        cur_gift_id, lv = bond_utils.get_gift_id_level(self.role_id, gift_type)
        gift_conf = bond_gift_config.GetBondGiftDataConfig().get(cur_gift_id, {})
        temp_gift_id = cur_gift_id if cur_gift_id else base_gift_id
        base_gift_id = bond_utils.get_base_gift(temp_gift_id)
        if lv:
            temp_lv = lv if 1 else 1
            temp_gift_conf = bond_gift_config.GetBondGiftDataConfig().get(temp_gift_id, {})
            if gift_type == bond_gift_config.BOND_GIFT_TYPE_DRIVER_GIFT and lv > 0:
                self.panel.btn_change.setVisible(True)
                self.can_change = True
            elif gift_type == bond_gift_config.BOND_GIFT_TYPE_BASE_GIFT and lv > 0:
                self.panel.btn_change.setVisible(True)
                if role_utils.is_crossover_role(self.role_id) or global_data.player.get_bond_role_num() >= bond_gift_config.REPLACE_GIFT_DRIVER_NUM:
                    self.can_change = True
            can_change_rp = bond_utils.has_uncheck_exchangeable_driver_gift(self.role_id)
            self.panel.btn_change.img_red.setVisible(can_change_rp)
            unlock_level = bond_utils.get_unlock_level_by_gift_id(self.role_id, base_gift_id)
            self.panel.lab_skill.SetString(temp_gift_conf['name_id'])
            desc_str = bond_utils.get_gift_desc(temp_gift_id)
            self.panel.lab_detail.SetString(desc_str)
            extra_desc_str = bond_utils.get_gift_extra_desc(temp_gift_id)
            self.panel.lab_detail_01.SetString(extra_desc_str)
            template_utils.init_bond_skill(nd_skill_des.temp_skill, temp_gift_id, temp_lv)
            if self._show_level_up_anim:
                nd_skill_des.temp_skill.PlayAnimation('up')
            max_level = base_gift_conf['max_level']
            self.panel.list_level.SetInitCount(max_level)
            for i in range(max_level):
                item_widget = self.panel.list_level.GetItem(i)
                gift_id = base_gift_id + i
                desc_str = bond_utils.get_gift_desc(gift_id)
                clr_str = '0x979da6'
                item_widget.img_bar.setVisible(False)
                if gift_id == cur_gift_id and lv > 0:
                    clr_str = '0xf3fafe'
                    item_widget.img_bar.setVisible(True)
                    if self._show_level_up_anim:
                        item_widget.PlayAnimation('up')
                elif gift_id < cur_gift_id:
                    clr_str = '0x3d3d3d'
                item_widget.lab_level.SetString('<color={}ff>LV.{}</color>'.format(clr_str, i + 1))
                item_widget.lab_detail.SetString('<color={}ff>{}</color>'.format(clr_str, desc_str))

            if lv > 0 and lv < max_level:
                self.panel.temp_btn_upgrade.btn_common.SetText(80542)
                self.panel.temp_btn_upgrade.btn_common.SetEnable(True)
            else:
                self.panel.temp_btn_upgrade.btn_common.SetText(2211)
                self.panel.temp_btn_upgrade.btn_common.SetEnable(False)
                self.panel.temp_btn_upgrade.btn_common.SetEnableTouch(True)
            item_no, num = gift_conf.get('upgrade_need_items', (0, 0))
            template_utils.splice_price(self.panel.temp_price, [{'original_price': num,'goods_payment': '{}_{}'.format(gconst.SHOP_PAYMENT_ITEM, item_no),'real_price': num}], show_owned=True)
            self.panel.lab_lock.setVisible(True)
            self.panel.temp_price.setVisible(False)
            self.panel.temp_btn_upgrade.setVisible(False)
            has_role = global_data.player.get_item_by_no(self.role_id)
            has_role or self.panel.lab_lock.SetString(870023)
        elif not global_data.player.has_permanent_role(self.role_id):
            self.panel.lab_lock.SetString(83488)
        elif bond_level < unlock_level:
            self.panel.lab_lock.SetString(get_text_by_id(870024, [unlock_level]))
        else:
            self.panel.lab_lock.SetString('')
            if num > 0:
                self.panel.temp_price.setVisible(True)
                self.panel.temp_btn_upgrade.setVisible(True)

        @self.panel.temp_btn_upgrade.btn_common.unique_callback()
        def OnClick(btn, touch):
            show_tips = False
            has_role = global_data.player.get_item_by_no(self.role_id)
            if not has_role:
                global_data.game_mgr.show_tip(870023)
                return
            else:
                if not cur_gift_id:
                    global_data.game_mgr.show_tip(get_text_by_id(870024, [unlock_level]))
                    return
                upgrade_gift_id = cur_gift_id
                item = global_data.player.get_item_by_no(item_no)
                own = global_data.player.get_item_num_by_no(item_no)
                if item and own >= num:
                    cur_gift_role = bond_gift_config.get_role_id_of_gift(cur_gift_id)
                    if self.role_id != cur_gift_role and bond_gift_config.get_bond_gift_type(cur_gift_id) == bond_gift_config.BOND_GIFT_TYPE_BASE_GIFT and not role_utils.is_crossover_role(self.role_id):
                        cur_role_bond_gifts = global_data.player.get_role_bond_gifts(self.role_id)
                        cur_gift_role_bond_gifts = global_data.player.get_role_bond_gifts(cur_gift_role)
                        cur_role_human_gift = None
                        cur_gift_role_human_gift = None
                        for gift_id in cur_role_bond_gifts:
                            if bond_gift_config.get_bond_gift_type(gift_id) == bond_gift_config.BOND_GIFT_TYPE_BASE_GIFT:
                                cur_role_human_gift = gift_id

                        for gift_id in cur_gift_role_bond_gifts:
                            if bond_gift_config.get_bond_gift_type(gift_id) == bond_gift_config.BOND_GIFT_TYPE_BASE_GIFT:
                                cur_gift_role_human_gift = gift_id

                        if not cur_role_human_gift or not cur_gift_role_human_gift:
                            return
                        cur_role_gift_lv = bond_gift_config.get_gift_level(cur_role_human_gift)
                        cur_gift_role_gift_lv = bond_gift_config.get_gift_level(cur_gift_role_human_gift)
                        upgrade_gift_id = cur_role_human_gift if cur_role_gift_lv < cur_gift_role_gift_lv else cur_gift_role_human_gift
                        if cur_role_gift_lv == cur_gift_role_gift_lv:
                            show_tips = True
                    BondSkillUpgradeConfirm.BondSkillUpgradeConfirm(None, self.role_id, upgrade_gift_id, show_tips)
                else:
                    from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2

                    def confirm():
                        from logic.gutils import item_utils
                        item_utils.jump_to_ui(gconst.SHOP_PAYMENT_BOND_SKILL_BOOK)

                    SecondConfirmDlg2().confirm(content=get_text_by_id(12192), confirm_callback=confirm)
                return

        self._show_level_up_anim = False

    def show_keepsake_detail(self):
        nd_upgrade_detail = self.panel.nd_upgrade_detail
        nd_change_detail = self.panel.nd_change_detail
        nd_upgrade_detail.setVisible(False)
        nd_change_detail.setVisible(True)
        self.panel.btn_change.setVisible(False)
        if self._select_keepsake_index < 0:
            self.init_keepsake_tabs()

    def init_keepsake_tabs(self):
        from logic.gutils import new_template_utils
        data_list = [{'text': 80451}, {'text': 870022}, {'text': 12013}]

        def callback(item_widget, index):
            self.show_keepsakes(index)

        new_template_utils.init_top_tab_list(self.panel.pnl_list_top_tab, data_list, callback)
        self.select_keepsake_tab(0)

    def select_keepsake_tab(self, index):
        tablist = self.panel.pnl_list_top_tab
        item_widget = tablist.GetItem(index)
        item_widget.btn_tab.OnClick(None)
        return

    def show_keepsakes(self, index, refresh=False):
        list_skill = self.panel.list_skill
        self._select_keepsake_index = index
        own_type = index
        items = bond_utils.get_keepsakes_by_type(own_type)
        count = len(items)
        self._keepsake_items = items
        if count <= 0:
            list_skill.setVisible(False)
            self.panel.nd_empty.setVisible(True)
            self.show_keepsake_item_detail(None)
            return
        else:
            list_skill.setVisible(True)
            self.panel.nd_empty.setVisible(False)
            list_skill.SetInitCount(count)

            def set_callback(index):

                def callback(*args):
                    self.select_keepsake(index)

                return callback

            select_index = 0
            for i in range(count):
                item_widget = list_skill.GetItem(i)
                gift_id = items[i]
                gift_conf = bond_gift_config.GetBondGiftDataConfig().get(gift_id)
                item_widget.lab_name.SetString(gift_conf['name_id'])
                desc_str = bond_utils.get_gift_desc(gift_id)
                item_widget.lab_detail.SetString(desc_str)
                template_utils.init_bond_skill(item_widget.btn_skill.temp_skill, gift_id, 0)
                item_widget.btn_skill.temp_skill.btn_skill.SetEnableTouch(False)
                item_widget.btn_skill.OnClick = set_callback(i)
                item_no = bond_gift_config.get_bond_gift_activate_item(gift_id)
                rp = global_data.lobby_red_point_data.get_rp_by_no(item_no)
                equiped = global_data.player.has_equiped_keepsake(self.role_id, gift_id)
                item_widget.btn_skill.img_select.setVisible(equiped)
                if equiped:
                    select_index = i
                if global_data.player.has_keepsake(gift_id):
                    item_widget.lab_name.SetColor('#SK')
                    item_widget.lab_detail.SetColor('#BC')
                    template_utils.replace_template('common/i_tips_red', item_widget.btn_skill.temp_skill, 'temp_tips')
                    item_widget.btn_skill.temp_skill.temp_tips.setVisible(rp)
                    ui_effect.set_gray(item_widget.btn_skill.temp_skill.img_skill, False)
                else:
                    item_widget.lab_name.SetColor('#BC')
                    item_widget.lab_detail.SetColor('#BC')
                    ui_effect.set_gray(item_widget.btn_skill.temp_skill.img_skill, True)

            if not refresh:
                self.select_keepsake(select_index)
            return

    def refresh_keepsakes(self):
        if not self._keepsake_items:
            return
        list_skill = self.panel.list_skill
        count = len(self._keepsake_items)
        for i in range(count):
            item_widget = list_skill.GetItem(i)
            gift_id = self._keepsake_items[i]
            equiped = global_data.player.has_equiped_keepsake(self.role_id, gift_id)
            item_widget.btn_skill.img_select.setVisible(equiped)

        if self._last_select_keepsake_index >= 0:
            gift_id = self._keepsake_items[self._last_select_keepsake_index]
            self.show_keepsake_item_detail(gift_id)

    def select_keepsake(self, index):
        list_skill = self.panel.list_skill
        if self._last_select_keepsake_index >= 0:
            item_widget = list_skill.GetItem(self._last_select_keepsake_index)
            item_widget.btn_skill.SetSelect(False)
        item_widget = list_skill.GetItem(index)
        item_widget.btn_skill.SetSelect(True)
        self._last_select_keepsake_index = index
        gift_id = self._keepsake_items[index]
        item_no = bond_gift_config.get_bond_gift_activate_item(gift_id)
        global_data.lobby_red_point_data.del_item_rp(item_no)
        global_data.player.req_del_item_redpoint(item_no)
        self.show_keepsake_item_detail(gift_id)

    def show_keepsake_item_detail(self, gift_id):
        if not gift_id:
            self.panel.nd_skill_des_2.setVisible(False)
            self.panel.temp_btn_get.setVisible(False)
            self.panel.temp_btn_change.setVisible(False)
            self.panel.lab_tips.setVisible(False)
            return
        self.panel.nd_skill_des_2.setVisible(True)
        gift_conf = bond_gift_config.GetBondGiftDataConfig().get(gift_id)
        desc_str = bond_utils.get_gift_desc(gift_id)
        self.panel.lab_detail_2.SetString(desc_str)
        self.panel.lab_lock_2.SetString(80733)
        has = global_data.player.has_keepsake(gift_id)
        equiped = global_data.player.has_equiped_keepsake(self.role_id, gift_id)
        self.panel.temp_btn_get.setVisible(not has)
        self.panel.temp_btn_change.setVisible(has)
        self.panel.temp_btn_change.btn_common.SetEnable(not equiped)
        if equiped:
            self.panel.temp_btn_change.btn_common.SetText(870040)
        else:
            self.panel.temp_btn_change.btn_common.SetText(18125)

    def on_get(self, *args):
        print('>>>> on_get')

    def on_change_driver_gift(self, *args):
        if self.can_change:
            BondSkillChange.BondSkillChange(None, self.role_id, self.sel_gift_type)
        else:
            global_data.game_mgr.show_tip(get_text_by_id(83522).format(bond_gift_config.REPLACE_GIFT_DRIVER_NUM))
        return

    def on_change_keepsake(self, *args):
        if self._last_select_keepsake_index < 0:
            return
        gift_id = self._keepsake_items[self._last_select_keepsake_index]
        if not global_data.player.has_keepsake(gift_id):
            return
        select_activate_item_no = bond_gift_config.GetBondGiftBaseDataConfig().get(gift_id, {}).get('activate_item_no', 0)
        cur_keepsake = global_data.player.get_role_keepsake(self.role_id)
        if not cur_keepsake:
            global_data.player.equip_bond_keepsake(self.role_id, select_activate_item_no)
        else:
            if str(select_activate_item_no) in cur_keepsake:
                return
            cur_activate_item_no = int(six_ex.keys(cur_keepsake)[0])
            global_data.player.update_bond_keepsake(self.role_id, cur_activate_item_no, select_activate_item_no)

    def show_skill_reset(self, gift_type):
        self.panel.nd_reset.setVisible(False)
        gift_id, lv = bond_utils.get_gift_id_level(self.role_id, gift_type)
        base_gift_id = bond_utils.get_base_gift(gift_id)
        if lv == 1:
            return
        reset_time_range = bond_gift_config.get_gift_reset_timestamp_range(base_gift_id)
        if not reset_time_range:
            return
        if global_data.player.get_item_by_no(self.role_id):
            has_role = True if 1 else False
            return has_role or None
        start_reset_timestamp, end_reset_timestamp = reset_time_range
        now = tutil.time()
        if now < start_reset_timestamp or now > end_reset_timestamp:
            return
        bond_last_reset_time = global_data.player.get_bond_gift_last_reset_time(base_gift_id)
        if start_reset_timestamp <= bond_last_reset_time <= end_reset_timestamp:
            return
        self.panel.nd_reset.setVisible(True)
        margin_to_end = end_reset_timestamp - now
        rest_reset_time_str = get_text_by_id(81056) + tutil.get_readable_time_day_hour_minitue(margin_to_end)
        self.panel.nd_reset.lab_time_limit.SetString(rest_reset_time_str)
        self.panel.nd_reset.btn_reset.SetText(870054)

        @self.panel.nd_reset.btn_reset.callback()
        def OnClick(btn, touch, cur_gift_id=gift_id):
            from logic.comsys.role_profile.SkillResetConfirmUI import SkillResetConfirmUI
            SkillResetConfirmUI(role_id=self.role_id, gift_id=cur_gift_id)