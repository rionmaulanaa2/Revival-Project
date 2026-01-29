# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/battleprepare/BestSkinShow.py
from __future__ import absolute_import
import six
from six.moves import range
import world
import math3d
import math
import game3d
import render
import cc
import weakref
from logic.manager_agents.manager_decorators import sync_exec
from logic.vscene.parts.PartModelDisplay import CLobbyModel
from common.algorithm import resloader
from common.utils.timer import CLOCK
from logic.gutils import lobby_model_display_utils
from common.uisys.render_target import RenderTargetHolder
from logic.gcommon.item.item_const import FASHION_POS_SUIT, FASHION_POS_HEADWEAR, FASHION_POS_BACK, FASHION_POS_SUIT_2, FASHION_OTHER_PENDANT_LIST
from .BestRoleModelAppearance import BestRoleModelAppearance, BestRoleModelAppearanceConcert
from .BestMechaModelAppearance import BestMechaModelAppearance
from logic.gcommon import time_utility as tutil
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.cfg import confmgr
from logic.gutils.template_utils import init_rank_title
from logic.gcommon.common_const import rank_const
from logic.gutils import role_head_utils
_HASH = game3d.calc_string_hash('Tex0')
LED_MODEL_RES = 'model_new/scene/items/common/items_common_led_01.gim'
SKIN_TYPE_ROLE = 'role'
SKIN_TYPE_MECHA = 'mecha'
RENDER_TICK_INTERVAL = 1.0 / 15

