# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEMainUIWidgetUI/PVEPetWidgetUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_1, UI_VKB_CLOSE
from logic.comsys.lobby.PetItemListWidget import PetItemListWidget
from logic.comsys.lobby.PetLevelWidget import PetLevelWidget
from logic.comsys.lobby.PetSkillWidget import PetSkillWidget
from logic.gutils.items_book_utils import get_items_skin_conf
from logic.client.const.items_book_const import PET_ID
from logic.gcommon.common_const.scene_const import SCENE_PVE_BOOK_WIDGET_UI
from logic.client.const.lobby_model_display_const import PVE_BOOK_WIDGET_UI
from logic.gcommon.common_const.pve_const import PVE_BOOK_DEFAULT_BG_PATH
from logic.gutils.pve_utils import reset_model_and_cam_pos, reset_cam_pos, get_attr_desc_text
from logic.gutils import lobby_model_display_utils
from logic.gutils.pet_utils import get_pet_level, get_pet_skill_level
from logic.gutils.mall_utils import item_can_use_by_item_no
from logic.gutils.scene_utils import cocos_pos_to_ui_world_pos
from common.framework import Functor
from logic.gutils import item_utils
from common.cfg import confmgr
import six_ex
import math3d
ROTATE_FACTOR = 850
SELECT_PET_ANIM_TIME = 1
PERSPECTIVE_RATIO = 0.8
MAX_MODEL_COUNT = 3

