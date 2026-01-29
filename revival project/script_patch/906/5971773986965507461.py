# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEBlessDonateTipsWidget.py
from __future__ import absolute_import
from logic.gcommon.time_utility import get_server_time
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.pve_utils import get_effect_desc_text, get_bless_elem_icon
from common.utils.timer import CLOCK
from common.cfg import confmgr
DUR = 10
INVERVAL = 0.5

class PVEBlessDonateTipsWidget(object):
    TEMPLATE = 'pve/shop/open_pve_give'

    def __init__(self, panel):
        self.panel = panel
        self.init_params()
        self.init_widget()
        self.init_ui_event()
        self.process_events(True)

    def init_params(self):
        self.widget = None
        self._anim_list = []
        self._is_animing = False
        self._is_closing = False
        self._timer = None
        self._remain_time = None
        self._donate_id = None
        self._donator_id = None
        self._char_name = None
        self._bless_id = None
        self._bless_conf = confmgr.get('bless_data', default=None)
        return

    def init_widget(self):
        self.widget = global_data.uisystem.load_template_create(self.TEMPLATE, self.panel)
        self.widget.setVisible(False)

    def init_ui_event(self):

        @self.widget.btn_confirm.unique_callback()
        def OnClick(btn, touch):
            self._handle_donate_bless('accept_pve_donate_bless')
            global_data.emgr.on_pve_handle_donate_bless.emit(self._char_name, self._bless_id, True)

        @self.widget.btn_cancel.unique_callback()
        def OnClick(btn, touch):
            self._handle_donate_bless('refuse_pve_donate_bless')
            global_data.emgr.on_pve_handle_donate_bless.emit(self._char_name, self._bless_id, False)

    def _handle_donate_bless(self, handle):
        if not self._donate_id:
            return
        else:
            if not self._donator_id:
                return
            if not global_data.player or not global_data.player.logic:
                return
            if not global_data.cam_lplayer:
                return
            global_data.cam_lplayer.send_event('E_CALL_SYNC_METHOD', handle, (self._donator_id, self._donate_id))
            self.unregister_timer()
            self._remain_time = 0
            self._update_timer_label()
            self._donate_id = None
            self._donator_id = None
            return

    def process_events(self, is_bind):
        econf = {'on_pve_notify_donate_bless_info': self.on_pve_notify_donate_bless_info
           }
        global_data.emgr.bind_events(econf) if is_bind else global_data.emgr.unbind_events(econf)

    def clear(self):
        self.widget and self.widget.Destroy()
        self.widget = None
        self._anim_list = []
        self._is_animing = False
        self._is_closing = False
        self._timer = None
        self._remain_time = 0
        self._donate_id = None
        self._donator_id = None
        self._char_name = None
        self._bless_id = None
        self.unregister_timer()
        return

    def unregister_timer(self):
        if self._timer:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
            self._timer = None
        return

    def destroy(self):
        self.clear()
        self.init_params()
        self.process_events(False)
        self.panel = None
        return

    def show_tip_anim(self, donate_info, need_append=True):
        if need_append:
            self._anim_list.append(donate_info)
        if self._is_animing:
            return
        show_anim_name = 'appear'
        if self.widget and self.widget.isValid():
            self._is_animing = True
            self._update_donate_bless_info(donate_info)
            self._donate_id = donate_info.get('donate_id', '')
            self._donator_id = donate_info.get('donator_id')
            self.widget.setVisible(True)
            self.widget.PlayAnimation(show_anim_name)
            self._remain_time = max(int(donate_info.get('timestamp') + DUR - get_server_time()), float(self.widget.GetAnimationMaxRunTime(show_anim_name)) + 1)
            self._timer = global_data.game_mgr.get_logic_timer().register(func=self._update_timer_label, interval=1, mode=CLOCK)
            self._update_timer_label()

    def _update_donate_bless_info(self, donate_info):
        self._char_name = donate_info.get('char_name', '')
        self._bless_id = donate_info.get('bless_id', '')
        bless_level = donate_info.get('bless_level', 0)
        bless_conf = self._bless_conf.get(str(self._bless_id), {})
        bless_name = get_text_by_id(bless_conf.get('name_id', 0))
        self.widget.lab_name.SetString(get_text_by_id(518).format(name=self._char_name, bless=bless_name))
        desc_id = bless_conf['desc_id']
        attr_conf = bless_conf.get('attr_text_conf', [])
        self.widget.lab_describe.SetString(get_effect_desc_text(desc_id, attr_conf, bless_level))
        elem_id = bless_conf.get('elem_id', None)
        if elem_id:
            tag_icon = get_bless_elem_icon(elem_id)
            icon_type = self.widget.icon_type
            icon_type.setVisible(True)
            icon_type.SetDisplayFrameByPath('', tag_icon)
        else:
            self.widget.icon_type.setVisible(False)
        self.widget.img_item.SetDisplayFrameByPath('', bless_conf['icon'])
        return

    def _update_timer_label(self):
        if not self._anim_list:
            self.unregister_timer()
            return
        if self._remain_time <= 0:
            hide_anim_name = 'disappear'
            if self.widget and self.widget.isValid():
                self.unregister_timer()
                self._anim_list.pop(0)
                hide_anim_time = float(self.widget.GetAnimationMaxRunTime(hide_anim_name)) + INVERVAL
                self.widget.setVisible(False)
                self.widget.PlayAnimation(hide_anim_name)
                self._is_closing = True

                def hide_delay_call():
                    self._is_closing = False
                    self._is_animing = False
                    if self._anim_list:
                        next_anim_data = self._anim_list[0]
                        self.show_tip_anim(next_anim_data, False)

                self.widget.DelayCall(hide_anim_time, hide_delay_call)
            return
        self.widget.prog.SetPercentage(float(self._remain_time) / DUR * 100)
        self.widget.lab_countdown.SetString('{}s'.format(int(self._remain_time)))
        self._remain_time -= 1

    def on_pve_notify_donate_bless_info(self, donate_info):
        self.show_tip_anim(donate_info)