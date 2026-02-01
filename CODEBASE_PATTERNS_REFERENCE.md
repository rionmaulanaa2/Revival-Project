# Codebase Patterns Reference Guide

## Overview
This document captures the proper patterns found in the revival project's script_patch and script_week folders for scene handling, file loading, function wrapping, and UI patching.

---

## 1. world.scene Usage Patterns

### Pattern A: Inheriting from world.scene
**Location**: `script_patch/609/11026820604907119192.py` (LoginScene)

```python
import world
from common.cfg import confmgr

class LoginScene(world.scene):
    """Login scene inherits from world.scene base class"""
    
    def __init__(self, scene_type, scene_data=None, callback=None, async_load=True, back_load=False):
        super(LoginScene, self).__init__()
        self.init_scene_info(scene_type, scene_data, callback)
        print('load scene id', id(self), scene_type)
        self.viewer_position = math3d.vector(0, 0, 0)
        self.tick_cnt = 0
        self.create_camera(True)
        self.load_scene(callback, async_load, back_load)
    
    def init_scene_info(self, scene_type, scene_data, callback):
        self.valid = True
        self.scene_type = scene_type
        self.scene_conf = confmgr.get('scenes', scene_type)
        self.scene_data = {} if scene_data is None else scene_data
        self._loaded = False
        self.parts = {}
        self.update_part_list = set()
        self.load_parts()
    
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
```

### Pattern B: Creating scene instances
**Location**: `script_patch/617/2654451385899978248.py` (AssetThumbRenderer)

```python
import world

# Create a bare scene instance
scene = world.scene()
scene.background_color = 0
scene.name = "MySceneName"

# Access scene's active camera
camera = scene.active_camera
```

### Pattern C: Using scene through Manager
**Location**: `script_patch/422/14606205992556332510.py` (Manager.do_load_scene)

```python
def do_load_scene(self, scene_type, scene_data, callback, async_load, back_load, release):
    """Manager handles scene loading with proper class selection"""
    scn_cls = None
    self._is_ingame_scene = False
    
    if scene_type in ('Main', 'Intro', 'MainHuawei'):
        from .vscene import login_scene
        scn_cls = login_scene.LoginScene
    else:
        from .vscene import scene
        scn_cls = scene.Scene
        self._is_ingame_scene = True
    
    # Delegate to external scene manager agent if available
    if global_data.ex_scene_mgr_agent:
        global_data.ex_scene_mgr_agent.do_load_scene(
            scn_cls, scene_type, scene_data, callback, async_load, back_load, release
        )
    else:
        self._naive_do_load_scene(
            scn_cls, scene_type, scene_data, callback, async_load, back_load
        )
```

### Pattern D: Scene has common attributes
```python
# Scene objects have these attributes:
scene.scene_type      # e.g., 'Main', 'Lobby', 'BattleMain'
scene.scene_data      # Dictionary of scene-specific data
scene.scene_conf      # Configuration from confmgr
scene.scene_col       # Collision system
scene.active_camera   # The current camera
scene.parts           # Dictionary of scene parts/components
scene._loaded         # Boolean flag for loaded state

# Scene objects have these methods:
scene.load(path, callback, async_load)     # Load scene from path
scene.load_env_new(xml_path)               # Load environment settings
scene.is_loaded()                          # Check if scene is loaded
scene.on_enter()                           # Called when entering scene
scene.on_exit()                            # Called when exiting scene
scene.destroy()                            # Cleanup scene resources
```

---

## 2. Scene Loading and Initialization Patterns

### Pattern A: Scene Manager load_scene method
**Location**: `script_patch/422/14606205992556332510.py`

```python
def load_scene(self, scene_type, scene_data=None, callback=None, 
               async_load=True, back_load=False, release=True):
    """Proper scene loading with deferred execution"""
    if self._is_exec:
        # If already executing, defer this load
        self.post_exec(self.do_load_scene, scene_type, scene_data, 
                      callback, async_load, back_load, release)
    else:
        # Execute immediately
        self.do_load_scene(scene_type, scene_data, callback, 
                          async_load, back_load, release)
```

