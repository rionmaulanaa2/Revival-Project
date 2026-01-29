# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/map/map_widget/MapScaleInterface.py
from __future__ import absolute_import
from __future__ import print_function
import six
from six.moves import range
from common.uisys.uielment.CCSprite import CCSprite
from common.uisys.uielment.CCNode import CCNode
import cc
import math
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gutils import map_utils
from logic.gutils.team_utils import get_mark_pic_path
from common.utils.cocos_utils import ccp
from logic.gcommon.common_const.battle_const import MAP_COL_BLUE, MAP_COL_GREEN, MAP_COL_RED, MAP_COL_YELLOW, MARK_NORMAL, MARK_DANGER, MARK_RES, LOCATE_NORMAL, LOCATE_DEAD, LOCATE_RECOURSE, LOCATE_DRIVE, MARK_BULLET, LOCATE_OFFLINE, LOCATE_PARACHUTE
from mobile.common.EntityManager import EntityManager
from logic.gcommon.cdata import status_config
from logic.gcommon.time_utility import time
from logic.gutils.map_utils import get_map_uv
from logic.gutils.map_utils import get_map_uv_ex
import weakref
LINE_WIDTH = 1

class MapScaleInterface(object):

    def __init__(self, parent_nd, map_panel=None):
        self.parent_nd = parent_nd
        self._nd = None
        self.is_nd_need_remove = True
        self.map_panel = map_panel
        self._res_detail_index = None
        self.parent_content_size = None
        if map_panel:
            map_panel.register_on_scale_listener(self)
        return

    def set_position(self, pos):
        if self._nd:
            self._nd._obj.setPosition(pos)

    def get_position(self):
        if self._nd:
            return self._nd.getPosition()
        else:
            return None
            return None

    def get_parent_content_size(self):
        return self.parent_content_size or self.parent_nd.GetContentSize()

    def set_world_position(self, world_pos):
        self.set_position(self.trans_world_position(world_pos))

    def set_world_position_ex(self, tuple_world_pos):
        self.set_position(self.trans_world_position_ex(tuple_world_pos))

    def trans_world_position(self, world_pos):
        uv = get_map_uv(world_pos)
        content_size = self.get_parent_content_size()
        return ccp(uv[0] * content_size[0], uv[1] * content_size[1])

    def trans_world_position_ex(self, tuple_world_pos):
        uv = get_map_uv_ex(tuple_world_pos)
        content_size = self.parent_nd.GetContentSize()
        return ccp(uv[0] * content_size[0], uv[1] * content_size[1])

    def destroy(self):
        if self._nd:
            if self.is_nd_need_remove:
                if isinstance(self._nd, CCNode):
                    self._nd.Destroy()
                else:
                    self._nd.removeFromParent()
            self._nd = None
        if self.parent_nd:
            self.parent_nd = None
        if self.map_panel:
            self.map_panel.unregister_on_scale_listener(self)
            self.map_panel = None
        return

    def on_map_scale(self, map_scale):
        self._nd.setScale(1.0 / map_scale)

    def is_visible(self):
        if self._nd and self._nd.isValid():
            return self._nd.isVisible()
        return False

    def show(self):
        self._nd.setVisible(True)

    def hide(self):
        if self._nd and self._nd.isValid():
            self._nd.setVisible(False)

    def play_animation(self, name):
        if self._nd:
            self._nd.PlayAnimation(name)

    def on_set_res_detail_index(self, detail_index):
        self._res_detail_index = detail_index


class MapMark(MapScaleInterface):

    def __init__(self, parent_nd):
        super(MapMark, self).__init__(parent_nd)
        self._nd = global_data.uisystem.load_template_create('map/ccb_map_mark')
        self.parent_nd.AddChild('', self._nd)

    def set_map_mark(self, type, color=None, pic_path=None):
        if pic_path is None:
            pic_path = MapMark.get_mark_pic_path(type, color)
        self._nd.sp_mark.SetDisplayFrameByPath('', pic_path)
        return

    @staticmethod
    def get_mark_pic_path(mark_type, color):
        return get_mark_pic_path(mark_type, color)


class LastVehicleMapMark(MapScaleInterface):

    def __init__(self, parent_nd):
        super(LastVehicleMapMark, self).__init__(parent_nd)
        self._nd = global_data.uisystem.load_template_create('map/ccb_map_mark')
        self.parent_nd.AddChild('', self._nd)
        self._nd.setAnchorPoint(ccp(0.5, 0.5))
        self._nd.sp_mark.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/map/icon_map_drive.png')


