# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartLobbyCharacter.py
from __future__ import absolute_import
from __future__ import print_function
import game
from . import ScenePart
from logic.units.LLobbyAvatar import LLobbyAvatar
from logic.units.LPet import LPet
from logic.comsys.lobby.LobbyRockerUI import LobbyRockerUI
import game3d
import logic.vscene.parts.ctrl.GamePyHook as game_hook
from common.cfg import confmgr

class PartLobbyCharacter(ScenePart.ScenePart):
    ENTER_EVENT = {'on_login_success_event': 'on_avatar_login_success'
       }

    def __init__(self, scene, name):
        super(PartLobbyCharacter, self).__init__(scene, name, True)
        self.init_event()
        self.init_keyboard_keys()
        self._delay_exec_id = None
        self._mp_puppets = {}
        return

    def on_enter(self):
        if not global_data.player:
            self.delay_create_character()
        else:
            self.create_character()

    def on_avatar_login_success(self):
        if global_data.lobby_player and global_data.player:
            global_data.lobby_player._owner = global_data.player
            global_data.player.on_visit_ready()

    def delay_create_character(self):

        def callback():
            if not global_data.player:
                self.delay_create_character()
            else:
                self.create_character()

        self._delay_exec_id = game3d.delay_exec(1000, callback)

    def create_character(self):
        player = LLobbyAvatar(global_data.player, None)
        global_data.lobby_player = player
        player.init_from_dict({'role_id': global_data.player.get_role()})
        self.register_keys()
        if not global_data.is_pc_mode:
            LobbyRockerUI()
        global_data.player.on_visit_ready()
        self.create_pet()
        return

    def create_pet(self, *args):
        from logic.gcommon.cdata.pet_status_config import PT_IDLE
        if not global_data.player or not global_data.lobby_player:
            return
        else:
            if not global_data.player.is_valid:
                return
            skin_id = global_data.player.get_choosen_pet()
            base_skin_id = confmgr.get('c_pet_info', str(skin_id), 'base_skin', default=skin_id)
            pet_item = global_data.player.get_item_by_no(base_skin_id)
            if pet_item:
                level = pet_item.level if 1 else 1
                if global_data.lobby_pet:
                    cur_skin_id = global_data.lobby_pet.ev_g_skin_id()
                    cur_level = global_data.lobby_pet.ev_g_level()
                    if cur_skin_id == skin_id and cur_level == level:
                        return
                    global_data.lobby_pet.destroy()
                    global_data.lobby_pet = None
                return skin_id or None
            pet = LPet(global_data.player, None)
            pet.init_from_dict({'owner_logic': global_data.lobby_player,
               'npc_id': 11001,'default_state': PT_IDLE,'pet_id': skin_id,
               'level': level,'in_lobby': True})
            global_data.lobby_pet = pet
            return

    def on_pause(self, flag):
        if flag and global_data.lobby_player:
            global_data.lobby_player.send_event('E_CLEAR_MODEL_LOAD_TASK')
        if not flag:
            self.create_pet()
        elif global_data.lobby_pet:
            global_data.lobby_pet.destroy()
            global_data.lobby_pet = None
        return

    def init_keyboard_keys(self):
        self.down_keys = [
         game.VK_F]
        self.up_keys = []
        self.handler_map = {(game.VK_F, game.MSG_KEY_DOWN): self.handler_force
           }

    from logic.gutils.pc_utils import skip_when_debug_key_disabled

    @skip_when_debug_key_disabled
    def handler_force(self):
        from logic.gutils import scene_utils
        position = self.scene().active_camera.world_position
        scene_utils.show_scene_collision(position)

    def register_keys(self):
        game_hook.add_key_handler(game.MSG_KEY_DOWN, self.down_keys, self._key_handler)
        game_hook.add_key_handler(game.MSG_KEY_UP, self.up_keys, self._key_handler)

    def unregister_keys(self):
        game_hook.remove_key_handler(game.MSG_KEY_DOWN, self.down_keys, self._key_handler)
        game_hook.remove_key_handler(game.MSG_KEY_UP, self.up_keys, self._key_handler)

    def _key_handler(self, msg, keycode):
        print('handle msg', msg, 'keycode', keycode)
        handler = self.handler_map.get((keycode, msg), None)
        if handler:
            handler()
        return

    def init_event(self):
        pass

    def on_update(self, dt):
        if global_data.lobby_player:
            global_data.lobby_player.tick(dt)
        if global_data.lobby_pet:
            global_data.lobby_pet.tick(dt)

    def on_exit(self):
        self.unregister_keys()
        if self._delay_exec_id:
            game3d.cancel_delay_exec(self._delay_exec_id)
            self._delay_exec_id = None
        if global_data.lobby_player:
            global_data.lobby_player.destroy()
            global_data.lobby_player = None
        global_data.emgr.on_login_success_event -= self.on_avatar_login_success
        if global_data.lobby_pet:
            global_data.lobby_pet.destroy()
            global_data.lobby_pet = None
        return