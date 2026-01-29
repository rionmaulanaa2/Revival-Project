# Version/Update Notification Technical Reference

**Detailed Code Patterns & Mechanisms**

---

## 1. Core Version Functions

### Location: `script_patch/785/785_17524466876519882393.py` (Lines 2569-2650)

#### Function: `get_cur_version_str()`
```python
def get_cur_version_str():
    global revivalinjectstatus
    engine_v = get_engine_version()
    engine_svn = get_engine_svn()
    script_v = get_script_version()
    if not revivalinjectstatus:
        Revival.initialize()
        revivalinjectstatus = True
    return ('{0}.{1}.{2}').format(engine_v, engine_svn, script_v)
```
**Purpose:** Formats version string as "ENGINE.SVN.SCRIPT"  
**Used for:** Display and comparison

#### Function: `get_script_version()`
```python
def get_script_version():
    try:
        version_conf = C_file.get_res_file('confs/version.json', '')
        version_conf = json.loads(version_conf)
        return version_conf.get('svn_version', '0')
    except:
        return '0'
```
**Config:** `confs/version.json`  
**Fallback:** Returns '0' on error  
**Key Field:** `svn_version`

#### Function: `get_tag()`
```python
def get_tag():
    try:
        version_conf = C_file.get_res_file('confs/version.json', '')
        version_conf = json.loads(version_conf)
        return version_conf.get('tag', 'None')
    except:
        return 'None'
```
**Purpose:** Gets version tag/build identifier  
**Key Field:** `tag`

#### Function: `get_server_version()`
```python
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
            exec data
        elif C_file.find_file(nxs_filename, ''):
            data = C_file.get_file(nxs_filename, '')
            import redirect
            data = redirect.NpkImporter.rotor.decrypt(data)
            data = zlib.decompress(data)
            data = redirect._reverse_string(data)
            data = marshal.loads(data)
            exec data
        else:
            return 0
        return VERSION
    except Exception as e:
        return 0
```
**Purpose:** Fetch server-side version  
**Formats:** Python (.py) or NXS (encrypted/compressed)  
**Fallback:** Returns 0

#### Function: `get_npk_version()`
```python
def get_npk_version():
    try:
        if not C_file.find_res_file(NPK_VERSION_FILE_NAME, ''):
            return -1
        else:
            str_npk_version = C_file.get_res_file(NPK_VERSION_FILE_NAME, '')
            return int(str_npk_version)
    except:
        return -1
```
**File:** `npk_version.config`  
**Returns:** Integer version or -1 on error  
**Purpose:** Package resource version

---

## 2. Extension Package Version Checking

### Location: `script_patch/785/12120475367754979724.py`

#### Class: `ExtPackageManager`

**Constructor (Lines 44-80):**
```python
def __init__(self):
    self.state = ext_c.EXT_STATE_INIT
    self._lock = threading.Lock()
    self._ext_dl_agent = None
    self._valid_npk_list = []
    
    self._enable_patch_npk = patch_const.ENABLE_PATCH_NPK if hasattr(...) else game3d.is_feature_ready('PATCH_NPK_MERGE')
    self._support_ui_astc = not is_android_dds and IS_MOBILE and game3d.is_feature_ready('UI_ASTC')
    
    self._using_ext_info = ext_package_utils.get_using_ext_info()
    self._ext_package_config = ext_package_utils.get_ext_package_config_v2()
    self._is_real_ext_package = ext_package_utils.is_real_ext_package()
    
    self.server_config, self.ver_config = ext_package_utils.init_server_and_version_config()
    self.force_stop = False
    
    self._init_patch_info()
    self._init_ext_npk_file_verification_data()
    self._init_ext_patch_analyze_info()
```

#### Method: `_check_ext_need_patch()` (Lines 202-231)