class SingleSkinUIModel(object):

    def __init__(self, sprite_obj, lab_name, temp_rank_title, index, test_role_id=None, test_dressed_clothing_id=None, test_cur_cam_pos=None):
        self.index = index
        self.lab_name = lab_name
        self.temp_rank_title = temp_rank_title
        self.test_role_id = test_role_id
        self.test_dressed_clothing_id = test_dressed_clothing_id
        self.test_cur_cam_pos = test_cur_cam_pos
        self.model_objs = []
        self.scene = None
        self._view_flag = True
        self.scene_data = {}
        self.init_scene_data()
        self.rendet_target_holder = None
        self.is_scene_ready = False
        self.init_render_target(sprite_obj)
        return

    def init_scene_data(self):
        self.box_name = 'plan_box'
        self.scene_data = {'box_name': self.box_name}

    def get_scene_content_type(self):
        return None

    def get_box_position(self, box_name):
        pos = None
        m = self.scene().get_model(box_name)
        if m:
            pos = m.position
        return pos

    def init_render_target--- This code section failed: ---

  78       0  LOAD_FAST             1  'sprite_obj'
           3  LOAD_ATTR             0  'getContentSize'
           6  CALL_FUNCTION_0       0 
           9  STORE_FAST            2  'sz'

  79      12  BUILD_MAP_5           5 

  80      15  LOAD_CONST            1  4278190080L
          18  LOAD_CONST            2  'scn_bg_color'
          21  STORE_MAP        

  81      22  LOAD_CONST            3  30.0
          25  LOAD_CONST            4  'cam_fov'
          28  STORE_MAP        

  82      29  LOAD_FAST             2  'sz'
          32  LOAD_ATTR             1  'width'
          35  LOAD_CONST            5  'rt_width'
          38  STORE_MAP        

  83      39  LOAD_FAST             2  'sz'
          42  LOAD_ATTR             2  'height'
          45  LOAD_CONST            6  'rt_height'
          48  STORE_MAP        

  84      49  LOAD_GLOBAL           3  'math3d'
          52  LOAD_ATTR             4  'vector'
          55  LOAD_CONST            7  ''
          58  LOAD_GLOBAL           5  'math'
          61  LOAD_ATTR             6  'pi'
          64  LOAD_CONST            7  ''
          67  CALL_FUNCTION_3       3 
          70  LOAD_CONST            8  'cam_euler'
          73  STORE_MAP        
          74  STORE_FAST            3  'MAP_RT_CONF'

  88      77  LOAD_CONST            7  ''
          80  LOAD_CONST            9  19
          83  LOAD_CONST           10  18.5
          86  BUILD_LIST_3          3 
          89  STORE_FAST            4  'cur_cam_pos'

  89      92  LOAD_FAST             0  'self'
          95  LOAD_ATTR             7  'test_cur_cam_pos'
          98  POP_JUMP_IF_FALSE   113  'to 113'

  90     101  LOAD_FAST             0  'self'
         104  LOAD_ATTR             7  'test_cur_cam_pos'
         107  STORE_FAST            4  'cur_cam_pos'
         110  JUMP_FORWARD        256  'to 369'

  92     113  LOAD_GLOBAL           8  'global_data'
         116  LOAD_ATTR             9  'battle'
         119  LOAD_ATTR            10  'get_top_nb_role_info'
         122  CALL_FUNCTION_0       0 
         125  STORE_FAST            5  'role_info_list'

  93     128  LOAD_GLOBAL          11  'len'
         131  LOAD_FAST             5  'role_info_list'
         134  CALL_FUNCTION_1       1 
         137  LOAD_FAST             0  'self'
         140  LOAD_ATTR            12  'index'
         143  COMPARE_OP            4  '>'
         146  POP_JUMP_IF_FALSE   369  'to 369'

  94     149  LOAD_FAST             5  'role_info_list'
         152  LOAD_FAST             0  'self'
         155  LOAD_ATTR            12  'index'
         158  BINARY_SUBSCR    
         159  STORE_FAST            6  'info'

  95     162  LOAD_FAST             6  'info'
         165  LOAD_CONST           11  1
         168  BINARY_SUBSCR    
         169  STORE_FAST            7  'role_id'

  96     172  LOAD_FAST             6  'info'
         175  LOAD_CONST           12  3
         178  BINARY_SUBSCR    
         179  STORE_FAST            8  'fashion_data'

  97     182  LOAD_FAST             8  'fashion_data'
         185  LOAD_ATTR            13  'get'
         188  LOAD_GLOBAL          14  'FASHION_POS_SUIT'
         191  CALL_FUNCTION_1       1 
         194  STORE_FAST            9  'dressed_clothing_id'

  98     197  LOAD_FAST             9  'dressed_clothing_id'
         200  POP_JUMP_IF_TRUE    243  'to 243'

  99     203  LOAD_GLOBAL          15  'confmgr'
         206  LOAD_ATTR            13  'get'
         209  LOAD_CONST           13  'role_info'
         212  LOAD_CONST           14  'RoleInfo'
         215  LOAD_CONST           15  'Content'
         218  LOAD_GLOBAL          16  'str'
         221  LOAD_FAST             7  'role_id'
         224  CALL_FUNCTION_1       1 
         227  LOAD_CONST           16  'default_skin'
         230  CALL_FUNCTION_5       5 
         233  LOAD_CONST            7  ''
         236  BINARY_SUBSCR    
         237  STORE_FAST            9  'dressed_clothing_id'
         240  JUMP_FORWARD          0  'to 243'
       243_0  COME_FROM                '240'

 100     243  LOAD_FAST             0  'self'
         246  LOAD_ATTR            17  'test_role_id'
         249  POP_JUMP_IF_FALSE   264  'to 264'

 101     252  LOAD_FAST             0  'self'
         255  LOAD_ATTR            17  'test_role_id'
         258  STORE_FAST            7  'role_id'
         261  JUMP_FORWARD          0  'to 264'
       264_0  COME_FROM                '261'

 102     264  LOAD_FAST             0  'self'
         267  LOAD_ATTR            18  'test_dressed_clothing_id'
         270  POP_JUMP_IF_FALSE   285  'to 285'

 103     273  LOAD_FAST             0  'self'
         276  LOAD_ATTR            18  'test_dressed_clothing_id'
         279  STORE_FAST            9  'dressed_clothing_id'
         282  JUMP_FORWARD          0  'to 285'
       285_0  COME_FROM                '282'

 104     285  LOAD_GLOBAL          15  'confmgr'
         288  LOAD_ATTR            13  'get'
         291  LOAD_CONST           17  'island_data'
         294  LOAD_GLOBAL          16  'str'
         297  LOAD_FAST             7  'role_id'
         300  CALL_FUNCTION_1       1 
         303  CALL_FUNCTION_2       2 
         306  STORE_FAST           10  'role_camera_data'

 105     309  LOAD_FAST            10  'role_camera_data'
         312  POP_JUMP_IF_FALSE   369  'to 369'

 106     315  LOAD_FAST            10  'role_camera_data'
         318  LOAD_ATTR            13  'get'
         321  LOAD_GLOBAL          16  'str'
         324  LOAD_FAST             9  'dressed_clothing_id'
         327  CALL_FUNCTION_1       1 
         330  LOAD_FAST            10  'role_camera_data'
         333  LOAD_ATTR            13  'get'
         336  LOAD_CONST           18  '0'
         339  CALL_FUNCTION_1       1 
         342  CALL_FUNCTION_2       2 
         345  STORE_FAST           11  'skin_camera_data'

 107     348  LOAD_FAST            11  'skin_camera_data'
         351  LOAD_ATTR            13  'get'
         354  LOAD_CONST           19  'cam_pos'
         357  CALL_FUNCTION_1       1 
         360  STORE_FAST            4  'cur_cam_pos'
         363  JUMP_ABSOLUTE       369  'to 369'
         366  JUMP_FORWARD          0  'to 369'
       369_0  COME_FROM                '366'
       369_1  COME_FROM                '110'

 109     369  LOAD_GLOBAL           3  'math3d'
         372  LOAD_ATTR             4  'vector'
         375  LOAD_FAST             4  'cur_cam_pos'
         378  CALL_FUNCTION_VAR_0     0 
         381  STORE_FAST           12  'cam_pos_vec'

 110     384  LOAD_FAST            12  'cam_pos_vec'
         387  LOAD_FAST             3  'MAP_RT_CONF'
         390  LOAD_CONST           19  'cam_pos'
         393  STORE_SUBSCR     

 112     394  LOAD_GLOBAL          19  'RenderTargetHolder'
         397  LOAD_CONST            0  ''
         400  LOAD_FAST             1  'sprite_obj'
         403  LOAD_FAST             3  'MAP_RT_CONF'
         406  LOAD_CONST           20  'all_light'
         409  LOAD_CONST           21  'dir_light'
         412  BUILD_LIST_1          1 
         415  CALL_FUNCTION_259   259 
         418  LOAD_FAST             0  'self'
         421  STORE_ATTR           21  'rendet_target_holder'

 113     424  LOAD_FAST             0  'self'
         427  LOAD_ATTR            21  'rendet_target_holder'
         430  LOAD_ATTR            22  'scn'
         433  LOAD_ATTR            23  'load_env'
         436  LOAD_CONST           22  'scene/scene_env_confs/default_nx2_mobile.xml'
         439  CALL_FUNCTION_1       1 
         442  POP_TOP          

 114     443  LOAD_CONST           23  16777215
         446  LOAD_FAST             0  'self'
         449  LOAD_ATTR            21  'rendet_target_holder'
         452  LOAD_ATTR            22  'scn'
         455  STORE_ATTR           24  'background_color'

 115     458  LOAD_FAST             0  'self'
         461  LOAD_ATTR            21  'rendet_target_holder'
         464  LOAD_ATTR            25  'apply_conf'
         467  LOAD_CONST           24  'zhanshi'
         470  CALL_FUNCTION_1       1 
         473  POP_TOP          

 117     474  LOAD_GLOBAL          26  'weakref'
         477  LOAD_ATTR            27  'ref'
         480  LOAD_FAST             0  'self'
         483  LOAD_ATTR            21  'rendet_target_holder'
         486  LOAD_ATTR            22  'scn'
         489  CALL_FUNCTION_1       1 
         492  LOAD_FAST             0  'self'
         495  STORE_ATTR           28  'scene'

 118     498  LOAD_CONST           25  'model\\others\\bw_box.gim'
         501  STORE_FAST           13  'mpath'

 119     504  LOAD_GLOBAL          29  'resloader'
         507  LOAD_ATTR            30  'load_res_attr'

 120     510  LOAD_ATTR            26  'weakref'

 121     513  LOAD_FAST            13  'mpath'
         516  LOAD_FAST             0  'self'
         519  LOAD_ATTR            31  'on_load_box_model_complete'
         522  BUILD_MAP_0           0 
         525  LOAD_CONST           27  'res_type'

 122     528  LOAD_CONST           28  'MODEL'
         531  LOAD_CONST           29  'priority'

 123     534  LOAD_GLOBAL          32  'game3d'
         537  LOAD_ATTR            33  'ASYNC_HIGH'
         540  CALL_FUNCTION_517   517 
         543  POP_TOP          
         544  LOAD_CONST            0  ''
         547  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_517' instruction at offset 540

    def on_load_box_model_complete(self, model, userdata, *args):
        if global_data.battle:
            model.name = self.box_name
            model.visible = False
            self.is_scene_ready = True
            self.rendet_target_holder.scn.add_object(model)
            self.update_show_model()

    def update_show_model(self):
        if self.is_scene_ready:
            self.clear_models()
            self.lab_name.SetString('')
            self.temp_rank_title.setVisible(False)
            role_info_list = global_data.battle.get_top_nb_role_info()
            if len(role_info_list) <= self.index:
                return
            role_info = role_info_list[self.index]
            self.lab_name.SetString(role_info[2])
            fashion_data = role_info[3]
            title_type = rank_const.get_rank_use_title_type(role_info[4] or {})
            rank_info = rank_const.get_rank_use_title(role_info[4] or {})
            init_rank_title(self.temp_rank_title, title_type, rank_info)
            role_item_no = fashion_data.get(FASHION_POS_SUIT)
            if not role_item_no:
                role_id = role_info[1]
                role_item_no = confmgr.get('role_info', 'RoleInfo', 'Content', str(role_id), 'default_skin')[0]
            role_head_no = fashion_data.get(FASHION_POS_HEADWEAR, None)
            bag_id = fashion_data.get(FASHION_POS_BACK, None)
            suit_id = fashion_data.get(FASHION_POS_SUIT_2, None)
            other_pendants = [ fashion_data.get(pos) for pos in FASHION_OTHER_PENDANT_LIST ]
            if self.test_dressed_clothing_id:
                self.model_data = lobby_model_display_utils.get_lobby_model_data(self.test_dressed_clothing_id, consider_second_model=False)
            elif self.test_role_id:
                self.model_data = lobby_model_display_utils.get_lobby_model_data(self.test_role_id, consider_second_model=False)
            else:
                self.model_data = lobby_model_display_utils.get_lobby_model_data(role_item_no, head_id=role_head_no, bag_id=bag_id, suit_id=suit_id, other_pendants=other_pendants, consider_second_model=False)
            self.model_data[0]['show_anim'] = self.model_data[0]['end_anim']

            def on_finish_create_model(model, *args):
                pass

            self.on_change_display_model(self.model_data, create_callback=on_finish_create_model, is_render_target_model=True, support_mirror=False, loaded_human_res_callback=self.on_load_human_res_callback)
        return

    def on_change_display_model(self, model_data, **kwargs):
        self.model_data = model_data
        if not model_data:
            return
        for data in model_data:
            obj = CLobbyModel(self, data, **kwargs)
            self.model_objs.append(obj)

    def on_load_human_res_callback(self):
        self.rendet_target_holder.start_render_target(2)

    def clear_models(self):
        for obj in self.model_objs:
            obj.destroy()

        self.model_objs = []

    def destroy--- This code section failed: ---

 195       0  LOAD_GLOBAL           0  'resloader'
           3  LOAD_ATTR             1  'del_res_attr'
           6  LOAD_ATTR             1  'del_res_attr'
           9  LOAD_GLOBAL           2  'True'
          12  CALL_FUNCTION_3       3 
          15  POP_TOP          

 196      16  LOAD_FAST             0  'self'
          19  LOAD_ATTR             3  'clear_models'
          22  CALL_FUNCTION_0       0 
          25  POP_TOP          

 198      26  LOAD_FAST             0  'self'
          29  LOAD_ATTR             4  'rendet_target_holder'
          32  POP_JUMP_IF_FALSE    60  'to 60'

 199      35  LOAD_FAST             0  'self'
          38  LOAD_ATTR             4  'rendet_target_holder'
          41  LOAD_ATTR             5  'destroy'
          44  CALL_FUNCTION_0       0 
          47  POP_TOP          

 200      48  LOAD_CONST            0  ''
          51  LOAD_FAST             0  'self'
          54  STORE_ATTR            4  'rendet_target_holder'
          57  JUMP_FORWARD          0  'to 60'
        60_0  COME_FROM                '57'
          60  LOAD_CONST            0  ''
          63  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 12


