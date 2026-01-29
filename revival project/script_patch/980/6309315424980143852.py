# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/Crown/CrownMarkWidget.py
from __future__ import absolute_import
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon import time_utility as tutil
import weakref
import math
from common.utils.cocos_utils import getScreenSize
import math3d
import common.utils.timer as timer
from common.const import uiconst
from common.uisys.uielment.CCUISpaceNode import CCUISpaceNode
from logic.comsys.common_ui import CommonInfoUtils
from common.utils.ui_utils import get_scale
from logic.gcommon.common_const import buff_const as bconst
from logic.gcommon.common_const.battle_const import CROWN_OTHER_FACTION, CROWN_SELF_FACTION, CROWN_TEAM_FACTION, MAIN_NODE_COMMON_INFO, CROWN_BATTLE_CROWN_TEAM_BORN_TIPS, CROWN_BATTLE_CROWN_OTHER_DIE_TIPS, CROWN_BATTLE_CROWN_OTHER_BORN_TIPS, CROWN_BATTLE_CROWN_TEAM_DIE_TIPS

class CrownMarkWidget(object):
    screen_size = getScreenSize()
    screen_angle_limit = math.atan(getScreenSize().height / 2.0 / (getScreenSize().width / 2.0)) * 180 / math.pi
    SCREEN_MARGIN = get_scale('40w')
    SMALL_MAP_FLAG_NORMAL_ID = 2031
    SMALL_MAP_FLAG_ENEMY_ID = 2032
    SMALL_MAP_FLAG_TEAMMATE_ID = 2033
    ZERO_VECTOR = math3d.vector(0, 0, 0)
    TYPE_TO_BIND_NODE = {'Avatar': 's_xuetiao',
       'Mecha': 'xuetiao',
       'Puppet': 's_xuetiao',
       'PuppetMecha': 'xuetiao',
       'huoLiuXingBall': None,
       'huoLiuXingBallPuppet': None
       }
    TYPE_TO_OFFSET = {'Avatar': math3d.vector(0, 0, 0),
       'Puppet': math3d.vector(0, 5.0 * NEOX_UNIT_SCALE, 0),
       'Mecha': math3d.vector(0, 0, 0),
       'PuppetMecha': math3d.vector(0, 5.0 * NEOX_UNIT_SCALE, 0),
       'huoLiuXingBall': math3d.vector(0, 0, 0),
       'huoLiuXingBallPuppet': math3d.vector(0, 75, 0)
       }

    def __init__(self, panel, ui_template, faction_id, mark_id=None):
        self.on_init(panel, ui_template, faction_id, mark_id)

    def on_init(self, panel, ui_template, faction_id, mark_id=None):
        self.init_parameters(panel, ui_template, faction_id, mark_id)
        self.init_node()
        self.init_event()
        self.init_timer()

    def init_parameters(self, panel, ui_template, faction_id, mark_id):
        self.ui_template = ui_template
        self.panel = panel
        self.faction_id = faction_id
        self.mark_id = mark_id
        self.target_id = None
        scn = global_data.game_mgr.scene
        self.camera = weakref.ref(scn.active_camera)
        self._binded_model = None
        self._binded_socket = None
        self.space_node = None
        self.base_node = None
        self.nd_rotate = None
        self.icon_update_timer = None
        self.mark_create = False
        return

    def init_node(self):
        ui_key = self.ui_template
        if ui_key:
            self.space_node = CCUISpaceNode.Create()
            self.base_node = CommonInfoUtils.create_ui(ui_key, self.space_node, False, False)
            self.base_node.setPosition(0, 0)
            if global_data.aim_transparent_mgr:
                global_data.aim_transparent_mgr.add_target_node(self.__class__.__name__, [self.base_node])
            horizontal_margin = 140 * self.panel.getScale()
            vertical_margin = 80 * self.panel.getScale()
            top_margin = self.SCREEN_MARGIN
            self.space_node.set_enable_limit_in_screen(True, horizontal_margin, horizontal_margin, top_margin, vertical_margin)
            self.space_node.set_screen_check_margin(0, 0, top_margin, 0)
            self.base_node.setVisible(False)
            self.nd_rotate = self.base_node.nd_rotate
            self.base_node.nd_rotate.setVisible(False)
            self.base_node.img_timebg.setVisible(False)
        else:
            self.base_node = None
        return

    def init_event(self):
        self.process_event(True)

    def init_timer(self):
        self.process_update_timer()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'on_crown_born': self._on_crown_born,
           'on_crown_death': self._on_crown_death
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def _on_crown_born(self, target_id, faction_id):
        if self.faction_id != faction_id:
            return
        else:
            self.target_id = target_id
            self._binded_model = None
            self._binded_socket = None
            if self.mark_id:
                self.create_flag_small_map_ui()
            return

    def _on_crown_death(self, target_id, faction_id):
        if self.faction_id != faction_id:
            return
        else:
            if self.mark_id:
                self.del_flag_small_map_ui()
            self.target_id = None
            self._binded_model = None
            self._binded_socket = None
            if self.base_node:
                self.base_node.setVisible(False)
            return

    def get_target_type(self, target_ent, ent_id):
        if not target_ent.logic:
            return 'None'
        target_type = target_ent.__class__.__name__
        if target_type == 'Mecha':
            is_ball = target_ent.logic.ev_g_has_buff_by_id(bconst.BUFF_ID_BALL_STATE)
            is_puppet = global_data.player.id == ent_id
            if is_ball:
                if is_puppet:
                    return 'huoLiuXingBallPuppet'
                else:
                    return 'huoLiuXingBall'

            elif is_puppet:
                return 'Mecha'
            else:
                return 'PuppetMecha'

        return target_type

    def get_ui_visible(self, target_eid):
        if target_eid == global_data.player.id:
            return False
        return True

    def _on_update_ui_state(self):
        self._on_update_pos_and_rot()
        self._on_update_small_map()

    def _on_update_pos_and_rot(self):
        if not self.base_node:
            return
        cam_lplayer = global_data.cam_lplayer
        lplayer_pos = self.get_target_pos(cam_lplayer)
        if not cam_lplayer:
            return
        if not self.camera():
            scn = global_data.game_mgr.scene
            self.camera = weakref.ref(scn.active_camera)
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
        if self.space_node.get_is_in_screen() or self.faction_id == CROWN_SELF_FACTION:
            self.nd_rotate.setVisible(False)
        else:
            self.nd_rotate.setVisible(True)
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
            self.base_node.setVisible(True)

    def _on_update_small_map(self):
        if not self.mark_create and self.target_id:
            self.create_flag_small_map_ui()

    def create_flag_small_map_ui(self):
        entity = global_data.battle.get_entity(self.target_id)
        if not entity:
            return
        global_data.emgr.scene_del_client_mark.emit(self.target_id)
        tmp_pos = entity.logic.ev_g_position()
        global_data.emgr.scene_add_client_mark.emit(self.target_id, self.mark_id, tmp_pos)
        self.mark_create = True

    def del_flag_small_map_ui(self):
        self.mark_create = False
        global_data.emgr.scene_del_client_mark.emit(self.target_id)

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
        return