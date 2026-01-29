# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/shader_warmup.py
from __future__ import absolute_import
from __future__ import print_function
import six
from six.moves import range
import render
import time
import json
import C_file
import world
import os
from common.framework import Singleton
from logic.vscene.global_display_setting import GlobalDisplaySeting
DEFAULT_LOD_MAPPING = {0: world.SHADER_LOD_LEVEL_2,
   1: world.SHADER_LOD_LEVEL_1,
   2: world.SHADER_LOD_LEVEL_0,
   3: world.SHADER_LOD_LEVEL_0
   }
PLAYER_EFFECTS = {
 'vbr_toon', 'vbr_toon_mecha'}

class ShaderWarmup(Singleton):
    IDLE_INTERVAL = 1.0

    def init(self):
        print('init ShaderWarmup Singleton')
        self.created_mat_map = {}
        self.iterator = None
        self.trival_iterator = None
        self._warmup_fninished = False
        self._total_time_cost = 0.0
        self._variation_count = 0
        self._loaded_json = 0
        self._total_json = 1
        self._time_log = {}
        self._trival_timer = None
        self.load_conf()
        self.init_event()
        if global_data.is_enable_shader_warmup and not global_data.is_low_mem_mode:
            self.create_trival_tick()
        return

    def on_finalize(self):
        print('finalize ShaderWarmup')
        self.cancel_trival_tick()

    def load_conf(self):
        self._json_conf_norm = json.loads(C_file.get_res_file('confs/shader_preload/normal_shaders.json', ''))
        self._json_conf_hefty = json.loads(C_file.get_res_file('confs/shader_preload/hefty_shaders.json', ''))
        self._iter_normal = self.itervariations([self._json_conf_norm])
        self._iter_hefty = self.itervariations([self._json_conf_hefty])
        self._iterall = self.iterall()
        self._total_json = len(self._json_conf_hefty) + len(self._json_conf_norm)

    def clear(self):
        self.created_mat_map = {}

    def init_event(self):
        emgr = global_data.emgr
        econf = {'warmup_shader_hefty_event': self.do_warmup_shader_hefty,
           'warmup_shader_trival_event': self.do_warmup_shader_trival,
           'warmup_shader_all_event': self.do_warmup_shader_all
           }
        emgr.bind_events(econf)

    def create_trival_tick(self):
        self.cancel_trival_tick()
        timermgr = global_data.game_mgr.get_logic_timer()
        self._trival_timer = timermgr.register(func=self.update_trival_tick, interval=5)

    def update_trival_tick(self):
        ui = global_data.ui_mgr.get_ui('ScreenTouchEffectUI')
        if not ui:
            return
        if not (global_data.game_mgr.scene and global_data.game_mgr.scene.is_loaded()):
            return
        if time.time() - ui._last_click_time > self.IDLE_INTERVAL:
            self.do_warmup_shader_trival(5, 0.1)

    def cancel_trival_tick(self):
        if self._trival_timer:
            timermgr = global_data.game_mgr.get_logic_timer()
            timermgr.unregister(self._trival_timer)

    def do_warmup_shader_hefty(self, limit=10, time_limit=None):
        if not self.warmup_finished:
            self.do_warmup(limit, time_limit, self._iter_hefty)

    def do_warmup_shader_trival(self, limit=1, time_limit=None):
        if not self.warmup_finished:
            if self.do_warmup(limit, time_limit, self._iter_normal):
                self.cancel_trival_tick()

    def do_warmup_shader_all(self, limit=10, time_limit=0.1):
        if not self.warmup_finished:
            self.do_warmup(limit, time_limit, self._iterall)

    @property
    def warmup_finished(self):
        return self._warmup_fninished

    @property
    def warmup_process(self):
        if self._total_json < 1:
            return 1.0
        if self._warmup_fninished:
            return 1.0
        return float(self._loaded_json) / self._total_json

    def adjust_macros(self, mat, is_player=False):
        quality = GlobalDisplaySeting().get_actual_quality()
        lod_level = DEFAULT_LOD_MAPPING.get(quality, 2)
        if mat.get_macro('LOD_LEVEL') is not None:
            if is_player:
                lod_level = max(lod_level - 1, 0)
            mat.set_macro('LOD_LEVEL', str(lod_level))
        if mat.get_macro('SHADOW_MAP_ENABLE') is not None:
            enable = GlobalDisplaySeting().actual_shadowmap_enabled
            enable_str = str(bool(enable)).upper()
            mat.set_macro('SHADOW_MAP_ENABLE', enable_str)
        if not world.is_gpu_skin_enable():
            mat.set_macro('GPU_SKIN_ENABLE', 'FALSE')
        return

    def precompile_shader(self, effectfile, tech, macros):
        t0 = time.time()
        if effectfile not in self.created_mat_map:
            technique = render.technique(1, effectfile, tech)
            self.created_mat_map[effectfile] = render.material(technique)
            self._variation_count += 1
        effname = os.path.splitext(os.path.basename(effectfile))[0]
        mat = self.created_mat_map.get(effectfile)
        if not macros:
            return
        for macro, val in macros:
            mat.set_macro(macro, val)

        self.adjust_macros(mat)
        mat.rebuild_tech()
        dtime = time.time() - t0
        self._total_time_cost += dtime
        self._variation_count += 1
        self._time_log[effname] = self._time_log.get(effname, 0.0) + dtime

    def itervariations(self, json_path_list):
        self._total_json = len(json_path_list)
        for json_conf in json_path_list:
            for shader_conf in json_conf:
                self._loaded_json += 1
                effectfile, tech = shader_conf['EffectFile'].replace('\\', '/'), shader_conf['Technique']
                macro_variations = shader_conf['MacroVariations']
                print('Precompile effect [%s] started, variation count %d' % (effectfile, len(macro_variations)))
                for variation in macro_variations:
                    yield (
                     effectfile, tech, variation)

    def get_iterator(self, categories=None):
        categories = categories or [self._json_conf_hefty, self._json_conf_hefty]
        return self.itervariations(categories)

    def iterall(self):
        for eff, tech, var in self._iter_hefty:
            yield (eff, tech, var)

        for eff, tech, var in self._iter_normal:
            yield (
             eff, tech, var)

    def iternormal(self):
        for eff, tech, var in self._iter_normal:
            yield (
             eff, tech, var)

    def iterhefty(self):
        for eff, tech, var in self._iter_hefty:
            yield (
             eff, tech, var)

    def do_warmup_imm(self):
        for eff, tech, macros in self.get_iterator():
            self.precompile_shader(eff, tech, macros)

    def do_warmup(self, limit=10, time_limit=None, iterator=None):
        if not iterator:
            iterator = self._iterall
        start_time = time.time()
        for i in range(limit):
            try:
                eff, tech, macros = next(iterator)
                self.precompile_shader(eff, tech, macros)
                cur_time = time.time()
                if time_limit and time_limit < cur_time - start_time:
                    break
            except StopIteration:
                if iterator is self._iterall:
                    print('Precompile finished, %d variations, costs %fs.' % (self._variation_count, self._total_time_cost))
                    for eff, t in six.iteritems(self._time_log):
                        print('%-25s time: %f' % (eff, t))

                    self.cancel_trival_tick()
                    self._warmup_fninished = True
                return True
            except:
                import traceback
                import exception_hook
                exception_hook.post_error(traceback.format_exc())
                self._warmup_fninished = True
                return True

        print('warmup time cost:', cur_time - start_time)
        return False

    def warmup_time_trial(self, budget_time, time_limit=0.1, iterator=None):
        start_time = time.time()
        if self.do_warmup(100, time_limit, iterator):
            return 0.0
        else:
            elapse_time = time.time() - start_time
            return budget_time - elapse_time