class SingleSkinPic(object):

    def __init__(self, sprite_obj, lab_name, temp_rank_title, tier_nd, index, test_role_id=None, test_dressed_clothing_id=None, test_cur_cam_pos=None):
        self.index = index
        self.img = sprite_obj
        self.lab_name = lab_name
        self.temp_rank_title = temp_rank_title
        self.tier_nd = tier_nd
        self.test_role_id = test_role_id
        self.test_dressed_clothing_id = test_dressed_clothing_id
        self.test_cur_cam_pos = test_cur_cam_pos
        self.initwidget()

    def initwidget(self):
        pass

    def initialize(self, info_list):
        self.lab_name.SetString('')
        self.temp_rank_title.setVisible(False)
        if len(info_list) <= self.index:
            return False
        info = info_list[self.index]
        self.lab_name.SetString(info[2])
        title_type = rank_const.get_rank_use_title_type(info[4] or {})
        rank_info = rank_const.get_rank_use_title(info[4] or {})
        init_rank_title(self.temp_rank_title, title_type, rank_info)
        return True

    def refresh_common(self, info, img_path, dressed_clothing_id):
        self.img.SetDisplayFrameByPath('', img_path)
        self.img.ReConfPosition()
        dan_dict = {}
        if len(info) > 5:
            dan_dict = info[5]
        is_settled = dan_dict or False if 1 else True
        res_path = role_head_utils.get_dan_path(dan_dict.get('dan'), dan_dict.get('lv'), is_settled)
        self.tier_nd.img_tier.SetDisplayFrameByPath('', res_path)
        role_id = info[1]
        cur_cam_pos = None
        if self.test_cur_cam_pos:
            cur_cam_pos = self.test_cur_cam_pos
        else:
            camera_data = confmgr.get('island_data', str(role_id))
            if camera_data:
                skin_camera_data = camera_data.get(str(dressed_clothing_id), camera_data.get('0'))
                if skin_camera_data:
                    cur_cam_pos = skin_camera_data.get('cam_pos')
        if cur_cam_pos:
            ori_x, ori_y = self.img.GetPosition()
            self.img.SetPosition(ori_x + cur_cam_pos[0], ori_y + cur_cam_pos[1])
        return


