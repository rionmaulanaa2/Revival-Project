# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/weapon_skin_utils.py
from __future__ import absolute_import
from common.cfg import confmgr
from logic.gutils import item_utils
from logic.gutils.dress_utils import DEFAULT_CLOTHING_ID
from logic.gutils.item_utils import get_lobby_item_type
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_MECHA_SKIN
from logic.gutils.skin_define_utils import is_main_skin, FILTER_SKIN
from .item_utils import get_lobby_item_belong_no
import world
import math3d
grenade_res_config = {}
firearm_res_config = {}
c_buff_data = {}

def get_weapon_skin_firearm_res(skin_id, attr):
    skin_id = str(skin_id)
    return firearm_res_config.get(skin_id, {}).get(attr, None)


def get_weapon_skin_grenade_weapon_sfx_path(skin_id, attr):
    skin_id = str(skin_id)
    return grenade_res_config.get(skin_id, {}).get(attr, None)


def set_weapon_skin_pic_pos_and_scale(img, item_fashion, item_no):
    ui_display_conf = confmgr.get('ui_display_conf', 'WeaponSkinPic', 'Content', default={})
    node_ui_conf = ui_display_conf.get(str(item_fashion)) or ui_display_conf.get(str(item_no)) or ui_display_conf.get(str(confmgr.get('item', str(item_no), default={}).get('iShader', None)))
    if not node_ui_conf:
        img.ReConfPosition()
        img.ScaleSelfNode()
        return
    else:
        pos = node_ui_conf.get('NodePos')
        if pos:
            img.SetPosition(*pos)
        else:
            img.ReConfPosition()
        scale = node_ui_conf.get('NodeScale')
        img.AddReordedNodeInfo('scale')
        if scale:
            img.SetScaleCheckRecord(scale * img.GetConfScaleX())
        else:
            img.ScaleSelfNode()
        return


def get_explosive_robot_conf_val(item_type, key, default=None, skin_id=None):
    item_type = str(item_type)
    val = confmgr.get('explosive_robot_conf', 'RobotConfig', 'Content', item_type, key, default=default)
    if skin_id is not None:
        val = confmgr.get('explosive_robot_conf', 'SkinConfig', 'Content', item_type, str(skin_id), key, default=val)
    return val


def get_explosive_robot_conf--- This code section failed: ---

  77       0  BUILD_MAP_0           0 
           3  STORE_FAST            2  'conf'

  78       6  LOAD_GLOBAL           0  'str'
           9  LOAD_FAST             0  'item_type'
          12  CALL_FUNCTION_1       1 
          15  STORE_FAST            0  'item_type'

  79      18  LOAD_FAST             2  'conf'
          21  LOAD_ATTR             1  'update'
          24  LOAD_GLOBAL           2  'confmgr'
          27  LOAD_ATTR             3  'get'
          30  LOAD_CONST            1  'explosive_robot_conf'
          33  LOAD_CONST            2  'RobotConfig'
          36  LOAD_CONST            3  'Content'
          39  LOAD_CONST            4  'default'
          42  BUILD_MAP_0           0 
          45  CALL_FUNCTION_260   260 
          48  CALL_FUNCTION_1       1 
          51  POP_TOP          

  80      52  LOAD_FAST             1  'skin_id'
          55  LOAD_CONST            0  ''
          58  COMPARE_OP            9  'is-not'
          61  POP_JUMP_IF_FALSE   119  'to 119'

  81      64  LOAD_GLOBAL           2  'confmgr'
          67  LOAD_ATTR             3  'get'
          70  LOAD_CONST            1  'explosive_robot_conf'
          73  LOAD_CONST            5  'SkinConfig'
          76  LOAD_CONST            3  'Content'
          79  LOAD_FAST             0  'item_type'
          82  LOAD_GLOBAL           0  'str'
          85  LOAD_FAST             1  'skin_id'
          88  CALL_FUNCTION_1       1 
          91  LOAD_CONST            4  'default'
          94  BUILD_MAP_0           0 
          97  CALL_FUNCTION_261   261 
         100  STORE_FAST            3  'skin_conf'

  82     103  LOAD_FAST             2  'conf'
         106  LOAD_ATTR             1  'update'
         109  LOAD_FAST             3  'skin_conf'
         112  CALL_FUNCTION_1       1 
         115  POP_TOP          
         116  JUMP_FORWARD          0  'to 119'
       119_0  COME_FROM                '116'

  83     119  LOAD_FAST             2  'conf'
         122  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_1' instruction at offset 48


def get_pve_bomb_puzzle_sfx_path--- This code section failed: ---

  87       0  LOAD_GLOBAL           0  'str'
           3  LOAD_FAST             0  'item_type'
           6  CALL_FUNCTION_1       1 
           9  STORE_FAST            0  'item_type'

  88      12  LOAD_GLOBAL           1  'confmgr'
          15  LOAD_ATTR             2  'get'
          18  LOAD_CONST            1  'pve/puzzle_data'
          21  LOAD_CONST            2  'BombConf'
          24  LOAD_CONST            3  'Content'
          27  LOAD_CONST            4  'default'
          30  BUILD_MAP_0           0 
          33  CALL_FUNCTION_260   260 
          36  STORE_FAST            1  'conf'

  89      39  LOAD_FAST             1  'conf'
          42  LOAD_ATTR             2  'get'
          45  LOAD_CONST            5  'bomb_effect'
          48  LOAD_CONST            6  ''
          51  CALL_FUNCTION_2       2 
          54  RETURN_VALUE     
          -1  RETURN_LAST      

Parse error at or near `CALL_FUNCTION_260' instruction at offset 33