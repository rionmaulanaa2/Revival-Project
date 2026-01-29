# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Settle/EndExpUI.py
from __future__ import absolute_import
import six
from six.moves import range
import time
from cocosui import cc
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_1, BG_ZORDER
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.client.const import game_mode_const
from logic.gutils.lv_template_utils import get_lv_upgrade_need_exp, is_full_lv
from common.cfg import confmgr
from logic.gutils import bond_utils
from logic.gcommon.ctypes.BattleReward import Reward, BattleReward
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no, get_lobby_item_name
from logic.gcommon.item.item_const import YUEAKA_EXP_ADD
from logic.gutils.lv_template_utils import init_lv_template
from logic.gutils.dress_utils import battle_id_to_mecha_lobby_id
from logic.gcommon.common_const.statistics_const import HANG_UP, ESCAPE_BATTLE
from logic.gcommon.common_const.battle_const import DEFAULT_GVG_DUAL_TID, DEFAULT_GVG_SINGLE_TID
from logic.gcommon.common_const import activity_const
EXP_DOUBLE_ITEM_NO = 50302011
EXP_YUKA_ITEM_PIC_PATH = 'gui/ui_res_2/main/buff_month_exp_up.png'
EXP_RECRUIT_GROUP_PIC_PATH = 'gui/ui_res_2/fight_end/img_end_exp_friend.png'
EXP_ROLE_PROGRESS_PATH = 'gui/ui_res_2/fight_end/prog_role.png'
PROGRESS_ADD_ALL_TIME = 60.0
PROGRESS_ADD_MIN_TIME = 6.0

def show_role_bond_lv_up(role_id, old_lv, new_lv, close_cb=None):
    data_dict = {'role_id': int(role_id),
       'old_lv': old_lv,
       'new_lv': new_lv,
       'close_cb': close_cb
       }
    ui = global_data.ui_mgr.show_ui('EndRoleLevelUI', 'logic.comsys.battle.Settle')
    ui.play_animation(data_dict)


def show_lv_up--- This code section failed: ---

  45       0  BUILD_MAP_4           4 

  46       3  BUILD_MAP_1           1 
           6  STORE_MAP        

  47       7  LOAD_FAST             1  'old_exp'
          10  LOAD_CONST            2  'old_exp'
          13  STORE_MAP        

  48      14  LOAD_FAST             2  'add_exp'
          17  LOAD_CONST            3  'add_exp'
          20  STORE_MAP        

  49      21  LOAD_FAST             3  'close_cb'
          24  LOAD_CONST            4  'close_cb'
          27  STORE_MAP        
          28  STORE_FAST            4  'data_dict'

  52      31  LOAD_GLOBAL           0  'global_data'
          34  LOAD_ATTR             1  'ui_mgr'
          37  LOAD_ATTR             2  'show_ui'
          40  LOAD_CONST            5  'EndLevelUI'
          43  LOAD_CONST            6  'logic.comsys.battle.Settle'
          46  CALL_FUNCTION_2       2 
          49  STORE_FAST            5  'ui'

  53      52  LOAD_FAST             5  'ui'
          55  LOAD_ATTR             3  'play_animation'
          58  LOAD_FAST             4  'data_dict'
          61  CALL_FUNCTION_1       1 
          64  POP_TOP          

