# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEMainUIWidgetUI/PVESelectLevelWidget.py
from __future__ import absolute_import
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.pve_utils import check_pve_key_enouth, update_price_list, check_read_archive_cost
from logic.gcommon.common_const.pve_const import NORMAL_DIFFICUTY, HARD_DIFFICUTY, HELL_DIFFICUTY, DIFFICUTY_LIST, PVE_DIFFICULTY_CACHE, PVE_ENTER_KEY_COUNT, DIFFICULTY_TEXT_LIST, get_read_archive_cost, PVE_MAX_PLAYER_COUNT, DIFFICULTY_COLOR_LIST
from logic.gcommon.common_utils.text_utils import get_color_str
from logic.gcommon.const import SHOP_PAYMENT_ITEM_PVE_KEY
from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
from logic.gcommon.common_const.battle_const import DEFAULT_PVE_TID
from logic.gcommon import time_utility as tutil
from logic.gutils.pve_utils import get_archive_key
from common.cfg import confmgr
from ext_package.ext_decorator import has_pve_ext
import six_ex
import cc
DIFFICULTY_LAB_TITLE_COLOR_DICT = {1: [60159, 857924],2: ['#SW', 0],3: ['#SW', 0]}
DIFFICULTY_LAB_TITLE2_COLOR_DICT = {1: ['#SW', 857924],2: [15918043, 0],3: [15916509, 0]}
from logic.gcommon.common_const.pve_const import LAB_TITLE_COLOR_DICT, LAB_TITLE2_COLOR_DICT
DIFFICULTY_PNL_PATH = 'gui/ui_res_2/pve/select_level_new/pnl_select_leve_content_{}.png'
DIFFICULTY_DEC_PATH = 'gui/ui_res_2/pve/select_level_new/img_select_leve_dec_{}.png'
DIFFICULTY_BTN_PATH = 'gui/ui_res_2/pve/select_level_new/btn_select_level_{}.png'
PVE_MATCH_STR_DICT = {(True, True): 469,
   (True, False): 469,
   (False, True): 13016,
   (False, False): 13018
   }
COUNTDOWN_TAG = 20231130

