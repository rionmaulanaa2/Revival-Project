# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/BattleInfoParadrop.py
from __future__ import absolute_import
from __future__ import print_function
from .BattleInfoMessage import BattleInfoMessage
from common.const.uiconst import BATTLE_MESSAGE_ZORDER, UI_TYPE_MESSAGE
from logic.comsys.ui_distortor.MechaDistortHelper import MechaDistortHelper
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.time_utility import time
import math3d
import cc

class BattleInfoParadrop(MechaDistortHelper, BattleInfoMessage):
    PANEL_CONFIG_NAME = 'battle_tips/common_tips/fight_top_paradrop_tips'
    DLG_ZORDER = BATTLE_MESSAGE_ZORDER
    UI_TYPE = UI_TYPE_MESSAGE
    UI_ACTION_EVENT = {'bg_layer.OnClick': 'on_click_bg_layer'
       }
    PC_ROOT_NODE_POS_X = 201

    def on_init_panel(self, on_process_done=None):
        super(BattleInfoParadrop, self).on_init_panel(on_process_done)
        BattleInfoMessage.on_init_panel(self, on_process_done)
        self.min_position_data = None
        self.check_visible('BattleInfoMessageVisibleUI')
        self.init_custom_com()
        self.panel.RecordAnimationNodeState('up_show')
        global_data.emgr.scene_del_paradrop += self.del_paradrop_mark
        if global_data.is_pc_mode:
            self.panel.SetPosition(self.PC_ROOT_NODE_POS_X, self.panel.GetPosition()[1])
        return

    def init_custom_com(self):
        from logic.comsys.setting_ui.CustomUIProxy import init_custom_com
        init_custom_com(self, {})

    def on_finalize_panel--- This code section failed: ---

  39       0  LOAD_GLOBAL           0  'super'
           3  LOAD_GLOBAL           1  'BattleInfoParadrop'
           6  LOAD_FAST             0  'self'
           9  CALL_FUNCTION_2       2 
          12  LOAD_ATTR             2  'on_finalize_panel'
          15  CALL_FUNCTION_0       0 
          18  POP_TOP          

  40      19  LOAD_CONST            0  ''
          22  LOAD_FAST             0  'self'
          25  STORE_ATTR            4  'min_position_data'

  41      28  LOAD_GLOBAL           5  'hasattr'
          31  LOAD_GLOBAL           1  'BattleInfoParadrop'
          34  CALL_FUNCTION_2       2 
          37  POP_JUMP_IF_FALSE    74  'to 74'
          40  LOAD_FAST             0  'self'
          43  LOAD_ATTR             6  'custom_ui_com'
        46_0  COME_FROM                '37'
          46  POP_JUMP_IF_FALSE    74  'to 74'

  42      49  LOAD_FAST             0  'self'
          52  LOAD_ATTR             6  'custom_ui_com'
          55  LOAD_ATTR             7  'destroy'
          58  CALL_FUNCTION_0       0 
          61  POP_TOP          

  43      62  LOAD_CONST            0  ''
          65  LOAD_FAST             0  'self'
          68  STORE_ATTR            6  'custom_ui_com'
          71  JUMP_FORWARD          0  'to 74'
        74_0  COME_FROM                '71'

  44      74  LOAD_GLOBAL           8  'global_data'
          77  LOAD_ATTR             9  'emgr'
          80  DUP_TOP          
          81  LOAD_ATTR            10  'scene_del_paradrop'
          84  LOAD_FAST             0  'self'
          87  LOAD_ATTR            11  'del_paradrop_mark'
          90  INPLACE_SUBTRACT 
          91  ROT_TWO          
          92  STORE_ATTR           10  'scene_del_paradrop'
          95  LOAD_CONST            0  ''
          98  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 34

    def init_event(self):
        pass

    def del_paradrop_mark(self, paradrop_id):
        if self.min_position_data and self.min_position_data[1] == paradrop_id:
            self.min_position_data = None
        return

    def process_one_message(self, message, finish_cb):
        paradrops = message[0]
        if paradrops and global_data.cam_lplayer:
            min_dis = None
            min_position = None
            min_paradrop_id = None
            min_paradrop_no = None
            position = global_data.cam_lplayer.ev_g_position()
            if not position:
                return
            for paradrop_id, paradrop_no, x, z in paradrops:
                paradrop_position = math3d.vector(x, position.y, z)
                dis = (paradrop_position - position).length
                if min_dis is None or dis < min_dis:
                    min_dis = dis
                    min_position = paradrop_position
                    min_paradrop_id = paradrop_id
                    min_paradrop_no = paradrop_no

            min_dis = int(min_dis / NEOX_UNIT_SCALE)
            from common.cfg import confmgr
            if min_paradrop_no:
                paradrop_conf = confmgr.get('paradrop_data', str(min_paradrop_no), default={})
                nondist_text, dist_text = paradrop_conf.get('paradrop_anchor_tip', [6028, 6029])
            else:
                nondist_text, dist_text = 6028, 6029
            print('process_one_message', message, nondist_text, dist_text, min_paradrop_no)
            if min_dis > 999:
                self.panel.lab_airdrop.SetString(get_text_by_id(nondist_text))
                self.panel.lab_distance.SetString(' ')
                self.panel.lab_distance.setVisible(False)
                self.min_position_data = None
            else:
                self.panel.lab_airdrop.SetString(get_text_by_id(dist_text))
                self.panel.lab_distance.setVisible(True)
                self.panel.lab_distance.SetString('%dm' % min_dis)
                global_data.emgr.scene_add_paradrop.emit(min_paradrop_id, min_position, min_paradrop_no)
                self.min_position_data = (time(), min_paradrop_id, min_position)
        else:
            self.panel.lab_distance.setVisible(False)

        def finished():
            if self and self.is_valid():
                self.up.setVisible(False)
                self.finish_cb()

        show_in_t = self.panel.GetAnimationMaxRunTime('up_show')
        ac_list = [
         cc.DelayTime.create(1)]
        ac_list.append(cc.DelayTime.create(show_in_t))
        ac_list.append(cc.CallFunc.create(finished))
        self.panel.stopAllActions()
        self._recover_animation_node_without_position('up_show')
        self.panel.PlayAnimation('up_show')
        self.panel.runAction(cc.Sequence.create(ac_list))
        self.up.setVisible(True)
        return

    def on_click_bg_layer(self, btn, touch):
        self.up.setVisible(False)
        self.playing = False
        self.process_next_message()

    def _recover_animation_node_without_position(self, animation):
        position = self.panel.up.getPosition()
        self.panel.RecoverAnimationNodeState(animation)
        self.panel.up.setPosition(position)