class CommonMapMark(MapScaleInterface):
    DEEP_PATH_KEY = 'ui_res2'
    NOT_DEEP_PATH_KEY = 'ui_res1'
    DEEP_ANIMATION = 'ui_deep_animation'
    STATE_PICS = 'state_pics'
    CUSTOM_TEMPLATE = 'custom_template'
    UI_ZORDER = 'ui_zorder'
    BIGMAP_ACTION = 'bigmap_action'
    UI_ANIM_RES1 = 'ui_anim_res1'
    DISTANCE_CHECK = 'dis_check'
    IS_FOLLOW = 'is_follow'
    SHOW_FORWARD = 'show_forward'
    INIT_DIST = 200
    MAX_X = 2048
    MAX_Y = 2048
    NODE_MARGIN = 24

    def __init__(self, parent_nd, mark_no, is_deep, state, parent=None, require_follow_model=False, **kwargs):
        super(CommonMapMark, self).__init__(parent_nd)
        from common.cfg import confmgr
        conf = confmgr.get('mark_data', str(mark_no))
        template_path = conf.get(CommonMapMark.CUSTOM_TEMPLATE, '')
        if not template_path:
            template_path = 'map/ccb_tools_mark'
        self._nd = global_data.uisystem.load_template_create(template_path)
        self.deep_animation = None
        self._v3d_pos = None
        self.is_deep = is_deep
        zorder = conf.get(CommonMapMark.UI_ZORDER, 1)
        self.parent_nd.AddChild('', self._nd, Z=zorder)
        self.deep_path = conf.get(CommonMapMark.DEEP_PATH_KEY, '')
        self.not_deep_path = conf.get(CommonMapMark.NOT_DEEP_PATH_KEY, '')
        self.deep_animation = conf.get(CommonMapMark.DEEP_ANIMATION, '')
        self.state_pic = conf.get(CommonMapMark.STATE_PICS, tuple())
        self.mark_no = mark_no
        if self.deep_animation:
            deep_timeout, animation_name = self.deep_animation
            self._nd.RecordAnimationNodeState(animation_name)
        self.ui_anim_res1 = conf.get(CommonMapMark.UI_ANIM_RES1)
        self.bigmap_action = conf.get(CommonMapMark.BIGMAP_ACTION)
        self.distance_check = conf.get(CommonMapMark.DISTANCE_CHECK)
        self.set_deep(is_deep)
        self.set_state(state)
        self.require_follow_model = require_follow_model
        self.is_follow = conf.get(CommonMapMark.IS_FOLLOW)
        self.show_forward = conf.get(CommonMapMark.SHOW_FORWARD)
        self.parent = parent
        self.map_pos = self.get_position()
        self.sp_dir = ccp(0, 1)
        if self.is_follow:
            self.init_map_parameter()
            self.update_small_map_pos()
        return

    def set_forward(self, dir):
        if not dir:
            return
        cc_dir = ccp(dir.x, dir.z)
        degree = cc_dir.getAngle(self.sp_dir) * 180 / math.pi
        self._nd.nd_dir.setVisible(True)
        self._nd.nd_dir.setRotation(degree)

    def get_ui_node(self):
        return self._nd

    def is_show_forward(self):
        return self.show_forward

    def is_follow_model(self):
        return self.require_follow_model

    def update_small_map_pos(self):
        from logic.comsys.map.SmallMapUINew import SmallMapBaseUI
        if not isinstance(self.parent, SmallMapBaseUI):
            return
        self._nd.runAction(cc.RepeatForever.create(cc.Sequence.create([
         cc.DelayTime.create(0.1),
         cc.CallFunc.create(self.on_update)])))

    def init_map_parameter(self):
        map_config = map_utils.get_map_config()
        import world
        size = map_config['arrMapResolution']
        map_cut = map_config.get('cMapCutEdge', None)
        map_pixel_height = size[1]
        map_height_offset = map_cut[0] if map_cut else 0
        scn = world.get_active_scene()
        LEFT_TRK_IDX, RIGHT_TRK_IDX, BOTTOM_TRK_IDX, UP_TRK_IDX, TRUNK_SIZE = scn.get_safe_scene_map_uv_parameters()
        MAP_HEIGHT_DIST = TRUNK_SIZE * (UP_TRK_IDX - BOTTOM_TRK_IDX + 1)
        METER_PIXEL_RATIO = (map_pixel_height - map_height_offset) / MAP_HEIGHT_DIST
        self.dist = self.INIT_DIST * NEOX_UNIT_SCALE * METER_PIXEL_RATIO
        return

    def on_update(self):
        if not self._v3d_pos:
            return
        cam_lplayer = global_data.cam_lplayer
        if not cam_lplayer:
            return
        player_position = cam_lplayer.ev_g_position()
        mark_pos = self.get_position()
        if not player_position or not mark_pos:
            return
        player_pos = self.trans_world_position(player_position)
        mark_pos = ccp(mark_pos.x, mark_pos.y)
        max_x, max_y = self.MAX_X, self.MAX_Y
        dist = self.dist
        view_left_x = max(0, player_pos.x - dist)
        view_right_x = min(max_x, player_pos.x + dist)
        view_upper_y = min(max_y, player_pos.y + dist)
        view_lower_y = max(0, player_pos.y - dist)
        if view_left_x <= self.map_pos.x <= view_right_x and view_lower_y <= self.map_pos.y <= view_upper_y:
            self._nd.nd_dir.setVisible(False)
            return
        margin = self.NODE_MARGIN
        left_x = view_left_x + margin
        right_x = view_right_x - margin
        upper_y = view_upper_y - margin
        lower_y = view_lower_y + margin
        start_x, start_y = player_pos.x, player_pos.y
        end_x, end_y = mark_pos.x, mark_pos.y
        x_delta = end_x - start_x
        y_delta = end_y - start_y
        border_x = right_x if x_delta >= 0 else left_x
        bx_delta = border_x - start_x
        x_ratio = bx_delta / x_delta if x_delta != 0 else 0
        border_z = upper_y if y_delta >= 0 else lower_y
        by_delta = border_z - start_y
        z_ratio = by_delta / y_delta if y_delta != 0 else 0
        ratio = min(x_ratio, z_ratio)
        self.set_position(ccp(start_x + x_delta * ratio, start_y + y_delta * ratio))
        self._nd.nd_dir.setVisible(True)
        mark_pos.subtract(player_pos)
        degree = mark_pos.getAngle(self.sp_dir) * 180 / math.pi
        self._nd.nd_dir.setRotation(degree)

    def set_deep(self, is_deep=False):
        self.is_deep = is_deep
        if is_deep:
            ui_res_path = self.deep_path if 1 else self.not_deep_path
            return ui_res_path or None
        else:
            if type(ui_res_path) == list:
                if self._res_detail_index is not None and self._res_detail_index < len(ui_res_path):
                    self._nd.sp_circle.SetDisplayFrameByPath('', ui_res_path[self._res_detail_index])
            else:
                self._nd.sp_circle.SetDisplayFrameByPath('', ui_res_path)
            self.check_anim_pic()
            return

    def check_play_deep(self, deep_timestamp, need_show_trans_deep_ani=False):
        if not self.is_deep or not self.deep_animation:
            return
        deep_timeout, animation_name = self.deep_animation
        if need_show_trans_deep_ani and deep_timeout > 0 and time() - deep_timestamp < deep_timeout or deep_timeout <= 0:
            self._nd.PlayAnimation(animation_name)

    def stop_deep(self):
        if self.is_deep:
            return
        if not self.deep_animation:
            return
        deep_timeout, animation_name = self.deep_animation
        self._nd.StopAnimation(animation_name)
        self._nd.RecoverAnimationNodeState(animation_name)

    def set_state(self, state):
        if state < len(self.state_pic):
            ui_res_path = self.state_pic[state]
            if ui_res_path:
                self._nd.sp_circle.SetDisplayFrameByPath('', ui_res_path)

    def on_set_res_detail_index(self, detail_index):
        if self._res_detail_index != detail_index:
            super(CommonMapMark, self).on_set_res_detail_index(detail_index)
            self.set_deep(self.is_deep)

    def check_anim_pic(self):
        if not (hasattr(self._nd, 'img_anim') and self._nd.img_anim):
            return
        else:
            if type(self.ui_anim_res1) == list:
                if self._res_detail_index is not None and self._res_detail_index < len(self.ui_anim_res1):
                    self._nd.img_anim.SetDisplayFrameByPath('', self.ui_anim_res1[self._res_detail_index])
            else:
                self._nd.img_anim.SetDisplayFrameByPath('', self.ui_anim_res1)
            self._nd.img_anim.ReConfPosition()
            return

    def check_bigmap_action(self):
        if self.bigmap_action:
            anim = self.bigmap_action.get('anim', '')
            if anim:
                self.play_animation(anim)

    def get_distance_check(self):
        return self.distance_check

    def on_set_v3d_pos(self, v3d_pos):
        self._v3d_pos = v3d_pos
        self.map_pos = self.trans_world_position(self._v3d_pos)

    def get_v3d_pos(self):
        return self._v3d_pos

    def set_node_visible(self, is_vis):
        self._nd.setVisible(is_vis)


