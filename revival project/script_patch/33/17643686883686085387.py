# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mall_ui/GetModelDisplayUI.py
from __future__ import absolute_import
import six
from six.moves import range
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import item_utils
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_ROLE, L_ITEM_TYPE_MECHA, L_ITEM_TYPE_ROLE_SKIN, L_ITEM_TYPE_MECHA_SKIN, L_ITEM_MECHA_SFX, L_ITEM_TYPE_WEAPON_SFX, L_ITEM_TYPE_HEAD, L_ITEM_TYPE_BODY, L_ITEM_TYPE_SUIT, L_ITEM_TYPE_PET_SKIN
from common.const.uiconst import UI_TYPE_MESSAGE
from logic.gcommon.common_const import mecha_const
from common.cfg import confmgr
from logic.gutils import dress_utils
from logic.gutils.activity_utils import has_item
from logic.gutils.dress_utils import mecha_lobby_id_2_battle_id, get_mecha_model_h_path, get_skin_default_wear_decoration_dict
from logic.gcommon.item.item_const import FASHION_POS_SUIT, RARE_DEGREE_7, RARE_DEGREE_6, RARE_DEGREE_5, RARE_DEGREE_4, RARE_DEGREE_3, RARE_DEGREE_2
from logic.gcommon import time_utility
from logic.gutils import bond_utils
from logic.client.const import lobby_model_display_const
from logic.gutils import lobby_model_display_utils
from logic.comsys.lobby.RoleBondTipsUI import RoleBondTipsUI
from logic.gutils.reinforce_card_utils import get_card_item_no
from logic.gutils.mecha_module_utils import init_module_temp_item
from logic.comsys.share.ScreenFrameHelper import ScreenFrameHelper
import logic.gcommon.item.item_const as item_const
from logic.gcommon.item import item_utility
from logic.gutils.skin_define_utils import get_main_skin_id
from logic.gutils.share_utils import check_add_shareui_battle_record_func, get_share_bg_path, check_add_shareui_kv_func
from logic.gutils.mecha_skin_utils import is_s_skin_that_can_upgrade
from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
CAIDAN_JINSE_ZHANSHI_SHADER_CONTROL_END_TIME = 1.9
EXCEPT_HIDE_UI_LIST = [
 'ReceiveRewardUI']
ROTATE_FACTOR = 850
RARE_NAME_CONFIG = {RARE_DEGREE_7: {'color': 15561215,'anim': 'appear_sp'},RARE_DEGREE_6: {'color': 16668716,'anim': 'appear_s_plus'},RARE_DEGREE_5: {'color': 15561215,'anim': 'appear_ss'},RARE_DEGREE_4: {'color': 16699994,'anim': 'appear_s'},RARE_DEGREE_3: {'color': 15309311,'anim': 'appear_a'},RARE_DEGREE_2: {'color': 4701439,'anim': 'appear_b'}}
TITLE_NAME = {L_ITEM_TYPE_MECHA: 80842,
   L_ITEM_TYPE_ROLE: 80843,
   L_ITEM_TYPE_MECHA_SKIN: 80844,
   L_ITEM_TYPE_ROLE_SKIN: 80845,
   L_ITEM_MECHA_SFX: 80975,
   L_ITEM_TYPE_WEAPON_SFX: 80844,
   L_ITEM_TYPE_HEAD: 81345,
   L_ITEM_TYPE_BODY: 81346,
   L_ITEM_TYPE_SUIT: 81347,
   L_ITEM_TYPE_PET_SKIN: [
                        634883, 860439]
   }

def get_title_name(item_type, item_no):
    if item_type == L_ITEM_TYPE_PET_SKIN:
        base_skin = confmgr.get('c_pet_info', str(item_no), 'base_skin', default=item_no)
        if str(base_skin) == str(item_no):
            return TITLE_NAME[L_ITEM_TYPE_PET_SKIN][0]
        return TITLE_NAME[L_ITEM_TYPE_PET_SKIN][1]
    return TITLE_NAME[item_type]


NUM_NAME = {L_ITEM_TYPE_MECHA: 80846,
   L_ITEM_TYPE_ROLE: 80847,
   L_ITEM_TYPE_MECHA_SKIN: 80848,
   L_ITEM_TYPE_ROLE_SKIN: 80849,
   L_ITEM_TYPE_WEAPON_SFX: '',
   L_ITEM_TYPE_HEAD: 81348,
   L_ITEM_TYPE_BODY: 81349,
   L_ITEM_TYPE_SUIT: 81350,
   L_ITEM_TYPE_PET_SKIN: ''
   }
BTN_NAME = {L_ITEM_TYPE_MECHA: 14009,
   L_ITEM_TYPE_ROLE: 80850,
   L_ITEM_TYPE_MECHA_SKIN: 80851,
   L_ITEM_TYPE_ROLE_SKIN: 80851,
   L_ITEM_TYPE_WEAPON_SFX: 80851,
   L_ITEM_TYPE_HEAD: 19001,
   L_ITEM_TYPE_BODY: 19001,
   L_ITEM_TYPE_SUIT: 19001,
   L_ITEM_TYPE_PET_SKIN: 80851
   }
MODEL_TYPE = [
 L_ITEM_TYPE_ROLE,
 L_ITEM_TYPE_MECHA,
 L_ITEM_TYPE_ROLE_SKIN,
 L_ITEM_TYPE_MECHA_SKIN,
 L_ITEM_TYPE_WEAPON_SFX,
 L_ITEM_TYPE_HEAD,
 L_ITEM_TYPE_BODY,
 L_ITEM_TYPE_SUIT,
 L_ITEM_TYPE_PET_SKIN]
from common.const import uiconst
NORMAL_ITEM_TYPE = 0
BOND_LEVEL_UP_TYPE = 1
MECHA_AND_MECHA_SKIN_ITEM_TYPE = 2
IGNORE_SFX_ITEM_IDS = frozenset([
 201801151, 201801161,
 201801054, 201801055, 201801056, 201801064, 201801065, 201801066,
 201802451, 201802452, 201802453,
 201801744,
 201800155, 201800156, 201800157,
 201802152, 201802153, 201802154, 201802162, 201802163, 201802164,
 201800456])
IGNORE_SFX_MECHA_IDS = frozenset([
 101008035])