class RoleSkinUIPic(SingleSkinPic):

    def __init__(self, sprite_obj, lab_name, temp_rank_title, tier_nd, index, test_role_id=None, test_dressed_clothing_id=None, test_cur_cam_pos=None):
        super(RoleSkinUIPic, self).__init__(sprite_obj, lab_name, temp_rank_title, tier_nd, index, test_role_id, test_dressed_clothing_id, test_cur_cam_pos)

    def initwidget(self):
        info_list = global_data.battle.get_top_nb_role_info()
        if not self.initialize(info_list):
            return
        info = info_list[self.index]
        role_id = info[1]
        fashion_data = info[3]
        dressed_clothing_id = fashion_data.get(FASHION_POS_SUIT)
        if not dressed_clothing_id:
            dressed_clothing_id = confmgr.get('role_info', 'RoleInfo', 'Content', str(role_id), 'default_skin')[0]
        if self.test_role_id:
            role_id = self.test_role_id
            dressed_clothing_id = confmgr.get('role_info', 'RoleInfo', 'Content', str(role_id), 'default_skin')[0]
        if self.test_dressed_clothing_id:
            dressed_clothing_id = self.test_dressed_clothing_id
        img_path = confmgr.get('role_info', 'RoleSkin', 'Content', str(dressed_clothing_id), 'img_role')
        self.refresh_common(info, img_path, dressed_clothing_id)


class MechaSkinUIPic(SingleSkinPic):

    def __init__(self, sprite_obj, lab_name, temp_rank_title, tier_nd, index, test_role_id=None, test_dressed_clothing_id=None, test_cur_cam_pos=None):
        super(MechaSkinUIPic, self).__init__(sprite_obj, lab_name, temp_rank_title, tier_nd, index, test_role_id, test_dressed_clothing_id, test_cur_cam_pos)

    def initwidget(self):
        info_list = global_data.battle.get_top_nb_mecha_info()
        if not self.initialize(info_list):
            return
        info = info_list[self.index]
        role_id = info[1]
        dict_data = info[3]
        fashion_data = dict_data.get('fashion', {})
        dressed_clothing_id = fashion_data.get(FASHION_POS_SUIT)
        if self.test_role_id:
            role_id = self.test_role_id
        if self.test_dressed_clothing_id:
            dressed_clothing_id = self.test_dressed_clothing_id
        img_path = confmgr.get('mecha_conf', 'SkinConfig', 'Content', str(dressed_clothing_id), 'img_path')
        self.refresh_common(info, img_path, dressed_clothing_id)


