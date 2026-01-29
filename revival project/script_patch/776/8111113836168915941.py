# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Death/ADCrystalRogueChooseBtnUI.py
from __future__ import absolute_import
import six_ex
from common.const.uiconst import BASE_LAYER_ZORDER, UI_VKB_NO_EFFECT
from common.uisys.basepanel import BasePanel
from logic.gcommon.common_const import battle_const
from logic.gutils import pc_utils
import math3d
import time
from common.const import uiconst

class ADCrystalRogueChooseBtnUI(BasePanel):
    ENABLE_PIC = [
     'gui/ui_res_2/battle_tdm/rogue/btn_battle_tdm_rogue_0.png',
     'gui/ui_res_2/battle_tdm/rogue/btn_battle_tdm_rogue_2.png',
     'gui/ui_res_2/battle_tdm/rogue/btn_battle_tdm_rogue_3.png']
    DISABLE_PIC = [
     'gui/ui_res_2/battle_tdm/rogue/btn_battle_tdm_rogue_3.png',
     'gui/ui_res_2/battle_tdm/rogue/btn_battle_tdm_rogue_3.png',
     'gui/ui_res_2/battle_tdm/rogue/btn_battle_tdm_rogue_3.png']
    PANEL_CONFIG_NAME = 'battle_tdm/tdm_fight_rogue'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_rogue.OnClick': '_on_click_btn'
       }
    HOT_KEY_FUNC_MAP = {'choose_death_rogue.DOWN_UP': '_on_click_btn'
       }
    HOT_KEY_FUNC_MAP_SHOW = {'choose_death_rogue': {'node': 'btn_rogue.temp_pc'}}

    def on_init_panel(self):
        self._first_in_base = True
        self.enable_choose = False
        self.init_event()
        self.init_custom_com()
        self._on_rogue_gift_update()
        self._check_if_enable()

    def init_custom_com(self):
        from logic.comsys.setting_ui.CustomUIProxy import init_custom_com
        init_custom_com(self, {})

    def init_event(self):
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'rogue_gift_update_candidates': self._on_rogue_gift_update,
           'rogue_gift_enable_out_base_choose': self._check_if_enable,
           'rogue_gift_update_select': self._on_rogue_gift_select,
           'rogue_gift_local_choose': self._on_local_choose,
           'death_in_base_part_change': self._on_base_change,
           'death_first_check_in_base': self._on_first_check,
           'player_revive_land': self._on_player_revive_land
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def _on_player_revive_land(self, id):
        if id != global_data.player.id:
            return
        self.check_revive_show()

    def _on_local_choose(self):
        res = self._count_unselected_count()
        if res >= 2:
            self.show()
        else:
            self.hide()

    def _count_unselected_count(self):
        player = global_data.cam_lplayer
        if not player or not player.id:
            return 0
        player_id = player.id
        total_rogue_gift_candidates = global_data.death_battle_data.rogue_gift_candidates.get(player_id, {})
        total_selected_rogue_gifts = global_data.death_battle_data.selected_rogue_gifts.get(player_id, {})
        time_idxs = six_ex.keys(total_rogue_gift_candidates)
        selected_idxs = six_ex.keys(total_selected_rogue_gifts)
        return len(time_idxs) - len(selected_idxs)

    def _on_rogue_gift_update(self, *args):
        player = global_data.cam_lplayer
        if not player or not player.id:
            return 0
        player_id = player.id
        total_rogue_gift_candidates = global_data.death_battle_data.rogue_gift_candidates.get(player_id, {})
        total_selected_rogue_gifts = global_data.death_battle_data.selected_rogue_gifts.get(player_id, {})
        in_base = global_data.death_battle_data.get_is_in_base_part()
        if in_base and len(total_rogue_gift_candidates) == 1 and len(total_selected_rogue_gifts) == 0:
            global_data.ui_mgr.show_ui('DeathRogueChooseUI', 'logic.comsys.battle.Death')
        self._check_if_show()

    def _on_rogue_gift_select(self, eid, rogue_key):
        self._check_if_show()
        player = global_data.cam_lplayer
        if not player or not player.id:
            return
        if eid == player.id:
            cnt = self._count_unselected_count()
            if cnt > 0:
                global_data.ui_mgr.show_ui('DeathRogueChooseUI', 'logic.comsys.battle.Death')

    def on_finalize_panel(self):
        self.destroy_widget('custom_ui_com')
        self.process_event(False)

    def _on_click_btn(self, *args):
        if not self.enable_choose:
            msg = {'i_type': battle_const.TDM_CHOOSE_ROGUE_NOT_IN_BASE}
            global_data.emgr.show_battle_main_message.emit(msg, battle_const.MAIN_NODE_COMMON_INFO)
            return
        cnt = self._count_unselected_count()
        if cnt:
            global_data.ui_mgr.show_ui('DeathRogueChooseUI', 'logic.comsys.battle.Death')

    def _on_first_check(self):
        self._check_if_enable()

    def check_revive_show(self):
        res = self._count_unselected_count()
        in_base = global_data.death_battle_data.on_check_base()
        if res > 0 and in_base:
            global_data.ui_mgr.show_ui('DeathRogueChooseUI', 'logic.comsys.battle.Death')

    def _on_base_change(self):
        self._check_if_enable()
        if self._first_in_base:
            player_id = global_data.cam_lplayer.id
            total_rogue_gift_candidates = global_data.death_battle_data.rogue_gift_candidates.get(player_id, {})
            total_selected_rogue_gifts = global_data.death_battle_data.selected_rogue_gifts.get(player_id, {})
            in_base = global_data.death_battle_data.get_is_in_base_part()
            if len(six_ex.keys(total_rogue_gift_candidates)) == 1 and len(total_selected_rogue_gifts) == 0 and in_base:
                global_data.ui_mgr.show_ui('DeathRogueChooseUI', 'logic.comsys.battle.Death')
        self._first_in_base = False

    def _check_if_show(self):
        player = global_data.cam_lplayer
        if not player or not player.id or player.id != global_data.player.id:
            self.close()
            return
        res = self._count_unselected_count()
        if res > 0:
            self.show()
        else:
            self.hide()

    def _check_if_enable(self):
        is_enable = False
        if global_data.death_battle_data:
            is_enable = global_data.death_battle_data.get_is_in_base_part() or global_data.death_battle_data.enable_out_base_rogue
        if not is_enable:
            self.show_btn(False)
            global_data.ui_mgr.close_ui('DeathRogueChooseUI')
        else:
            self.show_btn(True)

    def show_btn(self, flag):
        if flag:
            self.enable_choose = True
            self.panel.PlayAnimation('tips')
            self.panel.btn_rogue.SetFrames('', self.ENABLE_PIC)
        else:
            self.enable_choose = False
            self.panel.btn_rogue.SetFrames('', self.DISABLE_PIC)