# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/King/KothCampShopReplaceWeaponUI.py
from __future__ import absolute_import
from six.moves import range
from common.const.uiconst import DIALOG_LAYER_ZORDER
from common.uisys.basepanel import BasePanel
from logic.gcommon import const
from logic.gutils import koth_shop_utils
from common.const import uiconst

class KothCampShopReplaceWeaponUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_koth/mall_change_weapen'
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_close.OnClick': 'on_click_btn_close'}
    MAIN_WEAPON_LIST = (
     const.PART_WEAPON_POS_MAIN1, const.PART_WEAPON_POS_MAIN2, const.PART_WEAPON_POS_MAIN3)

    def on_init_panel(self):
        self._cur_sel_goods_data = {}
        self.init_own_weapons()
        self.init_changed_buttons()

    def on_click_btn_close(self, btn, touch):
        self.close()

    def on_finalize_panel(self):
        self._cur_sel_goods_data = {}

    def on_click_btn_mall(self, btn, touch):
        global_data.ui_mgr.show_ui('KothCampShopUI', 'logic.comsys.battle.King')
        from logic.comsys.battle.King.KothCampShopUI import KothCampShopUI
        KothCampShopUI()

    def init_changed_buttons(self):
        button_num = len(self.MAIN_WEAPON_LIST)
        for i in range(button_num):
            btn = getattr(self.panel, 'btn_change_%d' % (i + 1))
            if btn:

                @btn.btn_common.callback()
                def OnClick(btn, touch, idx=i):
                    if not global_data.player:
                        return
                    else:
                        bat = global_data.player.get_battle()
                        if not bat:
                            return
                        goods_id = self._cur_sel_goods_data.get('goods_id', None)
                        if goods_id is None:
                            return
                        pos = self.MAIN_WEAPON_LIST[idx]
                        level = 1
                        num = 1
                        goods_list = [(goods_id, pos, level, num)]
                        shop_lent = koth_shop_utils.get_cur_shop_lent()
                        if not shop_lent:
                            return
                        shop_lent.send_event('E_CALL_SYNC_METHOD', 'buy_goods', (global_data.player.id, goods_list), False, True)
                        self.close()
                        return

    def init_own_weapons(self):
        pos_list = self.MAIN_WEAPON_LIST
        if global_data.player:
            player = global_data.player.logic if 1 else None
            return player or None
        else:
            from logic.gutils import template_utils
            hand_pos = player.share_data.ref_wp_bar_cur_pos
            for pos in pos_list:
                weapon_obj = player.share_data.ref_wp_bar_mp_weapons.get(pos)
                if weapon_obj is None:
                    weapon_data = None if 1 else weapon_obj.get_data()
                    if weapon_data:
                        weapon_data['iBulletCap'] = weapon_obj.get_bullet_cap()
                    show_pos = self.get_pos_show_idx(pos)
                    if show_pos is None:
                        continue
                    item_widget = getattr(self.panel, 'nd_weapen_%d' % (show_pos + 1))
                    if not item_widget:
                        continue
                    template_utils.init_gun_equipment(item_widget, weapon_data, pos == const.PART_WEAPON_POS_MAIN1, player)

            return

    def get_pos_show_idx(self, weapon_pos):
        dic = {const.PART_WEAPON_POS_MAIN1: 0,
           const.PART_WEAPON_POS_MAIN2: 1,
           const.PART_WEAPON_POS_MAIN3: 2
           }
        return dic.get(weapon_pos, None)

    def set_sel_goods(self, goods_data):
        from logic.gutils.koth_shop_utils import init_shop_weapon_item
        init_shop_weapon_item(self.panel.nd_weapen_new, goods_data)
        self._cur_sel_goods_data = goods_data
        from logic.gcommon.common_utils.local_text import get_text_by_id
        from logic.gutils import item_utils
        item_no = goods_data.get('item_no', None)
        self.panel.tf_replace_desc.SetString(get_text_by_id(18212, {'gun_name': item_utils.get_item_name(item_no)}))
        return