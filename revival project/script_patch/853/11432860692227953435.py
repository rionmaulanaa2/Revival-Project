# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/control_ui/PVEInfoUI.py
from __future__ import absolute_import
from common.cfg import confmgr
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_CLOSE_BY_DEFAULT_FUNC_NAME, UI_TYPE_MESSAGE
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.pve_utils import get_effect_desc_text, is_pve_multi_player_team, get_bless_elem_res, DEFAULT_BLESS_BAR, set_elems_icon_list_by_bless
from logic.gcommon.time_utility import get_server_time
from logic.gutils.template_utils import set_ui_show_picture
from logic.comsys.battle.pve.PVETeamStatisticsWidget import PVETeamStatisticsWidget
from logic.comsys.battle.pve.PVEItemWidget import PVEBreakWidget, PVEBlessWidget, PVEItemWidget
import logic.gcommon.time_utility as tutils
from logic.gutils.dress_utils import battle_id_to_mecha_lobby_id
import six_ex
import time
import copy
import cc
from logic.gcommon.common_const.pve_const import EMPTY_WIDGET_PATH

class PVEInfoUI(BasePanel):
    PANEL_CONFIG_NAME = 'pve/info/pve_info_main'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE_BY_DEFAULT_FUNC_NAME
    MOUSE_CURSOR_TRIGGER_SHOW = True
    EXCEPT_HIDE_UI_LIST = [
     'FightLeftShotUI',
     'MoveRockerTouchUI',
     'FightReadyTipsUI',
     'PVEInfoUI',
     'PVEBlessConfUI',
     'PVEBreakConfUI',
     'PVEShopUI']
    UI_ACTION_EVENT = {'btn_close.OnClick': 'on_click_close_btn'
       }
    TAB_TEXT = [
     482,
     483]
    INFO = [
     [
      393,
      'ret_dur'],
     [
      394,
      'damage'],
     [
      395,
      'kill_monster'],
     [
      445,
      'coin'],
     [
      397,
      'crystal_stone'],
     [
      398,
      'story_card']]
    EXTRA_INFO = [
     [
      536,
      'pve/info/i_pve_info_element',
      'get_element_info']]
    TS_TAG = 20231019

    def on_init_panel(self, *args):
        super(PVEInfoUI, self).on_init_panel(*args)
        self.init_params()
        self.init_ui()
        self.init_widget()
        self.process_events(True)

    def on_finalize_panel(self):
        self.process_events(False)
        self.break_widget and self.break_widget.destroy()
        self.bless_widget and self.bless_widget.destroy()
        self.team_info_widget and self.team_info_widget.destroy()
        self.clear_async_action()
        super(PVEInfoUI, self).on_finalize_panel()

    def init_params(self):
        self.is_multi_player_team = is_pve_multi_player_team()
        self.select_tab_idx = -1
        self._create_idx = 0
        self._async_action = None
        self._other_ui_visible = False
        self.mecha_id = 8001
        if global_data.player and global_data.player.logic:
            self.mecha_id = global_data.player.logic.ev_g_get_bind_mecha_type()
        self.mecha_item_id = battle_id_to_mecha_lobby_id(self.mecha_id)
        self.skin_id = global_data.player.get_pve_using_mecha_skin(self.mecha_item_id)
        self.break_conf = confmgr.get('mecha_breakthrough_data', str(self.mecha_id), default=None)
        self.bless_conf = confmgr.get('bless_data', default=None)
        self.item_conf = confmgr.get('pve_shop_data')
        self.break_widget = None
        self.bless_widget = None
        self.item_widget = None
        self.bless_donate_left_cnt = None
        self.team_info_widget = None
        self.break_data = None
        self.bless_data = None
        self.item_data = None
        self.init_ts = 0
        self.my_pve_mecha_info = None
        return

    def get_info_logic(self):
        if global_data.player and global_data.player.logic:
            if global_data.player.is_in_global_spectate() or global_data.player.logic.ev_g_is_in_spectate():
                spectate_target = global_data.player.logic.ev_g_spectate_target()
                if spectate_target and spectate_target.logic:
                    return spectate_target.logic
            else:
                return global_data.player.logic
        return None

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'pve_battle_info_event': self.update_level_info,
           'pve_update_bless_event': self.on_pve_bless_update,
           'pve_remove_bless_event': self.on_pve_bless_update
           }
        emgr.bind_events(econf) if is_bind else emgr.unbind_events(econf)

    def init_ui(self):
        if not global_data.player or not global_data.player.logic:
            return
        if self.is_multi_player_team:
            self.panel.nd_content.nd_team.setVisible(True)
            self.panel.nd_content.nd_personal.setVisible(False)
            self.panel.list_tab.setVisible(True)
            self.init_list_tab()
        else:
            self.panel.nd_content.nd_personal.setVisible(True)
            self.panel.nd_content.nd_team.setVisible(False)
            self.panel.list_tab.setVisible(False)
        self.init_player_info()
        self.init_level_info()
        self.init_break()
        self.init_bless()
        self.init_item()

    def init_list_tab(self):
        self.panel.list_tab.SetInitCount(2)
        btn_team = self.panel.list_tab.GetItem(0).btn_tab
        btn_team.SetText(get_text_by_id(self.TAB_TEXT[0]))

        @btn_team.unique_callback()
        def OnClick(*args):
            self.panel.nd_content.nd_team.setVisible(True)
            self.panel.nd_content.nd_personal.setVisible(False)
            self.switch_select_tab(0)

        btn_single = self.panel.list_tab.GetItem(1).btn_tab
        btn_single.SetText(get_text_by_id(self.TAB_TEXT[1]))

        @btn_single.unique_callback()
        def OnClick(*args):
            self.panel.nd_content.nd_personal.setVisible(True)
            self.panel.nd_content.nd_team.setVisible(False)
            self.switch_select_tab(1)

        self.switch_select_tab(0)

    def switch_select_tab(self, idx):
        if idx != self.select_tab_idx:
            self.panel.list_tab.GetItem(self.select_tab_idx).btn_tab.SetSelect(False)
            self.panel.list_tab.GetItem(idx).btn_tab.SetSelect(True)
            self.select_tab_idx = idx
            self.on_click_empty()
            if self.team_info_widget:
                self.team_info_widget.on_click_empty()

    def init_player_info(self):
        set_ui_show_picture(self.skin_id, mecha_nd=self.panel.temp_pic)
        char_name = global_data.player.logic.ev_g_char_name()
        self.panel.lab_name.SetString(char_name)

    def on_pve_bless_update(self, *args):
        self.init_bless()
        self.init_level_info()

    def init_level_info(self):
        if not global_data.battle:
            return
        global_data.battle.request_pve_battle_info()

    def update_level_info(self, info):
        if not info:
            return
        else:
            start_ts = info['battle_start_ts']
            story_time = info['read_story_time']
            ret_dur = get_server_time() - start_ts - story_time
            info['ret_dur'] = tutils.get_delta_time_str(ret_dur)
            self.init_ts = ret_dur
            self.panel.StopTimerActionByTag(self.TS_TAG)
            self.panel.TimerActionByTag(self.TS_TAG, self.tick_ts, 3600, None, 1)
            self.panel.list_data.SetInitCount(len(self.INFO))
            for idx, ui_item in enumerate(self.panel.list_data.GetAllItem()):
                text_id, key = self.INFO[idx]
                ui_item.lab_info.SetString(get_text_by_id(text_id))
                ui_item.lab_data.SetString(str(info.get(key, '')))

            for extra_info in self.EXTRA_INFO:
                text_id, template_path, handler_attr = extra_info
                ui_item = self.panel.list_data.AddItem(global_data.uisystem.load_template(template_path))
                ui_item.lab_info.SetString(get_text_by_id(text_id))
                handler = getattr(self, handler_attr, None)
                handler and handler(ui_item)

            teammate_info = info.get('teammate_info', {})
            if global_data.player:
                my_player_info = teammate_info.get(global_data.player.id)
                if my_player_info:
                    self.my_pve_mecha_info = my_player_info.get('pve_mecha_base_info')
            if self.is_multi_player_team:
                self.bless_donate_left_cnt = info.get('bless_donate_left_cnt', 0)
                if teammate_info:
                    self.init_team_info(teammate_info)
            return

    def get_element_info(self, ui_item):
        if not global_data.player or not global_data.player.logic:
            self.panel.list_data.DeleteItem(ui_item)
            return
        bless_data = global_data.player.logic.ev_g_choosed_blesses()
        bless_keys = list(bless_data.keys())
        set_elems_icon_list_by_bless(ui_item.list_elements, bless_keys)

    def tick_ts(self, *args):
        self.init_ts += 1
        ret_dur = tutils.get_delta_time_str(self.init_ts)
        self.panel.list_data.GetItem(0).lab_data.SetString(ret_dur)

    def init_team_info(self, teammate_info):
        game_info = {}
        if global_data.battle:
            level = global_data.battle.get_cur_pve_level()
            main_level, sub_level = level
            game_info['chapter'] = main_level
            game_info['end_level'] = sub_level
            game_info['difficulty'] = global_data.battle.get_cur_pve_difficulty()
            game_info['bless_donate_left_cnt'] = self.bless_donate_left_cnt
        if not self.team_info_widget:
            self.team_info_widget = PVETeamStatisticsWidget(self.panel.nd_content.nd_team.temp_team_data, teammate_info, game_info)
        else:
            self.team_info_widget.update_info_widget(teammate_info, game_info)

    def init_break(self):
        ui_list = self.panel.list_breakthrough
        ui_list.DeleteAllSubItem()
        ui_list.SetInitCount(len(self.break_conf))
        break_data = global_data.player.logic.ev_g_mecha_breakthrough_data()
        break_slot_list = list(break_data.keys())
        for idx, ui_item in enumerate(ui_list.GetAllItem()):
            if idx < len(break_data):
                ui_item.nd_skill.setVisible(True)
                ui_item.nd_empty.setVisible(False)
                slot = break_slot_list[idx]
                level = break_data[slot]
                slot_conf = self.break_conf[str(slot)]
                conf = slot_conf[str(level)]
                ui_item.img_item.SetDisplayFrameByPath('', conf['icon'])
                ui_item.lab_name_skill.SetString(get_text_by_id(conf['name_id']))
                for i, btn in enumerate(ui_item.list_dot.GetAllItem()):
                    if i < level:
                        btn.SetSelect(True)
                    else:
                        break

                @ui_item.bar.unique_callback()
                def OnClick(_layer, _touch, _slot=slot, _level=level):
                    print 'break click'
                    if not self.break_widget:
                        return
                    if self.bless_widget.isVisible():
                        self.bless_widget.setVisible(False)
                    if self.item_widget.isVisible():
                        self.item_widget.setVisible(False)
                    self.break_widget.update_widget(self.mecha_id, _slot, _level, pve_mecha_base_info={})

            else:
                ui_item.nd_skill.setVisible(False)
                ui_item.nd_empty.setVisible(True)

    def init_bless(self):
        self.bless_data = global_data.player.logic.ev_g_choosed_blesses()
        self.bless_keys = list(self.bless_data.keys())
        self.bless_keys.sort()
        self.panel.nd_content.nd_personal.bar_energy.nd_empry.setVisible(len(self.bless_keys) == 0)
        self.clear_async_action()
        ui_list = self.panel.list_energy
        ui_list.RecycleAllItem()
        self._create_idx = 0
        self._async_action = self.panel.runAction(cc.RepeatForever.create(cc.Sequence.create([
         cc.DelayTime.create(0.03),
         cc.CallFunc.create(self.create_bless_item)])))

    def clear_async_action(self):
        self._create_idx = 0
        if self._async_action is not None:
            self.panel.stopAction(self._async_action)
            self._async_action = None
        return

    def create_bless_item(self):
        start_time = time.time()
        while self._create_idx < len(self.bless_keys):
            if not global_data.player or not global_data.player.logic:
                continue
            bless_id = self.bless_keys[self._create_idx]
            bless_conf = self.bless_conf.get(str(bless_id))
            if not bless_conf:
                self._create_idx += 1
                continue
            bless_item = self.panel.list_energy.ReuseItem(bRefresh=True)
            if not bless_item:
                bless_item = self.panel.list_energy.AddTemplateItem(bRefresh=True)
            bless_item.lab_name.SetString(get_text_by_id(bless_conf['name_id']))
            bless_item.img_item.SetDisplayFrameByPath('', bless_conf.get('icon', ''))
            cur_level = global_data.player.logic.ev_g_bless_level(bless_id)
            max_level = bless_conf.get('max_level', 1)
            if max_level == 1:
                bless_item.lab_level.setVisible(False)
                bless_item.icon.setVisible(True)
            else:
                bless_item.lab_level.setVisible(True)
                bless_item.icon.setVisible(False)
                bless_item.lab_level.SetString(str(cur_level))
            elem_id = bless_conf.get('elem_id', None)
            if elem_id:
                elem_icon, elem_pnl = get_bless_elem_res(elem_id, ['icon', 'bar'])
                bless_item.icon.SetDisplayFrameByPath('', elem_icon)
                bless_item.bar.SetDisplayFrameByPath('', elem_pnl)
            else:
                bless_item.bar.SetDisplayFrameByPath('', DEFAULT_BLESS_BAR)

            @bless_item.btn_energy.unique_callback()
            def OnClick(_layer, _touch, _bless_id=bless_id, cur_level=cur_level):
                print 'bless click'
                if not self.bless_widget:
                    return
                if self.break_widget.isVisible():
                    self.break_widget.setVisible(False)
                if self.item_widget.isVisible():
                    self.item_widget.setVisible(False)
                pve_mecha_base_info = {}
                if self.my_pve_mecha_info:
                    pve_mecha_base_info = self.my_pve_mecha_info
                self.bless_widget.update_widget(_bless_id, cur_level, pve_mecha_base_info, self.bless_donate_left_cnt)

            self._create_idx += 1
            if time.time() - start_time > 0.015:
                return

        self.clear_async_action()
        return

    def init_item(self):
        ui_list = self.panel.list_mod
        ui_list.DeleteAllSubItem()
        item_set = list(global_data.player.logic.ev_g_pve_item_set())
        self.panel.nd_content.nd_personal.bar_mod.nd_empry.setVisible(len(item_set) == 0)
        ui_list.SetInitCount(len(item_set))
        for idx, ui_item in enumerate(ui_list.GetAllItem()):
            item_id = item_set[idx]
            conf = self.item_conf.get(str(item_id))
            ui_item.lab_name.SetString(get_text_by_id(conf['name_id']))
            ui_item.img_item.SetDisplayFrameByPath('', conf['icon'])
            ui_item.bar_tag.setVisible(bool(conf.get('repeat_refresh', 0)))

            @ui_item.btn_item.unique_callback()
            def OnClick(_layer, _touch, _conf=conf):
                if not self.item_widget:
                    return
                if self.break_widget.isVisible():
                    self.break_widget.setVisible(False)
                if self.bless_widget.isVisible():
                    self.bless_widget.setVisible(False)
                self.item_widget.update_widget(_conf)

    def init_widget(self):
        self.empty_widget = global_data.uisystem.load_template_create(EMPTY_WIDGET_PATH, self.panel)

        @self.empty_widget.nd_empty.unique_callback()
        def OnClick(*args):
            self.on_click_empty(*args)

        self.empty_widget.nd_empty.set_sound_enable(False)
        self.break_widget = PVEBreakWidget(self.panel)
        self.break_widget.setVisible(False)
        self.bless_widget = PVEBlessWidget(self.panel)
        self.bless_widget.setVisible(False)
        self.item_widget = PVEItemWidget(self.panel)
        self.item_widget.setVisible(False)

    def is_appeared(self):
        return not self._other_ui_visible

    def appear(self):
        self.clear_show_count_dict()
        self.set_other_ui_visible(False)

    def disappear(self):
        self.set_other_ui_visible(True)
        self.close()

    def on_click_close_btn(self, *args):
        self.disappear()
        self.close()

    def on_click_empty(self, *args):
        self.break_widget and self.break_widget.setVisible(False)
        self.bless_widget and self.bless_widget.setVisible(False)
        self.item_widget and self.item_widget.setVisible(False)

    def get_block_ui_list(self):
        import copy
        from common.uisys import basepanel
        block_ui_list = copy.deepcopy(basepanel.MECHA_AIM_UI_LSIT)
        block_ui_list.append('StateChangeUI')
        return block_ui_list

    def set_other_ui_visible(self, visible):
        if self._other_ui_visible == visible:
            return
        self._other_ui_visible = visible
        if not visible:
            self.add_blocking_ui_list(self.get_block_ui_list())
            self.hide_main_ui(exceptions=self.EXCEPT_HIDE_UI_LIST, exception_types=(UI_TYPE_MESSAGE,))
        else:
            self.remove_blocking_ui_list()
            self.show_main_ui()
        ui = global_data.ui_mgr.get_ui('FightLeftShotUI')
        if ui:
            if not visible:
                ui.hide_aim_one_shot_button()
            else:
                ui.check_left_fire_ope()