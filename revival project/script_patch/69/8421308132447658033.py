# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/BattleSignalInfoUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import BASE_LAYER_ZORDER
from common.const import uiconst
from logic.gcommon.common_const import battle_const
from logic.gcommon import time_utility
import world

class BattleSignalInfoUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_tips/common_tips/fight_signal_tips'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT

    def init(self, parent=None, *arg, **kwargs):
        super(BattleSignalInfoUI, self).init(parent=parent, *arg, **kwargs)

    def on_init_panel(self):
        self.init_parameters()
        self.init_custom_com()
        self.panel.nd_tip.setVisible(False)
        self.panel.RecordAnimationNodeState('show')
        self.panel.RecordAnimationNodeState('hide')
        self.panel.RecordAnimationNodeState('warning')
        self.panel.RecordAnimationNodeState('warning_hide')
        self.panel.RecordAnimationNodeState('countdown')

    def init_custom_com(self):
        from logic.comsys.setting_ui.CustomUIProxy import init_custom_com
        init_custom_com(self, {})

    def on_finalize_panel(self):
        self.unbind_ui_event(self.player)
        self.player = None
        self.destroy_widget('custom_ui_com')
        emgr = global_data.emgr
        emgr.scene_player_setted_event -= self.on_player_setted
        emgr.scene_camera_player_setted_event -= self.on_scene_cam_player_setted
        emgr.net_reconnect_event -= self.on_reconnected
        emgr.net_login_reconnect_event -= self.on_reconnected
        emgr.cam_lplayer_gulag_state_changed -= self.on_player_gulag_state_changed
        return

    def init_parameters(self):
        self.player = None
        self._is_in_mecha = False
        self._is_in_poison = False
        self._showed_warning = False
        scn = world.get_active_scene()
        player = scn.get_player()
        self.add_hide_count(self.__class__.__name__)
        spectate_target = None
        if global_data.player and global_data.player.logic:
            spectate_target = global_data.player.logic.ev_g_spectate_target()
        if spectate_target and spectate_target.logic:
            self.on_player_setted(spectate_target.logic)
        elif player:
            self.on_player_setted(player)
        emgr = global_data.emgr
        emgr.scene_player_setted_event += self.on_player_setted
        emgr.scene_camera_player_setted_event += self.on_scene_cam_player_setted
        emgr.net_reconnect_event += self.on_reconnected
        emgr.net_login_reconnect_event += self.on_reconnected
        emgr.cam_lplayer_gulag_state_changed += self.on_player_gulag_state_changed
        return

    def on_scene_cam_player_setted(self):
        self.on_player_setted(global_data.cam_lplayer)

    def on_player_setted(self, player):
        self.unbind_ui_event(self.player)
        self.player = player
        if player:
            self.add_show_count(self.__class__.__name__)
            self.init_event()
            self.bind_ui_event(self.player)

    def on_reconnected(self, *args, **kw):
        if self.panel.lab_content_left.isVisible() or self.panel.lab_content.isVisible():
            self.leave_screen()

    def init_event(self):
        self._is_in_mecha = self.player.ev_g_in_mecha('Mecha')
        is_in_poison = self.player.ev_g_signal_in_poison()
        left_time = self.player.ev_g_signal_left_time()
        self.on_poison_area_change(self.player.id, is_in_poison, left_time)
        if not is_in_poison:
            return
        else:
            if left_time is not None:
                self.panel.lab_countdown_time.SetString(str(left_time))
            return

    def bind_ui_event(self, target):
        regist_func = target.regist_event
        regist_func('E_SIGNAL_CHANGE', self.on_update_signal_value)
        regist_func('E_ON_JOIN_MECHA', self.on_control_target_change)
        regist_func('E_ON_LEAVE_MECHA', self.on_control_target_change)

    def unbind_ui_event(self, target):
        if target and target.is_valid():
            unregist_func = target.unregist_event
            unregist_func('E_SIGNAL_CHANGE', self.on_update_signal_value)
            unregist_func('E_ON_JOIN_MECHA', self.on_control_target_change)
            unregist_func('E_ON_LEAVE_MECHA', self.on_control_target_change)

    def on_update_signal_value(self, cur_signal, percent, left_time):
        if cur_signal is None or left_time is None:
            return
        else:
            self._check_and_show_countdown(left_time)
            self.panel.lab_countdown_time.SetString(str(left_time))
            self.panel.vx_lab_countdown_time.SetString(str(left_time))
            self.panel.prog_countdown.SetPercentage(percent * 100)
            if left_time < 50:
                self.panel.lab_countdown_time.SetColor(16726037)
                self.panel.vx_lab_countdown_time.SetColor(16726037)
            else:
                self.panel.lab_countdown_time.SetColor('#DW')
                self.panel.vx_lab_countdown_time.SetColor('#DW')
            return

    def _switch_warning--- This code section failed: ---

 120       0  LOAD_FAST             1  'show'
           3  POP_JUMP_IF_FALSE   223  'to 223'

 121       6  LOAD_FAST             0  'self'
           9  LOAD_ATTR             0  '_is_in_mecha'
          12  POP_JUMP_IF_FALSE    43  'to 43'

 122      15  LOAD_FAST             0  'self'
          18  LOAD_ATTR             1  'panel'
          21  LOAD_ATTR             2  'lab_content'
          24  LOAD_ATTR             3  'setString'
          27  LOAD_GLOBAL           4  'get_text_by_id'
          30  LOAD_CONST            1  81996
          33  CALL_FUNCTION_1       1 
          36  CALL_FUNCTION_1       1 
          39  POP_TOP          
          40  JUMP_FORWARD         68  'to 111'

 123      43  LOAD_GLOBAL           5  'getattr'
          46  LOAD_GLOBAL           2  'lab_content'
          49  LOAD_GLOBAL           6  'False'
          52  CALL_FUNCTION_3       3 
          55  POP_JUMP_IF_FALSE    86  'to 86'

 124      58  LOAD_FAST             0  'self'
          61  LOAD_ATTR             1  'panel'
          64  LOAD_ATTR             2  'lab_content'
          67  LOAD_ATTR             3  'setString'
          70  LOAD_GLOBAL           4  'get_text_by_id'
          73  LOAD_CONST            3  17989
          76  CALL_FUNCTION_1       1 
          79  CALL_FUNCTION_1       1 
          82  POP_TOP          
          83  JUMP_FORWARD         25  'to 111'

 126      86  LOAD_FAST             0  'self'
          89  LOAD_ATTR             1  'panel'
          92  LOAD_ATTR             2  'lab_content'
          95  LOAD_ATTR             3  'setString'
          98  LOAD_GLOBAL           4  'get_text_by_id'
         101  LOAD_CONST            4  19824
         104  CALL_FUNCTION_1       1 
         107  CALL_FUNCTION_1       1 
         110  POP_TOP          
       111_0  COME_FROM                '83'
       111_1  COME_FROM                '40'

 127     111  LOAD_FAST             0  'self'
         114  LOAD_ATTR             7  '_showed_warning'
         117  POP_JUMP_IF_TRUE    378  'to 378'

 128     120  LOAD_FAST             0  'self'
         123  LOAD_ATTR             1  'panel'
         126  LOAD_ATTR             8  'IsPlayingAnimation'
         129  LOAD_CONST            5  'warning_hide'
         132  CALL_FUNCTION_1       1 
         135  POP_JUMP_IF_FALSE   157  'to 157'

 129     138  LOAD_FAST             0  'self'
         141  LOAD_ATTR             1  'panel'
         144  LOAD_ATTR             9  'StopAnimation'
         147  LOAD_CONST            5  'warning_hide'
         150  CALL_FUNCTION_1       1 
         153  POP_TOP          
         154  JUMP_FORWARD          0  'to 157'
       157_0  COME_FROM                '154'

 130     157  LOAD_FAST             0  'self'
         160  LOAD_ATTR             1  'panel'
         163  LOAD_ATTR            10  'RecoverAnimationNodeState'
         166  LOAD_CONST            6  'warning'
         169  CALL_FUNCTION_1       1 
         172  POP_TOP          

 131     173  LOAD_FAST             0  'self'
         176  LOAD_ATTR             1  'panel'
         179  LOAD_ATTR            11  'nd_tip'
         182  LOAD_ATTR            12  'setVisible'
         185  LOAD_GLOBAL          13  'True'
         188  CALL_FUNCTION_1       1 
         191  POP_TOP          

 132     192  LOAD_FAST             0  'self'
         195  LOAD_ATTR             1  'panel'
         198  LOAD_ATTR            14  'PlayAnimation'
         201  LOAD_CONST            6  'warning'
         204  CALL_FUNCTION_1       1 
         207  POP_TOP          

 133     208  LOAD_GLOBAL          13  'True'
         211  LOAD_FAST             0  'self'
         214  STORE_ATTR            7  '_showed_warning'
         217  JUMP_ABSOLUTE       378  'to 378'
         220  JUMP_FORWARD        155  'to 378'

 134     223  LOAD_FAST             0  'self'
         226  LOAD_ATTR             7  '_showed_warning'
         229  POP_JUMP_IF_FALSE   378  'to 378'

 135     232  LOAD_FAST             0  'self'
         235  LOAD_ATTR             1  'panel'
         238  LOAD_ATTR            11  'nd_tip'
         241  LOAD_ATTR            15  'isVisible'
         244  CALL_FUNCTION_0       0 
         247  STORE_FAST            2  'is_tip_visible'

 137     250  LOAD_FAST             0  'self'
         253  LOAD_ATTR             1  'panel'
         256  LOAD_ATTR             8  'IsPlayingAnimation'
         259  LOAD_CONST            6  'warning'
         262  CALL_FUNCTION_1       1 
         265  POP_JUMP_IF_FALSE   287  'to 287'

 138     268  LOAD_FAST             0  'self'
         271  LOAD_ATTR             1  'panel'
         274  LOAD_ATTR             9  'StopAnimation'
         277  LOAD_CONST            6  'warning'
         280  CALL_FUNCTION_1       1 
         283  POP_TOP          
         284  JUMP_FORWARD          0  'to 287'
       287_0  COME_FROM                '284'

 139     287  LOAD_FAST             0  'self'
         290  LOAD_ATTR             1  'panel'
         293  LOAD_ATTR            10  'RecoverAnimationNodeState'
         296  LOAD_CONST            6  'warning'
         299  CALL_FUNCTION_1       1 
         302  POP_TOP          

 141     303  LOAD_FAST             2  'is_tip_visible'
         306  POP_JUMP_IF_FALSE   347  'to 347'

 142     309  LOAD_FAST             0  'self'
         312  LOAD_ATTR             1  'panel'
         315  LOAD_ATTR            11  'nd_tip'
         318  LOAD_ATTR            12  'setVisible'
         321  LOAD_GLOBAL          13  'True'
         324  CALL_FUNCTION_1       1 
         327  POP_TOP          

 143     328  LOAD_FAST             0  'self'
         331  LOAD_ATTR             1  'panel'
         334  LOAD_ATTR            14  'PlayAnimation'
         337  LOAD_CONST            5  'warning_hide'
         340  CALL_FUNCTION_1       1 
         343  POP_TOP          
         344  JUMP_FORWARD         19  'to 366'

 145     347  LOAD_FAST             0  'self'
         350  LOAD_ATTR             1  'panel'
         353  LOAD_ATTR            11  'nd_tip'
         356  LOAD_ATTR            12  'setVisible'
         359  LOAD_GLOBAL           6  'False'
         362  CALL_FUNCTION_1       1 
         365  POP_TOP          
       366_0  COME_FROM                '344'

 146     366  LOAD_GLOBAL           6  'False'
         369  LOAD_FAST             0  'self'
         372  STORE_ATTR            7  '_showed_warning'
         375  JUMP_FORWARD          0  'to 378'
       378_0  COME_FROM                '375'
       378_1  COME_FROM                '220'