class BaseBestSkinShow(object):

    def __init__(self, parent, skin_type):
        self.parent = parent
        self.skin_type = skin_type
        self.chushegntai_model = None
        self.panel = None
        self.tex = None
        self.rt = None
        self._render_timer = None
        self._count_down_timer = None
        self._ui_stage = None
        self.test_role_id = None
        self.test_dressed_clothing_id = None
        self.test_cur_cam_pos = None
        self._ui_skin_model_list = []
        self._ui_skin_pic_list = []
        self.sub_mesh_name = None
        return

    def re_play(self, role_id=None, skin_id=None, test_cur_cam_pos=None):
        self.test_role_id = role_id
        self.test_dressed_clothing_id = skin_id
        self.test_cur_cam_pos = test_cur_cam_pos
        self.destroy_test()
        self.load_chushengtai_finish()

    def load_chushengtai_finish(self):
        if global_data.enable_island_chushengtai_ui_refresh:
            self.init_panel()
        self.refresh()

    def init_panel(self):
        resource_path = 'battle_before/hot_ranking_newmap'
        self.panel = global_data.uisystem.load_template_create(resource_path)
        self.panel.retain()
        self.panel.lab_star.SetString(get_text_by_id(19845))
        self.panel.lab_stat.SetString(get_text_by_id(19845))
        self.panel.temp_time.lab_title.SetString(get_text_by_id(83145))
        size = self.panel.getContentSize()
        old_design_size = global_data.ui_mgr.design_screen_size
        scale = min(old_design_size.width / size.width, old_design_size.height / size.height)
        if global_data.is_low_mem_mode:
            scale = scale * 0.5
        render_texture_size = (
         size.width * scale, size.height * scale)
        self.panel.setAnchorPoint(cc.Vec2(0, 0))
        if game3d.get_render_device() not in (game3d.DEVICE_GLES, game3d.DEVICE_GL):
            self.panel.setScale(scale)
            self.panel.SetPosition(0, 0)
        else:
            self.panel.setScaleX(scale)
            self.panel.setScaleY(-scale)
            self.panel.SetPosition(0, size.height * scale)
        self.tex = render.texture.create_empty(int(render_texture_size[0]), int(render_texture_size[1]), render.PIXEL_FMT_A8R8G8B8, True)
        self.rt = cc.RenderTexture.createWithITexture(self.tex)
        self.rt.retain()
        if self.sub_mesh_name:
            self.chushegntai_model.get_sub_material(self.sub_mesh_name).set_texture(_HASH, 'Tex0', self.tex)
        else:
            self.chushegntai_model.all_materials.set_texture(_HASH, 'Tex0', self.tex)
        self.start_render()

    def start_render(self):
        self.stop_render()
        self._render_timer = global_data.game_mgr.register_logic_timer(self.tick, RENDER_TICK_INTERVAL, mode=CLOCK)

    def stop_render(self):
        if self._render_timer:
            global_data.game_mgr.unregister_logic_timer(self._render_timer)
            self._render_timer = None
        return

    def tick(self):
        if global_data.battle:
            if self._ui_stage:
                self._ui_stage(RENDER_TICK_INTERVAL)
            self._draw_ui_to_rt(self.rt, self.panel)

    @sync_exec
    def _draw_ui_to_rt(self, rt, panel):
        if not panel or not panel.isValid():
            return
        rt.beginWithClear(0, 0, 0, 0)
        if hasattr(rt, 'addCommandsForNode'):
            rt.addCommandsForNode(panel.get())
        else:
            panel.visit()
        rt.end()

    def refresh_best_skin(self):
        if self.skin_type == SKIN_TYPE_ROLE:
            SingleSkinPicClass = RoleSkinUIPic
        else:
            SingleSkinPicClass = MechaSkinUIPic
        self._ui_skin_pic_list = []
        first_single_skin = SingleSkinPicClass(self.panel.img_role_first, self.panel.lab_name_first, self.panel.cut_middle.temp_title_2, self.panel.temp_tier_first, 0, self.test_role_id, self.test_dressed_clothing_id, self.test_cur_cam_pos)
        self._ui_skin_pic_list.append(first_single_skin)
        second_single_skin = SingleSkinPicClass(self.panel.img_role_second, self.panel.lab_name_second, self.panel.cut_left.temp_title_1, self.panel.temp_tier_second, 1, self.test_role_id, self.test_dressed_clothing_id, self.test_cur_cam_pos)
        self._ui_skin_pic_list.append(second_single_skin)
        third_single_skin = SingleSkinPicClass(self.panel.img_role_third, self.panel.lab_name_third, self.panel.cut_right.temp_title_3, self.panel.temp_tier_third, 2, self.test_role_id, self.test_dressed_clothing_id, self.test_cur_cam_pos)
        self._ui_skin_pic_list.append(third_single_skin)
        self.panel.PlayAnimation('stage3_human', force_resume=True)

    def start_count_down_timer(self):
        self.stop_count_down_timer()
        self._count_down_timer = global_data.game_mgr.register_logic_timer(self.update_ui_state_count_down, interval=1, times=-1, mode=CLOCK)

    def stop_count_down_timer(self):
        if self._count_down_timer:
            global_data.game_mgr.unregister_logic_timer(self._count_down_timer)
            self._count_down_timer = None
        return

    def update_ui_state_count_down(self):
        if global_data.battle:
            next_refresh_timestamp = global_data.battle.get_next_island_refresh_ts()
            if next_refresh_timestamp:
                left_time = next_refresh_timestamp - tutil.get_server_time()
                left_time = int(max(0, left_time))
                self.panel.temp_time.lab_time.SetString(str(left_time) + 'S')
                if left_time == 0:
                    self.stop_count_down_timer()

    def change_to_count_down(self):
        self._ui_stage = None
        self.refresh_best_skin()
        self.update_ui_state_count_down()
        self.start_count_down_timer()
        return

    def change_to_stage1_loop(self):
        self._ui_stage = None
        self.panel.PlayAnimation('stage1_loop', force_resume=True)
        return

    def change_to_stage2_show(self):
        self.stage2_show_time = 0
        self._ui_stage = self.stage2_show_func
        self.panel.PlayAnimation('stage2_show', force_resume=True)

    def stage2_show_func(self, interval):
        self.stage2_show_time += RENDER_TICK_INTERVAL
        if self.stage2_show_time > 0.6:
            self.change_to_count_down()

    def change_stage3_lock(self):
        self.stage3_lock_time = 0
        self._ui_stage = self.stage3_lock_func
        self.panel.PlayAnimation('stage3_lock', force_resume=True)
        self.panel.temp_time.lab_title.SetString(get_text_by_id(80448))
        self.panel.temp_time.lab_time.setVisible(False)
        self.panel.temp_time.nd_auto_fit.img_icon.setVisible(False)

    def stage3_lock_func(self, interval):
        self.stage3_lock_time += RENDER_TICK_INTERVAL
        if self.stage3_lock_time > 1:
            self._ui_stage = None
            self.refresh_best_skin()
        return

    def refresh_ui_state(self):
        if not self.panel or not global_data.battle:
            return
        next_refresh_timestamp = global_data.battle.get_next_island_refresh_ts()
        if next_refresh_timestamp == -1:
            self.change_stage3_lock()
            self.stop_count_down_timer()
        elif len(global_data.battle.get_top_nb_role_info()) == 0:
            self.change_to_stage1_loop()
        else:
            left_time = next_refresh_timestamp - tutil.get_server_time()
            if left_time > 2:
                self.change_to_stage2_show()
            else:
                self.change_to_count_down()

    def refresh(self):
        self.start_render()
        self.refresh_ui_state()

    def destroy_ui_kin_model(self):
        for skin_model in self._ui_skin_model_list:
            skin_model.destroy()

        self._ui_skin_model_list = []

    def destroy_test(self):
        self.stop_render()
        if self.rt:
            self.rt.release()
        self.rt = None
        self.tex = None
        if self.panel:
            self.panel.release()
            self.panel = None
        self.stop_count_down_timer()
        self.destroy_ui_kin_model()
        return

    def destroy(self):
        self.destroy_test()


