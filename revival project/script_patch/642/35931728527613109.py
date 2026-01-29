# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/role/PlayerInfoUI.py
from __future__ import absolute_import
import six_ex
import time
from common.const.property_const import *
from common.uisys.basepanel import BasePanel
from logic.gutils import lobby_model_display_utils
from logic.gutils.dress_utils import battle_id_to_mecha_lobby_id
from logic.gutils import red_point_utils
from logic.gcommon import const
from logic.gcommon.item import item_const
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_CLOSE_BY_DEFAULT_FUNC_NAME
from logic.gutils.system_unlock_utils import is_sys_unlocked, SYSTEM_CREDIT, SYSTEM_CAREER, show_sys_unlock_tips
from logic.comsys.role.PlayerRoleInfoWidget import PlayerRoleInfoWidget
from logic.comsys.role.PlayerBattleInfoWidget import PlayerBattleInfoWidget
from logic.comsys.role.PlayerHistoryRecordsWidget import PlayerHistoryRecordsWidget
from logic.comsys.role.PlayerCreditWidget import PlayerCreditWidget
from logic.comsys.role.PlayerIntimacyWidget import PlayerIntimacyWidget
from logic.comsys.role.PlayerBattleFlagWidget import PlayerBattleFlagWidget
from logic.comsys.role.PlayerCareerMedalWidget import PlayerCareerMedalWidget
from logic.comsys.role.PlayerMechaMemoryWidget import PlayerMechaMemoryWidget
from logic.gutils.skin_define_utils import get_main_skin_id
from collections import OrderedDict
from logic.gutils import skin_define_utils
from logic.gutils import item_utils as iutils
TAB_PLAYER_INFO = 0
TAB_BATTLE_INFO = 1
TAB_HISTORY_INFO = 2
TAB_MECHA_CAREER = 3
TAB_INTIMACY_INFO = 4
TAB_CREDIT_INFO = 5
TAB_BATTLE_FLAG = 6
TAB_CAREER_MEDAL = 7
SHOW_MODEL_PAGE = (
 TAB_PLAYER_INFO,)