Parse error at or near `CALL_FUNCTION_3' instruction at offset 52

    def _check_and_show_countdown(self, left_time):
        if self._is_in_mecha:
            return
        if self._is_in_poison:
            if 0 < left_time <= battle_const.BATTLE_SIGNAL_WARNING_LEFT_TIME_MIN:
                if not self.panel.IsPlayingAnimation('countdown'):
                    self.panel.PlayAnimation('countdown')
                self._showed_warning or self._switch_warning(show=True)
            self.panel.lab_content.setString(get_text_by_id(19824))
        else:
            self._switch_warning(show=False)
            if self.panel.IsPlayingAnimation('countdown'):
                self.panel.StopAnimation('countdown')
                self.panel.RecoverAnimationNodeState('countdown')
                self.panel.vx_lab_countdown_time.setVisible(False)

    def on_control_target_change--- This code section failed: ---

 165       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  'player'
           6  LOAD_ATTR             1  'ev_g_in_mecha'
           9  LOAD_CONST            1  'Mecha'
          12  CALL_FUNCTION_1       1 
          15  LOAD_FAST             0  'self'
          18  STORE_ATTR            2  '_is_in_mecha'

 167      21  LOAD_FAST             0  'self'
          24  LOAD_ATTR             2  '_is_in_mecha'
          27  POP_JUMP_IF_TRUE     45  'to 45'
          30  LOAD_GLOBAL           3  'getattr'
          33  LOAD_GLOBAL           2  '_is_in_mecha'
          36  LOAD_GLOBAL           4  'False'
          39  CALL_FUNCTION_3       3 
        42_0  COME_FROM                '27'
          42  POP_JUMP_IF_FALSE   111  'to 111'

 168      45  LOAD_FAST             0  'self'
          48  LOAD_ATTR             5  'panel'
          51  LOAD_ATTR             6  'nd_countdown'
          54  LOAD_ATTR             7  'setVisible'
          57  LOAD_GLOBAL           4  'False'
          60  CALL_FUNCTION_1       1 
          63  POP_TOP          

 169      64  LOAD_FAST             0  'self'
          67  LOAD_ATTR             5  'panel'
          70  LOAD_ATTR             8  'lab_content'
          73  LOAD_ATTR             9  'setString'
          76  LOAD_GLOBAL          10  'get_text_by_id'
          79  LOAD_CONST            3  81996
          82  CALL_FUNCTION_1       1 
          85  CALL_FUNCTION_1       1 
          88  POP_TOP          

 170      89  LOAD_FAST             0  'self'
          92  LOAD_ATTR            11  '_switch_warning'
          95  LOAD_CONST            4  'show'
          98  LOAD_FAST             0  'self'
         101  LOAD_ATTR            12  '_is_in_poison'
         104  CALL_FUNCTION_256   256 
         107  POP_TOP          
         108  JUMP_FORWARD         63  'to 174'

 172     111  LOAD_FAST             0  'self'
         114  LOAD_ATTR             5  'panel'
         117  LOAD_ATTR             6  'nd_countdown'
         120  LOAD_ATTR             7  'setVisible'
         123  LOAD_GLOBAL          13  'True'
         126  CALL_FUNCTION_1       1 
         129  POP_TOP          

 173     130  LOAD_FAST             0  'self'
         133  LOAD_ATTR            11  '_switch_warning'
         136  LOAD_CONST            4  'show'
         139  LOAD_GLOBAL           4  'False'
         142  CALL_FUNCTION_256   256 
         145  POP_TOP          

 174     146  LOAD_FAST             0  'self'
         149  LOAD_ATTR             0  'player'
         152  LOAD_ATTR            14  'ev_g_signal_left_time'
         155  CALL_FUNCTION_0       0 
         158  STORE_FAST            2  'left_time'

 175     161  LOAD_FAST             0  'self'
         164  LOAD_ATTR            15  '_check_and_show_countdown'
         167  LOAD_FAST             2  'left_time'
         170  CALL_FUNCTION_1       1 
         173  POP_TOP          
       174_0  COME_FROM                '108'

Parse error at or near `CALL_FUNCTION_3' instruction at offset 39

    def on_poison_area_change--- This code section failed: ---

 178       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  'player'
           6  POP_JUMP_IF_TRUE     13  'to 13'

 179       9  LOAD_CONST            0  ''
          12  RETURN_END_IF    
        13_0  COME_FROM                '6'

 180      13  LOAD_FAST             0  'self'
          16  LOAD_ATTR             0  'player'
          19  LOAD_ATTR             1  'id'
          22  LOAD_FAST             1  'player_id'
          25  COMPARE_OP            3  '!='
          28  POP_JUMP_IF_FALSE    35  'to 35'

 181      31  LOAD_CONST            0  ''
          34  RETURN_END_IF    
        35_0  COME_FROM                '28'

 182      35  LOAD_FAST             0  'self'
          38  LOAD_ATTR             2  '_is_in_poison'
          41  STORE_FAST            4  'old_poison'

 183      44  LOAD_FAST             2  'in_poison'
          47  LOAD_FAST             0  'self'
          50  STORE_ATTR            2  '_is_in_poison'

 184      53  LOAD_FAST             2  'in_poison'
          56  POP_JUMP_IF_TRUE    141  'to 141'

 185      59  LOAD_FAST             4  'old_poison'
          62  LOAD_FAST             2  'in_poison'
          65  COMPARE_OP            3  '!='
          68  POP_JUMP_IF_FALSE   122  'to 122'

 186      71  LOAD_FAST             0  'self'
          74  LOAD_ATTR             3  'panel'
          77  LOAD_ATTR             4  'StopAnimation'
          80  LOAD_CONST            1  'show'
          83  CALL_FUNCTION_1       1 
          86  POP_TOP          

 187      87  LOAD_FAST             0  'self'
          90  LOAD_ATTR             3  'panel'
          93  LOAD_ATTR             5  'RecoverAnimationNodeState'
          96  LOAD_CONST            2  'hide'
          99  CALL_FUNCTION_1       1 
         102  POP_TOP          

 188     103  LOAD_FAST             0  'self'
         106  LOAD_ATTR             3  'panel'
         109  LOAD_ATTR             6  'PlayAnimation'
         112  LOAD_CONST            2  'hide'
         115  CALL_FUNCTION_1       1 
         118  POP_TOP          
         119  JUMP_FORWARD          0  'to 122'
       122_0  COME_FROM                '119'

 189     122  LOAD_FAST             0  'self'
         125  LOAD_ATTR             7  '_switch_warning'
         128  LOAD_CONST            1  'show'
         131  LOAD_GLOBAL           8  'False'
         134  CALL_FUNCTION_256   256 
         137  POP_TOP          
         138  JUMP_FORWARD        213  'to 354'

 191     141  LOAD_FAST             0  'self'
         144  LOAD_ATTR             9  'enter_screen'
         147  CALL_FUNCTION_0       0 
         150  POP_TOP          

 192     151  LOAD_FAST             4  'old_poison'
         154  LOAD_FAST             2  'in_poison'
         157  COMPARE_OP            3  '!='
         160  POP_JUMP_IF_FALSE   214  'to 214'

 193     163  LOAD_FAST             0  'self'
         166  LOAD_ATTR             3  'panel'
         169  LOAD_ATTR             4  'StopAnimation'
         172  LOAD_CONST            2  'hide'
         175  CALL_FUNCTION_1       1 
         178  POP_TOP          

 194     179  LOAD_FAST             0  'self'
         182  LOAD_ATTR             3  'panel'
         185  LOAD_ATTR             5  'RecoverAnimationNodeState'
         188  LOAD_CONST            1  'show'
         191  CALL_FUNCTION_1       1 
         194  POP_TOP          

 195     195  LOAD_FAST             0  'self'
         198  LOAD_ATTR             3  'panel'
         201  LOAD_ATTR             6  'PlayAnimation'
         204  LOAD_CONST            1  'show'
         207  CALL_FUNCTION_1       1 
         210  POP_TOP          
         211  JUMP_FORWARD          0  'to 214'
       214_0  COME_FROM                '211'

 196     214  LOAD_FAST             0  'self'
         217  LOAD_ATTR            10  '_is_in_mecha'
         220  POP_JUMP_IF_TRUE    238  'to 238'
         223  LOAD_GLOBAL          11  'getattr'
         226  LOAD_GLOBAL           3  'panel'
         229  LOAD_GLOBAL           8  'False'
         232  CALL_FUNCTION_3       3 
       235_0  COME_FROM                '220'
         235  POP_JUMP_IF_FALSE   297  'to 297'

 197     238  LOAD_FAST             0  'self'
         241  LOAD_ATTR             7  '_switch_warning'
         244  LOAD_CONST            1  'show'
         247  LOAD_GLOBAL          12  'True'
         250  CALL_FUNCTION_256   256 
         253  POP_TOP          

 198     254  LOAD_FAST             0  'self'
         257  LOAD_ATTR             3  'panel'
         260  LOAD_ATTR            13  'nd_countdown'
         263  LOAD_ATTR            14  'isVisible'
         266  CALL_FUNCTION_0       0 
         269  POP_JUMP_IF_FALSE   354  'to 354'

 199     272  LOAD_FAST             0  'self'
         275  LOAD_ATTR             3  'panel'
         278  LOAD_ATTR            13  'nd_countdown'
         281  LOAD_ATTR            15  'setVisible'
         284  LOAD_GLOBAL           8  'False'
         287  CALL_FUNCTION_1       1 
         290  POP_TOP          
         291  JUMP_ABSOLUTE       354  'to 354'
         294  JUMP_FORWARD         57  'to 354'

 201     297  LOAD_FAST             0  'self'
         300  LOAD_ATTR             3  'panel'
         303  LOAD_ATTR            16  'lab_countdown_time'
         306  LOAD_ATTR            17  'SetString'
         309  LOAD_GLOBAL          18  'str'
         312  LOAD_FAST             3  'left_time'
         315  CALL_FUNCTION_1       1 
         318  CALL_FUNCTION_1       1 
         321  POP_TOP          

 202     322  LOAD_FAST             0  'self'
         325  LOAD_ATTR             3  'panel'
         328  LOAD_ATTR            13  'nd_countdown'
         331  LOAD_ATTR            15  'setVisible'
         334  LOAD_GLOBAL          12  'True'
         337  CALL_FUNCTION_1       1 
         340  POP_TOP          

 203     341  LOAD_FAST             0  'self'
         344  LOAD_ATTR            19  '_check_and_show_countdown'
         347  LOAD_FAST             3  'left_time'
         350  CALL_FUNCTION_1       1 
         353  POP_TOP          
       354_0  COME_FROM                '294'
       354_1  COME_FROM                '138'

Parse error at or near `CALL_FUNCTION_3' instruction at offset 232

    def on_player_gulag_state_changed(self, gulag_state, **kwargs):
        from logic.gcommon.common_const.battle_const import ST_IDLE
        self.is_in_gulag = gulag_state != ST_IDLE