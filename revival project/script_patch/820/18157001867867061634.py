# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/DeathRogueGiftTopRightUI.py
from __future__ import absolute_import
from six.moves import range
from common.const.uiconst import UI_VKB_NO_EFFECT, LOW_MESSAGE_ZORDER
from common.uisys.basepanel import BasePanel
from logic.comsys.ui_distortor.MechaDistortHelper import MechaDistortHelper
from logic.client.const import game_mode_const
from logic.gutils import rogue_utils as r_u

class DeathRogueGiftTopRightBaseUI(MechaDistortHelper, BasePanel):
    DLG_ZORDER = LOW_MESSAGE_ZORDER
    UI_VKB_TYPE = UI_VKB_NO_EFFECT
    GLOBAL_EVENT = {'global_rogue_gifts_updated': '_on_global_rogue_gifts_updated',
       'global_rogue_gifts_clear': '_on_rogue_clear'
       }
    GLOBAL_EVENT.update(MechaDistortHelper.GLOBAL_EVENT)

    def on_init_panel(self):
        BasePanel.on_init_panel(self)
        MechaDistortHelper.on_init_panel(self)
        game_mode = global_data.game_mode
        self._is_death = True if game_mode and game_mode.is_mode_type(game_mode_const.GAME_MODE_DEATH) else False
        self._init_data()
        battle_data = global_data.death_battle_data
        self._init_view(len(battle_data.rogue_distribute_times or []))

    def on_finalize_panel(self):
        if self._tips_widget:
            self._tips_widget.destroy()
        self._tips_widget = None
        BasePanel.on_finalize_panel(self)
        return

    def _init_data(self):
        self._human_state_pos = self.panel.nd_rot.GetPosition()
        self._mecha_state_pos = self.panel.nd_rot_mecha.GetPosition()

    def switch_to_mecha(self):
        MechaDistortHelper.switch_to_mecha(self)
        self.panel.nd_rot.SetPosition(*self._mecha_state_pos)

    def switch_to_non_mecha(self):
        MechaDistortHelper.switch_to_non_mecha(self)
        self.panel.nd_rot.SetPosition(*self._human_state_pos)

    def _on_rogue_clear(self):
        self._refresh_list([])

    def on_resolution_changed(self):
        in_mecha = MechaDistortHelper.in_mecha_state(self)
        self.switch_to_mecha() if in_mecha else self.switch_to_non_mecha()

    def _init_view(self, cnt):
        self.panel.list_icon.SetInitCount(cnt)
        self._view_list = []
        for i in range(cnt):
            self._view_list.append(self.panel.list_icon.GetItem(i))

        from logic.comsys.battle.DeathRogueGiftDetailWidget import DeathRogueGiftDetailWidget
        self._tips_widget = DeathRogueGiftDetailWidget(self, self.panel)
        self._tips_widget.hide()
        if global_data.player and global_data.player.logic:
            player = global_data.player.logic.ev_g_spectate_target()
            if not player:
                player = global_data.player.logic
        else:
            player = None
        self._refresh_list(r_u.get_lplayer_gifts(player))
        return

    def _refresh_list(self, gift_ids):
        cnt = self._get_list_cnt()
        data_cnt = len(gift_ids) if gift_ids else 0
        for i in range(cnt):
            if i < data_cnt:
                gift_id = gift_ids[i]
            else:
                gift_id = -1
            item = self._get_list_item(i)
            if gift_id == -1:
                item.SetEnable(False)
                continue
            item.SetEnable(True)
            icon_path = r_u.get_gift_icon(gift_id)
            item.SetFrames('', [icon_path, icon_path, r_u.get_gift_gray_icon()])

            @item.unique_callback()
            def OnBegin(btn, touch, gift_id=gift_id):
                wpos = touch.getLocation()
                self._show_tips(gift_id, wpos)
                return True

            @item.unique_callback()
            def OnEnd(btn, touch):
                self._hide_tips()

    def _get_list_item(self, idx):
        cnt = self._get_list_cnt()
        if idx >= 0 and idx < cnt:
            return self._view_list[idx].btn_rogue
        else:
            return None
            return None

    def _get_list_cnt(self):
        return len(self._view_list)

    def _show_tips(self, gift_id, click_wpos):
        if not self._tips_widget:
            return
        self._tips_widget.refresh_view(gift_id)
        pos_node = self._tips_widget.panel
        OFFSET_X = -160
        OFFSET_Y = -100
        lpos = pos_node.getParent().convertToNodeSpace(click_wpos)
        pos_node.SetPosition(lpos.x + OFFSET_X, lpos.y + OFFSET_Y)
        self._tips_widget.show()

    def _hide_tips(self):
        if not self._tips_widget:
            return
        self._tips_widget.hide()

    def _on_global_rogue_gifts_updated(self, unit_id, gift_ids):
        if not r_u.is_avatar_unit_id(unit_id) and not r_u.is_observed_unit_id(unit_id):
            return
        self._refresh_list(gift_ids)

    def on_observed_player_setted(self, ltarget):
        MechaDistortHelper.on_observed_player_setted(self, ltarget)
        self._refresh_list(r_u.get_lplayer_gifts(ltarget))


class DeathRogueGiftTopRightUI(DeathRogueGiftTopRightBaseUI):
    PANEL_CONFIG_NAME = 'battle_tdm/battle_rogue_right_top'