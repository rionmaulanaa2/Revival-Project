# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/loading/battle_loading.py
from __future__ import absolute_import
import six
import six_ex
from logic.comsys.loading.loading import UILoadingWidget
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.client.const import game_mode_const
import common.utils.timer as timer
from common.const.uiconst import DIALOG_LAYER_BAN_ZORDER, UI_TYPE_EFFECT, DIALOG_LAYER_ZORDER
from common.const import uiconst
from logic.gutils.role_head_utils import init_role_head, set_role_dan, init_privilege_badge, get_head_photo_res_path
from logic.gcommon.const import PRIV_SHOW_BADGE
from logic.gcommon.common_const import rank_const
from logic.gutils.template_utils import init_rank_title, set_ui_show_picture
from logic.gutils.intimacy_utils import get_intimacy_icon_by_type
from logic.gutils.item_utils import get_lobby_item_name, get_skin_rare_path_by_rare, get_item_rare_degree, get_lobby_item_belong_no
from logic.gcommon.item.item_const import DEFAULT_FLAG_FRAME, RARE_DEGREE_1
from random import randint
from logic.gutils import role_skin_utils, mecha_skin_utils
from common.cfg import confmgr
from logic.gutils.dress_utils import mecha_lobby_id_2_battle_id
from common.utils.ui_utils import get_screen_size
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode
from logic.gutils.items_book_utils import get_items_conf_by_config_name
from logic.gcommon import time_utility
TIPS_RANGE = (
 1012, 1046)
FORCE_FIRST_TIP = 1048
TIPS_REFRESH_INTERVAL = 5.0
LAB_MAP_COLOR = {game_mode_const.GAME_MODE_NIGHT_SURVIVAL: '#SW'}
LAB_MODE_COLOR = {game_mode_const.GAME_MODE_NIGHT_SURVIVAL: 12747007}
CHARM_RANK_LV_ICON = (
 'gui/ui_res_2/battle_before/hot_ranking/img_star_rank_1.png',
 'gui/ui_res_2/battle_before/hot_ranking/img_star_rank_2.png',
 'gui/ui_res_2/battle_before/hot_ranking/img_star_rank_3.png')
ENCOURAGE_TIPS_LIST = [
 357, 358, 359, 360, 361]
STANDARD_WIDTH_0 = 1334
STANDARD_INDENT_0 = 28
STANDARD_WIDTH_1 = 1624
STANDARD_INDENT_1 = 42

class BattleLoadingWidget(UILoadingWidget):
    PANEL_CONFIG_NAME = 'battle_before/fight_loading'
    IS_FULLSCREEN = False
    MOUSE_CURSOR_TRIGGER_SHOW = True

    def play_loading_ani(self):
        pass

    def init_bg(self):
        self.bg_ui = global_data.ui_mgr.show_ui('CommonBgUnAdjustUI', 'logic.comsys.common_ui')

    def on_init_panel(self, *args, **kwargs):
        self.init_bg()
        super(BattleLoadingWidget, self).on_init_panel(*args, **kwargs)
        self._is_observe_target_ready = True
        self.tips_refresh_timer = None
        global_data.emgr.need_wait_observed_player_loaded_event += self.set_need_wait_observe_target
        global_data.emgr.scene_camera_target_model_loaded_event += self.scene_observe_target_loaded
        self.init_tips(kwargs.get('map_id', 0))
        global_data.sound_mgr.stop_music()
        return

    def init_tips(self, map_id):
        self.panel.PlayAnimation('tips')
        self._show_map_mode_tips(map_id)
        self.refresh_tips()
        self.tips_refresh_timer = global_data.game_mgr.register_logic_timer(self.refresh_tips, TIPS_REFRESH_INTERVAL, times=-1, mode=timer.CLOCK)

        @self.panel.nd_tips.callback()
        def OnClick(*args):
            self.refresh_tips()
            if self.tips_refresh_timer:
                global_data.game_mgr.unregister_logic_timer(self.tips_refresh_timer)
            self.tips_refresh_timer = global_data.game_mgr.register_logic_timer(self.refresh_tips, TIPS_REFRESH_INTERVAL, times=-1, mode=timer.CLOCK)

    def _show_map_mode_tips(self, map_id):
        if not map_id or int(map_id) < 0:
            self.panel.nd_mode.setVisible(False)
            return
        from common.cfg import confmgr
        map_data_conf = confmgr.get('map_config', str(map_id), default={})
        map_mode = map_data_conf.get('cCMode')
        map_name_text_ids = map_data_conf.get('cMapNameTextIds', [])
        map_mode_text_id = map_data_conf.get('cMapModeTextId')
        map_mode_to_bgs = map_data_conf.get('cMapLoadingBgs')
        if not map_mode or not map_name_text_ids or not map_mode_text_id:
            self.panel.nd_mode.setVisible(False)
            return
        self.panel.nd_mode.setVisible(True)
        text_id_index = 0
        prefix_str = ''
        if len(map_name_text_ids) > 1 and global_data.battle and hasattr(global_data.battle, 'area_id'):
            text_id_index = min(int(global_data.battle.area_id), len(map_name_text_ids)) - 1
            prefix_str = '\xe2\x80\x94'
        sub_title = ''
        if global_data.game_mode and global_data.game_mode.is_night_weather():
            sub_title = get_text_by_id(17020)
        elif global_data.game_mode and global_data.game_mode.is_snow_weather():
            sub_title = get_text_by_id(19497)
        if map_name_text_ids:
            self.panel.lab_map.SetString(''.join([prefix_str, get_text_by_id(map_name_text_ids[text_id_index]), sub_title]))
        if map_mode_to_bgs:
            text_id_index = min(len(map_mode_to_bgs) - 1, text_id_index)
            self.bg_ui.img_bg.SetDisplayFrameByPath('', map_mode_to_bgs[text_id_index], force_sync=True)
        if map_mode in LAB_MAP_COLOR:
            self.panel.lab_map.SetColor(LAB_MAP_COLOR[map_mode])
        self.panel.lab_mode.SetString(map_mode_text_id)
        if map_mode in LAB_MODE_COLOR:
            self.panel.lab_mode.SetColor(LAB_MODE_COLOR[map_mode])
        if len(map_name_text_ids) > 1:
            self.panel.PlayAnimation('show_mode')
        old_sz = self.panel.bar_lab_mode.getPreferredSize()
        self.panel.bar_lab_mode.SetContentSize(self.panel.lab_mode.getTextContentSize().width + 100, old_sz.height)

    def update_percent(self, value):
        value = self.get_limited_percent(value)
        if self.panel:
            self.panel.lab_loading_time.SetString('%d%%' % value)

    def loading_init(self):
        self.update_percent(0)

    def can_close(self):
        return super(BattleLoadingWidget, self).can_close() and self._is_observe_target_ready

    def set_need_wait_observe_target(self, target_id):
        self._is_observe_target_ready = False

    def scene_observe_target_loaded(self):
        self._is_observe_target_ready = True
        if not self.need_wait_scene_finish_detail():
            self.finish_loading()

    def init_teammate_widget(self, teammate_dict):
        pass

    def on_finalize_panel(self):
        global_data.ui_mgr.close_ui('CommonBgUnAdjustUI')
        super(BattleLoadingWidget, self).on_finalize_panel()
        if self.tips_refresh_timer:
            global_data.game_mgr.unregister_logic_timer(self.tips_refresh_timer)
            self.tips_refresh_timer = None
        global_data.emgr.battle_loading_finished_event.emit()
        return

    def refresh_tips(self, force_tips_id=None):
        if force_tips_id:
            self.panel.lab_tips.SetString(force_tips_id)
        else:
            self.panel.lab_tips.SetString(self.get_random_tips())

    def get_random_tips(self):
        from random import randint
        text_id = randint(TIPS_RANGE[0], TIPS_RANGE[1])
        if text_id == 1020:
            text_id = 1051
        return get_text_by_id(text_id)