class BwBestSkinShow(BaseBestSkinShow):

    def __init__(self, parent, skin_type):
        super(BwBestSkinShow, self).__init__(parent, skin_type)
        self._scene_skin_model_dict = {}
        self.sub_mesh_name = 'chushengtai_role_b' if self.skin_type == SKIN_TYPE_ROLE else 'chushengtai_mecha_b'
        self.load_chushengtai_task = None
        self.load_chushengtai()
        return

    def load_chushengtai(self):
        if not global_data.battle.area_id:
            return
        else:
            born_data = global_data.game_mode.get_born_data()
            cur_area = born_data[str(global_data.battle.area_id)]
            data = None
            res_path = None
            if self.skin_type == SKIN_TYPE_ROLE:
                data = [
                 cur_area.get('role_pos'), cur_area.get('role_rot'), cur_area.get('role_scale')]
                res_path = confmgr.get('script_gim_ref')['chushengtai_role']
            else:
                data = [
                 cur_area.get('mecha_pos'), cur_area.get('mecha_rot'), cur_area.get('mecha_scale')]
                res_path = confmgr.get('script_gim_ref')['chushengtai_mecha']
            self.load_chushengtai_task = world.create_model_async(res_path, self.on_chushengtai_model_loaded, data, game3d.ASYNC_HIGH)
            return

    def on_chushengtai_model_loaded(self, model, data, task, *args):
        if global_data.battle:
            self.chushegntai_model = model
            self.chushegntai_model.all_materials.set_macro('LIGHT_MAP_ENABLE', 'FALSE')
            self.chushegntai_model.all_materials.rebuild_tech()
            model.world_position = math3d.vector(*data[0])
            rot = [ math.radians(i) for i in data[1] ]
            rotation_matrix = math3d.rotation_to_matrix(math3d.euler_to_rotation(math3d.vector(*rot)))
            model.world_rotation_matrix = rotation_matrix
            scene = self.parent.get_scene()
            if scene and scene.valid:
                scene.add_object(model)
                model.active_collision = True
            self.load_chushengtai_finish()

    def refresh_best_skin(self):
        super(BwBestSkinShow, self).refresh_best_skin()
        if self.chushegntai_model:
            self.refresh_scene_model()

    def destroy_scene_model(self):
        for skin_model in six.itervalues(self._scene_skin_model_dict):
            skin_model.destroy()

    def refresh_scene_model(self):
        if self.skin_type == SKIN_TYPE_ROLE:
            info_list = global_data.battle.get_top_nb_role_info()
        else:
            info_list = global_data.battle.get_top_nb_mecha_info()
        new_model_dict = {}
        for i in range(3):
            if len(info_list) > i:
                info = info_list[i]
                obj_id = info[0]
                role_name = info[2]
                cur_skin_model = self.get_scene_skin_model(obj_id)
                if cur_skin_model:
                    cur_skin_model.update_pos(i)
                elif self.skin_type == SKIN_TYPE_ROLE:
                    cur_skin_model = BestRoleModelAppearance(i, self.chushegntai_model)
                else:
                    cur_skin_model = BestMechaModelAppearance(i, self.chushegntai_model)
                new_model_dict[role_name] = cur_skin_model

        for key, skin_model in six.iteritems(self._scene_skin_model_dict):
            if key not in new_model_dict:
                skin_model.destroy()

        self._scene_skin_model_dict = new_model_dict

    def get_scene_skin_model(self, obj_id):
        for skin_model in six.itervalues(self._scene_skin_model_dict):
            if skin_model.obj_id == obj_id:
                return skin_model

    def destroy_test(self):
        super(BwBestSkinShow, self).destroy_test()
        self.destroy_scene_model()

    def destroy(self):
        super(BwBestSkinShow, self).destroy()
        if self.chushegntai_model and self.chushegntai_model.valid:
            self.chushegntai_model.destroy()
        self.chushegntai_model = None
        if self.load_chushengtai_task:
            self.load_chushengtai_task.cancel()
            self.load_chushengtai_task = None
        return


