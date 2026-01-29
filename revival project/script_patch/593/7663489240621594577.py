# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Settle/SettleAllUI.py
from __future__ import absolute_import
import six
from six.moves import range
from common.uisys.basepanel import BasePanel
from common.const.uiconst import UI_VKB_NO_EFFECT
from logic.gutils import bond_utils
from logic.gutils.dress_utils import battle_id_to_mecha_lobby_id
from common.cfg import confmgr
from logic.gcommon.common_utils.local_text import get_text_by_id
from cocosui import cc
from logic.gcommon.ctypes.BattleReward import Reward, BattleReward
from logic.gutils.lv_template_utils import get_lv_upgrade_need_exp, is_full_lv
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no, get_lobby_item_name
from logic.comsys.battle.Settle.SettleDanWidget import SettleDanWidget
from logic.gutils import season_utils
from logic.gcommon.common_const.battle_const import AGAIN_GAME_TYPE, BEGINNER_BATTLE_TYPE_BEGIN, NEWBIE_BATTLE_TYPE_END
from logic.gcommon.common_const.statistics_const import HANG_UP, ESCAPE_BATTLE
from logic.gcommon.item.item_const import YUEAKA_EXP_ADD
from logic.gcommon.common_const import battle_const
from logic.client.const.game_mode_const import GAME_MODE_ASSAULT
from logic.gcommon.common_const.team_const import TEAMMATE_MATCH_AGAIN_TYPE_NONE, TEAMMATE_MATCH_AGAIN_TYPE_NORMAL
HIDE_UI_LIST = [
 'SmallMapUI', 'QuickMarkUI', 'BattleRightTopUI', 'FightBagUI', 'HpInfoUI', 'FightSightUI',
 'FightStateUI', 'ScalePlateUI', 'WeaponBarSelectUI', 'BattleFightCapacity', 'FightKillNumberUI',
 'RogueGiftTopRightUI', 'BattleFightMeow', 'DeathRogueGiftTopRightUI']
EXP_DOUBLE_ITEM_NO = 50302011
EXP_YUKA_ITEM_PIC_PATH = 'gui/ui_res_2/main/buff_month_exp_up.png'
EXP_RECRUIT_GROUP_PIC_PATH = 'gui/ui_res_2/fight_end/img_end_exp_friend.png'
EXP_ROLE_PROGRESS_PATH = 'gui/ui_res_2/fight_end/prog_role.png'

def show_role_bond_lv_up(role_id, old_lv, new_lv, close_cb=None):
    data_dict = {'role_id': int(role_id),
       'old_lv': old_lv,
       'new_lv': new_lv,
       'close_cb': close_cb
       }
    ui = global_data.ui_mgr.show_ui('EndRoleLevelUI', 'logic.comsys.battle.Settle')
    ui.play_animation(data_dict)


def show_lv_up--- This code section failed: ---

  46       0  BUILD_MAP_4           4 

  47       3  BUILD_MAP_1           1 
           6  STORE_MAP        

  48       7  LOAD_FAST             1  'old_exp'
          10  LOAD_CONST            2  'old_exp'
          13  STORE_MAP        

  49      14  LOAD_FAST             2  'add_exp'
          17  LOAD_CONST            3  'add_exp'
          20  STORE_MAP        

  50      21  LOAD_FAST             3  'close_cb'
          24  LOAD_CONST            4  'close_cb'
          27  STORE_MAP        
          28  STORE_FAST            4  'data_dict'

  53      31  LOAD_GLOBAL           0  'global_data'
          34  LOAD_ATTR             1  'ui_mgr'
          37  LOAD_ATTR             2  'show_ui'
          40  LOAD_CONST            5  'EndLevelUI'
          43  LOAD_CONST            6  'logic.comsys.battle.Settle'
          46  CALL_FUNCTION_2       2 
          49  STORE_FAST            5  'ui'

  54      52  LOAD_FAST             5  'ui'
          55  LOAD_ATTR             3  'play_animation'
          58  LOAD_FAST             4  'data_dict'
          61  CALL_FUNCTION_1       1 
          64  POP_TOP          

