# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComSpotSoundPlayer.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
import math3d
import six

class ComSpotSoundPlayer(UnitCom):
    BIND_EVENT = {'E_SPOT_SOUND_PLAYER': 'ret_spot_sound'
       }

    def __init__(self):
        super(ComSpotSoundPlayer, self).__init__()

    def init_from_dict(self, unit_obj, bdict):
        super(ComSpotSoundPlayer, self).init_from_dict(unit_obj, bdict)
        self.pos = math3d.vector(*bdict.get('position'))
        self.event_name = bdict.get('sound_name').encode('utf-8')
        self.event_name = six.ensure_str(self.event_name)
        self.obj_id = None
        self.sound_id = None
        return

    def cache(self):
        self.clear_sound()
        super(ComSpotSoundPlayer, self).cache()

    def destroy(self):
        self.clear_sound()
        super(ComSpotSoundPlayer, self).destroy()

    def ret_spot_sound(self, ret):
        self.clear_sound()
        if ret:
            self.obj_id = global_data.sound_mgr.register_game_obj('SpotPlayer')
            self.sound_id = global_data.sound_mgr.post_event(self.event_name, self.obj_id, self.pos)

    def clear_sound(self):
        if self.sound_id:
            global_data.sound_mgr.stop_playing_id(self.sound_id)
            self.sound_id = None
        if self.obj_id:
            global_data.sound_mgr.unregister_game_obj(self.obj_id)
            self.obj_id = None
        return