### Pattern B: Scene unloading
**Location**: `script_patch/422/14606205992556332510.py`

```python
def unload_scene(self, is_exit=False):
    """Proper scene cleanup"""
    if self.scene:
        self.scene.on_exit()
        world.set_active_scene(None)
        if self.scene:
            self.scene.is_exit_destroy = is_exit
            self.scene.destroy()
            self.scene = None
```

### Pattern C: Scene reloading
```python
def reload_scene(self):
    """Reload current scene with same data"""
    if not self.scene:
        return
    old_scene_type = self.scene.scene_type
    old_scene_data = self.scene.scene_data
    self.post_exec(self.do_load_scene, old_scene_type, old_scene_data, 
                   None, True, False, True)
```

---

## 3. C_file.find_file Usage Patterns

### Pattern A: Check if file exists
**Location**: `script_patch/109/3268669426470549958.py` (Module loader)

```python
import C_file

def find_module_py(self, fullname, path=None):
    """Check for Python module files"""
    fullname = fullname.replace('.', '/')
    fullname_ext = fullname + '.py'
    pkg_name = fullname + '/__init__.py'
    
    for p in self._paths:
        # Check for package __init__.py
        if C_file.find_file(p + '/' + pkg_name, ''):
            return self
        # Check for module .py file
        if C_file.find_file(p + '/' + fullname_ext, ''):
            return self
    
    return None
```

### Pattern B: Load file after checking existence
**Location**: `script_patch/109/3268669426470549958.py`

```python
def load_module_py(self, fullname):
    """Load module file if it exists"""
    fullname = fullname.replace('.', '/')
    fullname_ext = fullname + '.py'
    pkg_name = fullname + '/__init__.py'
    path = ''
    is_pkg = False
    
    # Search for the file
    for p in self._paths:
        temp = p + '/' + pkg_name
        if C_file.find_file(temp, ''):
            path = temp
            is_pkg = True
            break
        temp = p + '/' + fullname_ext
        if C_file.find_file(temp, ''):
            path = temp
            is_pkg = False
            break
    
    # Load if found
    if path:
        self.check_login_redirect(path)
        data = C_file.get_file(path, '')  # Get file contents
        root_dir = game3d.get_script_path()
        import os
        data = compile(data, os.path.join(root_dir, path), 'exec')
        path = None
        if is_pkg:
            path = ['.']
        return C_file.new_module(mod_name, data, path)
    else:
        return None
```

### Pattern C: Check version file
**Location**: `script_patch/785/17524466876519882393.py` (version.py)

```python
def get_server_version():
    """Get server version from file, with fallback"""
    import C_file
    filename = 'logic/gcommon/cdata/server_version'
    py_filename = filename + '.py'
    nxs_filename = filename + '.nxs'
    
    try:
        VERSION = 0
        if C_file.find_file(py_filename, ''):
            # Load .py version
            data = C_file.get_file(py_filename, '')
            exec(data)
        elif C_file.find_file(nxs_filename, ''):
            # Load .nxs (compiled) version
            data = C_file.get_file(nxs_filename, '')
            # ... process compiled data
        else:
            return 0  # File not found - return default
        return VERSION
    except Exception as e:
        print('[Version] get_server_version except:', str(e))
        return 0  # Error - return safe default
```

### Pattern D: Check resource file existence
**Location**: `script_patch/259/10153562029345052269.py`

```python
# Check if a file exists in the file system
flist_exists = C_file.find_file('p_script_flist.txt', '')

if not flist_exists:
    print('[ERROR] File not found - taking appropriate action')
    return False

# Continue with file operations
```

---

## 4. File Loading Error Handling Patterns

### Pattern A: Try-except with fallback
**Location**: `script_patch/785/17524466876519882393.py`

```python
def get_script_version():
    """Get script version with error handling"""
    try:
        version_conf = C_file.get_res_file('confs/version.json', '')
        version_conf = json.loads(version_conf)
        return version_conf.get('svn_version', '0')
    except:
        return '0'  # Safe default on any error
```

