# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/hiding_edit.py
from __future__ import absolute_import
import game
from common.cfg import confmgr
model_list = []

def on_add_monster(monster_id):
    global model_list
    import world
    import common.utilities
    import math3d
    if not global_data.player or not global_data.player.logic:
        return
    pos = global_data.player.logic.ev_g_model_position()
    rotation = global_data.player.logic.ev_g_model_rotation()
    monster_data = confmgr.get('monster_data', 'Monster', 'Content', str(monster_id))
    model_path = monster_data['ResPath']
    m = world.model(model_path, world.get_active_scene())
    m.position = pos
    m.world_rotation_matrix = rotation
    m.scale = math3d.vector(monster_data['ModelScale'], monster_data['ModelScale'], monster_data['ModelScale'])
    m.set_attr('model_name', str(monster_id))
    model_list.append(m)
    radian = common.utilities.vector_radian(m.world_rotation_matrix.forward)


def on_add_build(model_path, model_name):
    import world
    import common.utilities
    import math3d
    if not global_data.player or not global_data.player.logic:
        return
    pos = global_data.player.logic.ev_g_model_position()
    rotation = global_data.player.logic.ev_g_model_rotation()
    m = world.model(model_path, world.get_active_scene(), False)
    m.position = pos
    m.world_rotation_matrix = rotation
    m.set_attr('model_name', model_name)
    model_list.append(m)
    radian = common.utilities.vector_radian(m.world_rotation_matrix.forward)


def on_add_emailbox():
    on_add_build('model_new/scene/interact/4201_mailbox.gim', 'mailbox')


def on_add_phonebooth():
    on_add_build('model_new/scene/interact/4202_phonebooth.gim', 'phonebooth')


def on_add_trashcan1():
    on_add_build('model_new/scene\\interact/4204_trashcan_01.gim', 'trashcan01')


def on_add_trashcan2():
    on_add_build('model_new/scene\\interact/4204_trashcan_02.gim', 'trashcan02')


def on_del_build():
    if model_list:
        m = model_list.pop()
        m.remove_from_parent()


def on_output():
    import common.utilities
    import json
    output = {}
    all_index = {}
    for model in model_list:
        model_name = model.get_attr('model_name')
        index = all_index.get(model_name, 0)
        all_index[model_name] = index + 1
        radian = common.utilities.vector_radian(model.world_rotation_matrix.forward)
        pos = []
        pos.append(model.position.x)
        pos.append(model.position.y)
        pos.append(model.position.z)
        output[model_name + '_' + str(all_index[model_name])] = pos

    fp = open('../monster_list.py', 'w')
    fp.write('_reload_all = True\n')
    fp.write('data=\n')
    fp.write(json.dumps(output, indent=4))
    fp.close()
    global_data.game_mgr.show_tip('\xe6\x88\x90\xe5\x8a\x9f\xe8\xbe\x93\xe5\x87\xba\xe6\x80\xaa\xe7\x89\xa9\xe5\x88\x97\xe8\xa1\xa8', True)


def on_add_monster1():
    on_add_monster(9001)


def on_add_monster2():
    on_add_monster(9002)


def on_add_monster3():
    on_add_monster(9003)


def on_add_monster4():
    on_add_monster(9004)


handler_dic = {game.VK_NUM_1: on_add_monster1,
   game.VK_NUM_2: on_add_monster2,
   game.VK_NUM_3: on_add_monster3,
   game.VK_NUM_4: on_add_monster4,
   game.VK_NUM_SUB: on_del_build,
   game.VK_NUM_ADD: on_output
   }
from logic.gutils.pc_utils import skip_when_debug_key_disabled

@skip_when_debug_key_disabled
def key_handler(msg, keycode):
    if not global_data.player:
        return
    else:
        if global_data.freefly_camera_mgr and global_data.freefly_camera_mgr.is_enable():
            return
        func = handler_dic.get(keycode, None)
        if func:
            func()
        return


def register_keys():
    game.add_key_handler(game.MSG_KEY_DOWN, (
     game.VK_NUM_1, game.VK_NUM_2, game.VK_NUM_3, game.VK_NUM_4, game.VK_NUM_SUB, game.VK_NUM_ADD), key_handler)