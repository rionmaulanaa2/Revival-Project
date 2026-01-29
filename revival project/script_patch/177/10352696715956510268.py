# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mall_ui/GetMechaModelDisplayUI.py
from __future__ import absolute_import
import six
from six.moves import range
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER
from logic.gutils import item_utils
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_ROLE, L_ITEM_TYPE_MECHA, L_ITEM_TYPE_ROLE_SKIN, L_ITEM_TYPE_MECHA_SKIN, L_ITEM_MECHA_SFX, L_ITEM_TYPE_WEAPON_SFX, L_ITEM_TYPE_HEAD, L_ITEM_TYPE_BODY, L_ITEM_TYPE_SUIT
from common.const.uiconst import UI_TYPE_MESSAGE
from logic.gcommon.common_const import mecha_const
from common.cfg import confmgr
from logic.gutils.dress_utils import mecha_lobby_id_2_battle_id, get_mecha_model_h_path, get_skin_default_wear_decoration_dict
from logic.gcommon.item.item_const import FASHION_POS_SUIT, RARE_DEGREE_5, RARE_DEGREE_4, RARE_DEGREE_3, RARE_DEGREE_2
from logic.gcommon import time_utility
from logic.gutils import bond_utils
from logic.client.const import lobby_model_display_const
from logic.gutils import lobby_model_display_utils
from logic.gutils.reinforce_card_utils import get_card_item_no
from logic.gutils.mecha_module_utils import init_module_temp_item
from logic.comsys.share.ScreenFrameHelper import ScreenFrameHelper
import logic.gcommon.item.item_const as item_const
from logic.gcommon.item import item_utility
from logic.gutils.skin_define_utils import get_main_skin_id
EXCEPT_HIDE_UI_LIST = [
 'ReceiveRewardUI']
ROTATE_FACTOR = 850
RARE_NAME_CONFIG = {RARE_DEGREE_5: {'color': 15561215,'anim': 'appear_ss'},RARE_DEGREE_4: {'color': 16699994,'anim': 'appear_s'},RARE_DEGREE_3: {'color': 15309311,'anim': 'appear_a'},RARE_DEGREE_2: {'color': 4701439,'anim': 'appear_b'}}
NUM_NAME = {L_ITEM_TYPE_MECHA: 80846,
   L_ITEM_TYPE_MECHA_SKIN: 80848
   }
BTN_NAME = {L_ITEM_TYPE_MECHA: 19001,
   L_ITEM_TYPE_MECHA_SKIN: 80851
   }
MODEL_TYPE = [
 L_ITEM_TYPE_MECHA, L_ITEM_TYPE_MECHA_SKIN]
from common.const import uiconst
NORMAL_ITEM_TYPE = 0

