# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/observe_ui/ScopePlayerUI.py
from __future__ import absolute_import
import six_ex
import weakref
from common.utils.cocos_utils import getScreenSize
import cc
import math3d
from logic.gcommon.const import NEOX_UNIT_SCALE
import math
from logic.gutils.team_utils import limit_pos_in_screen, get_dist_in_rect_angle
from mobile.common.EntityManager import EntityManager
from logic.gutils.team_utils import is_judge_group
from common.utils.cocos_utils import neox_pos_to_cocos
from common.utils.cocos_utils import cocos_screen_pos_to_cocos_design_pos
import world
from common.utils.cocos_utils import ccp
from logic.comsys.battle.TeammateWidget.TeammateWidget import TeammateBloodBarUI2
from logic.gutils.client_unit_tag_utils import register_unit_tag
OLD_MECHA_VEHICLE_TAG_VALUE = register_unit_tag(('LMecha', 'LMechaTrans'))

class PlayerHeadUI(object):

    def __init__(self, nd, pid, panel):
        self._nd = nd
        self.panel = panel
        self.pid = pid
        self._in_mecha = False
        scn = global_data.game_mgr.scene
        self.cam = weakref.ref(scn.active_camera)
        self.screen_size = getScreenSize()
        from logic.gcommon.common_const.battle_const import MAP_COL_WHITE
        self._hp_bar_widget = TeammateBloodBarUI2(nd, MAP_COL_WHITE)
        self.init_node()

    def _get_lplayer(self):
        ent = EntityManager.getentity(self.pid)
        if not (ent and ent.logic):
            return None
        else:
            return ent.logic

    def _get_player_info(self):
        return judge_utils.nb_get_player_info(self.pid)

    def init_node(self):
        player_info = self._get_player_info()
        name = player_info.get('char_name', '')
        self._nd.lab_name.SetString(name)
        group_id = player_info.get('group', -1)
        from logic.comsys.observe_ui.JudgeObservationListWidget import JudgeObservationListWidget
        if group_id != -1 and group_id is not None:
            self._nd.img_bg.SetDisplayFrameByPath('', JudgeObservationListWidget.get_team_bg_img_path(group_id, False))
        self._nd.lab_team_no.SetString(str(group_id))

        @self._nd.btn_watch.callback()
        def OnClick(btn, touch):
            from logic.gutils.judge_utils import try_switch_ob_target
            try_switch_ob_target(self.pid)

        self._init_node_show_internal()
        self.refresh()
        return

    def refresh(self):
        self.update_pos_and_scale()
        self.update_health()

    def _init_node_show_internal(self):
        if self._in_pure_mecha_mode():
            self._nd and self._nd.content.setVisible(self._in_mecha)

    def _set_in_mecha(self, in_mecha):
        old_val = self._in_mecha
        self._in_mecha = in_mecha
        if old_val != in_mecha:
            if self._in_pure_mecha_mode():
                self._nd and self._nd.content.setVisible(in_mecha)

    def _in_pure_mecha_mode(self):
        if not global_data.game_mode:
            return False
        from logic.client.const import game_mode_const
        return global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_GVG, game_mode_const.GAME_MODE_DUEL))

    def update_pos_and_scale(self):
        cam = self.cam()
        if cam:
            lplayer = self._get_lplayer()
            if lplayer and lplayer.is_valid():
                ctrl_target = lplayer.ev_g_control_target()
                bind_point_logic = lplayer
                bind_point = 's_xuetiao'
                in_mecha = False
                if ctrl_target and ctrl_target.logic and ctrl_target.logic.MASK & OLD_MECHA_VEHICLE_TAG_VALUE:
                    bind_point = 'xuetiao'
                    bind_point_logic = ctrl_target.logic
                    in_mecha = True
                self._set_in_mecha(in_mecha)
                if self._in_pure_mecha_mode() and not self._in_mecha:
                    return
                pos = None
                if bind_point is not None:
                    model = bind_point_logic.ev_g_model()
                    if model:
                        mat = model.get_socket_matrix(bind_point, world.SPACE_TYPE_WORLD)
                        pos = mat.translation
                if pos is None:
                    pos = lplayer.ev_g_model_position()
                if not pos:
                    return
                name_pos = math3d.vector(pos)
                nd = self._nd
                if nd:
                    x, y = cam.world_to_screen(name_pos)
                    new_x, new_y = limit_pos_in_screen(x, y)
                    is_in_screen = new_x == x and new_y == y
                    if is_in_screen:
                        new_x, new_y = neox_pos_to_cocos(new_x, new_y)
                        lpos = nd.getParent().convertToNodeSpace(cc.Vec2(new_x, new_y))
                        nd.setPosition(lpos)
                        nd.nd_details.setVisible(True)
                    else:
                        nd.nd_details.setVisible(False)
        return

    def update_health(self):
        lplayer = self._get_lplayer()
        if lplayer and lplayer.is_valid():
            self._hp_bar_widget.update_health(lplayer)
        else:
            self._hp_bar_widget.update_health(None)
        return

    def show(self):
        self._nd.setVisible(True)

    def hide(self):
        self._nd.setVisible(False)

    def destroy(self):
        self._nd.Destroy()
        self._nd = None
        self.panel = None
        self.cam = None
        self.screen_size = None
        self._hp_bar_widget.destroy()
        self._hp_bar_widget = None
        return


