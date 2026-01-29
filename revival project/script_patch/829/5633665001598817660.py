# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/concert/ArenaEndUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_NO_EFFECT
from logic.gutils import role_head_utils
from mobile.common.EntityManager import EntityManager
from logic.gutils.template_utils import init_tempate_mall_i_item

class ArenaEndUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_arena/battle_arena_end'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_like.OnClick': 'on_btn_like_click'
       }
    MOUSE_CURSOR_TRIGGER_SHOW = True

    def on_init_panel(self, *args, **kwargs):
        self.init_parameters()
        self.init_panel()

    def on_finalize_panel(self):
        pass

    def init_parameters(self):
        self.opponent = None
        return

    def set_winner(self, winner, is_king, is_winner, reward_cnt):
        bat = global_data.player.get_battle() or global_data.player.get_joining_battle()
        if not bat:
            return
        if bat.is_duel_stage():
            if is_winner and reward_cnt > 0:
                self.panel.lab_win.SetString(609912)
            else:
                self.panel.lab_win.SetString(17289)
        else:
            self.duel_end()
        king, defier, _, _ = bat.get_battle_data()
        self.panel.PlayAnimation('end')
        ani_name = 'win' if is_winner else 'defeat'
        self.panel.PlayAnimation(ani_name)
        self.opponent = defier if is_king else king
        self.update_photo(self.panel.temp_player, self.opponent)
        play_data = global_data.game_mode.get_cfg_data('play_data')
        if play_data:
            duel_reward = play_data.get('duel_reward', [])
            winer_reward = duel_reward.get('winer', [])
            loser_reward = duel_reward.get('loser', [])
            show_reward = winer_reward if is_winner else loser_reward
            self.panel.list_price.SetInitCount(len(show_reward))
            for i, reward_info in enumerate(show_reward):
                item_id, num = reward_info
                item = self.panel.list_price.GetItem(i)
                init_tempate_mall_i_item(item, item_id, item_num=num)

            need_show_rewards = bool(show_reward) and reward_cnt > 0
            self.panel.list_price.setVisible(need_show_rewards)
            self.panel.nd_defeat.pnl_defeat.setVisible(need_show_rewards)
            self.panel.nd_defeat.bg_defeat.setVisible(need_show_rewards)
            self.panel.nd_defeat.img_title.setVisible(need_show_rewards)
            self.panel.nd_win.img_title.setVisible(need_show_rewards)

    def update_photo(self, ui_item, entity_id):
        if not entity_id:
            return
        player = EntityManager.getentity(entity_id)
        if not (player and player.logic):
            return
        char_name = player.logic.ev_g_char_name()
        head_frame = player.logic.ev_g_head_frame()
        head_photo = player.logic.ev_g_head_photo()
        role_head_utils.init_role_head(ui_item.temp_head, head_frame, head_photo)
        ui_item.lab_name.SetString(char_name)

    def init_panel(self):

        @self.panel.nd_touch_layer.callback()
        def OnClick(btn, touch):
            self.close()

    def on_btn_like_click(self, btn, touch):
        if not self.opponent:
            return
        player = EntityManager.getentity(self.opponent)
        if player and player.uid:
            global_data.player.do_global_spectate_like(player.uid)
        self.panel.btn_like.SetEnable(False)

    def duel_end(self):
        self.panel.lab_win.SetString(609913)