# Version/Update Notification - Code Patterns & Examples

---

## Pattern 1: Complete Version Check & Update Flow

### Scenario: Check if game needs update on startup

```python
# In: game_launcher.py or init_game.py
def check_game_version():
    from version import get_cur_version_str, get_server_version
    from ext_package.ext_package_manager import get_ext_package_instance
    
    # Get current versions
    current_version = get_cur_version_str()
    server_version = get_server_version()
    
    print(f"Current: {current_version}, Server: {server_version}")
    
    # Check if patch needed
    ext_mgr = get_ext_package_instance()
    if ext_mgr._check_ext_need_patch():
        print("Update available - starting download")
        ext_mgr.ext_patch_info_analyze(on_patch_analyze_complete)
    else:
        print("Already up to date")
        start_game()

def on_patch_analyze_complete(result):
    if result == EXT_STATE_PATCH_INFO_ANALYZE_FINISH:
        print("Patch analysis complete")
        start_game()
    else:
        print(f"Patch analysis failed: {result}")
```

---

## Pattern 2: Version Comparison with Fallback

### Scenario: Safe version checking with error handling

```python
def safe_version_check():
    from version import get_script_version, get_server_version
    
    try:
        local_ver = get_script_version()
        server_ver = get_server_version()
        
        # Convert to integers safely
        local_ver_int = int(local_ver) if local_ver else 0
        server_ver_int = int(server_ver) if server_ver else 0
        
        if server_ver_int > local_ver_int:
            return True  # Update needed
        return False
    except Exception as e:
        print(f"Version check error: {e}")
        return False  # Assume no update on error

# Usage
if safe_version_check():
    show_update_available_dialog()
```

---

## Pattern 3: Display Version Info UI

### Scenario: Show current version in settings/about screen

```python
def show_version_info():
    from version import (
        get_engine_version, get_engine_svn, get_script_version,
        get_tag, get_cur_version_str, get_npk_version
    )
    
    version_data = {
        'full_version': get_cur_version_str(),
        'engine': get_engine_version(),
        'engine_svn': get_engine_svn(),
        'script': get_script_version(),
        'tag': get_tag(),
        'npk': get_npk_version()
    }
    
    # Create UI
    version_text = f"""
    Game Version: {version_data['full_version']}
    Engine: {version_data['engine']}
    SVN: {version_data['engine_svn']}
    Tag: {version_data['tag']}
    """
    
    ui_label.setString(version_text)
    return version_data
```

---

## Pattern 4: Override Version Check (Disable Updates)

### Scenario: Disable automatic update checking

```python
# Method A: Monkey patch the check function
def disable_update_checks():
    from ext_package.ext_package_manager import ExtPackageManager
    
    # Override method to always return False
    original_check = ExtPackageManager._check_ext_need_patch
    
    def patched_check(self):
        print("[PATCHED] Update check disabled")
        return False
    
    ExtPackageManager._check_ext_need_patch = patched_check
    
    print("Update checks disabled")

# Method B: Set force_stop flag
def stop_updates():
    from ext_package.ext_package_manager import get_ext_package_instance
    
    ext_mgr = get_ext_package_instance()
    ext_mgr.force_stop = True
    ext_mgr.stop_patch_downloader()
    
    print("Download stopped")

# Method C: Override initialization
def skip_update_init():
    import six.moves.builtins
    
    # Prevent PATCH_LIST from being set
    six.moves.builtins.__dict__['PATCH_LIST'] = []
    
    print("Patch list cleared")
```

---

## Pattern 5: Custom Update Notification Dialog

### Scenario: Show custom update available message

```python
def show_custom_update_dialog():
    from patch.patch_utils import show_confirm_box
    from patch.patch_lang import get_patch_text_id
    from version import get_cur_version_str
    
    def on_user_accept():
        print("User wants to update")
        # Start download
        start_patch_download()
    
    def on_user_decline():
        print("User declined update")
        # Continue game
        start_game()
    
    current_version = get_cur_version_str()
    
    dialog_message = f"New version available!\nCurrent: {current_version}\nWould you like to update?"
    
    show_confirm_box(
        on_user_accept,
        on_user_decline,
        dialog_message,
        "Update Now",
        "Play Now"
    )
```

---

## Pattern 6: Red Point Notification System

### Scenario: Manage in-game notification indicators (red dots)

