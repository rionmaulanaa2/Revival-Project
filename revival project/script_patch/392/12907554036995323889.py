# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEStoryUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_1, UI_VKB_CUSTOM
from logic.comsys.common_ui.NormalConfirmUI import NormalConfirmUI
from logic.gcommon.common_const.pve_const import PVE_STORY_TYPE_ITEM
from logic.gutils.InfiniteScrollHelper import InfiniteScrollHelper
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no
from logic.gcommon.common_utils.text_utils import remove_rich_tags
from common.utils.timer import CLOCK
from common.cfg import confmgr
import common.utilities
import world
import six
import six_ex
PLAYER_TEXT_TYPE = 0
ENEMY_TEXT_TYPE = 1
NORMAL_COLOR = '#SW'
BLACK_COLOR = 5592405
RICH_TAG_DICT = {'<u': '</u>',
   '<fontname': '</fontname>',
   '<color': '</color>',
   '<size': '</size>'
   }

class PVEStoryUI(BasePanel):
    DELAY_UPDATE_TEXT_TAG = 31415926
    DELAY_TRY_CLOSE_TAG = 20231116
    DELAY_CLOSE_TAG = 20231102
    PANEL_CONFIG_NAME = 'pve/story/pve_story_main'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = UI_VKB_CUSTOM
    MOUSE_CURSOR_TRIGGER_SHOW = True
    UI_ACTION_EVENT = {}

    def on_init_panel(self, lplayer=None, story_data=None, *args, **kwargs):
        super(PVEStoryUI, self).on_init_panel()
        self.hide_main_ui()
        self.init_params(lplayer, story_data)
        self.process_events(True)
        self.init_ui_events()
        self.init_ui()

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'scene_player_setted_event': self.on_player_setted
           }
        emgr.bind_events(econf) if is_bind else emgr.unbind_events(econf)

    def on_player_setted(self, lplayer):
        if lplayer is None:
            return
        else:
            self.lplayer = lplayer
            return

    def init_params(self, lplayer, story_data):
        self.lplayer = lplayer
        self._disappearing = False
        self.fade_out_timer = None
        self.times = 0
        self._tag_stack = []
        self._need_show_item = False
        self._is_auto_mode = False
        self._is_visible = True
        self._is_fading_out = False
        self._cur_index = 0
        self._cur_text_index = 0
        self._cur_all_text_index = 0
        self._finish_text = False
        self._role_img_list = []
        if story_data.get('version', 1) == 2:
            content_id = story_data.get('abstract', {}).get('content', 0)
            level = global_data.battle.get_cur_pve_level()
            if level:
                story_data = confmgr.get('pve/story_data/story_%s' % level[0], str(content_id), default={})
        self._story_data = story_data
        self._dialogs = story_data.get('dialogs', [])
        self._abstract = story_data.get('abstract', {})
        self._story_role_data = confmgr.get('story_role_data')
        self._all_text_conf_list = self._get_all_text_conf_list()
        return

    def init_ui_events(self):

        @self.panel.btn_playback.unique_callback()
        def OnClick(btn, touch, *args):
            self._init_playback_widget()
            self.panel.nd_playback.setVisible(True)

        @self.panel.btn_close.unique_callback()
        def OnClick(btn, touch, *args):
            self.panel.nd_playback.setVisible(False)

        @self.panel.list_lab_playback.unique_callback()
        def OnScrolling(sender):
            self._update_slider()

        @self.panel.btn_visible.unique_callback()
        def OnClick(btn, touch, *args):
            self._is_visible = not self._is_visible
            self._update_panel_visible()

        @self.panel.btn_skip.unique_callback()
        def OnClick(btn, touch, *args):
            self._init_skip_widget()
            self.panel.nd_skip.setVisible(True)

        @self.panel.btn_cancel.unique_callback()
        def OnClick(btn, touch, *args):
            self.panel.nd_skip.setVisible(False)

        @self.panel.btn_confirm.unique_callback()
        def OnClick(btn, touch, *args):
            self._try_close()

        @self.panel.btn_auto.unique_callback()
        def OnClick(btn, touch, *args):
            if self._check_text_is_finish():
                self._try_close()
                return
            self._is_auto_mode = not self._is_auto_mode
            if self._is_auto_mode:
                self._update_text()
            self._update_btn_auto()

        @self.panel.nd_talk.unique_callback()
        def OnClick(btn, touch, *args):
            self.StopTimerActionByTag(self.DELAY_UPDATE_TEXT_TAG)
            if self._finish_text:
                if self._check_text_is_finish():
                    self._try_close()
                else:
                    self._update_text()
            else:
                if self._check_text_is_finish():
                    return
                self._release_fade_out_timer_timer()
                self._cur_lab_content.SetString(self._cur_text)
                self._update_text_index()

    def on_resolution_changed(self):
        super(PVEStoryUI, self).on_resolution_changed()

    def _on_click_back(self, *args):
        self._try_close()

    def init_ui(self):
        self.panel.PlayAnimation('appear')
        self._role_img_list = [self.panel.img_pic_left, self.panel.img_pic_mid, self.panel.img_pic_right]
        self._init_skip_widget()
        self._init_clue_widget()
        self._init_bg(self._story_data.get('bg_path'))
        self._update_btn_auto()
        self._update_panel_visible()
        self._update_text()

    def _update_btn_auto(self):
        btn_auto = self.panel.btn_auto
        btn_auto.EnableCustomState(True)
        btn_auto.SetSelect(self._is_auto_mode)
        if self._is_auto_mode:
            btn_auto.lab_btn.nd_auto_fit.icon_btn.SetDisplayFrameByPath('', 'gui/ui_res_2/pve/story/icon_pve_story_play.png')
        else:
            btn_auto.lab_btn.nd_auto_fit.icon_btn.SetDisplayFrameByPath('', 'gui/ui_res_2/pve/story/icon_pve_story_stop.png')

    def _update_panel_visible(self):
        self.panel.nd_talk.setVisible(self._is_visible)
        self.panel.nd_clue.setVisible(self._is_visible and self._need_show_item)
        self.panel.nd_playback.setVisible(False)
        if self._is_visible:
            self.panel.btn_visible.icon_btn.SetDisplayFrameByPath('', 'gui/ui_res_2/pve/story/icon_pve_story_visible.png')
        else:
            self.panel.btn_visible.icon_btn.SetDisplayFrameByPath('', 'gui/ui_res_2/pve/story/icon_pve_story_invisible.png')

    def _init_skip_widget(self):
        if not global_data.battle:
            return
        level = global_data.battle.get_cur_pve_level()
        if not level:
            return
        chapter, sub_level = level
        if not chapter and not sub_level:
            return
        conf = confmgr.get('pve_level_conf', 'ChapterConf', 'Content', str(chapter))
        self.panel.lab_level.setString(get_text_by_id(conf.get('title_text')))
        self.panel.lab_name.setString(get_text_by_id(conf.get('sub_title_text')))
        self.panel.lab_sub_title.setString(get_text_by_id(self._abstract.get('title')))
        self.panel.lab_describe.setString(get_text_by_id(self._abstract.get('content')))

    def _init_clue_widget(self):
        story_type = self._story_data.get('trigger_type')
        if story_type == PVE_STORY_TYPE_ITEM:
            self._need_show_item = True
            item_no = self._story_data.get('trigger_params')
            img_path = get_lobby_item_pic_by_item_no(item_no)
            self.panel.img_item.SetDisplayFrameByPath('', img_path)
            self.panel.nd_clue.setVisible(True)
        else:
            self._need_show_item = False
            self.panel.nd_clue.setVisible(False)

    def _init_bg(self, bg_path):
        if bg_path:
            self.panel.bg.SetDisplayFrameByPath('', bg_path)
            self.panel.bg.setVisible(True)
        else:
            global_data.display_agent.set_post_effect_active('gaussian_blur', True)
            self.panel.bg.setVisible(False)

    def _get_cur_text_type(self):
        return self._dialogs[self._cur_index].get('text_type', 0)

    def _get_cur_speaker(self, index=None):
        if index is None:
            index = self._cur_index
        speaker = self._dialogs[index].get('speaker', 0)
        if not speaker and self._get_cur_role_info_list(index):
            role = self._get_cur_role_info_list(index)[0]['role']
            return self._story_role_data[str(role)]['speaker']
        else:
            return speaker

    def _get_cur_role_info_list(self, index=None):
        if index is None:
            index = self._cur_index
        return self._dialogs[index].get('roles', [])

    def _get_cur_text_list(self, index=None):
        if index is None:
            index = self._cur_index
        return self._dialogs[index].get('texts', [])

    def _get_cur_text_conf(self):
        return self._get_cur_text_list()[self._cur_text_index]

    def _get_all_text_conf_list(self):
        text_conf_list = []
        for idx in range(len(self._dialogs)):
            for text in self._get_cur_text_list(idx):
                text_conf_list.append({'speaker': self._get_cur_speaker(idx),
                   'content': text['content']
                   })

        return text_conf_list

    def _get_rich_text_end_tag(self, rich_tag):
        for tag, end_tag in six_ex.items(RICH_TAG_DICT):
            if tag == rich_tag:
                return end_tag

        return ''

    def _check_text_is_finish(self):
        return self._cur_all_text_index >= len(self._all_text_conf_list)

    def check_rich_tag_stack(self):
        text = self._cur_text
        while text[self.times] == '<':
            end_index = text.find('>', self.times)
            tag = text[self.times:end_index + 1]
            self.times += len(tag)
            is_end = False
            for i, tag_info in enumerate(self._tag_stack):
                end_tag = self._get_rich_text_end_tag(tag_info[0])
                if tag == end_tag:
                    is_end = True
                    del self._tag_stack[i]
                    break

            if not is_end and tag:
                self._tag_stack.append((tag, self.times))

    def fade_out_text(self):
        text = self._cur_text
        if self.times >= len(text):
            return
        self.check_rich_tag_stack()
        if six.PY2:
            if ord(text[self.times]) < 128:
                self.times += 1
            else:
                self.times += 3
        else:
            self.times += 1
        cur_str = text[:self.times]
        for tag, start_index in self._tag_stack:
            end_tag = self._get_rich_text_end_tag(tag)
            if tag and end_tag:
                cur_str = text[:start_index] + tag + text[start_index:self.times] + end_tag

        self._cur_lab_content.SetString(cur_str)
        if self.times == len(text):
            self._update_text_index()
            if self._is_auto_mode and not self._check_text_is_finish():
                self.panel.DelayCallWithTag(0.5, self._update_text, self.DELAY_UPDATE_TEXT_TAG)

    def _update_text_index(self):
        self._finish_text = True
        self._cur_all_text_index += 1
        if self._check_text_is_finish():
            if self._is_auto_mode:
                self.panel.DelayCallWithTag(0.5, self._try_close, self.DELAY_TRY_CLOSE_TAG)
            return
        if self._cur_text_index == len(self._get_cur_text_list()) - 1:
            self._cur_index += 1
            self._cur_text_index = 0
        else:
            self._cur_text_index += 1

    def _update_text(self):
        self.times = 0
        self._finish_text = False
        self._tag_stack = []
        cur_text_conf = self._get_cur_text_conf()
        text_type = self._get_cur_text_type()
        if text_type == PLAYER_TEXT_TYPE:
            self.panel.bar_red.setVisible(False)
            bar_blue = self.panel.bar_blue
            bar_blue.setVisible(True)
            self._cur_lab_content = bar_blue.lab_content
            bar_blue.lab_title.setString(get_text_by_id(self._get_cur_speaker()))
        elif text_type == ENEMY_TEXT_TYPE:
            self.panel.bar_blue.setVisible(False)
            bar_red = self.panel.bar_red
            bar_red.setVisible(True)
            self._cur_lab_content = bar_red.lab_content
            bar_red.lab_title.setString(get_text_by_id(self._get_cur_speaker()))
        self._cur_lab_content.SetString('')
        self._cur_text = get_text_by_id(cur_text_conf.get('content'))
        cur_bg = cur_text_conf.get('bg')
        if cur_bg:
            self._init_bg(cur_bg)
        if self._cur_text_index == 0:
            self._update_role_img()
        text_len = len(six.text_type(remove_rich_tags(self._cur_text)))
        self._release_fade_out_timer_timer()
        self.fade_out_timer = global_data.game_mgr.register_logic_timer(self.fade_out_text, interval=0.05, times=text_len, mode=CLOCK)

    def _update_role_img(self):
        role_info_list = self._get_cur_role_info_list()
        need_show_place_id_list = []
        for info in role_info_list:
            place_id = info['pos'] - 1
            role_path_id = str(info['role'])
            img_role = self._role_img_list[place_id]
            role_data = self._story_role_data.get(role_path_id)
            if role_data:
                need_show_place_id_list.append(place_id)
                path = role_data.get('path')
                img_role.SetDisplayFrameByPath('', path)
                if info.get('role_state', 0) == 1:
                    img_role.SetColor(BLACK_COLOR)
                else:
                    img_role.SetColor(NORMAL_COLOR)

        for i, img_role in enumerate(self._role_img_list):
            if i in need_show_place_id_list:
                img_role.setVisible(True)
            else:
                img_role.setVisible(False)

    def _release_fade_out_timer_timer(self):
        if self.fade_out_timer:
            global_data.game_mgr.unregister_logic_timer(self.fade_out_timer)
            self.fade_out_timer = None
        return

    def _init_playback_widget(self):
        list_lab_playback = self.panel.list_lab_playback
        list_lab_playback.RecycleAllItem()
        self.total_height = 0
        for index, conf in enumerate(self._all_text_conf_list):
            self._init_list_title_item(conf)
            self._init_list_text_item(index, conf)

        old_inner_size = list_lab_playback.GetInnerContentSize()
        list_lab_playback.SetInnerContentSize(old_inner_size.width, self.total_height)
        list_lab_playback.GetContainer()._refreshItemPos()
        list_lab_playback._refreshItemPos()
        self._update_slider()

    def _update_slider(self):
        percent = self.get_slider_info()
        max_percent = 95.0
        min_percent = 5.0
        percent = min_percent + (max_percent - min_percent) * (percent / 100.0)
        if percent < min_percent:
            percent = min_percent
        if percent > max_percent:
            percent = max_percent
        self.panel.img_slider.SetPosition('50%', '{}%'.format(100.0 - percent))

    def get_slider_info(self):
        import common.utilities
        percent = 0.0
        in_height = self.panel.list_lab_playback.GetInnerContentSize().height
        out_height = self.panel.list_lab_playback.getContentSize().height
        pos_y = self.panel.list_lab_playback.getInnerContainer().getPositionY()
        if out_height - in_height == 0.0:
            percent = 0.0
        else:
            percent = common.utilities.smoothstep(out_height - in_height, 0.0, pos_y) * 100.0
        return percent

    def _init_list_title_item(self, conf):
        item = self.panel.list_lab_playback.AddItem(global_data.uisystem.load_template('pve/story/i_pve_story_describe_name'))
        lab_name = item.lab_name
        lab_name.SetString(get_text_by_id(conf.get('speaker')))
        sz = lab_name.getTextContentSize()
        w, h = item.GetContentSize()
        height = sz.height + 10
        item.SetContentSize(w, height)
        self.total_height += height
        item.ChildRecursionRePosition()

    def _init_list_text_item(self, index, conf):
        item = self.panel.list_lab_playback.AddItem(global_data.uisystem.load_template('pve/story/i_pve_story_describe'))
        lab_describe = item.lab_describe
        lab_describe.SetString(get_text_by_id(conf.get('content')))
        lab_describe.formatText()
        cur_text_index = index + 1 if self.times == len(self._cur_text) else index
        item.nd_now.setVisible(cur_text_index == self._cur_all_text_index)
        sz = lab_describe.getTextContentSize()
        w, h = item.GetContentSize()
        height = sz.height + 20
        item.SetContentSize(w, height)
        self.total_height += height
        item.ChildRecursionRePosition()

    def _try_close(self):
        self.play_disappear_anim()

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
        self.lplayer and self.lplayer.send_event('REQUEST_STOP_PVE_DIALOG')
        self.process_events(False)
        global_data.display_agent.set_post_effect_active('gaussian_blur', False)
        self.show_main_ui()
        self._release_fade_out_timer_timer()
        self._disappearing = None
        self.times = 0
        self._tag_stack = []
        self._need_show_item = False
        self._is_auto_mode = False
        self._is_visible = True
        self._is_fading_out = False
        self._cur_index = 0
        self._cur_text_index = 0
        self._cur_all_text_index = 0
        self._finish_text = False
        self._role_img_list = []
        self._story_data = None
        self._dialogs = None
        self._abstract = None
        self._story_role_data = None
        self._all_text_conf_list = None
        super(PVEStoryUI, self).on_finalize_panel()
        return