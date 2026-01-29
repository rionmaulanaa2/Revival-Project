# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Settle/BRV2EndExpUI.py
from __future__ import absolute_import
from logic.comsys.battle.Settle.EndExpUI import EndExpUI
from logic.gcommon.item import item_const
from logic.gutils import bond_utils
from common.cfg import confmgr

class BRV2EndExpUI(EndExpUI):
    PANEL_CONFIG_NAME = 'end/end_exp_brv2'

    def on_custom_template_create(self, settle_dict, reward, settle_exp_dict, parent=None, **kwargs):
        super(BRV2EndExpUI, self).on_custom_template_create()
        bond_rewards = reward.bond
        if bond_utils.is_open_bond_sys() and bond_rewards:
            BRV2EndExpUI.PANEL_CONFIG_NAME = 'end/end_exp_brv2_new'
        else:
            BRV2EndExpUI.PANEL_CONFIG_NAME = 'end/end_exp_brv2'

    def show_mecha_exp(self, settle_dict, reward):
        pass

    def show_self_exp(self, settle_exp_dict, finished_cd):
        super(BRV2EndExpUI, self).show_self_exp(settle_exp_dict, finished_cd)
        if BRV2EndExpUI.PANEL_CONFIG_NAME == 'end/end_exp_brv2':
            fashion_dict = global_data.player.logic.ev_g_fashion()
            clothing_id = fashion_dict.get(item_const.FASHION_POS_SUIT)
            role_skin_config = confmgr.get('role_info', 'RoleSkin', 'Content')
            img_path = role_skin_config.get(str(clothing_id), {}).get('img_role')
            self.panel.img_role.SetDisplayFrameByPath('', img_path)