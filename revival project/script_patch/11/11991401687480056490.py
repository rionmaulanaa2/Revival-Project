# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/gvg/GVGChooseMecha.py
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

class CMechaBtn(object):

    def __init__(self, parent_panel, id):
        self.parent_panel = parent_panel
        self.select_id = id
        self.btn_nds = {}
        self.btn_cbs = {}
        self.init_parameters()

    def destroy(self):
        for nd in six.itervalues(self.btn_nds):
            if nd.getParent():
                nd.Destroy()
            else:
                nd.release()

        self.parent_panel = None
        self.select_id = 0
        self.btn_nds = {}
        self.btn_cbs = {}
        return

    def open_ui(self):
        for k in ['normal_nd', 'unable_nd']:
            if k in self.btn_nds:
                self.btn_nds[k].PlayAnimation('open')

    def init_parameters(self):
        self.nd_template_path = {'normal_nd': 'battle_mech/i_mech_item_active','select_nd': 'battle_mech/i_mech_item_sel','unable_nd': 'battle_mech/i_mech_item_lock'
           }
        self.select = False
        self.enable = True
        self.mecha_conf = confmgr.get('mecha_conf', 'UIConfig', 'Content')
        self.mecha_id = 8001
        self._limited_free = False

    def set_mecha_btn_data(self, mecha_id, is_owned):
        self.mecha_id = mecha_id
        self.is_owned = is_owned
        from logic.gcommon.cdata.limited_time_free_mecha_data import is_mecha_limited_free_now_by_mecha_id
        free_now = is_mecha_limited_free_now_by_mecha_id(mecha_id)
        self._limited_free = free_now
        conf = self.mecha_conf.get(str(mecha_id), {})
        icon_path = conf.get('icon_path', [])
        for nd in six.itervalues(self.btn_nds):
            if mecha_id > 0:
                nd.img_mech_icon.setVisible(True)
                nd.img_mech_icon.SetDisplayFrameByPath('', icon_path[0])
            else:
                nd.img_mech_icon.setVisible(False)
            if nd.nd_mode_tips:
                nd.nd_mode_tips.setVisible(free_now)

        self.update_mecha_state()

    def set_mecha_btn_chosen(self, is_chosen):
        self.set_enable(not is_chosen)
        if 'unable_nd' in self.btn_nds:
            self.btn_nds['unable_nd'].icon_lock.setVisible(not is_chosen)

    def update_mecha_state(self):
        self.set_enable(self.is_owned)

    def set_select(self, select):
        if select:
            self.creat_btn_nd('select_nd')
        else:
            self.creat_btn_nd('normal_nd')
        if not self.enable:
            return
        if self.select == select:
            return
        self.select = select
        ruler = {'normal_nd': not select,'select_nd': select,
           'unable_nd': False
           }
        for k, nd in six.iteritems(self.btn_nds):
            nd.setVisible(ruler.get(k, False))

    def set_enable(self, enable):
        if enable:
            self.creat_btn_nd('normal_nd')
        else:
            self.creat_btn_nd('unable_nd')
        if self.enable == enable:
            return
        self.enable = enable
        ruler = {'normal_nd': enable,'select_nd': False,
           'unable_nd': not enable
           }
        for k, nd in six.iteritems(self.btn_nds):
            nd.setVisible(ruler.get(k, False))

    def set_unique_callback(self, nd_type, cb):
        self.btn_cbs[nd_type] = cb

    def creat_btn_nd(self, nd_type):
        if not self.parent_panel:
            return
        if nd_type not in self.btn_nds and nd_type in self.nd_template_path:
            nd = global_data.uisystem.load_template_create(self.nd_template_path[nd_type], self.parent_panel)
            nd.btn_item.set_click_sound_name2('ui_gvg_mecha_click')
            if self.mecha_id > 0:
                conf = self.mecha_conf[str(self.mecha_id)]
                icon_path = conf.get('icon_path', [])
                nd.img_mech_icon.SetDisplayFrameByPath('', icon_path[0])
                nd.img_mech_icon.setVisible(True)
            else:
                nd.img_mech_icon.setVisible(False)
            if nd.nd_mode_tips:
                nd.nd_mode_tips.setVisible(self._limited_free)
            self.btn_nds[nd_type] = nd

            @nd.btn_item.unique_callback()
            def OnClick(btn, touch, nd_type=nd_type, select_id=self.select_id):
                cb = self.btn_cbs.get(nd_type)
                cb and cb(select_id)

    def get_btn_nd(self, nd_type):
        return self.btn_nds.get(nd_type)

    def add_btn_type(self, nd_type, nd_template_path):
        self.nd_template_path[nd_type] = nd_template_path

    def show_btn_type(self, nd_type, vis):
        self.creat_btn_nd(nd_type)
        for k, nd in six.iteritems(self.btn_nds):
            nd.setVisible(False)

        nd = self.get_btn_nd(nd_type)
        if nd:
            nd.setVisible(vis)


