# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/tools/map_name_ui2png.py
import cc
import render
import game3d
import os
from common.utils import timer
from common.cfg import confmgr
from logic.manager_agents.manager_decorators import sync_exec
from logic.gcommon.common_const.lang_data import code_2_shorthand, LANG_CN, LANG_EN, LANG_JA, LANG_KO
from logic.gcommon.common_utils import local_text
resource_path = 'map/i_map_name_scene_h'
save_path_root = 'F:\\client\\gameplay\\trunk\\src\\map_name'
map_name = [
 29]
fonts = {LANG_CN: 'gui/fonts/fzdys_special.ttf',LANG_EN: 'gui/fonts/fzdys.ttf',
   LANG_JA: 'gui/fonts/g93_jp_thick.ttf',
   LANG_KO: 'gui/fonts/g93_kr_thick.ttf'
   }
MAP_NAME = 'bw_all06'
RENDER_TARGET_FORMAT = render.PIXEL_FMT_A8R8G8B8 if game3d.get_render_device() == game3d.DEVICE_D3D9 else render.PIXEL_FMT_A4R4G4B4
tick_timer = None
i = 0
ui_panel = None

def save(file_name='', name_text_id=None):
    global i
    global tick_timer
    if name_text_id is None:

        def _cb():
            global i
            global tick_timer
            if i < len(map_name):
                save_one(i)
            else:
                tick_timer and global_data.game_mgr.get_logic_timer().unregister(tick_timer)
                tick_timer = None
                i = 0
                return
            i += 1
            return

        tick_timer = global_data.game_mgr.get_logic_timer().register(func=lambda : _cb(), mode=timer.CLOCK, interval=5)
    else:
        save_one(i, name_text_id=name_text_id, file_name=file_name)
    return


def save_one(i, name_text_id=None, file_name='temp'):
    global ui_panel
    lang = local_text.get_cur_text_lang()
    if ui_panel is None:
        ui_panel = global_data.uisystem.load_template_create(resource_path)
        ui_panel.retain()
    ui_panel.lab_name.SetFontName(fonts.get(lang, 'gui/fonts/fzy4jw.ttf'))
    if name_text_id is None:
        map_area_id = map_name[i]
        file_name = map_area_id
        area_info = confmgr.get('map_area_conf', MAP_NAME, 'Content', str(map_area_id))
        if area_info:
            name_text_id = area_info.get('name_text_id')
            print ('name_text_id--------------', name_text_id)
            ui_panel.lab_name.SetString(name_text_id)
    else:
        ui_panel.lab_name.SetString(name_text_id)
    size = ui_panel.getContentSize()
    scale = 1
    render_texture_size = (size.width * scale, size.height * scale)
    ui_panel.setAnchorPoint(cc.Vec2(0, 0))
    if game3d.get_render_device() not in (game3d.DEVICE_GLES, game3d.DEVICE_GL):
        ui_panel.setScale(scale)
        ui_panel.SetPosition(0, 0)
    else:
        ui_panel.setScaleX(scale)
        ui_panel.setScaleY(-scale)
        ui_panel.SetPosition(0, size.height * scale)
    tex = render.texture.create_empty(int(render_texture_size[0]), int(render_texture_size[1]), render.PIXEL_FMT_A8R8G8B8, True)
    rt = cc.RenderTexture.createWithITexture(tex)
    rt.retain()
    _draw_ui_to_rt(rt, lang, file_name)
    return


