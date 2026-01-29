# Version/Update Notification Mechanisms - Comprehensive Search Results

**Search Completed:** script_patch/ and script_week/ folders  
**Date:** January 28, 2026

---

## Executive Summary

This document contains findings on client version update notification code, version checking mechanisms, and related UI/dialog systems throughout the game client codebase.

---

## Primary Version Management System

### Core Version Functions
**Location:** [script_patch/785/785_17524466876519882393.py](script_patch/785/785_17524466876519882393.py)

#### Version Retrieval Functions (Lines 2569-2650)

```python
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
    filename = 'logic/gcommon/cdata/server_version'
    # Loads server version from py or nxs files
    # Returns VERSION = 0 on failure
    ...

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

**Key Variables:**
- `NPK_VERSION_FILE_NAME = 'npk_version.config'` (Line 7)
- Version config file: `confs/version.json`
- Server version file: `logic/gcommon/cdata/server_version`

---

## Patch/Update Checking System

### Extension Package Update Manager
**Location:** [script_patch/785/12120475367754979724.py](script_patch/785/12120475367754979724.py)

#### Version Patch Check Function (Lines 202-231)

This is the main update checking mechanism:

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
            cout_info(LOG_CHANNEL, 'old package, check and dl patch:{}'.format(ext_name))
            if check_local_ver_need_patch(ext_name):
                return True
        elif ext_name in active_ext_lst:
            if ext_name not in self._ext_ver_config:
                ext_ver = self._using_ext_config_dict[ext_name]['version']
            else:
                ext_ver = self._ext_ver_config[ext_name]
            cout_info(LOG_CHANNEL, 'using ext:{} ver:{} t_ver:{}'.format(ext_name, ext_ver, target_version))
            if int(ext_ver) < int(target_version):
                return True
        else:
            cout_info(LOG_CHANNEL, '{} no in using, skip patch'.format(ext_name))

    return False
```

