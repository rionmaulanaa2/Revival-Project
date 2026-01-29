# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartArtCheckAvatar.py
from __future__ import absolute_import
import six
from . import ScenePart
import game
from logic.units.LArtTestAvatar import LArtTestAvatar
from mobile.client.ClientEntity import ArtTestAvatar
from logic.units.LArtTestMecha import LArtTestMecha
import logic.vscene.parts.ctrl.GamePyHook as game_hook

class PartArtCheckAvatar(ScenePart.ScenePart):
    ENTER_EVENT = {'on_player_rechoose_mecha_event': 'on_choose_mecha'
       }

    def __init__(self, scene, name):
        super(PartArtCheckAvatar, self).__init__(scene, name, True)
        self.ctrl_mecha = False
        self.entity = None
        self.player = None
        self.mecha = None
        self.down_keys = []
        self.up_keys = []
        self.handler_map = {(game.VK_G, game.MSG_KEY_UP): self.on_choose_mecha,
           (game.VK_J, game.MSG_KEY_DOWN): (
                                          self.begin_fire, True),
           (game.VK_J, game.MSG_KEY_UP): (
                                        self.begin_fire, False)
           }
        for keycode, msg in six.iterkeys(self.handler_map):
            if msg == game.MSG_KEY_UP:
                self.up_keys.append(keycode)
            elif msg == game.MSG_KEY_DOWN:
                self.down_keys.append(keycode)

        return

    def on_enter(self):
        global_data.player = self.entity = ArtTestAvatar()
        self.create_character()

    def create_character(self):
        global_data.lobby_player = self.player = LArtTestAvatar(self.entity, None)
        self.entity.logic = self.player
        global_data.lobby_player.send_event('E_ENABLE_FREE_CAMERA', True)
        global_data.artcheck_scene = self.get_scene()
        self.player.init_from_dict({'role_id': 11})
        self.register_keys()
        return

    def create_mecha(self, mecha_id=None, skin_folder=None, lod=None):
        global_data.mecha = self.mecha = LArtTestMecha(self.entity, None)
        self.entity.logic = self.mecha
        self.mecha.init_from_dict({'npc_id': mecha_id,
           'mecha_id': mecha_id,
           'skin_folder': skin_folder,
           'lod': lod
           })
        return

    def destroy_mecha(self):
        if self.mecha:
            self.mecha.destroy()
        global_data.mecha = self.mecha = None
        return

    def on_update(self, dt):
        if not self.ctrl_mecha and global_data.lobby_player:
            global_data.lobby_player.tick(dt)
        elif self.ctrl_mecha and global_data.mecha:
            global_data.mecha.tick(dt)

    def on_choose_mecha(self, mecha_id=None, skin_folder=None, lod=None):
        self.ctrl_mecha = bool(mecha_id)
        if self.ctrl_mecha:
            self.player.destroy()
            global_data.lobby_player = None
            self.destroy_mecha()
            self.create_mecha(mecha_id, skin_folder, lod)
        elif self.mecha:
            self.destroy_mecha()
            self.create_character()
        global_data.emgr.on_observer_global_join_mecha.emit(self.ctrl_mecha)
        return

    def begin_fire(self, flag):
        if self.ctrl_mecha and global_data.mecha:
            global_data.mecha.send_event('E_SET_ATTR', 'keep_fire', flag)

    def on_exit(self):
        pass

    def register_keys(self):
        game_hook.add_key_handler(game.MSG_KEY_DOWN, self.down_keys, self._key_handler)
        game_hook.add_key_handler(game.MSG_KEY_UP, self.up_keys, self._key_handler)

    def unregister_keys(self):
        game_hook.remove_key_handler(game.MSG_KEY_DOWN, self.down_keys, self._key_handler)
        game_hook.remove_key_handler(game.MSG_KEY_UP, self.up_keys, self._key_handler)

    def _key_handler(self, msg, keycode):
        handler = self.handler_map.get((keycode, msg), None)
        args = []
        if type(handler) in (list, tuple):
            args = list(handler)
            handler = args.pop(0)
        if callable(handler):
            handler(*args)
        return