class GetMechaModelDisplayUI(BasePanel):
    PANEL_CONFIG_NAME = 'mall/get_model_display_new01'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE_BY_DEFAULT_FUNC_NAME
    UI_ACTION_EVENT = {'temp_btn_close.btn_back.OnClick': 'on_click_close_btn',
       'nd_touch.OnDrag': '_on_rotate_drag',
       'btn_share.OnClick': 'on_click_share'
       }
    GLOBAL_EVENT = {'test_get_mecha': '_on_test_get_mecha'
       }
    SHARE_TIPS_INFO = (
     'btn_share', 3154, ('50%', '50%50'))

    def _on_test_get_mecha(self, show=False):
        for c in self.panel.GetChildren():
            if c.widget_name == 'nd_touch':
                continue
            c.setVisible(show)

    def on_init_panel(self, *args, **kwargs):
        self._show_wait_list = []
        self.hide()
        self.close_callback = None
        self._screen_capture_helper = ScreenFrameHelper()
        self._showing_item_no = None
        self._share_content = None
        self._num_text = None
        if global_data.ui_mgr.get_ui('SkinDefineUI'):
            self.panel.temp_btn_use.setVisible(False)
        self._scene_loaded = False
        self._scene_sfx_id = None
        return

    def _clean_scene_sfx(self):
        if self._scene_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self._scene_sfx_id)
        self._scene_sfx_id = None
        return

    def on_finalize_panel--- This code section failed: ---

 105       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             0  '_scene_loaded'
           6  POP_JUMP_IF_FALSE   120  'to 120'

 106       9  LOAD_GLOBAL           1  'global_data'
          12  LOAD_ATTR             2  'emgr'
          15  LOAD_ATTR             3  'scene_switch_background'
          18  LOAD_ATTR             4  'emit'
          21  LOAD_CONST            0  ''
          24  CALL_FUNCTION_1       1 
          27  POP_TOP          

 107      28  LOAD_GLOBAL           1  'global_data'
          31  LOAD_ATTR             2  'emgr'
          34  LOAD_ATTR             6  'scene_destroy_background'
          37  LOAD_ATTR             4  'emit'
          40  LOAD_CONST            1  'GetMechaModelDisplay'
          43  CALL_FUNCTION_1       1 
          46  POP_TOP          

 109      47  LOAD_GLOBAL           1  'global_data'
          50  LOAD_ATTR             2  'emgr'
          53  LOAD_ATTR             7  'change_model_display_control_type'
          56  LOAD_ATTR             4  'emit'
          59  LOAD_CONST            0  ''
          62  CALL_FUNCTION_1       1 
          65  POP_TOP          

 110      66  LOAD_GLOBAL           1  'global_data'
          69  LOAD_ATTR             2  'emgr'
          72  LOAD_ATTR             8  'close_model_display_scene'
          75  LOAD_ATTR             4  'emit'
          78  CALL_FUNCTION_0       0 
          81  POP_TOP          

 111      82  LOAD_GLOBAL           1  'global_data'
          85  LOAD_ATTR             2  'emgr'
          88  LOAD_ATTR             9  'leave_current_scene'
          91  LOAD_ATTR             4  'emit'
          94  CALL_FUNCTION_0       0 
          97  POP_TOP          

 113      98  LOAD_GLOBAL           1  'global_data'
         101  LOAD_ATTR             2  'emgr'
         104  LOAD_ATTR             7  'change_model_display_control_type'
         107  LOAD_ATTR             4  'emit'
         110  LOAD_CONST            0  ''
         113  CALL_FUNCTION_1       1 
         116  POP_TOP          
         117  JUMP_FORWARD          0  'to 120'
       120_0  COME_FROM                '117'

 114     120  LOAD_FAST             0  'self'
         123  LOAD_ATTR            10  'show_main_ui'
         126  CALL_FUNCTION_0       0 
         129  POP_TOP          

 116     130  LOAD_FAST             0  'self'
         133  LOAD_ATTR            11  '_clean_scene_sfx'
         136  CALL_FUNCTION_0       0 
         139  POP_TOP          

 118     140  LOAD_CONST            0  ''
         143  LOAD_FAST             0  'self'
         146  STORE_ATTR           12  '_showing_item_no'

 119     149  LOAD_CONST            0  ''
         152  LOAD_FAST             0  'self'
         155  STORE_ATTR           13  '_num_text'

 121     158  LOAD_FAST             0  'self'
         161  LOAD_ATTR            14  '_screen_capture_helper'
         164  POP_JUMP_IF_FALSE   192  'to 192'

 122     167  LOAD_FAST             0  'self'
         170  LOAD_ATTR            14  '_screen_capture_helper'
         173  LOAD_ATTR            15  'destroy'
         176  CALL_FUNCTION_0       0 
         179  POP_TOP          

 123     180  LOAD_CONST            0  ''
         183  LOAD_FAST             0  'self'
         186  STORE_ATTR           14  '_screen_capture_helper'
         189  JUMP_FORWARD          0  'to 192'
       192_0  COME_FROM                '189'

 125     192  LOAD_GLOBAL          16  'hasattr'
         195  LOAD_GLOBAL           2  'emgr'
         198  CALL_FUNCTION_2       2 
         201  POP_JUMP_IF_FALSE   241  'to 241'

 126     204  LOAD_FAST             0  'self'
         207  LOAD_ATTR            17  '_share_content'
         210  POP_JUMP_IF_FALSE   229  'to 229'

 127     213  LOAD_FAST             0  'self'
         216  LOAD_ATTR            17  '_share_content'
         219  LOAD_ATTR            15  'destroy'
         222  CALL_FUNCTION_0       0 
         225  POP_TOP          
         226  JUMP_FORWARD          0  'to 229'
       229_0  COME_FROM                '226'

 128     229  LOAD_CONST            0  ''
         232  LOAD_FAST             0  'self'
         235  STORE_ATTR           17  '_share_content'
         238  JUMP_FORWARD          0  'to 241'
       241_0  COME_FROM                '238'

 133     241  LOAD_FAST             0  'self'
         244  LOAD_ATTR            18  'close_callback'
         247  POP_JUMP_IF_FALSE   278  'to 278'

 134     250  LOAD_FAST             0  'self'
         253  LOAD_ATTR            18  'close_callback'
         256  STORE_FAST            1  'func'

 135     259  LOAD_CONST            0  ''
         262  LOAD_FAST             0  'self'
         265  STORE_ATTR           18  'close_callback'

 136     268  LOAD_FAST             1  'func'
         271  CALL_FUNCTION_0       0 
         274  POP_TOP          
         275  JUMP_FORWARD          0  'to 278'
       278_0  COME_FROM                '275'
         278  LOAD_CONST            0  ''
         281  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 198

    def on_click_close_btn(self, *args):

        def cache_specific_reward_showed_callback():
            self.close()

        from logic.comsys.reward.ReceiveRewardUI import ReceiveRewardUI
        ui = global_data.ui_mgr.get_ui('ReceiveRewardUI')
        if not ui and not (global_data.player and global_data.player.is_in_battle()):
            ReceiveRewardUI()
        global_data.emgr.show_cache_specific_reward.emit(self._showing_item_no, cache_specific_reward_showed_callback)

    def _on_rotate_drag(self, layer, touch):
        delta_pos = touch.getDelta()
        global_data.emgr.rotate_model_display.emit(-delta_pos.x / ROTATE_FACTOR)

    def update_exclusive_icon(self, item_no):
        item_utils.update_limit_btn(item_no, self.panel.temp_limited, self.panel.temp_limited.nd_limit_describe)

    def show_new_model_item(self, *args, **kwargs):
        self.on_get_new_model_event(*args, **kwargs)

    def on_get_new_model_event(self, item_no, callback=None, use_pass_anim=False, begin_continue_show=False, extra_info=None):
        item_type = item_utils.get_lobby_item_type(item_no)
        if item_type in MODEL_TYPE:
            if item_utils.is_default_skin(item_no):
                return
            m_path, item_type = item_utils.get_lobby_item_model_display_info(item_no)
            if m_path:
                self.show_next_model(item_no, callback, use_pass_anim, extra_info)

    def update_model_name(self, item_no):
        item_name = item_utils.get_lobby_item_name(item_no)
        rare_degree = item_utils.get_item_rare_degree(item_no)
        rare_color = RARE_NAME_CONFIG.get(rare_degree, {}).get('color', None)
        if not rare_color:
            rare_color = 16777215
        self.panel.lab_model_name.SetString(item_name)
        self.panel.lab_model_name.SetColor(rare_color)
        return

    def play_appear_anim(self, item_no):
        return
        import game3d
        rare_degree = item_utils.get_item_rare_degree(item_no)
        anim_name = RARE_NAME_CONFIG.get(rare_degree, {}).get('anim', None)
        self.panel.PlayAnimation('reset')
        if anim_name:

            def delay_ani():
                if self.panel and self.panel.isValid():
                    self.panel.PlayAnimation(anim_name)

            game3d.delay_exec(500, delay_ani)
        return

    def show_next_model(self, item_no, callback=None, use_pass_anim=False, extra_info=None):
        self._showing_item_no = item_no
        item_type = item_utils.get_lobby_item_type(item_no)
        self.hide_main_ui(exceptions=EXCEPT_HIDE_UI_LIST, exception_types=(UI_TYPE_MESSAGE,))
        self.update_model_name(item_no)
        self.play_appear_anim(item_no)
        if global_data.ui_mgr.get_ui('SkinDefineUI'):
            self.panel.temp_btn_use.setVisible(False)
        else:
            self.panel.temp_btn_use.setVisible(True)
        self.panel.lab_use_time.setVisible(False)
        item = global_data.player.get_item_by_no(item_no)
        if item:
            if item.expire_time > 0:
                delta = (item.expire_time - time_utility.get_server_time()) / time_utility.ONE_DAY_SECONDS
                day = round(delta)
                self.panel.lab_use_time.SetString(get_text_by_id(603002) % day)
                self.panel.lab_use_time.setVisible(True)
                self.panel.lab_model_name.ChildResizeAndPosition()
        self.panel.nd_module.setVisible(False)
        if item_type == L_ITEM_TYPE_MECHA:
            self.panel.nd_module.setVisible(True)
            mecha_id = mecha_lobby_id_2_battle_id(item_no)
            module_conf = confmgr.get('mecha_default_module_conf', default={}).get(str(mecha_id))
            slot_1 = module_conf.get('slot_pos1')
            slot_2 = module_conf.get('slot_pos2')
            slot_3 = module_conf.get('slot_pos3')
            slot_4 = module_conf.get('slot_pos4')
            card_list = [slot_1[0], slot_2[0], slot_3[0]]
            card_list.extend(slot_4)
            l = len(card_list)
            self.panel.module_list.SetInitCount(l)
            for i in range(l):
                module_nd = self.panel.module_list.GetItem(i)
                _item_no = get_card_item_no(card_list[i])
                module_nd.img_skill.SetDisplayFrameByPath('', item_utils.get_lobby_item_pic_by_item_no(_item_no))
                self.register_module_info_click(module_nd, _item_no)

        mecha_items = global_data.player.get_items_by_type(item_type)
        mecha_items = item_utility.filter_default_skin(mecha_items)
        self._num_text = get_text_by_id(NUM_NAME[item_type], {'num': str(len(mecha_items))})
        self.panel.lab_get_num.SetString(self._num_text)
        self.panel.temp_btn_use.btn_common_big.SetText(BTN_NAME[item_type])

        @self.panel.temp_btn_use.btn_common_big.callback()
        def OnClick(*args):
            if item_type == L_ITEM_TYPE_MECHA:
                pass
            elif item_type == L_ITEM_TYPE_MECHA_SKIN:
                mecha_lobby_id = item_utils.get_lobby_item_belong_no(item_no)
                mecha_battle_id = mecha_lobby_id_2_battle_id(mecha_lobby_id)
                main_skin_id = get_main_skin_id(item_no)
                global_data.player.install_mecha_main_skin_scheme(mecha_battle_id, main_skin_id, {FASHION_POS_SUIT: item_no})
            if item_type in [L_ITEM_TYPE_MECHA_SKIN]:
                show_new = global_data.lobby_red_point_data.get_rp_by_no(item_no)
                if show_new:
                    global_data.player.req_del_item_redpoint(item_no)
            self.on_click_close_btn()

        if extra_info:
            show_only = extra_info.get('show_only', None)
            if show_only is not None:
                self.set_show_only(show_only)
        else:
            self.set_show_only(False)
        mecha_id = confmgr.get('lobby_item', str(item_no), 'belong_id')
        if not mecha_id:
            mecha_id = item_no
        default_sfx = confmgr.get('mecha_conf', 'LobbyMechaConfig', 'Content', str(mecha_id), 'default_sfx')
        item_display_data = confmgr.get('display_enter_effect', 'Content', str(default_sfx), default={})
        callOutSfxPath = item_display_data.get('lobbyCallOutSfxPath', '')
        cSfxSoundName = item_display_data.get('cSfxSoundName', '')

        def on_finish_create_model(model, *args):
            if model:
                self._clean_scene_sfx()
                m_pos = model.position
                import math3d
                sfx_pos = math3d.vector(m_pos)
                self._scene_sfx_id = global_data.sfx_mgr.create_sfx_in_scene('effect/fx/niudan/choujiang/scenes.sfx', pos=sfx_pos)
            rare_degree = item_utils.get_item_rare_degree(item_no)
            if rare_degree in (RARE_DEGREE_4, RARE_DEGREE_5):
                global_data.sound_mgr.play_ui_sound('luckball_show')
            elif callOutSfxPath:
                if cSfxSoundName:
                    global_data.sound_mgr.play_ui_sound(cSfxSoundName)

        def show_model_and_scene():

            def load_cb():
                global_data.player.trigger_delay_notice_by_item_no(item_no)
                from logic.gcommon.item.item_const import FASHION_POS_SUIT, FASHION_POS_HEADWEAR, FASHION_POS_BACK, FASHION_POS_SUIT_2, FASHION_OTHER_PENDANT_LIST
                default_wear_dict = get_skin_default_wear_decoration_dict(item_no, item_no)
                head_id = default_wear_dict.get(FASHION_POS_HEADWEAR)
                bag_id = default_wear_dict.get(FASHION_POS_BACK)
                suit_id = default_wear_dict.get(FASHION_POS_SUIT_2)
                other_pendants = [ default_wear_dict.get(pos) for pos in FASHION_OTHER_PENDANT_LIST ]
                model_data = lobby_model_display_utils.get_lobby_model_data(item_no, True, head_id=head_id, bag_id=bag_id, suit_id=suit_id, other_pendants=other_pendants)
                for data in model_data:
                    data['skin_id'] = item_no
                    if global_data.get_mecha_scale is not None and 'model_scale' in data:
                        data['model_scale'] = data['model_scale'] * global_data.get_mecha_scale
                    if global_data.get_mecha_offset:
                        if 'off_position' in data:
                            data['off_position'][0] += global_data.get_mecha_offset[0]
                            data['off_position'][1] += global_data.get_mecha_offset[1]
                            data['off_position'][2] += global_data.get_mecha_offset[2]
                        else:
                            data['off_position'] = global_data.get_mecha_offset

                global_data.emgr.shutdown_box_opened_sfx.emit()
                global_data.emgr.change_model_display_scene_item.emit(model_data, create_callback=on_finish_create_model, model_control_type=lobby_model_display_const.CT_GET_MECHA_MODEL_DISPLAY)
                global_data.emgr.change_model_display_control_type.emit(lobby_model_display_const.CT_GET_MECHA_MODEL_DISPLAY)
                bg = global_data.scene_background.get_ui('GetMechaModelDisplay')
                if bg:
                    bg.on_appear()
                if callback and callable(callback):
                    self.close_callback = callback
                self.show()
                self.panel.temp_btn_close.btn_back.SetEnable(True)
                return

            self.show_scene(load_cb)

        if use_pass_anim:

            def show_pass_anim():
                self.panel.temp_btn_close.btn_back.SetEnable(False)
                transition_ui = global_data.ui_mgr.get_ui('GetModelDisplayBeforeUI')
                if not transition_ui:
                    from logic.comsys.mall_ui.GetModelDisplayBeforeUI import GetModelDisplayBeforeUI
                    transition_ui = GetModelDisplayBeforeUI()
                transition_ui.show_transition(show_model_and_scene)

            show_pass_anim()
        else:
            show_model_and_scene()
        return

    def show_scene(self, load_cb=None):
        from logic.gcommon.common_const import scene_const

        def cb(*args):
            self._scene_loaded = True
            global_data.emgr.scene_switch_background.emit('GetMechaModelDisplay')
            if callable(load_cb):
                load_cb()

        global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_GET_MECHA_MODEL_DISPLAY, lobby_model_display_const.GET_MECHA_MODEL_DISPLAY, finish_callback=cb)

    def register_module_info_click(self, module_nd, item_no):
        if item_no:

            @module_nd.unique_callback()
            def OnClick(layer, touch, *args):
                position = touch.getLocation()
                global_data.emgr.show_item_desc_ui_event.emit(item_no, None, directly_world_pos=position)
                return

    def on_click_share(self, btn, touch):
        ui_names = [self.__class__.__name__, 'OpenBoxUI']
        share_spec = confmgr.get('c_share_item_conf', str(self._showing_item_no), default={})
        if not share_spec:
            if self._screen_capture_helper:

                def custom_cb(*args):
                    self.panel.temp_btn_close.setVisible(True)
                    self.panel.btn_share.setVisible(True and global_data.is_share_show)
                    if global_data.ui_mgr.get_ui('SkinDefineUI'):
                        self.panel.temp_btn_use.setVisible(False)
                    else:
                        self.panel.temp_btn_use.setVisible(True)

                self.panel.temp_btn_close.setVisible(False)
                self.panel.btn_share.setVisible(False)
                self.panel.temp_btn_use.setVisible(False)
                self._screen_capture_helper.take_screen_shot(ui_names, self.panel, custom_cb=custom_cb)
        else:
            from logic.comsys.share.ItemInfoShareCreator import ItemInfoShareCreator
            if not self._share_content:
                self._share_content = ItemInfoShareCreator()
            template = share_spec.get('cTemplate', None)
            if template == '':
                template = None
            self._share_content.create(None, template)
            self._share_content.update_share_item_pic(self._showing_item_no)
            if self._num_text:
                self._share_content.update_share_item_num(self._showing_item_no, self._num_text)
            from logic.comsys.share.ShareUI import ShareUI
            ShareUI(parent=self.panel).set_share_content_raw(self._share_content.get_render_texture(), share_content=self._share_content)
        return

    def set_show_only(self, hide_extra_btns):
        is_vis = not hide_extra_btns
        self.panel.nd_use.setVisible(is_vis)
        self.panel.btn_share.setVisible(is_vis)
        self.panel.lab_get_num.setVisible(is_vis)
        self.panel.sp_smc.setVisible(is_vis)