class MapDisturbCircle(MapScaleInterface):

    def __init__(self, parent_nd):
        from common.uisys.uielment.CCSprite import CCSprite
        from common.uisys.uielment.CCNode import CCNode
        super(MapDisturbCircle, self).__init__(parent_nd)
        self._nd = CCNode.Create()
        circle = CCSprite.Create(None, 'gui/ui_res_2/battle/map/circle_music.png')
        circle.setAnchorPoint(ccp(0.5, 0.5))
        circle.setOpacity(180)
        circle.setScale(2.0)
        icon = CCSprite.Create(None, 'gui/ui_res_2/battle/map/icon_music.png')
        icon.setAnchorPoint(ccp(0.5, 0.5))
        icon.setOpacity(130)
        self._nd.AddChild('', circle)
        self._nd.AddChild('', icon)
        self.parent_nd.AddChild('', self._nd)
        return

    def on_map_scale(self, map_scale):
        pass


class MapLocate(MapScaleInterface):

    def __init__(self, parent_nd, pos_trans_fun):
        super(MapLocate, self).__init__(parent_nd)
        self._nd = global_data.uisystem.load_template_create('map/ccb_map_locate')
        self.parent_nd.AddChild('', self._nd, Z=1)
        self.rotation = 0
        self.color = MAP_COL_BLUE
        self.type = LOCATE_NORMAL
        self.binded_event = {}
        self.target = None
        self.is_player = False
        self.pos_trans_fun = pos_trans_fun
        self.is_need_show_light = False
        self.locate_nd_pos_changed_callback = None
        self.start_tick()
        return

    def start_tick(self):
        import cc
        self._nd.runAction(cc.RepeatForever.create(cc.Sequence.create([
         cc.CallFunc.create(self.update_status),
         cc.DelayTime.create(0.1)])))

    def set_map_locate_color(self, color):
        self.color = color
        self.update_map_locate()

    def set_map_locate_type(self, type_info):
        self.type = type_info
        self.update_map_locate()
        self.setRotation(self.rotation)

    def update_map_locate(self):
        from logic.gutils.item_utils import get_locate_pic_path, get_locate_circle_path
        pic_path = get_locate_pic_path(self.type, self.color)
        self._nd.sp_locate.SetDisplayFrameByPath('', pic_path)
        circle_path = get_locate_circle_path(self.color)
        self._nd.sp_circle.SetDisplayFrameByPath('', circle_path)
        if self.is_need_show_light:
            self._nd.light.setVisible(True)
        else:
            self._nd.light.setVisible(False)

    def setRotation(self, rotation):
        self.rotation = rotation
        self._nd.nd_dir._obj.setRotation(rotation)

    def bind_dir_nd_with_target(self, target, is_player=False):
        self.unbind_events()
        self.target = target
        dead_func = self.on_locate_target_dead
        self.is_player = is_player
        target.regist_event('E_DEATH', dead_func)
        target.regist_event('E_AGONY', self.on_locate_target_down)
        target.regist_event('E_ON_SAVED', self.on_locate_saved)
        target.regist_event('E_ON_CONTROL_TARGET_CHANGE', self.on_switch_control_target, 10)
        target.regist_event('E_PARACHUTE_STATUS_CHANGED', self.on_parachute_change)
        target.regist_event('E_ON_STATUS_CHANGED', self.on_status_change)
        target.regist_event('E_PLANE', self.on_take_on_plane)
        target.regist_event('E_CONNECT_STATE', self.on_connect_state_change, 10)
        self.binded_event['E_DEATH'] = dead_func
        self.binded_event['E_AGONY'] = self.on_locate_target_down
        self.binded_event['E_ON_SAVED'] = self.on_locate_saved
        self.binded_event['E_ON_CONTROL_TARGET_CHANGE'] = self.on_switch_control_target
        self.binded_event['E_PARACHUTE_STATUS_CHANGED'] = self.on_parachute_change
        self.binded_event['E_ON_STATUS_CHANGED'] = self.on_status_change
        self.binded_event['E_PLANE'] = self.on_take_on_plane
        self.binded_event['E_CONNECT_STATE'] = self.on_connect_state_change
        is_dead = target.ev_g_death()
        ctrl_target = target.ev_g_control_target()
        if ctrl_target:
            self._bind_control_target_event(ctrl_target.id)
        else:
            self._bind_control_target_event(target.id)
        self.on_target_yaw_changed(0)
        if is_dead:
            self.on_locate_target_dead()
            model = target.ev_g_model()
            if model:
                self.on_target_pos_changed(model.world_position)
        else:
            self.on_check_cur_state()

    def _bind_control_target_event(self, control_target_id):
        return
        self._unbind_control_target_event()
        pos_func = self.on_target_pos_changed
        yaw_func = self.on_bind_puppet_yaw
        from mobile.common.EntityManager import EntityManager
        controll_target = EntityManager.getentity(control_target_id)
        if controll_target:
            if not self.is_player:
                controll_target.logic.regist_event('E_DELTA_YAW', yaw_func)
                self.binded_event['E_DELTA_YAW'] = (yaw_func, controll_target.id)
            pos = controll_target.logic.ev_g_position()
            controll_target.logic.regist_event('E_POSITION', pos_func)
            self.binded_event['E_POSITION'] = (pos_func, controll_target.id)
            self.on_target_pos_changed(pos)

    def _unbind_control_target_event(self):
        self.unbind_events(only_control_event=True)

    def unbind_events(self, only_control_event=False):
        del_event_list = []
        if self.target and self.target.unregist_event:
            for evt, func in six.iteritems(self.binded_event):
                if isinstance(func, tuple):
                    func, controller_id = func
                    _t = EntityManager.getentity(controller_id)
                    if _t:
                        _t = _t.logic
                else:
                    if only_control_event:
                        continue
                    _t = self.target
                if _t:
                    _t.unregist_event(evt, func)
                    del_event_list.append(evt)

        for e in del_event_list:
            del self.binded_event[e]

    def destroy(self):
        self.unbind_events()
        if self.target:
            self.target = None
        self.pos_trans_fun = None
        self.locate_nd_pos_changed_callback = None
        super(MapLocate, self).destroy()
        return

    def on_target_pos_changed(self, pos):
        map_pos = self.pos_trans_fun(pos)
        if map_pos:
            self.set_position(map_pos)

    def on_bind_puppet_yaw(self, *args):
        yaw = self.target.ev_g_yaw()
        self.on_target_yaw_changed(yaw)

    def on_target_yaw_changed(self, yaw):
        PI = 3.1415
        self.setRotation(yaw * 180 / PI)

    def on_locate_target_dead(self, *arg):
        self.set_map_locate_type(LOCATE_DEAD)

    def on_locate_target_down(self):
        self.set_map_locate_type(LOCATE_RECOURSE)

    def on_locate_saved(self, *args):
        if self.target:
            is_dying = self.target.ev_g_agony()
            if not is_dying and self.type != LOCATE_DEAD:
                self.set_map_locate_type(LOCATE_NORMAL)

    def need_show_light(self, is_need):
        self.is_need_show_light = is_need
        self.update_map_locate()

    def on_status_change(self):
        self.on_check_cur_state()

    def on_check_cur_state(self):
        from logic.gcommon.common_utils.parachute_utils import STAGE_PLANE, STAGE_FREE_DROP, STAGE_PARACHUTE_DROP
        if not self.target:
            return
        is_dead = False
        is_dying = False
        is_in_plane = False
        is_online = self.target.ev_g_connect_state()
        is_dead = self.target.ev_g_death()
        is_dying = self.target.ev_g_agony()
        parachute_stage = self.target.share_data.ref_parachute_stage
        is_in_plane = parachute_stage in (STAGE_PLANE,)
        is_in_parachute = parachute_stage in (STAGE_FREE_DROP, STAGE_PARACHUTE_DROP)
        if not is_online:
            self.set_map_locate_type(LOCATE_OFFLINE)
        elif is_dead:
            self.on_locate_target_dead()
        elif is_dying:
            self.on_locate_target_down()
        else:
            is_in_vehicle = self.target.ev_g_is_in_any_state((status_config.ST_MECHA_DRIVER, status_config.ST_MECHA_PASSENGER, status_config.ST_VEHICLE_GUNNER, status_config.ST_VEHICLE_PASSENGER))
            if is_in_parachute:
                self.set_map_locate_type(LOCATE_PARACHUTE)
            elif is_in_vehicle or is_in_plane:
                self.set_map_locate_type(LOCATE_DRIVE)
            else:
                self.set_map_locate_type(LOCATE_NORMAL)

    def on_switch_control_target(self, control_target_id, pos, *args):
        self._bind_control_target_event(control_target_id)
        self.on_check_cur_state()

    def on_parachute_change(self, *args):
        self.on_check_cur_state()

    def on_take_on_plane(self, *args):
        self.set_map_locate_type(LOCATE_DRIVE)

    def set_group_id(self, group_id):
        self._group_id = group_id
        self._nd.lab_team_no.SetString(str(group_id))
        self._show_group_id(True)

    def _show_group_id(self, is_show=True):
        self._nd.img_team_bg.setVisible(is_show)
        self._nd.lab_team_no.setVisible(is_show)

    def set_enable_click_func(self, func):
        if func:
            self._nd.btn.SetEnable(True)
            self._nd.btn.setVisible(True)
        else:
            self._nd.btn.SetEnable(False)
            self._nd.btn.setVisible(False)

        @self._nd.btn.unique_callback()
        def OnClick(*args):
            if func and callable(func):
                func()

    def set_select(self, is_sel):
        if is_sel:
            bg_pic = 'gui/ui_res_2/common/panel/pnl_team_no_bg_green.png'
        else:
            bg_pic = 'gui/ui_res_2/panel/pnl_team_no_bg.png'
        self._nd.img_team_bg.SetDisplayFrameByPath('', bg_pic)

    def on_connect_state_change(self, conn_state):
        if conn_state:
            self.on_check_cur_state()
        else:
            self.set_map_locate_type(LOCATE_OFFLINE)

    def update_pos(self):
        if self.target:
            position = self.target.ev_g_position()
            if position is not None:
                self.on_target_pos_changed(position)
        return

    def set_position(self, pos):
        super(MapLocate, self).set_position(pos)
        if self.locate_nd_pos_changed_callback:
            self.locate_nd_pos_changed_callback(pos)

    def set_locate_nd_pos_changed_callback(self, cb):
        self.locate_nd_pos_changed_callback = cb

    def update_status(self):
        if self.target:
            pos = self.target.ev_g_position()
            if pos:
                self.on_target_pos_changed(pos)
            if not self.is_player:
                yaw = self.target.ev_g_yaw()
                if yaw is not None:
                    self.on_target_yaw_changed(yaw)
        return


