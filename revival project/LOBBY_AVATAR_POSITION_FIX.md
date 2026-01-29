# Lobby Avatar Position Fix - Technical Reference

## Summary
Found complete information about how LLobbyAvatar (Unit with ComLobbyModel component) stores and accesses position, and how to prevent falling through the floor.

---

## 1. ComLobbyModel Component Location

**File Path:** [script_patch/526/4393565356253118274.py](script_patch/526/4393565356253118274.py)

**Embedded Original File:** `/Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_lobby_char/ComLobbyModel.py`

**Class:** `ComLobbyModel(UnitCom)` - Lines 38+

---

## 2. How LLobbyAvatar Stores and Accesses Position

### Position Storage
- **Position is stored on the MODEL object** (not directly on the Unit)
- The model is accessed via: `self._get_model()` → returns the 3D game model
- Position property: `model.world_position` (a math3d.vector)

### Key Position Methods in ComLobbyModel

| Method | Location | Purpose |
|--------|----------|---------|
| `get_pos()` | Line 666 | **Getter** - Returns model's `world_position` |
| `on_pos_changed(pos)` | Line 659 | **Event handler** - Sets model's `world_position` when Unit position changes |
| `get_model_position()` | Line 142 | **Alternative getter** - Returns `model.world_position` |

### Event Binding
```python
BIND_EVENT = {
    'E_POSITION': 'on_pos_changed',      # Unit position event → updates model position
    'G_POSITION': 'get_pos',             # Get current position from model
    'G_MODEL_POSITION': 'get_model_position',
    ...
}
```

---

## 3. Correct Way to Set Position of a Lobby Avatar

### Method 1: Set Position Directly on Unit (Recommended)
```python
# This triggers the event system which calls on_pos_changed()
unit.pos = math3d.vector(x, y, z)
```

### Method 2: Set Position on Wrapper (LLobbyAvatar)
```python
# Direct wrapper position setting
lobby_avatar.pos = math3d.vector(x, y, z)
```

### Method 3: Set Position Directly on Model (Low-level)
```python
model = lobby_avatar.logic.com_lobby_model._get_model()
if model:
    model.world_position = math3d.vector(x, y, z)
```

---

## 4. Velocity/Physics Attributes to Zero

### On Unit/Logic Object
```python
logic = getattr(lobby_player, 'logic', None)

# Zero horizontal and vertical velocity
if hasattr(logic, 'velocity'):
    logic.velocity = math3d.vector(0, 0, 0)
```

### On Wrapper (LLobbyAvatar)
```python
lp = global_data.lobby_player

# Zero wrapper velocity
if hasattr(lp, 'velocity'):
    lp.velocity = math3d.vector(0, 0, 0)
```

---

## 5. Complete Grounding Solution (from existing fix)

**File:** [script_patch/785/785_17524466876519882393.py](script_patch/785/785_17524466876519882393.py#L1050-L1120)

### Key Implementation Steps:

1. **Get Ground Height:**
   ```python
   from logic.gutils import scene_utils
   scn = global_data.game_mgr.get_cur_scene()
   y = scene_utils.get_ground_height(scn, (0, 0))
   ```

2. **Create Target Position (with buffer):**
   ```python
   import math3d
   target_y = y + 0.2  # Offset to prevent clipping
   target_pos = math3d.vector(0, target_y, 0)
   ```

3. **Set Position on Both Logic and Wrapper:**
   ```python
   logic = getattr(lobby_player, 'logic', None)
   if logic:
       logic.pos = target_pos  # Set on Unit first
   
   lobby_player.pos = target_pos  # Set on wrapper
   ```

4. **Zero Out Velocity (Critical):**
   ```python
   if hasattr(logic, 'velocity'):
       logic.velocity = math3d.vector(0, 0, 0)
   
   if hasattr(lobby_player, 'velocity'):
       lobby_player.velocity = math3d.vector(0, 0, 0)
   ```

---

## 6. Root Cause of Falling Through Floor

From the fix notes:
- **Root Cause:** LLobbyAvatar created by PartLobbyCharacter has **physics enabled**
- This causes the avatar to fall before proper positioning can occur
- The lobby scene collision must be fully ready before positioning
- Physics simulation can conflict with manual position setting

### Solution Pattern:
1. Wait for scene collision to be ready: `scene.scene_col`
2. Delay initialization to ensure physics system is stable
3. Set position **after** collision is ready, not before
4. Zero velocity immediately after position setting
5. Use both logic and wrapper position calls for redundancy

---

## 7. Event System

ComLobbyModel uses event binding for position:
- `E_POSITION` event triggers `on_pos_changed()` → updates model position
- `G_POSITION` request calls `get_pos()` → retrieves model position
- This means position changes on the Unit are automatically synchronized to the model

---

## 8. Related Components

**Lobby Avatar Components:** (from script_overview.txt)
- ComCharacterLobby
- ComAvatarUserData  
- **ComLobbyModel** ← Position handling
- ComSpringAnim
- ComWeaponLobby
- ComJumpLobby
- ComClimbLobby
- ComHairLogic

---

## Files Referenced

1. **ComLobbyModel**: [script_patch/526/4393565356253118274.py](script_patch/526/4393565356253118274.py)
2. **Falling Fix Implementation**: [script_patch/785/785_17524466876519882393.py](script_patch/785/785_17524466876519882393.py#L1022-L1120)
3. **Overview**: [notes/script_overview.txt](notes/script_overview.txt)

---

## Quick Reference

```python
# MINIMAL EXAMPLE: Ground a lobby avatar
import math3d
from logic.gutils import scene_utils

scn = global_data.game_mgr.get_cur_scene()
lp = global_data.lobby_player
logic = lp.logic

# Get ground position
y = scene_utils.get_ground_height(scn, (0, 0))
pos = math3d.vector(0, y + 0.2, 0)

# Set position
logic.pos = pos
lp.pos = pos

# Kill velocity
if hasattr(logic, 'velocity'):
    logic.velocity = math3d.vector(0, 0, 0)
if hasattr(lp, 'velocity'):
    lp.velocity = math3d.vector(0, 0, 0)
```
