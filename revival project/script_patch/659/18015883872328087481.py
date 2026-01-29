# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/PVELobbyUI.py
from __future__ import absolute_import
from __future__ import print_function
import six
from six.moves import range
import time
import game3d
import cc
from common.platform.device_info import DeviceInfo
from common.uisys.basepanel import BasePanel
from common.const.uiconst import BASE_LAYER_ZORDER, UI_VKB_CUSTOM
from logic.gutils.mall_utils import show_lobby_lottery_red_point, get_all_mall_red_point, has_any_discount_hint
from common.utils.redpoint_check_func import check_lobby_red_point
from logic.gutils.client_utils import post_ui_method, safe_widget, safe_call
from logic.gutils.role_head_utils import init_role_head
from logic.gutils.lv_template_utils import init_lv_template
from logic.gutils.red_point_utils import get_LobbyUI_role_head_level, show_red_point_template, get_priv_setting_rp, check_bgm_rp, RED_POINT_LEVEL_10, get_LobbyUI_item_book_rp_level
from logic.comsys.mall_ui.MallMainUI import MallMainUI
from logic.gutils.lobby_click_interval_utils import check_click_interval
from logic.gutils.jump_to_ui_utils import jump_to_lottery, jump_to_season_pass
from logic.gutils.advance_utils import BATTLE_PASS_ADVANCE
from logic.vscene.parts.gamemode.GMDecorator import halt_by_create_login
from logic.comsys.setting_ui.MainSettingUI import MainSettingUI
from logic.comsys.map.InteractionInvokeBtnWidget import InteractionInvokeBtnWidget
from logic.comsys.lobby.LobbyInteractionUI import LobbyInteractionUI
from logic.comsys.lobby.LobbyYueKaEntryWidget import LobbyYueKaEntryWidget
from logic.vscene.parts.ctrl.InputMockHelper import TouchMock
from logic.gutils.battle_pass_utils import need_sp_red
from logic.gutils.system_unlock_utils import is_sys_unlocked, SYSTEM_BATTLE_PASS
from logic.gutils.template_utils import create_and_init_mall_new_icon, create_and_init_mall_discount_icon
from logic.comsys.lobby.LobbyMoreListPanelWidget import LobbyMoreListPanelWidget
from logic.gcommon import time_utility as tutil
from logic.comsys.task.TaskMainUI import TaskMainUI
from logic.gutils.activity_utils import has_weekly_card_redpoint, has_yueka_redpoint, has_new_role_12_goods_redpoint