class PVEPetWidgetUI(BasePanel):
    DELAY_CLOSE_TAG = 20240109
    PANEL_CONFIG_NAME = 'pve/pet/pve_pet_main'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'btn_close.OnClick': 'close'
       }

    def on_init_panel(self, *args, **kwargs):
        super(PVEPetWidgetUI, self).on_init_panel()
        self.init_params()
        self.init_ui_events()
        self.do_switch_scene()

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'pve_pet_choosen_changed': self._on_pve_pet_choosen_changed,
           'pve_pet_backup_changed': self._on_pve_pet_choosen_changed,
           'pet_info_updated': self._on_pet_info_updated,
           'resolution_changed_end': self._on_resolution_changed_end
           }
        emgr.bind_events(econf) if is_bind else emgr.unbind_events(econf)

    def init_params(self):
        self._disappearing = False
        self._is_playing_select_anim = False
        self._is_in_expand_mode = False
        self._skin_list_widget = None
        self._level_widget = None
        self._skill_widget = None
        self._pet_conf = confmgr.get('c_pet_info', default={})
        self._pet_skill_conf = confmgr.get('pet_skill', default={})
        self._skin_config_dict = get_items_skin_conf(PET_ID)
        self._lobby_model_list = [None, None, None]
        self._cur_click_model = None
        self._show_cur_click_model_complete = True
        self._list_item = None
        self._cur_show_level = 0
        self._cur_select_slot = 0
        self.cur_skin_idx = 0
        self._get_skin_list()
        self._pet_pos_list_hide = []
        self._pet_pos_list_show = []
        self._has_init_model = False
        self._pet_type_list = [self.panel.temp_type_mid, self.panel.temp_type_left, self.panel.temp_type_right]
        self._pet_dict = global_data.player.get_pve_pet_dict() if global_data.player else {0: 0,1: 0,2: 0}
        self._cur_skin_id_list = [self._pet_dict.get(0), self._pet_dict.get(1), self._pet_dict.get(2)]
        return

    def _get_skin_list(self):

        def sort_function--- This code section failed: ---

  87       0  LOAD_GLOBAL           0  'int'
           3  LOAD_FAST             0  'pet_id'
           6  CALL_FUNCTION_1       1 
           9  STORE_FAST            0  'pet_id'

  88      12  LOAD_GLOBAL           1  'global_data'
          15  LOAD_ATTR             2  'player'
          18  POP_JUMP_IF_FALSE    36  'to 36'
          21  LOAD_GLOBAL           1  'global_data'
          24  LOAD_ATTR             2  'player'
          27  LOAD_ATTR             3  'get_pve_choosen_pet'
          30  CALL_FUNCTION_0       0 
        33_0  COME_FROM                '18'
          33  JUMP_IF_TRUE_OR_POP    39  'to 39'
          36  LOAD_CONST            0  ''
        39_0  COME_FROM                '33'
          39  STORE_FAST            1  'choosen_pet'

  89      42  LOAD_FAST             1  'choosen_pet'
          45  POP_JUMP_IF_FALSE    90  'to 90'

  90      48  LOAD_DEREF            0  'self'
          51  LOAD_ATTR             5  '_pet_conf'
          54  LOAD_ATTR             6  'get'
          57  LOAD_GLOBAL           7  'str'
          60  LOAD_FAST             1  'choosen_pet'
          63  CALL_FUNCTION_1       1 
          66  BUILD_MAP_0           0 
          69  CALL_FUNCTION_2       2 
          72  LOAD_ATTR             6  'get'
          75  LOAD_CONST            1  'base_skin'
          78  LOAD_FAST             1  'choosen_pet'
          81  CALL_FUNCTION_2       2 
          84  STORE_FAST            1  'choosen_pet'
          87  JUMP_FORWARD          0  'to 90'
        90_0  COME_FROM                '87'

  91      90  LOAD_GLOBAL           7  'str'
          93  LOAD_FAST             0  'pet_id'
          96  CALL_FUNCTION_1       1 
          99  LOAD_GLOBAL           7  'str'
         102  LOAD_FAST             1  'choosen_pet'
         105  CALL_FUNCTION_1       1 
         108  COMPARE_OP            2  '=='
         111  STORE_FAST            2  'is_pve_choosen_pet'

  93     114  LOAD_GLOBAL           1  'global_data'
         117  LOAD_ATTR             2  'player'
         120  POP_JUMP_IF_FALSE   138  'to 138'
         123  LOAD_GLOBAL           1  'global_data'
         126  LOAD_ATTR             2  'player'
         129  LOAD_ATTR             8  'get_pve_backup_pet_pet_list'
         132  CALL_FUNCTION_0       0 
         135  JUMP_FORWARD          3  'to 141'
         138  BUILD_LIST_0          0 
       141_0  COME_FROM                '135'
         141  STORE_FAST            3  'pve_backup_pet_list'

  94     144  LOAD_FAST             0  'pet_id'
         147  LOAD_FAST             3  'pve_backup_pet_list'
         150  COMPARE_OP            6  'in'
         153  STORE_FAST            4  'is_pve_backup_pet'

  96     156  LOAD_GLOBAL           9  'bool'
         159  LOAD_GLOBAL           1  'global_data'
         162  LOAD_ATTR             2  'player'
         165  JUMP_IF_FALSE_OR_POP   183  'to 183'
         168  LOAD_GLOBAL           1  'global_data'
         171  LOAD_ATTR             2  'player'
         174  LOAD_ATTR            10  'get_item_by_no'
         177  LOAD_FAST             0  'pet_id'
         180  CALL_FUNCTION_1       1 
       183_0  COME_FROM                '165'
         183  CALL_FUNCTION_1       1 
         186  STORE_FAST            5  'has_pet'

  98     189  LOAD_GLOBAL          11  'item_utils'
         192  LOAD_ATTR            12  'get_item_rare_degree'
         195  LOAD_ATTR             2  'player'
         198  CALL_FUNCTION_2       2 
         201  STORE_FAST            6  'rare_degree'

 101     204  LOAD_FAST             6  'rare_degree'
         207  LOAD_CONST            3  5
         210  COMPARE_OP            2  '=='
         213  POP_JUMP_IF_FALSE   225  'to 225'

 102     216  LOAD_CONST            4  6
         219  STORE_FAST            6  'rare_degree'
         222  JUMP_FORWARD         21  'to 246'

 103     225  LOAD_FAST             6  'rare_degree'
         228  LOAD_CONST            4  6
         231  COMPARE_OP            2  '=='
         234  POP_JUMP_IF_FALSE   246  'to 246'

 104     237  LOAD_CONST            3  5
         240  STORE_FAST            6  'rare_degree'
         243  JUMP_FORWARD          0  'to 246'
       246_0  COME_FROM                '243'
       246_1  COME_FROM                '222'

 106     246  LOAD_FAST             2  'is_pve_choosen_pet'
         249  LOAD_FAST             4  'is_pve_backup_pet'
         252  LOAD_FAST             5  'has_pet'
         255  LOAD_FAST             6  'rare_degree'
         258  LOAD_FAST             0  'pet_id'
         261  BUILD_TUPLE_5         5 
         264  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 198

        valid_skin_list = []
        inner_skin_list = []
        for skin_id in six_ex.keys(self._pet_conf):
            if not item_utils.is_itemtype_in_serving(skin_id):
                continue
            base_skin = self._pet_conf[skin_id].get('base_skin', skin_id)
            if str(base_skin) != str(skin_id):
                continue
            if self._skin_config_dict.get(skin_id, {}).get('inner_skin', 0):
                inner_skin_list.append(skin_id)
            else:
                valid_skin_list.append(skin_id)

        self.skin_list = valid_skin_list
        self.skin_list.sort(key=lambda x: sort_function(x), reverse=True)

    def init_ui(self):
        self._list_item = self.panel.nd_left.list_item
        self._has_init_model = self._pet_dict.get(0) == 0 and self._pet_dict.get(1) == 0 and self._pet_dict.get(2) == 0
        self._skin_list_widget = PetItemListWidget(self, self._list_item, self.on_create_skin_item, 6)
        self._level_widget = PetLevelWidget(self.panel, None)
        self._skill_widget = PetSkillWidget(self.panel)
        self._skin_list_widget.update_skin_data(self.skin_list, init_index=self.cur_skin_idx)
        return

    def init_ui_events(self):

        @self.panel.btn_show.unique_callback()
        def OnClick(btn, touch):
            if not self.panel:
                return
            if self._is_playing_select_anim:
                return
            self._expand_panel()

        @self.panel.temp_type_mid.bar_type_fight.lab_type.nd_auto_fit.btn_describe.unique_callback()
        def OnClick(btn, touch, *args):
            self._on_click_rule()

        @self.panel.temp_type_mid.bar_type_ready.lab_type.nd_auto_fit.btn_describe.unique_callback()
        def OnClick(btn, touch, *args):
            self._on_click_rule()

        @self.panel.temp_type_left.bar_type_fight.lab_type.nd_auto_fit.btn_describe.unique_callback()
        def OnClick(btn, touch, *args):
            self._on_click_rule()

        @self.panel.temp_type_left.bar_type_ready.lab_type.nd_auto_fit.btn_describe.unique_callback()
        def OnClick(btn, touch, *args):
            self._on_click_rule()

        @self.panel.temp_type_right.bar_type_fight.lab_type.nd_auto_fit.btn_describe.unique_callback()
        def OnClick(btn, touch, *args):
            self._on_click_rule()

        @self.panel.temp_type_right.bar_type_ready.lab_type.nd_auto_fit.btn_describe.unique_callback()
        def OnClick(btn, touch, *args):
            self._on_click_rule()

        @self.panel.temp_type_left.btn_add.unique_callback()
        def OnClick(btn, touch, *args):
            self._rotate_pet_counterclockwise()

        @self.panel.temp_type_right.btn_add.unique_callback()
        def OnClick(btn, touch, *args):
            self._rotate_pet_clockwise()

        @self.panel.btn_left.unique_callback()
        def OnClick(btn, touch):
            self._rotate_pet_counterclockwise()

        @self.panel.btn_right.unique_callback()
        def OnClick(btn, touch):
            self._rotate_pet_clockwise()

        @self.panel.nd_mech_pet_left.unique_callback()
        def OnClick(btn, touch):
            self._rotate_pet_counterclockwise()

        @self.panel.nd_mech_pet_right.unique_callback()
        def OnClick(btn, touch):
            self._rotate_pet_clockwise()

        @self.panel.btn_fight.unique_callback()
        def OnClick(btn, touch):
            if not global_data.player:
                return
            skin_id = self._cur_skin_id_list[self._cur_select_slot]
            real_skin_no = global_data.player.get_pet_sub_skin_choose(skin_id)
            global_data.player.set_pve_choosen_pet(real_skin_no)

        @self.panel.btn_ready.unique_callback()
        def OnClick(btn, touch):
            if not global_data.player:
                return
            pve_backup_pet_list = global_data.player.get_pve_backup_pet_pet_list()
            skin_id = self._cur_skin_id_list[self._cur_select_slot]
            if skin_id in pve_backup_pet_list:
                pve_backup_pet_list[pve_backup_pet_list.index(skin_id)] = 0
            pve_backup_pet_list[self._cur_select_slot - 1] = int(skin_id)
            global_data.player.set_pve_backup_pet_list(pve_backup_pet_list)

        @self.panel.btn_cancel.unique_callback()
        def OnClick(btn, touch):
            if not global_data.player:
                return
            if self._cur_select_slot == 0:
                global_data.player.set_pve_choosen_pet(0)
                self._unselect_skin_item()
            else:
                pve_backup_pet_list = global_data.player.get_pve_backup_pet_pet_list()
                pve_backup_pet_list[self._cur_select_slot - 1] = 0
                global_data.player.set_pve_backup_pet_list(pve_backup_pet_list)
                self._unselect_skin_item()

        @self.panel.nd_mech_pet_mid.unique_callback()
        def OnDrag(layer, touch):
            self._on_rotate_drag(0, touch)

        @self.panel.nd_mech_pet_mid2.unique_callback()
        def OnDrag(layer, touch):
            self._on_rotate_drag(0, touch)

        @self.panel.nd_mech_pet_left.unique_callback()
        def OnDrag(layer, touch):
            self._on_rotate_drag(1, touch)

        @self.panel.nd_mech_pet_right.unique_callback()
        def OnDrag(layer, touch):
            self._on_rotate_drag(2, touch)

        @self.panel.temp_title.lab_title.nd_auto_fit.btn_describe.callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(860356, 860357)

        @self.panel.btn_go.btn.unique_callback()
        def OnClick(btn, touch):
            skin_no = self._cur_skin_id_list[self._cur_select_slot]
            if not skin_no:
                return
            item_utils.jump_to_ui(skin_no)

    def _update_expand_camera(self):
        self._is_playing_select_anim = True
        self.panel.DelayCall(SELECT_PET_ANIM_TIME, self._set_playing_select_anim)
        for index, lobby_model in enumerate(self._lobby_model_list):
            if lobby_model:
                target_pet_off_pos_list = self._pet_pos_list_hide if self._is_in_expand_mode else self._pet_pos_list_show
                lobby_model.change_model_off_position(target_pet_off_pos_list[index], True)

        if self._cur_click_model:
            target_pet_off_pos_list = self._pet_pos_list_hide if self._is_in_expand_mode else self._pet_pos_list_show
            self._cur_click_model.change_model_off_position(target_pet_off_pos_list[self._cur_select_slot], True)

    def _set_playing_select_anim(self):
        self._is_playing_select_anim = False
        if self._is_in_expand_mode:
            self.panel.PlayAnimation('reset')
        else:
            self.panel.PlayAnimation('reset_more')
        self._update_pet_type_widget()

    def _on_select_next_or_previous_pet(self):
        self._is_playing_select_anim = True
        self.panel.DelayCall(SELECT_PET_ANIM_TIME, self._set_playing_select_anim)
        if self._cur_click_model:
            self._cur_click_model.hide_model()
        for index, lobby_model in enumerate(self._lobby_model_list):
            if lobby_model:
                pet_off_pos_list = self._pet_pos_list_show if self._is_in_expand_mode else self._pet_pos_list_hide
                lobby_model.change_model_off_position(pet_off_pos_list[index], True)
                lobby_model.show_model()
                ref_model = lobby_model.get_model()
                if ref_model:
                    origin_scale = lobby_model.model_data.get('model_scale', 1)
                    if index == self._cur_select_slot:
                        scale = origin_scale
                    else:
                        scale = origin_scale * PERSPECTIVE_RATIO
                    ref_model.scale = math3d.vector(scale, scale, scale)

        self._update_widget()
        skin_no = self._cur_skin_id_list[self._cur_select_slot]
        if skin_no:
            skin_no = self._pet_conf.get(str(skin_no), {}).get('base_skin', skin_no)
            index = self.skin_list.index(str(skin_no))
            self._update_skin_item_select(index)
        else:
            self._unselect_skin_item()

    def _on_rotate_drag(self, index, touch):
        pass

    def _on_resolution_changed_end(self):
        if self._is_in_expand_mode:
            self.panel.PlayAnimation('reset')
            self.panel.PlayAnimation('list_more')
        else:
            self.panel.PlayAnimation('reset_more')
            self.panel.PlayAnimation('list_less')
        self._get_pet_off_pos_list()
        for index, lobby_model in enumerate(self._lobby_model_list):
            if lobby_model:
                target_pet_off_pos_list = self._pet_pos_list_show if self._is_in_expand_mode else self._pet_pos_list_hide
                lobby_model.change_model_off_position(target_pet_off_pos_list[index], True)

        if self._cur_click_model:
            target_pet_off_pos_list = self._pet_pos_list_show if self._is_in_expand_mode else self._pet_pos_list_hide
            self._cur_click_model.change_model_off_position(target_pet_off_pos_list[self._cur_select_slot], True)

    def do_show_panel(self):
        super(PVEPetWidgetUI, self).do_show_panel()
        self.process_events(True)
        self._update_pet_item_list()
        self._refresh_btn()
        reset_cam_pos()

    def do_hide_panel(self):
        super(PVEPetWidgetUI, self).do_hide_panel()
        self.process_events(False)

    def play_anim(self):
        self.show()
        self.panel.PlayAnimation('appear')
        self.hide_main_ui()

    def _get_pet_off_pos_list(self):
        btn_add_size_y = self.panel.temp_type_mid.btn_add.GetContentSize()[1]
        nd_model_less = self.panel.nd_model_less
        pos1 = cocos_pos_to_ui_world_pos(nd_model_less.nd_mid_model.ConvertToWorldSpace(0, btn_add_size_y / 2))
        pos2 = cocos_pos_to_ui_world_pos(nd_model_less.nd_left_model.ConvertToWorldSpace(0, 0))
        pos3 = cocos_pos_to_ui_world_pos(nd_model_less.nd_right_model.ConvertToWorldSpace(0, 0))
        self._pet_pos_list_hide = [[pos1.x, pos1.y, pos1.z], [pos2.x, pos2.y, pos2.z], [pos3.x, pos3.y, pos3.z]]
        nd_model_more = self.panel.nd_model_more
        pos1 = cocos_pos_to_ui_world_pos(nd_model_more.nd_mid_model.ConvertToWorldSpace(0, btn_add_size_y / 2))
        pos2 = cocos_pos_to_ui_world_pos(nd_model_more.nd_left_model.ConvertToWorldSpace(0, 0))
        pos3 = cocos_pos_to_ui_world_pos(nd_model_more.nd_right_model.ConvertToWorldSpace(0, 0))
        self._pet_pos_list_show = [[pos1.x, pos1.y, pos1.z], [pos2.x, pos2.y, pos2.z], [pos3.x, pos3.y, pos3.z]]
        if self._cur_select_slot == 1:
            self._set_rotate_counterclockwise_pos_list()
        elif self._cur_select_slot == 2:
            self._set_rotate_clockwise_pos_list()

    def _init_show_pet_item(self):
        choosen_pet = global_data.player and global_data.player.get_pve_choosen_pet()
        if not choosen_pet:
            for index, skin_id in enumerate(self._cur_skin_id_list):
                if skin_id == int(self.skin_list[0]):
                    if index == 1:
                        self._set_rotate_counterclockwise_info()
                        break
                    elif index == 2:
                        self._set_rotate_clockwise_info()
                        break

    def do_switch_scene(self):

        def on_load_scene(*args):
            self._get_pet_off_pos_list()
            self._init_show_pet_item()
            global_data.emgr.change_model_display_scene_item.emit(None)
            self.init_ui()
            return

        scene_background_texture = PVE_BOOK_DEFAULT_BG_PATH
        global_data.emgr.show_lobby_relatived_scene.emit(SCENE_PVE_BOOK_WIDGET_UI, PVE_BOOK_WIDGET_UI, finish_callback=on_load_scene, update_cam_at_once=True, belong_ui_name='PVEPetWidgetUI', scene_content_type=SCENE_PVE_BOOK_WIDGET_UI, scene_background_texture=scene_background_texture)

    def on_create_skin_item(self, lst, index, item):
        valid = index < len(self.skin_list)
        if valid:
            skin_no = self.skin_list[index]
            real_skin_no = skin_no
            if global_data.player:
                real_skin_no = global_data.player.get_pet_sub_skin_choose(real_skin_no)
            item.img_itm.SetDisplayFrameByPath('', item_utils.get_lobby_item_pic_by_item_no(real_skin_no))
            item.lab_name.SetString(item_utils.get_lobby_item_name(real_skin_no))
            item.nd_lock.setVisible(not (global_data.player and global_data.player.has_item_by_no(int(real_skin_no))))
            item_utils.check_skin_tag(item.temp_level, real_skin_no)
            item.bar.SetDisplayFrameByPath('', item_utils.get_pet_rare_degree_pic_by_item_no(real_skin_no))
            item.btn_choose.BindMethod('OnClick', Functor(self._on_click_skin_item, index))
            show_new = global_data.lobby_red_point_data.get_rp_by_no(real_skin_no)
            item.img_new.setVisible(show_new)
            self._update_skin_item_tag(item, real_skin_no)
        else:
            item.bar.setVisible(False)

    def _expand_panel(self):
        if self._is_in_expand_mode:
            self._list_item.SetNumPerUnit(1)
            self.panel.PlayAnimation('reset_more')
            self.panel.PlayAnimation('list_less')
        else:
            self._list_item.SetNumPerUnit(2)
            self.panel.PlayAnimation('reset')
            self.panel.PlayAnimation('list_more')
        self._update_expand_camera()
        self._is_in_expand_mode = not self._is_in_expand_mode
        self._list_item.FitViewSizeToContainerSize()

    def _update_skin_item_tag(self, item, skin_no):
        item.lab_tag.setVisible(False)
        is_pve_choosen_pet = int(skin_no) == (global_data.player and global_data.player.get_pve_choosen_pet())
        pve_backup_pet_list = global_data.player.get_pve_backup_pet_pet_list() if global_data.player else []
        is_pve_backup_pet = int(skin_no) in pve_backup_pet_list
        item.lab_tag_fight.setVisible(is_pve_choosen_pet)
        item.lab_tag_ready.setVisible(is_pve_backup_pet)
        item.nd_tag.setVisible(is_pve_choosen_pet or is_pve_backup_pet)

    def _on_click_skin_item(self, index, *args):
        if not self.panel:
            return
        if not self._show_cur_click_model_complete:
            return
        if self._cur_skin_id_list[self._cur_select_slot] == int(self.skin_list[index]) and self._has_init_model:
            return
        if self._is_in_expand_mode:
            self._expand_panel()
        self._update_skin_item_select(index)
        self._update_widget()
        self._show_model()

    def _update_skin_item_select(self, index):
        self._unselect_skin_item()
        self.cur_skin_idx = index
        skin_no = self.skin_list[index]
        self._cur_skin_id_list[self._cur_select_slot] = int(skin_no)
        self._cur_show_level = get_pet_level(self._cur_skin_id_list[self._cur_select_slot])
        item = self._list_item.GetItem(index)
        self.panel.bar_level.lab_name.SetString(item_utils.get_lobby_item_name(skin_no))
        item_utils.check_skin_tag(self.panel.temp_kind, skin_no)
        show_new = global_data.lobby_red_point_data.get_rp_by_no(skin_no)
        if show_new:
            global_data.player and global_data.player.req_del_item_redpoint(skin_no)
            item.img_new.setVisible(False)
        item.setLocalZOrder(2)
        item.btn_choose.SetSelect(True)

    def _unselect_skin_item(self):
        prev_index = self.cur_skin_idx
        prev_item = self._list_item.GetItem(prev_index)
        if prev_item:
            prev_item.setLocalZOrder(0)
            prev_item.btn_choose.SetSelect(False)

    def _update_widget(self):
        skin_no = self._cur_skin_id_list[self._cur_select_slot]
        real_skin_no = skin_no
        if global_data.player:
            real_skin_no = global_data.player.get_pet_sub_skin_choose(skin_no)
        if skin_no:
            self._level_widget.update_skin_id(str(real_skin_no))
            self._skill_widget.update_skin_id(real_skin_no)
            self._refresh_btn()
            self.panel.nd_right.setVisible(True)
        else:
            self.panel.nd_right.setVisible(False)
        self._update_pet_type_widget()

    def _on_pet_info_updated(self, *args):
        cur_level = get_pet_level(self._cur_skin_id_list[self._cur_select_slot])
        if cur_level != self._cur_show_level:
            self._show_model()
            self._update_pet_type_widget()
            self._cur_show_level = cur_level

    def _on_pve_pet_choosen_changed(self, *args):
        global_data.emgr.close_model_display_scene.emit()
        self._pet_dict = global_data.player.get_pve_pet_dict() if global_data.player else {0: 0,1: 0,2: 0}
        self._cur_skin_id_list = [self._pet_dict.get(0), self._pet_dict.get(1), self._pet_dict.get(2)]
        for i, pet_id in enumerate(self.skin_list):
            self._update_skin_item_tag(self._list_item.GetItem(i), pet_id)

        self._update_widget()
        self._get_skin_list()
        skin_no = self._cur_skin_id_list[self._cur_select_slot]
        if skin_no != 0:
            self.panel.PlayAnimation('tips')
            skin_no = self._pet_conf.get(str(skin_no), {}).get('base_skin', skin_no)
            index = self.skin_list.index(str(skin_no))
            self._update_skin_item_select(index)
            self._skin_list_widget.update_skin_data(self.skin_list, False, index)
        else:
            self._skin_list_widget.update_skin_data(self.skin_list, False, 0, False)
        self._has_init_model = False
        self._show_model()

    def _update_pet_item_list(self, *args):
        if not self._list_item:
            return
        for i, pet_id in enumerate(self.skin_list):
            item = self._list_item.GetItem(i)
            item.nd_lock.setVisible(not (global_data.player and global_data.player.has_item_by_no(int(pet_id))))

    def _refresh_btn(self):
        skin_id = self._cur_skin_id_list[self._cur_select_slot]
        if skin_id is None:
            self.panel.btn_fight.setVisible(False)
            self.panel.btn_ready.setVisible(False)
            self.panel.btn_cancel.setVisible(False)
            self.panel.btn_go.setVisible(False)
            return
        else:
            skin_id = int(skin_id)
            real_pet_id = skin_id
            if global_data.player:
                real_pet_id = global_data.player.get_pet_sub_skin_choose(skin_id)
            item_can_use, _ = item_can_use_by_item_no(skin_id)
            pet_item = global_data.player and global_data.player.get_item_by_no(skin_id)
            skin_owned = pet_item is not None
            fight_pet_id = self._pet_dict.get(0)
            is_fighting = str(real_pet_id) == str(fight_pet_id)
            is_selecting_fight_slot = self._cur_select_slot == 0
            is_show_fight = not is_fighting and item_can_use and is_selecting_fight_slot
            self.panel.btn_fight.setVisible(is_show_fight)
            ready_pet_id_list = [
             self._pet_dict.get(1), self._pet_dict.get(2)]
            is_readying = False
            if skin_id in ready_pet_id_list:
                ready_index = ready_pet_id_list.index(skin_id) + 1
                is_readying = ready_index == self._cur_select_slot
            is_selecting_ready_slot = not is_selecting_fight_slot
            is_show_ready = not is_readying and item_can_use and is_selecting_ready_slot
            self.panel.btn_ready.setVisible(is_show_ready)
            is_using = (is_fighting or is_readying) and not is_show_fight and not is_show_ready
            self.panel.btn_cancel.setVisible(is_using)
            can_jump = skin_owned or not item_can_use
            jump_txt = item_utils.get_item_access(real_pet_id)
            enable = item_utils.can_jump_to_ui(real_pet_id) and can_jump
            self.panel.btn_go.btn.SetEnable(enable)
            self.panel.btn_go.btn.SetText(get_text_by_id(2222 if enable else 80828))
            self.panel.btn_go.setVisible(can_jump and bool(jump_txt))
            if enable:
                jump_txt = jump_txt if 1 else jump_txt + get_text_by_id(635079)
                self.panel.lab_get_method.SetString(jump_txt or '')
            else:
                self.panel.btn_go.setVisible(False)
            return

    def _show_model(self):

        def on_load_callback(lobby_model):
            index = lobby_model.model_data.get('pet_index')
            if index is None:
                return
            else:
                origin_scale = lobby_model.model_data.get('model_scale', 1)
                if index == self._cur_select_slot:
                    scale = origin_scale
                else:
                    scale = origin_scale * PERSPECTIVE_RATIO
                ref_model = lobby_model.get_model()
                if ref_model:
                    ref_model.scale = math3d.vector(scale, scale, scale)
                if index == self._cur_select_slot and not self._pet_dict.get(self._cur_select_slot):
                    self._cur_click_model = lobby_model
                else:
                    self._lobby_model_list[index] = lobby_model
                return

        def on_click_model_load_callback(lobby_model):
            self._show_cur_click_model_complete = True
            if not lobby_model:
                return
            origin_scale = lobby_model.model_data.get('model_scale', 1)
            ref_model = lobby_model.get_model()
            if ref_model:
                ref_model.scale = math3d.vector(origin_scale, origin_scale, origin_scale)
                self._cur_click_model = lobby_model

        if not self._has_init_model:
            self._has_init_model = True
            for index, skin_no in enumerate(self._cur_skin_id_list):
                if skin_no:
                    model_data = self._get_model_data(skin_no, index)
                    global_data.emgr.add_model_display_scene_item.emit(model_data, 'box_pve_01', False, load_callback=on_load_callback)

        else:
            self._show_cur_click_model_complete = False
            for index, lobby_model in enumerate(self._lobby_model_list):
                if index == self._cur_select_slot:
                    if lobby_model:
                        lobby_model.hide_model()

        if self._cur_click_model:
            self._cur_click_model.destroy()
        index = self._cur_select_slot
        if self._cur_skin_id_list[index]:
            model_data = self._get_model_data(self._cur_skin_id_list[index], index)
            global_data.emgr.add_model_display_scene_item.emit(model_data, 'box_pve_01', False, load_callback=on_click_model_load_callback)

    def _get_model_data(self, skin_no, index):
        real_skin_no = skin_no
        if global_data.player:
            real_skin_no = global_data.player.get_pet_sub_skin_choose(skin_no)
        skin_conf = self._pet_conf.get(str(real_skin_no), {})
        model_data = lobby_model_display_utils.get_lobby_model_data(real_skin_no, pet_level=get_pet_level(real_skin_no))
        model_data[0]['can_rotate_on_show'] = True
        pet_off_pos_list = self._pet_pos_list_show if self._is_in_expand_mode else self._pet_pos_list_hide
        model_data[0]['off_position'] = pet_off_pos_list[index]
        model_data[0]['end_anim'] = skin_conf['idle_anim'][0]
        model_data[0]['force_end_ani_loop'] = True
        model_data[0]['pet_index'] = index
        return model_data[0]

    def _rotate_pet_counterclockwise(self):
        if self._is_playing_select_anim:
            return
        if not self._pet_pos_list_hide or not self._pet_pos_list_show:
            return
        self._cur_skin_id_list = [self._pet_dict.get(0), self._pet_dict.get(1), self._pet_dict.get(2)]
        self._update_pet_type_widget()
        self._rotate_counterclockwise()
        self._on_select_next_or_previous_pet()

    def _rotate_counterclockwise(self):
        if self._is_in_expand_mode:
            anim_name = 'tips_left_more'
        else:
            anim_name = 'tips_left'
        self.panel.PlayAnimation(anim_name)
        show_anim_time = float(self.panel.GetAnimationMaxRunTime(anim_name))
        self.panel.DelayCall(show_anim_time, lambda : self._set_btn_describe_visible(self.panel.temp_type_left))
        self._set_rotate_counterclockwise_info()

    def _set_rotate_counterclockwise_info(self):
        self._set_rotate_counterclockwise_pos_list()
        last = self._pet_type_list[-1]
        for i in range(len(self._pet_type_list) - 1, 0, -1):
            self._pet_type_list[i] = self._pet_type_list[i - 1]

        self._pet_type_list[0] = last
        self._cur_select_slot += 1
        self._cur_select_slot %= MAX_MODEL_COUNT

    def _set_rotate_counterclockwise_pos_list(self):
        last = self._pet_pos_list_hide[-1]
        for i in range(len(self._pet_pos_list_hide) - 1, 0, -1):
            self._pet_pos_list_hide[i] = self._pet_pos_list_hide[i - 1]

        self._pet_pos_list_hide[0] = last
        last = self._pet_pos_list_show[-1]
        for i in range(len(self._pet_pos_list_show) - 1, 0, -1):
            self._pet_pos_list_show[i] = self._pet_pos_list_show[i - 1]

        self._pet_pos_list_show[0] = last

    def _rotate_pet_clockwise(self):
        if self._is_playing_select_anim:
            return
        if not self._pet_pos_list_hide or not self._pet_pos_list_show:
            return
        self._cur_skin_id_list = [self._pet_dict.get(0), self._pet_dict.get(1), self._pet_dict.get(2)]
        self._update_pet_type_widget()
        self._rotate_clockwise()
        self._on_select_next_or_previous_pet()

    def _rotate_clockwise(self):
        if self._is_in_expand_mode:
            anim_name = 'tips_right_more'
        else:
            anim_name = 'tips_right'
        self.panel.PlayAnimation(anim_name)
        show_anim_time = float(self.panel.GetAnimationMaxRunTime(anim_name))
        self.panel.DelayCall(show_anim_time, lambda : self._set_btn_describe_visible(self.panel.temp_type_right))
        self._set_rotate_clockwise_info()

    def _set_rotate_clockwise_info(self):
        self._set_rotate_clockwise_pos_list()
        first = self._pet_type_list[0]
        for i in range(len(self._pet_type_list) - 1):
            self._pet_type_list[i] = self._pet_type_list[i + 1]

        self._pet_type_list[-1] = first
        self._cur_select_slot -= 1
        self._cur_select_slot %= MAX_MODEL_COUNT

    def _set_rotate_clockwise_pos_list(self):
        first = self._pet_pos_list_hide[0]
        for i in range(len(self._pet_pos_list_hide) - 1):
            self._pet_pos_list_hide[i] = self._pet_pos_list_hide[i + 1]

        self._pet_pos_list_hide[-1] = first
        first = self._pet_pos_list_show[0]
        for i in range(len(self._pet_pos_list_show) - 1):
            self._pet_pos_list_show[i] = self._pet_pos_list_show[i + 1]

        self._pet_pos_list_show[-1] = first

    def _set_btn_describe_visible(self, pet_type):
        for _, _pet_type in enumerate(self._pet_type_list):
            if _pet_type == pet_type:
                _pet_type.bar_type_fight.lab_type.nd_auto_fit.btn_describe.setVisible(True)
                _pet_type.bar_type_ready.lab_type.nd_auto_fit.btn_describe.setVisible(True)
            else:
                _pet_type.bar_type_fight.lab_type.nd_auto_fit.btn_describe.setVisible(False)
                _pet_type.bar_type_ready.lab_type.nd_auto_fit.btn_describe.setVisible(False)

    def _update_pet_type_widget(self):
        if self._is_playing_select_anim:
            return
        for index, pet_type in enumerate(self._pet_type_list):
            skin_id = self._cur_skin_id_list[index]
            bar_type_fight = pet_type.bar_type_fight
            bar_type_ready = pet_type.bar_type_ready
            if index == 0:
                bar_type_fight.setVisible(True)
                bar_type_ready.setVisible(False)
                lab_type = bar_type_fight.lab_type
                if skin_id == self._pet_dict.get(index) and skin_id != 0:
                    text_id = 860342 if 1 else 860330
                    lab_type.setString(get_text_by_id(text_id))
                else:
                    bar_type_fight.setVisible(False)
                    bar_type_ready.setVisible(True)
                    lab_type = bar_type_ready.lab_type
                    text_id = 860343 if skin_id == self._pet_dict.get(index) and skin_id != 0 else 860331
                    lab_type.setString(get_text_by_id(text_id))
                if skin_id:
                    if global_data.player:
                        skin_id = global_data.player.get_pet_sub_skin_choose(skin_id)
                    pet_type.btn_add.setVisible(False)
                    pet_conf = self._pet_conf.get(str(skin_id))
                    skill_id = str(pet_conf.get('skill_id'))
                    skill_conf = self._pet_skill_conf.get(skill_id)
                    skill_conf or log_error('skill_id\xe9\x94\x99\xe8\xaf\xaf\xef\xbc\x8c\xe8\xaf\xb7\xe6\xa3\x80\xe6\x9f\xa5525\xe5\x8f\xb7\xe8\xa1\xa8\xef\xbc\x9a\xe5\xae\xa0\xe7\x89\xa9id\xef\xbc\x9a{}\xef\xbc\x8c\xe6\x8a\x80\xe8\x83\xbdid\xef\xbc\x9a{}'.format(skin_id, skill_id))
                    pet_type.bar_buff.setVisible(False)
                else:
                    skill_level = get_pet_skill_level(skin_id)
                    attr_str = get_attr_desc_text(skill_conf['short_desc_id'], skill_conf['short_desc_params'], skill_level)
                    bar_buff = pet_type.bar_buff
                    bar_buff.setVisible(True)
                    bar_buff.lab_info_buff.SetString(attr_str)
                    skin_conf = self._pet_conf.get(str(skin_id), {})
                    ss_add_text = skin_conf.get('add_attr_short_text')
                    pet_type.bar_buff_1.setVisible(bool(ss_add_text))
                    if ss_add_text:
                        ss_add_attr = skin_conf.get('add_attr')
                        pet_type.lab_info_buff_1.SetString(get_text_by_id(ss_add_text, ss_add_attr))
            else:
                pet_type.bar_buff.setVisible(False)
                pet_type.bar_buff_1.setVisible(False)
                pet_type.btn_add.setVisible(True)
            if pet_type == self.panel.temp_type_mid:
                bar_type_fight.lab_type.nd_auto_fit.btn_describe.setVisible(True)
                bar_type_ready.lab_type.nd_auto_fit.btn_describe.setVisible(True)
            else:
                bar_type_fight.lab_type.nd_auto_fit.btn_describe.setVisible(False)
                bar_type_ready.lab_type.nd_auto_fit.btn_describe.setVisible(False)

    def close(self, *args):
        self.play_disappear_anim()

    def _on_click_rule(self, *args):
        dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
        dlg.set_show_rule(860344, 860345)

    def play_disappear_anim(self):
        if self._disappearing:
            return
        self._disappearing = True
        anim_time = self.panel.GetAnimationMaxRunTime('disappear')

        def delay_call(*args):
            self._disappearing = False
            global_data.ui_mgr.close_ui(self.get_name())
            if global_data.player:
                global_data.emgr.on_pve_mecha_changed.emit(global_data.player.get_pve_select_mecha_id())

        self.panel.StopAnimation('disappear')
        self.panel.DelayCallWithTag(anim_time, delay_call, self.DELAY_CLOSE_TAG)
        self.panel.PlayAnimation('disappear')

    @staticmethod
    def check_red_point():
        return False

    def on_finalize_panel(self):
        super(PVEPetWidgetUI, self).on_finalize_panel()
        self.process_events(False)
        self._disappearing = None
        if self._skin_list_widget:
            self._skin_list_widget.destroy()
            self._skin_list_widget = None
        if self._level_widget:
            self._level_widget.destroy()
            self._level_widget = None
        if self._skill_widget:
            self._skill_widget.destroy()
            self._skill_widget = None
        global_data.emgr.close_model_display_scene.emit()
        global_data.emgr.leave_current_scene.emit()
        self.show_main_ui()
        if global_data.ui_mgr.get_ui('PVELevelWidgetUI'):
            from logic.gutils.jump_to_ui_utils import jump_to_pve_level_select
            jump_to_pve_level_select()
        else:
            if not global_data.ui_mgr.get_ui('PVEMainUI'):
                from logic.comsys.battle.pve.PVEMainUI import PVEMainUI
                PVEMainUI()
            reset_model_and_cam_pos(False)
        return