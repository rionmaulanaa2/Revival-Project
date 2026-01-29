# Version/Update Notification System - Complete Documentation Index

**Generated: January 28, 2026**  
**Scope: script_patch/ and script_week/ folders**  
**Total Code Analyzed: ~2600+ lines**

---

## 📚 Documentation Files Created

### 1. **VERSION_UPDATE_NOTIFICATION_SUMMARY.md** ⭐ START HERE
**Purpose:** Executive summary with file paths and code snippets  
**Contains:**
- Primary version management system overview
- Patch/update checking system
- Update notification UI system (show_confirm_box)
- Red point notification system
- Disabling/hiding mechanisms
- Files organized by functionality

**Best for:** Quick overview, finding specific mechanisms, understanding the big picture

---

### 2. **VERSION_UPDATE_TECHNICAL_REFERENCE.md** 🔧 DETAILED GUIDE
**Purpose:** Deep technical documentation with full code implementations  
**Contains:**
- Core version functions (get_engine_version, get_script_version, etc.)
- Extension package version checking
- Patch UI notification system
- Red point notification implementation
- Patch states and flow
- Error handling patterns
- Configuration and constants

**Best for:** Understanding implementation details, modifying code, debugging

---

### 3. **VERSION_UPDATE_QUICK_REFERENCE.md** ⚡ CHEAT SHEET
**Purpose:** Fast lookup guide with code snippets  
**Contains:**
- Key files at a glance
- Version functions quick reference
- Update check logic
- Notification systems
- Configuration files
- Common text IDs
- Debugging tips

**Best for:** Quick lookups, common operations, cheat sheet for developers

---

### 4. **VERSION_UPDATE_CODE_PATTERNS.md** 💻 EXAMPLES
**Purpose:** Real-world code patterns and implementation examples  
**Contains:**
- Complete version check flow
- Safe version checking with fallback
- Version info display UI
- Disabling updates (3 methods)
- Custom update dialogs
- Red point management
- Progress tracking
- Batch operations
- Conditional behaviors

**Best for:** Implementation, copy-paste examples, understanding workflows

---

## 🎯 Quick Navigation

### Finding a Specific Mechanism

#### How to check if game needs update?
→ See: **Quick Reference** → "Check if update available"  
→ Code: **Code Patterns** → "Pattern 1: Complete Version Check"

#### How to disable update notifications?
→ See: **Summary** → "Patterns for disabling"  
→ Code: **Code Patterns** → "Pattern 4: Disable Updates"

#### What files contain version code?
→ See: **Summary** → "Files Containing Version/Update Code"  
→ Reference: **Technical Reference** → Section 1-4

#### How do red dots work?
→ See: **Summary** → "Red Point Notification System"  
→ Code: **Code Patterns** → "Pattern 6: Red Point Notifications"

#### What are the version config files?
→ See: **Quick Reference** → "Configuration Files"  
→ Details: **Technical Reference** → Section 6

#### How to show custom update dialog?
→ Code: **Code Patterns** → "Pattern 5: Custom Update Dialog"

---

## 📍 Key Files in Codebase

| File | Type | Lines | Purpose |
|------|------|-------|---------|
| `script_patch/785/785_17524466876519882393.py` | **Core** | 2569-2650 | Version functions |
| `script_patch/785/12120475367754979724.py` | **Core** | 202-231 | Update checking |
| `script_patch/1016/16725989236121328167.py` | **UI** | 947+ | Patch dialogs |
| `script_patch/785/785_17524466876519882393.py` | **System** | 980-1065 | Red points |
| `script_patch/330/11323302825905596416.py` | **Utilities** | 325-663 | Patch utils |

---

## 🔍 System Overview

### Version Hierarchy
```
1. Local Version (cached)
   ↓
2. Config File (confs/version.json)
   ↓
3. NPK Version (npk_version.config)
   ↓
4. Server Version (logic/gcommon/cdata/server_version)
```