class ScreenSnapShotBattleLoadingWidget(BattleLoadingWidget):
    PANEL_CONFIG_NAME = 'battle_before/fight_loading_gvg'
    IS_FULLSCREEN = False

    def init_bg(self):
        self.panel.PlayAnimation('begin')
        ui = global_data.ui_mgr.get_ui('ScreenSnapShotLoadingBgUI')
        if ui:
            ui_context = ui.get_context()
            if ui_context == 'GVGEnterLoading':
                global_data.sound_mgr.play_ui_sound('ui_gvg_start')
        self.bg = ui

    def init_tips(self, map_id):
        self.panel.PlayAnimation('continue')
        self.panel.PlayAnimation('continue_2')
        self.panel.PlayAnimation('continue_3')

    def _show_map_mode_tips(self, map_id):
        pass

    def refresh_tips(self, force_tips_id=None):
        pass

    def on_finalize_panel(self):
        global_data.ui_mgr.close_ui('ScreenSnapShotLoadingBgUI')
        super(ScreenSnapShotBattleLoadingWidget, self).on_finalize_panel()

    def check_close(self):
        if self.is_valid() and self.can_close():

            def _cb():
                if self.is_valid():
                    self.close()

            self.panel.PlayAnimation('end_loading')
            max_time = self.panel.GetAnimationMaxRunTime('end_loading')
            self.panel.DelayCall(max_time, _cb)
            return True
        return False


class CloneBattleLoadingWidget(BattleLoadingWidget):
    PANEL_CONFIG_NAME = 'battle_clone/clone_loading_progress'
    IS_FULLSCREEN = False

    def init_bg(self):
        self.bg_ui = global_data.ui_mgr.show_ui('CloneLoadingUI', 'logic.comsys.battle.Clone')
        self.bg_ui.set_progress_widget(self)
        self.bg_ui.play_animation()

    def on_finalize_panel(self):
        global_data.ui_mgr.close_ui('CloneLoadingUI')
        super(CloneBattleLoadingWidget, self).on_finalize_panel()

    def update_percent(self, value):
        value = self.get_limited_percent(value)
        if self.panel:
            self.panel.lab_time.SetString('%d%%' % value)

    def init_tips(self, map_id):
        pass

    def _show_map_mode_tips(self, map_id):
        pass