class MapSegment(MapScaleInterface):

    def __init__(self, nd, parent_nd, map_scale):
        super(MapSegment, self).__init__(parent_nd)
        self.map_scale = map_scale
        self._nd = nd
        self.is_nd_need_remove = False
        self.draw_lens = None
        self.color = None
        self._end_position = None
        self._nd.setTouchEnabled(False)
        return

    def show_line(self, start_map_pos, end_map_pos):
        super(MapSegment, self).on_map_scale(self.map_scale)
        item_sz = self._nd.GetContainer().GetCtrlSize()
        self._nd.setPosition(start_map_pos)
        self._end_position = end_map_pos
        diff_vec = cc.Vec2(end_map_pos)
        diff_vec.subtract(start_map_pos)
        angle = diff_vec.getAngle()
        self._nd.setRotation(-1 * angle * 180 / 3.1415)
        lens = diff_vec.getLength()
        self.draw_lens = lens
        try:
            item_count = abs(int(lens / (item_sz.width * self._nd.getScale()))) + 1
        except Exception as e:
            print('start map pos ', start_map_pos, end_map_pos)
            print('lens ,item_sz.width', lens, item_sz.width, diff_vec)
            raise

        self._nd.SetInitCount(max(item_count, 0))
        self._nd.SetContentSize(lens / self._nd.getScale(), self._nd.getContentSize().height)

    def set_color(self, color):
        self.color = color
        from common.utils.cocos_utils import ccc3FromHex
        for item in self._nd.GetAllItem():
            item.sp_dir.SetColor(color)

    def on_map_scale(self, map_scale):
        import math
        self.map_scale = map_scale
        super(MapSegment, self).on_map_scale(map_scale)
        if not self.draw_lens:
            return
        item_sz = self._nd.GetContainer().GetCtrlSize()
        new_item_count = abs(int(self.draw_lens / (item_sz.width * self._nd.getScale()))) + 1
        self._nd.SetInitCount(new_item_count)
        if self.color:
            self.set_color(self.color)
        self._nd.SetContentSize(self.draw_lens / self._nd.getScale(), self._nd.getContentSize().height)

    def get_end_position(self):
        return self._end_position


