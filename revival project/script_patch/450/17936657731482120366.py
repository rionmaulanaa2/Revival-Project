# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/role_profile/RoleSkinDefineUI.py
from __future__ import absolute_import
import six
import six_ex
from six.moves import range
from copy import deepcopy
import math3d
import world
import logic.gcommon.const as gconst
from common.cfg import confmgr
from common.const.uiconst import NORMAL_LAYER_ZORDER_2, UI_VKB_CUSTOM
from common.const.uiconst import UI_TYPE_MESSAGE
from common.uisys.basepanel import BasePanel
from logic.client.const.lobby_model_display_const import CAM_MODE_NEAR, CAM_MODE_FAR, CAM_MODE_NEAR_HEAD, CAM_MODE_NEAR_LEG, DEFAULT_LEFT
from logic.comsys.common_ui.CommonBuyListUI import CommonBuyListUI
from logic.comsys.mall_ui.BuyConfirmUIInterface import role_or_skin_buy_confirmUI
from logic.comsys.mall_ui.PriceUIWidget import PriceUIWidget
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.item.item_const import FASHION_POS_SUIT, FASHION_POS_HEADWEAR, FASHION_POS_BACK, FASHION_POS_SUIT_2, FASHION_POS_FACE, FASHION_POS_WAIST, FASHION_POS_LEG, FASHION_DRESS_PARTS, FASHION_OTHER_PENDANT_LIST, FASHION_DECORATION_TYPE_LIST, FASHION_MAIN_PENDANT_LIST, FPOS_2_TAG_STR, FASHION_POS_HAIR, FASHION_POS_ARM, FASHION_POS_WEAPON_SFX
from logic.gutils import dress_utils, lobby_model_display_utils, template_utils, item_utils
from logic.gcommon.item import lobby_item_type
from logic.gutils import red_point_utils
from .SkinDefineWidget import SkinDefineWidget
ROLE_VIEW_PIC = 1
ROLE_VIEW_MODEL = 2
EXCEPT_HIDE_UI_LIST = []
ROTATE_FACTOR = 850
TAG_SUB_SKINS = 'sub_skins'
TAG_HEAD_DEC = 'head_dec'
TAG_FACE_DEC = 'face_dec'
TAG_HAIR_DEC = 'hair_dec'
TAG_ARM_DEC = 'arm_dec'
TAG_BACK_DEC = 'back_dec'
TAG_WAIST_DEC = 'waist_dec'
TAG_LEG_DEC = 'leg_dec'
TAG_SUIT_DEC = 'suit'
TAG_IMPROVE_DEC = 'improve'
from .SkinDefineDecorationWidget import SkinDefineDecorationWidget
from .SkinDefineImproveWidget import SkinDefineImproveWidget
from logic.gutils import mall_utils
from logic.client.const import mall_const
HEAD_TAG_LIST = (
 (
  FASHION_POS_HEADWEAR, 860097, FASHION_POS_HEADWEAR),)
BACK_TAG_LIST = (
 (
  FASHION_POS_BACK, 860099, FASHION_POS_BACK),)
ALL_TAG = {TAG_SUB_SKINS: (
                 860089, 'role_profile/i_role_skin_define_color', SkinDefineWidget),
   TAG_HEAD_DEC: (
                81229, 'role_profile/i_role_skin_define_dec',
                lambda parent, panel: SkinDefineDecorationWidget(parent, panel, HEAD_TAG_LIST)),
   TAG_FACE_DEC: (
                860098, 'role_profile/i_role_skin_define_dec',
                lambda parent, panel: SkinDefineDecorationWidget(parent, panel, ((FASHION_POS_FACE, 860098, FASHION_POS_FACE),))),
   TAG_HAIR_DEC: (
                81704, 'role_profile/i_role_skin_define_dec',
                lambda parent, panel: SkinDefineDecorationWidget(parent, panel, [(FASHION_POS_HAIR, '', FASHION_POS_HAIR)])),
   TAG_ARM_DEC: (
               81926, 'role_profile/i_role_skin_define_dec',
               lambda parent, panel: SkinDefineDecorationWidget(parent, panel, [(FASHION_POS_ARM, '', FASHION_POS_ARM)])),
   TAG_BACK_DEC: (
                860099, 'role_profile/i_role_skin_define_dec',
                lambda parent, panel: SkinDefineDecorationWidget(parent, panel, BACK_TAG_LIST)),
   TAG_WAIST_DEC: (
                 860100, 'role_profile/i_role_skin_define_dec',
                 lambda parent, panel: SkinDefineDecorationWidget(parent, panel, ((FASHION_POS_WAIST, 860100, FASHION_POS_WAIST),))),
   TAG_LEG_DEC: (
               860101, 'role_profile/i_role_skin_define_dec',
               lambda parent, panel: SkinDefineDecorationWidget(parent, panel, ((FASHION_POS_LEG, 860101, FASHION_POS_LEG),))),
   TAG_SUIT_DEC: (
                81228, 'role_profile/i_role_skin_define_dec',
                lambda parent, panel: SkinDefineDecorationWidget(parent, panel, [(FASHION_POS_SUIT_2, '', FASHION_POS_SUIT_2)])),
   TAG_IMPROVE_DEC: (
                   '', 'role_profile/i_role_promote', lambda parent, panel: SkinDefineImproveWidget(parent, panel))
   }
TAG_SEQ = (
 TAG_SUB_SKINS, TAG_HEAD_DEC, TAG_FACE_DEC, TAG_HAIR_DEC, TAG_ARM_DEC, TAG_BACK_DEC, TAG_WAIST_DEC, TAG_LEG_DEC, TAG_SUIT_DEC, TAG_IMPROVE_DEC)
TAG_HEAD = FASHION_POS_HEADWEAR
TAG_BAG = FASHION_POS_BACK
TAG_SUIT = FASHION_POS_SUIT_2
CONDUCT_EVENT = {FASHION_POS_HEADWEAR: 'change_model_display_head',
   FASHION_POS_BACK: 'change_model_display_bag',
   FASHION_POS_SUIT_2: 'change_model_display_suit'
   }
tag_type_dict = {TAG_HEAD_DEC: [
                FASHION_POS_HEADWEAR],
   TAG_FACE_DEC: [
                FASHION_POS_FACE],
   TAG_HAIR_DEC: [
                FASHION_POS_HAIR],
   TAG_ARM_DEC: [
               FASHION_POS_ARM],
   TAG_BACK_DEC: [
                FASHION_POS_BACK],
   TAG_WAIST_DEC: [
                 FASHION_POS_WAIST],
   TAG_LEG_DEC: [
               FASHION_POS_LEG],
   TAG_SUIT_DEC: [
                FASHION_POS_SUIT_2],
   TAG_IMPROVE_DEC: [
                   FASHION_POS_WEAPON_SFX]
   }
tag_cam_dict = {TAG_SUB_SKINS: CAM_MODE_FAR,
   TAG_HEAD_DEC: CAM_MODE_NEAR_HEAD,
   TAG_FACE_DEC: CAM_MODE_NEAR_HEAD,
   TAG_HAIR_DEC: CAM_MODE_NEAR_HEAD,
   TAG_ARM_DEC: CAM_MODE_NEAR,
   TAG_BACK_DEC: CAM_MODE_FAR,
   TAG_WAIST_DEC: CAM_MODE_NEAR,
   TAG_LEG_DEC: CAM_MODE_NEAR_LEG,
   TAG_SUIT_DEC: CAM_MODE_FAR,
   TAG_IMPROVE_DEC: CAM_MODE_FAR
   }
DEC_WIDGET_TAG_LIST = [
 TAG_HEAD_DEC, TAG_FACE_DEC, TAG_HAIR_DEC, TAG_BACK_DEC, TAG_WAIST_DEC, TAG_LEG_DEC, TAG_SUIT_DEC]
from logic.comsys.role_profile.PlanSkinDefineWidget import SkinPlanWidget

