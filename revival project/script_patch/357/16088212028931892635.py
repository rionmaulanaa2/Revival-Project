# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/gvg/GVGScoreDetailsUI.py
from __future__ import absolute_import
import six
from common.const.uiconst import BASE_LAYER_ZORDER_1, UI_VKB_CLOSE
from common.uisys.basepanel import BasePanel
from logic.gutils import role_head_utils
from common.utils.timer import CLOCK
from logic.client.const import game_mode_const

class GVGScoreDetailsUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_gvg/gvg_score_detials'
    DLG_ZORDER = BASE_LAYER_ZORDER_1
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'base_layer.OnClick': '_close_btn_cb',
       'temp_score_details.btn_close.OnClick': '_close_btn_cb'
       }

    def on_init_panel(self):
        self.init_parameters()
        self.process_event(True)
        self.init_panel()

    def on_finalize_panel(self):
        if self.get_details_timer:
            global_data.game_mgr.unregister_logic_timer(self.get_details_timer)
            self.get_details_timer = None
        self.process_event(False)
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_score_details': self.update_score_details
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_parameters(self):

        def update_details():
            bat = global_data.battle
            bat and bat.request_rank_data()

        update_details()
        self.get_details_timer = global_data.game_mgr.register_logic_timer(update_details, times=-1, interval=1, mode=CLOCK)
        bat = global_data.battle
        self.mecha_choose_dict = bat.mecha_choose_dict
        self.eid_to_index = bat.eid_to_index
        self.group_to_num = bat.group_to_num
        self.my_group = bat.my_group
        self.other_group = bat.other_group

    def init_panel(self):
        self.panel.temp_score_details.setVisible(False)
        self.panel.temp_score_details.list_blue.SetInitCount(self.group_to_num.get(self.my_group, 0))
        self.panel.temp_score_details.list_red.SetInitCount(self.group_to_num.get(self.other_group, 0))
        if global_data.gvg_battle_data:
            self.update_score_details(global_data.gvg_battle_data.get_score_details_data())

    def update_score_details(self, data):
        bat = global_data.battle
        frd_left_mecha_num = 0
        emy_left_mecha_num = 0
        for score_details_list in six.itervalues(data):
            for i, score_details in enumerate(score_details_list):
                soul_id, name, role_id, kill_num, assist, damage, hurt, mecha_use_count = score_details
                if bat.is_friend_group(soul_id):
                    frd_left_mecha_num += game_mode_const.GVG_MECHA_NUM - mecha_use_count
                    temp_nd = self.panel.temp_score_details.list_blue.GetItem(i)
                else:
                    emy_left_mecha_num += game_mode_const.GVG_MECHA_NUM - mecha_use_count
                    temp_nd = self.panel.temp_score_details.list_red.GetItem(i)
                if not temp_nd:
                    continue
                if global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_DUEL,)):
                    assist = ''
                temp_nd.img_single.setVisible(False)
                temp_nd.img_mine.setVisible(bat.is_observed_target_id(soul_id))
                for i, txt in enumerate([name, kill_num, assist]):
                    lab_nd_name = 'lab_%d' % i
                    lab_nd = getattr(temp_nd, lab_nd_name)
                    lab_nd.SetString(str(txt))
                    for round_idx, mecha_id in six.iteritems(self.mecha_choose_dict.get(soul_id, {})):
                        head_index = round_idx - mecha_use_count
                        head_nd_name = 'i_head_%d' % (head_index + game_mode_const.GVG_MECHA_NUM if head_index <= 0 else head_index)
                        head_nd = getattr(temp_nd, head_nd_name)
                        icon_path = role_head_utils.get_head_photo_res_path(int('3021%d' % mecha_id))
                        head_nd.img_head.SetDisplayFrameByPath('', icon_path)
                        head_nd.nd_die.setVisible(round_idx <= mecha_use_count)
                        if global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_DUEL,)):
                            soul_round_record = global_data.battle.get_round_record(soul_id) or [-1, -1, -1]
                            record_indx = round_idx - 1
                            if len(soul_round_record) > record_indx:
                                head_nd.img_ban.setVisible(soul_round_record[record_indx] == -1)

        self.panel.temp_score_details.temp_title_1.lab_num.SetString(str(frd_left_mecha_num))
        self.panel.temp_score_details.temp_title_2.lab_num.SetString(str(emy_left_mecha_num))
        if global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_DUEL,)):
            self.panel.temp_score_details.temp_title_1.img_assist.setVisible(False)
            self.panel.temp_score_details.temp_title_2.img_assist.setVisible(False)
            self.panel.temp_score_details.temp_title_1.lab_num.SetString('')
            self.panel.temp_score_details.temp_title_2.lab_num.SetString('')
        self.panel.temp_score_details.setVisible(True)

    def _close_btn_cb(self, *args):
        self.close()