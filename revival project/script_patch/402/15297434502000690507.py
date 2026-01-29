# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/role_profile/BondSkillChange.py
from __future__ import absolute_import
from __future__ import print_function
import six
from six.moves import range
from . import RoleBondRewardUI
from . import BondSkillUpgradeConfirm
import common.utilities
from common.cfg import confmgr
from common.const import uiconst
from logic.gutils import bond_utils, role_utils
import logic.gcommon.const as gconst
from logic.comsys.effect import ui_effect
from logic.gcommon.item import item_const
from logic.gcommon.cdata import bond_config
from logic.gcommon.cdata import bond_gift_config
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import mall_utils
from logic.gutils import template_utils
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no, get_lobby_item_name, get_lobby_item_desc, update_item_status
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase

class BondSkillChange(WindowMediumBase):
    PANEL_CONFIG_NAME = 'role_profile/skill_change'
    TEMPLATE_NODE_NAME = 'temp_window_small'
    DLG_ZORDER = uiconst.NORMAL_LAYER_ZORDER_2
    GLOBAL_EVENT = {'ret_bond_replace_driver_gift': 'init_widget',
       'ret_bond_refresh_driver_gifts': 'init_widget',
       'on_check_bond_exchange_driver_gift': 'refresh_red_point'
       }
    UI_ACTION_EVENT = {}

    def on_init_panel(self, role_id, gift_type):
        super(BondSkillChange, self).on_init_panel()
        self.role_id = role_id
        self.gift_type = gift_type
        self.set_title_text()
        self.init_widget()

    def on_finalize_panel(self):
        pass

    def on_get(self, *args):
        print('>>>> on_get')

    def on_bond_gift_update(self, role_id):
        if self.role_id == role_id:
            pass

    def init_widget(self, *args):
        bond_level, cur_exp = global_data.player.get_bond_data(self.role_id)
        gift_id, lv = bond_utils.get_gift_id_level(self.role_id, self.gift_type)
        gift_conf = bond_gift_config.GetBondGiftDataConfig().get(gift_id, {})
        if gift_conf:
            self.panel.lab_skill.SetString(gift_conf['name_id'])
            desc_str = bond_utils.get_gift_desc(gift_id)
            self.panel.lab_detail.SetString(desc_str)
        else:
            self.panel.lab_skill.SetString('')
            self.panel.lab_detail.SetString('')
        self.panel.nd_tips.setVisible(self.gift_type == bond_gift_config.BOND_GIFT_TYPE_BASE_GIFT and bond_level < bond_gift_config.REPLACE_GIFT_ROLE_LV and not role_utils.is_crossover_role(self.role_id))
        template_utils.init_bond_skill(self.panel.nd_skill_des.temp_skill, gift_id, lv)
        self.show_gifts()

    def refresh_red_point(self):
        self.show_gifts()

    def set_equip_gift_cb(self, gift_info, need_confirm):

        def callback(need_confirm=need_confirm):
            if need_confirm:
                BondSkillChangeConfirm(None, self.role_id, gift_info, lambda : self.close())
                return
            else:
                if gift_info['lv'] <= 0:
                    global_data.game_mgr.show_tip(get_text_by_id(870022))
                    return
                unlock_level = bond_gift_config.BOND_GIFT_DRIVER_GIFT_OTHER_CAN_EQUIP_MIN_LEVEL
                if gift_info['lv'] < unlock_level and gift_info['role_id'] != self.role_id:
                    global_data.game_mgr.show_tip(get_text_by_id(870035))
                    return
                global_data.player.replace_bond_driver_gift(self.role_id, gift_info['gift_id'])
                self.close()
                return

        return callback

    def show_gifts(self):
        list_skill = self.panel.list_skill
        cur_gift_id, lv = bond_utils.get_gift_id_level(self.role_id, self.gift_type)
        gift_list = bond_utils.get_ordered_driver_gifts(self.role_id, gift_type=self.gift_type)
        count = len(gift_list)
        list_skill.SetInitCount(count)
        gift_id_2_item_no = {v:k for k, v in six.iteritems(bond_gift_config.get_gift_activate_item_config())}
        for i in range(count):
            item_widget = list_skill.GetItem(i)
            gift_info = gift_list[i]
            gift_id = gift_info['gift_id']
            role_id = gift_info['role_id']
            base_gift_id = bond_utils.get_base_gift(gift_id)
            item_no = gift_id_2_item_no[base_gift_id]
            lv = gift_info['lv']
            bond_lv, _ = global_data.player.get_bond_data(role_id)
            cur_bond_lv, _ = global_data.player.get_bond_data(self.role_id)
            tips_args = []
            show_tips = None
            if self.gift_type != bond_gift_config.BOND_GIFT_TYPE_BASE_GIFT or role_utils.get_crossover_role_id(self.role_id):
                show_tips = None
            elif cur_bond_lv < bond_gift_config.REPLACE_GIFT_ROLE_LV and self.role_id != role_id:
                show_tips = 83523
                tips_args = [self.role_id, bond_gift_config.REPLACE_GIFT_ROLE_LV]
            elif bond_lv < bond_gift_config.REPLACE_GIFT_FROM_ROLE_LV and self.role_id != role_id:
                show_tips = 83528
                tips_args = [role_id, bond_gift_config.REPLACE_GIFT_FROM_ROLE_LV]
            else:
                show_tips = None
            if lv <= 0 or show_tips is not None:
                show_lock = True if 1 else False
                can_not_equip = lv < bond_gift_config.BOND_GIFT_DRIVER_GIFT_OTHER_CAN_EQUIP_MIN_LEVEL and not show_lock
                if role_id == self.role_id:
                    can_not_equip = False
                show_equip = False
                if gift_id == global_data.player.get_equip_driver_gift(self.role_id) or bond_gift_config.get_base_gift_id(gift_id) == bond_gift_config.get_base_gift_id(cur_gift_id):
                    show_equip = True
                    show_lock = False
                redpoint = False
                need_confirm = False
                if bond_gift_config.get_role_id_of_gift(gift_id) != self.role_id:
                    redpoint = not bond_utils.is_driver_gift_exchange_checked(gift_id)
                if self.gift_type == bond_gift_config.BOND_GIFT_TYPE_BASE_GIFT:
                    img_path = 'gui/ui_res_2/item/driver_bond/driver_tag/%s_tag.png' % role_id
                    item_widget.img_tag_driver.SetDisplayFrameByPath('', img_path)
                    item_widget.img_tag_driver.setVisible(True)
                    cur_role_gift = None
                    role_gift = None
                    for gift in global_data.player.get_role_bond_gifts(self.role_id):
                        if bond_gift_config.get_bond_gift_type(gift) == bond_gift_config.BOND_GIFT_TYPE_BASE_GIFT:
                            cur_role_gift = gift

                    cur_role_gift_level = bond_gift_config.get_gift_level(cur_role_gift)
                    role_gift_level = bond_gift_config.get_gift_level(gift_id)
                    if cur_role_gift_level < role_gift_level and not role_utils.is_crossover_role(self.role_id):
                        item_widget.lab_level.SetColor('#SR')
                        need_confirm = True
                    else:
                        item_widget.lab_level.SetColor('#SW')
                else:
                    item_widget.img_tag_driver.setVisible(False)
                template_utils.init_bond_skill2(item_widget, gift_id, lv, show_rp=redpoint, show_lock=show_lock, show_ban=can_not_equip, show_equipped=show_equip)

                def OnClick(touch, gift_info=gift_info, item_no=item_no, redpoint=redpoint, cur_index=i, tips_args=tips_args, need_confirm=need_confirm, show_equip=show_equip, show_tips=show_tips):
                    list_skill = self.panel.list_skill
                    item_count = list_skill.GetItemCount()
                    for j in range(item_count):
                        item_widget = list_skill.GetItem(j)
                        if item_widget:
                            item_widget.btn_skill.SetSelect(True if j == cur_index else False)

                    position = touch.getLocation()
                    desc_str = bond_utils.get_gift_desc(gift_info['gift_id'])
                    btn_enable = True if show_tips is None else False
                    if cur_gift_id == gift_info['gift_id'] or show_equip:
                        text_id = 870040
                        btn_enable = False
                    else:
                        text_id = 80589
                    global_data.emgr.show_item_desc_ui_event.emit(item_no, None, directly_world_pos=position, extra_info={'show_desc': desc_str,'show_yuanbao': False,
                       'btn_func': self.set_equip_gift_cb(gift_info, need_confirm),
                       'show_tips': show_tips,
                       'btn_text': text_id,
                       'btn_enable': btn_enable,
                       'tips_args': tips_args
                       })
                    if redpoint:
                        bond_utils.set_driver_gift_exchange_checked(gift_info['gift_id'])
                        global_data.emgr.on_check_bond_exchange_driver_gift.emit()
                    return

                item_widget.btn_skill.SetSwallowTouch(False)
                item_widget.btn_skill.OnClick = OnClick

        return

    def set_title_text(self):
        if self.gift_type == bond_gift_config.BOND_GIFT_TYPE_BASE_GIFT:
            self.panel.temp_window_small.lab_title.SetString(870067)


