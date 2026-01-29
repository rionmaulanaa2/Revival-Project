# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/soc_utils.py
from __future__ import absolute_import
from __future__ import print_function
import world
import math3d

def set_model_attach_soc(model, tag):
    if not global_data.use_soc:
        return
    model.set_attach_to_soc(tag)


debug_timer = None

def soc_debug_timer(enable, draw_occluder=False):
    global debug_timer
    if debug_timer:
        global_data.game_mgr.unregister_logic_timer(debug_timer)
    debug_timer = global_data.game_mgr.register_logic_timer(soc_debug, 3, (enable, draw_occluder), -1, 2)


def soc_debug(enable, draw_occluder=False):
    scn = global_data.game_mgr.scene
    model_list = scn.get_models()
    if enable:
        for model in model_list:
            if model.is_soc_occluder():
                model.enable_prez_transparent(True, 0.4)
                if draw_occluder:
                    color = 285277952
                    prim_type = 3
                    fvf = 66
                    index = model.get_soc_occluder_index()
                    vertex = model.get_soc_occluder_vertex()
                    t = model.world_transformation
                    vertex_out = []
                    line1 = t.right
                    line2 = t.up
                    line3 = t.forward
                    trans = t.translation
                    for v in vertex:
                        x = v[0]
                        y = v[1]
                        z = v[2]
                        x_ret = x * line1.x + y * line2.x + z * line3.x + trans.x
                        y_ret = x * line1.y + y * line2.y + z * line3.y + trans.y
                        z_ret = x * line1.z + y * line2.z + z * line3.z + trans.z
                        v_ret = (
                         x_ret, y_ret, z_ret, color)
                        vertex_out.append(v_ret)

                    pri = world.primitives(scn)
                    pri.create_primitives_indexed(prim_type, fvf, vertex_out, index)
            elif model.filename.find('_b.gim') != -1:
                model.enable_prez_transparent(True, 0.4)

    else:
        for model in model_list:
            if model.is_soc_occluder():
                model.enable_prez_transparent(True, 1.0)
            elif model.filename.find('_b.gim') != -1:
                model.enable_prez_transparent(True, 1.0)


debug_dis_timer = None

def soc_debug_dis_timer(enable):
    global debug_dis_timer
    if debug_dis_timer:
        global_data.game_mgr.unregister_logic_timer(debug_dis_timer)
    if enable:
        debug_dis_timer = global_data.game_mgr.register_logic_timer(soc_debug_dis, 1)


def soc_debug_dis():
    c_pos = global_data.game_mgr.scene.active_camera.world_position
    pos = global_data.player.logic.ev_g_position()
    dis = (c_pos - pos).length
    print(dis)