# Character Physics Fix - Visual Guide

## Problem → Solution → Result

```
┌─────────────────────────────────────────────────────────────────┐
│ BEFORE FIX                                                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Lobby Scene                                                   │
│   ───────────────────────────────────────────────               │
│   Terrain/Floor (LAND_GROUP collision)                          │
│   ↓                                                             │
│   Empty Space (no character physics)                            │
│   ↓↓↓↓ FALLING FOREVER ↓↓↓↓                                     │
│   LLobbyAvatar                                                  │
│   └─ ComCharacterLobby                                          │
│      └─ self.sd.ref_character = None  ❌                         │
│         (No collision.Character object)                        │
│         (No gravity)                                           │
│         (No ground detection)                                  │
│   ↓↓↓↓ FALLING THROUGH FLOOR ↓↓↓↓                              │
│   ∞ Infinite Void                                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

                            ↓↓↓ FIX APPLIED ↓↓↓

┌─────────────────────────────────────────────────────────────────┐
│ AFTER FIX                                                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Lobby Scene                                                   │
│   ───────────────────────────────────────────────               │
│   Terrain/Floor (LAND_GROUP collision)                          │
│   ↓                                                             │
│   [=========== CHARACTER STANDING ============]                 │
│   LLobbyAvatar                                                  │
│   └─ ComCharacterLobby                                          │
│      └─ self.sd.ref_character = collision.Character  ✅         │
│         ├─ Registered with scene.scene_col                     │
│         ├─ Gravity enabled (980 units/s²)                      │
│         ├─ Ground detection working                            │
│         └─ Collision response active                           │
│   ↓                                                             │
│   [Ground/Terrain - Character Stops Here]                      │
│                                                                 │
│   Character: STANDING ✅ NOT FALLING ✅                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Initialization Flow Diagram

```
BEFORE FIX:
───────────

LLobbyAvatar created
    ↓
ComCharacterLobby.__init__()
    ↓
on_init_complete()
    ↓
init_prs() called
    ↓
try to access self.sd.ref_character
    ↓
❌ CRASH/ERROR: ref_character is None!
   (Never created because _init_character() not called)


AFTER FIX:
──────────

LLobbyAvatar created
    ↓
ComCharacterLobby (inherits from ComCharacterBase)
    ↓
init_from_dict() [INHERITED - called by framework]
    ↓
_init_character() [INHERITED - called by init_from_dict()]
    ├─ Create collision.Character(width, height, stepheight)
    ├─ self.sd.ref_character = character [SET!]
    ├─ Register: scene.scene_col.add_character(character)
    ├─ Configure collision groups
    ├─ Enable physics callbacks
    ├─ Call: self.init_prs() [POLYMORPHIC - calls child version]
    │   └─ init_prs() [OVERRIDDEN by ComCharacterLobby]
    │       └─ Set position from lobby config
    ├─ Initialize callbacks
    └─ Reset physics attributes
    ↓
Character READY with PHYSICS
    ├─ ✅ collision.Character object exists
    ├─ ✅ Registered with scene_col
    ├─ ✅ Gravity enabled
    ├─ ✅ Ground detection active
    └─ ✅ Correct position set
```

## Physics Simulation Loop

```
EACH FRAME (every ~0.033 seconds):
─────────────────────────────────

┌─────────────────────────────────┐
│ 1. Apply Gravity                │
│    verticalVelocity -= 9.8 * dt │
└────────────┬────────────────────┘
             ↓
┌─────────────────────────────────┐
│ 2. Get Walk Input               │
│    from user/controller         │
└────────────┬────────────────────┘
             ↓
┌─────────────────────────────────┐
│ 3. Physics Simulation           │
│    (scene_col.tick())           │
│    ├─ Raycast downward          │
│    ├─ Check LAND_GROUP collision│
│    ├─ Update position           │
│    └─ Handle collisions         │
└────────────┬────────────────────┘
             ↓
┌─────────────────────────────────┐
│ 4. Ground Detection             │
│    if LAND_GROUP hit:           │
│      onGround() = True          │
│      character stops            │
│    else:                        │
│      onGround() = False         │
│      character falling          │
└────────────┬────────────────────┘
             ↓
