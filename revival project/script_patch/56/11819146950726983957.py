# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEMainUIWidgetUI/PVEDebrisWidgetUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_1, UI_VKB_CLOSE
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.template_utils import WindowTopSingleSelectListHelper
from logic.gutils.item_utils import get_lobby_item_type
from logic.gutils.pve_lobby_utils import get_debris_chapter_is_finished, get_debris_clue_is_finished
from logic.gcommon.common_const.pve_const import PVE_STORY_REWARD_TYPE_CHAPTER, PVE_STORY_REWARD_TYPE_CLUE, PVE_STORY_DEBRIS_CACHE
from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_ROLE_SKIN, L_ITEM_TYPE_MECHA_SKIN
from .PVEDebrisInfoUI import PVEDebrisInfoUI
from .PVEDebrisFusionUI import PVEDebrisFusionUI
from .PVEDebrisDecomposeUI import PVEDebrisDecomposeUI
from .PVEDonateDebrisWidget import PVEDonateDebrisWidget
from common.cfg import confmgr
import six_ex
import cc
SELECT_ALL = 0
SELECT_FINISH = 1
SELECT_UNFINISH = 2
LOCK_CLUE_PATH = 'gui/ui_res_2/pve/fragments/main/img_pve_fragments_main_{}_{}_lock.png'
UNLOCK_CLUE_PATH = 'gui/ui_res_2/pve/fragments/main/img_pve_fragments_main_{}_{}_unlock.png'
NORMAL_BAR_PATH = 'gui/ui_res_2/pve/fragments/bar_pve_fragments_reward.png'
RECEIVE_BAR_PATH = 'gui/ui_res_2/pve/fragments/bar_pve_fragments_reward2.png'
MECHA_SKIN_PATH = 'gui/ui_res_2/item/mecha_skin/{}.png'
DRIVER_SKIN_PATH = 'gui/ui_res_2/item/driver_skin/{}.png'
RECEIVE_COLOR = 16768512
NORMAL_COLOR = 16711679
RECEIVE_CHAPTER_COLOR = '<color=0xFFDE00FF>{}</color>'
NORMAL_CHAPTER_COLOR = '<color=0xFEFFFFFF>{}</color>'
CHAPTER_SIZE = '<size=36>{}</size>'
RECEIVE_CLUE_STR = '<size=28><color=0xFFDE00FF>{}</color></size>'
NORMAL_CLUE_STR = '<size=28><color=0xFEFFFFFF>{}</color></size>'

def save_locate_chapter(chapter):
    data = confmgr.get('story_debris_chapter_data')
    config_data = [ int(cpt) for cpt in data.keys() ]
    if chapter not in config_data:
        chapter = config_data[-1]
    global_data.achi_mgr.set_cur_user_archive_data('PveDebrisChapterId', chapter)
    PVEDebrisWidgetUI.STATIC_CHAPTER_ID = chapter


def get_locate_chapter():
    chapter_id = global_data.achi_mgr.get_cur_user_archive_data('PveDebrisChapterId', 1)
    data = confmgr.get('story_debris_chapter_data')
    config_data = [ int(cpt) for cpt in data.keys() ]
    if chapter_id not in config_data:
        chapter_id = config_data[-1]
    return chapter_id


