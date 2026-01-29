# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_display/MechaDetails.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
import cc
import game3d
import math3d
import logic.gcommon.const as gconst
from common.cfg import confmgr
from common.uisys.basepanel import BasePanel
from common.const.uiconst import UI_TYPE_MESSAGE
from common.const.uiconst import NORMAL_LAYER_ZORDER
from logic.client.const import lobby_model_display_const
from logic.gcommon.item import lobby_item_type
from logic.gcommon.common_const import mecha_const
from logic.gcommon.common_const import scene_const
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.comsys.mall_ui.PriceUIWidget import PriceUIWidget
from logic.comsys.mecha_display.MechaLobbyModuleWidget import MechaLobbyModuleWidget
from logic.gutils import item_utils
from logic.gutils import dress_utils
from logic.gutils import jump_to_ui_utils
from logic.gutils import mecha_skin_utils
from logic.gutils import lobby_model_display_utils
from logic.gutils.dress_utils import battle_id_to_mecha_lobby_id
from logic.gutils import template_utils
from logic.client.const.lobby_model_display_const import CAM_MODE_NEAR, CAM_MODE_FAR, ROTATE_FACTOR
from logic.vscene.parts.camera.CameraTrkPlayer import CameraTrkPlayer
from logic.gutils.reinforce_card_utils import get_card_item_no
from common.const import uiconst
from logic.gutils.skin_define_utils import get_main_skin_id
from logic.gutils import mall_utils
from logic.gutils import red_point_utils
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_MECHA_SKIN
from logic.gutils.share_utils import get_share_bg_path, on_share_switch_to_kv, is_mecha_id_can_show_kv, check_add_shareui_battle_record_func, check_add_shareui_kv_func, check_add_shareui_ex_privilege_func
from logic.gutils.video_utils import check_play_chuchang_video, get_relative_video_skin_list, get_chuchang_video_path
from logic.gutils.screen_effect_utils import create_screen_effect_directly
from logic.comsys.share.ShareTemplateBase import async_disable_wrapper
from logic.comsys.common_ui.MechaPreviewAdvancedAppearanceWidget import MechaPreviewAdvancedAppearanceWidget
from logic.gutils.mecha_utils import get_ex_skin_improve_item_no
import copy
import time
CLICK_BTN_INTERVAL_TIME = 0.5
ICON_PREFIX = 'gui/ui_res_2/battle/mech_main/'
_HASH_DIFFUSE = game3d.calc_string_hash('Tex0')
MECHA_VIEW_MODEL = 0
MECHA_VIEW_PIC = 1
PIC_TEXT_ID = 80820
MODULE_TEXT_ID = 2221
OFF_POSITION = [
 -8, 0, 0]
from logic.comsys.mecha_display.AnimDisplayChangeWidget import AnimDisplayChangeWidget

def disable_on_puppet(func):

    def inner(self, *args, **kwargs):
        if not self._is_for_puppet:
            return func(self, *args, **kwargs)
        else:
            return None
            return None

    return inner


