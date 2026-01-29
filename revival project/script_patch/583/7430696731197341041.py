# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Duel/DuelChooseMecha.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
from six.moves import range
import six
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER
from logic.client.const import lobby_model_display_const
from logic.gutils import lobby_model_display_utils
from logic.gcommon import time_utility
from common.cfg import confmgr
from logic.gutils import dress_utils
from random import choice
from logic.comsys.battle.gvg.GVGChooseMecha import CMechaBtn
MECHA_ITEM_TEMPLATE = ('battle_gvg/i_gvg_choose_mech_blue', 'battle_gvg/i_gvg_choose_mech_red',
                       'battle_gvg/i_gvg_choose_mech_blue_me')
from common.const import uiconst
EMPTY_SLOT_MECHA_ID = -1

class BanWidget(object):

    def __init__(self, parent, panel):
        self.panel = panel
        self.parent = parent
        self.mecha_ban_dict = {}
        self.mecha_conf = confmgr.get('mecha_conf', 'UIConfig', 'Content')
        self.mecha_ban_list_nd = (
         self.panel.nd_ban_blue.list_mech_ban, self.panel.nd_ban_red.list_mech_ban)
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {}
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def destroy(self):
        self.process_event(False)
        self.mecha_ban_dict = {}
        self.mecha_conf = {}
        self.panel = None
        self.parent = None
        return

    def refresh_start_new_ban(self, round_idx, round_end_ts):
        self.panel.lab_tips.SetString(930036)
        self.panel.lab_status.SetString(930035)
        revive_time = round_end_ts - time_utility.get_server_time()
        self.panel.PlayAnimation('choose_next')
        self.parent.on_count_down(revive_time)
        def_select_id = -1
        self.parent.set_mecha_btn_select(def_select_id)
        self.parent.check_sure_btn()

    def get_ban_list_node_index(self, soul_id):
        return self.parent.get_list_node_index(soul_id)

    def get_ban_list_template_index(self, eid):
        return self.parent.get_list_template_index(eid)

    def get_ban_list_node(self, eid):
        index = self.get_ban_list_template_index(eid)
        return self.mecha_ban_list_nd[index]

    def clear_ban_mecha_list(self):
        for nd in self.mecha_ban_list_nd:
            nd.DeleteAllSubItem()

    def init_ban_mecha_widget(self):
        bat = global_data.battle
        if bat.max_ban_round > 0:
            for ban_list_nd in self.mecha_ban_list_nd:
                ban_list_nd.SetInitCount(bat.max_ban_round)

        for eid in bat.eids:
            if eid in bat.eid_to_group_id:
                template_index = self.get_ban_list_template_index(eid)
                list_nd = self.mecha_ban_list_nd[template_index]
                for round_id in range(bat.max_ban_round):
                    item_widget = list_nd.GetItem(round_id)
                    round_id += 1
                    mecha_id = self.get_mecha_ban_dict().get(eid, {}).get(round_id)
                    self.refresh_ban_mecha_node(round_id, item_widget, mecha_id, eid)

    def refresh_ban_mecha_node(self, round_id, item_widget, mecha_id, eid):
        bat = global_data.battle
        is_choosing = round_id == bat.cur_ban_round and eid not in bat.confirm_set
        print('refresh_ban_mecha_node', round_id, eid, mecha_id, is_choosing, bat.cur_ban_round, bat.is_confirm)
        if not is_choosing:
            item_widget.StopAnimation('choose')
            item_widget.img_mech.setOpacity(255)
            item_widget.frame_choose.setVisible(False)
        else:
            item_widget.frame_choose.setVisible(True)
            item_widget.PlayAnimation('choose')
        self.set_ban_mecha_node(item_widget, mecha_id)

    def set_ban_mecha_node(self, nd, mecha_id):
        nd.mecha_id = mecha_id
        if mecha_id is None or mecha_id <= 0:
            nd.img_mech.setVisible(False)
        else:
            nd.img_mech.setVisible(True)
            conf = self.mecha_conf.get(str(mecha_id), {})
            icon_path = conf.get('icon_path', [])
            nd.img_mech.SetDisplayFrameByPath('', icon_path[0])
        return

    def refresh_ban_mecha(self, round_idx, soul_id, mecha_id):
        print('refresh_ban_mecha', round_idx, soul_id, mecha_id)
        node_index = self.get_ban_list_node_index(soul_id)
        mecha_lst_node = self.get_ban_list_node(soul_id)
        item_widget = mecha_lst_node.GetItem(node_index)
        self.refresh_ban_mecha_node(round_idx, item_widget, mecha_id, soul_id)

    def refresh_confirm_ban_mecha(self, soul_id):
        bat = global_data.battle
        if not bat.is_friend_group(soul_id):
            return
        node_index = self.get_ban_list_node_index(soul_id)
        mecha_lst_node = self.get_ban_list_node(soul_id)
        item_widget = mecha_lst_node.GetItem(node_index)
        round_idx = bat.cur_ban_round
        item_widget.StopAnimation('choose')
        item_widget.frame_choose.setVisible(False)
        mecha_id = self.get_mecha_ban_dict().get(soul_id, {}).get(round_idx)
        self.set_ban_mecha_node(item_widget, mecha_id)
        global_data.sound_mgr.play_ui_sound('ui_gvg_mecha_confirm')

    def set_all_ban_confirmed(self):
        bat = global_data.battle
        for eid in bat.eids:
            if eid in bat.eid_to_group_id:
                template_index = self.get_ban_list_template_index(eid)
                list_nd = self.mecha_ban_list_nd[template_index]
                for round_id in range(bat.max_ban_round):
                    item_widget = list_nd.GetItem(round_id)
                    if not item_widget:
                        continue
                    if item_widget.frame_choose.isVisible():
                        item_widget.StopAnimation('choose')
                        item_widget.img_mech.setOpacity(255)
                        item_widget.frame_choose.setVisible(False)

    def get_mecha_ban_dict(self):
        bat = global_data.battle
        if bat:
            self.mecha_ban_dict = bat.mecha_ban_dict
        return self.mecha_ban_dict

    def get_all_ban_mechas(self):
        all_entity_bans = self.get_mecha_ban_dict() or {}
        all_mecha_bans = []
        for ent_id, ent_round_mecha_dict in six.iteritems(all_entity_bans):
            for round_id, ban_mecha_id in six.iteritems(ent_round_mecha_dict):
                all_mecha_bans.append(ban_mecha_id)

        return all_mecha_bans