class BondSkillChangeConfirm(WindowMediumBase):
    PANEL_CONFIG_NAME = 'role_profile/skill_change_confirm'
    TEMPLATE_NODE_NAME = 'temp_bg'
    DLG_ZORDER = uiconst.NORMAL_LAYER_ZORDER_2

    def on_init_panel(self, role_id, gift_info, cb):
        super(BondSkillChangeConfirm, self).on_init_panel()
        self.role_id = role_id
        self.gift_info = gift_info
        cur_equip_gift = global_data.player.get_equip_human_gift(role_id)
        cur_base_gift_id = bond_utils.get_base_gift(cur_equip_gift)
        change_bast_gift_id = bond_utils.get_base_gift(gift_info['gift_id'])
        cur_level = cur_equip_gift - cur_base_gift_id + 1
        change_level = gift_info['lv']
        cur_role_gift_level = 0
        for gift_id in global_data.player.get_role_bond_gifts(role_id):
            if bond_gift_config.get_bond_gift_type(gift_id) == bond_gift_config.BOND_GIFT_TYPE_BASE_GIFT:
                cur_role_gift_level = bond_gift_config.get_gift_level(gift_id)

        template_utils.init_bond_skill(self.panel.temp_skill_before, cur_base_gift_id, cur_level)
        template_utils.init_bond_skill(self.panel.temp_skill_after, change_bast_gift_id, change_level)
        gift_conf = bond_gift_config.GetBondGiftDataConfig().get(gift_info['gift_id'], {})
        self.panel.lab_detail.SetString(get_text_by_id(83526).format(get_text_by_id(gift_conf['name_id']), cur_role_gift_level))

        @self.panel.temp_btn_confirm.btn_common.unique_callback()
        def OnClick(btn, touch, cb=cb):
            if gift_info['lv'] <= 0:
                global_data.game_mgr.show_tip(get_text_by_id(870022))
                return
            if global_data.player:
                global_data.player.replace_bond_driver_gift(self.role_id, gift_info['gift_id'])
            self.close()
            cb()

    def on_finalize_panel(self):
        pass