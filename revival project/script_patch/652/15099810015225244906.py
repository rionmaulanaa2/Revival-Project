# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Death/DeathPlayBackUI.py
from __future__ import absolute_import
import six_ex
from common.const.uiconst import BASE_LAYER_ZORDER, TOP_ZORDER
from common.uisys.basepanel import BasePanel
from logic.gutils import role_head_utils
from common.cfg import confmgr
from logic.gutils import item_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
import math3d
from common.const.uiconst import UI_TYPE_MESSAGE
from logic.comsys.battle.BattleInfoUI import BattleInfoUI
EXCEPT_HIDE_UI_LIST = [
 'DeathBeginCountDown', 'SurviveInfoUI', 'BattleInfoMessageVisibleUI']
HARM_TYPE_NORMAL_WEAPON = 1
HARM_TYPE_SPECIAL_HARM = 3
HARM_TYPE_UNHUMAN = 4
HARM_TYPE_OTHER = 5
HARM_TYPE_UNKNOWN = 6

class TDMEndDeathReplayWidget(object):

    def __init__(self, panel, data=None):
        self.panel = panel
        self.panel.temp_tier.setVisible(False)
        self.parse_death_detail_info(data)

    def on_finalize_panel(self):
        pass

    def parse_death_detail_info(self, replay_data):
        if not replay_data:
            return
        killer_info = replay_data.get('killer_info', {})
        killer_hit = replay_data.get('killer_hit', [])
        self.setup_player_cause_harm(killer_info, killer_hit)

    def setup_player_cause_harm(self, player_info, harm_source_list):
        mecha_id = player_info.get('mecha_id')
        if player_info and player_info.get('eid'):
            if mecha_id and global_data.cam_lplayer and global_data.cam_lplayer.ev_g_is_pure_mecha():
                self.setup_player_mecha_info(self.panel.bar_calculate, mecha_id)
            else:
                self.setup_player_person_info(self.panel.bar_calculate, player_info)
            role_name = player_info.get('role_name', '\xe6\x9c\xaa\xe7\x9f\xa5')
            self.setup_player_harm_info(harm_source_list, role_name)
        else:
            destroyed_mecha_id = player_info.get('destroyed_mecha_id')
            if destroyed_mecha_id and global_data.cam_lplayer and global_data.cam_lplayer.ev_g_is_pure_mecha():
                self.setup_player_mecha_info(self.panel.bar_calculate, destroyed_mecha_id)
                self.panel.lab_details.SetString(get_text_by_id(18232))
            else:
                from logic.client.const.game_mode_const import GAME_MODE_GOOSE_BEAR
                if global_data.game_mode.is_mode_type(GAME_MODE_GOOSE_BEAR):
                    player = global_data.cam_lplayer
                    if player:
                        cur_mecha_id = player.ev_g_get_bind_mecha_type()
                        self.setup_player_mecha_info(self.panel.bar_calculate, cur_mecha_id)
                        self.panel.lab_details.SetString(get_text_by_id(17155).format(player.ev_g_char_name()))
                else:
                    log_error('Should not have harm from non-player source!', player_info, harm_source_list)

    def setup_player_mecha_info(self, nd, mecha_id):
        icon_path = role_head_utils.get_head_photo_res_path(int('3021%d' % mecha_id))
        nd.temp_head.img_head.SetDisplayFrameByPath('', icon_path)

    def setup_player_person_info(self, nd, player_info):
        head_frame = player_info.get('head_frame')
        head_photo = player_info.get('head_photo')
        role_season_level = player_info.get('season_level', None)
        role_head_utils.init_role_head(nd.temp_head, head_frame, head_photo)
        return

    def preprocess_harm_source_list(self, harm_source_list, has_player):
        from logic.gcommon.item.item_utility import is_weapon
        from logic.gutils.new_template_utils import is_mecha_related_item
        res_list = []
        for ent_type, item_id, damage in harm_source_list:
            if 8000 <= item_id <= 8100:
                weapon_type = 8000
            else:
                weapon_type = confmgr.get('hit_hint', str(item_id), default={}).get('iWeaponType', '')
            if has_player:
                if weapon_type:
                    if is_weapon(weapon_type) and not is_mecha_related_item(weapon_type):
                        harm_type = HARM_TYPE_NORMAL_WEAPON
                    else:
                        harm_type = HARM_TYPE_SPECIAL_HARM
                else:
                    harm_type = HARM_TYPE_UNKNOWN
            else:
                harm_type = HARM_TYPE_UNHUMAN
            res_list.append({'htype': harm_type,'damage': damage,'ent_type': ent_type,'item_id': weapon_type})

        return res_list

    def setup_player_harm_info(self, harm_source_list, player_name):
        harm_list = self.preprocess_harm_source_list(harm_source_list, player_name)
        last_hit_dict = {}
        if len(harm_list) > 0:
            last_hit_dict = harm_list[-1]
        harm_type = last_hit_dict.get('htype', HARM_TYPE_NORMAL_WEAPON)
        damage = last_hit_dict.get('damage', 0)
        ent_type = last_hit_dict.get('ent_type', None)
        weapon_type = last_hit_dict.get('item_id', None)
        if harm_type == HARM_TYPE_NORMAL_WEAPON:
            weapon_name = item_utils.get_item_name(weapon_type)
            msg = get_text_by_id(18554, {'name': player_name,'weapon_name': weapon_name})
        elif harm_type == HARM_TYPE_SPECIAL_HARM:
            conf = confmgr.get('hit_hint', str(weapon_type), default={})
            weapon_name = get_text_by_id(conf.get('cReplayName', ''))
            msg = get_text_by_id(18554, {'name': player_name,'weapon_name': weapon_name})
        else:
            weapon_name = ''
            msg = ''
        self.panel.lab_details.SetString(msg)
        return