class DirectLine(MapScaleInterface):

    def __init__(self, map_panel, parent_nd, map_scale, has_tail=False, z=0):
        super(DirectLine, self).__init__(parent_nd, map_panel)
        from common.uisys.uielment.CCHorzTemplateList import CCHorzTemplateList
        self.template_name = 'map/ccb_plane_line'
        self.map_scale = map_scale
        container = CCHorzTemplateList.Create()
        self.init_container(container, indent=4)
        self.container_height = container.GetCtrlSize().height
        self._nd = container
        self.draw_lens = None
        self.parent_nd.AddChild(None, self._nd, Z=z)
        if has_tail:
            tail = CCSprite.Create(None, 'gui/ui_res_2/battle_before/img_map_line_flight_arrow.png')
            tail.setAnchorPoint(ccp(0.0, 0.5))
            self.parent_nd.AddChild(None, tail, Z=z + 1)
            self.tail_spirte = tail
            self.tail_spirte_original_scale = 1
        else:
            self.tail_spirte = None
        self._fix_scale = 233
        self._nd.setTouchEnabled(False)
        return

    def destroy(self):
        super(DirectLine, self).destroy()
        if self.tail_spirte:
            self.tail_spirte.Destroy()
            self.tail_spirte = None
        return

    def init_container(self, container, indent=0):
        initCount = 0
        numPerUnit = 1
        template_conf = global_data.uisystem.load_template(self.template_name)
        container.SetNumPerUnit(numPerUnit)
        container.SetHorzBorder(0)
        container.SetVertBorder(0)
        container.SetHorzIndent(indent)
        container.SetVertIndent(0)
        container.SetTemplateConf(template_conf)
        container.SetInitCount(initCount)

    def draw(self, start_world_pos, end_world_pos):
        start_map_pos = self.trans_world_position(start_world_pos)
        end_map_pos = self.trans_world_position(end_world_pos)
        scale = self.map_scale
        super(DirectLine, self).on_map_scale(scale)
        container = self._nd
        self._nd.setAnchorPoint(ccp(0, 0.5))
        item_sz = container.GetCtrlSize()
        self._nd.setPosition(start_map_pos)
        diff_vec = cc.Vec2(end_map_pos)
        diff_vec.subtract(start_map_pos)
        angle = diff_vec.getAngle()
        self._nd.setRotation(-1 * angle * 180 / 3.1415)
        lens = diff_vec.getLength()
        self.draw_lens = lens
        try:
            item_count = abs(int(lens / (item_sz.width * self._nd.getScale()))) + 1
        except Exception as e:
            print('start map pos ', start_map_pos, end_map_pos)
            print('lens ,item_sz.width', lens, item_sz.width, diff_vec)
            raise

        self._nd.SetInitCount(item_count)
        self._nd.SetContentSize(lens / self._nd.getScale(), self.container_height)
        if self.tail_spirte:
            self.tail_spirte.setScale(self.tail_spirte_original_scale * 1.0 / scale)
            diff_vec_copy = cc.Vec2(diff_vec)
            diff_vec_copy.normalize()
            offset = 0
            diff_vec_copy.scale(offset)
            arrow_pos = cc.Vec2(end_map_pos)
            arrow_pos.add(diff_vec_copy)
            self.tail_spirte.setPosition(arrow_pos)
            self.tail_spirte.setRotation(-1 * angle * 180 / 3.1415)

    def on_map_scale(self, map_scale):
        item_sz = self._nd.GetCtrlSize()
        super(DirectLine, self).on_map_scale(map_scale)
        if not self.draw_lens:
            return
        new_item_count = abs(int(self.draw_lens / (item_sz.width * self._nd.getScale()))) + 1
        self._nd.SetInitCount(new_item_count)
        self._nd.SetContentSize(self.draw_lens / self._nd.getScale(), self.container_height)
        if self.tail_spirte:
            self.tail_spirte.setScale(self.tail_spirte_original_scale * 1.0 / map_scale)