class PVESelectLevelWidget(object):

    def __init__(self, parent, panel):
        self._parent = parent
        self._panel = panel
        self.init_parameters()
        self.init_ui()
        self.init_ui_event()
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'player_item_update_event': self.on_item_update,
           'player_join_team_event': self._update_teammate_state,
           'player_leave_team_event': self._update_teammate_state,
           'player_add_teammate_event': self._update_teammate_state,
           'player_del_teammate_event': self._update_teammate_state,
           'player_set_ready_event': self._update_teammate_state,
           'player_change_leader_event': self._update_teammate_state,
           'room_player_return_to_lobby_event': self._update_teammate_state,
           'kick_out_from_custom_room': self._update_teammate_state,
           'update_allow_match_ts': self._update_teammate_state,
           'battle_match_status_event': self._update_teammate_state,
           'player_match_info_change_event': self._update_teammate_state,
           'pve_battle_info_change_event': self._update_teammate_state
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_parameters(self):
        self._chapter_id = global_data.player.get_last_pve_chapter() if global_data.player else 1
        self._archive_data = global_data.achi_mgr.get_general_archive_data()
        self._cur_difficulty = global_data.player.get_last_pve_difficulty() if global_data.player else NORMAL_DIFFICUTY
        self._cur_chapter_unlock_difficulty = None
        self._cur_player_count = global_data.player.get_last_pve_player_size() if global_data.player else 1
        self._btn_tab_list = [None]
        self._chapter_conf = confmgr.get('pve_level_conf', 'ChapterConf', 'Content')
        self._auto_match = global_data.player.get_pve_auto_match() if global_data.player else True
        self.match_tag = 10
        return

    def init_ui(self):
        self._update_price_list()
        self._update_chapter_info()
        self._init_difficulty_list()
        self._update_difficulty_info()
        self._update_archive()
        self._init_teammate_choose()
        self._update_teammate_state()

    def init_ui_event(self):
        nd_switch = self._panel.pnl_content.nd_switch

        @nd_switch.btn_left_level.callback()
        def OnClick(btn, touch):
            if self._chapter_id == 1:
                global_data.game_mgr.show_tip(get_text_by_id(1400041))
                return
            self.jump_to_chapter(self._chapter_id - 1, NORMAL_DIFFICUTY)

        @nd_switch.btn_right_level.callback()
        def OnClick(btn, touch):
            if self._chapter_id == len(self._chapter_conf) or self._chapter_id == global_data.pve_max_chapter:
                global_data.game_mgr.show_tip(get_text_by_id(1400041))
                return
            self.jump_to_chapter(self._chapter_id + 1, NORMAL_DIFFICUTY)

        @self._panel.btn_fight.callback()
        def OnClick(btn, touch):
            self._on_click_btn_fight()

        @self._panel.btn_again.unique_callback()
        def OnClick(btn, touch, *args):
            if not global_data.player:
                return
            if not has_pve_ext(self._chapter_id):
                global_data.game_mgr.show_tip(get_text_by_id(83610))
                global_data.ui_mgr.show_ui('ExtDownloadInfoUI', 'logic.comsys.lobby.ExtNpk')
                return
            if not global_data.enable_pve_team and global_data.player.is_in_team():
                global_data.game_mgr.show_tip(get_text_by_id(452))
                return
            if self.check_read_archive_cost():
                global_data.player.start_pve_battle(self._chapter_id, self._cur_difficulty, use_archive=True, player_size=self._cur_player_count)
                global_data.enter_pve_with_archive = True
            else:
                global_data.ui_mgr.show_ui('PVEKeyBuyUI', 'logic.comsys.battle.pve.PVEMainUIWidgetUI')
                global_data.game_mgr.show_tip(get_text_by_id(405))

        @self._panel.btn_file.unique_callback()
        def OnClick(btn, touch, *args):
            self.open_archive_file()

        @self._panel.btn_fight.nd_checkbox.lab_check.nd_auto_fit.icon_check.unique_callback()
        def OnClick(btn, touch, *args):
            self._auto_match = not self._auto_match
            global_data.player.select_pve_auto_match(self._auto_match)
            self._update_auto_match()
            self._set_match_info()

        @self._panel.pnl_content.btn_pet.unique_callback()
        def OnClick(btn, touch):
            global_data.ui_mgr.show_ui('PVEPetBuffUI', 'logic.comsys.battle.pve.PVEMainUIWidgetUI')

    def jump_to_chapter(self, chapter_id, difficulty):
        if not self.is_leader():
            global_data.game_mgr.show_tip(get_text_by_id(485))
            return
        self._cur_difficulty = difficulty
        self._chapter_id = chapter_id
        self._update_chapter_info()
        self._update_difficulty_info()
        self._set_match_info()

    def _on_click_btn_fight(self):
        if not global_data.player:
            return
        if not has_pve_ext(self._chapter_id):
            global_data.game_mgr.show_tip(get_text_by_id(83610))
            global_data.ui_mgr.show_ui('ExtDownloadInfoUI', 'logic.comsys.lobby.ExtNpk')
            return
        if not global_data.enable_pve_team and global_data.player.is_in_team():
            global_data.game_mgr.show_tip(get_text_by_id(452))
            return
        if not check_pve_key_enouth():

            def on_show_pve_key_buy_ui():
                global_data.ui_mgr.show_ui('PVEKeyBuyUI', 'logic.comsys.battle.pve.PVEMainUIWidgetUI')
                global_data.game_mgr.show_tip(get_text_by_id(405))

            if global_data.enable_pve_team and global_data.player.is_in_team():
                SecondConfirmDlg2(parent=self._panel).confirm(content=get_text_by_id(478), confirm_callback=on_show_pve_key_buy_ui)
            else:
                on_show_pve_key_buy_ui()
        if self._cur_difficulty > self._cur_chapter_unlock_difficulty:
            if self._cur_chapter_unlock_difficulty == 0 and self._chapter_id > 1:
                pre_conf = self._chapter_conf.get(str(self._chapter_id - 1))
                chapter1_str = get_text_by_id(pre_conf.get('title_text'))
                cur_conf = self._chapter_conf.get(str(self._chapter_id))
                chapter2_str = get_text_by_id(cur_conf.get('title_text'))
                global_data.game_mgr.show_tip(get_text_by_id(540).format(chapter1=chapter1_str, chapter2=chapter2_str))
                return
            else:
                difficulty_text = get_text_by_id(DIFFICULTY_TEXT_LIST[self._cur_difficulty])
                global_data.game_mgr.show_tip(get_text_by_id(480).format(inner_text_id=difficulty_text))
                return

        matching_type = global_data.player.get_matching_type()
        if matching_type and matching_type != DEFAULT_PVE_TID:
            battle_config = confmgr.get('battle_config')
            battle_info = battle_config.get(str(matching_type))
            name_text_id = battle_info.get('cNameTID', -1)
            name_text = get_text_by_id(name_text_id)
            global_data.game_mgr.show_tip(get_text_by_id(635143).format(name_text))
            return
        self._check_is_in_team_fight()

    def _check_is_in_team_fight(self):
        if global_data.enable_pve_team and global_data.player.is_in_team():
            is_hang_up = global_data.player.is_hang_up()
            if is_hang_up:
                global_data.player.end_hang_up()
            elif self.is_leader():
                team_info = global_data.player.get_team_info()
                is_hang_up = [ info.get('hang_up_ts', 0) > tutil.get_server_time() for info in six_ex.values(team_info['members']) ]
                if team_info and any(is_hang_up):
                    global_data.game_mgr.show_tip(get_text_by_id(13142))
                    return
                if not global_data.player.is_all_ready() and not global_data.player.is_matching:
                    global_data.game_mgr.show_tip(get_text_by_id(13054))
                self._on_confirm()
            else:
                self._on_confirm()
        else:
            archive_data = global_data.player.get_pve_archive()
            search_key = get_archive_key(self._chapter_id, self._cur_difficulty, self._cur_player_count)
            teammate_count = global_data.player.get_team_cur_count() if global_data.player else 1
            if search_key in archive_data and teammate_count == 1 and not self._auto_match:
                SecondConfirmDlg2(parent=self._panel).confirm(content=get_text_by_id(468), cancel_text=get_text_by_id(476), confirm_text=get_text_by_id(475), confirm_callback=self._on_confirm)
            elif self._cur_player_count > 1 and not self._auto_match:
                SecondConfirmDlg2().confirm(content=get_text_by_id(860393), confirm_callback=self._on_confirm)
            else:
                self._on_confirm()

    def _on_confirm(self):
        if not global_data.player:
            return
        if self.is_ready():
            global_data.player.get_ready(False, DEFAULT_PVE_TID, False)
        else:
            if global_data.player.is_matching:
                global_data.player.cancel_match()
                return
            auto_match = self._auto_match
            teammate_count = global_data.player.get_team_cur_count() if global_data.player else 1
            if not global_data.enable_pve_team or self._cur_player_count == teammate_count:
                auto_match = False
            global_data.player.start_pve_battle(chapter=self._chapter_id, difficulty=self._cur_difficulty, use_archive=False, player_size=self._cur_player_count, auto_match=self._auto_match)

    def _update_price_list(self):
        price_info = [
         {'original_price': PVE_ENTER_KEY_COUNT,
            'goods_payment': SHOP_PAYMENT_ITEM_PVE_KEY,
            'discount_price': PVE_ENTER_KEY_COUNT
            }]
        update_price_list(price_info, self._panel.btn_fight, self._panel.btn_fight.lab_btn)

    def on_item_update(self):
        self._update_price_list()
        self._update_archive()

    def get_current_chapter_info(self):
        return (
         self._chapter_id, self._cur_difficulty, self._cur_player_count)

    def _update_chapter_info(self):
        self._cur_chapter_unlock_difficulty = global_data.player.get_chapter_unlock_difficulty(self._chapter_id) if global_data.player else NORMAL_DIFFICUTY
        conf = self._chapter_conf.get(str(self._chapter_id))
        pnl_content = self._panel.pnl_content
        pnl_content.lab_title.SetString(get_text_by_id(conf.get('title_text')))
        pnl_content.lab_title2.SetString(get_text_by_id(conf.get('sub_title_text')))
        pnl_content.frame.bar_tips.lab_describe.setString(get_text_by_id(conf.get('desc_text')))
        self._update_archive()
        self._update_chapter_difficulty_pic()

    def _init_difficulty_list(self):
        list_tab = self._panel.pnl_content.pnl_tab.list_tab
        chapter_id = str(self._chapter_id)
        for i, difficulty in enumerate(DIFFICUTY_LIST):
            item = list_tab.AddTemplateItem()
            btn_tab = item.btn_tab
            self._btn_tab_list.append(btn_tab)
            btn_tab.SetText(get_text_by_id(DIFFICULTY_TEXT_LIST[difficulty]))
            btn_tab.EnableCustomState(True)
            path = DIFFICULTY_BTN_PATH.format(i)
            btn_tab.SetFrames('', [None, path, None])

            @btn_tab.callback()
            def OnClick(btn, touch, difficulty=difficulty):
                if difficulty > self._cur_chapter_unlock_difficulty:
                    if self._cur_chapter_unlock_difficulty == 0 and self._chapter_id > 1 and difficulty == NORMAL_DIFFICUTY:
                        pre_conf = self._chapter_conf.get(str(self._chapter_id - 1))
                        chapter1_str = get_text_by_id(pre_conf.get('title_text'))
                        cur_conf = self._chapter_conf.get(str(self._chapter_id))
                        chapter2_str = get_text_by_id(cur_conf.get('title_text'))
                        global_data.game_mgr.show_tip(get_text_by_id(540).format(chapter1=chapter1_str, chapter2=chapter2_str))
                        return
                    else:
                        global_data.game_mgr.show_tip(get_text_by_id(511))
                        return

                if not self.is_leader():
                    global_data.game_mgr.show_tip(get_text_by_id(485))
                    return
                self._on_click_difficulty(difficulty)
                self._set_match_info()

        return

    def _on_click_difficulty(self, difficulty):
        chapter_id = str(self._chapter_id)
        pve_difficulty_cache = self._archive_data.get_field(PVE_DIFFICULTY_CACHE, {})
        if not pve_difficulty_cache.get(chapter_id):
            pve_difficulty_cache[chapter_id] = []
        if difficulty <= self._cur_chapter_unlock_difficulty:
            self._cur_difficulty = difficulty
            if difficulty not in pve_difficulty_cache[chapter_id]:
                pve_difficulty_cache[chapter_id].append(difficulty)
                self._archive_data.set_field(PVE_DIFFICULTY_CACHE, pve_difficulty_cache)
            self._btn_tab_list[difficulty].temp_red.setVisible(False)
            self._update_difficulty_info()
        elif difficulty == HARD_DIFFICUTY:
            global_data.game_mgr.show_tip(get_text_by_id(429))
        elif difficulty == HELL_DIFFICUTY:
            global_data.game_mgr.show_tip(get_text_by_id(430))

    def _update_difficulty_info(self):
        pve_difficulty_cache = self._archive_data.get_field(PVE_DIFFICULTY_CACHE, {})
        pve_chapter_difficulty_cache = pve_difficulty_cache.get(str(self._chapter_id), [])
        for i, difficulty in enumerate(DIFFICUTY_LIST):
            btn_tab = self._btn_tab_list[difficulty]
            btn_tab.SetSelect(difficulty == self._cur_difficulty)
            is_unlock = difficulty <= self._cur_chapter_unlock_difficulty
            btn_tab.icon_lock.setVisible(not is_unlock)
            if difficulty <= self._cur_chapter_unlock_difficulty:
                btn_tab.temp_red.setVisible(is_unlock and difficulty not in pve_chapter_difficulty_cache and difficulty != NORMAL_DIFFICUTY)
            else:
                btn_tab.temp_red.setVisible(False)
            if difficulty == self._cur_difficulty:
                btn_tab.temp_red.setVisible(False)
                old_pve_difficulty_cache = pve_difficulty_cache
                chapter_id = str(self._chapter_id)
                if not pve_difficulty_cache.get(chapter_id):
                    pve_difficulty_cache[chapter_id] = []
                pve_difficulty_cache[chapter_id].append(difficulty)
                if old_pve_difficulty_cache != pve_difficulty_cache:
                    self._archive_data.set_field(PVE_DIFFICULTY_CACHE, pve_difficulty_cache)

        pnl_content = self._panel.pnl_content
        pnl_content.SetDisplayFrameByPath('', DIFFICULTY_PNL_PATH.format(self._cur_difficulty - 1))
        pnl_content.img_dec.SetDisplayFrameByPath('', DIFFICULTY_DEC_PATH.format(self._cur_difficulty - 1))
        lab_title = pnl_content.lab_title
        lab_title2 = pnl_content.lab_title2
        lab_title.SetColor(LAB_TITLE_COLOR_DICT[self._chapter_id][0])
        lab_title.EnableShadow(True, LAB_TITLE_COLOR_DICT[self._chapter_id][1], 255, cc.Size(4, -4))
        lab_title.SetString(lab_title.GetString())
        lab_title2.SetColor(LAB_TITLE2_COLOR_DICT[self._chapter_id][0])
        lab_title2.EnableShadow(LAB_TITLE2_COLOR_DICT[self._chapter_id][1], 255, {'width': 4,'height': -4})
        self._update_archive()
        self._update_chapter_difficulty_pic()

    def _update_chapter_difficulty_pic(self):
        conf = self._chapter_conf.get(str(self._chapter_id))
        icon_pic_list = conf.get('icon')
        icon_pic = icon_pic_list[self._cur_difficulty - 1]
        self._panel.pnl_content.frame.nd_cut.img_map.SetDisplayFrameByPath('', icon_pic)

    def _update_archive(self):
        if not global_data.player:
            return
        if global_data.enable_pve_team and global_data.player and global_data.player.is_in_team():
            self._parent.panel.PlayAnimation('disappear_file')
            return
        archive_data = global_data.player.get_pve_archive()
        search_key = get_archive_key(self._chapter_id, self._cur_difficulty, self._cur_player_count)
        if search_key in archive_data:
            self._parent.panel.PlayAnimation('appear_file')
            read_data = global_data.player.get_pve_archive_read_data()
            read_count = read_data.get(search_key, 0)
            archive_info = archive_data[search_key]
            difficulty = archive_info.get('difficulty', NORMAL_DIFFICUTY)
            difficulty_str = get_color_str(DIFFICULTY_COLOR_LIST[difficulty], get_text_by_id(DIFFICULTY_TEXT_LIST[difficulty]))
            chapter = archive_info.get('chapter', 1)
            level = archive_info.get('level', 0) + 1
            self._panel.btn_again.lab_tips_fight.SetString(get_text_by_id(525).format(str(read_count), difficulty_str, chapter, level))
            price_info = [
             {'original_price': get_read_archive_cost(read_count + 1),
                'goods_payment': SHOP_PAYMENT_ITEM_PVE_KEY,
                'discount_price': get_read_archive_cost(read_count + 1)
                }]
            update_price_list(price_info, self._panel.btn_again, self._panel.btn_again.lab_btn)
        else:
            self._parent.panel.PlayAnimation('disappear_file')

    def check_read_archive_cost(self):
        return check_read_archive_cost(self._chapter_id, self._cur_difficulty, self._cur_player_count)

    def open_archive_file(self):
        if not global_data.player:
            return
        archive_data = global_data.player.get_pve_archive()
        search_key = get_archive_key(self._chapter_id, self._cur_difficulty, self._cur_player_count)
        archive_file = archive_data.get(search_key, {})
        if archive_file:
            self._parent.panel.nd_main.setVisible(False)
            self._parent.panel.nd_file.setVisible(True)
        else:
            return

    def get_match_info(self):
        return (
         self._chapter_id, self._cur_difficulty, self._cur_player_count)

    def _set_match_info(self):
        if global_data.enable_pve_team and global_data.player.is_in_team() and self.is_leader():
            battle_tid = DEFAULT_PVE_TID
            auto_match = self._auto_match
            battle_info = {}
            battle_info['chapter'] = self._chapter_id
            battle_info['difficulty'] = self._cur_difficulty
            battle_info['pve_player_size'] = self._cur_player_count
            global_data.player and global_data.player.set_match_info(battle_tid, auto_match, battle_info)

    def _update_arrow(self):
        is_visible = self._panel.list_choose.isVisible()
        self._panel.pnl_content.frame.btn_num.icon_arrow.setRotation(90 if is_visible else 270)

    def _init_teammate_choose(self):
        enable_pve_team = global_data.enable_pve_team
        btn_num = self._panel.pnl_content.frame.btn_num
        btn_num.setVisible(enable_pve_team)
        if not enable_pve_team:
            return
        icon_check = self._panel.btn_fight.nd_checkbox.lab_check.nd_auto_fit.icon_check
        icon_check.EnableCustomState(True)
        lab_num = btn_num.lab_num
        lab_num.setString(get_text_by_id(481).format(self._cur_player_count))
        list_choose = self._panel.list_choose

        @btn_num.callback()
        def OnClick(*args):
            if not self.is_leader():
                global_data.game_mgr.show_tip(get_text_by_id(484))
                return
            list_choose.setVisible(not list_choose.isVisible())
            self._update_arrow()

        @list_choose.nd_close.callback()
        def OnClick(*args):
            list_choose.setVisible(False)
            self._update_arrow()

        option_list = list_choose.option_list
        option_list.BindMethod('OnCreateItem', self._on_create_callback)
        option_list.DeleteAllSubItem()
        option_list.SetInitCount(PVE_MAX_PLAYER_COUNT)

    def _on_create_callback(self, lv, index, item):
        if item:
            player_count = index + 1
            button = item.button
            button.SetText(get_text_by_id(481).format(player_count))

            @button.callback()
            def OnClick(btn, touch, player_count=player_count):
                is_matching = global_data.player.is_matching if global_data.player else False
                if is_matching:
                    return
                teammate_count = global_data.player.get_team_cur_count() if global_data.player else 1
                if teammate_count > player_count:
                    return
                lab_num = self._panel.pnl_content.frame.btn_num.lab_num
                lab_num.setString(get_text_by_id(481).format(player_count))
                self._panel.list_choose.setVisible(False)
                self._update_arrow()
                self._cur_player_count = player_count
                self._update_archive()
                self._update_auto_match()
                self._set_match_info()

    def _update_teammate_state(self, *args):
        chapter_id = self._chapter_id
        difficulty = self._cur_difficulty
        if global_data.player:
            if global_data.enable_pve_team and global_data.player.is_in_team():
                pve_battle_info = global_data.player.get_pve_battle_info()
                if pve_battle_info:
                    self._chapter_id = pve_battle_info.get('chapter')
                    self._cur_difficulty = pve_battle_info.get('difficulty')
                    self._cur_player_count = pve_battle_info.get('pve_player_size')
            else:
                self._chapter_id = global_data.player.get_last_pve_chapter()
                if self._cur_difficulty > self._cur_chapter_unlock_difficulty:
                    self._cur_difficulty = global_data.player.get_last_pve_difficulty()
        self._update_teammate_count()
        self._update_auto_match()
        self._update_match_widget()
        self._update_archive()
        if chapter_id != self._chapter_id:
            self._update_chapter_info()
            self._update_difficulty_info()
        if difficulty != self._cur_difficulty:
            self._update_difficulty_info()

    def _update_teammate_count(self):
        teammate_count = global_data.player.get_team_cur_count() if global_data.player else 1
        lab_num = self._panel.pnl_content.frame.btn_num.lab_num
        if teammate_count > self._cur_player_count:
            lab_num.setString(get_text_by_id(481).format(teammate_count))
            self._cur_player_count = teammate_count
        else:
            lab_num.setString(get_text_by_id(481).format(self._cur_player_count))

    def _update_auto_match(self):
        nd_checkbox = self._panel.btn_fight.nd_checkbox
        if not self.is_leader():
            nd_checkbox.setVisible(False)
            self._update_teammate_lab_btn()
            return
        teammate_count = global_data.player.get_team_cur_count() if global_data.player else 1
        if not global_data.enable_pve_team or self._cur_player_count == teammate_count:
            nd_checkbox.setVisible(False)
            self._update_teammate_lab_btn()
            return
        nd_checkbox.setVisible(True)
        nd_checkbox.lab_check.nd_auto_fit.icon_check.SetSelect(self._auto_match)
        if self._auto_match:
            self._panel.btn_fight.lab_btn.SetString(get_text_by_id(13017))
            self._update_price_list()
        else:
            self._update_teammate_lab_btn()

    def _update_teammate_lab_btn(self):
        if not global_data.enable_pve_team:
            return
        lab_btn = self._panel.btn_fight.lab_btn
        match_text = PVE_MATCH_STR_DICT[self.is_leader(), self.is_ready()]
        lab_btn.SetString(match_text)
        self._update_price_list()

    def _update_match_widget(self, *args):
        is_matching = global_data.player.is_matching if global_data.player else False
        match_start_timestamp = global_data.player.get_match_start_timestamp() if global_data.player else None
        btn_fight = self._panel.btn_fight
        btn_fight.nd_matching.setVisible(is_matching)
        btn_fight.temp_price.setVisible(not is_matching)
        btn_fight.lab_btn.setVisible(not is_matching)
        if is_matching:
            if match_start_timestamp is not None:
                self._show_time_passed()
                self._parent.panel.DelayCallWithTag(1, self._show_time_passed, COUNTDOWN_TAG)
        else:
            self._parent.panel.stopActionByTag(COUNTDOWN_TAG)
        return

    def _show_time_passed(self):
        if global_data.player:
            if not global_data.player.get_match_start_timestamp():
                self._parent.panel.stopActionByTag(COUNTDOWN_TAG)
                return
            delta = tutil.time() - global_data.player.get_match_start_timestamp()
            self._panel.btn_fight.nd_matching.lab_matching_time.setString(tutil.get_delta_time_str(delta)[3:])
            return True

    def is_leader(self):
        if not global_data.player:
            return False
        else:
            leader_id = global_data.player.get_leader_id()
            return leader_id is None or leader_id == global_data.player.uid

    def is_ready(self):
        if not global_data.player:
            return False
        team_info = global_data.player.get_team_info()
        return global_data.player.get_self_ready() and bool(team_info) and global_data.player.get_ready_battle_type() == DEFAULT_PVE_TID

    def destroy(self):
        self.process_event(False)
        global_data.player and global_data.player.set_last_pve_chapter_info(self._cur_difficulty, self._chapter_id, self._cur_player_count)
        self._chapter_id = None
        self._archive_data = None
        self._cur_difficulty = None
        self._cur_chapter_unlock_difficulty = None
        self._cur_player_count = 1
        self._btn_tab_list = None
        self._chapter_conf = None
        self._auto_match = False
        return