### Update Flow
```
Game Start
    ↓
Check Version → Need Update?
    ├─ YES → Download patches → Show progress → Apply updates
    └─ NO → Continue to game

Red Points (always check)
    ↓
Show notifications on UI
```

### Notification Types
1. **Version Update Dialogs** - Confirmation for patches
2. **Red Point System** - In-game notification indicators
3. **Progress UI** - Download speed and progress
4. **Permission Dialogs** - Settings/access requests

---

## 🛠️ Common Tasks

### Task 1: Add Version Display to UI
```python
# See: Code Patterns → Pattern 3
from version import get_cur_version_str
label.text = f"Version: {get_cur_version_str()}"
```

### Task 2: Check if Update Available
```python
# See: Code Patterns → Pattern 1
ext_mgr = get_ext_package_instance()
if ext_mgr._check_ext_need_patch():
    show_update_dialog()
```

### Task 3: Disable Update Checks
```python
# See: Summary → Patterns for disabling
# See: Code Patterns → Pattern 4
ext_mgr.force_stop = True
```

### Task 4: Manage Red Points
```python
# See: Code Patterns → Pattern 6
mall_mgr.show_notification('category', 5)
mall_mgr.clear_all_notifications()
```

### Task 5: Track Download Progress
```python
# See: Code Patterns → Pattern 7
tracker = PatchDownloadTracker()
progress = tracker.get_download_progress()
```

---

## 📊 Statistics

| Metric | Count |
|--------|-------|
| Key files analyzed | 6+ |
| Version functions | 6 |
| Red point methods | 5+ |
| Update check variations | 3 |
| Notification types | 4 |
| Code patterns documented | 12 |
| Text IDs referenced | 15+ |

---

## 🔑 Key Concepts

### Version Comparison Logic
```
if int(local_version) < int(target_version):
    # Update available
```

### Notification Mechanism
```
show_confirm_box(ok_callback, cancel_callback, message, ok_text, cancel_text)
```

### Red Point System
```
set_red_point(category, count)  # Show notification
clear_all_red_points()          # Hide all notifications
```

### Update Check
```
_check_ext_need_patch() → Returns True/False
```

---

## 🎓 Learning Path

**For Beginners:**
1. Start: VERSION_UPDATE_QUICK_REFERENCE.md
2. Then: VERSION_UPDATE_NOTIFICATION_SUMMARY.md
3. Finally: VERSION_UPDATE_CODE_PATTERNS.md

**For Intermediate Users:**
1. Start: VERSION_UPDATE_NOTIFICATION_SUMMARY.md
2. Then: VERSION_UPDATE_CODE_PATTERNS.md
3. Reference: VERSION_UPDATE_QUICK_REFERENCE.md

**For Advanced Users:**
1. Start: VERSION_UPDATE_TECHNICAL_REFERENCE.md
2. Reference: VERSION_UPDATE_CODE_PATTERNS.md
3. Deep dive: Actual source files

**For Implementation:**
1. Find pattern: VERSION_UPDATE_CODE_PATTERNS.md
2. Get details: VERSION_UPDATE_TECHNICAL_REFERENCE.md
3. Check quick: VERSION_UPDATE_QUICK_REFERENCE.md

---

## 🚀 Quick Start

### Want to understand the version system?
→ Read: **VERSION_UPDATE_NOTIFICATION_SUMMARY.md** (5 min read)

### Want to disable updates?
→ See: **VERSION_UPDATE_CODE_PATTERNS.md** → Pattern 4 (2 min read)

### Want to modify red point system?
→ See: **VERSION_UPDATE_CODE_PATTERNS.md** → Pattern 6 (3 min read)

### Want complete reference?
→ Read: **VERSION_UPDATE_TECHNICAL_REFERENCE.md** (30 min read)

### Want code examples?
→ See: **VERSION_UPDATE_CODE_PATTERNS.md** (10 min read)

---

## 📖 Table of Contents by Topic

### Version Functions
- **Summary:** Section "Core Version Functions"
- **Technical:** Section 1 "Core Version Functions"
- **Quick Ref:** "Version Functions Quick Reference"
- **Code:** Pattern 2, 3