**Full Implementation:**
```python
def _check_ext_need_patch(self):
    target_version = self._patch_target_version
    self._ext_ver_config = ext_package_utils.get_local_save_ext_version_config()

    def check_local_ver_need_patch(in_ext_name):
        if in_ext_name not in self._ext_ver_config:
            cout_info(LOG_CHANNEL, 'ext:{} has no local ver'.format(in_ext_name))
            return True
        ext_ver = self._ext_ver_config[in_ext_name]
        cout_info(LOG_CHANNEL, 'ext:{} ver:{} t_ver:{}'.format(in_ext_name, ext_ver, target_version))
        if int(ext_ver) < int(target_version):
            return True
        return False

    active_ext_lst = self.get_active_ext_name_lst()
    
    for ext_name in self._ext_package_config:
        if not self._is_real_ext_package:
            # Old package format
            cout_info(LOG_CHANNEL, 'old package, check and dl patch:{}'.format(ext_name))
            if check_local_ver_need_patch(ext_name):
                return True  # UPDATE NEEDED
        elif ext_name in active_ext_lst:
            # New package - check active extensions
            if ext_name not in self._ext_ver_config:
                ext_ver = self._using_ext_config_dict[ext_name]['version']
            else:
                ext_ver = self._ext_ver_config[ext_name]
            
            cout_info(LOG_CHANNEL, 'using ext:{} ver:{} t_ver:{}'.format(ext_name, ext_ver, target_version))
            
            if int(ext_ver) < int(target_version):
                return True  # UPDATE NEEDED
        else:
            # Extension not in use
            cout_info(LOG_CHANNEL, '{} no in using, skip patch'.format(ext_name))

    return False  # NO UPDATE NEEDED
```

**Key Logic:**
- Uses integer comparison: `int(ext_ver) < int(target_version)`
- Three package types: old, new with extension, new without extension
- `force_stop` flag can halt updates

#### Method: `stop_patch_downloader()` (Line 467)

```python
def stop_patch_downloader(self):
    self.force_stop = True
    self._ext_dl_agent.stop_download()
```

**Effect:** 
- Sets `force_stop = True`
- Stops active download agent
- Skips further patch processing (checked at line 1052)

#### Method: `ext_patch_info_analyze()` (Lines 571-600)

```python
def ext_patch_info_analyze(self, cb):
    self._init_ext_patch_analyze_info()
    self.set_state(ext_c.EXT_STATE_PATCH_INFO_ANALYZE)
    self._ext_patch_analyze_callback = cb
    
    if not self._check_ext_patch_npk():
        self._drpf('ExtMgr_PATCH_1', {'msg': 'check ext patch npk error'})
        self.ext_patch_info_analyze_callback(ext_c.EXT_STATE_PATCH_DL_FLIST_FAILED)
        return
    
    if not self._patch_list:
        self._drpf('ExtMgr_PATCH_1_0', {'msg': 'no patch list'})
        self.ext_patch_info_analyze_callback(ext_c.EXT_STATE_PATCH_INFO_ANALYZE_FINISH)
        return
    
    ext_need_patch_for_version_check = self._check_ext_need_patch()
    
    if not ext_need_patch_for_version_check:
        # NO UPDATE NEEDED
        cout_info(LOG_CHANNEL, 'no need ext patch for version')
        self._drpf('ExtMgr_PATCH_1_1', {'msg': 'no need ext patch for version'})
        self.ext_patch_analyze_info_progress = 1.0
        
        if self._enable_patch_npk:
            from .ext_pn_utils import insert_ext_npk_loader
            ret = insert_ext_npk_loader()
            if not ret:
                cout_error(LOG_CHANNEL, 'insert ext patch npk for version failed')
                self.ext_patch_info_analyze_callback(ext_c.EXT_STATE_PATCH_DL_FLIST_FAILED)
            else:
                self.ext_patch_info_analyze_callback(ext_c.EXT_STATE_PATCH_INFO_ANALYZE_FINISH)
        else:
            self.ext_patch_info_analyze_callback(ext_c.EXT_STATE_PATCH_INFO_ANALYZE_FINISH)
        return
    
    else:
        # UPDATE NEEDED - download patches
        target_version = self._patch_target_version
        target_flist_md5 = self._patch_list[0].filelist_md5
        filelist_data = patch_utils.get_temp_flist_data(target_version, target_flist_md5)
        
        if not filelist_data:
            # Download filelist
            cout_error(LOG_CHANNEL, 'local has no flist:{} then download'.format(target_version))
            self._drpf('ExtMgr_PATCH_1_2', {'msg': 'local has no flist:{} then download'.format(target_version)})
            flist_url = self._get_flist_url(self._patch_list[0].url)
```

---

## 3. Patch UI Notification System

### Location: `script_patch/1016/16725989236121328167.py` (patch_ui.py)

#### Class: `PatchUI`

**Constructor (Lines 32-60):**
```python
class PatchUI(object):
    instance = None

    def __init__(self, finished_callback):
        super(PatchUI, self).__init__()
        six.moves.builtins.__dict__['PATCH_UI_INSTANCE'] = self
        self._platform_name = game3d.get_platform()
        self._npk_version = version.get_npk_version()
        
        if not self.check_file_system():
            return
        
        self.init_android_priority()
        self.init_data()
        self.network_confirm = False
        self.patch_confirm = False
        
        try:
            patch_utils.init_wretched_config()
        except Exception as e:
            print('Except: init wretched config:', str(e))
        
        self.finished_callback = finished_callback
        self.use_orbit = False
        self.widget = None
        self.valid = True
        self._npk_dl_retry_count = 0
        self._npk_add_retry_count = 0
        self._support_astc = True
        self._support_ui_astc = True
        self._support_completion_npk = True
        self._init_package_property()
```