class MechaDetails(BasePanel):
    PANEL_CONFIG_NAME = 'mech_display/mech_main_new'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE_BY_DEFAULT_FUNC_NAME
    OPEN_SOUND_NAME = 'ui_mecha_zoom_in'
    HOT_KEY_NEED_SCROLL_SUPPORT = True
    NEED_SCROLL_ALWAYS = True
    CAM_SCALE_MOUSE_SEN_FACTOR = 60.0
    CAM_SCALE_TOUCH_SEN_FACTOR = 4.0
    UI_ACTION_EVENT = {'nd_mech_touch.OnBegin': '_on_rotate_drag_begin',
       'nd_mech_touch.OnDrag': '_on_rotate_drag',
       'nd_mech_touch.OnEnd': '_on_rotate_drag_end',
       'temp_btn_back.btn_back.OnClick': '_on_click_back_btn',
       'nd_btn_mech_change.btn_last_mech.OnClick': '_on_show_last_mecha',
       'nd_btn_mech_change.btn_next_mech.OnClick': '_on_show_next_mecha',
       'temp_btn_use.btn_common.OnClick': '_on_click_btn_use_mecha',
       'btn_more.OnClick': 'on_click_btn_more',
       'btn_change.OnClick': 'on_click_change',
       'btn_left.OnClick': '_on_click_btn_left',
       'btn_teach.OnClick': '_on_click_mecha_video',
       'btn_pic.OnClick': '_on_click_change_view_type'
       }
    GLOBAL_EVENT = {'player_item_update_event': '_on_buy_good_success',
       'on_lobby_mecha_changed': 'change_lobby_mecha',
       'show_to_gain_method_page_event': 'show_to_gain_method_page',
       'update_proficiency_reward_event': 'refresh_mecha_red_dot',
       'refresh_item_red_point': 'on_refresh_item_red_point',
       'change_mecha_view_type': 'switch_view_type',
       'change_mecha_view_zoom': '_on_change_mecha_view_zoom',
       'fold_mecha_details_widget': '_on_fold_mecha_details_widget'
       }

    def __init__(self):
        self._video_path = None
        super(MechaDetails, self).__init__()
        return

    def on_init_panel(self, *args, **kwargs):
        self.init_param()
        self.anim_display_change_widget = AnimDisplayChangeWidget(self.panel, self.panel.btn_change)
        self.mecha_preview_advnaced_appearance_widget = MechaPreviewAdvancedAppearanceWidget(self, self.panel.btn_splus_ex, True)
        self.hide_main_ui(exception_types=(UI_TYPE_MESSAGE,))
        self.init_parameters()
        self.init_tab_list()
        self.init_open_lst()
        self.reset_left_bottom_btn_position()
        self._is_for_puppet = False
        self._share_content = None

        @self.panel.nd_list_close.callback()
        def OnClick(*args):
            self.panel.nd_more.setVisible(False)

        self.panel.temp_btn_back.btn_back.set_click_sound_name('ui_click_mecha_back')
        self.price_top_widget = PriceUIWidget(self, list_money_node=self.panel.list_price)
        self.panel.PlayAnimation('appear')
        self._check_ext_tips()
        self.panel.btn_more.setVisible(False)
        return

    def on_finalize_panel(self):
        self.tab_list_data = []
        self._mecha_info_conf = None
        self._mecha_skin_conf = None
        self._mecha_conf = None
        self._skill_conf = None
        self._cur_select_mecha_effect_id = None
        self.destroy_widget('widgets_helper')
        self.destroy_widget('left_tab_list')
        self.destroy_widget('anim_display_change_widget')
        self.destroy_widget('mecha_preview_advnaced_appearance_widget')
        self.destroy_widget('_ext_tip_widget')
        if self._trk_player:
            self._trk_player.on_exit()
            self._trk_player = None
        self.price_top_widget and self.price_top_widget.on_finalize_panel()
        self.price_top_widget = None
        global_data.emgr.close_model_display_scene.emit()
        global_data.emgr.leave_current_scene.emit()
        global_data.emgr.reset_rotate_model_display.emit()
        if self._screen_capture_helper:
            self._screen_capture_helper.destroy()
            self._screen_capture_helper = None
        if self._share_content:
            self._share_content.destroy()
            self._share_content = None
        if self._share_content_kv:
            self._share_content_kv.destroy()
            self._share_content_kv = None
        self.show_main_ui()
        if self.screen_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.screen_sfx_id)
            self.screen_sfx_id = None
        self.execute_action_queue = []
        global_data.emgr.set_last_chuchang_id.emit(None)
        global_data.emgr.forbid_mecha_chuchang_scene.emit(False)
        if global_data.video_player.video_name == self._video_path:
            global_data.video_player.stop_video()
        return

    def set_is_for_puppet(self):
        self._is_for_puppet = True

    def on_resolution_changed(self):
        cur_index = self.widgets_helper.get_cur_index()
        if self.BASIC_INFO_WIDGET_IND == cur_index:
            self.is_fold = not self.is_fold
            self._on_fold_mecha_details_widget(is_slerp=False)
            self.widgets_helper.get_widget_by_index(cur_index).on_resolution_changed()
        else:
            self.panel.PlayAnimation('appear')
        self.reset_left_bottom_btn_position()

    def init_open_lst(self):
        if not global_data.player:
            self.close()
            return
        mecha_open_info = global_data.player.read_mecha_open_info()
        if mecha_open_info['opened_order']:
            self._open_mecha_lst = mecha_open_info['opened_order']

    def init_parameters(self):
        self.is_fold = False
        self.BASIC_INFO_WIDGET_IND = 0
        self.SKILL_WIDGET_IND = 1
        self.STORY_WIDGET_IND = 2
        self.MODULE_WIDGET_IND = 3
        self.MEMORY_WIDGET_IND = 4
        self._display_model_info = None
        self.tab_list_data = [
         {'text': 81356,
            'widget_func': self.init_mecha_basic_widget,
            'widget_template': 'mech_display/i_mech_info_basic',
            'red_point_func': self.basic_red_point_check_func
            },
         {'text': 81357,
            'widget_func': self.init_mecha_skill_widget,
            'widget_template': 'mech_display/i_mech_info_ability'
            },
         {'text': 80799,
            'widget_func': self.init_mecha_story,
            'widget_template': 'mech_display/i_mech_info_story'
            },
         {'text': 81874,
            'widget_func': self.init_mecha_module_widget,
            'widget_template': 'mech_display/i_mech_info_module'
            },
         {'text': 81607,
            'widget_func': self.init_mecha_career_widget,
            'widget_template': 'mech_display/career/i_mech_career_info'
            }]
        self.basic_widget_index = 0
        self.execute_action_queue = []
        self._video_path = None
        return

    def init_tab_list(self):
        from logic.comsys.common_ui.WidgetCommonComponent import WidgetCommonComponent

        def tab_sel_func(index):
            if index == self.MODULE_WIDGET_IND:
                jump_to_ui_utils.jump_to_mecha_module(self._cur_mecha_id)
                return
            self.switch_to_tab(index)
            return True

        self.widgets_helper = WidgetCommonComponent(self.panel.temp_content, self.tab_list_data)
        self.widgets_helper.set_widget_switch_func(self.on_widget_switch)
        from logic.gutils.new_template_utils import CommonLeftTabList

        def return_func():
            self.on_click_close_btn()

        self.left_tab_list = CommonLeftTabList(self.panel.tab_list, self.tab_list_data, return_func, tab_sel_func)

    def init_mecha_basic_widget(self, nd):
        from logic.comsys.mecha_display.MechaBasicInfoWidget import MechaBasicInfoWidget
        return MechaBasicInfoWidget(self, nd)

    def init_mecha_story(self, nd):
        from logic.comsys.mecha_display.MechaStoryWidget import MechaStoryWidget
        return MechaStoryWidget(self, nd, self._cur_mecha_id)

    def init_mecha_module_widget(self, nd):
        widget = MechaLobbyModuleWidget(self, nd, self._cur_mecha_id)
        widget.init_widget(self._cur_mecha_id)
        return widget

    def init_mecha_career_widget(self, nd):
        from logic.comsys.mecha_display.mecha_memory.MechaMemoryWidget import MechaMemoryWidget
        widget = MechaMemoryWidget(self, nd, self._cur_mecha_id)
        return widget

    def init_mecha_skill_widget(self, nd):
        from logic.comsys.mecha_display.MechaSkillInfoWidget import MechaSkillInfoWidget
        inst = MechaSkillInfoWidget(self, nd, self._cur_mecha_id)
        return inst

    def on_click_back_btn(self, btn, touch):
        global_data.emgr.close_model_display_scene.emit()
        global_data.emgr.leave_current_scene.emit()
        self.on_click_close_btn()

    def on_click_close_btn(self):
        self.close()

    def _on_rotate_drag_begin(self, layer, touch):
        if len(self._nd_touch_IDs) >= 2:
            return False
        tid = touch.getId()
        touch_wpos = touch.getLocation()
        if tid not in self._nd_touch_IDs:
            self._nd_touch_poses[tid] = touch_wpos
            self._nd_touch_IDs.append(tid)
        if len(self._nd_touch_IDs) >= 2:
            pts = six_ex.values(self._nd_touch_poses)
            from common.utils.cocos_utils import ccp
            self._double_touch_prev_len = ccp(pts[0].x - pts[1].x, pts[0].y - pts[1].y).getLength()
        return True

    def _on_rotate_drag(self, layer, touch):
        tid = touch.getId()
        touch_wpos = touch.getLocation()
        if tid not in self._nd_touch_IDs:
            return
        if len(self._nd_touch_IDs) == 1:
            delta_pos = touch.getDelta()
            global_data.emgr.rotate_model_display.emit(-delta_pos.x / ROTATE_FACTOR)
        elif len(self._nd_touch_IDs) >= 2:
            self._nd_touch_poses[tid] = touch_wpos
            pts = six_ex.values(self._nd_touch_poses)
            vec = cc.Vec2(pts[0])
            vec.subtract(pts[1])
            cur_dist = vec.getLength()
            delta = cur_dist - self._double_touch_prev_len
            self._double_touch_prev_len = cur_dist
            delta = delta / self.CAM_SCALE_TOUCH_SEN_FACTOR
            self._on_cam_pos_scroll_delta(delta)

    def _on_rotate_drag_end(self, layer, touch):
        if not global_data.video_player.is_in_init_state():
            global_data.video_player.stop_video()
        tid = touch.getId()
        if tid in self._nd_touch_IDs:
            self._nd_touch_IDs.remove(tid)
            del self._nd_touch_poses[tid]

    def _on_show_last_mecha(self, *args):
        now = time.time()
        if now - self.save_last_touch_time < CLICK_BTN_INTERVAL_TIME:
            return
        self.save_last_touch_time = now
        if not self.panel.isVisible():
            return
        if not global_data.video_player.is_in_init_state():
            global_data.video_player.stop_video(ignore_cb=True)
        if self._cur_cam_mode == CAM_MODE_NEAR:
            self._cur_cam_mode = CAM_MODE_FAR
            self.refresh_cur_mecha_cam()
        if self._cur_mecha_id in self._open_mecha_lst:
            index = self._open_mecha_lst.index(self._cur_mecha_id)
        else:
            index = 1
        last_index = len(self._open_mecha_lst) - 1 if index == 0 else index - 1
        self.show_mecha_details(self._open_mecha_lst[last_index])

    def init_param(self):
        self.disappearing = False
        self._tab_state = None
        self._mecha_info_conf = confmgr.get('mecha_conf', 'MechaConfig', 'Content')
        self._mecha_skin_conf = confmgr.get('mecha_conf', 'SkinConfig', 'Content')
        self._mecha_conf = confmgr.get('mecha_display', 'HangarConfig', 'Content')
        self._skill_conf = confmgr.get('mecha_display', 'HangarConfig_Skills', 'Content')
        self._timer_id = None
        self._cur_mecha_goods_id = None
        self.mecha_view_type = MECHA_VIEW_MODEL
        self._init_view_type()
        self._base_clothing_id_to_item = {}
        self._screen_capture_helper = None
        self._share_content_kv = None
        self.skin_list_cnf = None
        self.cur_create_skin_index = 0
        self._async_action = None
        self._open_mecha_lst = [
         8001]
        self._cur_mecha_id = None
        self._cur_scene_content_type = None
        self._cur_mecha_cam_data = None
        self._cur_select_mecha_effect_id = None
        self._by_role_panel = False
        self._cur_cam_mode = CAM_MODE_FAR
        self.clothing_selected_index = 0
        self.cur_clothing_id = 0
        self._trk_player = None
        self.screen_sfx_id = None
        self._cam_offset = [
         0, 0, 0]
        self._cam_position_bounds = (None, None, 0.0)
        self._double_touch_prev_len = 0.0
        self._nd_touch_IDs = []
        self._nd_touch_poses = {}
        self._cur_cam_offset_distance = 0.0
        self.chuchang_video_dict = {}
        self.first_load_tag = True
        self.save_last_touch_time = time.time()
        return

    def _init_view_type(self):
        from ext_package.ext_decorator import has_skin_ext
        if has_skin_ext():
            self.mecha_view_type = MECHA_VIEW_MODEL
            global_data.emgr.forbid_mecha_chuchang_scene.emit(False)
        else:
            self.mecha_view_type = MECHA_VIEW_PIC
            global_data.emgr.set_last_chuchang_id.emit(None)
            global_data.emgr.forbid_mecha_chuchang_scene.emit(True)
        return

    def _on_show_next_mecha(self, *args):
        now = time.time()
        if now - self.save_last_touch_time < CLICK_BTN_INTERVAL_TIME:
            return
        self.save_last_touch_time = now
        if not self.panel.isVisible():
            return
        if not global_data.video_player.is_in_init_state():
            global_data.video_player.stop_video(ignore_cb=True)
        if self._cur_cam_mode == CAM_MODE_NEAR:
            self._cur_cam_mode = CAM_MODE_FAR
            self.refresh_cur_mecha_cam()
        if self._cur_mecha_id in self._open_mecha_lst:
            index = self._open_mecha_lst.index(self._cur_mecha_id)
        else:
            index = len(self._open_mecha_lst) - 1
        next_index = 0 if index == len(self._open_mecha_lst) - 1 else index + 1
        self.show_mecha_details(self._open_mecha_lst[next_index])

    def get_mecha_fashion(self, cur_mecha_item_id):
        clothing_id = global_data.player.get_mecha_fashion(cur_mecha_item_id)
        if clothing_id == -1:
            clothing_id = confmgr.get('mecha_conf', 'LobbyMechaConfig', 'Content', str(cur_mecha_item_id), 'default_fashion')[0]
        return clothing_id

    def check_mecha_ui_visible(self, mecha_id):
        cur_mecha_item_id = battle_id_to_mecha_lobby_id(mecha_id)
        clothing_id = self.get_mecha_fashion(cur_mecha_item_id)
        chuchang_anim = confmgr.get('mecha_conf', 'SkinConfig', 'Content', str(clothing_id), 'chuchang_anim', default=None)
        if chuchang_anim:
            self._on_fold_mecha_details_widget()
            self.update_mecha_ui_visible(False)
        return

    def update_mecha_ui_visible(self, visible):
        self.panel.nd_content.btn_play.setVisible(visible)
        self.panel.nd_btn_mech_change.setVisible(visible)
        self.panel.nd_btn_left.setVisible(visible)

    def show_mecha_details(self, mecha_id, by_role_panel=False, force_clothing_id=None):
        if not mecha_id and force_clothing_id:
            mecha_id = mecha_skin_utils.get_mecha_battle_id_by_skin_id(force_clothing_id)
        if not self.panel:
            return
        else:
            if not force_clothing_id:
                if self._cur_mecha_id == mecha_id:
                    return
            elif force_clothing_id == self.cur_clothing_id:
                return
            self._by_role_panel = by_role_panel
            self._cur_mecha_id = mecha_id
            cur_mecha_item_id = battle_id_to_mecha_lobby_id(self._cur_mecha_id)
            if not force_clothing_id:
                clothing_id = self.get_mecha_fashion(cur_mecha_item_id)
            else:
                clothing_id = force_clothing_id
                self.cur_clothing_id = clothing_id
            self._update_cur_mecha_cam_data(str(mecha_id), clothing_id)
            if not self._mecha_info_conf:
                return
            self._cur_mecha_goods_id = self._mecha_info_conf.get(str(mecha_id), {}).get('goods_id', None)
            self.anim_display_change_widget.on_change_mecha(mecha_id, clothing_id)
            self.clothing_selected_index = 0
            self.refresh_cur_mecha_cam(not self.first_load_tag)
            conf = self._mecha_conf[str(mecha_id)]
            mecha_name = conf.get('name_mecha_text_id', '')
            self.panel.tab_list.lab_title.SetString(mecha_name)
            self.update_mecha_status()
            self.panel.nd_btn_mech_change.btn_last_mech.setVisible(not by_role_panel)
            self.panel.nd_btn_mech_change.btn_next_mech.setVisible(not by_role_panel)
            self.req_del_item_redpoint(clothing_id)
            self.update_tabs_red_point()
            self.on_show_mecha_update(mecha_id, clothing_id)
            return

    def on_show_mecha_update(self, mecha_id, clothing_id):
        is_change_lobby_model_display = False
        if self.widgets_helper:
            if self.widgets_helper.cur_index is None:
                self.left_tab_list.select_tab_btn(0)
                if self.widgets_helper.cur_index == self.BASIC_INFO_WIDGET_IND:
                    is_change_lobby_model_display = True
            else:
                cur_widget = self.widgets_helper.get_cur_widget()
                if cur_widget:
                    self.on_notify_sub_widget(cur_widget)
                    if self.widgets_helper.cur_index == self.BASIC_INFO_WIDGET_IND:
                        is_change_lobby_model_display = True
        if not is_change_lobby_model_display:
            self.change_lobby_model_display(mecha_id, clothing_id)
        self.refresh_teach_btn()
        self.first_load_tag = False
        return

    def refresh_mecha_name(self):
        cur_mecha_item_id = battle_id_to_mecha_lobby_id(self._cur_mecha_id)
        name_text = item_utils.get_lobby_item_name(cur_mecha_item_id)
        self.panel.lab_mecha_name.setString(name_text)
        clothing_id = self.cur_clothing_id
        if clothing_id == -1:
            clothing_id = confmgr.get('mecha_conf', 'LobbyMechaConfig', 'Content', str(cur_mecha_item_id), 'default_fashion')[0]
        clothing_name_text = item_utils.get_lobby_item_name(clothing_id)
        self.panel.lab_kind.setString(clothing_name_text)
        item_utils.check_skin_tag(self.panel.temp_kind_level, self.cur_clothing_id)

    def refresh_btn_change(self):
        if self.anim_display_change_widget.get_anim_display_anim_data() and self.mecha_view_type == MECHA_VIEW_MODEL:
            self.panel.btn_change.setVisible(True)
        else:
            self.panel.btn_change.setVisible(False)

    def _update_cur_mecha_cam_data(self, mecha_id, clothing_id):
        self._cur_mecha_cam_data = lobby_model_display_utils.get_mecha_display_cam_data(str(mecha_id), clothing_id)
        self._try_update_cam_position_bounds()
        self._reset_cur_cam_offset_dist()

    def _try_update_cam_position_bounds(self):
        if not self._cur_mecha_cam_data:
            self._cur_mecha_cam_data = lobby_model_display_utils.get_mecha_display_cam_data(str(self._cur_mecha_id), self.cur_clothing_id)
        far_display_type = str(self._cur_mecha_cam_data.get('far_cam', 11))
        near_display_type = str(self._cur_mecha_cam_data.get('near_cam', 10))
        near_mid_display_type = str(self._cur_mecha_cam_data.get('near_mid_cam', 45))
        self._cam_offset = [0, self._cur_mecha_cam_data.get('cam_voffset', 0), 0]
        skin_offset = self._cur_mecha_cam_data.get('skin_offset', None)
        if skin_offset:
            self._cam_offset = skin_offset
        far_pos = lobby_model_display_utils.get_cam_position(self._cur_scene_content_type, far_display_type)
        near_pos = lobby_model_display_utils.get_cam_position(self._cur_scene_content_type, near_display_type)
        near_mid_pos = lobby_model_display_utils.get_cam_position(self._cur_scene_content_type, near_mid_display_type)
        if self.is_fold:
            self._cam_position_bounds = (
             far_pos, near_mid_pos, (far_pos - near_mid_pos).length)
        else:
            self._cam_position_bounds = (
             far_pos, near_pos, (far_pos - near_pos).length)
        return

    def _reset_cur_cam_offset_dist(self):
        self._cur_cam_offset_distance = 0.0

    def refresh_cur_mecha_cam(self, is_slerp=False):
        if not self._cur_mecha_cam_data:
            return
        if not self._cur_cam_mode:
            return
        key = 'far_cam' if self._cur_cam_mode == CAM_MODE_FAR else 'near_cam'
        display_type = str(self._cur_mecha_cam_data[key])
        global_data.emgr.set_lobby_scene_display_type.emit(display_type, is_slerp)
        if key == 'near_cam':
            global_data.emgr.load_high_quality_decal.emit()
        self._update_cam_position(is_slerp=is_slerp)

    def refresh_view_type_state(self):
        self.panel.btn_pic.SetText('')
        if self.mecha_view_type == MECHA_VIEW_MODEL:
            self.panel.lab_pic.SetString(get_text_by_id(MODULE_TEXT_ID))
            self.panel.icon_pic.SetDisplayFrameByPath('', 'gui/ui_res_2/mech_display/icon_visible.png')
        else:
            self.panel.lab_pic.SetString(get_text_by_id(PIC_TEXT_ID))
            self.panel.icon_pic.SetDisplayFrameByPath('', 'gui/ui_res_2/mech_display/icon_define_equiped.png')

    def refresh_more_list_buttons(self):
        btns_info = []
        btns_info.extend([{'name': 80820 if self.mecha_view_type == MECHA_VIEW_MODEL else 2221,'OnClick': self._on_click_change_view_type}])

        def btn_init_cb(btn, info):
            btn.btn_common.SetText(info['name'])

            @btn.btn_common.callback()
            def OnClick(*args):
                self.panel.nd_more.setVisible(False)
                info['OnClick'](*args)

        template_utils.init_common_more_btn_list(self.panel.list_button, btns_info, btn_init_cb)

    def reset_left_bottom_btn_position(self):
        pass

    @disable_on_puppet
    def refresh_teach_btn(self):
        cur_mecha_item_id = battle_id_to_mecha_lobby_id(self._cur_mecha_id)
        show_rp = True if global_data.player.has_item_by_no(cur_mecha_item_id) else False
        show_rp = show_rp and not global_data.achi_mgr.get_cur_user_archive_data('teach_video_' + str(self._cur_mecha_id), default=0)
        red_point_utils.show_red_point_template(self.panel.temp_tips, show_rp)

    def set_cur_clothing_id(self, clothing_id):
        old_clothing_id = self.cur_clothing_id
        self.cur_clothing_id = clothing_id
        if old_clothing_id != self.cur_clothing_id:
            self.anim_display_change_widget.on_change_clothing(self.cur_clothing_id)
        self._update_cur_mecha_cam_data(self._cur_mecha_id, self.cur_clothing_id)

    def load_scene(self, skin_cnf, check_switch_memory_scene=False):
        scene_path = skin_cnf.get('zhanshi_scene_path')
        display_type = lobby_model_display_const.DEFAULT_LEFT
        if self._cur_mecha_cam_data:
            if self._cur_cam_mode == CAM_MODE_FAR:
                key = 'far_cam' if 1 else 'near_cam'
                display_type = str(self._cur_mecha_cam_data[key])
            if scene_path is not None:
                if check_switch_memory_scene:
                    return
                global_data.emgr.show_disposable_lobby_relatived_scene.emit(scene_const.SCENE_SKIN_ZHANSHI, scene_path, display_type, belong_ui_name='MechaDetails')
                cur_scene_content_type = scene_const.SCENE_SKIN_ZHANSHI
                async_load = False
            else:
                text_path = None
                if self.MEMORY_WIDGET_IND == self.widgets_helper.get_cur_index():
                    text_path = 'model_new/xuanjue/xuanjue_new/textures/bg_mecha_memory.tga'
                cur_scene_content_type = text_path or scene_const.SCENE_ZHANSHI_MECHA if 1 else scene_const.SCENE_ACTIVITY_LEICHONG
                global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_JIEMIAN_COMMON, str(display_type), finish_callback=self._on_change_scene, scene_content_type=cur_scene_content_type, belong_ui_name='MechaDetails', is_slerp=not self.first_load_tag, scene_background_texture=text_path)
                async_load = True
            self._cur_scene_content_type = cur_scene_content_type
            async_load or self._try_update_cam_position_bounds()
            self._update_cam_position(is_slerp=False)
        return

    def change_mecha_pic(self, mecha_id, clothing_id):
        global_data.emgr.change_model_display_scene_item.emit(None)
        clothing_id = dress_utils.get_mecha_skin_item_no(mecha_id, clothing_id)
        img_path = confmgr.get('mecha_conf', 'SkinConfig', 'Content', str(clothing_id), 'img_path')
        self.panel.img_mech.SetDisplayFrameByPath('', img_path)
        self.panel.nd_mech_pic.setVisible(True)
        self.mecha_preview_advnaced_appearance_widget.set_visible(False)
        return

    def get_mecha_decal(self, clothing_id):
        ret = global_data.player.get_mecha_decal().get(str(get_main_skin_id(clothing_id)), []) if global_data.player else []
        return ret

    def get_mecha_color(self, clothing_id):
        ret = global_data.player.get_mecha_color().get(str(clothing_id), {}) if global_data.player else {}
        return ret

    def get_mecha_lobby_mode_data(self, item_no):
        model_data = lobby_model_display_utils.get_lobby_model_data(item_no)
        return model_data

    def change_mecha_model(self, mecha_id, clothing_id, is_change_skin, shiny_id):
        item_no = dress_utils.get_mecha_skin_item_no(mecha_id, clothing_id)
        model_data = self.get_mecha_lobby_mode_data(item_no)
        is_play_show_anim = False
        for data in model_data:
            if not data['mecha_end_ani']:
                continue
            if not (self.panel.temp_content.isVisible() and self.panel.isVisible()):
                data['show_anim'] = data['mecha_end_ani']
                data['end_anim'] = data['mecha_end_ani']
            else:
                data['show_anim'] = data['mecha_first_ani']
                data['end_anim'] = data['mecha_end_ani']
                is_play_show_anim = True
            data['skin_id'] = clothing_id
            if shiny_id:
                data['shiny_preview'] = shiny_id
            data['decal_list'] = self.get_mecha_decal(clothing_id)
            data['color_dict'] = self.get_mecha_color(clothing_id)

        if self._trk_player:
            self._trk_player.on_exit()
            self._trk_player = None

        def create_callback(model):
            if is_play_show_anim and mecha_skin_utils.is_ss_level_skin(clothing_id) and not is_change_skin:
                if clothing_id in (201800251, 201800252, 201800253):
                    self.play_camera_trk_anim()
                if mecha_id in (8006, ) and model and model.valid:

                    def animation_cb(*args):
                        screen_sfx = 'effect/fx/mecha/8006/8006_zhanshi_007.sfx'
                        if self.screen_sfx_id:
                            global_data.sfx_mgr.remove_sfx_by_id(self.screen_sfx_id)
                        self.screen_sfx_id = create_screen_effect_directly(screen_sfx)

                    model.unregister_event(animation_cb, 'zhanshi001', 'shopshow02')
                    model.register_anim_key_event('shopshow02', 'zhanshi001', animation_cb)
            if self._cur_select_mecha_effect_id:
                conf = confmgr.get('display_enter_effect')
                conf = conf.get('Content', {})
                display_enter_config = conf.get(self._cur_select_mecha_effect_id, {})
                sound_name = display_enter_config.get('cSfxSoundName', '')
                global_data.emgr.change_model_preview_effect.emit(display_enter_config['lobbyCallOutSfxPath'], sound_name)
                self._cur_select_mecha_effect_id = None
            return

        self.panel.nd_mech_pic.setVisible(False)
        if self.is_fold:
            for info in model_data:
                info['off_position'] = OFF_POSITION

        global_data.emgr.change_model_display_scene_item.emit(model_data, create_callback=create_callback)
        if len(model_data) > 0:
            first_model_data = model_data[0]
            self._display_model_info = {'model_path': first_model_data.get('mpath'),'sub_mesh_path_list': first_model_data.get('sub_mesh_path_list', [])}
        return

    def change_lobby_model_display(self, mecha_id, clothing_id, is_change_skin=False, shiny_id=None):
        old_clothing_id = self.cur_clothing_id
        self.cur_clothing_id = clothing_id
        can_use, _ = mall_utils.item_can_use_by_item_no(clothing_id)
        if self._is_for_puppet:
            self.update_share_btn(False)
        else:
            self.update_share_btn(bool(can_use))
        self.refresh_view_type_state()
        self.refresh_mecha_name()
        if old_clothing_id != self.cur_clothing_id:
            self.anim_display_change_widget.set_cur_anim_index(0)
        cur_skin_cnf = self._mecha_skin_conf.get(str(self.cur_clothing_id), {})
        if self.mecha_view_type != MECHA_VIEW_PIC and check_play_chuchang_video(clothing_id) and not self.chuchang_video_dict.get(clothing_id, False):
            if not self.chuchang_video_dict.get(clothing_id, False):
                self.anim_display_change_widget.disable_btn_change()
                self.mecha_preview_advnaced_appearance_widget.set_visible(False)
                self.panel.nd_mech_pic.setVisible(False)
                self._play_mecha_chuchang_video(clothing_id)
                return
            if self.is_fold:
                self.panel.nd_content.btn_play.setVisible(True)

                @self.panel.nd_content.btn_play.unique_callback()
                def OnClick(*args):
                    self.on_click_play_mecha_chuchang_video()

        else:
            if not global_data.video_player.is_in_init_state():
                global_data.video_player.stop_video(ignore_cb=True)
            if self.panel.btn_play.isVisible():
                self.panel.btn_play.setVisible(False)
            if self.is_fold and check_play_chuchang_video(self.cur_clothing_id):
                self.panel.nd_content.btn_play.setVisible(True)

                @self.panel.nd_content.btn_play.unique_callback()
                def OnClick(*args):
                    self.on_click_play_mecha_chuchang_video()

        self.load_scene(cur_skin_cnf)
        if self.isPanelVisible() and global_data.emgr.check_mecha_chuchang.emit(clothing_id, self.__class__.__name__)[0]:
            self.panel.nd_mech_pic.setVisible(False)
            self.anim_display_change_widget.stop_forbidden_timer()
            self.mecha_preview_advnaced_appearance_widget.set_visible(False)
            self.anim_display_change_widget.disable_btn_change()
            return
        else:
            self.refresh_btn_change()
            if self.mecha_view_type == MECHA_VIEW_PIC:
                self.change_mecha_pic(mecha_id, clothing_id)
                self.mecha_preview_advnaced_appearance_widget.set_visible(False)
                return
            self.change_mecha_model(mecha_id, clothing_id, is_change_skin, shiny_id)
            self.anim_display_change_widget.refresh_btn_change_forbidden_time()
            self.mecha_preview_advnaced_appearance_widget.refresh_show_model(clothing_id, L_ITEM_TYPE_MECHA_SKIN, force_update=True)
            self.mecha_preview_advnaced_appearance_widget.set_visible(True)
            self.mecha_preview_advnaced_appearance_widget.set_position(None if self.panel.btn_change.isVisible() else self.panel.btn_change)
            return

    def _play_mecha_chuchang_video(self, skin_id):
        if not global_data.video_player.is_in_init_state():
            if not global_data.video_player.player:
                global_data.video_player.reset_data()
            else:
                return
        if self.chuchang_video_dict.get(skin_id, False):
            return
        self._video_path = get_chuchang_video_path(skin_id)
        if self._video_path:
            self._video_path = 'video/%s.mp4' % self._video_path
            global_data.video_player.play_video(self._video_path, self.on_reset_lobby_model, repeat_time=1, bg_play=True)
            for r_skin_id in get_relative_video_skin_list(skin_id):
                self.chuchang_video_dict[r_skin_id] = True

    def on_click_play_mecha_chuchang_video(self):
        if self.mecha_view_type == MECHA_VIEW_PIC:
            self.panel.nd_mech_pic.setVisible(False)
        skin_id = self.cur_clothing_id
        if not global_data.video_player.is_in_init_state():
            if not global_data.video_player.player:
                global_data.video_player.reset_data()
            else:
                return
        self._video_path = get_chuchang_video_path(skin_id)
        if self._video_path:
            self._video_path = 'video/%s.mp4' % self._video_path
            global_data.video_player.play_video(self._video_path, self.on_reset_lobby_model, repeat_time=1, bg_play=True)
            for r_skin_id in get_relative_video_skin_list(skin_id):
                self.chuchang_video_dict[r_skin_id] = True

        self.update_mecha_ui_visible(False)

    def _on_click_chuchang(self, *args):
        pass

    def _on_change_scene(self, scene_type):
        self._try_update_cam_position_bounds()
        self._update_cam_position(is_slerp=not self.first_load_tag)

    def on_click_change(self, btn, touch):
        self.anim_display_change_widget.on_click_change()

    @disable_on_puppet
    def update_mecha_status(self):
        cur_mecha_item_id = battle_id_to_mecha_lobby_id(self._cur_mecha_id)
        item_data = global_data.player.get_item_by_no(cur_mecha_item_id)
        temp_btn_use_show = False
        lab_status_show = False
        money_types = [
         gconst.SHOP_PAYMENT_DIAMON,
         gconst.SHOP_PAYMENT_YUANBAO]
        if item_data is not None:
            temp_btn_use_show = True
            lab_status_show = True
            mecha_id = global_data.player.get_lobby_selected_mecha_id()
            if self._cur_mecha_id == mecha_id:
                temp_btn_use_show = False
            else:
                lab_status_show = False
        elif self._cur_mecha_goods_id is not None:
            if item_utils.can_jump_to_ui(self._cur_mecha_goods_id):
                pass
            else:
                money_types.insert(1, gconst.SHOP_PAYMENT_GOLD)
        self.price_top_widget.show_money_types(money_types)
        self.panel.temp_btn_use.setVisible(temp_btn_use_show)
        self.panel.lab_status.setVisible(lab_status_show)
        template_utils.show_remain_time(self.nd_time, self.nd_time.lab_time, cur_mecha_item_id, 81017)
        return

    @disable_on_puppet
    def req_del_item_redpoint(self, skin_id):
        show_new = global_data.lobby_red_point_data.get_rp_by_no(skin_id)
        if show_new:
            global_data.player.req_del_item_redpoint(skin_id)

    def _on_click_back_btn(self, *args):
        if self.disappearing:
            return
        self.disappearing = True
        global_data.emgr.reset_rotate_model_display.emit()
        self.close()

    def _on_click_move_cam(self, *args):
        if not self._cur_mecha_cam_data:
            return None
        else:
            if self._cur_cam_mode == CAM_MODE_FAR:
                self._cur_cam_mode = CAM_MODE_NEAR
            elif self._cur_cam_mode == CAM_MODE_NEAR:
                self._cur_cam_mode = CAM_MODE_FAR
            self.refresh_cur_mecha_cam(True)
            return self._cur_cam_mode

    @disable_on_puppet
    def on_click_btn_more(self, *args):
        if global_data.player:
            archive_data = global_data.achi_mgr.get_user_archive_data(global_data.player.uid)
        self.panel.nd_tips.setVisible(False)
        self.panel.btn_more.red_point.setVisible(False)
        if not global_data.video_player.is_in_init_state():
            global_data.video_player.stop_video()
        if self.panel.nd_more.isVisible():
            self.panel.nd_more.setVisible(False)
        else:
            self.panel.nd_more.setVisible(True)

    def _on_click_mecha_video(self, *args):
        video_url = ''
        video_conf = confmgr.get('lobby_model_display_conf', 'VideoURL', 'Content').get(str(self._cur_mecha_id), {})
        if video_conf:
            from logic.gcommon.common_utils.local_text import get_cur_lang_name, get_default_lang_name
            lang_name = get_cur_lang_name()
            if lang_name in video_conf:
                video_url = video_conf[lang_name]
            else:
                video_url = video_conf.get(get_default_lang_name(), '')
        if video_url:
            if G_IS_NA_USER:
                import game3d
                game3d.open_url(video_url)
            else:

                def func():
                    from logic.comsys.video.VideoUILogicWidget import VideoUILogicWidget
                    VideoUILogicWidget().play_vod(video_url)

                from common.utils import network_utils
                cur_type = network_utils.g93_get_network_type()
                if cur_type == network_utils.TYPE_MOBILE:
                    from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
                    SecondConfirmDlg2().confirm(content=get_text_by_id(607499), confirm_callback=func)
                else:
                    func()
        else:
            global_data.game_mgr.show_tip(get_text_by_id(19206))
        global_data.achi_mgr.set_cur_user_archive_data('teach_video_' + str(self._cur_mecha_id), 1)
        red_point_utils.show_red_point_template(self.panel.temp_tips, False)

    @disable_on_puppet
    def _on_click_btn_use_mecha(self, *args):
        item_data = global_data.player.get_item_by_no(int(self._cur_mecha_goods_id))
        if item_data is not None:
            global_data.player.req_change_lobby_mecha(self._cur_mecha_id)
        return

    @disable_on_puppet
    def _on_click_view_ar(self, btn, touch):
        try:
            import ar
        except:
            ui = global_data.ui_mgr.show_ui('UpdateGameConfirmUI', 'logic.comsys.lobby')
            return

        if global_data.player and global_data.player.get_self_ready() or global_data.player.is_matching or global_data.player.get_battle():
            global_data.game_mgr.show_tip(get_text_by_id(12097))
            return
        from logic.comsys.ar.MechaARMainUI1 import IGNORE_MECHA_IDS
        if self._cur_mecha_id in IGNORE_MECHA_IDS:
            global_data.game_mgr.show_tip(get_text_by_id(80715))
            return
        skin_id = 0
        if self.widgets_helper:
            skin_id = self.widgets_helper.get_widget_by_index(0).get_basic_skin_widget().get_skin_id()
        all_show_skin_list_cnf = mecha_skin_utils.get_show_skin_list(self._cur_mecha_id)
        own_skin_id_list = []
        for index, one_conf in enumerate(all_show_skin_list_cnf):
            clothing_id = all_show_skin_list_cnf[index]
            clothing_data = global_data.player.get_item_by_no(clothing_id)
            cur_mecha_item_id = battle_id_to_mecha_lobby_id(self._cur_mecha_id)
            mecha_item_data = global_data.player.get_item_by_no(cur_mecha_item_id)
            if not clothing_data or not mecha_item_data:
                continue
            is_default_skin = False
            default_skin = confmgr.get('mecha_conf', 'LobbyMechaConfig', 'Content', str(cur_mecha_item_id), 'default_fashion')[0]
            if int(default_skin) == int(clothing_id):
                is_default_skin = True
            if is_default_skin:
                is_owned = clothing_data and clothing_data.get_expire_time() < 0
            else:
                is_owned = clothing_data
            if not is_owned:
                continue
            own_skin_id_list.append(clothing_id)

        if skin_id not in own_skin_id_list:
            global_data.game_mgr.show_tip(get_text_by_id(609392))
            return
        try:
            import ar
            if not ar.is_support_ar():
                global_data.game_mgr.show_tip(get_text_by_id(609393))
                return
        except:
            pass

        ui_name = 'MechaARMainUI1'
        global_data.ui_mgr.show_ui(ui_name, 'logic.comsys.ar')
        ui = global_data.ui_mgr.get_ui(ui_name)
        if ui:
            item_no = dress_utils.get_mecha_skin_item_no(self._cur_mecha_id, skin_id)
            model_data = lobby_model_display_utils.get_lobby_model_data(item_no)
            shiny_weapon_id = model_data[0]['shiny_weapon_id']
            ui.init_model_data(self._display_model_info, self._cur_mecha_id, skin_id, shiny_weapon_id)

    def _on_click_change_view_type(self, btn, touch):
        if self.mecha_view_type == MECHA_VIEW_MODEL:
            self.mecha_view_type = MECHA_VIEW_PIC
            global_data.emgr.end_mecha_chuchang_scene.emit()
            global_data.emgr.forbid_mecha_chuchang_scene.emit(True)
        else:
            self.mecha_view_type = MECHA_VIEW_MODEL
            global_data.emgr.forbid_mecha_chuchang_scene.emit(False)
            global_data.emgr.set_last_chuchang_id.emit(None)
        self.refresh_btn_change()
        self.change_lobby_model_display(self._cur_mecha_id, self.cur_clothing_id)
        return

    def on_click_btn_share(self, btn, touch):
        skin_id = self.cur_clothing_id
        if not global_data.video_player.is_in_init_state() and global_data.video_player.player:
            global_data.game_mgr.show_tip(get_text_by_id(82150))
            return
        if self.widgets_helper.get_cur_index() == self.MEMORY_WIDGET_IND:
            cur_widget = self.widgets_helper.get_cur_widget()
            if cur_widget:
                if getattr(cur_widget, 'show_widget_share_ui') and cur_widget.show_widget_share_ui:
                    cur_widget.show_widget_share_ui()
            return
        if not self._screen_capture_helper:
            from logic.comsys.share.ScreenFrameHelper import ScreenFrameHelper
            self._screen_capture_helper = ScreenFrameHelper()
        old_is_fold = self.is_fold
        from logic.gutils.dress_utils import battle_id_to_mecha_lobby_id
        default_skin = confmgr.get('mecha_conf', 'LobbyMechaConfig', 'Content', str(battle_id_to_mecha_lobby_id(self._cur_mecha_id)), 'default_fashion')
        if default_skin and int(default_skin[0]) == int(skin_id):
            is_default_skin = True
        else:
            is_default_skin = False
        share_spec = confmgr.get('c_share_item_conf', str(skin_id), default={})
        has_share_spec = bool(share_spec)
        can_kv = is_mecha_id_can_show_kv(self._cur_mecha_id) or has_share_spec
        need_kv = can_kv and is_default_skin or has_share_spec
        if self._screen_capture_helper:

            def custom_cb(*args):
                self.show_share_ui(need_kv, is_default_skin)
                if self.mecha_view_type == MECHA_VIEW_PIC:
                    self.panel.img_tab_left.setVisible(True)
                    self.panel.nd_hide.setVisible(True)
                    can_use, _ = mall_utils.item_can_use_by_item_no(skin_id)
                    self.update_share_btn(bool(can_use))
                    self.panel.nd_btn_mech_change.setVisible(True)
                    cur_widget = self.widgets_helper.get_cur_widget()
                    if cur_widget:
                        cur_widget.show()
                else:
                    self.panel.setVisible(True)
                self.is_fold = not old_is_fold
                self.panel.StopAnimation('return')
                self.panel.StopAnimation('move')
                self._on_fold_mecha_details_widget(is_slerp=False)

            show_item_no = is_default_skin or skin_id if 1 else battle_id_to_mecha_lobby_id(self._cur_mecha_id)
            self.is_fold = False
            self._on_fold_mecha_details_widget(is_slerp=False)
            if self.mecha_view_type == MECHA_VIEW_PIC:
                self.panel.nd_btn_mech_change.setVisible(False)
                self.update_share_btn(False)
                cur_widget = self.widgets_helper.get_cur_widget()
                if cur_widget:
                    cur_widget.hide()
                self.panel.nd_hide.setVisible(False)
                self.panel.img_tab_left.setVisible(False)
            else:
                self.panel.setVisible(False)
            if self.anim_display_change_widget.get_anim_display_anim_data() and self.anim_display_change_widget.get_cur_anim_index() > 0:
                need_end_anim = False
            else:
                need_end_anim = True
            self._screen_capture_helper.take_screen_shot([
             self.__class__.__name__], self.panel, custom_cb=custom_cb, head_nd_name='nd_player_info_1', item_detail_no=show_item_no, item_detail_no_is_get=False, need_share_ui=not need_kv, ToEndAnim=need_end_anim, need_draw_rt=not need_kv, HidePanelAfterEndChuChang=self.mecha_view_type == MECHA_VIEW_MODEL)

    def test_get_render_texture(self, is_to_kv=True):
        import common.utils.timer as timer

        def cb2():
            ui = global_data.ui_mgr.get_ui('ShareUI')
            if ui:
                if is_to_kv:
                    self._screen_capture_helper.get_share_content().get_render_texture()
                    ui.set_share_content_raw(self._share_content_kv.get_render_texture(), share_content=self._share_content_kv)
                else:
                    ui.set_share_content_raw(self._screen_capture_helper.get_share_content().get_render_texture(), share_content=self._share_content_kv)
                    self._share_content_kv.get_render_texture()
            else:
                if global_data.test_timer_id:
                    global_data.game_mgr.unregister_logic_timer(global_data.test_timer_id)
                global_data.test_timer_id = None
            return

        global_data.test_timer_id = global_data.game_mgr.register_logic_timer(cb2, 1, times=-1, mode=timer.LOGIC)

    def show_share_ui(self, need_kv, is_default_skin):
        if not global_data.ui_mgr.get_ui('ShareUI'):
            from logic.comsys.share.ShareUI import ShareUI
            ui = ShareUI()
            ui.clear_choose_list_func()
        skin_id = self.cur_clothing_id
        if need_kv:
            if not self._share_content_kv:
                from logic.comsys.share.ItemInfoShareCreator import ItemInfoShareCreator
                share_creator = ItemInfoShareCreator()
                share_creator.create()
                self._share_content_kv = share_creator
                check_add_shareui_battle_record_func(skin_id, True, self._share_content_kv, self._screen_capture_helper)
            if self._share_content_kv:

                def update_kv():
                    from logic.gutils.dress_utils import battle_id_to_mecha_lobby_id
                    lobby_mecha_id = battle_id_to_mecha_lobby_id(int(self._cur_mecha_id))
                    kv_path = get_share_bg_path(skin_id) or get_share_bg_path(lobby_mecha_id)
                    self._share_content_kv.get_ui_bg_sprite().SetDisplayFrameByPath('', kv_path, force_sync=True)
                    self._share_content_kv.set_show_record(False)
                    self._share_content_kv.show_share_detail(lobby_mecha_id if is_default_skin else skin_id, is_get=False)

                real_func = async_disable_wrapper(update_kv)
                real_func()
            check_add_shareui_kv_func(lambda is_to_kv: self.share_switch_to_kv(is_to_kv), False)
            self.share_switch_to_kv(False)
        else:
            check_add_shareui_battle_record_func(skin_id, True, None, self._screen_capture_helper)
            honer_count_item_no, _ = get_ex_skin_improve_item_no(skin_id)
            if honer_count_item_no and bool(global_data.player.get_item_by_no(honer_count_item_no)):
                check_add_shareui_ex_privilege_func(skin_id, self._screen_capture_helper)
        return

    def share_switch_to_kv(self, is_to_kv):
        on_share_switch_to_kv(self._share_content_kv, self._screen_capture_helper, is_to_kv)

    def on_widget_switch(self, index, widget, is_show):
        if is_show:
            self.on_notify_sub_widget(widget)
            if self.widgets_helper.get_cur_index() == self.MEMORY_WIDGET_IND:
                self.panel.nd_btn_mech_change.setVisible(False)
                self.panel.nd_btn_left.setVisible(False)
                if self._cur_scene_content_type != scene_const.SCENE_ACTIVITY_LEICHONG:
                    if self.cur_clothing_id:
                        cur_mecha_item_id = battle_id_to_mecha_lobby_id(self._cur_mecha_id)
                        dress_clothing_id = self.get_mecha_fashion(cur_mecha_item_id)
                        if dress_clothing_id != self.cur_clothing_id:
                            self.cur_clothing_id = dress_clothing_id
                        self.on_reset_lobby_model()
            else:
                self.panel.nd_btn_mech_change.setVisible(True)
                if self.widgets_helper.get_cur_index() == self.BASIC_INFO_WIDGET_IND:
                    self.panel.nd_btn_left.setVisible(True)
                else:
                    self.panel.nd_btn_left.setVisible(False)
                if self._cur_scene_content_type == scene_const.SCENE_ACTIVITY_LEICHONG:
                    if self.cur_clothing_id:
                        self.on_reset_lobby_model()

    def play_camera_trk_anim(self, *args):
        if self._trk_player:
            self._trk_player.on_exit()
        self._trk_player = CameraTrkPlayer()
        track_path = 'effect/fx/mecha/8002/camera/shopshow02.trk'
        self._trk_player.auto_play_track(track_path, None)
        return

    def do_show_panel_ex(self, ui_from):
        self.do_show_panel(ui_from=ui_from)

    def do_show_panel(self, ui_from=None):
        super(MechaDetails, self).do_show_panel()
        if ui_from == 'mecha_chuchang_scene':
            if self.is_fold:
                self._on_fold_mecha_details_widget()
            self.on_reset_lobby_model()
            return
        else:
            if self._cur_mecha_id:
                self.update_mecha_status()
                if self.widgets_helper:
                    cur_widget = self.widgets_helper.get_cur_widget()
                    if cur_widget:
                        self.on_notify_sub_widget(cur_widget)
                cur_mecha_item_id = battle_id_to_mecha_lobby_id(self._cur_mecha_id)
                cur_clothing_id = self.get_mecha_fashion(cur_mecha_item_id)
                if get_main_skin_id(cur_clothing_id) == get_main_skin_id(self.cur_clothing_id):
                    self.cur_clothing_id = cur_clothing_id
                if self.widgets_helper and self.widgets_helper.get_cur_index() == self.BASIC_INFO_WIDGET_IND:
                    global_data.emgr.set_last_chuchang_id.emit(None)
                else:
                    global_data.emgr.set_last_chuchang_id.emit(self.cur_clothing_id)
                self.on_reset_lobby_model()
                self._update_cur_mecha_cam_data(str(self._cur_mecha_id), self.cur_clothing_id)
            self.cur_clothing_id and self.req_del_item_redpoint(self.cur_clothing_id)
            default_skin = confmgr.get('mecha_conf', 'LobbyMechaConfig', 'Content', str(self._cur_mecha_id), 'default_fashion')
            if default_skin and int(default_skin[0]) == int(self.cur_clothing_id):
                self.req_del_item_redpoint(self._cur_mecha_id)
            return

    def on_notify_sub_widget(self, widget):
        widget.on_switch_to_mecha_type(self._cur_mecha_id)

    def do_hide_panel(self):
        super(MechaDetails, self).do_hide_panel()
        if self._trk_player:
            self._trk_player.on_exit()
            self._trk_player = None
        showing_manual_video = self.has_hide_reason('VideoManualCtrlUI')
        if not showing_manual_video:
            if not global_data.video_player.is_in_init_state():
                global_data.video_player.stop_video()
        global_data.emgr.forbid_mecha_chuchang_scene.emit(False)
        return

    def on_reset_lobby_model(self):
        if not self.panel:
            return
        else:
            if not self.widgets_helper:
                return
            if self.widgets_helper.get_cur_index() != self.MEMORY_WIDGET_IND:
                self.panel.nd_btn_mech_change.setVisible(True)
                if self.widgets_helper.get_cur_index() == self.BASIC_INFO_WIDGET_IND:
                    self.panel.nd_btn_left.setVisible(True)
            if self._cur_mecha_id is not None:
                self.change_lobby_model_display(self._cur_mecha_id, self.cur_clothing_id)
            else:
                text_path = None
                if self.MEMORY_WIDGET_IND == self.widgets_helper.get_cur_index():
                    text_path = 'model_new/xuanjue/xuanjue_new/textures/bg_mecha_memory.tga'
                cur_scene_content_type = text_path or scene_const.SCENE_ZHANSHI_MECHA if 1 else scene_const.SCENE_ACTIVITY_LEICHONG
                global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_JIEMIAN_COMMON, lobby_model_display_const.DEFAULT_LEFT, finish_callback=self._on_change_scene, scene_content_type=cur_scene_content_type, belong_ui_name='MechaDetails', scene_background_texture=text_path)
                self._cur_scene_content_type = cur_scene_content_type
            return

    def _on_buy_good_success(self):
        self.update_mecha_status()

    @disable_on_puppet
    def change_lobby_mecha(self):
        self.update_mecha_status()
        cur_mecha_item_id = global_data.player.get_lobby_selected_mecha_item_id()
        name_text = item_utils.get_lobby_item_name(cur_mecha_item_id)
        global_data.game_mgr.show_tip(get_text_by_id(14011, {'name': name_text}))

    def show_to_gain_method_page(self, gain_method, proficiency_level=None):
        ui_inst = global_data.ui_mgr.get_ui('InscriptionMainUI')
        if ui_inst:
            return
        else:
            if gain_method == mecha_const.MODULE_CARD_GAIN_VIA_SHOP_LOTTERY:
                global_data.ui_mgr.close_ui('MechaDetails')
                global_data.ui_mgr.show_ui('MallMainUI', 'logic.comsys.mall_ui')
            elif gain_method == mecha_const.MODULE_CARD_GAIN_VIA_MECHA_PROFICIENCY_REWARD:
                from logic.comsys.mecha_display.MechaProficiencyDetailsUI import MechaProficiencyDetailsUI
                MechaProficiencyDetailsUI(None, self._cur_mecha_id)
            return

    def refresh_mecha_red_dot(self, mecha_id, *args):
        need_red_point = self.basic_red_point_check_func()
        self.set_tab_red_point_visibility(self.BASIC_INFO_WIDGET_IND, need_red_point)

    def on_refresh_item_red_point(self):
        basic_need_red_point = self.basic_red_point_check_func()
        self.set_tab_red_point_visibility(self.BASIC_INFO_WIDGET_IND, basic_need_red_point)

    def _on_change_mecha_view_zoom(self, cam_mode):
        self._cur_cam_mode = cam_mode

    def set_cam_offset_dist(self, dist):
        far, near, length = self._cam_position_bounds
        self._cur_cam_offset_distance = min(length, max(0, dist))

    def switch_view_type(self, view_type, mecha_id, clothing_id, shiny_id):
        if view_type in [MECHA_VIEW_MODEL, MECHA_VIEW_PIC]:
            self.mecha_view_type = view_type
            if view_type == MECHA_VIEW_MODEL:
                global_data.emgr.forbid_mecha_chuchang_scene.emit(False)
        if self.mecha_view_type == MECHA_VIEW_MODEL:
            self.change_lobby_model_display(mecha_id, clothing_id, False, shiny_id)

    def jump_to_mecha_sfx(self, item_id):
        pass

    def jump_to_skin(self, skin_id):
        self.switch_to_tab(self.BASIC_INFO_WIDGET_IND)
        cur_widget = self.widgets_helper.get_cur_widget()
        cur_widget.jump_to_skin(int(skin_id))

    def switch_to_tab(self, tab_ind):
        if self.widgets_helper:
            self.widgets_helper.on_switch_to_widget(tab_ind)
            if tab_ind != self.BASIC_INFO_WIDGET_IND and lobby_model_display_utils.is_chuchang_scene():
                global_data.emgr.end_mecha_chuchang_scene.emit()

    def on_click_tab(self, tab_ind):
        if self.left_tab_list:
            self.left_tab_list.select_tab_btn(tab_ind)

    def update_tabs_red_point(self):
        for tab_index, tab_data in enumerate(self.tab_list_data):
            tab_red_point_func = tab_data.get('red_point_func', None)
            if tab_red_point_func:
                self.set_tab_red_point_visibility(tab_index, tab_red_point_func())

        return

    def set_tab_red_point_visibility(self, tab_ind, rp_level):
        all_count = self.panel.tab_list.tab_list.GetItemCount()
        if tab_ind >= all_count:
            return
        ui_item = self.panel.tab_list.tab_list.GetItem(tab_ind)
        red_point_utils.show_red_point_template(ui_item.img_red, rp_level, rp_level)

    def basic_red_point_check_func(self):
        mecha_id = self._cur_mecha_id
        if global_data.player.has_unreceived_prof_reward(mecha_id):
            return red_point_utils.RED_POINT_LEVEL_30
        mecha_lobby_id = battle_id_to_mecha_lobby_id(mecha_id)
        if global_data.lobby_red_point_data.get_rp_by_belong_no(mecha_lobby_id):
            return red_point_utils.RED_POINT_LEVEL_10
        return 0

    def effect_red_point_check_func(self, *args):
        if global_data.lobby_red_point_data.get_rp_by_type(lobby_item_type.L_ITEM_MECHA_SFX):
            return red_point_utils.RED_POINT_LEVEL_10
        return 0

    def select_type--- This code section failed: ---

