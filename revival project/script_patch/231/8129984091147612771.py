# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEEndVxUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const import uiconst
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.cfg import confmgr
from logic.gcommon.common_const.pve_const import SETTLE_WIN, SETTLE_LOSE, SETTLE_SAVE

class PVEEndVxUI(BasePanel):
    DELAY_CLOSE_TAG = 20231106
    PANEL_CONFIG_NAME = 'pve/end/open_pve_end_foreground'
    DLG_ZORDER = uiconst.NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'nd_close.OnClick': 'on_click_next'
       }
    VX_SOUND = {SETTLE_WIN: 'bt_victory',
       SETTLE_LOSE: 'bt_failure',
       SETTLE_SAVE: 'bt_draw'
       }
    ANIM_DICT = {SETTLE_WIN: ('appear', 'disappear', 'loop'),
       SETTLE_LOSE: ('appear_2', 'disappear_2', 'loop_2'),
       SETTLE_SAVE: ('appear_3', 'disappear_3', 'loop_3')
       }
    WIN_DIFFICULTY_PATH = 'gui/ui_res_2/txt_pic/text_pic_en/pve/txt_pve_chat_difficulty_{}_pass.png'

    def on_init_panel(self, settle_dict, finish_cb=None, *args, **kwargs):
        super(PVEEndVxUI, self).on_init_panel(*args, **kwargs)
        self.finish_cb = finish_cb
        self.settle_dict = settle_dict
        self._disappearing = False
        self.ret = 0
        self.begin_show()

    def on_finalize_panel(self):
        self._disappearing = None
        self.finish_cb = None
        super(PVEEndVxUI, self).on_finalize_panel()
        return

    def begin_show(self):
        if self.settle_dict.get('save_exit', False):
            self.ret = SETTLE_SAVE
        else:
            self.ret = SETTLE_WIN if self.settle_dict.get('rank', 0) == 1 else SETTLE_LOSE
        global_data.sound_mgr.play_ui_sound(self.VX_SOUND[self.ret])
        chapter_id = self.settle_dict.get('chapter', 1)
        difficulty = self.settle_dict.get('difficulty', 1)
        chapter_conf = confmgr.get('pve_level_conf', 'ChapterConf', 'Content', str(chapter_id))
        if self.ret == SETTLE_WIN:
            self.panel.nd_defeat.setVisible(False)
            self.panel.nd_file.setVisible(False)
            nd_victory = self.panel.nd_victory
            bar_info = nd_victory.bar_info
            bar_info.lab_name.setString(get_text_by_id(chapter_conf.get('title_text')))
            bar_info.lab_level.setString(get_text_by_id(chapter_conf.get('desc_text')))
            nd_victory.setVisible(True)
            self.panel.txt_title.SetDisplayFrameByPath('', self.WIN_DIFFICULTY_PATH.format(difficulty - 1))
        elif self.ret == SETTLE_LOSE:
            self.panel.nd_victory.setVisible(False)
            self.panel.nd_file.setVisible(False)
            nd_defeat = self.panel.nd_defeat
            bar_info = nd_defeat.bar_info
            bar_info.lab_name.setString(get_text_by_id(chapter_conf.get('title_text')))
            bar_info.lab_level.setString(get_text_by_id(chapter_conf.get('desc_text')))
            nd_defeat.setVisible(True)
        elif self.ret == SETTLE_SAVE:
            self.panel.nd_victory.setVisible(False)
            self.panel.nd_defeat.setVisible(False)
            nd_file = self.panel.nd_file
            bar_info = nd_file.bar_info
            bar_info.lab_name.setString(get_text_by_id(chapter_conf.get('title_text')))
            bar_info.lab_level.setString(get_text_by_id(chapter_conf.get('desc_text')))
            nd_file.setVisible(True)
        self.panel.PlayAnimation(self.ANIM_DICT[self.ret][0])
        self.panel.PlayAnimation(self.ANIM_DICT[self.ret][2])

    def on_click_next(self, *args):
        self.play_disappear_anim()

    def play_disappear_anim(self):
        if self._disappearing:
            return
        anim_name = self.ANIM_DICT[self.ret][1]
        self._disappearing = True
        anim_time = self.panel.GetAnimationMaxRunTime(anim_name)

        def delay_call(*args):
            self._disappearing = False
            if self.finish_cb and callable(self.finish_cb):
                self.finish_cb()
            self.close()

        self.panel.StopAnimation(anim_name)
        self.panel.DelayCallWithTag(anim_time, delay_call, self.DELAY_CLOSE_TAG)
        self.panel.PlayAnimation(anim_name)