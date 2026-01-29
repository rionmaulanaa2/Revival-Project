# Complete Collision System Architecture Explained

## 1. HOW COLLISION WORKS IN THIS ENGINE

### 1.1 Core Concept: Collision Groups (Bitmasks)

The engine organizes all collision objects into **groups** using bitmasks (bit flags):

```python
# From script_patch/928/10800259509576259540.py (collision_const.py)

# Individual bits represent collision types:
GROUP_STATIC_SHOOTUNIT = 256        # Bit 0 - Static terrain, buildings, immovable objects
TERRAIN_GROUP     = ... | 100       # Bit 100 - Natural terrain (dirt, grass, stone, etc.)
ROAD_GROUP        = ... | 101       # Bit 101 - Roads, platforms
DIRT_GROUP        = ... | 3         # Bit 3 - Dirt surfaces
GRASS_GROUP       = ... | 4         # Bit 4 - Grass surfaces
METAL_GROUP       = ... | 5         # Bit 5 - Metal objects
SAND_GROUP        = ... | 6         # Bit 6 - Sand surfaces
STONE_GROUP       = ... | 7         # Bit 7 - Stone surfaces
WOOD_GROUP        = ... | 9         # Bit 9 - Wood objects
BUILDING_GROUP    = ... | 10        # Bit 10 - Buildings, walls
GLASS_GROUP       = ... | 11        # Bit 11 - Glass surfaces
SLOPE_GROUP       = ... | 12        # Bit 12 - Slopes

# The COMPLETE LANDING GROUP (what player can walk on):
LAND_GROUP = GROUP_STATIC_SHOOTUNIT | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 100 | 101
           = 256 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 100 | 101
           = "Everything the player can walk on" (terrain, buildings, platforms, etc.)
```

**Why Bitmasks?** They allow fast collision queries:
- `hit_by_ray(..., LAND_GROUP, LAND_GROUP, ...)` → "Give me all terrain/ground objects below"
- `hit_by_ray(..., GROUP_SHOOTUNIT, LAND_GROUP, ...)` → "Give me hostile units on walkable ground"

### 1.2 Scene Collision System (scene.scene_col)

Every scene has a central collision manager (`scene.scene_col`) that:

1. **Stores collision objects** - All terrain, buildings, platforms registered here
2. **Manages character physics** - Gravity, velocity, ground detection
3. **Provides query APIs**:

```python
# Raycast query (primary ground detection method)
hit_result = scene.scene_col.hit_by_ray(
    start_pos,                    # Start position (usually character position)
    end_pos,                      # End position (usually below, e.g., -500)
    exclude_id,                   # Don't collide with object ID (0 = exclude none)
    group=LAND_GROUP,            # Check for objects in LAND_GROUP
    mask=LAND_GROUP,             # Filter to LAND_GROUP objects
    filter_type=INCLUDE_FILTER   # Include all LAND_GROUP objects
)
# Returns: (hit_bool, hit_point, normal, fraction, color, collision_obj)

# Static collision test (check if collision object overlaps terrain)
result = scene.scene_col.static_test(
    collision_object,
    group=LAND_GROUP,
    mask=LAND_GROUP,
    filter=INCLUDE_FILTER
)
# Returns: True if collision detected

# Dynamic collision sweep (move object and check for collisions)
result = scene.scene_col.sweep_test(
    collision_object,
    start_pos,
    end_pos,
    group=LAND_GROUP,
    mask=LAND_GROUP,
    filter=INCLUDE_FILTER
)
# Returns: (hit_bool, hit_point, normal, fraction)

# Register character for physics simulation
scene.scene_col.add_character(character)  # Now gravity/movement work

# Remove character physics
scene.scene_col.remove_character(character)
```

---

## 2. HOW CHARACTER WALKING WORKS (Physics Step-by-Step)

### 2.1 Character Creation and Registration