class CircleArcLine(MapScaleInterface):

    def __init__(self, parent_nd, map_scale, draw_indent=100):
        super(CircleArcLine, self).__init__(parent_nd)
        self.draw_indent = draw_indent
        self.map_scale = map_scale
        self.child_list = []
        self._free_nd = []
        self.is_drawed = False
        self._start_pos = None
        self._end_pos = None
        self._center_pos = None
        self._angle_diff = None
        self._radius = None
        self._length = None
        return

    def set_brush(self, pic_path='gui/ui_res_2/battle/map/plane_line.png'):
        self._pic_path = pic_path
        nd = CCSprite.Create('', pic_path)
        self.draw_indent = nd.getContentSize().width

    def get_line_segment(self):
        if len(self._free_nd) > 0:
            return self._free_nd.pop()
        nd = CCSprite.Create('', self._pic_path)
        self.parent_nd.AddChild('', nd, Z=0)
        self.child_list.append(nd)
        return nd

    def release_cur_line(self, is_destroy=False):
        for nd in self.child_list:
            nd.Destroy()

        self.child_list = []

    def draw_circle_data(self, start_pos, end_pos, center_pos, angle_range):
        self._start_pos = start_pos
        self._end_pos = end_pos
        self._center_pos = center_pos
        diff_vec = cc.Vec2(end_pos)
        diff_vec.subtract(center_pos)
        radius = diff_vec.getLength()
        ang_diff = -angle_range / 180.0 * 3.1415
        arc_length = abs(ang_diff) * radius
        self._angle_diff = ang_diff
        self._radius = radius
        self._length = arc_length
        self._real_draw()

    def _real_draw(self):
        if not self._start_pos:
            return
        if self.is_drawed:
            self.release_cur_line()
        self.is_drawed = True
        draw_num = self._length * self.map_scale / self.draw_indent
        angle_delta = self._angle_diff / draw_num
        for i in range(1, int(round(draw_num)) + 1):
            nd_seg = self.get_line_segment()
            cur_pos = cc.Vec2(self._start_pos)
            cur_pos.rotate(self._center_pos, angle_delta * i)
            nd_seg.setPosition(cur_pos)
            cur_pos.subtract(self._center_pos)
            cur_angle = cur_pos.getAngle() * 180 / 3.1415 + 90
            nd_seg.setRotation(-1 * cur_angle)

        self.set_nd_scale(self.map_scale)

    def destroy(self):
        super(CircleArcLine, self).destroy()
        self.release_cur_line(is_destroy=True)
        self.child_list = []
        self.release_free_nd()

    def release_free_nd(self):
        for nd in self._free_nd:
            nd.Destroy()

        self._free_nd = []

    def set_nd_scale(self, scale):
        for _nd in self.child_list:
            _nd.setScale(1.0 / scale)

    def on_map_scale(self, map_scale):
        self.map_scale = map_scale
        self._real_draw()


