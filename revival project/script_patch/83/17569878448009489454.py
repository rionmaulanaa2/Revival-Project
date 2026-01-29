# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVETeamListWidget.py
from __future__ import absolute_import
from logic.comsys.lobby.LobbyTeamListWidget import LobbyTeamListWidget
from logic.gcommon.common_const.battle_const import DEFAULT_PVE_TID
from logic.gutils.lv_template_utils import init_lv_template
from logic.gutils.dress_utils import mecha_lobby_id_2_battle_id
import six

class PVETeamListWidget(LobbyTeamListWidget):

    def __init__(self, parent_ui, panel):
        self.teammate_info_list = None
        super(PVETeamListWidget, self).__init__(parent_ui, panel)
        self.init_team_info_widget()
        return

    def destroy(self):
        super(PVETeamListWidget, self).destroy()
        global_data.emgr.player_teammate_info_update_event -= self.update_teammate_info_list

    def init_event(self):
        super(LobbyTeamListWidget, self).init_event()
        self.panel.btn_leave.BindMethod('OnClick', self.on_click_leave_team)
        self.panel.btn_add_player.BindMethod('OnClick', self.on_invite_clicked)

    def set_ready_state(self, widget, ready, battle_type):
        if battle_type != DEFAULT_PVE_TID:
            ready = False
        if ready == widget.icon_ready.isVisible():
            return
        if ready:
            widget.PlayAnimation('ready')
        else:
            widget.StopAnimation('ready')
            widget.icon_ready.setVisible(False)
        widget.icon_ready.setVisible(ready)

    def update_visit_icon(self, *args):
        pass

    def update_teammate_list(self, *args):
        super(PVETeamListWidget, self).update_teammate_list()
        team_info = global_data.player.get_team_info() if global_data.player else {}
        self.panel.btn_invite.setScale(0 if bool(team_info) else 1)
        if self.teammate_info_list:
            self.update_teammate_info_list()

    def init_team_info_widget(self):
        self.teammate_info_list = self.panel.list_teammate_info
        if self.teammate_info_list:
            global_data.emgr.player_teammate_info_update_event += self.update_teammate_info_list
            self.teammate_info_list.DeleteAllSubItem()
            self.uid_2_teammate_item = {}
            self.update_teammate_info_list()

    def update_teammate_info_list(self, *args):
        if not self.teammate_info_list:
            return
        else:
            if not global_data.player:
                return
            team_info = global_data.player.get_team_info()
            team_info = team_info or {}
            if not team_info:
                self.panel.btn_recruit.SetPosition('50%37', '100%-11')
                return
            team_dict = team_info.get('members', {})
            teammate_count = len(team_dict)
            if teammate_count:
                self.panel.btn_recruit.SetPosition('50%100', '100%-20')
            else:
                self.panel.btn_recruit.SetPosition('50%37', '100%-11')
            if teammate_count < len(self.uid_2_teammate_item):
                self.teammate_info_list.DeleteAllSubItem()
                self.uid_2_teammate_item = {}
            for uid, member in six.iteritems(team_dict):
                if self.uid_2_teammate_item.get(uid):
                    item = self.uid_2_teammate_item[uid]
                else:
                    item = self.teammate_info_list.AddTemplateItem()
                    self.uid_2_teammate_item[uid] = item
                nd_mecha = item.nd_mecha
                nd_empty = item.nd_empty
                nd_info = item.nd_info
                nd_info.lab_name.setString(member.get('char_name', ''))
                init_lv_template(nd_info.temp_level, member.get('lv', 1))
                nd_info.lab_id.setString('ID:{}'.format(uid))
                pve_mecha_info = member.get('pve_mecha_info', {})
                pve_lobby_mecha_id = pve_mecha_info.get('pve_lobby_mecha_id')
                if pve_lobby_mecha_id is None:
                    nd_empty.setVisible(True)
                    nd_mecha.setVisible(False)
                else:
                    nd_empty.setVisible(False)
                    nd_mecha.setVisible(True)
                    mecha_id = mecha_lobby_id_2_battle_id(pve_lobby_mecha_id)
                    icon_path = 'gui/ui_res_2/item/role_head/3021%s.png' % str(mecha_id)
                    nd_mecha.nd_cut.icon_mecha.SetDisplayFrameByPath('', icon_path)
                    nd_mecha.lab_level.setString('Lv.{}'.format(pve_mecha_info.get('pve_lobby_mecha_level', 0)))

            return