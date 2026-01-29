# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityMidAutumn/ActivityMidAutumnShare.py
from __future__ import absolute_import
from __future__ import print_function
from logic.comsys.activity.ActivityTemplate import ActivityBase
from common.cfg import confmgr
from logic.gutils import task_utils, activity_utils
from logic.gcommon import time_utility as tutil
from logic.comsys.share.ShareTemplateBase import ShareTemplateBase, async_disable_wrapper

class MidAutumnShareCreator(ShareTemplateBase):
    KIND = 'I_SHARE_MID_AUTUMN'

    def __init__(self):
        super(MidAutumnShareCreator, self).__init__()

    @async_disable_wrapper
    def create(self, parent=None, init_cb=None, tmpl=None):
        super(MidAutumnShareCreator, self).create(parent, tmpl)
        from logic.gcommon.common_const.lang_data import LANG_CN, LANG_ZHTW, LANG_JA, LANG_EN
        from logic.gcommon.common_utils.local_text import get_cur_text_lang
        self.panel.btn_share.setVisible(False)
        self.panel.nd_tips.setVisible(False)
        self.panel.nd_tips.setVisible(False)
        self.panel.btn_question.setVisible(False)
        self.panel.lab_time_01.setVisible(False)
        self.panel.btn_close.setVisible(False)
        self.panel.SetContentSize(1334, 750)
        self.panel.ChildResizeAndPosition()
        self.panel.nd_contain.SetPosition('50%-106', '50%2')
        self.panel.nd_title.SetPosition('50%324', '50%-1')
        pos_dict = {LANG_CN: ('50%-42', '50%-176'),
           LANG_ZHTW: ('50%-40', '50%-159'),
           LANG_EN: ('50%-52', '50%-269'),
           LANG_JA: ('50%-52', '50%-227')
           }
        pos = pos_dict.get(get_cur_text_lang(), pos_dict[LANG_EN])
        self.panel.nd_dec_seal.SetPosition(*pos)
        if callable(init_cb):
            init_cb()

    def destroy(self):
        super(MidAutumnShareCreator, self).destroy()


class ActivityMidAutumnShare(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityMidAutumnShare, self).__init__(dlg, activity_type)
        self.parent_task_id = confmgr.get('c_activity_config', self._activity_type, 'cTask', default='')
        self.children_task_list = task_utils.get_children_task(self.parent_task_id)
        self.activity_conf = confmgr.get('c_activity_config', self._activity_type)
        self._share_content = None
        return

    def on_init_panel(self):
        self.process_event(True)
        if not self.panel.HasRecordedAnimationNodeState('show'):
            self.panel.RecordAnimationNodeState('show')
        else:
            self.panel.RecoverAnimationNodeState('show')
        if not self.panel.HasRecordedAnimationNodeState('loop'):
            self.panel.RecordAnimationNodeState('loop')
        else:
            self.panel.RecoverAnimationNodeState('loop')
        self.panel.PlayAnimation('show')
        self.panel.PlayAnimation('loop')

        @self.panel.btn_question.callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(int(self.activity_conf['cNameTextID']), int(self.activity_conf['cDescTextID']))

        from logic.gcommon.common_const.lang_data import LANG_CN, LANG_ZHTW, LANG_JA, LANG_EN
        from logic.gcommon.common_utils.local_text import get_cur_text_lang
        pos_dict = {LANG_CN: ('50%-42', '50%-176'),
           LANG_ZHTW: ('50%-40', '50%-159'),
           LANG_EN: ('50%-52', '50%-269'),
           LANG_JA: ('50%-52', '50%-227')
           }
        pos = pos_dict.get(get_cur_text_lang(), pos_dict[LANG_EN])
        self.panel.nd_dec_seal.SetPosition(*pos)
        self.update_tips_show()
        conf = confmgr.get('c_activity_config', str(self._activity_type), default=None)
        if conf:
            begin_time = conf.get('cBeginTime', 0)
            end_time = conf.get('cEndTime', 0)
            start_date = tutil.get_date_str('%m.%d', begin_time)
            finish_date = tutil.get_date_str('%m.%d', end_time)
            print('start data', start_date)
            self.panel.lab_time_01.SetString(get_text_by_id(604006).format(start_date, finish_date))
        widget_type = activity_utils.get_activity_widget_type(self._activity_type)
        global_data.emgr.change_activity_main_close_btn_visibility.emit(widget_type, False)

        @self.panel.btn_close.callback()
        def OnClick(btn, touch):
            global_data.emgr.trigger_activity_main_close_btn.emit(widget_type)

        @self.panel.btn_share.callback()
        def OnClick(btn, touch):
            from logic.comsys.share.ShareUI import ShareUI
            share_ui = ShareUI(parent=self.panel)

            def share_inform_func():
                import cc
                if global_data.player:
                    act = [cc.DelayTime.create(0.3),
                     cc.CallFunc.create(lambda : global_data.player.share_activity('activity_20104')),
                     cc.CallFunc.create(lambda : global_data.player.share())]
                    self.panel.runAction(cc.Sequence.create(act))
                self.update_tips_show()

            share_ui.set_share_inform_func(share_inform_func)

            def init_cb():
                if share_ui and share_ui.is_valid():
                    share_ui.set_share_content_raw(self._share_content.get_render_texture(), need_scale=True, share_content=self._share_content)

            if not getattr(self, '_share_content', None):
                self._share_content = MidAutumnShareCreator()
                self._share_content.create(parent=None, init_cb=init_cb)
            else:
                init_cb()
            return

        return

    def on_finalize_panel(self):
        self.process_event(False)
        self.children_task_list = []
        if self._share_content:
            self._share_content.destroy()
        self._share_content = None
        widget_type = activity_utils.get_activity_widget_type(self._activity_type)
        global_data.emgr.change_activity_main_close_btn_visibility.emit(widget_type, True)
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self.update_reward_list,
           'task_prog_changed': self.update_reward_list
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def update_reward_list(self, *args):
        self.update_tips_show()
        global_data.emgr.refresh_activity_redpoint.emit()

    def update_tips_show(self):
        player = global_data.player
        if not player:
            return
        is_finished = global_data.player.is_task_finished(self.parent_task_id)
        self.panel.nd_tips.setVisible(not is_finished)