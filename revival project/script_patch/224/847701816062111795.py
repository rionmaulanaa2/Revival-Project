# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_lobby_char/com_lobby_appearance/ComLobbyEmoji.py
from __future__ import absolute_import
from __future__ import print_function
from logic.gcommon.component.UnitCom import UnitCom
import game3d
from logic.gutils import interaction_utils
import weakref
import common.utils.timer as timer
from common.framework import Functor
import math3d
from common.cfg import confmgr
from logic.gcommon.item.item_const import FASHION_POS_SUIT

class ComLobbyEmoji(UnitCom):
    BIND_EVENT = {'E_EMOJI': '_on_perform_emoji',
       'E_REMOTE_EMOJI': 'remove_emoji',
       'E_SHOW_CHAT_MESSAGE': 'on_show_chat_message'
       }

    def __init__(self):
        super(ComLobbyEmoji, self).__init__()
        self.init_emoji_data()

    def init_emoji_data(self):
        self.emoji_model_id = None
        self.emoji_model = None
        self.emoji_sfx_id = None
        self.emoji_update_id = None
        self.emoji_item_id = None
        return

    def _on_perform_emoji(self, emoji_id, mecha_skin_no=None, mecha_skin_kill_cnt=None):
        model = self.ev_g_model()
        if not model:
            return
        self.remove_emoji()
        model_ref = weakref.ref(model)
        self.emoji_model_id = interaction_utils.load_emoji(model_ref, emoji_id, self.on_emoji_loaded, True, mecha_skin_no, mecha_skin_kill_cnt)
        self.emoji_item_id = emoji_id
        emoji_duraction = interaction_utils.get_emoji_duration(self.emoji_item_id)
        self.emoji_update_id = global_data.game_mgr.register_logic_timer(self.play_emoji_close, emoji_duraction, times=1, mode=timer.CLOCK)

    def on_show_chat_message(self, *args):
        self.remove_emoji()

    def remove_emoji(self):
        if self.emoji_model_id:
            interaction_utils.remove_emoji(self.emoji_model_id, self.emoji_sfx_id, self.emoji_update_id)
        global_data.emgr.show_emoji_event.emit(self.unit_obj.id, self.emoji_item_id, False)
        self.emoji_model_id = None
        self.emoji_sfx_id = None
        self.emoji_update_id = None
        self.emoji_model = None
        self.emoji_item_id = None
        return

    def destroy(self):
        self.remove_emoji()
        super(ComLobbyEmoji, self).destroy()

    def play_emoji_close(self):
        global_data.sfx_mgr.remove_sfx_by_id(self.emoji_sfx_id)
        if self.emoji_model and self.emoji_model.valid:
            interaction_utils.play_emoji_close(self.emoji_model, Functor(self.delay_remove_emoji_by_id, self.emoji_model_id))

    def delay_remove_emoji_by_id(self, emoji_id, *args):

        def cb():
            if self.emoji_model_id == emoji_id:
                self.remove_emoji()

        game3d.delay_exec(1, cb)

    def on_emoji_loaded(self, emoji_model):
        self.emoji_model = emoji_model
        if self.ev_g_is_avatar():
            fashion_data = self.ev_g_fashion_info()
            dress_id = fashion_data.get(FASHION_POS_SUIT)
            if dress_id and str(dress_id) in confmgr.get('emoticon_conf', 'LobbyEmojiConf', 'Content', default={}):
                self.config_type = str(dress_id)
            else:
                self.config_type = 'lobby_avatar'
        else:
            self.config_type = 'lobby_puppet'
        interaction_utils.set_material_type(self.emoji_model, self.config_type)
        self.play_emoji_open()

    def play_emoji_open(self):
        bind_model = self.ev_g_model()
        if not bind_model:
            return
        interaction_utils.play_emoji_open(self.emoji_model, bind_model, True, self.emoji_item_id, self.play_emoji_idle)
        self.emoji_sfx_id = interaction_utils.play_emoji_sfx_open(bind_model, True, self.emoji_item_id, self.config_type)
        global_data.emgr.show_emoji_event.emit(self.unit_obj.id, self.emoji_item_id, True)

    def play_emoji_idle(self, *args):
        global_data.sfx_mgr.remove_sfx_by_id(self.emoji_sfx_id)
        bind_model = self.ev_g_model()
        if not bind_model:
            return
        interaction_utils.play_emoji_idle(self.emoji_model, bind_model, True, self.emoji_item_id)
        self.emoji_sfx_id = interaction_utils.play_emoji_sfx_idle(bind_model, True, self.emoji_item_id, self.config_type)