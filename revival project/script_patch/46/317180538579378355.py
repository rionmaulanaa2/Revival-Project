# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/part_sys/Concert/ConcertScnExportTools.py


def format_number--- This code section failed: ---

   2       0  LOAD_GLOBAL           0  'round'
           3  LOAD_GLOBAL           1  'is_integer'
           6  CALL_FUNCTION_2       2 
           9  STORE_FAST            1  'rounded_num'

   3      12  LOAD_FAST             1  'rounded_num'
          15  LOAD_ATTR             1  'is_integer'
          18  CALL_FUNCTION_0       0 
          21  POP_JUMP_IF_FALSE    34  'to 34'
          24  LOAD_GLOBAL           2  'int'
          27  LOAD_FAST             1  'rounded_num'
          30  CALL_FUNCTION_1       1 
          33  RETURN_END_IF    
        34_0  COME_FROM                '21'
          34  LOAD_FAST             1  'rounded_num'
          37  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_2' instruction at offset 6


def out_vec3(pos):
    if pos:
        return '[%s, %s, %s]' % (format_number(pos.x), format_number(pos.y), format_number(pos.z))
    else:
        return str(None)


def export_scene_spaceobject(scene_path='scene/znq/znq.scn', postfix='gim'):
    print 'Exporting scene spaceobjects'
    import world
    import math3d
    import math
    if scene_path:
        scn = world.scene()
        scn.load(scene_path, None, False)
        world.set_active_scene(scn)
        cam = scn.create_camera(True)
        cam.world_position = math3d.vector(24, 1, -566)
    if postfix == 'sfx':
        objs = world.get_active_scene().get_sfxes()
    else:
        objs = world.get_active_scene().get_models()
    if len(objs) == 0:
        print 'NO SFXSSSSSS'
    for obj in objs:
        if obj.get_parent() is not None:
            continue
        pos = obj.world_position
        rot = math3d.matrix_to_euler(obj.world_rotation_matrix)
        rot_degs = math3d.vector(math.degrees(rot.x), math.degrees(rot.y), math.degrees(rot.z))
        scale = obj.world_scale
        if abs(rot.x) < 0.0001 and abs(rot.z) < 0.0001:
            print 'sfx %s %s\t[%s, %s, %s]' % (obj.name, obj.filename, out_vec3(pos), format_number(math.degrees(rot.y)), out_vec3(scale))
        else:
            print 'sfx %s %s\t[%s, %s, %s]' % (obj.name, obj.filename, out_vec3(pos), out_vec3(rot_degs), out_vec3(scale))

    return


export_scene_spaceobject()

def convert_lyric_formato_text():
    a = '\n    [00:25:07]1600058\n    [00:03:11]1600059\n    [00:07:02]1600060\n    [00:10:04]1600061\n    [00:12:12]1600062\n    [00:15:02]1600063\n    [00:18:28]1600064\n    [00:21:28]1600065\n    '
    import re
    pattern = '\\[(\\d{2}:\\d{2}):(\\d{2})\\](\\d+)'

    def convert_base(match):
        num = int(match.group(2))
        print ('num', num)
        return '[' + match.group(1) + '.' + '%03d' % int(num / 30.0 * 1000) + ']' + match.group(3)

    result = re.sub(pattern, convert_base, a)
    print result