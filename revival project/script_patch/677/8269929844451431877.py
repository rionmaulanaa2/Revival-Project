# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Settle/EndRoleLevelUI.py
from __future__ import absolute_import
import cc
from common.cfg import confmgr
from logic.gutils import template_utils, bond_utils, role_utils
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_2
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no
from common.const import uiconst
SPECIAL_ROLE_PIC_OFFSET = {'201001370': ('50%-407', '50%-21'),
   '201001371': ('50%-407', '50%-21')
   }

class EndRoleLevelUI(BasePanel):
    PANEL_CONFIG_NAME = 'role_profile/role_level_up'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_2
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE
    UI_ACTION_EVENT = {'temp_btn_back.btn_back.OnClick': 'on_click_close_btn',
       'temp_btn_get.btn_common.OnClick': 'on_click_get_btn'
       }

    def on_finalize_panel(self):
        if self._close_cb:
            self._close_cb()
        self._close_cb = None
        self.show_main_ui()
        if global_data.player:
            global_data.player.check_waiting_bond_upgrade_sequences()
        return

    def on_click_close_btn(self, *args):
        self.close()

    def on_click_get_btn(self, *args):
        from logic.comsys.role_profile import RoleBondRewardUI
        RoleBondRewardUI.RoleBondRewardUI(None, self._role_id)
        return

    def on_init_panel(self, *args, **kwargs):
        self.hide_main_ui()
        self._close_cb = None
        return

    def play_animation(self, data):
        from logic.gcommon.cdata import bond_config
        self._role_id = data.get('role_id')
        self._old_lv = data.get('old_lv', 1)
        self._new_lv = data.get('new_lv', 1)
        self._close_cb = data.get('close_cb', None)
        self.init_widget()
        reward_id = bond_config.get_reward(self._role_id, self._new_lv)
        template_utils.init_common_reward_list(self.panel.list_reward, reward_id)

        def play_appear():
            if self._new_lv // 10 > self._old_lv // 10:
                self.panel.PlayAnimation('num_1')
            self.panel.PlayAnimation('appear')
            if global_data.sound_mgr:
                global_data.sound_mgr.play_ui_sound('ui_fetters_upgrade')

        self.panel.runAction(cc.Sequence.create([
         cc.CallFunc.create(play_appear),
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('loop'))]))
        return

    def init_lv_widgets(self, old_lv, now_lv):
        number_pic_path = 'gui/ui_res_2/role_profile/img_{}.png'
        old_lv_digit_1 = old_lv // 10
        old_lv_digit_2 = old_lv % 10
        now_lv_digit_1 = now_lv // 10
        now_lv_digit_2 = now_lv % 10

        def set_lv_widget_display(lv_widget, widget_1, widget_2, digit_1, digit_2):
            if digit_1 == 0:
                img_lv_x = lv_widget.getPositionX()
                img_num_1_x = widget_1.getPositionX()
                img_num_2_x = widget_2.getPositionX()
                img_lv_x = (img_lv_x + img_num_1_x) // 2
                img_num_2_x = (img_num_1_x + img_num_2_x) // 2
                lv_widget.setPositionX(img_lv_x)
                widget_1.setVisible(False)
                widget_2.setPositionX(img_num_2_x)
            widget_1.SetDisplayFrameByPath('', number_pic_path.format(digit_1))
            widget_2.SetDisplayFrameByPath('', number_pic_path.format(digit_2))

        nd_before = self.panel.nd_level_before
        nd_now = self.panel.nd_level_now
        set_lv_widget_display(nd_before.img_lv, nd_before.img_num_1, nd_before.img_num_2, old_lv_digit_1, old_lv_digit_2)
        set_lv_widget_display(nd_now.img_lv, nd_now.img_num_1, nd_now.img_num_2, now_lv_digit_1, now_lv_digit_2)
        set_lv_widget_display(nd_before.img_lv, nd_before.img_num_1_after, nd_before.img_num_2_after, now_lv_digit_1, now_lv_digit_2)

    def init_dialogue(self):
        self.panel.temp_dialogue.setVisible(False)
        role_name = confmgr.get('role_info', 'RoleProfile', 'Content', str(self._role_id), 'role_name')
        self.panel.temp_dialogue.lab_name.SetString(role_name)
        dialog_id = bond_utils.get_exp_dialog_id(self._role_id)
        if dialog_id:
            dialog_conf = confmgr.get('role_dialog_config', 'role_{}_dialog'.format(self._role_id), 'Content', str(dialog_id), default={})
            text = dialog_conf.get('content_text_id')
            self.panel.temp_dialogue.lab_dialogue.SetString(text)

    def init_widget(self):
        from logic.gcommon.item.item_const import FASHION_POS_SUIT
        role_id = self._role_id
        item_data = global_data.player.get_item_by_no(role_id)
        fashion_data = item_data.get_fashion()
        default_clothing_id = confmgr.get('role_info', 'RoleInfo', 'Content', str(self._role_id), 'default_skin')[0]
        dressed_clothing_id = fashion_data.get(FASHION_POS_SUIT, default_clothing_id)
        role_skin_config = confmgr.get('role_info', 'RoleSkin', 'Content')
        img_path = role_skin_config.get(str(dressed_clothing_id), {}).get('img_role')
        if img_path:
            self.panel.nd_role.SetDisplayFrameByPath('', img_path)
            special_pos_conf = confmgr.get('ui_display_conf', 'RoleSkinPicture', 'Content', default={})
            special_pos = special_pos_conf.get(str(dressed_clothing_id), {})
            if special_pos and special_pos.get('EndRoleLevel'):
                self.panel.nd_role.SetPosition(*special_pos.get('EndRoleLevel'))
        self.init_lv_widgets(self._old_lv, self._new_lv)
        self.init_dialogue()