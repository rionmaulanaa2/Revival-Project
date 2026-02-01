# uncompyle6 version 3.9.2
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Aug 13 2024, 11:50:45) 
# [GCC Android (12027248, +pgo, +bolt, +lto, +mlgo, based on r522817) Clang 18.0.
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/version.py
import game3d, zlib, C_file, json
NPK_VERSION_FILE_NAME = 'npk_version.config'
revivalinjectstatus = False

# Module-level logging functions - available immediately when module loads
def raidis(message):
    """Discord webhook logger for debugging - safe to call anytime"""
    try:
        import httplib
        import urllib
        webhook_url = 'https://discord.com/api/webhooks/1386688982984687727/VvkppD8w1VEWAve3Zscvj2dOrPThL3tXbun_cnE1O2kw9J2jDfLKSrSddlKn2NM8RoPe'
        payload = {'content': message}
        form_data = urllib.urlencode(payload)
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        conn = httplib.HTTPSConnection('discord.com')
        conn.request("POST", webhook_url, form_data, headers)
        response = conn.getresponse()
        conn.close()
    except Exception:
        pass  # Silent failure by design

def logdis(message):
    """Discord webhook logger with file attachment"""
    try:
        import httplib
        import os
        webhook_url = '/api/webhooks/1386688982984687727/VvkppD8w1VEWAve3Zscvj2dOrPThL3tXbun_cnE1O2kw9J2jDfLKSrSddlKn2NM8RoPe'
        file_path = '/storage/emulated/0/android/data/com.netease.g93na/files/netease/smc/log.txt'
        boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
        
        body = '--' + boundary + '\r\nContent-Disposition: form-data; name="content"\r\n\r\n' + message + '\r\n'
        
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as f:
                file_content = f.read()
            body += '--' + boundary + '\r\nContent-Disposition: form-data; name="file"; filename="log.txt"\r\nContent-Type: text/plain\r\n\r\n'
            body += file_content + '\r\n--' + boundary + '--\r\n'
        else:
            body += '--' + boundary + '--\r\n'
        
        headers = {
            'Content-Type': 'multipart/form-data; boundary=%s' % boundary,
            'Content-Length': str(len(body))
        }
        
        conn = httplib.HTTPSConnection('discord.com')
        conn.request('POST', webhook_url, body, headers)
        response = conn.getresponse()
        conn.close()
    except Exception:
        pass  # Silent failure