class MapAirLine(MapScaleInterface):

    def __init__(self, nd, map_scale):
        super(MapAirLine, self).__init__(None)
        self._nd = nd
        self.is_nd_need_remove = False
        self.map_scale = map_scale
        self.parts = []
        return

    def add_line(self, start_pos, end_pos):
        dl = DirectLine(self._nd, self.map_scale)
        dl.draw(start_pos, end_pos)
        self.parts.append(dl)

    def add_circle_arc(self, start_pos, end_pos, center_pos, angle_range):
        arc_line = CircleArcLine(self._nd, self.map_scale)
        arc_line.set_brush()
        arc_line.draw_circle_data(start_pos, end_pos, center_pos, angle_range)
        self.parts.append(arc_line)

    def destroy(self):
        for part in self.parts:
            part.destroy()

        self.parts = []
        super(MapAirLine, self).destroy()

    def on_map_scale(self, map_scale):
        self.map_scale = map_scale
        for part in self.parts:
            part.on_map_scale(map_scale)


class MapMoveablePoint(MapScaleInterface):

    def __init__(self, map_panel, parent_nd, map_scale, pic_path, z=0, updater=None):
        super(MapMoveablePoint, self).__init__(parent_nd, map_panel)
        self.map_scale = map_scale
        sprite = CCSprite.Create(None, pic_path)
        self.parent_nd.AddChild(None, sprite, Z=z)
        sprite.setVisible(False)
        if callable(updater):

            def _updater():
                updater(self)

            import cc
            sprite.runAction(cc.RepeatForever.create(cc.Sequence.create([
             cc.CallFunc.create(_updater),
             cc.DelayTime.create(0.1)])))
        self._nd = sprite
        return

    def destroy(self):
        self._nd.stopAllActions()
        super(MapMoveablePoint, self).destroy()

    def refresh(self, world_pos):
        if world_pos is None:
            self._nd.setVisible(False)
            return
        else:
            self._nd.setVisible(True)
            map_pos = self.trans_world_position(world_pos)
            spirte = self._nd
            spirte.setPosition(map_pos)
            scale = self.map_scale
            super(MapMoveablePoint, self).on_map_scale(scale)
            return

    def on_map_scale(self, map_scale):
        self.map_scale = map_scale
        super(MapMoveablePoint, self).on_map_scale(map_scale)


