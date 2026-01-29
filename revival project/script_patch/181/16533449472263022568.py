# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/FightReadyTipsUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_1
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import mecha_utils
from logic.gutils.item_utils import get_item_pic_by_item_no, is_health_item
import cc
from common.utils.timer import CLOCK
SAVE_OTHERS_MESSAGE = -1
BEING_SAVED_MESSAGE = -2
from common.const import uiconst

class FightReadyTipsUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_tips/common_tips/fight_read_tips'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    IS_FULLSCREEN = True
    HIDE_ACT = 180810
    HIDE_UI_LIST = mecha_utils.BULLET_RELOAD_HIDE_UI_LIST
    HOT_KEY_FUNC_MAP = {'cancel_action': 'cancel_btn_click'
       }
    HOT_KEY_FUNC_MAP_SHOW = {'cancel_action': {'node': ['btn_cancel.temp_pc', 'btn_refuse.temp_pc']}}
    RESCUE_TAG = 210708

    def on_init_panel(self):
        self.nd_refuse_tips = None
        self.init_event()
        self.cur_battle_progress_item_id = None
        self.cur_battle_progress_msg = None
        self.add_hide_count(self.__class__.__name__)
        self.is_finishing = False
        self.cancel_callback = None
        self.refuse_callback = None
        self.hide_timer = 0
        return

    def init_event(self):
        emgr = global_data.emgr
        econf = {'scene_camera_player_setted_event': self.on_camera_player_setted,
           'battle_show_progress_event': self.show_battle_info_progress,
           'battle_close_progress_event': self.on_cancel_battle_info_progress
           }
        emgr.bind_events(econf)

    def on_finalize(self):
        self.nd_refuse_tips = None
        self.cancel_callback = None
        self.refuse_callback = None
        self.cancel_hide_timer()
        super(FightReadyTipsUI, self).on_finalize()
        return

    def do_show_panel(self):
        super(FightReadyTipsUI, self).do_show_panel()
        self.hide_main_ui(self.HIDE_UI_LIST)

    def do_hide_panel(self):
        super(FightReadyTipsUI, self).do_hide_panel()
        self.show_main_ui()

    def on_show_progress(self, *args):
        self.panel.StopAnimation('cancel')
        self.panel.StopAnimation('disappear')
        self.panel.PlayAnimation('show')
        self.cancel_hide_timer()

    def on_cancel_progress(self, *args):
        if not self.is_finishing:
            self.panel.PlayAnimation('cancel')
        self.panel.pro_reading.StopTimerAction()
        self.delay_hide(0.8)
        if self.nd_refuse_tips and self.nd_refuse_tips.isVisible():
            self.hide_refuse_tips()

    def on_finish_progress(self, *args):
        self.panel.PlayAnimation('disappear')
        self.panel.pro_reading.StopTimerAction()
        self.delay_hide(0.8)
        if self.nd_refuse_tips and self.nd_refuse_tips.isVisible():
            self.hide_refuse_tips()

    def hide_refuse_tips(self):
        if self.nd_refuse_tips:
            self.nd_refuse_tips.setVisible(False)
            self.nd_refuse_tips.StopAnimation('show_refuse_tips')
            self.panel.stopActionByTag(self.RESCUE_TAG)

    def delay_hide(self, seconds):
        tm = global_data.game_mgr.get_logic_timer()

        def hide():
            if self.get_show_count(self.__class__.__name__) >= 0:
                self.add_hide_count(self.__class__.__name__)
            self.hide_timer = None
            return

        self.cancel_hide_timer()
        self.hide_timer = tm.register(func=hide, times=1, interval=seconds, mode=CLOCK)

    def cancel_hide_timer(self):
        tm = global_data.game_mgr.get_logic_timer()
        if self.hide_timer:
            tm.unregister(self.hide_timer)
        self.hide_timer = None
        return

    def on_change_progress(self, *args):
        self.cancel_hide_timer()
        self.panel.PlayAnimation('change')
        self.panel.pro_reading.StopTimerAction()

    def on_camera_player_setted(self):
        if self.cur_battle_progress_item_id in (SAVE_OTHERS_MESSAGE, BEING_SAVED_MESSAGE):
            self.on_cancel_battle_info_progress(self.cur_battle_progress_item_id)

    def show_battle_info_progress(self, progress_time, item_id, progress_msg, callback=None, start_time=0, cancel_callback=None, icon_path=None, refuse_callback=None, **kwargs):
        self.is_finishing = False
        MIN_PERCENT = 1.8
        MAX_PERCENT = 98.8
        self.panel.StopTimerAction()
        if self.get_show_count(self.__class__.__name__) < 0:
            self.add_show_count(self.__class__.__name__)
        if self.cur_battle_progress_item_id is not None:
            if self.cancel_callback:
                self.cancel_callback(False)
            self.cur_battle_progress_item_id = item_id
            self.on_change_progress()
        else:
            self.on_show_progress()
        self.cur_battle_progress_item_id = item_id
        self.cancel_callback = cancel_callback
        self.refuse_callback = refuse_callback
        if icon_path:
            item_pic = icon_path
            self.panel.sp_item.SetDisplayFrameByPath('', item_pic)
            self.panel.lab_action.SetString(progress_msg)
        elif item_id and item_id not in (SAVE_OTHERS_MESSAGE, BEING_SAVED_MESSAGE):
            item_pic = get_item_pic_by_item_no(item_id)
            self.panel.sp_item.SetDisplayFrameByPath('', item_pic)
            self.panel.lab_action.SetString(progress_msg)
        else:
            self.panel.sp_item.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/read_bar/icon_help.png')
            self.panel.lab_action.SetString(progress_msg)
        if not item_id or is_health_item(item_id):
            self.panel.pro_reading.SetProgressTexture('gui/ui_res_2/battle/read_bar/pro_help.png')
            self.panel.img_dec.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/read_bar/dec_help.png')
            self.panel.bar.SetColor('#SG')
        else:
            self.panel.pro_reading.SetProgressTexture('gui/ui_res_2/battle/read_bar/pro_normal.png')
            self.panel.img_dec.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/read_bar/dec_tools.png')
            self.panel.bar.SetColor('#SW')
        nd_progress = self.panel.pro_reading
        btn = self.panel.btn_cancel
        self.panel.StopTimerAction()
        nd_progress.stopAllActions()
        if progress_time is None:
            self.panel.bar_pro.setVisible(False)
            btn.setVisible(False)
            self.panel.bar.SetPosition(32, '50%')
            return
        else:
            self.panel.bar.SetPosition(0, '50%')
            self.panel.bar_pro.setVisible(True)
            if cancel_callback:
                self.panel.bar.SetPosition(0, '50%')
                self.panel.btn_cancel.setVisible(True)
            else:
                self.panel.bar.SetPosition(30, '50%')
                self.panel.btn_cancel.setVisible(False)
            if refuse_callback:
                self.panel.bar.SetPosition(0, '50%')
                self.panel.btn_refuse.setVisible(True)
            else:
                self.panel.bar.SetPosition(30, '50%')
                self.panel.btn_refuse.setVisible(False)
            tf_times = self.panel.lab_time
            nd_progress.setVisible(True)
            nd_progress.setPercentage(100)
            remain_time = round(progress_time - start_time, 1)
            if tf_times:
                tf_times.SetString(str(remain_time))
            from logic.gcommon.time_utility import time
            progress_start_time = time()

            def finish():
                self.on_finish_progress()
                if callback and not self.is_finishing:
                    self.is_finishing = True
                    callback()
                else:
                    self.is_finishing = True
                self.cur_battle_progress_item_id = None
                self.cur_battle_progress_msg = None
                return

            start_percent = start_time / float(progress_time) * 100
            nd_progress.stopAllActions()
            nd_progress.setPercentage(start_percent)
            sec_text = get_text_by_id(18534)

            def update_progress_time(dt, tf_times=tf_times):
                cur_time = time()
                cur_local_time = remain_time + progress_start_time - cur_time
                if cur_local_time < 0:
                    nd_progress.stopAllActions()
                    cur_local_time = 0
                    finish()
                cur_percent = min((cur_time - progress_start_time + start_time) / float(progress_time), 1)
                cur_percent = cur_percent * (MAX_PERCENT - MIN_PERCENT) + MIN_PERCENT
                nd_progress.setPercentage(cur_percent)
                if tf_times:
                    time_str = '%.1f' % cur_local_time
                    tf_times.SetString(str(time_str) + sec_text)

            self.cur_battle_progress_msg = progress_msg
            nd_progress.StopTimerAction()
            nd_progress.TimerAction(update_progress_time, remain_time, callback=finish)
            if kwargs.get('is_stranger_rescue', False):
                show_t = global_data.achi_mgr.get_general_archive_data_value('has_been_rescue_by_stranger', default=False)
                if not show_t:
                    if not self.nd_refuse_tips:
                        self.nd_refuse_tips = global_data.uisystem.load_template_create('battle_tips/common_tips/i_fight_refuse_tips', parent=self.panel.nd_mount, name='nd_refuse_tips')
                        self.nd_refuse_tips.setVisible(False)
                    if not self.nd_refuse_tips.isVisible():
                        self.nd_refuse_tips.setVisible(True)
                        self.nd_refuse_tips.PlayAnimation('show_refuse_tips')
                        self.panel.SetTimeOut(4.0, lambda : global_data.achi_mgr.save_general_archive_data_value('has_been_rescue_by_stranger', True), tag=self.RESCUE_TAG)
            elif self.nd_refuse_tips and self.nd_refuse_tips.isVisible():
                self.hide_refuse_tips()

            @self.panel.btn_cancel.unique_callback()
            def OnClick(btn, touch, item_id=item_id):
                if self.is_finishing:
                    return
                else:
                    if self.cancel_callback:
                        self.cancel_callback()
                        self.cancel_callback = None
                    return

            @self.panel.btn_refuse.unique_callback()
            def OnClick(btn, touch, item_id=item_id):
                if self.is_finishing:
                    return
                else:
                    if self.refuse_callback:
                        self.refuse_callback()
                        self.refuse_callback = None
                    return

            return

    def on_cancel_battle_info_progress(self, item_id=None):

        def hide_ui():
            self.cancel_battle_info_progress()

        if item_id is None or item_id == self.cur_battle_progress_item_id:
            if item_id is not None:
                from logic.gutils.item_utils import get_item_name
                txt = get_text_local_content(18127)
                whole_txt = txt.format(itemtype=get_item_name(item_id))
                action = cc.FadeIn.create(0.2)
                self.show_main_ui()
                self.on_cancel_progress()
            else:
                if self.cur_battle_progress_item_id is not None:
                    return
                hide_ui()
            self.cur_battle_progress_item_id = None
            self.cur_battle_progress_msg = None
            self.cancel_callback = None
            self.is_finishing = False
        return

    def cancel_battle_info_progress(self):
        self.on_cancel_progress()
        nd_progress = self.panel.pro_reading
        nd_progress.stopAllActions()

    def cancel_btn_click(self, msg, keycode):
        if self.cancel_callback:
            self.panel.btn_cancel.OnClick(None)
        if self.refuse_callback:
            self.panel.btn_refuse.OnClick(None)
        return