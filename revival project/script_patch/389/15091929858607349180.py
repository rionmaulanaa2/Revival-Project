# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/ZombieFFA/ZombieFFAScoreDetailsUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const import uiconst
from common.utils.timer import CLOCK
from logic.gutils.role_head_utils import init_mecha_head

class ZombieFFAScoreDetailsUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_ffa/battle_ffa_score_details'
    DLG_ZORDER = uiconst.BASE_LAYER_ZORDER_1
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    GLOBAL_EVENT = {'zombieffa_update_socre_details': 'update_score_details'
       }
    UI_ACTION_EVENT = {'base_layer.OnClick': 'close'
       }

    def on_init_panel(self):
        self.init_parameters()
        self.update_score_details(global_data.zombieffa_battle_data.get_score_details_data())

    def on_finalize_panel(self):
        if self.get_details_timer:
            global_data.game_mgr.unregister_logic_timer(self.get_details_timer)
            self.get_details_timer = None
        return

    def init_parameters(self):
        TEMP_PATH = 'battle_ffa/i_score_details_1v1'
        self.score_details_node = global_data.uisystem.load_template_create(TEMP_PATH, self.panel.nd_details_check, name='score_details_node')
        self.show_top_point = global_data.game_mode.get_cfg_data('play_data').get('notify_top_points', 3)

        @self.score_details_node.btn_close.callback()
        def OnClick(btn, touch):
            self.close()

        def update_details():
            if not (global_data.cam_lplayer and global_data.cam_lplayer.get_owner()):
                return
            if not global_data.battle:
                return
            global_data.battle.request_rank_data()

        update_details()
        self.get_details_timer = global_data.game_mgr.register_logic_timer(update_details, times=-1, interval=1, mode=CLOCK)

    def update_score_details(self, data):
        my_group_id = global_data.cam_lplayer.ev_g_group_id()
        nd_list = self.score_details_node.list_score
        nd_list.SetInitCount(len(data))
        for idx, widget in enumerate(nd_list.GetAllItem()):
            rank, group_id, group_point, mecha_id, mem_data = data[idx]
            eid, uid, name, head_frame, kill_mecha_num, mecha_damage, has_enhanced_buff, mecha_dead_times = mem_data
            is_my_group = group_id == my_group_id
            widget.lab_rank.SetString(str(rank))
            init_mecha_head(widget.temp_head, head_frame, mecha_id)
            widget.lab_name.SetString(name)
            widget.lab_mech.SetString(str(kill_mecha_num))
            widget.lab_rank.SetColor('#SS' if is_my_group else '#SW')
            widget.lab_score.SetColor('#DB' if is_my_group else '#SW')
            widget.nd_self.setVisible(is_my_group)
            widget.nd_1st.setVisible(rank == 1 and group_point > self.show_top_point)
            widget.nd_cover.setVisible(bool(idx % 2))
            widget.img_buff_dps.setVisible(has_enhanced_buff)