class GetModelDisplayUI(BasePanel):
    PANEL_CONFIG_NAME = 'mall/get_model_display'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE_BY_DEFAULT_FUNC_NAME
    GLOBAL_EVENT = {'show_new_model_item': 'on_get_new_model_event',
       'show_bond_level_up': 'on_bond_level_up_event',
       'show_new_effect_item': 'on_get_new_effect_event',
       'ui_close_event': 'on_ui_close',
       'close_share_ui_event': 'on_use_item_success'
       }
    UI_ACTION_EVENT = {'temp_btn_close.btn_back.OnClick': 'on_click_close_btn',
       'nd_touch.OnDrag': '_on_rotate_drag',
       'btn_share.btn_common_big.OnClick': 'on_click_share'
       }
    SHARE_TIPS_INFO = (
     'btn_share', 3154, ('50%', '50%50'))

    def on_init_panel(self, *args, **kwargs):
        self._show_wait_list = []
        self.music_name = None
        self.hide()
        self.close_callback = None
        self._screen_capture_helper = ScreenFrameHelper()
        self._showing_item_no = None
        self._share_content = None
        self._share_content_kv = None
        self._num_text = None
        self._blink_sfx_id = None
        self._zhaohuan_sfx_id = None
        self._is_in_share_anim = False
        self._is_model_unready = False
        self._need_model_share = False
        self._is_used = False
        if global_data.ui_mgr.get_ui('SkinDefineUI'):
            self.panel.temp_btn_use.setVisible(False)
        return

    def on_finalize_panel--- This code section failed: ---

 178       0  LOAD_CONST            0  ''
           3  LOAD_FAST             0  'self'
           6  STORE_ATTR            1  '_showing_item_no'

 179       9  LOAD_CONST            0  ''
          12  LOAD_FAST             0  'self'
          15  STORE_ATTR            2  '_num_text'

 180      18  LOAD_CONST            0  ''
          21  LOAD_FAST             0  'self'
          24  STORE_ATTR            3  'music_name'

 181      27  LOAD_CONST            0  ''
          30  LOAD_FAST             0  'self'
          33  STORE_ATTR            4  '_blink_sfx_id'

 182      36  LOAD_GLOBAL           5  'global_data'
          39  LOAD_ATTR             6  'emgr'
          42  LOAD_ATTR             7  'change_model_display_control_type'
          45  LOAD_ATTR             8  'emit'
          48  LOAD_CONST            0  ''
          51  CALL_FUNCTION_1       1 
          54  POP_TOP          

 183      55  LOAD_FAST             0  'self'
          58  LOAD_ATTR             9  '_screen_capture_helper'
          61  POP_JUMP_IF_FALSE    89  'to 89'

 184      64  LOAD_FAST             0  'self'
          67  LOAD_ATTR             9  '_screen_capture_helper'
          70  LOAD_ATTR            10  'destroy'
          73  CALL_FUNCTION_0       0 
          76  POP_TOP          

 185      77  LOAD_CONST            0  ''
          80  LOAD_FAST             0  'self'
          83  STORE_ATTR            9  '_screen_capture_helper'
          86  JUMP_FORWARD          0  'to 89'
        89_0  COME_FROM                '86'

 186      89  LOAD_GLOBAL          11  'hasattr'
          92  LOAD_GLOBAL           1  '_showing_item_no'
          95  CALL_FUNCTION_2       2 
          98  POP_JUMP_IF_FALSE   138  'to 138'

 187     101  LOAD_FAST             0  'self'
         104  LOAD_ATTR            12  '_share_content'
         107  POP_JUMP_IF_FALSE   126  'to 126'

 188     110  LOAD_FAST             0  'self'
         113  LOAD_ATTR            12  '_share_content'
         116  LOAD_ATTR            10  'destroy'
         119  CALL_FUNCTION_0       0 
         122  POP_TOP          
         123  JUMP_FORWARD          0  'to 126'
       126_0  COME_FROM                '123'

 189     126  LOAD_CONST            0  ''
         129  LOAD_FAST             0  'self'
         132  STORE_ATTR           12  '_share_content'
         135  JUMP_FORWARD          0  'to 138'
       138_0  COME_FROM                '135'

 190     138  LOAD_FAST             0  'self'
         141  LOAD_ATTR            13  '_share_content_kv'
         144  POP_JUMP_IF_FALSE   172  'to 172'

 191     147  LOAD_FAST             0  'self'
         150  LOAD_ATTR            13  '_share_content_kv'
         153  LOAD_ATTR            10  'destroy'
         156  CALL_FUNCTION_0       0 
         159  POP_TOP          

 192     160  LOAD_CONST            0  ''
         163  LOAD_FAST             0  'self'
         166  STORE_ATTR           13  '_share_content_kv'
         169  JUMP_FORWARD          0  'to 172'
       172_0  COME_FROM                '169'
         172  LOAD_CONST            0  ''
         175  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_2' instruction at offset 95

    def do_hide_panel(self):
        super(GetModelDisplayUI, self).do_hide_panel()
        if self.music_name:
            global_data.sound_mgr.play_event('Stop_Char_Music')

    def on_click_close_btn(self, *args):
        if not self._is_me_handling():
            return
        self.panel.PlayAnimation('reset')
        self.dispatch_event_data()

    def _is_handling_event(self):
        return self._is_me_handling() or bool(self._show_wait_list)

    def _is_me_handling(self):
        return self.isPanelVisible()

    def is_showing_model_item(self):
        normal_showing = self._is_me_handling()
        mecha_ui = global_data.ui_mgr.get_ui('GetMechaModelDisplayUI')
        mecha_showing = bool(mecha_ui) and mecha_ui.isPanelVisible()
        return normal_showing or mecha_showing

    def dispatch_event_data(self):
        if len(self._show_wait_list) > 0:
            self.hide()
            event_data = self._show_wait_list[0]
            e_type = event_data['type']
            if e_type == NORMAL_ITEM_TYPE:
                data = event_data['data']

                def cache_specific_reward_showed_callback():
                    if self._show_wait_list:
                        self._show_wait_list.pop(0)
                    self.set_show_only(False)
                    self.show_next_model(*data)

                from logic.comsys.reward.ReceiveRewardUI import ReceiveRewardUI
                ui = global_data.ui_mgr.get_ui('ReceiveRewardUI')
                if not ui and not global_data.player.is_in_battle():
                    ReceiveRewardUI()
                global_data.emgr.show_cache_specific_reward.emit(data[0], cache_specific_reward_showed_callback)
            elif e_type == BOND_LEVEL_UP_TYPE:
                from logic.comsys.battle.Settle import EndExpUI
                role_id, old_lv, level = event_data['data']

                def close_cb():
                    if not (self.panel and self.panel.isValid()):
                        return
                    if self._show_wait_list:
                        self._show_wait_list.pop(0)
                    if self._show_wait_list and self._show_wait_list[0]['type'] == BOND_LEVEL_UP_TYPE:
                        if self.panel:
                            self.panel.DelayCall(0.03, self.dispatch_event_data)
                    else:
                        self.dispatch_event_data()

                EndExpUI.show_role_bond_lv_up(role_id, old_lv, level, close_cb=close_cb)
            elif e_type == MECHA_AND_MECHA_SKIN_ITEM_TYPE:
                data = event_data['data']
                item_no, callback, use_pass_anim, begin_continue_show, extra_info = data
                self.close_callback = callback
                mecha_ui = global_data.ui_mgr.show_ui('GetMechaModelDisplayUI', 'logic.comsys.mall_ui')

                def close_cb():
                    if self._show_wait_list:
                        self._show_wait_list.pop(0)
                    if self._show_wait_list and self._show_wait_list[0]['type'] == MECHA_AND_MECHA_SKIN_ITEM_TYPE:
                        self.panel.DelayCall(0.03, self.dispatch_event_data)
                    else:
                        self.dispatch_event_data()

                mecha_ui.show_new_model_item(item_no, close_cb, use_pass_anim, begin_continue_show, extra_info)
        else:
            self.hide()

            def cache_specific_reward_showed_callback():
                global_data.emgr.change_model_display_control_type.emit(None)
                global_data.emgr.close_model_display_scene.emit()
                global_data.emgr.leave_current_scene.emit()
                self.show_main_ui()
                self._showing_item_no = None
                if self.close_callback:
                    func = self.close_callback
                    self.close_callback = None
                    func()
                else:
                    from logic.comsys.reward.ReceiveRewardUI import ReceiveRewardUI
                    ui = global_data.ui_mgr.get_ui('ReceiveRewardUI')
                    if not ui and not (global_data.player and global_data.player.is_in_battle()):
                        ReceiveRewardUI()
                    global_data.emgr.show_cache_generic_reward.emit()
                global_data.emgr.leave_get_model_display_ui.emit()
                return

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

    def on_get_new_effect_event(self, item_no, callback=None, extra_info=None):
        item_type = item_utils.get_lobby_item_type(item_no)
        if item_type != L_ITEM_MECHA_SFX:
            return
        else:
            self.panel.btn_share.setVisible(False)
            self.panel.lab_title.SetString(get_title_name(item_type, item_no))
            self.panel.lab_title.ChildResizeAndPosition()
            self.update_model_name(item_no)
            self.panel.nd_cv.setVisible(False)
            self.panel.lab_get_num.SetString('')
            if global_data.ui_mgr.get_ui('SkinDefineUI'):
                self.panel.temp_btn_use.setVisible(False)
            else:
                self.panel.temp_btn_use.setVisible(True)
            self.panel.lab_use_time.setVisible(False)
            self.update_exclusive_icon(item_no)
            self.hide_main_ui(exceptions=EXCEPT_HIDE_UI_LIST, exception_types=(UI_TYPE_MESSAGE,))
            self.panel.PlayAnimation('appear')
            if callback and callable(callback):
                self.close_callback = callback
            if extra_info:
                show_only = extra_info.get('show_only', None)
                if show_only is not None:
                    self.set_show_only(show_only)
            global_data.emgr.shutdown_box_opened_sfx.emit()
            self.show()
            self.panel.temp_btn_close.btn_back.SetEnable(True)
            self.panel.temp_btn_use.btn_common_big.SetText(80851)

            @self.panel.temp_btn_use.btn_common_big.callback()
            def OnClick(*args):
                from logic.gutils.dress_utils import battle_id_to_mecha_lobby_id
                item_config = confmgr.get('display_enter_effect', 'Content', str(item_no))
                lobby_mecha_id = global_data.player.get_lobby_selected_mecha_id()
                mecha_item_id = battle_id_to_mecha_lobby_id(lobby_mecha_id)
                global_data.player.try_set_mecha_sfx(mecha_item_id, item_config['itemNo'])
                global_data.game_mgr.show_tip(609656)
                self.on_click_close_btn()

            self.panel.nd_module.setVisible(False)
            item_display_data = confmgr.get('display_enter_effect', 'Content', str(item_no), default={})
            callOutSfxPath = item_display_data.get('lobbyCallOutSfxPath', '')
            cSfxSoundName = item_display_data.get('cSfxSoundName', '')

            def on_finish_create_model(model, *args):
                if not self._is_model_unready:
                    return
                else:
                    if callOutSfxPath:
                        if model:
                            model.visible = False
                        global_data.emgr.change_model_preview_effect.emit(callOutSfxPath)
                    self._is_model_unready = False
                    if self._need_model_share:
                        self._need_model_share = False
                        self.on_click_share(None, None)
                    return

            from logic.gcommon.common_const import scene_const
            global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_JIEMIAN_COMMON, lobby_model_display_const.DEFAULT_MID, scene_content_type=scene_const.SCENE_GET_MODEL_DISPLAY)
            mecha_item_id = global_data.player.get_lobby_selected_mecha_item_id()
            model_data = lobby_model_display_utils.get_lobby_model_data(mecha_item_id, True)
            self._is_model_unready = True
            global_data.emgr.change_model_display_scene_item.emit(model_data, create_callback=on_finish_create_model, model_control_type=lobby_model_display_const.CT_GET_MODEL_DISPLAY)
            global_data.emgr.change_model_display_control_type.emit(lobby_model_display_const.CT_GET_MODEL_DISPLAY)
            return

    def on_get_new_model_event(self, item_no, callback=None, use_pass_anim=False, begin_continue_show=False, extra_info=None):
        item_type = item_utils.get_lobby_item_type(item_no)
        if item_type in MODEL_TYPE:
            m_path, item_type = item_utils.get_lobby_item_model_display_info(item_no)
            if m_path or item_type in (L_ITEM_TYPE_HEAD, L_ITEM_TYPE_BODY, L_ITEM_TYPE_SUIT):
                ui = global_data.ui_mgr.get_ui('SeasonPassLevelUp')
                if ui:
                    ui.hide()
                if self._is_handling_event():
                    event_data = {'type': NORMAL_ITEM_TYPE,'data': [item_no, callback, use_pass_anim, begin_continue_show, extra_info]}
                    self._show_wait_list.append(event_data)
                else:
                    self.hide_main_ui(exceptions=EXCEPT_HIDE_UI_LIST, exception_types=(UI_TYPE_MESSAGE,))
                    self.show_next_model(item_no, callback, use_pass_anim, begin_continue_show, extra_info)

    def merge_bond_level_up_event(self):
        count = len(self._show_wait_list)
        if count <= 1:
            return
        else:
            start_index = 0
            cur_event = self._show_wait_list[0]
            if cur_event['type'] == BOND_LEVEL_UP_TYPE:
                start_index = 1
            roles_map = {}
            for i in range(start_index, count):
                event_data = self._show_wait_list[i]
                if event_data['type'] == BOND_LEVEL_UP_TYPE:
                    data = event_data['data']
                    role_id = data[0]
                    if role_id not in roles_map:
                        roles_map[role_id] = {'min': data[1],'max': data[2]}
                    else:
                        cache = roles_map[role_id]
                        cache['min'] = min(cache['min'], data[1])
                        cache['max'] = max(cache['max'], data[2])

            replace_map = {}
            for i in range(count):
                event_data = self._show_wait_list[i]
                if i < start_index or event_data['type'] != BOND_LEVEL_UP_TYPE:
                    continue
                role_id = event_data['data'][0]
                if role_id not in replace_map:
                    replace_map[role_id] = 1
                    event_data['data'] = [role_id, roles_map[role_id]['min'], roles_map[role_id]['max']]
                else:
                    self._show_wait_list[i] = None

            self._show_wait_list = list([ _f for _f in self._show_wait_list if _f ])
            return

    def on_bond_level_up_event(self, data):
        event_data = {'type': BOND_LEVEL_UP_TYPE,'data': data}
        if self._is_handling_event():
            self._show_wait_list.append(event_data)
            self.merge_bond_level_up_event()
        else:
            self._show_wait_list.append(event_data)
            self.dispatch_event_data()

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
        import game3d
        if item_utils.get_lobby_item_type(item_no) == L_ITEM_TYPE_WEAPON_SFX:
            from logic.gutils.dress_utils import get_weapon_sfx_skin_show_mount_item_no
            mount_item_no = get_weapon_sfx_skin_show_mount_item_no(item_no)
            if not is_s_skin_that_can_upgrade(mount_item_no):
                anim_name = 'appear_ex'
            else:
                anim_name = 'appear_s_plus'
        else:
            rare_degree = item_utils.get_item_rare_degree(item_no)
            anim_name = RARE_NAME_CONFIG.get(rare_degree, {}).get('anim', None)
        self.panel.PlayAnimation('reset')
        if anim_name:

            def delay_ani():
                if self.panel and self.panel.isValid():
                    self.panel.PlayAnimation(anim_name)

            game3d.delay_exec(500, delay_ani)
        return

    def show_next_model(self, item_no, callback=None, use_pass_anim=False, begin_continue_show=False, extra_info=None):
        self.reset_use_item_state()
        self._showing_item_no = item_no
        item_type = item_utils.get_lobby_item_type(item_no)
        self.hide_main_ui(exceptions=EXCEPT_HIDE_UI_LIST, exception_types=(UI_TYPE_MESSAGE,))
        self.panel.btn_share.setVisible(True and global_data.is_share_show)
        self.panel.lab_title.SetString(get_title_name(item_type, item_no))
        self.panel.lab_title.ChildResizeAndPosition()
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
        if item_type == L_ITEM_TYPE_ROLE:
            self.panel.nd_cv.setVisible(global_data.channel.get_name() not in ('toutiao_sdk', ))
            cv_name = confmgr.get('role_info', 'RoleProfile', 'Content', str(item_no), 'cv_name')
            self.panel.nd_cv.cv_name.SetString(cv_name)
            get_role_music = confmgr.get('role_info', 'RoleInfo', 'Content', str(item_no)).get('get_role_music', None)
            if get_role_music:
                self.music_name = global_data.sound_mgr.get_playing_music()
                global_data.sound_mgr.play_event(str(get_role_music))
        else:
            self.panel.nd_cv.setVisible(False)
        self.update_exclusive_icon(item_no)
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
            for i in range(len(card_list)):
                module_nd = self.panel.module_list.GetItem(i)
                _item_no = get_card_item_no(card_list[i])
                module_nd.img_skill.SetDisplayFrameByPath('', item_utils.get_lobby_item_pic_by_item_no(_item_no))
                self.register_module_info_click(module_nd, _item_no)

        elif item_type in [L_ITEM_TYPE_ROLE, L_ITEM_TYPE_ROLE_SKIN]:
            role_id = confmgr.get('lobby_item', str(item_no), 'belong_id')
            if not role_id:
                role_id = item_no
            dialog_id = bond_utils.get_skin_dialog_id(role_id)
            if dialog_id:
                tips_ui = global_data.ui_mgr.get_ui('RoleBondTipsUI')
                if tips_ui:
                    tips_ui.init_widget(role_id, {'dialog_id': dialog_id})
                else:
                    RoleBondTipsUI(None, role_id, {'dialog_id': dialog_id})
        mecha_items = global_data.player.get_items_by_type(item_type)
        mecha_items = item_utility.filter_default_skin(mecha_items)
        if item_type in [L_ITEM_TYPE_ROLE_SKIN, L_ITEM_TYPE_MECHA_SKIN]:
            rare_degree = item_utils.get_item_rare_degree(item_no)
            degree_name = item_utils.get_rare_degree_name(rare_degree)
            target_skins = item_utility.get_item_rare_degree_count(mecha_items, target_rare_degrees=[rare_degree])
            self._num_text = self._num_text = get_text_by_id(NUM_NAME[item_type], {'num': str(len(target_skins)),'level': degree_name})
        else:
            self._num_text = get_text_by_id(NUM_NAME[item_type], {'num': str(len(mecha_items))})
        self.panel.lab_get_num.SetString(self._num_text)
        self.panel.temp_btn_use.btn_common_big.SetText(BTN_NAME[item_type])

        @self.panel.temp_btn_use.btn_common_big.callback()
        def OnClick(*args):
            self.use_item(item_no)
            self.on_use_item_success()

        mecha_id = confmgr.get('lobby_item', str(item_no), 'belong_id')
        if not mecha_id:
            mecha_id = item_no
        default_sfx = confmgr.get('mecha_conf', 'LobbyMechaConfig', 'Content', str(mecha_id), 'default_sfx')
        item_display_data = confmgr.get('display_enter_effect', 'Content', str(default_sfx), default={})
        callOutSfxPath = item_display_data.get('lobbyCallOutSfxPath', '')
        cSfxSoundName = item_display_data.get('cSfxSoundName', '')

        def on_finish_create_model(model, *args):
            if not self._is_model_unready:
                return
            else:
                rare_degree = item_utils.get_item_rare_degree(item_no)
                if rare_degree in (RARE_DEGREE_4, RARE_DEGREE_5, RARE_DEGREE_6, RARE_DEGREE_7):
                    if item_type in (L_ITEM_TYPE_ROLE, L_ITEM_TYPE_ROLE_SKIN, L_ITEM_TYPE_HEAD, L_ITEM_TYPE_BODY, L_ITEM_TYPE_SUIT, L_ITEM_TYPE_PET_SKIN):
                        sfx_path = ''
                        socket_name = 'fx_root'
                    else:
                        if rare_degree == RARE_DEGREE_4:
                            sfx_path = 'effect/fx/niudan/caidan_jinse_zhanshi.sfx'
                        else:
                            sfx_path = 'effect/fx/niudan/caidan_jinse_zhanshi.sfx'
                        socket_name = 'fx_zhaohuan'
                    if sfx_path and int(mecha_id) not in IGNORE_SFX_MECHA_IDS and int(item_no) not in IGNORE_SFX_ITEM_IDS:
                        self._zhaohuan_sfx_id = global_data.sfx_mgr.create_sfx_on_model(sfx_path, model, socket_name)
                    global_data.sound_mgr.play_ui_sound('luckball_show')
                elif callOutSfxPath:
                    if model:
                        model.visible = False
                    global_data.emgr.change_model_preview_effect.emit(callOutSfxPath, cSfxSoundName)
                    if cSfxSoundName:
                        global_data.sound_mgr.play_ui_sound(cSfxSoundName)
                self._is_model_unready = False
                if self._need_model_share:
                    self._need_model_share = False
                    self.on_click_share(None, None)
                return

        if not begin_continue_show:
            self.enter_show_camera_scene()
        if extra_info:
            show_only = extra_info.get('show_only', None)
            if show_only is not None:
                self.set_show_only(show_only)
        else:
            self.set_show_only(False)

        def begin_model_show--- This code section failed: ---

 673       0  LOAD_DEREF            0  'begin_continue_show'
           3  POP_JUMP_IF_FALSE    19  'to 19'

 674       6  LOAD_DEREF            1  'self'
           9  LOAD_ATTR             0  'enter_show_camera_scene'
          12  CALL_FUNCTION_0       0 
          15  POP_TOP          
          16  JUMP_FORWARD          0  'to 19'
        19_0  COME_FROM                '16'

 676      19  LOAD_GLOBAL           1  'global_data'
          22  LOAD_ATTR             2  'sfx_mgr'
          25  LOAD_ATTR             3  'create_sfx_in_scene'
          28  LOAD_CONST            1  'effect/fx/niudan/caidan_jinse_zhanshi_02.sfx'
          31  CALL_FUNCTION_1       1 
          34  LOAD_DEREF            1  'self'
          37  STORE_ATTR            4  '_blink_sfx_id'

 677      40  LOAD_GLOBAL           1  'global_data'
          43  LOAD_ATTR             5  'player'
          46  LOAD_ATTR             6  'trigger_delay_notice_by_item_no'
          49  LOAD_DEREF            2  'item_no'
          52  CALL_FUNCTION_1       1 
          55  POP_TOP          

 679      56  LOAD_DEREF            3  'item_type'
          59  LOAD_GLOBAL           7  'L_ITEM_TYPE_HEAD'
          62  LOAD_GLOBAL           8  'L_ITEM_TYPE_BODY'
          65  LOAD_GLOBAL           9  'L_ITEM_TYPE_SUIT'
          68  BUILD_TUPLE_3         3 
          71  COMPARE_OP            6  'in'
          74  POP_JUMP_IF_FALSE    95  'to 95'

 680      77  LOAD_GLOBAL          10  'lobby_model_display_utils'
          80  LOAD_ATTR            11  'get_pendant_show_data'
          83  LOAD_DEREF            2  'item_no'
          86  CALL_FUNCTION_1       1 
          89  STORE_FAST            0  'model_data'
          92  JUMP_FORWARD        265  'to 360'

 682      95  LOAD_CONST            2  ''
          98  LOAD_CONST            3  ('FASHION_POS_SUIT', 'FASHION_POS_HEADWEAR', 'FASHION_POS_BACK', 'FASHION_POS_SUIT_2', 'FASHION_OTHER_PENDANT_LIST')
         101  IMPORT_NAME          12  'logic.gcommon.item.item_const'
         104  IMPORT_FROM          13  'FASHION_POS_SUIT'
         107  STORE_FAST            1  'FASHION_POS_SUIT'
         110  IMPORT_FROM          14  'FASHION_POS_HEADWEAR'
         113  STORE_FAST            2  'FASHION_POS_HEADWEAR'
         116  IMPORT_FROM          15  'FASHION_POS_BACK'
         119  STORE_FAST            3  'FASHION_POS_BACK'
         122  IMPORT_FROM          16  'FASHION_POS_SUIT_2'
         125  STORE_FAST            4  'FASHION_POS_SUIT_2'
         128  IMPORT_FROM          17  'FASHION_OTHER_PENDANT_LIST'
         131  STORE_FAST            5  'FASHION_OTHER_PENDANT_LIST'
         134  POP_TOP          

 684     135  LOAD_GLOBAL          18  'get_skin_default_wear_decoration_dict'
         138  LOAD_DEREF            2  'item_no'
         141  LOAD_DEREF            2  'item_no'
         144  CALL_FUNCTION_2       2 
         147  STORE_FAST            6  'default_wear_dict'

 685     150  LOAD_FAST             6  'default_wear_dict'
         153  LOAD_ATTR            19  'get'
         156  LOAD_FAST             2  'FASHION_POS_HEADWEAR'
         159  CALL_FUNCTION_1       1 
         162  STORE_FAST            7  'head_id'

 686     165  LOAD_FAST             6  'default_wear_dict'
         168  LOAD_ATTR            19  'get'
         171  LOAD_FAST             3  'FASHION_POS_BACK'
         174  CALL_FUNCTION_1       1 
         177  STORE_FAST            8  'bag_id'

 687     180  LOAD_FAST             6  'default_wear_dict'
         183  LOAD_ATTR            19  'get'
         186  LOAD_FAST             4  'FASHION_POS_SUIT_2'
         189  CALL_FUNCTION_1       1 
         192  STORE_FAST            9  'suit_id'

 688     195  BUILD_LIST_0          0 
         198  LOAD_FAST             5  'FASHION_OTHER_PENDANT_LIST'
         201  GET_ITER         
         202  FOR_ITER             21  'to 226'
         205  STORE_FAST           10  'pos'
         208  LOAD_FAST             6  'default_wear_dict'
         211  LOAD_ATTR            19  'get'
         214  LOAD_FAST            10  'pos'
         217  CALL_FUNCTION_1       1 
         220  LIST_APPEND           2  ''
         223  JUMP_BACK           202  'to 202'
         226  STORE_FAST           11  'other_pendants'

 689     229  LOAD_GLOBAL          10  'lobby_model_display_utils'
         232  LOAD_ATTR            20  'get_lobby_model_data'

 690     235  LOAD_DEREF            2  'item_no'
         238  LOAD_GLOBAL          21  'True'
         241  LOAD_CONST            4  'head_id'
         244  LOAD_FAST             7  'head_id'
         247  LOAD_CONST            5  'bag_id'
         250  LOAD_FAST             8  'bag_id'
         253  LOAD_CONST            6  'suit_id'
         256  LOAD_FAST             9  'suit_id'
         259  LOAD_CONST            7  'other_pendants'
         262  LOAD_FAST            11  'other_pendants'
         265  CALL_FUNCTION_1026  1026 
         268  STORE_FAST            0  'model_data'

 691     271  LOAD_DEREF            3  'item_type'
         274  LOAD_GLOBAL          22  'L_ITEM_TYPE_WEAPON_SFX'
         277  COMPARE_OP            2  '=='
         280  POP_JUMP_IF_FALSE   333  'to 333'

 692     283  LOAD_DEREF            2  'item_no'
         286  STORE_FAST           12  'shiny_weapon_id'

 693     289  SETUP_LOOP           68  'to 360'
         292  LOAD_FAST             0  'model_data'
         295  GET_ITER         
         296  FOR_ITER             30  'to 329'
         299  STORE_FAST           13  'data'

 694     302  LOAD_FAST            13  'data'
         305  LOAD_CONST            8  'item_no'
         308  BINARY_SUBSCR    
         309  LOAD_FAST            13  'data'
         312  LOAD_CONST            9  'skin_id'
         315  STORE_SUBSCR     

 695     316  LOAD_FAST            12  'shiny_weapon_id'
         319  LOAD_FAST            13  'data'
         322  LOAD_CONST           10  'shiny_weapon_id'
         325  STORE_SUBSCR     
         326  JUMP_BACK           296  'to 296'
         329  POP_BLOCK        
       330_0  COME_FROM                '289'
         330  JUMP_FORWARD         27  'to 360'

 697     333  SETUP_LOOP           24  'to 360'
         336  LOAD_FAST             0  'model_data'
         339  GET_ITER         
         340  FOR_ITER             16  'to 359'
         343  STORE_FAST           13  'data'

 698     346  LOAD_DEREF            2  'item_no'
         349  LOAD_FAST            13  'data'
         352  LOAD_CONST            9  'skin_id'
         355  STORE_SUBSCR     
         356  JUMP_BACK           340  'to 340'
         359  POP_BLOCK        
       360_0  COME_FROM                '333'
       360_1  COME_FROM                '289'
       360_2  COME_FROM                '92'

 700     360  LOAD_DEREF            3  'item_type'
         363  LOAD_GLOBAL          23  'L_ITEM_TYPE_PET_SKIN'
         366  COMPARE_OP            2  '=='
         369  POP_JUMP_IF_FALSE   411  'to 411'

 702     372  SETUP_LOOP           36  'to 411'
         375  LOAD_FAST             0  'model_data'
         378  GET_ITER         
         379  FOR_ITER             25  'to 407'
         382  STORE_FAST           13  'data'

 703     385  LOAD_CONST            2  ''
         388  LOAD_CONST           11  10
         391  LOAD_CONST            2  ''
         394  BUILD_LIST_3          3 
         397  LOAD_FAST            13  'data'
         400  LOAD_CONST           12  'off_position'
         403  STORE_SUBSCR     
         404  JUMP_BACK           379  'to 379'
         407  POP_BLOCK        
       408_0  COME_FROM                '372'
         408  JUMP_FORWARD          0  'to 411'
       411_0  COME_FROM                '372'

 704     411  LOAD_GLOBAL           1  'global_data'
         414  LOAD_ATTR            24  'emgr'
         417  LOAD_ATTR            25  'shutdown_box_opened_sfx'
         420  LOAD_ATTR            26  'emit'
         423  CALL_FUNCTION_0       0 
         426  POP_TOP          

 705     427  LOAD_GLOBAL          21  'True'
         430  LOAD_DEREF            1  'self'
         433  STORE_ATTR           27  '_is_model_unready'

 706     436  LOAD_GLOBAL           1  'global_data'
         439  LOAD_ATTR            24  'emgr'
         442  LOAD_ATTR            28  'change_model_display_scene_item'
         445  LOAD_ATTR            26  'emit'
         448  LOAD_ATTR            13  'FASHION_POS_SUIT'
         451  LOAD_DEREF            4  'on_finish_create_model'
         454  LOAD_CONST           14  'model_control_type'
         457  LOAD_GLOBAL          29  'lobby_model_display_const'
         460  LOAD_ATTR            30  'CT_GET_MODEL_DISPLAY'
         463  CALL_FUNCTION_513   513 
         466  POP_TOP          

 707     467  LOAD_GLOBAL           1  'global_data'
         470  LOAD_ATTR            24  'emgr'
         473  LOAD_ATTR            31  'change_model_display_control_type'
         476  LOAD_ATTR            26  'emit'
         479  LOAD_GLOBAL          29  'lobby_model_display_const'
         482  LOAD_ATTR            30  'CT_GET_MODEL_DISPLAY'
         485  CALL_FUNCTION_1       1 
         488  POP_TOP          

 708     489  LOAD_DEREF            1  'self'
         492  LOAD_ATTR            32  'panel'
         495  LOAD_ATTR            33  'PlayAnimation'
         498  LOAD_CONST           15  'appear'
         501  CALL_FUNCTION_1       1 
         504  POP_TOP          

 709     505  LOAD_DEREF            5  'callback'
         508  POP_JUMP_IF_FALSE   535  'to 535'
         511  LOAD_GLOBAL          34  'callable'
         514  LOAD_DEREF            5  'callback'
         517  CALL_FUNCTION_1       1 
       520_0  COME_FROM                '508'
         520  POP_JUMP_IF_FALSE   535  'to 535'

 710     523  LOAD_DEREF            5  'callback'
         526  LOAD_DEREF            1  'self'
         529  STORE_ATTR           35  'close_callback'
         532  JUMP_FORWARD          0  'to 535'
       535_0  COME_FROM                '532'

 711     535  LOAD_DEREF            1  'self'
         538  LOAD_ATTR            36  'show'
         541  CALL_FUNCTION_0       0 
         544  POP_TOP          

 712     545  LOAD_DEREF            1  'self'
         548  LOAD_ATTR            32  'panel'
         551  LOAD_ATTR            37  'temp_btn_close'
         554  LOAD_ATTR            38  'btn_back'
         557  LOAD_ATTR            39  'SetEnable'
         560  LOAD_GLOBAL          21  'True'
         563  CALL_FUNCTION_1       1 
         566  POP_TOP          

