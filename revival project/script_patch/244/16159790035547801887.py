# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/role_profile/RoleBondRewardUI.py
from __future__ import absolute_import
from six.moves import range
import common.utilities
from common.cfg import confmgr
from common.const import uiconst
from logic.gcommon.item import item_const
from logic.gcommon.cdata import bond_config
from logic.gcommon.cdata import bond_gift_config
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import mall_utils
from logic.gutils.template_utils import init_tempate_mall_i_item
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no, get_lobby_item_name, get_lobby_item_desc, update_item_status
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase

class RoleBondRewardUI(WindowMediumBase):
    PANEL_CONFIG_NAME = 'role_profile/role_level_reward'
    TEMPLATE_NODE_NAME = 'temp_bg'
    DLG_ZORDER = uiconst.NORMAL_LAYER_ZORDER_2
    GLOBAL_EVENT = {'bond_role_reward': 'on_bond_reward'
       }

    def on_init_panel(self, role_id):
        super(RoleBondRewardUI, self).on_init_panel()
        self.role_id = None
        self._reward_levels = None
        self._reward_item_dict = None
        self.init_widget(role_id)
        return

    def on_finalize_panel(self):
        self._reward_levels = None
        self._reward_item_dict = None
        return

    def init_widget(self, role_id):
        if not global_data.player:
            return
        if self.role_id == role_id:
            return
        self.role_id = role_id
        self.show_role_info()
        self.show_all_reward_status()

    def on_bond_reward(self, role_id):
        role_id = int(role_id)
        if self.role_id == role_id:
            self.show_all_reward_status()

    def on_update_reward_status(self, role_id, lv):
        if self.role_id != role_id:
            return
        else:
            if not self._reward_item_dict:
                return
            reward_item = self._reward_item_dict.get(lv, None)
            if not reward_item:
                return
            cur_lv, _ = global_data.player.get_bond_data(self.role_id)
            if lv > cur_lv or not global_data.player.get_item_by_no(self.role_id):
                status = item_const.ITEM_UNGAIN
            elif global_data.player.is_bond_reward_received(self.role_id, lv):
                status = item_const.ITEM_RECEIVED
            else:
                status = item_const.ITEM_UNRECEIVED
            reward_id = bond_config.get_reward(self.role_id, lv)
            reward_conf = confmgr.get('common_reward_data', str(reward_id), default={})
            reward_list = reward_conf.get('reward_list', [])
            count = len(reward_list)
            for i in range(2):
                temp_item = getattr(reward_item, 'temp_item_{}'.format(i + 1))
                if i > count - 1:
                    temp_item.setVisible(False)
                    continue
                temp_item.setVisible(True)
                update_item_status(temp_item, status if global_data.player.has_permanent_role(role_id) else item_const.ITEM_UNGAIN)

            if status == item_const.ITEM_UNGAIN:
                reward_item.img_lock.setVisible(True)
            else:
                reward_item.img_lock.setVisible(False)
            return

    def init_reward_data(self):
        self._reward_item_dict = {}
        self._reward_levels = bond_config.get_bond_levels()
        self._reward_levels = [ lv for lv in self._reward_levels if bond_config.get_reward(self.role_id, lv) ]
        nd = self.panel
        nd.list_reward.DeleteAllSubItem()

        @self.panel.list_reward.unique_callback()
        def OnCreateItem(lv, idx, ui_item):
            self.init_reward_item(ui_item, idx)

        nd.list_reward.SetInitCount(len(self._reward_levels))
        level, exp = global_data.player.get_bond_data(self.role_id)
        show_idx = max(0, level - 2)
        nd.list_reward.LocatePosByItem(show_idx)
        nd.list_reward.scroll_Load()
        nd.list_reward._refreshItemPos()

    def init_reward_item(self, reward_item, idx):
        lv = self._reward_levels[idx]
        self._reward_item_dict[lv] = reward_item
        reward_item.lab_level.SetString('LV{}'.format(lv))
        reward_id = bond_config.get_reward(self.role_id, lv)
        reward_conf = confmgr.get('common_reward_data', str(reward_id), default={})
        reward_list = reward_conf.get('reward_list', [])
        count = len(reward_list)
        for i in range(2):
            if i > count - 1:
                continue
            reward_info = reward_list[i]
            temp_item = getattr(reward_item, 'temp_item_{}'.format(i + 1))
            item_no = reward_info[0]
            item_num = reward_info[1]
            init_tempate_mall_i_item(temp_item, item_no, item_num)

            @temp_item.btn_choose.unique_callback()
            def OnClick(btn, touch, level=lv, item_no=item_no):
                x, y = btn.GetPosition()
                w, h = btn.GetContentSize()
                x += w * 0.5
                wpos = btn.ConvertToWorldSpace(x, y)
                global_data.emgr.show_item_desc_ui_event.emit(item_no, wpos, extra_info={'show_jump': False})
                return True

        @reward_item.unique_callback()
        def OnClick(btn, touch):
            if not global_data.player.is_bond_reward_received(self.role_id, lv):
                global_data.player.receive_bond_reward(self.role_id, lv)

        self.on_update_reward_status(self.role_id, lv)

    def show_all_reward_status(self):
        if self._reward_item_dict is None:
            self.init_reward_data()
        else:
            max_idx = 0
            for idx in range(len(self._reward_levels)):
                lv = self._reward_levels[idx]
                reward_item = self._reward_item_dict.get(lv, None)
                if reward_item:
                    self.on_update_reward_status(self.role_id, lv)
                    max_idx = idx

        return

    def show_role_info(self):
        self.panel.temp_role.lab_role.SetString(get_lobby_item_name(self.role_id))
        img_role = mall_utils.get_half_pic_by_item_no(self.role_id)
        if img_role:
            self.panel.temp_role.img_role.SetDisplayFrameByPath('', img_role)
        level, exp = global_data.player.get_bond_data(self.role_id)
        nxt_level, nxt_exp = bond_config.get_nxt_bond_level_strength(level)
        if nxt_exp == 0:
            max_level, max_exp = bond_config.get_nxt_bond_level_strength(level - 1)
            exp = nxt_exp = max_exp
        self.panel.temp_role.lab_level.SetString('Lv{}'.format(level))
        percent = common.utilities.safe_percent(exp, nxt_exp)
        self.panel.temp_role.lab_exp.SetString('#SW{}#n/#SH{}#n'.format(exp, nxt_exp))
        self.panel.temp_role.progress_exp.SetPercentage(percent)