┌─────────────────────────────────┐
│ 5. Update Animation             │
│    if onGround:                 │
│      Play walking anim          │
│    else:                        │
│      Play falling anim          │
└─────────────────────────────────┘

BACKUP GROUNDING (every 0.2 seconds):
─────────────────────────────────────

┌─────────────────────────────────┐
│ 1. Raycast Downward             │
│    from character position      │
│    down 500 units               │
└────────────┬────────────────────┘
             ↓
        IF HIT LAND_GROUP:
             ↓
    ┌───────────────────────────┐
    │ Ground found at Y=ground_y│
    │ Target Y = ground_y +     │
    │            STAND_HEIGHT + │
    │            0.2            │
    └───────────────┬───────────┘
                    ↓
        IF CURRENT Y < TARGET Y:
                    ↓
        ┌───────────────────────┐
        │ Teleport up to target │
        │ (prevent sinking)     │
        └───────────────────────┘
             
        IF NO HIT (no LAND_GROUP):
             ↓
    ┌───────────────────────────┐
    │ Use fallback floor:       │
    │ Target Y = 23.6 +         │
    │           STAND_HEIGHT +  │
    │           0.2             │
    └───────────────┬───────────┘
                    ↓
        IF CURRENT Y < TARGET Y:
                    ↓
        ┌───────────────────────┐
        │ Teleport up to floor  │
        │ (prevent falling)     │
        └───────────────────────┘
```

## LAND_GROUP Composition

```
LAND_GROUP = 256 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 100 | 101

Bit 256 (Bit 0):  GROUP_STATIC_SHOOTUNIT (Static terrain, buildings)
Bit 3:            DIRT surfaces
Bit 4:            GRASS surfaces
Bit 5:            METAL objects
Bit 6:            SAND surfaces
Bit 7:            STONE surfaces
Bit 8:            (Intermediate material)
Bit 9:            WOOD objects
Bit 10:           BUILDINGS, walls
Bit 11:           GLASS surfaces
Bit 12:           SLOPES
Bit 100:          TERRAIN/PLATFORM surfaces
Bit 101:          ROADS

Result: Everything solid that player can walk on
        = Natural terrain + buildings + platforms + special surfaces
```

## Character Object Architecture

```
collision.Character
├─ Physics Parameters:
│  ├─ width: 1.0 (shoulder width)
│  ├─ height: 2.0 (head to feet)
│  └─ stepheight: 0.5 (can climb stairs up to 0.5 high)
│
├─ Collision Parameters:
│  ├─ padding: 0.05
│  ├─ addedMargin: 0.02
│  ├─ maxSlope: 45 degrees
│  └─ smoothFactor: 0.5
│
├─ Physics State (per-frame):
│  ├─ position: (x, y, z)
│  ├─ verticalVelocity: current downward speed
│  ├─ onGround: bool (touching terrain?)
│  ├─ canJump: bool (can jump?)
│  └─ getFootPosition: where feet are
│
├─ Input Control:
│  ├─ setWalkDirection(vector3) - movement
│  ├─ setJumpSpeed(speed) - jump
│  ├─ teleport(position) - instant move
│  └─ setGravity(value) - control gravity
│
└─ Registration:
   scene.scene_col.add_character(this)
   └─ Now physics simulation affects this character
```

## Scene Collision API

```
scene.scene_col
├─ hit_by_ray(start, end, exclude_id, group, mask, filter_type)
│  │
│  ├─ Input:
│  │  ├─ start: raycast start position
│  │  ├─ end: raycast end position (usually below start)
│  │  ├─ exclude_id: don't hit this object ID
│  │  ├─ group: which collision bits to search for
│  │  ├─ mask: filter collision bits
│  │  └─ filter_type: INCLUDE_FILTER or EQUAL_FILTER
│  │
│  └─ Output: (hit_bool, hit_point, normal, fraction, color, obj)
│
├─ add_character(character)
│  ├─ Purpose: Register character for physics simulation
│  └─ Result: Physics engine updates position each frame
│
├─ remove_character(character)
│  ├─ Purpose: Remove character from physics
│  └─ Result: Character no longer affected by gravity/physics
│
├─ static_test(col_obj, group, mask, filter)
│  ├─ Purpose: Check if collision object overlaps terrain
│  └─ Result: True/False
│
└─ sweep_test(col_obj, start, end, group, mask, filter)
   ├─ Purpose: Move object and check for collisions
   └─ Result: (hit_bool, hit_point, normal, fraction)
