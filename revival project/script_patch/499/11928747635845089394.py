# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVETeamTeleportWidget.py
from __future__ import absolute_import
from common.utils.timer import CLOCK
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.time_utility import get_server_time

class PVETeamTeleportWidget(object):

    def __init__(self, panel):
        self.panel = panel
        self.init_params()
        self.init_widget()
        self.process_events(True)

    def init_params(self):
        self.widget = None
        self.timer_id = None
        self.ts = 39
        return

    def process_events(self, is_bind):
        econf = {'pve_teleport_ts_event': self.show_tips,
           'pve_teammate_confirm_teleport': self.on_add_confirm,
           'scene_camera_player_setted_event': self.on_cam_lplayer_setted
           }
        global_data.emgr.bind_events(econf) if is_bind else global_data.emgr.unbind_events(econf)

    def clear(self):
        self.widget and self.widget.setVisible(False)
        self.reset_timer()

    def destroy(self):
        self.clear()
        self.init_params()
        self.process_events(False)
        self.panel = None
        return

    def init_widget(self):
        self.widget = global_data.uisystem.load_template_create('battle_tips/pve/i_pve_tips_team_next_level', self.panel)
        self.widget.setVisible(False)

        @self.widget.btn_confirm.unique_callback()
        def OnClick(*args):
            self.on_click_confirm()

    def on_cam_lplayer_setted(self):
        if global_data.cam_lplayer and global_data.player and global_data.cam_lplayer.id == global_data.player.id:
            self.widget and self.widget.btn_confirm.setVisible(True)
        else:
            self.widget and self.widget.btn_confirm.setVisible(False)

    def show_tips(self, ts, show_self=True):
        if not self.widget:
            return
        if global_data.cam_lplayer and global_data.cam_lplayer.id == global_data.player.id and show_self:
            self.widget and self.widget.btn_confirm.setVisible(True)
        else:
            self.widget and self.widget.btn_confirm.setVisible(False)
        time_ts = get_server_time()
        self.ts = ts - time_ts
        self.widget.setVisible(True)
        self.widget.PlayAnimation('show')
        self.init_timer()

    def is_showing(self):
        return self.widget and self.widget.isValid() and self.widget.isVisible() and self.widget.btn_confirm.isVisible()

    def on_add_confirm(self, confirm_count, alive_count):
        self.widget.lab_text_2.SetString(get_text_by_id(495).format(confirm_count, alive_count))

    def init_timer(self):
        self.reset_timer()
        self.timer_id = global_data.game_mgr.register_logic_timer(self.tick_timer, 1.0, None, int(self.ts), CLOCK)
        return

    def reset_timer(self):
        if self.timer_id:
            global_data.game_mgr.unregister_logic_timer(self.timer_id)
            self.timer_id = None
        return

    def tick_timer(self, *args):
        self.ts -= 1
        self.widget.lab_text.SetString(get_text_by_id(496).format(int(self.ts)))
        if self.ts <= 0:
            self.reset_timer()
            self.widget.setVisible(False)

    def on_click_confirm(self, *args):
        ret_box = global_data.emgr.pve_get_box_tracked_event.emit()[0]
        ret_shop = global_data.emgr.pve_get_shop_tracked_event.emit()[0]
        print ret_box
        print ret_shop
        from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2

        def on_confirm():
            global_data.battle.try_enter_next_level()
            global_data.sound_mgr.post_event_2d_non_opt('Play_ui_pve_transfer', None)
            self.widget and self.widget.btn_confirm.setVisible(False)
            return

        def on_cancel():
            pass

        if ret_box or ret_shop:
            SecondConfirmDlg2(parent=self.panel).confirm(content=get_text_by_id(83496), cancel_text=19001, cancel_callback=on_confirm, confirm_text=19002, confirm_callback=on_cancel)
        else:
            global_data.battle.try_enter_next_level()