class KongdaoBestSkinShow(BaseBestSkinShow):

    def __init__(self, parent, skin_type):
        super(KongdaoBestSkinShow, self).__init__(parent, skin_type)
        self.sub_mesh_name = 'chushengtai_role_011'
        self.chushegntai_obj_name = 'chushengtai_role_01515151' if skin_type == SKIN_TYPE_ROLE else 'chushengtai_role_2505050'
        self.origin_tex0 = 'model_new/scene/kongdao_final/zycz/texture/item/chushengtai_role_01/chushengtaikd_mecha_01_bc.tga'
        self.load_chushengtai_timer = None
        self.check_chushengtai()
        return

    def check_chushengtai(self):
        scene = self.parent.get_scene()
        model = scene.get_model(self.chushegntai_obj_name)
        if model and model.valid:
            self.chushegntai_model = model
            self.chushegntai_model.scale = math3d.vector(model.scale.x, model.scale.y, model.scale.z * 1.1)
            self.stop_load_chushengtai()
            self.load_chushengtai_finish()
        elif not self.load_chushengtai_timer:
            self.load_chushengtai_timer = global_data.game_mgr.register_logic_timer(self.check_chushengtai, 2, mode=CLOCK)

    def stop_load_chushengtai(self):
        if self.load_chushengtai_timer:
            global_data.game_mgr.unregister_logic_timer(self.load_chushengtai_timer)
            self.load_chushengtai_timer = None
        return

    def destroy(self):
        super(KongdaoBestSkinShow, self).destroy()
        self.stop_load_chushengtai()
        if self.chushegntai_model and self.chushegntai_model.valid:
            self.chushegntai_model.get_sub_material(self.sub_mesh_name).set_texture(_HASH, 'Tex0', self.origin_tex0)
            self.chushegntai_model.scale = math3d.vector(self.chushegntai_model.scale.x, self.chushegntai_model.scale.y, self.chushegntai_model.scale.z / 1.1)


class ConcertBestSkinShow(BaseBestSkinShow):

    def __init__(self, parent, skin_type):
        super(ConcertBestSkinShow, self).__init__(parent, skin_type)
        self.sub_mesh_name = ''
        self.load_chushengtai_task = None
        self.load_chushengtai()
        return

    def get_model_info(self, _tv_id):
        from logic.client.path_utils import DEFAULT_TV_PATH
        tv_e_conf = confmgr.get('tv_conf', 'cl_tv_entity', 'Content', default={})
        tv_c_conf = confmgr.get('tv_conf', 'tv_channel', 'Content', default={})
        channel_id = tv_e_conf.get(str(_tv_id), {}).get('channel_id', 1)
        pos = tv_e_conf.get(str(_tv_id), {}).get('pos', [0, 0, 0])
        rot = tv_e_conf.get(str(_tv_id), {}).get('rot', [0, 0, 0, 1])
        if rot is None:
            rot = [0, 0, 0, 1] if 1 else rot
            model_path = tv_e_conf.get(str(_tv_id), {}).get('model_path', '')
            model_path = model_path or tv_c_conf.get(str(channel_id), {}).get('model_path', DEFAULT_TV_PATH)
        model_scale = tv_e_conf.get(str(_tv_id), {}).get('scale', [1, 1, 1])
        return (
         model_path, (pos, rot, model_scale), int(channel_id))

    def load_chushengtai(self):
        model_path, transform, channel_id = self.get_model_info(30001)
        res_path = model_path
        data = transform
        self.load_chushengtai_task = world.create_model_async(res_path, self.on_chushengtai_model_loaded, data, game3d.ASYNC_HIGH)

    def on_chushengtai_model_loaded(self, model, data, task, *args):
        if global_data.battle:
            self.chushegntai_model = model
            rot = [ math.radians(i) for i in data[1] ]
            scale = math3d.vector(*data[2])
            rotation_matrix = math3d.rotation_to_matrix(math3d.euler_to_rotation(math3d.vector(*rot)))
            model.world_rotation_matrix = rotation_matrix
            model.scale = scale
            model.world_position = math3d.vector(*data[0])
            scene = self.parent.get_scene()
            if scene and scene.valid:
                scene.add_object(model)
            self.load_chushengtai_finish()

    def destroy(self):
        super(ConcertBestSkinShow, self).destroy()
        if self.chushegntai_model and self.chushegntai_model.valid:
            self.chushegntai_model.destroy()
        self.chushegntai_model = None
        if self.load_chushengtai_task:
            self.load_chushengtai_task.cancel()
            self.load_chushengtai_task = None
        return


