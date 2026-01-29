# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/GenLandscapeDiffuse.py
from __future__ import absolute_import
from __future__ import print_function
import game3d
import render
import os.path
from cocosui import cc
from common.utils.path import get_neox_dir
from logic.gutils.gen_compress_texture_utils import DiffuseRenderTarget
IDLE = 0
RENDERING = 1

class GenLandscapeDiffuse(object):

    def __init__(self):
        self._tex_size = (2048, 2048)
        self._tex1_size = tuple([ int(v * 0.5) for v in self._tex_size ])
        self.cur_gen_index = ''
        self.cur_compress_index = ''
        self.cur_landscape_indexes = [[], []]
        self.pending_compress_indexes = [[], []]
        self.complele_set = [
         set(), set()]
        self.diffuse_map = {0: {},1: {}}
        self.normal_map = {0: {},1: {}}
        self.compress_diffuse_map = {0: {},1: {}}
        self.compress_normal_map = {0: {},1: {}}
        self.diffuse_render_target = [
         None, None]
        self.compress_render_target = [None, None]
        self.compress_enable = False
        if True:
            self.compress_enable = True
        self._cur_state = IDLE
        self._cur_gen_type = 0
        self._compress_stage = 0
        self._rendering_count = 0
        self._ui = None
        self._last_src_tex = None
        self._last_dst_tex = None
        self.check_timer_id = None
        self.history_check_index0 = []
        self.history_check_index1 = []
        self.cache_history_limit_count = 5
        self._stopping = False
        return

    def destroy(self):
        self.unregister_timer()
        self._stopping = True
        for rto in self.diffuse_render_target:
            if not rto:
                continue
            rto.destroy()

        for rto in self.compress_render_target:
            if not rto:
                continue
            rto.destroy()

        self.diffuse_render_target = [None, None]
        self.compress_render_target = [None, None]
        if self._ui:
            self._ui.close()
        self._ui = None
        self._last_src_tex = None
        self._last_dst_tex = None
        self.cur_landscape_indexes = [[], []]
        self.pending_compress_indexes = [[], []]
        self.complele_set = [
         set(), set()]
        self.diffuse_map = {0: {},1: {}}
        self.normal_map = {0: {},1: {}}
        self.compress_diffuse_map = {0: {},1: {}}
        self.compress_normal_map = {0: {},1: {}}
        return

    def register_timer(self):
        from common.utils.timer import CLOCK
        self.unregister_timer()
        self.check_timer_id = global_data.game_mgr.get_logic_timer().register(func=self.check_landscape, interval=0.5, mode=CLOCK)

    def unregister_timer(self):
        if self.check_timer_id:
            global_data.game_mgr.get_logic_timer().unregister(self.check_timer_id)
        self.check_timer_id = None
        return

    def set_detail_diffuse(self, tag, index_key, tex):
        self.diffuse_map[tag][index_key] = tex

    def set_detail_normal(self, tag, index_key, tex):
        self.normal_map[tag][index_key] = tex
        if self.compress_enable:
            self.pending_compress_indexes[tag].append(index_key)
        else:
            scn = global_data.game_mgr.scene
            scn.landscape.set_detail_diffuse(index_key, self.diffuse_map[tag][index_key], tex)
            self._show_ui(self.diffuse_map[tag][index_key], tex)

    def set_detail_compress_diffuse(self, tag, index_key, tex):
        self.compress_diffuse_map[tag][index_key] = tex
        print('>>>> set_detail_compress_diffuse', tag, index_key)
        del self.diffuse_map[tag][index_key]

    def set_detail_compress_normal(self, tag, index_key, tex):
        self.compress_normal_map[tag][index_key] = tex
        print('>>>> set_detail_compress_normal', tag, index_key)
        del self.normal_map[tag][index_key]
        scn = global_data.game_mgr.scene
        scn.landscape.set_detail_diffuse(index_key, self.compress_diffuse_map[tag][index_key], tex)
        self._show_ui(self.compress_diffuse_map[tag][index_key], tex)

    def remove_detail_diffuse(self, tag, remove_set):
        scn = global_data.game_mgr.scene
        for index_key in remove_set:
            if index_key in self.complele_set[tag]:
                self.complele_set[tag].remove(index_key)
            if index_key in self.compress_diffuse_map[tag]:
                del self.compress_diffuse_map[tag][index_key]
            if index_key in self.compress_normal_map[tag]:
                del self.compress_normal_map[tag][index_key]
            if index_key in self.diffuse_map[tag]:
                del self.diffuse_map[tag][index_key]
            if index_key in self.normal_map[tag]:
                del self.normal_map[tag][index_key]
            scn.landscape.set_detail_diffuse(index_key, None, None)

        return

    def check_landscape(self):
        scn = global_data.game_mgr.scene
        checking_indexes0 = scn.landscape.get_cur_landscape_detail_indexes(0)
        checking_indexes1 = scn.landscape.get_cur_landscape_detail_indexes(1)
        self.history_check_index0.append(checking_indexes0)
        if len(self.history_check_index0) > self.cache_history_limit_count:
            self.history_check_index0.pop(0)
            cur_set = set(self.history_check_index0[0])
            for indexes in self.history_check_index0:
                cur_set &= set(indexes)

            add_set = cur_set - self.complele_set[0]
            self.cur_landscape_indexes[0] = list(add_set)
            remove_set = self.complele_set[0] - cur_set
            self.remove_detail_diffuse(0, remove_set)
        self.history_check_index1.append(checking_indexes1)
        if len(self.history_check_index1) > self.cache_history_limit_count:
            self.history_check_index1.pop(0)
            cur_set = set(self.history_check_index1[0])
            for indexes in self.history_check_index1:
                cur_set &= set(indexes)

            add_set = cur_set - self.complele_set[1] - set(set(self.cur_landscape_indexes[0]) | self.complele_set[0])
            self.cur_landscape_indexes[1] = list(add_set)
            remove_set = self.complele_set[1] - cur_set
            self.remove_detail_diffuse(1, remove_set)
        self.do_next_diffuse()

    def start(self):
        self.diffuse_render_target[0] = DiffuseRenderTarget(use_u32_tex=False, use_etc2_tex=False, size_scale=1, do_copy=False, do_save=False, use_main_camera=True, size=self._tex_size)
        self.diffuse_render_target[0]._render_count_limit = 1
        self.diffuse_render_target[1] = DiffuseRenderTarget(use_u32_tex=False, use_etc2_tex=False, size_scale=1, do_copy=False, do_save=False, use_main_camera=True, size=self._tex1_size)
        self.diffuse_render_target[1]._render_count_limit = 1
        if self.compress_enable:
            if game3d.get_platform() == game3d.PLATFORM_ANDROID:
                self.compress_render_target[0] = DiffuseRenderTarget(use_u32_tex=True, use_etc2_tex=True, size_scale=4, do_copy=True, do_save=False, size=self._tex_size)
                self.compress_render_target[1] = DiffuseRenderTarget(use_u32_tex=True, use_etc2_tex=True, size_scale=4, do_copy=True, do_save=False, size=self._tex1_size)
            else:
                self.compress_render_target[0] = DiffuseRenderTarget(use_u32_tex=False, use_etc2_tex=False, size_scale=1, do_copy=True, do_save=False, size=self._tex_size)
                self.compress_render_target[1] = DiffuseRenderTarget(use_u32_tex=False, use_etc2_tex=False, size_scale=1, do_copy=True, do_save=False, size=self._tex1_size)
            self.compress_render_target[0]._render_count_limit = 1
            self.compress_render_target[1]._render_count_limit = 1
        scn = global_data.game_mgr.scene
        scn.landscape.set_landscape_gen_diffuse_distance(0, 430)
        scn.landscape.set_landscape_gen_diffuse_distance(1, 860)
        self.register_timer()

    def do_next_diffuse(self, gen_first=True):
        scn = global_data.game_mgr.scene
        if scn and scn.valid:
            scn.landscape.set_cur_gen_landscape_index('')
        if self._stopping:
            return
        if self.is_compressing():
            return
        if self._cur_state != IDLE:
            return
        if gen_first:
            if self.cur_landscape_indexes[0]:
                self._do_next_diffuse(0)
                return
            if self.pending_compress_indexes[0]:
                self.try_compress()
                return
        else:
            if self.pending_compress_indexes[0]:
                self.try_compress()
                return
            if self.cur_landscape_indexes[0]:
                self._do_next_diffuse(0)
                return
        if gen_first:
            if self.cur_landscape_indexes[1]:
                self._do_next_diffuse(1)
                return
            if self.pending_compress_indexes[1]:
                self.try_compress()
                return
        else:
            if self.pending_compress_indexes[1]:
                self.try_compress()
                return
            if self.cur_landscape_indexes[1]:
                self._do_next_diffuse(1)
                return

    def _do_next_diffuse(self, index):
        import traceback
        print('>>> _do_next_diffuse', self.complele_set[index])
        scn = global_data.game_mgr.scene
        if self.cur_landscape_indexes[index]:
            self.cur_gen_index = self.cur_landscape_indexes[index].pop(-1)
            print('>>>> cur_landscape_indexes', index, self.cur_gen_index, self.cur_landscape_indexes[index])
        else:
            self.cur_gen_index = ''
        self._cur_gen_type = 0
        self._last_gen_type = self._cur_state
        if not self.cur_gen_index:
            return
        rt_scn = self.diffuse_render_target[index].get_scene()
        scn.landscape.set_OtherSceneContext(rt_scn)

        def render_landscape_and_copy():
            if self._stopping:
                return
            scn = global_data.game_mgr.scene
            checking_indexes0 = set(scn.landscape.get_cur_landscape_detail_indexes(0))
            checking_indexes1 = set(scn.landscape.get_cur_landscape_detail_indexes(1))
            checking_indexes1 = checking_indexes1 - checking_indexes0
            checking_indexes = checking_indexes0 if index == 0 else checking_indexes1
            if self.cur_gen_index not in checking_indexes:
                self._cur_state = IDLE
                self.do_next_diffuse(gen_first=True)
                return
            self._cur_state = RENDERING
            self._rendering_count = 0
            scn.landscape.set_cur_gen_landscape_index(self.cur_gen_index + '_{}'.format(self._cur_gen_type))

            def render_landscape_callback():
                print('>>>> chain_callback', self._cur_state, self.complele_set[index])
                cur_gen_landscape_index, is_finish = scn.landscape.get_cur_gen_landscape_index()
                print('>>>> cur_gen_landscape_index', self._cur_state, cur_gen_landscape_index, is_finish)
                if self._cur_state == RENDERING:
                    self._rendering_count += 1
                    if self._rendering_count > 3:
                        self.diffuse_render_target[index].stop_render_target()
                        self.remove_detail_diffuse(index, set([self.cur_gen_index]))

                        def delay():
                            self._cur_state = IDLE
                            self.do_next_diffuse(gen_first=True)

                        global_data.game_mgr.next_exec(delay)
                        return
                if self._cur_state == RENDERING and self.cur_gen_index and is_finish:
                    if self._rendering_count != 2:
                        print('>>>>--------- copy_texture 00000', self._rendering_count)
                        self.diffuse_render_target[index].stop_render_target()
                        self.remove_detail_diffuse(index, set([self.cur_gen_index]))

                        def delay():
                            self._cur_state = IDLE
                            self.do_next_diffuse(gen_first=True)

                        global_data.game_mgr.next_exec(delay)
                        return
                    self.diffuse_render_target[index].stop_render_target()
                    print('>>>>--------- copy_texture', self._rendering_count)
                    render.texture.copy_texture(self.diffuse_render_target[index].get_rt_holder().tex, self.diffuse_render_target[index].get_dst_texture(), 0, 0, 0, 0, 0, 0, 0, 0)

                    def delay2():
                        if self._cur_gen_type == 0:
                            self._cur_gen_type = 1
                            self.set_detail_diffuse(index, self.cur_gen_index, self.diffuse_render_target[index].get_dst_texture())
                            self.diffuse_render_target[index].create_dst_texture()
                            global_data.game_mgr.next_exec(render_landscape_and_copy)
                        elif self._cur_gen_type == 1:
                            self.set_detail_normal(index, self.cur_gen_index, self.diffuse_render_target[index].get_dst_texture())
                            self.diffuse_render_target[index].create_dst_texture()
                            self.complele_set[index].add(self.cur_gen_index)
                            if self.cur_gen_index in self.cur_landscape_indexes[index]:
                                self.cur_landscape_indexes[index].remove(self.cur_gen_index)

                            def delay():
                                self._cur_state = IDLE
                                self.do_next_diffuse(gen_first=True)

                            global_data.game_mgr.next_exec(delay)

                    delay2()

            dirpath = get_neox_dir() + '/res/'
            self.diffuse_render_target[index].do_copy = False
            self.diffuse_render_target[index].do_save = False
            self.diffuse_render_target[index].create_landscape_diffuse(os.path.join(dirpath, 'landscape_{}_{}.png'.format(index, self.cur_gen_index)), render_landscape_callback)

        render_landscape_and_copy()

    def is_compressing(self):
        return self._compress_stage != 0

    def try_compress(self):
        if self._compress_stage != 0:
            return
        tag = 0
        pending_compress_indexes = self.pending_compress_indexes[0]
        if not pending_compress_indexes:
            tag = 1
            pending_compress_indexes = self.pending_compress_indexes[1]
        if not pending_compress_indexes:
            return
        index_key = pending_compress_indexes.pop()
        self.do_next_compress(tag, index_key)

    def do_next_compress(self, tag, index_key):
        if index_key not in self.diffuse_map[tag]:
            global_data.game_mgr.next_exec(lambda : self.do_next_diffuse(gen_first=False))
            return
        print('>>>> do_next_compress 000 xxxxxxxxxxxxxxxx', index_key)
        self._compress_stage = 1

        def compress_callback():
            self.compress_render_target[tag].stop_render_target()
            if self._stopping:
                return
            print('>>>> compress_callback', self._compress_stage)
            if self._compress_stage == 1:
                self._compress_stage = 2
                print('>>>> do_next_compress 111', index_key)
                if index_key not in self.normal_map[tag]:
                    self._compress_stage = 0
                    global_data.game_mgr.next_exec(lambda : self.do_next_diffuse(gen_first=False))
                    return
                self.set_detail_compress_diffuse(tag, index_key, self.compress_render_target[tag].get_dst_texture())
                self.compress_render_target[tag].create_dst_texture()

                def delay():
                    if index_key not in self.normal_map[tag]:
                        self._compress_stage = 0
                        global_data.game_mgr.next_exec(lambda : self.do_next_diffuse(gen_first=False))
                        return
                    self.compress_render_target[tag].do_copy = True
                    self.compress_render_target[tag].create_diffuse(self.normal_map[tag][index_key], '', compress_callback)

                global_data.game_mgr.next_exec(delay)
            elif self._compress_stage == 2:
                self._compress_stage = 0
                print('>>>> do_next_compress 222', index_key)
                if index_key not in self.compress_diffuse_map[tag]:
                    global_data.game_mgr.next_exec(lambda : self.do_next_diffuse(gen_first=False))
                    return
                self.set_detail_compress_normal(tag, index_key, self.compress_render_target[tag].get_dst_texture())
                self.compress_render_target[tag].create_dst_texture()
                global_data.game_mgr.next_exec(lambda : self.do_next_diffuse(gen_first=False))

        self.compress_render_target[tag].do_copy = True
        self.compress_render_target[tag].create_diffuse(self.diffuse_map[tag][index_key], '', compress_callback)

        def delay():
            self.compress_render_target[tag].do_copy = True
            self.compress_render_target[tag].create_diffuse(self.diffuse_map[tag][index_key], '', compress_callback)

    def show_ui(self):
        if not self._last_src_tex:
            return
        src = self._last_src_tex
        dst = self._last_dst_tex
        if not self._ui or not (self._ui.panel and self._ui.panel.isValid()):
            ui = global_data.ui_mgr.create_simple_dialog('battle/empty')
            self._ui = ui
        ui = self._ui
        for child in ui.panel.GetChildren():
            child.RemoveFromParent()

        rt = cc.Texture2D.createWithITexture(src)
        sprite = cc.Sprite.createWithTexture(rt)
        rt = cc.Texture2D.createWithITexture(dst)
        sprite2 = cc.Sprite.createWithTexture(rt)
        scale = 2048.0 / self._tex_size[0]
        ui.panel.addChild(sprite)
        sprite.setPosition(cc.Vec2(330, 375))
        sprite.setScale(0.3 * scale)
        ui.panel.addChild(sprite2)
        sprite2.setPosition(cc.Vec2(980, 375))
        sprite2.setScale(0.3 * scale)

    def _show_ui(self, src, dst):
        pass