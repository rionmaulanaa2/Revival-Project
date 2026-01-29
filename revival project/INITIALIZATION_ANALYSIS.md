# Deep Analysis: Offline Lobby Initialization vs Normal Login Flow

## Executive Summary

**Critical Issues Found:**
1. **Missing Scene Initialization**: PartLobby.init_data_mgr() not called
2. **Missing Event Emissions**: on_login_success_event never emitted
3. **Missing Manager Initialization**: Several key managers not initialized
4. **Collision System**: Ground collision not registered before character spawn
5. **Physics Timing**: Character falls before ground detection completes

---

## Normal Login Flow (Complete Initialization)

### Phase 1: Authentication & Connection
```
1. LoginFunctionUI → Server connection
2. Server auth success
3. Avatar.on_become_player() called
4. Emits: global_data.emgr.on_login_success_event.emit()
```

### Phase 2: Manager Initialization
```
Avatar.on_become_player() triggers:
├─ global_data.player = self
├─ global_data.owner_entity = self
├─ global_data.emgr.on_login_success_event.emit()
│  └─ Triggers ALL registered listeners across ~130 imp* modules
├─ LoginSetting().update_local_server_lst()
├─ global_data.message_data.read_local_data()
├─ update_dump_user_info()
├─ global_data.channel.set_user_info()
├─ global_data.emgr.avatar_finish_create_event.emit()
├─ global_data.emgr.avatar_finish_create_event_global.emit()
├─ global_data.channel.query_linegame_third_cred()
├─ self._call_meta_member_func('_on_login_@_success')  ← CRITICAL
│  └─ Calls ALL imp*.on_login_success() methods
└─ self.start_game_sync_time()
```

### Phase 3: Scene Loading & Part Initialization
```
Scene loads Lobby → PartLobby.__init__() called:
├─ self.init_data_mgr()
│  ├─ LobbyRedPointData() singleton created
│  ├─ LobbyMallData() singleton created
│  └─ MessageBoardManager() singleton created
├─ self.init_log_mgr()
│  └─ UILifetimeLogMgr() created & listener started
├─ global_data.scene_type = SCENE_TYPE_LOBBY
├─ global_data.voice_mgr.init_ngvoice()
├─ AntiCheatSDKMgr.init_acsdk()
└─ BattleCheckPos() singleton created
```

### Phase 4: Lobby Character Creation
```
PartLobbyCharacter.create_character():
├─ Creates LLobbyAvatar entity
├─ ComCharacterLobby component initialized
│  ├─ Inherits from ComCharacterBase
│  ├─ init_from_dict() calls _init_character()
│  ├─ _init_character() creates collision.Character
│  ├─ scene.scene_col.add_character() registers physics
│  └─ Physics now ACTIVE (gravity enabled)
├─ Character position set
└─ global_data.lobby_player = lobby_avatar
```

### Phase 5: UI & Event System Ready
```
LobbyUI.__init__():
├─ Reads global_data.lobby_red_point_data (already initialized)
├─ Calls init_mall_redpoint_and_new()
├─ Registers event listeners
└─ UI becomes visible
```

---

## Offline Flow (Your Patched Code)

### Phase 1: Button Click Bypass
```
on_click_feedback_btn() instead of normal login:
├─ Create Avatar entity manually
├─ Call avatar.init_from_dict(bdict)
│  ├─ Does NOT call on_become_player()
│  ├─ Does NOT emit on_login_success_event
│  └─ Does NOT call _on_login_@_success metafunc
├─ Manually create some global managers:
│  ├─ camera_state_pool ✓
│  ├─ ex_scene_mgr_agent ✓
│  ├─ gsetting ✓
│  ├─ anticheat_utils ✓
│  ├─ moveKeyboardMgr ✓
│  ├─ track_cache ✓
│  ├─ game_voice_mgr ✓
│  ├─ ccmini_mgr ✓
│  └─ lobby_red_point_data ✓ (stub)
└─ CharacterSelectUINew() shown
```