```python
# From ComCharacterBase._init_character() [script_patch/620, lines 229-243]

# 1. CREATE collision.Character object with physics parameters
character = collision.Character(
    width=1.0,        # Character width (shoulder width)
    height=2.0,       # Character height (head to feet)
    stepheight=0.5    # How high stairs character can climb
)

# 2. CONFIGURE physics properties
character.setYOffset(-height * 0.5)    # Center character capsule vertically
character.setPadding(0.05)             # Padding from collision surfaces
character.setAddedMargin(0.02)         # Extra margin for stability
character.setMaxSlope(math.radians(45))# Max slope angle (45 degrees = 45%)
character.setSmoothFactor(0.5)         # Position interpolation smoothness
character.enableLeaveOverlap(True)     # Allow exiting overlapping geometry

# 3. REGISTER with scene collision system
self.scene.scene_col.add_character(character)
# ⭐ THIS IS CRITICAL - Without this line, character has no physics!

# 4. SET collision groups
character.group = GROUP_CHARACTER_INCLUDE (bits 0-3, mainly bits 0-3)
character.filter = GROUP_CHARACTER_INCLUDE  # Can interact with LAND_GROUP

# 5. STORE reference for later use
self.sd.ref_character = character
```

### 2.2 Physics Simulation Each Frame

```
EVERY FRAME:
┌──────────────────────────────────────────────────────────────┐
│ 1. Apply gravity to character                               │
│    char_ctrl.verticalVelocity -= gravity * delta_time        │
│                                                               │
│ 2. Apply walk direction input                               │
│    char_ctrl.setWalkDirection(input_direction * speed)      │
│                                                               │
│ 3. Scene collision system performs physics step:            │
│    a) Check ground below character                          │
│       - Raycast downward to find LAND_GROUP collision       │
│       - If hit: place character on ground                   │
│       - If miss: character continues falling                │
│    b) Move character based on walk direction                │
│    c) Handle collision response (stop against walls, etc.)  │
│                                                               │
│ 4. Update character position                                │
│    character.physicalPosition = calculated_position         │
│                                                               │
│ 5. Check if on ground                                       │
│    if char_ctrl.onGround():                                │
│       - Play walking animation                              │
│       - Allow jumping                                       │
│    else:                                                     │
│       - Play falling animation                              │
│       - Disable jumping                                     │
└──────────────────────────────────────────────────────────────┘
```

### 2.3 Ground Detection API (How onGround() Works)

```python
# Character queries collision system:
is_on_ground = char_ctrl.onGround()  # Returns True if standing on LAND_GROUP

# Internally, engine does something like:
# 1. Raycast from character feet downward (short distance, e.g., 0.5 units)
# 2. Check if it hits any LAND_GROUP collision object
# 3. Return True if hit, False if not

# Other useful methods:
foot_position = char_ctrl.getFootPosition()     # Character's foot Y position
vertical_velocity = char_ctrl.verticalVelocity  # Current downward velocity
can_jump = char_ctrl.canJump()                  # Can jump (only if onGround)
jump_speed = char_ctrl.getJumpSpeed()           # Current jump velocity
```

---

## 3. LOBBY SCENE COLLISION (The Problem)

### 3.1 Lobby Avatar Structure

```
LLobbyAvatar (Lobby Player Model)
├── ComCharacterLobby (from script_patch/614)
│   └── Inherits from ComCharacterBase
│       BUT OVERRIDES init_prs() to ONLY set position
│       Does NOT call _init_character() properly!
├── ComAvatarUserData (user profile data)
├── ComLobbyModel (visual model)
└── Other animation/display components
```

### 3.2 ComCharacterLobby vs ComCharacterBase

#### ComCharacterBase (Battle Avatar - FULL PHYSICS)
```python
# script_patch/620/17485016098020089777.py

def init_prs(self):
    # ✓ Calls _init_character()
    # ✓ Creates collision.Character
    # ✓ Adds to scene.scene_col
    # ✓ Enables gravity, ground detection, collision
    # ✓ Character can walk, climb stairs, interact with terrain
    pass
```