```

## Console Output Timeline

```
T=0.0s  Game loads
        ↓
        Initializing systems...

T=1.0s  Lobby scene loaded
        ↓
        Waiting for player initialization...

T=2.0s  AUTO-SCREENSHOT
        ├─ [Screenshot] Captured at 1280x720
        ├─ [Screenshot] Saved to temp file
        └─ [Screenshot] Sent to Discord webhook

T=2.0s  GROUNDING STARTS
        ├─ Starting continuous ground clamp...
        
T=2.1s  FIRST CLAMP ITERATION
        ├─ [Physics Check] Character object exists, valid=True ✅
        ├─ [Physics Check] Character has gravity: 980.0 ✅
        ├─ [Clamp] Ground detected via raycast at y=23.5 ✅
        │  OR
        ├─ [Clamp] No ground found via raycast, using fallback y=23.6 ⚠️
        │
        └─ Character GROUNDED - No more falling!

T=2.3s+ ONGOING MONITORING
        ├─ Every 0.2s: Raycast check
        ├─ If character still at correct height: silent (OK)
        ├─ If character sinking: teleport up (recovering)
        └─ Only logs on first iteration and errors
```

## Comparison: Before vs After

```
┌──────────────────┬─────────────────────┬─────────────────────┐
│ Aspect           │ BEFORE (Broken)     │ AFTER (Fixed)       │
├──────────────────┼─────────────────────┼─────────────────────┤
│ Physics Enabled  │ ❌ NO               │ ✅ YES              │
│ Gravity Working  │ ❌ NO               │ ✅ YES (980 u/s²)   │
│ Ground Detect    │ ❌ NO               │ ✅ YES (raycast)    │
│ Falls Through    │ ✅ YES (∞)         │ ❌ NO (stops)       │
│ Can Walk         │ ❌ NO (no physics)  │ ✅ YES (real)       │
│ Can Jump         │ ❌ NO (no gravity)  │ ✅ YES (with grav)  │
│ Can Climb        │ ❌ NO (no physics)  │ ✅ YES (step=0.5)   │
│ Console Output   │ No diagnostics      │ Physics check logs  │
│ Character Model  │ Just visual         │ Physics-based       │
│ Animation        │ Static/frozen       │ Dynamic            │
│ Realism          │ ❌ Poor            │ ✅ Good            │
└──────────────────┴─────────────────────┴─────────────────────┘
```

## Error States

```
ERROR STATE 1: Physics Check Fails
───────────────────────────────────
Console shows:
  [Physics Check] Character object exists, valid=False

Meaning: Character object not created
Action: Check ComCharacterLobby.init_prs() is called properly

ERROR STATE 2: No LAND_GROUP Collision
──────────────────────────────────────
Console shows:
  [Clamp] No ground found via raycast, using fallback y=23.6
  (repeating)

Meaning: Lobby scene has no collision geometry
Action: Character uses fallback floor (still works, but no real walking)

ERROR STATE 3: Wrong Fallback Height
─────────────────────────────────────
Character appears sinking through visual floor
OR floating above visual floor

Meaning: Fallback floor height (23.6) doesn't match scene
Action: Adjust lobby_floor_y = 23.6 in grounding code
```

## Success State

```
✅ EVERYTHING WORKING
──────────────────

Console Output:
  [Physics Check] Character object exists, valid=True
  [Physics Check] Character has gravity: 980.0
  [Clamp] Ground detected via raycast at y=23.5

Visual Result:
  ✅ Character at spawn location
  ✅ Character not falling
  ✅ Character position matches where you see it
  ✅ Character doesn't sink into floor
  ✅ Character can interact with lobby (if supported)

Physics State:
  ✅ collision.Character object exists
  ✅ Registered with scene.scene_col
  ✅ Gravity = 980.0 units/s²
  ✅ onGround() = True (standing)
  ✅ LAND_GROUP collision detected
```

---

**Visual Guide Complete**  
For more details, see [README.md](README.md)
