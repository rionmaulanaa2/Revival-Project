# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/role_profile/BondShowChatMgr.py
from __future__ import absolute_import
import six
import time
from random import randint
from common.cfg import confmgr
from logic.gutils import bond_utils
from logic.gutils import item_utils
from common.utils.timer import CLOCK
BOND_ANIM_DELAY = 5
BOND_TOUCH_CHAT_INTERVAL = 0.3

class BondShowChatMgr(object):

    def __init__(self, panel):
        self.panel = panel
        self._chat_timer = 0
        self._chat_end_time = -1
        self._last_chat_time_map = {bond_utils.DIALOG_TYPE_TOUCH: -1,
           bond_utils.DIALOG_TYPE_GIFT: -1,
           bond_utils.DIALOG_TYPE_JABBER: time.time() + BOND_ANIM_DELAY
           }

    def start(self):
        self.register_timer()
        self.refresh_jabber_time()
        self.process_event(True)

    def destroy(self):
        self.panel = None
        self.unregister_timer()
        self.process_event(False)
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'role_show_chat': self.on_role_show_chat,
           'rotate_model_display': self.refresh_jabber_time
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def refresh_jabber_time(self, *args):
        self._last_chat_time_map[bond_utils.DIALOG_TYPE_JABBER] = time.time()

    def refresh_touch_time(self, *args):
        self._last_chat_time_map[bond_utils.DIALOG_TYPE_TOUCH] = time.time()

    def refresh_all_time(self, add_time=0):
        for d_type, _ in six.iteritems(self._last_chat_time_map):
            self._last_chat_time_map[d_type] = time.time() + add_time

    def get_last_chat_jabber_time(self):
        return self._last_chat_time_map[bond_utils.DIALOG_TYPE_JABBER]

    def get_last_chat_touch_time(self):
        return self._last_chat_time_map[bond_utils.DIALOG_TYPE_TOUCH]

    def unregister_timer(self):
        if self._chat_timer > 0:
            global_data.game_mgr.get_logic_timer().unregister(self._chat_timer)
        self._chat_timer = 0

    def register_timer(self):
        self.unregister_timer()
        self._chat_timer = global_data.game_mgr.get_logic_timer().register(func=self.on_chat_timer, interval=1, mode=CLOCK)

    def on_chat_timer(self):
        now = time.time()
        if self._chat_end_time > 0 and now >= self._chat_end_time:
            self._chat_end_time = -1
            self.panel.nd_dialogue.setVisible(False)
            self.refresh_touch_time()
            self.refresh_jabber_time()
        if self.panel.has_select_role() and now - self.get_last_chat_jabber_time() >= randint(10, 20):
            dialog_id = bond_utils.get_jabber_dialog_id(self.panel.role_id)
            if dialog_id:
                self.on_role_show_chat(self.panel.role_id, dialog_id)

    def check_chat(self, chat_case):
        if chat_case == bond_utils.DIALOG_TYPE_GIFT:
            return True
        if chat_case == bond_utils.DIALOG_TYPE_JABBER:
            if self._chat_end_time < 0:
                return True
        if chat_case == bond_utils.DIALOG_TYPE_TOUCH:
            interval = time.time() - self.get_last_chat_touch_time()
            if self._chat_end_time < 0 and interval >= BOND_TOUCH_CHAT_INTERVAL:
                return True
        return False

    def can_show_chat(self):
        if not self.panel:
            return False
        return self.panel.isPanelVisible() and self.panel.is_bond_tag()

    def on_role_show_chat(self, role_id, dialog_id):
        block_anim_and_sfx = confmgr.get('ui_animate_sound', 'block_anim_and_sfx', 'Content', str(role_id), 'skins', default=[])
        from logic.gutils.dress_utils import get_role_dress_clothing_id
        skin_id = get_role_dress_clothing_id(role_id, check_default=True)
        if skin_id and skin_id in block_anim_and_sfx:
            self.refresh_jabber_time()
            self.refresh_touch_time()
            return
        if not self.can_show_chat():
            return
        if self.panel.role_id != role_id:
            return
        item_data = global_data.player.get_item_by_no(role_id)
        if not item_data or not dialog_id:
            return
        show_time = 2
        dialog_conf = confmgr.get('role_dialog_config', 'role_{}_dialog'.format(role_id), 'Content', str(dialog_id), default={})
        text = dialog_conf.get('content_text_id')
        show_time = dialog_conf.get('show_time', show_time)
        if not self.check_chat(dialog_conf['case_type']):
            return
        self._last_chat_time_map[dialog_conf['case_type']] = time.time()
        animate_sound_map = confmgr.get('ui_animate_sound', str(role_id), 'Content', str(dialog_conf.get('anim_sound_id', '')), default={})
        if animate_sound_map:
            global_data.emgr.show_extra_socket_objs.emit(0, False)
        skip_bond_effect = confmgr.get('role_info', 'RoleSkin', 'Content', str(skin_id), 'skip_bond_effect') or False
        if not skip_bond_effect:
            global_data.emgr.play_bond_effect_by_index.emit(0, role_id, dialog_id)
        self.panel.nd_dialogue.setVisible(True)
        self.panel.temp_dialogue.PlayAnimation('show')
        self.panel.temp_dialogue.lab_name.SetString(item_utils.get_lobby_item_name(role_id))
        self.panel.temp_dialogue.lab_dialogue.SetString(text)
        self.refresh_jabber_time()
        self._chat_end_time = time.time() + show_time