class GVGLoadingWidget(BattleLoadingWidget):
    PANEL_CONFIG_NAME = 'battle_gvg/gvg_loading'
    IS_FULLSCREEN = True
    DLG_ZORDER = DIALOG_LAYER_BAN_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_TYPE = UI_TYPE_EFFECT

    def on_init_panel(self, *args, **kwargs):
        super(GVGLoadingWidget, self).on_init_panel(*args, **kwargs)

    def process_event(self, is_bind):
        super(GVGLoadingWidget, self).process_event(is_bind)
        emgr = global_data.emgr
        econf = {'gvg_player_loading_update': self.update_player_load_prog
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def play_loading_ani(self):
        pass

    def init_bg(self):
        from logic.comsys.battle.gvg.GVGLoadingUI import GVGLoadingUI
        self.bg_ui = GVGLoadingUI(self.panel)
        self.bg_ui.on_init_panel()
        global_data.sound_mgr.play_ui_sound('ui_gvg_start')

    def init_tips(self, map_id):
        pass

    def _show_map_mode_tips(self, map_id):
        pass

    def refresh_tips(self, force_tips_id=None):
        pass

    def update_percent(self, value):
        value = self.get_limited_percent(value)
        self.bg_ui.update_percent(value)
        global_data.battle and global_data.battle.report_soul_load_prog(value)

    def update_player_load_prog(self, soul_id, value):
        self.bg_ui.update_percent(value, soul_id)


class DuelLoadingWidget(BattleLoadingWidget):
    PANEL_CONFIG_NAME = 'battle_duel/battle_duel_loading'
    IS_FULLSCREEN = True
    DLG_ZORDER = DIALOG_LAYER_BAN_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_TYPE = UI_TYPE_EFFECT

    def on_init_panel(self, *args, **kwargs):
        super(DuelLoadingWidget, self).on_init_panel(*args, **kwargs)

    def process_event(self, is_bind):
        super(DuelLoadingWidget, self).process_event(is_bind)
        emgr = global_data.emgr
        econf = {'gvg_player_loading_update': self.update_player_load_prog,
           'custom_loading_close_event': self.check_close
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def play_loading_ani(self):
        pass

    def init_bg(self):
        from logic.comsys.battle.Duel.DuelLoadingUI import DuelLoadingUI
        self.bg_ui = DuelLoadingUI(self.panel)
        self.bg_ui.on_init_panel()
        global_data.sound_mgr.play_ui_sound('ui_gvg_start')

    def init_tips(self, map_id):
        pass

    def _show_map_mode_tips(self, map_id):
        pass

    def refresh_tips(self, force_tips_id=None):
        pass

    def can_close(self):
        loading_end = super(DuelLoadingWidget, self).can_close()
        if loading_end:
            if global_data.battle:
                return global_data.battle.is_can_close_loading()
            else:
                return False

    def update_percent(self, value):
        value = self.get_limited_percent(value)
        self.bg_ui.update_percent(value)
        global_data.battle and global_data.battle.report_soul_load_prog(value)

    def update_player_load_prog(self, soul_id, value):
        self.bg_ui.update_percent(value, soul_id)


class BanPickLoadingWidget(BattleLoadingWidget):
    PANEL_CONFIG_NAME = 'lobby/bp_choose_loading'
    IS_FULLSCREEN = True
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_TYPE = UI_TYPE_EFFECT

    def on_init_panel(self, *args, **kwargs):
        super(BanPickLoadingWidget, self).on_init_panel(*args, **kwargs)
        from common.cfg import confmgr
        if global_data.battle:
            from common.cfg import confmgr
            bp_mode, bp_area = global_data.battle.get_banpick_para()
            if bp_mode is not None and bp_area is not None:
                play_type_conf = confmgr.get('battle_bp_config', str(global_data.battle.battle_tid), str(bp_mode), default={})
                mode_bg_pic = play_type_conf.get('load_img_path', '')
                name_tid = play_type_conf.get('name_tid', '')
                area_conf_list = play_type_conf.get('area_conf', [])
                if bp_area >= len(area_conf_list):
                    log_error('invalid bp area', area_conf_list, bp_area)
                area_conf = area_conf_list[bp_area]
                map_id = area_conf.get('map_id', 0)
                born_idx = area_conf.get('born_idx', 0)
                img_path = area_conf.get('img_path', 0)
                map_data_conf = confmgr.get('map_config', str(map_id), default={})
                map_mode = map_data_conf.get('cCMode')
                map_name_text_ids = map_data_conf.get('cMapNameTextIds', [])
                map_mode_text_id = map_data_conf.get('cMapModeTextId')
                map_mode_to_bgs = map_data_conf.get('cMapLoadingBgs')
                text_id_index = 0
                prefix_str = ''
                if len(map_name_text_ids) > 1 and global_data.battle and hasattr(global_data.battle, 'area_id'):
                    text_id_index = min(int(global_data.battle.area_id), len(map_name_text_ids)) - 1
                if map_mode_to_bgs:
                    text_id_index = min(len(map_mode_to_bgs) - 1, text_id_index)
                self.panel.lab_mode.SetString(name_tid)
                self.panel.lab_map.SetString(self.get_born_area_name(map_id, born_idx))
                self.panel.img_mode.SetDisplayFrameByPath('', mode_bg_pic, force_sync=True)
                self.panel.img_map.SetDisplayFrameByPath('', map_mode_to_bgs[text_id_index], force_sync=True)
        return

    def get_born_area_name(self, map_id, born_idx):
        from common.cfg import confmgr
        map_config = confmgr.get('map_config')
        map_info = map_config.get(str(map_id))
        if map_info is None:
            return ''
        else:
            born_list = map_info.get('bornList')
            if not born_list:
                return ''
            if born_idx == -1:
                return get_text_by_id(608159)
            born_idx = born_idx if 0 <= born_idx <= len(born_list) - 1 else None
            if born_idx is None:
                return ''
            return get_text_by_id(born_list[born_idx])

    def init_bg(self):
        pass

    def _show_map_mode_tips(self, map_id):
        pass

    def on_finalize_panel(self):
        super(BanPickLoadingWidget, self).on_finalize_panel()


class PlayerListLoadingWidget(BattleLoadingWidget):
    PANEL_CONFIG_NAME = 'battle_loading/bg_battle_loading'
    IS_FULLSCREEN = True
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_TYPE = UI_TYPE_EFFECT

    def on_init_panel(self, *args, **kwargs):
        self.group_player_eids_dict = {}
        self.player_eid_2_prog_ui = {}
        self.soul_loading_data = {}
        self.default_show_role = 0
        self.hot_keylist = ['summon_call_mecha', 'switch_setting_ui', 'move_forward', 'move_backward', 'move_left', 'move_right', 'tdm_open_weapon']
        if not global_data.battle:
            return
        else:
            self.is_in_spectate = global_data.player and global_data.player.is_in_global_spectate()
            self.init_player_list_widget()
            self.init_encourage_btn()
            self.guangmu_id = None
            if global_data.player and not global_data.player.is_in_global_spectate():
                self.guangmu_id = global_data.player.get_selected_guangmu()
            self.guangmu_sound_id = None
            self.cur_guangmu_item = None
            self.panel.btn_light.setVisible(bool(self.guangmu_id))
            self.guangmu_config_dict = get_items_conf_by_config_name('GuangmuConfig')
            self.panel.btn_light.BindMethod('OnClick', self.on_click_btn_guangmu)
            super(PlayerListLoadingWidget, self).on_init_panel(*args, **kwargs)
            self.panel.PlayAnimation('loop')
            self.block_pc_hot_keys(True)
            return

    def on_finalize_panel(self):
        super(PlayerListLoadingWidget, self).on_finalize_panel()
        self.block_pc_hot_keys(False)
        self.soul_loading_data = {}
        self.group_player_eids_dict = {}
        self.player_eid_2_prog_ui = {}
        self.cur_guangmu_item = None
        self.hot_keylist = []
        if self.guangmu_sound_id:
            global_data.sound_mgr.stop_playing_id(self.guangmu_sound_id)
            self.guangmu_sound_id = None
        return

    def process_event(self, is_bind):
        super(PlayerListLoadingWidget, self).process_event(is_bind)
        emgr = global_data.emgr
        econf = {'on_try_encourage_teammates_event': self.on_try_encourage_teammates,
           'on_play_guangmu': self.on_play_guangmu,
           'player_loading_prog_change_event': self.on_player_loading_prog_change,
           'all_member_ready_event': self.on_all_member_ready
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_all_member_ready(self):
        if not self.need_wait_scene_finish_detail():
            self.finish_loading()

    def can_close(self):
        if global_data.player and global_data.player.is_in_global_spectate():
            return super(PlayerListLoadingWidget, self).can_close()
        else:
            return super(PlayerListLoadingWidget, self).can_close() and global_data.battle and global_data.battle.is_all_member_ready()

    def init_bg(self):
        pass

    def init_tips(self, map_id):
        player_nums = []
        for group_id, group_data in six.iteritems(self.group_loading_dict):
            player_nums.append(len(group_data))

        if 5 in player_nums:
            self.panel.lab_match.SetPosition('50%-526', '50%0')
            self.panel.nd_tips.SetPosition('50%522', '50%0')
        elif 6 in player_nums:
            self.panel.lab_match.SetPosition('50%-625', '50%0')
            self.panel.nd_tips.SetPosition('50%636', '50%0')
        else:
            self.panel.lab_match.SetPosition('50%-526', '50%0')
            self.panel.nd_tips.SetPosition('50%522', '50%0')
        self._show_map_mode_tips(map_id)

    def _show_map_mode_tips(self, map_id):
        if not map_id or map_id < 0:
            self.panel.lab_match.setVisible(False)
            return
        from common.cfg import confmgr
        map_data_conf = confmgr.get('map_config', str(map_id), default={})
        map_mode = map_data_conf.get('cCMode')
        map_name_text_ids = map_data_conf.get('cMapNameTextIds', [])
        map_mode_text_id = map_data_conf.get('cMapModeTextId')
        if not map_mode or not map_name_text_ids or not map_mode_text_id:
            self.panel.lab_match.setVisible(False)
            return
        self.panel.lab_match.setVisible(True)
        self.panel.lab_match.SetString(map_mode_text_id)
        text_id_index = 0
        if len(map_name_text_ids) > 1 and global_data.battle and hasattr(global_data.battle, 'area_id'):
            text_id_index = min(int(global_data.battle.area_id), len(map_name_text_ids)) - 1
        sub_title = ''
        if global_data.game_mode and global_data.game_mode.is_night_weather():
            sub_title = get_text_by_id(17020)
        elif global_data.game_mode and global_data.game_mode.is_snow_weather():
            sub_title = get_text_by_id(19497)
        if map_name_text_ids:
            self.panel.lab_map.SetString(''.join([get_text_by_id(map_name_text_ids[text_id_index]), sub_title]))

    def refresh_tips(self, force_tips_id=None):
        pass

    def loading_init(self):
        if global_data.player:
            self.on_player_loading_prog_change(global_data.player.id, 0)

    def loading_end(self):
        if global_data.player:
            self.on_player_loading_prog_change(global_data.player.id, 100)

    def update_percent(self, value):
        value = self.get_limited_percent(value)
        global_data.battle and global_data.battle.report_soul_load_prog(value)
        global_data.player and self.on_player_loading_prog_change(global_data.player.id, value)

    def on_player_loading_prog_change(self, soul_id, value):
        lab_loading = self.player_eid_2_prog_ui.get(soul_id, None)
        lab_loading and lab_loading.isValid() and lab_loading.SetString('{}%'.format(value))
        return

    def init_encourage_btn(self):

        @self.panel.btn_click.unique_callback()
        def OnClick(*args):
            self.on_click_btn_encourage()

        self.panel.list_head.DeleteAllSubItem()
        if self.is_in_spectate:
            self.panel.list_head.setVisible(False)
            self.panel.btn_click.setVisible(False)
            return
        else:
            my_group_id = global_data.battle.get_loading_group_id()
            if my_group_id is None:
                return
            encouraged_players = global_data.battle.get_group_encourage_dict().get(my_group_id)
            if not encouraged_players:
                self.panel.lab_tips.SetString('')
                return
            for player_eid in encouraged_players:
                player_info = self.group_loading_dict.get(my_group_id, {}).get(player_eid, {})
                if not player_info:
                    continue
                item = self.panel.list_head.AddTemplateItem()
                head_photo = player_info.get('head_photo')
                res_path = get_head_photo_res_path(head_photo)
                item.icon_head.SetDisplayFrameByPath('', res_path)

            if len(encouraged_players) == len(self.group_loading_dict.get(my_group_id)):
                self.panel.btn_click.SetEnable(False)
            if len(encouraged_players) <= 0:
                self.panel.lab_tips.SetString('')
            else:
                encouraged_cnt = len(encouraged_players)
                tips_cnt = len(ENCOURAGE_TIPS_LIST)
                tip_text = ENCOURAGE_TIPS_LIST[(encouraged_cnt - 1) % tips_cnt]
                self.panel.lab_tips.SetString(tip_text)
            return

    def on_click_btn_encourage(self):
        if not global_data.player:
            return
        if global_data.player.is_in_global_spectate():
            return
        global_data.battle and global_data.battle.try_encourage_teammates()
        self.panel.PlayAnimation('show_hand')
        self.panel.btn_click.SetSelect(True)

    def on_try_encourage_teammates(self, soul_id, group_id, tip_text_id, all_encourage):
        player_info = self.group_loading_dict.get(group_id, {}).get(soul_id, {})
        if not player_info:
            return
        head_photo = player_info.get('head_photo')
        item = self.panel.list_head.AddTemplateItem()
        res_path = get_head_photo_res_path(head_photo)
        item.icon_head.SetDisplayFrameByPath('', res_path)
        item.PlayAnimation('show')
        if tip_text_id > 0:
            self.panel.lab_tips.SetString(tip_text_id)
        if all_encourage:
            self.panel.btn_click.SetEnable(False)

    def on_click_btn_guangmu(self, *args):
        self.guangmu_id and global_data.battle and global_data.battle.try_show_guangmu(self.guangmu_id)
        self.panel.PlayAnimation('show_light')

    def on_play_guangmu(self, soul_id, guangmu_id, next_play_guangmu_time):
        guangmu_left_time = next_play_guangmu_time - time_utility.time()
        if guangmu_left_time <= 0:
            return
        else:
            global_data.game_mgr.delay_exec(guangmu_left_time, self.on_guangmu_finish)
            self.panel.btn_light.SetEnable(False)
            guangmu_config = self.guangmu_config_dict.get(str(guangmu_id), {})
            if not guangmu_config:
                return
            if self.cur_guangmu_item:
                self.cur_guangmu_item.StopAnimation_csb('show', True)
                self.cur_guangmu_item = None
            group_id = self.player_eid_2_group_id[soul_id]
            is_group_1 = group_id == global_data.battle.get_loading_group_id()
            item_list = self.panel.list_item_1 if is_group_1 else self.panel.list_item_2
            group_player = self.group_player_eids_dict.get(group_id, [])
            if soul_id in group_player:
                player_idx = group_player.index(soul_id) if 1 else 0
                ui_item = item_list.GetItem(player_idx)
                flag_guangmu_path = ui_item.nd_guangmu.guangmu_item or guangmu_config.get('loading_flag_vx_path')
                if flag_guangmu_path:
                    global_data.uisystem.load_template_create(flag_guangmu_path, parent=ui_item.nd_guangmu, name='guangmu_item')
            if ui_item.nd_guangmu.guangmu_item:
                self.cur_guangmu_item = ui_item.nd_guangmu.guangmu_item
                self.cur_guangmu_item.PlayAnimation('show')
            bg_nd = self.panel.nd_guangmu_up if is_group_1 else self.panel.nd_guangmu_down
            if self.panel.nd_guangmu_up.guangmu_item:
                self.panel.nd_guangmu_up.guangmu_item.RemoveFromParent()
            if self.panel.nd_guangmu_down.guangmu_item:
                self.panel.nd_guangmu_down.guangmu_item.RemoveFromParent()
            bg_guangmu_path = guangmu_config.get('loading_bg_vx_path')
            if bg_guangmu_path:
                global_data.uisystem.load_template_create(bg_guangmu_path, parent=bg_nd, name='guangmu_item')
            if bg_nd.guangmu_item:
                bg_nd.setVisible(True)
                bg_nd.guangmu_item.PlayAnimation('show')
            sound_name = guangmu_config.get('loading_sound')
            sound_mgr = global_data.sound_mgr
            if self.guangmu_sound_id:
                sound_mgr.stop_playing_id(self.guangmu_sound_id)
                self.guangmu_sound_id = None
            if sound_name:
                self.guangmu_sound_id = sound_mgr.post_event_2d_non_opt(sound_name, None)
            return

    def on_guangmu_finish(self):
        if not self.is_valid or not self.panel:
            return
        else:
            self.panel.btn_light.SetEnable(True)
            if self.panel.nd_guangmu_up.guangmu_item:
                self.panel.nd_guangmu_up.guangmu_item.StopAnimation('show')
                self.panel.nd_guangmu_up.setVisible(False)
            if self.panel.nd_guangmu_down.guangmu_item:
                self.panel.nd_guangmu_down.guangmu_item.StopAnimation('show')
                self.panel.nd_guangmu_down.setVisible(False)
            ui_item_list = self.panel.list_item_1.GetAllItem()
            ui_item_list.extend(self.panel.list_item_2.GetAllItem())
            for item in ui_item_list:
                if item.nd_guangmu.guangmu_item:
                    item.nd_guangmu.guangmu_item.StopAnimation_csb('show', True)

            if self.guangmu_sound_id:
                global_data.sound_mgr.stop_playing_id(self.guangmu_sound_id)
                self.guangmu_sound_id = None
            return

    def init_player_card(self, player_eid, player_info, ui_item):
        self.player_eid_2_prog_ui[player_eid] = ui_item.lab_prog
        if self.is_in_spectate:
            ui_item.lab_prog.SetString('{}%'.format(100))
        else:
            prog = self.soul_loading_data.get(player_eid, 0) or 0
            ui_item.lab_prog.SetString('{}%'.format(prog))
        from logic.gutils.new_template_utils import init_player_loading_card
        init_player_loading_card(self.panel, player_eid, player_info, ui_item, self.get_my_player_eid(), self.on_click_player_card, self.default_show_role)

    def on_click_player_card(self, ui_item, role_visible, mecha_visible):
        ui_item.nd_role_locate.setVisible(role_visible)
        ui_item.temp_level_role.nd_kind.setVisible(role_visible)
        ui_item.img_role_charm_level.setVisible(role_visible)
        ui_item.bar_charm_role.setVisible(role_visible)
        ui_item.lab_role_skin_name.setVisible(role_visible)
        ui_item.icon_relation.setVisible(role_visible)
        ui_item.lab_value.setVisible(role_visible)
        ui_item.nd_mech_locate.setVisible(mecha_visible)
        ui_item.temp_level_mecha.nd_kind.setVisible(mecha_visible)
        ui_item.img_mecha_charm_level.setVisible(mecha_visible)
        ui_item.bar_charm_mecha.setVisible(mecha_visible)
        ui_item.lab_mecha_skin_name.setVisible(mecha_visible)
        ui_item.temp_tier.setVisible(mecha_visible)
        if ui_item.temp_level_role.nd_kind.isVisible() and ui_item.temp_level_role.isVisible():
            ui_item.bar_level_bg.setVisible(True)
        elif ui_item.temp_level_mecha.nd_kind.isVisible() and ui_item.temp_level_mecha.isVisible():
            ui_item.bar_level_bg.setVisible(True)
        else:
            ui_item.bar_level_bg.setVisible(False)

    def init_player_card_list(self, group_id, card_list, new_indent):
        card_list.SetInitCount(len(self.group_player_eids_dict[group_id]))
        card_list.SetHorzIndent(new_indent)
        for idx, ui_item in enumerate(card_list.GetAllItem()):
            player_eid = self.group_player_eids_dict.get(group_id, {})[idx]
            player_info = self.group_loading_dict.get(group_id, {}).get(player_eid, {})
            self.init_player_card(player_eid, player_info, ui_item)

    def init_player_list_widget(self):
        self.soul_loading_data = global_data.battle.get_soul_loading_data()
        self.group_loading_dict = global_data.battle.get_group_loading_dict()
        self.default_show_role = global_data.battle.get_default_show_role()
        if len(self.group_loading_dict) > 2:
            self.init_player_list_widget_common()
        else:
            self.init_player_list_widget_death_like()

    def init_player_list_widget_common(self):
        self.all_player_eids = []
        self.player_eid_2_group_id = {}
        for group_id, group_data in six.iteritems(self.group_loading_dict):
            self.all_player_eids.extend(six_ex.keys(group_data))
            for player_eid in six_ex.keys(group_data):
                self.player_eid_2_group_id[player_eid] = group_id

        player_num_per_side = int((len(self.all_player_eids) + 1) / 2)
        new_indent = self.calc_list_item_indent()
        self.panel.list_item_1.SetInitCount(player_num_per_side)
        self.panel.list_item_1.SetHorzIndent(new_indent)
        ui_item_list = self.panel.list_item_1.GetAllItem()
        left_player_num = len(self.all_player_eids) - player_num_per_side
        if left_player_num > 0:
            self.panel.list_item_2.SetInitCount(left_player_num)
            self.panel.list_item_2.SetHorzIndent(new_indent)
            ui_item_list.extend(self.panel.list_item_2.GetAllItem())
        my_player_eid = self.get_my_player_eid()
        if my_player_eid in self.all_player_eids:
            idx_me = self.all_player_eids.index(my_player_eid)
            if idx_me >= player_num_per_side:
                idx_new = randint(0, player_num_per_side - 1)
                old_eid = self.all_player_eids[idx_new]
                self.all_player_eids[idx_new] = my_player_eid
                self.all_player_eids[idx_me] = old_eid
        idx = 0
        for player_eid in self.all_player_eids:
            group_id = self.player_eid_2_group_id[player_eid]
            player_info = self.group_loading_dict.get(group_id, {}).get(player_eid, {})
            self.init_player_card(player_eid, player_info, ui_item_list[idx])
            idx += 1

    def init_player_list_widget_death_like(self):
        ui_list_dict = {1: self.panel.list_item_1,
           2: self.panel.list_item_2
           }
        self.all_player_eids = []
        self.player_eid_2_group_id = {}
        new_indent = self.calc_list_item_indent()
        for group_id, group_data in six.iteritems(self.group_loading_dict):
            self.all_player_eids.extend(six_ex.keys(group_data))
            for player_eid in six_ex.keys(group_data):
                self.player_eid_2_group_id[player_eid] = group_id

            self.group_player_eids_dict[group_id] = six_ex.keys(group_data)
            self.init_round_group_tips(group_id)
            if len(ui_list_dict) == 1:
                ui_list_key = six_ex.keys(ui_list_dict)[0]
                self.init_player_card_list(group_id, ui_list_dict[ui_list_key], new_indent)
                return
            if group_id == global_data.battle.get_loading_group_id():
                self.init_player_card_list(group_id, self.panel.list_item_1, new_indent)
                ui_list_dict.pop(1)
            else:
                self.init_player_card_list(group_id, self.panel.list_item_2, new_indent)
                ui_list_dict.pop(2)

    @execute_by_mode(True, (game_mode_const.GAME_MODE_TRAIN,))
    def init_round_group_tips(self, group_id):
        if not global_data.battle:
            return
        round = global_data.battle.get_round() + 2
        atk_group = global_data.battle.get_atk_group_id()
        if group_id == global_data.battle.get_loading_group_id():
            nd = self.panel.list_item_1.nd_auto_fit
        else:
            nd = self.panel.list_item_2.nd_auto_fit
        nd.setVisible(True)
        if atk_group == group_id:
            nd.nd_camp.lab_round.SetString(17824)
            nd.nd_camp.lab_round.SetColor('#SB')
            nd.nd_camp.lab_title.SetString(17825)
            nd.nd_camp.lab_title.SetColor('#SB')
        else:
            nd.nd_camp.lab_round.SetString(17824)
            nd.nd_camp.lab_round.SetColor('#SR')
            nd.nd_camp.lab_title.SetString(17826)
            nd.nd_camp.lab_title.SetColor('#SR')

    def block_pc_hot_keys(self, is_block):
        from logic.vscene.parts.ctrl.PCCtrlManager import PCCtrlManager
        for hot_key in self.hot_keylist:
            if is_block:
                PCCtrlManager().block_hotkey(hot_key, 'player_list_loading')
            else:
                PCCtrlManager().unblock_hotkey(hot_key, 'player_list_loading')

    def get_my_player_eid(self):
        if not global_data.player:
            return None
        else:
            if self.is_in_spectate:
                my_player_eid = global_data.player.get_global_spectate_player_id()
            else:
                my_player_eid = global_data.player.id
            return my_player_eid

    def calc_list_item_indent(self):
        from common.utils.cocos_utils import getScreenSize
        sz = getScreenSize()
        cur_width = sz.width
        if cur_width <= STANDARD_WIDTH_0:
            new_indent = STANDARD_INDENT_0
        elif cur_width <= STANDARD_WIDTH_1:
            new_indent = int(14.0 / 290 * cur_width - 36.4)
        else:
            new_indent = STANDARD_INDENT_1
        return new_indent


class SnatchEggPlayerListLoadingWidget(BattleLoadingWidget):
    PANEL_CONFIG_NAME = 'battle_golden_egg/battle_golden_egg_loading'
    IS_FULLSCREEN = True
    DLG_ZORDER = DIALOG_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_TYPE = UI_TYPE_EFFECT
    GLOBAL_EVENT = {'scene_player_setted_event': 'on_player_setted'
       }

    def update_percent(self, value):
        pass

    def init_tips(self, map_id):
        self._show_map_mode_tips(map_id)

    def on_init_panel(self, *args, **kwargs):
        self.group_player_eids_dict = {}
        self.player_eid_2_prog_ui = {}
        self.soul_loading_data = {}
        self.default_show_role = 0
        self.group_idx_dict = {}
        self.group_ready_dict = {}
        self.hot_keylist = ['summon_call_mecha', 'switch_setting_ui', 'move_forward', 'move_backward', 'move_left', 'move_right', 'tdm_open_weapon']
        self.show_group_list = []
        if not global_data.battle:
            return
        self.is_in_spectate = global_data.player and global_data.player.is_in_global_spectate()
        self.init_player_list_widget()
        super(SnatchEggPlayerListLoadingWidget, self).on_init_panel(*args, **kwargs)
        self.block_pc_hot_keys(True)

    def on_finalize_panel(self):
        super(SnatchEggPlayerListLoadingWidget, self).on_finalize_panel()
        self.block_pc_hot_keys(False)
        self.soul_loading_data = {}
        self.group_player_eids_dict = {}
        self.player_eid_2_prog_ui = {}
        self.hot_keylist = []
        self.group_ready_dict = {}
        self.show_group_list = []

    def init_player_list_widget(self):
        self.soul_loading_data = global_data.battle.get_soul_loading_data()
        self.group_loading_dict = global_data.battle.get_group_loading_dict()
        self.default_show_role = global_data.battle.get_default_show_role()
        if not global_data.player:
            return
        self.show_group_list = global_data.battle.get_show_group_list()
        self.init_player_list_widget_common()

    def on_player_setted(self, *args):
        if not self.show_group_list:
            self.show_group_list = global_data.battle.get_show_group_list()
            self.init_player_list_widget_common()
            for soul_id, value in six.iteritems(self.soul_loading_data):
                self.on_player_loading_prog_change(soul_id, value)

    def init_player_list_widget_common(self):
        player = global_data.player
        self.all_player_eids = []
        self.player_eid_2_group_id = {}
        self.panel.list_item.SetInitCount(len(self.group_loading_dict))
        idx = 0
        for group_id in self.show_group_list:
            group_data = self.group_loading_dict.get(group_id, {})
            self.group_idx_dict[group_id] = idx
            self.group_player_eids_dict[group_id] = six_ex.keys(group_data)
            self.panel.list_item.GetItem(idx).lab_state.SetString('WAITING')
            self.init_player_card_list(group_id, self.panel.list_item.GetItem(idx).list_item)
            idx += 1

    def init_player_card_list(self, group_id, card_list):
        card_list.SetInitCount(len(self.group_player_eids_dict[group_id]))
        for idx, ui_item in enumerate(card_list.GetAllItem()):
            player_eid = self.group_player_eids_dict.get(group_id, {})[idx]
            self.player_eid_2_group_id[player_eid] = group_id
            player_info = self.group_loading_dict.get(group_id, {}).get(player_eid, {})
            self.init_player_card(player_eid, player_info, ui_item)

    def init_player_card(self, player_eid, player_info, ui_item):
        self.player_eid_2_prog_ui[player_eid] = ui_item.lab_prog
        if self.is_in_spectate:
            ui_item.lab_prog.SetString('{}%'.format(100))
        else:
            prog = self.soul_loading_data.get(player_eid, 0) or 0
            ui_item.lab_prog.SetString('{}%'.format(prog))
        dan_info = player_info.get('dan_info')
        set_role_dan(ui_item.temp_tier, dan_info)
        char_name = player_info.get('char_name')
        ui_item.lab_name.SetString(char_name)
        if player_eid == self.get_my_player_eid():
            ui_item.bar_name.SetDisplayFrameByPath('', 'gui/ui_res_2/battle_golden_egg/bar_golden_egg_loading_name_0.png')
        else:
            ui_item.bar_name.SetDisplayFrameByPath('', 'gui/ui_res_2/battle_golden_egg/bar_golden_egg_loading_name_2.png')
        priv_lv = player_info.get('priv_lv') or 0
        priv_settings = player_info.get('priv_settings', {}) or {}
        show_badge = priv_settings.get(PRIV_SHOW_BADGE, False)
        if priv_lv > 0 and show_badge:
            init_privilege_badge(ui_item.temp_badge, priv_lv, show_badge)
            ui_item.temp_badge.setVisible(True)
        else:
            ui_item.temp_badge.setVisible(False)
        rank_use_title_dict = player_info.get('rank_use_title_dict') or {}
        rank_info = rank_const.get_rank_use_title(rank_use_title_dict)
        rank_title_type = rank_const.get_rank_use_title_type(rank_use_title_dict)
        init_rank_title(ui_item.temp_title, rank_title_type, rank_info, icon_scale=0.5)

        def hide_title():
            if not self.panel or not self.panel.isValid():
                return
            if not ui_item or not ui_item.isValid():
                return
            if not ui_item.temp_title and not ui_item.temp_title.isValid():
                return
            ui_item.PlayAnimation('hide_title')

        if rank_info and rank_title_type:
            ui_item.temp_title.SetTimeOut(10, hide_title)
        role_skin = player_info.get('role_skin')
        mecha_skin = player_info.get('mecha_skin')
        ui_item.pic.SetDisplayFrameByPath('', 'gui/ui_res_2/item/mecha_skin/{}.png'.format(mecha_skin))
        mecha_skin_weapon_sfx = player_info.get('mecha_skin_weapon_sfx', 0)
        mecha_skin_rare_degree = get_item_rare_degree(mecha_skin, weapon_sfx_item=mecha_skin_weapon_sfx)
        if mecha_skin_rare_degree <= RARE_DEGREE_1:
            ui_item.temp_level.setVisible(False)
        else:
            mecha_skin_lv_icon = get_skin_rare_path_by_rare(mecha_skin_rare_degree)
            ui_item.temp_level.setVisible(True)
            ui_item.temp_level.bar_level.SetDisplayFrameByPath('', mecha_skin_lv_icon)
        role_charm_rank = player_info.get('role_charm_rank')
        mecha_charm_rank = player_info.get('mecha_charm_rank', -1)
        if 0 <= mecha_charm_rank < len(CHARM_RANK_LV_ICON):
            ui_item.img_mecha_charm_level.SetDisplayFrameByPath('', CHARM_RANK_LV_ICON[mecha_charm_rank])
        else:
            ui_item.nd_charm.setVisible(False)

    def get_my_player_eid(self):
        if not global_data.player:
            return None
        else:
            if self.is_in_spectate:
                my_player_eid = global_data.player.get_global_spectate_player_id()
            else:
                my_player_eid = global_data.player.id
            return my_player_eid

    def get_born_area_name(self, map_id, born_idx):
        from common.cfg import confmgr
        map_config = confmgr.get('map_config')
        map_info = map_config.get(str(map_id))
        if map_info is None:
            return ''
        else:
            born_list = map_info.get('bornList')
            if not born_list:
                return ''
            if born_idx == -1:
                return get_text_by_id(608159)
            born_idx = born_idx if 0 <= born_idx <= len(born_list) - 1 else None
            if born_idx is None:
                return ''
            return get_text_by_id(born_list[born_idx])

    def process_event(self, is_bind):
        super(SnatchEggPlayerListLoadingWidget, self).process_event(is_bind)
        emgr = global_data.emgr
        econf = {'player_loading_prog_change_event': self.on_player_loading_prog_change,
           'all_member_ready_event': self.on_all_member_ready
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_all_member_ready(self):
        self.on_all_group_ready()
        if not self.need_wait_scene_finish_detail():
            self.finish_loading()

    def on_all_group_ready(self):
        for group_item in self.panel.list_item.GetAllItem():
            group_item.lab_state.SetString('GO GO GO!')

    def _show_map_mode_tips(self, map_id):
        if not map_id or map_id < 0:
            self.panel.lab_match.setVisible(False)
            return
        from common.cfg import confmgr
        map_data_conf = confmgr.get('map_config', str(map_id), default={})
        map_mode = map_data_conf.get('cCMode')
        map_name_text_ids = map_data_conf.get('cMapNameTextIds', [])
        map_mode_text_id = map_data_conf.get('cMapModeTextId')
        if not map_mode or not map_name_text_ids or not map_mode_text_id:
            self.panel.lab_match.setVisible(False)
            return
        self.panel.lab_match.setVisible(True)
        self.panel.lab_match.SetString(map_mode_text_id)
        text_id_index = 0
        if len(map_name_text_ids) > 1 and global_data.battle and hasattr(global_data.battle, 'area_id'):
            text_id_index = min(int(global_data.battle.area_id), len(map_name_text_ids)) - 1
        sub_title = ''
        if global_data.game_mode and global_data.game_mode.is_night_weather():
            sub_title = get_text_by_id(17020)
        elif global_data.game_mode and global_data.game_mode.is_snow_weather():
            sub_title = get_text_by_id(19497)
        if map_name_text_ids:
            self.panel.lab_map.SetString(''.join([get_text_by_id(map_name_text_ids[text_id_index]), sub_title]))

    def loading_init(self):
        if global_data.player:
            self.on_player_loading_prog_change(global_data.player.id, 0)

    def loading_end(self):
        if global_data.player:
            self.on_player_loading_prog_change(global_data.player.id, 100)

    def update_percent(self, value):
        value = self.get_limited_percent(value)
        global_data.battle and global_data.battle.report_soul_load_prog(value)
        global_data.player and self.on_player_loading_prog_change(global_data.player.id, value)

    def on_player_loading_prog_change(self, soul_id, value):
        lab_loading = self.player_eid_2_prog_ui.get(soul_id, None)
        lab_loading and lab_loading.isValid() and lab_loading.SetString('{}%'.format(value))
        self.soul_loading_data[soul_id] = value
        for gid in six_ex.keys(self.group_loading_dict):
            if self.group_ready_dict.get(gid):
                continue
            self.group_ready_check(gid)

        return

    def group_ready_check(self, group_id):
        if group_id and group_id in self.group_player_eids_dict:
            for sid in self.group_player_eids_dict[group_id]:
                if self.soul_loading_data.get(sid, 0) < 100:
                    return

        if group_id and group_id in self.group_player_eids_dict:
            self.panel.list_item.GetItem(self.group_idx_dict[group_id]).lab_state.SetString('READY')
        self.group_ready_dict[group_id] = True
        for gid in self.group_loading_dict:
            if not self.group_ready_dict.get(gid):
                return

        self.on_all_group_ready()

    def block_pc_hot_keys(self, is_block):
        from logic.vscene.parts.ctrl.PCCtrlManager import PCCtrlManager
        for hot_key in self.hot_keylist:
            if is_block:
                PCCtrlManager().block_hotkey(hot_key, 'player_list_loading')
            else:
                PCCtrlManager().unblock_hotkey(hot_key, 'player_list_loading')

    def can_close(self):
        if global_data.player and global_data.player.is_in_global_spectate():
            return super(SnatchEggPlayerListLoadingWidget, self).can_close()
        else:
            return super(SnatchEggPlayerListLoadingWidget, self).can_close() and global_data.battle and global_data.battle.is_all_member_ready()