Parse error at or near `STORE_MAP' instruction at offset 6


from common.const import uiconst

class EndExpUI(BasePanel):
    PANEL_CONFIG_NAME = 'end/end_exp'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    MOUSE_CURSOR_TRIGGER_SHOW = True
    TICK_INTERVAL = 0.03
    CLOSE_UI_DELAY = 1
    UI_ACTION_EVENT = {'btn_exit.btn_major.OnClick': 'on_click_btn_exit'
       }

    def on_custom_template_create(self, *args, **kwargs):
        super(EndExpUI, self).on_custom_template_create(*args, **kwargs)

    def on_init_panel(self, settle_dict, reward, settle_exp_dict, finished_cd=None):
        self.exp_decay_percent = 0.0
        self.is_double_exp = False
        self.is_yueka_exp = False
        self.recruit_group_exp_rate = 0
        self.end_callback_list = []
        self.show_end_callback = True
        self.showing_end_callback = False
        self._mecha_ids = []
        self._role_ids = []
        self._prof_conf = confmgr.get('proficiency_config', 'Proficiency')
        self._dan_conf = confmgr.get('proficiency_config', 'ProficiencyDan')
        self._max_level = len(self._prof_conf)
        self._max_dan_lv = len(self._dan_conf)
        show_attention = settle_dict.get(ESCAPE_BATTLE, False) or settle_dict.get('afk', False)
        self.panel.nd_attention and self.panel.nd_attention.setVisible(show_attention)
        is_survivals = global_data.game_mode and global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_SURVIVALS)
        self.panel.btn_help.setVisible(is_survivals)
        self.calculate_exp_data(reward)
        self.show_exp_extra_addition()
        self.show_mecha_exp(settle_dict, reward)
        self.show_role_bond_exp(settle_dict, reward)
        self.show_exp_list(settle_dict, reward)
        self.show_self_exp(settle_exp_dict, finished_cd)
        self.show_reward_items(reward)
        self.show_gold_reward(settle_dict, reward)
        self.show_meow_reward(settle_dict, reward)
        hide_ui_list = [
         'SmallMapUI', 'QuickMarkUI', 'BattleRightTopUI', 'FightBagUI', 'HpInfoUI', 'FightSightUI', 'FightStateUI', 'ScalePlateUI', 'WeaponBarSelectUI', 'BattleFightCapacity', 'FightKillNumberUI', 'RogueGiftTopRightUI', 'DeathRogueGiftTopRightUI', 'BattleFightMeow']
        self.hide_main_ui(hide_ui_list)
        if global_data.battle and global_data.battle.get_battle_tid() in (DEFAULT_GVG_SINGLE_TID, DEFAULT_GVG_DUAL_TID) and global_data.player.is_leader():
            self.panel.btn_again.setVisible(True)

            @self.panel.btn_again.btn_major.unique_callback()
            def OnClick(*args):
                if global_data.player:
                    global_data.player.quit_battle(True)
                    global_data.player.match_again = True
                self.close()

        elif self.panel.btn_again:
            self.panel.btn_again.setVisible(False)
            self.panel.btn_exit.setPosition(self.panel.btn_again.getPosition())

    def calculate_exp_data(self, reward):
        exp_reward = reward.get_reward(BattleReward.EXP_REWARD)
        for exp_type, data in exp_reward.extra_exp:
            if exp_type in (Reward.DUO_EXP_TIME, Reward.DUO_EXP_POINT):
                self.is_double_exp = True
            elif exp_type == Reward.YUEKA_EXP:
                self.is_yueka_exp = True
            elif exp_type == Reward.DECAY_EXP:
                self.exp_decay_percent = data
            elif exp_type == Reward.RECRUIT_RATE:
                self.recruit_group_exp_rate = data

    def on_finalize_panel(self):
        self.show_main_ui()

    def add_end_callback(self, callback, pending):
        old_cb_count = len(self.end_callback_list)
        self.end_callback_list.append([callback, pending])
        if old_cb_count == 0 and not self.showing_end_callback:
            self.exec_end_callback()

    def exec_end_callback(self):
        if not self.show_end_callback:
            return
        if not self.end_callback_list:
            self.showing_end_callback = False
            return
        while self.end_callback_list:
            callback, pending = self.end_callback_list[0]
            self.end_callback_list.pop(0)
            callback()
            self.showing_end_callback = pending
            if pending:
                break

    def _get_dan_lv(self, level):
        dan_lv = 1
        for dan_lv in range(1, self._max_dan_lv + 1):
            max_level = self._dan_conf[str(dan_lv)]['max_level']
            if level < max_level:
                break

        return dan_lv

    def show_exp_extra_addition(self):
        self.panel.lv_exp_plus.DeleteAllSubItem()
        delay_time = 0.5
        if self.is_yueka_exp:
            text = get_text_by_id(23014) + '+{0}%'.format(int(YUEAKA_EXP_ADD * 100))
            self.panel.DelayCall(delay_time, self.add_exp_animation, text, EXP_YUKA_ITEM_PIC_PATH)
            delay_time += 0.6
        if self.is_double_exp:
            text = get_text_by_id(80782) + '+100%'
            self.panel.DelayCall(delay_time, self.add_exp_animation, text, EXP_DOUBLE_ITEM_NO)
            delay_time += 0.6
        if self.recruit_group_exp_rate > 0:
            text = get_text_by_id(400090) + '+{0}%'.format(int(self.recruit_group_exp_rate * 100))
            self.panel.DelayCall(delay_time, self.add_exp_animation, text, EXP_RECRUIT_GROUP_PIC_PATH)
            delay_time += 0.6

    def add_exp_animation(self, text, item_no_or_pic_path):
        panel = self.panel.lv_exp_plus.AddTemplateItem()
        panel.lab_exp_plus.SetString(text)
        if isinstance(item_no_or_pic_path, int):
            pic_path = get_lobby_item_pic_by_item_no(item_no_or_pic_path)
        else:
            pic_path = item_no_or_pic_path
            if item_no_or_pic_path != EXP_RECRUIT_GROUP_PIC_PATH:
                panel.img_exp_plus.setScale(1.7)
        panel.img_exp_plus.SetDisplayFrameByPath('', pic_path)
        panel.PlayAnimation('exp_plus')

    def show_mecha_exp(self, settle_dict, reward):
        created_mecha_ids = settle_dict.get('created_mecha_ids', []) or []
        created_mecha_ids = [ str(cid) for cid in created_mecha_ids ]
        unique_created_mecha_ids = []
        for c_id in created_mecha_ids:
            if c_id not in unique_created_mecha_ids:
                unique_created_mecha_ids.append(c_id)

        self._mecha_ids = [ c_id for c_id in unique_created_mecha_ids if c_id in reward.proficiency ]

    def show_role_bond_exp(self, settle_dict, reward):
        if bond_utils.is_open_bond_sys():
            bond_rewards = reward.bond
            for str_role_id, add_exp in six.iteritems(bond_rewards):
                if add_exp > 0:
                    self._role_ids.append(str_role_id)

    def show_exp_list(self, settle_dict, reward):
        if not self.panel.list_mech:
            return
        mecha_count = len(self._mecha_ids)
        role_count = len(self._role_ids)
        count = mecha_count + role_count
        has_list = True if count > 0 else False
        if self.panel.nd_empty:
            self.panel.nd_empty.setVisible(not has_list)
        nd_list = self.panel.list_mech
        if count >= 5:
            self.panel.list_mech.setVisible(False)
            nd_list = self.panel.list_mech_5more
            self.panel.img_arrow.setVisible(True)
            self.panel.PlayAnimation('arrow')
        nd_list.setVisible(has_list)
        nd_list.SetInitCount(count)
        for idx, mecha_id in enumerate(self._mecha_ids):
            mecha_item = nd_list.GetItem(idx)
            self.init_mecha_exp_item(mecha_item, settle_dict, reward, mecha_id)

        for idx, role_id in enumerate(self._role_ids):
            role_item = nd_list.GetItem(mecha_count + idx)
            self.init_role_exp_item(role_item, settle_dict, reward, role_id)

    def init_mecha_exp_item(self, mech_item, settle_dict, reward, mecha_id):
        mech = mech_item
        nd_prof_lv = mech.nd_proficiency_level
        mech.nd_proficiency_level_human.setVisible(False)
        mech.nd_proficiency_level_human.stopAllActions()
        mech.nd_proficiency_level.setVisible(True)
        lobby_mecha_id = battle_id_to_mecha_lobby_id(int(mecha_id))
        mech.img_mech.SetDisplayFrameByPath('', 'gui/ui_res_2/item/mecha/%d.png' % lobby_mecha_id)
        conf = confmgr.get('mecha_display', 'HangarConfig', 'Content')[str(mecha_id)]
        mecha_name = conf.get('name_mecha_text_id', '')
        mech.lab_mech.SetString(mecha_name)
        proficiency_data = settle_dict.get('proficiency_data', {}).get(str(mecha_id), {})
        lv = proficiency_data.get('level', 1)
        proficiency = proficiency_data.get('proficiency', 0)
        self._update_mech_proficiency_data(mech, lv, proficiency)
        pro_get = reward.proficiency.get(str(mecha_id), 0)
        nd_prof_lv.lab_exp_get.SetString(get_text_by_id(400011) + '+' + str(pro_get))
        upgrade_value = self._get_upgrade_need_value(lv)
        upgraded_exp = proficiency + pro_get
        final_lv, final_prof = self._cal_final_lv_and_proficiency(lv, upgraded_exp)
        cur_prof = proficiency
        upgrade_need_prof = upgrade_value
        cur_lv = lv
        update_info = {'cur_prof': cur_prof,'upgrade_need_prof': upgrade_need_prof,
           'cur_lv': cur_lv
           }
        remain_time = pro_get * EndExpUI.TICK_INTERVAL
        nd_prof_lv.progress_exp.StopTimerAction()

        def finish():
            self._update_mech_proficiency_data(mech, final_lv, final_prof)

        def update_proficiency(t, update_info=update_info):
            cur_prof = update_info['cur_prof']
            cur_lv = update_info['cur_lv']
            upgrade_need_prof = update_info['upgrade_need_prof']
            cur_prof += 1
            if cur_lv == self._max_level:
                if cur_prof > upgrade_need_prof:
                    cur_prof = upgrade_need_prof
            elif cur_prof >= upgrade_need_prof:
                cur_prof -= upgrade_need_prof
                cur_lv += 1
                upgrade_need_prof = self._get_upgrade_need_value(cur_lv)
            self._update_mech_proficiency_data(mech, cur_lv, cur_prof)
            update_info['cur_prof'] = cur_prof
            update_info['cur_lv'] = cur_lv
            update_info['upgrade_need_prof'] = upgrade_need_prof

        nd_prof_lv.progress_exp.TimerAction(update_proficiency, remain_time, callback=finish, interval=EndExpUI.TICK_INTERVAL)

    def _cal_final_lv_and_proficiency(self, cur_lv, cur_proficiency):
        if cur_lv == self._max_level:
            max_need_value = self._get_upgrade_need_value(cur_lv)
            if cur_proficiency >= max_need_value:
                cur_proficiency = max_need_value
            return (cur_lv, cur_proficiency)
        flag = True
        while flag:
            exp = self._get_upgrade_need_value(cur_lv)
            if cur_proficiency >= exp:
                cur_proficiency -= exp
                cur_lv += 1
                if cur_lv == self._max_level:
                    max_need_value = self._get_upgrade_need_value(cur_lv)
                    if cur_proficiency >= max_need_value:
                        cur_proficiency = max_need_value
                    return (cur_lv, cur_proficiency)
            else:
                flag = False

        return (
         cur_lv, cur_proficiency)

    def _get_upgrade_need_value(self, lv):
        if lv < self._max_level:
            return self._prof_conf.get(str(lv + 1), {}).get('upgrade_value', 0)
        else:
            return self._prof_conf.get(str(lv), {}).get('upgrade_value', 0)

    def _update_mech_proficiency_data(self, nd, lv, proficiency):
        upgrade_value = self._get_upgrade_need_value(lv)
        if lv == self._max_level:
            proficiency = upgrade_value
        nd_prof_lv = nd.nd_proficiency_level
        nd_prof_lv.lab_level.SetString('Lv%d' % lv)
        nd_prof_lv.lab_exp_need.SetString('/%d' % upgrade_value)
        nd_prof_lv.lab_exp_need.lab_exp.SetString('%d' % proficiency)
        if upgrade_value:
            nd_prof_lv.progress_exp.SetPercentage(proficiency * 100.0 / upgrade_value)
        else:
            nd_prof_lv.progress_exp.SetPercentage(100)
        dan_lv = self._get_dan_lv(lv)
        icon_path = self._dan_conf.get(str(dan_lv), {}).get('icon_path', '')
        name = self._dan_conf.get(str(dan_lv), {}).get('name', 0)
        if icon_path:
            nd_prof_lv.img_proficiency_level.SetDisplayFrameByPath('', icon_path)

    def show_self_exp(self, settle_exp_dict, finished_cd):
        self._finished_cd = finished_cd
        self._progress_val = 0
        self._old_lv = settle_exp_dict.get('old_lv', 1)
        self._old_exp = settle_exp_dict.get('old_exp', 0)
        self._add_exp = settle_exp_dict.get('add_exp', 0)
        self._updated_lv = self._old_lv
        self._updated_exp = self._old_exp + self._add_exp
        upgrade_need_exp = get_lv_upgrade_need_exp(self._old_lv)
        if self._updated_exp >= upgrade_need_exp:
            self._updated_lv = self._old_lv + 1
            self._show_upgrade()
        else:
            self._show_next_lv(self._old_lv, self._old_lv + 1, upgrade_need_exp, self._updated_exp, self._add_exp, True)

    def show_reward_items(self, reward):
        items = {}
        for reward_type in (BattleReward.ITEM_REWARD, BattleReward.FVICTORY_REWARD):
            reward_info = reward.get_reward(reward_type)
            reward_items = reward_info.items
            for item_no, item_num in six.iteritems(reward_items):
                items.setdefault(item_no, 0)
                items[item_no] += item_num

        count = len(items)
        list_get_item = self.panel.list_get_item
        list_get_item.SetInitCount(count)
        index = 0
        for item_no, cnt in six.iteritems(items):
            item_widget = list_get_item.GetItem(index)
            item_pic = get_lobby_item_pic_by_item_no(item_no)
            item_widget.icon.SetDisplayFrameByPath('', item_pic)
            item_name = get_lobby_item_name(item_no)
            desc = '{0}x{1}'.format(item_name, cnt)
            item_widget.lab_get.SetString(desc)
            index += 1

    def on_click_btn_exit(self, *args):
        if global_data.player:
            global_data.player.quit_battle(True)
        self.close()

    def _calc_exp_add_per_tick(self, add_exp, upgrade_exp):
        tick_add = upgrade_exp / PROGRESS_ADD_ALL_TIME
        if tick_add > add_exp / PROGRESS_ADD_MIN_TIME:
            tick_add = add_exp / PROGRESS_ADD_MIN_TIME
        if tick_add < 1:
            tick_add = 1
        return int(tick_add)

    def _show_upgrade(self):
        init_lv_template(self.panel.nd_level_now, self._old_lv)
        init_lv_template(self.panel.nd_level_next, self._updated_lv)
        self.panel.PlayAnimation('exp_appear')
        upgrade_need_exp = get_lv_upgrade_need_exp(self._old_lv)
        add_exp = upgrade_need_exp - self._old_exp
        ADD_EXP_PER_TICK = self._calc_exp_add_per_tick(add_exp, upgrade_need_exp)
        remain_time = (add_exp / ADD_EXP_PER_TICK + 1) * EndExpUI.TICK_INTERVAL
        self.panel.progress_exp.StopTimerAction()
        self._progress_val = self._old_exp
        self.show_add_exp_info()
        self.panel.progress_exp.SetPercentage(self._progress_val / float(upgrade_need_exp) * 100)
        self.panel.lab_exp_progress.SetString('%s/%s' % (self._progress_val, upgrade_need_exp))

        def finish():
            self.panel.PlayAnimation('level_up')
            left_exp = self._updated_exp - upgrade_need_exp
            if is_full_lv(self._updated_lv) or left_exp == 0:
                self.panel.DelayCall(EndExpUI.CLOSE_UI_DELAY, self._finished_cd)
                return
            lv_upgrade_need_exp = get_lv_upgrade_need_exp(self._updated_lv)
            if left_exp < 0:
                log_error('EndExpUI _show_upgrade self._old_exp=%s, self._old_lv=%s, self._add_exp=%s, left_exp=%s, lv_upgrade_need_exp=%s', self._old_exp, self._old_lv, self._add_exp, left_exp, lv_upgrade_need_exp)
                self.panel.DelayCall(EndExpUI.CLOSE_UI_DELAY, self._finished_cd)
                return
            self.panel.DelayCall(1.5, lambda : self._show_next_lv(self._updated_lv, self._updated_lv + 1, lv_upgrade_need_exp, left_exp, left_exp, False))

        def update_progress_time(dt):
            self._progress_val += ADD_EXP_PER_TICK
            if self._progress_val > upgrade_need_exp:
                self._progress_val = upgrade_need_exp
            self.panel.progress_exp.SetPercentage(self._progress_val / float(upgrade_need_exp) * 100)
            self.panel.lab_exp_progress.SetString('%s/%s' % (self._progress_val, upgrade_need_exp))

        self.panel.progress_exp.TimerAction(update_progress_time, remain_time, callback=finish, interval=EndExpUI.TICK_INTERVAL)
        if get_lv_upgrade_need_exp(self._old_lv) <= self._old_exp + self._add_exp:

            def callback():
                show_lv_up(self._old_lv, self._old_exp, self._add_exp, close_cb=self.exec_end_callback)

            self.add_end_callback(callback, True)
            self.panel.DelayCall(3, lambda : self.exec_end_callback())

    def _show_next_lv(self, cur_lv, next_lv, upgrade_lv_need_exp, left_exp, add_exp, show_appear=True):
        if show_appear:
            self.panel.PlayAnimation('exp_appear')
        init_lv_template(self.panel.nd_level_now, cur_lv)
        init_lv_template(self.panel.nd_level_next, next_lv)
        self.panel.progress_exp.StopTimerAction()
        old_exp = left_exp - add_exp
        self._progress_val = old_exp
        self.show_add_exp_info()
        ADD_EXP_PER_TICK = self._calc_exp_add_per_tick(add_exp, upgrade_lv_need_exp)
        self.panel.progress_exp.SetPercentage(self._progress_val / float(upgrade_lv_need_exp) * 100)
        self.panel.lab_exp_progress.SetString('%s/%s' % (self._progress_val, upgrade_lv_need_exp))
        remain_time = (left_exp / ADD_EXP_PER_TICK + 1) * EndExpUI.TICK_INTERVAL

        def finish():
            if self._finished_cd:
                self.panel.DelayCall(EndExpUI.CLOSE_UI_DELAY, self._finished_cd)

        def update_progress_time(dt):
            self._progress_val += ADD_EXP_PER_TICK
            if self._progress_val > left_exp:
                self._progress_val = left_exp
            self.panel.progress_exp.SetPercentage(self._progress_val / float(upgrade_lv_need_exp) * 100)
            self.panel.lab_exp_progress.SetString('%s/%s' % (self._progress_val, upgrade_lv_need_exp))

        self.panel.progress_exp.TimerAction(update_progress_time, remain_time, callback=finish, interval=EndExpUI.TICK_INTERVAL)

    def show_add_exp_info(self):
        base_text = get_text_by_id(18223).format(add_point=self._add_exp)
        self.panel.btn_exp_down.setVisible(False)
        if self.exp_decay_percent != 0.0:
            decay_text = get_text_by_id(605001).format(str(int(self.exp_decay_percent * 100)))
            self.panel.btn_exp_down.setVisible(True)

            @self.panel.btn_exp_down.unique_callback()
            def OnBegin(*args):
                self.panel.img_fatigue_tips.setVisible(True)

            @self.panel.btn_exp_down.unique_callback()
            def OnEnd(*args):
                self.panel.img_fatigue_tips.setVisible(False)

            self.panel.lab_fatigue_tips.SetString(decay_text)
        self.panel.lab_exp.SetString(base_text)

    def init_role_exp_item(self, role_item, settle_dict, reward, role_id):
        from common import utilities
        from logic.gcommon.cdata import bond_config
        from logic.gcommon.item.item_const import FASHION_POS_SUIT
        role_item.nd_proficiency_level_human.setVisible(True)
        role_item.nd_proficiency_level.setVisible(False)
        role_item.nd_proficiency_level.stopAllActions()
        bond_rewards = reward.bond
        role_id = int(role_id)
        item_data = global_data.player.get_item_by_no(role_id)
        fashion_data = item_data.get_fashion()
        dressed_clothing_id = fashion_data.get(FASHION_POS_SUIT)
        role_skin_config = confmgr.get('role_info', 'RoleSkin', 'Content')
        img_path = role_skin_config.get(str(dressed_clothing_id), {}).get('half_img_role')
        if img_path:
            role_item.img_mech.SetDisplayFrameByPath('', img_path)
        role_info = confmgr.get('role_info', 'RoleProfile', 'Content', str(role_id))
        role_item.lab_mech.SetString(role_info['role_name'])
        bond_data = settle_dict.get('bond_data', {}).get(str(role_id), {})
        if not bond_data:
            bond_level, new_exp = global_data.player.get_bond_data(role_id)
        else:
            old_lv = bond_data.get(u'lv', 1)
            old_exp = bond_data.get(u'st', 0)
            add_exp = bond_rewards[str(role_id)]
            bond_level, new_exp = bond_config.get_new_bond_level_strength(old_lv, old_exp, add_exp)
        self.show_bond_ani(role_item, settle_dict, reward, role_id)

    def show_bond_ani(self, role_item, settle_dict, reward, role_id):
        from common import utilities
        from logic.gcommon.cdata import bond_config
        bond_rewards = reward.bond
        bond_data = settle_dict.get('bond_data', {}).get(str(role_id), {})
        if not bond_data:
            old_lv, old_exp = global_data.player.get_bond_data(role_id)
            add_exp = 0
        else:
            old_lv = bond_data.get(u'lv', 1)
            old_exp = bond_data.get(u'st', 0)
            add_exp = bond_rewards.get(str(role_id), 0)
        nd_prof_lv = role_item.nd_proficiency_level_human
        nd_prof_lv.lab_exp_get.SetString('{}+ {}'.format(get_text_by_id(870046), add_exp))
        _, old_max_exp = bond_config.get_nxt_bond_level_strength(old_lv)
        if old_max_exp == 0:
            old_max_exp = old_exp
        elif old_exp + add_exp >= old_max_exp:
            pos = self.panel.list_mech.convertToWorldSpace(role_item.getPosition())
            pos = self.panel.list_mech.GetParent().convertToWorldSpace(pos)
            self.show_bond_dialog(role_id, pos=cc.Vec2(pos.x + 50, pos.y + 150))
        old_percent = utilities.safe_percent(old_exp, old_max_exp)
        nd_prof_lv.lab_level.SetString('Lv{}'.format(old_lv))
        nd_prof_lv.lab_exp_need.SetString('/{}'.format(old_max_exp))
        nd_prof_lv.lab_exp_need.lab_exp.SetString('{}'.format(old_exp))
        nd_prof_lv.progress_exp.SetProgressTexture(EXP_ROLE_PROGRESS_PATH)
        nd_prof_lv.progress_exp.SetPercentage(old_percent)
        actions = []

        def set_per_cb(total_exp):

            def OnSetPercentage(precent):
                lerp_to_exp = int(float(total_exp) * precent / 100)
                nd_prof_lv.lab_exp_need.lab_exp.SetString('{}'.format(lerp_to_exp))

            return OnSetPercentage

        def add_progress_ani(from_exp, to_exp, total_exp, to_lv):
            if total_exp == 0:

                def callback():
                    nd_prof_lv.lab_exp_need.SetString('/{}'.format(to_exp))
                    nd_prof_lv.lab_exp_need.lab_exp.SetString('{}'.format(to_exp))
                    nd_prof_lv.progress_exp.SetPercentage(100)

                actions.append(cc.CallFunc.create(callback))
                return
            from_percent = float(from_exp) / total_exp
            to_percent = float(to_exp) / total_exp
            last_time = 1.0 * (to_percent - from_percent)

            def end_cb():
                if to_percent >= 1.0:
                    _, nxt_exp = bond_config.get_nxt_bond_level_strength(to_lv)
                    end_exp = 0
                    end_percentage = 0
                    if to_lv >= bond_config.get_bond_max_level():
                        nxt_exp = bond_config.get_cur_bond_level_strength(to_lv)
                        end_exp = nxt_exp
                        end_percentage = 100
                    nd_prof_lv.lab_exp_need.SetString('/{}'.format(nxt_exp))
                    nd_prof_lv.lab_exp_need.lab_exp.SetString('{}'.format(end_exp))
                    nd_prof_lv.progress_exp.SetPercentage(end_percentage)
                    nd_prof_lv.lab_level.SetString('Lv{}'.format(to_lv))
                    cur_lv, _ = global_data.player.get_bond_data(role_id)
                    if cur_lv == to_lv:

                        def callback():
                            show_role_bond_lv_up(role_id, old_lv, cur_lv, close_cb=self.exec_end_callback)

                        self.add_end_callback(callback, True)

            def callback():
                nd_prof_lv.lab_exp_need.SetString('/{}'.format(total_exp))
                nd_prof_lv.progress_exp.OnSetPercentage = set_per_cb(total_exp)
                nd_prof_lv.progress_exp.SetPercentageWithAni(to_percent * 100, last_time)

            actions.append(cc.CallFunc.create(callback))
            actions.append(cc.DelayTime.create(last_time))
            actions.append(cc.CallFunc.create(end_cb))

        cur_cal_lv = old_lv
        cur_cal_exp = old_exp
        cur_add_exp = add_exp
        nd_prof_lv.progress_exp.StopTimerAction()
        while cur_add_exp > 0:
            nxt_level, nxt_exp = bond_config.get_nxt_bond_level_strength(cur_cal_lv)
            if nxt_exp == 0:
                if cur_cal_lv >= bond_config.get_bond_max_level():
                    cur_cal_exp = bond_config.get_cur_bond_level_strength(cur_cal_lv)
                nd_prof_lv.lab_exp_need.SetString('/{}'.format(cur_cal_exp))
                nd_prof_lv.lab_exp_need.lab_exp.SetString('{}'.format(cur_cal_exp))
                nd_prof_lv.progress_exp.SetPercentage(100)
                break
            if cur_cal_exp + cur_add_exp < nxt_exp:
                new_cal_exp = cur_cal_exp + cur_add_exp
                add_progress_ani(cur_cal_exp, new_cal_exp, nxt_exp, cur_cal_lv)
                cur_cal_exp = new_cal_exp
                cur_add_exp = 0
            else:
                add_progress_ani(cur_cal_exp, nxt_exp, nxt_exp, cur_cal_lv + 1)
                cur_add_exp -= nxt_exp - cur_cal_exp
                cur_cal_exp = 0
                cur_cal_lv += 1

        if actions:
            role_item.runAction(cc.Sequence.create(actions))

    def show_bond_dialog(self, role_id, pos=None):
        dialog_id = bond_utils.get_exp_dialog_id(role_id)
        if not dialog_id:
            self.panel.temp_dialogue.setVisible(False)
            return
        self.panel.temp_dialogue.setVisible(True)
        if pos:
            self.panel.temp_dialogue.setPosition(pos)
        if global_data.player:
            if not global_data.player.is_running_show_advance():
                global_data.player.start_show_advance()
        dialog_conf = confmgr.get('role_dialog_config', 'role_{}_dialog'.format(role_id), 'Content', str(dialog_id), default={})
        text_id = dialog_conf.get('content_text_id')
        show_time = dialog_conf.get('show_time', 2)
        self.panel.temp_dialogue.lab_dialogue.SetString(text_id)
        show_ani = 'show'
        play_ani = 'play'
        hide_ani = 'disappear'

        def do_end():
            self.panel.temp_dialogue.PlayAnimation(hide_ani)

        def do_play():
            voice_info = dialog_conf.get('voice', {})
            for trigger, info in six.iteritems(voice_info):
                if type(info) == str:
                    global_data.emgr.play_voice_by_uid.emit('HumanVoice', info)
                    break

            self.panel.temp_dialogue.PlayAnimation(play_ani)
            self.panel.temp_dialogue.SetTimeOut(show_time, do_end)

        self.panel.temp_dialogue.PlayAnimation(show_ani)
        self.panel.temp_dialogue.SetTimeOut(self.panel.temp_dialogue.GetAnimationMaxRunTime(show_ani), do_play)

    def show_gold_reward(self, settle_dict, reward):
        battle_reward = global_data.player.get_battle_reward(battle_settle=True)
        got_gold = battle_reward['gold']
        add_gold = battle_reward['last_add_gold']
        max_gold = battle_reward['max_gold']
        has_yueka = global_data.player.has_yueka()
        has_glod_weekcard = global_data.player.has_gold_weeklycard()
        has_summer_gold_add = settle_dict.get('has_summer_gold_add', False) if settle_dict else False
        text_content = get_text_by_id(80195) + '<color=0xFFF101FF>+%d#n' % add_gold
        first_victory_gold = min(reward.get_first_victory_gold(), add_gold)
        extra_content_list = []
        if first_victory_gold > 0:
            if has_summer_gold_add:
                first_victory_gold /= 1.0 + activity_const.SUMMER_WELFARE_GOLD_ADD_FACTOR
                first_victory_gold = int(first_victory_gold)
            extra_content_list.append('%s%d' % (get_text_by_id(634671), first_victory_gold))
        if has_summer_gold_add:
            extra_content_list.append(get_text_by_id(609725))
        addition = 0
        addition_text_list = []
        if has_glod_weekcard:
            addition += 30
            addition_text_list.append(get_text_by_id(607445))
        if has_yueka:
            addition += 10
            addition_text_list.append(get_text_by_id(607446))
        addition_text = '&'.join(addition_text_list)
        if addition:
            extra_content_list.append('{}+{}%'.format(addition_text, str(addition)))
        privilege_gold_info = global_data.player.logic.ev_g_priv_extra_gold()
        has_privilege_gold = bool(privilege_gold_info)
        privilege_text = ''
        if has_privilege_gold:
            addition += 10
            user_name = global_data.player.get_name()
            user_id = global_data.player.uid
            if user_id in privilege_gold_info:
                privilege_text = get_text_by_id(610214)
            else:
                teaminfo = global_data.player.logic.ev_g_teammate_infos()
                team_uid = privilege_gold_info[0]
                for info in six.itervalues(teaminfo):
                    if info.get('uid', 0) == team_uid:
                        privilege_text = get_text_by_id(610273).format(info.get('char_name', ''))

            extra_content_list.append('{}+{}%'.format(privilege_text, str(10)))
        if extra_content_list:
            text_content += '(%s)' % ','.join(extra_content_list)
        self.panel.lab_coin_num.SetString(text_content)
        from logic.gutils.intimacy_utils import init_intimacy_icon_with_uid_list
        from logic.gcommon.common_const.buff_const import BUFF_ID_BE_RESCUE_TIME_REDUCE
        intimacy_gold_info = global_data.player.logic.ev_g_intimacy_extra_gold()
        has_intimacy_gold = bool(intimacy_gold_info)
        self.panel.temp_buff.setVisible(has_intimacy_gold)
        if has_intimacy_gold:
            self.panel.temp_buff.lab_buff.SetString(get_text_by_id(3257, {'n': 5}))
            init_intimacy_icon_with_uid_list(self.panel.temp_buff.temp_intimacy, intimacy_gold_info, show_level=False)
        old_gold = max(got_gold - add_gold, 0)
        new_gold = got_gold
        interval = 2.0
        delta_gold = int(max(add_gold / (interval * 30), 1) + 0.5)
        self._gold_value = old_gold

        def gold_progress_tick(dt):
            self.panel.lab_coin_progress.SetString(get_text_by_id(609129) + str(self._gold_value) + '/' + str(max_gold))
            self.panel.progress_coin.SetPercentage(self._gold_value * 100.0 / max_gold)
            if self._gold_value >= new_gold:
                self.panel.nd_coin.StopTimerAction()
            self._gold_value = min(self._gold_value + delta_gold, new_gold)

        gold_progress_tick(0)
        if delta_gold > 0:
            self.panel.nd_coin.TimerAction(gold_progress_tick, interval + 0.01, interval=0.03)

    def show_meow_reward(self, settle_dict, reward):
        if G_IS_NA_PROJECT:
            self.panel.nd_miaomiao.setVisible(False)
            return
        meow_coin_data = reward.meow_coin_data
        if not meow_coin_data:
            self.panel.nd_miaomiao.setVisible(False)
            return
        self.panel.nd_miaomiao.setVisible(True)
        bag = meow_coin_data.get('bag', 0)
        safe_box = meow_coin_data.get('safe_box', 0)
        this_total = meow_coin_data.get('this_total', 0)
        week_limit = meow_coin_data.get('week_limit', 0)
        mail_box = meow_coin_data.get('mail_box', 0)
        week_total = meow_coin_data.get('week_total', 0)
        self.panel.lab_num_all.SetString(str(this_total))
        is_limit = week_total >= week_limit
        self.panel.lab_num_all.SetColor('#SW' if is_limit else '#SY')
        self.panel.lab_upper_limit.SetString('%d/%d' % (week_total, week_limit))
        self.panel.lab_upper_limit.SetColor('#DY' if is_limit else '#SW')
        self.panel.prog_coin.SetPercentage(1.0 * (week_total - this_total) / week_limit * 100)
        self.panel.prog_coin_increase.SetPercentage(1.0 * week_total / week_limit * 100)
        self.panel.lab_safe_num.SetString(str(safe_box))
        self.panel.lab_bag_num.SetString(str(bag - safe_box))
        self.panel.lab_mail_num.SetString(str(mail_box))
        self.panel.btn_help.SetForceHandleTouch(True)

        @self.panel.btn_help.unique_callback()
        def OnBegin(btn, touch):
            wpos = touch.getLocation()
            if btn.IsPointIn(wpos):
                if self.panel.nd_miaomiao_describe.isVisible():
                    self.panel.nd_miaomiao_describe.setVisible(False)
                    return False
                return True
            self.panel.nd_miaomiao_describe.setVisible(False)
            return False

        @self.panel.btn_help.unique_callback()
        def OnClick(btn, touch):
            vis = not self.panel.nd_miaomiao_describe.isVisible()
            self.panel.nd_miaomiao_describe.setVisible(vis)