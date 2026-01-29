# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_item/ComPickableSound.py
from __future__ import absolute_import
import math3d
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.const import NEOX_UNIT_SCALE
from common.cfg import confmgr
import common.utils.timer as timer

class ComPickableSound(UnitCom):
    BIND_EVENT = {'E_MODEL_LOADED': '_on_model_loaded',
       'E_SCENE_BOX_STAT_CHANGE': '_on_scene_box_stat_change',
       'E_PLAY_OPENING_SOUND': '_on_play_opening_sound',
       'E_STOP_OPENING_SOUND': '_on_stop_opening_sound'
       }
    BOX_SOUND_MAX_DIS_SQR = (50 * NEOX_UNIT_SCALE) ** 2
    BOX_SOUND_MIN_DIS_SQR = (45 * NEOX_UNIT_SCALE) ** 2

    def __init__(self):
        super(ComPickableSound, self).__init__()
        self._sound_id = None
        self._sound_player_id = None
        self._check_timer = None
        self._opening_sound_id = None
        return

    def reuse(self, share_data):
        super(ComPickableSound, self).reuse(share_data)
        self._sound_id = None
        self._sound_player_id = None
        self._check_timer = None
        self._opening_sound_id = None
        return

    def cache(self):
        self.del_box_sound()
        super(ComPickableSound, self).cache()

    def init_from_dict(self, unit_obj, bdict):
        super(ComPickableSound, self).init_from_dict(unit_obj, bdict)
        self._item_id = bdict.get('item_id')
        x, y, z = bdict.get('position', (0, 0, 0))
        self._item_pos = math3d.vector(x, y, z)

    def destroy(self):
        self.del_box_sound()
        super(ComPickableSound, self).destroy()

    def _on_model_loaded(self, model):
        if not self.ev_g_scene_box_is_open():
            self.add_box_sound(self._item_pos, self._item_id)

    def _on_scene_box_stat_change(self, status):
        open_sound = confmgr.get('item', str(self._item_id), 'open_sound', default=None)
        if open_sound and self.unit_obj.is_model_valid():
            position = self.unit_obj.get_model_attr('position')
            global_data.sound_mgr.play_sound('Play_props', position, ('props_option', open_sound))
        self.del_box_sound()
        return

    def _on_play_opening_sound(self, item_id=None):
        if item_id is not None:
            opening_sound = confmgr.get('item', str(item_id), 'opening_sound', default=None)
        else:
            opening_sound = confmgr.get('item', str(self._item_id), 'opening_sound', default=None)
        if opening_sound and self.unit_obj.is_model_valid():
            position = self.unit_obj.get_model_attr('position')
            self._opening_sound_id = global_data.sound_mgr.play_sound('Play_props', position, ('props_option', opening_sound))
        return

    def _on_stop_opening_sound(self):
        if self._opening_sound_id:
            global_data.sound_mgr.stop_playing_id(self._opening_sound_id)
            self._opening_sound_id = None
        return

    def add_box_sound(self, pos, item_id):
        sound_conf = confmgr.get('item_backpack_sound_conf', str(self._item_id), default=None)
        if sound_conf:
            sound_mgr = global_data.sound_mgr
            self._sound_id = global_data.sound_mgr.register_game_obj('item_backpack')
            sound_mgr.set_position(self._sound_id, pos)
            sound_mgr.set_switch('box', 'treasure_chest', self._sound_id)
            self._check_timer = global_data.game_mgr.register_logic_timer(self.check_sound, interval=1, times=-1, mode=timer.CLOCK)
        return

    def check_sound(self):
        if not self.unit_obj.is_model_valid():
            return
        else:
            cam_lplayer = global_data.cam_lplayer
            if not cam_lplayer:
                return
            player_pos = cam_lplayer.ev_g_model_position()
            if not player_pos:
                return
            distance_sqr = (player_pos - self.unit_obj.get_model_attr('world_position')).length_sqr
            if distance_sqr < self.BOX_SOUND_MIN_DIS_SQR and not self._sound_player_id and self._sound_id:
                self._sound_player_id = global_data.sound_mgr.post_event('Play_treasure_chest', self._sound_id)
            elif distance_sqr > self.BOX_SOUND_MAX_DIS_SQR and self._sound_player_id:
                global_data.sound_mgr.stop_playing_id(self._sound_player_id)
                self._sound_player_id = None
            return

    def del_box_sound(self, *args):
        if self._sound_player_id:
            global_data.sound_mgr.stop_playing_id(self._sound_player_id)
            self._sound_player_id = None
        if self._sound_id:
            global_data.sound_mgr.unregister_game_obj(self._sound_id)
            self._sound_id = None
        if self._check_timer:
            global_data.game_mgr.unregister_logic_timer(self._check_timer)
            self._check_timer = None
        return