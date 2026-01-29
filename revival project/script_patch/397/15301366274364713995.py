# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/SurviveInfoUI.py
from __future__ import absolute_import
from six.moves import range
from common.uisys.basepanel import BasePanel
import world
import cc
from common.const.uiconst import NORMAL_LAYER_ZORDER
from common.uisys.uielment.CCRichText import CCRichText
from common.utils.cocos_utils import ccc3FromHex, ccp, CCRect, CCSizeZero, ccc4FromHex, ccc4aFromHex
from logic.gcommon.common_utils import battle_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_const import battle_const as bconst
from logic.gutils.team_utils import get_teammate_colors
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode
from logic.client.const import game_mode_const
from common.const import uiconst
from logic.comsys.common_ui import CommonInfoUtils
from logic.gutils import mecha_skin_utils
TIP_HEIGHT = 28

class SurviveInfoUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/fight_survive'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    UI_ACTION_EVENT = {}
    UI_CLICK_SALOG_DIC = {}

    def on_init_panel(self):
        self.init_parameters()
        self.init_panel_event()

    def on_finalize_panel(self):
        self.player = None
        return

    def leave_screen(self):
        super(SurviveInfoUI, self).leave_screen()
        global_data.ui_mgr.close_ui('SurviveInfoUI')

    def init_parameters(self):
        self.player = None
        scn = world.get_active_scene()
        player = scn.get_player()
        emgr = global_data.emgr
        self.battle_report_queue = []
        self.history_battle_report_list = []
        self.can_showing_battle_report = True
        self._on_fly_battle_report_num = 0
        self._on_fly_msg_nds = []
        self.team_title_height = 0
        self._cur_battle_report_show_index = 0
        self._history_node_size_queue = []
        self.is_in_observe = False
        if player:
            spec_target = player.ev_g_spectate_target()
            if spec_target:
                self.on_enter_observed(spec_target.logic)
            else:
                self.on_player_setted(player)
        emgr.scene_player_setted_event += self.on_player_setted
        emgr.scene_observed_player_setted_event += self.on_enter_observed
        econf = {'scene_set_survive_visible_event': self.set_survive_visible,
           'show_battle_report_event': self.show_battle_report,
           'show_battle_report_msg_event': self._show_battle_report,
           'show_battle_report_msg_ex_event': self._show_battle_report_ex,
           'move_survive_info_ui_event': self.move_survive_ui_from_time_stamp,
           'cam_lplayer_gulag_state_changed': self.on_player_gulag_state_changed
           }
        emgr.bind_events(econf)
        return

    def on_player_setted(self, player):
        self.player = player

    def set_survive_visible(self, key, vis):
        if not vis:
            self.add_hide_count(key)
        else:
            self.add_show_count(key)

    def get_mvp_template(self):
        return bconst.COMMON_SURVIVAL_KILL_MVP_MESSAGE

    def get_ss_msg_type(self):
        return bconst.COMMON_SURVIVAL_SS_KILL_MESSAGE

    def add_node_by_type(self, nd, msg, align=2):
        if not nd:
            return
        else:
            if not hasattr(nd, 'rt_msg'):
                nd.rt_msg = None
            msg_type = msg.get('msg_type')
            kill_msg = None
            if nd.rt_msg:
                if nd.rt_msg.msg_type != msg_type:
                    if nd.rt_msg.msg_type == None:
                        nd.rt_msg.Destroy()
                    else:
                        CommonInfoUtils.destroy_ui(nd.rt_msg)
                    nd.rt_msg = None
                elif msg_type == bconst.MAIN_KILL_KING:
                    kill_msg = nd.rt_msg
                    self.refresh_mvp_info(kill_msg, msg)
                elif msg_type in [bconst.COMMON_SURVIVAL_SS_KILL_MESSAGE, bconst.COMMON_SURVIVAL_SS_KILL_MESSAGE_PC]:
                    kill_msg = nd.rt_msg
                    self.refresh_ss_skin_info(kill_msg, msg)
                    nd.bar_message.SetContentSize(0, nd.bar_message.GetContentSize()[1])
            if not nd.rt_msg:
                if msg_type == bconst.MAIN_KILL_KING:
                    kill_msg = CommonInfoUtils.create_ui(self.get_mvp_template(), nd.nd_kill_message)
                    self.refresh_mvp_info(kill_msg, msg)
                    nd.rt_msg = kill_msg
                    nd.rt_msg.msg_type = msg_type
                    kill_msg.ignoreAnchorPointForPosition(False)
                elif msg_type in [bconst.COMMON_SURVIVAL_SS_KILL_MESSAGE, bconst.COMMON_SURVIVAL_SS_KILL_MESSAGE_PC]:
                    kill_msg = CommonInfoUtils.create_ui(msg_type, nd.nd_kill_message)
                    self.refresh_ss_skin_info(kill_msg, msg)
                    nd.rt_msg = kill_msg
                    nd.rt_msg.msg_type = msg_type
                    nd.bar_message.SetContentSize(0, nd.bar_message.GetContentSize()[1])
                    kill_msg.ignoreAnchorPointForPosition(False)
            if kill_msg:
                if align == 2:
                    kill_msg.setAnchorPoint(cc.Vec2(1, 0.5))
                    kill_msg.SetPosition('100%', '50%')
                elif align == 0:
                    kill_msg.setAnchorPoint(cc.Vec2(0, 0.5))
                    kill_msg.SetPosition('0%', '50%')
            return

    def refresh_mvp_info(self, nd, msg):
        name = msg.get('name', '')
        is_groupmate = msg.get('is_groupmate', False)
        killer_id = msg.get('killer_id')
        nd.killer.SetString(name)
        nd.img_teammate_bg.setVisible(is_groupmate)
        content = get_text_by_id(19792)
        icon_txt = '<color=0XFFFFFFFF><img ="gui/ui_res_2/fight_end/end_tdm/anim_mvp_0001_mvp.png",scale=0.0></color>'
        txt = content.format(mvp=icon_txt)
        nd.lab_teammate.SetString(80890 if is_groupmate else ' ')
        nd.verb.SetString(txt)
        o_pos = nd.nd_auto_fit.getPosition()
        if is_groupmate:
            nd.nd_auto_fit.setPosition(cc.Vec2(0, o_pos.y))
        else:
            nd.nd_auto_fit.setPosition(cc.Vec2(-20, o_pos.y))
        if is_groupmate and global_data.cam_lplayer:
            from logic.gutils.item_utils import get_teammate_tag_path
            all_teammates = global_data.cam_lplayer.ev_g_groupmate()
            player_col = get_teammate_colors(all_teammates)
            color = player_col.get(killer_id, bconst.MAP_COL_BLUE)
            nd.img_teammate_bg.SetDisplayFrameByPath('', get_teammate_tag_path(color))

    def refresh_ss_skin_info(self, nd, msg):
        msg_str = msg.get('msg')
        color_str = msg.get('color_str')
        align = 2 if global_data.is_pc_mode else 0
        mecha_fashion_id = msg.get('skin_id')
        mecha_pic_path = mecha_skin_utils.get_mecha_pic_path(mecha_fashion_id)
        self.add_rich_text_str(nd.nd_message, msg_str, color_str, align, global_data.is_pc_mode or 80 if 1 else 70)
        nd.img_mecha.SetDisplayFrameByPath('', mecha_pic_path)
        if global_data.is_pc_mode:
            bar_size = nd.nd_message.bar_message.getContentSize()
            nd.nd_adapt.SetContentSize(bar_size.width, nd.nd_adapt.getContentSize().height)

    def add_rich_text_str(self, nd, input_str, color_str, align=2, extra_bar_width=0, extra_right_x_offset=0):
        if not nd:
            return
        else:
            rich_str = color_str + '<align=1><shadow=1>' + input_str + '</shadow></align></color>'
            if not hasattr(nd, 'rt_msg'):
                nd.rt_msg = None
            if nd.rt_msg:
                if nd.rt_msg.msg_type:
                    CommonInfoUtils.destroy_ui(nd.rt_msg)
                    nd.rt_msg = None
                else:
                    nd.rt_msg.SetString(rich_str)
                    nd.rt_msg.formatText()
                    kill_msg = nd.rt_msg
            if not nd.rt_msg:
                kill_msg = CCRichText.Create(rich_str, 18, cc.Size(nd.getContentSize().width, 0))
                kill_msg.setVerticalSpace(0)
                nd.nd_kill_message.AddChild('', kill_msg)
                nd.rt_msg = kill_msg
                nd.rt_msg.msg_type = None
                kill_msg.ignoreAnchorPointForPosition(False)
            if align == 2:
                kill_msg.setAnchorPoint(cc.Vec2(1, 0.5))
                kill_msg.SetPosition('100%%%d' % extra_right_x_offset, '50%')
                kill_msg.SetHorizontalAlign(2)
            elif align == 0:
                kill_msg.setAnchorPoint(cc.Vec2(0, 0.5))
                kill_msg.SetPosition('0%', '50%')
                kill_msg.SetHorizontalAlign(0)
            if nd.rt_msg and nd.bar_message:
                nd.rt_msg.formatText()
                text_width = nd.rt_msg.GetTextContentSize().width
                if text_width <= 0:
                    text_width = 300
                origin_text_height = nd.bar_message.GetContentSize()[1]
                extra_width = 10
                nd.bar_message.SetContentSize(text_width + extra_width + extra_bar_width, origin_text_height)
            return

    def init_panel_event(self):
        self.message_nd_pool = [
         self.panel.kill_message_1, self.panel.kill_message_2,
         self.panel.kill_message_3, self.panel.kill_message_4,
         self.panel.kill_message_5, self.panel.kill_message_6]

    def show_battle_report(self, report_dict):
        bat = global_data.battle
        if hasattr(bat, 'is_duel_player'):
            killer_id, _, _ = battle_utils.parse_battle_report_death(report_dict)
            if not bat.is_duel_player(killer_id):
                return
        if report_dict['event_type'] == bconst.FIGHT_EVENT_ELIMINATE:
            color = '#SR'
            if global_data.is_in_judge_camera:
                color = '#SW'
            for name in report_dict.get('eliminate_names', []):
                msg = get_text_by_id(18548).format(**{'injured': name
                   })
                self._show_battle_report(msg, color, report_dict)

        elif report_dict['event_type'] == bconst.FIGHT_EVENT_REVIVE:
            for name in report_dict.get('revive_names', []):
                msg = get_text_by_id(17982, {'playername': name})
                self._show_battle_report(msg, '#SW')

        elif report_dict['event_type'] == bconst.FIGHT_EVENT_RESET_MECHA:
            name = report_dict.get('char_name', '')
            if self.player and name == self.player.ev_g_char_name():
                color = '#SG'
            elif global_data.is_in_judge_camera:
                color = '#SW'
            else:
                color = '#SR'
            msg = get_text_by_id(81387, {'name': name})
            self._show_battle_report(msg, color, report_dict)
        else:
            msg, msg_color, trigger_other_info = self.parse_battle_report(report_dict)
            is_ss = mecha_skin_utils.is_ss_level_skin(trigger_other_info.get('skin_id'))
            if msg:
                if is_ss and trigger_other_info.get('enable_ss_skin_broadcast'):
                    msg_type = self.get_ss_msg_type()
                    msg_dict = {'msg_type': msg_type,'msg': msg,'color_str': msg_color,'skin_id': trigger_other_info.get('skin_id')
                       }
                    self._show_battle_report(msg_dict, msg_color, report_dict)
                else:
                    self._show_battle_report(msg, msg_color, report_dict)

    def _show_battle_report(self, msg, msg_color, report_dict=None):
        if msg:
            killer_id = ''
            if global_data.is_judge_ob and report_dict:
                killer_id = self.get_report_dict_killer_id(report_dict)
            self.battle_report_queue.append((msg, msg_color, killer_id))
            self._show_next_battle_report()

    def _show_battle_report_ex(self, msg_dict):
        if msg_dict:
            killer_id = ''
            self.battle_report_queue.append((msg_dict, None, killer_id))
            self._show_next_battle_report()
        return

    def test_battle_report(self):
        import random
        bg_path = 'gui/ui_res_2/common/panel/kill_bar_normal.png'
        msg = ('test_battle_report ' + str(random.randint(1, 100)), '#SW')
        self.battle_report_queue.append(msg)
        self._show_next_battle_report()

    def test_2(self):
        from bson.objectid import ObjectId
        a = {'bleed_source': None,'event_type': 2,'injured_faction': -21,'death_source': [3,
                          {'maker_type': 2,'mecha_id': 8003,
                             's_pos': [
                                     -5322.1533203125,
                                     773.1218872070312,
                                     -11027.5791015625],
                             'trigger_parts': [],'trigger_faction': -20,
                             'points': None,
                             'trigger_id': ObjectId('5e12a53e3817886dbfb810d6'),
                             'item_id': 800302,
                             'trigger_name': 'DM_\xe6\x88\x90\xe6\x95\x99\xe9\x99\xa2\xe8\x80\x81\xe6\x98\xaf'
                             }],
           'injured_id': ObjectId('5e12a58e3817886dbfb81180'),
           'injured_name': 'DM_O\xe5\x8f\xb8\xe4\xbb\xa4\xe5\xae\x98O','points': None}
        self.show_battle_report(a)
        return

    def test_3(self):
        from bson.objectid import ObjectId
        a = {'is_defeated_valid': False,'injured_name': '\xe5\xad\x97\xe5\x85\xab\xe7\xbb\x99\xe4\xb8\xaa\xe5\xad\x97 ','bleed_source': None,'event_type': 2,'killer_assisters': [],'injured_faction': -5,'death_source': [1,
                          {'maker_type': 2,'mecha_id': 8008,'skin_id': 201800851,
                             'trigger_parts': [1],'hit_head': False,
                             'trigger_faction': 1,'points': None,
                             'trigger_id': ObjectId('6254e69178cddf7cdf00de17'),
                             'die_pos': [-306.573486328125, 246.8636016845703, 433.5661926269531],'item_id': 800802,
                             'trigger_name': '\xe5\xad\x97\xe5\x85\xab\xe4\xb8\xaa\xe5\xad\x97\xe4\xbd\x86',
                             'item_eid': 0
                             }],
           'injured_id': ObjectId('62593fa178cddf54075a6d34'),
           'no_kill_camera': False,'points': None}
        self.show_battle_report(a)
        return

    def test_4(self):
        from bson.objectid import ObjectId
        b = {'is_defeated_valid': False,'injured_name': '\xe7\x8e\xa9\xe5\xae\xb6\xe5\x90\x8d\xe5\xad\x97\xe5\x85\xab\xe7\xbb\x99\xe4\xb8\xaa\xe5\xad\x97','bleed_source': None,'event_type': 2,'killer_assisters': [],'injured_faction': -5,'death_source': [1,
                          {'maker_type': 2,'mecha_id': 8008,'trigger_parts': [
                                             1],
                             'hit_head': False,
                             'trigger_faction': 1,
                             'points': None,
                             'trigger_id': ObjectId('6254e69178cddf7cdf00de17'),
                             'die_pos': [-306.573486328125, 246.8636016845703, 433.5661926269531],'item_id': 800802,
                             'trigger_name': '\xe6\x9d\x80\xe6\x89\x8b\xe5\x90\x8d\xe5\xad\x97\xe5\x85\xab\xe4\xb8\xaa\xe5\xad\x97\xe4\xbd\x86',
                             'item_eid': 0
                             }],
           'injured_id': ObjectId('62593fa178cddf54075a6d34'),
           'no_kill_camera': False,'points': None}
        self.show_battle_report(b)
        return

    def test_mvp(self, name='BigBrother', is_groupmate=True):
        from bson.objectid import ObjectId
        mvp_msg = ({'name': name,'killer_id': ObjectId('5fa38b071876eb2bd0f32ec1'),'msg_type': 4,'is_groupmate': is_groupmate}, None, None)
        self.battle_report_queue.append(mvp_msg)
        self._show_next_battle_report()
        return

    def get_message_nd_height(self, nd):
        _height = TIP_HEIGHT
        if not nd or not nd.rt_msg or nd.rt_msg.msg_type is None:
            _height = TIP_HEIGHT
        else:
            children = nd.nd_kill_message.getChildren()
            if children:
                _height = children[0].getContentSize().height
        return _height

    def _show_next_battle_report(self):
        MAX_ON_FLY_NUM = 4
        _on_fly_battle_report_num = len(self._on_fly_msg_nds)

        def get_cur_tips_pos_y(index, cur_nd, from_index=0):
            START_POS = 13
            height = self.panel.kill_message.getContentSize().height
            sum_height = 0
            first_height = 0
            sz_queue = self._history_node_size_queue[-self._cur_battle_report_show_index:]
            for i in range(from_index, index):
                if i < len(sz_queue):
                    _height = sz_queue[i]
                    if i == from_index:
                        sum_height += _height / 2.0
                    else:
                        sum_height += _height
                else:
                    log_error('get_cur_tips_pos_y failed to find node height???????', index, self._cur_battle_report_show_index, self._history_node_size_queue)

            cur_height = self.get_message_nd_height(cur_nd)
            half_cur = 0
            if index > from_index:
                half_cur = cur_height / 2.0
            pos_y = height - START_POS - sum_height - half_cur
            return pos_y

        if not self.can_showing_battle_report:
            return
        else:

            def get_msg_show_action(slow_appear=False):
                check_time = 0
                if not slow_appear:
                    act0 = cc.ScaleTo.create(0.3, 1, 1)
                    check_time = 0.3
                else:
                    act0 = cc.ScaleTo.create(0.4, 1, 1)
                    check_time = 0.4
                act1 = cc.DelayTime.create(0.4)
                check_time += 0.4
                self.panel.kill_message.SetTimeOut(check_time, self.check_next_battle_report)
                delay_act2 = cc.DelayTime.create(3)
                act2_5 = cc.Spawn.create([cc.ScaleTo.create(0.3, 1, 0), cc.FadeTo.create(0.3, 0)])
                act3 = cc.CallFunc.create(self.finish_show_battle_report)
                acts = cc.Sequence.create([act0, act1, delay_act2, act2_5, act3])
                return acts

            if len(self.battle_report_queue) > 0:
                msg_nd = self._get_free_message_node()
                if msg_nd is None or not msg_nd.nd_message:
                    return
                msg, color_str, killer_id = self.battle_report_queue.pop(0)
                text_align = 2 if global_data.is_pc_mode else 0
                right_offset = -10 if global_data.is_pc_mode else 0
                if isinstance(msg, dict):
                    self.add_node_by_type(msg_nd.nd_message, msg, text_align)
                else:
                    self.add_rich_text_str(msg_nd.nd_message, msg, color_str, text_align, extra_right_x_offset=right_offset)

                @msg_nd.nd_message.callback()
                def OnClick(btn, touch, killer_id=killer_id):
                    if global_data.is_judge_ob:
                        if killer_id:
                            from logic.gutils.judge_utils import try_switch_ob_target
                            try_switch_ob_target(killer_id)

                if self._cur_battle_report_show_index < MAX_ON_FLY_NUM:
                    self.can_showing_battle_report = False
                    msg_nd.setVisible(True)
                    msg_nd.ReConfPosition()
                    msg_nd.SetPosition(msg_nd.getPositionX(), get_cur_tips_pos_y(self._cur_battle_report_show_index, msg_nd.nd_message))
                    msg_nd.setScaleY(0)
                    msg_nd.setOpacity(255)
                    acts = get_msg_show_action()
                    msg_nd.stopAllActions()
                    msg_nd.runAction(acts)
                    self._on_fly_msg_nds.append(msg_nd)
                    self._history_node_size_queue.append(self.get_message_nd_height(msg_nd.nd_message))
                    self._cur_battle_report_show_index += 1
                elif self._cur_battle_report_show_index >= MAX_ON_FLY_NUM:
                    first_and_sec_mid_point_dist = TIP_HEIGHT
                    if len(self._history_node_size_queue) >= MAX_ON_FLY_NUM:
                        first_and_sec_mid_point_dist = self._history_node_size_queue[-MAX_ON_FLY_NUM] / 2.0 + self._history_node_size_queue[-MAX_ON_FLY_NUM + 1] / 2.0
                    for idx, other_msg_nd in enumerate(self._on_fly_msg_nds):
                        if len(self._on_fly_msg_nds) >= MAX_ON_FLY_NUM and idx == 0:
                            other_msg_nd.stopAllActions()
                            act = cc.MoveBy.create(0.3, ccp(0, first_and_sec_mid_point_dist / 2.0))
                            act2_5 = cc.Spawn.create([
                             act, cc.ScaleTo.create(0.3, 1, 0), cc.FadeTo.create(0.3, 0)])
                            act3 = cc.CallFunc.create(self.finish_show_battle_report)
                            acts = cc.Sequence.create([act2_5, act3])
                            other_msg_nd.runAction(acts)
                        else:
                            other_msg_nd.runAction(cc.MoveBy.create(0.3, ccp(0, first_and_sec_mid_point_dist)))

                    self.can_showing_battle_report = False
                    msg_nd.ReConfPosition()
                    msg_nd.setVisible(True)
                    msg_nd.setScaleY(0)
                    node_pos_y = get_cur_tips_pos_y(MAX_ON_FLY_NUM, msg_nd.nd_message, from_index=1)
                    msg_nd.SetPosition(msg_nd.getPositionX(), node_pos_y)
                    self._cur_battle_report_show_index = MAX_ON_FLY_NUM
                    msg_nd.setOpacity(255)
                    acts = get_msg_show_action(True)
                    msg_nd.stopAllActions()
                    msg_nd.runAction(acts)
                    self._on_fly_msg_nds.append(msg_nd)
                    self._history_node_size_queue.append(self.get_message_nd_height(msg_nd.nd_message))
            return

    def finish_show_battle_report(self):
        msg_nd = self._on_fly_msg_nds.pop(0)
        msg_nd.stopAllActions()
        msg_nd.setVisible(False)
        if len(self._on_fly_msg_nds) == 0:
            self._cur_battle_report_show_index = 0
            self._history_node_size_queue = []
        self._on_fly_battle_report_num -= 1
        self.message_nd_pool.append(msg_nd)
        self._show_next_battle_report()

    def check_next_battle_report(self):
        self.can_showing_battle_report = True
        self._show_next_battle_report()

    def _get_free_message_node(self):
        if len(self.message_nd_pool) > 0:
            return self.message_nd_pool.pop()
        else:
            return None
            return None

    def on_enter_observed(self, ltarget):
        self.is_in_observe = True
        self.on_player_setted(ltarget)

    def parse_battle_report(self, report_dict):
        from .BattleInfo.BattleReportParser import BattleReportParser
        return BattleReportParser().parse_battle_report(report_dict)

    def get_report_dict_killer_id(self, report_dict):
        from .BattleInfo.BattleReportParser import BattleReportParser
        killer_name, killer_id, killer_weap_id, bleed_damage_type, killer_damage_type, trigger_parts, mecha_id, damage_type, tigger_other_info = BattleReportParser()._parse_report_data(report_dict)
        return killer_id

    def move_survive_ui_from_time_stamp--- This code section failed: ---

 562       0  LOAD_FAST             3  'tag'
           3  LOAD_CONST            0  ''
           6  COMPARE_OP            9  'is-not'
           9  POP_JUMP_IF_FALSE   124  'to 124'

 563      12  LOAD_GLOBAL           1  'getattr'
          15  LOAD_GLOBAL           1  'getattr'
          18  LOAD_CONST            0  ''
          21  CALL_FUNCTION_3       3 
          24  POP_JUMP_IF_TRUE     39  'to 39'

 564      27  BUILD_MAP_0           0 
          30  LOAD_FAST             0  'self'
          33  STORE_ATTR            2  'move_by_tag'
          36  JUMP_FORWARD          0  'to 39'
        39_0  COME_FROM                '36'

 565      39  LOAD_FAST             3  'tag'
          42  LOAD_FAST             0  'self'
          45  LOAD_ATTR             2  'move_by_tag'
          48  COMPARE_OP            6  'in'
          51  POP_JUMP_IF_FALSE    96  'to 96'

 566      54  LOAD_FAST             1  'move_down'
          57  POP_JUMP_IF_FALSE    80  'to 80'

 567      60  LOAD_FAST             2  'move_dist'
          63  LOAD_FAST             0  'self'
          66  LOAD_ATTR             2  'move_by_tag'
          69  LOAD_FAST             3  'tag'
          72  BINARY_SUBSCR    
          73  INPLACE_SUBTRACT 
          74  STORE_FAST            2  'move_dist'
          77  JUMP_ABSOLUTE        96  'to 96'

 569      80  LOAD_FAST             0  'self'
          83  LOAD_ATTR             2  'move_by_tag'
          86  LOAD_FAST             3  'tag'
          89  BINARY_SUBSCR    
          90  STORE_FAST            2  'move_dist'
          93  JUMP_FORWARD          0  'to 96'
        96_0  COME_FROM                '93'

 570      96  LOAD_FAST             1  'move_down'
          99  POP_JUMP_IF_FALSE   108  'to 108'
         102  LOAD_FAST             2  'move_dist'
         105  JUMP_FORWARD          3  'to 111'
         108  LOAD_CONST            2  ''
       111_0  COME_FROM                '105'
         111  LOAD_FAST             0  'self'
         114  LOAD_ATTR             2  'move_by_tag'
         117  LOAD_FAST             3  'tag'
         120  STORE_SUBSCR     
         121  JUMP_FORWARD          0  'to 124'
       124_0  COME_FROM                '121'

 571     124  LOAD_FAST             0  'self'
         127  LOAD_ATTR             3  'panel'
         130  LOAD_ATTR             4  'kill_message'
         133  LOAD_ATTR             5  'getPosition'
         136  CALL_FUNCTION_0       0 
         139  STORE_FAST            4  'now_pos'

 572     142  LOAD_FAST             1  'move_down'
         145  POP_JUMP_IF_FALSE   183  'to 183'

 573     148  LOAD_FAST             0  'self'
         151  LOAD_ATTR             3  'panel'
         154  LOAD_ATTR             4  'kill_message'
         157  LOAD_ATTR             6  'SetPosition'
         160  LOAD_FAST             4  'now_pos'
         163  LOAD_ATTR             7  'x'
         166  LOAD_FAST             4  'now_pos'
         169  LOAD_ATTR             8  'y'
         172  LOAD_FAST             2  'move_dist'
         175  BINARY_SUBTRACT  
         176  CALL_FUNCTION_2       2 
         179  POP_TOP          
         180  JUMP_FORWARD         32  'to 215'

 575     183  LOAD_FAST             0  'self'
         186  LOAD_ATTR             3  'panel'
         189  LOAD_ATTR             4  'kill_message'
         192  LOAD_ATTR             6  'SetPosition'
         195  LOAD_FAST             4  'now_pos'
         198  LOAD_ATTR             7  'x'
         201  LOAD_FAST             4  'now_pos'
         204  LOAD_ATTR             8  'y'
         207  LOAD_FAST             2  'move_dist'
         210  BINARY_ADD       
         211  CALL_FUNCTION_2       2 
         214  POP_TOP          
       215_0  COME_FROM                '180'

 576     215  LOAD_GLOBAL           9  'True'
         218  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 21

    def on_player_gulag_state_changed(self, game_id, **kwargs):
        from logic.gcommon.common_const.battle_const import REVIVE_NONE
        if game_id == REVIVE_NONE:
            self.add_show_count('gulag')
        else:
            self.add_hide_count('gulag')


class SurviveInfoUIPC(SurviveInfoUI):

    def get_mvp_template(self):
        return bconst.COMMON_SURVIVAL_KILL_MVP_MESSAGE_PC

    def get_ss_msg_type(self):
        return bconst.COMMON_SURVIVAL_SS_KILL_MESSAGE_PC