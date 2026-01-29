# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/utils/render_utils.py
from __future__ import absolute_import
from __future__ import print_function
from six.moves import range
import game3d
import render
SEMI_TRANSPARENT_MTG = 'character/11/2000/11_character_stealth.mtg'
TRANSPARENT_MTG = render.material_group_data(SEMI_TRANSPARENT_MTG)
EXCLUDE_MESH_NAME = set(('hit', ))

def set_semi_transparent(model, enable):
    if not model:
        return
    mesh_count = model.get_submesh_count()
    handler = enable_semi_transparent if enable else disable_semi_transparent
    for mesh_idx in range(0, mesh_count):
        mesh_name = model.get_submesh_name(mesh_idx)
        if mesh_name in EXCLUDE_MESH_NAME:
            model.set_submesh_visible(mesh_idx, False)
        handler(model, mesh_idx)


def enable_semi_transparent(model, mesh_idx):
    print('TRANSPARENT_MTG is', TRANSPARENT_MTG)
    model.set_material_group_data(TRANSPARENT_MTG, mesh_idx)


def disable_semi_transparent(model, mesh_idx):
    model.set_material_group_data(None, mesh_idx)
    return