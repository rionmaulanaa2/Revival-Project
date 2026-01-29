# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/record_shader.py
from __future__ import absolute_import
from __future__ import print_function
import six
import six_ex
import os
import time
import json
import game
import render
import C_file
from common.framework import Singleton
from common.utils.path import get_neox_dir
from logic.gcommon.time_utility import get_date_str
FILE_VERSION_NEED = ('nfx.json', '.nfx')
TIME_OUT = 5
FTP_PORT = 8001
FTP_IP = '10.224.40.205'
EFFECT_INFO_FILE_NAME = 'effect_info.json'

class ShaderRecord(Singleton):

    def init(self):
        if not hasattr(render, 'enable_effect_recorder'):
            return
        else:
            if not self.check_enable_record():
                return
            self._root_dir = get_neox_dir()
            from common.platform.dctool.interface import get_shader_record_device_name
            self._device_name = get_shader_record_device_name()
            if not self._device_name:
                return
            self._is_uploading = False
            self._collect_cache_lst = []
            res_info_exist = C_file.find_res_file(EFFECT_INFO_FILE_NAME, '')
            if not res_info_exist:
                return
            self._res_effect_info = json.loads(C_file.get_res_file(EFFECT_INFO_FILE_NAME, ''))
            self._upload_shaders = {}
            self._nums = 0
            render.enable_effect_recorder(True)
            game.on_new_effect_compile = self._record_effect
            try:
                from mobile.common.JsonConfig import parse
                uploaded_json_path = os.path.join(self._root_dir, 'all_uploaded_shaders.json')
                if os.path.exists(uploaded_json_path):
                    self._all_upload_shaders = parse(uploaded_json_path)
                else:
                    self._all_upload_shaders = {}
            except Exception as e:
                log_error('[ShaderRecord] get all uploaded error: %s' % str(e))
                self._all_upload_shaders = {}

            date_str = get_date_str()
            last_day = self._all_upload_shaders.get('last_date_str', None)
            if last_day != date_str:
                self._all_upload_shaders = {'last_date_str': date_str,'uploaded_shaders': {}}
            global_data.emgr.scene_after_enter_event += self._on_enter_scene
            return

    def _split_macros(self, macro_str):
        lines = macro_str.splitlines()[:-1]
        return [ line.replace('#define', '').strip().split(' ') for line in lines ]

    def _record_effect(self, effect, tech, macros, macro_id, time_cost, tid, define_key=''):
        if self._is_uploading:
            self._collect_cache_lst.append((effect, tech, macros, macro_id, time_cost, tid, define_key))
            return
        if define_key == '':
            return
        if '*' in define_key:
            return
        effect = effect.replace('\\', '/')
        effect = effect.replace('.fx', '.nfx')
        effect_info = self._res_effect_info.get(effect, {})
        if not effect_info:
            tmp_effect_path = effect.replace('/', '\\')
            effect_info = self._res_effect_info.get(tmp_effect_path, {})
            if not effect_info:
                return
        effect_version = self._get_simple_version(effect_info)
        if not effect_version:
            return
        self._all_upload_shaders.setdefault('uploaded_shaders', {}).setdefault(effect, {})
        self._all_upload_shaders['uploaded_shaders'][effect].setdefault('define_keys_dict', {})
        version = self._all_upload_shaders['uploaded_shaders'][effect].setdefault('version', effect_version)
        if not self._check_version(version, effect_version):
            self._all_upload_shaders['uploaded_shaders'][effect]['version'] = version
            self._all_upload_shaders['uploaded_shaders'][effect]['define_keys_dict'] = {}
            if effect in self._upload_shaders:
                self._upload_shaders[effect] = {}
        self._all_upload_shaders['uploaded_shaders'][effect]['define_keys_dict'].setdefault(self._device_name, [])
        define_key_lst = self._all_upload_shaders['uploaded_shaders'][effect]['define_keys_dict'][self._device_name]
        if define_key in define_key_lst:
            return
        self._all_upload_shaders['uploaded_shaders'][effect]['define_keys_dict'][self._device_name].append(define_key)
        self._upload_shaders.setdefault(effect, {})
        self._upload_shaders[effect].setdefault('version', version)
        self._upload_shaders[effect].setdefault('devices', {})
        self._upload_shaders[effect]['devices'].setdefault(self._device_name, [])
        if define_key in self._upload_shaders[effect]['devices'][self._device_name]:
            return
        self._upload_shaders[effect]['devices'][self._device_name].append(define_key)
        self._nums += 1

    def _dump_and_upload(self):
        if not self._upload_shaders:
            if global_data.is_inner_server:
                print('[ShaderRecord] no upload shaders')
            return
        if self._is_uploading:
            return
        json_path = os.path.join(self._root_dir, 'effect_collections.json')
        zip_path = os.path.join(self._root_dir, 'collect_collect.zip')
        with open(json_path, 'w') as tmp_file:
            json.dump(self._upload_shaders, tmp_file, sort_keys=True)
        try:
            import zipfile
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
                time_stamp = time.strftime('%H%M%S')
                user_id = global_data.player or 'empty' if 1 else global_data.player.uid
                log_name = '%s_%s.json' % (user_id, time_stamp)
                z.write(json_path, log_name)
        except Exception as e:
            log_error('[ShaderRecord] zip error:%s' % str(e))
            return

        if global_data.is_inner_server:
            self._upload_file_inner(zip_path)
        else:
            self._upload_file_outer(zip_path)

    def _upload_file_inner(self, log_path):

        def upload_by_ftp--- This code section failed: ---

 202       0  LOAD_CONST            1  ''
           3  LOAD_CONST            2  ('FTP',)
           6  IMPORT_NAME           0  'ftplib'
           9  IMPORT_FROM           1  'FTP'
          12  STORE_FAST            1  'FTP'
          15  POP_TOP          

 203      16  LOAD_FAST             1  'FTP'
          19  LOAD_CONST            3  'timeout'
          22  LOAD_GLOBAL           2  'TIME_OUT'
          25  CALL_FUNCTION_256   256 
          28  STORE_FAST            2  'ftp_client'

 204      31  SETUP_EXCEPT         36  'to 70'

 205      34  LOAD_FAST             2  'ftp_client'
          37  LOAD_ATTR             3  'connect'
          40  LOAD_GLOBAL           4  'FTP_IP'
          43  LOAD_GLOBAL           5  'FTP_PORT'
          46  CALL_FUNCTION_2       2 
          49  POP_TOP          

 206      50  LOAD_FAST             2  'ftp_client'
          53  LOAD_ATTR             6  'login'
          56  LOAD_CONST            4  'ftp_shader'
          59  LOAD_CONST            5  'voyage'
          62  CALL_FUNCTION_2       2 
          65  POP_TOP          
          66  POP_BLOCK        
          67  JUMP_FORWARD         46  'to 116'
        70_0  COME_FROM                '31'

 207      70  DUP_TOP          
          71  LOAD_GLOBAL           7  'Exception'
          74  COMPARE_OP           10  'exception-match'
          77  POP_JUMP_IF_FALSE   115  'to 115'
          80  POP_TOP          
          81  STORE_FAST            3  'e'
          84  POP_TOP          

 208      85  LOAD_GLOBAL           8  'log_error'
          88  LOAD_CONST            6  '[ShaderRecord] can not connect to %s:%s'
          91  LOAD_GLOBAL           4  'FTP_IP'
          94  LOAD_GLOBAL           9  'str'
          97  LOAD_FAST             3  'e'
         100  CALL_FUNCTION_1       1 
         103  BUILD_TUPLE_2         2 
         106  BINARY_MODULO    
         107  CALL_FUNCTION_1       1 
         110  POP_TOP          

 209     111  LOAD_GLOBAL          10  'False'
         114  RETURN_VALUE     
         115  END_FINALLY      
       116_0  COME_FROM                '115'
       116_1  COME_FROM                '67'

 211     116  LOAD_GLOBAL          11  'time'
         119  LOAD_ATTR            12  'strftime'
         122  LOAD_CONST            7  '%H%M%S'
         125  CALL_FUNCTION_1       1 
         128  STORE_FAST            4  'time_stamp'

 212     131  LOAD_GLOBAL          13  'global_data'
         134  LOAD_ATTR            14  'player'
         137  POP_JUMP_IF_TRUE    146  'to 146'
         140  LOAD_CONST            8  'empty'
         143  JUMP_FORWARD          9  'to 155'
         146  LOAD_GLOBAL          13  'global_data'
         149  LOAD_ATTR            14  'player'
         152  LOAD_ATTR            15  'uid'
       155_0  COME_FROM                '143'
         155  STORE_FAST            5  'user_id'

 213     158  LOAD_CONST            9  '%s_%s.zip'
         161  LOAD_FAST             5  'user_id'
         164  LOAD_FAST             4  'time_stamp'
         167  BUILD_TUPLE_2         2 
         170  BINARY_MODULO    
         171  STORE_FAST            6  'log_name'

 214     174  SETUP_EXCEPT         55  'to 232'

 215     177  LOAD_GLOBAL          16  'open'
         180  LOAD_GLOBAL          10  'False'
         183  CALL_FUNCTION_2       2 
         186  SETUP_WITH           27  'to 216'
         189  STORE_FAST            7  'fp'

 216     192  LOAD_FAST             2  'ftp_client'
         195  LOAD_ATTR            17  'storbinary'
         198  LOAD_CONST           11  'STOR %s'
         201  LOAD_FAST             6  'log_name'
         204  BINARY_MODULO    
         205  LOAD_FAST             7  'fp'
         208  CALL_FUNCTION_2       2 
         211  POP_TOP          
         212  POP_BLOCK        
         213  LOAD_CONST            0  ''
       216_0  COME_FROM_WITH           '186'
         216  WITH_CLEANUP     
         217  END_FINALLY      

 217     218  LOAD_FAST             2  'ftp_client'
         221  LOAD_ATTR            18  'close'
         224  CALL_FUNCTION_0       0 
         227  POP_TOP          
         228  POP_BLOCK        
         229  JUMP_FORWARD         40  'to 272'
       232_0  COME_FROM                '174'

 218     232  DUP_TOP          
         233  LOAD_GLOBAL           7  'Exception'
         236  COMPARE_OP           10  'exception-match'
         239  POP_JUMP_IF_FALSE   271  'to 271'
         242  POP_TOP          
         243  STORE_FAST            3  'e'
         246  POP_TOP          

 219     247  LOAD_GLOBAL           8  'log_error'
         250  LOAD_CONST           12  '[ShaderRecord] ftp_client store binary error: %s'
         253  LOAD_GLOBAL           9  'str'
         256  LOAD_FAST             3  'e'
         259  CALL_FUNCTION_1       1 
         262  BINARY_MODULO    
         263  CALL_FUNCTION_1       1 
         266  POP_TOP          

 220     267  LOAD_GLOBAL          10  'False'
         270  RETURN_VALUE     
         271  END_FINALLY      
       272_0  COME_FROM                '271'
       272_1  COME_FROM                '229'

 221     272  LOAD_GLOBAL          19  'True'
         275  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_2' instruction at offset 183

        def upload_by_ftp_empty(file_path):
            return True

        def finish_cb(request, ret, path=log_path):
            try:
                os.remove(path)
            except Exception as e:
                log_error('[ShaderRecord] os remove error:%s' % str(e))

            self._on_upload_finish(ret)

        self._is_uploading = True
        from common.daemon_thread import DaemonThreadPool
        DaemonThreadPool().add_threadpool(upload_by_ftp_empty, finish_cb, log_path)

    def _upload_file_outer(self, zip_path):
        if not global_data.player:
            return False
        self._is_uploading = True
        global_data.player.try_upload_shader_collect(zip_path, self._upload_to_file_picker_cb)
        return True

    def _upload_to_file_picker_cb(self, status, error, record_names, file_path):
        self._on_upload_finish(status)
        try:
            os.remove(file_path)
        except Exception as e:
            log_error('[ShaderRecord] os remove error:%s' % str(e))

    def _on_upload_finish(self, ret):
        self._is_uploading = False
        if ret:
            print('up num:', self._nums)
            self._upload_shaders = {}
            self._nums = 0
            try:
                uploaded_json_path = os.path.join(self._root_dir, 'all_uploaded_shaders.json')
                with open(uploaded_json_path, 'w') as tmp_file:
                    json.dump(self._all_upload_shaders, tmp_file, sort_keys=True)
            except Exception as e:
                log_error('[ShaderRecord] save all_uploaded_shaders error: %s' % str(e))

        for effect_collect_info in self._collect_cache_lst:
            effect, tech, macros, macro_id, time_cost, tid, define_key = effect_collect_info
            self._record_effect(effect, tech, macros, macro_id, time_cost, tid, define_key)

        self._collect_cache_lst = []

    def _get_simple_version(self, effect_version_info):
        ret_version_info = {}
        for shader_file, version_data in six.iteritems(effect_version_info):
            is_need_version = False
            for path_suffix in FILE_VERSION_NEED:
                if shader_file.endswith(path_suffix):
                    is_need_version = True
                    continue

            if not is_need_version:
                continue
            if isinstance(version_data, list):
                version_data = version_data[0]
            ret_version_info[shader_file] = version_data

        return ret_version_info

    def _check_version(self, v_a, v_b):
        if len(six_ex.keys(v_a)) != len(six_ex.keys(v_b)):
            return False
        else:
            for file_key in v_a:
                if v_a[file_key] != v_b.get(file_key, None):
                    return False

            return True

    def _on_enter_scene(self, *args):
        from logic.gcommon.common_const.scene_const import SCENE_LOBBY
        cur_scene = global_data.game_mgr.scene
        if cur_scene.scene_type != SCENE_LOBBY:
            return
        self._dump_and_upload()

    def check_enable_record(self):
        import game3d
        from common.platform import is_android, is_ios
        if is_android():
            return False
        if is_ios():
            return game3d.get_render_device() == game3d.DEVICE_METAL
        work_dir = game3d.get_doc_dir() if is_ios() else game3d.get_root_dir()
        try:
            res_npk_exist = os.path.isfile(os.path.join(work_dir, 'res.npk'))
            is_program_multi_client = os.path.isfile(os.path.join(work_dir, 'tt.txt')) and not res_npk_exist
            if is_program_multi_client:
                return False
            shader_source_dir = os.path.join(work_dir, 'res', 'shader')
            is_shader_resource_exist = os.path.isdir(shader_source_dir)
            if is_shader_resource_exist:
                return False
        except Exception as e:
            log_error('[ShaderRecord] check_enable_record error:%s' % str(e))
            return False

        return True

    def on_finalize(self):
        pass