from common.uisys.basepanel import BasePanel
from common.const.uiconst import SCALE_PLATE_ZORDER
from logic.gutils import judge_utils
from logic.gutils.team_utils import is_judge_group
from common.const import uiconst

class ScopePlayerUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/empty'
    DLG_ZORDER = SCALE_PLATE_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT

    def on_init_panel(self):
        self.show_player_map = {}
        self.hide_player_map = {}
        self.ob_target_ref = None
        self.cur_tick_count = 0
        self.init_event()
        self.panel.setLocalZOrder(1)
        return

    def on_finalize_panel(self):
        self.stop_tick()
        global_data.emgr.scene_observed_player_setted_event -= self._on_switch_ob
        self.clear_player_hide_map()
        self.clear_player_show_map()
        self.ob_target_ref = None
        return

    def show(self):
        super(ScopePlayerUI, self).show()
        self.check_player_head_ui_show()
        self.start_tick()

    def hide(self):
        super(ScopePlayerUI, self).hide()
        self.stop_tick()

    def start_tick(self):
        self.update()
        self.panel.runAction(cc.RepeatForever.create(cc.Sequence.create([
         cc.CallFunc.create(self.update),
         cc.DelayTime.create(0.033)])))

    def stop_tick(self):
        self.panel.stopAllActions()

    def update(self):
        self.cur_tick_count += 1
        if self.cur_tick_count > 10:
            self.check_player_head_ui_show()
            self.cur_tick_count = 0
        self.update_player_head_uis()

    def init_event(self):
        spectate_target = None
        if global_data.player and global_data.player.logic:
            spectate_target = global_data.player.logic.ev_g_spectate_target()
        if spectate_target and spectate_target.logic:
            self._on_switch_ob(spectate_target.logic)
        global_data.emgr.scene_observed_player_setted_event += self._on_switch_ob
        return

    def check_player_head_ui_show(self):
        should_show_set = set(judge_utils.get_readonly_nearby_pids())
        ob_target = self.ob_target_ref() if self.ob_target_ref else None
        if ob_target is not None and not global_data.is_in_judge_camera:
            if ob_target.id in should_show_set:
                should_show_set.remove(ob_target.id)
            pids = ob_target.ev_g_groupmate()
            if pids:
                for pid in pids:
                    if pid in should_show_set:
                        should_show_set.remove(pid)

        cur_show_set = set(six_ex.keys(self.show_player_map))
        need_show_list = should_show_set - cur_show_set
        need_hide_list = cur_show_set - should_show_set
        for pid in need_show_list:
            self.show_player_head_ui_out(pid)

        for pid in need_hide_list:
            self.hide_player_head_ui(pid)

        return

    def update_player_head_uis(self):
        for nd in six_ex.values(self.show_player_map):
            nd.refresh()

    def show_player_head_ui_out(self, pid):
        if pid in self.hide_player_map:
            nd = self.hide_player_map[pid]
            del self.hide_player_map[pid]
            nd.show()
        else:
            nd = self.create_player_head_ui(pid)
        if not nd:
            return
        self.show_player_map[pid] = nd

    def hide_player_head_ui(self, pid):
        if pid in self.show_player_map:
            nd = self.show_player_map[pid]
            del self.show_player_map[pid]
            nd.hide()
            self.hide_player_map[pid] = nd
        if len(self.hide_player_map) > 10:
            self.clear_player_hide_map()

    def clear_player_show_map(self):
        for nd in six_ex.values(self.show_player_map):
            nd.destroy()

        self.show_player_map = {}

    def clear_player_hide_map(self):
        for nd in six_ex.values(self.hide_player_map):
            nd.destroy()

        self.hide_player_map = {}

    def del_player_head_ui(self, pid):
        nd = None
        if pid in self.hide_player_map:
            nd = self.hide_player_map[pid]
            del self.hide_player_map[pid]
        if pid in self.show_player_map:
            nd = self.show_player_map[pid]
            del self.show_player_map[pid]
        if nd:
            nd.destroy()
        return

    def create_player_head_ui(self, pid):
        ent = EntityManager.getentity(pid)
        if not (ent and ent.logic):
            log_error('Try to create head ui for non-exist player')
            return None
        else:
            nd = global_data.uisystem.load_template_create('observe/i_watching_player_ui')
            self.panel.AddChild('', nd)
            head_ui = PlayerHeadUI(nd, pid, self)
            return head_ui

    def _on_switch_ob(self, ltarget):
        if not ltarget:
            return
        self.ob_target_ref = weakref.ref(ltarget)
        if self.isPanelVisible():
            self.check_player_head_ui_show()