class RoleSkinDefineUI(BasePanel):
    PANEL_CONFIG_NAME = 'role_profile/role_skin_define'
    UI_VKB_TYPE = UI_VKB_CUSTOM
    DLG_ZORDER = NORMAL_LAYER_ZORDER_2
    BOX_OFFSET = [-5.04, 0, 0]
    UI_ACTION_EVENT = {'temp_btn_back.btn_back.OnClick': 'on_click_close_btn',
       'btn_manage.btn_common.OnClick': 'on_click_manager_btn',
       'btn_equiped_close.OnClick': 'on_click_close_manager_btn',
       'nd_mech_touch.OnDrag': '_on_rotate_drag',
       'temp_btn_use.btn_common.OnClick': 'on_click_btn_use',
       'temp_btn_buy.btn_common.OnClick': 'on_click_btn_buy',
       'btn_details.OnClick': 'on_click_details_btn',
       'btn_last.OnClick': 'on_click_btn_last',
       'btn_next.OnClick': 'on_click_btn_next',
       'btn_glass.OnClick': 'on_click_btn_glass'
       }
    GLOBAL_EVENT = {'update_role_id': 'update_war_role',
       'player_item_update_event': 'on_buy_good_success',
       'refresh_item_red_point': 'refresh_role_skin_rp',
       'role_fashion_chagne': 'on_role_fashion_change',
       'response_fashion_scheme_event': 'response_fashion_scheme_fetched',
       'response_role_top_skin_scheme_event': 'on_role_top_skin_scheme_responed',
       'role_top_skin_scheme_change_event': 'on_role_top_skin_scheme_changed_event'
       }

    def on_init_panel--- This code section failed: ---

 160       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  'hide_main_ui'
           6  LOAD_CONST            1  'exceptions'
           9  LOAD_GLOBAL           1  'EXCEPT_HIDE_UI_LIST'
          12  LOAD_CONST            2  'exception_types'
          15  LOAD_GLOBAL           2  'UI_TYPE_MESSAGE'
          18  BUILD_TUPLE_1         1 
          21  CALL_FUNCTION_512   512 
          24  POP_TOP          

 161      25  LOAD_GLOBAL           3  'PriceUIWidget'
          28  LOAD_GLOBAL           3  'PriceUIWidget'
          31  LOAD_FAST             0  'self'
          34  LOAD_ATTR             4  'panel'
          37  LOAD_ATTR             5  'list_price'
          40  CALL_FUNCTION_257   257 
          43  LOAD_FAST             0  'self'
          46  STORE_ATTR            6  'price_top_widget'

 164      49  LOAD_CONST            4  '%d_%d'
          52  LOAD_GLOBAL           7  'gconst'
          55  LOAD_ATTR             8  'SHOP_PAYMENT_ITEM'
          58  LOAD_GLOBAL           7  'gconst'
          61  LOAD_ATTR             9  'SHOP_ITEM_DEC_COIN'
          64  BUILD_TUPLE_2         2 
          67  BINARY_MODULO    

 166      68  LOAD_GLOBAL           7  'gconst'
          71  LOAD_ATTR            10  'SHOP_PAYMENT_YUANBAO'
          74  BUILD_LIST_2          2 
          77  LOAD_FAST             0  'self'
          80  STORE_ATTR           11  'money_type_list'

 168      83  LOAD_FAST             0  'self'
          86  LOAD_ATTR             6  'price_top_widget'
          89  LOAD_ATTR            12  'show_money_types'
          92  LOAD_FAST             0  'self'
          95  LOAD_ATTR            11  'money_type_list'
          98  CALL_FUNCTION_1       1 
         101  POP_TOP          

 171     102  LOAD_GLOBAL          13  'confmgr'
         105  LOAD_ATTR            14  'get'
         108  LOAD_CONST            5  'role_info'
         111  LOAD_CONST            6  'RoleSkin'
         114  LOAD_CONST            7  'Content'
         117  CALL_FUNCTION_3       3 
         120  LOAD_FAST             0  'self'
         123  STORE_ATTR           15  'role_skin_config'

 172     126  LOAD_GLOBAL          13  'confmgr'
         129  LOAD_ATTR            14  'get'
         132  LOAD_CONST            8  'top_role_skin_conf'
         135  LOAD_CONST            9  'default'
         138  BUILD_MAP_0           0 
         141  CALL_FUNCTION_257   257 
         144  LOAD_FAST             0  'self'
         147  STORE_ATTR           16  'top_skin_config'

 173     150  LOAD_CONST            0  ''
         153  LOAD_FAST             0  'self'
         156  STORE_ATTR           18  'role_id'

 174     159  LOAD_CONST            0  ''
         162  LOAD_FAST             0  'self'
         165  STORE_ATTR           19  'top_skin_id'

 175     168  BUILD_MAP_0           0 
         171  LOAD_FAST             0  'self'
         174  STORE_ATTR           20  'preview_decoration'

 176     177  BUILD_MAP_0           0 
         180  LOAD_FAST             0  'self'
         183  STORE_ATTR           21  'default_decoration'

 177     186  LOAD_CONST           10  ''
         189  LOAD_FAST             0  'self'
         192  STORE_ATTR           22  'preview_skin'

 178     195  LOAD_GLOBAL          23  'False'
         198  LOAD_FAST             0  'self'
         201  STORE_ATTR           24  '_block_preview_model_display_refresh'

 179     204  LOAD_CONST            0  ''
         207  LOAD_FAST             0  'self'
         210  STORE_ATTR           25  '_showed_preview_skin_id'

 180     213  BUILD_MAP_0           0 
         216  LOAD_FAST             0  'self'
         219  STORE_ATTR           26  '_showed_preview_decoration'

 181     222  LOAD_GLOBAL          27  'CAM_MODE_FAR'
         225  LOAD_FAST             0  'self'
         228  STORE_ATTR           28  'cur_cam_mode'

 182     231  LOAD_GLOBAL          23  'False'
         234  LOAD_FAST             0  'self'
         237  STORE_ATTR           29  'btn_glass_clicked'

 183     240  LOAD_CONST            0  ''
         243  LOAD_FAST             0  'self'
         246  STORE_ATTR           30  'model'

 184     249  LOAD_CONST            0  ''
         252  LOAD_FAST             0  'self'
         255  STORE_ATTR           31  'cam_data'

 187     258  LOAD_CONST           11  ''
         261  LOAD_FAST             0  'self'
         264  STORE_ATTR           32  '_cur_tag'

 188     267  BUILD_MAP_0           0 
         270  LOAD_FAST             0  'self'
         273  STORE_ATTR           33  'widget_dict'

 189     276  BUILD_MAP_0           0 
         279  LOAD_FAST             0  'self'
         282  STORE_ATTR           34  'tag_btn_dict'

 191     285  LOAD_GLOBAL          23  'False'
         288  LOAD_FAST             0  'self'
         291  STORE_ATTR           35  '_is_in_request_fashion_scheme'

 193     294  LOAD_GLOBAL          23  'False'
         297  LOAD_FAST             0  'self'
         300  STORE_ATTR           36  '_is_in_role_request_fashion_scheme'

 194     303  LOAD_CONST            0  ''
         306  LOAD_FAST             0  'self'
         309  STORE_ATTR           37  '_need_jump_to_skin'

 195     312  LOAD_CONST            0  ''
         315  LOAD_FAST             0  'self'
         318  STORE_ATTR           38  '_need_jump_to_item_no'

 196     321  LOAD_CONST            0  ''
         324  LOAD_FAST             0  'self'
         327  STORE_ATTR           39  '_need_jump_to_improve_s_plus'

 197     330  BUILD_LIST_0          0 
         333  LOAD_FAST             0  'self'
         336  STORE_ATTR           40  '_changed_target_fashion_parts'

 200     339  LOAD_GLOBAL          41  'SkinPlanWidget'
         342  LOAD_FAST             0  'self'
         345  LOAD_ATTR             4  'panel'
         348  LOAD_ATTR            42  'temp_list_plan'
         351  LOAD_FAST             0  'self'
         354  CALL_FUNCTION_2       2 
         357  LOAD_FAST             0  'self'
         360  STORE_ATTR           43  'skin_plan_widget'

 201     363  LOAD_FAST             0  'self'
         366  LOAD_ATTR            43  'skin_plan_widget'
         369  LOAD_ATTR            44  'set_callback'
         372  LOAD_FAST             0  'self'
         375  LOAD_ATTR            45  'save_preview_data_to_plan_list'
         378  LOAD_FAST             0  'self'
         381  LOAD_ATTR            46  'set_all_preview_items'
         384  CALL_FUNCTION_2       2 
         387  POP_TOP          

 202     388  LOAD_GLOBAL          23  'False'
         391  LOAD_FAST             0  'self'
         394  STORE_ATTR           47  '_skin_plan_widget_inited'

 204     397  LOAD_FAST             0  'self'
         400  LOAD_ATTR             4  'panel'
         403  LOAD_ATTR            48  'PlayAnimation'
         406  LOAD_CONST           12  'appear'
         409  CALL_FUNCTION_1       1 
         412  POP_TOP          

 205     413  LOAD_FAST             0  'self'
         416  LOAD_ATTR             4  'panel'
         419  LOAD_ATTR            49  'btn_clear'
         422  LOAD_ATTR            50  'BindMethod'
         425  LOAD_CONST           13  'OnClick'
         428  LOAD_FAST             0  'self'
         431  LOAD_ATTR            51  'on_click_btn_clear'
         434  CALL_FUNCTION_2       2 
         437  POP_TOP          

 206     438  LOAD_FAST             0  'self'
         441  LOAD_ATTR             4  'panel'
         444  LOAD_ATTR            52  'btn_full_screen'
         447  LOAD_ATTR            50  'BindMethod'
         450  LOAD_CONST           13  'OnClick'
         453  LOAD_FAST             0  'self'
         456  LOAD_ATTR            53  'on_click_btn_full_screen'
         459  CALL_FUNCTION_2       2 
         462  POP_TOP          

 207     463  LOAD_FAST             0  'self'
         466  LOAD_ATTR             4  'panel'
         469  LOAD_ATTR            54  'btn_manage'
         472  LOAD_ATTR            55  'setVisible'
         475  LOAD_GLOBAL          23  'False'
         478  CALL_FUNCTION_1       1 
         481  POP_TOP          

 209     482  LOAD_GLOBAL          56  'dress_utils'
         485  LOAD_ATTR            57  'get_invisible_decoration_id_list'
         488  CALL_FUNCTION_0       0 
         491  LOAD_FAST             0  'self'
         494  STORE_ATTR           58  '_invisible_decoration_id_list'

 210     497  BUILD_LIST_0          0 
         500  LOAD_FAST             0  'self'
         503  STORE_ATTR           59  '_waiting_for_batch_buy_item_list'

 211     506  LOAD_CONST            0  ''
         509  LOAD_FAST             0  'self'
         512  STORE_ATTR           60  '_batch_buy_dec_preview_skin'

 214     515  LOAD_CONST            0  ''
         518  LOAD_FAST             0  'self'
         521  STORE_ATTR           61  'adapt_dec_no'

 215     524  BUILD_LIST_0          0 
         527  LOAD_FAST             0  'self'
         530  STORE_ATTR           62  'adapt_skin_id_list'

 216     533  BUILD_LIST_0          0 
         536  LOAD_FAST             0  'self'
         539  STORE_ATTR           63  'adapt_dec_no_list'

 217     542  LOAD_FAST             0  'self'
         545  LOAD_ATTR             4  'panel'
         548  LOAD_ATTR            64  'btn_sort'
         551  LOAD_ATTR            55  'setVisible'
         554  LOAD_GLOBAL          23  'False'
         557  CALL_FUNCTION_1       1 
         560  POP_TOP          
         561  LOAD_CONST            0  ''
         564  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_257' instruction at offset 40

    def on_finalize_panel(self):
        self._waiting_for_batch_buy_item_list = []
        self._batch_buy_dec_preview_skin = None
        global_data.emgr.set_reward_show_blocking_item_no_event.emit(self._waiting_for_batch_buy_item_list)
        for widget in six.itervalues(self.widget_dict):
            widget.destroy()

        self.tag_btn_dict = None
        self.price_top_widget and self.price_top_widget.on_finalize_panel()
        self.price_top_widget = None
        self.destroy_widget('skin_plan_widget')
        global_data.emgr.close_model_display_scene.emit()
        global_data.emgr.leave_current_scene.emit()
        global_data.emgr.reset_rotate_model_display.emit()
        global_data.ui_mgr.close_ui('GameRuleDescUI')
        global_data.ui_mgr.close_ui('CommonBuyListUI')
        self.show_main_ui()
        return

    def set_role_top_skin(self, role_id, skin_id, preview_skin=None):
        self.role_id = role_id
        self.top_skin_id = skin_id
        self.init_tag_show()
        import copy
        special_conf = confmgr.get('lobby_model_display_conf', 'SpecialRoleSkinDefineCam', 'Content')
        self.cam_data = copy.deepcopy(special_conf.get(str(self.top_skin_id), {}))
        if not self.cam_data:
            conf = confmgr.get('lobby_model_display_conf', 'RoleSkinDefineCam', 'Content')
            self.cam_data = copy.deepcopy(conf.get(str(self.role_id), {}))
        if global_data.player.check_need_request_role_top_skin_scheme(self.role_id):
            self._is_in_role_request_fashion_scheme = True
            global_data.player.request_role_skin_scheme(self.role_id)
            return
        else:
            self.preview_skin = preview_skin or self.get_chosen_skin()
            self.preview_decoration = dict(self.get_skin_decoration_data(self.preview_skin, is_for_show=True))
            self.chosen_dec_item = dict(self.preview_decoration)
            self.default_decoration = dress_utils.get_skin_default_wear_decoration_dict(self.preview_skin, self.preview_skin)
            self.check_role_status()
            self.init_preview_model()
            for tag, widget in six.iteritems(self.widget_dict):
                if tag in self.valid_tags:
                    widget.set_role_id(role_id, skin_id)

            if not self._cur_tag or self._cur_tag not in self.valid_tags:
                self._cur_tag = self._cur_tag or self.get_first_valid_tag()
                self.select_tag(self._cur_tag, True, lerp_cam=False)
            else:
                self.widget_dict[self._cur_tag].refresh_all_content()
            self.refresh_role_skin_rp()
            if global_data.player:
                skin_plan = global_data.player.get_fashion_scheme(self.top_skin_id)
                if skin_plan is None:
                    global_data.player.request_fashion_scheme(self.top_skin_id)
            return

    def save_preview_data_to_plan_list(self):
        preview_skin = self.get_preview_skin_id()
        ls = []
        ls.append(preview_skin)
        preview_decoration_data = self.get_preview_decoration_data()
        new_dict = dict(preview_decoration_data)
        new_dict.update({FASHION_POS_SUIT: preview_skin})
        return dress_utils.fashion_dict_to_skin_plan(new_dict)

    def response_fashion_scheme_fetched(self, fashion_id):
        if self._is_in_request_fashion_scheme:
            if str(fashion_id) == str(self.top_skin_id):
                self._is_in_request_fashion_scheme = False
                self.on_click_manager_btn()

    def jump_to_skin(self, skin_id):
        self.hide_dec_adapt_guide_list()
        belong_ino = item_utils.get_lobby_item_belong_no(skin_id)
        if global_data.player.check_need_request_role_top_skin_scheme(belong_ino):
            self._need_jump_to_skin = skin_id
            self._is_in_role_request_fashion_scheme = True
            global_data.player.request_role_skin_scheme(belong_ino)
            return
        else:
            self._need_jump_to_skin = None
            self._block_preview_model_display_refresh = True
            self.set_role_top_skin(belong_ino, dress_utils.get_top_skin_id_by_skin_id(skin_id))
            if TAG_SUB_SKINS in self.valid_tags:
                self.select_tag(TAG_SUB_SKINS)
                self.widget_dict[TAG_SUB_SKINS].jump_to_skin(skin_id)
            else:
                self.select_tag(self.valid_tags[0])
                self.widget_dict[self.valid_tags[0]].refresh_all_content()
                skin_list = self.top_skin_config.get(str(self.top_skin_id), [])
                if skin_id in skin_list:
                    self.preview_skin = skin_id
                else:
                    self.preview_skin = skin_list[0]
            self._block_preview_model_display_refresh = False
            if self.is_diff_with_in_preview_data(self.preview_skin, self.preview_decoration):
                self.update_role_view()
            return

    def jump_to_improve_s_plus(self, skin_id):
        self.hide_dec_adapt_guide_list()
        belong_ino = item_utils.get_lobby_item_belong_no(skin_id)
        if global_data.player.check_need_request_role_top_skin_scheme(belong_ino):
            self._need_jump_to_improve_s_plus = skin_id
            self._is_in_role_request_fashion_scheme = True
            global_data.player.request_role_skin_scheme(belong_ino)
            return
        else:
            self._need_jump_to_improve_s_plus = None
            self._block_preview_model_display_refresh = True
            self.set_role_top_skin(belong_ino, dress_utils.get_top_skin_id_by_skin_id(skin_id))
            if TAG_IMPROVE_DEC in self.valid_tags:
                self.select_tag(TAG_IMPROVE_DEC)
                self.widget_dict[TAG_IMPROVE_DEC].refresh_all_content()
            else:
                self.select_tag(self.valid_tags[0])
                self.widget_dict[self.valid_tags[0]].refresh_all_content()
            skin_list = self.top_skin_config.get(str(self.top_skin_id), [])
            if skin_id in skin_list:
                self.preview_skin = skin_id
            else:
                self.preview_skin = skin_list[0]
            self._block_preview_model_display_refresh = False
            self.update_role_view()
            return

    def is_diff_with_in_preview_data(self, preview_skin, preview_dec):
        if self._showed_preview_skin_id != preview_skin:
            return True
        if type(preview_skin) != type(self._showed_preview_decoration):
            return True
        if type(preview_skin) == dict:
            for pos in FASHION_DECORATION_TYPE_LIST:
                new_one = preview_dec.get(pos)
                old_one = self._showed_preview_decoration.get(pos)
                if new_one != old_one:
                    return True

        return False

    def jump_to_item_no(self, item_no, skin_id=None):
        if not skin_id:
            self.hide_dec_adapt_guide_list()
        from logic.gutils import item_utils
        from logic.gcommon.item import lobby_item_type
        belong_ino = item_utils.get_lobby_item_belong_no(item_no)
        if global_data.player.check_need_request_role_top_skin_scheme(belong_ino):
            self._need_jump_to_item_no = item_no
            self._is_in_role_request_fashion_scheme = True
            global_data.player.request_role_skin_scheme(belong_ino)
            return
        else:
            self._need_jump_to_item_no = None
            item_type = item_utils.get_lobby_item_type(item_no)
            if item_type not in [lobby_item_type.L_ITEM_TYPE_HEAD, lobby_item_type.L_ITEM_TYPE_BODY,
             lobby_item_type.L_ITEM_TYPE_SUIT, lobby_item_type.L_ITEM_TYPE_FACE_DEC,
             lobby_item_type.L_ITEM_TYPE_WAIST_DEC, lobby_item_type.L_ITEM_TYPE_LEG_DEC,
             lobby_item_type.L_ITEM_TYPE_HAIR_DEC, lobby_item_type.L_ITEM_TYPE_ARM_DEC]:
                return
            self._block_preview_model_display_refresh = True
            convert_tag_dict = {lobby_item_type.L_ITEM_TYPE_HEAD: TAG_HEAD_DEC,
               lobby_item_type.L_ITEM_TYPE_BODY: TAG_BACK_DEC,
               lobby_item_type.L_ITEM_TYPE_SUIT: TAG_SUIT_DEC,
               lobby_item_type.L_ITEM_TYPE_FACE_DEC: TAG_FACE_DEC,
               lobby_item_type.L_ITEM_TYPE_HAIR_DEC: TAG_HAIR_DEC,
               lobby_item_type.L_ITEM_TYPE_WAIST_DEC: TAG_WAIST_DEC,
               lobby_item_type.L_ITEM_TYPE_LEG_DEC: TAG_LEG_DEC,
               lobby_item_type.L_ITEM_TYPE_ARM_DEC: TAG_ARM_DEC
               }
            target_tag = convert_tag_dict[item_type]
            role_skin_id = self.get_default_choose_skin(belong_ino)
            if not skin_id:
                choose_role_skin_id = dress_utils.get_top_skin_id_by_skin_id(role_skin_id)
                if not dress_utils.check_valid_decoration(choose_role_skin_id, item_no):
                    skin_list = dress_utils.get_decoration_id_skin_list(item_no)
                    if skin_list:
                        choose_role_skin_id = skin_list[0]
            else:
                choose_role_skin_id = skin_id
            if not dress_utils.check_valid_decoration(choose_role_skin_id, item_no):
                usable_skin_list = dress_utils.handle_usable_skin_list(item_no)
                if usable_skin_list:
                    choose_role_skin_id = usable_skin_list[0]
            self.set_role_top_skin(belong_ino, dress_utils.get_top_skin_id_by_skin_id(choose_role_skin_id), choose_role_skin_id)
            self.select_tag(target_tag)
            self.widget_dict[target_tag].jump_to_item_no(item_no=item_no)
            self._block_preview_model_display_refresh = False
            if self.is_diff_with_in_preview_data(self.preview_skin, self.preview_decoration):
                self.update_role_view()
            return

    def set_all_preview_items(self, preview_skin, preview_decoration):
        self._block_preview_model_display_refresh = True
        if preview_skin != self.preview_skin:
            if TAG_SUB_SKINS in self.widget_dict:
                self.widget_dict[TAG_SUB_SKINS].jump_to_skin(preview_skin)
            self.preview_skin = preview_skin
            self.default_decoration = dress_utils.get_skin_default_wear_decoration_dict(self.preview_skin, self.preview_skin)
            self.chosen_dec_item = dict(self.get_skin_decoration_data(self.preview_skin))
        if self.preview_decoration != preview_decoration:
            self.preview_decoration = preview_decoration
            for tag, widget in six.iteritems(self.widget_dict):
                if tag != TAG_SUB_SKINS:
                    widget.refresh_all_content()

        self._block_preview_model_display_refresh = False
        global_data.emgr.change_model_display_scene_item.emit(None)
        self.update_role_view()
        return

    def update_money_type(self):
        skin_item_data = global_data.player.get_item_by_no(self.preview_skin)
        has_skin = skin_item_data is not None
        price_list = []
        if not has_skin:
            goods_id = self.role_skin_config.get(str(self.preview_skin), {}).get('goods_id')
            price = mall_utils.get_mall_item_price(goods_id)
            if price:
                price_list.append(price)
        own_dict, no_own_dict, can_buy_dict, no_can_buy_dict = self.get_decoration_buy_info()
        for item_no in six.itervalues(can_buy_dict):
            goods_id = dress_utils.get_goods_id_of_role_dress_related_item_no(item_no)
            price = mall_utils.get_mall_item_price(goods_id)
            if price:
                price_list.append(price)

        payment_list = []
        for prices in price_list:
            for p in prices:
                goods_payment = p.get('goods_payment')
                if goods_payment is not None:
                    payment_list.append(goods_payment)

        new_money_types_list = []
        new_money_types_list.extend(self.money_type_list)
        for p in payment_list:
            if p not in new_money_types_list:
                new_money_types_list.append(p)

        self.price_top_widget.show_money_types(new_money_types_list)
        return

    def show_improve_skin_tips(self, parent):
        nd = global_data.uisystem.load_template_create('mech_display/i_define_item_tips', parent=self.panel, name='improve_skin_tips')
        pos = parent.getParent().convertToWorldSpace(parent.getPosition())
        pos = self.panel.convertToNodeSpace(pos)
        nd.setPosition(pos)
        nd.nd_splus_hint.setVisible(True)
        nd.PlayAnimation('show_hint')
        nd.PlayAnimation('show_hint_arrow')

    def hide_improve_skin_tips(self, parent):
        nd = getattr(self.panel, 'improve_skin_tips', None)
        if nd:
            nd.nd_splus_hint.setVisible(False)
            nd.StopAnimation('show_hint')
            nd.StopAnimation('show_hint_arrow')
        return

    def init_tag_show(self):
        self.valid_tags = self.get_valid_tags(TAG_SEQ)
        valid_tags = self.valid_tags
        self.panel.list_tab.SetInitCount(len(valid_tags))
        all_item = self.panel.list_tab.GetAllItem()
        for ui_item in all_item:
            ui_item.PlayAnimation('appear')

        self._list_tab = [ self.panel.list_tab.GetItem(i) for i in range(len(valid_tags)) ]
        self.tag_btn_dict = {}
        for index, tag in enumerate(valid_tags):
            tag_name = ALL_TAG[tag][0]
            tag_btn = self._list_tab[index]
            if tag == TAG_IMPROVE_DEC:
                tag_btn.RecordAnimationNodeState('loop')
                tag_btn.icon_splus.setVisible(True)
                common_pic = 'gui/ui_res_2/mech_display/btn_tab_splus.png'
                select_pic = 'gui/ui_res_2/mech_display/btn_tab_splus_2.png'
                tag_btn.btn.SetFrames('', [common_pic, select_pic, select_pic], False, None)
            else:
                tag_btn.icon_splus.setVisible(False)
            self.tag_btn_dict[tag] = tag_btn
            tag_btn.btn.SetText(tag_name)
            tag_btn.btn.BindMethod('OnClick', lambda b, t, tag=tag: self.select_tag(tag))
            if tag == TAG_IMPROVE_DEC:
                if item_utils.check_show_skin_improve_tips(self.top_skin_id):
                    self.show_improve_skin_tips(tag_btn.btn)
                else:
                    self.hide_improve_skin_tips(tag_btn.btn)

        return

    def get_valid_tags(self, tag_seq):
        valid_tag_seq = []
        for tag in tag_seq:
            tag_fashion_pos_list = tag_type_dict.get(tag, [])
            if not tag_fashion_pos_list:
                valid_tag_seq.append(tag)
            elif tag == TAG_IMPROVE_DEC:
                skin_improve_collected_items = confmgr.get('role_info', 'RoleSkin', 'Content', str(self.top_skin_id), 'skin_improve_collected_items', default=[])
                if skin_improve_collected_items:
                    valid_tag_seq.append(tag)
            else:
                f_name_list = [ FPOS_2_TAG_STR.get(f_pos, '') for f_pos in tag_fashion_pos_list ]
                deco_list = dress_utils.get_valid_deco_list_for_skin_id(self.role_id, self.top_skin_id, f_name_list)
                if deco_list:
                    valid_tag_seq.append(tag)

        if TAG_SUB_SKINS in valid_tag_seq:
            sec_skin_list = self.top_skin_config.get(str(self.top_skin_id))
            if not sec_skin_list or len(sec_skin_list) <= 1:
                valid_tag_seq.remove(TAG_SUB_SKINS)
        if not valid_tag_seq:
            valid_tag_seq.append(TAG_SUB_SKINS)
        return valid_tag_seq

    def get_first_valid_tag(self):
        return self.valid_tags[0]

    def select_tag(self, tag, change_role=False, **kwargs):
        if tag not in self.valid_tags:
            log_error('This tag is not a valid tag', tag)
            return
        if self._cur_tag == tag and not change_role:
            return
        if tag not in self.widget_dict:
            _, template_name, widget_cls = ALL_TAG[tag]
            panel = global_data.uisystem.load_template_create(template_name, parent=self.panel.nd_content, name=tag)
            widget = widget_cls(self, panel)
            widget.set_role_id(self.role_id, self.top_skin_id)
            self.widget_dict[tag] = widget
        for _tag, widget in six.iteritems(self.widget_dict):
            widget.show_panel(_tag == tag)

        for _tag, tag_btn in six.iteritems(self.tag_btn_dict):
            tag_btn.btn.SetSelect(_tag == tag)
            if _tag == TAG_IMPROVE_DEC:
                if tag == _tag:
                    tag_btn.PlayAnimation('loop')
                    tag_btn.btn.icon_splus.SetDisplayFrameByPath('', 'gui/ui_res_2/mech_display/icon_splus_2.png')
                else:
                    tag_btn.StopAnimation('loop')
                    tag_btn.RecoverAnimationNodeState('loop')
                    tag_btn.btn.icon_splus.SetDisplayFrameByPath('', 'gui/ui_res_2/mech_display/icon_splus.png')

        if not change_role:
            if self._cur_tag:
                self.widget_dict[self._cur_tag].on_hide()
        self.widget_dict[tag].refresh_all_content()
        if tag == TAG_IMPROVE_DEC:
            self.hide_improve_skin_tips(self.tag_btn_dict[tag].btn)
            item_utils.write_show_skin_improve_tips(self.top_skin_id)
            self.widget_dict[tag].check_play_unlock_anim()
        need_check_role_status = False
        if tag == TAG_IMPROVE_DEC or self._cur_tag == TAG_IMPROVE_DEC:
            need_check_role_status = True
        self._cur_tag = tag
        if need_check_role_status:
            self.check_role_status()
        self.on_click_btn_glass(reset=True, is_slerp=kwargs.get('lerp_cam', True))

    def init_preview_model(self):
        self.update_role_view()

    def on_reset_lobby_model(self):
        self.update_role_view()

    def refresh_relatived_scene(self):
        if self.role_id:
            role_cam_data = lobby_model_display_utils.get_role_display_cam_data(self.role_id, self.preview_skin)
            key = 'far_cam' if self.cur_cam_mode == CAM_MODE_FAR else 'near_cam'
            display_type = str(role_cam_data.get(key, DEFAULT_LEFT))
        else:
            display_type = DEFAULT_LEFT
        from logic.gcommon.common_const import scene_const
        scene_path = confmgr.get('role_info', 'RoleSkin', 'Content', str(self.preview_skin), 'zhanshi_scene_path')
        if scene_path is not None:
            global_data.emgr.show_disposable_lobby_relatived_scene.emit(scene_const.SCENE_SKIN_ZHANSHI, scene_path, display_type, belong_ui_name='RoleSkinDefineUI')
        else:
            global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_JIEMIAN_COMMON, str(display_type), scene_content_type=scene_const.SCENE_ZHANSHI, belong_ui_name='RoleSkinDefineUI')
        return

    def do_show_panel(self):
        super(RoleSkinDefineUI, self).do_show_panel()
        self.on_reset_lobby_model()
        self.preview_skin and self.req_del_item_redpoint(self.preview_skin)
        default_skin = confmgr.get('role_info', 'RoleInfo', 'Content', str(self.role_id), 'default_skin')
        if default_skin and int(default_skin[0]) == int(self.preview_skin):
            self.req_del_item_redpoint(self.role_id)

    def update_war_role(self, role_id):
        self.check_role_status()

    def on_buy_good_success(self):
        self.check_role_status()
        self.panel.SetTimeOut(0.1, lambda : self.check_batch_buy_show())
        if self.panel.btn_sort.isVisible() and self.adapt_dec_no:
            self.refresh_skin_mode_list(self.adapt_dec_no, self.adapt_skin_id_list, self.adapt_dec_no_list)

    def change_preview_skin(self, skin_data=None):
        if self.preview_skin == skin_data:
            return
        self.preview_skin = skin_data
        self.default_decoration = dress_utils.get_skin_default_wear_decoration_dict(self.preview_skin, self.preview_skin)
        self.chosen_dec_item = dict(self.get_skin_decoration_data(self.preview_skin))
        self.preview_decoration = deepcopy(self.chosen_dec_item)
        self.check_role_status()
        if self._showed_preview_skin_id != self.preview_skin:
            self.update_role_view()

    def change_preview_decoration(self, tag, item_no):
        skin_id = self.preview_skin
        if self.preview_decoration.get(tag) == item_no:
            return
        for preview_tag, pre_item_no in six.iteritems(self.preview_decoration):
            if tag == TAG_SUIT:
                if preview_tag not in [TAG_SUIT, FASHION_POS_SUIT] and pre_item_no:
                    self.revert_preview_decoration(preview_tag)
                    for widget_tag in six.iterkeys(self.widget_dict):
                        if widget_tag not in [TAG_SUIT_DEC, TAG_SUB_SKINS, TAG_IMPROVE_DEC]:
                            if hasattr(self.widget_dict[widget_tag], 'force_revert'):
                                self.widget_dict[widget_tag].force_revert()

            elif preview_tag in [TAG_SUIT] and pre_item_no:
                self.revert_preview_decoration(preview_tag)
                for widget_tag in six.iterkeys(self.widget_dict):
                    if widget_tag in [TAG_SUIT_DEC]:
                        self.widget_dict[widget_tag].force_revert()

        self.preview_decoration[tag] = item_no
        if self._showed_preview_skin_id == self.preview_skin:
            if tag in CONDUCT_EVENT:
                global_data.emgr.emit(CONDUCT_EVENT[tag], int(item_no), int(skin_id))
            else:
                self.refresh_other_pendant_info(self.preview_decoration, int(skin_id))
        else:
            self.update_role_view()
        self.check_role_status()

    def revert_preview_decoration(self, tag):
        if not self.preview_decoration.get(tag):
            return
        skin_id = self.preview_skin
        self.preview_decoration[tag] = 0
        if tag in self.default_decoration:
            self.preview_decoration[tag] = self.default_decoration[tag]
        if tag in CONDUCT_EVENT:
            global_data.emgr.emit(CONDUCT_EVENT[tag], self.preview_decoration[tag], int(skin_id))
        else:
            self.refresh_other_pendant_info(self.preview_decoration, skin_id)
        self.check_role_status()

    def refresh_other_pendant_info(self, preview_decoration, skin_id):
        new_pendant_info = {}
        for tag, item_no in six.iteritems(preview_decoration):
            if item_no and tag not in FASHION_MAIN_PENDANT_LIST and tag in FASHION_OTHER_PENDANT_LIST:
                new_pendant_info[tag] = item_no

        pendant_id_list = six_ex.values(new_pendant_info)
        global_data.emgr.emit('change_display_model_other_pendant', pendant_id_list, skin_id)

    def get_skin_decoration_data(self, skin_id, decoration_type=FASHION_DECORATION_TYPE_LIST, is_for_show=False):
        if self._is_in_role_request_fashion_scheme:
            return {}
        decoration_data = dress_utils.get_role_fashion_decoration_dict(self.role_id, skin_id)
        if is_for_show:
            has_set = global_data.player.check_has_set_skin_scheme(self.role_id, skin_id)
            if not has_set:
                default_show_dict = dress_utils.get_skin_default_show_decoration_dict(skin_id)
                return default_show_dict
            else:
                return decoration_data

        else:
            return decoration_data

    def get_chosen_role_skin_data(self, role_id, top_skin_id):
        role_skin_id = dress_utils.get_top_skin_clothing_id(role_id, top_skin_id)
        return (
         role_skin_id, self.get_skin_decoration_data(role_skin_id))

    def check_is_all_preview_is_equipped(self):
        role_skin_id, role_skin_decoration_data = self.get_chosen_role_skin_data(self.role_id, self.top_skin_id)
        decoration_type = FASHION_DECORATION_TYPE_LIST
        if role_skin_id == self.preview_skin:
            for tag in decoration_type:
                preview_one = self.preview_decoration.get(tag)
                equipped_one = role_skin_decoration_data.get(tag)
                if preview_one and preview_one != equipped_one:
                    return False

            return True
        return False

    def req_del_item_redpoint(self, skin_id):
        show_new = global_data.lobby_red_point_data.get_rp_by_no(skin_id)
        if show_new:
            global_data.player.req_del_item_redpoint(skin_id)

    def on_role_fashion_change(self, item_no, fashion_data):
        if item_no != self.role_id:
            return
        if not self.isPanelVisible():
            return
        self.chosen_dec_item = dict(self.get_skin_decoration_data(self.preview_skin))
        self.widget_dict[self._cur_tag].refresh_all_content()
        self.check_role_status()

    def update_role_view(self):
        self.refresh_relatived_scene()
        if not self._block_preview_model_display_refresh:
            model_data = self.get_preview_model_data()
            if self._is_in_role_request_fashion_scheme:
                return
            global_data.emgr.change_model_display_scene_item.emit(model_data)
            self._showed_preview_skin_id = self.preview_skin
            self._showed_preview_decoration = dict(self.preview_decoration)
            self.on_click_btn_glass(reset=True, is_slerp=False)

    def get_preview_model_data(self, other_preview_decoration=None):
        role_id = self.role_id
        skin_id = self.preview_skin
        mpath = dress_utils.get_role_model_path_by_lod(role_id, skin_id, 'h')
        item_no = dress_utils.get_role_item_no(role_id, skin_id)
        preview_decoration = dict(self.preview_decoration)
        if other_preview_decoration:
            preview_decoration.update(other_preview_decoration)
        if mpath is not None:
            head_id = preview_decoration.get(FASHION_POS_HEADWEAR)
            bag_id = preview_decoration.get(FASHION_POS_BACK)
            suit_id = preview_decoration.get(FASHION_POS_SUIT_2)
            other_pendants = [ preview_decoration.get(pos) for pos in FASHION_OTHER_PENDANT_LIST ]
            model_data = lobby_model_display_utils.get_lobby_model_data(item_no, skin_id=self.preview_skin, head_id=head_id, bag_id=bag_id, suit_id=suit_id, other_pendants=other_pendants)
            if model_data:
                for m in model_data:
                    m['off_position'] = self.BOX_OFFSET
                    m['show_anim'] = m['end_anim']

            return model_data
        else:
            return

    def refresh_role_skin_rp(self):
        if TAG_SUB_SKINS in self.tag_btn_dict:
            skin_list = dress_utils.get_role_top_skin_owned_second_skin_list(self.top_skin_id)
            rp_vis = global_data.lobby_red_point_data.get_rp_by_item_no_list(skin_list)
            red_point_utils.show_red_point_template(self.tag_btn_dict[TAG_SUB_SKINS].btn.temp_reddot, rp_vis)
        for tag in tag_type_dict:
            if tag in self.tag_btn_dict:
                tag_dec_types = tag_type_dict[tag]
                tag_dec_strs = [ FPOS_2_TAG_STR.get(t, '') for t in tag_dec_types ]
                valid_dec_item_nos = dress_utils.get_valid_deco_list_for_skin_id(self.role_id, self.top_skin_id, tag_dec_strs)
                rp_vis = global_data.lobby_red_point_data.get_rp_by_item_no_list(valid_dec_item_nos)
                red_point_utils.show_red_point_template(self.tag_btn_dict[tag].btn.temp_reddot, rp_vis)

    def get_preview_skin_id(self):
        return self.preview_skin

    def get_preview_skin_decoration(self):
        return self.preview_decoration

    def get_chosen_skin(self):
        chosen_item = dress_utils.get_top_skin_clothing_id(self.role_id, self.top_skin_id)
        if chosen_item is None:
            chosen_item = self.top_skin_id
        return chosen_item

    def get_default_choose_skin(self, role_id):
        role_skin_id = dress_utils.get_role_dress_clothing_id(role_id)
        if role_skin_id:
            return role_skin_id
        else:
            default_skin = confmgr.get('role_info', 'RoleInfo', 'Content', str(role_id), 'default_skin')[0]
            return default_skin

    def get_preview_decoration_data(self):
        return self.preview_decoration

    def on_click_close_btn(self, *args):
        if self.cal_preview_different_with_equiped_skin_and_dec(self.preview_skin, self.preview_decoration) >= 2:
            from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
            dlg = SecondConfirmDlg2()

            def on_cancel():
                dlg.close()

            def on_confirm():
                dlg.close()
                self.close()

            dlg.confirm(content=get_text_local_content(81471), cancel_callback=on_cancel, confirm_callback=on_confirm, unique_callback=on_cancel)
        else:
            self.close()

    def on_click_btn_buy(self, *args):
        player = global_data.player
        cur_role_id = player.get_role()
        role_item_data = player.get_item_by_no(self.role_id)
        has_role = role_item_data is not None or cur_role_id == self.role_id
        skin_item_data = player.get_item_by_no(self.preview_skin)
        has_skin = skin_item_data is not None
        if not has_role:
            if item_utils.can_jump_to_ui(self.role_id):
                global_data.ui_mgr.close_ui('RoleAndSkinBuyConfirmUI')
                from logic.comsys.mall_ui.RoleAndSkinBuyConfirmUI import RoleAndSkinBuyConfirmUI
                ui = RoleAndSkinBuyConfirmUI(goods_id=str(self.role_id))
                ui.set_buttom_ui_price_nd(self.panel.nd_top)
                callback = lambda : item_utils.jump_to_ui(self.role_id)
                ui.enable_btn_buy_get(callback, item_utils.get_item_access(self.role_id))
            else:
                role_goods_id = confmgr.get('role_info', 'RoleInfo', 'Content', str(self.role_id), 'goods_id')
                price = mall_utils.get_mall_item_price(role_goods_id)
                if price:
                    ui = role_or_skin_buy_confirmUI(role_goods_id)
                    ui.set_buttom_ui_price_nd(self.panel.nd_top)
                else:
                    log_error('on_click_btn_buy try to buy role_id failed', self.role_id)
        else:
            show_buy_item_data_list = []
            if not has_skin:
                show_buy_item_data_list.append({'item_no': self.preview_skin,'quantity': 1})
            own_dict, no_own_dict, can_buy_dict, no_can_buy_dict = self.get_decoration_buy_info()
            if no_own_dict:
                for item_no in six.itervalues(no_own_dict):
                    if item_no not in six_ex.values(self.default_decoration) and dress_utils.check_valid_decoration(self.preview_skin, item_no):
                        show_buy_item_data_list.append({'item_no': item_no,'quantity': 1})

            if show_buy_item_data_list:
                ui = CommonBuyListUI()
                if ui:
                    ui.set_item_remove_callback(self.on_remove_item_when_view_buy_list)
                    ui.set_batch_buy_callback(self.on_about_to_buy_callback)
                    ui.init_buy_list_item(show_buy_item_data_list)
            else:
                self.try_deploy_preview_item()
        return

    def on_click_details_btn(self, *args):
        from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
        dlg = GameRuleDescUI()
        title, rule = (81467, 81468)
        dlg.set_show_rule(get_text_local_content(title), get_text_local_content(rule))

    def try_on_item_no(self, item_no):
        has_item = global_data.player.has_item_by_no(item_no)
        if not has_item:
            return
        belong_no = item_utils.get_lobby_item_belong_no(item_no)
        if belong_no != self.role_id:
            return
        item_type = item_utils.get_lobby_item_type(item_no)
        if item_type == lobby_item_type.L_ITEM_TYPE_ROLE_SKIN:
            if self.get_chosen_skin() == item_no:
                return
            global_data.player.install_role_skin_scheme(self.role_id, dress_utils.get_top_skin_id_by_skin_id(item_no), item_no, {FASHION_POS_SUIT: item_no})
        elif item_type in lobby_item_type.ITEM_TYPE_DEC:
            fashion_pos = dress_utils.get_lobby_type_fashion_pos(item_type)
            self.choose(fashion_pos, item_no)

    def on_remove_item_when_view_buy_list(self, item_no):
        has_item = global_data.player.has_item_by_no(item_no)
        if has_item:
            if item_no == self.preview_skin:
                global_data.player.install_role_skin_scheme(self.role_id, self.top_skin_id, self.preview_skin, {FASHION_POS_SUIT: self.preview_skin})
                self._changed_target_fashion_parts.append(FASHION_POS_SUIT)
            if not self.preview_decoration:
                return
            for tag, dec_item_no in six.iteritems(self.preview_decoration):
                if item_no == dec_item_no:
                    self.choose(tag, item_no)

        elif item_no == self.preview_skin:
            new_preview_skin = dress_utils.get_top_skin_clothing_id(self.role_id, self.top_skin_id)
            self.set_all_preview_items(new_preview_skin, self.preview_decoration)
        else:
            if not self.preview_decoration:
                return
            new_preview_dec = dict(self.preview_decoration)
            for tag, dec_item_no in six.iteritems(self.preview_decoration):
                if item_no == dec_item_no:
                    new_preview_dec[tag] = self.chosen_dec_item.get(tag)

            self.set_all_preview_items(self.preview_skin, new_preview_dec)

    def on_about_to_buy_callback(self, batch_buy_item_list):
        self._waiting_for_batch_buy_item_list = [ item_no for item_no in batch_buy_item_list if item_no not in self._invisible_decoration_id_list ]
        self._batch_buy_dec_preview_skin = self.preview_skin or self.get_chosen_skin()
        global_data.emgr.set_reward_show_blocking_item_no_event.emit(self._waiting_for_batch_buy_item_list)

    def clear_buy_reward_blocking(self):
        self._waiting_for_batch_buy_item_list = []
        self._batch_buy_dec_preview_skin = None
        global_data.emgr.set_reward_show_blocking_item_no_event.emit(self._waiting_for_batch_buy_item_list)
        return

    def test_check_batch_buy_show(self):
        self._waiting_for_batch_buy_item_list = [
         201001131, 20501403]
        self.check_batch_buy_show()

    def check_batch_buy_show(self):
        if not self._waiting_for_batch_buy_item_list:
            return
        else:
            if global_data.player:
                for item_no in self._waiting_for_batch_buy_item_list:
                    if not global_data.player.has_item_by_no(item_no):
                        return
                    self.try_on_item_no(item_no)

                preview_skin = self._batch_buy_dec_preview_skin or self.get_chosen_skin()
                new_skin = None
                current_preview_item = dict(self.chosen_dec_item)
                preview_decoration_list = []
                for item_no in self._waiting_for_batch_buy_item_list:
                    item_type = item_utils.get_lobby_item_type(item_no)
                    if item_type == lobby_item_type.L_ITEM_TYPE_ROLE_SKIN:
                        new_skin = item_no
                        preview_skin = item_no
                    else:
                        preview_decoration_list.append(item_no)

                decoration_dict = dress_utils.decoration_list_to_fashion_dict(preview_decoration_list)
                current_preview_item.update(decoration_dict)
                if preview_decoration_list:
                    from logic.comsys.role_profile.RoleSkinBuyShowUI import RoleSkinBuyShowUI
                    ui = RoleSkinBuyShowUI()
                    if ui:
                        ui.set_role_top_skin(self.role_id, self.top_skin_id, preview_skin, new_skin, current_preview_item, decoration_dict)
                        ui.set_close_callback(self.clear_buy_reward_blocking)
                else:
                    self.clear_buy_reward_blocking()
            return

    def on_click_btn_use(self, *args):
        self.on_click_btn_buy()

    def try_deploy_preview_item(self):
        player = global_data.player
        cur_role_id = player.get_role()
        skin_data = global_data.player.get_item_by_no(self.preview_skin)
        if skin_data:
            global_data.player.install_role_skin_scheme(self.role_id, self.top_skin_id, self.preview_skin, {FASHION_POS_SUIT: self.preview_skin})
            self._changed_target_fashion_parts.append(FASHION_POS_SUIT)
        else:
            log_error('try to put on clothing that is no owned!')
        if self.preview_decoration:
            own_dict, no_own_dict, can_buy_dict, no_can_buy_dict = self.get_decoration_buy_info()
            if not no_own_dict:
                for tag, item_no in six.iteritems(self.preview_decoration):
                    if item_no:
                        self.choose(tag, item_no)

    def _on_rotate_drag(self, layer, touch):
        delta_pos = touch.getDelta()
        global_data.emgr.rotate_model_display.emit(-delta_pos.x / ROTATE_FACTOR)

    def _update_buttons_by_skin_item_no(self, item_no):
        item_data = global_data.player.get_item_by_no(item_no)
        if item_data is None:
            goods_id = self.role_skin_config.get(str(item_no), {}).get('goods_id')
            price = mall_utils.get_mall_item_price(goods_id)
            if price:
                self.panel.nd_buy.setVisible(True)
                self.panel.lab_get_method.setVisible(False)
                self.panel.temp_btn_use.setVisible(False)
                template_utils.init_price_view(self.panel.temp_price, goods_id, mall_const.DEF_PRICE_COLOR)
                self.panel.temp_btn_buy.btn_common.SetText(get_text_by_id(860095))
            elif item_utils.can_jump_to_ui(item_no):
                self.panel.nd_buy.setVisible(False)
                self.panel.lab_get_method.setVisible(True)
                self.panel.temp_btn_use.setVisible(True)
                self.panel.lab_get_method.SetString(item_utils.get_item_access(item_no))
                self.panel.temp_btn_use.btn_common.SetText(2222)
            else:
                self.panel.nd_buy.setVisible(False)
                self.panel.temp_btn_use.setVisible(True)
                self.panel.temp_btn_use.btn_common.SetEnable(False)
                self.panel.temp_btn_use.btn_common.SetText(80828)
                access_txt = item_utils.get_item_access(str(item_no))
                if access_txt:
                    self.panel.lab_get_method.SetString(access_txt)
                    self.panel.lab_get_method.setVisible(True)
        return

    def check_role_status(self):
        self.update_money_type()
        self.panel.nd_buy.setVisible(False)
        self.panel.temp_btn_use.setVisible(False)
        self.panel.lab_get_method.setVisible(False)
        self.panel.temp_btn_use.btn_common.SetEnable(True)
        self.panel.lab_get_method.ReConfColor()
        player = global_data.player
        cur_role_id = player.get_role()
        role_item_data = player.get_item_by_no(self.role_id)
        has_role = role_item_data is not None or cur_role_id == self.role_id
        skin_item_data = player.get_item_by_no(self.preview_skin)
        has_skin = skin_item_data is not None
        if not has_role:
            if self._cur_tag == TAG_IMPROVE_DEC:
                return
            role_goods_id = confmgr.get('role_info', 'RoleInfo', 'Content', str(self.role_id), 'goods_id')
            if role_goods_id is not None:
                price = mall_utils.get_mall_item_price(role_goods_id)
                if item_utils.can_jump_to_ui(self.role_id):
                    self.panel.nd_buy.temp_btn_buy.btn_common.SetEnable(True)
                    self.panel.lab_get_method.setVisible(True)
                    self.panel.temp_btn_use.setVisible(True)
                    self.panel.lab_get_method.SetString(item_utils.get_item_access(self.role_id))
                    self.panel.temp_btn_use.btn_common.SetText(860106)
                elif price:
                    self.panel.nd_buy.setVisible(True)
                    self.panel.temp_price.setVisible(True)
                    template_utils.init_price_view(self.panel.temp_price, role_goods_id, mall_const.DEF_PRICE_COLOR)
                    self.panel.temp_btn_buy.btn_common.SetText(get_text_by_id(860094))
                else:
                    self.panel.nd_buy.setVisible(False)
                    self.panel.temp_btn_use.setVisible(False)
                    self.panel.lab_get_method.setVisible(False)
            else:
                self.panel.temp_btn_use.setVisible(True)
                self.panel.temp_btn_use.btn_common.SetEnable(False)
                self.panel.temp_btn_use.btn_common.SetText(get_text_by_id(14008))
        else:
            if self._cur_tag == TAG_IMPROVE_DEC:
                return
            if self.check_is_all_preview_is_equipped():
                return
            is_skin_can_buy = False
            if not has_skin:
                goods_id = self.role_skin_config.get(str(self.preview_skin), {}).get('goods_id')
                price = mall_utils.get_mall_item_price(goods_id)
                is_skin_can_buy = bool(price)
            own_dict, no_own_dict, can_buy_dict, no_can_buy_dict = self.get_decoration_buy_info()
            if not no_own_dict and has_skin:
                self.panel.nd_buy.setVisible(False)
                self.panel.temp_btn_use.setVisible(True)
                prices = [{'goods_payment': gconst.SHOP_PAYMENT_GOLD,'original_price': 0}]
                template_utils.splice_price(self.panel.temp_price, prices)
                self.panel.temp_btn_buy.btn_common.SetText(get_text_by_id(860096))
                self.panel.temp_btn_use.btn_common.SetText(get_text_by_id(860096))
            else:
                if no_can_buy_dict or not has_skin and not is_skin_can_buy:
                    self.panel.lab_get_method.SetString(860076)
                    self.panel.lab_get_method.setVisible(True)
                    self.panel.lab_get_method.SetColorCheckRecord('#BR')
                self.panel.nd_buy.setVisible(False)
                self.panel.temp_btn_use.setVisible(True)
                self.panel.temp_btn_use.btn_common.SetText(get_text_by_id(860091))
        return

    def get_decoration_buy_info(self):
        own_dict = {}
        no_own_dict = {}
        can_buy_dict = {}
        no_can_buy_dict = {}
        decoration_key_list = FASHION_DECORATION_TYPE_LIST
        for dec_key in decoration_key_list:
            item_no = self.preview_decoration.get(dec_key, None)
            if not item_no:
                continue
            own = global_data.player.has_item_by_no(item_no) if global_data.player else False
            if own:
                own_dict[dec_key] = item_no
            else:
                no_own_dict[dec_key] = item_no

        for dec_key, item_no in six.iteritems(no_own_dict):
            goods_id = dress_utils.get_goods_id_of_role_dress_related_item_no(item_no)
            price = mall_utils.get_mall_item_price(goods_id)
            if price:
                can_buy_dict[dec_key] = item_no
            else:
                no_can_buy_dict[dec_key] = item_no

        return (own_dict, no_own_dict, can_buy_dict, no_can_buy_dict)

    def on_click_btn_clear(self, *args):
        role_skin_id, role_skin_decoration_data = self.get_chosen_role_skin_data(self.role_id, self.top_skin_id)
        if self.cal_preview_different_with_equiped_skin_and_dec(self.preview_skin, self.preview_decoration) >= 2:
            from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
            dlg = SecondConfirmDlg2()

            def on_cancel():
                dlg.close()

            def on_confirm():
                dlg.close()
                self.set_all_preview_items(role_skin_id, role_skin_decoration_data)

            dlg.confirm(content=get_text_local_content(81472), cancel_callback=on_cancel, confirm_callback=on_confirm, unique_callback=on_cancel)
        else:
            self.set_all_preview_items(role_skin_id, role_skin_decoration_data)

    def cal_preview_different_with_equiped_skin_and_dec(self, preview_skin, preview_dec):
        role_skin_id, role_skin_decoration_data = self.get_chosen_role_skin_data(self.role_id, self.top_skin_id)
        diff_num = 0
        if preview_skin != role_skin_id:
            diff_num += 1
        for dec in FASHION_DECORATION_TYPE_LIST:
            if preview_dec.get(dec) != role_skin_decoration_data.get(dec) and preview_dec.get(dec):
                diff_num += 1

        return diff_num

    cam_key = {CAM_MODE_FAR: 'far_cam',
       CAM_MODE_NEAR: 'near_cam',
       CAM_MODE_NEAR_LEG: 'leg_cam',
       CAM_MODE_NEAR_HEAD: 'head_cam'
       }

    def set_cam_mode(self, cam_mode, is_slerp=True):
        self.cur_cam_mode = cam_mode
        if self.cam_data is None:
            return
        else:
            key = self.cam_key.get(cam_mode, 'near_cam')
            cam_pos = self.cam_data.get(key, None)
            cam_pos and global_data.emgr.change_model_display_scene_cam_pos.emit(math3d.vector(*cam_pos), is_slerp)
            return

    def on_click_btn_full_screen(self, *args):
        self.set_cam_mode(CAM_MODE_FAR)
        self.panel.StopAnimation('appear')
        self.panel.PlayAnimation('disappear')
        if self._cur_tag:
            self.widget_dict[self._cur_tag].panel.PlayAnimation('disappear')
        if self.panel.temp_list_plan.isVisible() or self.panel.IsPlayingAnimation('show_plan'):
            self.panel.StopAnimation('show_plan')
            self.panel.PlayAnimation('disappear_plan')
        from logic.comsys.common_ui.FullScreenBackUI import FullScreenBackUI
        ui = FullScreenBackUI()
        if ui:
            ui.setBackFunctionCallback(self.recover_from_full_screen)
            ui.setZoomButtonCallback(self.zoom_change)

    def recover_from_full_screen(self):
        if self.panel and self.panel.isValid():
            self.on_click_btn_glass(reset=True)
            self.panel.PlayAnimation('appear')
            if self._cur_tag:
                self.widget_dict[self._cur_tag].panel.PlayAnimation('appear')

    def zoom_change(self):
        if self.cur_cam_mode == CAM_MODE_FAR:
            self.set_cam_mode(CAM_MODE_NEAR)
            return False
        else:
            self.set_cam_mode(CAM_MODE_FAR)
            return True

    def on_click_manager_btn(self, *args):

        def _show_plan():
            self.panel.StopAnimation('disappear_plan')
            self.panel.PlayAnimation('show_plan')

        if not self._skin_plan_widget_inited:
            if global_data.player:
                skin_plan = global_data.player.get_fashion_scheme(self.top_skin_id)
                if skin_plan is None:
                    global_data.player.request_fashion_scheme(self.top_skin_id)
                    self._is_in_request_fashion_scheme = True
                else:
                    self.skin_plan_widget.set_plan_info(self.role_id, self.top_skin_id, skin_plan)
                    self._skin_plan_widget_inited = True
                    _show_plan()
        else:
            _show_plan()
        return

    def on_click_close_manager_btn(self, btn, touch):
        self.panel.StopAnimation('show_plan')
        self.panel.PlayAnimation('disappear_plan')

    def get_player_skin_list(self):
        top_skin_list = []
        _top_skin_list = confmgr.get('role_info', 'RoleInfo', 'Content', str(self.role_id), 'skin_list')
        if _top_skin_list:
            for item_id in _top_skin_list:
                if item_utils.can_open_show(item_id):
                    top_skin_list.append(item_id)

        showed_skin_list = dress_utils.get_top_skin_clothing_id_list(self.role_id, top_skin_list)
        return (
         top_skin_list, showed_skin_list)

    def on_click_btn_last(self, *args):
        top_skin_list, showed_skin_list = self.get_player_skin_list()
        if self.top_skin_id not in top_skin_list:
            return
        cur_index = top_skin_list.index(self.top_skin_id)
        new_skin_id = showed_skin_list[-1] if cur_index == 0 else showed_skin_list[cur_index - 1]
        self.jump_to_skin(new_skin_id)

    def on_click_btn_next(self, *args):
        top_skin_list, showed_skin_list = self.get_player_skin_list()
        if self.top_skin_id not in top_skin_list:
            return
        cur_index = top_skin_list.index(self.top_skin_id)
        new_skin_id = showed_skin_list[0] if cur_index == len(showed_skin_list) - 1 else showed_skin_list[cur_index + 1]
        self.jump_to_skin(new_skin_id)

    def on_click_btn_glass(self, *args, **kwargs):
        reset = kwargs.get('reset', False)
        is_slerp = kwargs.get('is_slerp', True)
        self.btn_glass_clicked = not (reset or self.btn_glass_clicked)
        if self.btn_glass_clicked:
            self.panel.btn_glass.icon_glass.SetDisplayFrameByPath('', 'gui/ui_res_2/common/icon/icon_glass_big.png')
            self.set_cam_mode(CAM_MODE_FAR, is_slerp)
        else:
            self.panel.btn_glass.icon_glass.SetDisplayFrameByPath('', 'gui/ui_res_2/common/icon/icon_glass_small.png')
            self.set_cam_mode(tag_cam_dict.get(self._cur_tag, CAM_MODE_NEAR), is_slerp)
        if reset:
            self.panel.btn_glass.setVisible(self.cur_cam_mode != CAM_MODE_FAR)

    def revert_choose(self, tag):
        if not self.chosen_dec_item.get(tag):
            return
        self.chosen_dec_item[tag] = 0
        self._changed_target_fashion_parts.append(tag)
        global_data.player.uninstall_role_skin_scheme(self.role_id, self.top_skin_id, self.preview_skin, [tag])

    def choose(self, tag, item_no):
        if self.chosen_dec_item.get(tag) == item_no:
            return
        suit_revert_list = list(FASHION_DRESS_PARTS)
        if FASHION_POS_SUIT_2 in suit_revert_list:
            suit_revert_list.remove(FASHION_POS_SUIT_2)
        if FASHION_POS_SUIT in suit_revert_list:
            suit_revert_list.remove(FASHION_POS_SUIT)
        revert_tag = suit_revert_list if tag == TAG_SUIT else (TAG_SUIT,)
        for _tag in revert_tag:
            for widget_tag in DEC_WIDGET_TAG_LIST:
                if widget_tag in self.widget_dict:
                    self.widget_dict[widget_tag].revert_choose_by_tag(_tag)
                else:
                    self.revert_choose(_tag)

        self.chosen_dec_item[tag] = item_no
        self._changed_target_fashion_parts.append(tag)
        global_data.player.install_role_skin_scheme(self.role_id, self.top_skin_id, self.preview_skin, {tag: item_no})

    def on_role_top_skin_scheme_responed(self, role_id):
        if not self.panel.IsVisible():
            return
        else:
            if self._need_jump_to_item_no:
                self._is_in_role_request_fashion_scheme = False
                self.jump_to_item_no(self._need_jump_to_item_no, self.adapt_skin_id_list[0] if self.adapt_dec_no else None)
            elif self._need_jump_to_skin:
                self._is_in_role_request_fashion_scheme = False
                self.jump_to_skin(self._need_jump_to_skin)
            elif self._need_jump_to_improve_s_plus:
                self._is_in_role_request_fashion_scheme = False
                self.jump_to_improve_s_plus(self._need_jump_to_improve_s_plus)
            else:
                if str(role_id) != str(self.role_id):
                    return
                self._is_in_role_request_fashion_scheme = False
                self.set_role_top_skin(self.role_id, self.top_skin_id)
            return

    def on_role_top_skin_scheme_changed_event(self, role_id, fashion_id, scheme):
        if not self.isPanelVisible():
            return
        if str(role_id) != str(self.role_id):
            return
        if not self._changed_target_fashion_parts:
            new_skin_id = int(scheme.get(FASHION_POS_SUIT, fashion_id))
            self.change_preview_skin(new_skin_id)
            self.widget_dict[self._cur_tag].on_dress_change(new_skin_id)
            self.check_role_status()
        else:
            if FASHION_POS_SUIT in self._changed_target_fashion_parts:
                new_skin_id = int(scheme.get(FASHION_POS_SUIT, fashion_id))
                self.change_preview_skin(new_skin_id)
                self.widget_dict[self._cur_tag].on_dress_change(new_skin_id)
                self._changed_target_fashion_parts.remove(FASHION_POS_SUIT)
            if self._changed_target_fashion_parts:
                self.widget_dict[self._cur_tag].on_dress_change(self.preview_skin)
                self.check_role_status()
            self._changed_target_fashion_parts = []

    def ui_vkb_custom_func(self):
        self.on_click_close_btn()

    def show_dec_adapt_skin_list(self, dec_no, _, dec_no_list):
        skin_id_list = dress_utils.handle_usable_skin_list(dec_no)
        self.adapt_dec_no = dec_no
        self.adapt_skin_id_list = skin_id_list
        self.adapt_dec_no_list = dec_no_list
        self.panel.btn_sort.setVisible(True)
        self.panel.nd_sort_list.setVisible(True)
        self.refresh_skin_mode_list(dec_no, skin_id_list, dec_no_list)
        is_guided = global_data.achi_mgr.get_cur_user_archive_data('xingyuan_dec_adapt_guide')
        if not is_guided:
            self.panel.PlayAnimation('guide')
            global_data.achi_mgr.set_cur_user_archive_data('xingyuan_dec_adapt_guide', True)

    def hide_dec_adapt_guide_list(self):
        self.adapt_dec_no = None
        self.adapt_skin_id_list = []
        self.adapt_dec_no_list = []
        self.panel.StopAnimation('guide')
        self.panel.nd_guide.setVisible(False)
        self.panel.btn_sort.setVisible(False)
        return

    def refresh_skin_mode_list(self, dec_no, skin_id_list, dec_no_list):
        from logic.gutils import template_utils
        from logic.gutils import item_utils, role_head_utils
        mode_option = [ {'name': item_utils.get_lobby_item_name(item_no),'mode': int(item_no),'icon': item_utils.get_lobby_item_pic_by_item_no(item_no)} for item_no in skin_id_list
                      ]

        @self.panel.btn_sort.unique_callback()
        def OnClick(btn, touch):
            if not self.panel.nd_sort_list.isVisible():
                self.panel.nd_sort_list.setVisible(True)
                self.panel.img_arrow.setRotation(180)
            else:
                self.panel.nd_sort_list.setVisible(False)
                self.panel.img_arrow.setRotation(0)

        def call_back(index):
            option = mode_option[index]
            to_skin_id = option['mode']
            self.panel.lab_skin_name.SetString(option['name'])
            pic_path = option.get('icon', '')
            self.panel.img_role.SetDisplayFrameByPath('', pic_path)
            self.panel.img_role.setVisible(bool(pic_path))
            self.panel.nd_sort_list.setVisible(False)
            self.panel.img_arrow.setRotation(0)
            l_item_type = item_utils.get_lobby_item_type(dec_no)
            fashion_pos = dress_utils.get_lobby_type_fashion_pos(l_item_type)
            valid_deco_list = dress_utils.get_valid_deco_list_for_skin_id(None, to_skin_id, [FPOS_2_TAG_STR.get(fashion_pos, '')])
            target_dec_no = dec_no
            if dec_no_list:
                for _dec_no in dec_no_list:
                    if _dec_no in valid_deco_list:
                        target_dec_no = _dec_no

            self.jump_to_item_no(target_dec_no, to_skin_id)
            return

        self.init_common_choose_list_for_role_define(self.panel.nd_sort_list, mode_option, call_back, max_height=600)
        call_back(0)

    def init_common_choose_list_for_role_define(self, widget, option_list, callback=None, max_height=None, close_cb=None, reverse=False):
        if reverse:
            option_list.reverse()
        old_size = widget.bar.getContentSize()
        old_list_size = widget.sort_list.getContentSize()
        extra_height = old_size.height - old_list_size.height
        widget.sort_list.SetInitCount(len(option_list))
        all_items = widget.sort_list.GetAllItem()
        for index, item_widget in enumerate(all_items):
            option = option_list[index]
            display_text = option['name']
            display_font = option.get('font', None)
            item_no = option.get('mode', None)
            own = global_data.player.has_item_by_no(item_no)
            item_widget.lab_have.setVisible(own)
            item_widget.lab_not_have.setVisible(not own)
            if type(display_text) is int:
                item_widget.lab_skin_name.SetText(get_text_by_id(option['name']), font_name=display_font)
            else:
                item_widget.lab_skin_name.SetString(option['name'])
            if 'icon' in option:
                item_widget.img_role.SetDisplayFrameByPath('', option['icon'])
                item_widget.img_role.setVisible(True)
            else:
                item_widget.img_role.setVisible(False)

            @item_widget.button.unique_callback()
            def OnClick(btn, touch, index=index):
                if callback:
                    callback(index)
                widget.setVisible(False)
                if close_cb:
                    close_cb()

        width, _ = widget.sort_list.GetContentSize()
        _, height = widget.sort_list.GetContainer().GetContentSize()
        if max_height:
            height = min(height, max_height)
        widget.sort_list.SetContentSize(width, height)
        widget.bar.SetContentSize(old_size.width, height + extra_height)
        if reverse:
            widget.sort_list.ScrollToBottom()
        return