from common.const import uiconst

class DeathPlayBackUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_tdm/fight_tdm_count'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {}
    HOT_KEY_FUNC_MAP = {'any_key_close': 'click_btn'
       }
    HOT_KEY_FUNC_MAP_SHOW = {'any_key_close': {'node': 'temp_button.temp_pc'}}

    def on_init_panel(self):
        self.init_parameters()
        self.init_event(True)
        self.init_panel()
        except_list = list(EXCEPT_HIDE_UI_LIST)
        except_list.extend([ i.__name__ for i in six_ex.values(BattleInfoUI.MAIN_NODE_MESSAGE) ])
        from logic.gutils import judge_utils
        if judge_utils.is_ob():
            except_list.append('ObserveUI')
            except_list.append('ObserveUIPC')
            except_list.append('FightKillNumberUI')
        self.hide_main_ui(exceptions=except_list)
        global_data.emgr.death_playback_ui_lifetime.emit(True)

    def on_finalize_panel(self):
        self.show_main_ui()
        self.init_event(False)
        global_data.emgr.death_playback_ui_lifetime.emit(False)

    def init_parameters(self):
        pass

    def init_panel(self):
        play_back_nd = global_data.uisystem.load_template_create('battle_tdm/tdm_calculate', self.panel.temp_panel, name='play_back_nd')
        play_back_nd.SetPosition('50%', '50%')
        self.play_back_widget = TDMEndDeathReplayWidget(play_back_nd)

        @self.panel.temp_button.btn_major.cb_with_ani(self.panel.temp_button)
        def OnClick(btn, touch):
            self.on_send_data()

        self.can_start_jump(not bool(global_data.ui_mgr.get_ui('DeathBeginCountDown')))
        if global_data.player and global_data.player.logic:
            is_in_spec = global_data.player.logic.ev_g_is_in_spectate()
            if is_in_spec:
                self.panel.temp_button.setVisible(False)

    def click_btn(self, msg, keycode):
        self.panel.temp_button.btn_major.OnClick(None)
        return

    def on_send_data(self):
        player = global_data.player
        if not player:
            return
        bat = player.get_battle() or player.get_joining_battle()
        from logic.client.const import game_mode_const
        if global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_SNATCHEGG,)):
            if player and player.logic and player.logic.ev_g_death():
                log_error('player has already dead!')
                return
        bat and bat.start_combat()

    def set_play_back_info(self, replay_data):
        self.play_back_widget.parse_death_detail_info(replay_data)

    def init_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'death_count_down_start': self.count_down_start,
           'death_count_down_over': self.count_down_over
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def count_down_start(self):
        self.can_start_jump(False)

    def count_down_over(self):
        self.can_start_jump(True)

    def can_start_jump(self, can):
        self.panel.temp_button.btn_major.SetEnable(can)

    def set_revive_time(self, revive_time):
        return
        if revive_time <= 0 and global_data.player and global_data.player.logic:
            from logic.gcommon import time_utility as t_util
            de_timestamp = global_data.player.logic.ev_g_defeated_timestamp()
            delay_time = de_timestamp - t_util.get_server_time()
            revive_time = delay_time
        cfg = global_data.game_mode.get_cfg_data('play_data')
        delay_time = revive_time + cfg.get('force_revive_time', 8)

        def revive_callback():
            self.on_send_data()

        if delay_time > 0:
            self.panel.SetTimeOut(delay_time, revive_callback)
        else:
            self.panel.SetTimeOut(0.03, revive_callback)