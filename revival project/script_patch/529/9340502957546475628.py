# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/ParachuteInviteFollowUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import TOP_ZORDER
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_utils import parachute_utils
import cc
from common.const import uiconst

class ParachuteInviteFollowUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_before/follow_invite'
    DLG_ZORDER = TOP_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_agree.OnClick': 'agree',
       'btn_reject.OnClick': 'reject',
       'btn_tick.OnEnd': 'refuse_receive'
       }
    ID_PIC_PATH = [
     'gui/ui_res_2/battle_before/pnl_invitation_no1.png',
     'gui/ui_res_2/battle_before/pnl_invitation_no2.png',
     'gui/ui_res_2/battle_before/pnl_invitation_no3.png']
    COUNT_DOWN_TAG = 202010

    def on_init_panel(self, *args):
        self.inviter_eid = None
        self.inviter_name = 'Secret'
        self.block_inviter = False
        self.is_assign = False
        self.panel.PlayAnimation('appear')
        return

    def update_count_down(self):
        if global_data.cam_lplayer:
            player = global_data.cam_lplayer
        else:
            player = global_data.player.logic if global_data.player else None
        if player and player.is_valid() and player.share_data.ref_parachute_stage not in (parachute_utils.STAGE_NONE, parachute_utils.STAGE_MECHA_READY, parachute_utils.STAGE_PLANE, parachute_utils.STAGE_ISLAND):
            self.close()
            return
        else:
            self.count_down -= 1
            if self.count_down != 0:
                self.panel.lab_sec.SetString('({}s)'.format(self.count_down))
            else:
                self.agree()
            return

    def set_invite_follow_info(self, eid, pic_index, name, is_assign=False):
        self.inviter_eid = eid
        self.inviter_name = name
        self.is_assign = is_assign
        text_id = 19784 if is_assign else 80711
        self.panel.lab_invite.SetString(text_id)
        self.panel.img_num.SetDisplayFrameByPath('', self.ID_PIC_PATH[pic_index])
        self.panel.lab_nub.SetString(str(pic_index + 1))
        self.panel.lab_name.SetString(name)
        self.panel.lab_sec.SetString('(10s)')
        self.count_down = 10
        action = cc.RepeatForever.create(cc.Sequence.create([
         cc.DelayTime.create(1),
         cc.CallFunc.create(self.update_count_down)]))
        action.setTag(self.COUNT_DOWN_TAG)
        self.panel.runAction(action)

    def agree(self, *args):
        if global_data.cam_lplayer:
            player = global_data.cam_lplayer
        else:
            player = global_data.player.logic if global_data.player else None
        if player and player.is_valid():
            self.panel.stopActionByTag(self.COUNT_DOWN_TAG)
            if self.is_assign:
                if self.inviter_eid != player.ev_g_parachute_follow_target():
                    return
                player.send_event('E_CALL_SYNC_METHOD', 'respond_transfer_parachute_leader', (self.inviter_eid, True))
                global_data.game_mgr.show_tip(get_text_by_id(13098, {'playername': self.inviter_name}))
            else:
                player.send_event('E_CALL_SYNC_METHOD', 'follow_parachute', (self.inviter_eid,))
            self.close()
        return

    def reject(self, *args):
        if global_data.cam_lplayer:
            player = global_data.cam_lplayer
        else:
            player = global_data.player.logic if global_data.player else None
        if player and player.is_valid():
            self.panel.stopActionByTag(self.COUNT_DOWN_TAG)
            flag = self.panel.btn_tick.GetCheck()
            if self.is_assign:
                if self.inviter_eid != player.ev_g_parachute_follow_target():
                    return
                player.send_event('E_CALL_SYNC_METHOD', 'respond_transfer_parachute_leader', (self.inviter_eid, False, flag))
                global_data.game_mgr.show_tip(get_text_by_id(13099, {'playername': self.inviter_name}))
            else:
                player.send_event('E_CALL_SYNC_METHOD', 'refuse_follow_parachute', (self.inviter_eid, flag))
                global_data.game_mgr.show_tip(get_text_by_id(13042, {'playername': self.inviter_name}))
            self.close()
        return

    def refuse_receive(self, *args):
        self.panel.stopActionByTag(self.COUNT_DOWN_TAG)
        self.panel.lab_sec.SetString('')