1534       0  LOAD_GLOBAL           0  'getattr'
           3  LOAD_GLOBAL           1  'None'
           6  LOAD_CONST            0  ''
           9  CALL_FUNCTION_3       3 
          12  POP_JUMP_IF_TRUE     19  'to 19'

1535      15  LOAD_CONST            0  ''
          18  RETURN_END_IF    
        19_0  COME_FROM                '12'

1536      19  LOAD_FAST             0  'self'
          22  LOAD_ATTR             2  'left_tab_list'
          25  LOAD_ATTR             3  'select_tab_btn'
          28  LOAD_FAST             1  'tab_ind'
          31  CALL_FUNCTION_1       1 
          34  POP_TOP          
          35  LOAD_CONST            0  ''
          38  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 9

    def select_module_btn(self, module_btn_idx):
        if self.widgets_helper:
            cur_widget = self.widgets_helper.get_cur_widget()
            if cur_widget:
                if isinstance(cur_widget, MechaLobbyModuleWidget):
                    cur_widget.select_module_btn(module_btn_idx)

    def _get_cam_position(self, offset_dist):
        far, near, length = self._cam_position_bounds
        if far is None or near is None:
            return
        else:
            diff = near - far
            if diff.length_sqr < offset_dist * offset_dist:
                return math3d.vector(near)
            if offset_dist < 0:
                return math3d.vector(far)
            direction = math3d.vector(diff)
            if direction.is_zero:
                return
            direction.normalize()
            offset = direction * offset_dist
            return far + offset
            return

    def _modify_cur_cam_offset_dist(self, offset):
        far, near, length = self._cam_position_bounds
        dst_offset_dist = self._cur_cam_offset_distance + offset
        dst_offset_dist = min(length, max(0, dst_offset_dist))
        prev = self._cur_cam_offset_distance
        self._cur_cam_offset_distance = dst_offset_dist
        thres = length / 2.0
        if prev < thres and dst_offset_dist >= thres:
            global_data.emgr.load_high_quality_decal.emit()

    def check_can_mouse_scroll(self):
        return True

    def on_hot_key_mouse_scroll(self, msg, delta, key_state):
        delta = delta / self.CAM_SCALE_MOUSE_SEN_FACTOR
        self._on_cam_pos_scroll_delta(delta)

    def _on_cam_pos_scroll_delta(self, delta):
        self._modify_cur_cam_offset_dist(delta)
        self._update_cam_position(is_slerp=True)

    def _update_cam_position(self, is_slerp):
        if lobby_model_display_utils.is_chuchang_scene():
            return
        else:
            pos = self._get_cam_position(self._cur_cam_offset_distance)
            if pos is not None:
                offset_pos = math3d.vector(*self._cam_offset)
                global_data.emgr.change_model_display_scene_cam_pos.emit(pos + offset_pos, is_slerp=is_slerp)
                return True
            return False
            return

    def test_cam_offset(self, offset_x, offset_y, offset_z):
        if lobby_model_display_utils.is_chuchang_scene():
            return
        else:
            pos = self._get_cam_position(self._cur_cam_offset_distance)
            if pos is not None:
                offset_pos = math3d.vector(offset_x, offset_y, offset_z)
                global_data.emgr.change_model_display_scene_cam_pos.emit(pos + offset_pos, is_slerp=False)
                return True
            return False
            return

    def test2(self):
        import math
        import math3d
        ui = global_data.ui_mgr.get_ui('MechaDetails')
        nd = ui.panel.temp_content.nd_gyrpo
        if not nd:
            ui.test_gyrposcope()
            ui = global_data.ui_mgr.get_ui('MechaDetails')
            nd = ui.panel.temp_content.nd_gyrpo
        self.sum_gyro_vector = math3d.vector(0, 0, 0)

        def new_func(new_gyro_vector, raw_rotate_speed, sum_gyrp_vector):
            print('gyro_callback', new_gyro_vector, raw_rotate_speed, sum_gyrp_vector)
            self.sum_gyro_vector.x += new_gyro_vector.x
            self.sum_gyro_vector.y += new_gyro_vector.y
            nd.nd_card.setRotation3D(cc.Vec3(raw_rotate_speed.x * 180 / math.pi, raw_rotate_speed.y * 180 / math.pi, 0))

        ui.gyro_com._gryo_update_cb = new_func

    def get_program(self):
        SHADER_VS = 'common/shader/cocosui/positiontexturecolor_nomvp.vs'
        SHADER_PS_IOS = 'common/shader/cocosui/positiontexturecolor_nomvp_y_cbcr.ps'
        SHADER_PS = SHADER_PS_IOS
        program = cc.GLProgram.createWithFilenames(SHADER_VS, SHADER_PS)
        return cc.GLProgramState.create(program)

    def test_ar(self, ar_debug_two_tex_in_one_sprite, *args):
        import render
        import logic.comsys.effect.ui_effect as ui_effect
        director = cc.Director.getInstance()
        view = director.getOpenGLView()
        print(('GL View Size: ', view.getVisibleSize()))
        view_w = view.getVisibleSize().width
        view_h = view.getVisibleSize().height
        view_center = cc.Vec2(view_w / 2, view_h / 2)
        Y_TEX_PATH = 'gui/ar_ios/y.png'
        CBCR_TEX_PATH = 'gui/ar_ios/cbcr.png'
        nx_y_tex = render.texture(Y_TEX_PATH, False, False, render.TEXTURE_TYPE_UNKNOWN, False, None, None, 0, 0, False)
        print(('Camera Y Tex Size: ', nx_y_tex.size))
        nx_uv_tex = render.texture(CBCR_TEX_PATH, False, False, render.TEXTURE_TYPE_UNKNOWN, False, None, None, 0, 0, False)
        print(('Camera UV Tex Size: ', nx_uv_tex.size))
        cc_y_tex = cc.Texture2D.createWithITexture(nx_y_tex)
        cc_uv_tex = cc.Texture2D.createWithITexture(nx_uv_tex)
        if ar_debug_two_tex_in_one_sprite == 1:
            gl_pg = ui_effect.get_GLProgram('ar', 'positiontexturecolor_nomvp', 'positiontexturecolor_nomvp_y_cbcr')
            if not gl_pg:
                print(('test--test_ar--step1--gl_pg =', gl_pg))
                return
            cc_sprite = cc.Sprite.createWithTexture(cc_y_tex)
            pg_state = ui_effect.get_gl_program_state(cc_sprite, 'ar', gl_pg)
            pg_state.setUniformTexture('CC_Texture0', cc_y_tex)
            pg_state.setUniformTexture('CC_Texture2', cc_uv_tex)
            cc_y_tex.retain()
            cc_uv_tex.retain()
            cc_sprite.setGLProgramState(pg_state)
            self.panel.layer.addChild(cc_sprite)
            cc_sprite.setContentSize(cc.Size(nx_y_tex.size[0], nx_y_tex.size[1]))
            cc_sprite.setTextureRect(cc.Rect(0, 0, nx_y_tex.size[0], nx_y_tex.size[1]))
            print(('test--test_ar--step2--nx_y_tex.size =', nx_y_tex.size))
        else:
            y_sprite = cc.Sprite.createWithTexture(cc_y_tex)
            uv_sprite = cc.Sprite.createWithTexture(cc_uv_tex)
            y_sprite.setPosition(view_center)
            uv_sprite.setPosition(view_center)
            self.panel.layer.addChild(y_sprite)
            self.panel.layer.addChild(uv_sprite)
        return

    def _on_fold_mecha_details_widget(self, is_slerp=True):
        self.panel.nd_btn_mech_change.setVisible(True)
        if not self.widgets_helper:
            return
        widget = self.widgets_helper.get_widget_by_index(self.BASIC_INFO_WIDGET_IND)
        if not widget:
            return
        if self.panel.IsPlayingAnimation('appear'):
            max_appear_time = self.panel.GetAnimationMaxRunTime('appear')
            self.panel.FastForwardToAnimationTime('appear', max_appear_time)
        nd = widget.panel.img_icon_put_away_left
        if self.is_fold:
            nd.SetDisplayFrameByPath('', 'gui/ui_res_2/mech_display/icon_put_away_right.png')
            if is_slerp:
                self.panel.PlayAnimation('return')
            else:
                self.panel.PlayAnimation('return')
                max_time = self.panel.GetAnimationMaxRunTime('return')
                self.panel.FastForwardToAnimationTime('return', max_time)
            global_data.emgr.change_model_display_off_position.emit(is_slerp=is_slerp)

            @self.panel.nd_content.nd_mech_video.unique_callback()
            def OnClick(*args):
                pass

            self.panel.nd_content.btn_play.setVisible(False)

            @self.panel.nd_content.btn_play.unique_callback()
            def OnClick(*args):
                pass

        else:
            nd.SetDisplayFrameByPath('', 'gui/ui_res_2/mech_display/icon_put_away_left.png')
            if is_slerp:
                self.panel.PlayAnimation('move')
            else:
                self.panel.PlayAnimation('move')
                max_time = self.panel.GetAnimationMaxRunTime('move')
                self.panel.FastForwardToAnimationTime('move', max_time)
            global_data.emgr.change_model_display_off_position.emit(OFF_POSITION, is_slerp)

            @self.panel.nd_content.nd_mech_video.unique_callback()
            def OnClick(*args):
                if not global_data.video_player.is_in_init_state():
                    global_data.video_player.stop_video()

            if check_play_chuchang_video(self.cur_clothing_id):
                self.panel.nd_content.btn_play.setVisible(True)

                @self.panel.nd_content.btn_play.unique_callback()
                def OnClick(*args):
                    self.on_click_play_mecha_chuchang_video()

        self.is_fold = not self.is_fold
        self._try_update_cam_position_bounds()
        self.set_cam_offset_dist(self._cur_cam_offset_distance)
        self._update_cam_position(is_slerp=True)

    def _on_click_btn_left(self, *args):
        self._on_fold_mecha_details_widget()

    def reset_share_btn(self):
        can_use, _ = mall_utils.item_can_use_by_item_no(self.cur_clothing_id)
        self.update_share_btn(bool(can_use))

    def update_share_btn(self, visible):
        basic_widget = self.widgets_helper.tab_widgets.get(self.basic_widget_index, None)
        basic_widget and basic_widget.panel.btn_share.setVisible(visible and global_data.is_share_show)
        memory_widget = self.widgets_helper.tab_widgets.get(self.MEMORY_WIDGET_IND, None)
        memory_widget and memory_widget.panel.btn_share.setVisible(visible and global_data.is_share_show)
        return

    def _check_ext_tips(self):
        from ext_package.ext_decorator import has_skin_ext
        if not has_skin_ext() and self.panel and self.panel.isValid():
            from logic.comsys.lobby.ExtNpk.ExtTipsWidget import ExtTipsWidget
            tips_nd = global_data.uisystem.load_template_create('common/i_common_base_package_tips', self.panel.nd_base_package)
            self._ext_tip_widget = ExtTipsWidget(self.panel, tips_nd, 'mech_main_new')