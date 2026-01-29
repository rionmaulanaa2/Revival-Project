# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/SnatchEgg/EggMarkWidget.py
from __future__ import absolute_import
import six
from logic.gcommon.const import NEOX_UNIT_SCALE
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
from logic.gcommon.common_const.battle_const import SNATCHEGG_BATTLE_EGG_LOCATE_UI
from common.utils.ui_utils import get_scale
import common.utils.cocos_utils as cocos_utils
from logic.gcommon.common_const import buff_const as bconst
from logic.gutils.judge_utils import is_ob

class EggMarkWidget(object):
    screen_size = getScreenSize()
    screen_angle_limit = math.atan(getScreenSize().height / 2.0 / (getScreenSize().width / 2.0)) * 180 / math.pi
    SCREEN_MARGIN = get_scale('40w')
    UI_TEM = SNATCHEGG_BATTLE_EGG_LOCATE_UI
    SMALL_MAP_EGG_ID = 2050
    ZERO_VECTOR = math3d.vector(0, 0, 0)
    TYPE_TO_BIND_NODE = {'Goldenegg': 'fx_glow',
       'Avatar': 's_xuetiao',
       'Mecha': 'xuetiao',
       'Puppet': 's_xuetiao',
       'PuppetMecha': 'xuetiao',
       'huoLiuXingBall': None,
       'huoLiuXingBallPuppet': None
       }
    TYPE_TO_OFFSET = {'Goldenegg': math3d.vector(0, 7.0 * NEOX_UNIT_SCALE, 0),
       'Avatar': math3d.vector(0, 0, 0),
       'Puppet': math3d.vector(0, 5.0 * NEOX_UNIT_SCALE, 0),
       'PuppetMecha': math3d.vector(0, 1.0, 0),
       'Mecha': math3d.vector(0, 6.0 * NEOX_UNIT_SCALE, 0),
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
        self.nd_rotate = self.base_node.nd_rotate
        self.base_node.setPosition(0, 0)
        if global_data.aim_transparent_mgr:
            global_data.aim_transparent_mgr.add_target_node(self.__class__.__name__, [self.base_node])
        self.switch_egg_active_ui()
        horizontal_margin = 140 * self.panel.getScale()
        vertical_margin = 80 * self.panel.getScale()
        top_margin = self.SCREEN_MARGIN
        self.space_node.set_enable_limit_in_screen(True, horizontal_margin, horizontal_margin, top_margin, vertical_margin)
        self.space_node.set_screen_check_margin(0, 0, top_margin, 0)

    def init_parameters(self, target_id, panel):
        self.egg_id = target_id
        self.target_id = None
        self.panel = panel
        scn = global_data.game_mgr.scene
        self.camera = weakref.ref(scn.active_camera)
        self._binded_model = None
        self._binded_socket = None
        self.space_node = None
        self.base_node = None
        self.nd_rotate = None
        self.icon_update_timer = None
        self.change_follow_target_timer = None
        self.pos_update_count = 0
        self.pos_update_need_count = 20
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
        econf = {'snatchegg_egg_drop': self._on_egg_recover,
           'snatchegg_egg_pick_up': self._on_egg_pick_up,
           'flagsnatch_flag_init_complete': self._on_flag_init_complete,
           'scene_observed_player_setted_event': self.on_enter_observed
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_event(self):
        self.process_event(True)

    def on_enter_observed(self, *args):
        self.init_egg()

    def init_egg(self):
        egg_holder = None
        if global_data.death_battle_data:
            for holder_id, npc_id in six.iteritems(global_data.death_battle_data.egg_picker_dict):
                if npc_id == self.egg_id:
                    egg_holder = holder_id
                    break

        if egg_holder:
            from mobile.common.EntityManager import EntityManager
            ent = EntityManager.getentity(egg_holder)
            if ent and ent.logic:
                picker_faction = ent.logic.ev_g_group_id()
                self._on_egg_pick_up(egg_holder, picker_faction, self.egg_id)
            else:
                self.base_node.DelayCallWithTag(1.5, self.init_egg, tag=230423)
        else:
            self.switch_egg_active_ui(None, None)
        return

    def switch_egg_active_ui(self, picker_id=None, picker_faction=None, is_on_throw=False):
        if not global_data.cam_lplayer:
            return
        if not self.base_node:
            return
        if is_on_throw:
            self.base_node.icon_normal.setVisible(False)
            self.base_node.icon_hold_blue.setVisible(False)
            self.base_node.icon_hold_red.setVisible(False)
            self.base_node.icon_drop.setVisible(True)
            return
        if not picker_faction:
            self.base_node.icon_normal.setVisible(True)
            self.base_node.icon_hold_blue.setVisible(False)
            self.base_node.icon_hold_red.setVisible(False)
            self.base_node.icon_drop.setVisible(False)
        else:
            self.base_node.icon_normal.setVisible(False)
            if picker_id:
                if picker_faction == global_data.cam_lplayer.ev_g_group_id():
                    self.base_node.icon_hold_blue.setVisible(True)
                    self.base_node.icon_hold_red.setVisible(False)
                else:
                    self.base_node.icon_hold_blue.setVisible(False)
                    self.base_node.icon_hold_red.setVisible(True)
            else:
                self.base_node.icon_drop.setVisible(False)

    def _on_egg_pick_up(self, picker_id, picker_faction, npc_id):
        if npc_id != self.egg_id:
            return
        self.switch_egg_active_ui(picker_id, picker_faction)
        self._change_follow_target_to_player(picker_id)

    def _on_flag_init_complete(self, eid, pos):
        self.init_egg()
        global_data.emgr.scene_del_client_mark.emit(eid)
        global_data.emgr.scene_add_client_mark.emit(eid, self.SMALL_MAP_EGG_ID, pos, kwargs={'egg_id': eid})

    def _on_egg_recover(self, holder_id, holder_faction, reason, npc_id):
        if npc_id != self.egg_id:
            return
        else:
            from logic.gcommon.common_const.battle_const import THROW_EGG
            is_on_throw = reason == THROW_EGG
            self.switch_egg_active_ui(None, None, is_on_throw=is_on_throw)
            self._change_follow_target_to_egg()
            return

    def _change_follow_target_to_egg(self, *args):
        self.nd_rotate.setVisible(True)
        self.update_follow_target(None)
        return

    def _change_follow_target_to_player(self, ent_id, *args):
        is_visible = self.get_ui_visible(ent_id)
        if not is_visible:
            self.nd_rotate.setVisible(False)
        self.update_follow_target(ent_id)

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

    def _on_update_pos_and_rot(self):
        cam_lplayer = global_data.cam_lplayer
        lplayer_pos = self.get_target_pos(cam_lplayer)
        if not cam_lplayer:
            return
        if self.space_node:
            is_in_screen = self.space_node.get_is_in_screen()
            self.base_node.setScale(1.0 if is_in_screen else 0.8)
            self.nd_rotate.setVisible(not is_in_screen)
            self.base_node.bar.setVisible(is_in_screen)
        self.update_nd_pos_and_rot(self.camera(), cam_lplayer, lplayer_pos, self.target_id or self.egg_id)

    def get_target_pos(self, ltarget):
        if ltarget:
            control_target = ltarget.sd.ref_ctrl_target
            if control_target and control_target.logic:
                pos = control_target.logic.ev_g_model_position()
                return pos
        return None

    def update_nd_pos_and_rot(self, camera, cam_lplayer, lplayer_pos, target_eid):
        self.pos_update_count += 1
        target_ent = global_data.battle.get_entity(target_eid)
        if not (target_ent and target_ent.logic):
            return
        else:
            ctrl_entity = target_ent.logic.ev_g_control_target() or None
            if ctrl_entity and ctrl_entity.logic:
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
            if self.pos_update_count >= self.pos_update_need_count:
                global_data.emgr.scene_modify_client_mark_pos.emit(self.egg_id, target_position)
                self.pos_update_count = 0
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
        global_data.emgr.scene_del_client_mark.emit(self.egg_id)
        return

    def show(self):
        self.space_node.setVisible(True)

    def hide(self):
        self.space_node.setVisible(False)