### Phase 2: Character Selection
```
start_newbie_qte_guide() triggered by character select:
├─ Update avatar.role_id
├─ Manually ensure lobby_red_point_data (again)
├─ Create Lobby entity
├─ Call lobby.init_from_dict()
│  └─ Scene loads, PartLobby.__init__() called
│      ├─ init_data_mgr() tries to create:
│      │  ├─ LobbyRedPointData() → FAILS (already exists as stub)
│      │  ├─ LobbyMallData() → CREATES new singleton
│      │  └─ MessageBoardManager() → CREATES new singleton
│      └─ Physics collision system initializes
└─ _delayed_lobby_init() schedules lobby loading
```

### Phase 3: Ground Collision Racing Condition
```
_wait_for_collision_and_open_ui() loop:
├─ Waits for scene.scene_col to exist
├─ Waits for lobby_player to exist
├─ lobby_player created BY PartLobbyCharacter
│  ├─ ComCharacterLobby creates collision.Character
│  ├─ Gravity IMMEDIATELY active (980 units/s²)
│  ├─ Character starts falling
│  └─ NO GROUND COLLISION exists yet!
├─ _force_ground_avatar() tries raycast
│  └─ Returns MISS (no ground collision registered)
└─ Character continues falling infinitely
```

---

## Missing Initialization Components

### 1. **Event System Not Triggered**
```python
# MISSING in offline flow:
global_data.emgr.on_login_success_event.emit()
avatar._call_meta_member_func('_on_login_@_success')

# These trigger initialization in ~130 imp* modules:
- impBattle.on_login_success()
- impFriend.on_login_success()
- impShop.on_login_success()
- impTeam.on_login_success()
- impMecha.on_login_success()
- impTask.on_login_success()
... (127+ more modules)
```

### 2. **Scene Part Managers**
```python
# PartLobby.init_data_mgr() creates singletons:
LobbyRedPointData()  # Your stub conflicts with real singleton
LobbyMallData()      # Never initialized manually
MessageBoardManager()  # Never initialized manually

# PartLobby.init_log_mgr() creates:
UILifetimeLogMgr()  # Never initialized manually
```

### 3. **Global Data Managers**
```python
# MISSING managers (normal flow initializes these):
global_data.nile_sdk  # SDK integration
global_data.anticheatsdk_mgr  # Anti-cheat (you have anticheat_utils only)
global_data.sound_mgr  # Sound system
global_data.battle_check_pos  # Battle position checker
global_data.message_data  # Message system
global_data.voice_mgr.init_ngvoice()  # Voice chat
```

### 4. **Channel & Platform Integration**
```python
# MISSING platform calls:
global_data.channel.set_user_info()
global_data.channel.set_roleinfo()
global_data.channel.query_linegame_third_cred()
```

### 5. **Scene Type & Context**
```python
# PartLobby sets this, but might be needed earlier:
global_data.scene_type = SCENE_TYPE_LOBBY
```

---

## Why Collision Fails

### Root Cause Chain:
```
1. lobby.init_from_dict() → Scene loads
2. Scene loads PartLobby → __init__() runs
3. PartLobby creates lobby scene (visual + collision geometry)
4. Scene collision system initializes (scene.scene_col ready)
5. PartLobbyCharacter.create_character() creates lobby_player
6. lobby_player has ComCharacterLobby → creates collision.Character
7. collision.Character registered with scene.scene_col
8. Gravity IMMEDIATELY active (980 units/s²)
9. _wait_for_collision_and_open_ui() detects lobby_player exists
10. Calls _force_ground_avatar() → raycasts for ground
11. Raycast returns NO HIT (lobby scene has no LAND_GROUP collision!)
12. Uses fallback floor y=23.6
13. Character position set to y=25.8
14. But gravity pulls character down FASTER than clamp loop (0.02s interval)
15. Character falls through fallback floor
```

### The Real Problem:
**Lobby scene file has NO collision geometry!**
- Visual models exist (you see the floor)
- But collision layer is missing or not tagged as LAND_GROUP
- Raycasts can't find anything to hit
- Character has no physical ground to stand on