Parse error at or near `CALL_FUNCTION_513' instruction at offset 463

        if use_pass_anim:

            def show_pass_anim():
                self.panel.temp_btn_close.btn_back.SetEnable(False)
                transition_ui = global_data.ui_mgr.get_ui('GetModelDisplayBeforeUI')
                if not transition_ui:
                    from logic.comsys.mall_ui.GetModelDisplayBeforeUI import GetModelDisplayBeforeUI
                    transition_ui = GetModelDisplayBeforeUI()
                transition_ui.show_transition(begin_model_show)

            show_pass_anim()
        else:
            begin_model_show()
        return

    def enter_show_camera_scene(self):
        from logic.gcommon.common_const import scene_const
        global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_JIEMIAN_COMMON, lobby_model_display_const.DEFAULT_MID, scene_content_type=scene_const.SCENE_GET_MODEL_DISPLAY)

    def register_module_info_click(self, module_nd, item_no):
        if item_no:

            @module_nd.unique_callback()
            def OnClick(layer, touch, *args):
                position = touch.getLocation()
                global_data.emgr.show_item_desc_ui_event.emit(item_no, None, directly_world_pos=position)
                return

    def share_switch_to_kv(self, is_to_kv):
        from logic.gutils.share_utils import on_share_switch_to_kv
        on_share_switch_to_kv(self._share_content_kv, self._screen_capture_helper, is_to_kv)

    def on_click_share(self, btn, touch):
        if self._is_model_unready:
            self._need_model_share = True
            return
        else:
            if not (self.panel and self.panel.isValid()):
                return
            from logic.gutils.dress_utils import mecha_lobby_id_2_battle_id
            from logic.gutils.item_utils import get_lobby_item_type, get_lobby_item_belong_no
            from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_MECHA_SKIN, L_ITEM_TYPE_MECHA
            item_type = item_utils.get_lobby_item_type(self._showing_item_no)
            from logic.gutils.share_utils import get_share_bg_path, is_mecha_id_can_show_kv
            share_spec = confmgr.get('c_share_item_conf', str(self._showing_item_no), default={})
            bEnableScreenShot = share_spec.get('bEnableScreenShot')
            share_bg_path = None
            if item_type == L_ITEM_TYPE_MECHA or item_utils.is_default_skin(self._showing_item_no):
                if item_type == L_ITEM_TYPE_MECHA_SKIN:
                    belong_id = get_lobby_item_belong_no(self._showing_item_no)
                else:
                    belong_id = self._showing_item_no
                kv_id = mecha_lobby_id_2_battle_id(belong_id)
                is_can_show = is_mecha_id_can_show_kv(kv_id)
                if is_can_show:
                    share_bg_path = get_share_bg_path(self._showing_item_no)
                else:
                    share_bg_path = ''
            share_role_bg_path = None
            if item_type == L_ITEM_TYPE_ROLE or item_utils.is_default_skin(self._showing_item_no):
                if item_type != L_ITEM_TYPE_ROLE:
                    belong_id = get_lobby_item_belong_no(self._showing_item_no)
                    role_kv_id = mecha_lobby_id_2_battle_id(belong_id)
                else:
                    role_kv_id = self._showing_item_no
                share_role_bg_path = get_share_bg_path(role_kv_id)
            show_kv = bool(share_bg_path or share_role_bg_path) or bEnableScreenShot
            delay_time = 0.001
            ui_names = [
             self.__class__.__name__, 'OpenBoxUI']
            self.check_share_anim()
            self.use_item(self._showing_item_no, is_share=True)
            if share_spec and bEnableScreenShot or not share_spec:
                if self._screen_capture_helper:
                    old_vis = self.panel.lab_get_num.isVisible()
                    old_module = self.panel.nd_module.isVisible()

                    def custom_cb(*args):
                        if show_kv:
                            from logic.comsys.share.ShareUI import ShareUI
                            share_ui = ShareUI()
                        ui = global_data.ui_mgr.get_ui('ShareUI')
                        if ui:
                            ui.clear_choose_list_func()
                        if show_kv:
                            if not self._share_content_kv:
                                from logic.comsys.share.ItemInfoShareCreator import ItemInfoShareCreator
                                share_creator = ItemInfoShareCreator()
                                share_creator.create()
                                self._share_content_kv = share_creator
                            if self._share_content_kv:
                                kv_path = get_share_bg_path(self._showing_item_no)
                                self._share_content_kv.get_ui_bg_sprite().SetDisplayFrameByPath('', kv_path, force_sync=True)
                                self._share_content_kv.show_share_detail(self._showing_item_no)
                                self._share_content_kv.set_show_record(False)
                            check_add_shareui_battle_record_func(self._showing_item_no, False, self._share_content_kv, self._screen_capture_helper)
                            if item_type not in [L_ITEM_TYPE_MECHA, L_ITEM_TYPE_MECHA]:
                                check_add_shareui_kv_func(lambda is_to_kv: self.share_switch_to_kv(is_to_kv), True)
                                self.share_switch_to_kv(True)
                            else:
                                check_add_shareui_kv_func(lambda is_to_kv: self.share_switch_to_kv(is_to_kv), False)
                                self.share_switch_to_kv(False)
                        else:
                            check_add_shareui_battle_record_func(self._showing_item_no, False, None, self._screen_capture_helper)
                        self.panel.temp_btn_close.setVisible(True)
                        self.panel.btn_share.setVisible(True and global_data.is_share_show)
                        self.panel.lab_get_num.setVisible(old_vis)
                        self.panel.nd_content.setVisible(True)
                        self.panel.nd_module.setVisible(old_module)
                        if global_data.ui_mgr.get_ui('SkinDefineUI'):
                            self.panel.temp_btn_use.setVisible(False)
                        else:
                            self.panel.temp_btn_use.setVisible(True)
                        return

                    self.panel.lab_get_num.setVisible(False)
                    self.panel.nd_content.setVisible(False)
                    self.panel.temp_btn_close.setVisible(False)
                    self.panel.btn_share.setVisible(False)
                    self.panel.temp_btn_use.setVisible(False)
                    self.panel.nd_module.setVisible(False)
                    if self._blink_sfx_id:
                        global_data.sfx_mgr.shutdown_sfx_by_id(self._blink_sfx_id)
                        self._blink_sfx_id = None
                    if self._zhaohuan_sfx_id:
                        sfx = global_data.sfx_mgr.get_sfx_by_id(self._zhaohuan_sfx_id)
                        if sfx and sfx.valid:
                            if sfx.cur_time < CAIDAN_JINSE_ZHANSHI_SHADER_CONTROL_END_TIME:
                                sfx.set_curtime_directly(CAIDAN_JINSE_ZHANSHI_SHADER_CONTROL_END_TIME)
                    item_display_data = confmgr.get('display_enter_effect', 'Content', str(self._showing_item_no), default={})
                    callOutSfxPath = item_display_data.get('lobbyCallOutSfxPath', '')
                    if callOutSfxPath:
                        global_data.emgr.clear_enter_display_sfx.emit()

                def func():
                    if self.panel and self.panel.isValid() and self.panel.IsVisible():
                        self._screen_capture_helper.take_screen_shot(ui_names, self.panel, custom_cb=custom_cb, head_nd_name='nd_player_info_1', item_detail_no=self._showing_item_no, need_share_ui=not show_kv, FastForwardAnim=True, need_draw_rt=not show_kv)

                self.panel.DelayCall(delay_time, func)
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
                bEnableShareDetails = share_spec.get('bEnableShareDetails', True)
                if bEnableShareDetails:
                    self._share_content.show_share_detail(self._showing_item_no)
                from logic.comsys.share.ShareUI import ShareUI
                ShareUI(parent=self.panel).set_share_content_raw(self._share_content.get_render_texture(), share_content=self._share_content)
                ui = global_data.ui_mgr.get_ui('ShareUI')
                ui.set_hide_main_ui()
                check_add_shareui_battle_record_func(self._showing_item_no, False, self._share_content, None)
            return

    def check_share_anim(self):
        model_conf = confmgr.get('c_share_model_conf', str(self._showing_item_no), default={})
        if not model_conf:
            model_conf = confmgr.get('c_share_model_conf', str(item_utils.get_lobby_item_belong_no(self._showing_item_no)), default={})
        anim = model_conf.get('cAnim')
        if anim:
            anim_name = anim[0]
            animation_args = anim[1:]
            global_data.emgr.change_model_display_anim_directly.emit(anim_name, -1, anim_arg=animation_args, is_back_to_end_show_anim=True)
            self._is_in_share_anim = True
        else:
            model_data = lobby_model_display_utils.get_lobby_model_data(self._showing_item_no)
            for data in model_data:
                end_anim = data['end_anim']
                anim_name = end_anim
                init_time = 10000
                global_data.emgr.change_model_display_anim_directly.emit(anim_name, -1, anim_arg=[
                 0, -1, init_time, 0, 1.0], is_back_to_end_show_anim=True)

    def set_show_only(self, hide_extra_btns):
        is_vis = not hide_extra_btns
        self.panel.nd_use.setVisible(is_vis)
        self.panel.btn_share.setVisible(is_vis)
        self.panel.lab_get_num.setVisible(is_vis)
        self.panel.lab_get_num.setVisible(is_vis)
        self.panel.sp_smc.setVisible(is_vis)

    def on_ui_close(self, uiname):
        if uiname == 'ShareUI':
            if self._is_in_share_anim:
                model_data = lobby_model_display_utils.get_lobby_model_data(self._showing_item_no)
                for data in model_data:
                    first_ani = data['mecha_end_ani']
                    anim_name = first_ani
                    global_data.emgr.change_model_display_anim_directly.emit(anim_name, -1, anim_arg=[
                     0, -1, 0, 0, 1.0], is_back_to_end_show_anim=True)

                self._is_in_share_anim = False

    def use_item(self, item_no, is_share=False):
        item_type = item_utils.get_lobby_item_type(item_no)
        if item_type == L_ITEM_TYPE_ROLE:
            global_data.player.try_set_role(item_no)
        elif item_type == L_ITEM_TYPE_MECHA:
            mecha_id = mecha_lobby_id_2_battle_id(item_no)
            global_data.player.req_change_lobby_mecha(mecha_id)
        elif item_type == L_ITEM_TYPE_ROLE_SKIN:
            global_data.player.dress_role_top_skin_fashion(item_no)
            self.confirm_use_role(item_no, is_share=is_share)
        elif item_type == L_ITEM_TYPE_MECHA_SKIN:
            mecha_lobby_id = item_utils.get_lobby_item_belong_no(item_no)
            mecha_battle_id = mecha_lobby_id_2_battle_id(mecha_lobby_id)
            main_skin_id = get_main_skin_id(item_no)
            global_data.player.install_mecha_main_skin_scheme(mecha_battle_id, main_skin_id, {FASHION_POS_SUIT: item_no})
            self.confirm_display_mecha(item_no, is_share=is_share)
        elif item_type == L_ITEM_TYPE_PET_SKIN:
            base_skin = confmgr.get('c_pet_info', str(item_no), 'base_skin', default=item_no)
            if str(base_skin) == str(item_no):
                global_data.player.set_choosen_pet(item_no)
            else:
                global_data.player.set_pet_sub_skin(item_no)
        if item_type in [L_ITEM_TYPE_ROLE, L_ITEM_TYPE_ROLE_SKIN, L_ITEM_TYPE_MECHA_SKIN]:
            show_new = global_data.lobby_red_point_data.get_rp_by_no(item_no)
            if show_new:
                global_data.player.req_del_item_redpoint(item_no)

    def reset_use_item_state(self):
        self._is_used = False
        self.panel.temp_btn_use.setVisible(True)
        self.panel.btn_share.btn_common_big.SetText(633911)

    def on_use_item_success(self):
        self.panel.temp_btn_use.setVisible(False)
        self.confirm_use_mecha_role()
        if self._is_used:
            return
        if self._showing_item_no:
            global_data.game_mgr.show_tip(633912)
        self._is_used = True
        self.panel.btn_share.btn_common_big.SetText(3155)

    def confirm_use_mecha_role(self):
        item_type = item_utils.get_lobby_item_type(self._showing_item_no)
        if item_type == L_ITEM_TYPE_ROLE_SKIN:
            self.confirm_use_role(self._showing_item_no)
        elif item_type == L_ITEM_TYPE_MECHA_SKIN:
            self.confirm_display_mecha(self._showing_item_no)

    def confirm_use_role(self, item_no, is_share=False):
        if is_share:
            return
        cur_role_id = global_data.player.get_role()
        belong_no = item_utils.get_lobby_item_belong_no(item_no)
        has_role = global_data.player.get_item_by_no(belong_no)
        if has_role and cur_role_id != belong_no:

            def set_role(role=belong_no):
                global_data.player.try_set_role(role)

            SecondConfirmDlg2().confirm(content=get_text_by_id(634056).format(driver_name=item_utils.get_lobby_item_name(belong_no)), confirm_callback=set_role)

    def confirm_display_mecha(self, item_no, is_share=False):
        if is_share:
            return
        cur_mecha_item_id = global_data.player.get_lobby_selected_mecha_item_id()
        belong_no = item_utils.get_lobby_item_belong_no(item_no)
        has_mecha = global_data.player.get_item_by_no(belong_no)
        if has_mecha and cur_mecha_item_id != belong_no:

            def set_mecha(mecha=dress_utils.mecha_lobby_id_2_battle_id(belong_no)):
                global_data.player.req_change_lobby_mecha(mecha)

            SecondConfirmDlg2().confirm(content=get_text_by_id(634057).format(mecha_name=item_utils.get_lobby_item_name(belong_no)), confirm_callback=set_mecha)