#### ComCharacterLobby (Lobby Avatar - ANIMATION ONLY)
```python
# script_patch/614/3778584141950362127.py

class ComCharacterLobby(ComCharacterBase):
    def init_prs(self):
        # ✗ OVERRIDES parent's init_prs()
        # ✗ ONLY sets position from config
        # ✗ Does NOT call _init_character()
        # ✗ Character has NO collision.Character object
        # ✗ Character is just a visual model
        
        pos = confmgr.get('mecha_display', 'LobbyTransform', 'Content', 'character')
        self.sd.ref_character.physicalPosition = math3d.vector(pos['x'], pos['y'], pos['z'])
        self._yaw = confmgr.get('mecha_display', 'LobbyTransform', 'Content', 'character', 'yaw')
        # That's it! No physics setup!
```

### 3.3 Root Cause of Character Falling

```
⭐ THE CRITICAL ISSUE:

ComCharacterLobby.init_prs() tries to set position on self.sd.ref_character
BUT self.sd.ref_character is NEVER created (no _init_character() call)!

This means:
1. Character has NO collision.Character object
2. Character NOT registered with scene.scene_col
3. Character has NO gravity support (no physics)
4. Character has NO ground detection
5. Character is just a visual model floating in space

So the character falls because there's NO PHYSICS AT ALL, not because
there's no ground collision. It's like a wooden doll with no gravity
physics assigned to it.
```

### 3.4 Lobby Scene Collision Objects (Unknown Status)

The lobby scene `SCENE_JIEMIAN_COMMON` may or may not have LAND_GROUP collision objects:

```python
# HYPOTHESIS 1: Scene has no collision geometry
Lobby Scene = Just visual models, no collision layer
├── Visual models (character, furniture, walls - visual only)
└── No collision objects in LAND_GROUP
    → Raycast always returns miss
    → Character would fall through floor even with physics enabled

# HYPOTHESIS 2: Scene has collision geometry but avatar not using it
Lobby Scene = Has visual + collision layer
├── Visual models
├── Collision objects (LAND_GROUP) - but avatar not set up to detect them
└── Character not registered with scene_col
    → Ground exists but character can't see it (no physics)
    → Character falls anyway

# WHAT YOUR CODE IS DOING:
Using hit_by_ray to detect LAND_GROUP:
├── If hit: place character at ground_y
├── If miss: fallback to hardcoded y=23.6
└── Clamp every 0.2s with E_TELEPORT to keep character above floor
    → Works! Character appears to stand on floor
    → BUT: Artificial, not real physics-based walking
```

---

## 4. WHY CURRENT SOLUTION IS ARTIFICIAL

### 4.1 Current Approach (Your Code)
```python
# From script_patch/785, lines 1108-1340

# EVERY 0.2 seconds:
hit_result = scene.scene_col.hit_by_ray(
    char_pos,
    char_pos + (0, -500, 0),
    0,
    LAND_GROUP,
    LAND_GROUP,
    INCLUDE_FILTER
)

if hit_result[0]:  # If raycast hit ground
    ground_y = hit_result[1].y
else:  # If raycast missed
    ground_y = 23.6  # Fallback floor

# Teleport character to maintain position above floor
E_TELEPORT(character, pos=(x, ground_y + CHARACTER_STAND_HEIGHT + 0.2))

# ⭐ RESULT: Character is FROZEN in place at Y position
#    Not walking, not falling, just STUCK at calculated height
#    This prevents infinite falling but breaks natural movement
```

### 4.2 Why This Isn't Real Walking

```
Real Walking (Battle Avatar):
1. Character moves forward with gravity applied
2. Gravity pulls character down each frame
3. Collision system detects ground below
4. Character stops on ground (onGround() = True)
5. Walking animation plays naturally
6. Can climb stairs (gravity + character controller handles it)

Artificial Walking (Current Lobby):
1. Character has NO physics
2. Every 0.2s: Raycast for ground
3. Every 0.2s: Teleport to maintain height
4. Result: Character appears to stand but CAN'T:
   ✗ Walk smoothly (jerky teleport every 0.2s)
   ✗ Climb stairs (no gravity to follow slope)
   ✗ Jump (gravity disabled)
   ✗ Fall naturally when running off edge
   ✗ Respond to physics (just frozen in place)
```

