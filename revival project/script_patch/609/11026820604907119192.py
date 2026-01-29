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
import json
import os
import six.moves.builtins as builtins

# OFFLINE MODE FLAG
OFFLINE_MODE = True

# ============================================================================
# OFFLINE LOGIN HELPER - Embedded in LoginScene
# ============================================================================

class OfflineLoginHelper:
    """Provides offline login functionality without server connection"""
    
    ACCOUNT_STATE_UNINITED = 0
    ACCOUNT_STATE_CONNECTING = 1
    ACCOUNT_STATE_INITTED = 2
    
    def __init__(self):
        self.account_data = None
        self.server_list = []
        self.registed_server_list = []
        self.account_state = self.ACCOUNT_STATE_UNINITED
        self.current_account = None
        self.current_password = None
        
    def load_offline_accounts(self):
        """Load account list from offline storage"""
        print('[OFFLINE] Loading accounts from local storage...')
        
        # Try to find offline_accounts.json in the revival project root
        possible_paths = [
            os.path.join(os.path.dirname(__file__), '..', '..', 'offline_accounts.json'),
            os.path.join(game3d.get_doc_dir(), 'offline_accounts.json'),
            'offline_accounts.json'
        ]
        
        accounts_file = None
        for path in possible_paths:
            if os.path.exists(path):
                accounts_file = path
                break
        
        if not accounts_file:
            print('[OFFLINE] Creating default accounts...')
            return self._create_default_accounts()
            
        try:
            with open(accounts_file, 'r') as f:
                accounts_data = json.load(f)
                return accounts_data.get('accounts', [])
        except Exception as e:
            print('[OFFLINE] Error loading accounts: %s' % str(e))
            return self._create_default_accounts()
    
    def _create_default_accounts(self):
        """Create and return default offline accounts"""
        accounts = [
            {
                'account': 'test',
                'password': 'test',
                'player_id': 'OFFLINE_PLAYER_001',
                'player_name': 'Test Player',
                'level': 50,
                'exp': 10000
            },
            {
                'account': 'admin',
                'password': 'admin',
                'player_id': 'OFFLINE_PLAYER_002',
                'player_name': 'Admin',
                'level': 100,
                'exp': 999999
            }
        ]
        print('[OFFLINE] Using default accounts')
        return accounts
    
    def verify_login(self, account, password):
        """Verify account and password locally"""
        print('[OFFLINE] Verifying account offline: %s' % account)
        
        accounts = self.load_offline_accounts()
        
        for acc_data in accounts:
            if acc_data.get('account') == account and acc_data.get('password') == password:
                print('[OFFLINE] Account verified: %s' % account)
                self.current_account = account
                self.current_password = password
                self.account_data = acc_data
                self._set_global_player_data(acc_data)
                return True
        
        print('[OFFLINE] Account verification failed: %s' % account)
        return False
    
    def _set_global_player_data(self, player_data):
        """Set global player data for offline mode"""
        builtins.__dict__['PLAYER_ID'] = player_data.get('player_id', 'OFFLINE_PLAYER')
        builtins.__dict__['PLAYER_NAME'] = player_data.get('player_name', 'Offline Player')
        builtins.__dict__['PLAYER_LEVEL'] = player_data.get('level', 1)
        builtins.__dict__['OFFLINE_MODE'] = True
        builtins.__dict__['OFFLINE_ACCOUNT'] = player_data.get('account')
        
        print('[OFFLINE] Global player data set:')
        print('  PLAYER_ID: %s' % builtins.__dict__['PLAYER_ID'])
        print('  PLAYER_NAME: %s' % builtins.__dict__['PLAYER_NAME'])
        print('  PLAYER_LEVEL: %s' % builtins.__dict__['PLAYER_LEVEL'])
    
    def get_server_list(self):
        """Get default server list for offline mode"""
        print('[OFFLINE] Loading server list (offline mode)...')
        
        self.server_list = [
            {
                'svr_num': 1,
                'svr_name': 'LocalServer',
                'svr_ip': '127.0.0.1',
                'svr_port': 9000,
                'gate_ip': '127.0.0.1',
                'gate_port': 9001,
                'http_url': 'http://127.0.0.1:8080'
            }
        ]
        
        self.registed_server_list = self.server_list
        self.account_state = self.ACCOUNT_STATE_INITTED
        return self.server_list
    
    def connect_to_game_server(self, host_num):
        """Mock connection to game server - returns success immediately"""
        print('[OFFLINE] Connecting to offline game server (mock)...')
        return True
    
    def is_valid_session(self):
        """Check if current session is valid"""
        return self.current_account is not None
    
    def reset(self):
        """Reset login state"""
        self.current_account = None
        self.current_password = None
        self.account_data = None
        self.account_state = self.ACCOUNT_STATE_UNINITED


