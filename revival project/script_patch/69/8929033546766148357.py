# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Magic/MagicRuneConfUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_2, BASE_LAYER_ZORDER
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import granbelm_utils
from logic.gcommon.item.item_const import ITEM_NO_MAGIC_COIN
from logic.gcommon.common_const.battle_const import MAGIC_MONSTER_TIP, MAGIC_ACHIEVE, MAIN_NODE_COMMON_INFO
from common.const import uiconst
HUNTER_BADGE_DESC = 17866
MAX_EXCHANGE_TIMES = 3
ICON_PATH = ('gui/ui_res_2/battle_hunter/icon_battle_hunter_fight_green.png', 'gui/ui_res_2/battle_hunter/icon_battle_hunter_fight_blue.png',
             'gui/ui_res_2/battle_hunter/icon_battle_hunter_fight_purple.png')
LIGHT_PATH = ('gui/ui_res_2/fight_end/img_center_light_green.png', 'gui/ui_res_2/fight_end/img_center_light_blue.png',
              'gui/ui_res_2/fight_end/img_center_light.png')
PROG_PATH = ('gui/ui_res_2/battle_hunter/prog_battle_hunter_fight_green.png', 'gui/ui_res_2/battle_hunter/prog_battle_hunter_fight_blue.png',
             'gui/ui_res_2/battle_hunter/prog_battle_hunter_fight_purple.png')

class MagicRuneConfUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_hunter/battle_hunter_choose_button'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {'btn_talent.OnClick': '_on_click_conf'
       }
    HOT_KEY_FUNC_MAP = {'toggle_moon_rune_list.DOWN': 'keyboard_toggle_magic_rune_list'
       }
    HOT_KEY_FUNC_MAP_SHOW = {'toggle_moon_rune_list': {'node': 'btn_talent.temp_pc'}}

    def on_init_panel(self, *args, **kwargs):
        super(MagicRuneConfUI, self).on_init_panel()
        self.init_params()
        self.process_events(True)
        self.init_custom_com()
        self.panel.nd_desc.setVisible(False)
        self.panel.nd_desc.temp_talent_desc.SetString(HUNTER_BADGE_DESC)
        self.update_all()
        self.panel.RecordAnimationNodeState('loop')
        self.panel.lab_activate.setVisible(False)
        self.panel.img_gear2.setVisible(False)
        self.panel.img_gear3.setVisible(False)

    def init_custom_com(self):
        from logic.comsys.setting_ui.CustomUIProxy import init_custom_com
        init_custom_com(self, {})

    def init_params(self):
        self.hunter_badge_get = False
        self.hunter_coin_cnt = 0
        self.per_magic_item_cost = None
        if global_data.cam_lplayer:
            self.hunter_badge_get = bool(global_data.cam_lplayer.ev_g_exchanged_magic())
            self.hunter_coin_cnt, self.per_magic_item_cost = global_data.cam_lplayer.ev_g_magic_coin_cnt()
        self.full_anim_played = False
        self.first_get_tip_showed = False
        return

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'scene_camera_player_setted_event': self.update_all,
           'update_hunter_coin_count': self.update_all,
           'on_magic_exchange_times_change': self.update_all
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def update_all(self, *args):
        if not global_data.cam_lplayer:
            return
        exchanged_times = global_data.cam_lplayer.ev_g_magic_exchange_times()
        show = exchanged_times < MAX_EXCHANGE_TIMES
        self.panel.btn_talent.setVisible(show)
        if not show:
            return
        coin_cnt, self.per_magic_item_cost = global_data.cam_lplayer.ev_g_magic_coin_cnt()
        coin_cnt, self.hunter_coin_cnt = self.hunter_coin_cnt, coin_cnt
        if coin_cnt < self.hunter_coin_cnt:
            self.panel.PlayAnimation('get')
            global_data.emgr.show_battle_main_message.emit({'i_type': MAGIC_MONSTER_TIP,
               'content_txt': get_text_by_id(17571, (str(self.hunter_coin_cnt - coin_cnt),)),
               'icon_path': 'gui/ui_res_2/battle_hunter/icon_battle_hunter_tips_monster_1.png'
               }, MAIN_NODE_COMMON_INFO)
            if coin_cnt == 0:
                self.show_first_get_coin_tip()
        unuse_cnt = self.hunter_coin_cnt - self.per_magic_item_cost * exchanged_times
        prog = unuse_cnt if unuse_cnt < self.per_magic_item_cost else self.per_magic_item_cost
        self.panel.prog_gear.SetPercent(prog * 100.0 / self.per_magic_item_cost)
        change_color = unuse_cnt > self.per_magic_item_cost
        self.panel.lab_num.SetString('{}{}{}/{}'.format('<color=0XFF0000FF>' if change_color else '', str(unuse_cnt), '</color>' if change_color else '', str(self.per_magic_item_cost)))
        can_exchange_times = unuse_cnt / self.per_magic_item_cost
        self.panel.img_gear.setVisible(True)
        self.panel.img_gear.SetDisplayFrameByPath('', ICON_PATH[exchanged_times])
        self.panel.img_gear_vx.SetDisplayFrameByPath('', ICON_PATH[exchanged_times])
        self.panel.prog_gear.SetPath('', PROG_PATH[exchanged_times])
        self.panel.vx_light.SetDisplayFrameByPath('', LIGHT_PATH[exchanged_times])
        should_play = unuse_cnt >= self.per_magic_item_cost
        if should_play and not self.full_anim_played:
            self.panel.PlayAnimation('full')
            self.show_coin_full_tip()
            self.full_anim_played = True
        playing = self.panel.IsPlayingAnimation('loop')
        if should_play and not playing:
            self.panel.PlayAnimation('loop')
        elif not should_play and playing:
            self.panel.StopAnimation('loop')
            self.panel.RecoverAnimationNodeState('loop')

    def _on_click_conf(self, *args):
        if not global_data.cam_lplayer or not global_data.cam_lplayer.ev_g_is_avatar():
            return
        if self.hunter_badge_get:

            @self.panel.nd_desc.temp_talent_desc.nd_bg.unique_callback()
            def OnBegin(_layer, _touch, *args):
                self.panel.nd_desc.setVisible(False)

            self.panel.nd_desc.setVisible(True)
        else:
            global_data.ui_mgr.show_ui('MagicRuneListUI', 'logic.comsys.battle.Magic')

    def keyboard_toggle_magic_rune_list(self, msg, keycode):
        if global_data.ui_mgr.get_ui('MagicRuneListUI'):
            global_data.ui_mgr.close_ui('MagicRuneListUI')
        else:
            self._on_click_conf()

    def on_finalize_panel(self):
        self.process_events(False)
        self.destroy_widget('custom_ui_com')
        super(MagicRuneConfUI, self).on_finalize_panel()

    def show_first_get_coin_tip(self):
        global_data.emgr.show_human_tips.emit(get_text_by_id(17873), 3)

    def show_coin_full_tip(self):
        global_data.emgr.show_human_tips.emit(get_text_by_id(17868), 3)