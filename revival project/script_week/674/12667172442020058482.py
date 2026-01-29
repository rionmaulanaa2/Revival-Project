# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_display/mecha_memory/MechaMemoryWidget.py
from __future__ import absolute_import
import six
from six.moves import range
from common.cfg import confmgr
from common.uisys.BaseUIWidget import BaseUIWidget
import cc
from common.uisys.BaseUIWidget import BaseUIWidget
from common.cfg import confmgr
from logic.gutils import item_utils
from logic.gutils.mall_utils import mecha_has_owned_by_mecha_id
from logic.gutils.mecha_career_utils import MechaMemoryStatWidget, init_career_titile, get_career_season_name
from logic.comsys.share.ShareTemplateBase import async_disable_wrapper
from logic.gcommon.common_const.web_const import MECHA_MEMORY_ALL_SEASON_MODE, MECHA_MEMORY_OLD_SEASON_MODE

class MechaSimpleInfoProficiencyWidget(BaseUIWidget):

    def __init__(self, parent, panel, mecha_type, uid=None):
        self.global_events = {'update_proficiency_event': self.on_player_update_proficiency
           }
        super(MechaSimpleInfoProficiencyWidget, self).__init__(parent, panel)
        if global_data.player:
            cur_season = global_data.player.get_battle_season()
        else:
            from logic.gcommon.cdata import season_data
            cur_season = season_data.get_cur_battle_season()
        self._cur_battle_season_id = cur_season
        self.is_mine = True if uid is None else False
        self._season = None
        self.cur_season_data = {}
        self.init_parameters()
        self.on_switch_mecha_type(mecha_type)
        return

    def on_switch_mecha_type(self, mecha_type):
        self.init_widget(str(mecha_type))

    def set_season_data(self, season, season_data):
        self._season = season
        self.cur_season_data = season_data
        self.on_switch_mecha_type(self._cur_mecha_type)

    def init_parameters(self):
        self._prof_conf = confmgr.get('proficiency_config', 'Proficiency')
        self._dan_conf = confmgr.get('proficiency_config', 'ProficiencyDan')
        self._mecha_conf = confmgr.get('mecha_conf', 'MechaConfig', 'Content', default=[])
        self._max_dan_lv = len(self._dan_conf)
        self._max_level = len(self._prof_conf)
        self._cur_mecha_type = None
        return

    def init_widget(self, mecha_type):
        if not global_data.player:
            return
        self._cur_mecha_type = mecha_type
        if not self.cur_season_data:
            if self.is_mine:
                level, proficiency = self.get_mecha_season_proficiency(self._cur_mecha_type, self._cur_battle_season_id)
            else:
                level, proficiency = 1, 0
            mecha_name = item_utils.get_mecha_name_by_id(self._cur_mecha_type)
            self.panel.lab_mech.SetString(mecha_name)
            self.on_update_proficiency(mecha_type, level, proficiency)
            return
        level, proficiency = self.get_mecha_season_proficiency(self._cur_mecha_type, self._season)
        mecha_name = item_utils.get_mecha_name_by_id(self._cur_mecha_type)
        self.panel.lab_mech.SetString(mecha_name)
        self.on_update_proficiency(mecha_type, level, proficiency)

    def get_mecha_season_proficiency(self, mecha_id, season):
        mecha_proficiency = self.cur_season_data.get('mecha_proficiency', {}).get(str(mecha_id), [1, 0])
        if self.is_mine and (season == self._cur_battle_season_id or season == MECHA_MEMORY_ALL_SEASON_MODE):
            if global_data.player:
                get_proficiency = global_data.player.get_proficiency if 1 else (lambda _: mecha_proficiency)
                return get_proficiency(mecha_id)
        return mecha_proficiency

    def on_player_update_proficiency(self, mecha_type, level, proficiency, lv_up=False):
        if self.is_mine:
            self.on_update_proficiency(mecha_type, level, proficiency, lv_up)

    def on_update_proficiency(self, mecha_type, level, proficiency, lv_up=False):
        if self._cur_mecha_type != mecha_type:
            return
        if level < self._max_level:
            upgrade_value = self._prof_conf.get(str(level + 1), {}).get('upgrade_value', 0)
        else:
            upgrade_value = self._prof_conf.get(str(level), {}).get('upgrade_value', 0)
            proficiency = upgrade_value
        nd = self.panel
        nd.lab_level.SetString('Lv%d' % level)
        if upgrade_value:
            nd.prog.SetPercent(proficiency * 100.0 / upgrade_value)
        else:
            nd.prog.SetPercent(100)
        dan_lv = self.get_dan_lv(level)
        self.update_nd_dan_lv(nd, dan_lv)

    def update_nd_dan_lv(self, nd, dan_lv, show_dan_level=True):
        if not show_dan_level:
            nd.img_proficiency_level.setVisible(False)
            nd.lab_proficiency_level.setVisible(False)
        else:
            icon_path = self._dan_conf.get(str(dan_lv), {}).get('icon_path', '')
            name = self._dan_conf.get(str(dan_lv), {}).get('name', 0)
            if icon_path:
                nd.img_proficiency_level.SetDisplayFrameByPath('', icon_path)
            if name:
                nd.lab_proficiency_level.SetString(get_text_by_id(name))

    def get_dan_lv(self, level):
        dan_lv = 1
        for dan_lv in range(1, self._max_dan_lv + 1):
            max_level = self._dan_conf[str(dan_lv)]['max_level']
            if level < max_level:
                break

        return dan_lv

    def destroy(self):
        self._prof_conf = None
        self._dan_conf = None
        self.cur_season_data = None
        super(MechaSimpleInfoProficiencyWidget, self).destroy()
        return


