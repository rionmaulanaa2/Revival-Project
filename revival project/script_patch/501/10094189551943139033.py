# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/role_profile/BondSkillUpgradeConfirm.py
from __future__ import absolute_import
from . import RoleBondRewardUI
import common.utilities
from common.cfg import confmgr
from common.const import uiconst
from logic.gutils import bond_utils
import logic.gcommon.const as gconst
from logic.gcommon.item import item_const
from logic.gcommon.cdata import bond_config
from logic.gcommon.cdata import bond_gift_config
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import mall_utils
from logic.gutils import template_utils
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no, get_lobby_item_name, get_lobby_item_desc, update_item_status
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase

class BondSkillUpgradeConfirm(WindowMediumBase):
    PANEL_CONFIG_NAME = 'role_profile/skill_upgrade_confirm'
    TEMPLATE_NODE_NAME = 'temp_bg'
    DLG_ZORDER = uiconst.NORMAL_LAYER_ZORDER_2
    GLOBAL_EVENT = {}

    def on_init_panel(self, role_id, cur_gift_id, show_tips=False):
        super(BondSkillUpgradeConfirm, self).on_init_panel()
        self.role_id = role_id
        self.cur_gift_id = cur_gift_id
        gift_conf = bond_gift_config.GetBondGiftDataConfig().get(cur_gift_id, {})
        next_gift_conf = bond_gift_config.GetBondGiftDataConfig().get(cur_gift_id + 1, {})
        base_gift_id = gift_conf['base_gift_id']
        cur_level = cur_gift_id - base_gift_id + 1
        self.panel.lab_skill.SetString(gift_conf['name_id'])
        desc_id = gift_conf['desc_id']
        desc_param = gift_conf.get('desc_param', [])
        next_desc_param = next_gift_conf.get('desc_param', [])
        clr = '#DP'
        new_desc_param = []
        for i, str_num in enumerate(desc_param):
            if str_num != next_desc_param[i]:
                new_desc_param.append('{}{}#n->{}{}#n'.format(clr, str_num, clr, next_desc_param[i]))
            else:
                new_desc_param.append('{}{}#n'.format(clr, str_num))

        desc_str = get_text_by_id(desc_id, args=new_desc_param or None if 1 else new_desc_param)
        self.panel.lab_detail.SetString(desc_str)
        template_utils.init_bond_skill(self.panel.temp_skill_before, base_gift_id, cur_level)
        template_utils.init_bond_skill(self.panel.temp_skill_after, base_gift_id, cur_level + 1)
        item_no, num = gift_conf.get('upgrade_need_items', (0, 0))
        template_utils.init_price_template({'original_price': num,'goods_payment': '{}_{}'.format(gconst.SHOP_PAYMENT_ITEM, item_no),'real_price': num}, self.panel.temp_price, color='#SS')

        @self.panel.temp_btn_buy.btn_common.unique_callback()
        def OnClick(btn, touch, show_tips=show_tips):
            own = global_data.player.get_item_num_by_no(item_no)
            if own >= num:
                global_data.player.request_upgrade_role_bond_gift(self.role_id, cur_gift_id)
                if show_tips:
                    global_data.game_mgr.show_tip(get_text_by_id(83527).format(bond_gift_config.get_gift_level(self.cur_gift_id)))
                self.close()

        return

    def on_finalize_panel(self):
        pass

    def on_bond_gift_update(self, role_id):
        role_id = int(role_id)
        if self.role_id == role_id:
            pass