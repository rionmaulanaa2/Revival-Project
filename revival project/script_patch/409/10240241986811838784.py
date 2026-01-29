# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_building/ComMusicPlayer.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from mobile.common.IdManager import IdManager

class ComMusicPlayer(UnitCom):
    BIND_EVENT = {'E_SHOW_DISTURB_CIRCLE': '_on_show_distrub_circle',
       'E_COLLSION_LOADED': '_on_col_loaded'
       }

    def __init__(self):
        super(ComMusicPlayer, self).__init__()

    def init_from_dict(self, unit_obj, bdict):
        super(ComMusicPlayer, self).init_from_dict(unit_obj, bdict)
        self._pos = self.ev_g_position()
        self._show_circle = False
        self._music_obj = global_data.sound_mgr.register_game_obj('music_player')
        self._play_id = None
        effect_players = bdict.get('effect_players', [])
        player = global_data.player
        if player is not None and player.id in effect_players:
            self._on_show_distrub_circle(True)
        return

    def _on_show_distrub_circle(self, show_circle):
        global_data.emgr.scene_draw_music_disturb_circle.emit(show_circle, IdManager.id2str(self.unit_obj.id), self._pos)
        if show_circle:
            self._play_id = global_data.sound_mgr.post_event('Play_musicplayer', self._music_obj, self._pos)
        elif self._play_id:
            global_data.sound_mgr.stop_playing_id(self._play_id)
            self._play_id = None
        return

    def destroy(self):
        global_data.sound_mgr.unregister_game_obj(self._music_obj)
        if self._play_id:
            global_data.sound_mgr.stop_playing_id(self._play_id)
            self._play_id = None
        super(ComMusicPlayer, self).destroy()
        return

    def _on_col_loaded(self, m, col):
        self.send_event('E_MOUNTS_LOADED', m, 'ActionDriveMusicPlayer')