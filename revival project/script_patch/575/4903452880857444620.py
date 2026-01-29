# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/gvg/GVGLoadingUI.py
from __future__ import absolute_import
from __future__ import print_function
from six.moves import range
import copy
from logic.gutils import role_head_utils
from common.cfg import confmgr
import cc
from logic.gutils.template_utils import get_ui_picture_pos_anim

class GVGLoadingUI(object):
    NODE_PATH = [
     {'img_first_mecha': [
                          'img_mecha', 'vx_img_mecha1', 'vx_img_mecha2'],
        'img_bar': 'img_bar_player',
        'lab_name': 'lab_mecha_name',
        'img_mecha_head': [
                         'img_mecha_bar_3', 'img_mecha_bar_2', 'img_mecha_bar_1']
        },
     {'img_first_mecha': [
                          'img_mecha_teamate', 'vx_img_mecha_teamate1', 'vx_img_mecha_teamate2'],
        'img_bar': 'img_bar_teamate',
        'lab_name': 'lab_name_teamate',
        'img_mecha_head': [
                         'img_mecha_bar_3', 'img_mecha_bar_2', 'img_mecha_bar_1']
        },
     {'img_first_mecha': [
                          'img_mecha_enemy2', 'vx_img_mecha_enemy2_1', 'vx_img_mecha_enemy2_2'],
        'img_bar': 'img_bar_enemy_2',
        'lab_name': 'lab_name_enemy_2',
        'img_mecha_head': [
                         'img_mecha_bar_1', 'img_mecha_bar_2', 'img_mecha_bar_3']
        },
     {'img_first_mecha': [
                          'img_mecha_enemy1', 'vx_img_mecha_enemy1_1', 'vx_img_mecha_enemy1_2'],
        'img_bar': 'img_bar_enemy_1',
        'lab_name': 'lab_name_enemy_1',
        'img_mecha_head': [
                         'img_mecha_bar_1', 'img_mecha_bar_2', 'img_mecha_bar_3']
        }]

    def __init__(self, panel):
        self.panel = panel
        self.spectate_player_id = None
        return

    def on_init_panel(self, *args, **kwargs):
        if not global_data.battle:
            return
        self.init_parameter()
        self.init_widget()
        self.play_animation()

    def play_animation(self):
        self.panel.PlayAnimation('show_bg')
        for i in range(len(self.sorted_eids)):
            if self.sorted_eids[i] is not None:
                print(self.sorted_eids[i], 'show_%d' % (i + 1))
                self.panel.PlayAnimation('show_%d' % (i + 1))

        self.panel.PlayAnimation('arrow_loop')
        self.panel.PlayAnimation('fire_loop')
        return

    def init_parameter(self):
        battle = global_data.battle
        self.group_data = copy.deepcopy(battle.group_data)
        self.mecha_choose_dict = copy.deepcopy(battle.mecha_choose_dict)
        self.my_group = battle.my_group
        self.other_group = battle.other_group
        self.sorted_eids = copy.deepcopy(battle.eids)
        self.spectate_player_id = global_data.player.get_global_spectate_player_id()
        if self.spectate_player_id is None:
            self.spectate_player_id = global_data.player.id
        if not (global_data.battle and global_data.battle.get_need_preserve_group_sequence()):
            friend = [
             self.spectate_player_id, None]
            enemy = []
            for eid in self.sorted_eids:
                if eid == self.spectate_player_id:
                    continue
                if battle.is_friend_group(eid):
                    friend[1] = eid
                else:
                    enemy.append(eid)

            while len(enemy) < 2:
                enemy.append(None)

            self.sorted_eids = friend + enemy
        else:
            friend = []
            enemy = []
            for eid in self.sorted_eids:
                if battle.is_friend_group(eid):
                    friend.append(eid)
                else:
                    enemy.append(eid)

            while len(enemy) < 2:
                enemy.append(None)

            while len(friend) < 2:
                friend.append(None)

            self.sorted_eids = friend + enemy
        self.eid_2_lab_loading = {}
        return

    def init_widget(self):
        soul_loading_data = global_data.battle.battle_bdict.get('soul_loading_data', {})
        for i in range(4):
            eid = self.sorted_eids[i]
            node_path = self.NODE_PATH[i]
            img_bar = getattr(self.panel, node_path['img_bar'])
            lab_loading = img_bar.img_loading_bar.lab_loading
            name_node = getattr(img_bar, node_path['lab_name'])
            if eid is None:
                char_name = ''
                mecha_choose_dict = {1: 8001,2: 8002,3: 8003}
                mecha_fashion_list = [201800100, 201800200, 201800300]
            else:
                group = self.my_group if global_data.battle.is_friend_group(eid) else self.other_group
                data = self.group_data[group][eid]
                char_name = str(data.get('char_name'))
                mecha_choose_dict = self.mecha_choose_dict[eid]
                mecha_possess_dict = data.get('mecha_dict', None)
                mecha_fashion_list = []
                for idx in range(1, 4):
                    if idx not in mecha_choose_dict:
                        mecha_id = 8001
                    else:
                        mecha_id = mecha_choose_dict[idx]
                    if mecha_possess_dict is None or mecha_possess_dict.get(mecha_id, None) is None:
                        mecha_fashion = '201%d00' % mecha_id
                    else:
                        mecha_fashion = mecha_possess_dict[mecha_id]['fashion']['0']
                    mecha_fashion_list.append(mecha_fashion)

            name_node.setString(char_name)
            lab_loading.setString('%d%%' % soul_loading_data.get(eid, 0))
            self.eid_2_lab_loading[eid] = lab_loading
            icon_path = []
            for idx in range(3):
                icon_path.append('gui/ui_res_2/item/mecha_skin/{}.png'.format(str(mecha_fashion_list[idx])))
                getattr(img_bar, node_path['img_mecha_head'][idx]).cut_mask.img_mecha_head.SetDisplayFrameByPath('', icon_path[idx])

            img_path, anim_name = get_ui_picture_pos_anim(mecha_fashion_list[0])
            for nd_name in node_path['img_first_mecha']:
                node = getattr(self.panel, nd_name)
                if node is None or node.img is None:
                    continue
                node.img.SetDisplayFrameByPath('', img_path)
                anim_name and node.PlayAnimation(anim_name)

        return

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
            lab_loading and lab_loading.setString('%d%%' % value)
            return