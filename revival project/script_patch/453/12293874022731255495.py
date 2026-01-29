# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComMechaBlind.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
import math3d
from logic.gcommon.common_const.buff_const import BUFF_ID_8034_BLIND
from logic.gutils.screen_effect_utils import create_screen_effect_directly
from logic.gutils.screen_effect_utils import SCREEN_EFFECT_SCALE
from logic.gcommon.const import SFX_FULL_SCREEN_SIZE
SMOKE_SFX_PATH = 'effect/fx/mecha/8034/8034_smoke_pm_start.sfx'
PM_SFX_PATH = 'effect/fx/mecha/8034/8034_smoke_pm.sfx'
FULL_BLIND_SFX_PATH = 'effect/fx/mecha/8034/8034_vice_pm_01.sfx'
SFX_POS = [
 [
  (0.5, -140), (0.5, -160)],
 [
  (-0.5, 140), (-0.5, 160)],
 [
  (0.5, -140), (-0.5, 160)],
 [
  (-0.5, 140), (0.5, -160)],
 [
  (0, 0), (-0.5, -40)],
 [
  (0, 0), (0.5, 40)]]

def get_sfx_pos--- This code section failed: ---

  25       0  LOAD_FAST             0  'idx'
           3  LOAD_GLOBAL           0  'len'
           6  LOAD_GLOBAL           1  'SFX_POS'
           9  CALL_FUNCTION_1       1 
          12  COMPARE_OP            5  '>='
          15  POP_JUMP_IF_TRUE     27  'to 27'
          18  POP_JUMP_IF_TRUE      1  'to 1'
          21  COMPARE_OP            0  '<'
        24_0  COME_FROM                '18'
        24_1  COME_FROM                '15'
          24  POP_JUMP_IF_FALSE    46  'to 46'

  26      27  LOAD_GLOBAL           2  'math3d'
          30  LOAD_ATTR             3  'vector'
          33  LOAD_CONST            1  ''
          36  LOAD_CONST            1  ''
          39  LOAD_CONST            1  ''
          42  CALL_FUNCTION_3       3 
          45  RETURN_END_IF    
        46_0  COME_FROM                '24'

  27      46  LOAD_GLOBAL           2  'math3d'
          49  LOAD_ATTR             3  'vector'

  28      52  LOAD_GLOBAL           1  'SFX_POS'
          55  LOAD_FAST             0  'idx'
          58  BINARY_SUBSCR    
          59  LOAD_CONST            1  ''
          62  BINARY_SUBSCR    
          63  LOAD_CONST            1  ''
          66  BINARY_SUBSCR    
          67  LOAD_GLOBAL           4  'SFX_FULL_SCREEN_SIZE'
          70  LOAD_CONST            1  ''
          73  BINARY_SUBSCR    
          74  BINARY_MULTIPLY  
          75  LOAD_GLOBAL           5  'SCREEN_EFFECT_SCALE'
          78  LOAD_ATTR             6  'x'
          81  BINARY_MULTIPLY  
          82  LOAD_GLOBAL           1  'SFX_POS'
          85  LOAD_FAST             0  'idx'
          88  BINARY_SUBSCR    
          89  LOAD_CONST            1  ''
          92  BINARY_SUBSCR    
          93  LOAD_CONST            2  1
          96  BINARY_SUBSCR    
          97  BINARY_ADD       

  29      98  LOAD_GLOBAL           1  'SFX_POS'
         101  LOAD_FAST             0  'idx'
         104  BINARY_SUBSCR    
         105  LOAD_CONST            2  1
         108  BINARY_SUBSCR    
         109  LOAD_CONST            1  ''
         112  BINARY_SUBSCR    
         113  LOAD_GLOBAL           4  'SFX_FULL_SCREEN_SIZE'
         116  LOAD_CONST            2  1
         119  BINARY_SUBSCR    
         120  BINARY_MULTIPLY  
         121  LOAD_GLOBAL           5  'SCREEN_EFFECT_SCALE'
         124  LOAD_ATTR             7  'y'
         127  BINARY_MULTIPLY  
         128  LOAD_GLOBAL           1  'SFX_POS'
         131  LOAD_FAST             0  'idx'
         134  BINARY_SUBSCR    
         135  LOAD_CONST            2  1
         138  BINARY_SUBSCR    
         139  LOAD_CONST            2  1
         142  BINARY_SUBSCR    
         143  BINARY_ADD       

  30     144  LOAD_CONST            1  ''
         147  CALL_FUNCTION_3       3 
         150  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `POP_JUMP_IF_TRUE' instruction at offset 18


def on_create_sfx(sfx, alpha):
    sfx.alpha_percent = alpha


class ComMechaBlind(UnitCom):
    BIND_EVENT = {'E_SYNC_BLIND': 'on_sync_blind'
       }

    def init_from_dict(self, unit_obj, bdict):
        super(ComMechaBlind, self).init_from_dict(unit_obj, bdict)
        self.blind_score = 0
        self.is_blind_ongoing = False
        self.inc_value = 0
        self.dec_value = 0
        self.sfx_list = [ None for i in range(len(SFX_POS)) ]
        self.full_blind_sfx = None
        self.full_blind = False
        self.need_update = False
        self.is_cam_player = bool(global_data.cam_lplayer and self.sd.ref_driver_id == global_data.cam_lplayer.id)
        self.process_event(True)
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'scene_observed_player_setted_event': self.on_player_setted
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_player_setted(self, *args):
        is_cam_player = bool(global_data.cam_lplayer and self.sd.ref_driver_id == global_data.cam_lplayer.id)
        if is_cam_player ^ self.is_cam_player:
            self.is_cam_player = is_cam_player
            if not is_cam_player:
                global_data.sfx_mgr.remove_sfx_by_id(self.full_blind_sfx)
                self.full_blind_sfx = None
                for i, sfx_id in enumerate(self.sfx_list):
                    global_data.sfx_mgr.remove_sfx_by_id(sfx_id)
                    self.sfx_list[i] = None

        return

    def on_sync_blind(self, blind_detail):
        self.blind_score = blind_detail.get('blind_score', 0)
        is_blind_ongoing = blind_detail.get('is_blind_ongoing', False)
        self.sd.ref_is_blinded = is_blind_ongoing
        if self.is_cam_player and is_blind_ongoing ^ self.is_blind_ongoing:
            global_data.sound_mgr.play_sound_2d('m_8034_gas_in_1p' if is_blind_ongoing else 'm_8034_gas_out_1p')
            global_data.emgr.cam_lplayer_in_fog_changed.emit(is_blind_ongoing)
        self.is_blind_ongoing = is_blind_ongoing
        self.inc_value = blind_detail.get('inc_value', 0)
        self.dec_value = blind_detail.get('dec_value', 0)
        self.need_update = True
        self.update_flag_ui()

    def update_flag_ui(self):
        self.send_event('E_AUTO_AIM_BY_OTHERS', self.blind_score > 0.0 and not self.full_blind, BUFF_ID_8034_BLIND, None)
        self.send_event('E_AUTO_AIM_BY_OTHERS', self.blind_score > 0.0 and self.full_blind, BUFF_ID_8034_BLIND + 1, None)
        return

    def tick(self, delta):
        self.blind_score = min(max(self.blind_score + (self.inc_value if self.is_blind_ongoing else -self.dec_value) * delta, 0.0), 1.0)
        self.update_pm_sfx()
        full_blind = self.blind_score >= 1.0
        if full_blind ^ self.full_blind:
            self.on_full_blind(full_blind)
        self.need_update = self.blind_score < 1.0 and self.is_blind_ongoing or self.blind_score > 0.0 and not self.is_blind_ongoing

    def update_pm_sfx(self):
        if not self.is_cam_player:
            return
        else:
            for i, sfx_id in enumerate(self.sfx_list):
                sfx_alpha = min(max(self.blind_score * len(SFX_POS) - i, 0), 1)
                if sfx_id:
                    sfx = global_data.sfx_mgr.get_sfx_by_id(sfx_id)
                    if sfx:
                        if sfx.alpha_percent == 0.0 and sfx_alpha == 0.0:
                            global_data.sfx_mgr.remove_sfx_by_id(sfx_id)
                            self.sfx_list[i] = None
                        else:
                            sfx.alpha_percent = sfx_alpha
                    elif sfx_alpha == 0.0 and not self.is_blind_ongoing:
                        global_data.sfx_mgr.remove_sfx_by_id(sfx_id)
                        self.sfx_list[i] = None
                elif sfx_alpha > 0:
                    self.sfx_list[i] = create_screen_effect_directly(SMOKE_SFX_PATH, get_sfx_pos(i), on_create_func=lambda sfx, a=sfx_alpha: on_create_sfx(sfx, a))

            return

    def on_full_blind(self, is_full_blind):
        self.full_blind = is_full_blind
        if self.is_cam_player:
            if is_full_blind:
                self.full_blind_sfx = global_data.sfx_mgr.create_sfx_in_scene(FULL_BLIND_SFX_PATH, math3d.vector(0, 0, 0))
            else:
                global_data.sfx_mgr.remove_sfx_by_id(self.full_blind_sfx)
                self.full_blind_sfx = None
        else:
            self.update_flag_ui()
        return

    def destroy(self):
        super(ComMechaBlind, self).destroy()
        self.process_event(False)
        for sfx_id in self.sfx_list:
            global_data.sfx_mgr.remove_sfx_by_id(sfx_id)

        self.sfx_list = None
        global_data.sfx_mgr.remove_sfx_by_id(self.full_blind_sfx)
        self.full_blind_sfx = None
        return