### Pattern B: Graceful degradation
**Location**: `script_patch/1016/16725989236121328167.py` (PatchUI)

```python
def check_file_system(self):
    """Check filesystem with clear error messages"""
    print('check filesystem')
    print('find res file:', C_file.find_res_file('gui/template/login/login.json', ''))
    
    if not C_file.find_res_file('gui/template/login/login.json', ''):
        text_id = 90032
        try:
            print('start obb_analyze')
            check_res = patch_utils.obb_analyze()
            if check_res == patch_utils.OBB_CHECK_RES_FILE_NOT_EXIST:
                text_id = 90101
        except:
            pass
        
        # Show error dialog and exit gracefully
        print('warning t id', text_id)
        game3d.show_msg_box(get_patch_text_id(text_id), 
                           get_patch_text_id(90013), 
                           game3d.exit, None, 
                           get_patch_text_id(90013), 
                           get_patch_text_id(90003))
        return False
    
    return True
```

---

## 5. Function Wrapping/Decoration Patterns

### Pattern A: Store original and wrap with error handling
**Location**: `script_patch/785/785_17524466876519882393.py`

```python
# Hook C_file.find_file to handle missing scene environment maps
if hasattr(C_file, 'find_file'):
    orig_find_file = C_file.find_file  # Store original
    
    def _wrapped_find_file(path, tag=''):
        """Wrapped version with additional logic"""
        result = orig_find_file(path, tag)  # Call original
        
        if result != 1:
            # Check if it's a scene environment resource
            path_lower = path.lower()
            is_env_resource = any(pattern in path_lower for pattern in [
                '/probe/',           # Reflection probes
                '_irrad.sh',         # Irradiance spherical harmonics
                '_reflect.',         # Reflection maps
                'skybox_',           # Skybox resources
                '_content/',         # Scene content folders
            ])
            
            if is_env_resource and path not in _missing_scene_resources:
                _missing_scene_resources.add(path)
                raidis('[SceneFix] Missing env resource (using fallback): %s' % path[:100])
        
        return result
    
    C_file.find_file = _wrapped_find_file  # Replace with wrapper
```

### Pattern B: Wrap with exception recovery
**Location**: `script_patch/785/785_17524466876519882393.py`

```python
# Patch world.scene.load to handle errors gracefully
if hasattr(world, 'scene') and hasattr(world.scene, 'load'):
    orig_scene_load = world.scene.load
    
    def _wrapped_scene_load(*args, **kwargs):
        try:
            return orig_scene_load(*args, **kwargs)
        except Exception as e:
            error_str = str(e)
            # If error is about missing probe/irradiance files, return success anyway
            if any(keyword in error_str.lower() for keyword in 
                   ['probe', 'irrad', 'skybox', 'sh not found']):
                raidis('[SceneFix] Scene load continued despite missing env map: %s' % error_str[:150])
                return True  # Scene loaded despite missing environment map
            else:
                raise  # Re-raise non-environment errors
    
    world.scene.load = _wrapped_scene_load
```

### Pattern C: Wrap method on class instance
**Location**: `script_patch/785/785_17524466876519882393.py`

```python
from logic.gcommon.component.client.com_camera.ComStateTrkCam import ComStateTrkCam

# Wrap cancel_trk_with_check
if hasattr(ComStateTrkCam, 'cancel_trk_with_check'):
    orig_cancel_trk_with_check = ComStateTrkCam.cancel_trk_with_check
    
    def cancel_trk_with_check_wrapper(self, *args, **kwargs):
        try:
            return orig_cancel_trk_with_check(self, *args, **kwargs)
        except TypeError as e:
            if 'positional arguments' in str(e):
                return None  # Gracefully handle signature mismatch
            raise
    
    ComStateTrkCam.cancel_trk_with_check = cancel_trk_with_check_wrapper
```

### Pattern D: Stub out unwanted functionality
**Location**: `script_patch/785/785_17524466876519882393.py`

