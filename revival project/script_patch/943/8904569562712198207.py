# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/MechaBuffUI.py
from __future__ import absolute_import
import six_ex
import six
from common.uisys.basepanel import BasePanel
from common.const.uiconst import BASE_LAYER_ZORDER
from logic.gcommon.common_const.ui_operation_const import WEAPON_BAR_LOCAL_ZORDER
from common.const import uiconst

class MechaBuffUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_mech/fight_mech_buff'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {}
    SHOW_BUFF_ID = [
     334, 335, 336, 407]

    def on_init_panel(self):
        self.panel.setLocalZOrder(WEAPON_BAR_LOCAL_ZORDER)
        self.buff_temp = global_data.uisystem.load_template('battle_mech/i_mech_buff')
        self.init_parameters()

    def on_finalize_panel(self):
        self.bind_event(False)
        self.remove_all_buff()

    def enter_screen(self):
        super(MechaBuffUI, self).enter_screen()
        self.init_parameters()
        self.bind_event(True)
        self.init_buff()

    def leave_screen(self):
        super(MechaBuffUI, self).leave_screen()
        self.on_finalize_panel()

    def init_parameters(self):
        self.buff_dict = {}
        self.cur_cam_target_id = None
        return

    def bind_event(self, is_bind):
        econf = {'battle_add_mecha_buff': self.add_buff,
           'battle_remove_mecha_buff': self.remove_buff,
           'scene_camera_player_setted_event': self.on_camera_player_setted
           }
        emgr = global_data.emgr
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def remove_all_buff(self):
        for b_id in six_ex.keys(self.buff_dict):
            self.remove_buff(b_id)

    def add_buff(self, buff_id, remain_time, add_time, duration):
        if buff_id not in self.SHOW_BUFF_ID:
            return
        from common.cfg import confmgr
        conf = confmgr.get('c_buff_data', str(buff_id))
        self.add_common_buff(buff_id, conf, duration, add_time)

    def add_common_buff(self, buff_id, conf, duration, add_time):
        from logic.gcommon import time_utility
        icon_bar = conf.get('IconPath', None)
        if not icon_bar:
            return
        else:
            progress_bar = conf.get('ProgressPath', 'gui/ui_res_2/battle/buff/buff_progress_yellow.png')
            nd_progress = None
            buff_item_list = self.panel.list_buff
            if buff_id in self.buff_dict:
                nd_progress = self.buff_dict[buff_id]
            else:
                nd_progress = buff_item_list.AddItem(self.buff_temp)
            progress = nd_progress.progress_buff
            progress.SetProgressTexture(progress_bar)
            bar = nd_progress.bar
            bar.SetDisplayFrameByPath('', icon_bar)
            pass_time = time_utility.get_server_time() - add_time
            remain_time = duration - pass_time
            if duration and remain_time > 0:

                def finish():
                    idx = buff_item_list.getIndexByItem(nd_progress)
                    buff_item_list.DeleteItemIndex(idx)
                    del self.buff_dict[buff_id]

                def update_progress_time(dt):
                    _remain_time = duration - (time_utility.get_server_time() - add_time)
                    progress.setPercentage(_remain_time / duration * 100)

                progress.stopAllActions()
                progress.TimerAction(update_progress_time, remain_time, callback=finish, interval=0.05)
            self.buff_dict[buff_id] = nd_progress
            return

    def remove_buff(self, buff_id, *args):
        if buff_id not in self.SHOW_BUFF_ID:
            return
        if buff_id in self.buff_dict:
            nd_progress = self.buff_dict[buff_id]
            nd_progress.stopAllActions()
            buff_item_list = self.panel.list_buff
            idx = buff_item_list.getIndexByItem(nd_progress)
            buff_item_list.DeleteItemIndex(idx)
            del self.buff_dict[buff_id]

    def on_camera_player_setted(self, *args):
        if global_data.cam_lplayer is None:
            self.remove_all_buff()
        elif global_data.cam_lplayer.id != self.cur_cam_target_id:
            self.remove_all_buff()
            self.cur_cam_target_id = global_data.cam_lplayer.id
        return

    def init_buff(self, *args):
        self.remove_all_buff()
        if not global_data.cam_lplayer:
            return
        control_target = global_data.cam_lplayer.ev_g_control_target()
        if not control_target and control_target.logic:
            return
        target_type = control_target.__class__.__name__
        if target_type != 'Mecha':
            return
        from logic.gcommon import time_utility
        buffs = control_target.logic.ev_g_get_buff_data() or {}
        for buff_key_set in six.itervalues(buffs):
            for buff_id, buff_id_set in six.iteritems(buff_key_set):
                for data in six.itervalues(buff_id_set):
                    duration = data.get('duration', 0)
                    duration = 100000
                    if duration:
                        add_time = data.get('add_time', 0)
                        left_time = add_time + duration - time_utility.get_server_time()
                        left_time = duration if left_time > duration else left_time
                        self.add_buff(buff_id, left_time, add_time)