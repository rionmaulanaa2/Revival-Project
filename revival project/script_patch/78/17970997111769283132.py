# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/observe_ui/JudgeTeamBloodUI.py
from __future__ import absolute_import
import six
from common.uisys.basepanel import BasePanel
from common.const.uiconst import ROCKER_LAYER_ZORDER
from logic.comsys.battle.TeammateWidget.TeammateWidget import TeammateBloodBarUI2, JudgeTeammateStatusUI
import common.utils.timer as timer
from logic.comsys.ui_distortor.UIDistortHelper import UIDistorterHelper
from logic.comsys.ui_distortor.MechaDistortHelper import MechaDistortHelper
from logic.gutils import judge_utils
from common.const import uiconst

class JudgeTeamBloodUI(MechaDistortHelper, BasePanel):
    PANEL_CONFIG_NAME = 'battle/fight_teammate_judgement'
    DLG_ZORDER = ROCKER_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT

    def on_init_panel(self):
        super(JudgeTeamBloodUI, self).on_init_panel()
        global_data.ui_mgr.close_ui('TeamBloodUI')
        self.teammate_ids = []
        self._teammate_ref = {}
        self.teammate_maps = {}
        self.disapear_timer_maps = {}
        self.init_observe_player()
        self.process_event(True)
        self.start_tick()
        self._init_stat_widget()
        self._update_judge_need_hide_details()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'add_teammate_blood_event': self.add_teammate,
           'scene_camera_player_setted_event': self.init_observe_player,
           'scene_on_teammate_change': self.on_teammate_member_change,
           'judge_need_hide_details_event': self._update_judge_need_hide_details
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def start_tick(self):
        import cc
        self.panel.runAction(cc.RepeatForever.create(cc.Sequence.create([
         cc.CallFunc.create(self.update_teammate_status),
         cc.DelayTime.create(1.0)])))

    def init_observe_player(self):
        self.clear_all_players()
        observe_player = global_data.cam_lplayer
        if not observe_player:
            self.panel.nd_team_statue.setVisible(False)
            return
        self.panel.nd_team_statue.setVisible(True)
        teammates = observe_player.ev_g_groupmate()
        teammate_infos = observe_player.ev_g_teammate_infos()
        import copy
        teammate_ids = copy.deepcopy(teammates) or []
        teammate_ids.sort()
        for tid in teammates:
            finish_battle = teammate_infos.get(tid, {}).get('finish_battle', False)
            if finish_battle:
                teammate_ids.remove(tid)

        self.set_teammates(teammate_ids, teammate_infos)

    def clear_all_players(self):
        self.teammate_ids = []
        self.clear_teamate_ui()
        self.clear_del_timers()

    def clear_teamate_ui(self):
        for tid, t_info in six.iteritems(self.teammate_maps):
            _, bloodbar_ui, state_ui = t_info
            bloodbar_ui.destroy()
            state_ui.destroy()

        self.teammate_maps = {}

    def set_teammates(self, teammate_ids, teammate_infos):
        from logic.gutils.team_utils import get_teammate_colors
        if not global_data.cam_lplayer:
            return
        else:
            all_teammates = global_data.cam_lplayer.ev_g_groupmate()
            player_col = get_teammate_colors(all_teammates)
            self.teammate_ids = teammate_ids
            self.teammate_ids.sort()
            self.panel.lv_teammate.SetInitCount(len(self.teammate_ids))
            all_teammate_ui = self.panel.lv_teammate.GetAllItem()
            for idx, tid in enumerate(self.teammate_ids):
                teammate_ui = all_teammate_ui[idx]
                t_dic_info = teammate_infos.get(tid, {})
                from logic.gcommon.common_const.battle_const import MAP_COL_BLUE
                self.bind_teammate_ui(teammate_ui, tid, player_col.get(tid, MAP_COL_BLUE), t_dic_info)
                teammate_ui.nd_choosing.setVisible(global_data.cam_lplayer is not None and global_data.cam_lplayer.id == tid)
                teammate_ui.player._secret_player_id_ = tid

                @teammate_ui.player.unique_callback()
                def OnClick(btn, touch):
                    judge_utils.try_switch_ob_target(btn._secret_player_id_)

            return

    def bind_teammate_ui(self, node, teammate_id, color, t_dic_info):
        lent = self.get_entity(teammate_id)
        self.teammate_maps[teammate_id] = [node, TeammateBloodBarUI2(node, color), JudgeTeammateStatusUI(node, color)]
        if lent:
            name = lent.ev_g_char_name()
            if name:
                node.teamate_name.SetString(name)
            _, bloodbar_ui, state_ui = self.teammate_maps[teammate_id]
        else:
            char_name = t_dic_info.get('char_name', '')
            node.teamate_name.SetString(char_name)
            _, bloodbar_ui, state_ui = self.teammate_maps[teammate_id]
            bloodbar_ui.init_by_teammate_dict(t_dic_info)
            state_ui.init_by_teammate_dict(t_dic_info)

    def update_teammate_status(self):
        del_player_ids = []
        if not global_data.cam_lplayer:
            return
        else:
            teammate_infos = global_data.cam_lplayer.ev_g_teammate_infos()
            for tid, t_info in six.iteritems(self.teammate_maps):
                lent = self.get_entity(tid)
                if lent:
                    _, bloodbar_ui, state_ui = t_info
                    bloodbar_ui.update_health(lent)
                    state_ui.update_status(lent, tid)
                else:
                    _, bloodbar_ui, state_ui = t_info
                    state_ui.update_status(None, None)
                    bloodbar_ui.update_health(None)
                if teammate_infos:
                    finish_battle = teammate_infos.get(tid, {}).get('finish_battle', False)
                    if finish_battle:
                        del_player_ids.append(tid)

            self.delay_to_disapear_player(del_player_ids)
            return

    def delay_to_disapear_player(self, def_tids):
        tm = global_data.game_mgr.get_logic_timer()
        for tid in def_tids:
            del_timer = self.disapear_timer_maps.get(tid, None)
            if del_timer:
                continue
            self.disapear_timer_maps[tid] = tm.register(func=self.del_player, args=(tid,), interval=10, times=1, mode=timer.CLOCK)

        return

    def del_player(self, player_id):
        self.disapear_timer_maps.pop(player_id)
        self.clear_teamate_ui()
        self.teammate_ids.remove(player_id)
        observe_player = global_data.cam_lplayer
        if not observe_player:
            self.panel.nd_team_statue.setVisible(False)
            return
        self.panel.nd_team_statue.setVisible(True)
        teammate_infos = observe_player.ev_g_teammate_infos()
        self.set_teammates(self.teammate_ids, teammate_infos)

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
                node, _, _ = self.teammate_maps[lent.id]
                node.teamate_name.SetString(lent.ev_g_char_name())

    def on_finalize_panel(self):
        self.clear_all_players()
        self.process_event(False)
        self.destroy_widget('_survive_widget')

    def clear_del_timers(self):
        tm = global_data.game_mgr.get_logic_timer()
        for del_timer in six.itervalues(self.disapear_timer_maps):
            if del_timer:
                tm.unregister(del_timer)

        self.disapear_timer_maps = {}

    def on_teammate_member_change(self, unit_id):
        if global_data.cam_lplayer and unit_id == global_data.cam_lplayer.id:
            self.init_observe_player()

    def on_change_ui_custom_data(self):
        if self._in_mecha_state:
            UIDistorterHelper().apply_ui_distort(self.__class__.__name__)

    def _is_solo_battle(self):
        if global_data.player:
            bat = global_data.player.get_battle()
            if bat:
                return bat.is_single_person_battle()
        return True

    def _init_stat_widget(self):
        from logic.comsys.battle.BattleInfo.SurviveWidget import SurviveWidget
        self._survive_widget = SurviveWidget(team_kill_num_changed=self._on_team_kill_num_changed, team_kill_mecha_num_changed=self._on_team_kill_mecha_num_changed)
        if self._is_solo_battle():
            text_id = 80640
        else:
            text_id = 19612
        self.panel.lab_all.SetString(text_id)

    def _on_team_kill_num_changed(self, num):
        self.panel.lab_kill_num.SetString(str(num))

    def _on_team_kill_mecha_num_changed(self, num):
        self.panel.lab_mech_num.SetString(str(num))

    def _update_judge_need_hide_details(self):
        self.panel.nd_team_stat.setVisible(not global_data.judge_need_hide_details)