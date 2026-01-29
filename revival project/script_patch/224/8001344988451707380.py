# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/ffa/FFAScoreDetailsUI.py
from __future__ import absolute_import
import six_ex
from common.cfg import confmgr
from common.utils.timer import CLOCK
from logic.gutils.role_head_utils import init_role_head, init_mecha_head
from bson.objectid import ObjectId
from common.const.uiconst import BASE_LAYER_ZORDER_1, UI_VKB_CLOSE
from common.uisys.basepanel import BasePanel

class FFAScoreDetailsUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_ffa/battle_ffa_score_details'
    DLG_ZORDER = BASE_LAYER_ZORDER_1
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'base_layer.OnClick': '_close_btn_cb'
       }
    GLOBAL_EVENT = {'update_score_details': 'update_score_details'
       }
    TEMP_PATH = {1: 'battle_ffa/i_score_details_1v1',2: 'battle_ffa/i_score_details_2v2'
       }

    def on_init_panel(self):
        self.init_parameters()
        self.init_panel()

    def on_finalize_panel(self):
        if self.get_details_timer:
            global_data.game_mgr.unregister_logic_timer(self.get_details_timer)
            self.get_details_timer = None
        return

    def init_panel(self):
        self.update_score_details(global_data.ffa_battle_data.get_score_details_data())

    def init_parameters(self):
        battle_conf = confmgr.get('battle_config')
        team_num = 1
        if global_data.battle:
            team_num = battle_conf.get(str(global_data.battle.battle_tid), {}).get('cTeamNum', 1)
        self.score_details_node = global_data.uisystem.load_template_create(self.TEMP_PATH.get(team_num), self.panel.nd_details_check, name='score_details_node')

        @self.score_details_node.btn_close.unique_callback()
        def OnClick(btn, touch):
            self._close_btn_cb()

        def update_details():
            if not (global_data.cam_lplayer and global_data.cam_lplayer.get_owner()):
                return
            bat = global_data.battle
            if not bat:
                return
            bat.call_soul_method('request_rank_data', (global_data.cam_lplayer.get_owner(),))

        update_details()
        self.get_details_timer = global_data.game_mgr.register_logic_timer(update_details, times=-1, interval=1, mode=CLOCK)

    def update_score_details(self, data):
        if not data:
            return
        if not global_data.cam_lplayer:
            return
        lst_nd = self.score_details_node.list_score
        lst_nd.SetInitCount(len(data))
        my_group_id = global_data.cam_lplayer.ev_g_group_id()
        my_eid = global_data.cam_lplayer.id
        for index, widget in enumerate(lst_nd.GetAllItem()):
            rank, group_id, group_point, dict_data = data[index]
            group_has_buff = False
            for e_index, soul_id in enumerate(six_ex.keys(dict_data)):
                soul_id, uid, name, head_photo, head_frame, kill_num, kill_mecha_num, points, has_buff, mecha_id, human_damage, mecha_damage = dict_data[soul_id]
                soul_id = ObjectId(soul_id)
                item_nd = getattr(widget, 'nd_player_%d' % (e_index + 1))
                nd_stat = getattr(item_nd, 'nd_stat%d' % (e_index + 1))
                if mecha_id:
                    init_mecha_head(item_nd.temp_head, head_frame, mecha_id)
                else:
                    init_role_head(item_nd.temp_head, head_frame, head_photo)
                item_nd.lab_name.SetString(name)
                nd_stat.lab_mech.SetString(str(kill_mecha_num))
                is_my = my_eid == soul_id
                item_nd.lab_name.SetColor('#DB' if is_my else '#SW')
                nd_stat.lab_mech.SetColor('#DB' if is_my else '#SW')
                group_has_buff = group_has_buff or has_buff

            is_my_group = my_group_id == group_id
            widget.lab_rank.SetString(str(rank))
            widget.lab_rank.SetColor('#SS' if is_my_group else '#SW')
            widget.lab_score.SetString(str(group_point))
            widget.lab_score.SetColor('#DB' if is_my_group else '#SW')
            widget.nd_self.setVisible(is_my_group)
            widget.nd_1st.setVisible(rank == 1)
            widget.nd_cover.setVisible(bool(index % 2))
            widget.img_buff_dps.setVisible(group_has_buff)

    def _close_btn_cb(self, *args):
        self.close()