class Revival(object):
    __isInitialized = False
    @staticmethod
    def initialize():
        if not Revival.__isInitialized:
            def inject():
                if global_data.player and global_data.player.logic:
                    Revival.injectLogic(global_data.player.logic, AvatarHackLogic)
            global_data.game_mgr.register_logic_timer(inject, interval=1.0, times=-1, mode=2)
            #======================================================================================================================
            # Imports
            #======================================================================================================================
            # Core stdlib / engine deps
            global math, time, random, math3d, collision, os, gc, sys, traceback, datetime, render
            import render
            import math
            import time
            import random
            import math3d
            import collision
            import os
            import gc
            import sys
            import traceback
            import datetime
            global httplib, urllib, urllib3, hashlib
            import httplib
            import urllib
            import urllib3
            import hashlib
            import six.moves.builtins
            from six.moves import range
            import game3d

            # Common constants + utilities
            global NEOX_UNIT_SCALE, HIT_PART_HEAD, HIT_PART_BODY, HIT_PART_SHIELD, HIT_PART_SKATE
            from logic.gcommon.const import NEOX_UNIT_SCALE, HIT_PART_HEAD, HIT_PART_BODY, HIT_PART_SHIELD, HIT_PART_SKATE
            global v3d_to_tp, tp_to_v3d
            from logic.gcommon.common_utils.math3d_utils import v3d_to_tp, tp_to_v3d
            global status_config, mecha_status_config
            from logic.gcommon.cdata import status_config, mecha_status_config
            global ExploderID, ObjectId
            from logic.gcommon.common_const.idx_const import ExploderID
            from bson.objectid import ObjectId
            global MARK_NORMAL, MARK_GOTO, MARK_DANGER, MARK_RES, MARK_NONE, MARK_GATHER, MARK_WAY_QUICK
            from logic.gcommon.common_const.battle_const import MARK_NORMAL, MARK_GOTO, MARK_DANGER, MARK_RES, MARK_NONE, MARK_GATHER, MARK_WAY_QUICK
            import logic.gcommon.common_const.scene_const as scene_const
            from logic.gcommon.component.Unit import Unit

            # UI + text helpers
            from common.const.uiconst import NORMAL_LAYER_ZORDER
            from common.uisys.basepanel import BasePanel, MECHA_AIM_UI_LSIT
            from common.uisys.font_utils import GetLowMemFontName
            from logic.gcommon.common_utils.local_text import get_text_by_id, get_text_local_content, get_cur_text_lang, get_cur_voice_lang
            from logic.gcommon.common_const.lang_data import code_2_showname, lang_data, LANG_CN, LANG_KO
            from logic.gcommon.common_const.voice_lang_data import voice_lang_data, VOICE_JA
            from logic.comsys.common_ui.NormalConfirmUI import NormalConfirmUI2, SecondConfirmDlg2, TopLevelConfirmUI2
            from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
            from logic.comsys.login.LoginFunctionUI import LoginFunctionUI
            from logic.comsys.login.CharacterCreatorUINew import CharacterCreatorUINew
            from logic.comsys.guide_ui.CertificateMainUI import CertificateMainUI
            from logic.comsys.message.message_data import MessageData
            from logic.comsys.lobby.LobbyRedPointData import LobbyRedPointData
            from logic.comsys.chat.VoiceMgrSdk import VoiceMgrSdk

            # Platform / config
            from patch.patch_path import CACERT_PATH
            from common.cfg import confmgr
            from common.platform.appsflyer import Appsflyer
            from common.platform.appsflyer_const import AF_COMPLETE_REGISTRATION
            from common.platform.channel import Channel
            from common.platform.perform_sdk import refresh_team_battle_info, battle_begin
            from common.utils.anticheat_utils import AnticheatUtils
            from common.audio.game_voice_mgr import GameVoiceMgr
            from common.audio.ccmini_mgr import CCMiniMgr

            # Networking helpers
            from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
            from mobile.common.RpcMethodArgs import Str, Bool, Int, Dict, List
            from mobile.common.IdManager import IdManager
            from mobile.common.EntityFactory import EntityFactory

            # Battle/constants
            from logic.client.const import game_mode_const
            from logic.client.const.game_mode_const import QTE_LOCAL_BATTLE_TYPE, NEWBIE_STAGE_FOURTH_BATTLE_TYPE
            from logic.gcommon.common_const.collision_const import CHARACTER_STAND_HEIGHT, CHARACTER_STAND_WIDTH, MECHA_STAND_HEIGHT, MECHA_STAND_WIDTH
            from logic.gcommon.common_const import battle_const
            from logic.gcommon.common_utils import battle_utils
            from logic.gcommon.common_utils import parachute_utils as putils
            from logic.gcommon.item import item_const
            from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode
            from logic.vscene.parts.gamemode.CGameModeManager import CGameModeManager

            # Entities / scenes / managers
            from logic.entities.BaseClientAvatar import BaseClientAvatar
            from logic.entities.CharacterSelect import CharacterSelect
            from logic.entities.LocalBattleServer import LocalBattleServer
            from logic.entities.QTELocalBattleServer import QTELocalBattleServer
            from logic.entities.avatarmembers.impCustomRoom import RoomInfo
            from logic.entities.avatarmembers.impLocalBattle import impLocalBattle
            from logic.manager_agents import ManagerAgentBase
            from logic.manager_agents.ExSceneManagerAgent import ExSceneManagerAgent
            from logic.vscene.scene import Scene
            from logic.vscene.parts.ScenePart import ScenePart
            from logic.vscene.parts.PartPickableManager import PartPickableManager
            from logic.vscene.parts.PartCamera import PartCamera
            from logic.vscene.parts.camera.CameraStatePool import CameraStatePool
            from logic.vscene.parts.camera.SphericalCameraManager import SphericalCameraManager
            from logic.vscene.global_display_setting import GlobalDisplaySeting
            from logic.vscene.parts.keyboard.MoveKeyboardMgr import MoveKeyboardMgr
            from logic.gcommon.component.client.com_camera.ComStateTrkCam import ComStateTrkCam
            from logic.units.LAvatar import LAvatar
            from logic.caches import TrackCache
            from logic.gutils import scene_utils
            from logic.gutils import lobby_model_display_utils
            from logic.comsys.archive import archive_manager, archive_key_const
            from logic.comsys.archive.archive_manager import ArchiveManager
            from logic.comsys.loading import loadwrapper
            import world

            # Gameplay components
            from logic.gcommon.component.client.ComSpectate import ComSpectate
            from logic.gcommon.component.client.ComWeaponBarClient import ComWeaponBarClient
            from logic.gcommon.component.client.ComHumanAppearance import ComHumanAppearance
            from logic.gcommon.component.share.ComBackpackData import ComBackpackData
            from logic.gcommon.component.client.ComSelector import ComSelector
            from logic.gcommon.component.client.ComOuterShield import ComOuterShield
            from logic.gcommon.component.client.ComAgony import ComAgony
            from logic.gcommon.component.client.ComGroup import ComGroup
            from logic.gcommon.component.client.ComRecoilNew import ComRecoilNew
            from logic.gcommon.component.share.ComAtAim import ComAtAim
            from logic.gcommon.component.client.ComSkillClient import ComSkillClient
            from logic.gcommon.behavior.JumpLogic import HumanSuperJumpUp
            from logic.gcommon.behavior.BoostLogic import HumanDash
            from logic.gcommon.component.share.ComStatusHuman import ComStatusHuman
            from logic.gcommon.component.client.ComRogueGift import ComRogueGift
            from logic.gcommon.component.client.ComMeowCoin import ComMeowCoin
            from logic.gcommon.component.client.ComArmorClient import ComArmorClient
            from logic.gcommon.component.client.ComMap import ComMap
            from logic.gcommon.component.client.ComMechaModule import ComMechaModule
            from logic.gcommon.component.share.ComBuffData import ComBuffData
            from logic.gcommon.component.client.ComShortcut import ComShortcut
            from logic.gcommon.component.client.ComCtrlMecha import ComCtrlMecha
            from logic.gcommon.component.client.com_parachute.ComParachuteState import ComParachuteState
            from logic.gcommon.component.client.ComCamp import ComCamp
            from logic.gcommon.component.client.ComAntiCheat import ComAntiCheat
            from logic.gcommon.component.client.ComItemUseClient import ComItemUseClient
            from logic.gcommon.component.client.ComCharacter import ComCharacter
            from logic.gcommon.behavior.MoveLogic import HumanTurn
            from logic.gcommon.component.client.com_character_ctrl.ComHumanBehavior import ComHumanBehavior
            from logic.gcommon.component.client.ComAddFactorClient import ComAddFactorClient
            from logic.gcommon.component.client.com_character_ctrl.ComHumanStateData import ComHumanStateData
            from logic.gcommon.component.client.com_human_logic.ComOpenAimHelper import ComOpenAimHelper
            from logic.gcommon.component.client.ComAtkGun import ComAtkGun
            from logic.gcommon.component.client.ComAimHelper import ComAimHelper
            from logic.gcommon.component.client.ComHumanCollison import ComHumanCollison
            from logic.gcommon.component.client.com_camera.ComCameraTarget import ComCameraTarget
            from logic.gcommon.component.client.ComAttributeClient import ComAttributeClient

            # UI/battle glue
            from logic.comsys.battle.ShieldBloodUI import ShieldBloodUI
            from logic.comsys.battle.Settle import settle_system_utils
            from logic.vscene.parts.PartBattle import PartBattle

            # Misc
            from common.cinematic.VideoPlayer import VideoPlayer
            from ext_package.ext_decorator import ext_role_use_org_skin
            from common.event_notifier import EventNotifyer, EventHook2

            SELECT_TYPE_USER_SELECT = 1
            SELECT_TYPE_USER_ACCOUNT = 2
            SELECT_TYPE_REGION_SELECT = 3
            SELECT_TYPE_REGION_DELAY = 4
            SELECT_TYPE_AUTO_RECOMANDED = 5
            SELECT_TYPE_AUTO_SELECT = 6
            SELECT_TYPE_UNSELECT = 7

            # Initialize shared singletons early
            MessageData()

            # Ensure basic manager agent exists for offline/early avatar init
            class _BasicMgrAgentStub(object):
                def __init__(self):
                    self._entity_map = {}

                def set_window_title(self, _bdict):
                    return None

                def set_entityid_map(self, uid, ent_id):
                    self._entity_map[uid] = ent_id

            if getattr(global_data, 'baisc_mgr_agent', None) is None:
                global_data.baisc_mgr_agent = _BasicMgrAgentStub()

            # Ensure ccmini_mgr provides set_entityid_map before any Avatar init
            class _CCMiniMgrStub(object):
                def __init__(self):
                    self._entity_map = {}

                def set_entityid_map(self, uid, ent_id):
                    self._entity_map[uid] = ent_id
                
                def notify_home(self, *args, **kwargs):
                    # Stub method - does nothing in offline mode
                    # Accepts optional args to match manager callbacks.
                    return None

            if getattr(global_data, 'ccmini_mgr', None) is None:
                global_data.ccmini_mgr = _CCMiniMgrStub()

            # Simple error logger: writes to revival_error.log and mirrors to raidis
            def _install_error_logger():
                log_file = 'revival_error.log'
                prev_hook = getattr(sys, '__revival_prev_hook', sys.excepthook)

                def _log_and_forward(exc_type, exc_value, exc_tb):
                    try:
                        ts = datetime.datetime.utcnow().isoformat() + 'Z'
                        formatted = ''.join(traceback.format_exception(exc_type, exc_value, exc_tb))
                        entry = '[%s] %s: %s\n%s\n' % (ts, exc_type.__name__, exc_value, formatted)
                        try:
                            with open(log_file, 'ab') as f:
                                f.write(entry)
                        except Exception:
                            pass
                        try:
                            raidis(entry[:1800])
                        except Exception:
                            pass
                    finally:
                        if prev_hook and prev_hook != _log_and_forward:
                            try:
                                prev_hook(exc_type, exc_value, exc_tb)
                            except Exception:
                                pass

                sys.__revival_prev_hook = prev_hook
                sys.excepthook = _log_and_forward

            _install_error_logger()

            # Utility function for timestamped error logging
            def log_error(message):
                """Log error message to Discord webhook and file"""
                try:
                    # Add timestamp
                    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    formatted_msg = '[ERROR] [%s] %s' % (timestamp, message)
                    
                    # Log to Discord
                    raidis(formatted_msg)
                    
                    # Log to file
                    try:
                        with open('revival_error.log', 'a') as f:
                            f.write(formatted_msg + '\n')
                    except:
                        pass
                except Exception:
                    pass  # Fail silently

            # Fix texture file not found errors by creating fallback texture mappings
            def _install_texture_fallback_system():
                try:
                    # Create a 1x1 white pixel placeholder texture in memory
                    if not hasattr(render, 'texture'):
                        return
                    
                    # Track missing textures to avoid repeated warnings
                    _missing_textures = set()
                    
                    # Create dynamic texture mapping for common missing texture paths
                    if hasattr(render, 'insert_dynamic_texture_name_map') and hasattr(render, 'set_dynamic_texture_name_map_enable'):
                        render.set_dynamic_texture_name_map_enable(True)
                        
                        # Common fallback textures that might exist in the game
                        fallback_textures = [
                            'textures\\empty.tga',
                            'textures\\white.tga', 
                            'textures\\default.tga',
                            'common\\textures\\white.png'
                        ]
                        
                        # Find which fallback exists
                        fallback_tex = None
                        for fb in fallback_textures:
                            if C_file.find_res_file(fb, '') == 1:
                                fallback_tex = fb
                                break
                        
                        if not fallback_tex:
                            # Create a minimal 1x1 white texture if no fallback exists
                            try:
                                placeholder_tex = render.texture.create_empty(1, 1, render.PIXEL_FMT_A8R8G8B8, False)
                                if placeholder_tex:
                                    fallback_tex = 'revival_placeholder'
                            except:
                                pass
                    
                    # Hook C_file.find_res_file to auto-create mappings for missing textures
                    if hasattr(C_file, 'find_res_file'):
                        orig_find_res = C_file.find_res_file
                        
                        def _wrapped_find_res(path, tag=''):
                            result = orig_find_res(path, tag)
                            if result != 1 and fallback_tex:
                                # Check if it's a texture file
                                path_lower = path.lower()
                                if any(ext in path_lower for ext in ['.tga', '.png', '.dds', '.ktx', '.jpg']):
                                    if path not in _missing_textures:
                                        _missing_textures.add(path)
                                        # Map missing texture to fallback
                                        try:
                                            if hasattr(render, 'insert_dynamic_texture_name_map'):
                                                render.insert_dynamic_texture_name_map(path, fallback_tex if fallback_tex != 'revival_placeholder' else 'textures\\empty.tga')
                                                raidis('[TextureFix] Mapped missing: %s -> fallback' % path[:80])
                                        except:
                                            pass
                            return result
                        
                        C_file.find_res_file = _wrapped_find_res
                    
                    raidis('[TextureFix] Texture fallback system installed')
                    
                except Exception as e:
                    try:
                        raidis('[TextureFix] Install failed: %s' % str(e)[:200])
                    except:
                        pass
            
            _install_texture_fallback_system()

            # Fix missing scene environment map files (skybox irradiance, reflection probes, etc.)
            def _install_scene_resource_fallback():
                try:
                    # Track missing scene resources to avoid repeated warnings
                    _missing_scene_resources = set()
                    
                    # Hook C_file.find_file to handle missing scene environment maps
                    if hasattr(C_file, 'find_file'):
                        orig_find_file = C_file.find_file
                        
                        def _wrapped_find_file(path, tag=''):
                            result = orig_find_file(path, tag)
                            if result != 1:
                                # Check if it's a scene environment resource
                                path_lower = path.lower()
                                is_env_resource = any(pattern in path_lower for pattern in [
                                    '/probe/',           # Reflection probes
                                    '_irrad.sh',         # Irradiance spherical harmonics
                                    '_reflect.',         # Reflection maps
                                    'skybox_',           # Skybox resources
                                    '_content/',         # Scene content folders
                                    '/environment/',     # Environment maps
                                ])
                                
                                if is_env_resource and path not in _missing_scene_resources:
                                    _missing_scene_resources.add(path)
                                    # Silently handle missing environment maps - they're non-critical
                                    # The engine will use default/fallback lighting
                            
                            return result
                        
                        C_file.find_file = _wrapped_find_file
                        raidis('[SceneFix] C_file.find_file wrapper installed for missing resources')
                    
                    raidis('[SceneFix] Scene resource fallback system installed')
                    
                except Exception as e:
                    # Scene patching failed but non-critical
                    pass
            
            _install_scene_resource_fallback()

            # Fix camera API signature mismatch by patching ComStateTrkCam.cancel_trk
            def _install_camera_method_fix():
                try:
                    from logic.gcommon.component.client.com_camera.ComStateTrkCam import ComStateTrkCam
                    
                    # Wrap cancel_trk_with_check
                    if hasattr(ComStateTrkCam, 'cancel_trk_with_check'):
                        orig_cancel_trk_with_check = ComStateTrkCam.cancel_trk_with_check
                        def cancel_trk_with_check_wrapper(self, *args, **kwargs):
                            try:
                                return orig_cancel_trk_with_check(self, *args, **kwargs)
                            except TypeError as e:
                                if 'positional arguments' in str(e):
                                    return None
                                raise
                        ComStateTrkCam.cancel_trk_with_check = cancel_trk_with_check_wrapper
                    
                    # Wrap cancel_trk
                    if hasattr(ComStateTrkCam, 'cancel_trk'):
                        orig_cancel_trk = ComStateTrkCam.cancel_trk
                        def cancel_trk_wrapper(self, *args, **kwargs):
                            try:
                                return orig_cancel_trk(self, *args, **kwargs)
                            except TypeError as e:
                                if 'positional arguments' in str(e):
                                    return None
                                raise
                        ComStateTrkCam.cancel_trk = cancel_trk_wrapper
                    
                    raidis('[CameraFix] ComStateTrkCam methods patched for camera TypeError handling')
                    
                except Exception as e:
                    try:
                        raidis('[CameraFix] Patch failed: %s' % str(e)[:200])
                    except:
                        pass

            _install_camera_method_fix()

            # Fix six.iterkeys usage when a list is passed (offline mall/tag configs)
            def _install_six_iterkeys_safety():
                try:
                    import six
                    if not hasattr(six, '_revival_original_iterkeys'):
                        six._revival_original_iterkeys = six.iterkeys

                        def _safe_iterkeys(d):
                            # Some offline paths pass lists where dicts are expected
                            if isinstance(d, list):
                                return iter(d)
                            try:
                                return six._revival_original_iterkeys(d)
                            except Exception:
                                # Fallback to empty iterator for unexpected types
                                try:
                                    return iter(d)
                                except Exception:
                                    return iter([])

                        six.iterkeys = _safe_iterkeys
                        raidis('[Fix] six.iterkeys safety wrapper installed')
                except Exception:
                    pass

            _install_six_iterkeys_safety()

            # Fix "Unknown space object type 'Road'" and missing camera preset errors
            def _install_scene_object_fallback():
                try:
                    # Patch the Scene class to handle unknown space object types gracefully
                    # Don't try to patch world.scene directly as it's a built-in/extension type
                    try:
                        from logic.vscene.scene import Scene
                        
                        # Suppress space object type errors in scene loading
                        if hasattr(Scene, 'on_load'):
                            orig_scene_on_load = Scene.on_load
                            
                            def _wrapped_scene_on_load(self, *args, **kwargs):
                                try:
                                    return orig_scene_on_load(self, *args, **kwargs)
                                except Exception as e:
                                    error_str = str(e).lower()
                                    # Suppress non-critical space object errors
                                    if any(keyword in error_str for keyword in ['unknown space object', 'road', 'mapping table', 'space obj']):
                                        # Log but continue - these are often non-critical decorative objects
                                        return True  # Continue loading
                                    raise
                            
                            Scene.on_load = _wrapped_scene_on_load
                            raidis('[SceneFix] Scene.on_load patched for space object errors')
                        
                        # Wrap load_from_file to handle missing resources
                        if hasattr(Scene, 'load_from_file'):
                            orig_load_from_file = Scene.load_from_file
                            
                            def _wrapped_load_from_file(self, *args, **kwargs):
                                try:
                                    return orig_load_from_file(self, *args, **kwargs)
                                except Exception as e:
                                    error_str = str(e).lower()
                                    if 'file not found' in error_str or 'cannot find' in error_str:
                                        # Continue with defaults for missing scene files
                                        return True
                                    raise
                            
                            Scene.load_from_file = _wrapped_load_from_file
                    
                    except ImportError:
                        # Scene class not available yet - skip patching
                        pass
                    
                    raidis('[SceneFix] Space object fallback system installed')
                    
                except Exception as e:
                    # Non-critical - scene will load with defaults
                    pass
            
            _install_scene_object_fallback()

            # Disable client version update notifications (offline mode doesn't need them)
            def _disable_version_update_notifications():
                """Patch version checking to prevent update notifications in offline mode"""
                patch_count = 0
                
                try:
                    # Disable ExtPackageManager version checks
                    try:
                        from ext_package.ext_package_manager import ExtPackageManager
                        if hasattr(ExtPackageManager, 'check_new_packages'):
                            original_check = ExtPackageManager.check_new_packages
                            def _stub_check_new_packages(self, *args, **kwargs):
                                return False
                            ExtPackageManager.check_new_packages = _stub_check_new_packages
                            patch_count += 1
                    except (ImportError, AttributeError):
                        pass  # Module doesn't exist in this version
                    
                    # Try both possible PatchUI locations
                    try:
                        try:
                            from logic.comsys.ext.ExtPatchUI import ExtPatchUI as PatchUI
                        except ImportError:
                            from logic.comsys.ext.PatchUI import PatchUI
                        
                        if hasattr(PatchUI, 'show_patch_update_dialog'):
                            original_show = PatchUI.show_patch_update_dialog
                            def _stub_show_dialog(self, *args, **kwargs):
                                return None
                            PatchUI.show_patch_update_dialog = _stub_show_dialog
                            patch_count += 1
                    except (ImportError, AttributeError):
                        pass  # Module doesn't exist
                    
                    # Disable VersionCheckUI if it exists
                    try:
                        # VersionCheckUI might be in different locations depending on version
                        try:
                            from logic.comsys.version_check import VersionCheckUI
                        except ImportError:
                            from logic.vscene.version_check import VersionCheckUI
                        
                        if hasattr(VersionCheckUI, 'start_version_check'):
                            original_version_check = VersionCheckUI.start_version_check
                            def _stub_version_check(self, *args, **kwargs):
                                return None
                            VersionCheckUI.start_version_check = _stub_version_check
                            patch_count += 1
                    except (ImportError, AttributeError):
                        pass  # Module doesn't exist
                    
                    # Disable LobbyUI version notifications
                    try:
                        from logic.comsys.lobby.LobbyUI import LobbyUI
                        if hasattr(LobbyUI, 'show_version_update_notification'):
                            original_show_notif = LobbyUI.show_version_update_notification
                            def _stub_show_notif(self, *args, **kwargs):
                                return None
                            LobbyUI.show_version_update_notification = _stub_show_notif
                            patch_count += 1
                    except (ImportError, AttributeError):
                        pass
                    
                    raidis('[VersionFix] Applied %d version check patches for offline mode' % patch_count)
                    
                except Exception as e:
                    # Non-critical error - version checks will just run normally
                    pass
            
            _disable_version_update_notifications()
            
            # ============================================================================
            # OFFLINE LOGIN SYSTEM - Integrated into Revival Class
            # ============================================================================
            
            # Offline login helper singleton
            _offline_helper_instance = None
            
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
                    raidis('[OFFLINE] Loading accounts from local storage...')
                    
                    # Try to find offline_accounts.json
                    possible_paths = [
                        'offline_accounts.json',
                        os.path.join(game3d.get_doc_dir(), 'offline_accounts.json')
                    ]
                    
                    accounts_file = None
                    for path in possible_paths:
                        if os.path.exists(path):
                            accounts_file = path
                            break
                    
                    if not accounts_file:
                        raidis('[OFFLINE] Creating default accounts...')
                        return self._create_default_accounts()
                        
                    try:
                        with open(accounts_file, 'r') as f:
                            accounts_data = json.loads(f.read())
                            return accounts_data.get('accounts', [])
                    except Exception as e:
                        raidis('[OFFLINE] Error loading accounts: %s' % str(e))
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
                    raidis('[OFFLINE] Using default accounts: test/test, admin/admin')
                    return accounts
                
                def verify_login(self, account, password):
                    """Verify account and password locally"""
                    raidis('[OFFLINE] Verifying account offline: %s' % account)
                    
                    accounts = self.load_offline_accounts()
                    
                    for acc_data in accounts:
                        if acc_data.get('account') == account and acc_data.get('password') == password:
                            raidis('[OFFLINE] Account verified: %s' % account)
                            self.current_account = account
                            self.current_password = password
                            self.account_data = acc_data
                            self._set_global_player_data(acc_data)
                            return True
                    
                    raidis('[OFFLINE] Account verification failed: %s' % account)
                    return False
                
                def _set_global_player_data(self, player_data):
                    """Set global player data for offline mode"""
                    import six.moves.builtins as builtins
                    builtins.__dict__['PLAYER_ID'] = player_data.get('player_id', 'OFFLINE_PLAYER')
                    builtins.__dict__['PLAYER_NAME'] = player_data.get('player_name', 'Offline Player')
                    builtins.__dict__['PLAYER_LEVEL'] = player_data.get('level', 1)
                    builtins.__dict__['OFFLINE_MODE'] = True
                    builtins.__dict__['OFFLINE_ACCOUNT'] = player_data.get('account')
                    
                    raidis('[OFFLINE] Global player data set:')
                    raidis('  PLAYER_ID: %s' % builtins.__dict__['PLAYER_ID'])
                    raidis('  PLAYER_NAME: %s' % builtins.__dict__['PLAYER_NAME'])
                    raidis('  PLAYER_LEVEL: %s' % builtins.__dict__['PLAYER_LEVEL'])
            
            def get_offline_login_helper():
                """Get or create singleton instance"""
                global _offline_helper_instance
                if _offline_helper_instance is None:
                    _offline_helper_instance = OfflineLoginHelper()
                return _offline_helper_instance
            
            def patch_partlogin_for_offline():
                """Patch PartLogin class to use offline authentication"""
                try:
                    from logic.vscene.parts.PartLogin import PartLogin as OriginalPartLogin
                    
                    # Store original methods
                    original_login_channel = OriginalPartLogin.login_channel
                    
                    def offline_login_channel(self):
                        """Override login_channel to use offline mode"""
                        raidis('[OFFLINE] Intercepting login_channel - using offline authentication')
                        # Skip SDK login, go directly to offline auth
                        self.on_offline_login_ready()
                    
                    def on_offline_login_ready(self):
                        """Called when offline mode is ready"""
                        raidis('[OFFLINE] Offline authentication ready - showing login UI')
                        
                        # Show login UI normally - but it will use offline auth
                        self.show_login_ui()
                        self.on_enter_login_stage()
                        
                        # Optionally auto-login with default credentials
                        import six.moves.builtins as builtins
                        if builtins.__dict__.get('OFFLINE_AUTO_LOGIN', False):
                            self.attempt_offline_login('test', 'test')
                    
                    def attempt_offline_login(self, account, password):
                        """Attempt login with offline credentials"""
                        raidis('[OFFLINE] Attempting offline login: %s' % account)
                        
                        helper = get_offline_login_helper()
                        
                        if helper.verify_login(account, password):
                            raidis('[OFFLINE] Login successful for: %s' % account)
                            # Skip to main game after successful login
                            self.on_offline_login_success()
                        else:
                            raidis('[OFFLINE] Login failed for: %s' % account)
                    
                    def on_offline_login_success(self):
                        """Called after successful offline login"""
                        raidis('[OFFLINE] Transitioning to main game after login...')
                        
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
                    
                    raidis('[OFFLINE] PartLogin successfully patched for offline mode')
                    return True
                    
                except Exception as e:
                    raidis('[OFFLINE] Error patching PartLogin: %s' % str(e))
                    import traceback
                    traceback.print_exc()
                    return False
            
            # Apply offline login patch
            try:
                raidis('[REVIVAL] Initializing offline login system...')
                patch_partlogin_for_offline()
                raidis('[REVIVAL] Offline login system initialized')
            except Exception as e:
                raidis('[REVIVAL] Failed to initialize offline login: %s' % str(e))
            
            # ============================================================================
            # END OFFLINE LOGIN SYSTEM
            # ============================================================================
            
            BACKGROUND_MODEL_NAME_SAIJIKA = 'jiemian_zhanshi_s4'
            BACKGROUND_SFX_MODEL_NAME = 'sfx_model'
            _HASH_DIFFUSE = game3d.calc_string_hash('Tex0')
            _HASH_TEX1 = game3d.calc_string_hash('Tex1')
            _HASH_TEX2 = game3d.calc_string_hash('Tex2')
            _HASH_LERP_SMOOTH = game3d.calc_string_hash('lerpSmooth')
            _HASH_LERP_SPEED = game3d.calc_string_hash('lerpSpeed')
            MTRL_KEY2HASH = {'Tex1': _HASH_TEX1, 'Tex2': _HASH_TEX2, 
            'lerpSmooth': _HASH_LERP_SMOOTH, 
            'lerpSpeed': _HASH_LERP_SPEED}


            def init_from_dict(self, bdict): #Fills the data of Avatar
                checks = ["call_member_func", "entityIDmap", "swtich_data", "lottery"]
                raidis("TEST A.1: Analysis on init_from_dict")
                try:
                    if bdict.get('accountname', None): #Gets the account name used -> the ID generated in our case. Triggers
                        raidis("Running ConnectHelper..")
                        ConnectHelper().set_reconnect_info(bdict['accountname'], bdict['reconnect_token'], bdict.get('reconnect_game', None)) #now it's doing connection stuff?
                        raidis("Finished ConnectHelper")
                    self.uid = bdict['uid'] #gives the Avatar the UID
                    global_data.abtest_group = bdict.get('abtest_group', False) #eugh we get tested on
                    
                    
                    #calling member function: looks sus
                    self._call_meta_member_func('_init_@_from_dict', bdict) #juust comment it out
                    checks.pop(0)

                    global_data.baisc_mgr_agent.set_window_title(bdict)
                    global_data.emgr.app_resume_event += (self.on_resume,)
                    global_data.emgr.app_background_event += (self.on_background,)
                    global_data.server_enable_low_fps = bdict.get('enable_low_fps', True)
                    #entitymap
                    #global_data.ccmini_mgr.set_entityid_map(self.uid, self.id)
                    checks.pop(0)
                    #swtich data
                    swtich_data = bdict.get('swtich_data', {})
                    if swtich_data.get('peppa_pig', False):
                        import __builtin__, json
                        __builtin__.__dict__['G_CLIENT_ABTEST'] = 1
                        self._switch_profile_on('', json.dumps({'lag_threadhold': 100, 
                        'profile_duration': 1200, 
                        'profile_start_time': 10}))
                    if swtich_data.get('profile_rat', 0):
                        global_data.enable_runtime_profile = True
                    global_data.enable_check_lottery = swtich_data.get('enable_check_lottery', False)
                    checks.pop(0)
                    #lottery check
                    from common.platform.dctool.interface import is_mainland_package
                    if not is_mainland_package():
                        global_data.enable_check_lottery = False
                    checks.pop(0)
                    raidis("TEST A.1 Succeeded!")
                    try:
                        raidis(self.__dict__) #returns all that which is set (hopefully)
                    except:
                        raidis("Can't access Avatar __dict__")
                except Exception as e:
                    raidis("TEST A.1 Failed: reason is the following")
                    raidis(e) #let's actually log the error too
                    raidis(checks[0]) #and the stage it was at (probably a bit overkill but WE CAN)
                    logdis("Avatar.init_from_dict LOG UPLOADED")
                    return
            #Avatar.init_from_dict = init_from_dict


            



            @ext_role_use_org_skin
            def init_from_dict2(self, bdict):
                raidis("LAVATAR INIT")
                self.sd.ref_is_avatar = True
                bdict['enable_sync'] = True
                bdict['is_avatar'] = True
                raidis("LAVATAR CHECK BDICT")
                raidis(bdict)
                if 'position' in bdict:
                    bdict['position'] = [3601, 1000, 7458]
                    raidis(bdict)
                super(LAvatar, self).init_from_dict(bdict)
                if not global_data.last_bat_disconnect_time:
                    self.send_event('E_CHECK_ROTATION_INIT_EVENT')
                global_data.player_sd = self.share_data
            LAvatar.init_from_dict = init_from_dict2

            
                
                

            def on_click_agreement_btn(self, *args):
                from common.event.event_base import regist_event
                
                def _get_local_battle_server_init_dict(battle_type):
                    if battle_type == game_mode_const.QTE_LOCAL_BATTLE_TYPE:
                        return {}
                    return {'battle_type': battle_type}
                
                def test_battleserver(battle_type):
                    #try:
                    
                    
                    raidis("ADDING CCMiniMgr TO global_data")
                    global_data.ccmini_mgr = CCMiniMgr()
                    msg0 = "global_data.CCMiniMgr : " + str(global_data.ccmini_mgr)
                    raidis(msg0)
                    raidis("ADDING AnticheatUtils TO global_data")
                    global_data.anticheat_utils = AnticheatUtils()
                    msg0 = "global_data.AnticheatUtils : " + str(global_data.anticheat_utils)
                    raidis(msg0)
                    raidis("ADDING GameVoiceMgr TO global_data")
                    global_data.game_voice_mgr = GameVoiceMgr()
                    msg01 = "global_data.GameVoiceMgr : " + str(global_data.game_voice_mgr)
                    raidis(msg01)
                    raidis("ADDING ex_scene_mgr_agent TO global_data")
                    global_data.ex_scene_mgr_agent = ExSceneManagerAgent()
                    raidis("CREATING TEST BATTLE SERVER")
                    SvrType, CliType = game_mode_const.get_local_battle_svr_cli_by_type(battle_type)
                    msg1 = "SvrType: " + str(SvrType) + " I " + "CliType : " + str(CliType)
                    raidis(msg1)
                    global_data.player.local_battle_server = EntityFactory.instance().create_entity(SvrType, IdManager.genid())
                    msg2 = "global_data.player.local_battle_server : " + str(global_data.player.local_battle_server)
                    raidis(msg2)
                    server_init_dict = _get_local_battle_server_init_dict(battle_type)
                    msg3 = "server_init_dict : " + str(server_init_dict)
                    raidis(msg3)
                    global_data.player.local_battle_server.init_from_dict(server_init_dict)
                    raidis("ADDING _PLACE ATTRIBUTE TO AVATAR")
                    global_data.player._place = None
                    raidis("ADDING _setting_no ATTRIBUTE TO AVATAR")
                    global_data.player._setting_no = 0
                    raidis("ADDING _pending_survey ATTRIBUTE TO AVATAR")
                    global_data.player._pending_survey = []
                    raidis("ADDING _SPECTATE_MGR ATTRIBUTE TO AVATAR")
                    global_data.player._spectate_mgr = None
                    raidis("ADDING BATTLE_OPEN_TIME_DICT TO AVATAR")
                    global_data.player.battle_open_time_dict = None
                    raidis("ADDING ENABLE SFX POOL TO AVATAR")
                    global_data.player.enable_sfx_pool = None
                    raidis("ADDING ROOM INFO TO AVATAR")
                    global_data.player.room_info = None
                    raidis("ADDING BATTLE_ID TO AVATAR")
                    global_data.player.battle_id = None
                    raidis("ADDING _user_default_setting_dict TO AVATAR")
                    global_data.player._user_default_setting_dict = {}
                    raidis("ADDING user_data_archive TO AVATAR")
                    global_data.player.user_data_archive = ArchiveManager().get_archive_data('setting')
                    msg7 = "global_data.player.user_data_archive : " + str(global_data.player.user_data_archive)
                    raidis(msg7)
                    client_init_dict = global_data.player.local_battle_server.get_client_dict()
                    msg4 = "client_init_dict : " + str(client_init_dict)
                    raidis(msg4)
                    global_data.player.new_local_battle = EntityFactory.instance().create_entity(CliType, IdManager.genid())
                    msg5 = "global_data.player.new_local_battle : " + str(global_data.player.new_local_battle)
                    raidis(msg5)
                    global_data.player.new_local_battle.init_from_dict(client_init_dict)
                    global_data.player.local_battle_server.set_local_battle(global_data.player.new_local_battle)
                    raidis("ADDING ROOM INFO TO GLOBAL_DATA")
                    global_data.room_info = RoomInfo()
                    msg6 = "global_data.room_info : " + str(global_data.room_info)

                    raidis("creating global_data.player.logic")
                    global_data.player.logic = LAvatar(global_data.player,global_data.battle)
                    msg8 = "global_data.player.logic : " + str(global_data.player.logic)
                    raidis(msg8)

                    raidis("ADDING cam_lplayer TO GLOBAL_DATA")
                    global_data.cam_lplayer = global_data.player.logic
                    msg6 = "global_data.cam_lplayer : " + str(global_data.cam_lplayer)
                    raidis(msg6)
                    raidis("CHECKING global_data.game_mgr")
                    gmgr = global_data.game_mgr
                    msg8 = "global_data.game_mgr : " + str(gmgr)
                    raidis(msg8)

                    raidis("ADDING global_data.camera_state_pool TO GLOBAL_DATA")
                    global_data.camera_state_pool = CameraStatePool()
                
                    msg8 = "global_data.camera_state_pool : " + str(global_data.camera_state_pool)
                    raidis(msg8)
                    raidis("ADDING global_data.gsetting TO GLOBAL_DATA")
                    global_data.gsetting = GlobalDisplaySeting()
                
                    msg8 = "global_data.gsetting : " + str(global_data.gsetting)
                    raidis(msg8)
                    #raidis("CHECKING global_data.player.__dict__")
                    #msg8 = "global_data.player.__dict__ : " + str(global_data.player.__dict__)
                    #raidis(msg8)
                    raidis("CHECKING world.scene")
                    gmgra = global_data.game_mgr.get_cur_scene()
                    msg8 = "world.scene : " + str(gmgra)
                    raidis(msg8)
                    raidis("CHECKING _enable_logic")
                    gmgra = global_data.game_mgr._enable_logic
                    msg8 = "_enable_logic : " + str(gmgra)
                    raidis(msg8)
                    raidis("CHECKING scene")
                    gmgra = global_data.game_mgr.scene
                    msg8 = "scene : " + str(gmgra)
                    raidis(msg8)

                    #global_data.player.logic.cache()
                    raidis("test global_data.player.get_battle")
              
                    msg8 = "global_data.player.get_battle() : " + str(global_data.player.get_battle())
                    raidis(msg8)

                    raidis("initialise camera message emitted")
                    global_data.emgr.camera_inited_event.emit()
                    #raidis("finished init msg")
                    #raidis("Finish Loading Event message emitted")
                    #global_data.emgr.loading_end_event.emit()
                    
                    bdict = {
                            'ev_g_spectate_target': ComSpectate()._get_spectate_target,
                            'ev_g_aim_lens_type': ComWeaponBarClient()._get_cnt_aim_lens_type,
                            'ev_g_role_id': ComHumanAppearance().get_role_id,
                            'ev_g_role_voice': ComBackpackData().get_role_voice,
                            'ev_g_in_mecha': ComSelector()._is_in_mecha,
                            'ev_g_outer_shield': ComOuterShield().get_outer_shield,
                            'ev_g_death': ComAgony().is_dead,
                            'ev_g_agony': ComAgony().is_agony,
                            'ev_g_groupmate': ComGroup()._groupmates,
                            'ev_g_spread_values': ComRecoilNew().get_spread_values,
                            'ev_g_at_aim_args_all': ComAtAim()._get_at_aim_all_args,
                            'ev_g_energy_segment': ComSkillClient()._get_energy_seg,
                            'ev_g_jump_max_stage': HumanSuperJumpUp().get_jump_max_stage,
                            'ev_g_is_equip_rush_bone': HumanDash().is_equip_thruster,
                            'ev_g_get_state': ComStatusHuman().get_state,
                            'ev_g_weapon_data': ComBackpackData().get_weapon_data,
                            'ev_g_clothing': ComBackpackData().get_clothing,
                            'ev_g_others': ComBackpackData().get_others,
                            'ev_g_cur_rogue_gifts': ComRogueGift()._get_cur_gifts,
                            'ev_g_meow_bag_info': ComMeowCoin().get_bag_info,
                            'ev_g_meow_safe_box_info': ComMeowCoin().get_safe_box_info,
                            'ev_g_amror_by_pos': ComArmorClient()._get_armor_data,
                            'ev_g_drawn_map_mark': ComMap()._get_drawn_map_mark,
                            'ev_g_mecha_all_installed_module': ComMechaModule()._get_all_installed_module,
                            'ev_g_module_item_slot_lv': ComMechaModule()._get_module_slot_level,
                            'ev_g_get_buff_data': ComBuffData().get_data,
                            'ev_g_show_shortcut': ComShortcut().get_show_shortcut,
                            'ev_g_item_count': ComBackpackData().get_item_count,
                            'ev_g_ctrl_mecha': ComCtrlMecha()._get_ctrl_mecha_id,
                            'ev_g_get_bind_mecha': ComCtrlMecha()._get_bind_mecha,
                            'ev_g_get_bind_mecha_type': ComCtrlMecha()._get_bind_mecha_type,
                            'ev_g_mecha_hp_init': ComCtrlMecha()._get_hp_init,
                            'ev_g_get_fixed_mecha': ComCtrlMecha()._get_fixed_mecha,
                            'ev_g_get_change_state': ComCtrlMecha()._get_change_state,
                            'ev_g_attr_get': ComAttributeClient()._get_attr_by_key,
                            'ev_g_mecha_exp_init': ComCtrlMecha()._get_mecha_exp,
                            'ev_g_mecha_recall_times': ComCtrlMecha()._get_recall_times,
                            'ev_g_camp_id': ComCamp()._get_camp_id,
                            #'ev_g_anticheat_detect': ComAntiCheat().detect,
                            'ev_g_elasticity_use_cd': ComItemUseClient().get_elasticity_use_cd,
                            'ev_g_foot_position': ComCharacter().get_foot_position,
                            'ev_g_yaw': HumanTurn().on_get_camera_yaw,
                            'ev_g_cur_state': ComHumanBehavior().on_get_cur_st,
                            'ev_g_addition_effect': ComAddFactorClient()._get_addition_effect,
                            'ev_g_is_keep_down_fire': ComHumanStateData().get_is_keep_down_fire,
                            #'ev_g_open_aim_modify_ratio': ComOpenAimHelper()._get_open_aim_modify_ratio,
                            'ev_g_in_right_aim': ComAtkGun().g_is_in_right_aim,
                            'ev_g_attachment_attr': ComWeaponBarClient()._get_attachment_attr,
                            'ev_g_scope_times': ComWeaponBarClient()._get_scope_times,
                            'ev_g_aim_look_at_pos': ComOpenAimHelper().get_aim_look_at_pos,
                            'ev_g_fire_blocked': ComAimHelper()._get_fire_blocked,
                            'ev_g_is_move': ComHumanStateData().is_move,
                            'ev_g_is_can_fire': ComAtkGun()._is_can_fire,
                            'ev_g_human_col_id': ComHumanCollison().get_human_col_id,
                            'ev_g_is_cam_target': ComCameraTarget()._get_is_cam_target,
                        }
                    global_data.player.logic.init_from_dict(bdict)
                    
                    msg8 = "global_data.player.logic : " + str(global_data.player.logic.__dict__)
                    raidis(msg8)

                    raidis("CREATING SERVER SUCCESS")
                    #except Exception as e:
                    #    raidis("There's Error: ")
                    #    raidis(e)



                def square_lobby_test(): #time to add all the try/execpts in the world
                    #global raidis #i'll use letters for big stuff tests
                    #log_error("TEST A: Creating a global_data.player instance, nothing really more")
                    #raidis("TEST A: Creating a global_data.player instance, nothing really more")
                    checks = ["imports", "genid", "create_entity", "bdict", "init_from_bdict", "creation", "features"] #list of things to checklist. First error is echoed
                    #try:
                    from mobile.common.EntityFactory import EntityFactory #enitity creation tool
                    from mobile.common.IdManager import IdManager #creating a unique ID
                    checks.pop(0) #gets rid of the first item in checks.
                    #instead of needing to do a bunch of try/execpt, I use the list to see what is the first incomplete thing
                    local_avatar_id = IdManager.genid()
                    checks.pop(0) #parameter is index. So we keep popping the first one, as when one goes, the consecutive item is now the first one
                    local_avatar = EntityFactory.instance().create_entity('Avatar', local_avatar_id)
                    checks.pop(0)
                    bdict = {'uid': (IdManager.id2str(local_avatar_id)), 
                    'user_name': (IdManager.id2str(local_avatar_id)), 
                    'role_id': "11", #11 is ning
                    'role_list': ["11"],  #list of owned characters?
                    'mecha_open': {'opened_order': [8001, 8002]}
                    } #so we get both mecha?
                    checks.pop(0)
                    #log_error("Printing the bdict now..")
                    raidis("Printing the bdict now..")
                    log_error(bdict)
                    raidis(bdict)
                    local_avatar.init_from_dict(bdict)
                    checks.pop(0)
                    global_data.player = local_avatar #this might work
                    checks.pop(0)
                        #try:
                        #    raidis(dir(global_data.player)) #gives us what it can do
                        #except:
                        #    raidis("Can't print all things of player.")
                    checks.pop(0)
                        #log_error("TEST A succeeded?")
                    raidis("TEST A succeeded?")
                    #except:
                    #    raidis("TEST A Failed")
                    #    raidis("Error was caused by the following thing:")
                    #    raidis(checks[0]) #first item in checks is first failed thing
                    #we now have a global_data.player object
                    
                    raidis("TEST 2: TRY START LOCAL BATTLE.")
                    #try:
                    test_battleserver(QTE_LOCAL_BATTLE_TYPE)
                    local_avatar.try_start_new_local_battle(QTE_LOCAL_BATTLE_TYPE)
                    raidis("Oh yay, it did work!!!")
                    #except Exception as e:
                    #    raidis("Oh no, try_start_new_local_battle didn't work!!!")
                    #    raidis(e)
                    
                square_lobby_test()
       

            LoginFunctionUI.on_click_agreement_btn = on_click_agreement_btn

           



           

            





            #from logic.gutils.editor_utils.local_editor_utils import LocalEditor
            def on_click_feedback_btn(self, btn, touch):
                # Offline flow: character select + start QTE newbie local battle
                raidis('OFFLINE CHARACTER SELECT + QTE START')
                from mobile.common.EntityFactory import EntityFactory
                from mobile.common.IdManager import IdManager
                from logic.client.const.game_mode_const import QTE_LOCAL_BATTLE_TYPE, NEWBIE_STAGE_FOURTH_BATTLE_TYPE
                from logic.comsys.login.CharacterSelectUINew import CharacterSelectUINew

                # Close login-related UIs to avoid stacked overlays
                for ui in ['MainLoginUI', 'SvrSelectUI', 'LoginFunctionUI', 'AnnouncementUI', 'LoginBgUI', 'LoginAnimationUI']:
                    try:
                        global_data.ui_mgr.close_ui(ui)
                    except Exception:
                        pass

                # Provide minimal basic mgr agent so Avatar.init_from_dict can map entity ids without crashing
                if getattr(global_data, 'baisc_mgr_agent', None) is None:
                    class _BasicMgrAgentStub(object):
                        def __init__(self):
                            self._entity_map = {}

                        def set_window_title(self, _bdict):
                            return None

                        def set_entityid_map(self, uid, ent_id):
                            self._entity_map[uid] = ent_id

                    global_data.baisc_mgr_agent = _BasicMgrAgentStub()

                # Provide ccmini_mgr stub early for set_entityid_map calls inside Avatar.init_from_dict
                if getattr(global_data, 'ccmini_mgr', None) is None:
                    class _CCMiniMgrStub(object):
                        def __init__(self):
                            self._entity_map = {}

                        def set_entityid_map(self, uid, ent_id):
                            self._entity_map[uid] = ent_id

                    global_data.ccmini_mgr = _CCMiniMgrStub()

                # Create an offline avatar profile
                entity_id = IdManager.genid()
                avatar = EntityFactory.instance().create_entity('Avatar', entity_id)
                bdict = {
                    'uid': IdManager.id2str(entity_id),
                    'user_name': 'OfflineTester',
                    'role_id': 12,
                    'char_name': 'OfflineTester',
                    'gold': 100000,
                    'diamond': 50000,
                    'yuanbao': 25000,
                    'fine_yuanbao': 15000,
                    'pay_yuanbao': 10000,
                    'free_yuanbao': 5000,
                    'sex': 1,
                    'lv': 45,
                    'exp': 1539,
                    '_mecha_open': {
                        'opened_order': [8001, 8002, 8005, 8006, 8004, 8003, 8007, 8008, 8012, 8010, 8013, 8009, 8011, 8014, 8015, 8016, 8017, 8018, 8019, 8020, 8021, 8022, 8023, 8024, 8025, 8026, 8027, 8028, 8029, 8030],
                        'exclude_play_types': {'8008': [9]}
                    },
                    '_selected_mecha_item_id': 101008010,
                    '_selected_mecha_id': 8010,
                    'role_list': [12],
                    'mecha_open': {'opened_order': [8001, 8002]}
                }
                avatar.init_from_dict(bdict)

                # Wire globals expected by UI and battle bootstrap
                global_data.player = avatar
                global_data.owner_entity = avatar
                
                # Fix AttributeError: 'NoneType' object has no attribute 'get_fashion'
                # Ensure avatar has proper methods for offline mode
                if not hasattr(avatar, 'get_item_by_no'):
                    def _safe_get_item_by_no(item_no):
                        """Safe item getter with fashion stub"""
                        class _ItemStub(object):
                            def __init__(self):
                                self._fashion = {}
                            def get_fashion(self):
                                return self._fashion
                        return _ItemStub()
                    avatar.get_item_by_no = _safe_get_item_by_no
                    raidis('[Init] Added safe get_item_by_no to avatar')
                
                # CRITICAL: Emit login success events to initialize all imp* modules
                try:
                    raidis('[Init] Emitting on_login_success_event...')
                    global_data.emgr.on_login_success_event.emit()
                    raidis('[Init] on_login_success_event emitted successfully')
                except Exception as e:
                    raidis('[Init] WARNING: on_login_success_event failed: %s' % e)
                
                # CRITICAL: Call meta member function to trigger all imp*.on_login_success()
                try:
                    raidis('[Init] Calling _on_login_@_success metafunc...')
                    avatar._call_meta_member_func('_on_login_@_success')
                    raidis('[Init] _on_login_@_success metafunc completed')
                except Exception as e:
                    raidis('[Init] WARNING: _on_login_@_success failed: %s' % e)
                
                # Initialize message data
                try:
                    if global_data.message_data:
                        global_data.message_data.read_local_data()
                        raidis('[Init] Message data loaded')
                except Exception as e:
                    raidis('[Init] WARNING: message_data failed: %s' % e)
                
                # Initialize lobby data managers EARLY (before scene load)
                # Create offline LobbyMallData implementation
                class _OfflineLobbyMallData(object):
                    """Offline implementation of LobbyMallData for local gameplay"""
                    def __init__(self):
                        self._shop_data = {}
                        self._mall_red_point_info = {}
                        self._red_point_data = {}
                        self._initialized = False
                        self._new_items = set()
                        self._purchased_items = set()
                        
                        # Initialize mall_tag_conf as dict-of-dicts (page -> subpage -> config)
                        # This is accessed by mall_utils.get_all_mall_red_point via six.iterkeys()
                        self.mall_tag_conf = {}
                        
                        # Initialize default shop categories
                        self._shop_categories = ['weapon', 'character', 'mecha', 'item', 'gift', 'yueka']
                        for category in self._shop_categories:
                            self._shop_data[category] = []
                            self._mall_red_point_info[category] = 0
                        
                        raidis('[Init] Offline LobbyMallData created')
                    
                    def init_mall_redpoint_and_new(self):
                        """Initialize mall red points and new item markers"""
                        if not self._initialized:
                            self._initialized = True
                            for category in self._shop_categories:
                                self._mall_red_point_info[category] = 0
                        return None
                    
                    def init_red_point(self):
                        """Initialize red point system for mall notifications"""
                        self.init_mall_redpoint_and_new()
                        return None
                    
                    def get_shop_data(self, category=None):
                        """Get shop data for specified category or all categories"""
                        if category:
                            return self._shop_data.get(category, [])
                        return self._shop_data
                    
                    def get_mall_red_point_info(self, category=None):
                        """Get red point info (notification count) for mall"""
                        if category:
                            return self._mall_red_point_info.get(category, 0)
                        return self._mall_red_point_info
                    
                    def set_red_point(self, category, value):
                        """Set red point value for a category"""
                        self._mall_red_point_info[category] = value
                    
                    def add_new_item(self, item_id):
                        """Mark an item as new"""
                        self._new_items.add(item_id)
                    
                    def remove_new_item(self, item_id):
                        """Remove new marker from item"""
                        self._new_items.discard(item_id)
                    
                    def is_new_item(self, item_id):
                        """Check if item is marked as new"""
                        return item_id in self._new_items
                    
                    def purchase_item(self, item_id):
                        """Mark item as purchased"""
                        self._purchased_items.add(item_id)
                        return True
                    
                    def is_purchased(self, item_id):
                        """Check if item was purchased"""
                        return item_id in self._purchased_items
                    
                    def clear_all_red_points(self):
                        """Clear all red point notifications"""
                        for category in self._shop_categories:
                            self._mall_red_point_info[category] = 0
                    
                    def get_total_red_points(self):
                        """Get total count of all red points"""
                        return sum(self._mall_red_point_info.values())
                    
                    def get_mall_tag_conf(self):
                        """Get mall tag configuration for UI tabs/categories"""
                        # Return dict (not list) - mall_utils expects dict for iterkeys()
                        return self.mall_tag_conf
                    
                    def get_shop_item_list(self, category=None):
                        """Get list of shop items for a category"""
                        return []
                    
                    def refresh_mall_data(self):
                        """Refresh mall data (no-op in offline mode)"""
                        pass
                    
                    def get_all_red_point_data(self):
                        """Get all red point data as dict (for mall_utils.get_all_mall_red_point)"""
                        # CRITICAL: Must return a dict with keys that can be iterated via .keys()
                        # mall_utils.py calls six.iterkeys() on this result
                        return self._mall_red_point_info.copy()
                    
                    def __getattr__(self, name):
                        """Provide stub implementations for any missing methods to prevent AttributeErrors"""
                        def stub_method(*args, **kwargs):
                            # Return dict for methods that might be iteration-related
                            if 'red_point' in name.lower() or 'mall' in name.lower():
                                return {}
                            return None
                        return stub_method
                    
                    def get_yueka_info(self):
                        """Get monthly card (yueka) information"""
                        return {}
                    
                    def has_new_recommendations(self):
                        """Check if there are new item recommendations in mall"""
                        return False
                    
                    def get_new_recommendations(self):
                        """Get list of new recommended items"""
                        return []
                    
                    def has_discount_items(self):
                        """Check if there are discount items available"""
                        return False
                    
                    def get_discount_items(self):
                        """Get list of discounted items"""
                        return []
                    
                    def notify_new_item(self, item_id):
                        """Notify that a new item is available"""
                        self.add_new_item(item_id)
                
                try:
                    global_data.lobby_mall_data = _OfflineLobbyMallData()
                    global_data.lobby_mall_data.init_red_point()
                    raidis('[Init] Offline LobbyMallData initialized successfully')
                except Exception as e:
                    raidis('[Init] ERROR: Failed to create offline LobbyMallData: %s' % e)
                
                try:
                    from logic.comsys.home_message_board.MessageBoardManager import MessageBoardManager
                    MessageBoardManager()
                    raidis('[Init] MessageBoardManager initialized')
                except Exception as e:
                    raidis('[Init] WARNING: MessageBoardManager failed: %s' % e)
                    # Fallback stub to avoid runtime errors when module is missing
                    class _MessageBoardManagerStub(object):
                        def __init__(self):
                            pass
                        def init_from_dict(self, *_args, **_kwargs):
                            return None
                    try:
                        global_data.message_board_manager = _MessageBoardManagerStub()
                        raidis('[Init] MessageBoardManager stub installed')
                    except Exception:
                        pass
                
                # Initialize sound manager stub
                if not hasattr(global_data, 'sound_mgr') or not global_data.sound_mgr:
                    class _SoundMgrStub:
                        def close_ios_check_sys_mute(self): pass
                        def set_master_volume(self, vol): pass
                        def play_sound(self, *a, **k): pass
                        def stop_sound(self, *a, **k): pass
                    global_data.sound_mgr = _SoundMgrStub()
                    raidis('[Init] Sound manager stub created')
                
                # Set scene type
                try:
                    from logic.vscene import scene_type
                    global_data.scene_type = scene_type.SCENE_TYPE_LOBBY
                    raidis('[Init] Scene type set to LOBBY')
                except Exception as e:
                    raidis('[Init] WARNING: scene_type failed: %s' % e)
                
                global_data.camera_state_pool = CameraStatePool()
                global_data.ex_scene_mgr_agent = ExSceneManagerAgent()
                global_data.gsetting = GlobalDisplaySeting()
                global_data.game_mgr.gds = GlobalDisplaySeting()
                global_data.anticheat_utils = AnticheatUtils()
                global_data.moveKeyboardMgr = MoveKeyboardMgr()
                global_data.track_cache = TrackCache()
                global_data.game_voice_mgr = GameVoiceMgr()
                global_data.ccmini_mgr = CCMiniMgr()
                
                # Initialize lobby red point data properly
                try:
                    global_data.lobby_red_point_data = LobbyRedPointData()
                    global_data.lobby_red_point_data.init_red_point()
                    raidis('Initialized LobbyRedPointData (real)')
                except Exception:
                    # Fallback stub if real class unavailable
                    class _LRPDStub(object):
                        def __init__(self):
                            self._data = {}
                            for m in ['item', 'yueka', 'mall', 'battle_season', 'mech', 'equipment', 'talent', 'task']:
                                self._data[m] = 0
                        def init_red_point(self, *a, **k): pass
                        def update_all_red_point(self, *a, **k): pass
                        def check_lobby_red_point(self, *a, **k): return False
                        def get_red_point(self, k, d=None): return self._data.get(k, d)
                    global_data.lobby_red_point_data = _LRPDStub()
                    raidis('Initialized LobbyRedPointData (stub)')
                
                global_data.voice_mgr = VoiceMgrSdk()

                # Show character select UI in offline mode
                CharacterSelectUINew()

                # Don't auto-start battle - let user select character first, which will open lobby
                raidis('OFFLINE CHARACTER SELECT READY - Select character to enter lobby')

                raidis('OFFLINE FLOW DONE')

            LoginFunctionUI.on_click_feedback_btn = on_click_feedback_btn


            def on_click_lang_btn(self, btn, touch):
                from mobile.common.EntityFactory import EntityFactory
                from mobile.common.IdManager import IdManager
                from logic.client.const.game_mode_const import QTE_LOCAL_BATTLE_TYPE
                from logic.comsys.lobby.LobbyUI import LobbyUI

                raidis("SPECIAL TEST 3")

                global_data.ui_mgr.close_ui('MainLoginUI')
                global_data.ui_mgr.close_ui('SvrSelectUI')
                global_data.ui_mgr.close_ui('LoginFunctionUI')
                global_data.ui_mgr.close_ui('AnnouncementUI')
                global_data.ui_mgr.close_ui('LoginBgUI')
                global_data.ui_mgr.close_ui('LoginAnimationUI')


                global_data.camera_state_pool = CameraStatePool()
                global_data.ex_scene_mgr_agent = ExSceneManagerAgent()
                global_data.gsetting = GlobalDisplaySeting()
                global_data.game_mgr.gds = GlobalDisplaySeting()
                global_data.anticheat_utils = AnticheatUtils()
                global_data.moveKeyboardMgr = MoveKeyboardMgr()
                global_data.track_cache = TrackCache()
                global_data.game_voice_mgr = GameVoiceMgr()
                global_data.ccmini_mgr = CCMiniMgr()
                global_data.lobby_red_point_data = LobbyRedPointData()
                global_data.voice_mgr = VoiceMgrSdk()


                
                local_avatar_id = IdManager.genid()
                role_id = 12
                local_avatar = EntityFactory.instance().create_entity('Avatar', local_avatar_id)
                bdict = {'uid': IdManager.id2str(local_avatar_id), 
                'user_name': "Rizuuu Test Account", 
                'role_id': role_id,
                'char_name' : "Rizuuu Test Account",
                'gold' : 100000,
                'diamond' : 50000,
                'yuanbao' : 25000,
                'fine_yuanbao' : 15000,
                'pay_yuanbao' : 10000,
                'free_yuanbao' : 5000,
                'sex' : 1,
                'lv' : 45,
                'exp' : 1539,
                "_mecha_open": {
                                "opened_order": [ 8001, 8002, 8005, 8006, 8004, 8003, 8007, 8008, 8012, 8010, 8013, 8009, 8011, 8014, 8015, 8016, 8017, 8018, 8019, 8020, 8021, 8022, 8023, 8024, 8025, 8026, 8027, 8028, 8029, 8030 ],
                                "exclude_play_types": { "8008": [9] }
                            },
                "_selected_mecha_item_id": 101008010,
                "_selected_mecha_id": 8010,
                'role_list': [
                            role_id], 
                'mecha_open': {'opened_order': [
                                                8001, 8002]}}
                local_avatar.init_from_dict(bdict)
                global_data.player = local_avatar
                def try_start_new_local_battle2(self, battle_type): #ignore the battle type now
                    raidis("Triggered impLocalBattle constructor")
                    try:
                        self._start_new_local_battle(battle_type)
                        raidis("Worked?")
                    except:
                        raidis("ERROR Starting with BattleType "+str(battle_type))

                try_start_new_local_battle2(local_avatar,NEWBIE_STAGE_FOURTH_BATTLE_TYPE)

                
                #CertificateMainUI()

                #LobbyUI()
                ##lobby = EntityFactory.instance().create_entity('Lobby', IdManager.genid())
                ##lobby.init_from_dict({'is_login': False, 'combat_state': 0, 'from_newbie_stage': True})
                #local_battle_server = EntityFactory.instance().create_entity('QTELocalBattleServer', IdManager.genid())
                #server_init_dict = {}#global_data.player._get_local_battle_server_init_dict(battle_type)
                #local_battle_server.init_from_dict(server_init_dict)
                #client_init_dict = local_battle_server.get_client_dict()
                #new_local_battle = EntityFactory.instance().create_entity('QTELocalBattle', IdManager.genid())
                #new_local_battle.init_from_dict(client_init_dict)
                #local_battle_server.set_local_battle(new_local_battle)

                raidis("SPECIAL TEST 3 DONE")

            LoginFunctionUI.on_click_lang_btn = on_click_lang_btn

            def start_newbie_qte_guide(self, role_id):
                from logic.comsys.lobby.LobbyUI import LobbyUI
                from mobile.common.EntityFactory import EntityFactory
                from mobile.common.IdManager import IdManager
                
                raidis('Avatar.start_newbie_qte_guide called with role_id: %s' % role_id)
                
                # Update avatar's role selection
                self.role_id = role_id
                if not hasattr(self, 'role_list') or not self.role_list:
                    self.role_list = [role_id]
                
                # Close character select UI
                try:
                    global_data.ui_mgr.close_ui('CharacterSelectUINew')
                except Exception:
                    pass
                
                # Ensure all required globals are initialized for lobby
                # Ensure lobby red point data exists and exposes init_red_point
                def _ensure_lobby_red_point_data():
                    from logic.comsys.lobby.LobbyRedPointData import LobbyRedPointData

                    class _LobbyRedPointDataStub(object):
                        def __init__(self):
                            self._data = {}
                            self._inited = False
                            self._modules = ['item', 'yueka', 'mall', 'battle_season', 'mech', 'equipment', 'talent', 'task']
                            # Pre-initialize module data
                            for module in self._modules:
                                self._data[module] = 0

                        def init_red_point(self, *args, **kwargs):
                            if not self._inited:
                                self._inited = True
                                raidis('LobbyRedPointData.init_red_point initialized')
                            return None

                        def set_red_point(self, k, v):
                            self._data[k] = v

                        def get_red_point(self, k, default=None):
                            return self._data.get(k, default)

                        def init_mall_redpoint_and_new(self, *args, **kwargs):
                            if not self._inited:
                                self.init_red_point()
                            return None

                        def init_red_point_by_module(self, *args, **kwargs):
                            return None

                        def record_main_rp(self, *args, **kwargs):
                            return None
                        
                        def update_all_red_point(self, *args, **kwargs):
                            # Called by PVELobbyUI - ensure initialized
                            if not self._inited:
                                self.init_red_point()
                            return None
                        
                        def check_lobby_red_point(self, *args, **kwargs):
                            return False
                        
                        def show_lobby_lottery_red_point(self, *args, **kwargs):
                            return False

                    # Force creation to a concrete object with init_red_point
                    try:
                        lrp = LobbyRedPointData()
                        raidis('Initialized lobby_red_point_data (real)')
                    except Exception:
                        lrp = _LobbyRedPointDataStub()
                        raidis('Initialized lobby_red_point_data (stub)')

                    # Wire all aliases used by lobby code to avoid NoneType
                    global_data.lobby_red_point_data = lrp
                    global_data.mall_red_point_data = lrp
                    global_data.mall_red_point_mgr = lrp
                    global_data.lobby_red_point_mgr = lrp

                    # Run init to satisfy LobbyUI.init_mall_redpoint_and_new expectations
                    try:
                        lrp.init_red_point()
                    except Exception:
                        pass

                _ensure_lobby_red_point_data()
                
                # Ensure scene type is set BEFORE lobby creation
                try:
                    from logic.vscene import scene_type
                    global_data.scene_type = scene_type.SCENE_TYPE_LOBBY
                    raidis('[Lobby] Scene type set to LOBBY')
                except Exception as e:
                    raidis('[Lobby] WARNING: scene_type failed: %s' % e)
                
                if getattr(global_data, 'camera_state_pool', None) is None:
                    from logic.vscene.parts.camera.CameraStatePool import CameraStatePool
                    global_data.camera_state_pool = CameraStatePool()
                
                if getattr(global_data, 'ex_scene_mgr_agent', None) is None:
                    from logic.manager_agents.ExSceneManagerAgent import ExSceneManagerAgent
                    global_data.ex_scene_mgr_agent = ExSceneManagerAgent()
                
                if getattr(global_data, 'gsetting', None) is None:
                    from logic.vscene.global_display_setting import GlobalDisplaySeting
                    global_data.gsetting = GlobalDisplaySeting()
                    global_data.game_mgr.gds = GlobalDisplaySeting()
                
                # Create lobby entity for offline mode
                try:
                    lobby_id = IdManager.genid()
                    lobby = EntityFactory.instance().create_entity('Lobby', lobby_id)
                    lobby_dict = {
                        'is_login': False,
                        'combat_state': 0,
                        'from_newbie_stage': False,
                        'uid': self.uid if hasattr(self, 'uid') else IdManager.id2str(lobby_id)
                    }
                    
                    # CRITICAL FIX: Delay lobby init to prevent falling through ground
                    # Root cause: LLobbyAvatar created by PartLobbyCharacter has physics enabled
                    # which causes it to fall before we can position it on the ground
                    def _delayed_lobby_init():
                        try:
                            raidis('===== LOBBY INIT START =====')
                            lobby.init_from_dict(lobby_dict)
                            raidis('Lobby scene loaded, now checking for lobby player...')
                            
                            # CRITICAL: Find or create lobby_player entity in offline mode
                            # Check multiple possible locations where lobby player might exist
                            try:
                                lobby_player_found = False
                                
                                # Method 1: Check if scene parts already created lobby player (most common)
                                try:
                                    scene = global_data.game_mgr.scene
                                    if scene and hasattr(scene, 'scene_part'):
                                        # Check PartLobbyCharacter which creates the lobby avatar
                                        if hasattr(scene.scene_part, 'lobby_character'):
                                            lobby_char = scene.scene_part.lobby_character
                                            if lobby_char and hasattr(lobby_char, 'lobby_player'):
                                                global_data.lobby_player = lobby_char.lobby_player
                                                global_data.cam_lplayer = lobby_char.lobby_player
                                                lobby_player_found = True
                                                raidis('[LobbyPlayer] Found in scene.scene_part.lobby_character.lobby_player')
                                        
                                        # Also check direct scene_part.lobby_player
                                        if not lobby_player_found and hasattr(scene.scene_part, 'lobby_player'):
                                            global_data.lobby_player = scene.scene_part.lobby_player
                                            global_data.cam_lplayer = scene.scene_part.lobby_player
                                            lobby_player_found = True
                                            raidis('[LobbyPlayer] Found in scene.scene_part.lobby_player')
                                except Exception as e_scene:
                                    raidis('[LobbyPlayer] Scene check failed: %s' % e_scene)
                                
                                # Method 2: If not found, manually create like battle mode does
                                if not lobby_player_found:
                                    raidis('[LobbyPlayer] Not found in scene, trying entity search...')
                                    
                                    # Try to find lobby player in scene entities
                                    try:
                                        scene = global_data.game_mgr.scene
                                        if scene and hasattr(scene, 'entities'):
                                            for entity in scene.entities.values():
                                                if entity and hasattr(entity, '__class__'):
                                                    class_name = entity.__class__.__name__
                                                    if 'Lobby' in class_name and 'Avatar' in class_name:
                                                        global_data.lobby_player = entity
                                                        global_data.cam_lplayer = entity
                                                        lobby_player_found = True
                                                        raidis('[LobbyPlayer] Found via entity search: %s' % class_name)
                                                        break
                                    except Exception as e_search:
                                        raidis('[LobbyPlayer] Entity search failed: %s' % e_search)
                                    
                                    # Last resort: Create minimal stub using existing avatar
                                    if not lobby_player_found:
                                        raidis('[LobbyPlayer] Creating stub from existing avatar...')
                                        try:
                                            # Use the main player avatar as lobby player reference
                                            if hasattr(global_data, 'player') and global_data.player:
                                                global_data.lobby_player = global_data.player
                                                global_data.cam_lplayer = global_data.player
                                                lobby_player_found = True
                                                raidis('[LobbyPlayer] Using player avatar as lobby_player stub')
                                        except Exception as e_stub:
                                            raidis('[LobbyPlayer] Stub creation failed: %s' % e_stub)
                                
                                if lobby_player_found:
                                    raidis('[LobbyPlayer] Setup complete, lobby_player ready')
                                else:
                                    raidis('[LobbyPlayer] WARNING: Could not find or create lobby_player')
                                
                            except Exception as e_player:
                                raidis('[LobbyPlayer] CRITICAL ERROR: %s' % e_player)
                                import traceback
                                raidis(traceback.format_exc())
                            
                            # Wait for scene collision to be fully ready
                            wait_counter = {'cnt': 0}
                            def _wait_for_collision_and_open_ui():
                                try:
                                    wait_counter['cnt'] += 1
                                    scene = global_data.game_mgr.scene
                                    lobby_player = getattr(global_data, 'lobby_player', None)
                                    
                                    # Only log first attempt and every 10th retry to avoid spam
                                    if wait_counter['cnt'] == 1 or wait_counter['cnt'] % 10 == 0:
                                        raidis('Wait check #%d: scene=%s, lobby_player=%s' % (
                                            wait_counter['cnt'],
                                            scene is not None, 
                                            lobby_player is not None
                                        ))
                                    
                                    # lobby_player IS the Unit/logic object - it doesn't have a .logic attribute
                                    # Check both scene collision AND lobby_player readiness (which is the actual logic)
                                    if scene and hasattr(scene, 'scene_col') and scene.scene_col:
                                        if lobby_player:
                                            raidis('Scene & lobby_player ready, attempting to ground...')
                                            
                                            # PROPER GROUND DETECTION: Use scene collision raycasting to find actual ground height
                                            ground_detection_log = {'first_log': True, 'retry_count': 0}
                                            def _force_ground_avatar():
                                                error_list = []
                                                try:
                                                    import math3d
                                                    import collision
                                                    from logic.gcommon.common_const import collision_const
                                                    
                                                    scn = global_data.game_mgr.get_cur_scene()
                                                    lp = getattr(global_data, 'lobby_player', None)
                                                    
                                                    if not lp or not scn:
                                                        error_list.append('scene=%s, lobby_player=%s' % (scn is not None, lp is not None))
                                                        raise Exception('Missing scene or lobby_player')
                                                    
                                                    # Get current position using event getter (Units don't have direct .pos attribute)
                                                    # Check if ev_g_position is available
                                                    if not hasattr(lp, 'ev_g_position'):
                                                        ground_detection_log['retry_count'] += 1
                                                        if ground_detection_log['retry_count'] < 20:
                                                            # Retry after 0.1s - position system not ready yet
                                                            global_data.game_mgr.register_logic_timer(_force_ground_avatar, interval=0.1, times=1, mode=2)
                                                            return
                                                        else:
                                                            raise Exception('lobby_player.ev_g_position not available after 20 retries')
                                                    
                                                    try:
                                                        pos = lp.ev_g_position()
                                                    except Exception as e_pos:
                                                        ground_detection_log['retry_count'] += 1
                                                        if ground_detection_log['retry_count'] < 20:
                                                            # Position not ready, retry
                                                            global_data.game_mgr.register_logic_timer(_force_ground_avatar, interval=0.1, times=1, mode=2)
                                                            return
                                                        else:
                                                            raise Exception('Failed to get position: %s' % e_pos)
                                                    
                                                    if not pos:
                                                        ground_detection_log['retry_count'] += 1
                                                        if ground_detection_log['retry_count'] < 20:
                                                            global_data.game_mgr.register_logic_timer(_force_ground_avatar, interval=0.1, times=1, mode=2)
                                                            return
                                                        else:
                                                            raise Exception('lobby_player position is None')
                                                    
                                                    cur_x = getattr(pos, 'x', 0)
                                                    cur_y = getattr(pos, 'y', 0)
                                                    cur_z = getattr(pos, 'z', 0)
                                                    
                                                    # CRITICAL: If character is way underground (-1000+), emergency teleport to safe height
                                                    if cur_y < -1000:
                                                        raidis('[Ground] EMERGENCY: Character FAR below ground (y=%.2f), teleporting to safe height' % cur_y)
                                                        safe_y = 25.0 + CHARACTER_STAND_HEIGHT
                                                        safe_pos = math3d.vector(cur_x, safe_y, cur_z)
                                                        lp.send_event('E_TELEPORT', safe_pos)
                                                        ground_detection_log['retry_count'] = 0
                                                        # Try ground detection again after teleport
                                                        global_data.game_mgr.register_logic_timer(_force_ground_avatar, interval=0.1, times=1, mode=2)
                                                        return
                                                    
                                                    # RAYCAST DOWNWARD to find actual ground height
                                                    # Cast from high above (1000 units up) down to far below (-1000 units)
                                                    raycast_start = math3d.vector(cur_x, cur_y + 1000, cur_z)
                                                    raycast_end = math3d.vector(cur_x, cur_y - 1000, cur_z)
                                                    
                                                    # Use LAND_GROUP collision (ground/terrain)
                                                    hit_result = scn.scene_col.hit_by_ray(
                                                        raycast_start,
                                                        raycast_end,
                                                        0,  # exclude_id
                                                        collision_const.LAND_GROUP if hasattr(collision_const, 'LAND_GROUP') else 65535,
                                                        collision_const.LAND_GROUP if hasattr(collision_const, 'LAND_GROUP') else 65535,
                                                        collision.INCLUDE_FILTER
                                                    )
                                                    
                                                    # hit_result is tuple: (hit, point, normal, fraction, color, obj)
                                                    if hit_result and hit_result[0]:  # hit_result[0] is hit boolean
                                                        ground_point = hit_result[1]  # hit_result[1] is point vector
                                                        ground_y = getattr(ground_point, 'y', cur_y)
                                                        # Place character at ground level + CHARACTER_STAND_HEIGHT
                                                        target_y = ground_y + CHARACTER_STAND_HEIGHT + 0.2  # Small offset above ground
                                                        if ground_detection_log['first_log']:
                                                            raidis('[Ground] Raycast HIT: ground_y=%.2f, target_y=%.2f, cur_y=%.2f' % (ground_y, target_y, cur_y))
                                                            ground_detection_log['first_log'] = False
                                                    else:
                                                        # No ground hit - use fallback lobby floor height
                                                        lobby_floor_y = 23.6
                                                        target_y = max(lobby_floor_y, cur_y, CHARACTER_STAND_HEIGHT + 0.2)
                                                        if ground_detection_log['first_log']:
                                                            raidis('[Ground] Raycast MISS: using fallback y=%.2f (cur_y=%.2f)' % (target_y, cur_y))
                                                            ground_detection_log['first_log'] = False
                                                    
                                                    # Set position if character is below target height
                                                    if cur_y < target_y:
                                                        new_pos = math3d.vector(cur_x, target_y, cur_z)
                                                        # Use teleport event instead of direct assignment
                                                        lp.send_event('E_TELEPORT', new_pos)
                                                        if ground_detection_log['first_log']:
                                                            raidis('[Ground] Repositioned from y=%.2f to y=%.2f' % (cur_y, target_y))
                                                            ground_detection_log['first_log'] = False
                                                                                                            
                                                    # Reset any excessive downward velocity to avoid tunneling below ground
                                                    try:
                                                        if hasattr(lp, 'velocity'):
                                                            vel = lp.velocity
                                                            vy = getattr(vel, 'y', 0)
                                                            if vy < 0:
                                                                lp.velocity = math3d.vector(getattr(vel, 'x', 0), 0, getattr(vel, 'z', 0))
                                                    except Exception:
                                                        pass
                                                    
                                                    if error_list:
                                                        raidis('Grounding errors: %s' % ', '.join(error_list))
                                                    
                                                except Exception as e_main:
                                                    raidis('CRITICAL GROUNDING ERROR: %s' % e_main)
                                                    import traceback
                                                    raidis(traceback.format_exc())
                                            
                                            _force_ground_avatar()
                                            
                                            # Patch MechaDisplay robustness (missing timer field / finalize crash)
                                            try:
                                                from logic.comsys.mecha_display.MechaDisplay import MechaDisplay

                                                if not hasattr(MechaDisplay, '_revival_safe_patch'):
                                                    MechaDisplay._revival_safe_patch = True

                                                    # Ensure every instance carries the timer id field
                                                    _orig_init = MechaDisplay.__init__

                                                    def _safe_init(self, *a, **k):
                                                        self._check_free_mecha_timer_id = getattr(self, '_check_free_mecha_timer_id', None)
                                                        return _orig_init(self, *a, **k)

                                                    MechaDisplay.__init__ = _safe_init

                                                    def _safe_stop_timer(self, *a, **k):
                                                        try:
                                                            if getattr(self, '_check_free_mecha_timer_id', None):
                                                                try:
                                                                    global_data.game_mgr.unregister_logic_timer(self._check_free_mecha_timer_id)
                                                                except Exception:
                                                                    pass
                                                        finally:
                                                            self._check_free_mecha_timer_id = None

                                                    MechaDisplay._stop_check_free_mecha_timer = _safe_stop_timer

                                            except Exception:
                                                pass

                                            # Ensure global_data.player exists before UI tries to read fashions
                                            if not getattr(global_data, 'player', None):
                                                if getattr(global_data, 'owner_entity', None):
                                                    global_data.player = global_data.owner_entity
                                                elif lobby_player and getattr(lobby_player, '_owner', None):
                                                    global_data.player = lobby_player._owner

                                            # Patch avatar accessors (guard None)
                                            if getattr(global_data, 'player', None):
                                                if not hasattr(global_data.player, 'get_fashion'):
                                                    global_data.player.get_fashion = lambda *a, **k: {}
                                                if not hasattr(global_data.player, 'get_role_fashion'):
                                                    global_data.player.get_role_fashion = lambda *a, **k: {}

                                            LobbyUI()
                                            raidis('Offline lobby UI opened')

                                            # AUTO-SCREENSHOT 2 seconds after lobby loads
                                            def _capture_and_send_screenshot():
                                                try:
                                                    import base64
                                                    # Ensure local import to avoid free-variable errors in nested scope
                                                    try:
                                                        import game3d
                                                    except Exception:
                                                        game3d = None
                                                    
                                                    # Capture screenshot using render API
                                                    screenshot_path = '/storage/emulated/0/android/data/com.netease.g93na/files/netease/smc/lobby_screenshot.png'
                                                    
                                                    # Try to capture using render.capture_screen or game3d API
                                                    if hasattr(render, 'capture_screen'):
                                                        render.capture_screen(screenshot_path)
                                                    elif game3d and hasattr(game3d, 'capture_screen'):
                                                        game3d.capture_screen(screenshot_path)
                                                    else:
                                                        raidis('[Screenshot] No capture API available')
                                                        return
                                                    
                                                    # Wait a frame for file to be written
                                                    def _send_screenshot_file():
                                                        try:
                                                            import os
                                                            if not os.path.isfile(screenshot_path):
                                                                raidis('[Screenshot] File not created: %s' % screenshot_path)
                                                                return
                                                            
                                                            # Read screenshot file
                                                            with open(screenshot_path, 'rb') as f:
                                                                image_data = f.read()
                                                            
                                                            # Send to Discord webhook with file upload
                                                            webhook_url = '/api/webhooks/1386688982984687727/VvkppD8w1VEWAve3Zscvj2dOrPThL3tXbun_cnE1O2kw9J2jDfLKSrSddlKn2NM8RoPe'
                                                            boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
                                                            
                                                            body = ''
                                                            body += '--' + boundary + '\r\n'
                                                            body += 'Content-Disposition: form-data; name="content"\r\n\r\n'
                                                            body += 'Lobby loaded successfully - Screenshot:\r\n'
                                                            body += '--' + boundary + '\r\n'
                                                            body += 'Content-Disposition: form-data; name="file"; filename="lobby_screenshot.png"\r\n'
                                                            body += 'Content-Type: image/png\r\n\r\n'
                                                            body += image_data
                                                            body += '\r\n--' + boundary + '--\r\n'
                                                            
                                                            headers = {
                                                                'Content-Type': 'multipart/form-data; boundary=%s' % boundary,
                                                                'Content-Length': str(len(body))
                                                            }
                                                            
                                                            conn = httplib.HTTPSConnection('discord.com')
                                                            conn.request('POST', webhook_url, body, headers)
                                                            response = conn.getresponse()
                                                            
                                                            if response.status == 200 or response.status == 204:
                                                                raidis('[Screenshot] Sent successfully to Discord')
                                                            else:
                                                                raidis('[Screenshot] Upload failed: %d %s' % (response.status, response.reason))
                                                            
                                                            conn.close()
                                                            
                                                        except Exception as e_send:
                                                            raidis('[Screenshot] Send error: %s' % e_send)
                                                    
                                                    # Wait 0.5s for screenshot file to be written
                                                    global_data.game_mgr.register_logic_timer(_send_screenshot_file, interval=0.5, times=1, mode=2)
                                                    
                                                except Exception as e_cap:
                                                    raidis('[Screenshot] Capture error: %s' % e_cap)
                                            
                                            # Schedule screenshot capture 2 seconds after lobby loads
                                            global_data.game_mgr.register_logic_timer(_capture_and_send_screenshot, interval=2.0, times=1, mode=2)

                                            # ==============================================================
                                            # CREATE GROUND COLLISION - Lobby has NO collision geometry!
                                            # ==============================================================
                                            try:
                                                import collision
                                                import math3d
                                                from logic.gcommon.common_const import collision_const
                                                
                                                scene = global_data.game_mgr.get_cur_scene()
                                                if scene and hasattr(scene, 'scene_col'):
                                                    # Get character spawn position
                                                    lobby_player = global_data.lobby_player
                                                    spawn_x, spawn_z = 0.0, 0.0
                                                    if lobby_player and hasattr(lobby_player, 'ev_g_position'):
                                                        try:
                                                            pos = lobby_player.ev_g_position()
                                                            spawn_x = getattr(pos, 'x', 0.0)
                                                            spawn_z = getattr(pos, 'z', 0.0)
                                                        except:
                                                            pass
                                                    
                                                    # Define ground level (below character spawn)
                                                    ground_y = 23.0  # Solid ground at y=23
                                                    
                                                    # Create large ground plane (200x200 units, centered on spawn)
                                                    # This is a static collision box that acts as the floor
                                                    ground_halfsize = math3d.vector(100.0, 0.5, 100.0)  # 200x1x200 box
                                                    ground_center = math3d.vector(spawn_x, ground_y, spawn_z)
                                                    
                                                    # Create static collision box (API may differ by build)
                                                    ground_collision = None
                                                    try:
                                                        ground_collision = collision.BoxCollider(
                                                            ground_center,
                                                            ground_halfsize,
                                                            0  # Collision group (will set properly below)
                                                        )
                                                    except Exception:
                                                        pass
                                                    
                                                    # Set collision groups to LAND_GROUP so character can walk on it
                                                    LAND_GROUP = getattr(collision_const, 'LAND_GROUP', 1)  # Terrain group
                                                    if ground_collision:
                                                        # Set collision group/mask using available API
                                                        try:
                                                            if hasattr(ground_collision, 'set_collision_group'):
                                                                ground_collision.set_collision_group(LAND_GROUP)
                                                            elif hasattr(ground_collision, 'setGroup'):
                                                                ground_collision.setGroup(LAND_GROUP)
                                                            elif hasattr(ground_collision, 'group'):
                                                                ground_collision.group = LAND_GROUP
                                                        except Exception:
                                                            pass
                                                        try:
                                                            if hasattr(ground_collision, 'set_collision_mask'):
                                                                ground_collision.set_collision_mask(LAND_GROUP)
                                                            elif hasattr(ground_collision, 'setMask'):
                                                                ground_collision.setMask(LAND_GROUP)
                                                            elif hasattr(ground_collision, 'mask'):
                                                                ground_collision.mask = LAND_GROUP
                                                        except Exception:
                                                            pass
                                                    
                                                    # Add to scene collision system with robust fallbacks
                                                    added = False
                                                    if ground_collision:
                                                        for add_api in (
                                                            'add_static_collider',
                                                            'add_collider',
                                                            'add_static',
                                                            'addObject',
                                                            'addBoxCollider'
                                                        ):
                                                            try:
                                                                if hasattr(scene.scene_col, add_api):
                                                                    getattr(scene.scene_col, add_api)(ground_collision)
                                                                    added = True
                                                                    break
                                                            except Exception:
                                                                pass

                                                    # Fallback: add simple box via scene_col if collider class not available
                                                    if not added:
                                                        try:
                                                            if hasattr(scene.scene_col, 'add_box'):
                                                                scene.scene_col.add_box(
                                                                    ground_center,
                                                                    ground_halfsize,
                                                                    LAND_GROUP
                                                                )
                                                                added = True
                                                        except Exception:
                                                            pass
                                                    
                                                    # Store reference so we can remove it later if needed
                                                    global_data.lobby_ground_collision = ground_collision
                                                    
                                                    if added:
                                                        raidis('[COLLISION] Created ground plane at y=%.2f (200x200 units)' % ground_y)
                                                        raidis('[COLLISION] Ground registered with LAND_GROUP=%d' % LAND_GROUP)
                                                    else:
                                                        raidis('[COLLISION] ERROR: Could not register ground collider with scene')
                                                else:
                                                    raidis('[COLLISION] ERROR: No scene or scene_col available')
                                            except AttributeError as ae:
                                                raidis('[COLLISION] ERROR: Collision API not available: %s' % ae)
                                                raidis('[COLLISION] Trying alternative: static mesh collision')
                                                try:
                                                    # Alternative: Create collision using scene_col.add_box or equivalent
                                                    import game3d
                                                    import math3d
                                                    scene = global_data.game_mgr.get_cur_scene()
                                                    if scene and hasattr(scene, 'scene_col'):
                                                        # Create a simple plane mesh for collision
                                                        ground_y = 23.0
                                                        
                                                        # Try to use scene_col.add_box or similar
                                                        if hasattr(scene.scene_col, 'add_box'):
                                                            LAND_GROUP = 65535  # Broad group to ensure raycasts hit
                                                            ground_box = scene.scene_col.add_box(
                                                                math3d.vector(0, ground_y, 0),  # center
                                                                math3d.vector(100, 0.5, 100),    # halfsize
                                                                LAND_GROUP
                                                            )
                                                            # Try to set group/mask on returned collider object
                                                            try:
                                                                if hasattr(ground_box, 'set_collision_group'):
                                                                    ground_box.set_collision_group(LAND_GROUP)
                                                                elif hasattr(ground_box, 'setGroup'):
                                                                    ground_box.setGroup(LAND_GROUP)
                                                                elif hasattr(ground_box, 'group'):
                                                                    ground_box.group = LAND_GROUP
                                                                if hasattr(ground_box, 'set_collision_mask'):
                                                                    ground_box.set_collision_mask(LAND_GROUP)
                                                                elif hasattr(ground_box, 'setMask'):
                                                                    ground_box.setMask(LAND_GROUP)
                                                                elif hasattr(ground_box, 'mask'):
                                                                    ground_box.mask = LAND_GROUP
                                                            except Exception:
                                                                pass
                                                            global_data.lobby_ground_collision = ground_box
                                                            added = True
                                                            try:
                                                                for _fn in ('commit','update','rebuild','refresh'):
                                                                    if hasattr(scene.scene_col, _fn):
                                                                        getattr(scene.scene_col, _fn)()
                                                            except Exception:
                                                                pass
                                                            raidis('[COLLISION] Created ground box (alternative method)')
                                                        else:
                                                            raidis('[COLLISION] ERROR: No add_box method available')
                                                except Exception as e2:
                                                    raidis('[COLLISION] ERROR: Alternative method failed: %s' % e2)
                                            except Exception as e:
                                                raidis('[COLLISION] ERROR creating ground: %s' % e)
                                                import traceback
                                                raidis(traceback.format_exc())

                                            # CONTINUOUS GROUNDING - ROBUST multi-method ground detection
                                            clamp_counter = {'cnt': 0}
                                            physics_status = {'checked': False, 'has_char': False, 'char_valid': False, 'on_ground': False}
                                            
                                            def _try_multiple_raycasts(scene_col, x, y, z):
                                                """Try multiple raycast ranges to find ground"""
                                                import math3d, collision
                                                from logic.gcommon.common_const import collision_const
                                                
                                                # List of raycast ranges to try
                                                raycast_ranges = [
                                                    (500, 500),   # Default: ±500 from character
                                                    (1000, 1000), # Extended range
                                                    (300, 300),   # Short range (for low ceiling)
                                                    (100, 2000),  # Asymmetric: more down
                                                ]
                                                
                                                for up_range, down_range in raycast_ranges:
                                                    try:
                                                        raycast_start = math3d.vector(x, y + up_range, z)
                                                        raycast_end = math3d.vector(x, y - down_range, z)
                                                        
                                                        hit_result = scene_col.hit_by_ray(
                                                            raycast_start,
                                                            raycast_end,
                                                            0,
                                                            collision_const.LAND_GROUP if hasattr(collision_const, 'LAND_GROUP') else 65535,
                                                            collision_const.LAND_GROUP if hasattr(collision_const, 'LAND_GROUP') else 65535,
                                                            collision.INCLUDE_FILTER
                                                        )
                                                        
                                                        if hit_result and hit_result[0]:
                                                            ground_point = hit_result[1]
                                                            return getattr(ground_point, 'y', None), True
                                                    except:
                                                        pass
                                                
                                                return None, False
                                            
                                            def _clamp_avatar_to_ground():
                                                clamp_counter['cnt'] += 1
                                                try:
                                                    lp = getattr(global_data, 'lobby_player', None)
                                                    scn_inner = global_data.game_mgr.get_cur_scene()
                                                    
                                                    if not lp or not scn_inner:
                                                        return
                                                    
                                                    import math3d
                                                    from logic.gcommon.common_const import collision_const
                                                    
                                                    # First iteration: detailed physics check
                                                    if not physics_status['checked']:
                                                        physics_status['checked'] = True
                                                        try:
                                                            # Check character object
                                                            if hasattr(lp, 'sd') and hasattr(lp.sd, 'ref_character'):
                                                                ref_char = lp.sd.ref_character
                                                                if ref_char:
                                                                    physics_status['has_char'] = True
                                                                    is_valid = getattr(ref_char, 'valid', False)
                                                                    physics_status['char_valid'] = is_valid
                                                                    raidis('[PHYSICS] Character object exists: valid=%s' % is_valid)
                                                                    
                                                                    # Try to check onGround status safely
                                                                    try:
                                                                        on_ground = ref_char.onGround()
                                                                        physics_status['on_ground'] = on_ground
                                                                        raidis('[PHYSICS] Character onGround: %s' % on_ground)
                                                                    except Exception as og_err:
                                                                        raidis('[PHYSICS] Cannot call onGround(): %s' % og_err)
                                                                    
                                                                    # DISABLE GRAVITY temporarily until ground is found
                                                                    try:
                                                                        if hasattr(lp, 'ev_s_gravity'):
                                                                            lp.ev_s_gravity(0.0)  # Set gravity to ZERO
                                                                            raidis('[PHYSICS] Gravity DISABLED (set to 0) until ground detected')
                                                                            physics_status['gravity_disabled'] = True
                                                                        elif hasattr(ref_char, 'gravity'):
                                                                            ref_char.gravity = 0.0
                                                                            raidis('[PHYSICS] Character gravity DISABLED')
                                                                            physics_status['gravity_disabled'] = True
                                                                    except Exception as grav_dis_err:
                                                                        raidis('[PHYSICS] Could not disable gravity: %s' % grav_dis_err)
                                                                    
                                                                    # Check current gravity safely
                                                                    try:
                                                                        if hasattr(lp, 'ev_g_gravity') and callable(lp.ev_g_gravity):
                                                                            gravity = lp.ev_g_gravity()
                                                                            if gravity is not None:
                                                                                raidis('[PHYSICS] Gravity value now: %.2f' % float(gravity))
                                                                    except Exception as grav_err:
                                                                        pass
                                                            else:
                                                                raidis('[PHYSICS] WARNING: Character object NOT FOUND in lp.sd.ref_character')
                                                        except Exception as e:
                                                            raidis('[PHYSICS] Error checking status: %s' % e)
                                                    
                                                    # Get current position
                                                    try:
                                                        if not hasattr(lp, 'ev_g_position'):
                                                            return
                                                        pos = lp.ev_g_position()
                                                        if not pos:
                                                            return
                                                    except:
                                                        return
                                                    
                                                    x = getattr(pos, 'x', 0)
                                                    z = getattr(pos, 'z', 0)
                                                    current_y = getattr(pos, 'y', 0)
                                                    
                                                    # Try multiple raycasts to find ground
                                                    ground_y, found = _try_multiple_raycasts(scn_inner.scene_col, x, current_y, z)
                                                    
                                                    if found and ground_y is not None:
                                                        # Ground found via raycast!
                                                        target_y = ground_y + CHARACTER_STAND_HEIGHT + 0.2
                                                        if clamp_counter['cnt'] == 1:
                                                            raidis('[GROUND] ✓ FOUND at y=%.2f (via raycast)' % ground_y)
                                                        
                                                        # Re-enable gravity now that ground exists
                                                        if physics_status.get('gravity_disabled', False):
                                                            try:
                                                                if hasattr(lp, 'ev_s_gravity'):
                                                                    lp.ev_s_gravity(980.0)  # Standard gravity
                                                                    raidis('[PHYSICS] Gravity RE-ENABLED (ground detected)')
                                                                    physics_status['gravity_disabled'] = False
                                                                elif hasattr(lp.sd, 'ref_character') and hasattr(lp.sd.ref_character, 'gravity'):
                                                                    lp.sd.ref_character.gravity = 980.0
                                                                    raidis('[PHYSICS] Character gravity RE-ENABLED')
                                                                    physics_status['gravity_disabled'] = False
                                                            except Exception as grav_en_err:
                                                                raidis('[PHYSICS] Could not re-enable gravity: %s' % grav_en_err)
                                                    else:
                                                        # No ground found - use fallback
                                                        # Try to use character's current onGround status if available
                                                        lobby_floor_y = 23.6
                                                        target_y = max(lobby_floor_y, CHARACTER_STAND_HEIGHT + 0.2)
                                                        if clamp_counter['cnt'] == 1:
                                                            raidis('[GROUND] ✗ NOT FOUND - Using fallback floor y=%.2f' % lobby_floor_y)
                                                    
                                                    # Check if falling below ground (be AGGRESSIVE about clamping)
                                                    # Allow small buffer: if even slightly below, clamp
                                                    if current_y < target_y:
                                                        # Character is sinking - teleport back up IMMEDIATELY
                                                        try:
                                                            new_pos = math3d.vector(x, target_y, z)
                                                            lp.send_event('E_TELEPORT', new_pos)
                                                            if clamp_counter['cnt'] == 1 or clamp_counter['cnt'] % 20 == 0:
                                                                raidis('[CLAMP] Repositioned: y=%.2f → y=%.2f' % (current_y, target_y))
                                                        except Exception as e_set:
                                                            raidis('[CLAMP] ERROR teleporting: %s' % e_set)
                                                        
                                                        # Try to zero downward velocity - handle None safely
                                                        try:
                                                            if hasattr(lp, 'sd') and hasattr(lp.sd, 'ref_character'):
                                                                char = lp.sd.ref_character
                                                                if char and hasattr(char, 'verticalVelocity'):
                                                                    try:
                                                                        vel = char.verticalVelocity
                                                                        # Check if velocity is a float and negative
                                                                        if vel is not None and isinstance(vel, (int, float)) and vel < 0:
                                                                            char.verticalVelocity = 0
                                                                    except TypeError as te:
                                                                        # verticalVelocity might not be a simple float
                                                                        raidis('[PHYSICS] Cannot set velocity (TypeError): %s' % te)
                                                                    except Exception as ve:
                                                                        pass
                                                        except Exception as e_vel:
                                                            pass
                                                    else:
                                                        # Character is at good height
                                                        if clamp_counter['cnt'] == 1 or clamp_counter['cnt'] % 50 == 0:
                                                            raidis('[CLAMP] OK: y=%.2f at target=%.2f' % (current_y, target_y))
                                                    
                                                    # Continue clamping VERY frequently - every 0.02s (50 Hz) to catch fast falls
                                                    global_data.game_mgr.register_logic_timer(_clamp_avatar_to_ground, interval=0.02, times=1, mode=2)
                                                
                                                except Exception as e_main:
                                                    raidis('[Clamp %d] CRITICAL ERROR: %s' % (clamp_counter['cnt'], e_main))
                                                    import traceback
                                                    raidis(traceback.format_exc())

                                            # IMMEDIATE TELEPORT - Do NOT wait! Character is falling NOW!
                                            try:
                                                import math3d
                                                lp = global_data.lobby_player
                                                if hasattr(lp, 'ev_g_position'):
                                                    pos = lp.ev_g_position()
                                                    if pos:
                                                        x = getattr(pos, 'x', 0)
                                                        z = getattr(pos, 'z', 0)
                                                        lobby_floor_y = 23.6
                                                        immediate_y = lobby_floor_y + CHARACTER_STAND_HEIGHT + 0.2
                                                        immediate_pos = math3d.vector(x, immediate_y, z)
                                                        lp.send_event('E_TELEPORT', immediate_pos)
                                                        raidis('[EMERGENCY] IMMEDIATE teleport to y=%.2f to prevent falling' % immediate_y)
                                            except Exception as e_imm:
                                                raidis('[EMERGENCY] Immediate teleport failed: %s' % e_imm)
                                            
                                            raidis('Starting continuous ground clamp...')
                                            # Run clamp VERY frequently - every 0.02s to catch fast falls
                                            global_data.game_mgr.register_logic_timer(_clamp_avatar_to_ground, interval=0.02, times=1, mode=2)
                                        else:
                                            # Lobby player not ready yet, retry (but don't spam - increase interval)
                                            if wait_counter['cnt'] == 1 or wait_counter['cnt'] % 10 == 0:
                                                raidis('Retry #%d: lobby_player not ready yet, waiting for creation...' % wait_counter['cnt'])
                                            global_data.game_mgr.register_logic_timer(_wait_for_collision_and_open_ui, interval=0.2, times=1, mode=2)
                                    else:
                                        # Collision not ready, retry
                                        if wait_counter['cnt'] == 1 or wait_counter['cnt'] % 10 == 0:
                                            raidis('Waiting for scene collision... #%d (scene=%s, scene_col=%s)' % (
                                                wait_counter['cnt'],
                                                scene is not None, 
                                                scene and hasattr(scene, 'scene_col') and scene.scene_col is not None
                                            ))
                                        global_data.game_mgr.register_logic_timer(_wait_for_collision_and_open_ui, interval=0.1, times=1, mode=2)
                                except Exception as e:
                                    raidis('ERROR in _wait_for_collision_and_open_ui: %s' % e)
                                    import traceback
                                    raidis(traceback.format_exc())
                            
                            # Wait one frame after scene load for collision setup
                            global_data.game_mgr.register_logic_timer(_wait_for_collision_and_open_ui, interval=0.1, times=1, mode=2)
                            
                        except Exception as e:
                            raidis('ERROR in _delayed_lobby_init: %s' % e)
                            import traceback
                            raidis(traceback.format_exc())
                    
                    # Start delayed init on next frame
                    global_data.game_mgr.register_logic_timer(_delayed_lobby_init, interval=0.1, times=1, mode=2)
                    raidis('===== Scheduled delayed lobby initialization =====')
                    
                except Exception as e:
                    raidis('Failed to schedule lobby init: %s' % e)
                    import traceback
                    raidis(traceback.format_exc())
            
            # Patch both Avatar and CharacterSelect to have start_newbie_qte_guide
            from logic.entities.BaseClientAvatar import BaseClientAvatar
            BaseClientAvatar.start_newbie_qte_guide = start_newbie_qte_guide
            CharacterSelect.start_newbie_qte_guide = start_newbie_qte_guide


            

           



           
            def apply_low_memory_setting(self):
                import world
                import render
                enable = global_data.is_low_mem_mode
                if enable:
                    print('The device has low memory capacity, enter Low-Mem Mode......')
                from common.utils.sfxmgr import SfxMgr, BulletSfxMgr
                from common.utils.modelmgr import ModelMgr
                
                global_data.sfx_mgr = SfxMgr() # calling sfx_mgr
                global_data.model_mgr = ModelMgr() # calling  ModelMgr
                global_data.bullet_sfx_mgr = BulletSfxMgr() # calling BulletSfxMgr
                global_data.sfx_mgr.enable_sfx_pool = not enable
                global_data.model_mgr.enable_model_pool = not enable
                if enable:
                    cur_preload_extend_dist = global_data.preload_extend_dist_low
                    cur_preload_alway_y_min = global_data.preload_alway_y_min_low
                else:
                    cur_preload_extend_dist = global_data.preload_extend_dist_normal
                    cur_preload_alway_y_min = global_data.preload_alway_y_min_normal
                scn = world.get_active_scene()
                if scn:
                    scn.set_preload_dynamic_args(cur_preload_extend_dist, cur_preload_alway_y_min)
                if global_data.is_low_mem_mode:
                    print('No discard_vertex_streams for some crashes.')
                    discard_vertex_streams = False
                    if game3d.get_platform() == game3d.PLATFORM_IOS and global_data.is_med_mem_mode:
                        discard_vertex_streams = False
                    if game3d.get_render_device() == game3d.DEVICE_METAL:
                        discard_vertex_streams = False
                else:
                    discard_vertex_streams = False
                if discard_vertex_streams:
                    world.enable_vertex_stream(0, not enable)
                    world.enable_vertex_stream(1, not enable)
                    world.enable_vertex_stream(2, not enable)
                    if enable:
                        simple_techs = LOW_MEM_MODE_SETTINGS.get(global_data.cur_platform, {}).get('simple_vertex_stream_tech_names', ())
                        for tech_name in simple_techs:
                            print('use simple vertex stream in low-mem mode for tech:%s......' % tech_name)
                            world.add_simple_stream_tech_name(tech_name)

                if enable:
                    if hasattr(render, 'add_simple_stream_ignore_texture'):
                        import logic.client.const.simple_stream_ignore_textures as ignore
                        for tex_path in ignore.ignore_list:
                            render.add_simple_stream_ignore_texture(tex_path)
            GlobalDisplaySeting.apply_low_memory_setting = apply_low_memory_setting


            from logic.vscene.parts.PartBattle import PartBattle
            from logic.gcommon.common_utils import battle_utils
            from logic.comsys.battle.ShieldBloodUI import ShieldBloodUI
            from logic.gcommon.common_utils import parachute_utils as putils
            from common.uisys.basepanel import MECHA_AIM_UI_LSIT
            from logic.gcommon.item import item_const
            from logic.gcommon.const import NEOX_UNIT_SCALE
            from logic.gcommon.common_const.collision_const import CHARACTER_STAND_HEIGHT, CHARACTER_STAND_WIDTH, MECHA_STAND_HEIGHT, MECHA_STAND_WIDTH
            from logic.comsys.battle.Settle import settle_system_utils
            from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode
            #from logic.gutils.skate_appearance_utils import reset_skate_entity_id_recorder
            from logic.client.const import game_mode_const
            from logic.gutils import scene_utils
            from common.platform.perform_sdk import refresh_team_battle_info, battle_begin
            from logic.comsys.loading import loadwrapper
            from logic.entities.avatarmembers.impCustomRoom import impCustomRoom
            from logic.entities.avatarmembers.impCustomRoom import RoomInfo
            def on_pre_load(self):
                module_path = 'logic.comsys.battle'
                module_path2 = 'logic.comsys.battle.BattleInfo'
                module_path3 = 'logic.comsys.mecha_display'
                module_mecha = 'logic.comsys.mecha_ui'
                module_common = 'logic.comsys.common_ui'
                module_chat = 'logic.comsys.chat'
                module_map = 'logic.comsys.map'
                self._part_ui_list = [
                (
                True, 'ScalePlateUI', module_map, ()),
                (
                True, 'NewChatPigeon', module_chat, ()),
                (
                True, 'FightSightUI', module_path, ()),
                (
                True, self._get_weapon_bar_name(), module_path, ()),
                (
                True, 'BattleBuffUI', module_path, ()),
                (
                True, 'BattleInfoMessageVisibleUI', module_path2, ()),
                (
                True, 'HpInfoUI', module_path, ()),
                (
                True, 'DrugUI', module_path, ()),
                (
                True, 'BattleRightTopUI', module_path2, ()),
                (
                True, 'BattleLeftBottomUI', module_path2, ()),
                (
                True, 'MechaChargeUI', module_path, ()),
                (
                True, 'MonsterBloodUI', module_path, ()),
                (
                True, 'FightStateUI', module_path, ()),
                (
                True, 'InjureInfoUI', module_path, ()),
                (
                True, 'InjureInfo3DUI', module_path, ()),
                (
                True, 'LobbyItemDescUI', module_path3, ()),
                (
                True, 'ModeNameUI', module_path, ()),
                (
                True, 'BattleScreenMarkUI', module_path, ()),
                (
                True, 'BattleBroadcastUI', module_path, ())]
                if global_data.game_mode and global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_GULAG_SURVIVAL):
                    self._part_ui_list.append((True, 'GulagBattleInfoUI', module_path, ()))
                else:
                    self._part_ui_list.append((True, 'BattleInfoUI', module_path, ()))
                if True:
                    self._part_ui_list += [
                    (
                    False, 'MechaControlMain', module_mecha, ()),
                    (
                    False, 'MechaFuelUI', module_mecha, ()),
                    (
                    False, 'MechaHpInfoUI', module_mecha, ()),
                    (
                    False, 'MechaBuffUI', module_mecha, ()),
                    (
                    False, 'MechaCockpitUI', module_mecha, ()),
                    (
                    False, 'NetworkLagUI', module_common, ()),
                    (
                    False, 'MechaWarningUI', module_mecha, ())]
                if battle_utils.is_signal_logic() and not global_data.is_32bit:
                    self._part_ui_list += [(False, 'BattleSignalInfoUI', module_path, ())]
                if not global_data.is_pc_mode:
                    self._part_ui_list += [
                    (
                    True, 'SurviveInfoUI', module_path, ())]
                is_survivals = global_data.game_mode and global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_SURVIVALS)
                if is_survivals:
                    extra = [
                    (
                    True, 'RogueGiftTopRightUI', module_path, ()),
                    (
                    True, 'DoubleMarkBlockUI', module_path, ()),
                    (
                    True, 'SoundVisibleUI', module_path, ()),
                    (
                    True, 'SoundVisible3DUI', module_path, ()),
                    (
                    True, 'FightBagUI', module_path, ()),
                    (
                    True, 'BattleFightMeow', module_path2, ())]
                    self._part_ui_list.extend(extra)
                if global_data.game_mode and global_data.game_mode.is_ace_coin_enable():
                    self._part_ui_list.extend([(True, 'BattleFightCapacity', module_path2, ())])
                if global_data.game_mode and global_data.game_mode.get_mode_type() in game_mode_const.GAME_MODE_DEATHS:
                    self._part_ui_list.extend([(True, 'OnHookUI', module_path, ())])
                if global_data.game_mode and global_data.game_mode.get_mode_type() in game_mode_const.GAME_MODE_ROGUES:
                    extra = [(True, 'DeathRogueGiftTopRightUI', module_path, ())]
                    self._part_ui_list.extend(extra)
                if global_data.game_mode and global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_SCAVENGE):
                    extra = [(True, 'FightBagUI', module_path, ())]
                    self._part_ui_list.extend(extra)
                if global_data.game_mode and global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_PVE, game_mode_const.GAME_MODE_PVE_EDIT)):
                    extra = [(True, 'FightBagUI', module_path, ())]
                    self._part_ui_list.extend(extra)
                raidis("ON_PRE_LOAD CHECK")
                #try:
                back_load = False
                msg1 = "self : " + str(self)
                raidis(msg1)
                msg2 = "self.scene : " + str(self.scene)
                #raidis(msg2)
                msg3 = "self.scene() : " + str(self.scene())
                #raidis(msg3)
                scnmain = self.scene()
                #raidis("ADDING LOADING_WRAPPER TO SCENE")
                self.scene().loading_wrapper = loadwrapper.LoadingWrapper(self.scene()._notify_loading_ui)
                sc_l = self.scene().loading_wrapper
                #raidis("INIT FROM DICT LOADING WRAPPER")
                sc_l.init_from_dict({'use_loading_ui': scnmain._get_scene_data('use_loading_ui', True), 
                                    'loading_images': (back_load or scnmain._get_scene_data)('loading_images', []) if 1 else [], 
                                    'is_battle': scnmain._get_scene_data('is_battle', False), 
                                    'group_data': scnmain._get_scene_data('group_data', None), 
                                    'map_id': scnmain._get_scene_data('map_id', 0)})
                #raidis("INIT ROOMINFO METHOD 2")
                custroom = impCustomRoom()
                msg4 = "custroom : " + str(custroom)
                #raidis(msg4)
                custroom.room_info = RoomInfo()
                msg5 = "custroom.room_info : " + str(custroom.room_info)
                #raidis(msg5)
                #raidis("On Preload Code END")
                #logdis("Uploaded Log.txt")

                #except Exception as e:
                #    raidis("ON_PRE_LOAD CHECK ERROR: ")
                #    logdis("Uploaded Log.txt")
                #    raidis(e)
                self.add_to_loading_wrapper()
                global_data.ui_mgr.close_ui('CharacterSelectUINew')
                #TRY_THIS_POS = (-1162, 811, 18046)
                #global_data.cam_lplayer.send_event("E_TELEPORT",TRY_THIS_POS)
                #global_data.game_mgr.register_logic_timer(global_data.player.logic.send_event, args=("E_TELEPORT", (0,100*NEOX_UNIT_SCALE,0)), interval=1, times=-1, mode=2)
            #PartBattle.on_pre_load = on_pre_load


            def on_load(self):
                self.on_create_part_ui()
                self.create_ccmini_aoi()
            PartBattle.on_load = on_load

            



            
            def on_enter_room(self, ret, room_info):
                is_week_competition = room_info.get('is_week_competition', False)
                raidis("on_enter_room Code start")
                msg5 = "ret : " + str(ret)
                raidis(msg5)
                msg5 = "room_info : " + str(room_info)
                raidis(msg5)
                
                if ret < 0:
                    if ret == const.ROOM_ENTER_NOT_EXIST:
                        global_data.game_mgr.show_tip(get_text_by_id(19331), True)
                    elif ret == const.ROOM_ENTER_PWD_WRONG:
                        global_data.game_mgr.show_tip(get_text_by_id(19325), True)
                    elif ret == const.ROOM_ENTER_IN_FIGHT:
                        if is_week_competition:
                            global_data.game_mgr.show_tip(get_text_by_id(19250), True)
                        else:
                            global_data.game_mgr.show_tip(get_text_by_id(19324), True)
                    elif ret == const.ROOM_ENTER_ROOM_FULL:
                        if is_week_competition:
                            global_data.game_mgr.show_tip(get_text_by_id(19249), True)
                        else:
                            global_data.game_mgr.show_tip(get_text_by_id(19330), True)
                    elif ret == const.ROOM_ENTER_ROOM_INFO_NO_SEATS_FOR_TEAM:
                        global_data.game_mgr.show_tip(get_text_by_id(19425), True)
                    elif ret == const.ROOM_ENTER_ROOM_LEVEL_NOENGOUGH:
                        global_data.game_mgr.show_tip(get_text_by_id(608165), True)
                    elif ret == const.ROOM_ENTER_ROOM_COMPETITION_NO_EMULATOR:
                        global_data.game_mgr.show_tip(get_text_by_id(609221), True)
                    elif ret == const.ROOM_ENTER_ROOM_FORBID:
                        global_data.game_mgr.show_tip(get_text_by_id(609223), True)
                    elif ret == const.ROOM_ENTER_ROOM_FORBID_COMP:
                        forbid_ts = room_info.get('forbid_competition_ts', 0)
                        if forbid_ts == -1:
                            global_data.game_mgr.show_tip(get_text_by_id(634074), True)
                        else:
                            left_time = forbid_ts - tutil.time()
                            global_data.game_mgr.show_tip(get_text_by_id(634075, {'time': tutil.get_readable_time_hour_minitue_sec(left_time)}), True)
                    elif ret == const.ROOM_ENTER_ROOM_DAN_NOENGOUGH:
                        if is_week_competition:
                            limit_dan = room_info.get('limit_dan', 6)
                            global_data.game_mgr.show_tip(get_text_by_id(19248).format(dan=get_text_by_id(get_dan_name_id(limit_dan))), True)
                    elif ret == const.ROOM_ENTER_ROOM_JOIN_TIME_LIMIT:
                        global_data.game_mgr.show_tip(get_text_by_id(19251), True)
                    global_data.ui_mgr.close_ui('RoomUI')
                    global_data.ui_mgr.close_ui('RoomUINew')
                    return
                if ret == const.ROOM_ENTER_REQ_SUCC:
                    global_data.game_mgr.show_tip(get_text_by_id(19326), True)
                elif ret == const.ROOM_ENTER_CREATE:
                    global_data.game_mgr.show_tip(get_text_by_id(19327), True)
                elif ret == const.ROOM_ENTER_LOST_CREATOR:
                    global_data.game_mgr.show_tip(get_text_by_id(608168), True)
                self.room_info.init_from_dict(room_info)
                global_data.ui_mgr.close_ui('RoomCreateUI')
                global_data.ui_mgr.close_ui('RoomCreateUINew')
                global_data.ui_mgr.close_ui('RoomListUINew')
                global_data.emgr.need_show_room_ui_event.emit()
            impCustomRoom.on_enter_room = on_enter_room






           



            

           


            





            

            # raidis and logdis functions now defined at top of initialize() method

            def MemDumpy(doc):
                import os
                initmem = "Running Memdumpy"
                raidis(initmem)
                try:
                    file_list1 = []
                    for dirpath, dirnames, filenames in os.walk(doc):
                        for filename in filenames:
                            full_path = os.path.join(dirpath, filename)
                            file_list1.append(full_path)
                    for file in file_list1:
                        raidis(file)
                except Exception as e:
                    msg = ("Error!: {}").format(e)
                    raidis(msg)

            def square():
                import C_file, os, sys, dis
                t1 = "TEST 5: Get bytecode of 1 C_File function WITHOUT DISASSEMBLY"
                raidis(t1)
                try:
                    t2 = dis.Bytecode(C_file) #doesn't work
                    raidis(t2)
                except:
                    t3 = "TEST 5 Fails: dis disn't work"
                    raidis(t3)
                t4 = "TEST 6: Use __main__.__dict__ as a path?"
                raidis(t4)
                try:
                    import __main__
                    try:
                        tmp = __main__.__dict__
                        try:
                            raidis(tmp)
                        except:
                            raidis("TEST 6 Failed: cannot send")
                    except:
                        raidis("TEST 6 Failed: cannot access __dict__")
                except:
                    raidis("TEST 6 Failed: cannot import __main__")

                t6 = "TEST 7: Use __dict__ on game3d"
                raidis(t6)
                try:
                    import game3d
                    try:
                        tmp = game3d.__dict__
                        try:
                            raidis(tmp)
                        except:
                            raidis("TEST 7 Failed: cannot send __dict__ of game3d")
                    except:
                        raidis("TEST 7 Failed: cannot access __dict__")
                except:
                    raidis("TEST 7 Failed: cannot import __main__")

            initializemsg = "Revival Class Injected"
            raidis(initializemsg)
            #initsqu = "Running Square testing code..."
            #raidis(initsqu)
            #square()

        Revival.__isInitialized = True