---

## Recommended Fixes

### Fix 1: Call Missing Initialization (CRITICAL)
```python
# Add to on_click_feedback_btn() after avatar creation:

# Emit critical events that trigger module initialization
global_data.player = avatar
global_data.owner_entity = avatar

# Trigger login success event (initializes all imp* modules)
try:
    global_data.emgr.on_login_success_event.emit()
except Exception as e:
    raidis('[Init] on_login_success_event emit failed: %s' % e)

# Call meta member function for imp* module initialization
try:
    avatar._call_meta_member_func('_on_login_@_success')
except Exception as e:
    raidis('[Init] _on_login_@_success metafunc failed: %s' % e)

# Initialize message data
try:
    if global_data.message_data:
        global_data.message_data.read_local_data()
except Exception as e:
    raidis('[Init] message_data initialization failed: %s' % e)
```

### Fix 2: Pre-Initialize Lobby Managers
```python
# Add to on_click_feedback_btn() BEFORE showing CharacterSelectUINew:

# Initialize lobby data managers early
try:
    from logic.comsys.lobby.LobbyMallData import LobbyMallData
    LobbyMallData()
except Exception as e:
    raidis('[Init] LobbyMallData failed: %s' % e)

try:
    from logic.comsys.home_message_board.MessageBoardManager import MessageBoardManager
    MessageBoardManager()
except Exception as e:
    raidis('[Init] MessageBoardManager failed: %s' % e)
```

### Fix 3: Ground Collision Creation (ALREADY IMPLEMENTED)
Your recent code already creates ground collision:
```python
ground_collision = collision.BoxCollider(...)
scene.scene_col.add_static_collider(ground_collision)
```
**Status: ✓ Done**

### Fix 4: Disable Gravity Until Ground Ready (ALREADY IMPLEMENTED)
Your recent code disables gravity initially:
```python
lp.ev_s_gravity(0.0)  # Disable until ground found
```
**Status: ✓ Done**

### Fix 5: Scene Type Declaration
```python
# Add to start_newbie_qte_guide() before lobby creation:
from logic.vscene import scene_type
global_data.scene_type = scene_type.SCENE_TYPE_LOBBY
```

### Fix 6: Initialize Sound Manager Stub
```python
# Add to on_click_feedback_btn():
if not hasattr(global_data, 'sound_mgr') or not global_data.sound_mgr:
    class _SoundMgrStub:
        def close_ios_check_sys_mute(self): pass
        def set_master_volume(self, vol): pass
        def play_sound(self, *a, **k): pass
    global_data.sound_mgr = _SoundMgrStub()
```

---

## Impact Assessment

### Current State:
- ✓ Basic globals initialized (camera, scene manager, etc.)
- ✓ Ground collision created
- ✓ Gravity disabled initially
- ✗ Event system not triggered (130+ modules uninitialized)
- ✗ Lobby data managers not pre-created
- ✗ Sound/voice managers missing
- ✗ imp* module callbacks not called

### Risk Level:
- **High Risk**: Event system (can cause crashes in UI callbacks)
- **Medium Risk**: Lobby data managers (UI may fail to load data)
- **Low Risk**: Sound/voice managers (gracefully handled with stubs)
- **Fixed**: Collision/gravity issues (recent patches address this)

---

## Testing Checklist

After applying all fixes:
1. Load lobby - check console for initialization messages
2. Verify character doesn't fall underground
3. Try opening lobby UI panels (inventory, shop, etc.)
4. Check for any NoneType errors in console
5. Verify character position stays stable
6. Test if raycasts find the created ground collision

---

## Conclusion

Your offline flow bypasses critical initialization that normal login performs automatically. The main issues are:

1. **Event emission missing** → 130+ modules never initialize their login callbacks
2. **Manager pre-creation missing** → Singletons created in wrong order
3. **Collision timing** → Ground doesn't exist when character spawns (FIXED)
4. **Gravity timing** → Character falls before grounding (FIXED)

The collision/gravity fixes are good, but event system initialization is still needed for full stability.
