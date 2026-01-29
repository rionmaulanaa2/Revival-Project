# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/NewSystemPromptUI.py
from __future__ import absolute_import
from common.const.uiconst import NORMAL_LAYER_ZORDER_1, UI_VKB_CUSTOM
from common.uisys.basepanel import BasePanel
import cc
import time

class NewSystemPromptUIBase(BasePanel):
    PANEL_CONFIG_NAME = 'lobby/system_open'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = UI_VKB_CUSTOM
    UI_ACTION_EVENT = {'temp_button.btn.OnClick': '_on_click_goto_btn',
       'btn_close.OnClick': '_on_click_close_btn'
       }
    OUT_DELAY_TIMER_TAG = 31415926
    APPEAR_CHAIN_TAG = 31415927
    INIT_DELAY_CLOSE_TAG = 31415928
    DELAY_SHOW_NEXT_TAG = 31415929
    FLY_OUT_ANIM_TAG = 31415930

    def on_init_panel(self, *args, **kwargs):
        super(NewSystemPromptUIBase, self).on_init_panel()
        self._vcp_factory = self._gen_view_content_provider_factory()
        self._on_close_cb = None
        self._cur_vcp = None
        self._out_animating = False
        self._init_close = False
        init_img_icon_pos = cc.Vec2(*self.panel.img_icon.GetPosition())
        self._fly_src_wpos = self.panel.img_icon.getParent().convertToWorldSpace(init_img_icon_pos)
        self.panel.RecordAnimationNodeState('in')
        self.panel.RecordAnimationNodeState('loop')
        self.panel.RecordAnimationNodeState('loop2')
        self.panel.RecordAnimationNodeState('out')
        vcp = self._vcp_factory.peek_next()
        if vcp is None:
            self._init_close = True
            self.add_hide_count('_init_close')

            def cb():
                self.close()

            self.panel.DelayCallWithTag(0.01, cb, self.INIT_DELAY_CLOSE_TAG)
        else:
            self._vcp_factory.pop_next()
            self._play_single(vcp)
        return

    def on_finalize_panel(self):
        super(NewSystemPromptUIBase, self).on_finalize_panel()

    def _exec_only_valid(self, func):

        def real(*args, **kwargs):
            if not self.panel or not self.panel.isValid():
                return
            return func(*args, **kwargs)

        return real

    def _gen_view_content_provider_factory(self):
        raise NotImplementedError

    def _reset_anim_view(self):
        self.panel.StopAnimation('in')
        self.panel.StopAnimation('loop')
        self.panel.StopAnimation('loop2')
        self._stop_out_anim()
        self.panel.RecoverAnimationNodeState('in')
        self.panel.RecoverAnimationNodeState('loop')
        self.panel.RecoverAnimationNodeState('loop2')
        self.panel.RecoverAnimationNodeState('out')

    def _play_appear(self):
        self._reset_anim_view()
        self.panel.PlayAnimation('in')
        appear_time = self.panel.GetAnimationMaxRunTime('in')

        def appeared():
            self.panel.PlayAnimation('loop')
            self.panel.PlayAnimation('loop2')

        self.panel.DelayCallWithTag(appear_time, appeared, self.APPEAR_CHAIN_TAG)
        global_data.sound_mgr.play_ui_sound('system_open')

    def _refresh_view(self, vcp):
        pic_path = vcp.get_system_text_pic_path()
        self.panel.nd_text.img_text.SetDisplayFrameByPath('', pic_path)
        self.panel.nd_text_vx.img_text.SetDisplayFrameByPath('', pic_path)
        self.panel.vx_cut.SetMaskFrameByPath('', pic_path)
        icon_path = vcp.get_system_icon_path()
        self.panel.img_icon.SetDisplayFrameByPath('', icon_path)

    def ui_vkb_custom_func(self):
        self._try_close(True)
        return True

    def _gen_inbetween_blocking_action(self, vcp, resume_cb):
        return None

    def _try_close(self, anim):
        if self._init_close:
            return
        else:
            if anim and self._out_animating:
                return
            self.panel.stopActionByTag(self.OUT_DELAY_TIMER_TAG)
            self._out_animating = False
            if anim:
                self._out_animating = True
                ok, duration = self._play_out_anim()

                def handle_next():
                    vcp = self._vcp_factory.peek_next()
                    if vcp is None:
                        self._out_animating = False
                        self.close()
                    else:
                        self._vcp_factory.pop_next()

                        def delay_play_next():
                            self._out_animating = False
                            self._play_single(vcp)

                        self.panel.DelayCallWithTag(1, delay_play_next, self.DELAY_SHOW_NEXT_TAG)
                    return

                if ok:

                    def out_finished():
                        inbetween_action = self._gen_inbetween_blocking_action(self._cur_vcp, handle_next)
                        if callable(inbetween_action):
                            inbetween_action()
                        else:
                            handle_next()

                    self.panel.DelayCallWithTag(duration, out_finished, self.OUT_DELAY_TIMER_TAG)
                else:
                    handle_next()
            else:
                vcp = self._vcp_factory.peek_next()
                if vcp is None:
                    self.close()
                else:
                    self._vcp_factory.pop_next()
                    self._play_single(vcp)
            return

    def _on_click_goto_btn(self, *args, **kw):
        self._defautl_on_click_goto_btn()

    def _defautl_on_click_goto_btn(self):
        self._try_close(False)

    def _on_click_close_btn(self, *args, **kw):
        self._try_close(True)

    def _play_single(self, vcp):
        self._cur_vcp = vcp
        self._reset_anim_view()
        self._play_appear()
        self._refresh_view(vcp)
        self._on_play_single(vcp)

    def _on_play_single(self, vcp):
        pass

    def _play_fly_anim(self, src_wpos, dst_wpos, motion):
        start_t = time.time()

        def update_motion(_, prev_t=[start_t]):
            cur_time = time.time()
            delta = cur_time - prev_t[0]
            motion.update(delta)
            node = self.panel.img_icon
            wpos = motion.get_pos()
            lpos = node.getParent().convertToNodeSpace(wpos)
            node.setPosition(lpos)
            alpha = motion.get_alpha()
            node.setOpacity(int(alpha))
            scale = motion.get_scale()
            node.setScaleX(scale.x)
            node.setScaleY(scale.y)
            prev_t[0] = cur_time

        self.panel.StopTimerActionByTag(self.FLY_OUT_ANIM_TAG)
        duration = motion.get_max_time()
        self.panel.TimerActionByTag(self.FLY_OUT_ANIM_TAG, update_motion, duration)

    def _play_out_anim(self):
        dst_wpos, motion = self._get_fly_anim_params(self._cur_vcp)
        if dst_wpos and motion:
            self.panel.PlayAnimation('out')
            out_anim_time = self.panel.GetAnimationMaxRunTime('out')
            self._play_fly_anim(self._fly_src_wpos, dst_wpos, motion)
            duration = motion.get_max_time()
            anim_total_time = max(duration, out_anim_time)
            return (
             True, anim_total_time)
        else:
            return (
             False, 0.0)

    def _get_fly_anim_params(self, vcp):
        return self._get_fly_anim_params_core(vcp, self._fly_src_wpos)

    def _get_fly_anim_params_core(self, vcp, fly_src_wpos):
        return (None, None)

    def _stop_out_anim(self):
        self.panel.StopAnimation('out')
        self.panel.StopTimerActionByTag(self.FLY_OUT_ANIM_TAG)