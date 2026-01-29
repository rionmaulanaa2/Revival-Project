# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/MutiOccupy/MutiOccupyBornChooseUI.py
from __future__ import absolute_import
import six
from six.moves import range
from common.const.uiconst import BASE_LAYER_ZORDER, UI_VKB_NO_EFFECT
from common.uisys.basepanel import BasePanel
from common.utils.timer import CLOCK
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.role_head_utils import get_head_photo_res_path, get_role_default_photo
from common.const import uiconst
from logic.gcommon.common_const.battle_const import STATE_OCCUPY_EMPTY, STATE_OCCUPY_SELF, STATE_OCCUPY_ENEMY, STATE_OCCUPY_SNATCH, OCCUPY_POINT_STATE_IDLE, OCCUPY_POINT_STATE_DEC, OCCUPY_POINT_STATE_INC
from logic.comsys.battle.MutiOccupy.MutiOccupyPoint import TICK_TIME, PROG_ADD, PROG_SCALE
BTN_TO_TEXT = {0: get_text_by_id(17458),
   1: get_text_by_id(17459),
   2: get_text_by_id(17460),
   3: get_text_by_id(17461)
   }

class MutiOccupyBornChooseUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_control/i_control_map_choose'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_NO_EFFECT
    MOUSE_CURSOR_TRIGGER_SHOW = True

    def on_init_panel(self):
        self.init_parameters()
        self.init_panel()
        self.init_btn_event()
        self.process_event(True)
        self.update_occupy_point_state()

    def on_finalize_panel(self):
        self.born_data_dict = {}
        self.process_event(False)

    def init_panel(self):
        self.panel.nd_content.setVisible(not bool(global_data.ui_mgr.get_ui('DeathBeginCountDown')))
        self.panel.list_btn.SetInitCount(4)
        self.btn_list = self.panel.list_btn.GetAllItem()
        self.panel.lab_tips.SetString(get_text_by_id(17347))

    def init_parameters(self):
        self.chooose_idx = -1
        self.born_data_dict = {}
        self.btn_timer = None
        for idx in range(3):
            self.born_data_dict[idx + 1] = getattr(self.panel, 'temp_item%d' % (idx + 1))
            self.born_data_dict[idx + 1].nd_vx.setVisible(False)

        return

    def init_btn_event(self):
        for idx in range(len(self.btn_list)):
            btn = self.btn_list[idx]
            btn.btn_confirm.SetText(BTN_TO_TEXT.get(idx))
            btn.btn_confirm.BindMethod('OnClick', lambda b, t, idx=idx: self.send_born_data(idx))

    def check_can_revive(self, idx):
        if not global_data.death_battle_data:
            return False
        occupy_data = global_data.death_battle_data.occupy_data
        server_data = occupy_data[idx].get_occupy_server_data()
        group_id = server_data.get('group_id', 0)
        is_occupy = server_data.get('is_occupy', False)
        if group_id == STATE_OCCUPY_SELF and is_occupy:
            return True

    def send_born_data(self, idx):
        player = global_data.player
        if not player:
            return
        if idx != 0:
            if not self.check_can_revive(idx):
                global_data.game_mgr.show_tip(get_text_by_id(17346))
        bat = player.get_battle() or player.get_joining_battle()
        bat and bat.start_combat(idx)

    def update_btn_state(self):
        self.is_can_revive(True)

    def is_can_revive(self, state):
        self.panel.nd_content.setVisible(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_occupy_point_state': self.update_occupy_point_state,
           'death_count_down_over': self.update_btn_state
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def update_occupy_point_state(self):
        if not global_data.death_battle_data:
            return
        occupy_data = global_data.death_battle_data.occupy_data
        for part_id, occupy in six.iteritems(occupy_data):
            server_data = occupy.get_occupy_server_data()
            base_data = occupy.get_occupy_base_data()
            group_id = server_data.get('group_id', 0)
            is_occupy = server_data.get('is_occupy', False)
            progress = server_data.get('progress', 0)
            born_item = self.born_data_dict[part_id]
            if not group_id == STATE_OCCUPY_SELF or not is_occupy:
                born_item.nd_vx.setVisible(False)
                if self.chooose_idx == part_id:
                    self.chooose_idx = -1
            if group_id == STATE_OCCUPY_SELF and is_occupy == True:
                born_item.img_prog_blue.setVisible(True)
                born_item.img_prog_red.setVisible(False)
                prog_nd = born_item.img_prog_blue
                born_item.nd_vx.setVisible(True)
                born_item.PlayAnimation('choose')
            elif group_id == STATE_OCCUPY_ENEMY and is_occupy == True:
                born_item.img_prog_blue.setVisible(False)
                born_item.img_prog_red.setVisible(True)
                prog_nd = born_item.img_prog_red
                born_item.nd_vx.setVisible(False)
                born_item.StopAnimation('choose')
            else:
                born_item.img_prog_blue.setVisible(False)
                born_item.img_prog_red.setVisible(False)
                prog_nd = born_item.img_prog_red
                born_item.nd_vx.setVisible(False)
                born_item.StopAnimation('choose')
            if group_id == STATE_OCCUPY_SELF and is_occupy:
                self.btn_list[part_id].btn_confirm.SetEnable(True)
            else:
                self.btn_list[part_id].btn_confirm.SetEnable(False)