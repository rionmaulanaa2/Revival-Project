# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/meow/MeowPostboxUI.py
from __future__ import absolute_import
from logic.gcommon.cdata import meow_capacity_config
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_CLOSE
from logic.comsys.common_ui.ItemNumBtnWidget import ItemNumBtnWidget
from mobile.common.EntityManager import EntityManager
from logic.gutils.item_utils import get_item_max_count_weekly
from logic.gcommon.item.item_const import ITEM_NO_MEOW_COIN
import cc

class MeowPostboxUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/battle_coin'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'btn_back.OnClick': 'on_close',
       'btn_send.OnClick': 'on_send_coin'
       }
    MOUSE_CURSOR_TRIGGER_SHOW = True
    GLOBAL_EVENT = {'scene_player_setted_event': 'on_player_setted'
       }
    HOT_KEY_FUNC_MAP = {'scene_interaction': 'keyboard_interaction'
       }

    def on_init_panel(self, *args, **kwargs):
        self.init_parameters()
        self.hide_main_ui(['SceneInteractionUI'])
        self.item_num_btn_widget = ItemNumBtnWidget(self.panel.nd_control)

    def on_finalize_panel(self):
        self.unregister_event()
        self.destroy_widget('item_num_btn_widget')
        self.show_main_ui()

    def init_parameters(self):
        self.item_total_num = 999
        self.mail_box_size = 0
        self.mail_box_num = 0
        self.bag_num = 0
        self.send_num = 0
        self.lplayer = None
        self.mail_entity_id = None
        return

    def set_postbox_entity_id(self, entity_id):
        self.mail_entity_id = entity_id
        self.panel.stopAllActions()
        self.on_player_setted(global_data.cam_lplayer)
        self.item_num_btn_widget.panel.btn_increase_max.OnClick(None)
        self.start_check_pos_player()
        return

    def keyboard_interaction(self, msg, keycode):
        self.close()

    def on_player_setted(self, lplayer):
        self.unregister_event()
        if lplayer is None:
            return
        else:
            self.lplayer = lplayer
            self.register_event()
            self._on_meow_coin_change()
            return

    def register_event(self):
        if not self.lplayer:
            return
        register_event = self.lplayer.regist_event
        register_event('E_MEOW_COIN_CHANGE', self._on_meow_coin_change)

    def unregister_event(self):
        if not self.lplayer:
            return
        unregister_event = self.lplayer.unregist_event
        unregister_event('E_MEOW_COIN_CHANGE', self._on_meow_coin_change)

    def _on_meow_coin_change(self):
        if not self.lplayer or not self.lplayer.is_valid():
            return
        self.bag_num, bag_size = self.lplayer.ev_g_meow_bag_info() or (0, 0)
        self.mail_box_num, self.mail_box_size, mail_box_times = self.lplayer.ev_g_meow_mail_box_info() or (0,
                                                                                                           0,
                                                                                                           0)
        self.panel.lab_tishi.SetString(get_text_by_id(18258).format(num=self.mail_box_num))
        self.panel.lab_frequency_num.SetString('%d/%d' % (meow_capacity_config.meow_mail_max_times - mail_box_times, meow_capacity_config.meow_mail_max_times))
        total_num = max(min(self.mail_box_size, self.bag_num), 1)
        if self.item_total_num != total_num and self.item_num_btn_widget:
            self.item_total_num = total_num
            self.item_num_btn_widget.init_item({'quantity': total_num}, self.set_total_num, max_callback=self.max_callback)
        if self.lplayer:
            is_enable = self.bag_num > 0
            is_enable = is_enable and not self.lplayer.ev_g_have_sent_mail(self.mail_entity_id)
            is_enable = is_enable and self.lplayer.ev_g_mail_total_times() < meow_capacity_config.meow_mail_max_times
            is_enable = is_enable and self.lplayer.ev_g_week_limit_num() < get_item_max_count_weekly(ITEM_NO_MEOW_COIN)
            self.panel.btn_send.SetShowEnable(is_enable)

    def max_callback(self, max_num):
        self.panel.PlayAnimation('max')

    def set_total_num(self, *args):
        _, num = args
        self.panel.lab_max.SetColor('#SR' if num >= self.mail_box_size else '#SK')
        self.panel.lab_max.SetString(get_text_by_id(18257).format(n='%d/%d' % (num, self.mail_box_size)))
        self.panel.nd_control.lab_num.SetString(str(num))
        self.send_num = min(self.bag_num, num)

    def on_close(self, btn, touch):
        self.close()

    def on_send_coin(self, btn, touch):
        if not self.mail_entity_id:
            return
        if not self.lplayer or not self.lplayer.is_valid():
            return
        if self.send_num <= 0:
            global_data.game_mgr.show_tip(get_text_by_id(18278))
            return
        self.lplayer.send_event('E_TRY_MAIL_MEOW_COIN', self.mail_entity_id, self.send_num)

    def start_check_pos_player(self):
        self.panel.runAction(cc.RepeatForever.create(cc.Sequence.create([
         cc.CallFunc.create(self.check_pos),
         cc.DelayTime.create(1)])))

    def check_pos(self):
        if self.mail_entity_id:
            mail_ent = EntityManager.getentity(self.mail_entity_id)
            if mail_ent and mail_ent.logic and global_data.player and global_data.player.logic:
                pos = global_data.player.logic.ev_g_position()
                if pos:
                    is_enter, _ = mail_ent.logic.ev_g_check_enter_consoloe_zone(pos)
                    if is_enter:
                        return
        self.close()