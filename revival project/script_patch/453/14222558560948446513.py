# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/part_sys/Concert/ExtraCopyScreen.py
from __future__ import absolute_import
from __future__ import print_function
import math3d
import math
import time
import cclive
import render
import game3d
import os
import C_file
from random import randint
from logic.vscene.part_sys.Concert.ConcertMVMgr import s_tv_info, s_mv_model
_HASH_DIFFUSE = game3d.calc_string_hash('Tex0')

class ExtraCopyScreen(object):

    def __init__(self, prs_info=s_tv_info, model_path=s_mv_model):
        self.is_destroyed = False
        self.mv_model = None
        self.mv_model_vis = False
        self.mv_wait_model = None
        self.mv_wait_model_vis = False
        self.render_texture = None
        self.prs_info = prs_info
        self.model_path = model_path
        self.process_event(True)
        return

    def destroy(self):
        self.is_destroyed = True
        self.process_event(False)
        self.render_texture = None
        if self.mv_model and self.mv_model.valid:
            self.mv_model.destroy()
        self.mv_model = None
        if self.mv_wait_model and self.mv_wait_model.valid:
            self.mv_wait_model.destroy()
        self.mv_wait_model = None
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_concert_copy_mv_model_visible': self.update_copy_mv_model_visible,
           'update_concert_copy_kv_model_visible': self.update_copy_kv_mode_visible,
           'bind_concert_copy_mv_model_tex': self.bind_copy_mv_model_tex,
           'bind_concert_copy_kv_model_pic': self.refresh_kv_pic
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def create_mv_model(self):

        def create_cb(model):
            if self.is_destroyed:
                return
            self.mv_model = model
            if game3d.get_platform() == game3d.PLATFORM_ANDROID and cclive.support_hardware_decoder():
                model.all_materials.set_technique(1, 'shader/g93shader/effect_g93_cclive.nfx::TShader')
            rot = self.prs_info[0][1]
            rot_matrix = math3d.euler_to_matrix(math3d.vector(math.pi * rot[0] / 180.0, math.pi * rot[1] / 180.0, math.pi * rot[2] / 180.0))
            model.world_rotation_matrix = rot_matrix
            model.scale = math3d.vector(*self.prs_info[0][2])
            self.mv_model.visible = self.mv_model_vis
            if self.render_texture:
                self.mv_model.all_materials.set_texture(_HASH_DIFFUSE, 'Tex0', self.render_texture)

        global_data.model_mgr.create_model_in_scene(self.model_path, math3d.vector(*self.prs_info[0][0]), on_create_func=create_cb)

        def create_cb_mv_wait(model):
            if self.is_destroyed:
                return
            self.mv_wait_model = model
            rot = self.prs_info[0][1]
            rot_matrix = math3d.euler_to_matrix(math3d.vector(math.pi * rot[0] / 180.0, math.pi * rot[1] / 180.0, math.pi * rot[2] / 180.0))
            model.world_rotation_matrix = rot_matrix
            model.scale = math3d.vector(*self.prs_info[0][2])
            model.visible = self.mv_wait_model_vis

        global_data.model_mgr.create_model_in_scene(self.model_path, math3d.vector(*self.prs_info[0][0]), on_create_func=create_cb_mv_wait)

    def refresh_kv_pic(self, kv_pic):
        if self.mv_wait_model and self.mv_wait_model.valid:
            tex = render.texture(kv_pic)
            self.mv_wait_model.all_materials.set_texture(_HASH_DIFFUSE, 'Tex0', tex)
            self.cur_kv_pic = kv_pic

    def update_copy_mv_model_visible(self, vis):
        self.mv_model_vis = vis
        if self.mv_model and self.mv_model.valid:
            self.mv_model.visible = vis

    def update_copy_kv_mode_visible(self, vis):
        self.mv_wait_model_vis = vis
        if self.mv_wait_model and self.mv_wait_model.valid:
            self.mv_wait_model.visible = vis

    def bind_copy_mv_model_tex(self, render_tex):
        self.render_texture = render_tex
        if self.mv_model and self.mv_model.valid:
            self.mv_model.all_materials.set_texture(_HASH_DIFFUSE, 'Tex0', render_tex)