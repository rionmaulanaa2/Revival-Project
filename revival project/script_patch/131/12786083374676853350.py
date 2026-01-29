# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/NBomb/NBombCoreCollectUI.py
from __future__ import absolute_import
import six
import math
from common.uisys.basepanel import BasePanel
import cc
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.comsys.battle.NBomb.NBombBattleDefines import POWER_CORE_ID_LST, GROUP_IDX_2_ICON, CORE_CIRCLE_MAP_FRAME, NBOMB_INSTALL_TOTAL_TIME, COLLECT_BTN_ICON
from logic.gcommon import time_utility as tutil
from common.cfg import confmgr
from common.const import uiconst
from logic.gcommon.cdata.status_config import ST_USE_ITEM
from logic.gcommon.cdata.mecha_status_config import MC_USE_ITEM
from logic.comsys.battle.NBomb import nbomb_utils

class NBombCoreCollectUI(BasePanel):
    START_BTN_TAG = 1001
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    PANEL_CONFIG_NAME = 'battle_bomb/i_battle_bomb_collection'
    HOT_KEY_FUNC_MAP = {'nbomb_device_place': 'quick_nbomb_count_down'
       }
    HOT_KEY_FUNC_MAP_SHOW = {'nbomb_device_place': {'node': 'btn_start.temp_pc'}}

    def on_init_panel(self):
        self.panel.btn_start.BindMethod('OnClick', self.on_start_nbomb_count_down)
        self.init_place_btn_frame()
        self.init_nbomb_core_list()
        self.update_nbomb_core_btn()
        self.update_act = None
        return

    def on_finalize_panel(self):
        self.update_act = None
        return

    def init_nbomb_core_list(self):
        self.panel.list_item.SetInitCount(len(POWER_CORE_ID_LST))
        cnt = len(POWER_CORE_ID_LST)
        for i in range(cnt):
            item = self.panel.list_item.GetItem(i)

            @item.btn_item.unique_callback()
            def OnClick(btn, touch, idx=i):
                wpos = touch.getLocation()
                lobby_item_id = confmgr.get('item', str(POWER_CORE_ID_LST[idx]), 'lobby_item_id')
                global_data.emgr.show_item_desc_ui_event.emit(lobby_item_id, None, directly_world_pos=wpos)
                return

    def init_place_btn_frame(self):
        btn_frames = [
         'gui/ui_res_2/common/button/btn_secondary_middle.png',
         'gui/ui_res_2/common/button/btn_secondary_middle.png',
         'gui/ui_res_2/common/button/btn_secondary_useless.png']
        self.btn_start.SetFrames('', btn_frames)

    def set_place_btn_gray(self, is_gray):
        normal_frame = 'gui/ui_res_2/common/button/btn_secondary_middle.png'
        gray_frame = 'gui/ui_res_2/common/button/btn_secondary_useless.png'
        btn_frame = gray_frame if is_gray else normal_frame
        self.btn_start.SetFrames('', [btn_frame, btn_frame, btn_frame])

    def update_btn_frames(self, btn, core_config_id, enable):
        btn_frame_dict = COLLECT_BTN_ICON[core_config_id]
        btn_frame = btn_frame_dict['normal'] if enable else btn_frame_dict['disable']
        btn.SetFrames('', [btn_frame, btn_frame, btn_frame])

    def update_nbomb_core_btn(self, core_exchange_info=None):
        self.update_start_btn_state()
        cnt = len(POWER_CORE_ID_LST)
        own_core_info = global_data.nbomb_battle_data.get_own_team_core_info()
        for i in range(cnt):
            item = self.panel.list_item.GetItem(i)
            core_config_id = POWER_CORE_ID_LST[i]
            player_id = own_core_info[core_config_id]
            own = player_id != 0
            self.update_btn_frames(item.btn_item, core_config_id, own)
            teammate = global_data.cam_lplayer.ev_g_groupmate() if global_data.cam_lplayer else []
            is_teammate = player_id in (teammate or [])
            icon_idx = teammate.index(player_id) if is_teammate else -1
            item.icon_teammate.setVisible(own and icon_idx != -1)
            icon_idx != -1 and item.icon_teammate.SetDisplayFrameByPath('', GROUP_IDX_2_ICON[icon_idx])
            EMENY_VX_PATH = 'gui/ui_res_2/battle/map/icon_bigrecourse_ball_anim.png'
            vx_path = CORE_CIRCLE_MAP_FRAME[core_config_id] if is_teammate else EMENY_VX_PATH
            item.vx_light_0.SetDisplayFrameByPath('', vx_path)
            item.vx_light_1.SetDisplayFrameByPath('', vx_path)
            if core_exchange_info:
                if core_config_id in core_exchange_info:
                    ani_name = 'show_team' if is_teammate else 'show'
                    item.PlayAnimation(ani_name)

    def quick_nbomb_count_down(self, msg, keycode):
        self.on_start_nbomb_count_down(None, None)
        return

    def on_start_nbomb_count_down(self, btn, touch):
        if not nbomb_utils.is_data_ready():
            return
        if not global_data.player or not global_data.player.logic.ev_g_status_check_pass(ST_USE_ITEM):
            return
        control_target = global_data.player.logic.ev_g_control_target()
        if control_target and control_target.logic:
            target_type = control_target.logic.__class__.__name__
            if target_type == 'LMecha':
                if not control_target.logic.ev_g_status_check_pass(MC_USE_ITEM):
                    return
            elif target_type == 'LMechaTrans':
                if control_target.logic.ev_g_shape_shift() and not control_target.logic.ev_g_status_check_pass(MC_USE_ITEM):
                    return
            elif target_type == 'LMotorcycle':
                if not control_target.logic.ev_g_status_check_pass(MC_USE_ITEM):
                    return
        is_installing, _ = self.get_install_time()
        if is_installing:
            global_data.battle.call_soul_method('cancel_nbomb_confirm', ())
        else:
            global_data.battle.call_soul_method('start_nbomb_confirm', ())

    def get_install_time(self):
        end_time = global_data.nbomb_battle_data.get_nbomb_install_timestamp()
        cur_time = tutil.get_server_time()
        delta_time = max(end_time - cur_time, 0)
        is_installing = end_time > 0 and delta_time > 0
        return (
         is_installing, delta_time)

    def update_install_btn_state(self):
        is_self_install = global_data.nbomb_battle_data.get_nbomb_install_player_id() == global_data.player.id
        is_installing, delta_time = self.get_install_time()
        start_content = get_text_by_id(18303)
        recall_content = get_text_by_id(18304, {'countdown': math.ceil(delta_time)})
        self.panel.btn_start.SetText(recall_content if is_installing else start_content)
        self.panel.prog_btn.setVisible(is_installing and is_self_install)
        is_self_install and self.panel.prog_btn.SetPercentage(100.0 * delta_time / NBOMB_INSTALL_TOTAL_TIME)
        if delta_time <= 0:
            self.stop_timer()
        is_show_tips = is_installing and delta_time > 0
        self.show_tips_ui(is_show_tips, is_self_install)

    def show_tips_ui(self, is_show, is_self_install=None):
        if is_show:
            ui = global_data.ui_mgr.show_ui('NBombStartReadyUI', 'logic.comsys.battle.NBomb')
            ui.set_sub_title(get_text_by_id(18357) if is_self_install else '')
        else:
            global_data.ui_mgr.close_ui('NBombStartReadyUI')

    def update_start_btn_state(self):
        lplayer = global_data.player.logic
        is_installing, _ = self.get_install_time()
        is_self_install = global_data.nbomb_battle_data.get_nbomb_install_player_id() == global_data.player.id
        can_click = not is_installing or is_self_install
        is_all_collect = global_data.nbomb_battle_data.is_collect_all_core()
        is_not_in_spectate = not (lplayer and lplayer.ev_g_is_in_spectate())
        is_enable = can_click and is_all_collect and is_not_in_spectate
        self.panel.btn_start.SetEnable(is_enable)
        is_normal_frame = not is_installing and is_all_collect and is_not_in_spectate
        self.set_place_btn_gray(not is_normal_frame)

    def on_start_install_nbomb(self):
        self.update_start_btn_state()
        self.update_install_btn_state()
        self.register_timer()

    def on_stop_install_nbomb(self):
        self.stop_timer()
        self.update_start_btn_state()
        self.update_install_btn_state()

    def count_down(self):
        self.update_install_btn_state()

    def stop_timer(self):
        if self.update_act:
            self.panel.stopActionByTag(self.START_BTN_TAG)
            self.update_act = None
        return

    def register_timer(self):
        is_installing, _ = self.get_install_time()
        if self.update_act and not is_installing:
            return
        self.update_act = self.panel.runAction(cc.RepeatForever.create(cc.Sequence.create([
         cc.DelayTime.create(0.1),
         cc.CallFunc.create(self.count_down)])))
        self.update_act.setTag(self.START_BTN_TAG)