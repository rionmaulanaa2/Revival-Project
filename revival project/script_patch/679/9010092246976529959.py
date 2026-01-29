# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/effect_cache.py
from __future__ import absolute_import
from __future__ import print_function
import six
import os
import json
import C_file
import render
import game3d
import shutil
from common.platform import is_ios, is_android
from common.framework import Singleton
from logic.comsys.archive.archive_manager import ArchiveManager
BEHAVIOR_SAVE_AND_LOAD = 12
COMPILE_ERROR_LINE_THRESHOLD = 3000
EFFECT_INFO_FILE_NAME = 'effect_info.json'
LOG_BEGIN = '[effect_cache] set effect cache behavior'
ERROR_LOG = 'compile error:'
ANDROID_FINGER_PRINT_INDEX = 5

class EffectCache(Singleton):

    def init(self):
        self._inited = False
        self._pc_enable_effect_upload = False
        self._has_del_cache = False
        if is_ios():
            self._cache_root = os.path.join(game3d.get_doc_dir(), 'res', 'effect_cache')
        else:
            self._cache_root = os.path.join(game3d.get_root_dir(), 'res', 'effect_cache')
        self._cache_effect_info_path = os.path.join(self._cache_root, EFFECT_INFO_FILE_NAME)
        self.res_effect_info = {}
        self.cache_effect_info = {}
        self._uploaded_data = None
        global_data.emgr.scene_after_enter_event += self._on_enter_scene
        return

    def is_shader_source_exist(self):
        work_dir = game3d.get_root_dir()
        if os.path.isdir(os.path.join(work_dir, 'res', 'shader')):
            log_error('[EffectCache] res/shader file exists')
            return True
        if os.path.isdir(os.path.join(work_dir, 'res', 'common', 'shader')):
            log_error('[EffectCache] common/shader file exists')
            return True
        if os.path.isdir(os.path.join(work_dir, 'res', 'common', 'pipeline')):
            log_error('[EffectCache] common/pipeline file exists')
            return True
        return False

    def _is_dx_platform(self):
        return render.get_render_system_name() in ('DirectX 9', 'DirectX 11')

    def init_behavior(self, force=False):
        if hasattr(render, 'is_support_binary_shader'):
            if not render.is_support_binary_shader():
                log_error('[EffectCache] do not support binary shader')
                return
        if self.is_shader_source_exist():
            log_error('[EffectCache] There is shader source in res path, will disable EffectCache')
            return
        if not hasattr(render, 'set_effect_cache_behavior'):
            log_error('[EffectCache] engine version is too low to enable EffectCacheMgr!')
            return
        if global_data.deviceinfo.is_emulator():
            return
        self._revert_effect_cache()
        behavior = global_data.effect_cache_behavior
        cur_behavior = render.get_effect_cache_behavior()
        if force or not self._inited:
            try:
                if not self.check_effect_cache():
                    log_error('[EffectCache] check effect_cache ver failed, will not enable EffectCacheMgrt.')
                    return
            except Exception as e:
                log_error('[EffectCache] check_effect_cache except:{}'.format(str(e)))
                return

            self._del_invalid_cache()
        print(LOG_BEGIN)
        render.set_effect_cache_behavior(BEHAVIOR_SAVE_AND_LOAD)
        self._inited = True

    def _del_invalid_cache(self):
        if is_android() and hasattr(game3d, 'get_android_build_info'):
            android_sys_data = ArchiveManager().get_archive_data('sys_info')
            finger_print_info_cache = android_sys_data.get_field('android_sys_data', '')
            finger_print_info_now = str(game3d.get_android_build_info(ANDROID_FINGER_PRINT_INDEX))
            if finger_print_info_now and finger_print_info_now != finger_print_info_cache:
                try:
                    shutil.rmtree(self._cache_root, True)
                    print('[EffectCache] del for android change from {0} to {1}'.format(finger_print_info_cache, finger_print_info_now))
                    self._has_del_cache = True
                    android_sys_data.set_field('android_sys_data', finger_print_info_now)
                    android_sys_data.save()
                except Exception as e:
                    log_error('[EffectCache] rmtree cache file error: %s' % str(e))

                return
        from common.utils.path import get_neox_dir
        log_path = os.path.join(get_neox_dir(), 'log_old_0.txt')
        line_num = 0
        begin_num = 0
        if not os.path.exists(self._cache_root):
            return
        try:
            if os.path.exists(log_path):
                with open(log_path, 'rb') as tmp_f:
                    log_data = six.ensure_str(tmp_f.read())
                    for line in log_data.splitlines():
                        line_num += 1
                        if LOG_BEGIN in line:
                            begin_num = line_num
                        if ERROR_LOG in line:
                            shutil.rmtree(self._cache_root, True)
                            print('[EffectCache] del for log detect')
                            self._has_del_cache = True
                            return
                        if line_num - begin_num > COMPILE_ERROR_LINE_THRESHOLD:
                            return

        except Exception as e:
            log_error('[EffectCache] _del_invalid_cache error: %s' % str(e))

    def _revert_effect_cache(self):
        sys_data = ArchiveManager().get_archive_data('sys_info')
        last_render_name = sys_data.get_field('last_render_name', '')
        now_render_name = render.get_render_system_name()
        last_res_region = sys_data.get_field('last_res_region', '')
        now_res_region = self.get_region_flag()
        print('[EffectCache] res region:', now_res_region)
        if not last_render_name:
            sys_data.set_field('last_render_name', now_render_name)
            sys_data.save()
        if not last_res_region:
            sys_data.set_field('last_res_region', now_res_region)
            sys_data.save()
        need_del_cache = False
        if now_render_name and now_render_name != last_render_name:
            print('[EffectCache] del for render change from {0} to {1}'.format(last_render_name, now_render_name))
            need_del_cache = True
            sys_data.set_field('last_render_name', now_render_name)
            sys_data.save()
        if now_res_region and now_res_region != last_res_region:
            print('[EffectCache] del for res change from {0} to {1}'.format(last_res_region, now_res_region))
            need_del_cache = True
            sys_data.set_field('last_res_region', now_res_region)
            sys_data.save()
        if need_del_cache:
            try:
                shutil.rmtree(self._cache_root, True)
                self._has_del_cache = True
            except Exception as e:
                log_error('[EffectCache] rmtree cache file error: %s' % str(e))

        if global_data.is_pc_mode and self._is_dx_platform():
            cache_backup_file = 'effect_cache_backup_{0}'.format(self.get_region_flag())
            backup_cache_root = os.path.join(game3d.get_root_dir(), 'res', cache_backup_file)
            try:
                if not os.path.exists(self._cache_root) and os.path.exists(backup_cache_root):
                    print('[EffectCache] copy backup')
                    shutil.copytree(backup_cache_root, self._cache_root)
            except Exception as e:
                log_error('[EffectCache] move effect_cache_backup wrong %s' % str(e))

    def check_res_diff(self):
        diff_list = []
        for k, v in six.iteritems(self.res_effect_info):
            if k not in self.cache_effect_info:
                diff_list.append(k)
                continue
            cache_shader_info = self.cache_effect_info[k]
            for shader_key, res_shader_info in six.iteritems(self.res_effect_info[k]):
                if shader_key not in cache_shader_info:
                    diff_list.append(k)
                    break
                if isinstance(res_shader_info, list):
                    res_shader_info = res_shader_info[0]
                cache_info = cache_shader_info[shader_key]
                if isinstance(cache_info, list):
                    cache_info = cache_info[0]
                if cache_info != res_shader_info:
                    diff_list.append(k)
                    break

        return diff_list

    def check_effect_cache(self):
        res_info_exist = C_file.find_res_file(EFFECT_INFO_FILE_NAME, '')
        if not res_info_exist:
            return False
        else:
            self.res_effect_info = json.loads(C_file.get_res_file(EFFECT_INFO_FILE_NAME, ''))
            try:
                if os.path.exists(self._cache_effect_info_path):
                    with open(self._cache_effect_info_path, 'rb') as tmp_f:
                        self.cache_effect_info = json.loads(tmp_f.read())
            except Exception as e:
                log_error('[EffectCache] load cache info except: %s' % str(e))
                self.cache_effect_info = {}

            diff_list = self.check_res_diff()
            if len(diff_list) > 0:
                print("[EffectCache] cache info doesn't match:", len(diff_list))
                return self.reset_effect_cache_dir(diff_list)
            print('[EffectCache] no diff, cache info matched !')
            return True

    def reset_effect_cache_dir(self, diff_list):
        if not os.path.exists(self._cache_root):
            os.makedirs(self._cache_root, 511)
        for diff_item in diff_list:
            item_path = os.path.join(self._cache_root, diff_item)
            if os.path.exists(item_path):
                try:
                    shutil.rmtree(item_path, ignore_errors=True)
                except Exception as e:
                    log_error('[EffectCache] remove cache failed, error message:{}'.format(str(e)))

        try:
            with open(self._cache_effect_info_path, 'wb') as tmp_f:
                w_data = json.dumps(self.res_effect_info)
                tmp_f.write(six.ensure_binary(w_data))
        except Exception as e:
            log_error('[EffectCache] save cache info except: {}'.format(str(e)))
            return False

        return True

    def shader_to_cache_dir(self, shader_path):
        suffix_list = [
         '.fx', '.nfx', '_gl.vs', '_gl.ps', '_metal.vs', '_metal.ps', '.vs', '.ps', '.nfx.json']
        if shader_path.startswith('common') or shader_path.startswith('shader'):
            for suffix in suffix_list:
                if shader_path.endswith(suffix):
                    cache_path = shader_path.replace(suffix, '.nfx')
                    return cache_path

    def get_effect_caches_to_remove(self, file_changed_list):
        dirs_to_remove = set()
        for file_changed in file_changed_list:
            cache_dir = self.shader_to_cache_dir(file_changed)
            if cache_dir:
                dirs_to_remove.add(cache_dir)

        return dirs_to_remove

    def remove_caches(self, dirs_to_remove):
        for dir_name in dirs_to_remove:
            abs_dir = os.path.join(self._cache_root, dir_name)
            if os.path.exists(abs_dir) and os.path.isdir(abs_dir):
                shutil.rmtree(abs_dir)

    def test_clean(self, test_files=None):
        changed_files = test_files or [
         'common\\pipeline\\bloom_downsample.nfx',
         'shader\\split_texture.fx',
         'common\\shader\\simpletech_gl.ps']
        to_remove = self.get_effect_caches_to_remove(changed_files)
        self.remove_caches(to_remove)

    def _init_effect_upload(self):
        if self._inited:
            return
        if global_data.is_pc_mode and hasattr(render, 'enable_effect_upload') and hasattr(render, 'get_no_cache_effects'):
            from logic.comsys.archive.archive_manager import ArchiveManager
            from logic.gcommon.time_utility import get_server_time, ONE_WEEK_SECONDS
            self._uploaded_data = ArchiveManager().get_archive_data('effect_cache_data')
            begin_time = self._uploaded_data.get_field('begin_time', 0)
            if get_server_time() - begin_time > ONE_WEEK_SECONDS:
                self._uploaded_data['begin_time'] = get_server_time()
                self._uploaded_data['uploaded_dict'] = {}
                self._uploaded_data.save(encrypt=True)
            render.enable_effect_upload(True)
            self._pc_enable_effect_upload = True

    def _on_enter_scene(self, *args):
        from logic.gcommon.common_const.scene_const import SCENE_LOBBY
        cur_scene = global_data.game_mgr.scene
        if cur_scene.scene_type != SCENE_LOBBY:
            return
        else:
            if not self._has_del_cache and hasattr(render, 'get_shader_compile_error_times'):
                error_times = render.get_shader_compile_error_times()
                print('[EffectCache] error times:', error_times)
                if error_times and error_times > 0:
                    try:
                        shutil.rmtree(self._cache_root, True)
                        self._has_del_cache = True
                    except Exception as e:
                        log_error('[EffectCache] rmtree cache file error: %s' % str(e))

            if not self._pc_enable_effect_upload or self._uploaded_data is None:
                return
            try:
                cache_info = render.get_no_cache_effects()
                render.reset_no_cache_effects()
                if self._uploaded_data:
                    up_dict = {}
                    count = 0
                    for effect_file, keys_lst in six.iteritems(cache_info):
                        if count > 150:
                            break
                        if effect_file.startswith('common\\pipeline') or effect_file.startswith('common/pipeline'):
                            continue
                        uploaded_dict = self._uploaded_data.get_field('uploaded_dict', {})
                        old_lst = uploaded_dict.get(effect_file, [])
                        for key in keys_lst:
                            if key not in old_lst:
                                count += 1
                                if count > 150:
                                    break
                                up_dict.setdefault(effect_file, [])
                                up_dict[effect_file].append(key)
                                self._uploaded_data['uploaded_dict'].setdefault(effect_file, [])
                                self._uploaded_data['uploaded_dict'][effect_file].append(key)
                                old_lst.append(key)

                        self._uploaded_data[effect_file] = old_lst

                    if up_dict:
                        self._uploaded_data.save(encrypt=True)
                        if global_data.player:
                            global_data.player.call_server_method('client_sa_log', ('OnEffectCacheUpload', {'up_effect_info': up_dict}))
            except Exception as e:
                log_error('[EffectCache] upload effect cache info error:%s' % str(e))

            return

    def get_region_flag(self):
        import social
        res_flag = 'na' if G_IS_NA_PROJECT else 'cn'
        channel = social.get_channel()
        if channel and channel.name == 'steam':
            res_flag = 'cn'
        return res_flag

    def restart(self):
        global_data.game_mgr.try_restart_app()

    def _upload_android_cpu_info(self):
        if not G_IS_NA_PROJECT or not is_android():
            return
        if self._has_upload_android_cpu:
            return
        self._has_upload_android_cpu = True
        is_64, ret_info = self._android_is_aarch64()
        if is_64:
            return
        print('[EffectCache] android 32')
        sys_data = ArchiveManager().get_archive_data('sys_info')
        last_str = sys_data.get_field('android_cpu_up_time', '')
        from logic.gcommon.time_utility import get_date_str
        date_str = get_date_str()
        if date_str != last_str:
            from logic.gutils.salog import SALog
            log_writer = SALog.get_instance()
            log_writer.write(SALog.ANDROID_32_BIT, ret_info)
            sys_data.set_field('android_cpu_up_time', date_str)
            sys_data.save()

    def _android_is_aarch64(self):
        if not is_android():
            return (False, {})
        uname_text = ''
        list_64_names = ('aarch64_be', 'aarch64', 'armv8b', 'armv8l', 'x86_64', 'AArch64_be',
                         'AArch64')
        try:
            output = os.popen('uname -m')
            uname_text = output.read()
            output.close()
            for arch_name in list_64_names:
                if arch_name in uname_text:
                    return (True, {})

        except Exception as e:
            print('[EffectCache] uname -a error:', str(e))

        cpu_info_path = '/proc/cpuinfo'
        if not os.path.exists(cpu_info_path):
            return (False, {'uname_text': uname_text})
        try:
            with open(cpu_info_path, 'r') as f:
                max_line = 8
                line_num = 0
                ret_info = ''
                for line in f:
                    line_num += 1
                    if 'aarch64' in line or 'AArch64' in line or 'CPU architecture: 8' in line:
                        return (True, {})
                    if line_num <= max_line:
                        ret_info += line

                return (
                 False, {'cpu_info': ret_info,'uname_text': uname_text})
        except Exception as e:
            print('[EffectCache] get cpu info error:', str(e))

        return (False, {})