Parse error at or near `STORE_MAP' instruction at offset 6


class SettleAllUI(BasePanel):
    PANEL_CONFIG_NAME = 'end/end_exp_and_tier'
    UI_VKB_TYPE = UI_VKB_NO_EFFECT
    MOUSE_CURSOR_TRIGGER_SHOW = True
    TICK_INTERVAL = 0.03
    GLOBAL_EVENT = {'on_notify_rematch': '_on_notify_rematch',
       'player_teammate_info_update_event': 'init_again_btn'
       }

    def on_custom_template_create(self, *arg, **kwargs):
        if not global_data.player:
            return
        dan_info = global_data.player.get_last_battle_dan_info()
        cur_dan = dan_info.get('dan', (1, 1))[0]
        stage_template = season_utils.get_dan_template(cur_dan)
        self._custom_template_info = {'temp_tier': {'template_info': {'temp_tier': {'ccbFile': stage_template}}}}

    def on_init_panel(self, settle_dict, reward, settle_exp_dict, finished_cd=None):
        self.settle_dict = settle_dict
        self.reward = reward
        self.exp_dict = settle_exp_dict
        self._prof_conf = confmgr.get('proficiency_config', 'Proficiency')
        self._dan_conf = confmgr.get('proficiency_config', 'ProficiencyDan')
        self._max_level = len(self._prof_conf)
        self._max_dan_lv = len(self._dan_conf)
        self.is_double_exp = False
        self.is_yueka_exp = False
        self.recruit_group_exp_rate = 0
        self.end_callback_list = []
        self.show_end_callback = True
        self.showing_end_callback = False
        self.member_still_playing = False
        self.first_victory_list = []
        self.init_mecha_role_list_widget()
        self.init_gold_reward_item()
        self.init_exp_reward_item()
        self.init_meow_reward_item()
        self.init_item_reward_item()
        self.init_dan_widget()
        self.init_buttons()
        self.init_attention_tips()
        self.init_exp_extra_addition_tips()
        self.panel.PlayAnimation('exp_appear')
        self.hide_main_ui(HIDE_UI_LIST)
        self.show_reward_item_anim()
        self.show_first_victory()
        self.show_teammate_match_again()

    def on_finalize_panel(self):
        self.member_still_playing = False
        self.first_victory_list = []
        self.dan_widget and self.dan_widget.destroy_widget()
        self.show_main_ui()

    def show_first_victory(self):
        from logic.gcommon.ctypes.BattleReward import BattleReward
        has_first_victory = self.settle_dict.get('reward', {}).get(BattleReward.FVICTORY_REWARD, {}).get('get_fv_reward', False)
        if has_first_victory:

            def check_percentage_change_is_stop():
                if self.dan_widget and self.dan_widget.is_percentage_ani_ended():
                    ui_item = self.panel.lab_score.nd_auto_fit
                    ui_item.temp_first_win.setVisible(True)
                    for _item in self.first_victory_list:
                        if _item and not _item.IsDestroyed():
                            _item.temp_first_win.setVisible(True)

                    return None
                else:
                    return 0.1
                    return None

            self.panel.DelayCallWithTag(0.3, check_percentage_change_is_stop, tag=230705)

    def init_dan_widget(self):
        if not global_data.player:
            self.panel.nd_left.setVisible(False)
            return
        dan_info = global_data.player.get_last_battle_dan_info()
        if not dan_info:
            dan_info.update({'no_dan': True
               })
        dan_info.update({'settle_reason': self.settle_dict.get('settle_reason', battle_const.BATTLE_SETTLE_REASON_NORMAL),
           'is_surrender': self.settle_dict.get('extra_detail').get('is_surrender', False),
           'map_id': self.settle_dict.get('map_id')
           })
        self.dan_widget = SettleDanWidget(self.panel, dan_info)
        self.dan_widget.init_widget()
        has_first_victory = self.settle_dict.get('reward', {}).get(BattleReward.FVICTORY_REWARD, {}).get('get_fv_reward', False)
        self.dan_widget.check_show_first_victory_node(has_first_victory)

    def init_mecha_role_list_widget(self):
        mecha_ids = self.get_show_mecha_ids()
        role_ids = self.get_show_role_ids()
        mecha_count = len(mecha_ids)
        if not self.panel.list_mech:
            return
        else:
            count = len(mecha_ids) + len(role_ids)
            if count >= 4:
                nd_list = self.panel.list_mech_5more
                self.panel.list_mech.setVisible(False)
                self.panel.list_mech_5more.setVisible(True)
            elif count > 0:
                nd_list = self.panel.list_mech
                self.panel.list_mech.setVisible(True)
                self.panel.list_mech_5more.setVisible(False)
            else:
                nd_list = None
                self.panel.list_mech.setVisible(False)
                self.panel.list_mech_5more.setVisible(False)
            if nd_list:
                nd_list.SetInitCount(count)
                for idx, mecha_id in enumerate(mecha_ids):
                    mecha_item = nd_list.GetItem(idx)
                    self.init_mecha_exp_item(mecha_item, mecha_id)

                for idx, role_id in enumerate(role_ids):
                    role_item = nd_list.GetItem(mecha_count + idx)
                    self.init_role_exp_item(role_item, role_id)

            return

    def get_show_mecha_ids(self):
        created_mecha_ids = self.settle_dict.get('created_mecha_ids', []) or []
        created_mecha_ids = [ str(mecha_id) for mecha_id in created_mecha_ids ]
        unique_created_mecha_ids = []
        for mecha_id in created_mecha_ids:
            if mecha_id not in unique_created_mecha_ids:
                unique_created_mecha_ids.append(mecha_id)

        mecha_ids = [ mecha_id for mecha_id in unique_created_mecha_ids if mecha_id in self.reward.proficiency ]
        return mecha_ids

    def get_show_role_ids(self):
        role_ids = []
        if bond_utils.is_open_bond_sys():
            bond_rewards = self.reward.bond
            for str_role_id, add_exp in six.iteritems(bond_rewards):
                add_exp > 0 and role_ids.append(str_role_id)

        return role_ids

    def init_mecha_exp_item(self, mech_item, mecha_id):
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
        proficiency_data = self.settle_dict.get('proficiency_data', {}).get(str(mecha_id), {})
        lv = proficiency_data.get('level', 1)
        proficiency = proficiency_data.get('proficiency', 0)
        self._update_mech_proficiency_data(mech, lv, proficiency)
        pro_get = self.reward.proficiency.get(str(mecha_id), 0)
        nd_prof_lv.lab_exp_get.SetString(get_text_by_id(400011) + '+' + str(pro_get))
        upgrade_value = self._get_upgrade_need_value(lv)
        upgraded_exp = proficiency + pro_get
        final_lv, final_prof = self._cal_final_lv_and_proficiency(lv, upgraded_exp)
        cur_prof = proficiency
        upgrade_need_prof = upgrade_value
        cur_lv = lv
        update_info = {'cur_prof': cur_prof,
           'upgrade_need_prof': upgrade_need_prof,
           'cur_lv': cur_lv
           }
        remain_time = pro_get * SettleAllUI.TICK_INTERVAL
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

        nd_prof_lv.progress_exp.TimerAction(update_proficiency, remain_time, callback=finish, interval=SettleAllUI.TICK_INTERVAL)

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
        if icon_path:
            nd_prof_lv.img_proficiency_level.SetDisplayFrameByPath('', icon_path)

    def _get_dan_lv(self, level):
        dan_lv = 1
        for dan_lv in range(1, self._max_dan_lv + 1):
            max_level = self._dan_conf[str(dan_lv)]['max_level']
            if level < max_level:
                break

        return dan_lv

    def init_role_exp_item(self, role_item, role_id):
        from logic.gcommon.item.item_const import FASHION_POS_SUIT
        role_item.nd_proficiency_level_human.setVisible(True)
        role_item.nd_proficiency_level.setVisible(False)
        role_item.nd_proficiency_level.stopAllActions()
        role_id = int(role_id)
        item_data = global_data.player.get_item_by_no(role_id)
        if not item_data:
            return
        fashion_data = item_data.get_fashion()
        dressed_clothing_id = fashion_data.get(FASHION_POS_SUIT)
        role_skin_config = confmgr.get('role_info', 'RoleSkin', 'Content')
        img_path = role_skin_config.get(str(dressed_clothing_id), {}).get('half_img_role')
        if img_path:
            role_item.img_mech.SetDisplayFrameByPath('', img_path)
        role_info = confmgr.get('role_info', 'RoleProfile', 'Content', str(role_id))
        role_item.lab_mech.SetString(role_info['role_name'])
        self.show_bond_ani(role_item, role_id)

    def show_bond_ani(self, role_item, role_id):
        from common import utilities
        from logic.gcommon.cdata import bond_config
        bond_rewards = self.reward.bond
        bond_data = self.settle_dict.get('bond_data', {}).get(str(role_id), {})
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
                    cur_lv = 8
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

    def init_exp_reward_item(self):
        old_lv = self.exp_dict.get('old_lv', 1)
        old_exp = self.exp_dict.get('old_exp', 0)
        add_exp = self.exp_dict.get('add_exp', 0)
        player = global_data.player
        if player:
            cur_lv = player.get_lv()
            cur_exp = player.get_exp()
            upgrade_need_exp = get_lv_upgrade_need_exp(cur_lv)
        else:
            updated_exp = old_exp + add_exp
            upgrade_need_exp = get_lv_upgrade_need_exp(old_lv)
            if updated_exp >= upgrade_need_exp:
                cur_lv = old_lv + 1
                upgrade_need_exp = get_lv_upgrade_need_exp(cur_lv)
                cur_exp = updated_exp - upgrade_need_exp
            else:
                cur_lv = old_lv
                cur_exp = updated_exp
        ui_item = self.panel.list_expitem.AddTemplateItem(bRefresh=True)
        ui_item.icon.SetDisplayFrameByPath('', 'gui/ui_res_2/icon/icon_exp.png')
        ui_item.lab_name.SetString(215003)
        ui_item.lab_add_exp.SetString('+{}'.format(str(add_exp)))
        ui_item.lab_exp.SetString('({}/{})'.format(cur_exp, upgrade_need_exp))
        if cur_lv > old_lv:

            def callback():
                show_lv_up(old_lv, old_exp, add_exp, close_cb=self.exec_end_callback)

            self.add_end_callback(callback, True)
            self.exec_end_callback()
        self.update_ui_item_first_victory(ui_item, 'fv_exp')

    def update_ui_item_first_victory(self, ui_item, fv_key):
        from logic.gcommon.ctypes.BattleReward import BattleReward
        has_first_victory = self.settle_dict.get('reward', {}).get(BattleReward.FVICTORY_REWARD, {}).get('get_fv_reward', False)
        if has_first_victory:
            from common.cfg import confmgr
            fv_exp = confmgr.get('daily_first_victory_conf', fv_key, 'Value', default=0)
            ui_item.temp_first_win.lab_value_add.SetString('+%s' % fv_exp)
            self.first_victory_list.append(ui_item)

    def init_gold_reward_item(self):
        player = global_data.player
        if not player:
            return
        battle_reward = player.get_battle_reward(battle_settle=True)
        got_gold = battle_reward['gold']
        add_gold = self.reward.gold
        max_gold = battle_reward['max_gold']
        ui_item = self.panel.list_expitem.AddTemplateItem(bRefresh=True)
        ui_item.icon.SetDisplayFrameByPath('', 'gui/ui_res_2/icon/icon_gold.png')
        ui_item.lab_name.SetString(215002)
        ui_item.lab_add_exp.SetString('+{}'.format(str(add_gold)))
        ui_item.lab_exp.SetString('({}/{})'.format(got_gold, max_gold))
        self.update_ui_item_first_victory(ui_item, 'fv_gold')

    def init_meow_reward_item(self):
        meow_coin_data = self.reward.meow_coin_data
        this_total = meow_coin_data.get('this_total', 0)
        week_total = meow_coin_data.get('week_total', 0)
        week_limit = meow_coin_data.get('week_limit', 0)
        ui_item = self.panel.list_expitem.AddTemplateItem(bRefresh=True)
        ui_item.icon.SetDisplayFrameByPath('', 'gui/ui_res_2/icon/icon_1059951.png')
        ui_item.lab_name.SetString(219851)
        ui_item.lab_add_exp.SetString('+{}'.format(str(this_total)))
        ui_item.lab_exp.SetString('({}/{})'.format(week_total, week_limit))
        self.update_ui_item_first_victory(ui_item, 'fv_meow')

    def init_item_reward_item(self):
        items = {}
        for reward_type in (BattleReward.ITEM_REWARD, BattleReward.FVICTORY_REWARD):
            reward_info = self.reward.get_reward(reward_type)
            reward_items = reward_info.items
            for item_no, item_num in six.iteritems(reward_items):
                items.setdefault(item_no, 0)
                items[item_no] += item_num

        for item_no, item_num in six.iteritems(items):
            ui_item = self.panel.list_expitem.AddTemplateItem(bRefresh=True)
            icon_path = 'gui/ui_res_2/icon/icon_{}.png'.format(item_no)
            item_name = get_lobby_item_name(item_no)
            ui_item.icon.SetDisplayFrameByPath('', icon_path)
            ui_item.lab_name.SetString(item_name)
            ui_item.lab_add_num.SetString('+{}'.format(str(item_num)))
            ui_item.nd_num.setVisible(True)

    def show_reward_item_anim(self):
        for idx, item in enumerate(self.panel.list_expitem.GetAllItem()):
            self.panel.DelayCall(0.1 * (idx + 1), lambda ui_item=item: self.play_reward_item_anim(ui_item))

    def play_reward_item_anim(self, ui_item):
        if self and self.panel and self.panel.isValid() and ui_item.isValid():
            ui_item.PlayAnimation('show')

    def init_buttons(self):
        battle_type = global_data.battle.get_battle_tid() if global_data.battle else 0
        again_mode = battle_type in AGAIN_GAME_TYPE or BEGINNER_BATTLE_TYPE_BEGIN < battle_type < NEWBIE_BATTLE_TYPE_END
        self.panel.btn_again.setVisible(bool(again_mode))
        if again_mode:
            self.init_again_btn()
            self.init_again_btn_click()
        else:
            self.panel.btn_again and self.panel.btn_exit.setPosition(self.panel.btn_again.getPosition())
        self.init_exit_btn()

    def init_again_btn(self, *args):
        btn_major = self.panel.btn_again.btn_major
        self.member_still_playing = False
        rank = self.settle_dict.get('rank')
        if rank == 1:
            btn_major.SetShowEnable(True)
            return
        else:
            if global_data.player:
                team_info = global_data.player.get_team_info() if 1 else None
                if not team_info:
                    btn_major.SetShowEnable(True)
                    return
                members = team_info.get('members')
                members or btn_major.SetShowEnable(True)
                return
            for member_info in six.itervalues(members):
                match_stub = member_info.get('match_stub')
                if match_stub:
                    self.member_still_playing = True
                    btn_major.SetShowEnable(not self.member_still_playing)
                    return

            return

    def init_again_btn_click(self):

        @self.panel.btn_again.btn_major.unique_callback()
        def OnClick(*args):
            if self.member_still_playing:
                global_data.game_mgr.show_tip(get_text_by_id(635245))
                return
            self._match_again()
            self.close()

    def init_exit_btn(self):

        @self.panel.btn_exit.btn_major.unique_callback()
        def OnClick(*args):
            self.on_click_btn_exit()

    def on_click_btn_exit(self, *args):
        global_data.player and global_data.player.quit_battle(True)
        self.close()

    def init_attention_tips(self):
        if global_data.game_mode and global_data.game_mode.is_mode_type(GAME_MODE_ASSAULT):
            show_attention = False
        else:
            show_attention = self.settle_dict.get(ESCAPE_BATTLE, False) or self.settle_dict.get('afk', False)
        self.panel.nd_attention and self.panel.nd_attention.setVisible(show_attention)

    def init_exp_extra_addition_tips(self):
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

    def add_end_callback(self, callback, pending):
        self.end_callback_list.append([callback, pending])

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

    def show_teammate_match_again(self):
        if global_data.player and global_data.player.teammate_match_again_type and not global_data.player.match_again:
            self._on_notify_rematch()
            global_data.player.teammate_match_again_type = TEAMMATE_MATCH_AGAIN_TYPE_NORMAL

    def _match_again(self):
        if global_data.player:
            global_data.player.quit_battle(True, True)
            global_data.player.match_again = True
            global_data.has_show_rematch_dialog = True

    def _on_notify_rematch(self, *args):
        if not global_data.player:
            return
        if global_data.has_show_rematch_dialog:
            return
        global_data.has_show_rematch_dialog = True
        from logic.comsys.common_ui.NormalConfirmUI import NormalConfirmUI2
        NormalConfirmUI2().init_widget(content=get_text_by_id(635264), cancel_text=19002, on_confirm=self._match_again)