**Call Location:** [Line 575](script_patch/785/12120475367754979724.py#L575)
```python
ext_need_patch_for_version_check = self._check_ext_need_patch()
if not ext_need_patch_for_version_check:
    cout_info(LOG_CHANNEL, 'no need ext patch for version')
```

---

## Update Notification UI System

### Patch UI Class - Update Confirmation Dialogs
**Location:** [script_patch/1016/16725989236121328167.py](script_patch/1016/16725989236121328167.py)  
**(Original Source: patch/patch_ui.py)**

#### Notification Dialog Function (show_confirm_box)

Usage Patterns (Lines 947, 970, 994, 1031, 1109, 1156, 1204, 1230, 1254, 1334):

```python
from .patch_utils import show_confirm_box, PATCH_UI_LAYER, normalize_widget

# Example notification call:
show_confirm_box(ok_cb, cc_cb, text, get_patch_text_id(90004), get_patch_text_id(90005))

# Pattern for permission dialogs:
show_confirm_box(confirm_go_to_setting, cancel_go_to_setting, 
                 get_patch_text_id(3112), 
                 get_patch_text_id(80284), 
                 get_patch_text_id(19002))
```

**Notification Mechanism Features:**
- Dialog displayed in `PATCH_UI_LAYER`
- Callbacks for OK/Cancel actions
- Text IDs from localization system
- Centralized through `patch_utils.show_confirm_box()`

---

## Red Point Notification System

### Mall Red Point Notification
**Location:** [script_patch/785/785_17524466876519882393.py#L980-L1040](script_patch/785/785_17524466876519882393.py#L980-L1040)

```python
def init_red_point(self):
    """Initialize red point system for mall notifications"""
    self.init_mall_redpoint_and_new()
    return None

def get_mall_red_point_info(self, category=None):
    """Get red point info (notification count) for mall"""
    if category:
        return self._mall_red_point_info.get(category, 0)
    return self._mall_red_point_info

def set_red_point(self, category, value):
    """Set red point value for a category"""
    self._mall_red_point_info[category] = value

def clear_all_red_points(self):
    """Clear all red point notifications"""
    for category in self._shop_categories:
        self._mall_red_point_info[category] = 0

def get_total_red_points(self):
    """Get total count of all red points"""
    return sum(self._mall_red_point_info.values())
```

**Related Functions:**
- `update_all_red_point()` [Line 1157, 1317](script_patch/785/785_17524466876519882393.py#L1157)
- `init_mall_redpoint_and_new()` [Line 980](script_patch/785/785_17524466876519882393.py#L980)

---

## Update Notification Dialog Locations

### show_confirm_box Usage in Patch Flow
**Location:** [script_patch/1016/16725989236121328167.py](script_patch/1016/16725989236121328167.py)

| Line | Purpose | Text ID |
|------|---------|---------|
| 947 | Download confirmation | 90004, 90005 |
| 970 | Settings dialog | 3112, 80284, 19002 |
| 994 | Download confirmation | 90004, 90005 |
| 1031 | Hint dialog | 90010, 90013 |
| 1109 | Generic dialog | 90010, 90013 |
| 1156 | Generic dialog | 90010, 90013 |
| 1204 | Download confirmation | 90004, 90005 |
| 1230 | Generic dialog | 90010, 90013 |
| 1254 | Download confirmation | 90004, 90005 |
| 1334 | Hint dialog | 90010, 90013 |

---

## Additional Update Dialog References

### Audio System Update
**Location:** [script_patch/698/15454690172617402547.py#L531](script_patch/698/15454690172617402547.py#L531)

```python
from patch.patch_utils import show_confirm_box

show_confirm_box(confirm_go_to_setting, cancel_go_to_setting, 
                 get_text_by_id(11017), 
                 get_text_by_id(80284), 
                 get_text_by_id(19002))
```

### Permission Dialog (CCMini Manager)
**Location:** [script_patch/903/1715884096419019473.py#L247](script_patch/903/1715884096419019473.py#L247)

```python
from patch.patch_utils import show_confirm_box

show_confirm_box(confirm_go_to_setting, cancel_go_to_setting, 
                 get_text_by_id(3119), 
                 get_text_by_id(80284), 
                 get_text_by_id(19002))
```

### Patch Utilities Dialogs
**Location:** [script_patch/330/11323302825905596416.py](script_patch/330/11323302825905596416.py)

Multiple notification calls:
- Line 325: Download prompt
- Line 329: Alternative download prompt  
- Line 647: General hint
- Line 663: Settings navigation

---

## Disabling/Hiding Notification Mechanisms

### Force Stop Update Download
**Location:** [script_patch/785/12120475367754979724.py#L82, L467, L1052](script_patch/785/12120475367754979724.py#L82)

```python
def stop_patch_downloader(self):
    self.force_stop = True
    self._ext_dl_agent.stop_download()
```

**Check Location:**
```python
if self.force_stop:
    # Skip processing
    ...
```

### Red Point Clearing
**Location:** [script_patch/785/785_17524466876519882393.py#L1030-L1032](script_patch/785/785_17524466876519882393.py#L1030)

```python
def clear_all_red_points(self):
    """Clear all red point notifications"""
    for category in self._shop_categories:
        self._mall_red_point_info[category] = 0
```

### Update Check Skipping Pattern
**Location:** [script_patch/785/12120475367754979724.py#L231](script_patch/785/12120475367754979724.py#L231)

```python
cout_info(LOG_CHANNEL, '{} no in using, skip patch'.format(ext_name))
# Automatically skips patch for inactive extensions
```

---

## Version Comparison Logic

### Integer-Based Version Comparison
**Location:** [script_patch/785/12120475367754979724.py#L215-L220](script_patch/785/12120475367754979724.py#L215)

```python
if int(ext_ver) < int(target_version):
    return True  # Update needed
return False      # No update needed
```

**Flow:**
1. Get local version from `ext_ver_config`
2. Compare with `target_version` (integer comparison)
3. Return True if local version is older
4. Triggers patch download if needed

---

## Configuration Files Referenced

| File | Purpose |
|------|---------|
| `confs/version.json` | Script version config |
| `confs/version.config` | Alternative version file |
| `npk_version.config` | NPK package version |
| `logic/gcommon/cdata/server_version` | Server version data |
| `confs/na_patch_bg_img_config.json` | NA region patch UI |
| `confs/patch_bg_img_config.json` | Standard patch UI |
| `confs/c_screen_adapt.json` | Screen adaptation settings |

---

## Text ID References for Notifications

| ID Range | Purpose |
|----------|---------|
| 90000-90150 | Patch UI messages |
| 3100-3120 | Permission messages |
| 80280-80290 | Common button labels |
| 11000-11020 | Audio system messages |

---

## Update Notification Flow

```
1. PatchUI.__init__() 
   ├─ check_file_system()
   ├─ init_widget()
   └─ start_logic()

2. ExtPackageManager._check_ext_need_patch()
   ├─ Load local version config
   ├─ Compare with target_version
   └─ Return True if update needed

3. ext_patch_info_analyze()
   ├─ If no patch needed: show_confirm_box()
   ├─ If patch needed: download_ext_npk_list()
   └─ Display progress dialog

4. Red Point Notifications
   ├─ init_red_point()
   ├─ get_mall_red_point_info()
   ├─ set_red_point()
   └─ clear_all_red_points()
```

---

## Summary of Key Mechanisms

### ✅ Version Checking
- **Multi-level versioning:** Engine, Script, Server, NPK
- **JSON configuration:** `confs/version.json`
- **Integer-based comparison:** `if int(local_ver) < int(target_ver)`

### ✅ Update Notifications
- **Primary system:** `show_confirm_box()` from patch_utils
- **Red point system:** Mall category notifications
- **Progress UI:** Patch UI layer with download progress

### ✅ Disabling/Hiding
- **Force stop:** `force_stop` flag and `stop_patch_downloader()`
- **Clear notifications:** `clear_all_red_points()` function
- **Skip inactive:** Automatic skip for non-active extensions

### ✅ Dialogs & Messages
- **Show confirm box:** Localized text IDs (90xxx range)
- **Permission dialogs:** Settings navigation (IDs 3100-3120)
- **Progress tracking:** Download speed, size, percentage

---

## Files Containing Version/Update Code

### script_patch Folder
- [785/785_17524466876519882393.py](script_patch/785/785_17524466876519882393.py) - **Core version functions**
- [785/12120475367754979724.py](script_patch/785/12120475367754979724.py) - **Patch checking & downloading**
- [1016/16725989236121328167.py](script_patch/1016/16725989236121328167.py) - **Patch UI with notifications**
- [330/11323302825905596416.py](script_patch/330/11323302825905596416.py) - **Patch utilities dialogs**
- [903/1715884096419019473.py](script_patch/903/1715884096419019473.py) - **Permission notifications**
- [698/15454690172617402547.py](script_patch/698/15454690172617402547.py) - **Audio update dialogs**

### script_week Folder
- Limited version/update specific code
- Mostly gameplay and battle mechanics

---

## Recommendations for Modification

If you need to **disable or hide** version update notifications:

1. **Prevent update checks:**
   - Set `self.force_stop = True` in ExtPackageManager
   - Modify `_check_ext_need_patch()` to always return False

2. **Hide red point notifications:**
   - Call `clear_all_red_points()` after initialization
   - Override `get_mall_red_point_info()` to return 0

3. **Skip confirmation dialogs:**
   - Modify `show_confirm_box()` to automatically accept
   - Or redirect calls to no-op functions

4. **Disable version retrieval:**
   - Modify version functions to return cached values
   - Override comparisons to skip version checking

---

**End of Report**
