# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/control_ui/SOSUI.py
from __future__ import absolute_import
import six
from common.const import uiconst
from common.const.uiconst import BASE_LAYER_ZORDER
from common.cfg import confmgr
from common.uisys.basepanel import BasePanel
from logic.gcommon.common_const import ui_operation_const
from logic.gcommon.common_const.battle_const import SOS_RESCUE, SOS_FIGHT, SOS_ESCAPE, SOS_COVER
ASSOCIATE_UI_LIST = [
 'FireRockerUI', 'FightLeftShotUI', 'PostureControlUI', 'BattleControlUIPC', 'WeaponBarSelectUI', 'BulletReloadUI']

class SOSUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/fight_down'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_sos.OnDrag': 'on_sos_drag',
       'btn_sos.OnBegin': 'on_sos_begin',
       'btn_sos.OnEnd': 'on_sos_end',
       'temp_chat.btn_down_signal.OnClick': 'on_show_chat_lst'
       }
    GLOBAL_EVENT = {'show_sos_btn_event': 'show_sos_btn'
       }

    def on_init_panel(self):
        self.panel.setLocalZOrder(ui_operation_const.FIRE_LOCAL_ZORDER)
        self.add_blocking_ui_list(ASSOCIATE_UI_LIST)
        self.init_parameters()

    def on_finalize_panel(self):
        global_data.ui_mgr.close_ui('BegChatUI')

    def init_parameters(self):
        self.is_spread_sos = False
        self.cur_sos_type = None
        self.sos_nodes = {SOS_RESCUE: self.panel.temp_rescue,
           SOS_FIGHT: self.panel.temp_fight,
           SOS_ESCAPE: self.panel.temp_escape,
           SOS_COVER: self.panel.temp_cover
           }
        self.panel.RecordAnimationNodeState('show_extend')
        self.panel.RecordAnimationNodeState('disappear_extend')
        self.panel.nd_chat.setVisible(True)
        return

    def show_sos_btn(self):
        if self.is_valid():
            self.panel.btn_sos.setVisible(True)

    def on_sos_drag(self, layer, touch):
        if not self.btn_sos.GetMovedDistance() or self.panel.IsPlayingAnimation('show_extend'):
            return
        else:
            self.cur_sos_type = None
            wpos = self.panel.btn_sos.getParent().convertToNodeSpace(touch.getLocation())
            for type, node in six.iteritems(self.sos_nodes):
                lpos = node.getPosition()
                nw, nh = node.GetContentSize()
                if abs(wpos.x - lpos.x) < nw * 0.5 and abs(wpos.y - lpos.y) < nh * 0.5:
                    node.btn_down_signal.SetSelect(True)
                    node.btn_icon.SetSelect(True)
                    self.cur_sos_type = type
                else:
                    node.btn_down_signal.SetSelect(False)
                    node.btn_icon.SetSelect(False)

            return

    def on_sos_begin(self, layer, touch):
        node = self.sos_nodes.get(self.cur_sos_type)
        if node:
            node.btn_down_signal.SetSelect(False)
            node.btn_icon.SetSelect(False)
        if not self.is_spread_sos:
            self.panel.StopAnimation('disappear_extend')
            self.panel.RecoverAnimationNodeState('show_extend')
            self.panel.PlayAnimation('show_extend')
            self.is_spread_sos = True
        return True

    def on_sos_end(self, layer, touch):
        if self.is_spread_sos and global_data.cam_lplayer:
            self.panel.StopAnimation('show_extend')
            self.panel.RecoverAnimationNodeState('disappear_extend')
            self.panel.temp_chat.setOpacity(255)
            self.panel.PlayAnimation('disappear_extend')
            self.is_spread_sos = False
            if not self.cur_sos_type:
                return
            sos_tid = self._get_sos_text_id()
            voice_trigger_type = self._get_sos_voice_trigger_type()
            lplayer = global_data.cam_lplayer
            lplayer and lplayer.send_event('E_SEND_BATTLE_GROUP_MSG', {'text': sos_tid or 7037,'sos_type': self.cur_sos_type,'voice_trigger_type': voice_trigger_type}, True)
            self.cur_sos_type = None
        return

    def on_show_chat_lst(self, *args):
        self.panel.btn_sos.setVisible(False)
        ui = global_data.ui_mgr.show_ui('BegChatUI', 'logic.comsys.chat')
        ui.chat_open()

    def _get_sos_text_id(self):
        if global_data.cam_lplayer:
            role_id = global_data.cam_lplayer.ev_g_role_id() if 1 else None
            DEFAULT_ROLE_ID = '0'
            conf = confmgr.get('down_quick_chat', str(role_id), default=None)
            if not conf:
                conf = confmgr.get('down_quick_chat', DEFAULT_ROLE_ID)
            sos_type_conf = conf.get(str(self.cur_sos_type), None)
            return sos_type_conf or None
        else:
            return sos_type_conf['text_id']

    def _get_sos_voice_trigger_type(self):
        if global_data.cam_lplayer:
            role_id = global_data.cam_lplayer.ev_g_role_id() if 1 else None
            DEFAULT_ROLE_ID = '0'
            conf = confmgr.get('down_quick_chat', str(role_id), default=None)
            if not conf:
                conf = confmgr.get('down_quick_chat', DEFAULT_ROLE_ID)
            sos_type_conf = conf.get(str(self.cur_sos_type), None)
            return sos_type_conf or None
        else:
            return sos_type_conf.get('trigger_type')