class DuelChooseMecha(BasePanel):
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_CUSTOM
    PANEL_CONFIG_NAME = 'battle_duel/battle_duel_choose_main'
    UI_ACTION_EVENT = {'btn_sure.OnClick': 'on_btn_call'
       }

    def ui_vkb_custom_func(self):
        return True

    def on_init_panel(self):
        if global_data.video_player:
            global_data.video_player.force_stop_video()
        self.ban_widget = BanWidget(self, self.panel)
        self.init_parameters()
        self.process_event(True)
        self.init_display()
        self.target_eid = global_data.is_judge_ob or global_data.player.id if 1 else global_data.player.get_global_spectate_player_id()
        self.hide()
        self.panel.btn_sure.EnableCustomState(True)
        if global_data.is_judge_ob:
            self.panel.btn_sure.setVisible(False)
            self.panel.lab_tips.setVisible(False)
            self.panel.lab_first_player_name.setVisible(True)
            self.panel.lab_first_player_name.setString('')

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'refresh_choose_mecha': self.refresh_choose_mecha,
           'refresh_confirm_choose_mecha': self.refresh_confirm_choose_mecha,
           'refresh_start_new_round': self.refresh_start_new_round,
           'choose_mecha_finished': self.choose_mecha_finished,
           'refresh_ban_mecha_event': self.refresh_ban_mecha,
           'refresh_confirm_ban_mecha_event': self.refresh_confirm_ban_mecha,
           'refresh_start_new_ban': self.refresh_start_new_ban,
           'choose_mecha_finished_pre': self.on_choose_mecha_finished_pre
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def refresh_ban_mecha(self, round_idx, soul_id, mecha_id):
        if self.ban_widget:
            self.ban_widget.refresh_ban_mecha(round_idx, soul_id, mecha_id)
        self.check_confirm_tips()

    def refresh_confirm_ban_mecha(self, soul_id):
        if self.ban_widget:
            self.ban_widget.refresh_confirm_ban_mecha(soul_id)
        self.check_confirm_tips()

    def refresh_start_new_ban(self, round_idx, round_end_ts):
        if self.ban_widget:
            self.ban_widget.refresh_start_new_ban(round_idx, round_end_ts)

    def enter_choose_mecha(self):
        self.init_battle_data()
        self.init_ban_mecha_widget()
        self.init_choose_mecha_widget()
        self.init_players_widget()
        self.show()
        self.panel.PlayAnimation('show')
        bat = self.get_battle()
        if not self.is_ban_stage():
            mecha_id = self.get_mecha_choose_dict().get(self.target_eid, {}).get(bat.cur_choose_round)
            select_id = mecha_id or self.select_id
            self.set_mecha_btn_select(select_id)
        else:
            mecha_id = self.ban_widget.get_mecha_ban_dict().get(self.target_eid, {}).get(bat.cur_ban_round)
            select_id = mecha_id or self.select_id
            self.set_mecha_btn_select(select_id)
        self.choose_mecha_finished()
        global_data.sound_mgr.play_music('gvg_pre')
        global_data.sound_mgr.play_ui_sound('ui_gvg_mecha_select')
        global_data.sound_mgr.play_sound_2d('Play_ui_notice', ('ui_notice', 'medal_flight'))
        global_data.ui_mgr.add_ui_show_whitelist(['DuelChooseMecha', 'NormalConfirmUI2'], self.__class__.__name__)
        global_data.ui_mgr.remove_ui_show_whitelist('GVGReadyUI')
        if global_data.is_judge_ob:
            self.panel.lab_first_player_name.setVisible(True)
            bat = global_data.battle
            if bat and global_data.player:
                eid = global_data.player.get_global_spectate_player_id()
                group_data = bat.group_data
                group_id = bat.eid_to_group_id[eid]
                name = group_data[group_id][eid]['char_name']
                self.panel.lab_first_player_name.SetString(name)
                team_names = bat.get_competition_team_names()

    def on_finalize_panel(self):
        if self.ban_widget:
            self.ban_widget.destroy()
            self.ban_widget = None
        self.process_event(False)
        for mecha_btn in six.itervalues(self.mecha_btn):
            mecha_btn.destroy()

        self.mecha_btn = {}
        global_data.ui_mgr.remove_ui_show_whitelist(self.__class__.__name__)
        return

    def get_battle(self):
        return global_data.battle

    def init_parameters(self):
        self.mecha_list_nd = (
         self.panel.list_mech_blue, self.panel.list_mech_red)
        self.choose_finished_timer = None
        self._chosen_mecha_conf = global_data.uisystem.load_template('battle_gvg/i_gvg_pre_mech_role2')
        self._choosing_mecha_conf = global_data.uisystem.load_template('battle_gvg/i_gvg_pre_mech_role1')
        self.select_id = None
        self.mecha_btn = {}
        self.group_data = {}
        self.mecha_order = []
        self.mecha_choose_dict = {}
        self.is_gvg_confirm = False
        self.mecha_conf = confmgr.get('mecha_conf', 'UIConfig', 'Content')
        self.usual_mecha_ids = global_data.player.get_usual_mecha_ids()
        return

    def is_ban_stage(self):
        bat = global_data.battle
        if not bat:
            return False
        else:
            if bat.cur_ban_round <= bat.max_ban_round and bat.cur_choose_round == 0 and bat.choose_round_end_ts == 0:
                return True
            return False

    def init_battle_data(self):
        bat = self.get_battle()
        self.eid_to_group_id = bat.eid_to_group_id
        self.eids = bat.eids
        self.eid_to_index = bat.eid_to_index
        self.map_conf = confmgr.get('map_config', str(bat.map_id), default={})
        self.group_data = bat.group_data
        if global_data.player:
            mecha_open_info = global_data.player.read_mecha_open_info()
            self.update_mecha_info(mecha_open_info)

    def update_mecha_info(self, result):
        self.mecha_order = []
        self.owned_mechas = []
        mecha_open_order = result.get('opened_order', [])
        mecha_closed = []
        for mecha_id in mecha_open_order:
            if self._has_mecha(mecha_id):
                self.mecha_order.append(mecha_id)
                self.owned_mechas.append(mecha_id)
            else:
                mecha_closed.append(mecha_id)

        if not self.is_ban_stage():
            all_ban_mecha = self.ban_widget.get_all_ban_mechas()
            mecha_closed = sorted(mecha_closed, key=lambda x: [x not in all_ban_mecha, x])
        self.mecha_order.extend(mecha_closed)

    def init_display(self):

        @self.panel.nd_touch.unique_callback()
        def OnDrag(btn, touch):
            delta_pos = touch.getDelta()
            global_data.emgr.rotate_model_display.emit(-delta_pos.x / lobby_model_display_const.ROTATE_FACTOR)

    def init_players_widget(self):
        bat = self.get_battle()
        map_name_text_ids = self.map_conf.get('cMapNameTextIds', [])
        prefix_str = ''
        if len(map_name_text_ids) > 1 and global_data.battle and hasattr(global_data.battle, 'area_id'):
            text_id_index = min(int(global_data.battle.area_id), len(map_name_text_ids)) - 1
            prefix_str = '\xe2\x80\x94'
        self.panel.lab_map_name.setVisible(bool(prefix_str))
        self.panel.lab_map_name.SetString(''.join([prefix_str, get_text_by_id(map_name_text_ids[text_id_index])]))
        if self.is_ban_stage():
            self.ban_widget.refresh_start_new_ban(bat.cur_ban_round, bat.ban_round_end_ts)
        else:
            self.refresh_start_new_round(bat.cur_choose_round, bat.choose_round_end_ts, is_need_refresh_mecha=False)

    def is_confirm(self):
        bat = self.get_battle()
        if bat:
            self.is_gvg_confirm = bat.is_confirm or bat.choose_finished
        return self.is_gvg_confirm

    def get_mecha_choose_dict(self):
        bat = self.get_battle()
        if bat:
            self.mecha_choose_dict = bat.mecha_choose_dict
        return self.mecha_choose_dict

    def init_ban_mecha_widget(self):
        bat = self.get_battle()
        self.check_sure_btn()
        if self.ban_widget:
            self.ban_widget.clear_ban_mecha_list()
            self.ban_widget.init_ban_mecha_widget()

    def init_choose_mecha_widget(self):
        bat = self.get_battle()
        self.check_sure_btn()
        for nd in self.mecha_list_nd:
            nd.DeleteAllSubItem()

        need_preserve = global_data.battle and global_data.battle.get_need_preserve_group_sequence()
        for eid in self.eids:
            if bat.is_observed_target_id(eid) and not need_preserve:
                continue
            if eid in self.eid_to_group_id:
                template_index = self.get_list_template_index(eid)
                item_template = global_data.uisystem.load_template(MECHA_ITEM_TEMPLATE[template_index])
                list_nd = self.mecha_list_nd[template_index]
                item_widget = global_data.uisystem.create_item(item_template)
                list_nd.AddControl(item_widget)
                self.set_mecha_item(eid, item_widget)
                for round_id in range(3):
                    round_id += 1
                    mecha_id = self.get_mecha_choose_dict().get(eid, {}).get(round_id)
                    self.refresh_choose_mecha_node(round_id, item_widget, mecha_id, eid)

        if not need_preserve:
            item_template = global_data.uisystem.load_template(MECHA_ITEM_TEMPLATE[-1])
            list_nd = self.mecha_list_nd[0]
            item_widget = global_data.uisystem.create_item(item_template)
            list_nd.AddControl(item_widget)
            item_widget.PlayAnimation('continue')
            for nd in self.mecha_list_nd:
                delay_time = 0
                for widget in nd.GetAllItem():
                    if delay_time:

                        def _cb(widget=widget):
                            widget.PlayAnimation('show')

                        widget.SetTimeOut(delay_time, _cb)
                    else:
                        widget.PlayAnimation('show')
                    delay_time += 0.2

            item_widget.PlayAnimation('continue')
            self.set_mecha_item(bat.observed_target_id, item_widget)
        for round_id in range(3):
            round_id += 1
            mecha_id = self.get_mecha_choose_dict().get(bat.observed_target_id, {}).get(round_id)
            self.refresh_choose_mecha_node(round_id, item_widget, mecha_id, bat.observed_target_id)

        for soul_id in bat.confirm_set:
            self.refresh_confirm_choose_mecha(soul_id)

        self.init_mecha_select_list()

    def check_need_remove_ban_empty_slot(self):
        if not self.is_ban_stage() and EMPTY_SLOT_MECHA_ID in self.mecha_order:
            self.init_mecha_select_list()

    def init_mecha_select_list(self):
        if self.is_ban_stage():
            if EMPTY_SLOT_MECHA_ID not in self.mecha_order:
                self.mecha_order.insert(0, EMPTY_SLOT_MECHA_ID)
        else:
            if EMPTY_SLOT_MECHA_ID in self.mecha_order:
                self.mecha_order.remove(EMPTY_SLOT_MECHA_ID)
            all_ban_mecha = self.ban_widget.get_all_ban_mechas()
            self.mecha_order = sorted(self.mecha_order, key=lambda x: [not self._has_mecha(x), int(not self._has_mecha(x)) * int(x not in all_ban_mecha), x])
        for mecha_btn in six.itervalues(self.mecha_btn):
            mecha_btn.destroy()

        self.mecha_btn = {}
        self.select_id = None
        choose_list_node = self.panel.mech_choose_list

        @choose_list_node.unique_callback()
        def OnCreateItem(lv, index, item_widget):
            self.cb_create_item(index, item_widget)

        choose_list_node.SetInitCount((len(self.mecha_order) + 1) // 2)
        all_items = choose_list_node.GetAllItem()
        for index, widget in enumerate(all_items):
            if type(widget) in [dict, six.text_type, str]:
                continue
            self.cb_create_item(index, widget)

        return

    def set_mecha_item(self, eid, item_widget):
        group_id = self.eid_to_group_id[eid]
        name = self.group_data[group_id][eid]['char_name']
        player_mech_lab_node = item_widget.player_mech.lab_player_name
        player_mech_lab_node.SetString(name)

    def cb_create_item(self, index, item_widget):
        mecha_id_1 = self.mecha_order[index * 2]
        self.set_mecha_btn(item_widget.list_mech_1, mecha_id_1)
        next_index = index * 2 + 1
        if next_index < len(self.mecha_order):
            mecha_id_2 = self.mecha_order[next_index]
            item_widget.list_mech_2.setVisible(True)
            self.set_mecha_btn(item_widget.list_mech_2, mecha_id_2)
        else:
            item_widget.list_mech_2.setVisible(False)

    def set_mecha_btn(self, item_widget, mecha_id):
        if mecha_id not in self.mecha_btn:
            self.mecha_btn[mecha_id] = CMechaBtn(item_widget, mecha_id)
        btn = self.mecha_btn[mecha_id]
        is_ban_stage = self.is_ban_stage()
        own = self._has_mecha(mecha_id)
        btn.set_mecha_btn_data(mecha_id, own or is_ban_stage)
        if self.is_ban_stage():
            btn.add_btn_type('select_nd', 'battle_mech/i_mech_item_ban')
        if not global_data.is_judge_ob:
            btn.set_unique_callback('normal_nd', self.set_mecha_btn_select)
        if self.select_id and self.select_id == mecha_id:
            btn.set_select(True)
        if not self.ban_widget:
            return
        all_mecha_bans = self.ban_widget.get_all_ban_mechas()
        if mecha_id in all_mecha_bans:
            btn.add_btn_type('nd_ban', 'battle_mech/i_mech_item_ban')
            btn.show_btn_type('nd_ban', True)
        else:
            self.set_mecha_chosen(self.get_round_id_by_mecha_id(mecha_id))

    def set_mecha_btn_select(self, select_id):
        if not global_data.battle:
            return
        if self.is_confirm():
            return
        if select_id == self.select_id:
            return
        if select_id:
            btn = self.mecha_btn.get(select_id)
            if btn:
                btn.set_select(True)
                select_nd = btn.get_btn_nd('select_nd')
                select_nd and select_nd.PlayAnimation('choose')
        if self.select_id:
            btn = self.mecha_btn.get(self.select_id)
            if btn:
                btn.set_select(False)
        self.set_mecha_select(select_id)
        self.check_sure_btn()

    def set_mecha_select(self, select_id):
        self.select_id = select_id
        lobby_select_id = None
        if select_id:
            if not global_data.is_judge_ob:
                dressed_clothing_id = dress_utils.get_mecha_dress_clothing_id(select_id)
            else:
                mecha_dict = global_data.player.get_player_info_for_ob(self.target_eid, 'mecha_dict', {})
                dressed_clothing_id = dress_utils.get_ob_mecha_dress_clothing_id(select_id, mecha_dict)
            if dressed_clothing_id is not None:
                lobby_select_id = dressed_clothing_id
            if lobby_select_id is None:
                lobby_select_id = dress_utils.battle_id_to_mecha_lobby_id(select_id)
            bat = self.get_battle()
            if not self.is_ban_stage():
                bat and bat.request_choose_mecha(bat.cur_choose_round, select_id)
            else:
                bat and bat.request_ban_mecha(bat.cur_ban_round, select_id)
        if lobby_select_id is None:
            global_data.emgr.change_model_display_scene_item.emit(None)
        else:
            display_type = lobby_model_display_const.GVG_CHOOSE_MECHA_SCENE
            if lobby_model_display_utils.is_little_mecha(select_id):
                display_type = lobby_model_display_const.GVG_CHOOSE_LITTLE_MECHA_SCENE
            global_data.emgr.set_lobby_scene_display_type.emit(display_type)
            model_data = lobby_model_display_utils.get_lobby_model_data(lobby_select_id, consider_second_model=False)
            if select_id == 8028:
                for data in model_data:
                    data['show_anim'] = data['end_anim']

            global_data.emgr.change_model_display_scene_item.emit(model_data)
        return

    def on_count_down(self, revive_time):

        def refresh_time(pass_time):
            left_time = int(revive_time - pass_time)
            if global_data.battle:
                if self.is_ban_stage():
                    if left_time > 2:
                        if not self.panel.bar_ban.isVisible():
                            self.panel.PlayAnimation('show_tips_ban')
                    if left_time <= 1:
                        if self.panel.bar_ban.isVisible() and not self.panel.IsPlayingAnimation('hide_tips_ban'):
                            self.panel.PlayAnimation('hide_tips_ban')
                else:
                    bat = global_data.battle
                    if self.panel.bar_ban.isVisible() and not self.panel.IsPlayingAnimation('hide_tips_ban'):
                        self.panel.PlayAnimation('hide_tips_ban')
                    if left_time > 2 or bat.cur_choose_round < bat.max_choose_round:
                        if not self.panel.bar_choose.isVisible():
                            self.panel.PlayAnimation('show_tips_choose')
                    if left_time <= 1:
                        if bat.cur_choose_round == bat.max_choose_round:
                            if self.panel.bar_choose.isVisible() and not self.panel.IsPlayingAnimation('hide_tips_choose'):
                                self.panel.PlayAnimation('hide_tips_choose')
            self.panel.nd_choose_mech.lab_time.SetString('%.2ds' % left_time)
            self.panel.nd_choose_mech.lab_time_vx.SetString('%.2ds' % left_time)
            if left_time in (3, 2, 1, 0):
                global_data.sound_mgr.play_ui_sound('ui_gvg_countdown')

        def refresh_time_finsh():
            self.panel.nd_choose_mech.lab_time.SetString('00s')
            self.panel.nd_choose_mech.lab_time_vx.SetString('00s')

        self.panel.StopTimerAction()
        if revive_time <= 0:
            refresh_time_finsh()
            return
        refresh_time(0)
        self.panel.TimerAction(refresh_time, revive_time, callback=refresh_time_finsh, interval=1)

    def get_list_node_index(self, soul_id):
        return self.eid_to_index.get(soul_id, 0)

    def get_list_template_index(self, eid):
        bat = self.get_battle()
        if bat.is_friend_group(eid):
            return 0
        return 1

    def get_list_node(self, eid):
        index = self.get_list_template_index(eid)
        return self.mecha_list_nd[index]

    def refresh_confirm_choose_mecha(self, soul_id):
        bat = self.get_battle()
        if not bat.is_friend_group(soul_id):
            return
        else:
            node_index = self.get_list_node_index(soul_id)
            mecha_lst_node = self.get_list_node(soul_id)
            lst_node = mecha_lst_node.GetItem(node_index).mech_list
            round_idx = bat.cur_choose_round
            cur_index = round_idx - 1
            nd = lst_node.GetItem(cur_index)
            if hasattr(nd, 'is_choosing') and nd.is_choosing:
                mecha_id = None
                if hasattr(nd, 'mecha_id'):
                    mecha_id = nd.mecha_id
                lst_node.DeleteItemIndex(cur_index)
                nd = global_data.uisystem.create_item(self._chosen_mecha_conf)
                lst_node.AddControl(nd, index=cur_index)
                nd.PlayAnimation('confirm')
                global_data.sound_mgr.play_ui_sound('ui_gvg_mecha_confirm')
                self.set_mecha_node(nd, mecha_id)
            self.check_confirm_tips()
            return

    def on_choose_mecha_finished_pre(self, soul_id):
        bat = self.get_battle()
        if not bat.is_friend_group(soul_id):
            return
        round_idx = bat.cur_choose_round
        self.set_mecha_chosen(round_idx)
        self.check_sure_btn()
        self.check_confirm_tips()

    def refresh_choose_mecha(self, round_idx, soul_id, mecha_id=None):
        node_index = self.get_list_node_index(soul_id)
        mecha_lst_node = self.get_list_node(soul_id)
        item_widget = mecha_lst_node.GetItem(node_index)
        lst_node = item_widget.mech_list
        last_index = round_idx - 2
        nd = lst_node.GetItem(last_index)
        if nd and nd.is_choosing:
            last_mecha_id = nd.mecha_id
            lst_node.DeleteItemIndex(last_index)
            new_nd = global_data.uisystem.create_item(self._chosen_mecha_conf)
            new_nd.is_choosing = False
            lst_node.AddControl(new_nd, index=last_index)
            self.set_mecha_node(new_nd, last_mecha_id)
        self.refresh_choose_mecha_node(round_idx, item_widget, mecha_id, soul_id)

    def refresh_choose_mecha_node(self, round_idx, item_widget, mecha_id=None, eid=None):
        bat = self.get_battle()
        lst_node = item_widget.mech_list
        cur_index = round_idx - 1
        nd = lst_node.GetItem(cur_index)
        is_choosing = round_idx == bat.cur_choose_round
        if nd and nd.is_choosing != is_choosing:
            lst_node.DeleteItemIndex(cur_index)
            nd = None
        if not nd:
            nd = global_data.uisystem.create_item(self._choosing_mecha_conf if is_choosing else self._chosen_mecha_conf)
            nd.is_choosing = is_choosing
            lst_node.AddControl(nd, index=cur_index)
        if nd:
            if is_choosing:
                if global_data.is_judge_ob:
                    if eid != self.target_eid:
                        nd.img_frame.setVisible(False)
                        print('shenme shihou yincang de ya ', nd)
        if is_choosing:
            if global_data.is_judge_ob:
                if eid == self.target_eid:
                    self.set_mecha_btn_select(mecha_id)
        self.set_mecha_node(nd, mecha_id)
        return

    def set_mecha_node(self, nd, mecha_id=None):
        nd.mecha_id = mecha_id
        if mecha_id is None:
            nd.img_mech.setVisible(False)
        else:
            nd.img_mech.setVisible(True)
            icon_path = 'gui/ui_res_2/mech_display/img_mech%d.png' % mecha_id
            nd.img_mech.SetDisplayFrameByPath('', icon_path)
        return

    def refresh_start_new_round(self, round_idx, round_end_ts, is_need_refresh_mecha=True):
        self.ban_widget and self.ban_widget.set_all_ban_confirmed()
        self.check_need_remove_ban_empty_slot()
        self.panel.lab_tips.SetString(930038)
        self.panel.lab_status.SetString(930037)
        revive_time = round_end_ts - time_utility.get_server_time()
        self.panel.PlayAnimation('choose_next')
        self.on_count_down(revive_time)
        if is_need_refresh_mecha:
            for eid in self.eids:
                self.refresh_choose_mecha(round_idx, eid)

        self.set_mecha_btn_select(self.get_def_select_id(round_idx))
        self.check_sure_btn()
        self.set_mecha_chosen(round_idx - 1)

    def get_def_select_id(self, round_idx):
        if not self.is_ban_stage():
            all_ban_mechas = self.ban_widget.get_all_ban_mechas()
        else:
            all_ban_mechas = []
        choosen_mecha_ids = six_ex.values(self.get_mecha_choose_dict().get(self.target_eid, {}))
        unusable_mecha_ids = all_ban_mechas + choosen_mecha_ids
        usual_usable_mecha_ids = [ m_id for m_id in self.usual_mecha_ids if m_id not in unusable_mecha_ids ]
        other_mecha_ids = [ m_id for m_id in self.owned_mechas if m_id not in unusable_mecha_ids and m_id not in usual_usable_mecha_ids ]
        usable_mecha_ids = usual_usable_mecha_ids + other_mecha_ids
        if usable_mecha_ids:
            mecha_id = usable_mecha_ids[0]
        else:
            mecha_id = 8001
        if mecha_id not in unusable_mecha_ids:
            return mecha_id
        mecha_list = list(set(self.owned_mechas) - set(unusable_mecha_ids))
        if mecha_list:
            return choice(list(mecha_list))

    def on_btn_call(self, *args):
        bat = self.get_battle()
        if bat:
            if self.is_ban_stage():
                bat.confirm_ban_mecha(bat.cur_ban_round)
            else:
                bat.confirm_choose_mecha(bat.cur_choose_round)
            self.SetConfirmEnable(False)

    def SetConfirmEnable(self, enable):
        self.panel.btn_sure.SetEnable(enable)
        if self.is_ban_stage():
            if enable:
                self.panel.btn_sure.SetSelect(False)
            self.panel.btn_sure.SetText(930046 if enable else 18235)
        else:
            if enable:
                self.panel.btn_sure.SetSelect(True)
            self.panel.btn_sure.SetText(80436 if enable else 18235)

    def check_confirm_tips(self):
        if self.is_confirm():
            if self.is_ban_stage():
                self.panel.lab_tips.SetString(930040)
                self.panel.lab_status.SetString(get_text_by_id(930039))
            else:
                self.panel.lab_tips.SetString(930042)
                self.panel.lab_status.SetString(930041)
        elif self.is_ban_stage():
            self.panel.lab_tips.SetString(930036)
            self.panel.lab_status.SetString(930035)
        else:
            self.panel.lab_tips.SetString(930038)
            self.panel.lab_status.SetString(930037)

    def choose_mecha_finished(self):
        bat = self.get_battle()
        if bat and bat.choose_finished:
            global_data.emgr.change_model_display_scene_item.emit(None)
        return

    def check_sure_btn(self):
        self.SetConfirmEnable(bool(not self.is_confirm() and self.select_id is not None))
        return

    def get_round_id_by_mecha_id(self, mecha_id):
        for round_id, choose_mecha_id in six.iteritems(self.get_mecha_choose_dict().get(self.target_eid, {})):
            if mecha_id == choose_mecha_id:
                return round_id

    def set_mecha_chosen(self, round_idx):
        if not round_idx:
            return
        bat = self.get_battle()
        if bat.cur_choose_round == round_idx:
            return
        mecha_id = self.get_mecha_choose_dict().get(self.target_eid, {}).get(round_idx)
        btn = self.mecha_btn.get(mecha_id)
        btn and btn.set_mecha_btn_chosen(True)

    def _avatar_has_mecha(self, mecha_id):
        bat = self.get_battle()
        if bat:
            return bat.avatar_has_mecha(mecha_id)
        return False

    def _has_mecha(self, mecha_id):
        if not global_data.is_judge_ob:
            return self._avatar_has_mecha(mecha_id)
        else:
            if global_data.player:
                mecha_dict = global_data.player.get_player_info_for_ob(self.target_eid, 'mecha_dict', {})
                return mecha_id in mecha_dict
            return False