class MechaMemoryWidget(BaseUIWidget):

    def __init__(self, parent, panel, mecha_type, puppet_uid=None):
        self.global_events = {'update_proficiency_event': self.on_player_update_proficiency
           }
        super(MechaMemoryWidget, self).__init__(parent, panel)
        self._puppet_uid = puppet_uid
        self._puppet_mecha_dict = {}
        self.is_mine = self._puppet_uid is None
        self._mecha_conf = confmgr.get('mecha_display', 'HangarConfig', 'Content')
        self._story_conf = confmgr.get('mecha_display', 'MechaStory', 'Content')
        self.mecha_type = None
        self.season_data = {}
        self._need_check_all = False
        self._screen_capture_helper = None
        self._share_content = None
        self._cur_battle_season_id = global_data.player.get_battle_season()
        self._show_battle_season_id = self._cur_battle_season_id
        self.prof_widget = MechaSimpleInfoProficiencyWidget(self, self.panel, mecha_type, self._puppet_uid)
        self.share_prof_widget = None
        self.memory_widget = MechaMemoryStatWidget()
        self.share_memory_widget = MechaMemoryStatWidget()
        if self._puppet_uid:
            self.memory_widget.set_uid(self._puppet_uid)
            self.share_memory_widget.set_uid(self._puppet_uid)
        self.memory_widget.set_data_cb(self.on_received_memory_data)
        self.memory_widget.set_data_modify_cb(self.on_modify_memory_data)
        self.share_memory_widget.set_data_modify_cb(self.on_modify_memory_data)
        self.memory_widget.set_node(self.panel.list_lab, self.panel.list_btn)
        self.on_switch_to_mecha_type(mecha_type)
        self.init_widget()
        return

    def destroy(self):
        super(MechaMemoryWidget, self).destroy()
        if self.prof_widget:
            self.prof_widget.destroy()
            self.prof_widget = None
        self.season_data = None
        if self.share_prof_widget:
            self.share_prof_widget.destroy()
            self.share_prof_widget = None
        if self.memory_widget:
            self.memory_widget.destroy()
            self.memory_widget = None
        if self.share_memory_widget:
            self.share_memory_widget.destroy()
            self.share_memory_widget = None
        if self._screen_capture_helper:
            self._screen_capture_helper.destroy()
        self._screen_capture_helper = None
        if self._share_content:
            self._share_content.destroy()
        self._share_content = None
        self.mecha_type = None
        self._mecha_conf = {}
        self._story_conf = {}
        return

    def on_switch_to_mecha_type(self, mecha_type):
        if self.mecha_type == mecha_type:
            return
        self.mecha_type = mecha_type
        if not self.mecha_type:
            return
        if self.memory_widget:
            self.memory_widget.set_mecha_type(self.mecha_type)
        self.init_base_panel()
        self.init_choose_list_array()
        if self.prof_widget:
            self.prof_widget.on_switch_mecha_type(mecha_type)

    def init_base_panel(self):
        self.panel.bar_rank.setVisible(False)
        mecha_name = item_utils.get_mecha_name_by_id(self.mecha_type)
        self.panel.lab_mecha.SetString(mecha_name)
        self.panel.bar_title.lab_title.SetString(get_text_by_id(83256, {'name': mecha_name}))
        self.panel.bar_title2.lab_title.SetString(get_text_by_id(83257, {'name': mecha_name}))

    def init_choose_list_array(self):
        if not global_data.player:
            return
        from logic.gutils.memory_utils import get_memory_record_start_season
        start_season = get_memory_record_start_season()
        seasons_list = list(range(start_season, self._cur_battle_season_id + 1))
        from logic.gutils import template_utils
        if self._cur_battle_season_id not in seasons_list:
            seasons_list.append(self._cur_battle_season_id)
        mode_option = [ {'name': get_career_season_name(s_id),'mode': s_id} for s_id in reversed(seasons_list) ]
        mode_option.append({'name': 83360,'mode': MECHA_MEMORY_ALL_SEASON_MODE})

        def call_back(index):
            option = mode_option[index]
            if self.memory_widget:
                mode = option['mode']
                if mode == MECHA_MEMORY_ALL_SEASON_MODE:
                    self.memory_widget.on_need_show_show_battle_season_id(MECHA_MEMORY_ALL_SEASON_MODE)
                    self._show_battle_season_id = MECHA_MEMORY_ALL_SEASON_MODE
                    self._need_check_all = True
                else:
                    self.memory_widget.on_need_show_show_battle_season_id(option['mode'])
                    self._show_battle_season_id = option['mode']
                    self._need_check_all = False
                self.panel.lab_tips.setVisible(self._show_battle_season_id == MECHA_MEMORY_ALL_SEASON_MODE)
                self.panel.lab_tips.SetString(get_text_by_id(83359, {'season': get_career_season_name(get_memory_record_start_season())}))
                self.memory_widget.refresh()
            self.panel.btn_choose_mecha.lab_bp.SetString(option['name'])

        def close_callback():
            pass

        template_utils.init_common_choose_list_2(self.panel.choose_list_array, self.panel.btn_choose_mecha.icon_arrow, mode_option, call_back, close_cb=close_callback, func_btn=self.panel.btn_choose_mecha, extra_bar_list=[self.panel.bar_choose_list_array])
        call_back(0)

    def init_widget(self):
        self.panel.btn_right.BindMethod('OnClick', self.parent._on_show_next_mecha)
        self.panel.btn_left.BindMethod('OnClick', self.parent._on_show_last_mecha)
        self.panel.btn_share.BindMethod('OnClick', self.parent.on_click_btn_share)

    def show_widget_share_ui(self):
        if not self._screen_capture_helper:
            from logic.comsys.share.ScreenFrameHelper import ScreenFrameHelper
            self._screen_capture_helper = ScreenFrameHelper()
        ui_names = [
         self.__class__.__name__]

        def cb(*args):
            self.update_share_panel_func(self._share_content.panel)
            self._share_content.update_ui_bg_sprite()
            from logic.comsys.share.ShareUI import ShareUI
            share_ui = ShareUI()
            share_ui.set_share_content_raw(self._share_content.get_render_texture(), share_content=self._share_content)
            self.parent.reset_share_btn()

        if self._screen_capture_helper:
            self.parent.update_share_btn(False)
            if not self._share_content:
                tmpl = 'mech_display/career/i_mech_career_share_info'
                from logic.comsys.share.CommonShareCreator import CommonPosterShareCreator
                share_creator = CommonPosterShareCreator()
                share_creator.create(None, tmpl)
                self._share_content = share_creator
            self._screen_capture_helper.set_custom_share_content(self._share_content)
            self._screen_capture_helper.take_screen_shot(ui_names, self.panel, custom_cb=cb, need_share_ui=False, head_nd_name='nd_player_info_1', need_draw_rt=False)
        if not global_data.ui_mgr.get_ui('ShareUI'):
            from logic.comsys.share.ShareUI import ShareUI
            ui = ShareUI()
            ui.clear_choose_list_func()
        return

    @async_disable_wrapper
    def update_share_panel_func(self, panel):
        mecha_type = self.mecha_type
        from logic.gutils.season_utils import get_mecha_best_region_rank
        best_rank = get_mecha_best_region_rank(mecha_type)
        init_career_titile(panel.temp_activity.bar_rank, best_rank)
        if not self.share_memory_widget:
            return
        self.share_memory_widget.set_mecha_type(self.mecha_type)
        self.share_memory_widget.set_node(panel.temp_activity.list_lab, panel.temp_activity.list_btn)
        self.share_memory_widget.on_need_show_show_battle_season_id(self._show_battle_season_id)
        self.share_memory_widget.refresh()
        if not self.share_prof_widget:
            self.share_prof_widget = MechaSimpleInfoProficiencyWidget(self, panel.temp_activity, mecha_type)
        self.share_prof_widget.on_switch_mecha_type(mecha_type)
        self.share_prof_widget.set_season_data(self._show_battle_season_id, self.season_data)
        mecha_name = item_utils.get_mecha_name_by_id(self.mecha_type)
        panel.temp_activity.lab_mech.SetString(mecha_name)
        panel.temp_activity.lab_mecha.SetString(mecha_name)
        panel.temp_activity.btn_choose_mecha.lab_bp.SetString(self.panel.btn_choose_mecha.lab_bp.GetString())
        panel.temp_activity.bar_title.lab_title.SetString(get_text_by_id(83256, {'name': mecha_name}))
        panel.temp_activity.bar_title2.lab_title.SetString(get_text_by_id(83257, {'name': mecha_name}))

    def on_received_memory_data(self, season_id, season_data, fake_init=False):
        if season_id != self._show_battle_season_id:
            return
        if fake_init:
            return
        self.season_data = season_data
        self.prof_widget.set_season_data(self._show_battle_season_id, season_data)
        self.update_title(season_data)

    def on_modify_memory_data(self, season_id, season_data, fake_init, mecha_dict, skill_dict, icon_dict):
        if season_id != self._show_battle_season_id:
            return (mecha_dict, skill_dict, icon_dict)
        else:
            if fake_init:
                return (mecha_dict, skill_dict, icon_dict)
            if not self._need_check_all:
                return (mecha_dict, skill_dict, icon_dict)
            _mecha_conf = confmgr.get('mecha_conf', 'MechaConfig', 'Content', default=[])
            mecha_type = self.mecha_type
            task_statistics_list = _mecha_conf.get(str(mecha_type), {}).get('task_statistics', [])
            from collections import OrderedDict
            new_mecha_dict = OrderedDict()
            for key, value in six.iteritems(mecha_dict):
                new_mecha_dict[key] = value
                if key == 'mecha_fight_time':
                    task_id = task_statistics_list[0]
                    if global_data.player:
                        task_cur_prog = global_data.player.get_task_prog(task_id)
                    else:
                        task_cur_prog = 0
                    mecha_fight_time = mecha_dict['mecha_fight_time'] or 0
                    new_mecha_dict['mecha_fight_time'] = max(task_cur_prog, mecha_fight_time)
                elif key == 'mecha_kill_num':
                    task_id = task_statistics_list[1]
                    if global_data.player:
                        task_cur_prog = global_data.player.get_task_prog(task_id)
                    else:
                        task_cur_prog = 0
                    mecha_kill_num = mecha_dict['mecha_kill_num'] or 0
                    new_mecha_dict['mecha_kill_num'] = max(task_cur_prog, mecha_kill_num)
                else:
                    task_id = None

            return (
             new_mecha_dict, skill_dict, icon_dict)
            return

    def update_title(self, season_data):
        mecha_type = self.mecha_type
        best_rank = self.get_mecha_season_title(season_data, mecha_type, self._show_battle_season_id)
        init_career_titile(self.panel.bar_rank, best_rank)

    def get_mecha_season_title(self, season_data, mecha_id, season):
        title = season_data.get('mecha_top_title', {}).get(str(mecha_id), [])
        if self.is_mine:
            if season == self._cur_battle_season_id:
                from logic.gutils.season_utils import get_mecha_best_region_rank
                best_rank = get_mecha_best_region_rank(mecha_id)
                return best_rank
        title_copy = list(title)
        if title_copy:
            from logic.gcommon.common_const import rank_const
            title_copy.insert(0, rank_const.RANK_TITLE_MECHA_REGION)
            title_copy.append(-1)
        return title_copy

    def on_player_update_proficiency(self, mecha_type, level, proficiency, lv_up=False):
        if self.is_mine:
            if self.memory_widget:
                self.memory_widget.refresh()
            if self.share_memory_widget:
                self.share_memory_widget.refresh()