class PVEDebrisWidgetUI(BasePanel):
    PANEL_CONFIG_NAME = 'pve/fragments/pve_fragments_main'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'btn_close.OnClick': '_on_click_back'
       }
    STATIC_CHAPTER_ID = get_locate_chapter()

    def on_init_panel(self, default_chapter=None, *args, **kwargs):
        super(PVEDebrisWidgetUI, self).on_init_panel()
        self.init_params(default_chapter=default_chapter)
        self.init_ui()
        self.process_events(True)
        self.init_ui_events()

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_pve_debris_chapter_reward_update': (
                                                 self._update_chapter_state, self._update_btn_get_and_read),
           'on_pve_debris_clue_reward_update': (
                                              self._update_clue_state, self._update_btn_get_and_read),
           'on_receive_pve_story_all_reward_update': (
                                                    self._update_chapter_state, self._update_clue_state, self._update_btn_get_and_read),
           'on_pve_debris_merge': self.on_pve_debris_update,
           'on_receive_pve_story_debris_by_donator': (
                                                    self.on_pve_debris_update, self._update_red_point),
           'on_receive_all_pve_story_debris': (
                                             self.on_pve_debris_update, self._update_red_point),
           'on_get_pve_unreceived_story_debris_update': (
                                                       self._update_btn_get_and_read, self._update_red_point),
           'on_story_debris_cache_update': (
                                          self._update_btn_get_and_read, self._update_red_point),
           'receive_award_end_event': self.receive_award_end_event
           }
        emgr.bind_events(econf) if is_bind else emgr.unbind_events(econf)

    def play_anim(self):
        self.show()
        self.panel.PlayAnimation('appear')
        self.hide_main_ui()

    def init_params(self, default_chapter=None):
        self.tab_list = [{'type': SELECT_ALL,'text': 1400009,'widget': self.panel.bar_skin}, {'type': SELECT_FINISH,'text': 1400010,'widget': self.panel.nd_info_1}, {'type': SELECT_UNFINISH,'text': 1400011,'widget': self.panel.nd_info_2}]
        self._chapter_conf = confmgr.get('pve_level_conf', 'ChapterConf', 'Content')
        self._chapter_debris_conf = confmgr.get('story_debris_chapter_data')
        self._clue_conf = confmgr.get('story_debris_clue_data')
        self._story_debris_conf = confmgr.get('story_debris_data', default={})
        self._clue_id_2_item = {}
        self._reward_id_list = []
        self._open_donate_debris_after_get_model = False
        self._set_static_chapter_id(default_chapter)
        global_data.player and global_data.player.request_unreceived_story_debris()

    def _set_static_chapter_id(self, default_chapter):
        if default_chapter:
            save_locate_chapter(default_chapter)
            return
        pve_story_debris_cache = global_data.achi_mgr.get_general_archive_data().get_field(PVE_STORY_DEBRIS_CACHE, [])
        has_red_point_chapter_list = []
        for debris_no, debris_conf in six_ex.items(self._story_debris_conf):
            chapter = debris_conf.get('chapter', 1)
            if chapter in has_red_point_chapter_list:
                continue
            debris_no = int(debris_no)
            if bool(global_data.player and global_data.player.get_item_by_no(debris_no)) and debris_no not in pve_story_debris_cache:
                if chapter not in has_red_point_chapter_list:
                    has_red_point_chapter_list.append(chapter)

        if has_red_point_chapter_list:
            has_red_point_chapter_list.sort()
            save_locate_chapter(has_red_point_chapter_list[0])

    def init_ui(self):
        self.panel.PlayAnimation('show_completed')
        self.panel.btn_get_reward.EnableCustomState(True)
        self.panel.nd_btn.setVisible(True)
        self._init_debris_bar()
        self._update_view()

    def init_ui_events(self):

        @self.panel.btn_left_level.callback()
        def OnClick(btn, touch):
            _chapter_id = PVEDebrisWidgetUI.STATIC_CHAPTER_ID
            if _chapter_id == 1:
                global_data.game_mgr.show_tip(get_text_by_id(1400041))
                return
            save_locate_chapter(_chapter_id - 1)
            self._update_view()

        @self.panel.btn_right_level.callback()
        def OnClick(btn, touch):
            _chapter_id = PVEDebrisWidgetUI.STATIC_CHAPTER_ID
            if _chapter_id == len(self._chapter_conf) or _chapter_id == global_data.pve_max_chapter:
                global_data.game_mgr.show_tip(get_text_by_id(1400041))
                return
            save_locate_chapter(_chapter_id + 1)
            self._update_view()

        def _on_click_reward(btn):
            if not global_data.player:
                return
            else:
                _chapter_id = PVEDebrisWidgetUI.STATIC_CHAPTER_ID
                is_finished = get_debris_chapter_is_finished(_chapter_id)
                is_receive = global_data.player.get_debris_reward_is_receive(PVE_STORY_REWARD_TYPE_CHAPTER, _chapter_id)
                if is_finished and not is_receive:
                    global_data.player.receive_story_debris_reward(PVE_STORY_REWARD_TYPE_CHAPTER, _chapter_id)
                else:
                    chapter_debris_conf = self._chapter_debris_conf.get(str(_chapter_id))
                    reward_id = chapter_debris_conf.get('clear_reward')
                    reward_list = confmgr.get('common_reward_data', str(reward_id), 'reward_list', default=[])
                    item_no = reward_list[0][0]
                    x, y = btn.GetPosition()
                    w, _ = btn.GetContentSize()
                    x -= w * 0.5
                    wpos = btn.ConvertToWorldSpace(x, y)
                    global_data.emgr.show_item_desc_ui_event.emit(item_no, None, wpos)
                return

        @self.panel.btn_reward.callback()
        def OnClick(btn, touch):
            _on_click_reward(btn)

        @self.panel.btn_get_reward.callback()
        def OnClick(btn, touch):
            _on_click_reward(btn)

        @self.panel.btn_fusion.callback()
        def OnClick(btn, touch):
            _chapter_id = PVEDebrisWidgetUI.STATIC_CHAPTER_ID
            PVEDebrisFusionUI(chapter_id=_chapter_id)

        @self.panel.btn_recycle.callback()
        def OnClick(btn, touch):
            _chapter_id = PVEDebrisWidgetUI.STATIC_CHAPTER_ID
            PVEDebrisDecomposeUI(chapter_id=_chapter_id)

        @self.panel.btn_give.callback()
        def OnClick(btn, touch):
            PVEDonateDebrisWidget(default_tab_index=1)

        @self.panel.temp_title.lab_title.nd_auto_fit.btn_describe.callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(1400037, 1400038)

        @self.panel.btn_get_all.callback()
        def OnClick(btn, touch):
            self._on_get_all()

        @self.panel.btn_read_all.callback()
        def OnClick(btn, touch):
            self._on_read_all()

    def _on_click_back(self, *args):
        self.close()

    def _init_debris_bar(self):
        list_tab = self.panel.list_tab
        list_tab.DeleteAllSubItem()
        list_tab.SetInitCount(len(self.tab_list))

        def init_btn(node, data):
            btn_tab = node.btn_tab
            btn_tab.SetText(get_text_by_id(data.get('text', '')))

        def btn_click_cb(ui_item, data, index):
            self._cur_select_type = data.get('type')
            self._update_list_item()
            self._update_clue_state()

        self._debris_bar_wrapper = WindowTopSingleSelectListHelper()
        self._debris_bar_wrapper.set_up_list(list_tab, self.tab_list, init_btn, btn_click_cb)
        self._debris_bar_wrapper.set_node_click(list_tab.GetItem(0))

    def _update_view(self):
        self._update_chapter()
        self._update_list_item()
        self._update_chapter_state()
        self._update_clue_state()
        self._update_red_point()
        self._update_btn_get_and_read()

    def _update_chapter(self):
        _chapter_id = PVEDebrisWidgetUI.STATIC_CHAPTER_ID
        conf = self._chapter_conf.get(str(_chapter_id))
        from logic.gcommon.common_const.pve_const import LAB_TITLE_COLOR_DICT, LAB_TITLE2_COLOR_DICT
        self.panel.lab_title.SetColor(LAB_TITLE_COLOR_DICT[_chapter_id][0])
        self.panel.lab_title.EnableShadow(True, LAB_TITLE_COLOR_DICT[_chapter_id][1], 255, cc.Size(4, -4))
        self.panel.lab_title.SetString(get_text_by_id(conf.get('title_text')))
        self.panel.lab_title2.SetColor(LAB_TITLE2_COLOR_DICT[_chapter_id][0])
        self.panel.lab_title2.EnableShadow(LAB_TITLE2_COLOR_DICT[_chapter_id][1], 255, {'width': 4,'height': -4})
        self.panel.lab_title2.SetString(get_text_by_id(conf.get('sub_title_text')))
        chapter_debris_conf = self._chapter_debris_conf.get(str(_chapter_id))
        reward_id = chapter_debris_conf.get('clear_reward')
        reward_list = confmgr.get('common_reward_data', str(reward_id), 'reward_list', default=[])
        item_no = reward_list[0][0]
        lobby_item_type = get_lobby_item_type(str(item_no))
        path = ''
        if lobby_item_type == L_ITEM_TYPE_ROLE_SKIN:
            path = DRIVER_SKIN_PATH.format(item_no)
        elif lobby_item_type == L_ITEM_TYPE_MECHA_SKIN:
            path = MECHA_SKIN_PATH.format(item_no)
        self.panel.icon_reward.SetDisplayFrameByPath('', path)

    def _update_list_item(self):
        _chapter_id = PVEDebrisWidgetUI.STATIC_CHAPTER_ID
        select_type = self._cur_select_type or SELECT_ALL
        list_item = self.panel.list_item
        list_item.DeleteAllSubItem()
        self._clue_id_2_item = {}
        clue_list = self._get_clue_list(select_type)
        pve_story_debris_cache = global_data.achi_mgr.get_general_archive_data().get_field(PVE_STORY_DEBRIS_CACHE, [])
        for clue_id in clue_list:
            clue_conf = self._clue_conf.get(str(clue_id))
            clue_item = list_item.AddTemplateItem()
            clue_item.bar_tips.lab_tips.setString(get_text_by_id(clue_conf.get('name_id', '')))
            debris_list = clue_conf.get('debris')
            finish_count = 0
            is_show_red_dot = False
            debris_count = len(debris_list)
            for debris_no in debris_list:
                if bool(global_data.player and global_data.player.get_item_by_no(debris_no)):
                    finish_count += 1
                    if debris_no not in pve_story_debris_cache and not is_show_red_dot:
                        is_show_red_dot = True

            if finish_count == debris_count:
                clue_color = RECEIVE_CLUE_STR if 1 else NORMAL_CLUE_STR
                clue_str = clue_color.format(finish_count)
                clue_item.lab_prog.setString('{}/{}'.format(clue_str, debris_count))
                clue_item.img_tag.setVisible(is_show_red_dot)
                if finish_count == debris_count:
                    clue_item.nd_cut.img_pic.SetDisplayFrameByPath('', UNLOCK_CLUE_PATH.format(_chapter_id, clue_id % 100))
                else:
                    clue_item.nd_cut.img_pic.SetDisplayFrameByPath('', LOCK_CLUE_PATH.format(_chapter_id, clue_id % 100))
                self._clue_id_2_item[clue_id] = clue_item
                reward_list = confmgr.get('common_reward_data', str(clue_conf.get('clear_reward')), 'reward_list', default=[])
                self._reward_id_list.append(reward_list[0])
                reward_item_no = reward_list[0][0]
                path = confmgr.get('lobby_item', str(reward_item_no), 'icon', default='')
                clue_item.bar_reward.img_item.SetDisplayFrameByPath('', path)

                @clue_item.btn_choose.callback()
                def OnClick(btn, touch, clue_id=clue_id, clue_item=clue_item):
                    if not global_data.player:
                        return
                    is_finished = get_debris_clue_is_finished(clue_id)
                    is_receive = global_data.player.get_debris_reward_is_receive(PVE_STORY_REWARD_TYPE_CLUE, clue_id)
                    if is_finished and not is_receive:
                        global_data.player.receive_story_debris_reward(PVE_STORY_REWARD_TYPE_CLUE, clue_id)
                    else:
                        clue_item.img_tag.setVisible(False)
                        PVEDebrisInfoUI(chapter_id=_chapter_id, clue_id=clue_id)

    def _get_clue_list(self, select_type):
        _chapter_id = PVEDebrisWidgetUI.STATIC_CHAPTER_ID
        chapter_debris_conf = self._chapter_debris_conf.get(str(_chapter_id))
        clue_list = chapter_debris_conf.get('clue')
        if select_type == SELECT_ALL:
            return clue_list
        finish_clue_list = []
        unfinish_clue_list = []
        for clue_id in clue_list:
            clue_conf = self._clue_conf.get(str(clue_id))
            debris_list = clue_conf.get('debris')
            is_own = True
            for debris_no in debris_list:
                is_own = bool(global_data.player and global_data.player.get_item_by_no(debris_no))
                if not is_own:
                    unfinish_clue_list.append(clue_id)
                    break

            if is_own:
                finish_clue_list.append(clue_id)

        if select_type == SELECT_FINISH:
            return finish_clue_list
        if select_type == SELECT_UNFINISH:
            return unfinish_clue_list

    def _update_chapter_state(self):
        _chapter_id = PVEDebrisWidgetUI.STATIC_CHAPTER_ID
        is_receive = global_data.player.get_debris_reward_is_receive(PVE_STORY_REWARD_TYPE_CHAPTER, _chapter_id) if global_data.player else False
        if is_receive:
            self.panel.PlayAnimation('stamp_tips')
        else:
            self.panel.img_completed.setVisible(False)
        chapter_debris_conf = self._chapter_debris_conf.get(str(_chapter_id))
        clue_list = chapter_debris_conf.get('clue')
        finish_debris_count = 0
        all_debris_count = 0
        for clue_id in clue_list:
            clue_conf = self._clue_conf.get(str(clue_id))
            debris_list = clue_conf.get('debris')
            is_own = True
            for debris_no in debris_list:
                all_debris_count += 1
                is_own = bool(global_data.player and global_data.player.get_item_by_no(debris_no))
                if is_own:
                    finish_debris_count += 1

        is_finish = finish_debris_count == all_debris_count
        can_receive = not is_receive and is_finish
        debris_color = RECEIVE_CHAPTER_COLOR if is_finish else NORMAL_CHAPTER_COLOR
        debris_str = CHAPTER_SIZE.format(debris_color.format(finish_debris_count))
        self.panel.lab_prog.setString('{}/{}'.format(debris_str, all_debris_count))
        self.panel.lab_got.setVisible(is_receive)
        btn_get_reward = self.panel.btn_get_reward
        btn_get_reward.SetSelect(can_receive)
        reward_lab_btn_str = get_text_by_id(610637) if can_receive else get_text_by_id(601197)
        reward_lab_btn = btn_get_reward.lab_btn
        reward_lab_btn.setVisible(not is_receive)
        reward_lab_btn.setString(reward_lab_btn_str)
        reward_lab_color = RECEIVE_COLOR if can_receive else NORMAL_COLOR
        reward_lab_btn.SetColor(reward_lab_color)
        self.panel.btn_fusion.setVisible(not is_finish)
        self.panel.btn_recycle.setVisible(is_finish)

    def _update_clue_state(self):
        for clue_id, clue_item in six_ex.items(self._clue_id_2_item):
            if clue_item and clue_item.isValid():
                bar_reward = clue_item.bar_reward
                nd_get_tips = clue_item.nd_get_tips
                is_finished = get_debris_clue_is_finished(clue_id)
                is_receive = global_data.player.get_debris_reward_is_receive(PVE_STORY_REWARD_TYPE_CLUE, clue_id) if global_data.player else False
                if is_finished:
                    if is_receive:
                        bar_reward.nd_got.setVisible(True)
                        bar_reward.nd_lock.setVisible(False)
                        bar_reward.SetDisplayFrameByPath('', NORMAL_BAR_PATH)
                        nd_get_tips.setVisible(False)
                        clue_item.StopAnimation('get_tips')
                    else:
                        bar_reward.nd_got.setVisible(False)
                        bar_reward.nd_lock.setVisible(False)
                        bar_reward.SetDisplayFrameByPath('', RECEIVE_BAR_PATH)
                        nd_get_tips.setVisible(True)
                        clue_item.PlayAnimation('get_tips')
                else:
                    bar_reward.nd_got.setVisible(False)
                    bar_reward.nd_lock.setVisible(True)
                    bar_reward.SetDisplayFrameByPath('', NORMAL_BAR_PATH)
                    nd_get_tips.setVisible(False)
                    clue_item.StopAnimation('get_tips')

    def _update_red_point(self, *args):
        btn_give_red_point = self.panel.btn_give.temp_red.img_red
        if not global_data.player:
            btn_give_red_point.setVisible(False)
            return
        btn_give_red_point.setVisible(PVEDebrisWidgetUI.check_unreceived_story_debris_red_point())

    def _update_btn_get_and_read(self):
        if not global_data.player:
            return
        if global_data.player.get_unreceived_story_debris_dict() or PVEDebrisWidgetUI.check_can_receive_chapter_reward() or PVEDebrisWidgetUI.check_can_receive_clue_reward():
            self.panel.btn_get_all.setVisible(True)
            self.panel.btn_read_all.setVisible(False)
        elif PVEDebrisWidgetUI.check_debris_red_point():
            self.panel.btn_get_all.setVisible(False)
            self.panel.btn_read_all.setVisible(True)
        else:
            self.panel.btn_get_all.setVisible(False)
            self.panel.btn_read_all.setVisible(False)

    def _on_get_all(self):
        if not global_data.player:
            return
        chapter_id_list = PVEDebrisWidgetUI.get_can_receive_chapter_reward_list()
        clue_id_list = PVEDebrisWidgetUI.get_can_receive_clue_reward_list()
        if chapter_id_list or clue_id_list:
            receive_dict = {PVE_STORY_REWARD_TYPE_CHAPTER: chapter_id_list,
               PVE_STORY_REWARD_TYPE_CLUE: clue_id_list
               }
            global_data.player.receive_all_story_debris_reward(receive_dict)
        if global_data.player.get_unreceived_story_debris_dict():
            if chapter_id_list:
                self._open_donate_debris_after_get_model = True
            else:
                PVEDonateDebrisWidget()
        self._update_btn_get_and_read()

    def _on_read_all(self):
        if not global_data.player:
            return
        if PVEDebrisWidgetUI.check_debris_red_point():
            pve_story_debris_cache = []
            for debris_no in six_ex.keys(self._story_debris_conf):
                has_item = bool(global_data.player and global_data.player.get_item_by_no(int(debris_no)))
                if has_item:
                    pve_story_debris_cache.append(int(debris_no))

            global_data.achi_mgr.get_general_archive_data().set_field(PVE_STORY_DEBRIS_CACHE, pve_story_debris_cache)
            for clue_id, clue_item in six_ex.items(self._clue_id_2_item):
                if clue_item and clue_item.isValid():
                    clue_item.img_tag.setVisible(False)

        self._update_btn_get_and_read()

    def receive_award_end_event(self):
        ui = global_data.ui_mgr.get_ui('ReceiveRewardUI')
        is_showing = ui.is_showing() if ui else False
        if self._open_donate_debris_after_get_model and not is_showing:
            PVEDonateDebrisWidget()
            self._open_donate_debris_after_get_model = False

    def on_pve_debris_update(self, *args):
        self._update_list_item()
        self._update_clue_state()
        self._update_chapter_state()
        self._update_btn_get_and_read()

    @staticmethod
    def check_can_receive_chapter_reward():
        if not global_data.player:
            return False
        chapter_debris_data = confmgr.get('story_debris_chapter_data')
        for chapter_id in six_ex.keys(chapter_debris_data):
            is_finished = get_debris_chapter_is_finished(chapter_id)
            is_receive = global_data.player.get_debris_reward_is_receive(PVE_STORY_REWARD_TYPE_CHAPTER, chapter_id)
            if is_finished and not is_receive:
                return True

        return False

    @staticmethod
    def get_can_receive_chapter_reward_list():
        if not global_data.player:
            return []
        chapter_id_list = []
        chapter_debris_data = confmgr.get('story_debris_chapter_data')
        for chapter_id in six_ex.keys(chapter_debris_data):
            is_finished = get_debris_chapter_is_finished(chapter_id)
            is_receive = global_data.player.get_debris_reward_is_receive(PVE_STORY_REWARD_TYPE_CHAPTER, chapter_id)
            if is_finished and not is_receive:
                chapter_id_list.append(int(chapter_id))

        return chapter_id_list

    @staticmethod
    def check_can_receive_clue_reward():
        if not global_data.player:
            return False
        clue_data = confmgr.get('story_debris_clue_data')
        for clue_id in six_ex.keys(clue_data):
            is_finished = get_debris_clue_is_finished(clue_id)
            is_receive = global_data.player.get_debris_reward_is_receive(PVE_STORY_REWARD_TYPE_CLUE, clue_id)
            if is_finished and not is_receive:
                return True

        return False

    @staticmethod
    def get_can_receive_clue_reward_list():
        if not global_data.player:
            return []
        clue_id_list = []
        clue_data = confmgr.get('story_debris_clue_data')
        for clue_id in six_ex.keys(clue_data):
            is_finished = get_debris_clue_is_finished(clue_id)
            is_receive = global_data.player.get_debris_reward_is_receive(PVE_STORY_REWARD_TYPE_CLUE, clue_id)
            if is_finished and not is_receive:
                clue_id_list.append(int(clue_id))

        return clue_id_list

    @staticmethod
    def check_debris_red_point():
        if not global_data.player:
            return False
        pve_story_debris_cache = global_data.achi_mgr.get_general_archive_data().get_field(PVE_STORY_DEBRIS_CACHE, [])
        story_debris_data = confmgr.get('story_debris_data')
        for debris_no in six_ex.keys(story_debris_data):
            debris_no = int(debris_no)
            if bool(global_data.player.get_item_by_no(debris_no)) and debris_no not in pve_story_debris_cache:
                return True

        return False

    @staticmethod
    def check_unreceived_story_debris_red_point():
        if not global_data.player:
            return False
        return bool(global_data.player.get_unreceived_story_debris_dict())

    @staticmethod
    def check_red_point():
        if PVEDebrisWidgetUI.check_can_receive_chapter_reward():
            return True
        if PVEDebrisWidgetUI.check_can_receive_clue_reward():
            return True
        if PVEDebrisWidgetUI.check_debris_red_point():
            return True
        if PVEDebrisWidgetUI.check_unreceived_story_debris_red_point():
            return True
        return False

    def on_finalize_panel(self):
        self.process_events(False)
        self.tab_list = None
        self._chapter_conf = None
        self._chapter_debris_conf = None
        self._clue_conf = None
        self._open_donate_debris_after_get_model = False
        self._clue_id_2_item = None
        self._reward_id_list = None
        self.show_main_ui()
        super(PVEDebrisWidgetUI, self).on_finalize_panel()
        return