class PlayerInfoUI(BasePanel):
    PANEL_CONFIG_NAME = 'role/player_info'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE_BY_DEFAULT_FUNC_NAME
    GLOBAL_EVENT = {'message_on_player_detail_inf': 'on_refresh_player_detail_inf',
       'message_on_player_stat_inf': 'on_player_stat_inf',
       'refresh_item_red_point': 'refresh_tag_rp',
       'on_receive_credit_reward': 'refresh_tag_rp',
       'message_refresh_intimacy_msg': 'refresh_tag_rp',
       'message_on_intimacy_event': 'refresh_tag_rp'
       }
    UI_ACTION_EVENT = {'temp_btn_back.btn_back.OnClick': 'on_click_back_btn'
       }
    UI_EFFECT_LIST = [{'node': 'temp_left_tab','anim': 'in','time': 0}]
    DELAY_TIME = 0.5
    DELAY_TAG = 20210116

    def jump_to_tab(self, page_tab, uid, sub_tab=None, sel_item_no=None):
        self._init_tab = page_tab
        self._jump_to_sub_tab = sub_tab
        self._jump_to_sub_tab_item_no = sel_item_no
        self.refresh_by_uid(uid)

    def get_battle_flag_page_tab_btn(self):
        tab_count = self.panel.temp_left_tab.tab_list.GetItemCount()
        if tab_count >= TAB_BATTLE_FLAG + 1:
            return self.panel.temp_left_tab.tab_list.GetItem(TAB_BATTLE_FLAG)
        else:
            return None

    def on_init_panel(self, close_cb=None):
        self._close_cb = close_cb
        self._loaded_model_set = set()
        self._on_need_share_model_idx = None
        self._my_uid = global_data.player.uid
        self._cur_uid = None
        self._record_uid_list = OrderedDict()
        self._player_stat_inf = {}
        self._player_detail_inf = {}
        self.cur_show_model_item_no = ()
        self._panel_dict = {}
        self._init_tab = 0
        self._cur_tab = 0
        self._jump_to_sub_tab = None
        self._jump_to_sub_tab_item_no = None
        self._message_data = global_data.message_data
        self.init_tab_data()
        self.tab_widgets = {}
        self.init_left_tab_list()
        self._change_scene()
        self.hide_main_ui()
        return

    def _change_scene(self):
        from logic.gcommon.common_const import scene_const
        from logic.client.const import lobby_model_display_const
        global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_JIEMIAN_COMMON, lobby_model_display_const.MAIN_RANK_SCENE, scene_content_type=scene_const.SCENE_MAIN_RANK)

    def on_delay_init_panel(self, *args, **kwargs):
        if not global_data.player:
            self.close()
            return
        self.init_show_tab()

    def on_click_close_btn(self):
        if self.check_and_remove_record_uid():
            global_data.emgr.on_recover_player_info_ui.emit()
            return
        anim_time = self.panel.temp_left_tab.GetAnimationMaxRunTime('out')
        self.panel.SetTimeOut(anim_time, self.close)
        self.panel.temp_left_tab.PlayAnimation('out')
        for widget in six_ex.values(self.tab_widgets):
            if widget.panel.isVisible():
                widget.on_disappear()

    def on_finalize_panel(self):
        self.on_finalize_scene()
        global_data.message_data.remove_all_intimacy_event_data()
        self.show_main_ui()
        self.tab_list = []
        self._record_uid_list.clear()
        self._record_uid_list = None
        for widget in six_ex.values(self.tab_widgets):
            widget.destroy()

        self.tab_widgets = {}
        if self.left_tab_list:
            self.left_tab_list.destroy()
            self.left_tab_list = None
        if callable(self._close_cb):
            self._close_cb()
        return

    def on_finalize_scene(self):
        ui = global_data.ui_mgr.get_ui('MainRank')
        if ui:
            return
        global_data.emgr.close_model_display_scene.emit()
        global_data.emgr.leave_current_scene.emit()

    def do_hide_panel(self):
        super(PlayerInfoUI, self).do_hide_panel()

    def do_show_panel(self):
        super(PlayerInfoUI, self).do_show_panel()
        self.cur_show_model_item_no = None
        self._change_scene()
        cur_id = self.left_tab_list.get_select_tab_btn_idx()
        if cur_id in SHOW_MODEL_PAGE:
            self._show_model()
        return

    def init_tab_data(self):
        self.tab_list = [{'text': 10055,'widget_cls': PlayerRoleInfoWidget}, {'text': 10057,'widget_cls': PlayerBattleInfoWidget}, {'text': 10059,'widget_cls': PlayerHistoryRecordsWidget}, {'text': 83340,'widget_cls': PlayerMechaMemoryWidget}, {'text': 3214,'widget_cls': PlayerIntimacyWidget}, {'text': 900001,'widget_cls': PlayerCreditWidget,'sys_type': SYSTEM_CREDIT}, {'text': 81701,'widget_cls': PlayerBattleFlagWidget,'widget_init_func': self._init_battle_flag_widget}, {'text': 82077,'widget_cls': PlayerCareerMedalWidget,'sys_type': SYSTEM_CAREER}]

    def refresh_tag_rp(self, *args):
        if self._my_uid == self._cur_uid:
            tab_role_rp = red_point_utils.get_player_info_ui_red()
            red_point_utils.show_red_point_template(self.panel.temp_left_tab.tab_list.GetItem(TAB_PLAYER_INFO).img_red, tab_role_rp)
            tab_credit_rp = red_point_utils.get_credit_reward_rd()
            red_point_utils.show_red_point_template(self.panel.temp_left_tab.tab_list.GetItem(TAB_CREDIT_INFO).img_red, tab_credit_rp, red_point_utils.RED_POINT_LEVEL_30)
            from common.utils.redpoint_check_func import check_func_intimacy_tab
            tab_intimacy_rp = check_func_intimacy_tab()
            red_point_utils.show_red_point_template(self.panel.temp_left_tab.tab_list.GetItem(TAB_INTIMACY_INFO).img_red, tab_intimacy_rp)
        else:
            red_point_utils.show_red_point_template(self.panel.temp_left_tab.tab_list.GetItem(TAB_PLAYER_INFO).img_red, False)

    def init_left_tab_list(self):

        def return_func():
            self.on_click_close_btn()

        def tab_sel_func(index):
            self._cur_tab = index
            to_sub_tab = self._jump_to_sub_tab
            to_item_no = self._jump_to_sub_tab_item_no
            self.update_uid_to_record_list(self._cur_uid, index)
            sys_type = self.tab_list[index].get('sys_type')
            if sys_type and not is_sys_unlocked(sys_type):
                show_sys_unlock_tips(sys_type)
                return False
            else:
                if index in SHOW_MODEL_PAGE:
                    if self.cur_show_model_item_no:
                        global_data.emgr.lobby_set_models_visible_event.emit(True)
                    else:
                        self._show_model()
                elif self.cur_show_model_item_no:
                    self.clear_model_show()
                if index in self.tab_widgets:
                    for ind in self.tab_widgets:
                        widget = self.tab_widgets[ind]
                        if index == ind:
                            widget.on_select(self._player_detail_inf)
                            widget.show()
                            widget.on_appear()
                            if to_sub_tab is not None:
                                widget.jump_to_tab(to_sub_tab, to_item_no)
                        else:
                            widget.hide()

                elif index < len(self.tab_list):
                    widget_cls = self.tab_list[index].get('widget_cls')
                    widget_init_func = self.tab_list[index].get('widget_init_func', self.init_widget)
                    if widget_cls:
                        for ind in self.tab_widgets:
                            cur_widget = self.tab_widgets[ind]
                            if index != ind:
                                cur_widget.hide()

                        widget = widget_init_func(widget_cls)
                        self.tab_widgets[index] = widget
                        widget.show()
                        widget.on_appear()
                        if to_sub_tab is not None:
                            widget.jump_to_tab(to_sub_tab, to_item_no)
                    else:
                        global_data.game_mgr.show_tip(get_text_by_id(10063))
                        return False
                return True

        from logic.gutils.new_template_utils import CommonLeftTabList
        self.left_tab_list = CommonLeftTabList(self.panel.temp_left_tab, self.tab_list, return_func, tab_sel_func)
        for idx, conf in enumerate(self.tab_list):
            if conf.get('sys_type') and not is_sys_unlocked(conf.get('sys_type')):
                tab_btn = self.panel.temp_left_tab.tab_list.GetItem(idx)
                if tab_btn:
                    tab_btn.img_lock.setVisible(True)
                    self.left_tab_list.set_btn_text(tab_btn, '')
                    tab_btn.lab_lock.SetString(get_text_by_id(conf['text']))

        self.refresh_tag_rp()

    def init_widget(self, cls):
        widget = cls(self.panel)
        if self._player_stat_inf:
            widget.on_player_stat_inf(self._player_stat_inf)
        if self._player_detail_inf:
            widget.on_refresh_player_detail_inf(self._player_detail_inf)
        return widget

    def _init_battle_flag_widget(self, *args):
        widget = PlayerBattleFlagWidget(self, self.panel)
        return widget

    def init_show_tab(self):
        self.left_tab_list.select_tab_btn(self._init_tab)
        self._jump_to_sub_tab = None
        self._jump_to_sub_tab_item_no = None
        return

    def refresh_by_uid(self, uid):
        history_ui_list = ('MutiOccupyStatisticsShareUI', 'FlagStatisticsShareUI',
                           'CrownStatisticsShareUI', 'DeathStatisticsShareUI', 'FFAStatisticsShareUI',
                           'GVGStatisticsShareUI', 'ImproviseHistoryStatUI', 'EndStatisticsShareUI',
                           'DeathEndTransitionUI', 'ArmRaceStatisticsShareUI', 'OccupyStatisticsShareUI',
                           'CrystalEndStatisticsShareUI', 'ADCrystalEndStatisticsShareUI',
                           'TrainEndStatisticsShareUI', 'GoldenEggEndStatisticsShareUI',
                           'GooseBearEndStatisticsShareUI')
        for ui_name in history_ui_list:
            global_data.ui_mgr.close_ui(ui_name)

        self._cur_uid = uid
        self.on_reset_widget_states()
        self.push_uid_to_record_list(uid, self._cur_tab)
        show = True if uid == global_data.player.uid else False
        player_inf = self._message_data.get_player_detail_inf(self._cur_uid)
        if player_inf and time.time() - player_inf['save_time'] < 300:
            self.on_refresh_player_detail_inf(player_inf)
        else:
            global_data.player.request_player_detail_inf(self._cur_uid)
            self.left_tab_list.show_tab(TAB_MECHA_CAREER, show)
        stat_inf = self._message_data.get_player_stat_inf(self._cur_uid)
        if stat_inf and time.time() - stat_inf['save_time'] < 300:
            self.on_player_stat_inf(stat_inf)
        else:
            global_data.player.request_player_stat_info(self._cur_uid, global_data.player.get_battle_season())
        self.left_tab_list.show_tab(TAB_CREDIT_INFO, show)
        self.left_tab_list.show_tab(TAB_BATTLE_FLAG, show)
        self.left_tab_list.show_tab(TAB_CAREER_MEDAL, show)

    def push_uid_to_record_list(self, uid, cur_tab):
        if uid in self._record_uid_list:
            self._record_uid_list.pop(uid)
        self._record_uid_list[uid] = cur_tab

    def pop_uid_from_record_list(self, uid):
        if len(self._record_uid_list) <= 0:
            return
        if uid == six_ex.keys(self._record_uid_list)[-1]:
            self._record_uid_list.pop(uid)

    def update_uid_to_record_list(self, uid, cur_tab):
        self._record_uid_list[uid] = cur_tab

    def check_and_remove_record_uid(self):
        self.pop_uid_from_record_list(self._cur_uid)
        if len(self._record_uid_list) <= 0:
            return False
        else:
            last_uid = six_ex.keys(self._record_uid_list)[-1]
            last_tab = self._record_uid_list[last_uid]
            self.cur_show_model_item_no = None
            self.clear_model_show()
            self.refresh_by_uid(last_uid)
            self.left_tab_list.select_tab_btn(last_tab)
            return True
            return

    def on_player_stat_inf(self, stat_inf):
        if stat_inf[U_ID] != self._cur_uid:
            return
        self._player_stat_inf = stat_inf
        for widget in six_ex.values(self.tab_widgets):
            widget.on_player_stat_inf(stat_inf)

    def on_refresh_player_detail_inf(self, player_inf):
        if player_inf[U_ID] != self._cur_uid:
            return
        self._player_detail_inf = player_inf
        for widget in six_ex.values(self.tab_widgets):
            widget.on_refresh_player_detail_inf(player_inf)

        if self._init_tab in SHOW_MODEL_PAGE and not self.cur_show_model_item_no:
            self._show_model()
        self.refresh_tag_rp()
        self.left_tab_list.show_tab(TAB_MECHA_CAREER, self.get_can_show_mecha_career(player_inf))

    def get_can_show_mecha_career(self, player_inf):
        from logic.gcommon.common_const.ui_operation_const import REVEAL_MECHA_MEMORY_DEFAULT
        if self._cur_uid == global_data.player.uid:
            return True
        else:
            reveal_ = REVEAL_MECHA_MEMORY_DEFAULT
            val = player_inf.get(DETAIL_INFO_REVEAL_MECHA_MEMORY, None)
            if val is not None:
                from logic.entities.avatarmembers.impUserSetting import deserialize_setting_2_val
                reveal_ = deserialize_setting_2_val(val)
                if not isinstance(reveal_, bool):
                    reveal_ = REVEAL_MECHA_MEMORY_DEFAULT
            else:
                reveal_ = REVEAL_MECHA_MEMORY_DEFAULT
            return not reveal_
            return

    def on_reset_widget_states(self):
        for widget in six_ex.values(self.tab_widgets):
            widget.on_reset_states()

    def _show_model(self):
        self.panel.stopActionByTag(self.DELAY_TAG)
        self.panel.DelayCallWithTag(self.DELAY_TIME, self._do_show_model, self.DELAY_TAG)

    def _do_show_model(self):
        if not self.panel or not self.panel.isVisible() or self.left_tab_list.get_select_tab_btn_idx() not in SHOW_MODEL_PAGE and self._on_need_share_model_idx is None:
            return
        else:
            if not self._player_detail_inf:
                return
            is_mine = True if self._cur_uid == global_data.player.uid else False
            if is_mine:
                mecha_id = global_data.player.get_lobby_selected_mecha_id()
                mecha_pose_dict = global_data.player.get_mecha_pose()
                is_apply = global_data.player.is_apply_mecha_pose()
                mecha_item_id = battle_id_to_mecha_lobby_id(mecha_id)
                mecha_item_no = global_data.player.get_mecha_fashion(mecha_item_id)
                mecha_pose = skin_define_utils.get_mecha_gesture_pose(mecha_item_id, is_apply, mecha_pose_dict)
                role_id = global_data.player.get_role()
                item_data = global_data.player.get_item_by_no(role_id)
                fashion_data = item_data.get_fashion()
            else:
                is_apply = self._player_detail_inf.get(item_const.MECHA_LOBBY_POSE_SHOW, False)
                mecha_item_no = self._player_detail_inf.get(item_const.MECHA_LOBBY_FASHION_KEY, None)
                lobby_mecha_id = self._player_detail_inf.get(item_const.MECHA_LOBBY_ID_KEY, 101008001)
                mecha_pose_dict = self._player_detail_inf.get(item_const.MECHA_LOBBY_POSE, {})
                mecha_pose = skin_define_utils.get_mecha_gesture_pose(lobby_mecha_id, is_apply, mecha_pose_dict)
                if mecha_item_no is None:
                    mecha_item_no = lobby_mecha_id
                fashion_data = self._player_detail_inf.get(item_const.INF_ROLE_FASHION_KEY, {})
            role_item_no = fashion_data.get(item_const.FASHION_POS_SUIT, 201001100)
            role_head_no = fashion_data.get(item_const.FASHION_POS_HEADWEAR, None)
            bag_id = fashion_data.get(item_const.FASHION_POS_BACK, None)
            suit_id = fashion_data.get(item_const.FASHION_POS_SUIT_2, None)
            other_pendants = [ fashion_data.get(pos) for pos in item_const.FASHION_OTHER_PENDANT_LIST ]
            if role_item_no <= 0 or mecha_item_no <= 0:
                return
            model_item_no = [role_item_no, mecha_item_no]
            pet_id, pet_level = (None, None)
            if is_mine:
                pet_id = global_data.player.get_choosen_pet()
                pet_item = global_data.player.get_item_by_no(pet_id)
                pet_level = pet_item.level if pet_item else 1
            else:
                if 'pet_info' in self._player_detail_inf:
                    pet_id = self._player_detail_inf['pet_info'].get('pet_id', None)
                    pet_level = self._player_detail_inf['pet_info'].get('level', None)
                if pet_id:
                    model_item_no.append('{}{}'.format(pet_id, pet_level))
                if self.cur_show_model_item_no == model_item_no:
                    return
            self.cur_show_model_item_no = model_item_no
            role_model_data = lobby_model_display_utils.get_lobby_model_data(role_item_no, head_id=role_head_no, bag_id=bag_id, suit_id=suit_id, other_pendants=other_pendants, is_get_player_data=is_mine)
            for data in role_model_data:
                data['model_scale'] = data.get('model_scale', 1.0) * const.ROLE_SCALE
                data['off_euler_rot'][1] = const.ROLE_ROTATION_Y
                data['ignore_chuchang_sfx'] = True
                if not is_mine and fashion_data.get(item_const.FASHION_POS_WEAPON_SFX):
                    data['improved_skin_sfx_id'] = fashion_data[item_const.FASHION_POS_WEAPON_SFX]

            if pet_id:
                from common.cfg import confmgr
                pet_model_data = lobby_model_display_utils.get_lobby_model_data(pet_id, pet_level=pet_level)
                for data in pet_model_data:
                    data['model_scale'] = const.PET_SCALE * confmgr.get('c_pet_info', str(pet_id), 'human_scale', default=1.0)
                    data['off_euler_rot'][1] = const.PET_ROTATION_Y
                    data['off_position'] = const.PET_OFF_POSITION

                role_model_data.extend(pet_model_data)
            mecha_model_data = lobby_model_display_utils.get_lobby_model_data(mecha_item_no, is_get_player_data=is_mine)
            for data in mecha_model_data:
                data['skin_id'] = mecha_item_no
                if mecha_pose:
                    data['show_anim'] = iutils.get_lobby_item_res_path(mecha_pose, get_main_skin_id(mecha_item_no))
                data['model_scale'] = data.get('model_scale', 1.0) * const.MECHA_SCALE
                data['off_euler_rot'][1] = const.MECHA_ROTATION_Y
                if is_mine:
                    data['decal_list'] = global_data.player.get_mecha_decal().get(str(get_main_skin_id(mecha_item_no)), [])
                    data['color_dict'] = global_data.player.get_mecha_color().get(str(mecha_item_no), {})
                else:
                    skin_define_data = self._player_detail_inf.get(item_const.MECHA_LOBBY_CUSTOM_SKIN_KEY, {})
                    if skin_define_data:
                        data['decal_list'] = skin_define_data.get('decal', [])
                        data['color_dict'] = skin_define_data.get('color', {})
                sfx_key = self._player_detail_inf.get(item_const.MECHA_LOBBY_WP_SFX_KEY)
                if not is_mine and sfx_key is not None and sfx_key > 0:
                    data['shiny_weapon_id'] = self._player_detail_inf.get(item_const.MECHA_LOBBY_WP_SFX_KEY)

            global_data.emgr.change_model_display_scene_item_ex.emit(mecha_model_data, role_model_data, create_callback=self._on_load_model_success)
            self._loaded_model_set = set()
            return

    def _on_load_model_success(self, model):
        if self.panel and self.panel.isVisible():
            if self.left_tab_list:
                cur_id = self.left_tab_list.get_select_tab_btn_idx()
                if cur_id not in SHOW_MODEL_PAGE and self._on_need_share_model_idx is None:
                    self.clear_model_show()
        self._loaded_model_set.add(model.get_unique_id())
        if self.is_all_model_loaded():
            self.panel and self.panel.SetTimeOut(0.1, lambda : self.notify_share_model_ok(), tag=20210207)
        return

    def is_all_model_loaded(self):
        return self.cur_show_model_item_no and len(self._loaded_model_set) == len(self.cur_show_model_item_no)

    def share_page_require_model_show(self, index):
        self._on_need_share_model_idx = index
        if index is not None:
            if not self.cur_show_model_item_no:
                self._do_show_model()
            else:
                global_data.emgr.lobby_set_models_visible_event.emit(True)
                self.panel.SetTimeOut(0.1, lambda : self.notify_share_model_ok(), tag=20210207)
        else:
            self.clear_model_show()
        return

    def on_click_back_btn(self, btn, touch):
        self.on_click_close_btn()

    def clear_model_show(self):
        global_data.emgr.lobby_set_models_visible_event.emit(False)

    def notify_share_model_ok(self):
        if self.panel and self.panel.isValid():
            if self._on_need_share_model_idx is not None:
                if self.left_tab_list:
                    cur_id = self.left_tab_list.get_select_tab_btn_idx()
                    if cur_id == self._on_need_share_model_idx:
                        self.tab_widgets[cur_id].on_share_model_loaded()
        return

    def get_widget_by_tab(self, page_tab):
        return self.tab_widgets.get(page_tab)

    def on_resolution_changed(self):
        for widget in six_ex.values(self.tab_widgets):
            if hasattr(widget, 'on_resolution_changed') and widget.on_resolution_changed:
                widget.on_resolution_changed()