```python
class NotificationManager:
    def __init__(self):
        self.mall_manager = get_mall_manager()
    
    # Show notification
    def show_notification(self, category, count):
        self.mall_manager.set_red_point(category, count)
        print(f"Red point set: {category} = {count}")
    
    # Hide notification
    def hide_notification(self, category):
        self.mall_manager.set_red_point(category, 0)
        print(f"Red point cleared: {category}")
    
    # Hide all notifications
    def clear_all_notifications(self):
        self.mall_manager.clear_all_red_points()
        print("All red points cleared")
    
    # Get notification count
    def get_notification_count(self, category=None):
        if category:
            return self.mall_manager.get_mall_red_point_info(category)
        return self.mall_manager.get_mall_red_point_info()
    
    # Get total notifications
    def get_total_notifications(self):
        return self.mall_manager.get_total_red_points()

# Usage
notif_mgr = NotificationManager()
notif_mgr.show_notification('shop_weapons', 3)
notif_mgr.show_notification('shop_cosmetics', 5)

total = notif_mgr.get_total_notifications()  # Returns 8
notif_mgr.clear_all_notifications()
```

---

## Pattern 7: Patch Download Progress Tracking

### Scenario: Monitor and display download progress

```python
class PatchDownloadTracker:
    def __init__(self):
        from ext_package.ext_package_manager import get_ext_package_instance
        self.ext_mgr = get_ext_package_instance()
    
    def get_download_progress(self):
        """Get download progress (0.0 to 1.0)"""
        progress, is_downloading = self.ext_mgr.get_progress()
        return progress
    
    def get_download_speed(self):
        """Get download speed in MB/s"""
        speed_mb, total_size = self.ext_mgr.get_speed_and_size()
        return speed_mb
    
    def is_downloading(self):
        """Check if download is in progress"""
        return self.ext_mgr.get_is_downloading()
    
    def get_download_state(self):
        """Get current download state"""
        return self.ext_mgr.get_state()
    
    def stop_download(self):
        """Stop ongoing download"""
        self.ext_mgr.stop_patch_downloader()
        print("Download stopped")
    
    def update_ui(self):
        """Update progress UI"""
        if self.is_downloading():
            progress = self.get_download_progress()
            speed = self.get_download_speed()
            
            progress_percent = progress * 100
            print(f"Download: {progress_percent:.1f}% ({speed:.2f} MB/s)")

# Usage
tracker = PatchDownloadTracker()
while tracker.is_downloading():
    tracker.update_ui()
    time.sleep(0.5)
```

---

## Pattern 8: Version Config Management

### Scenario: Load, save, and manage version configurations

```python
import json
import C_file

class VersionConfigManager:
    def __init__(self):
        self.config = self.load_config()
    
    def load_config(self):
        """Load version configuration from file"""
        try:
            config_data = C_file.get_res_file('confs/version.json', '')
            return json.loads(config_data)
        except Exception as e:
            print(f"Failed to load version config: {e}")
            return {}
    
    def get_field(self, field_name, default=None):
        """Get configuration field"""
        return self.config.get(field_name, default)
    
    def get_svn_version(self):
        """Get SVN version"""
        return self.get_field('svn_version', '0')
    
    def get_tag(self):
        """Get build tag"""
        return self.get_field('tag', 'None')
    
    def get_all_fields(self):
        """Get all configuration fields"""
        return self.config
    
    def validate_version(self, version_str):
        """Validate version string format"""
        try:
            return int(version_str) > 0
        except:
            return False
    
    def compare_versions(self, v1, v2):
        """Compare two versions"""
        try:
            int_v1 = int(v1)
            int_v2 = int(v2)
            
            if int_v1 < int_v2:
                return -1  # v1 is older
            elif int_v1 > int_v2:
                return 1   # v1 is newer
            else:
                return 0   # Same version
        except:
            return None

# Usage
config_mgr = VersionConfigManager()
svn = config_mgr.get_svn_version()
tag = config_mgr.get_tag()

comparison = config_mgr.compare_versions('12345', '12346')
if comparison == -1:
    print("Version 12345 is older than 12346")
```

---

## Pattern 9: Auto-Accept Update Dialog

### Scenario: Automatically accept update confirmation dialog

