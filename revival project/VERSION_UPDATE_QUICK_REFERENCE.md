# Version/Update Notification - Quick Reference Guide

**Fast lookup for version checking and update notification mechanisms**

---

## 📍 Key Files at a Glance

| File | Purpose | Lines |
|------|---------|-------|
| `script_patch/785/785_17524466876519882393.py` | **VERSION FUNCTIONS** | 2569-2650 |
| `script_patch/785/12120475367754979724.py` | **PATCH CHECKING** | 202-231 |
| `script_patch/1016/16725989236121328167.py` | **PATCH UI DIALOGS** | 947, 970, 994, 1031 |
| `script_patch/785/785_17524466876519882393.py` | **RED POINT NOTIFICATIONS** | 980-1065 |

---

## 🔍 Version Functions Quick Reference

### Get Current Version String
```python
from version import get_cur_version_str
version_str = get_cur_version_str()  # Returns: "ENGINE.SVN.SCRIPT"
```

### Get Individual Versions
```python
from version import (
    get_engine_version(),      # Engine version number
    get_engine_svn(),          # Engine SVN revision
    get_script_version(),      # Script SVN version from confs/version.json
    get_tag(),                 # Build tag from confs/version.json
    get_server_version(),      # Server version from logic/gcommon/cdata/server_version
    get_npk_version()          # NPK package version from npk_version.config
)
```

### Get Version Config
```python
import json
import C_file

# Get full version config
version_conf = C_file.get_res_file('confs/version.json', '')
version_conf = json.loads(version_conf)

# Access fields
svn_version = version_conf.get('svn_version', '0')
tag = version_conf.get('tag', 'None')
```

---

## ⚙️ Update Check Logic

### Check if Update Needed
```python
from ext_package.ext_package_manager import get_ext_package_instance

ext_mgr = get_ext_package_instance()
needs_update = ext_mgr._check_ext_need_patch()

if needs_update:
    print("Update available!")
else:
    print("Already up to date")
```

### Version Comparison Algorithm
```python
local_version = 12345
target_version = 12346

if int(local_version) < int(target_version):
    # Update needed
    pass
```

### Skip Update Check
```python
ext_mgr.force_stop = True
ext_mgr.stop_patch_downloader()
```

---

## 🔔 Notification Systems

### Show Confirmation Dialog
```python
from patch.patch_utils import show_confirm_box
from patch.patch_lang import get_patch_text_id

def on_user_accept():
    print("User accepted")
    # Start download

def on_user_cancel():
    print("User cancelled")
    # Exit or skip

show_confirm_box(
    on_user_accept,
    on_user_cancel,
    get_patch_text_id(90004),  # Dialog message
    get_patch_text_id(90004),  # OK button text
    get_patch_text_id(90005)   # Cancel button text
)
```

### Red Point Notifications

#### Initialize Red Points
```python
mall_mgr.init_red_point()
```

#### Get Red Point Count
```python
# Get all red points
all_points = mall_mgr.get_mall_red_point_info()

# Get specific category
category_points = mall_mgr.get_mall_red_point_info('shop_weapons')

# Get total count
total = mall_mgr.get_total_red_points()
```

#### Set Red Point
```python
mall_mgr.set_red_point('shop_weapons', 5)  # Show 5 red dots
```

#### Clear Red Points
```python
# Clear all
mall_mgr.clear_all_red_points()

# Clear specific
mall_mgr.set_red_point('shop_weapons', 0)
```

---

## 📋 Configuration Files

| File | Contains |
|------|----------|
| `confs/version.json` | Script version & tag |
| `confs/version.config` | Alternative version |
| `npk_version.config` | NPK package version |
| `logic/gcommon/cdata/server_version` | Server version (py or nxs) |

### Example version.json
```json
{
    "svn_version": "12345",
    "tag": "v1.2.3-release"
}
```

---

## 🎯 Common Text IDs

| ID | Text |
|----|------|
| 90001 | "Title" |
| 90003 | "Close" |
| 90004 | "OK" / "Confirm" |
| 90005 | "Cancel" / "Decline" |
| 90013 | "Cancel" |
| 3112 | Settings/permission message |
| 80284 | "OK" |
| 19002 | "Cancel" |

---

## 🚫 Disable Update Notifications

### Method 1: Prevent Update Check
```python
# In ExtPackageManager
ext_mgr = get_ext_package_instance()
ext_mgr.force_stop = True
```