class ChartLine(MapScaleInterface):

    def __init__(self, parent_nd, map_scale, z=0, frame_path=''):
        super(ChartLine, self).__init__(parent_nd)
        self.map_scale = map_scale
        self.container_list = []

    def add_container(self, indent, template_name, z):
        from common.uisys.uielment.CCHorzTemplateList import CCHorzTemplateList
        container = CCHorzTemplateList.Create()
        self.init_container(container, template_name, indent=indent)
        self.container_height = container.GetCtrlSize().height
        self._nd = container
        self.draw_lens = None
        self.parent_nd.AddChild(None, self._nd, Z=z)
        self._nd.setTouchEnabled(False)
        self.container_list.append(self._nd)
        return len(self.container_list) - 1

    def destroy(self):
        self._nd = None
        super(ChartLine, self).destroy()
        self.delete_all_container()
        return

    def init_container(self, container, template_name, indent=0):
        initCount = 0
        num_per_unit = 1
        template_conf = global_data.uisystem.load_template(template_name)
        container.SetNumPerUnit(num_per_unit)
        container.SetHorzBorder(0)
        container.SetVertBorder(0)
        container.SetHorzIndent(indent)
        container.SetVertIndent(0)
        container.SetTemplateConf(template_conf)
        container.SetInitCount(initCount)

    def draw(self, start_map_pos, end_map_pos, indent, template_name, index=None):
        if not index:
            ret = self.add_container(indent, template_name, 0)
        else:
            ret = None
            self._nd = self.container_list[index]
        scale = self.map_scale
        super(ChartLine, self).on_map_scale(scale)
        container = self._nd
        self._nd.setAnchorPoint(ccp(0, 0.5))
        item_sz = container.GetCtrlSize()
        self._nd.setPosition(start_map_pos)
        diff_vec = cc.Vec2(end_map_pos)
        diff_vec.subtract(start_map_pos)
        angle = diff_vec.getAngle()
        self._nd.setRotation(-1 * angle * 180 / 3.1415)
        lens = diff_vec.getLength()
        self.draw_lens = lens
        try:
            item_count = abs(int(lens / (item_sz.width * self._nd.getScale()))) + 1
        except Exception as e:
            raise

        self._nd.SetInitCount(item_count)
        self._nd.SetContentSize(lens / self._nd.getScale(), self.container_height)
        return ret

    def delete_all_container(self):
        for container in self.container_list:
            if isinstance(container, CCNode):
                container.Destroy()
            else:
                container.removeFromParent()

        self.container_list = []
        self._nd = None
        return