# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/login/CharacterSelectUINew.py
from __future__ import absolute_import
import time
from common.uisys.basepanel import BasePanel
from logic.gutils.salog import SALog
from logic.gutils.template_utils import show_account_find_dialog
from common.const.uiconst import UI_VKB_NO_EFFECT
from logic.gutils import qte_guide_utils

class CharacterSelectUINew(BasePanel):
    PANEL_CONFIG_NAME = 'guide/guide_choose_role'
    UI_VKB_TYPE = UI_VKB_NO_EFFECT
    IS_FULLSCREEN = True
    RECREATE_WHEN_RESOLUTION_CHANGE = True
    UI_ACTION_EVENT = {'btn_left.OnClick': 'on_click_left',
       'btn_right.OnClick': 'on_click_right'
       }
    DELAY_MAIN_DISAPPEAR_TAG = 31415926

    def on_init_panel(self, **kwargs):
        super(CharacterSelectUINew, self).on_init_panel(*kwargs)
        self._init_members()
        self._init_view()
        self.panel.PlayAnimation('show')
        self.panel.PlayAnimation('loop')
        self._opt_time = 0
        self.role_id = None
        salog_writer = SALog.get_instance()
        if salog_writer:
            salog_writer.write(SALog.TUTORIAL, 1)
        show_account_find_dialog()
        return

    def on_finalize_panel(self):
        if self.played_video:
            inst = global_data.singleton_map.get('VideoPlayer', None)
            if inst:
                inst.force_stop_video()
        super(CharacterSelectUINew, self).on_finalize_panel()
        return

    def _init_members(self):
        self._opt_time = 0
        self.role_id = None
        self.played_video = False
        return

    def _init_view(self):
        support_spine = global_data.feature_mgr.is_support_spine_3_8()
        self._male_panel = global_data.uisystem.load_template_create('guide/role_choose_rom', parent=self.panel)
        if self.IS_FULLSCREEN:
            self._male_panel.SeFullBgMode()
        self._male_panel.setVisible(False)
        self._male_panel.spine_role_rom.setVisible(support_spine)
        self._male_panel.img_role_rom.setVisible(not support_spine)
        self._female_panel = global_data.uisystem.load_template_create('guide/role_choose_ningning', parent=self.panel)
        if self.IS_FULLSCREEN:
            self._female_panel.SeFullBgMode()
        self._female_panel.setVisible(False)
        self._female_panel.spine_role_ning.setVisible(support_spine)
        self._female_panel.img_role_ning.setVisible(not support_spine)
        is_huawei = global_data.deviceinfo.is_huawei_device()
        if not is_huawei:
            from common.cinematic.VideoPlayer import VideoPlayer
            inst = VideoPlayer()
            inst.force_stop_video()
            inst.play_video('video/choose_pilot_bg.mp4', cb=None, repeat_time=0, bg_play=True, disable_sound_mgr=False, can_jump=False)
            self.played_video = True
            self.panel.nd_bg.setVisible(False)
        else:
            self.played_video = False
            self.panel.nd_bg.setVisible(True)
        self._init_ui_event()
        return

    def _init_ui_event(self):
        panel = self._male_panel
        panel.temp_btn_choose.btn_major.BindMethod('OnClick', self.on_confirm)
        panel.btn_other_role.BindMethod('OnClick', self.on_to_female)
        panel = self._female_panel
        panel.btn_choose.btn_major.BindMethod('OnClick', self.on_confirm)
        panel.btn_other_role.BindMethod('OnClick', self.on_to_male)

    def _can_intro_interact(self):
        return not (self._male_panel.isVisible() or self._female_panel.isVisible())

    def main_to_select(self, opt):
        if self.panel.IsPlayingAnimation('disappear'):
            return
        delay = self.panel.GetAnimationMaxRunTime('disappear')
        self.panel.PlayAnimation('disappear')
        self.panel.DelayCallWithTag(delay, lambda : self.character_select(opt), self.DELAY_MAIN_DISAPPEAR_TAG)

    def on_click_left(self, *_):
        if not self._can_intro_interact():
            return
        self.main_to_select(1)

    def on_click_right(self, *_):
        if not self._can_intro_interact():
            return
        self.main_to_select(2)

    def on_to_male(self, *_):
        self.character_select(1)

    def on_to_female(self, *_):
        self.character_select(2)

    def character_select(self, opt):
        cur_time = time.time()
        if cur_time - self._opt_time < 0.5:
            return
        self._opt_time = cur_time
        self._character_select(opt)

    def _character_select(self, opt):
        if opt == 1:
            self.choose_male()
        else:
            self.choose_female()

    def _choose_gender_core(self, role_id, prev_panel, cur_panel):
        prev_panel.setVisible(False)
        prev_panel.StopAnimation('loop')
        cur_panel.setVisible(True)
        cur_panel.PlayAnimation('show')
        cur_panel.PlayAnimation('loop')
        self.role_id = role_id

    def choose_male(self):
        self._choose_gender_core('12', self._female_panel, self._male_panel)

    def choose_female(self, *_):
        self._choose_gender_core('11', self._male_panel, self._female_panel)

    def on_confirm(self, *_):
        role_id = self.role_id
        if role_id is None:
            return
        else:
            qte_guide_utils.save_qte_chosen_role_id(role_id)
            global_data.owner_entity.start_newbie_qte_guide(role_id)
            self.close()
            return