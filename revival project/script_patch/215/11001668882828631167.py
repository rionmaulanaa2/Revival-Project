# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartSceneSound.py
from __future__ import absolute_import
import six_ex
from .ScenePart import ScenePart
from common.cfg import confmgr
from common.utils.timer import CLOCK
import math3d
from logic.gcommon.common_const.scene_const import MTL_DIRT, MTL_METAL, MTL_STONE, MTL_SAND, MTL_WOOD, MTL_DEEP_WATER, MTL_GRASS, MTL_GLASS, MTL_WATER, MTL_HOUSE, MTL_ICE
from logic.gcommon.common_utils.parachute_utils import STAGE_LAND, STAGE_ISLAND

class PartSceneSound(ScenePart):
    INIT_EVENT = {'scene_player_setted_event': 'on_player_setted',
       'on_player_parachute_stage_changed': 'on_stage_changed'
       }
    ENTER_EVENT = {}
    tick_dur = 1.0
    WATER_MAP = {MTL_WATER: 'river',
       MTL_DEEP_WATER: 'river'
       }
    MTL_MAP = {MTL_SAND: 'desert',
       MTL_GRASS: 'field'
       }
    AREA_MAP = {101: 'uptown',
       102: 'factory',
       103: 'downtown',
       104: 'mine',
       105: 'factory',
       106: 'downtown',
       107: 'uptown',
       108: 'uptown',
       109: 'factory',
       110: 'factory'
       }
    DEFAULT = 'field'

    def __init__(self, scene, name, need_update=False):
        super(PartSceneSound, self).__init__(scene, name, need_update)
        self.init_param()

    def init_param(self):
        self.player = None
        conf = confmgr.get('scene_sound_conf')
        self.spot_conf = conf['SpotSound']['Content']
        self.spot_timer_id = None
        self.spot_sound_id = {}
        self.spot_game_obj_id = {}
        self.spot_sound = []
        self.area_timer_id = None
        self.area_play_id = None
        self.area_state = None
        self.parachute_stage = None
        self.scene_name = ''
        return

    def on_enter(self):
        self.record_scene_name()
        self.register_game_obj()
        self.init_spot()

    def init_spot(self):
        self.spot_sound = []
        idx = 0
        for item in six_ex.values(self.spot_conf):
            if item['scene_name'] == self.scene_name:
                self.spot_sound.append({idx: item})
            idx += 1

    def record_scene_name(self):
        self.scene_name = global_data.battle.get_scene_name()

    def register_game_obj(self):
        self.obj_2d_id = global_data.sound_mgr.register_game_obj('scene_area_sound')

    def register_spot_game_obj(self, key):
        return global_data.sound_mgr.register_game_obj(key)

    def unregister_spot_game_obj(self, key):
        global_data.sound_mgr.unregister_game_obj(key)

    def on_player_setted(self, player):
        self.player = player
        self.post_spot_sound()

    def on_stage_changed(self, stage):
        if not self.scene_name:
            return
        if self.scene_name == 'kongdao':
            if stage in (STAGE_ISLAND, STAGE_LAND):
                self.post_area_sound()
            elif self.parachute_stage == STAGE_ISLAND:
                self.stop_area_sound()
        self.parachute_stage = stage

    def post_spot_sound(self):
        if self.spot_sound:
            self.spot_sound_id = {}
            self.spot_game_obj_id = {}
            self.init_spot_timer()

    def init_spot_timer(self):
        if self.spot_timer_id:
            global_data.game_mgr.unregister_logic_timer(self.spot_timer_id)
        self.spot_timer_id = global_data.game_mgr.register_logic_timer(self.tick_spot, interval=self.tick_dur, mode=CLOCK)

    def tick_spot(self, *args):
        if not self.player:
            return
        ppos = self.player.ev_g_position()
        if not ppos:
            return
        for idx, item in enumerate(self.spot_sound):
            cpos = item[idx]['pos']
            pos = math3d.vector(cpos[0], cpos[1], cpos[2])
            decay = item[idx]['decay']
            dis = (ppos - pos).length
            if dis < decay:
                if idx in self.spot_sound_id:
                    pass
                else:
                    game_obj_id = self.register_spot_game_obj('scene_spot_{}'.format(idx))
                    self.spot_game_obj_id[idx] = game_obj_id
                    event = item[idx]['event']
                    play_id = global_data.sound_mgr.post_event(event, game_obj_id, pos)
                    self.spot_sound_id[idx] = play_id
            elif idx in self.spot_sound_id:
                global_data.sound_mgr.stop_playing_id(self.spot_sound_id[idx])
                del self.spot_sound_id[idx]
                self.unregister_spot_game_obj(self.spot_game_obj_id[idx])
                del self.spot_game_obj_id[idx]

    def post_area_sound(self):
        if self.area_play_id:
            global_data.sound_mgr.stop_playing_id(self.area_play_id)
        self.set_area_state()
        self.area_play_id = global_data.sound_mgr.post_event_2d('Play_amb_area_fukongdao', self.obj_2d_id)
        self.init_area_timer()

    def init_area_timer(self):
        if self.area_timer_id:
            global_data.game_mgr.unregister_logic_timer(self.area_timer_id)
        self.area_timer_id = global_data.game_mgr.register_logic_timer(self.tick_area, interval=self.tick_dur, mode=CLOCK)

    def tick_area(self, *args):
        if not self.player:
            return
        pos = self.player.ev_g_position()
        if not pos:
            return
        mtl_idx = self.scene().get_scene_info_2d(pos.x, pos.z)
        if mtl_idx in self.WATER_MAP:
            state = self.WATER_MAP[mtl_idx]
            if state == self.area_state:
                return
            self.set_area_state(state)
        else:
            area_info = self.scene().get_scene_area_info(pos.x, pos.z)
            if area_info in self.AREA_MAP:
                state = self.AREA_MAP[area_info]
                if state == self.area_state:
                    return
                self.set_area_state(state)
            else:
                final_state = self.MTL_MAP.get(mtl_idx, self.DEFAULT)
                if final_state == self.area_state:
                    return
                self.set_area_state(final_state)

    def set_area_state(self, state=DEFAULT):
        global_data.sound_mgr.set_state('area_fukongdao', state)
        self.area_state = state

    def on_update(self, dt):
        pass

    def stop_area_sound(self):
        if self.area_timer_id:
            global_data.game_mgr.unregister_logic_timer(self.area_timer_id)
            self.area_timer_id = None
        if self.area_play_id:
            global_data.sound_mgr.stop_playing_id(self.area_play_id)
            self.area_play_id = None
        return

    def on_exit(self):
        if self.spot_timer_id:
            global_data.game_mgr.unregister_logic_timer(self.spot_timer_id)
            self.spot_timer_id = None
        if self.spot_sound_id:
            for sound_id in six_ex.values(self.spot_sound_id):
                global_data.sound_mgr.stop_playing_id(sound_id)

            self.spot_sound_id = {}
        if self.spot_game_obj_id:
            for game_obj_id in six_ex.values(self.spot_game_obj_id):
                global_data.sound_mgr.unregister_game_obj(game_obj_id)

            self.spot_game_obj_id = {}
        if self.area_timer_id:
            global_data.game_mgr.unregister_logic_timer(self.area_timer_id)
            self.area_timer_id = None
        if self.area_play_id:
            global_data.sound_mgr.stop_playing_id(self.area_play_id)
            self.area_play_id = None
        self.parachute_stage = None
        return