```python
def enable_auto_update_mode():
    """Automatically accept all update dialogs"""
    from patch import patch_utils
    
    # Store original function
    original_show_confirm_box = patch_utils.show_confirm_box
    
    # Create wrapper that auto-accepts
    def auto_accept_confirm_box(ok_cb, cancel_cb, text, ok_text, cancel_text):
        print(f"[AUTO-ACCEPT] Dialog: {text}")
        # Automatically call OK callback
        if ok_cb:
            ok_cb()
    
    # Replace function
    patch_utils.show_confirm_box = auto_accept_confirm_box
    
    print("Auto-accept mode enabled")

# Usage
enable_auto_update_mode()
# Now all update dialogs will be auto-accepted
```

---

## Pattern 10: Version Logging and Reporting

### Scenario: Log version info for debugging/reporting

```python
import json
import time

class VersionLogger:
    def __init__(self):
        self.log_entries = []
    
    def log_version_info(self):
        """Log all version information"""
        from version import (
            get_engine_version, get_engine_svn, get_script_version,
            get_tag, get_cur_version_str, get_npk_version
        )
        
        entry = {
            'timestamp': time.time(),
            'full_version': get_cur_version_str(),
            'engine': get_engine_version(),
            'engine_svn': get_engine_svn(),
            'script': get_script_version(),
            'tag': get_tag(),
            'npk': get_npk_version()
        }
        
        self.log_entries.append(entry)
        return entry
    
    def log_update_check(self, result):
        """Log update check result"""
        entry = {
            'timestamp': time.time(),
            'event': 'update_check',
            'result': 'needed' if result else 'not_needed'
        }
        self.log_entries.append(entry)
    
    def export_log(self, filename='version_log.json'):
        """Export version log to file"""
        try:
            with open(filename, 'w') as f:
                json.dump(self.log_entries, f, indent=2)
            print(f"Log exported to {filename}")
        except Exception as e:
            print(f"Failed to export log: {e}")
    
    def print_log(self):
        """Print version log to console"""
        print("=== Version Log ===")
        for entry in self.log_entries:
            print(json.dumps(entry, indent=2))

# Usage
logger = VersionLogger()
logger.log_version_info()
logger.log_update_check(False)
logger.print_log()
```

---

## Pattern 11: Notification Batch Operations

### Scenario: Update multiple notification indicators at once

```python
class NotificationBatch:
    def __init__(self):
        self.mall_manager = get_mall_manager()
        self.updates = {}
    
    def add_notification(self, category, count):
        """Queue notification update"""
        self.updates[category] = count
    
    def add_notifications(self, notification_dict):
        """Queue multiple notifications"""
        self.updates.update(notification_dict)
    
    def apply(self):
        """Apply all queued notifications"""
        for category, count in self.updates.items():
            self.mall_manager.set_red_point(category, count)
            print(f"Updated {category}: {count}")
        self.updates.clear()
    
    def clear(self):
        """Clear all notifications"""
        self.mall_manager.clear_all_red_points()
        self.updates.clear()

# Usage
batch = NotificationBatch()
batch.add_notifications({
    'shop_weapons': 3,
    'shop_cosmetics': 2,
    'shop_battle_pass': 1,
    'achievements': 5
})
batch.apply()  # Apply all at once
```

---

## Pattern 12: Conditional Update Behavior

### Scenario: Different update behavior based on conditions

```python
def determine_update_behavior():
    """Determine how to handle updates based on conditions"""
    import time
    from version import get_cur_version_str
    from ext_package.ext_package_manager import get_ext_package_instance
    
    ext_mgr = get_ext_package_instance()
    
    # Get current time and version
    current_hour = time.localtime().tm_hour
    current_version = get_cur_version_str()
    
    # Define behavior rules
    if current_hour >= 22 or current_hour < 6:
        # Night time: disable updates
        print("Night time - disabling updates")
        ext_mgr.force_stop = True
    
    elif ext_mgr._check_ext_need_patch():
        # Update available
        if is_on_wifi():
            # WiFi: auto-download
            print("WiFi detected - starting automatic download")
            start_auto_download()
        else:
            # Mobile data: ask user
            print("Mobile data - asking user permission")
            show_update_prompt()
    
    else:
        # No update needed
        print(f"Version {current_version} is current")
        start_game()

def is_on_wifi():
    """Check if device is on WiFi"""
    # Implementation depends on platform
    return True

def start_auto_download():
    """Start automatic download"""
    pass

def show_update_prompt():
    """Show user update prompt"""
    pass

def start_game():
    """Start the game"""
    pass
```

---

**End of Code Patterns**
