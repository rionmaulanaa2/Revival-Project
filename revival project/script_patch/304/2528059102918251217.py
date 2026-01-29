# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/rank/PVERankSelComditionComp.py
from __future__ import absolute_import
import six_ex
from common.utils.cocos_utils import ccp
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.cfg import confmgr
from logic.gcommon.common_const.pve_const import DIFFICUTY_LIST, DIFFICULTY_TEXT_LIST, TYPE_LIST_2_TEXT_ID, TYPE_PVE_RANK_LIST
from logic.gcommon.common_const.pve_rank_const import PVE_RANK_1_ALL, PVE_RANK_2_TEAM, PVE_RANK_3_TEAM, PVE_RANK_1_FRIEND
from logic.gutils.template_utils import init_common_choose_list_2
from logic.comsys.battle.pve.rank.PVERankDataObj import PVERankDataObj

class PVERankSelComditionComp(object):
    RANK_PAGE_TYPE = None

    def __init__(self, template_root, page_config, rank_page_type):
        self._template_root = template_root
        self.RANK_PAGE_TYPE = rank_page_type
        self.init_args()
        self.condition_obj = PVERankDataObj(page_config)
        self.on_refresh_all_list_choose()
        self.process_event(True)

    def process_event(self, is_bind):
        if self._has_binded_event == is_bind:
            return
        emgr = global_data.emgr
        econf = {'on_change_pve_rank_condition': self._on_change_pve_rank_condition
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)
        self._has_binded_event = is_bind

    def destroy(self):
        self.process_event(False)
        self.init_args()
        self._template_root = None
        return

    def init_args(self):
        self._has_binded_event = None
        self._list_type_sel_table = None
        self._list_type_choosed = None
        self._difficulty_sel_table = None
        self._difficulty_choosed = None
        self._chapter_sel_table = None
        self._chapter_choosed = None
        self._player_cnt_sel_table = None
        self._player_cnt_choosed = None
        return

    def _on_change_pve_rank_condition(self, source_key, config):
        global_data.emgr.on_change_pve_rank_page_config.emit(self.RANK_PAGE_TYPE, source_key, config)

    def modify_config_data(self, page_config):
        self.condition_obj.modify_config_data(page_config)

    def switch_choose_mecha(self, _mecha_id):
        self.condition_obj.switch_choose_mecha(_mecha_id)

    def get_cur_config(self):
        return self.condition_obj.get_cur_config()

    def is_friend_rank(self):
        return self.condition_obj.is_friend_rank()

    def get_choosed_player_cnt(self):
        return self.condition_obj.get_player_cnt()

    def get_choosed_list_type(self):
        return self.condition_obj.get_list_type()

    def get_choosed_mecha_id(self):
        return self.condition_obj.get_mecha_id()

    def get_cur_rank_key(self):
        return self.condition_obj.get_rank_key()

    def get_data_obj(self):
        return self.condition_obj

    def load_page_config(self, page_config):
        self.condition_obj.load_page_config(page_config)

    def _on_choose_list_to_close_other(self, choosed_item_temp):
        if self._list_type_choosed and self._list_type_choosed != choosed_item_temp:
            self._on_choose_list_type()
        if self._difficulty_choosed and self._difficulty_choosed != choosed_item_temp:
            self._on_choose_difficulty()
        if self._chapter_choosed and self._chapter_choosed != choosed_item_temp:
            self._on_choose_chapter()
        if self._player_cnt_choosed and self._player_cnt_choosed != choosed_item_temp:
            self._on_choose_player_cnt()

    def on_refresh_all_list_choose(self):
        self._on_choose_list_type()
        self._on_choose_difficulty()
        self._on_choose_chapter()
        self._on_choose_player_cnt()

    def init_type_choose_list(self):
        lst_type = self.condition_obj.get_list_type()
        self._list_type_sel_table = self._template_root.temp_choose_type
        self._list_type_choosed = self._template_root.temp_title_choose_type
        self._list_type_choosed.icon_arrow.setRotation(0)
        self._list_type_choosed.lab_title_rank.SetString(get_text_by_id(TYPE_LIST_2_TEXT_ID[lst_type]))
        self._list_type_sel_table.setVisible(False)
        self._init_list_type_list()

        @self._list_type_choosed.unique_callback()
        def OnClick(*args):
            old_visible = self._list_type_sel_table.isVisible()
            is_show = not old_visible
            self._list_type_choosed.icon_arrow.setRotation(180 if is_show else 0)
            self._list_type_sel_table.setVisible(is_show)
            is_show and self._on_choose_list_to_close_other(self._list_type_choosed)

        @self._list_type_sel_table.nd_close.unique_callback()
        def OnClick(btn, touch):
            self._on_choose_list_type()

    def _init_list_type_list(self):
        temp_choose = self._list_type_sel_table

        def callback(index):
            _lst_type = TYPE_PVE_RANK_LIST[index]
            self.condition_obj.switch_choose_list_type(_lst_type)
            self._on_choose_list_type()

        option_list = [ {'name': get_text_by_id(TYPE_LIST_2_TEXT_ID[lst_type])} for lst_type in TYPE_PVE_RANK_LIST ]
        init_common_choose_list_2(temp_choose, self._list_type_choosed.icon_arrow, option_list, callback)

    def _on_choose_list_type(self):
        if not self._list_type_sel_table:
            return
        lst_type = self.condition_obj.get_list_type()
        self._list_type_sel_table.setVisible(False)
        self._list_type_choosed.icon_arrow.setRotation(0)
        self._list_type_choosed.lab_title_rank.setString(get_text_by_id(TYPE_LIST_2_TEXT_ID[lst_type]))

    def init_disfficulty_choose_list(self):
        difficuty = self.condition_obj.get_difficulty()
        self._difficulty_sel_table = self._template_root.temp_choose_diffc
        self._difficulty_choosed = self._template_root.temp_title_choose_diffc
        self._difficulty_choosed.icon_arrow.setRotation(0)
        self._difficulty_choosed.lab_title_rank.SetString(get_text_by_id(DIFFICULTY_TEXT_LIST[difficuty]))
        self._difficulty_sel_table.setVisible(False)
        self._init_disfficulty_list()

        @self._difficulty_choosed.unique_callback()
        def OnClick(*args):
            old_visible = self._difficulty_sel_table.isVisible()
            is_show = not old_visible
            self._difficulty_choosed.icon_arrow.setRotation(180 if is_show else 0)
            self._difficulty_sel_table.setVisible(is_show)
            is_show and self._on_choose_list_to_close_other(self._difficulty_choosed)

        @self._difficulty_sel_table.nd_close.unique_callback()
        def OnClick(btn, touch):
            self._on_choose_difficulty()

    def _init_disfficulty_list(self):
        temp_choose = self._difficulty_sel_table

        def callback(index):
            _difficuty = DIFFICUTY_LIST[index]
            self.condition_obj.switch_choose_difficulty(_difficuty)
            self._on_choose_difficulty()

        option_list = [ {'name': get_text_by_id(DIFFICULTY_TEXT_LIST[difficuty])} for difficuty in DIFFICUTY_LIST ]
        init_common_choose_list_2(temp_choose, self._difficulty_choosed.icon_arrow, option_list, callback)

    def _on_choose_difficulty(self):
        if not self._difficulty_sel_table:
            return
        difficuty = self.condition_obj.get_difficulty()
        self._difficulty_choosed.icon_arrow.setRotation(0)
        self._difficulty_choosed.lab_title_rank.setString(get_text_by_id(DIFFICULTY_TEXT_LIST[difficuty]))
        self._difficulty_sel_table.setVisible(False)
        self._difficulty_sel_table.bar.ResizeAndPosition()

    def _load_chapter_conf(self):
        conf = confmgr.get('pve_level_conf', 'ChapterConf', 'Content')
        self.chapter_conf = {}
        for s_chapter, info in six_ex.items(conf):
            self.chapter_conf[int(s_chapter)] = get_text_by_id(info.get('title_text'))

    def init_chapter_choose_list(self):
        self._load_chapter_conf()
        self._chapter_sel_table = self._template_root.temp_choose_chapter
        self._chapter_choosed = self._template_root.temp_title_choose_chapter
        self._on_choose_chapter()
        self._init_chapter_list()

        @self._chapter_choosed.unique_callback()
        def OnClick(*args):
            old_visible = self._chapter_sel_table.isVisible()
            is_show = not old_visible
            self._chapter_choosed.icon_arrow.setRotation(180 if is_show else 0)
            self._chapter_sel_table.setVisible(is_show)
            is_show and self._on_choose_list_to_close_other(self._chapter_choosed)

        @self._chapter_sel_table.nd_close.unique_callback()
        def OnClick(btn, touch):
            self._on_choose_chapter()

    def _init_chapter_list(self):
        chapters = list(self.chapter_conf.keys())
        chapters.sort()
        temp_choose = self._chapter_sel_table

        def callback(index):
            _chapter = chapters[index]
            self.condition_obj.switch_choose_chapter(_chapter)
            self._on_choose_chapter()

        option_list = [ {'name': self.chapter_conf[chapter]} for chapter in chapters ]
        init_common_choose_list_2(temp_choose, self._chapter_choosed.icon_arrow, option_list, callback)

    def _on_choose_chapter(self):
        if not self._chapter_sel_table:
            return
        chapter = self.condition_obj.get_chapter()
        self._chapter_choosed.icon_arrow.setRotation(0)
        self._chapter_choosed.lab_title_rank.setString(self.chapter_conf[chapter])
        self._chapter_sel_table.setVisible(False)
        self._chapter_sel_table.bar.ResizeAndPosition()

    def is_open_team_rank(self):
        from logic.gcommon import time_utility as tutil
        OPEN_TIME = 1711944000
        return int(tutil.get_server_time()) >= OPEN_TIME

    def check_red_point(self):
        red_dot_ui = self._player_cnt_choosed.temp_red
        is_open = self.is_open_team_rank()
        is_showed = global_data.achi_mgr.get_general_archive_data_value('pve_team_rank_red_point', default=False)
        red_dot_ui.setVisible(len(self.player_cnt_keys) > 2 and is_open and not is_showed)

    def is_not_open_team_rank(self, models):
        is_open = self.is_open_team_rank()
        if not is_open:
            models = [PVE_RANK_1_ALL, PVE_RANK_1_FRIEND]
        return models

    def _load_player_cnt_conf(self, _models=None):
        config = {PVE_RANK_1_ALL: [
                          1, get_text_by_id(481).format(1), False],
           PVE_RANK_2_TEAM: [
                           2, get_text_by_id(481).format(2), False],
           PVE_RANK_3_TEAM: [
                           3, get_text_by_id(481).format(3), False],
           PVE_RANK_1_FRIEND: [
                             1, get_text_by_id(635379), True]
           }
        models = _models if _models else [PVE_RANK_1_ALL, PVE_RANK_2_TEAM, PVE_RANK_3_TEAM, PVE_RANK_1_FRIEND]
        models = self.is_not_open_team_rank(models)
        self.player_cnt_keys = []
        self.player_cnt_conf = {}
        for model in models:
            self.player_cnt_conf[model] = config[model]
            self.player_cnt_keys.append(model)

    def init_player_cnt_choose_list(self, _models=None):
        self._load_player_cnt_conf(_models)
        self._player_cnt_sel_table = self._template_root.temp_choose_num
        self._player_cnt_choosed = self._template_root.temp_title_choose_num
        self.check_red_point()
        self._on_choose_player_cnt()
        self._init_player_cnt_list()

        @self._player_cnt_choosed.unique_callback()
        def OnClick(*args):
            old_visible = self._player_cnt_sel_table.isVisible()
            is_show = not old_visible
            self._player_cnt_choosed.icon_arrow.setRotation(180 if is_show else 0)
            self._player_cnt_sel_table.setVisible(is_show)
            is_show and self._on_choose_list_to_close_other(self._player_cnt_choosed)

        @self._player_cnt_sel_table.nd_close.unique_callback()
        def OnClick(btn, touch):
            self._on_choose_player_cnt()

    def _init_player_cnt_list(self):
        temp_choose = self._player_cnt_sel_table

        def callback(index):
            config = self.player_cnt_conf[self.player_cnt_keys[index]]
            self.condition_obj.switch_choose_player_cnt(config[0], config[2])
            self._on_choose_player_cnt()

        option_list = [ {'name': self.player_cnt_conf[index][1]} for index in self.player_cnt_conf ]
        init_common_choose_list_2(temp_choose, self._player_cnt_choosed.icon_arrow, option_list, callback)

    def _on_choose_player_cnt(self):
        if not self._player_cnt_sel_table:
            return
        player_mode = self.condition_obj.get_player_cnt_mode()
        player_cnt = self.condition_obj.get_player_cnt()
        config = self.player_cnt_conf[player_mode]
        self._player_cnt_choosed.icon_arrow.setRotation(0)
        self._player_cnt_choosed.lab_title_rank.setString(config[1])
        self._player_cnt_sel_table.setVisible(False)
        self._player_cnt_sel_table.bar.ResizeAndPosition()
        if player_cnt > 1:
            global_data.achi_mgr.save_general_archive_data_value('pve_team_rank_red_point', True)
            self.check_red_point()

    def init_friend_choose(self):
        frd_btn = self._template_root.btn_choose_friend
        self._update_friend_btn_state()

        @frd_btn.unique_callback()
        def OnClick(btn, touch):
            is_friend = self.condition_obj.is_friend_rank()
            self.condition_obj.switch_choose_friend_rank(not is_friend)
            self._update_friend_btn_state()

    def _update_friend_btn_state(self):
        is_friend = self.is_friend_rank()
        frd_btn = self._template_root.btn_choose_friend
        icon = self._template_root.icon
        sel = 'gui/ui_res_2/pve/rank/icon_pve_rank_choose_3.png'
        un_sel = 'gui/ui_res_2/pve/rank/icon_pve_rank_choose_2.png'
        frd_btn.SetSelect(is_friend)
        icon.SetDisplayFrameByPath('', sel if is_friend else un_sel)