### Update Checking
- **Summary:** Section "Patch/Update Checking System"
- **Technical:** Section 2 "Extension Package Version Checking"
- **Quick Ref:** "Update Check Logic"
- **Code:** Pattern 1, 4

### Notifications (Dialogs)
- **Summary:** Section "Update Notification UI System"
- **Technical:** Section 3 "Patch UI Notification System"
- **Quick Ref:** "Notification Systems"
- **Code:** Pattern 5, 9

### Red Points
- **Summary:** Section "Red Point Notification System"
- **Technical:** Section 4 "Red Point Notification System"
- **Quick Ref:** "Red Point Notifications"
- **Code:** Pattern 6, 11

### Disabling
- **Summary:** Section "Disabling/Hiding Notification Mechanisms"
- **Technical:** Section 7 "Disabling Mechanisms"
- **Code:** Pattern 4, 9

### Configuration
- **Summary:** Section "Configuration Files Referenced"
- **Technical:** Section 6 "Configuration & Constants"
- **Quick Ref:** "Configuration Files"
- **Code:** Pattern 8

---

## 🔗 Cross References

### By File
- `785_17524466876519882393.py` → Summary, Tech §1/§4, Quick §1/§6, Code §2/§3
- `12120475367754979724.py` → Summary, Tech §2, Quick §2, Code §1/§4/§7
- `16725989236121328167.py` → Summary, Tech §3, Quick §3, Code §5/§9
- `11323302825905596416.py` → Summary, Tech §5, Code §5

### By Concept
- Version Display → Tech §1, Quick §1, Code §3
- Update Flow → Tech §6, Code §1, §7
- Disable Updates → Summary, Tech §7, Code §4, §9
- Notifications → Summary, Tech §3/§4, Quick §3, Code §5/§6/§11

---

## ✅ Verification Checklist

Use this to verify you've covered everything:

- [ ] Read the summary document
- [ ] Identified all version source files
- [ ] Understand version comparison logic
- [ ] Found red point notification system
- [ ] Reviewed notification dialogs
- [ ] Checked disabling mechanisms
- [ ] Examined configuration files
- [ ] Reviewed code patterns
- [ ] Tested with actual codebase

---

## 📞 Support & References

### For Questions About...

**Version Functions**
→ Technical Reference §1 + Code Pattern 3

**Update Checking**
→ Summary + Technical Reference §2 + Code Pattern 1

**Notification UI**
→ Technical Reference §3 + Code Pattern 5

**Red Points**
→ Summary + Technical Reference §4 + Code Pattern 6

**Configuration**
→ Quick Reference + Technical Reference §6

**Implementation**
→ Code Patterns (all patterns)

**Debugging**
→ Quick Reference → Debugging Tips

---

## 🎯 Next Steps

1. **Review:** Choose a documentation file based on your needs
2. **Find:** Use Quick Reference for fast lookups
3. **Implement:** Use Code Patterns for copy-paste ready examples
4. **Deep Dive:** Use Technical Reference for implementation details
5. **Reference:** Keep Quick Reference nearby for common operations

---

## 📝 Notes

- All code is from decompiled bytecode (uncompyle6)
- Files are Python 2.7 compatible
- Paths are relative to game root
- Text IDs are localization references (see patch_lang.py)
- Timestamps and logging are optional

---

## 🔄 Document Version History

| Date | Version | Changes |
|------|---------|---------|
| 2026-01-28 | 1.0 | Initial comprehensive documentation |

---

## 📄 All Documents Summary

```
INDEX (This file)
│
├─ VERSION_UPDATE_NOTIFICATION_SUMMARY.md (Main overview)
├─ VERSION_UPDATE_TECHNICAL_REFERENCE.md (Deep dive)
├─ VERSION_UPDATE_QUICK_REFERENCE.md (Cheat sheet)
└─ VERSION_UPDATE_CODE_PATTERNS.md (Examples)
```

---

**Ready to dive in? Start with the documentation file that matches your needs!**

✨ Happy coding! ✨
