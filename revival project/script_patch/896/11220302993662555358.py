# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEMainUIWidgetUI/PVEDebrisInfoUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_1, UI_VKB_CLOSE
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.template_utils import WindowTopSingleSelectListHelper, FrameLoaderTemplate
from logic.gutils.item_utils import payment_item_pic, get_lobby_item_name, get_lobby_item_desc
from logic.gutils.pve_lobby_utils import init_story_debris_item
from logic.gcommon.common_const.pve_const import PVE_STORY_DEBRIS_CACHE
from .PVEDebrisDecomposeUI import PVEDebrisDecomposeUI
from .PVEDebrisFusionUI import PVEDebrisFusionUI
from functools import cmp_to_key
from common.cfg import confmgr
import six_ex
import cc
CLUE_BG_PATH = 'gui/ui_res_2/pve/fragments/open/bg_pve_fragments_{}_{}.png'
RECEIVE_COLOR = '<size=32><color=0xFFDE00FF>{}</color></size>'
NORMAL_COLOR = '<size=32><color=0xFEFFFFFF>{}</color></size>'

class PVEDebrisInfoUI(BasePanel):
    DELAY_CLOSE_TAG = 20231106
    PANEL_CONFIG_NAME = 'pve/fragments/open_pve_fragments_info'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'nd_content.pnl_info.btn_back.OnClick': '_on_click_back'
       }

    def on_init_panel(self, chapter_id, clue_id, *args, **kwargs):
        super(PVEDebrisInfoUI, self).on_init_panel()
        self.init_params(chapter_id, clue_id)
        self.init_ui()
        self.process_events(True)
        self.init_ui_events()

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_pve_debris_merge': self.on_pve_debris_merge,
           'on_change_pve_wished_debris_id': self.update_wish_state,
           'on_donate_story_debris_succ': self.on_donate_story_debris_succ,
           'on_receive_pve_story_debris_by_donator': self.on_receive_story_debris_succ,
           'on_receive_all_pve_story_debris': self.on_receive_story_debris_succ
           }
        emgr.bind_events(econf) if is_bind else emgr.unbind_events(econf)

    def init_params(self, chapter_id, clue_id):
        self._chapter_id = chapter_id
        self._clue_id = clue_id
        self._chapter_debris_conf = confmgr.get('story_debris_chapter_data')
        self._all_clue_conf = confmgr.get('story_debris_clue_data')
        self._clue_conf = self._all_clue_conf.get(str(self._clue_id))
        self._has_debris_list = []
        self._debris_list = []
        self._debris_item_dict = {}
        self._is_finish = False
        self._frame_loader_template = None
        self._disappearing = False
        return

    def init_ui(self):
        self.panel.PlayAnimation('appear')
        self._update_panel()

    def _update_panel(self):
        self._update_btn()
        self._update_desc()
        self._update_list_item()
        self._update_prog()

    def init_ui_events(self):

        @self.panel.btn_fusion.callback()
        def OnClick(btn, touch):
            if self._is_finish:
                PVEDebrisDecomposeUI(chapter_id=self._chapter_id)
            else:
                PVEDebrisFusionUI(chapter_id=self._chapter_id)

        @self.panel.btn_describe.callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(1400037, 1400038)

    def _on_click_back(self, *args):
        self.play_disappear_anim()

    def _update_btn(self):
        chapter_debris_conf = self._chapter_debris_conf.get(str(self._chapter_id))
        clue_list = chapter_debris_conf.get('clue')
        finish_debris_count = 0
        all_debris_count = 0
        for clue_id in clue_list:
            clue_conf = self._all_clue_conf.get(str(clue_id))
            debris_list = clue_conf.get('debris')
            is_own = True
            for debris_no in debris_list:
                all_debris_count += 1
                is_own = bool(global_data.player and global_data.player.get_item_by_no(debris_no))
                if is_own:
                    finish_debris_count += 1

        self._is_finish = finish_debris_count == all_debris_count
        if self._is_finish:
            self.panel.btn_fusion.lab_btn.SetString(get_text_by_id(1400073))
        else:
            self.panel.btn_fusion.lab_btn.SetString(get_text_by_id(1400005))

    def _update_desc(self):
        self.panel.pnl_describe.lab_title.setString(get_text_by_id(self._clue_conf.get('name_id')))
        self.panel.bg.SetDisplayFrameByPath('', CLUE_BG_PATH.format(self._chapter_id, self._clue_id % 100))
        list_describe = self.panel.list_describe
        list_describe.SetInitCount(1)
        text_item = list_describe.GetItem(0)
        lab_describe = text_item.lab_describe
        lab_describe.SetString(get_text_by_id(self._clue_conf.get('desc_id')))
        lab_describe.formatText()
        sz = lab_describe.GetTextContentSize()
        old_sz = text_item.getContentSize()
        text_item.setContentSize(cc.Size(old_sz.width, sz.height))
        text_item.RecursionReConfPosition()
        old_inner_size = list_describe.GetInnerContentSize()
        list_describe.SetInnerContentSize(old_inner_size.width, sz.height)
        list_describe.GetContainer()._refreshItemPos()
        list_describe._refreshItemPos()

    def on_pve_debris_merge(self, debris_id):
        debris_conf = confmgr.get('story_debris_data', str(debris_id))
        chapter_id = debris_conf.get('chapter')
        clue_id = debris_conf.get('clue')
        self.init_params(chapter_id, clue_id)
        self._update_panel()
        self._update_btn()

    def on_donate_story_debris_succ(self, debris_id):
        clue_item = self._debris_item_dict.get(debris_id)
        if clue_item and clue_item.isValid():
            temp_item = clue_item.btn_info.temp_item
            item_num = global_data.player.get_item_num_by_no(int(debris_id)) if global_data.player else 0
            init_story_debris_item(temp_item, debris_id, item_num)
        self.update_wish_state()
        self._update_btn()

    def on_receive_story_debris_succ(self, *args):
        for debris_id, clue_item in six_ex.items(self._debris_item_dict):
            if clue_item and clue_item.isValid():
                temp_item = clue_item.btn_info.temp_item
                item_num = global_data.player.get_item_num_by_no(int(debris_id)) if global_data.player else 0
                init_story_debris_item(temp_item, debris_id, item_num)

        self.update_wish_state()
        self._update_btn()

    def _update_list_item(self):
        self._debris_list = []
        for item_no in self._clue_conf.get('debris'):
            self._debris_list.append(item_no)
            if bool(global_data.player and global_data.player.get_item_num_by_no(int(item_no))):
                self._has_debris_list.append(item_no)

        def cmp_func(a, b):
            priority_a = bool(global_data.player and global_data.player.get_item_by_no(a))
            priority_b = bool(global_data.player and global_data.player.get_item_by_no(b))
            return six_ex.compare(priority_a, priority_b)

        self._debris_list.sort(key=cmp_to_key(cmp_func), reverse=True)
        if self._frame_loader_template:
            self._frame_loader_template.destroy()
            self._frame_loader_template = None
        self._frame_loader_template = FrameLoaderTemplate(self.panel.list_item, len(self._debris_list), self.init_list_item, self._on_init_complete)
        return

    def init_list_item(self, clue_item, cur_index):
        debris_id = self._debris_list[cur_index]
        btn_info = clue_item.btn_info
        temp_item = btn_info.temp_item
        btn_item = temp_item.btn_item
        self._debris_item_dict[debris_id] = clue_item
        btn_info.lab_title.setString(get_lobby_item_name(debris_id))
        item_num = global_data.player.get_item_num_by_no(int(debris_id)) if global_data.player else 0
        lab_describe = btn_info.lab_describe
        lab_describe.setVisible(item_num > 0)
        lab_describe.setString(get_lobby_item_desc(debris_id))
        init_story_debris_item(temp_item, debris_id, item_num)
        btn_info.EnableCustomState(True)
        btn_item.EnableCustomState(True)
        if item_num > 0:
            btn_info.SetSelect(True)
            btn_item.SetSelect(True)
        else:
            btn_info.SetSelect(False)
            btn_item.SetSelect(False)

        @clue_item.btn_give.callback()
        def OnClick(btn, touch):
            from .PVEDonateDebrisWidget import PVEDonateDebrisWidget
            PVEDonateDebrisWidget(default_tab_index=1, select_debris_id=debris_id)

        @clue_item.btn_wish.callback()
        def OnClick(btn, touch):
            if not global_data.player:
                return
            global_data.player.request_change_pve_wished_debris_id(debris_id)

    def _update_prog(self):
        get_count = len(self._has_debris_list)
        all_count = len(self._clue_conf.get('debris'))
        is_all_get = get_count == all_count
        debris_color = RECEIVE_COLOR if get_count == all_count else NORMAL_COLOR
        debris_str = debris_color.format(get_count)
        self.panel.lab_prog.setString(get_text_by_id(1400006).format(debris_str, all_count))
        self.panel.list_describe.setVisible(is_all_get)
        self.panel.img_completed.setVisible(is_all_get)
        self.panel.lab_lock.setVisible(not is_all_get)

    def _on_init_complete(self):
        self._update_cache()
        self.update_wish_state()

    def _update_cache(self):
        archive_data = global_data.achi_mgr.get_general_archive_data()
        pve_story_debris_cache = archive_data.get_field(PVE_STORY_DEBRIS_CACHE, [])
        pve_story_debris_cache = list(set(pve_story_debris_cache + self._has_debris_list))
        archive_data.set_field(PVE_STORY_DEBRIS_CACHE, pve_story_debris_cache)
        global_data.emgr.on_story_debris_cache_update.emit()

    def update_wish_state(self):
        wish_debris_id = global_data.player.get_pve_wished_debris_id() if global_data.player else None
        for debris_id, clue_item in six_ex.items(self._debris_item_dict):
            if clue_item and clue_item.isValid():
                item_num = global_data.player.get_item_num_by_no(int(debris_id)) if global_data.player else 0
                btn_give = clue_item.btn_give
                btn_give.setVisible(item_num > 1)
                btn_wish = clue_item.btn_wish
                btn_wish.setVisible(item_num == 0 and wish_debris_id != debris_id)
                clue_item.lab_wished.setVisible(wish_debris_id == debris_id)

        return

    def play_disappear_anim(self):
        if self._disappearing:
            return
        self._disappearing = True
        anim_time = self.panel.GetAnimationMaxRunTime('disappear')

        def delay_call(*args):
            self._disappearing = False
            self.close()

        self.panel.StopAnimation('disappear')
        self.panel.DelayCallWithTag(anim_time, delay_call, self.DELAY_CLOSE_TAG)
        self.panel.PlayAnimation('disappear')

    def on_finalize_panel(self):
        self.process_events(False)
        self._disappearing = None
        self._clue_id = None
        self._clue_conf = None
        self._has_debris_list = None
        self._debris_list = None
        if self._frame_loader_template:
            self._frame_loader_template.destroy()
            self._frame_loader_template = None
        super(PVEDebrisInfoUI, self).on_finalize_panel()
        return