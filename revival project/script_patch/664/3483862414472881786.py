# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/LobbyRecruimentEndAddFriend.py
from __future__ import absolute_import
from math import floor
from common.cfg import confmgr
from common.const import uiconst
from common.const.uiconst import NORMAL_LAYER_ZORDER_2
from common.uisys.basepanel import BasePanel
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import role_head_utils

class LobbyRecruimentEndAddFriend(BasePanel):
    PANEL_CONFIG_NAME = 'battle_recruit/battle_recruit_team_invite'
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    DLG_ZORDER = NORMAL_LAYER_ZORDER_2
    UI_ACTION_EVENT = {'btn_close.OnClick': 'on_back_to_lobby'
       }

    def process_event(self, is_bind):
        event_mgr = global_data.emgr
        e_event = {'app_resume_event': self.on_app_resume
           }
        if is_bind:
            event_mgr.bind_events(e_event)
        else:
            event_mgr.unbind_events(e_event)

    def on_init_panel(self, teammates_head_info, battle_type):
        battle_name = confmgr.get('battle_config', str(battle_type), 'cNameTID', default='')
        self.process_event(True)
        self.set_teammate_info(teammates_head_info, battle_name)
        self.panel.PlayAnimation('invite_show')
        self.panel.TimerAction(self.countdown, 20, interval=1, callback=self.close)

    def countdown(self, pass_time, **kwargs):
        self.panel.lab_title.SetString(get_text_by_id(83161) + '<color=0x509EFFFF>({}S)</color>'.format(20 - int(floor(pass_time))))

    def set_teammate_info(self, teammate_infos, battle_name):
        if len(teammate_infos) == 1:
            self.panel.temp_player2.setVisible(False)
        for idx, teammate_key in enumerate(teammate_infos):
            teammate_info = teammate_infos.get(teammate_key, {})
            self.set_single_teammate_info(getattr(self.panel, 'temp_player%d' % (idx + 1)), teammate_key, teammate_info, battle_name)

    def set_single_teammate_info(self, node, teammate_key, teammate_info, battle_name):
        player_name = teammate_info.get('char_name', '')
        head_frame = teammate_info.get('head_frame', '')
        head_photo = teammate_info.get('head_photo', '')
        dan_info = teammate_info.get('dan_info', '')
        node.name.SetString(player_name)
        node.mode.SetString(battle_name)
        role_head_utils.init_role_head(node.head, head_frame, head_photo)
        role_head_utils.set_role_dan(node.temp_tier, dan_info)

        @node.btn_invite.unique_callback()
        def OnClick(btn, touch, player_id=teammate_key):
            btn.SetEnable(False)
            btn.lab_invite.SetString(83163)
            global_data.player.req_add_friend(player_id)

    def on_back_to_lobby(self, btn, touch):
        self.close()

    def on_finalize_panel(self):
        super(LobbyRecruimentEndAddFriend, self).on_finalize_panel()
        self.process_event(False)
        self.panel.StopTimerAction()

    def on_app_resume(self):
        self.close()