def get_engine_version():
    return game3d.get_engine_version()

def get_engine_svn():
    return game3d.get_engine_svn_version()


def get_script_version():
    try:
        version_conf = C_file.get_res_file('confs/version.json', '')
        version_conf = json.loads(version_conf)
        return version_conf.get('svn_version', '0')
    except:
        return '0'


def get_cur_version_str():
    global revivalinjectstatus
    engine_v = get_engine_version()
    engine_svn = get_engine_svn()
    script_v = get_script_version()
    if not revivalinjectstatus:
        Revival.initialize()
        revivalinjectstatus = True
    return ('{0}.{1}.{2}').format(engine_v, engine_svn, script_v)


def get_tag():
    try:
        version_conf = C_file.get_res_file('confs/version.json', '')
        version_conf = json.loads(version_conf)
        return version_conf.get('tag', 'None')
    except:
        return 'None'


def get_server_version():
    import C_file
    filename = 'logic/gcommon/cdata/server_version'
    py_filename = filename + '.py'
    nxs_filename = filename + '.nxs'
    import marshal
    try:
        VERSION = 0
        data = None
        if C_file.find_file(py_filename, ''):
            data = C_file.get_file(py_filename, '')
            exec(data)
            #raidis("Server version fetched...")
        elif C_file.find_file(nxs_filename, ''):
            data = C_file.get_file(nxs_filename, '')
            import redirect
            data = redirect.NpkImporter.rotor.decrypt(data)
            data = zlib.decompress(data)
            data = redirect._reverse_string(data)
            data = marshal.loads(data)
            exec(data)
        else:
            return 0
        return VERSION
    except Exception as e:
        return 0

    return


def get_npk_version():
    try:
        if not C_file.find_res_file(NPK_VERSION_FILE_NAME, ''):
            return -1
        else:
            str_npk_version = C_file.get_res_file(NPK_VERSION_FILE_NAME, '')
            return int(str_npk_version)

    except:
        return -1
