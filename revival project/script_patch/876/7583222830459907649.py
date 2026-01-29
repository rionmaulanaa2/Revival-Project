# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Improvise/ImproviseScoreDetailsUI.py
from __future__ import absolute_import
import six
from six.moves import range
from common.const.uiconst import BASE_LAYER_ZORDER_1, UI_VKB_CLOSE
from common.uisys.basepanel import BasePanel
from common.utils.timer import CLOCK
from logic.gutils.role_head_utils import get_head_photo_res_path, get_role_default_photo, get_mecha_photo

class ImproviseScoreDetailsUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_3v3/3v3_score_detials'
    DLG_ZORDER = BASE_LAYER_ZORDER_1
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'base_layer.OnClick': '_close_btn_cb',
       'btn_close.OnClick': '_close_btn_cb'
       }
    GLOBAL_EVENT = {'update_score_details': 'update_score_details'
       }

    def on_init_panel(self):
        self._init_parameters()
        self._init_panel()

    def on_finalize_panel(self):
        if self.get_details_timer:
            global_data.game_mgr.unregister_logic_timer(self.get_details_timer)
        self.get_details_timer = None
        return

    def _init_parameters(self):

        def update_details():
            bat = global_data.battle
            bat and bat.request_rank_data()

        self.get_details_timer = global_data.game_mgr.register_logic_timer(update_details, times=-1, interval=1, mode=CLOCK)
        update_details()
        self.update_score_details(global_data.improvise_battle_data.get_score_details_data())

    def _init_panel(self):
        pass

    def _close_btn_cb(self, *args):
        self.close()

    def update_score_details(self, data):
        self_lplayer = global_data.cam_lplayer
        if self_lplayer is None:
            return
        else:
            self_group_id = self_lplayer.ev_g_group_id()
            for group_id, _ in six.iteritems(data):
                if group_id != self_group_id:
                    oppo_group_id = group_id
                    break
            else:
                oppo_group_id = None

            self.update_group_score_details(self.panel.temp_score_details.nd_blue.list_score, data.get(self_group_id, []), self_group_id)
            self.update_group_score_details(self.panel.temp_score_details.nd_red.list_score, data.get(oppo_group_id, []), oppo_group_id)
            return

    def update_group_score_details(self, list_node, details_list, group_id):
        group_hp_dict = global_data.improvise_battle_data.get_group_hp_dict()
        single_group_hp_data = group_hp_dict.get(group_id, {})
        list_node.SetInitCount(len(details_list))
        for i in range(len(details_list)):
            item = list_node.GetItem(i)
            details = details_list[i]
            pid, name, is_alive, kill_num, kill_mecha_num, role_id, is_mvp, assist_total, called_mecha_id, score = details
            hp_data = single_group_hp_data.get(pid, {})
            item.lab_name.SetString(name)
            item.img_die.setVisible(not is_alive)
            item.lab_kill.SetString(str(kill_num))
            item.lab_mech.SetString(str(assist_total))
            if is_mvp:
                item.lab_score.setVisible(False)
                item.img_mvp.setVisible(True)
                path = 'gui/ui_res_2/fight_end/img_mvp1.png'
                item.img_mvp.SetDisplayFrameByPath('', path)
                item.lab_score2.SetString('%.1f' % float(score))
            else:
                item.lab_score.setVisible(True)
                item.lab_score.SetString('%.1f' % float(score))
                item.img_mvp.setVisible(False)
            mecha_type_id = hp_data.get('in_mecha_type', 0)
            in_mecha = mecha_type_id > 0
            if in_mecha:
                photo_no = get_mecha_photo(mecha_type_id)
            else:
                photo_no = get_role_default_photo(role_id)
            avatar_icon_path = get_head_photo_res_path(photo_no)
            item.temp_role.frame_head.img_head.SetDisplayFrameByPath('', avatar_icon_path)