---

## 5. WHAT NEEDS TO FIX LOBBY CHARACTER WALKING

### Option A: Give Lobby Avatar Full Physics (RECOMMENDED)

```python
# Modify ComCharacterLobby.init_prs() to call parent's _init_character()

class ComCharacterLobby(ComCharacterBase):
    def init_prs(self):
        # Call parent's _init_character() first
        super(ComCharacterLobby, self).init_prs()
        
        # THEN override position from lobby config
        pos = confmgr.get('mecha_display', 'LobbyTransform', 'Content', 'character')
        # Now character has physics AND correct starting position
        
        self._yaw = confmgr.get('mecha_display', 'LobbyTransform', 'Content', 'character', 'yaw')

# Result:
# ✓ Character has collision.Character object
# ✓ Character registered with scene.scene_col
# ✓ Gravity works
# ✓ Ground detection works
# ✓ Natural walking/climbing/jumping works
```

### Option B: Ensure Lobby Scene Has LAND_GROUP Collision

```python
# Verify lobby scene setup:
# 1. Scene file must include collision geometry layer
# 2. Floor/ground must be marked as LAND_GROUP (bits 0, 3-12, 100-101)
# 3. Buildings/walls must have collision objects
# 4. Without these, raycast will always miss

# Can verify by checking scene_col contents:
scene.scene_col.hit_by_ray(
    (0, 100, 0),           # From above
    (0, 0, 0),             # To floor
    0,
    LAND_GROUP,
    LAND_GROUP,
    INCLUDE_FILTER
)
# If returns False: Scene has no LAND_GROUP objects
```

### Option C: Hybrid Approach (Your Current Solution)

```python
# Keep raycast-based grounding
# + Add fallback floor when raycast misses
# - Character can't walk naturally (frozen by teleport)

# This prevents infinite falling but at cost of:
✗ No natural walking
✗ No climbing stairs
✗ No jumping
✗ Jerky movement (teleport every 0.2s)
```

---

## 6. CHARACTER WALKING - COMPLETE IMPLEMENTATION

### 6.1 How Engine Handles Walking Input

```python
# From ComCharacterBase._set_walk_direction() [script_patch/620]

def _set_walk_direction(self, walk_direction, ...)
    char_ctrl = self._get_character()
    if char_ctrl:
        # Apply walk direction to character physics
        char_ctrl.setWalkDirection(walk_direction)
        # Engine then:
        # 1. Applies velocity in that direction
        # 2. Checks collision with walls
        # 3. Handles ground response
        # 4. Updates position

# Input format: math3d.vector(x, 0, z) - direction * speed
```

### 6.2 How Engine Handles Stairs/Slopes

```python
# Character has stepheight parameter:
character = collision.Character(width=1.0, height=2.0, stepheight=0.5)

# This means:
# ✓ Can climb obstacles up to 0.5 units high
# ✓ Handles slopes with gravity automatically
# ✓ Slides down slopes when walking off edge
# ✓ All handled by physics engine, not manual code

# For slopes to work:
# 1. Slope geometry must be in scene collision (SLOPE_GROUP)
# 2. Character must have gravity enabled
# 3. Character must be registered with scene_col.add_character()
```

### 6.3 Debug Information (Understanding Movement State)

```python
# From ComCharacterBase debug output [script_patch/318, line 714]:

char_ctrl = self._get_character()

# Movement state:
print(char_ctrl.onGround())           # True = standing, False = falling
print(char_ctrl.getFootPosition())    # Y position of character's feet
print(char_ctrl.verticalVelocity)     # Current falling speed
print(char_ctrl.physicalPosition)     # Character's current 3D position

# Physics state:
print(self.ev_g_gravity())            # Gravity strength
print(char_ctrl.canJump())            # Can jump (only True if onGround)
print(char_ctrl.getJumpSpeed())       # Current jump speed (0 if not jumping)

# Input state:
print(walk_direction)                 # Current movement input
print(normalize_walk_direction)       # Normalized direction (0-1)
```

