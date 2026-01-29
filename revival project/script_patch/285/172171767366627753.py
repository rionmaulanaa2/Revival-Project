# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/control_ui/DroneUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import BASE_LAYER_ZORDER
import cc
from common.utils.cocos_utils import ccc3FromHex
from common.cfg import confmgr
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.const import uiconst

class DroneUI(BasePanel):
    PANEL_CONFIG_NAME = 'capsule/capsule_uav'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_exit.OnClick': '_control_back_to_human'
       }
    ASSOCIATE_UI_LIST = [
     'FightLeftShotUI', 'SceneInteractionUI', 'PickUI', 'FireRockerUI', 'ThrowRockerUI', 'FrontSightUI',
     'WeaponBarSelectUI', 'StateChangeUI', 'BulletReloadUI']
    TEXT_COLORS = ['#SW', '#SW', '#SD', '#SD', '#SR', '#SR', '#SR', '#SR', '#SD', '#SD']
    TIMER_ACTION = 1
    HEALTH_ACTION = 2
    DISTANCE_ACTION = 3
    TEXT_DICT = {TIMER_ACTION: 'lab_time',
       HEALTH_ACTION: 'lab_hp',
       DISTANCE_ACTION: 'lab_distance'
       }

    def on_init_panel(self):
        self.drone_npc_ref = None
        self.drone_timer = None
        self.left_time = None
        self.left_time_action = None
        self.max_dis = 0
        self.max_hp = 0
        self.hide_main_ui(DroneUI.ASSOCIATE_UI_LIST)
        self.init_event()
        self.panel.PlayAnimation('splash')
        return

    def on_finalize_panel(self):
        self.drone_npc_ref = None
        self.show_main_ui()
        return

    def init_event(self):
        emgr = global_data.emgr
        econf = {'scene_update_drone_distance': self._update_drone_distance,
           'scene_update_life_time': self._update_drone_lift_time,
           'scene_close_drone_ui': self.close_drone_ui,
           'sound_visible_add': self._sound_nearby
           }
        emgr.bind_events(econf)

    def close_drone_ui(self):
        drone_npc = self.drone_npc_ref() if self.drone_npc_ref else None
        if drone_npc:
            drone_npc.unregist_event('E_HEALTH_HP_CHANGE', self._hp_change)
        self.panel.SetTimeOut(0.8, self.close)
        self.panel.PlayAnimation('splash')
        return

    def _update_drone_distance(self, dis):
        self.panel.lab_distance.SetString(get_text_by_id(157).format(int(dis)))
        self.panel.progress_distance.SetPercentage((self.max_dis - dis) / self.max_dis * 100.0)
        if dis >= self.max_text_warning_dis:
            self.start_text_ani(DroneUI.DISTANCE_ACTION)
        else:
            self.panel.stopActionByTag(DroneUI.DISTANCE_ACTION)
            self.panel.lab_distance.SetColor('#SW')

    def _update_drone_health(self, health):
        self.lab_hp.SetString(get_text_by_id(158).format(health))
        if health <= 20:
            self.start_text_ani(DroneUI.HEALTH_ACTION)
        else:
            self.panel.stopActionByTag(DroneUI.HEALTH_ACTION)
            self.panel.lab_hp.SetColor('#SW')

    def _sound_nearby(self, *args):
        self.panel.StopAnimation('show_alarm')
        self.panel.PlayAnimation('show_alarm')

    def _update_drone_lift_time(self, left_time, full_time):
        self.left_time = left_time
        self.full_time = full_time
        if self.drone_timer:
            self.panel.nd_time.StopTimerAction()
        self.drone_timer = self.panel.nd_time.TimerAction(self._update_left_time, self.left_time, interval=1)
        self._update_left_time(None)
        return

    def _update_left_time(self, time):
        if self.left_time:
            self.left_time -= 1
            if self.left_time >= 0:
                percent = self.left_time / self.full_time * 100
                self.panel.progress_time.SetPercentage(percent)
                self.panel.lab_time.SetString(get_text_by_id(159).format(int(self.left_time)))
                if self.left_time < self.full_time - 10 and not self.panel.getActionByTag(DroneUI.TIMER_ACTION):
                    self.start_text_ani(DroneUI.TIMER_ACTION)
                return
        self.stopActionByTag(DroneUI.TIMER_ACTION)
        self.panel.lab_time.SetColor('#SW')
        self.left_time = None
        self.panel.nd_time.StopTimerAction()
        return

    def start_text_ani(self, tag):
        if self.panel.getActionByTag(tag):
            return
        from common.framework import Functor
        action = self.panel.runAction(cc.RepeatForever.create(cc.Sequence.create([
         cc.CallFunc.create(Functor(self.show_color, tag)),
         cc.DelayTime.create(0.1)])))
        action.setTag(tag)

    def show_color--- This code section failed: ---

 130       0  LOAD_GLOBAL           0  'getattr'
           3  LOAD_GLOBAL           1  'None'
           6  LOAD_FAST             1  'tag'
           9  BINARY_MODULO    
          10  LOAD_CONST            0  ''
          13  CALL_FUNCTION_3       3 
          16  STORE_FAST            2  'index'

 131      19  LOAD_FAST             2  'index'
          22  LOAD_CONST            0  ''
          25  COMPARE_OP            8  'is'
          28  POP_JUMP_IF_FALSE    57  'to 57'

 132      31  LOAD_GLOBAL           2  'setattr'
          34  LOAD_GLOBAL           1  'None'
          37  LOAD_FAST             1  'tag'
          40  BINARY_MODULO    
          41  LOAD_CONST            2  ''
          44  CALL_FUNCTION_3       3 
          47  POP_TOP          

 133      48  LOAD_CONST            2  ''
          51  STORE_FAST            2  'index'
          54  JUMP_FORWARD          0  'to 57'
        57_0  COME_FROM                '54'

 134      57  LOAD_GLOBAL           0  'getattr'
          60  LOAD_FAST             0  'self'
          63  LOAD_ATTR             3  'panel'
          66  LOAD_CONST            3  '%s'
          69  LOAD_FAST             0  'self'
          72  LOAD_ATTR             4  'TEXT_DICT'
          75  LOAD_FAST             1  'tag'
          78  BINARY_SUBSCR    
          79  BINARY_MODULO    
          80  LOAD_CONST            0  ''
          83  CALL_FUNCTION_3       3 
          86  STORE_FAST            3  'nd_txt'

 135      89  LOAD_FAST             3  'nd_txt'
          92  LOAD_ATTR             5  'SetColor'
          95  LOAD_FAST             0  'self'
          98  LOAD_ATTR             6  'TEXT_COLORS'
         101  LOAD_FAST             2  'index'
         104  BINARY_SUBSCR    
         105  CALL_FUNCTION_1       1 
         108  POP_TOP          

 136     109  LOAD_GLOBAL           2  'setattr'
         112  LOAD_GLOBAL           1  'None'
         115  LOAD_FAST             1  'tag'
         118  BINARY_MODULO    
         119  LOAD_FAST             2  'index'
         122  LOAD_CONST            4  1
         125  BINARY_ADD       
         126  LOAD_CONST            5  10
         129  BINARY_MODULO    
         130  CALL_FUNCTION_3       3 
         133  POP_TOP          
         134  LOAD_CONST            0  ''
         137  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 13

    def set_drone_npc(self, drone_npc, max_dis):
        import weakref
        self.max_dis = max_dis
        self.max_text_warning_dis = max_dis * 0.8
        self.hide_main_ui(DroneUI.ASSOCIATE_UI_LIST)
        self.panel.stopAllActions()
        self.drone_npc_ref = weakref.ref(drone_npc)
        self.init_health()

    def init_health(self):
        drone_npc = self.drone_npc_ref() if self.drone_npc_ref else None
        if drone_npc:
            cur_hp = drone_npc.ev_g_hp()
            self.max_hp = drone_npc.ev_g_max_hp()
            self.panel.progress_hp.SetPercentage(cur_hp / self.max_hp * 100.0)
            self.panel.lab_hp.SetString(get_text_by_id(158).format(cur_hp))
            drone_npc.regist_event('E_HEALTH_HP_CHANGE', self._hp_change)
        return

    def _hp_change(self, hp, mod):
        self.panel.progress_hp.SetPercentage(float(hp) / self.max_hp * 100.0)
        self.panel.lab_hp.SetString(get_text_by_id(158).format(hp))

    def _control_back_to_human(self, btn, touch):
        drone_npc = self.drone_npc_ref() if self.drone_npc_ref else None
        if drone_npc:
            drone_npc.send_event('E_YIELD_CONTROL', global_data.player.id)
        return