### Method 2: Override Version Check
```python
# Monkey patch - Always return False
def _check_ext_need_patch(self):
    return False

ExtPackageManager._check_ext_need_patch = _check_ext_need_patch
```

### Method 3: Auto-Accept Dialogs
```python
# Monkey patch - Auto-click OK
def show_confirm_box_override(ok_cb, cancel_cb, *args, **kwargs):
    ok_cb()

patch_utils.show_confirm_box = show_confirm_box_override
```

### Method 4: Clear All Notifications
```python
mall_mgr.clear_all_red_points()
```

---

## 📊 State Machine Quick View

```
PatchUI.init_widget()
    ↓
PatchUI.start_logic()
    ↓
ExtPackageManager.ext_patch_info_analyze()
    ↓
ExtPackageManager._check_ext_need_patch()
    ├─→ Needs Update → Show Dialog → Download
    └─→ No Update → Skip to Game Start
```

---

## 🔐 Version Sources (Priority Order)

1. **Local Cache:** `_ext_ver_config`
2. **Active Extensions:** `_using_ext_config_dict`
3. **Config File:** `confs/version.json`
4. **Server:** `logic/gcommon/cdata/server_version`
5. **Fallback:** Returns '0' or -1

---

## 🎨 UI Layers & Constants

```python
PATCH_UI_LAYER = 100  # Patch UI z-order
```

### PatchUI States
- `EXT_STATE_INIT` - Initializing
- `EXT_STATE_DOWNLOADING` - Downloading updates
- `EXT_STATE_ANALYZING` - Analyzing files
- `EXT_STATE_VERIFYING` - Verifying checksums

---

## 💾 Important Variables

| Variable | Purpose |
|----------|---------|
| `self._patch_target_version` | Target version to update to |
| `self._ext_ver_config` | Local version configuration |
| `self.force_stop` | Stop download flag |
| `self._valid_npk_list` | List of verified NPK files |
| `self._mall_red_point_info` | Red point notification counts |

---

## ✅ Common Operations Cheat Sheet

### Check if update available
```python
ext_mgr = get_ext_package_instance()
if ext_mgr._check_ext_need_patch():
    # Show update available message
    pass
```

### Get version for display
```python
from version import get_cur_version_str
display_text = "Version: " + get_cur_version_str()
```

### Disable notifications
```python
# Disable red point
mall_mgr.clear_all_red_points()

# Disable update check
ext_mgr.force_stop = True
```

### Show custom dialog
```python
from patch.patch_utils import show_confirm_box
from patch.patch_lang import get_patch_text_id

show_confirm_box(
    lambda: print("Accept"),
    lambda: print("Cancel"),
    "Custom message",
    "OK",
    "Cancel"
)
```

---

## 🐛 Debugging Tips

### Check Version Loaded
```python
import version
print("Script version:", version.get_script_version())
print("Current version:", version.get_cur_version_str())
print("NPK version:", version.get_npk_version())
```

### Check Update Status
```python
ext_mgr = get_ext_package_instance()
print("Force stop:", ext_mgr.force_stop)
print("Patch target version:", ext_mgr._patch_target_version)
print("Local version config:", ext_mgr._ext_ver_config)
```

### Check Red Points
```python
mall_mgr = get_mall_manager()
print("All red points:", mall_mgr.get_mall_red_point_info())
print("Total notifications:", mall_mgr.get_total_red_points())
```

---

## 📚 Related Modules

```python
# Version system
from version import *

# Patch manager
from ext_package.ext_package_manager import ExtPackageManager, get_ext_package_instance

# Patch utilities
from patch import patch_utils, patch_const, patch_path

# Localization
from patch.patch_lang import get_patch_text_id

# UI
from cocosui import cc, ccui, ccs
```

---

## 🎓 Architecture Overview

```
Game Client
    ↓
PatchUI (Handles UI display)
    ↓
ExtPackageManager (Manages updates)
    ├─ _check_ext_need_patch() (Version checking)
    ├─ ext_patch_info_analyze() (Patch analysis)
    └─ stop_patch_downloader() (Download control)
    ↓
Version System (Gets version info)
    ├─ confs/version.json (Script config)
    ├─ npk_version.config (Package version)
    └─ logic/gcommon/cdata/server_version (Server version)
    ↓
Notification System (Shows dialogs)
    ├─ show_confirm_box() (Confirmation)
    └─ Red Point System (Status indicators)
```

---

**Last Updated:** January 28, 2026  
**Total Coverage:** ~2600+ lines of code analyzed  
**Key Findings:** 6 major notification mechanisms identified
