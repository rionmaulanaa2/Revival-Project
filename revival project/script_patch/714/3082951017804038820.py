# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Flag/FlagMarkWidget.py
from __future__ import absolute_import
from common.const.uiconst import SMALL_MAP_ZORDER
from logic.gcommon.const import NEOX_UNIT_SCALE
from common.uisys.basepanel import BasePanel
from logic.comsys.battle import BattleUtils
from logic.gcommon import time_utility as tutil
import weakref
import copy
import math
from common.utils.cocos_utils import getScreenSize
import math3d
import common.utils.timer as timer
from common.const import uiconst
from common.uisys.uielment.CCUISpaceNode import CCUISpaceNode
from logic.comsys.common_ui import CommonInfoUtils
from logic.gcommon.common_const.building_const import FLAG_RECOVER_BY_DROPPING, FLAG_RECOVER_BY_PLANTING, FLAG_RECOVER_BY_TIME_UP, FLAG_RECOVER_BY_INVALID_REGION
from logic.gcommon.common_const.battle_const import FLAG_BATTLE_FLAG_BASE_BLUE_LOCATE_UI, FLAG_BATTLE_FLAG_BASE_RED_LOCATE_UI, FLAG_BATTLE_FLAG_LOCATE_UI
from common.utils.ui_utils import get_scale
import common.utils.cocos_utils as cocos_utils
from logic.gcommon.common_const import buff_const as bconst
from logic.gutils.judge_utils import is_ob

