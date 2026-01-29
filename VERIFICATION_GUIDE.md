# Verification Guide: Character Physics Fix

## Quick Summary
- **What was fixed:** Lobby character now has full physics instead of being just a visual model
- **Result:** Character should no longer fall underground
- **Mechanism:** ComCharacterLobby now properly initializes collision.Character object through parent class

## How to Verify the Fix Works

### 1. Visual Check
- Load into the lobby
- Character should spawn and stay on ground
- Character should NOT fall through the floor
- Character should be visible in the same position as before

### 2. Console Output Check
Launch game and check logs/console for these messages within first 3 seconds:

**Good Signs:**
```
[Physics Check] Character object exists, valid=True
[Physics Check] Character has gravity: 980.0
[Clamp] Ground detected via raycast at y=23.5
```

**Acceptable (fallback is working):**
```
[Physics Check] Character object exists, valid=True
[Physics Check] Character has gravity: 980.0
[Clamp] No ground found via raycast, using fallback floor y=23.6
```

**Bad Signs (Physics not enabled):**
```
[Physics Check] Character object exists, valid=False
```
OR
```
(No [Physics Check] message at all)
```

### 3. Behavior Tests (if applicable)

#### Walking Test
- If lobby supports character movement
- Try moving character around
- ✓ Character should move smoothly (not jerky)
- ✓ Character should not fall when standing still
- ✗ Character should NOT be able to move down infinitely

#### Jumping Test (if supported)
- Try jumping with character
- ✓ Character should go up then fall back down
- ✓ Character should land on ground and stop
- ✗ Character should NOT fall through floor after landing

#### Stairs/Slopes Test (if available)
- Try moving character up stairs or slopes
- ✓ Character should climb naturally
- ✓ Character should slide down slopes (with gravity)
- ✗ Character should NOT become stuck

### 4. Position Check
- Open console and check character position multiple times
- Position Y should remain consistent (not constantly decreasing)
- X and Z can change (if character moves)

## Understanding the Physics System

### What "Physics Enabled" Means
- Character has `collision.Character` object (3D capsule representing body)
- Gravity pulls character down (9.8 m/s² equivalent)
- Ground detection checks if character is standing on terrain
- Collision response prevents character from walking through walls/terrain

### What "Physics Disabled" Means
- Character is just visual model with no collision object
- No gravity (character doesn't fall)
- No ground detection (character can't check if standing)
- Character can pass through everything
- Character position is manually controlled (not physics-based)

## Common Issues and Solutions

### Issue: Character still falls underground

**Cause 1: Physics not enabled**
- **Check:** Console should show `[Physics Check] Character object exists, valid=True`
- **If shows False or missing:** Physics initialization failed, check logs for errors

**Cause 2: Lobby scene has no ground collision**
- **Check:** Console should show `[Clamp] Ground detected via raycast`
- **If shows "No ground found":** Lobby scene missing LAND_GROUP collision geometry
- **Solution:** Fallback floor (y=23.6) should catch character, but character can't walk naturally

**Cause 3: Fallback floor height wrong**
- **Check:** Character lands but is sinking through visual floor
- **Solution:** Adjust `lobby_floor_y = 23.6` in grounding code (increase value to raise floor)

### Issue: Character can't move

**This is expected in lobby** - Lobby scenes typically only support viewing character, not controlling movement. This is not a bug.

### Issue: Physics Check shows error

```
[Physics Check] Error checking physics: AttributeError
```
- **Cause:** Character component not fully initialized yet
- **Solution:** Increase wait time before physics check (already handled in code)
- **This is normal:** Code will auto-retry until physics is ready

## Diagnostic Commands (if debugging)

If you want to manually check character physics state, you could add debug code:

```python
# Check if character has physics
lp = global_data.lobby_player
if hasattr(lp, 'sd') and hasattr(lp.sd, 'ref_character'):
    char = lp.sd.ref_character
    print("Character exists:", char is not None)
    if char:
        print("Character valid:", char.valid)
        print("Gravity:", lp.ev_g_gravity() if hasattr(lp, 'ev_g_gravity') else "N/A")
        print("On ground:", char.onGround() if hasattr(char, 'onGround') else "N/A")
        print("Position:", char.position)
```

## Architecture Comparison

### Before Fix (Broken)
```
LLobbyAvatar
└── ComCharacterLobby
    ├── Inherits: ComCharacterBase
    ├── Problem: init_prs() doesn't work properly
    ├── Result: self.sd.ref_character = None (never created)
    └── Physics: ✗ DISABLED
        ├── No collision.Character object
        ├── No gravity
        ├── No ground detection
        └── Character falls forever
```

### After Fix (Working)
```
LLobbyAvatar
└── ComCharacterLobby
    ├── Inherits: ComCharacterBase
    ├── Solution: Uses parent's init_from_dict() → _init_character() flow
    ├── Result: self.sd.ref_character = collision.Character object
    └── Physics: ✓ ENABLED
        ├── collision.Character created and registered
        ├── Gravity applied (980 units/s²)
        ├── Ground detection working
        └── Fallback floor (y=23.6) catches if no scene collision
```

## Expected Log Timeline

### T+0s: Game loads
- Waiting for scene collision setup

### T+1-2s: Scene initialized
- Lobby player created
- Character physics component initialized

### T+2s: Screenshot taken
- Auto-screenshot captured
- Uploaded to Discord

### T+2-3s: First clamp iteration
- Physics check performed
- Ground detection raycast
- Console shows diagnostic messages

### T+3s+: Continuous monitoring
- Every 0.2s: Ground check and potential clamping
- Only logs on errors or first iteration

## What Each Log Message Means

| Message | Meaning |
|---------|---------|
| `[Physics Check] Character object exists, valid=True` | ✓ Good - Physics system ready |
| `[Physics Check] Character has gravity: 980.0` | ✓ Good - Gravity enabled |
| `[Clamp] Ground detected via raycast at y=23.5` | ✓ Good - Found real ground collision |
| `[Clamp] No ground found via raycast, using fallback floor y=23.6` | ⚠️ OK - Using fallback (lobby may lack collision) |
| `[Clamp] Raycast error: ...` | ⚠️ OK - Fallback will be used |
| `[Physics Check] Character object exists, valid=False` | ✗ Bad - Physics didn't initialize |
| `[Clamp] ERROR: lobby_player is None` | ✗ Bad - Character entity not created |

## Performance Impact

- **Per-frame overhead:** Minimal (character physics handled by engine)
- **Grounding code:** Runs every 0.2s (lightweight raycast + teleport if needed)
- **Memory:** Character object ~1-2 KB additional
- **Expected FPS impact:** None (physics engine is optimized)

## Success Criteria

Fix is working when ALL of these are true:
1. ✓ Character spawns in lobby
2. ✓ Character does NOT fall infinitely
3. ✓ Console shows `[Physics Check] Character object exists, valid=True`
4. ✓ Console shows either:
   - `[Clamp] Ground detected via raycast` OR
   - `[Clamp] No ground found via raycast, using fallback floor`
5. ✓ Character position stays consistent over time
6. ✓ Character visual matches position in physics system

## If Fix Doesn't Work

Contact support with:
1. Full console output (especially [Physics Check] and [Clamp] messages)
2. Character position at time of issue
3. Screenshot of character position in lobby
4. Any error messages (including traceback)

This will help determine if the issue is:
- Physics initialization failure (ComCharacterLobby problem)
- Lobby scene missing collision (scene setup problem)
- Fallback floor height incorrect (needs adjustment)
- Different root cause (unexpected issue)