class PVELobbyUI(BasePanel):
    PANEL_CONFIG_NAME = 'lobby/lobby_new_pve'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_ACTION_EVENT = {'nd_lobby_normal.btn_swich_lobby.OnClick': 'on_click_back_to_normal_lobby',
       'btn_head.OnClick': 'on_click_player_detail_inf',
       'temp_mall.btn_mall.OnClick': 'on_click_btn_mall',
       'temp_lottery.btn_lottery.OnClick': 'on_click_btn_lottery',
       'temp_season_pass.btn_season_pass.OnClick': 'on_click_btn_season_pass',
       'btn_friends.OnClick': 'on_click_btn_friends',
       'btn_mail.OnClick': 'on_click_btn_mail',
       'btn_red_packet.OnClick': 'on_click_btn_red_packet',
       'btn_more.OnClick': 'on_click_btn_more',
       'temp_mech.btn_mech.OnClick': 'on_click_btn_mech',
       'temp_equip.btn_equip.OnClick': 'on_click_btn_equip',
       'temp_talent.btn_talent.OnClick': 'on_click_btn_talent',
       'temp_catalogue.btn_catalogue.OnClick': 'on_click_btn_catalogue',
       'temp_task.btn_task.OnClick': 'on_click_btn_task',
       'btn_setting.OnBegin': 'on_click_btn_setting',
       'btn_rank.OnClick': 'on_click_btn_rank',
       'temp_bag.btn_bag.OnClick': 'on_click_btn_bag',
       'btn_mode_choose.OnClick': 'on_click_btn_mode_choose'
       }
    GLOBAL_EVENT = {'net_delay_time_event': 'update_network_delay',
       'net_disconnect_event': 'on_net_disconnect',
       'net_login_reconnect_event': 'on_login_reconnect',
       'net_reconnect_event': 'on_net_reconnect',
       'message_update_global_reward_receive': 'update_lottery_red_point',
       'message_update_global_stat': 'update_lottery_red_point',
       'newbiepaas_update_lv': 'update_battle_season_red_point',
       'season_pass_update_lv': 'update_battle_season_red_point',
       'season_pass_update_daily_award': 'update_battle_season_red_point',
       'refresh_item_red_point': 'update_item_red_point',
       'corp_task_changed_event': 'update_task_red_point',
       'receive_task_reward_succ_event': ('update_task_red_point', 'update_lottery_red_point'),
       'season_pass_open_type': 'update_task_red_point',
       'task_prog_changed': ('update_task_red_point', 'update_lottery_red_point'),
       'receive_task_prog_reward_succ_event': ('update_task_red_point', 'update_lottery_red_point'),
       'update_day_vitality_event': 'update_task_red_point',
       'update_day_vitality_reward_event': 'update_task_red_point',
       'update_week_vitality_event': 'update_task_red_point',
       'update_week_vitality_reward_event': 'update_task_red_point',
       'update_setting_btn_red_point': 'update_setting_red_point',
       'system_unlocked': '_on_system_unlocked'
       }
    HOT_KEY_FUNC_MAP = {'switch_interaction.CANCEL': 'keyboard_use_spray_ui_cancel',
       'switch_interaction.DOWN_UP': 'keyboard_use_spray_ui',
       'open_lobby_chat': 'keyboard_open_lobby_chat'
       }
    SIGNAL_INTENSITY = ('gui/ui_res_2/main/icon_{0}01.png', 'gui/ui_res_2/main/icon_{0}02.png',
                        'gui/ui_res_2/main/icon_{0}03.png')
    UI_VKB_TYPE = UI_VKB_CUSTOM
    INIT_RED_POINT_MODULE = [
     'item', 'yueka', 'mall', 'battle_season', 'mech', 'equipment', 'talent', 'task']

    def on_init_panel(self, *args, **kwargs):
        self.init_parameter()
        self.init_status()
        self.init_widget()
        self.init_season_pass_state()
        self.init_all_red_point_and_info()
        self.init_lobby_btns_data()
        self.init_lobby_btns_view()
        self.init_item_book_info()
        self.check_system_open()

    def init_parameter(self):
        self.is_wifi = False
        self.is_disconnect = False
        self.last_update_battery_time = 0
        self.start_count_open_answer_time = 0

    def init_status(self):
        self.panel.img_battery.setVisible(not global_data.is_pc_mode)

        def update_status():
            if not global_data.player:
                return
            cur_time = time.time()
            if cur_time - self.last_update_battery_time > 60:
                self.panel.pg_battery.setPercentage(game3d.get_battery_level())
                self.last_update_battery_time = cur_time
            device_info = DeviceInfo.get_instance()
            net_work_status = device_info.get_network()
            platform = game3d.get_platform()
            if platform in (game3d.PLATFORM_ANDROID, game3d.PLATFORM_IOS):
                is_wifi = net_work_status == 'wifi'
                if is_wifi != self.is_wifi:
                    self.is_wifi = is_wifi
                    global_data.player.do_sync_time()
            else:
                self.is_wifi = True

        self.panel.runAction(cc.RepeatForever.create(cc.Sequence.create([
         cc.CallFunc.create(update_status),
         cc.DelayTime.create(5.0)])))
        update_status()
        global_data.player.do_sync_time()

    def init_widget(self):
        self.show_battlepass_advance = False
        self.init_yueka_entry_widget()
        self.init_inter_invoke_btn_widget()
        self.init_voice_widget()
        self.init_red_packet()
        self.init_lobby_more_list_widget()

    def init_all_red_point_and_info(self):
        self.update_player_info()
        self.update_all_red_point()

    def update_all_red_point--- This code section failed: ---

 170       0  SETUP_LOOP           57  'to 60'
           3  LOAD_FAST             0  'self'
           6  LOAD_ATTR             0  'INIT_RED_POINT_MODULE'
           9  GET_ITER         
          10  FOR_ITER             46  'to 59'
          13  STORE_FAST            1  'module'

 171      16  LOAD_GLOBAL           1  'getattr'
          19  LOAD_GLOBAL           1  'getattr'
          22  LOAD_ATTR             2  'format'
          25  LOAD_FAST             1  'module'
          28  CALL_FUNCTION_1       1 
          31  LOAD_CONST            0  ''
          34  CALL_FUNCTION_3       3 
          37  STORE_FAST            2  'update_func'

 172      40  LOAD_FAST             2  'update_func'
          43  POP_JUMP_IF_FALSE    10  'to 10'

 173      46  LOAD_FAST             2  'update_func'
          49  CALL_FUNCTION_0       0 
          52  POP_TOP          
          53  JUMP_BACK            10  'to 10'
          56  JUMP_BACK            10  'to 10'
          59  POP_BLOCK        
        60_0  COME_FROM                '0'
          60  LOAD_CONST            0  ''
          63  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 34

    def update_item_red_point(self):
        self.update_catalogue_red_point()
        self.update_role_head_rp()
        self.update_setting_red_point()

    @check_click_interval()
    def on_click_player_detail_inf(self, *args):
        ui = global_data.ui_mgr.show_ui('PlayerInfoUI', 'logic.comsys.role')
        ui.refresh_by_uid(global_data.player.uid)
        global_data.lobby_red_point_data.record_main_rp('role_head_rp')

    def update_player_info(self, *args):
        player = global_data.player
        init_role_head(self.panel.btn_head, player.get_head_frame(), player.get_head_photo())
        init_lv_template(self.panel.temp_level, player.get_lv())
        self.panel.lab_name.SetString(player.get_name())
        if G_IS_NA_USER:
            self.panel.lab_id.SetString('ID:{}'.format(global_data.player.uid))
        else:
            show_id = int(global_data.player.uid)
            show_id -= global_data.uid_prefix
            self.panel.lab_id.SetString('ID:{}'.format(show_id))
        have_click_lottery_tab = getattr(global_data, 'have_click_lottery_tab', None)
        if have_click_lottery_tab is None:
            global_data.have_click_lottery_tab = {}
        self.update_lottery_red_point()
        self.update_role_head_rp()
        return

    @post_ui_method
    def update_role_head_rp(self):
        rp_level = get_LobbyUI_role_head_level()
        show_red_point_template(self.panel.btn_head.temp_head_red, rp_level, rp_level)

    @safe_widget
    def init_yueka_entry_widget(self):
        from logic.comsys.lobby.LobbyYueKaEntryWidget import LobbyYueKaEntryWidget
        self.yueka_entry_widget = LobbyYueKaEntryWidget(self, self.panel)

    def update_yueka_red_point(self):
        month_card_red_visible = has_weekly_card_redpoint() or has_yueka_redpoint() or has_new_role_12_goods_redpoint()
        self.panel.btn_month_card.img_red.setVisible(month_card_red_visible)

    @check_click_interval()
    def on_click_btn_mall(self, *args):
        print('\xe6\x89\x93\xe5\xbc\x80pve\xe5\x95\x86\xe5\x9f\x8e')

    def update_mall_red_point(self):
        pass

    @check_click_interval()
    def on_click_btn_lottery(self, *args):
        if not global_data.player:
            return
        global_data.sound_mgr.play_ui_sound('ui_click_luckyhouse')
        from logic.gutils.jump_to_ui_utils import jump_to_lottery
        gift_obj = global_data.player.get_lottery_10_try_gift()
        if gift_obj:
            lottery_id = gift_obj.get_determine_lottery_id()
            jump_to_lottery(lottery_id)
            return
        jump_to_lottery()

    @post_ui_method
    def update_lottery_red_point(self, *args, **kargs):
        red_point = show_lobby_lottery_red_point() and check_lobby_red_point()
        if red_point:
            self.panel.temp_lottery.StopAnimation('lottery')
            self.panel.temp_lottery.RecoverAnimationNodeState('lottery')
            self.panel.temp_lottery.PlayAnimation('lottery_sp')
        else:
            self.panel.temp_lottery.StopAnimation('lottery_sp')
            self.panel.temp_lottery.RecoverAnimationNodeState('lottery_sp')
            self.panel.temp_lottery.PlayAnimation('lottery')
        self.panel.temp_lottery.btn_lottery.red_point.setVisible(red_point)

    def update_battle_season_red_point(self, *args):
        from logic.gutils.battle_pass_utils import need_sp_red
        need_show = True if need_sp_red() else False
        self.update_season_red_point(need_show)

    def init_season_pass_state(self, *args):
        has_unlock = is_sys_unlocked(SYSTEM_BATTLE_PASS)
        self.panel.temp_season_pass.setVisible(has_unlock)

    @check_click_interval()
    def on_click_btn_season_pass(self, *args):
        from logic.gutils import advance_utils
        from logic.gutils.jump_to_ui_utils import jump_to_season_pass
        jump_to_season_pass()
        if self.show_battlepass_advance:
            self.show_battlepass_advance = False
            global_data.player.add_advance_ids(advance_utils.BATTLE_PASS_ADVANCE)
            global_data.player.start_show_advance()

    @halt_by_create_login
    def update_season_red_point(self, need_show):
        need_show = need_show and check_lobby_red_point()
        self.panel.temp_season_pass.btn_season_pass.red_point.setVisible(need_show)

    def on_click_btn_friends(self, *args):
        global_data.ui_mgr.show_ui('MainFriend', 'logic.comsys.message')

    def on_click_btn_mail(self, *args):
        global_data.ui_mgr.show_ui('MainEmail', 'logic.comsys.message')

    @safe_widget
    def init_inter_invoke_btn_widget(self):
        self.inter_invoke_btn_widget = InteractionInvokeBtnWidget(self.panel.btn_interaction, self.panel, LobbyInteractionUI, self.__class__.__name__)
        self.panel.btn_interaction.BindMethod('OnBegin', self.inter_invoke_btn_widget.on_touch_inter_begin)
        self.panel.btn_interaction.BindMethod('OnDrag', self.inter_invoke_btn_widget.on_touch_inter_drag)
        self.panel.btn_interaction.BindMethod('OnEnd', self.inter_invoke_btn_widget.on_touch_inter_end)
        self.panel.btn_interaction.BindMethod('OnCancel', self.inter_invoke_btn_widget.on_touch_inter_cancel)

    @safe_widget
    def init_voice_widget(self):
        from logic.comsys.lobby.LobbyVoiceWidget import LobbyVoiceWidget
        self.voice_widget = LobbyVoiceWidget(self, self.panel)

    def init_red_packet(self):
        self._red_packet_timer = None
        if G_IS_NA_USER:
            self.panel.btn_red_packet.SetPosition(450, 16)
        else:
            self.panel.btn_red_packet.SetPosition(384, 16)
        self.panel.btn_red_packet.setVisible(False)
        return

    def on_click_btn_red_packet(self, btn, touch):
        ui = global_data.ui_mgr.get_ui('MainChat')
        if ui:
            ui.show_main_chat_ui()
        self.hide_red_packet_vx()

    def show_red_packet_vx(self, red_packet_info):
        self.panel.PlayAnimation('hongbaorukou_loop')
        self.panel.btn_red_packet.setVisible(True)
        if self._red_packet_timer:
            global_data.game_mgr.unregister_logic_timer(self._red_packet_timer)
        global_data.game_mgr.register_logic_timer(self.hide_red_packet_vx, interval=6, times=1, mode=2)

    def hide_red_packet_vx(self):
        if not self.panel or not self.panel.isValid():
            return
        self.panel.StopAnimation('hongbaorukou_loop')
        self.panel.btn_red_packet.setVisible(False)

    def ui_vkb_custom_func(self):
        if self.team_invite_widget.nd_vis:
            self.team_invite_widget.hide()
            return True
        else:
            vis = self.panel.list_more_panel.isVisible()
            if vis:
                self.lobby_more_list_widget.hide_widget()
                return True
            return False

    def init_lobby_btns_data(self):
        from logic.gutils import system_unlock_utils
        self._orig_lobby_btn_data_list = [
         (None, 'temp_mech', 'lab_mech'),
         (None, 'temp_equip', 'lab_equip'),
         (None, 'temp_talent', 'lab_talent'),
         (None, 'temp_catalogue', 'lab_catalogue'),
         (None, 'temp_bag', 'temp_bag'),
         (None, 'temp_task', 'lab_task')]
        self._effective_sys_set = set()
        self._lock_ui_data = {}
        self._update_effective_lobby_btn_data_list()
        return None

    def _update_effective_lobby_btn_data_list(self):
        self._effective_lobby_btn_data_list = []
        self._effective_sys_set.clear()
        for btn_data in self._orig_lobby_btn_data_list:
            sys_type = btn_data[0]
            if sys_type is not None:
                from logic.gutils import system_unlock_utils
                if sys_type == system_unlock_utils.SYSTEM_INSCRIPTION:
                    has_open = global_data.player.has_open_inscription()
                    if not has_open:
                        continue
                else:
                    has_u = system_unlock_utils.is_sys_unlocked(sys_type)
                    has_m = system_unlock_utils.has_sys_unlock_mechanics(sys_type)
                    if has_m and not has_u:
                        continue
            self._effective_lobby_btn_data_list.append(btn_data)
            self._effective_sys_set.add(sys_type)

        self._refresh_lobby_btns_active_state()
        return

    def _refresh_lobby_btns_active_state(self):
        for btn_data in self._orig_lobby_btn_data_list:
            sys_type = btn_data[0]
            if sys_type is None:
                continue
            lock_ui_data = self._lock_ui_data.get(sys_type, None)
            if lock_ui_data is None:
                continue
            icon_name = lock_ui_data[0]
            lab_normal_color = lock_ui_data[1]
            lab_lock_color = lock_ui_data[2]
            temp, lab = btn_data[1], btn_data[2]
            temp_item = getattr(self.panel, temp)
            if not temp_item:
                continue
            lab_item = getattr(temp_item, lab)
            icon_item = getattr(temp_item, icon_name)
            lock_item = getattr(temp_item, 'img_lock')
            active = sys_type in self._effective_sys_set
            icon_item and icon_item.setVisible(active)
            lock_item and lock_item.setVisible(not active)
            if active:
                lab_color = lab_normal_color if 1 else lab_lock_color
                lab_item and lab_item.SetColor(lab_color)

        return

    def init_lobby_btns_view(self):
        self.refresh_lobby_btn_text_position()
        self.random_play_animation()

    def refresh_lobby_btn_text_position(self):
        for btn_data in self._orig_lobby_btn_data_list:
            temp, lab = btn_data[1], btn_data[2]
            temp_item = getattr(self.panel, temp)
            if temp_item:
                lab_item = getattr(temp_item, lab)
                if lab_item:
                    lab_item.RefreshChildByRealSize()

    def random_play_animation(self):
        import random
        t = random.randrange(10, 61)
        self.panel.SetTimeOut(t / 10.0, lambda : self.play_random_node())

    def play_random_node(self):
        btn_data_list = self._effective_lobby_btn_data_list
        import random
        btn_data = random.choice(btn_data_list)
        node_name = btn_data[1]
        temp_item = getattr(self.panel, node_name)
        if temp_item and temp_item.IsPlayingAnimation('show'):
            for i in range(0, 4):
                btn_data = random.choice(btn_data_list)
                node_name = btn_data[1]
                temp_item = getattr(self.panel, node_name)
                if temp_item:
                    if not temp_item.IsPlayingAnimation('show'):
                        break

        temp_item.PlayAnimation('show')
        self.random_play_animation()

    @safe_widget
    def init_lobby_more_list_widget(self):
        self.lobby_more_list_widget = LobbyMoreListPanelWidget(self, self.panel)
        self.lobby_more_list_widget.init_survey()

    def on_click_btn_more(self, btn, touch):
        vis = self.panel.list_more_panel.isVisible()
        if not vis:
            angle = 180 if 1 else 0
            self.panel.btn_more.icon_more.setRotation(angle)
            vis or self.lobby_more_list_widget.show_widget()
        else:
            self.lobby_more_list_widget.hide_widget()

    def on_click_btn_mech(self, *args):
        print('\xe6\x89\x93\xe5\xbc\x80pve\xe6\x9c\xba\xe7\x94\xb2')

    @post_ui_method
    def update_mech_red_point(self):
        pass

    def on_click_btn_equip(self, *args):
        print('\xe6\x89\x93\xe5\xbc\x80pve\xe8\xa3\x85\xe5\xa4\x87')

    @post_ui_method
    def update_equipment_red_point(self):
        pass

    def on_click_btn_talent(self, *args):
        global_data.ui_mgr.show_ui('PVETalentUI', 'logic.comsys.battle.pve')

    @post_ui_method
    def update_talent_red_point(self):
        pass

    def init_item_book_info(self):
        from common.cfg import confmgr
        self._item_book_need_remind_item = None
        weapon_conf = confmgr.get('items_book_conf', 'WeaponConfig', 'Content')
        for lobby_item_no, item_data in six.iteritems(weapon_conf):
            if item_data.get('new_weapon_tip_text_id', 0) > 0:
                self._item_book_need_remind_item = item_data
                break

        return

    def _is_need_show_item_book_new_item_tip(self):
        if self._item_book_need_remind_item:
            item_no = self._item_book_need_remind_item.get('default_fashion', 0)
            return not global_data.lobby_red_point_data.has_remind_item_book_new_item(item_no)
        return False

    @check_click_interval()
    def on_click_btn_catalogue(self, *args):
        if not global_data.player:
            return
        if self._is_need_show_item_book_new_item_tip():
            from logic.gutils import jump_to_ui_utils
            item_no = self._item_book_need_remind_item.get('default_fashion', 0)
            jump_to_ui_utils.jump_to_display_detail_by_item_no(item_no)
            global_data.lobby_red_point_data.mark_item_book_new_item_reminded(item_no)
            self.update_catalogue_red_point()
        else:
            from logic.comsys.items_book_ui.ItemsBookMainUI import ItemsBookMainUI
            ItemsBookMainUI()
            global_data.lobby_red_point_data.record_main_rp('item_book_rp')

    @post_ui_method
    def update_catalogue_red_point(self, *args):
        rp_level = get_LobbyUI_item_book_rp_level()
        show_red_point_template(self.panel.temp_catalogue.btn_catalogue.red_point, rp_level, rp_level)

    def on_click_btn_task(self, *args):
        ui = global_data.ui_mgr.get_ui('TaskMainUI')
        if not ui:
            ui = global_data.ui_mgr.show_ui('TaskMainUI', 'logic.comsys.task')
        if ui:
            ui.show()

    def update_task_red_point(self, *args):
        redpoint = TaskMainUI.check_red_point() and check_lobby_red_point()
        self.panel.temp_task.btn_task.red_point.setVisible(redpoint)

    def on_click_btn_setting(self, *args):
        MainSettingUI(parent=self.panel)

    @post_ui_method
    def update_setting_red_point(self):
        new_priv_setting = get_priv_setting_rp()
        new_bgm = check_bgm_rp()
        self.panel.btn_setting.img_red.setVisible(new_priv_setting or new_bgm)
        show_red_point_template(self.panel.btn_head.temp_head_red, new_priv_setting, RED_POINT_LEVEL_10)

    @check_click_interval()
    def on_click_btn_rank(self, *args):
        print('\xe6\x89\x93\xe5\xbc\x80pve\xe6\x8e\x92\xe8\xa1\x8c\xe6\xa6\x9c')

    def on_click_btn_bag(self, *args):
        global_data.ui_mgr.show_ui('LobbyBagUI', 'logic.comsys.lobby')

    def on_click_btn_mode_choose(self, *args):
        global_data.ui_mgr.show_ui('PVESelectChapterUI', 'logic.comsys.battle.pve')

    def check_system_open(self):
        has_open = global_data.player.has_open_inscription()
        if has_open:
            from logic.gutils.bond_utils import need_bond_guided
            if need_bond_guided():
                return
            global_data.emgr.on_notify_guide_event.emit('inscr_guide_lobby')
            from logic.gutils import system_unlock_utils
            self._on_system_unlocked(system_unlock_utils.SYSTEM_INSCRIPTION)

    def on_inscription_open(self):
        self.check_system_open()
        self.refresh_lobby_btn_text_position()

    def _on_system_unlocked(self, sys_type):
        interested = False
        for btn_data in self._orig_lobby_btn_data_list:
            _sys_type = btn_data[0]
            if _sys_type == sys_type:
                interested = True
                break

        if interested:
            self._update_effective_lobby_btn_data_list()
        from logic.gutils import system_unlock_utils
        if sys_type == system_unlock_utils.SYSTEM_BATTLE_PASS:
            self.init_season_pass_state()
            self.update_battle_season_red_point()
            self.update_task_red_point()
            self.show_battlepass_advance = True

    def on_click_back_to_normal_lobby(self, *args):
        global_data.is_pve_lobby = False
        global_data.emgr.change_lobby_scene.emit()

    def keyboard_use_spray_ui(self, msg, keycode):
        return self.inter_invoke_btn_widget.on_switch_interactio_key_down_up(msg, keycode)

    def keyboard_use_spray_ui_cancel(self):
        return self.inter_invoke_btn_widget.on_switch_interactio_key_cancel()

    def keyboard_open_lobby_chat(self, *args):
        chat_ui = global_data.ui_mgr.get_ui('MainChat')
        if not chat_ui:
            return
        if not chat_ui.isPanelVisible() or not self.isPanelVisible():
            return

        def auto_click_input_box():
            if not chat_ui:
                return
            else:
                if chat_ui._input_box is None:
                    return
                if chat_ui._input_box._pnl_input is None:
                    return
                click_input_box = getattr(chat_ui._input_box._pnl_input.touch_layer, 'OnClick')
                click_input_box(TouchMock(None))
                return

        chat_ui._on_main_chat_ui(on_shown_cb=auto_click_input_box)

    def _show_scene_stack_log(self):
        if not self.panel or not self.panel.isVisible():
            return
        ag = global_data.ex_scene_mgr_agent
        global_data.game_mgr.show_tip('\xe5\x86\x85\xe6\x9c\x8d\xef\xbc\x9a\xe5\xa4\xa7\xe5\x8e\x85\xe5\x9c\xba\xe6\x99\xaf\xe6\xa0\x88\xe5\xbc\x95\xe7\x94\xa8\xe6\xb8\x85\xe7\xa9\xba' + ('---\xe5\xa4\xb1\xe8\xb4\xa5!!' if ag.scene_stack or ag.scene_ui_stack or ag.scene_ui_map else '\xe6\x88\x90\xe5\x8a\x9f'))
        global_data.game_mgr.show_tip('\xe5\x86\x85\xe6\x9c\x8d\xef\xbc\x9a\xe5\xa4\xa7\xe5\x8e\x85\xe5\x9c\xba\xe6\x99\xaf\xe6\xa0\x88\xe5\xbc\x95\xe7\x94\xa8\xe6\xb8\x85\xe7\xa9\xba' + ('---\xe5\xa4\xb1\xe8\xb4\xa5!!' if ag.scene_stack or ag.scene_ui_stack or ag.scene_ui_map else '\xe6\x88\x90\xe5\x8a\x9f'))
        global_data.game_mgr.show_tip('\xe5\x86\x85\xe6\x9c\x8d\xef\xbc\x9a\xe5\xa4\xa7\xe5\x8e\x85\xe5\x9c\xba\xe6\x99\xaf\xe6\xa0\x88\xe5\xbc\x95\xe7\x94\xa8\xe6\xb8\x85\xe7\xa9\xba' + ('---\xe5\xa4\xb1\xe8\xb4\xa5!!' if ag.scene_stack or ag.scene_ui_stack or ag.scene_ui_map else '\xe6\x88\x90\xe5\x8a\x9f'))

    def update_network_delay(self, rtt_type, rtt):
        delay = min(999, int(rtt * 1000))
        if rtt_type == tutil.TYPE_GAME:
            self.panel.lab_network.SetString('{0}ms'.format(delay))
            intensity = 0 if delay < 100 else (1 if delay < 250 else 2)
            pic = self.SIGNAL_INTENSITY[intensity].format('wifi' if self.is_wifi else 'xin')
            self.panel.img_wifi.SetDisplayFrameByPath('', pic)

    def on_login_reconnect(self, *args):
        self.on_net_reconnect()

    def on_net_reconnect(self, *args):
        self.is_disconnect = False
        self.panel.img_wifi.setVisible(True)
        self.panel.nd_connecting.setVisible(False)
        self.panel.StopAnimation('connecting')

    def on_net_disconnect(self, *args):
        self.is_disconnect = True
        self.panel.img_wifi.setVisible(False)
        self.panel.nd_connecting.setVisible(True)
        self.panel.PlayAnimation('connecting')

    def on_finalize_panel(self):
        super(PVELobbyUI, self).on_finalize_panel()
        self.unit_widget()

    def unit_widget(self):
        self.inter_invoke_btn_widget.destory()
        self.inter_invoke_btn_widget = None
        self.destroy_widget('voice_widget')
        self.destroy_widget('yueka_entry_widget')
        self.destroy_widget('lobby_more_list_widget')
        return

    def do_hide_panel(self):
        super(PVELobbyUI, self).do_hide_panel()
        self.yueka_entry_widget.on_lobby_ui_hide()
        global_data.emgr.lobby_ui_visible.emit(False)

    def do_show_panel(self):
        super(PVELobbyUI, self).do_show_panel()
        global_data.emgr.lobby_ui_visible.emit(True)