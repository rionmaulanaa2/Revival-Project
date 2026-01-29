# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/rank/PVEBaseRankWidget.py
from __future__ import absolute_import
from logic.gcommon.common_const import rank_const
import time
import six_ex
from common.utils.cocos_utils import ccp
from logic.gutils import locate_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.pve_rank_utils import get_config_pve_rank_data
from logic.comsys.battle.pve.rank.PVERankSelComditionComp import PVERankSelComditionComp

class PVEBaseRankWidget(object):
    RANK_PAGE_TYPE = None
    RANK_MINE_ITEM_BAR_BG = 'gui/ui_res_2/pve/rank/bar_pve_rank_mine.png'

    def __init__(self, rank_page_config, page_config=None):
        self.rank_page_config = rank_page_config
        self._cur_show_index = -1
        self.list_rank_empty = None
        self.is_scrolling = False
        self._last_scroll_time = 0
        self._last_scroll_interval = 1
        self._has_binded_event = False
        self._request_players_limit = 30
        self._request_players_interval = 0.5
        self._request_players_time = 0
        self._choose_pass_uid = None
        self._message_data = global_data.message_data
        self._data_list = []
        self._data_dict = None
        self._my_rank_data = None
        self._save_time = None
        self.init_ui()
        self.load_page_panel()
        self.cur_sel_condition = PVERankSelComditionComp(self._template_root, page_config, self.RANK_PAGE_TYPE)
        self.init_choose_list()
        self.reset_cur_page()
        self.process_event(True)
        self.init_question_btn()
        return

    def destroy(self):
        self.process_event(False)
        if self.cur_sel_condition:
            self.cur_sel_condition.destroy()
            self.cur_sel_condition = None
        if self._template_root:
            self._template_root.Destroy()
            self._template_root = None
        return

    def init_ui(self):
        self._template_root = None
        self.list_rank = None
        return

    def reset_cur_choosed_info(self):
        pass

    def init_question_btn(self):
        btn_question = self.get_question_btn()

        @btn_question.unique_callback()
        def OnClick(*args):
            from logic.gutils.pve_rank_utils import show_role_tips
            content, title = self.rank_page_config[3]
            show_role_tips(title, content)

    def listen_dynamic_add_item(self):
        self._is_check_sview = False

        def scroll_callback(sender, eventType):
            if self._is_check_sview == False:
                self._is_check_sview = True
                self.list_rank.SetTimeOut(0.001, self.check_sview)

        self.list_rank.addEventListener(scroll_callback)

    def check_sview(self):
        if not self._data_list:
            return
        msg_count = len(self._data_list)
        self._cur_show_index = self.list_rank.AutoAddAndRemoveItem(self._cur_show_index, self._data_list, msg_count, self.add_rank_item, 200, 200)
        self._is_check_sview = False
        if self._cur_show_index >= 0 and self._cur_show_index < msg_count:
            uid = self._data_list[self._cur_show_index]
            if not self._message_data.has_player_inf(uid):
                self.request_players_info()

    def get_list_rank(self):
        return self.list_rank

    def load_page_panel(self):
        raise NotImplementedError('place implement _template_root and list_rank obj: ', self.__class__.__name__)

    def init_choose_list(self):
        pass

    def get_page_model_ctrl_key(self):
        return self.rank_page_config[4].get('model_ctrl', rank_const.PVE_RANK_MODEL_CTRL)

    def set_visible(self, is_show):
        self._template_root and self._template_root.setVisible(is_show)
        if is_show:
            self.process_event(True)
            self.reset_cur_page()
        else:
            self.process_event(False)

    def process_event(self, is_bind):
        self._has_binded_event = is_bind

    def get_default_config(self):
        raise NotImplementedError('place implement [get_default_config] function: ', self.__class__.__name__)

    def load_page_data(self):
        raise NotImplementedError('place implement [load_page_data] function: ', self.__class__.__name__)

    def get_question_btn(self):
        return self._template_root.btn_question

    def show_page_by_config(self, config):
        self.load_page_config(config)
        self.reset_cur_page()

    def is_rank_data_valid(self):
        if self._save_time and time.time() - self._save_time < rank_const.RANK_DATA_CACHE_MAX_TIME:
            return True
        rank_data = self.get_cur_pve_rank_data()
        if not rank_data:
            return False
        return False

    def load_page_config(self, page_config):
        self.cur_sel_condition.load_page_config(page_config)

    def modify_config_data(self, page_config):
        self.cur_sel_condition.modify_config_data(page_config)

    def get_choosed_player_cnt(self):
        return self.cur_sel_condition.get_choosed_player_cnt()

    def get_choosed_list_type(self):
        return self.cur_sel_condition.get_choosed_list_type()

    def get_choosed_mecha_id(self):
        return self.cur_sel_condition.get_choosed_mecha_id()

    def is_friend_rank(self):
        return self.cur_sel_condition.is_friend_rank()

    def switch_choose_list_type(self, _list_type):
        self.cur_sel_condition.switch_choose_list_type(_list_type)

    def get_cur_rank_key(self):
        return self.cur_sel_condition.get_cur_rank_key()

    def get_data_obj(self):
        return self.cur_sel_condition.get_data_obj()

    def get_rank_data_by_index(self, index):
        return self._data_dict[self._data_list[index]]

    def add_rank_item(self, uid_key, is_back_item, index=-1, bRefresh=True):
        raise NotImplementedError('place implement [add_rank_item] function: ', self.__class__.__name__)

    def refresh_data_only(self):
        if not self.is_rank_data_valid():
            return
        item_count = self.list_rank.GetItemCount()
        now_data_count = len(self._data_list)
        if now_data_count < item_count:
            self.refresh()
            return
        data_index = self._cur_show_index - item_count
        for panel in self.list_rank.GetAllItem():
            data_index += 1
            data = self.get_rank_data_by_index(data_index)
            self.refresh_item(panel, data)

    def refresh_rank(self, item, pass_time, rank, is_mine):
        bar_rank_path = ''
        if pass_time < 0:
            item.img_rank.setVisible(False)
            item.lab_rank.setVisible(True)
            item.lab_rank.setString(get_text_by_id(635395))
        elif rank < 0:
            item.img_rank.setVisible(False)
            item.lab_rank.setVisible(True)
            item.lab_rank.setString(get_text_by_id(635395))
        elif rank <= 3:
            item.lab_rank.setVisible(False)
            item.img_rank.setVisible(True)
            item.img_rank.SetDisplayFrameByPath('', 'gui/ui_res_2/pve/rank/img_pve_rank_{}.png'.format(rank))
            bar_rank_path = 'gui/ui_res_2/pve/rank/bar_pve_rank_{}.png'.format(rank)
        else:
            item.img_rank.setVisible(False)
            item.lab_rank.setVisible(True)
            item.lab_rank.setString(str(rank))
            bar_rank_path = 'gui/ui_res_2/pve/rank/bar_pve_rank_others.png'
        if is_mine:
            bar_rank_path = self.RANK_MINE_ITEM_BAR_BG
        bar_rank_path and item.bar_rank.SetDisplayFrameByPath('', bar_rank_path)

    def get_cur_pve_rank_data(self):
        rank_data = self._message_data.get_pve_rank_data(self.get_cur_rank_key())
        return rank_data

    def refresh_rank_content(self):
        if not self.is_rank_data_valid():
            return
        self.refresh()
        self.refresh_my_data()

    def refresh(self):
        raise NotImplementedError('place implement [refresh] function: ', self.__class__.__name__)

    def refresh_my_data(self):
        raise NotImplementedError('place implement [refresh_my_data] function: ', self.__class__.__name__)

    def on_choosed_config_refresh_ui(self, rank_type, source_key, config):
        if self.RANK_PAGE_TYPE != rank_type:
            return
        self.reset_cur_page()

    def reset_cur_page(self):
        self.cur_sel_condition.on_refresh_all_list_choose()
        self.load_page_data()
        self._choose_pass_uid = None
        self.reset_cur_choosed_info()
        self.request_rank_data()
        self.listen_dynamic_add_item()
        return

    def request_rank_data(self):
        if not global_data.player:
            return
        condition_obj = self.get_data_obj()
        if self.is_rank_data_valid():
            self.refresh_rank_content()
        else:
            self.on_show_empty_rank_list(True)
            locate_utils.request_pve_rank_data(condition_obj.clone())

    def on_pass_info_back(self, rank_key):
        if not self._template_root:
            return
        cur_key = self.get_cur_rank_key()
        if rank_key != cur_key:
            return
        self.show_player_pve_pass_ui(rank_key)
        self.on_click_cur_player_item()

    def on_click_cur_player_item(self):
        pass

    def on_update_mine_pass_info(self, rank_type_list):
        cur_key = self.get_cur_rank_key()
        if cur_key not in rank_type_list:
            return
        self.load_page_data()
        self.request_players_info(force=True)

    def on_pve_rank_data(self, rank_type):
        if rank_type != self.get_cur_rank_key():
            return
        self.load_page_data()
        self.request_players_info(force=True)

    def request_players_info(self, force=False):
        raise NotImplementedError('place implement [request_players_info] function: ', self.__class__.__name__)

    def on_players_detail_info_cb(self, *args):
        self.on_players_detail_inf()

    def on_players_detail_inf(self, *args):
        if not self._template_root or not self.list_rank:
            return
        if not self.is_rank_data_valid():
            return
        item_count = self.list_rank.GetItemCount()
        if item_count <= 0:
            self.refresh_rank_content()
        else:
            self.refresh_data_only()

    def add_player_simple_callback(self, panel, uid):

        @panel.unique_callback()
        def OnClick(*args):
            from logic.comsys.message.PlayerSimpleInf import BTN_TYPE_PLAYER_INF
            if global_data.player and uid == global_data.player.uid:
                return
            ui = global_data.ui_mgr.show_ui('PlayerSimpleInf', 'logic.comsys.message')
            if ui:
                ui.custom_show_btn([BTN_TYPE_PLAYER_INF])
                ui.hide_btn_chat()
                ui.refresh_by_uid(uid)

    def on_show_empty_rank_list(self, is_empty):
        if is_empty:
            global_data.emgr.on_pve_rank_show_self_model.emit()
            self._template_root.nd_empty.setVisible(True)
            self._template_root.bar_reward.setVisible(False)
        else:
            self._template_root.nd_empty.setVisible(False)

    def show_player_pve_pass_ui(self, rank_key):
        pass

    def show_rewards(self, rank):
        is_show_items = self.show_item_rewards(rank)
        is_show_title = self.show_title(rank)
        self._template_root.bar_reward.setVisible(is_show_items or is_show_title)

    def show_item_rewards(self, rank):
        from common.cfg import confmgr
        from logic.gutils.template_utils import init_common_reward_list_simple
        if rank < 0:
            self._template_root.list_reward.setVisible(False)
            return False
        else:
            rank_key = self.get_cur_rank_key()
            rank_config = get_config_pve_rank_data(rank_key)
            if not rank_config:
                raise Exception('[no such pve rank key place check [227.PVE\xe6\x8e\x92\xe8\xa1\x8c\xe6\xa6\x9c.xlsx] ==>%s' % rank_key)
            stage_min_rank = 1
            stage_max_rank = 1
            reward_id = None
            reward_list = rank_config.get('item_reward', [])
            for reward_conf in reward_list:
                max_rank = reward_conf[0]
                rwd_id = reward_conf[1]
                stage_min_rank = stage_max_rank
                stage_max_rank = max_rank
                if rank <= max_rank:
                    reward_id = rwd_id
                    break

            is_show = len(reward_list) > 0
            s_rank_range = str(stage_min_rank) if stage_min_rank == stage_max_rank else '{}-{}'.format(stage_min_rank + 1, stage_max_rank)
            text = get_text_by_id(635378, (s_rank_range,))
            self._template_root.list_reward.setVisible(is_show)
            self._template_root.lab_title_reward.setString(text)
            init_common_reward_list_simple(self._template_root.list_reward, reward_id)
            return is_show

    def show_title(self, rank):
        from logic.gutils import template_utils
        if not self._template_root.temp_title:
            return False
        else:
            data_obj = self.get_data_obj()
            rank_info = [data_obj.clone(), rank, None]
            is_show = template_utils.init_rank_title(self._template_root.temp_title, rank_const.RANK_TITLE_PVE, rank_info, icon_scale=0.85)
            return is_show