```python
try:
    from logic.comsys.loading.PatchUI import PatchUI
    
    if hasattr(PatchUI, 'show_patch_update_dialog'):
        original_show = PatchUI.show_patch_update_dialog
        
        def _stub_show_dialog(self, *args, **kwargs):
            # Don't show version update dialogs
            raidis('[VersionFix] Version update dialog suppressed')
            return None
        
        PatchUI.show_patch_update_dialog = _stub_show_dialog
        raidis('[VersionFix] PatchUI.show_patch_update_dialog disabled')
except Exception as e:
    raidis('[VersionFix] PatchUI patch failed: %s' % e)
```

---

## 6. UI Patching Patterns

### Pattern A: PatchUI class structure
**Location**: `script_patch/1016/16725989236121328167.py`

```python
class PatchUI(object):
    instance = None  # Singleton pattern
    
    def __init__(self, finished_callback):
        super(PatchUI, self).__init__()
        six.moves.builtins.__dict__['PATCH_UI_INSTANCE'] = self
        
        # Store platform info
        self._platform_name = game3d.get_platform()
        self._npk_version = version.get_npk_version()
        
        # Initialize
        if not self.check_file_system():
            return
        
        self.finished_callback = finished_callback
        self.widget = None
        self.valid = True
        
        # ... more initialization
        
        PatchUI.instance = self  # Set singleton
```

### Pattern B: Version check UI patterns
**Location**: `script_patch/785/785_17524466876519882393.py`

```python
# Disable version check on startup
try:
    from logic.vscene.VersionCheckUI import VersionCheckUI
    
    if hasattr(VersionCheckUI, 'start_version_check'):
        original_version_check = VersionCheckUI.start_version_check
        
        def _stub_version_check(self, *args, **kwargs):
            # Skip version checking
            raidis('[VersionFix] Version check skipped')
            return None
        
        VersionCheckUI.start_version_check = _stub_version_check
        raidis('[VersionFix] VersionCheckUI.start_version_check disabled')
except Exception as e:
    raidis('[VersionFix] VersionCheckUI patch failed: %s' % e)
```

### Pattern C: ExtPatchUI class
**Location**: `script_patch/330/11323302825905596416.py`

```python
class ExtPatchUI(object):
    """Extended patch UI for additional package management"""
    
    def __init__(self):
        super(ExtPatchUI, self).__init__()
        # Initialization logic
```

---

## 7. Scene Method Wrapping (Alternative to Direct Patching)

### Pattern A: Wrap scene's on_load method
**Location**: `script_patch/785/785_17524466876519882393.py`

```python
try:
    from logic.vscene import scene as scene_module
    
    # Suppress space object type errors in scene loading
    if hasattr(scene_module, 'Scene'):
        Scene = scene_module.Scene
        
        if hasattr(Scene, 'on_load'):
            orig_scene_on_load = Scene.on_load
            
            def _wrapped_scene_on_load(self, *args, **kwargs):
                try:
                    return orig_scene_on_load(self, *args, **kwargs)
                except Exception as e:
                    error_str = str(e).lower()
                    if any(keyword in error_str for keyword in 
                           ['unknown space object', 'road', 'mapping table']):
                        raidis('[SceneFix] Scene loaded despite space object error: %s' % str(e)[:150])
                        return True  # Continue loading
                    raise
            
            Scene.on_load = _wrapped_scene_on_load
except ImportError:
    pass
```

### Pattern B: Wrap scene object methods
**Location**: `script_patch/785/785_17524466876519882393.py`

```python
# Hook scene loading to suppress "Unknown space object type" errors
if hasattr(world.scene, 'get_space_obj_by_id'):
    orig_get_space_obj = world.scene.get_space_obj_by_id
    
    def _wrapped_get_space_obj(*args, **kwargs):
        try:
            return orig_get_space_obj(*args, **kwargs)
        except Exception as e:
            error_str = str(e).lower()
            if 'unknown space object type' in error_str or 'road' in error_str:
                # Return None for unknown types like "Road" - they're non-critical
                raidis('[SceneFix] Suppressed unknown space object error: %s' % str(e)[:120])
                return None
            raise
    
    world.scene.get_space_obj_by_id = _wrapped_get_space_obj
```

