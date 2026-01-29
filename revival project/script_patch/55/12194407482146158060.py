# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/role_profile/SkillResetConfirmUI.py
from __future__ import absolute_import
import six
from common.uisys.basepanel import BasePanel
from common.const.uiconst import SECOND_CONFIRM_LAYER
from logic.gutils import template_utils, bond_utils
from logic.gcommon.cdata import bond_gift_config
from common.const import uiconst

class SkillResetConfirmUI(BasePanel):
    DLG_ZORDER = SECOND_CONFIRM_LAYER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    PANEL_CONFIG_NAME = 'role_profile/skill_reset_confirm'
    UI_ACTION_EVENT = {'temp_bg.btn_close.OnClick': 'on_close',
       'temp_confirm.btn_common_big.OnClick': 'on_confirm'
       }
    GLOBAL_EVENT = {'player_money_info_update_event': 'on_reset_success'
       }

    def on_init_panel(self, role_id, gift_id):
        self.gift_id = gift_id
        self.role_id = role_id
        self.init_widgets()

    def on_finalize_panel(self):
        pass

    def init_widgets(self):
        item_temp = self.panel.temp_item
        give_back_items = bond_gift_config.calc_reset_gift_give_back_items(self.gift_id)
        for item_no, num in six.iteritems(give_back_items):
            template_utils.init_tempate_mall_i_simple_item(item_temp, item_no, num)

    def on_close(self, *args):
        self.close()

    def on_confirm(self, *args):
        if self.gift_id is None:
            return
        else:
            global_data.player.reset_bond_gift(self.gift_id)
            return

    def on_reset_success(self, *args):
        from logic.gcommon.common_utils.local_text import get_text_by_id
        gift_type = bond_utils.get_gift_type(self.gift_id)
        text_id = 870057 if gift_type == bond_gift_config.BOND_GIFT_TYPE_BASE_GIFT else 870058
        global_data.game_mgr.show_tip(get_text_by_id(text_id))
        self.close()