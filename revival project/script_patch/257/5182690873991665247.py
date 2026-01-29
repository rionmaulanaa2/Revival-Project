# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/tools/plist_tools/plist_checker.py
import json
import os
import os.path

class PlistUsageCollector(object):

    def __init__(self):
        self.plist_usage_dict = {}
        self.path_timing_list = []
        global_data.emgr.scene_after_enter_event += self._on_enter_scene

    def record_plist(self, plist, path, usage, use_node_belong_json):
        self.plist_usage_dict.setdefault(plist, {})
        self.plist_usage_dict[plist].setdefault(usage, {})
        self.plist_usage_dict[plist][usage].setdefault(path, [])
        if use_node_belong_json not in self.plist_usage_dict[plist][usage][path]:
            self.plist_usage_dict[plist][usage][path].append(use_node_belong_json)
        from logic.gcommon import time_utility as tutil
        bat = global_data.battle
        self.path_timing_list.append({'time': tutil.get_server_time(),'usage': usage,'in_battle': bat is not None,'displayFrame': {'plist': plist,'path': path},'belong': use_node_belong_json})
        return

    def record_plist_helper(self, plist, path, node):
        if not (plist and path):
            return
        from logic.gutils.scene_utils import is_in_lobby
        if global_data.game_mgr.scene:
            usage = global_data.scene_type
        else:
            usage = 'NO_SCENE'
        self.record_plist(plist, path, usage, [])

    def check_plist_usage(self):
        for plist, usage_dict in self.plist_usage_dict.iteritems():
            if len(usage_dict) > 1:
                log_error('plist used in battle and lobby in the same time', plist, usage_dict)
                msg = 'plist used in battle and lobby in the same time' + str(plist) + str(usage_dict)
                global_data.uisystem.post_wizard_trace(msg)
                import exception_hook
                err_msg = msg
                exception_hook.post_error(err_msg)

        plist_timing_list = []
        usage_dict2 = {}
        for path_info in self.path_timing_list:
            sp = path_info.get('displayFrame', {}).get('path', '')
            rec_plist = path_info.get('displayFrame', {}).get('plist', '')
            plist = global_data.uisystem.GetSpriteFramePlistByPath(sp) or rec_plist
            if plist:
                plist_timing_list.append([plist, path_info])
                usage_dict2.setdefault(plist, {})
                in_battle = path_info.get('in_battle')
                usage_dict2[plist][in_battle] = path_info

        for plist, usage_dict in usage_dict2.iteritems():
            if len(usage_dict) > 1:
                log_error('plist used in battle and lobby in the same time', plist, usage_dict)
                msg = 'plist used in battle and lobby in the same time' + str(plist) + str(usage_dict)
                global_data.uisystem.post_wizard_trace(msg)
                import exception_hook
                err_msg = msg
                exception_hook.post_error(err_msg)

    def reset(self):
        self.plist_usage_dict = {}

    def destroy(self):
        self.plist_usage_dict = {}

    def _on_enter_scene(self, *args):
        from logic.gcommon.common_const.scene_const import SCENE_LOBBY
        cur_scene = global_data.game_mgr.scene
        if cur_scene.scene_type != SCENE_LOBBY:
            return
        print '_on_enter_scene dump and upload'
        self.check_plist_usage()

    def report_outside_error(self, *args):
        import traceback
        stack = traceback.extract_stack()
        import exception_hook
        err_msg = 'Check input value!\n' + str(stack) + '\n' + str(args)
        exception_hook.post_error(err_msg)