### Pattern C: Hook camera preset loading with fallback
```python
# Hook camera preset loading to provide fallback for missing presets
if hasattr(world.scene, 'get_preset_camera'):
    orig_get_preset_camera = world.scene.get_preset_camera
    
    def _wrapped_get_preset_camera(camera_name):
        try:
            result = orig_get_preset_camera(camera_name)
            if result is None:
                # Return identity matrix for missing camera presets
                raidis('[SceneFix] Using identity matrix for missing camera: %s' % camera_name)
            return result
        except Exception as e:
            # Return None to trigger default identity matrix
            raidis('[SceneFix] Camera preset error, using fallback: %s' % str(e)[:120])
            return None
    
    world.scene.get_preset_camera = _wrapped_get_preset_camera
```

---

## 8. Best Practices Summary

### Function Wrapping Strategy
1. **Always store the original function** before replacing
2. **Use try-except blocks** in wrappers for error recovery
3. **Call the original function** from within the wrapper
4. **Provide fallback behavior** for known error cases
5. **Re-raise unexpected errors** that shouldn't be suppressed
6. **Log all interventions** for debugging

### File Loading Strategy
1. **Always check file existence** before attempting to load
2. **Provide default values** when files are missing
3. **Use try-except blocks** around file operations
4. **Return safe defaults** on errors rather than crashing
5. **Log errors clearly** for debugging

### Scene Patching Strategy
1. **Wrap methods rather than replacing attributes** when possible
2. **Use hasattr checks** before accessing attributes
3. **Import inside try-except blocks** to handle missing modules
4. **Provide fallback behavior** for non-critical scene resources
5. **Don't modify world.scene directly** - wrap its methods instead

### Error Handling Strategy
1. **Catch specific exceptions** when possible (TypeError, ImportError, etc.)
2. **Always provide context** in error messages
3. **Truncate long error messages** to avoid log spam
4. **Use graceful degradation** - continue with reduced functionality
5. **Don't crash on non-critical errors** - log and continue

---

## 9. Common Patterns to AVOID

### ❌ DON'T: Modify class attributes directly
```python
# BAD - fragile and can cause issues
world.scene.some_attribute = new_value
```

### ✅ DO: Wrap methods instead
```python
# GOOD - preserves original behavior, adds new functionality
orig_method = world.scene.some_method
def wrapped_method(*args, **kwargs):
    # Your logic here
    return orig_method(*args, **kwargs)
world.scene.some_method = wrapped_method
```

### ❌ DON'T: Assume files exist
```python
# BAD - will crash if file doesn't exist
data = C_file.get_file('some/path.txt', '')
```

### ✅ DO: Check existence first
```python
# GOOD - handles missing files gracefully
if C_file.find_file('some/path.txt', ''):
    data = C_file.get_file('some/path.txt', '')
else:
    data = default_data  # Use fallback
```

### ❌ DON'T: Catch and suppress all exceptions blindly
```python
# BAD - hides real problems
try:
    some_operation()
except:
    pass
```

### ✅ DO: Catch specific exceptions and log
```python
# GOOD - handles known issues, reveals unknown ones
try:
    some_operation()
except FileNotFoundError as e:
    log_error('File missing: %s' % e)
    use_fallback()
except Exception as e:
    log_error('Unexpected error: %s' % e)
    raise  # Re-raise if not handled
```

---

## 10. Key Takeaways

1. **world.scene** is a base class that scene types inherit from (LoginScene, Scene)
2. **Scene instances** have attributes like scene_type, scene_data, scene_conf, scene_col
3. **Scene loading** is managed through Manager.load_scene() and Manager.do_load_scene()
4. **C_file.find_file()** returns 1 if file exists, checks before loading with get_file()
5. **Function wrapping** preserves original behavior while adding new functionality
6. **Error handling** uses try-except with specific exception types and fallback values
7. **PatchUI exists** at `script_patch/1016/16725989236121328167.py` for update UI
8. **Version check UIs** can be found and stubbed out to disable update prompts
9. **Always wrap, never replace** - wrapping preserves compatibility
10. **Log all patches** with clear messages for debugging and verification
