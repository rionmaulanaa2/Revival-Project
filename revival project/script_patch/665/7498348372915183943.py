# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/LobbyNoticeWidget.py
from __future__ import absolute_import
import cc
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no
from logic.gutils.item_utils import get_lobby_item_type
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_WEAPON_SFX
from logic.gutils.item_utils import get_skin_rare_path_by_rare
from logic.gutils.item_utils import get_item_rare_degree
BROADCAST_STAY_TIME = 3
from logic.gutils.mecha_skin_utils import is_s_skin_that_can_upgrade

class LobbyNoticeWidget(object):

    def __init__(self, parent, panel):
        self.parent = parent
        self.panel = panel
        self.on_init_panel()

    def destroy(self):
        self.on_finalize_panel()
        self.panel = None
        self.parent = None
        return

    def on_init_panel(self):
        self.panel.nd_tips.setVisible(False)
        self.broadcast_queue = []
        self.is_broadcasting = False
        global_data.emgr.broadcast_lottery_result += self.on_receive_broadcast_notice

    def on_finalize_panel(self):
        global_data.emgr.broadcast_lottery_result -= self.on_receive_broadcast_notice

    def on_receive_broadcast_notice(self, notice_text, item_no, info_dict):
        self.broadcast_queue.append((notice_text, item_no, info_dict))
        self.show_next_notice()

    def show_next_notice(self):
        if self.is_broadcasting or not self.broadcast_queue:
            if not self.broadcast_queue:
                self.panel.nd_tips.setVisible(False)
            return
        self.panel.nd_tips.setVisible(True)
        self.is_broadcasting = True
        notice_text, item_no, info_dict = self.broadcast_queue.pop(0)
        self.panel.lab_get_tips.SetString(notice_text)
        item_type = get_lobby_item_type(item_no)
        show_item_no = item_no
        if item_type == L_ITEM_TYPE_WEAPON_SFX:
            from logic.gutils.dress_utils import get_weapon_sfx_skin_show_mount_item_no
            show_item_no = get_weapon_sfx_skin_show_mount_item_no(item_no)
            if not show_item_no:
                show_item_no = item_no
            if is_s_skin_that_can_upgrade(show_item_no):
                self.panel.temp_ex.img_ex.SetDisplayFrameByPath('', 'gui/ui_res_2/mech_display/icon_s_plus.png')
            else:
                self.panel.temp_ex.img_ex.SetDisplayFrameByPath('', 'gui/ui_res_2/mech_display/img_ex.png')
            self.panel.temp_ex.setVisible(True)
            self.panel.temp_kind.setScale(0.0001)
        else:
            self.panel.temp_ex.setVisible(False)
            self.panel.temp_kind.setScale(1.0)
            quality = info_dict.get('quality') or get_item_rare_degree(item_no, ignore_imporve=True)
            self.panel.temp_kind.SetDisplayFrameByPath('', get_skin_rare_path_by_rare(quality))
        self.panel.img_skin.SetDisplayFrameByPath('', get_lobby_item_pic_by_item_no(show_item_no))

        def finish():
            self.is_broadcasting = False
            self.show_next_notice()

        action_list = []
        action_list.append(cc.CallFunc.create(lambda : self.panel.PlayAnimation('appear')))
        action_list.append(cc.DelayTime.create(self.panel.GetAnimationMaxRunTime('appear') + BROADCAST_STAY_TIME))
        action_list.append(cc.CallFunc.create(lambda : self.panel.PlayAnimation('disappear')))
        action_list.append(cc.DelayTime.create(self.panel.GetAnimationMaxRunTime('disappear') + 0.2))
        action_list.append(cc.CallFunc.create(finish))
        self.panel.runAction(cc.Sequence.create(action_list))