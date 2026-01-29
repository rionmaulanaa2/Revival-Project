# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComMonsterSound.py
from __future__ import absolute_import
from __future__ import print_function
from .ComMechaSound import ComMechaSound
from common.cfg import confmgr
import six

class ComMonsterSound(ComMechaSound):
    BIND_EVENT = ComMechaSound.BIND_EVENT.copy()
    BIND_EVENT.update({'E_ON_STATE_EXIT': 'on_state_exit'
       })

    def init_from_dict(self, unit_obj, bdict):
        super(ComMonsterSound, self).init_from_dict(unit_obj, bdict)
        self.monster_id = bdict.get('npc_id')
        self.game_obj_id = self._human_sound_id
        self.state_rec = {}

    def on_model_loaded(self, model):
        conf = confmgr.get('pve_monster_sound', str(self.monster_id), default={})
        if not conf:
            return
        for anim, anim_conf in six.iteritems(conf):
            for event, event_conf in six.iteritems(anim_conf):
                for param in event_conf:
                    self.send_event('E_REGISTER_ANIM_KEY_EVENT', anim, event, self.trigger_anim_event, param, True)

    def trigger_anim_event(self, model, anim, event, data=None):
        c_type, sound, state, need_stop = data
        if global_data.debug_pve_state:
            print('ComMonsterSound trigger_anim_event', anim, event, c_type, sound, state, need_stop)
        if c_type:
            play_id = global_data.sound_mgr.post_event(sound, self.game_obj_id, self.ev_g_position())
            if need_stop:
                ori_play_id = self.state_rec.get(state, {}).get(sound, None)
                if ori_play_id:
                    global_data.sound_mgr.stop_playing_id(ori_play_id)
                self.state_rec.setdefault(state, {})
                self.state_rec[state][sound] = play_id
        else:
            play_id = self.state_rec.get(state, {}).get(sound, None)
            if play_id:
                global_data.sound_mgr.stop_playing_id(play_id)
                self.state_rec[state][sound] = None
        return

    def on_state_exit(self, sid):
        if sid in self.state_rec:
            for play_id in six.itervalues(self.state_rec[sid]):
                global_data.sound_mgr.stop_playing_id(play_id)

            self.state_rec[sid] = {}

    def destroy(self):
        super(ComMonsterSound, self).destroy()
        for sid in self.state_rec:
            for play_id in six.itervalues(self.state_rec[sid]):
                global_data.sound_mgr.stop_playing_id(play_id)

        self.state_rec = {}