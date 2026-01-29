# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Granbelm/GranbelmRuneConfUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_2, BASE_LAYER_ZORDER
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_const.battle_const import GRANBELM_MAX_RUNE_COUNT
from logic.gutils import granbelm_utils
from common.const import uiconst

class GranbelmRuneConfUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_moon/fight_moon_choose_button'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_talent.OnClick': '_on_click_conf'
       }
    HOT_KEY_FUNC_MAP = {'toggle_moon_rune_list.DOWN': 'keyboard_toggle_moon_rune_list'
       }
    HOT_KEY_FUNC_MAP_SHOW = {'toggle_moon_rune_list': {'node': 'btn_talent.temp_pc'}}
    TAG1 = 20200427
    TAG2 = 20200510

    def on_init_panel(self, *args, **kwargs):
        super(GranbelmRuneConfUI, self).on_init_panel()
        self.init_params()
        self.init_widget()
        self.process_events(True)
        self.init_custom_com()
        self.panel.nd_desc.setVisible(False)
        self.update_rune_count(self._rune_count, True)
        self.update_rune_id(self._rune_id)
        self.update_region_tag(self._region_tag)
        self.panel.RecordAnimationNodeState('loop')

    def init_custom_com(self):
        from logic.comsys.setting_ui.CustomUIProxy import init_custom_com
        init_custom_com(self, {})

    def init_params(self):
        if global_data.cam_lplayer:
            count, _id, tag = global_data.cam_lplayer.ev_g_granbelm_rune_data()
            self._rune_count = count
            self._rune_id = _id
            self._region_tag = tag
        else:
            self._rune_count = 0
            self._rune_id = None
            self._region_tag = False
        self.tip_widget = None
        self._play_loop_tag = False
        self.finish_tips_played_tag = False
        return

    def init_widget(self):
        self.finish_tips_widget = global_data.uisystem.load_template_create('battle_tips/full_moon/i_gear_full_tips', self.panel)
        self.finish_tips_widget.setVisible(False)
        self.region_tips_widget = global_data.uisystem.load_template_create('battle_tips/full_moon/gear_up_tips', self.panel)
        self.region_tips_widget.setVisible(False)

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'scene_camera_player_setted_event': self.on_cam_player_setted,
           'update_granbelm_rune_count': self.update_rune_count,
           'update_granbelm_rune_id': self.update_rune_id,
           'update_granbelm_region_tag': self.update_region_tag,
           'on_region_show_tips': self.on_region_show_tips
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_cam_player_setted(self):
        if global_data.cam_lplayer:
            count, _id, tag = global_data.cam_lplayer.ev_g_granbelm_rune_data()
            self._rune_count = count
            self._rune_id = _id
            self._region_tag = tag
        else:
            self._rune_count = 0
            self._rune_id = None
            self._region_tag = False
        self.update_rune_count(self._rune_count, True)
        self.update_rune_id(self._rune_id)
        self.update_region_tag(self._region_tag)
        return

    def update_rune_count(self, rune_count, is_self_inc):
        if rune_count <= GRANBELM_MAX_RUNE_COUNT:
            if rune_count > self._rune_count:
                if not self._region_tag and is_self_inc:
                    self.panel.PlayAnimation('increase')
                else:
                    self.panel.PlayAnimation('get')
            self.panel.prog_gear.SetPercent(rune_count * 100.0 / GRANBELM_MAX_RUNE_COUNT)
            self._rune_count = rune_count
            self.panel.lab_num.SetString(str(rune_count) + '/200')
            if rune_count == GRANBELM_MAX_RUNE_COUNT:
                self.on_granbelm_rune_finish()

    def on_granbelm_rune_finish(self):
        if not self._rune_id:
            if self._rune_count == GRANBELM_MAX_RUNE_COUNT:
                if not self.finish_tips_played_tag:
                    self.panel.img_gear.SetDisplayFrameByPath('', granbelm_utils.get_rune_pic_path(True))
                    ani_time = float(self.finish_tips_widget.GetAnimationMaxRunTime('show'))
                    self.finish_tips_widget.setVisible(True)
                    self.finish_tips_widget.PlayAnimation('show')

                    def delay_call():
                        self.panel.PlayAnimation('full')
                        self.finish_tips_widget.setVisible(False)

                    self.panel.DelayCallWithTag(ani_time, delay_call, self.TAG1)
                    self.finish_tips_played_tag = True
                if not self.panel.IsPlayingAnimation('loop'):
                    self.panel.PlayAnimation('loop')
                    self._play_loop_tag = True

    def _on_click_conf(self, *args):
        if not global_data.cam_lplayer or not global_data.cam_lplayer.ev_g_is_avatar():
            return
        if not self._rune_id:
            global_data.ui_mgr.show_ui('GranbelmRuneListUI', 'logic.comsys.battle.Granbelm')
        else:
            desc_text = granbelm_utils.get_rune_ability_dict(self._rune_id).get('desc')
            self.panel.nd_desc.temp_talent_desc.SetString(get_text_by_id(desc_text))

            @self.panel.nd_desc.temp_talent_desc.nd_bg.unique_callback()
            def OnBegin(_layer, _touch, *args):
                self.panel.nd_desc.setVisible(False)

            self.panel.nd_desc.setVisible(True)

    def update_rune_id(self, rune_id):
        if rune_id:
            self._rune_id = rune_id
            self._set_rune_display()
        else:
            self._revert_rune_display()

    def _set_rune_display(self):
        self.panel.img_gear.setVisible(False)
        self.panel.img_stone.SetDisplayFrameByPath('', granbelm_utils.get_rune_ability_dict(self._rune_id).get('path'))
        self.panel.img_stone.setVisible(True)
        self.panel.PlayAnimation('success')
        self.panel.lab_activate.setVisible(True)
        self.panel.lab_num.setVisible(False)
        self.panel.prog_gear.setVisible(False)
        self.panel.prog_gear_bkg.setVisible(False)
        if self._play_loop_tag:
            self.panel.StopAnimation('loop')
            self.panel.RecoverAnimationNodeState('loop')
            self._play_loop_tag = False
        self.panel.nd_up.setVisible(False)
        if self.panel.IsPlayingAnimation('up'):
            self.panel.StopAnimation('up')

    def _revert_rune_display(self):
        self.panel.img_gear.setVisible(True)
        self.panel.img_stone.setVisible(False)
        self.panel.lab_activate.setVisible(False)
        self.panel.lab_num.setVisible(True)
        self.panel.prog_gear.setVisible(True)
        self.panel.prog_gear_bkg.setVisible(True)

    def update_region_tag(self, tag):
        self._region_tag = tag
        is_playing = self.panel.IsPlayingAnimation('up')
        if self._rune_id:
            self.panel.nd_up.setVisible(False)
            if is_playing:
                self.panel.StopAnimation('up')
            return
        if tag:
            self.panel.nd_up.setVisible(True)
            if not is_playing:
                self.panel.PlayAnimation('up')
        else:
            self.panel.nd_up.setVisible(False)
            if is_playing:
                self.panel.StopAnimation('up')

    def on_region_show_tips(self):
        ani_time = float(self.finish_tips_widget.GetAnimationMaxRunTime('show'))
        self.region_tips_widget.setVisible(True)
        self.region_tips_widget.PlayAnimation('show')

        def delay_call():
            self.panel.PlayAnimation('full')
            self.finish_tips_widget.setVisible(False)

        self.panel.DelayCallWithTag(ani_time, delay_call, self.TAG2)

    def on_finalize_panel(self):
        self.process_events(False)
        self._rune_count = -1
        if self.tip_widget:
            self.tip_widget.destroy()
            self.tip_widget = None
        self._play_loop_tag = False
        self.destroy_widget('custom_ui_com')
        super(GranbelmRuneConfUI, self).on_finalize_panel()
        return

    def keyboard_toggle_moon_rune_list(self, msg, keycode):
        if global_data.ui_mgr.get_ui('GranbelmRuneListUI'):
            global_data.ui_mgr.close_ui('GranbelmRuneListUI')
        else:
            self._on_click_conf()