MECHA_ITEM_TEMPLATE = ('battle_gvg/i_gvg_choose_mech_blue', 'battle_gvg/i_gvg_choose_mech_red',
                       'battle_gvg/i_gvg_choose_mech_blue_me')
from common.const import uiconst
MECHA_START_ITEM_TEMPLATE = ('battle_gvg/i_gvg_start_mech_blue', 'battle_gvg/i_gvg_start_mech_red',
                             'battle_gvg/i_gvg_start_mech_blue_me')

class GVGChooseMecha(BasePanel):
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_CUSTOM
    PANEL_CONFIG_NAME = 'battle_gvg/gvg_choose_mech'
    UI_ACTION_EVENT = {'btn_sure.OnClick': 'on_btn_call'
       }

    def ui_vkb_custom_func(self):
        return True

    def on_init_panel(self):
        if global_data.video_player:
            global_data.video_player.force_stop_video()
        self.init_parameters()
        self.process_event(True)
        self.init_display()
        self.target_eid = global_data.is_judge_ob or global_data.player.id if 1 else global_data.player.get_global_spectate_player_id()
        self.hide()
        if global_data.is_judge_ob:
            self.panel.btn_sure.setVisible(False)
            self.panel.lab_time_details.setVisible(False)
            self.panel.lab_first_player_name.setVisible(True)
            self.panel.lab_first_player_name.setString('')

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'refresh_choose_mecha': self.refresh_choose_mecha,
           'refresh_confirm_choose_mecha': self.refresh_confirm_choose_mecha,
           'refresh_start_new_round': self.refresh_start_new_round,
           'choose_mecha_finished': self.choose_mecha_finished
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def enter_choose_mecha(self):
        self.init_battle_data()
        self.init_choose_mecha_widget()
        self.init_players_widget()
        self.show()
        self.panel.PlayAnimation('show')
        bat = self.get_battle()
        mecha_id = self.get_mecha_choose_dict().get(self.target_eid, {}).get(bat.cur_round)
        select_id = mecha_id or self.select_id
        self.set_mecha_btn_select(select_id)
        self.choose_mecha_finished()
        global_data.sound_mgr.play_music('gvg_pre')
        global_data.sound_mgr.play_ui_sound('ui_gvg_mecha_select')
        global_data.sound_mgr.play_sound_2d('Play_ui_notice', ('ui_notice', 'medal_flight'))
        global_data.ui_mgr.add_ui_show_whitelist(['GVGChooseMecha', 'NormalConfirmUI2'], 'GVGChooseMecha')
        global_data.ui_mgr.remove_ui_show_whitelist('GVGReadyUI')
        if global_data.is_judge_ob:
            self.panel.img_blue_team_name.setVisible(True)
            self.panel.img_red_team_name.setVisible(True)
            self.panel.lab_first_player_name.setVisible(True)
            bat = global_data.battle
            if bat and global_data.player:
                eid = global_data.player.get_global_spectate_player_id()
                group_data = bat.group_data
                group_id = bat.eid_to_group_id[eid]
                name = group_data[group_id][eid]['char_name']
                self.panel.lab_first_player_name.SetString(name)
                team_names = bat.get_competition_team_names()
                self.panel.lab_blue_team_name.SetString(team_names.get(bat.my_group, ''))
                self.panel.lab_red_team_name.SetString(team_names.get(bat.other_group, ''))

    def on_finalize_panel(self):
        self.process_event(False)
        for mecha_btn in six.itervalues(self.mecha_btn):
            mecha_btn.destroy()

        self.mecha_btn = {}
        self.get_bg_ui() and self.get_bg_ui().close()
        self.bg_ui = None
        global_data.ui_mgr.remove_ui_show_whitelist('GVGChooseMecha')
        return

    def get_battle(self):
        return global_data.battle

    def init_parameters(self):
        self.mecha_list_nd = (
         self.panel.list_mech_blue, self.panel.list_mech_red)
        self.mecha_list_start_nd = (self.panel.list_start_blue, self.panel.list_start_red)
        self.choose_finished_timer = None
        self.bg_ui = None
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
        mecha_open_order = result.get('opened_order', [])
        mecha_closed = []
        for mecha_id in mecha_open_order:
            if self._has_mecha(mecha_id):
                self.mecha_order.append(mecha_id)
            else:
                mecha_closed.append(mecha_id)

        self.mecha_order.extend(mecha_closed)

    def init_display(self):

        @self.panel.nd_touch.unique_callback()
        def OnDrag(btn, touch):
            delta_pos = touch.getDelta()
            global_data.emgr.rotate_model_display.emit(-delta_pos.x / lobby_model_display_const.ROTATE_FACTOR)

    def get_bg_ui(self):
        if self.bg_ui and self.bg_ui.is_valid():
            return self.bg_ui

    def do_hide_panel(self):
        super(GVGChooseMecha, self).do_hide_panel()
        self.get_bg_ui() and self.get_bg_ui().setVisible(False)

    def do_show_panel(self):
        super(GVGChooseMecha, self).do_show_panel()
        self.get_bg_ui() and self.get_bg_ui().setVisible(True)

    def init_players_widget(self):
        bat = self.get_battle()
        map_name_text_ids = self.map_conf.get('cMapNameTextIds', [])
        prefix_str = ''
        if len(map_name_text_ids) > 1 and global_data.battle and hasattr(global_data.battle, 'area_id'):
            text_id_index = min(int(global_data.battle.area_id), len(map_name_text_ids)) - 1
            prefix_str = '\xe2\x80\x94'
        self.panel.lab_map_name.setVisible(bool(prefix_str))
        self.panel.lab_map_name.SetString(''.join([prefix_str, get_text_by_id(map_name_text_ids[text_id_index])]))
        self.refresh_start_new_round(bat.cur_round, bat.round_end_ts, is_need_refresh_mecha=False)

    def is_confirm(self):
        bat = self.get_battle()
        if bat:
            self.is_gvg_confirm = bat.is_confirm
        return self.is_gvg_confirm

    def get_mecha_choose_dict(self):
        bat = self.get_battle()
        if bat:
            self.mecha_choose_dict = bat.mecha_choose_dict
        return self.mecha_choose_dict

    def init_choose_mecha_widget(self):
        bat = self.get_battle()
        self.check_sure_btn()
        for nd in self.mecha_list_nd:
            nd.DeleteAllSubItem()

        for nd in self.mecha_list_start_nd:
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
                start_item_template = global_data.uisystem.load_template(MECHA_START_ITEM_TEMPLATE[template_index])
                start_list_nd = self.mecha_list_start_nd[template_index]
                start_item_widget = global_data.uisystem.create_item(start_item_template)
                start_list_nd.AddControl(start_item_widget)
                self.set_mecha_item(eid, item_widget, start_item_widget)
            for round_id in range(3):
                round_id += 1
                mecha_id = self.get_mecha_choose_dict().get(eid, {}).get(round_id)
                self.refresh_choose_mecha_node(round_id, item_widget, start_item_widget, mecha_id, eid)

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

            start_item_template = global_data.uisystem.load_template(MECHA_START_ITEM_TEMPLATE[-1])
            start_list_nd = self.mecha_list_start_nd[0]
            start_item_widget = global_data.uisystem.create_item(start_item_template)
            start_list_nd.AddControl(start_item_widget)
            item_widget.PlayAnimation('continue')
            self.set_mecha_item(bat.observed_target_id, item_widget, start_item_widget)
        for round_id in range(3):
            round_id += 1
            mecha_id = self.get_mecha_choose_dict().get(bat.observed_target_id, {}).get(round_id)
            self.refresh_choose_mecha_node(round_id, item_widget, start_item_widget, mecha_id, bat.observed_target_id)

        for soul_id in bat.confirm_set:
            self.refresh_confirm_choose_mecha(soul_id)

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

    def set_mecha_item(self, eid, item_widget, start_widget):
        group_id = self.eid_to_group_id[eid]
        name = self.group_data[group_id][eid]['char_name']
        player_mech_lab_node = item_widget.player_mech.lab_player_name
        start_player_lab_node = start_widget.nd_start_player.lab_player_name
        player_mech_lab_node.SetString(name)
        start_player_lab_node.SetString(name)

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
        own = self._has_mecha(mecha_id)
        btn.set_mecha_btn_data(mecha_id, own)
        if not global_data.is_judge_ob:
            btn.set_unique_callback('normal_nd', self.set_mecha_btn_select)
        if self.select_id and self.select_id == mecha_id:
            btn.set_select(True)
        self.set_mecha_chosen(self.get_round_id_by_mecha_id(mecha_id))

    def set_mecha_btn_select(self, select_id):
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
            bat and bat.request_choose_mecha(bat.cur_round, select_id)
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
            self.panel.img_score_bg.lab_time.SetString('%.2ds' % left_time)
            self.panel.img_score_bg.lab_time_vx.SetString('%.2ds' % left_time)

        def refresh_time_finsh():
            self.panel.img_score_bg.lab_time.SetString('00s')
            self.panel.img_score_bg.lab_time_vx.SetString('00s')

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

    def get_list_start_node(self, eid):
        index = self.get_list_template_index(eid)
        return self.mecha_list_start_nd[index]

    def refresh_confirm_choose_mecha(self, soul_id):
        bat = self.get_battle()
        if not bat.is_friend_group(soul_id):
            return
        else:
            node_index = self.get_list_node_index(soul_id)
            mecha_lst_node = self.get_list_node(soul_id)
            lst_node = mecha_lst_node.GetItem(node_index).mech_list
            round_idx = bat.cur_round
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
            return

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
        mecha_lst_node = self.get_list_start_node(soul_id)
        start_item_widget = mecha_lst_node.GetItem(node_index)
        self.refresh_choose_mecha_node(round_idx, item_widget, start_item_widget, mecha_id, soul_id)

    def refresh_choose_mecha_node(self, round_idx, item_widget, start_item_widget, mecha_id=None, eid=None):
        bat = self.get_battle()
        lst_node = item_widget.mech_list
        cur_index = round_idx - 1
        nd = lst_node.GetItem(cur_index)
        is_choosing = round_idx == bat.cur_round
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
        lst_node = start_item_widget.confirm_list
        nd = lst_node.GetItem(cur_index)
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
        self.panel.lab_time_details.SetString(get_text_by_id(19491).format(n=round_idx))
        revive_time = round_end_ts - time_utility.time()
        self.panel.PlayAnimation('choose_next')
        self.on_count_down(revive_time)
        if is_need_refresh_mecha:
            for eid in self.eids:
                self.refresh_choose_mecha(round_idx, eid)

        self.set_mecha_btn_select(self.get_def_select_id(round_idx))
        self.check_sure_btn()
        self.set_mecha_chosen(round_idx - 1)

    def get_def_select_id(self, round_idx):
        mecha_id = self.usual_mecha_ids[round_idx - 1]
        choosen_mecha_ids = six_ex.values(self.get_mecha_choose_dict().get(self.target_eid, {}))
        if len(choosen_mecha_ids) == round_idx or mecha_id not in choosen_mecha_ids:
            return mecha_id
        mecha_list = list(set(self.usual_mecha_ids) - set(choosen_mecha_ids))
        if mecha_list:
            return choice(list(set(self.usual_mecha_ids) - set(choosen_mecha_ids)))

    def on_btn_call(self, *args):
        bat = self.get_battle()
        if bat:
            bat.confirm_choose_mecha(bat.cur_round)
            self.SetConfirmEnable(False)

    def SetConfirmEnable(self, enable):
        self.panel.btn_sure.SetEnable(enable)
        self.panel.btn_sure.SetText(80436 if enable else 18235)

    def choose_mecha_finished(self):
        bat = self.get_battle()
        if bat.choose_finished:
            global_data.emgr.change_model_display_scene_item.emit(None)
        return

    def check_sure_btn(self):
        self.SetConfirmEnable(bool(not self.is_confirm() and self.select_id))

    def get_round_id_by_mecha_id(self, mecha_id):
        for round_id, choose_mecha_id in six.iteritems(self.get_mecha_choose_dict().get(self.target_eid, {})):
            if mecha_id == choose_mecha_id:
                return round_id

    def set_mecha_chosen(self, round_idx):
        if not round_idx:
            return
        bat = self.get_battle()
        if bat.cur_round == round_idx:
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