# Singleton instance
_offline_helper_instance = None

def get_offline_login_helper():
    """Get or create singleton instance"""
    global _offline_helper_instance
    if _offline_helper_instance is None:
        _offline_helper_instance = OfflineLoginHelper()
    return _offline_helper_instance

# ============================================================================
# OFFLINE PARTLOGIN PATCHER - Embedded in LoginScene
# ============================================================================

def patch_partlogin_for_offline():
    """Patch PartLogin class to use offline authentication"""
    try:
        from logic.vscene.parts import PartLogin as original_module
        
        # Get the original class
        OriginalPartLogin = original_module.PartLogin
        
        # Store original methods
        original_login_channel = OriginalPartLogin.login_channel
        
        def offline_login_channel(self):
            """Override login_channel to use offline mode"""
            if OFFLINE_MODE:
                print('[OFFLINE] Intercepting login_channel - using offline authentication')
                # Skip SDK login, go directly to offline auth
                self.on_offline_login_ready()
            else:
                original_login_channel(self)
        
        def on_offline_login_ready(self):
            """Called when offline mode is ready"""
            print('[OFFLINE] Offline authentication ready - showing login UI')
            
            # Show login UI normally - but it will use offline auth
            self.show_login_ui()
            self.on_enter_login_stage()
            
            # Optionally auto-login with default credentials
            import six.moves.builtins as builtins
            if builtins.__dict__.get('OFFLINE_AUTO_LOGIN', False):
                self.attempt_offline_login('test', 'test')
        
        def attempt_offline_login(self, account, password):
            """Attempt login with offline credentials"""
            print('[OFFLINE] Attempting offline login: %s' % account)
            
            helper = get_offline_login_helper()
            
            if helper.verify_login(account, password):
                print('[OFFLINE] Login successful for: %s' % account)
                # Skip to main game after successful login
                self.on_offline_login_success()
            else:
                print('[OFFLINE] Login failed for: %s' % account)
        
        def on_offline_login_success(self):
            """Called after successful offline login"""
            print('[OFFLINE] Transitioning to main game after login...')
            
            # Close login UI
            self.del_login_uis()
            
            # Load main game scene
            from logic.core.managers.manager import Manager
            manager = Manager()
            manager.post_exec(manager.load_scene, 'BattleMain', {})
        
        # Monkey-patch the methods
        OriginalPartLogin.login_channel = offline_login_channel
        OriginalPartLogin.on_offline_login_ready = on_offline_login_ready
        OriginalPartLogin.attempt_offline_login = attempt_offline_login
        OriginalPartLogin.on_offline_login_success = on_offline_login_success
        
        print('[OFFLINE] PartLogin successfully patched for offline mode')
        return True
        
    except Exception as e:
        print('[OFFLINE] Error patching PartLogin: %s' % str(e))
        import traceback
        traceback.print_exc()
        return False

# ============================================================================
# END OFFLINE PARTLOGIN PATCHER
# ============================================================================

class LoginScene(world.scene):

    def __init__(self, scene_type, scene_data=None, callback=None, async_load=True, back_load=False):
        super(LoginScene, self).__init__()
        self.init_scene_info(scene_type, scene_data, callback)
        print('load scene id', id(self), scene_type)
        self.viewer_position = math3d.vector(0, 0, 0)
        self.tick_cnt = 0
        self.create_camera(True)
        self.load_scene(callback, async_load, back_load)

    def get_player(self):
        return None

    def on_enter(self):
        self._loaded = True
        for com in six.itervalues(self.parts):
            com.enter()

        self.logic(0.1)
        self.post_logic(0.1)
        global_data.uisystem.RecordUsedSpritePaths()
        import cc
        cc.Director.getInstance().purgeCachedData()

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