@sync_exec
def _draw_ui_to_rt--- This code section failed: ---

  91       0  LOAD_GLOBAL           0  'ui_panel'
           3  UNARY_NOT        
           4  POP_JUMP_IF_TRUE     20  'to 20'
           7  LOAD_GLOBAL           0  'ui_panel'
          10  LOAD_ATTR             1  'isValid'
          13  CALL_FUNCTION_0       0 
          16  UNARY_NOT        
        17_0  COME_FROM                '4'
          17  POP_JUMP_IF_FALSE    24  'to 24'

  92      20  LOAD_CONST            0  ''
          23  RETURN_END_IF    
        24_0  COME_FROM                '17'

  93      24  LOAD_FAST             0  'rt'
          27  LOAD_ATTR             2  'begin'
          30  CALL_FUNCTION_0       0 
          33  POP_TOP          

  94      34  LOAD_GLOBAL           3  'hasattr'
          37  LOAD_GLOBAL           1  'isValid'
          40  CALL_FUNCTION_2       2 
          43  POP_JUMP_IF_FALSE    68  'to 68'

  95      46  LOAD_FAST             0  'rt'
          49  LOAD_ATTR             4  'addCommandsForNode'
          52  LOAD_GLOBAL           0  'ui_panel'
          55  LOAD_ATTR             5  'get'
          58  CALL_FUNCTION_0       0 
          61  CALL_FUNCTION_1       1 
          64  POP_TOP          
          65  JUMP_FORWARD         10  'to 78'

  97      68  LOAD_GLOBAL           0  'ui_panel'
          71  LOAD_ATTR             6  'visit'
          74  CALL_FUNCTION_0       0 
          77  POP_TOP          
        78_0  COME_FROM                '65'

  98      78  LOAD_FAST             0  'rt'
          81  LOAD_ATTR             7  'end'
          84  CALL_FUNCTION_0       0 
          87  POP_TOP          

 100      88  LOAD_CONST               '<code_object to_save_path_callback>'
          91  MAKE_FUNCTION_0       0 
          94  STORE_FAST            3  'to_save_path_callback'

 103      97  LOAD_GLOBAL           8  'code_2_shorthand'
         100  LOAD_ATTR             5  'get'
         103  LOAD_GLOBAL           9  'int'
         106  LOAD_FAST             1  'lang'
         109  CALL_FUNCTION_1       1 
         112  CALL_FUNCTION_1       1 
         115  STORE_FAST            4  'lang_str'

 104     118  LOAD_FAST             4  'lang_str'
         121  POP_JUMP_IF_FALSE   224  'to 224'

 105     124  LOAD_GLOBAL          10  'save_path_root'
         127  LOAD_CONST            3  '//'
         130  BINARY_ADD       
         131  LOAD_FAST             4  'lang_str'
         134  BINARY_ADD       
         135  STORE_FAST            5  'path'

 106     138  LOAD_GLOBAL          11  'os'
         141  LOAD_ATTR            12  'path'
         144  LOAD_ATTR            13  'exists'
         147  LOAD_FAST             5  'path'
         150  CALL_FUNCTION_1       1 
         153  STORE_FAST            6  'folder'

 107     156  LOAD_FAST             6  'folder'
         159  POP_JUMP_IF_TRUE    178  'to 178'

 108     162  LOAD_GLOBAL          11  'os'
         165  LOAD_ATTR            14  'makedirs'
         168  LOAD_FAST             5  'path'
         171  CALL_FUNCTION_1       1 
         174  POP_TOP          
         175  JUMP_FORWARD          0  'to 178'
       178_0  COME_FROM                '175'

 109     178  LOAD_FAST             0  'rt'
         181  LOAD_ATTR            15  'saveToFile'
         184  LOAD_FAST             5  'path'
         187  LOAD_CONST            3  '//'
         190  BINARY_ADD       
         191  LOAD_GLOBAL          16  'str'
         194  LOAD_FAST             2  'file_name'
         197  CALL_FUNCTION_1       1 
         200  BINARY_ADD       
         201  LOAD_CONST            4  '.png'
         204  BINARY_ADD       
         205  LOAD_GLOBAL          17  'cc'
         208  LOAD_ATTR            18  'IMAGE_FORMAT_PNG'
         211  LOAD_GLOBAL          19  'True'
         214  LOAD_FAST             3  'to_save_path_callback'
         217  CALL_FUNCTION_4       4 
         220  POP_TOP          
         221  JUMP_FORWARD          0  'to 224'
       224_0  COME_FROM                '221'

 110     224  LOAD_FAST             0  'rt'
         227  LOAD_ATTR            20  'release'
         230  CALL_FUNCTION_0       0 
         233  POP_TOP          

Parse error at or near `CALL_FUNCTION_2' instruction at offset 40