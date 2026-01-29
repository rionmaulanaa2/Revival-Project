# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/ffa/FFAChooseMechaUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_CUSTOM
from common.cfg import confmgr
from logic.gutils import dress_utils
from logic.gcommon import time_utility as tutil
from logic.gutils import item_utils
from logic.comsys.battle.ffa.FFAChooseMechaInfoWidget import FFAChooseMechaInfoWidget
import cc
TRK_ACTION_TAG = 16383

class FFAChooseMechaUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_ffa/ffa2_choose_mech'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CUSTOM
    UI_ACTION_EVENT = {'nd_touch.OnDrag': 'on_drag_model',
       'btn_sure.OnClick': 'on_confirm_choose'
       }
    GLOBAL_EVENT = {'on_ffa_choose_mecha_start': 'start_countdown_widget',
       'ffa_choose_mecha_finish': 'choose_mecha_finish',
       'ffa_confirmed_cnt_update': 'refresh_confirmed_info'
       }

    def ui_vkb_custom_func(self):
        return True

    def on_init_panel(self, *args, **kwargs):
        self.init_parameter()
        self.hide()

    def init_parameter(self):
        self.select_id = global_data.battle.chosen_mecha_id
        self.choose_finished_timer = None
        self.skill_info_widget = None
        self.select_idx = -1
        return

    def enter_choose_mecha(self):
        self.init_battle_data()
        self.init_choose_mecha_widget()
        self.init_map_info_widget()
        self.refresh_confirmed_info()
        self.start_countdown_widget()
        self.show()
        global_data.sound_mgr.play_music('gvg_pre')
        global_data.sound_mgr.play_ui_sound('ui_gvg_mecha_select')
        global_data.sound_mgr.play_sound_2d('Play_ui_notice', ('ui_notice', 'medal_flight'))
        global_data.ui_mgr.add_ui_show_whitelist(['FFAChooseMechaUI', 'NoticeUI', 'BattleReconnectUI', 'NormalConfirmUI2'], 'FFAChooseMecha')
        self.panel.PlayAnimation('show')
        self.panel.PlayAnimation('keep')
        if not self.is_confirmed():
            self.panel.PlayAnimation('yes')

    def on_finalize_panel(self):
        if self.skill_info_widget:
            self.skill_info_widget.destroy()
        global_data.ui_mgr.remove_ui_show_whitelist('FFAChooseMecha')

    def init_battle_data(self):
        battle = global_data.battle
        self.map_conf = confmgr.get('map_config', str(battle.map_id), default={})
        self.mecha_order = []
        if global_data.player:
            mecha_open_info = global_data.player.read_mecha_open_info()
            mecha_closed = []
            mecha_open_order = mecha_open_info.get('opened_order', [])
            for mecha_id in mecha_open_order:
                if self._avatar_has_mecha(mecha_id):
                    self.mecha_order.append(mecha_id)
                else:
                    mecha_closed.append(mecha_id)

            self.mecha_order.extend(mecha_closed)

    def on_drag_model(self, btn, touch):
        from logic.client.const import lobby_model_display_const
        delta_pos = touch.getDelta()
        global_data.emgr.rotate_model_display.emit(-delta_pos.x / lobby_model_display_const.ROTATE_FACTOR)

    def on_confirm_choose(self, *args):
        if not global_data.battle:
            return
        self.panel.btn_sure.SetEnable(False)
        self.panel.btn_sure.SetText('')
        self.panel.runAction(cc.Sequence.create([
         cc.CallFunc.create(lambda : self.panel.StopAnimation('yes')),
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('tap')),
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('change')),
         cc.DelayTime.create(self.panel.GetAnimationMaxRunTime('tap')),
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('wait')),
         cc.CallFunc.create(lambda : self.panel.nd_wait.setVisible(True))]))
        self.panel.lab_prompt.SetString(18235)
        self.panel.nd_await.setVisible(False)
        self.panel.nd_ready.setVisible(True)
        global_data.battle.confirm_choose_mecha()

    def refresh_confirmed_info(self):
        battle = global_data.battle
        if not battle:
            pass
        progress_str = '{}/{}'.format(battle.choose_mecha_confirmed_cnt, battle.choose_mecha_player_cnt)
        self.panel.lab_nub.SetString(progress_str)
        self.panel.PlayAnimation('player')
        if self.is_confirmed():
            self.on_confirm_choose()

    def is_confirmed(self):
        battle = global_data.battle
        if battle:
            return battle.choose_mecha_confirm
        return False

    def choose_mecha_finish(self):
        battle = global_data.battle
        if not battle or not battle.choose_mecha_finish:
            return
        self.panel.runAction(cc.Sequence.create([
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('out')),
         cc.DelayTime.create(self.panel.GetAnimationMaxRunTime('out')),
         cc.CallFunc.create(lambda : global_data.emgr.change_model_display_scene_item.emit(None)),
         cc.CallFunc.create(lambda : global_data.emgr.ffa_enter_battle.emit())]))

    def init_choose_mecha_widget(self):
        choose_list_node = self.panel.mech_choose_list
        choose_list_node.SetInitCount(len(self.mecha_order))
        all_items = choose_list_node.GetAllItem()
        for index, widget in enumerate(all_items):
            self.create_choose_item(index, widget)

    def create_choose_item(self, index, widget):
        from logic.gutils import mecha_skin_utils
        mecha_id = self.mecha_order[index]
        own_mecha = self._avatar_has_mecha(mecha_id)
        mecha_base_skin = mecha_skin_utils.get_original_skin_lst(mecha_id)[0]
        image_path = 'gui/ui_res_2/item/mecha_skin/%s.png' % mecha_base_skin
        widget.img_mech.SetDisplayFrameByPath('', image_path)
        widget.img_mech_shade.SetDisplayFrameByPath('', image_path)
        from logic.gcommon.cdata.limited_time_free_mecha_data import is_mecha_limited_free_now_by_mecha_id
        free = is_mecha_limited_free_now_by_mecha_id(mecha_id)
        widget.nd_mode_tips.setVisible(free)
        if own_mecha:
            widget.nd_lock.setVisible(False)
        else:
            widget.nd_lock.setVisible(True)
        if self.select_id == mecha_id:
            self.select_idx = index
            widget.img_choose.setVisible(True)
            self.set_mecha_chosen(mecha_id)
            self.switch_select_widget(None, widget)

        @widget.btn_dian.callback()
        def OnClick(touch, btn, mecha_id=mecha_id, idx=index, own=own_mecha):
            if self.is_confirmed():
                return
            if not own:
                global_data.game_mgr.show_tip(get_text_by_id(81030))
                return
            self.set_mecha_btn_select(idx, mecha_id)

        return

    def switch_select_widget(self, prev_widget, cur_widget):
        if prev_widget:
            self.panel.stopActionByTag(TRK_ACTION_TAG)
            prev_widget.img_choose.setVisible(False)
            prev_widget.setLocalZOrder(0)
            prev_widget.StopAnimation('loop')
            prev_widget.PlayAnimation('endloop')
            prev_widget.PlayAnimation('reduce')
            prev_widget.RecoverAnimationNodeState('choose')
        cur_widget.img_choose.setVisible(True)
        cur_widget.setLocalZOrder(1)
        cur_widget.RecordAnimationNodeState('choose')
        action = self.panel.runAction(cc.Sequence.create([
         cc.CallFunc.create(lambda : cur_widget.PlayAnimation('choose')),
         cc.DelayTime.create(cur_widget.GetAnimationMaxRunTime('choose')),
         cc.CallFunc.create(lambda : cur_widget.PlayAnimation('loop'))]))
        action.setTag(TRK_ACTION_TAG)

    def set_mecha_btn_select(self, idx, select_id):
        if self.select_id == select_id:
            return
        else:
            if select_id:
                pre_idx = self.select_idx
                self.select_idx = idx
                self.select_id = select_id
                prev_widget = None
                if pre_idx >= 0:
                    prev_widget = self.panel.mech_choose_list.GetItem(pre_idx)
                widget = self.panel.mech_choose_list.GetItem(self.select_idx)
                self.switch_select_widget(prev_widget, widget)
            self.set_mecha_chosen(select_id)
            return

    def init_map_info_widget(self):
        battle = global_data.battle
        map_name_text_ids = self.map_conf.get('cMapNameTextIds', [])
        text_id_index = 0
        prefix_str = ''
        if len(map_name_text_ids) > 1 and battle and hasattr(battle, 'area_id'):
            text_id_index = min(int(battle.area_id), len(map_name_text_ids)) - 1
            prefix_str = '\xe2\x80\x94'
        self.panel.lab_map_name.setVisible(bool(prefix_str))
        map_text = ''.join([prefix_str, get_text_by_id(map_name_text_ids[text_id_index])])
        self.panel.lab_map_name.SetString(map_text)

    def refresh_mecha_info(self, mecha_id):
        if not self.skill_info_widget:
            self.skill_info_widget = FFAChooseMechaInfoWidget(self, self.panel.nd_ability, mecha_id)
        else:
            self.skill_info_widget.on_switch_to_mecha_type(mecha_id)
        mecha_name = item_utils.get_mecha_name_by_id(mecha_id)
        self.panel.nd_name.lab_name1.SetString(mecha_name)
        self.panel.nd_name.lab_name2.SetString(mecha_name)
        self.panel.nd_name.lab_name3.SetString(mecha_name)

    def start_countdown_widget(self):
        battle = global_data.battle
        if not battle or not battle.choose_mecha_end_ts:
            return
        total_time = battle.choose_mecha_end_ts - tutil.time()
        self.start_countdown(total_time)

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

    def set_mecha_chosen(self, select_id):
        self.select_id = select_id
        self.switch_mecha_display(select_id)
        self.refresh_mecha_info(select_id)

    def switch_mecha_display(self, mecha_id):
        from logic.client.const import lobby_model_display_const
        from logic.gutils import lobby_model_display_utils
        battle = global_data.battle
        battle and battle.request_choose_mecha(mecha_id)
        lobby_select_id = dress_utils.get_mecha_dress_clothing_id(mecha_id) or dress_utils.battle_id_to_mecha_lobby_id(mecha_id)
        shiny_weapon_id = dress_utils.get_mecha_dress_shiny_weapon_id(mecha_id)
        display_type = lobby_model_display_const.FFA_CHOOSE_MECHA_SCENE
        global_data.emgr.set_lobby_scene_display_type.emit(display_type)
        model_data = lobby_model_display_utils.get_lobby_model_data(lobby_select_id, consider_second_model=False)
        for data in model_data:
            data['skin_id'] = lobby_select_id
            data['model_scale'] = 3
            data['shiny_weapon_id'] = shiny_weapon_id
            if mecha_id == 8028:
                data['show_anim'] = data['end_anim']

        global_data.emgr.change_model_display_scene_item.emit(model_data)

    def _avatar_has_mecha(self, mecha_id):
        bat = global_data.battle
        if bat:
            return bat.avatar_has_mecha(mecha_id)
        return False