---

## 7. COLLISION CONSTANTS - COMPLETE REFERENCE

### Groups Used in Game

```python
# Character collision
GROUP_CHARACTER_INCLUDE = 15          # Character collision bits (0-3)

# Terrain/Ground types
GROUP_STATIC_SHOOTUNIT = 256          # Bit 0 - Static terrain/buildings
TERRAIN_GROUP = ... | 100             # Bit 100 - Natural terrain
ROAD_GROUP = ... | 101                # Bit 101 - Roads/platforms
DIRT_GROUP = ... | 3                  # Bit 3
GRASS_GROUP = ... | 4                 # Bit 4
METAL_GROUP = ... | 5                 # Bit 5
SAND_GROUP = ... | 6                  # Bit 6
STONE_GROUP = ... | 7                 # Bit 7
WOOD_GROUP = ... | 9                  # Bit 9
BUILDING_GROUP = ... | 10             # Bit 10
GLASS_GROUP = ... | 11                # Bit 11
SLOPE_GROUP = ... | 12                # Bit 12
ICE_GROUP = ... | 13                  # Bit 13
LAND_GROUP = 256 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 100 | 101

# Other objects
GROUP_SHOOTUNIT = STATIC | DYNAMIC    # All shootable units
GROUP_WATER_SHOOTUNIT = 8192          # Water bodies
GROUP_GRENADE = 4096                  # Grenades
GROUP_SHIELD = 2048                   # Shield objects
```

### Filter Types

```python
collision.INCLUDE_FILTER   # Include all objects matching group/mask
collision.EQUAL_FILTER     # Exact match on group only
collision.DEFAULT_FILTER   # Default engine filter
```

---

## 8. HOW TO VERIFY COLLISION SYSTEM WORKS

### 8.1 Check if Scene Has Ground

```python
# From your current patch:
hit_result = scene.scene_col.hit_by_ray(
    character_pos,
    character_pos + (0, -500, 0),  # Raycast 500 units down
    0,
    collision_const.LAND_GROUP,
    collision_const.LAND_GROUP,
    collision.INCLUDE_FILTER
)

if hit_result[0]:
    print("✓ Scene has LAND_GROUP collision objects!")
    print(f"  Ground at Y: {hit_result[1].y}")
else:
    print("✗ Scene has NO LAND_GROUP collision objects")
    print("  Lobby scene may be missing collision geometry")
```

### 8.2 Check if Character Has Physics

```python
char_ctrl = self.sd.ref_character

if char_ctrl and char_ctrl.valid:
    print("✓ Character object exists")
    print(f"  Height: {char_ctrl.height}")
    print(f"  Width: {char_ctrl.width}")
    print(f"  On ground: {char_ctrl.onGround()}")
    print(f"  Vertical velocity: {char_ctrl.verticalVelocity}")
    print(f"  Gravity: {self.ev_g_gravity()}")
else:
    print("✗ Character object NOT created or invalid")
    print("  Character missing collision.Character object")
```

### 8.3 Check Collision Registration

```python
# If character registered with scene_col:
# - scene_col.add_character() was called
# - Character can be affected by gravity
# - Ground detection works

# If character NOT registered:
# - No gravity
# - No ground detection
# - No collision response
```

---

## SUMMARY

**Your lobby character is falling because:**
1. ✗ `ComCharacterLobby` doesn't call `_init_character()`
2. ✗ No `collision.Character` object created
3. ✗ Not registered with `scene.scene_col`
4. ✗ No physics/gravity enabled
5. ✗ Just a visual model in space

**Current patch solution:**
- Raycasts for ground every 0.2s
- Teleports character to maintain height
- Prevents infinite falling ✓
- But breaks natural walking ✗

**To fix:**
- **Option A** (Best): Add full physics to `ComCharacterLobby` (call parent's `_init_character()`)
- **Option B**: Ensure lobby scene has LAND_GROUP collision objects
- **Option C** (Current): Keep fallback floor but accept limited movement
