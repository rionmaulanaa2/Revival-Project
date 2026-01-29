# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/item_use/UseProficiencyCardUI.py
from __future__ import absolute_import
import cc
import collision
from common.uisys.basepanel import BasePanel
from common.utils.cocos_utils import neox_pos_to_cocos, cocos_pos_to_neox
from common.const.uiconst import NORMAL_LAYER_ZORDER, BG_ZORDER
from logic.gutils.dress_utils import mecha_lobby_id_2_battle_id
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_MECHA
from logic.comsys.login.LoginSetting import LoginSetting
from logic.gutils import role_head_utils
from common.platform.dctool import interface
from logic.gutils.item_utils import get_mecha_role_pic, get_lobby_item_name, get_lobby_item_pic_by_item_no, init_lobby_bag_item
from common.cfg import confmgr
from common.utils.timer import CLOCK
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase

class UseProficiencyCardUI(WindowMediumBase):
    PANEL_CONFIG_NAME = 'bag/bag_quick_multi_use'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_ACTION_EVENT = {}
    GLOBAL_EVENT = {'update_proficiency_event': 'on_update_proficiency',
       'on_lobby_bag_item_changed_event': 'on_card_num_changed'
       }
    USE_CNT_LIST = [
     1, 2, 5]
    TEMPLATE_NODE_NAME = 'window_medium'

    def on_init_panel(self, *args, **kwargs):
        super(UseProficiencyCardUI, self).on_init_panel()
        self.mecha_item = {}
        self._cur_card_num = 0
        self._cur_card_no = None
        self._prof_conf = confmgr.get('proficiency_config', 'Proficiency')
        self._max_level = len(self._prof_conf)
        self._cnt_timer = None
        self._use_cnt_idx = 0
        self._use_timer = None
        self._can_use = True
        self._item_data = {}
        return

    def on_finalize_panel(self):
        self.cancel_cnt_timer()
        self.cancel_use_timer()

    def init_card_num(self, item_id):
        item = global_data.player.get_item_by_id(item_id)
        if not item:
            return
        self._cur_card_no = item.get_item_no()
        self._cur_card_num = item.get_current_stack_num()
        self.panel.card_num.txt_price.SetString(str(self._cur_card_num))
        card_icon = get_lobby_item_pic_by_item_no(self._cur_card_no)
        self.panel.card_num.price_icon.SetDisplayFrameByPath('', card_icon)

    def init_mecha_list(self):
        mecha_items = global_data.player.get_items_by_type(L_ITEM_TYPE_MECHA)
        mecha_list = self.panel.mech_list
        mecha_list.DeleteAllSubItem()
        self.mecha_item = {}
        for mecha_item in mecha_items:
            mecha_id = mecha_lobby_id_2_battle_id(mecha_item.item_no)
            mecha_nd_item = mecha_list.AddTemplateItem()
            icon_path = get_mecha_role_pic(str(mecha_id))
            mecha_nd_item.mech_head.img_mech_head.SetDisplayFrameByPath('', icon_path)
            mecha_nd_item.lab_mech_name.SetString(get_lobby_item_name(str(mecha_item.item_no)))
            self.mecha_item[str(mecha_id)] = mecha_nd_item
            level, proficiency = global_data.player.get_proficiency(mecha_id)
            self.on_update_proficiency(mecha_id, level, proficiency)
            mecha_nd_item.btn_add.mecha_id = mecha_id

            @mecha_nd_item.btn_add.unique_callback()
            def OnBegin(btn, touch):
                if self._use_timer:
                    return False
                else:
                    self._use_cnt_idx = 0
                    if self.use_card(btn.mecha_id):
                        self._cnt_timer = global_data.game_mgr.register_logic_timer(self.on_add_use_cnt, 2, mode=CLOCK)
                        self._use_timer = global_data.game_mgr.register_logic_timer(self.use_card, 0.3, (btn.mecha_id,), mode=CLOCK)
                        return True
                    global_data.game_mgr.show_tip(get_text_by_id(19003))
                    return False

            @mecha_nd_item.btn_add.unique_callback()
            def OnCancel(btn, touch):
                self.cancel_cnt_timer()
                self.cancel_use_timer()
                self._use_cnt_idx = 0
                self._can_use = True
                return True

            @mecha_nd_item.btn_add.unique_callback()
            def OnEnd(btn, touch):
                self.cancel_cnt_timer()
                self.cancel_use_timer()
                self._use_cnt_idx = 0
                self._can_use = True
                return True

    def use_card(self, mecha_id):
        if not self._can_use:
            return
        use_cnt = min(self._cur_card_num, self.USE_CNT_LIST[self._use_cnt_idx])
        if use_cnt > 0:
            global_data.player.use_item(self._item_data['id'], use_cnt, {'mecha_type': str(mecha_id)})
            self._can_use = False
            return True
        return False

    def on_card_num_changed(self):
        item = global_data.player.get_item_by_id(self._item_data['id'])
        if item:
            new_card_num = item.get_current_stack_num()
            if new_card_num < self._cur_card_num:
                self._can_use = True
            self._cur_card_num = new_card_num
            self.panel.card_num.txt_price.SetString(str(self._cur_card_num))
        else:
            self._cur_card_num = 0
            self.panel.card_num.txt_price.SetString(str(0))

    def on_add_use_cnt(self):
        self._use_cnt_idx += 1
        if self._use_cnt_idx == len(self.USE_CNT_LIST) - 1:
            self.cancel_cnt_timer()

    def cancel_cnt_timer(self):
        if self._cnt_timer:
            global_data.game_mgr.unregister_logic_timer(self._cnt_timer)
        self._cnt_timer = None
        return

    def cancel_use_timer(self):
        if self._use_timer:
            global_data.game_mgr.unregister_logic_timer(self._use_timer)
        self._use_timer = None
        return

    def on_update_proficiency(self, mecha_id, level, proficiency, up_level=False):
        mecha_item = self.mecha_item.get(str(mecha_id), None)
        if not mecha_item:
            return
        else:
            if level < self._max_level:
                upgrade_value = self._prof_conf.get(str(level + 1), {}).get('upgrade_value', 0)
            else:
                upgrade_value = self._prof_conf.get(str(level), {}).get('upgrade_value', 0)
                proficiency = upgrade_value
            mecha_item.lab_proficiency_lv.SetString('Lv%s   %s/%s' % (level, proficiency, upgrade_value))
            if upgrade_value:
                mecha_item.bar_progress.proficiency_progress.SetPercent(proficiency * 100.0 / upgrade_value)
            else:
                mecha_item.bar_progress.proficiency_progress.SetPercent(100)
            return

    def set_use_params(self, item_data, *args, **kwargs):
        self._item_data = item_data
        self.init_card_num(item_data['id'])
        self.init_mecha_list()