def copy_npk_res_to_document_path--- This code section failed: ---

  99       0  LOAD_CONST            1  -1
           3  LOAD_CONST            0  ''
           6  IMPORT_NAME           0  'cc'
           9  STORE_FAST            2  'cc'

 100      12  LOAD_CONST            1  -1
          15  LOAD_CONST            0  ''
          18  IMPORT_NAME           1  'os'
          21  STORE_FAST            3  'os'

 101      24  LOAD_FAST             2  'cc'
          27  LOAD_ATTR             2  'FileUtils'
          30  LOAD_ATTR             3  'getInstance'
          33  CALL_FUNCTION_0       0 
          36  LOAD_ATTR             4  'isFileExist'
          39  LOAD_FAST             0  'npk_path'
          42  CALL_FUNCTION_1       1 
          45  POP_JUMP_IF_TRUE     52  'to 52'

 102      48  LOAD_CONST            2  ''
          51  RETURN_END_IF    
        52_0  COME_FROM                '45'

 105      52  LOAD_FAST             3  'os'
          55  LOAD_ATTR             5  'path'
          58  LOAD_ATTR             6  'exists'
          61  LOAD_FAST             1  'doc_path'
          64  CALL_FUNCTION_1       1 
          67  POP_JUMP_IF_FALSE    74  'to 74'

 106      70  LOAD_FAST             1  'doc_path'
          73  RETURN_END_IF    
        74_0  COME_FROM                '67'

 108      74  LOAD_CONST            1  -1
          77  LOAD_CONST            0  ''
          80  IMPORT_NAME           7  'C_file'
          83  STORE_FAST            4  'C_file'

 109      86  LOAD_FAST             4  'C_file'
          89  LOAD_ATTR             8  'get_res_file'
          92  LOAD_ATTR             2  'FileUtils'
          95  CALL_FUNCTION_2       2 
          98  STORE_FAST            5  's'

 110     101  LOAD_FAST             5  's'
         104  POP_JUMP_IF_FALSE   147  'to 147'

 111     107  LOAD_GLOBAL           9  'open'
         110  LOAD_FAST             1  'doc_path'
         113  LOAD_CONST            3  'wb'
         116  CALL_FUNCTION_2       2 
         119  SETUP_WITH           20  'to 142'
         122  STORE_FAST            6  'tmp_file'

 112     125  LOAD_FAST             6  'tmp_file'
         128  LOAD_ATTR            10  'write'
         131  LOAD_FAST             5  's'
         134  CALL_FUNCTION_1       1 
         137  POP_TOP          
         138  POP_BLOCK        
         139  LOAD_CONST            0  ''
       142_0  COME_FROM_WITH           '119'
         142  WITH_CLEANUP     
         143  END_FINALLY      
         144  JUMP_FORWARD          0  'to 147'
       147_0  COME_FROM                '144'

 113     147  LOAD_FAST             3  'os'
         150  LOAD_ATTR             5  'path'
         153  LOAD_ATTR             6  'exists'
         156  LOAD_FAST             1  'doc_path'
         159  CALL_FUNCTION_1       1 
         162  POP_JUMP_IF_FALSE   185  'to 185'

 114     165  LOAD_GLOBAL          11  'log_error'
         168  LOAD_CONST            4  'copy_npk_img_to_document_path(converted) success'
         171  LOAD_FAST             0  'npk_path'
         174  LOAD_FAST             1  'doc_path'
         177  CALL_FUNCTION_3       3 
         180  POP_TOP          

 115     181  LOAD_FAST             1  'doc_path'
         184  RETURN_END_IF    
       185_0  COME_FROM                '162'

 117     185  LOAD_GLOBAL          11  'log_error'
         188  LOAD_CONST            5  'copy_npk_img_to_document_path(converted) failed'
         191  LOAD_FAST             0  'npk_path'
         194  LOAD_FAST             1  'doc_path'
         197  CALL_FUNCTION_3       3 
         200  POP_TOP          

 118     201  LOAD_CONST            2  ''
         204  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 95


