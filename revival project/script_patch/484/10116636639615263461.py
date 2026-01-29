# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Settle/EndContinueUI.py
from __future__ import absolute_import
from __future__ import print_function
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER
from logic.gcommon.common_const import battle_const
from common.const import uiconst

class EndContinueUI(BasePanel):
    PANEL_CONFIG_NAME = 'end/end_continue'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    GLOBAL_EVENT = {'notify_begin_spectate_successfully': 'block_exit_btn'
       }
    UI_ACTION_EVENT = {'btn_watching.btn_common.OnClick': '_on_click_btn_watch',
       'btn_exit.btn_common.OnClick': '_on_click_btn_exit'
       }

    def on_init_panel(self, *args, **kwargs):
        self._exit_callback = None
        self._next_step_cb = None
        self._has_end_statistics = False
        self.quit_timer = None
        self.exit_btn_enabled = True
        self._exit_btn_in_next = False
        self.hide_main_ui(exceptions=('EndContinueUI', 'EndDeathReplayUI'))
        return

    def on_show_imp(self, group_num, replay_dict, exit_btn_callback=None, next_step_cb=None):
        print(('on_show_imp', replay_dict))
        self.clear_parameters()
        if exit_btn_callback:
            self._exit_callback = exit_btn_callback
            self._has_end_statistics = True
        else:
            self._has_end_statistics = False
        self._next_step_cb = next_step_cb
        if not self._exit_btn_in_next:
            self._exit_btn_in_next = callable(next_step_cb)
            self._refresh_exit_btn_lab()
        self.panel.setLocalZOrder(1)
        from logic.client.const import game_mode_const
        if not global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_SURVIVALS) and not global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_SNATCHEGG):
            self.panel.btn_watching.setVisible(False)
            self.panel.img_tips.setVisible(False)
        else:
            from logic.gcommon.common_utils.local_text import get_text_by_id
            self.panel.lab_survive.setString(get_text_by_id(6024).format('%d' % group_num))
            if global_data.player and global_data.player.logic:
                can_do_spectate = replay_dict.get('can_do_spectate', False) if replay_dict else False
                if can_do_spectate:
                    from logic.gutils.team_utils import is_all_death
                    teammate = global_data.player.logic.ev_g_groupmate()
                    if is_all_death(teammate):
                        self.panel.btn_watching.btn_common.SetText(19782)
                        self.panel.img_tips.setVisible(False)
                else:
                    self.panel.btn_watching.setVisible(False)
                    self.panel.img_tips.setVisible(False)

        def quit_count_down():
            self._on_click_btn_exit()

        from common.utils.timer import CLOCK
        self.quit_timer = global_data.game_mgr.register_logic_timer(quit_count_down, interval=90, times=1, mode=CLOCK)

    def _refresh_exit_btn_lab(self):
        if self._exit_btn_in_next:
            text_id = 80552
        else:
            text_id = 80376
        self.panel.btn_exit.btn_common.SetText(text_id)

    def on_finalize_panel(self):
        self.clear_parameters()
        self.show_main_ui()

    def clear_parameters(self):
        self._exit_callback = None
        self._next_step_cb = None
        if self.quit_timer:
            global_data.game_mgr.unregister_logic_timer(self.quit_timer)
            self.quit_timer = None
        return

    def block_exit_btn(self):
        self.exit_btn_enabled = False

    def _on_click_btn_exit(self, *args):
        if not self.exit_btn_enabled:
            return
        if self._exit_btn_in_next:
            self._on_click_btn_next()
        else:
            self._on_click_btn_exit_for_real()

    def _on_click_btn_next(self):
        if callable(self._next_step_cb):
            self._next_step_cb()
        self._exit_btn_in_next = False
        self._refresh_exit_btn_lab()

    def _on_click_btn_exit_for_real(self):
        if self._exit_callback:
            self._exit_callback()
        global_data.player.quit_battle()
        if not self._has_end_statistics:
            from logic.comsys.battle.Settle.SettleSystem import SettleSystem
            SettleSystem().close_all_dlg()
        self.close()

    def _on_click_btn_watch(self, *args):
        if global_data.player and global_data.player.logic:
            from logic.entities.Battle import Battle
            status = global_data.battle.battle_status
            if status in {Battle.BATTLE_STATUS_INIT, Battle.BATTLE_STATUS_PARACHUTE, Battle.BATTLE_STATUS_PREPARE}:
                global_data.game_mgr.show_tip(get_text_by_id(19847))
                return
            global_data.player.logic.send_event('E_REQ_SPECTATE')