# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Clone/CloneLoadingUI.py
from __future__ import absolute_import
import six
from six.moves import zip
from six.moves import range
from common.uisys.basepanel import BasePanel
from common.const import uiconst
from common.cfg import confmgr
from logic.gutils import dress_utils, item_utils
from logic.gcommon.item import item_const
import cc
PLAYER_HEAD_DELAY = 0.35
PLAYER_HEAD_INTERVAL = 0.06
PROGRESS_BAR_DELAY = 0.11

class CloneLoadingUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_clone/clone_loading'
    DLG_ZORDER = uiconst.DIALOG_LAYER_BAN_ZORDER
    IS_FULLSCREEN = True
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT

    def on_init_panel(self, *args, **kwargs):
        self.init_parameter()
        self.action_list = [
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('show')),
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('loop')),
         cc.DelayTime.create(PLAYER_HEAD_DELAY)]
        self.init_widget()
        self.create_head_animation_seq()

    def on_finalize_panel(self):
        pass

    def init_parameter(self):
        battle = global_data.battle
        if battle:
            self.group_data = battle.group_data
            self.mecha_use_dict = battle.mecha_use_dict
            self.group_mecha_fashion = battle.group_mecha_fashion
            self.my_group = battle.my_group
            if global_data.player.is_in_global_spectate():
                spectate_obj_id = global_data.player.get_global_spectate_player_id()
                self.my_group = battle.eid_2_group_id[spectate_obj_id]
        else:
            self.group_data = {}
            self.mecha_use_dict = {}
            self.group_mecha_fashion = {}
            self.my_group = -1

    def set_progress_widget(self, widget):
        self.action_list.extend([
         cc.DelayTime.create(PROGRESS_BAR_DELAY),
         cc.CallFunc.create(lambda : widget.panel.PlayAnimation('show'))])

    def play_animation(self):
        self.panel.runAction(cc.Sequence.create(self.action_list))

    def init_widget(self):
        for i, (group_id, mecha_id) in enumerate(six.iteritems(self.mecha_use_dict)):
            group_conf = self.group_data[group_id]
            mecha_fashion = self.group_mecha_fashion[group_id]
            if group_id == self.my_group:
                self.init_group_info(self.panel.nd_me, group_conf, mecha_fashion, mecha_id, my_group=True)
            else:
                self.init_group_info(self.panel.nd_other, group_conf, mecha_fashion, mecha_id)

    def _select_most_awesome_skin(self, mecha_fashion_dict):
        mem_id = None
        most_awesome = item_const.RARE_DEGREE_0
        for eid, fashion in six.iteritems(mecha_fashion_dict):
            if not fashion:
                continue
            fashion_id = fashion.get(item_const.FASHION_POS_SUIT)
            skin_rare_degree = item_utils.get_item_rare_degree(fashion_id)
            if skin_rare_degree > most_awesome:
                mem_id = eid
                most_awesome = skin_rare_degree

        return mem_id

    def init_group_info(self, group_nd, group_conf, mecha_fashion, mecha_id, my_group=False):
        awesome_mem_id = self._select_most_awesome_skin(mecha_fashion)
        group_nd.nd_team.team_head_list.DeleteAllSubItem()
        group_nd.nd_team.team_head_list.SetInitCount(len(group_conf))
        group_node_list = group_nd.nd_team.team_head_list.GetAllItem()
        for eid, mem_data in six.iteritems(group_conf):
            mem_index = mem_data['index']
            if mem_index == 0:
                _info = group_conf[awesome_mem_id or eid]
                _fashion = mecha_fashion.get(awesome_mem_id or eid, {})
                self.init_big_picture(_info, mecha_id, _fashion, group_nd.nd_name, my_group)
            item = group_node_list[mem_index]
            is_myself = eid == global_data.player.id
            fashion_data = mecha_fashion.get(eid, {})
            self.init_one_head_photo(item, mem_data, mecha_id, fashion_data, mygroup=my_group, myself=is_myself)

    def create_head_animation_seq(self):
        my_group_head_list = self.panel.nd_me.nd_team.team_head_list.GetAllItem()
        my_group_head_list.reverse()
        other_group_head_list = self.panel.nd_other.nd_team.team_head_list.GetAllItem()
        append_cnt = 0
        for my_group_nd, other_group_nd in zip(my_group_head_list, other_group_head_list):
            append_cnt += 1
            my_group_nd.setVisible(False)
            other_group_nd.setVisible(False)
            self.action_list.extend([
             cc.CallFunc.create(lambda nd=my_group_nd: nd.setVisible(True)),
             cc.CallFunc.create(lambda nd=my_group_nd: nd.PlayAnimation('blue')),
             cc.CallFunc.create(lambda nd=other_group_nd: nd.setVisible(True)),
             cc.CallFunc.create(lambda nd=other_group_nd: nd.PlayAnimation('red')),
             cc.DelayTime.create(PLAYER_HEAD_INTERVAL)])

        my_group_list_len = len(my_group_head_list)
        other_group_list_len = len(other_group_head_list)
        if my_group_list_len == other_group_list_len:
            return
        if my_group_list_len > other_group_list_len:
            group_list = my_group_head_list
            ani_name = 'blue'
        else:
            group_list = other_group_head_list
            ani_name = 'red'
        for i in range(append_cnt, len(group_list)):
            nd = group_list[i]
            nd.setVisible(False)
            self.action_list.extend([
             cc.CallFunc.create(lambda nd=nd: nd.setVisible(True)),
             cc.CallFunc.create(lambda nd=nd: nd.PlayAnimation(ani_name)),
             cc.DelayTime.create(PLAYER_HEAD_INTERVAL)])

        self.action_list.pop()

    def init_big_picture(self, mem_info, mecha_id, mecha_fashion, name_nd, my_group):
        if my_group:
            img_nd = self.panel.img_mech if 1 else self.panel.img_mech_other
            mecha_fashion_item_no = mecha_fashion.get(item_const.FASHION_POS_SUIT)
            mecha_fashion_item_no = mecha_fashion_item_no or dress_utils.get_mecha_skin_item_no(mecha_id, -1)
        mecha_name_item = mecha_fashion_item_no
        if item_utils.get_item_rare_degree(mecha_fashion_item_no) == item_const.RARE_DEGREE_0:
            mecha_name_item = dress_utils.battle_id_to_mecha_lobby_id(mecha_id)
        img_path = confmgr.get('mecha_conf', 'SkinConfig', 'Content', str(mecha_fashion_item_no), 'img_path')
        img_nd.SetDisplayFrameByPath('', img_path)
        name_nd.lab_name.SetString(mem_info['char_name'])
        name_nd.lab_name_mech.SetString(item_utils.get_lobby_item_name(mecha_name_item))

    def init_one_head_photo(self, nd, player_info, mecha_id, fashion_data, mygroup=False, myself=False):
        mask_png = 'gui/ui_res_2/battle_clone/clone_blue_kuang_.png' if mygroup else 'gui/ui_res_2/battle_clone/clone_red_kuang.png'
        nd.img_zhezhao.SetDisplayFrameByPath('', mask_png)
        nd.bar.SetDisplayFrameByPath('', 'gui/ui_res_2/battle_clone/clone_blue_di.png')
        fashion_no = fashion_data.get(item_const.FASHION_POS_SUIT) or dress_utils.get_mecha_skin_item_no(mecha_id, -1)
        skin_half_img_path = confmgr.get('mecha_conf', 'SkinConfig', 'Content', str(fashion_no), 'half_img_path')
        nd.img_mech.SetDisplayFrameByPath('', skin_half_img_path)
        nd.lab_name.SetString(player_info['char_name'])
        nd.img_empty.setVisible(False)
        nd.img_ready.setVisible(False)
        nd.img_notready.setVisible(False)
        if myself:
            nd.img_wo.setVisible(True)
            nd.lab_name.SetColor(7471101)