class PlistShowChecker(object):

    def __init__(self, plist, png):
        pass

    @staticmethod
    def get_plist_png_info(plist, png):
        from common.utils.ui_utils import GetPlistConf
        import cc
        dict_ = cc.FileUtils.getInstance().getValueMapFromFile(plist)
        png_info = dict_.get('frames', {}).get(png)
        if not png_info:
            print (
             'can not found png info', png_info)
        return png_info

    @staticmethod
    def RectFromString(str_rect):
        from common.utils.cocos_utils import ccc3FromHex, CCRect, CCRectZero
        rect = CCRectZero
        if not str_rect:
            return rect
        str_tuple_rect = str_rect.replace('{', '[').replace('}', ']')
        try:
            tuple_rect = eval(str_tuple_rect)
        except Exception as e:
            log_error(str(e))
            return

        return CCRect(tuple_rect[0][0], tuple_rect[0][1], tuple_rect[1][0], tuple_rect[1][1])

    @staticmethod
    def show_in_ui(plist, png):
        from tools.plist_tools.PlistPngShowUI import PlistPngShowUI
        ui = PlistPngShowUI()
        ui.show_in_ui(plist, png)
        import cc
        import game3d
        dict_ = cc.FileUtils.getInstance().getValueMapFromFile(plist)
        png_name = dict_.get('metadata', {}).get('realTextureFileName') or dict_.get('metadata', {}).get('textureFileName')
        plist_png = os.path.join(os.path.dirname(plist), png_name)
        dst_path = os.path.join(game3d.get_doc_dir(), 'plist.plist')
        copy_npk_res_to_document_path(plist, dst_path)
        dst_path = os.path.join(game3d.get_doc_dir(), 'plist.png')
        print ('plist_png', plist_png)
        copy_npk_res_to_document_path(plist_png, dst_path)

    @staticmethod
    def for_bp_ui():
        sp = global_data.ui_mgr.get_ui('ModeBanPickUI').btn_send.btn_common._display_spts[0]
        print ('cur sprite ', sp._cur_target_path, sp._cur_target_plist)


from common.uisys.basepanel import BasePanel
from common.const.uiconst import SECOND_CONFIRM_LAYER
from common.const import uiconst
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_NO_EFFECT

class JsonLoadChecker(BasePanel):
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    PANEL_CONFIG_NAME = 'test/test_sprite_clear'
    DLG_ZORDER = SECOND_CONFIRM_LAYER
    UI_ACTION_EVENT = {'btn_start.OnClick': 'on_click_btn_start',
       'btn_end.OnClick': 'on_click_btn_end',
       'btn_clear.OnClick': 'on_click_btn_clear',
       'btn_test.OnClick': 'on_click_btn_test'
       }

    def on_init_panel(self, *args, **kwargs):
        from tools.json_tools.for_each_json import for_file_in_res_do
        self.all_template_paths = []

        def file_callback(full_path):
            full_path = os.path.normpath(full_path)
            if 'gui\\template\\' in full_path:
                full_path = full_path[full_path.index('template') + len('template') + 1:]
            full_path = full_path.replace('.json', '')
            self.all_template_paths.append(full_path)

        for_file_in_res_do(file_callback, postfixs=('.json', ))

    def init_event(self):
        pass

    def on_click_btn_start(self, *args):
        import random
        samp = random.sample(self.all_template_paths, 10)
        for full_path in samp:
            try:
                global_data.uisystem.load_template_create(full_path, parent=self.panel.nd_content)
            except:
                pass

    def on_click_btn_clear(self, *args):
        allchild = self.panel.nd_content.GetChildren()
        for c in allchild:
            c.Destroy()

    def on_click_btn_test(self, *args):
        plist = 'gui/ui_res_plist/common.plist'
        png = 'gui/ui_res_2/common/button/btn_send_fight_end.png'
        from tools.plist_tools.plist_checker import PlistShowChecker
        PlistShowChecker.show_in_ui(plist, png)

    def on_click_btn_end(self, *args):
        global_data.ui_mgr.close_ui('PlistPngShowUI')
        global_data.ui_mgr.close_ui('ModeBanPickUI')
        from logic.comsys.lobby.BanPick.ModeBanPickUI import ModeBanPickUI
        ModeBanPickUI()