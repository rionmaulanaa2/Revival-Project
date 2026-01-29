# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/login_scene.py
from __future__ import absolute_import
from __future__ import print_function
import six
from six.moves import range
import math3d
import world
from common.cfg import confmgr

# OFFLINE MODE FLAG
OFFLINE_MODE = True

class LoginScene(world.scene):

    def __init__(self, scene_type, scene_data=None, callback=None, async_load=True, back_load=False):
        super(LoginScene, self).__init__()
        self.init_scene_info(scene_type, scene_data, callback)
        print('load scene id', id(self), scene_type)
        self.viewer_position = math3d.vector(0, 0, 0)
        self.tick_cnt = 0
        self.create_camera(True)
        
        # OFFLINE MODE: Auto-login and transition to main game
        if OFFLINE_MODE:
            print('[OFFLINE MODE] Skipping login UI, auto-logging in...')
            self.offline_auto_login()
        else:
            self.load_scene(callback, async_load, back_load)

    def get_player(self):
        return None

    def offline_auto_login(self):
        """OFFLINE MODE: Auto-authenticate locally without server checks"""
        print('[OFFLINE MODE] Initializing offline authentication...')
        
        # Create fake player/session data locally
        import six.moves.builtins as builtins
        if not hasattr(builtins, 'PLAYER_ID'):
            builtins.__dict__['PLAYER_ID'] = 'OFFLINE_PLAYER_001'
        if not hasattr(builtins, 'SESSION_ID'):
            builtins.__dict__['SESSION_ID'] = 'OFFLINE_SESSION_001'
        if not hasattr(builtins, 'OFFLINE_MODE'):
            builtins.__dict__['OFFLINE_MODE'] = True
        
        print('[OFFLINE MODE] Local player initialized: PLAYER_ID=%s' % builtins.__dict__.get('PLAYER_ID'))
        
        # Skip login UI entirely - transition directly to main game
        self.transition_to_main_game()

    def transition_to_main_game(self):
        """Skip LoginScene and load main game scene directly"""
        print('[OFFLINE MODE] Transitioning to main game scene...')
        
        # Get the Manager singleton and load the game scene
        from logic.core.managers.manager import Manager
        manager = Manager()
        
        # Load the actual gameplay scene instead of staying at login
        # Use 'BattleMain' or 'Main' depending on your game structure
        manager.post_exec(manager.load_scene, 'BattleMain', {})
        print('[OFFLINE MODE] Main game scene queued for loading')

    def init_scene_info(self, scene_type, scene_data, callback):
        self.valid = True
        self.scene_type = scene_type
        self.scene_conf = confmgr.get('scenes', scene_type)
        self.scene_data = {} if scene_data is None else scene_data
        self._loaded = False
        self.parts = {}
        self.update_part_list = set()
        self.load_parts()
        return

    def __str__(self):
        return '{{Scene:{0} {1}}}'.format(self.scene_type, id(self))

    def reset_data(self):
        self.valid = False
        self.scene_data = None
        self.scene_conf = None
        self.parts = {}
        self.update_part_list = set()
        return

    def reinit_scene(self, scene_type, scene_data, callback):
        if self.parts:
            log_error('Try to reinit a unrelease scene!!!!')
            import traceback
            traceback.print_stack()
        self.reset_data()
        self.init_scene_info(scene_type, scene_data, callback)
        for cname, com in six.iteritems(self.parts):
            com.on_pre_load()

        for cname, com in six.iteritems(self.parts):
            com.on_load()

        self.on_enter()
        if callback:
            callback()

    def destroy(self):
        if not self.valid:
            return
        if self._loaded:
            raise Exception('destroy without calling scene.on_exit()')
        self.reset_data()
        super(LoginScene, self).destroy()

    def get_type(self):
        return self.scene_type

    def is_same_scene(self, scene_type, scene_data):
        print('self.scene type', self.scene_type, 'new scene type', scene_type)
        if self.scene_type != scene_type:
            return False
        return self.is_same_scene_path(scene_data)

    def on_pause(self, *args):
        pass

    def is_same_scene_path(self, scene_data):
        print('scene data is', scene_data)
        scene_path = scene_data.get('scene_path', None)
        print('self scene path', self._get_scene_data('scene_path', None), 'new scene path', scene_path)
        if scene_path:
            return scene_path == self._get_scene_data('scene_path', None)
        else:
            return False

    def _get_scene_data(self, key, default=None):
        return self.scene_data.get(key, self.scene_conf.get(key, default))

    def load_scene(self, callback=None, async_load=True, back_load=False):

        def _load_finish_cb():
            if not self.valid:
                return
            for cname, com in six.iteritems(self.parts):
                com.on_load()

            if back_load:
                self._loaded = True
                self.logic(0.1)
                self.post_logic(0.1)
                self._loaded = False
            else:
                self.on_enter()
            if callback:
                callback()

        scn_path = self._get_scene_data('scene_path', None)
        async_load = self._get_scene_data('async_load', async_load)
        for cname, com in six.iteritems(self.parts):
            com.on_pre_load()

        if scn_path:
            self.load(scn_path, None, async_load)
        _load_finish_cb()
        return

    def is_loaded(self):
        return self._loaded

    def on_enter(self):
        self._loaded = True
        
        # OFFLINE MODE: Skip UI rendering and directly proceed
        if OFFLINE_MODE:
            print('[OFFLINE MODE] Skipping UI part rendering and entering game loop')
            # Don't call part.enter() for any UI parts since we skipped loading them
            # Just mark as loaded and ready
            return
        
        for com in six.itervalues(self.parts):
            com.enter()

        self.logic(0.1)
        self.post_logic(0.1)
        global_data.uisystem.RecordUsedSpritePaths()
        import cc
        cc.Director.getInstance().purgeCachedData()

    def on_exit(self):
        from cocosui import ccs
        ccs.ActionManagerEx.getInstance().releaseActions()
        for com in six.itervalues(self.parts):
            com.exit()

        for com in six.itervalues(self.parts):
            com.after_exit()

        if self.parts:
            del com
        self.parts = {}
        self.update_part_list = set()
        self._loaded = False

    def get_com(self, name):
        return self.parts.get(name)

    def get_sub_sys(self, com_name, sys_name):
        com = self.get_com(com_name)
        if not com:
            return None
        else:
            return com._sub_sys.get(sys_name, None)

    def post_logic(self, dt):
        if not self._loaded:
            return

    def fix_logic(self, dt=1 / 30.0):
        pass

    def logic(self, dt=1 / 30.0):
        self.tick_cnt += 1
        if not self._loaded:
            return
        self.update_parts(dt)

    def update_parts(self, dt):
        del_list = []
        update_list = self.update_part_list
        for part in update_list:
            ret = part.on_update(dt)
            if ret == part.REMOVE_UPDATE_AFTER_LOOP:
                del_list.append(part)

        if del_list:
            del_list.reverse()
            for part in del_list:
                update_list.remove(part)

    def load_parts(self):
        import logic.vscene.parts.factory as factory
        config_coms = self.scene_conf.get('coms', [])
        
        # OFFLINE MODE: Skip loading login UI parts
        if OFFLINE_MODE:
            print('[OFFLINE MODE] Skipping login UI parts (PartLogin3D, buttons, dialogs)')
            return
        
        for com_type in config_coms:
            factory.load_com(self, com_type)

    def enable_distortion(self, enable):
        global_data.display_agent.set_longtime_post_process_active('distortion', enable)

    def enable_hdr(self, enable):
        import device_limit
        import device_compatibility
        import render
        import game3d
        if device_limit.is_running_gles2() or not device_compatibility.can_use_hdr():
            pass
        elif enable:
            _HASH_ToneFactor = game3d.calc_string_hash('ToneFactor')
            _HASH_BloomThreshold = game3d.calc_string_hash('BloomThreshold')
            _HASH_BloomWidth = game3d.calc_string_hash('BloomWidth')
            _HASH_BloomLayer = game3d.calc_string_hash('bloomlayer')
            _HASH_BloomCoeff = game3d.calc_string_hash('BloomCoeff')
            _HASH_BloomCoeff2 = game3d.calc_string_hash('BloomCoeff2')
            _HASH_intensity_x = game3d.calc_string_hash('intensity_x')
            _HASH_intensity_y = game3d.calc_string_hash('intensity_y')
            conf = {'BloomWidth': 4.0,
               'bloomlayer': 0.5,
               'BloomIntensity': 1.0,
               'BloomThreshold': 0.8,
               'BloomCoeff': 4.0,
               'BloomCoeff2': 0.5
               }
            self.set_tone_factor(0.25)
            hdr_params = {}
            mtl0 = {_HASH_BloomThreshold: (
                                    'var', 'BloomThreshold', conf['BloomThreshold'])
               }
            hdr_params[0] = mtl0
            for i in range(1, 5):
                mat_i = {}
                hdr_params[i] = mat_i
                mat_i[_HASH_BloomWidth] = (
                 'var', 'BloomWidth', conf['BloomWidth'])
                mat_i[_HASH_BloomCoeff] = ('var', 'BloomCoeff', conf.get('BloomCoeff', 1.0))
                mat_i[_HASH_BloomCoeff2] = ('var', 'BloomCoeff2', conf.get('BloomCoeff2', 1.0))

            mtl_merge = {_HASH_BloomLayer: (
                                'var', 'bloomlayer', conf['bloomlayer'])
               }
            hdr_params[5] = mtl_merge
            global_data.display_agent.set_longtime_post_process_active('hdr_tonemap', False)
            global_data.display_agent.set_longtime_post_process_active('hdr', True, hdr_params)

    def set_preload_dynamic_args(self, extend_dist, always_y_min):
        pass

    def set_preload_dynamic_level(self, level):
        pass

    def refresh_graphics_style(self):
        pass