#### Method: `check_file_system()` (Lines 168-187)

```python
def check_file_system(self):
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
        
        print('warning t id', text_id)
        # ERROR DIALOG
        game3d.show_msg_box(
            get_patch_text_id(text_id), 
            get_patch_text_id(90013), 
            game3d.exit, None, 
            get_patch_text_id(90013), 
            get_patch_text_id(90003)
        )
        return False
    else:
        print('find npk_version file:', C_file.find_res_file('npk_version.config', ''))
        self._npk_version = version.get_npk_version()
        
        if self._npk_version == -2:
            patch_utils.send_script_error('get_npk_version_except')
            game3d.show_msg_box(
                get_patch_text_id(90101), 
                get_patch_text_id(90013), 
                game3d.exit, None, 
                get_patch_text_id(90013), 
                get_patch_text_id(90003)
            )
            return False
        return True
```

#### Method: `start_download_patch()` (Lines 1003-1050)

```python
def start_download_patch(self):
    patch_size = self.downloader.get_patch_size()
    self.download_start_time = time.time()
    self.init_prog_ui()

    def ok_cb():
        upload_info = {'BEGIN_DL_PATCH': 'size:{}'.format(patch_size)}
        patch_dctool.get_dctool_instane().send_patch_process_info_info(upload_info)
        self.downloader.download_patch_files(self.on_download_patch_finished)
        self.rec_patch_download_info(self.reach_ui_time, self.download_start_time, 
                                     self.download_start_time, 0)

    def cc_cb():
        upload_info = {
            'stage': 'download patch',
            'info': 'player cancel download patch because of no space'
        }
        patch_dctool.get_dctool_instane().send_patch_process_info_info(upload_info)
        game3d.exit()

    ignore_space_check = six.moves.builtins.__dict__.get('IGNORE_PATCH_SPACE_CHECK', False)
    need_remind_space = False
    
    if self._platform_name == game3d.PLATFORM_ANDROID and hasattr(game3d, 'get_available_memory'):
        try:
            available_memory = game3d.get_available_memory()
            patch_size_m = patch_size * 1.0 / 1024.0 / 1024.0
            
            if available_memory - 20 < patch_size_m:
                process_info = {
                    'stage': 'download patch',
                    'info': 'no enough space, has:{}, need:{}'.format(available_memory, patch_size_m)
                }
                patch_dctool.get_dctool_instane().send_patch_process_info_info(process_info)
                need_remind_space = True
        except:
            pass
    
    # Show confirmation dialog if needed
    if need_remind_space and not ignore_space_check:
        # SHOW CONFIRM BOX
        show_confirm_box(ok_cb, cc_cb, text, get_patch_text_id(90004), get_patch_text_id(90005))
    else:
        ok_cb()
```

---

## 4. Red Point Notification System

### Location: `script_patch/785/785_17524466876519882393.py` (Lines 980-1065)

#### Initialization
```python
self._mall_red_point_info = {}
self._red_point_data = {}

# Initialize categories
for category in self._shop_categories:
    self._mall_red_point_info[category] = 0
```

#### Core Methods

**init_red_point():**
```python
def init_red_point(self):
    """Initialize red point system for mall notifications"""
    self.init_mall_redpoint_and_new()
    return None
```

**get_mall_red_point_info():**
```python
def get_mall_red_point_info(self, category=None):
    """Get red point info (notification count) for mall"""
    if category:
        return self._mall_red_point_info.get(category, 0)
    return self._mall_red_point_info
```

**set_red_point():**
```python
def set_red_point(self, category, value):
    """Set red point value for a category"""
    self._mall_red_point_info[category] = value
```

**clear_all_red_points():**
```python
def clear_all_red_points(self):
    """Clear all red point notifications"""
    for category in self._shop_categories:
        self._mall_red_point_info[category] = 0
```

**get_total_red_points():**
```python
def get_total_red_points(self):
    """Get total count of all red points"""
    return sum(self._mall_red_point_info.values())
```

#### Reference Methods
- `update_all_red_point()` [Lines 1157, 1317] - Updates all red points
- `init_mall_redpoint_and_new()` [Line 980] - Initializes red points and new item markers

---

## 5. Notification UI Reference

### Confirm Box Dialog Pattern