class FlagMarkWidgetUI(object):
    screen_size = getScreenSize()
    screen_angle_limit = math.atan(getScreenSize().height / 2.0 / (getScreenSize().width / 2.0)) * 180 / math.pi
    SCREEN_MARGIN = get_scale('40w')
    UI_TEM = FLAG_BATTLE_FLAG_LOCATE_UI
    SMALL_MAP_FLAG_NORMAL_ID = 2031
    SMALL_MAP_FLAG_ENEMY_ID = 2032
    SMALL_MAP_FLAG_TEAMMATE_ID = 2033
    ZERO_VECTOR = math3d.vector(0, 0, 0)
    TYPE_TO_BIND_NODE = {'FlagBuilding': 'fx_glow',
       'Avatar': 's_xuetiao',
       'Mecha': 'xuetiao',
       'Puppet': 's_xuetiao',
       'PuppetMecha': 'xuetiao',
       'huoLiuXingBall': None,
       'huoLiuXingBallPuppet': None
       }
    TYPE_TO_OFFSET = {'FlagBuilding': math3d.vector(0, 7.0 * NEOX_UNIT_SCALE, 0),
       'Avatar': math3d.vector(0, 0, 0),
       'Puppet': math3d.vector(0, 5.0 * NEOX_UNIT_SCALE, 0),
       'PuppetMecha': math3d.vector(0, 0, 0),
       'Mecha': math3d.vector(0, 5.0 * NEOX_UNIT_SCALE, 0),
       'huoLiuXingBall': math3d.vector(0, 0, 0),
       'huoLiuXingBallPuppet': math3d.vector(0, 75, 0)
       }

    def __init__(self, target_id, panel):
        self.on_init(target_id, panel)

    def on_init(self, target_id, panel):
        self.init_parameters(target_id, panel)
        self.init_node()
        self.init_event()
        self.init_timer()

    def init_node(self):
        self.space_node = CCUISpaceNode.Create()
        ui_key = self.UI_TEM
        self.base_node = CommonInfoUtils.create_ui(ui_key, self.space_node, False, False)
        self.base_node.setPosition(0, 0)
        if global_data.aim_transparent_mgr:
            global_data.aim_transparent_mgr.add_target_node(self.__class__.__name__, [self.base_node])
        self.pos_node_norm = self.base_node.nd_mark_flag
        self.pos_node_blue = self.base_node.nd_mark_blue
        self.pos_node_red = self.base_node.nd_mark_red
        self.lab_time = None
        self.bar_time = None
        self.switch_flag_active_ui()
        horizontal_margin = 140 * self.panel.getScale()
        vertical_margin = 80 * self.panel.getScale()
        top_margin = self.SCREEN_MARGIN
        self.space_node.set_enable_limit_in_screen(True, horizontal_margin, horizontal_margin, top_margin, vertical_margin)
        self.space_node.set_screen_check_margin(0, 0, top_margin, 0)
        return

    def init_parameters(self, target_id, panel):
        self.target_id = target_id
        self.panel = panel
        faction_to_flag_base_id = global_data.death_battle_data.faction_to_flag_base_id
        scn = global_data.game_mgr.scene
        self.camera = weakref.ref(scn.active_camera)
        self._binded_model = None
        self._binded_socket = None
        self.space_node = None
        self.base_node = None
        self.pos_node_norm = None
        self.pos_node_blue = None
        self.pos_node_red = None
        self.nd_rotate = None
        self.lab_time = None
        self.lab_time_vx = None
        self.bar_time = None
        self.icon_update_timer = None
        self.change_follow_target_timer = None
        self._last_alarm_time = None
        self._lock = False
        self._unlock_timer = None
        return

    def init_timer(self):
        self.process_update_timer(True)

    def update_follow_target(self, target_id):
        self.target_id = target_id
        self._binded_model = None
        self._binded_socket = None
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'flagsnatch_flag_recover': self._on_flag_recover,
           'flagsnatch_flag_pick_up': self._on_flag_pick_up,
           'flagsnatch_flag_init_complete': self._on_flag_init_complete
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_event(self):
        self.process_event(True)

    def set_ui_to_lock_state(self):
        self.pos_node_norm.img_timebg.setVisible(True)
        self.pos_node_norm.lock.setVisible(True)
        self.pos_node_norm.icon.setVisible(False)
        self._lock = True

    def set_ui_to_unlock_state(self):
        self.pos_node_norm.img_timebg.setVisible(False)
        self.pos_node_norm.lock.setVisible(False)
        self.pos_node_norm.icon.setVisible(True)
        self._lock = False

    def switch_flag_active_ui(self, picker_faction=None):
        if not picker_faction:
            self.base_node.PlayAnimation('loop')
            self.pos_node_norm.setVisible(True)
            self.pos_node_blue.setVisible(False)
            self.pos_node_red.setVisible(False)
            self.pos_node = self.pos_node_norm
        elif picker_faction == global_data.player.logic.ev_g_group_id():
            self.base_node.PlayAnimation('blueloop')
            self.pos_node_norm.setVisible(False)
            self.pos_node_blue.setVisible(True)
            self.pos_node_red.setVisible(False)
            self.pos_node = self.pos_node_blue
        else:
            self.base_node.PlayAnimation('redloop')
            self.pos_node_norm.setVisible(False)
            self.pos_node_blue.setVisible(False)
            self.pos_node_red.setVisible(True)
            self.pos_node = self.pos_node_red
        self.nd_rotate = self.pos_node.nd_rotate
        if self.pos_node.img_timebg:
            self.lab_time = self.pos_node.img_timebg.lab_time
            self.lab_time_vx = self.pos_node.img_timebg.lab_time_vx
        self.bar_time = self.pos_node.bar_time

    def _on_flag_pick_up(self, picker_id, picker_faction):
        self.switch_flag_active_ui(picker_faction)
        self.show_flag_pick_warn(picker_faction)
        self._change_follow_target_to_player(picker_id)
        self._on_update_time()
        self._change_flag_small_map_status(picker_faction)

    def _on_flag_init_complete(self, eid, pos):
        global_data.emgr.scene_del_client_mark.emit(eid)
        global_data.emgr.scene_add_client_mark.emit(eid, self.SMALL_MAP_FLAG_NORMAL_ID, pos)

    def show_flag_pick_warn(self, picker_faction):
        if picker_faction == global_data.player.logic.ev_g_group_id():
            self.base_node.PlayAnimation('get_blue')
        else:
            self.base_node.PlayAnimation('get_red')

    def _on_flag_recover(self, holder_id, holder_faction, reason):
        self.switch_flag_active_ui()
        self._change_follow_target_to_flag()
        if reason == FLAG_RECOVER_BY_TIME_UP or reason == FLAG_RECOVER_BY_PLANTING or reason == FLAG_RECOVER_BY_INVALID_REGION:
            self._on_lock_flag()
        self._on_update_time()
        self._change_flag_small_map_status(None)
        return

    def _on_lock_flag(self):
        self.set_ui_to_lock_state()
        unlock_time = global_data.death_battle_data.flag_lock_time
        if self._unlock_timer:
            global_data.game_mgr.unregister_logic_timer(self._unlock_timer)
        self._unlock_timer = global_data.game_mgr.register_logic_timer(self.set_ui_to_unlock_state, unlock_time, mode=timer.CLOCK)

    def _change_follow_target_to_flag(self, *args):
        self.nd_rotate.setVisible(True)
        self.update_follow_target(global_data.death_battle_data.flag_ent_id)

    def _change_follow_target_to_player(self, ent_id, *args):
        is_visible = self.get_ui_visible(ent_id)
        if not is_visible:
            self.nd_rotate.setVisible(False)
        self.update_follow_target(ent_id)

    def _change_flag_small_map_status(self, picker_faction=None):
        flag_id = global_data.death_battle_data.flag_ent_id
        flag_ent = global_data.battle.get_entity(flag_id)
        if not flag_ent:
            return
        global_data.emgr.scene_del_client_mark.emit(flag_id)
        tmp_pos = flag_ent.logic.ev_g_position()
        if not picker_faction:
            global_data.emgr.scene_add_client_mark.emit(flag_id, self.SMALL_MAP_FLAG_NORMAL_ID, tmp_pos)
        elif picker_faction == global_data.player.logic.ev_g_group_id():
            global_data.emgr.scene_add_client_mark.emit(flag_id, self.SMALL_MAP_FLAG_TEAMMATE_ID, tmp_pos)
        else:
            global_data.emgr.scene_add_client_mark.emit(flag_id, self.SMALL_MAP_FLAG_ENEMY_ID, tmp_pos)

    def get_target_type(self, target_ent, ent_id):
        if not target_ent.logic:
            return 'None'
        target_type = target_ent.__class__.__name__
        if target_type == 'Mecha':
            is_ball = target_ent.logic.ev_g_has_buff_by_id(bconst.BUFF_ID_BALL_STATE)
            if global_data.cam_lplayer:
                is_puppet = global_data.cam_lplayer != ent_id
            else:
                is_puppet = global_data.player.id != ent_id
            if is_ball:
                if is_puppet:
                    return 'huoLiuXingBallPuppet'
                else:
                    return 'huoLiuXingBall'

            elif is_puppet:
                return 'PuppetMecha'
            else:
                return 'Mecha'

        return target_type

    def get_ui_visible(self, target_eid):
        if target_eid == global_data.player.id:
            return False
        return True

    def _on_update_ui_state(self):
        self._on_update_pos_and_rot()
        self._on_update_time()

    def _on_update_time(self):
        if not self.lab_time:
            return
        tmp_time = tutil.time()
        mod_time = int(tmp_time)
        if self._lock:
            flag_lock_start_time = global_data.death_battle_data.flag_lock_start_time
            flag_lock_time = global_data.death_battle_data.flag_lock_time
            if not flag_lock_start_time:
                return
            passed_time = tmp_time - flag_lock_start_time
            res_time = flag_lock_time - passed_time
            percent = max(0, min(res_time / flag_lock_time * 100, 100))
        else:
            flag_reset_start_time = global_data.death_battle_data.flag_reset_start_time
            flag_refresh_time = global_data.death_battle_data.flag_refresh_time
            if not flag_reset_start_time:
                return
            passed_time = tmp_time - flag_reset_start_time
            res_time = flag_refresh_time - passed_time
            percent = max(0, min(res_time / flag_refresh_time * 100, 100))
        if self.bar_time:
            self.bar_time.SetPercentage(percent)
        displaied_res_time = int(math.ceil(res_time))
        displaied_res_time = tutil.get_delta_time_str(displaied_res_time)[3:]
        self.lab_time.setString(displaied_res_time)
        if mod_time != self._last_alarm_time:
            if res_time < 10:
                self.lab_time.SetColor('#SR')
                if self.lab_time_vx:
                    self.lab_time_vx.setString(displaied_res_time)
                    if mod_time != self._last_alarm_time:
                        self.base_node.PlayAnimation('alarm')
            else:
                self.lab_time.SetColor('#SW')
        self._last_alarm_time = mod_time

    def _on_update_pos_and_rot(self):
        cam_lplayer = global_data.cam_lplayer
        lplayer_pos = self.get_target_pos(cam_lplayer)
        if not cam_lplayer:
            return
        self.update_nd_pos_and_rot(self.camera(), cam_lplayer, lplayer_pos, self.target_id)

    def get_target_pos(self, ltarget):
        if ltarget:
            control_target = ltarget.sd.ref_ctrl_target
            if control_target and control_target.logic:
                pos = control_target.logic.ev_g_model_position()
                return pos
        return None

    def update_nd_pos_and_rot(self, camera, cam_lplayer, lplayer_pos, target_eid):
        target_ent = global_data.battle.get_entity(target_eid)
        if not target_ent:
            return
        else:
            ctrl_entity = target_ent.logic.ev_g_control_target() or None
            if ctrl_entity:
                target_type = self.get_target_type(ctrl_entity, target_eid)
                target_model = ctrl_entity.logic.ev_g_model()
            else:
                target_type = self.get_target_type(target_ent, target_eid)
                target_model = target_ent.logic.ev_g_model()
            pos_offset = self.TYPE_TO_OFFSET.get(target_type, math3d.vector(0, 0, 0))
            bind_node = self.TYPE_TO_BIND_NODE.get(target_type, None)
            if not target_model:
                return False
            if not lplayer_pos:
                return False
            target_position = target_model.world_position
            if not target_position:
                return False
            self.try_bind_model(self.space_node, target_model, pos_offset, bind_node)
            self.update_rot(camera, target_position, lplayer_pos)
            return True

    def update_rot(self, camera, target_position, lplayer_pos):
        target_camera_pos = camera.world_to_camera(target_position)
        angle = math.atan2(target_camera_pos.y, target_camera_pos.x)
        angle = angle * 180 / math.pi
        if angle < 0:
            angle += 360
        self.nd_rotate.setRotation(-(angle - 90))

    def try_bind_model(self, node, interact_model, pos_offset=None, socket=None):
        if not node:
            return
        if not self._binded_model or self._binded_model() != interact_model or self._binded_socket != socket:
            if not node:
                return
            if socket:
                node.bind_model(interact_model, socket)
                node.set_fix_xz(False)
            else:
                node.bind_space_object(interact_model)
            self._binded_model = weakref.ref(interact_model)
            self._binded_socket = socket
            if pos_offset is not self.ZERO_VECTOR:
                node.set_pos_offset(pos_offset)

    def process_update_timer(self, tag=True):
        if tag:
            if not self.icon_update_timer:
                self.icon_update_timer = global_data.game_mgr.register_logic_timer(self._on_update_ui_state, 0.02, mode=timer.CLOCK)
        elif self.icon_update_timer:
            global_data.game_mgr.unregister_logic_timer(self.icon_update_timer)
            self.icon_update_timer = None
        return

    def on_finalize(self):
        self.process_event(False)
        self.process_update_timer(False)
        self.panel = None
        self.nd_rotate = None
        self.base_node = None
        if self.space_node:
            self.space_node.Destroy()
        self.space_node = None
        self.pos_offset = None
        if self.change_follow_target_timer:
            global_data.game_mgr.unregister_logic_timer(self.change_follow_target_timer)
        if self._unlock_timer:
            global_data.game_mgr.unregister_logic_timer(self._unlock_timer)
        return