class ConcertKizunaSkinShow(object):

    def __init__(self, skin_type=SKIN_TYPE_ROLE):
        self.chushegntai_model = None
        self.skin_type = skin_type
        self._scene_skin_model_dict = {}
        self.load_chushengtai()
        return

    def destroy(self):
        self.destroy_scene_model()
        if self.chushegntai_model and self.chushegntai_model.valid:
            self.chushegntai_model.destroy()
        self.chushegntai_model = None
        if self.load_chushengtai_task:
            self.load_chushengtai_task.cancel()
            self.load_chushengtai_task = None
        return

    def load_chushengtai(self):
        data = None
        res_path = None
        data = [
         (254.23, 810.13, 2313.94), (0, 336, 0), (1, 1, 1)]
        res_path = confmgr.get('script_gim_ref')['concert_chushengtai_role']
        self.load_chushengtai_task = world.create_model_async(res_path, self.on_chushengtai_model_loaded, data, game3d.ASYNC_HIGH)
        return

    def on_chushengtai_model_loaded(self, model, data, task, *args):
        if global_data.battle:
            self.chushegntai_model = model
            self.chushegntai_model.all_materials.set_macro('LIGHT_MAP_ENABLE', 'FALSE')
            self.chushegntai_model.all_materials.rebuild_tech()
            model.world_position = math3d.vector(*data[0])
            rot = [ math.radians(i) for i in data[1] ]
            rotation_matrix = math3d.rotation_to_matrix(math3d.euler_to_rotation(math3d.vector(*rot)))
            model.world_rotation_matrix = rotation_matrix
            scene = global_data.game_mgr.scene
            if scene and scene.valid:
                scene.add_object(model)
                model.active_collision = True
                self.refresh_scene_model()

    def destroy_scene_model(self):
        for skin_model in six.itervalues(self._scene_skin_model_dict):
            skin_model.destroy()

        self._scene_skin_model_dict = {}

    def refresh_scene_model(self):
        if not self.chushegntai_model:
            return
        from logic.gutils.item_utils import get_lobby_item_name, get_lobby_item_belong_no
        skin_list = (201011100, 201011151, 201011153, 201011152)
        info_list = [ [i, get_lobby_item_belong_no(i), get_lobby_item_name(i), {FASHION_POS_SUIT: i}, {'scale': 1.3}] for i in skin_list ]
        new_model_dict = {}
        for i in range(len(skin_list)):
            if len(info_list) > i:
                info = info_list[i]
                obj_id = info[0]
                role_name = info[2]
                cur_skin_model = self.get_scene_skin_model(obj_id)
                if cur_skin_model:
                    cur_skin_model.update_pos(i)
                elif self.skin_type == SKIN_TYPE_ROLE:
                    cur_skin_model = BestRoleModelAppearanceConcert(i, self.chushegntai_model, force_info_list=info_list)
                else:
                    cur_skin_model = BestMechaModelAppearance(i, self.chushegntai_model, force_info_list=info_list)
                new_model_dict[role_name] = cur_skin_model

        for key, skin_model in six.iteritems(self._scene_skin_model_dict):
            if key not in new_model_dict:
                skin_model.destroy()

        self._scene_skin_model_dict = new_model_dict

    def get_scene_skin_model(self, obj_id):
        for skin_model in six.itervalues(self._scene_skin_model_dict):
            if skin_model.obj_id == obj_id:
                return skin_model


class ConcertBestSkinShowWithModel(BwBestSkinShow):

    def load_chushengtai(self):
        if not global_data.battle.area_id:
            return
        else:
            data = None
            res_path = None
            if self.skin_type == SKIN_TYPE_ROLE:
                data = [
                 (396.52, 301.63, -1086.04), (0, 160, 0), (0.87, 0.49, 1)]
                res_path = confmgr.get('script_gim_ref')['concert_best_skin_role']
            else:
                data = [
                 (-1130.85, 23.6, 51.79), (0, 0, 0), (1, 1, 1)]
                res_path = confmgr.get('script_gim_ref')['chushengtai_mecha']
            self.load_chushengtai_task = world.create_model_async(res_path, self.on_chushengtai_model_loaded, data, game3d.ASYNC_HIGH)
            return