**Import:**
```python
from .patch_utils import show_confirm_box, PATCH_UI_LAYER, normalize_widget
```

**Usage Pattern:**
```python
def callback_ok():
    # User clicked OK
    ...

def callback_cancel():
    # User clicked Cancel
    ...

text = get_patch_text_id(TEXT_ID)
ok_button_text = get_patch_text_id(OK_TEXT_ID)
cancel_button_text = get_patch_text_id(CANCEL_TEXT_ID)

show_confirm_box(callback_ok, callback_cancel, text, ok_button_text, cancel_button_text)
```

### Common Text IDs

| ID Range | Usage |
|----------|-------|
| 90000-90010 | Basic patch UI text |
| 90013 | "Cancel" button |
| 90004 | OK/Accept button |
| 90005 | Cancel/Decline button |
| 3112 | Settings prompt |
| 80284 | "OK" text |
| 19002 | "Cancel" text |

---

## 6. State Machine & Flow

### Patch States
```python
EXT_STATE_INIT = 0
EXT_STATE_DOWNLOAD_NPK_LIST = 1
EXT_STATE_VERIFYING_EXT_NPK = 2
EXT_STATE_DL_MISSING_EXT_NPK = 3
EXT_STATE_PATCH_DOWNLOADING = 4
EXT_STATE_PATCH_INFO_ANALYZE = 5
EXT_STATE_PATCH_COPYING = 6
EXT_STATE_PATCH_NPK_UPDATE = 7
EXT_STATE_PATCH_NPK_VERIFY = 8
```

### Version Check Flow

```
1. PatchUI.init_widget()
   └─ PatchUI.start_logic()
      └─ ExtPackageManager.ext_patch_info_analyze()
         └─ ExtPackageManager._check_ext_need_patch()
            ├─ Load local version config
            ├─ Get active extensions list
            ├─ For each extension:
            │  ├─ Compare: int(local_ver) < int(target_ver)
            │  └─ Return True if update needed
            └─ Call callback with result

2. If Update Needed:
   ├─ Download filelist
   ├─ Analyze patch info
   ├─ Show progress UI
   ├─ Download patches
   └─ Copy/update files

3. If No Update Needed:
   └─ Skip to game start
```

---

## 7. Disabling Mechanisms

### Method 1: Force Stop Download
```python
ext_mgr = get_ext_package_instance()
ext_mgr.force_stop = True
ext_mgr.stop_patch_downloader()
```

### Method 2: Override Check Function
```python
def _check_ext_need_patch(self):
    return False  # Always skip updates
```

### Method 3: Clear Notifications
```python
mall_mgr.clear_all_red_points()  # Clear all red dots
mall_mgr.set_red_point(category, 0)  # Clear specific category
```

### Method 4: Skip Dialog
```python
# Override show_confirm_box to auto-accept
def show_confirm_box(ok_cb, cancel_cb, *args):
    ok_cb()  # Auto-call OK callback
```

---

## Configuration & Constants

### Extension Package Constants (ext_package_const.py)
```python
EXT_PATCH_LIST_NAME = 'ext_patch_list'
EXT_VERSION_PATH = 'ext_version'
LOCAL_SAVED_EXT_FLIST_PATTERN = 'local_saved_ext_flist_{}'
EXTEND_FOLDER = 'extend'
EXT_NPK_LOADER_TAG = 'ext_tag'
```

### Patch Constants (patch_const.py)
```python
ENABLE_PATCH_NPK = True/False
CHUNK_SIZE = buffer size for MD5 verification
```

---

## Error Handling

### Try-Catch Patterns

**Version Loading:**
```python
try:
    version_conf = C_file.get_res_file('confs/version.json', '')
    version_conf = json.loads(version_conf)
    return version_conf.get('svn_version', '0')
except:
    return '0'  # Safe fallback
```

**NPK Verification:**
```python
try:
    m = hashlib.md5()
    with open(npk_path, 'rb') as tmp_file:
        file_buffer = tmp_file.read(CHUNK_SIZE)
        while file_buffer:
            self._ext_npk_checked_size += len(file_buffer)
            m.update(file_buffer)
            file_buffer = tmp_file.read(CHUNK_SIZE)
    
    if str(m.hexdigest()) == npk_md5:
        self._valid_npk_list.append(tmp_npk_name)
    else:
        invalid_list.append(tmp_npk_name)
        os.remove(npk_path)
except Exception as e:
    self._err_log('verify ext npk md5 with exception:{}'.format(str(e)))
    invalid_list.append(tmp_npk_name)
```

---

**End of Technical Reference**
