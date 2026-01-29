# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/chat/VoiceAILab.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
from common.framework import Singleton
from logic.gcommon.common_utils.local_text import get_text_by_id

class VoiceAILab(Singleton):
    ALIAS_NAME = 'voice_ailab'
    METHODID_DICT = {'hasPermissions': 'has_permission_callback',
       'onRequestPermissions': 'request_permission_callback',
       'onVMInitFinish': 'init_vm_callback',
       'onVMRegisterFinish': 'stop_register_callback',
       'onVMRecognizeFinish': 'stop_recongnize_callback',
       'onGetCacheCmdFinish': 'get_cache_cmd_callback'
       }

    def init(self):
        self.permission = False
        self.vm_valid = False

    def init_ailab(self):
        if global_data.channel:
            for methodId, cb in six_ex.items(self.METHODID_DICT):
                callback = getattr(self, cb, None)
                if callback:
                    global_data.channel.register_extend_callback_function(self.__class__.__name__, methodId, callback)

        self.has_permission()
        return

    def on_finalize(self):
        if global_data.channel:
            for methodId, cb in six_ex.items(self.METHODID_DICT):
                callback = getattr(self, cb, None)
                if callback:
                    global_data.channel.unregister_extend_callback_function(self.__class__.__name__, methodId, callback)

        return

    def has_permission(self):
        command = {'methodId': 'hasPermissions'}
        global_data.channel.extend_func_by_dict(command)

    def has_permission_callback(self, json_dict):
        result = json_dict.get('result', {})
        if result:
            success = result.get('success', False)
            if success:
                self.permission = True
            else:
                self.permission = False

    def request_permission(self):
        global_data.channel.set_prop_int('ENABLE_UNISDK_PERMISSION_TIPS', 1)
        global_data.channel.set_prop_str('UNISDK_NGVOICE_PERMISSION_TIPS', get_text_by_id(604101))
        command = {'methodId': 'onRequestPermissions'
           }
        global_data.channel.extend_func_by_dict(command)

    def request_permission_callback(self, json_dict):
        result = json_dict.get('result', {})
        if result:
            success = result.get('success', False)
            if success:
                self.permission = True
            else:
                self.permission = False

    def init_vm(self):
        command = {'methodId': 'initVM',
           'token': 'E7q9H4j6TdAoxBmyB6J2KYUybQ95yn'
           }
        global_data.channel.extend_func_by_dict(command)

    def init_vm_callback(self, json_dict):
        result = json_dict.get('result', {})
        if result:
            code = result.get('code', 1)
            if code == 0:
                self.vm_valid = True
            else:
                self.vm_valid = False

    def start_register(self, index_id):
        if not self.permission or not self.vm_valid:
            global_data.game_mgr.show_tip('start_register failed, no permissions')
            return
        command = {'methodId': 'startRegister',
           'id': index_id
           }
        global_data.channel.extend_func_by_dict(command)

    def stop_register(self):
        if not self.permission or not self.vm_valid:
            global_data.game_mgr.show_tip('stop_register failed, no permissions')
            return
        command = {'methodId': 'stopRegister'
           }
        global_data.channel.extend_func_by_dict(command)

    def stop_register_callback(self, json_dict):
        methodId = json_dict.get('methodId', None)
        if methodId:
            if methodId == 'stopRegister':
                pass
            elif methodId == 'onVMRegisterFinish':
                result = json_dict.get('result', {})
                if result:
                    code = result.get('code', 1)
                    if code == 0:
                        global_data.game_mgr.show_tip('stop_register success!')
                    else:
                        global_data.game_mgr.show_tip('stop_register falied code: ' + str(code))
        return

    def start_recongnize(self):
        if not self.permission or not self.vm_valid:
            global_data.game_mgr.show_tip('start_recongnize failed, no permissions')
            return
        command = {'methodId': 'startRecognize'
           }
        global_data.channel.extend_func_by_dict(command)

    def stop_recongnize(self):
        if not self.permission or not self.vm_valid:
            global_data.game_mgr.show_tip('stop_recongnize failed, no permissions')
            return
        command = {'methodId': 'stopRecognize'
           }
        global_data.channel.extend_func_by_dict(command)

    def stop_recongnize_callback(self, json_dict):
        result = json_dict.get('result', {})
        if result:
            code = result.get('code', 1)
            if code == 0:
                index_id = result.get('id')
                global_data.game_mgr.show_tip('stop_recongnize success! id: ' + str(index_id))
            else:
                global_data.game_mgr.show_tip('stop_recongnize falied code: ' + str(code))

    def set_vm_option(self):
        pass

    def delete_voice_cmd(self, index_id):
        if not self.permission or not self.vm_valid:
            pass
        command = {'methodId': 'deleteVoiceCmd',
           'id': index_id
           }
        global_data.channel.extend_func_by_dict(command)

    def stop_decoder(self):
        if not self.permission or not self.vm_valid:
            pass
        command = {'methodId': 'stopDecoder'
           }
        global_data.channel.extend_func_by_dict(command)

    def get_cache_cmd(self):
        if not self.permission or not self.vm_valid:
            pass
        command = {'methodId': 'getCacheCmd'
           }
        global_data.channel.extend_func_by_dict(command)

    def get_cache_cmd_callback(self, json_dict):
        result = json_dict.get('result', [])
        if result:
            print(result)
            global_data.game_mgr.show_tip('get_cache_cmd result: ')
            global_data.game_mgr.show_tip(str(result))