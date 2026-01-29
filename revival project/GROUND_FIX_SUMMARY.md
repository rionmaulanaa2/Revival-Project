# Character Falling Underground - COMPREHENSIVE FIX

## Root Cause Analysis

**Problem:** Character falls through the lobby ground immediately upon entering the lobby.

**Root Cause:** 
- `LLobbyAvatar` is created by `PartLobbyCharacter.create_character()` 
- The Unit logic immediately has physics/gravity enabled
- Physics pulls the character downward before the position can be set on the ground
- Original ground detection was too late and lacked error visibility

## Solution Implemented

### 1. **Aggressive Grounding with Multi-Step Approach**
Located in `script_patch/785/785_17524466876519882393.py` lines 1020-1180

The fix uses a 6-step grounding process:

```
Step 1: Detect ground height via scene_utils.get_ground_height()
        ↓
Step 2: Create target position (ground_height + 0.2 units)
        ↓
Step 3: Set position on Unit.logic directly (bypass wrapper)
        ↓
Step 4: Set position on wrapper (redundancy)
        ↓
Step 5: Zero velocity on logic (kill downward momentum)
        ↓
Step 6: Zero velocity on wrapper (redundancy)
```

### 2. **Continuous Ground Clamping (100 iterations = 10 seconds)**

After initial grounding, a continuous clamping loop runs that:
- Checks every 0.1 seconds if the avatar is falling
- Detects when Y position drops below ground level
- Immediately repositions the avatar on the ground
- Kills any downward velocity
- Logs each iteration with detailed status

### 3. **Comprehensive Error Catching**

Every major operation is wrapped with try-catch blocks that:
- Capture error messages without crashing
- Log specific failures (e.g., "get_ground_height failed: X")
- Continue with fallbacks when possible
- Print full traceback on critical errors

## Error Logging Output

The fix adds detailed logging at each stage:

```
===== LOBBY INIT START =====
Lobby scene loaded, waiting for physics to stabilize...
Wait check: scene=True, lobby_player=True
Scene & lobby_player ready, attempting to ground...
Ground height detected: 100.50
Target position: (0, 100.70, 0)
Set position on logic: (0, 100.70, 0)
Set position on wrapper: (0, 100.70, 0)
Velocity zeroed on logic
Velocity zeroed on wrapper
Starting continuous ground clamp...
[Clamp 1] OK: y=100.70 >= target=100.70 (ground=100.50)
[Clamp 2] OK: y=100.70 >= target=100.70 (ground=100.50)
...
===== GROUNDING COMPLETE after 100 iterations =====
```

## Key Changes Made

1. **Initial Grounding Function `_force_ground_avatar()`**
   - Runs once when scene and lobby_player are ready
   - Attempts 6 different positioning/velocity fixes
   - Collects errors in a list for logging
   - Uses fallback `CHARACTER_STAND_HEIGHT` if ground detection fails

2. **Continuous Clamping Loop `_clamp_avatar_to_ground()`**
   - Counter tracks iteration number (1-100)
   - Each iteration logs: `[Clamp N] status/error`
   - Compares current Y position against ground level + 0.2 buffer
   - If falling, repositions and logs exact delta
   - Continues for 100 iterations (max 10 seconds)

3. **Wait Logic `_wait_for_collision_and_open_ui()`**
   - Checks scene collision readiness with specific error messages
   - Checks lobby_player existence and logic initialization
   - Reports retry reasons (e.g., "lobby_player not ready (has logic=False, has pos=False)")
   - Retries with appropriate intervals (0.1s or 0.2s)

## Error Messages to Expect

If something goes wrong, you'll see messages like:

```
[Clamp 5] ERROR: lobby_player is None
[Clamp 10] ERROR getting pos: 'NoneType' object has no attribute 'x'
[Clamp 15] get_ground_height error: collision not ready
[Clamp 20] ERROR setting pos: pos property is read-only
[Clamp 25] ERROR zeroing velocity: no velocity attribute
```

These errors don't stop the process—they're logged and the fix continues trying.

## If Issue Persists

Check the logs for:
1. **Missing `global_data.lobby_player`** → PartLobbyCharacter.create_character() wasn't called
2. **"collision not ready"** → Scene collision system not initialized before lobby init
3. **"get_ground_height error"** → Ground mesh not loaded or collision group mismatch
4. **"pos property is read-only"** → Can't set position on this entity type
5. **Repeated falling in clamp loop** → Physics/gravity component overriding position each frame

## Files Modified

- `script_patch/785/785_17524466876519882393.py` (lines 1020-1180)
  - Expanded from ~160 lines to ~280 lines
  - Added comprehensive error catching and logging
  - Changed clamping from 50 iterations to 100
  - Added detailed status messages at each step
