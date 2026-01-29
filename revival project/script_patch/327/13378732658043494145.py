# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/King/KingBattleReviveUI.py
from __future__ import absolute_import
from common.cfg import confmgr
from common.uisys.basepanel import BasePanel
from common.const.uiconst import BASE_LAYER_ZORDER
from logic.gutils.item_utils import get_gun_pic_by_item_id
from logic.gcommon.ctypes.FightData import FD_MAKER_SOUL, FD_MAKER_MECHA, FD_MAKER_MONSTER
CAMP_ICON_PATH = 'gui/ui_res_2/battle_koth/stat/'

class KingBattleReviveUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_koth/koth_revive'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_ACTION_EVENT = {'temp_revive.btn_close.OnClick': 'on_click_close_btn'
       }

    def on_init_panel(self):
        self.init_parameters()
        self.init_event()
        self.hide_main_ui()

    def on_finalize_panel(self):
        self.unbind_events()
        self.panel.nd_time.StopTimerAction()
        self.acts = None
        self.show_main_ui()
        return

    def init_parameters(self):
        self.left_time = None
        self.acts = None
        return

    def init_event(self):
        self.bind_events()

    def on_delay_close(self, revive_time):
        self.left_time = revive_time

        def refresh_time(pass_time):
            self.left_time = revive_time - pass_time
            left_time = int(self.left_time)
            if left_time <= 5 and self.acts is None:
                self.acts = self.panel.PlayAnimation('count')
            self.panel.lab_time.SetString('%dS' % left_time)
            self.panel.lab_time_dec.SetString('%dS' % left_time)
            return

        def refresh_time_finsh():
            self.panel.lab_time.SetString('0S')
            self.panel.lab_time_dec.SetString('0S')
            self.close()

        self.panel.nd_time.StopTimerAction()
        self.panel.nd_time.TimerAction(refresh_time, revive_time, callback=refresh_time_finsh)

    def on_show_defeat_info(self, killer_id, kill_info):
        temp_revive = self.panel.temp_revive.nd_revive_view
        maker_type = kill_info.get('maker_type', None)
        if maker_type is None:
            temp_revive.setVisible(False)
            return
        else:
            if maker_type == FD_MAKER_MONSTER:
                temp_revive.nd_method.nd_mech.setVisible(False)
                temp_revive.nd_method.nd_human.setVisible(False)
                temp_revive.nd_enemy.camp_icon.setVisible(False)
                temp_revive.nd_enemy.lab_name.SetString(18549)
                temp_revive.nd_score.lab_name.SetString(str(0))
            else:
                killer_name = kill_info['trigger_name']
                points = kill_info['points']
                trigger_faction = kill_info['trigger_faction']
                side = global_data.king_battle_data.get_side_by_faction_id(trigger_faction)
                if side == 1:
                    camp_path = CAMP_ICON_PATH + 'img_icon_enemy1.png'
                else:
                    camp_path = CAMP_ICON_PATH + 'img_icon_enemy2.png'
                temp_revive.nd_enemy.camp_icon.SetDisplayFrameByPath('', camp_path)
                temp_revive.nd_enemy.lab_name.SetString(str(killer_name))
                temp_revive.nd_score.lab_name.SetString(str(points))
            if maker_type == FD_MAKER_MECHA:
                mecha_conf = confmgr.get('mecha_conf', 'UIConfig', 'Content')
                mecha_id = kill_info.get('mecha_id')
                conf = mecha_conf[str(mecha_id)]
                icon_path = conf.get('icon_path', [])
                temp_revive.nd_method.nd_human.setVisible(False)
                temp_revive.nd_method.nd_mech.setVisible(True)
                temp_revive.nd_method.nd_mech.img_mech.SetDisplayFrameByPath('', icon_path[0])
            elif maker_type == FD_MAKER_SOUL:
                item_id = kill_info.get('item_id')
                if item_id:
                    gun_path = get_gun_pic_by_item_id(item_id)
                    temp_revive.nd_method.nd_human.img_gun.SetDisplayFrameByPath('', gun_path)
                else:
                    log_error('no item_id in kill info in event target_defeated_event')
                temp_revive.nd_method.nd_mech.setVisible(False)
                temp_revive.nd_method.nd_human.setVisible(True)
            return

    def bind_events(self):
        if global_data.player and global_data.player.logic:
            func = global_data.player.logic.regist_event
            func('E_START_BE_RESCUE', self.start_rescue)
            func('E_STOP_RESCUE', self.stop_rescue, 100)
            func('E_ON_SAVED', self.on_saved, 100)
            func('E_REVIVE', self.on_saved, 100)

    def unbind_events(self):
        if global_data.player and global_data.player.logic:
            func = global_data.player.logic.unregist_event
            func('E_START_BE_RESCUE', self.start_rescue)
            func('E_STOP_RESCUE', self.stop_rescue)
            func('E_ON_SAVED', self.on_saved)
            func('E_REVIVE', self.on_saved)

    def start_rescue(self, *args):
        if self.left_time is None:
            return
        else:
            self.panel.nd_time.StopTimerAction()
            if self.acts:
                func = self.panel.getActionManager().pauseTarget
                func(self.panel.tip.get())
                func(self.panel.lab_time_dec.get())
                func(self.panel.lab_time.get())
            return

    def stop_rescue(self, *args):
        if self.left_time is None:
            return
        else:
            if global_data.player and global_data.player.logic:
                if global_data.player.logic.ev_g_rescue_groupmate_num() == 0:
                    if self.acts:
                        func = self.panel.getActionManager().resumeTarget
                        func(self.panel.tip.get())
                        func(self.panel.lab_time_dec.get())
                        func(self.panel.lab_time.get())
                    self.on_delay_close(self.left_time)
            else:
                self.close()
            return

    def on_click_close_btn(self, *args):
        self.panel.nd_playback.setVisible(False)

    def on_saved(self, *args):
        self.close()