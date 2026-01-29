# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/exercise_ui/ExerciseDPSInfoUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_2, BASE_LAYER_ZORDER
from logic.comsys.ui_distortor.MechaDistortHelper import MechaDistortHelper
import time
from common.const import uiconst

class ExerciseDPSInfoUI(MechaDistortHelper, BasePanel):
    PANEL_CONFIG_NAME = 'battle_train/fight_data'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {}
    IMG_MAN = 'Robot'
    IMG_MECHA = 'Mecha'
    IMG_MODEL = 'ExerciseTarget'
    target_type = ''
    TEXT_HIT = 5072
    TEXT_TIME = 5073
    TEXT_DAMAGE = 5074
    TEXT_COUNT = 5075
    CLEAR_TIME = 5.0
    TAG = 191119
    data_DPS = 0
    data_hit_rate = 0.0
    data_time = 0.0
    data_total_dagame = 0
    data_hit_count = 0
    t_start = -1
    fire_count = 0
    in_mecha = False
    TIME_MIN_SHOW = 0.01

    def on_init_panel(self, *args, **kwargs):
        super(ExerciseDPSInfoUI, self).on_init_panel(self, *args, **kwargs)
        self.init_ui_items()
        self.init_text()
        self.lplayer = None
        self.process_events(True)
        self.reset_data()
        return

    def init_ui_items(self):
        self.list_1.SetInitCount(2)
        self.ui_dps = self.list_1.GetItem(0)
        self.ui_hit_rate = self.list_1.GetItem(1)
        self.list_2.SetInitCount(3)
        self.ui_time = self.list_2.GetItem(0)
        self.ui_total_damage = self.list_2.GetItem(1)
        self.ui_hit_count = self.list_2.GetItem(2)

    def init_text(self):
        self.ui_dps.lab_title.SetString('DPS')
        self.ui_hit_rate.lab_title.SetString(self.TEXT_HIT)
        self.ui_time.lab_title.SetString(self.TEXT_TIME)
        self.ui_total_damage.lab_title.SetString(self.TEXT_DAMAGE)
        self.ui_hit_count.lab_title.SetString(self.TEXT_COUNT)

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'scene_camera_player_setted_event': self.on_cam_player_setted,
           'observer_module_changed_event': self.on_cam_player_setted,
           'scene_player_setted_event': self.on_player_setted
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def reset_data(self):
        self.data_DPS = 0
        self.data_hit_rate = 0.0
        self.data_time = 0.0
        self.data_total_dagame = 0
        self.data_hit_count = 0
        self.t_start = -1
        self.fire_count = 0
        self.hide()
        if not global_data.cam_lplayer:
            return
        if global_data.cam_lplayer.ev_g_in_mecha('Mecha'):
            self.in_mecha = True
        else:
            self.in_mecha = False

    def on_player_setted(self, lplayer):
        self.lplayer = lplayer
        lplayer.regist_event('E_TRY_SWITCH', self.on_switch_weapon)

    def on_switch_weapon(self, *args, **kwargs):
        self.reset_data()

    def on_cam_player_setted(self):
        if not global_data.cam_lplayer:
            return
        if global_data.cam_lplayer.ev_g_in_mecha('Mecha'):
            self.switch_to_mecha()
        else:
            self.switch_to_man()

    def switch_to_mecha(self):
        self.reset_data()
        self.in_mecha = True
        super(ExerciseDPSInfoUI, self).switch_to_mecha()

    def switch_to_man(self):
        self.reset_data()
        self.in_mecha = False
        super(ExerciseDPSInfoUI, self).switch_to_non_mecha()

    def update_data(self, data_dict):
        self.clear_show_count_dict()
        self.restart_clear_timer()
        target_type = data_dict.get('target_type', None)
        self.switch_icon(target_type)
        damage = data_dict.get('damage', 0)
        self.data_total_dagame += damage
        self.ui_total_damage.lab_data.SetString(str(self.data_total_dagame))
        if damage != 0:
            self.data_hit_count += 1
        self.ui_hit_count.lab_data.SetString(str(self.data_hit_count))
        if self.t_start == -1:
            self.t_start = time.time()
            self.ui_time.lab_data.SetString('-')
        else:
            t_stop = time.time()
            pass_time = t_stop - self.t_start
            self.t_start = t_stop
            self.data_time += pass_time
            if self.data_time < self.TIME_MIN_SHOW:
                self.ui_time.lab_data.SetString('-')
            else:
                self.ui_time.lab_data.SetString(str(self.format_two_digit_float(self.data_time)) + 's')
        if self.data_time < self.TIME_MIN_SHOW:
            self.ui_dps.lab_data.SetString('-')
        else:
            self.data_DPS = int(self.data_total_dagame / self.data_time)
            self.ui_dps.lab_data.SetString(str(self.data_DPS))
        if self.in_mecha:
            self.ui_hit_rate.lab_data.SetString('-')
        else:
            self.fire_count += 1
            self.data_hit_rate = float(self.data_hit_count) / self.fire_count
            self.ui_hit_rate.lab_data.SetString(self.format_percentage_int(self.data_hit_rate))
        return

    def restart_clear_timer(self):

        def hide_act():
            self.reset_data()

        self.panel.SetTimeOut(self.CLEAR_TIME, hide_act, tag=self.TAG)

    def switch_icon(self, target_type):
        if self.target_type != target_type:
            self.img_man.setVisible(target_type in (self.IMG_MAN, self.IMG_MODEL))
            self.img_mech.setVisible(target_type == self.IMG_MECHA)
            self.reset_data()
            self.target_type = target_type
            self.show()

    def format_two_digit_float(self, data):
        if isinstance(data, float):
            result = '%.2f' % data
            return result
        else:
            return None
            return None

    def format_percentage_int(self, data):
        if isinstance(data, float):
            result = str(int(data * 100)) + '%'
            return result
        else:
            return None
            return None

    def on_finalize_panel(self):
        self.reset_data()
        self.process_events(False)
        if self.lplayer:
            self.lplayer.unregist_event('E_TRY_SWITCH', self.reset_data())
        super(ExerciseDPSInfoUI, self).on_finalize_panel()