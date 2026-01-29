# OFFLINE MODE: Modified PartLogin with offline authentication
# This intercepts login requests and authenticates against local account data

from __future__ import absolute_import
from __future__ import print_function

OFFLINE_MODE = True

def patch_partlogin_for_offline():
    """Patch PartLogin class to use offline authentication"""
    try:
        from logic.vscene.parts import PartLogin as original_module
        
        # Get the original class
        OriginalPartLogin = original_module.PartLogin
        
        # Store original methods
        original_login_channel = OriginalPartLogin.login_channel
        original_on_sdk_logined_cb = OriginalPartLogin.on_sdk_logined_cb
        
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
            # This can be controlled by a flag
            import six.moves.builtins as builtins
            if builtins.__dict__.get('OFFLINE_AUTO_LOGIN', False):
                self.attempt_offline_login('test', 'test')
        
        def attempt_offline_login(self, account, password):
            """Attempt login with offline credentials"""
            print('[OFFLINE] Attempting offline login: %s' % account)
            
            from logic.vscene import login_scene
            helper = login_scene.get_offline_login_helper()
            
            if helper.verify_login(account, password):
                print('[OFFLINE] Login successful for: %s' % account)
                # Skip to main game after successful login
                self.on_offline_login_success()
            else:
                print('[OFFLINE] Login failed for: %s' % account)
                # Could show error message here
        
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


# Apply patch when module loads
if OFFLINE_MODE:
    patch_partlogin_for_offline()
