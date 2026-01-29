# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/intimacy/IntimacyLevelupUI.py
from __future__ import absolute_import
from six.moves import range
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
from common.const.property_const import U_ID, C_NAME
from logic.gutils.role_head_utils import PlayerInfoManager
from common.const.uiconst import DIALOG_LAYER_ZORDER_1
from logic.gutils.intimacy_utils import INTIMACY_PIC, get_relation_by_uid
from logic.gcommon.cdata.intimacy_data import LV_CAP, LV_CAP_REWARD_LV, get_lv_data, LV_CAP_REWARD, get_unreceived_intimacy_rewards
from common.cfg import confmgr
REWARD_MAP = (({'icon': 'gui/ui_res_2/friend/intimacy/reward/intimacy01.png','name': 3261}, {'icon': 'gui/ui_res_2/friend/intimacy/reward/intimacy.png','name': 3262}), {'icon': 'gui/ui_res_2/friend/intimacy/reward/teamup.png','name': 3263}, {'icon': 'gui/ui_res_2/friend/intimacy/reward/mechashare.png','name': 3264}, {'icon': 'gui/ui_res_2/friend/intimacy/reward/intimacy01.png','name': 3265}, {'icon': 'gui/ui_res_2/friend/intimacy/reward/spray1.png','name': 3266}, {'icon': 'gui/ui_res_2/friend/intimacy/reward/mecha_proficiency.png','name': 3267}, {'icon': 'gui/ui_res_2/friend/intimacy/reward/intimacy03.png','name': 3268}, {'icon': 'gui/ui_res_2/friend/intimacy/reward/coin_up.png','name': 3269}, {'icon': 'gui/ui_res_2/friend/intimacy/reward/spray.png','name': 3270}, {'icon': 'gui/ui_res_2/friend/intimacy/reward/rename.png','name': 3271}, {'icon': 'gui/ui_res_2/friend/intimacy/reward/spray.png','name': 3272})

class IntimacyLevelupUI(WindowMediumBase):
    PANEL_CONFIG_NAME = 'friend/intimacy_level_up'
    TEMPLATE_NODE_NAME = 'temp_bg'
    UI_ACTION_EVENT = {'btn_confirm.btn_common.OnClick': 'custom_close'
       }
    GLOBAL_EVENT = {'message_on_player_simple_inf': 'set_player_inf'
       }
    DLG_ZORDER = DIALOG_LAYER_ZORDER_1

    def on_init_panel(self, *args, **kwargs):
        super(IntimacyLevelupUI, self).on_init_panel(*args, **kwargs)
        self.set_custom_close_func(self.custom_close)
        self.msg = []
        self.uid = None
        self.close_cb = None
        self.panel.setVisible(False)
        return

    def level_up(self, old_lv, new_lv, player_inf):
        self.panel.lab_low.SetString('Lv.%d' % old_lv)
        self.panel.lab_high.SetString('Lv.%d' % new_lv)
        uid = player_inf[U_ID]
        update_head_info = global_data.message_data.get_role_head_info(uid)
        frame = update_head_info.get('head_frame', None)
        photo = update_head_info.get('head_photo', None)
        if frame and photo:
            player_inf['head_frame'] = frame
            player_inf['head_photo'] = photo
        player_info_manager = PlayerInfoManager()
        player_info_manager.add_head_item_auto(self.panel.temp_head, uid, 0, player_inf)
        self.panel.lab_user_name.SetString(player_inf[C_NAME])
        relation = get_relation_by_uid(uid)
        if relation in INTIMACY_PIC:
            self.panel.img_icon.SetDisplayFrameByPath('', INTIMACY_PIC[relation])
        reward_list = self.get_reward_list(old_lv, new_lv)
        reward_count = len(reward_list)
        self.panel.list_reward.setVisible(reward_count <= 2)
        self.panel.list_reward_muti.setVisible(reward_count > 2)
        list_reward = self.panel.list_reward if reward_count <= 2 else self.panel.list_reward_muti
        list_reward.DeleteAllSubItem()
        list_reward.SetInitCount(reward_count)
        for idx, reward in enumerate(reward_list):
            item = list_reward.GetItem(idx)
            item.img_item.SetDisplayFrameByPath('', reward['icon'])
            item.lab_item.SetString(reward['name'])

        self.panel.setVisible(True)
        return

    def get_reward_list(self, old_lv, new_lv):
        reward_list = []

        def append_reward(reward):
            if type(reward) in (list, tuple):
                reward_list.extend(reward)
            else:
                reward_list.append(reward)

        if old_lv <= LV_CAP:
            old_lv += 1
            while old_lv <= min(LV_CAP, new_lv):
                reward = REWARD_MAP[old_lv - 1]
                append_reward(reward)
                old_lv += 1

            if old_lv > new_lv:
                return reward_list
        old_extra_lv = old_lv - LV_CAP
        old_extra_lv -= old_extra_lv % LV_CAP_REWARD_LV
        new_extra_lv = new_lv - LV_CAP
        extra_reward_count = int((new_extra_lv - old_extra_lv) / LV_CAP_REWARD_LV)
        for i in range(extra_reward_count):
            append_reward(REWARD_MAP[-1])

        return reward_list

    def show_msg(self, uid, msg, close_cb=None):
        self.msg = msg
        self.uid = str(uid)
        self.close_cb = close_cb
        player_inf = global_data.message_data.get_player_simple_inf(uid)
        if player_inf:
            self.set_player_inf(player_inf)

    def set_player_inf(self, player_inf):
        uid = str(player_inf[U_ID])
        if self.uid == uid and self.msg:
            self.level_up(self.msg[0], self.msg[1], player_inf)

    def custom_close(self, *args):
        self.close()
        if callable(self.close_cb):
            self.close_cb()