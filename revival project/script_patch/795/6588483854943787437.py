# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Settle/EndEntireTeamUI.py
from __future__ import absolute_import
from six.moves import range
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER
from common.utils.cocos_utils import ccc3FromHex
from common.const import uiconst

class EndEntireTeamUI(BasePanel):
    PANEL_CONFIG_NAME = 'end/end_show'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_exit.btn_common.OnClick': '_on_click_btn_exit'
       }

    def on_init_panel(self, group_num, settle_dict, teaminfo):
        rank = settle_dict.get('rank')
        self.panel.lab_rank.setString(get_text_local_content(19404).format(num=rank))
        teammate_num = len(teaminfo)
        txt_num = 19406 if teammate_num > 1 else 19405
        txt = get_text_local_content(txt_num).format(num=group_num)
        self.panel.lab_player_num.setString(txt)
        self.panel.PlayAnimation('rank_show')
        from mobile.common.EntityManager import EntityManager
        com_settle = global_data.game_mgr.scene.get_com('PartSettle')
        for i in range(4):
            node = getattr(self.panel, 'nd_info_' + str(i + 1))
            node.setVisible(False)
            if i >= teammate_num:
                continue
            info = teaminfo[i].get('info', {})
            node.setVisible(True)
            node.lab_name.setString(teaminfo[i].get('name', ''))
            node.lab_damage_num.setString(str(info.get('damage', 0)))
            com_settle.add_avatar_model(dress_dict=teaminfo[i].get('clothing', {}))
            if teammate_num > 1 and info.get('id') == global_data.player.id:
                node.lab_name.SetColor('#SG')

    def _on_click_btn_exit(self, *args):
        from logic.comsys.battle.Settle.SettleSystem import SettleSystem
        SettleSystem.finalize()
        self.close()
        global_data.emgr.settle_ui_exit.emit()