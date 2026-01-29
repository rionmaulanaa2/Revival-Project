# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/TeammateStatusWidget.py
from __future__ import absolute_import
import six
from six.moves import range
from .TeammateWidget.TeammateWidget import TeammateBloodBarUI2, TeammateStatusUI2, TeammateParachuteStatusUI, TeammateFollowInfoUI
from .TeamBloodUI import TeammateMarkUI
from logic.gutils.role_head_utils import init_role_head_by_id
from logic.comsys.common_ui.CommonTips import TipsManager
from logic.comsys.chat.FightChatUI import FightChatTips
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.item_utils import get_item_name
from logic.gutils import chat_utils

class TeammateStatusWidget(object):

    def __init__(self, panel):
        self.panel = panel
        self.player = None
        self.following_id = None
        self.teammate_ids = []
        self._teammate_ref = {}
        self.teammate_maps = {}
        self.eid_to_id_dict = dict()
        self.init_events()
        self.start_tick()
        if global_data.cam_lplayer:
            self.on_player_setted(global_data.cam_lplayer)
        elif global_data.player and global_data.player.logic:
            self.on_player_setted(global_data.player.logic)
        return

    def destroy(self):
        self.clear_all_players()
        self.process_events(False)
        self.player = None
        self.panel = None
        return

    def init_events(self):
        self.process_events(True)

    def process_events(self, is_bind):
        emgr = global_data.emgr
        econf = {'add_teammate_blood_event': self.add_teammate,
           'scene_camera_player_setted_event': self.on_observe_player_setted,
           'ccmini_team_speaking_list': self.refresh_team_speak,
           'scene_on_teammate_change': self.on_teammate_member_change,
           'scene_player_setted_event': self.on_player_setted,
           'add_battle_group_msg_event': self.on_receive_msg
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def start_tick(self):
        self.update_teammate_status()
        import cc
        self.panel.runAction(cc.RepeatForever.create(cc.Sequence.create([
         cc.CallFunc.create(self.update_teammate_status),
         cc.DelayTime.create(0.1)])))

    def init_observe_player(self, lplayer):
        self.player = lplayer
        self.clear_all_players()
        if not lplayer:
            self.panel.list_teammate.setVisible(False)
            return
        self.panel.list_teammate.setVisible(True)
        teammates = lplayer.ev_g_groupmate()
        teammate_infos = lplayer.ev_g_teammate_infos()
        import copy
        teammate_ids = copy.deepcopy(teammates) or []
        teammate_ids.sort()
        self.set_teammates(teammate_ids, teammate_infos)
        self.set_btn_follow(teammate_ids)

    def clear_all_players(self):
        self.teammate_ids = []
        for tid, t_info in six.iteritems(self.teammate_maps):
            _, bloodbar_ui, state_ui, mark_ui, parachute_ui, follow_ui, tips_manager = t_info
            bloodbar_ui.destroy()
            state_ui.destroy()
            mark_ui.destroy()
            parachute_ui.destroy()
            follow_ui.destroy()
            tips_manager.destroy()

        self.teammate_maps = {}
        self.eid_to_id_dict.clear()

    def set_teammates(self, teammate_ids, teammate_infos):
        from logic.gutils.team_utils import get_teammate_colors
        player_col = get_teammate_colors(teammate_ids)
        self.teammate_ids = teammate_ids
        self.teammate_ids.sort()
        self.eid_to_id_dict.clear()
        for idx, tid in enumerate(self.teammate_ids):
            self.eid_to_id_dict[tid] = idx

        self.panel.list_teammate.SetInitCount(len(self.teammate_ids))
        all_teammate_ui = self.panel.list_teammate.GetAllItem()
        from logic.gcommon.common_const.battle_const import PLAY_TYPE_RECRUITMENT
        from logic.gcommon.common_utils.battle_utils import get_play_type_by_battle_id
        if global_data.battle and get_play_type_by_battle_id(global_data.battle.get_battle_tid()) == PLAY_TYPE_RECRUITMENT:
            self.panel.list_teammate.SetInitCount(3)
            all_teammate_ui = self.panel.list_teammate.GetAllItem()
            for idx in range(len(self.teammate_ids), 3):
                teammate_ui = all_teammate_ui[idx]
                self.set_up_empty_teammate_node(teammate_ui, idx)

        for idx, tid in enumerate(self.teammate_ids):
            teammate_ui = all_teammate_ui[idx]
            t_dic_info = teammate_infos.get(tid, {})
            from logic.gcommon.common_const.battle_const import MAP_COL_BLUE
            self.bind_teammate_ui(teammate_ui, tid, player_col.get(tid, MAP_COL_BLUE), len(teammate_ids) != 1, self.eid_to_id_dict, t_dic_info)

    def set_up_empty_teammate_node(self, node, idx):
        node.nd_follow_set.setVisible(False)
        teammate_ui = node.temp_status
        teammate_ui.sp_locate.SetDisplayFrameByPath('', 'gui/ui_res_2/battle_recruit/icon_teammate_num%d_grey.png' % (idx + 1))
        teammate_ui.img_bar.SetDisplayFrameByPath('', 'gui/ui_res_2/battle_recruit/pnl_team_list_grey.png')
        teammate_ui.hp_progress.SetPercentage(0)
        teammate_ui.img_jump.setVisible(False)
        teammate_ui.nd_teamate_name.teamate_name.SetString(83160)

    def _show_follow_button(self, btn):
        self.panel.nd_back.setVisible(True)
        if self.panel.nd_back.getOpacity() == 0:
            self.panel.StopAnimation('shouqi')
            self.panel.PlayAnimation('zhankai')
            for eid, wrapper in six.iteritems(self.teammate_maps):
                wrapper[5].set_follow_btn(self.get_entity(eid))

            btn.img_jiao2.setScaleX(0.9)

    def _hide_follow_button(self, btn):
        if self.panel.nd_back.getOpacity() == 255:
            self.panel.StopAnimation('zhankai')
            self.panel.PlayAnimation('shouqi')
            for eid, wrapper in six.iteritems(self.teammate_maps):
                wrapper[5].hide_follow_btn()

            btn.img_jiao2 and btn.img_jiao2.setScaleX(-0.9)

    def set_btn_follow(self, teammate_ids):
        in_group = len(teammate_ids) != 1
        self.panel.btn_follow_set.setVisible(in_group)
        self.panel.StopAnimation('follow_tips')
        self.panel.nd_back.setVisible(False)
        self.panel.nd_back.setOpacity(0)
        if in_group:
            if len(teammate_ids) == 2:
                size = self.panel.nd_back.img_follow_bg.getContentSize()
                self.panel.nd_back.img_follow_bg.SetContentSize(size.width, 106)
                self.panel.nd_back.img_follow_bg.ChildResizeAndPosition()
            self.panel.PlayAnimation('follow_tips')

            @self.panel.btn_follow_set.unique_callback()
            def OnClick(btn, touch, *args):
                opacity = self.panel.nd_back.getOpacity()
                if opacity == 0:
                    self._show_follow_button(btn)
                elif opacity == 255:
                    self._hide_follow_button(btn)

            @self.panel.btn_shouqi.unique_callback()
            def OnClick(btn, touch, *args):
                self._hide_follow_button(btn)

            self.update_btn_follow(force_update=True)

    def update_btn_follow(self, force_update=False):
        if not self.player:
            if not global_data.cam_lplayer:
                return
            self.player = global_data.cam_lplayer
        follow_id = self.player.ev_g_parachute_follow_target()
        not_following = follow_id is None
        is_followed = self.player.ev_g_has_parachute_follower()
        if not (follow_id != self.following_id and follow_id) and is_followed == self.panel.btn_follow_set.nd_follow_leader.isVisible() and not_following == self.panel.lab_none.isVisible() and not force_update:
            return
        else:
            self.following_id = follow_id
            self.panel.nd_follow_leader.setVisible(is_followed)
            self.panel.nd_follow.setVisible(not not_following)
            self.panel.lab_none.setVisible(not_following and not is_followed)
            if not is_followed and not not_following:
                ID_PIC_PATH = ['gui/ui_res_2/battle/icon/icon_teammate_num_blue.png',
                 'gui/ui_res_2/battle/icon/icon_teammate_num_green.png',
                 'gui/ui_res_2/battle/icon/icon_teammate_num_yellow.png',
                 'gui/ui_res_2/battle/icon/icon_teammate_num_red.png']
                lent = self.get_entity(follow_id)
                if lent and follow_id in self.eid_to_id_dict:
                    self.panel.lab_player_name.SetString(lent.ev_g_char_name() or '')
                    pic_path = ID_PIC_PATH[self.eid_to_id_dict[follow_id]]
                    self.panel.img_num.SetDisplayFrameByPath('', pic_path)
                else:
                    self.following_id = None
            return

    def bind_teammate_ui(self, node, teammate_id, color, has_teammate, eid_to_id_dict, t_dic_info):
        node_wrapper = self.setup_teammate_node(node, teammate_id, color, has_teammate, eid_to_id_dict, t_dic_info)
        self.teammate_maps[teammate_id] = node_wrapper

    def setup_teammate_node(self, node, teammate_id, color, has_teammate, eid_to_id_dict, t_dic_info):
        from logic.gutils.intimacy_utils import init_intimacy_icon_with_uid
        lent = self.get_entity(teammate_id)
        wrapper = [
         node,
         TeammateBloodBarUI2(node.temp_status, color),
         TeammateStatusUI2(node.temp_status, color),
         TeammateMarkUI(node.img_mark, color, teammate_id),
         TeammateParachuteStatusUI(node),
         TeammateFollowInfoUI(node, has_teammate, teammate_id, eid_to_id_dict),
         TipsManager(node.temp_status.temp_teammate_message, FightChatTips, color, preload_tip_num=2)]
        _, bloodbar_ui, state_ui, mark_ui, _, follow_ui, _ = wrapper
        name_node = self.get_name_node_with_eid(node, teammate_id)
        if lent:
            name = lent.ev_g_char_name()
            head_frame = lent.ev_g_head_frame()
            if name:
                name_node.SetString(name)
                init_role_head_by_id(node.temp_head, head_frame, lent.ev_g_role_id())
            mark_ui.init_by_teammate(lent)
            follow_ui.init_by_teammate(lent)
        else:
            char_name = t_dic_info.get('char_name', '')
            head_frame = t_dic_info.get('head_frame', 0)
            name_node.SetString(char_name)
            init_role_head_by_id(node.temp_head, head_frame, t_dic_info.get('role_id', 0))
            bloodbar_ui.init_by_teammate_dict(t_dic_info)
            state_ui.init_by_teammate_dict(t_dic_info)
            follow_ui.init_by_teammate(t_dic_info)
        return wrapper

    def update_teammate_status(self):
        for tid, t_info in six.iteritems(self.teammate_maps):
            lent = self.get_entity(tid)
            _, bloodbar_ui, state_ui, mark_ui, parachute_ui, follow_ui, _ = t_info
            if lent:
                mark_ui.init_by_teammate(lent)
                bloodbar_ui.update_health(lent)
                state_ui.update_status(lent)
                parachute_ui.update_status(lent)
                follow_ui.update_status(lent)
            else:
                mark_ui.update_teammate_mark(None)
                state_ui.update_status(None)
                bloodbar_ui.update_health(None)
                parachute_ui.update_status(None)
                follow_ui.update_status(None)

        self.update_btn_follow()
        return

    def get_entity(self, tid):
        t_ent = None
        if tid in self._teammate_ref:
            t_ent = self._teammate_ref[tid]()
            if not (t_ent and t_ent.is_valid()):
                del self._teammate_ref[tid]
                t_ent = None
        if not t_ent:
            import weakref
            from mobile.common.EntityManager import EntityManager
            ent = EntityManager.getentity(tid)
            if ent and ent.logic:
                self._teammate_ref[tid] = weakref.ref(ent.logic)
                t_ent = ent.logic
        return t_ent

    def add_teammate(self, lent):
        if lent:
            if lent.id in self.teammate_maps:
                node, _, _, mark_ui, _, follow_ui, _ = self.teammate_maps[lent.id]
                name_node = self.get_name_node_with_eid(node, lent.id)
                name_node.SetString(lent.ev_g_char_name())
                mark_ui.init_by_teammate(lent)

    def refresh_team_speak(self, session_id, all_list, all_energy):
        from logic.gcommon.common_utils import ui_gameplay_utils as ui_utils
        if all_list:
            for index, eid in enumerate(all_list):
                entity_id = global_data.ccmini_mgr.get_entity_id_by_eid(eid, session_id=session_id)
                player_node, _, _, _, _, follow_ui, _ = self.teammate_maps.get(entity_id, (None,
                                                                                           None,
                                                                                           None,
                                                                                           None,
                                                                                           None,
                                                                                           None,
                                                                                           None))
                if player_node:
                    voice = player_node.temp_status.voice
                    energy_level = ui_utils.get_energy_level(all_energy[index])
                    voice.setVisible(True)
                    for i in range(3):
                        img_voice = getattr(voice, 'voice_%d' % (i + 1), None)
                        if img_voice:
                            if i + 1 <= energy_level:
                                img_voice.setVisible(True)
                            else:
                                img_voice.setVisible(False)

        else:
            for t_info in six.itervalues(self.teammate_maps):
                player_node, _, _, _, _, follow_ui, _ = t_info
                if player_node:
                    voice = player_node.temp_status.voice
                    voice.setVisible(False)

        return

    def on_receive_msg(self, unit_id, char_name, data):
        dmsg = data.get('msg', {})
        if 'text' in dmsg:
            chat_utils.format_msg_data(dmsg)
            _, _, _, _, _, _, chat_tip_mgr = self.teammate_maps.get(unit_id, (None,
                                                                              None,
                                                                              None,
                                                                              None,
                                                                              None,
                                                                              None,
                                                                              None))
            if chat_tip_mgr:
                self.add_chat_board_text(chat_tip_mgr, dmsg)
        return None

    def add_chat_board_text(self, chat_tip_mgr, dmsg):
        if chat_tip_mgr:
            chat_tip_mgr.add_tips(dmsg)

    def on_teammate_member_change(self, unit_id):
        if self.player and unit_id == self.player.id:
            self.init_observe_player(self.player)

    def on_player_setted(self, lplayer):
        self.init_observe_player(lplayer)

    def on_observe_player_setted(self):
        self.on_player_setted(global_data.cam_lplayer)

    def get_name_node_with_eid(self, node, eid):
        from logic.gutils.intimacy_utils import init_intimacy_icon_with_uid
        teammate_infos = self.player.ev_g_teammate_infos()
        uid = teammate_infos.get(eid, {}).get('uid', None)
        if uid is None:
            show_intimacy = False
        else:
            show_intimacy = init_intimacy_icon_with_uid(node.temp_status.temp_intimacy, uid, show_level=False)
        node.temp_status.nd_teamate_name.teamate_name.setVisible(not show_intimacy)
        name_node = node.temp_status.temp_intimacy.teamate_name if show_intimacy else node.temp_status.nd_teamate_name.teamate_name
        return name_node