# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/ZombieFFA/ZombieFFAChooseMechaUI.py
from __future__ import absolute_import
import six
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_CUSTOM
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import dress_utils
from logic.gutils import mecha_skin_utils
from common.cfg import confmgr
from logic.gcommon import time_utility as tutil
from logic.gcommon.item import item_const as iconst
from logic.gutils import item_utils
from logic.comsys.battle.ffa.FFAChooseMechaInfoWidget import FFAChooseMechaInfoWidget
from logic.comsys.battle.ZombieFFA.ZombieFFAPriceUIWidget import ZombieFFAPriceUIWidget
from logic.vscene.parts.gamemode.CGameModeManager import CGameModeManager
import cc
from logic.gutils import item_utils
TRK_ACTION_TAG = 16383
OWN_HANDLER = {iconst.ITEM_NO_GOLD: lambda player: player.get_gold(),
   iconst.ITEM_NO_DIAMOND: lambda player: player.get_diamond(),
   iconst.ITEM_NO_YUANBAO: lambda player: player.get_yuanbao()
   }

class ZombieFFAChooseMechaUI(BasePanel):
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CUSTOM
    PANEL_CONFIG_NAME = 'battle_ffa3/ffa3_choose_mech'
    UI_ACTION_EVENT = {'nd_touch.OnDrag': 'on_drag_model',
       'btn_skill.OnBegin': 'on_click_skill_begin',
       'btn_skill.OnEnd': 'on_click_skill_end',
       'btn_sure.OnClick': 'on_click_confirm',
       'btn_change_mecha.OnClick': 'request_change_mecha'
       }
    GLOBAL_EVENT = {'zombieffa_on_player_confirmed': 'refresh_confirmed_info',
       'zombieffa_on_player_mecha_change': 'refresh_mecha_usage',
       'zombieffa_change_mecha_result': 'refresh_mecha_result',
       'zombieffa_choose_mecha_finish': 'choose_mecha_finish'
       }

    def ui_vkb_custom_func(self):
        return True

    def on_init_panel(self, *args, **kwargs):
        self.init_parameters()
        self.hide()
        global_data.ui_mgr.add_ui_show_whitelist(['ZombieFFAChooseMechaUI', 'NoticeUI', 'BattleReconnectUI', 'CloneMechaSkillDetail'], 'ZombieFFAChooseMecha')

    def init_parameters(self):
        battle = global_data.battle
        if not battle:
            return
        else:
            self.player = global_data.cam_lplayer
            self.skill_info_widget = None
            self.eid_2_enemy_widget = {}
            self.player_names = battle.choose_mecha_player_names
            play_data = CGameModeManager().get_cfg_data_by_map_id(battle.map_id, 'play_data')
            self.refresh_mecha_cost = play_data.get('refresh_mecha_cost_item_num', [])
            self.refresh_mecha_cost_item_no = play_data.get('refresh_mecha_cost_item_id', 50101002)
            self.price_widget = ZombieFFAPriceUIWidget(self, self.panel.list_money)
            self.refresh_mecha_free_times = 0
            if self.refresh_mecha_cost:
                cfg = self.refresh_mecha_cost[0]
                if cfg.get('cost') == 0:
                    self.refresh_mecha_free_times = cfg.get('to', 0) - cfg.get('from', 0) + 1
            return

    def on_finalize_panel(self):
        self.price_widget and self.price_widget.on_finalize_panel()
        global_data.ui_mgr.remove_ui_show_whitelist('ZombieFFAChooseMecha')

    def enter_choose_mecha(self):
        self.panel.nd_player_frame.lab_name_mine.SetString(global_data.player.get_name())
        self.init_map_info_widget()
        self.init_mecha_usage()
        self.init_countdown_widget()
        self.init_refresh_widget()
        self.refresh_confirmed_info()
        self.show()
        global_data.sound_mgr.play_music('clone_standby')
        global_data.sound_mgr.play_ui_sound('ui_gvg_mecha_select')
        global_data.sound_mgr.play_sound_2d('Play_ui_notice', ('ui_notice', 'medal_flight'))
        self.panel.PlayAnimation('show')
        self.panel.PlayAnimation('keep')
        self.panel.RecordAnimationNodeState('loop')
        self.panel.PlayAnimation('loop')
        if not self.is_confirmed():
            self.panel.PlayAnimation('yes')

    def init_mecha_usage(self):
        battle = global_data.battle
        if not battle:
            return
        player_cnt = len(battle.choose_mecha_player_names)
        if player_cnt > 1:
            self.panel.enemy_list.SetInitCount(player_cnt - 1)
        idx = 0
        for eid, mecha_id in six.iteritems(battle.mecha_usage_dict):
            if eid == global_data.player.id:
                self.switch_mecha(mecha_id)
                continue
            widget = self.panel.enemy_list.GetItem(idx)
            idx += 1
            self.eid_2_enemy_widget[eid] = widget
            widget.lab_name.SetString(self.player_names[eid])
            widget.img_mecha.SetDisplayFrameByPath('', self.get_mecha_pic_path(mecha_id))
            if eid in battle.confirmed_player_list:
                widget.img_lock.setVisible(True)

    def init_map_info_widget(self):
        battle = global_data.battle
        if not battle:
            return
        map_name_text_ids = confmgr.get('map_config', str(battle.map_id), 'cMapNameTextIds', default={})
        text_id_index = 0
        prefix_str = ''
        if len(map_name_text_ids) > 1 and battle and hasattr(battle, 'area_id'):
            text_id_index = min(int(battle.area_id), len(map_name_text_ids)) - 1
            prefix_str = '\xe2\x80\x94'
        self.panel.lab_map_name.setVisible(bool(prefix_str))
        map_text = ''.join([prefix_str, get_text_by_id(map_name_text_ids[text_id_index])])
        self.panel.lab_map_name.SetString(map_text)

    def init_countdown_widget(self):
        battle = global_data.battle
        if not battle or not battle.choose_mecha_end_ts:
            return
        total_time = battle.choose_mecha_end_ts - tutil.get_server_time_battle()
        self.start_countdown(total_time)

    def init_refresh_widget(self):
        battle = global_data.battle
        if not battle:
            return
        cost_item_pic = item_utils.get_money_icon(self.refresh_mecha_cost_item_no)
        self.panel.img_icon.SetDisplayFrameByPath('', cost_item_pic)
        self.refresh_cost_widget()

    def refresh_cost_widget(self):
        left_free_count = self.get_left_free_refresh_mecha_time()
        next_cost = 0
        if left_free_count > 0:
            self.panel.nd_money.setVisible(False)
            self.panel.nd_free.setVisible(True)
            self.panel.nd_free.lab_free.SetString(19787, args={'n': left_free_count})
        else:
            self.panel.nd_free.setVisible(False)
            self.panel.nd_money.setVisible(True)
            next_cost = self.get_refresh_mecha_cost()
            self.panel.lab_money.SetString(str(next_cost))
        player = global_data.player
        battle = global_data.battle
        if player and battle:
            own_num = OWN_HANDLER[self.refresh_mecha_cost_item_no](player)
            left_num = own_num - battle.refresh_mecha_cost
            money_info = {'count': left_num}
            self.price_widget.update_money_info({self.refresh_mecha_cost_item_no: money_info})

    def request_change_mecha(self, *args):
        battle = global_data.battle
        if not battle:
            return
        if self.is_confirmed():
            return
        next_cost = self.get_refresh_mecha_cost()
        own_num = OWN_HANDLER[self.refresh_mecha_cost_item_no](global_data.player)
        left_num = own_num - battle.refresh_mecha_cost
        if left_num < next_cost:
            global_data.game_mgr.show_tip(19788)
            return
        battle.request_change_mecha()

    def on_drag_model(self, btn, touch):
        from logic.client.const import lobby_model_display_const
        delta_pos = touch.getDelta()
        global_data.emgr.rotate_model_display.emit(-delta_pos.x / lobby_model_display_const.ROTATE_FACTOR)

    def on_click_confirm(self, *args):
        if global_data.battle:
            global_data.battle.confirm_mecha_usage()

    def on_click_skill_begin(self, *args):
        battle = global_data.battle
        if not battle:
            return
        mecha_id = battle.mecha_usage_dict.get(global_data.player.id)
        ui = global_data.ui_mgr.show_ui('CloneMechaSkillDetail', 'logic.comsys.battle.Clone')
        ui.refresh_ui(mecha_id)
        ui.PlayAnimation('appear')
        self.panel.img_shadow.setVisible(True)
        return True

    def on_click_skill_end(self, *args):
        global_data.ui_mgr.close_ui('CloneMechaSkillDetail')
        self.panel.img_shadow.setVisible(False)
        return True

    def refresh_mecha_result(self, success, mecha_id):
        battle = global_data.battle
        if not battle:
            return
        if not success:
            return
        self.switch_mecha(mecha_id)
        self.panel.StopAnimation('loop')
        self.panel.RecoverAnimationNodeState('loop')
        self.panel.stopActionByTag(TRK_ACTION_TAG)
        action_seq = [
         cc.CallFunc.create(lambda : self.panel.btn_change_mecha.SetEnable(False)),
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('switch')),
         cc.DelayTime.create(self.panel.GetAnimationMaxRunTime('switch') / 2),
         cc.CallFunc.create(self.refresh_cost_widget),
         cc.DelayTime.create(self.panel.GetAnimationMaxRunTime('switch') / 2),
         cc.CallFunc.create(lambda : self.panel.btn_change_mecha.SetEnable(True))]
        own_num = OWN_HANDLER[self.refresh_mecha_cost_item_no](global_data.player)
        left_num = own_num - battle.refresh_mecha_cost
        if left_num > 0:
            action_seq.extend([
             cc.DelayTime.create(self.panel.GetAnimationMaxRunTime('switch') / 2),
             cc.CallFunc.create(lambda : self.panel.PlayAnimation('loop'))])
        action = self.panel.runAction(cc.Sequence.create(action_seq))
        action.setTag(TRK_ACTION_TAG)

    def refresh_mecha_usage(self, eid, mecha_id):
        if eid == global_data.player.id:
            return
        widget = self.eid_2_enemy_widget[eid]
        widget.lab_name.SetString(self.player_names[eid])
        widget.img_mecha.SetDisplayFrameByPath('', self.get_mecha_pic_path(mecha_id))

    def refresh_confirmed_info(self, eid=None):
        battle = global_data.battle
        if not battle:
            pass
        confirm_cnt = len(battle.confirmed_player_list)
        all_cnt = len(battle.choose_mecha_player_names)
        progress_str = '{}/{}'.format(confirm_cnt, all_cnt)
        self.panel.lab_nub.SetString(progress_str)
        self.panel.PlayAnimation('player')
        widget = self.eid_2_enemy_widget.get(eid)
        if widget:
            widget.img_lock.setVisible(True)
        elif eid == global_data.player.id:
            self.on_confirm_choose()

    def choose_mecha_finish(self):
        battle = global_data.battle
        if not battle or not battle.choose_mecha_finish:
            return
        self.panel.runAction(cc.Sequence.create([
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('out')),
         cc.DelayTime.create(self.panel.GetAnimationMaxRunTime('out')),
         cc.CallFunc.create(lambda : global_data.emgr.change_model_display_scene_item.emit(None))]))

    def on_confirm_choose(self, *args):
        self.panel.btn_sure.SetEnable(False)
        self.panel.btn_sure.SetText('')
        self.panel.runAction(cc.Sequence.create([
         cc.CallFunc.create(lambda : self.panel.StopAnimation('yes')),
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('tap')),
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('change')),
         cc.DelayTime.create(self.panel.GetAnimationMaxRunTime('tap')),
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('wait')),
         cc.CallFunc.create(lambda : self.panel.nd_wait.setVisible(True)),
         cc.CallFunc.create(lambda : self.panel.btn_change_mecha.setVisible(False))]))
        self.panel.lab_prompt.SetString(18235)
        self.panel.nd_await.setVisible(False)
        self.panel.nd_ready.setVisible(True)

    def get_left_free_refresh_mecha_time(self):
        battle = global_data.battle
        if not battle:
            return 0
        return max(0, self.refresh_mecha_free_times - battle.refresh_mecha_times)

    def get_refresh_mecha_cost(self):
        battle = global_data.battle
        if not battle:
            return 0
        else:
            next_time = battle.refresh_mecha_times + 1
            for cost in self.refresh_mecha_cost:
                num = cost.get('cost')
                if cost.get('from', 0) > next_time:
                    continue
                if cost.get('to') is None or cost.get('to', 0) >= next_time:
                    return num

            return 0

    def set_mecha_info(self, mecha_id):
        if not self.skill_info_widget:
            self.skill_info_widget = FFAChooseMechaInfoWidget(self, self.panel.nd_ability, mecha_id)
        else:
            self.skill_info_widget.on_switch_to_mecha_type(mecha_id)
        mecha_name = item_utils.get_mecha_name_by_id(mecha_id)
        self.panel.nd_name.lab_name1.SetString(mecha_name)
        self.panel.nd_name.lab_name2.SetString(mecha_name)
        self.panel.nd_name.lab_name3.SetString(mecha_name)

    def get_usage_mecha_id(self, eid):
        battle = global_data.battle
        if not battle:
            return
        return battle.mecha_usage_dict[eid]

    def start_countdown(self, total_time):

        def update_count_down(pass_time):
            left_time = int(total_time - int(pass_time))
            self.panel.lab_time.SetString('%.2ds' % left_time)
            if left_time <= 10:
                self.panel.PlayAnimation('alarm')
                self.panel.lab_time.SetColor(16721472)

        def update_count_down_finish():
            self.panel.lab_time.SetString('00s')

        self.panel.StopTimerAction()
        if total_time < 0:
            update_count_down_finish()
            return
        update_count_down(pass_time=0)
        self.panel.TimerAction(update_count_down, total_time, callback=update_count_down_finish, interval=1)

    def is_confirmed(self):
        battle = global_data.battle
        player = global_data.player
        if battle and player:
            return player.id in battle.confirmed_player_list
        return False

    def get_mecha_pic_path(self, mecha_id):
        mecha_base_skin = mecha_skin_utils.get_original_skin_lst(mecha_id)[0]
        return 'gui/ui_res_2/item/mecha_skin/%s.png' % mecha_base_skin

    def switch_mecha(self, mecha_id):
        from logic.client.const import lobby_model_display_const
        from logic.gutils import lobby_model_display_utils
        self.set_mecha_info(mecha_id)
        image_path = self.get_mecha_pic_path(mecha_id)
        self.panel.nd_player_frame.temp_mech.img_mech.SetDisplayFrameByPath('', image_path)
        self.panel.nd_player_frame.temp_mech.img_mech_shade.SetDisplayFrameByPath('', image_path)
        lobby_select_id = dress_utils.get_mecha_dress_clothing_id(mecha_id) or dress_utils.battle_id_to_mecha_lobby_id(mecha_id)
        shiny_weapon_id = dress_utils.get_mecha_dress_shiny_weapon_id(mecha_id)
        display_type = lobby_model_display_const.ZOMBIEFFA_CHOOSE_MECHA_SCENE
        global_data.emgr.set_lobby_scene_display_type.emit(display_type)
        model_data = lobby_model_display_utils.get_lobby_model_data(lobby_select_id, consider_second_model=False)
        for data in model_data:
            data['skin_id'] = lobby_select_id
            data['model_scale'] = 3
            data['shiny_weapon_id'] = shiny_weapon_id
            if mecha_id == 8028:
                data['show_anim'] = data['end_anim']

        global_data.emgr.change_model_display_scene_item.emit(model_data)