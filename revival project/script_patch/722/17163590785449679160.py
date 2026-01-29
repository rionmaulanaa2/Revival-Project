# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Duel/DuelLoadingUI.py
from __future__ import absolute_import
from six.moves import range
import copy
from logic.gutils import role_head_utils
from common.cfg import confmgr
import cc
from logic.gutils.template_utils import get_ui_picture_pos_anim

class DuelLoadingUI(object):
    NODE_PATH = [
     {'img_bar': 'img_bar_blue',
        'lab_name': 'lab_num_blue',
        'img_mecha_head': [
                         'img_mecha_bar_3', 'img_mecha_bar_2', 'img_mecha_bar_1'],
        'lab_num': 'lab_num_blue'
        },
     {'img_bar': 'img_bar_red',
        'lab_name': 'lab_num_red',
        'img_mecha_head': [
                         'img_mecha_bar_3', 'img_mecha_bar_2', 'img_mecha_bar_1'],
        'lab_num': 'lab_num_red'
        }]

    def __init__(self, panel):
        self.panel = panel

    def on_init_panel(self, *args, **kwargs):
        if not global_data.battle:
            return
        self.init_parameter()
        self.init_widget()
        self.play_animation()

    def play_animation(self):
        self.panel.PlayAnimation('show_bg')
        self.panel.PlayAnimation('show')
        self.panel.PlayAnimation('arrow_loop')
        self.panel.PlayAnimation('fire_loop')

    def init_parameter(self):
        battle = global_data.battle
        self.group_data = copy.deepcopy(battle.group_data)
        self.mecha_choose_dict = copy.deepcopy(battle.mecha_choose_dict)
        self.my_group = battle.my_group
        self.other_group = battle.other_group
        self.default_show_role = global_data.battle.get_default_show_role()
        self.sorted_eids = copy.deepcopy(battle.eids)
        self.spectate_player_id = global_data.player.get_global_spectate_player_id()
        if self.spectate_player_id is None:
            self.spectate_player_id = global_data.player.id
        if not (global_data.battle and global_data.battle.get_need_preserve_group_sequence()):
            friend = [
             self.spectate_player_id]
            enemy = []
            for eid in self.sorted_eids:
                if eid == self.spectate_player_id:
                    continue
                if battle.is_friend_group(eid):
                    continue
                    enemy.append(eid)

            self.sorted_eids = friend + enemy
        else:
            friend = []
            enemy = []
            for eid in self.sorted_eids:
                if battle.is_friend_group(eid):
                    friend.append(eid)
                else:
                    enemy.append(eid)

            self.sorted_eids = friend + enemy
        self.eid_2_lab_loading = {}
        return

    def init_widget(self):
        soul_loading_data = global_data.battle.battle_bdict.get('soul_loading_data', {})
        self.panel.list_player.SetInitCount(len(self.sorted_eids))
        for i in range(len(self.sorted_eids)):
            eid = self.sorted_eids[i]
            node_path = self.NODE_PATH[i]
            img_bar = getattr(self.panel, node_path['img_bar'])
            lab_loading = img_bar.img_loading_bar.lab_loading
            name_node = getattr(img_bar, node_path['lab_name'])
            num_node = getattr(img_bar, node_path['lab_num'])
            if eid is None:
                char_name = ''
                mecha_choose_dict = {1: 8001,2: 8002,3: 8003}
                mecha_fashion_list = [201800100, 201800200, 201800300]
                win_num = 0
            else:
                group = self.my_group if global_data.battle.is_friend_group(eid) else self.other_group
                data = self.group_data[group][eid]
                char_name = str(data.get('char_name'))
                mecha_choose_dict = self.mecha_choose_dict.get(eid, [None, None, None, None])
                mecha_possess_dict = data.get('mecha_dict', None)
                mecha_fashion_list = []
                for idx in range(1, 4):
                    mecha_id = mecha_choose_dict[idx] or 8001
                    if mecha_possess_dict is None or mecha_possess_dict.get(mecha_id, None) is None:
                        mecha_fashion = '201%d00' % mecha_id
                    else:
                        mecha_fashion = mecha_possess_dict[mecha_id]['fashion']['0']
                    mecha_fashion_list.append(mecha_fashion)

                win_num = global_data.battle.duel_win_cnt_dict.get(eid, 0)
                player_info = dict(data)
                player_info['role_charm_rank'] = -1
                player_info['mecha_charm_rank'] = -1
                player_info['battle_flag_frame'] = data.get('battle_flag', {}).get('frame', None)
                list_ui_item = self.panel.list_player.GetItem(i)
                list_ui_item.lab_prog.setVisible(False)
                self.init_player_card(eid, player_info, list_ui_item)
            name_node.setString(char_name)
            num_node.setString(get_text_by_id(15024) + ': %d' % win_num)
            lab_loading.setString('%d%%' % soul_loading_data.get(eid, 0))
            self.eid_2_lab_loading[eid] = lab_loading
            icon_path = []
            for idx in range(3):
                icon_path.append('gui/ui_res_2/item/mecha_skin/{}.png'.format(str(mecha_fashion_list[idx])))
                getattr(img_bar, node_path['img_mecha_head'][idx]).cut_mask.img_mecha_head.SetDisplayFrameByPath('', icon_path[idx])

        return

    def init_player_card(self, player_eid, player_info, ui_item):
        from logic.gutils.new_template_utils import init_player_loading_card
        init_player_loading_card(self.panel, player_eid, player_info, ui_item, self.spectate_player_id, self.on_click_player_card, self.default_show_role)

    def on_click_player_card(self, ui_item, role_visible, mecha_visible):
        ui_item.nd_role_locate.setVisible(role_visible)
        ui_item.temp_level_role.nd_kind.setVisible(role_visible)
        ui_item.img_role_charm_level.setVisible(role_visible)
        ui_item.bar_charm_role.setVisible(role_visible)
        ui_item.lab_role_skin_name.setVisible(role_visible)
        ui_item.icon_relation.setVisible(role_visible)
        ui_item.lab_value.setVisible(role_visible)
        ui_item.nd_mech_locate.setVisible(mecha_visible)
        ui_item.temp_level_mecha.nd_kind.setVisible(mecha_visible)
        ui_item.img_mecha_charm_level.setVisible(mecha_visible)
        ui_item.bar_charm_mecha.setVisible(mecha_visible)
        ui_item.lab_mecha_skin_name.setVisible(mecha_visible)
        ui_item.temp_tier.setVisible(mecha_visible)
        if ui_item.temp_level_role.nd_kind.isVisible() and ui_item.temp_level_role.isVisible():
            ui_item.bar_level_bg.setVisible(True)
        elif ui_item.temp_level_mecha.nd_kind.isVisible() and ui_item.temp_level_mecha.isVisible():
            ui_item.bar_level_bg.setVisible(True)
        else:
            ui_item.bar_level_bg.setVisible(False)

    def update_percent(self, value, soul_id=None):
        if not self.panel:
            return
        else:
            if global_data.player is None:
                return
            if soul_id is None:
                if self.spectate_player_id:
                    soul_id = self.spectate_player_id
                else:
                    return
            lab_loading = self.eid_2_lab_loading.get(soul_id, None)
            if soul_id != self.spectate_player_id:
                value = min(value, 99)
            lab_loading and lab_loading.setString('%d%%' % value)
            return

    def hide_loading_percent(self):
        for i in range(len(self.sorted_eids)):
            node_path = self.NODE_PATH[i]
            img_bar = getattr(self.panel, node_path['img_bar'])
            img_bar.img_loading_bar.setScale(0)