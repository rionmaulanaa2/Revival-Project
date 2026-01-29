# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityAnnivSecretLetter.py
from __future__ import absolute_import
from six.moves import range
from common.cfg import confmgr
from logic.gutils import mall_utils
from logic.gutils import task_utils
from logic.gutils.activity_utils import get_left_time
from logic.gutils.template_utils import get_left_info, init_common_reward_list, init_price_template, init_tempate_mall_i_item
from logic.gcommon.item.item_const import ITEM_UNRECEIVED, ITEM_RECEIVED, ITEM_UNGAIN
from logic.client.const.mall_const import DARK_PRICE_COLOR
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gcommon.time_utility import get_readable_time, get_readable_time_day_hour_minitue, ONE_HOUR_SECONS

class ActivityAnnivSecretLetter(ActivityBase):
    LETTER_ITEM_NO = 50600036
    REWARD_COUNT = 5
    MAX_LETTER_REWARD_NUM = 50
    PAGE_COUNT = 6
    LEFT_PAGE_COUNT = 8
    RIGHT_PAGE_COUNT = 6
    TASK_ID = '1440503'
    COLLECT_TASK_ID = '1440505'
    DAILY_LETTER_TASK_ID = '1440504'
    TEXT_ID_RANGE = [610392, 610461]

    def __init__(self, dlg, activity_type):
        super(ActivityAnnivSecretLetter, self).__init__(dlg, activity_type)
        self._lab_letter_num = None
        self._list_letter_reward = None
        self._list_letter_page_tab = None
        self._prog_letter_collect = None
        self._nd_book_home = None
        self._nd_book_page = None
        self._left_page = None
        self._right_page = None
        self._nd_letter_open = None
        self._btn_daily_letter = None
        self._lab_time_home = None
        self._lab_time_page = None
        self._selected_page_idx = 0
        self._selected_item_idx = None
        self._page_item_range = None
        return

    def on_init_panel(self):
        self._init_parameters()
        self.__init_nodes()
        self.__init_ui_state()
        self._init_event()
        self._init_ui_event()

    def _init_parameters(self):
        self.TASK_ID = confmgr.get('c_activity_config', self._activity_type, 'cTask', default='')
        self.DAILY_LETTER_TASK_ID, self.COLLECT_TASK_ID = task_utils.get_children_task(self.TASK_ID)
        UIData = confmgr.get('c_activity_config', self._activity_type, 'cUiData', default={})
        self.LETTER_ITEM_NO = UIData.get('letter_item_no', self.LETTER_ITEM_NO)
        self.TEXT_ID_RANGE = UIData.get('text_id_range', self.TEXT_ID_RANGE)
        self.cNameTextID = confmgr.get('c_activity_config', self._activity_type, 'cNameTextID', default=610551)
        self.cRuleTextID = confmgr.get('c_activity_config', self._activity_type, 'cRuleTextID', default=610553)

    def _init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_task_content_event': self._on_page_content_changed,
           'receive_task_prog_reward_succ_event': self._on_page_content_changed,
           'receive_task_reward_succ_event': self._on_page_content_changed
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def _init_ui_event(self):
        for i in range(self.PAGE_COUNT):
            item_widget = self._list_letter_page_tab.GetItem(i)

            @item_widget.unique_callback()
            def OnClick(btn, touch, tab_id=i):
                self.select_tab(tab_id)

        self._init_page_ui_event(self.LEFT_PAGE_COUNT, True)
        self._init_page_ui_event(self.RIGHT_PAGE_COUNT, False)

        @self._nd_book_home.nd_left.lab_rules.nd_auto_fit.btn_question.unique_callback()
        def OnClick(_btn, _touch, *args):
            self.click_detail()

        @self._nd_book_page.lab_rules.nd_auto_fit.btn_question.unique_callback()
        def OnClick(_btn, _touch, *args):
            self.click_detail()

        @self._btn_daily_letter.unique_callback()
        def OnClick(btn, touch):
            self.recv_daily_letter()

        @self.panel.btn_share.unique_callback()
        def OnClick(btn, touch):
            self.click_share_home()

        @self._nd_letter_open.bar_share.btn_share2.unique_callback()
        def OnClick(btn, touch):
            self.click_share_letter()

        @self._nd_book_home.nd_right.bar_reward.btn_item.unique_callback()
        def OnClick(btn, touch, *args):
            global_data.emgr.show_item_desc_ui_event.emit(self.LETTER_ITEM_NO, None, directly_world_pos=touch.getLocation())
            return

    def _init_page_ui_event(self, count, is_left_page):
        for i in range(count):
            if is_left_page:
                item_widget = self._left_page.GetItem(i)
            else:
                item_widget = self._right_page.GetItem(i)

            @item_widget.nd_non_act.btn_item.unique_callback()
            def OnClick(btn, touch, item_id=i, is_left_page=is_left_page):
                self.click_letter(item_id, is_left_page)

            @item_widget.nd_act.btn_item.unique_callback()
            def OnClick(btn, touch, item_id=i, is_left_page=is_left_page):
                self.click_letter(item_id, is_left_page)

    def __init_nodes(self):
        self._lab_letter_num = self.panel.img_book.pnl_reward.lab_get_num
        self._list_letter_reward = self.panel.img_book.pnl_reward.list_item
        self._prog_letter_collect = self.panel.img_book.pnl_reward.bar_prog.prog
        self._list_letter_page_tab = self.panel.list_tab
        self._nd_book_home = self.panel.img_book.nd_home
        self._nd_book_page = self.panel.img_book.nd_page
        self._left_page = self._nd_book_page.list_left
        self._right_page = self._nd_book_page.list_right
        ui = global_data.ui_mgr.show_ui('LetterOpenUI', 'logic.comsys.activity')
        self._nd_letter_open = ui.panel
        self._nd_letter_open.setVisible(False)
        self._lab_time_home = self._nd_book_home.nd_left.lab_times
        self._lab_time_page = self._nd_book_page.lab_times
        self._btn_daily_letter = self._nd_book_home.nd_right.temp_get.btn_common

    def __init_ui_state(self):
        self.__init_static_ui_state()
        self.__init_dynamic_ui_state()

    def __init_static_ui_state(self):
        for i in range(self.REWARD_COUNT):
            item_widget = self._list_letter_reward.GetItem(i)
            item_widget.lab_collect.setString(str((i + 1) * 10))

        for i in range(self.PAGE_COUNT - 1):
            item_widget = self._list_letter_page_tab.GetItem(i + 1)
            page_tab_string = '%d-%d' % (i * 14 + 1, (i + 1) * 14)
            item_widget.lab_num.setString(page_tab_string)

    def __init_dynamic_ui_state(self):
        self.update_collect_ui_state()
        self.update_rewards_state()
        self.update_time()
        self.update_tab_red_point_state()
        self.update_daily_letter_state()
        self.select_tab(0)

    def _on_page_content_changed(self, *args):
        self.select_tab(self._selected_page_idx)
        self.update_letter_share_content(self._selected_item_idx)
        self.update_collect_ui_state()
        self.update_rewards_state()
        self.update_outer_tab_red_point_state()
        self.update_tab_red_point_state()
        self.update_daily_letter_state()

    def click_detail(self):
        from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
        dlg = GameRuleDescUI()
        title, rule = self.cNameTextID, self.cRuleTextID
        dlg.set_show_rule(get_text_by_id(title), get_text_by_id(rule))

    def recv_daily_letter(self):
        global_data.player.receive_task_reward(self.DAILY_LETTER_TASK_ID)

    def select_tab(self, index):
        if index is None:
            return
        else:
            self._selected_page_idx = index
            self.update_page_content(index)
            self.update_tab_select_state(index)
            return

    def click_letter(self, in_page_id, is_left_page):
        if not self._page_item_range:
            return
        if not is_left_page:
            in_page_id += self.LEFT_PAGE_COUNT
        item_id = in_page_id + self._page_item_range[0]
        self._selected_item_idx = item_id
        activated_indexes = global_data.player.get_task_content(self.COLLECT_TASK_ID, 'activated_indexes') or []
        if not self._nd_letter_open:
            ui = global_data.ui_mgr.show_ui('LetterOpenUI', 'logic.comsys.activity')
            self._nd_letter_open = ui.panel

            @self._nd_letter_open.bar_share.btn_share2.unique_callback()
            def OnClick(btn, touch):
                self.click_share_letter()

        if not (self._nd_letter_open and self._nd_letter_open.isValid()):
            return
        if item_id not in activated_indexes:
            self._nd_letter_open.setVisible(True)
            self.set_letter_open_node_to_origin()

            @self._nd_letter_open.nd_touch.unique_callback()
            def OnClick(btn, touch, tmp_item_id=item_id):
                self.click_open_letter(item_id)

        else:
            self._nd_letter_open.setVisible(True)
            self.set_letter_open_node_to_share()
            self.update_letter_share_content(item_id)

            @self._nd_letter_open.nd_touch.unique_callback()
            def OnClick(btn, touch, tmp_item_id=item_id):
                self.set_letter_open_node_to_origin()
                self._nd_letter_open.setVisible(False)

    def click_open_letter(self, item_id):
        if not (self._nd_letter_open and self._nd_letter_open.isValid()):
            return

        @self._nd_letter_open.nd_touch.unique_callback()
        def OnClick(btn, touch, tmp_item_id=item_id):
            self.set_letter_open_node_to_origin()
            self._nd_letter_open.setVisible(False)

        activated_indexes = global_data.player.get_task_content(self.COLLECT_TASK_ID, 'activated_indexes') or []
        if item_id not in activated_indexes:
            extra_info = [
             item_id]
            global_data.player.update_task_extra_info(self.COLLECT_TASK_ID, extra_info)

    def click_share_home(self):
        global_data.ui_mgr.close_ui('LetterOpenUI')
        self._nd_letter_open = None
        self.share_activity_home()
        return

    def click_share_letter(self):
        global_data.ui_mgr.close_ui('LetterOpenUI')
        self._nd_letter_open = None
        self.share_activity_letter()
        return

    def share_activity_home(self):
        from logic.comsys.share.LetterHomeShareCreator import LetterHomeShareCreator
        from logic.comsys.share.ShareUI import ShareUI
        share_creator = LetterHomeShareCreator()
        share_creator.create()
        share_creator.set_end_time(self.get_time_string())
        share_content = share_creator
        ShareUI().set_share_content_raw(share_content.get_render_texture(), share_content=share_content)

    def share_activity_letter(self):
        from logic.comsys.share.LetterOpenShareCreator import LetterOpenShareCreator
        from logic.comsys.share.ShareUI import ShareUI
        share_creator = LetterOpenShareCreator()
        share_creator.create()
        share_creator.set_letter_info(self.get_letter_text(self._selected_item_idx))
        share_content = share_creator
        from logic.comsys.share.ShareUI import ShareUI
        ShareUI().set_share_content_raw(share_content.get_render_texture(), share_content=share_content)

    def update_daily_letter_state(self):
        if global_data.player.has_receive_reward(self.DAILY_LETTER_TASK_ID):
            self._btn_daily_letter.SetEnable(False)
            self._btn_daily_letter.SetText(604029)
        else:
            self._btn_daily_letter.SetEnable(True)
            self._btn_daily_letter.SetText(604030)

    def update_rewards_state(self):
        collected_indexes = global_data.player.get_task_content(self.COLLECT_TASK_ID, 'collected_indexes') or []
        rewards_dic = task_utils.get_prog_rewards_detail_in_dict(self.COLLECT_TASK_ID)
        collected_count = len(collected_indexes) if collected_indexes else 0
        for i in range(self.REWARD_COUNT):
            item_widget = self._list_letter_reward.GetItem(i)
            tmp_target_prog = (i + 1) * 10
            reward_status = self.get_reward_status(tmp_target_prog, collected_count)
            tmp_reward_info = rewards_dic.get(tmp_target_prog)
            self.update_reward_item_state(item_widget.list_item, reward_status, tmp_reward_info, tmp_target_prog)

    def update_reward_item_state(self, item_node, receive_state, tmp_reward_info, target_prog):
        reward_id, reward_count = tmp_reward_info[1][0]
        if receive_state == ITEM_UNGAIN:
            init_tempate_mall_i_item(item_node, reward_id, item_num=reward_count, show_tips=True)
            item_node.nd_get_tips.setVisible(False)
            item_node.nd_get.setVisible(False)
            item_node.StopAnimation('get_tips')
        elif receive_state == ITEM_UNRECEIVED:

            def callback():
                global_data.player.receive_task_prog_reward(self.COLLECT_TASK_ID, target_prog)

            init_tempate_mall_i_item(item_node, reward_id, item_num=reward_count, callback=callback)
            item_node.nd_get_tips.setVisible(True)
            item_node.PlayAnimation('get_tips')
            item_node.nd_get.setVisible(False)
        elif receive_state == ITEM_RECEIVED:
            item_node.StopAnimation('get_tips')
            init_tempate_mall_i_item(item_node, reward_id, item_num=reward_count, show_tips=True)
            item_node.nd_get_tips.setVisible(False)
            item_node.nd_get.setVisible(True)

    def get_reward_status(self, target_prog, tmp_prog):
        if tmp_prog < target_prog:
            return ITEM_UNGAIN
        else:
            if global_data.player.has_receive_prog_reward(self.COLLECT_TASK_ID, target_prog):
                return ITEM_RECEIVED
            return ITEM_UNRECEIVED

    def update_letter_share_content(self, index):
        if not self._page_item_range or index is None:
            return
        else:
            self.set_letter_open_node_to_share()
            letter_content = self.get_letter_text(index)
            if letter_content and self._nd_letter_open and self._nd_letter_open.isValid():
                self._nd_letter_open.bar_share.lab_benediction.SetString(letter_content)
            return

    def get_letter_text(self, index):
        tmp_text = get_text_by_id(self.TEXT_ID_RANGE[0] + index)
        if tmp_text:
            tmp_text.replace('/n', '\n')
        return tmp_text

    def set_letter_open_node_to_origin(self):
        if self._nd_letter_open and self._nd_letter_open.isValid():
            self._nd_letter_open.bar_open.setVisible(True)
            self._nd_letter_open.bar_share.setVisible(False)

    def set_letter_open_node_to_share(self):
        if self._nd_letter_open and self._nd_letter_open.isValid():
            self._nd_letter_open.bar_open.setVisible(False)
            self._nd_letter_open.bar_share.setVisible(True)

    def update_collect_ui_state(self):
        collected_indexes = global_data.player.get_task_content(self.COLLECT_TASK_ID, 'collected_indexes') or []
        letter_num = collected_indexes or 0 if 1 else len(collected_indexes)
        self._lab_letter_num.SetString(get_text_by_id(610389).format(str(letter_num)))
        letter_num = min(self.MAX_LETTER_REWARD_NUM, letter_num)
        letter_num = max(letter_num - 10, 0)
        percent = float(letter_num) / (self.MAX_LETTER_REWARD_NUM - 10)
        percent = min(1, percent)
        self._prog_letter_collect.SetPercent(percent * 88)

    def update_page_content(self, index):
        if index == 0:
            self._nd_book_page.setVisible(False)
            self._nd_book_home.setVisible(True)
        else:
            self._nd_book_page.setVisible(True)
            self._nd_book_home.setVisible(False)
            page_item_range = [(index - 1) * 14, index * 14 - 1]
            self._page_item_range = page_item_range
            collected_indexes = global_data.player.get_task_content(self.COLLECT_TASK_ID, 'collected_indexes') or []
            activated_indexes = global_data.player.get_task_content(self.COLLECT_TASK_ID, 'activated_indexes') or []
            for collected_index in collected_indexes:
                is_collected = False
                is_activated = False
                if page_item_range[0] <= collected_index <= page_item_range[1]:
                    is_collected = True
                    if collected_index in activated_indexes:
                        is_activated = True
                    in_page_index = collected_index - page_item_range[0]
                    self.update_letter_item_status(in_page_index, collected_index, is_collected, is_activated)

        for letter_index in range(page_item_range[0], page_item_range[1] + 1):
            if letter_index not in collected_indexes:
                in_page_index = letter_index - page_item_range[0]
                self.update_letter_item_status(in_page_index, letter_index, False, False)

    def update_tab_select_state(self, index):
        for i in range(self.PAGE_COUNT):
            item_widget = self._list_letter_page_tab.GetItem(i)
            if i == index:
                item_widget.SetSelect(True)
            else:
                item_widget.SetSelect(False)

    def update_tab_red_point_state(self):
        collected_indexes = global_data.player.get_task_content(self.COLLECT_TASK_ID, 'collected_indexes') or []
        activated_indexes = global_data.player.get_task_content(self.COLLECT_TASK_ID, 'activated_indexes') or []
        for page_id in range(self.PAGE_COUNT):
            page_widget = self._list_letter_page_tab.GetItem(page_id)
            show_red = False
            page_item_range = [(page_id - 1) * 14, page_id * 14 - 1]
            for i in range(page_item_range[0], page_item_range[1] + 1):
                if i in collected_indexes and i not in activated_indexes:
                    show_red = True
                    break

            if show_red:
                page_widget.temp_red.setVisible(True)
            else:
                page_widget.temp_red.setVisible(False)

    def update_outer_tab_red_point_state(self):
        global_data.emgr.refresh_activity_redpoint.emit()

    def update_letter_item_status(self, in_page_index, letter_index, is_collected, is_activated):
        if in_page_index < self.LEFT_PAGE_COUNT:
            target_page = self._left_page
            target_index = in_page_index
        else:
            target_page = self._right_page
            target_index = in_page_index - self.LEFT_PAGE_COUNT
        target_item = target_page.GetItem(target_index)
        nd_none_flag = not is_collected
        nd_non_act_flag = is_collected and not is_activated
        nd_act_flag = is_collected and is_activated
        target_item.nd_none.setVisible(nd_none_flag)
        target_item.nd_non_act.setVisible(nd_non_act_flag)
        target_item.nd_act.setVisible(nd_act_flag)
        target_item.nd_act.lab_num.SetString(str(letter_index + 1))
        target_item.nd_none.lab_num.SetString(str(letter_index + 1))
        target_item.nd_non_act.lab_num.SetString(str(letter_index + 1))
        if nd_act_flag:
            tmp_text = self.get_letter_text(letter_index)
            self.update_letter_item_content(target_item.nd_act.lab_letter, tmp_text)

    def update_letter_item_content(self, node, content):
        if not content:
            return
        node.setString(content)

    def update_time(self):
        time_string = self.get_time_string()
        self._lab_time_home.SetString(time_string)
        self._lab_time_page.SetString(time_string)

    def get_time_string(self):
        left_time = task_utils.get_raw_left_open_time(self.COLLECT_TASK_ID)
        if left_time > 0:
            if left_time > ONE_HOUR_SECONS:
                time_string = get_text_by_id(607014).format(get_readable_time_day_hour_minitue(left_time))
            else:
                time_string = get_text_by_id(607014).format(get_readable_time(left_time))
        else:
            close_left_time = 0
            time_string = get_readable_time(close_left_time)
        return time_string

    def refresh_panel(self):
        pass

    def set_show(self, show, is_init=False):
        super(ActivityAnnivSecretLetter, self).set_show(show, is_init)

    def on_finalize_panel(self):
        global_data.ui_mgr.close_ui('LetterOpenUI')
        self._nd_letter_open = None
        self.process_event(False)
        return