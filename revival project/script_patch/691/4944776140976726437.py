# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/screen_utils.py
from __future__ import absolute_import
from common.utils.cocos_utils import neox_pos_to_cocos, cocos_screen_pos_to_cocos_design_pos
import cc
import math

def limit_pos_in_screen_normal(screen_size, is_full_screen, x, y, scale_data):
    scale_90 = scale_data.get('scale_90', (0, 0))
    scale_40 = scale_data.get('scale_40', (0, 0))
    scale_90 = scale_90[0] if is_full_screen else scale_90[1]
    scale_40 = scale_40[0] if is_full_screen else scale_40[1]
    new_pos_x = max(min(x, screen_size.width - scale_90), scale_90)
    new_pos_y = max(min(y, screen_size.height - scale_40), scale_40)
    return (
     new_pos_x, new_pos_y)


def limit_pos_in_screen(screen_size, is_full_screen, x, y, scale_data):
    scale_left = scale_data.get('scale_left', (0, 0))
    scale_right = scale_data.get('scale_right', (0, 0))
    scale_up = scale_data.get('scale_up', (0, 0))
    scale_low = scale_data.get('scale_low', (0, 0))
    scale_left = scale_left[0] if is_full_screen else scale_left[1]
    scale_right = scale_right[0] if is_full_screen else scale_right[1]
    scale_up = scale_up[0] if is_full_screen else scale_up[1]
    scale_low = scale_low[0] if is_full_screen else scale_low[1]
    if x > 0:
        new_pos_x = max(min(x, screen_size.width - scale_right), scale_right)
    else:
        new_pos_x = max(min(x, screen_size.width - scale_left), scale_left)
    if y > 0:
        new_pos_y = max(min(y, screen_size.height - scale_low), scale_low)
    else:
        new_pos_y = max(min(y, screen_size.height - scale_up), scale_up)
    return (new_pos_x, new_pos_y)


def get_dist_in_rect_angle(screen_size, screen_angle_limit, angle):
    if angle > 180:
        x, y = get_dist_in_rect_angle(screen_size, screen_angle_limit, 360 - angle)
        return (
         x, -y)
    else:
        if angle > 90:
            x, y = get_dist_in_rect_angle(screen_size, screen_angle_limit, 180 - angle)
            return (
             -x, y)
        if angle <= screen_angle_limit:
            return (screen_size.width / 2.0, screen_size.width / 2.0 * math.tan(math.radians(angle)))
        return (
         screen_size.height / 2.0 * math.tan(math.radians(90 - angle)), screen_size.height / 2.0)


def world_pos_to_screen_pos(nd, position, screen_size, screen_angle_limit, is_full_screen, scale_data={}):
    camera = global_data.game_mgr.scene.active_camera
    if not camera:
        return (False, cc.Vec2(0, 0), 0)
    x, y = camera.world_to_screen(position)
    new_x, new_y = limit_pos_in_screen_normal(screen_size, is_full_screen, x, y, scale_data)
    in_screen = new_x == x and new_y == y
    if in_screen:
        new_x, new_y = neox_pos_to_cocos(new_x, new_y)
        pos = nd.getParent().convertToNodeSpace(cc.Vec2(new_x, new_y))
        angle = 0
    else:
        cam_pos = camera.world_to_camera(position)
        mid_point = cc.Vec2(screen_size.width / 2.0, screen_size.height / 2.0)
        angle = math.atan2(cam_pos.y, cam_pos.x)
        angle = angle * 180 / math.pi
        if angle < 0:
            angle += 360
        dist_x, dist_y = get_dist_in_rect_angle(screen_size, screen_angle_limit, angle)
        mid_point.add(cc.Vec2(dist_x, dist_y))
        dist_x, dist_y = limit_pos_in_screen(screen_size, is_full_screen, mid_point.x, mid_point.y, scale_data)
        dist_x, dist_y = cocos_screen_pos_to_cocos_design_pos(dist_x, dist_y)
        pos = nd.getParent().convertToNodeSpace(cc.Vec2(dist_x, dist_y))
        angle = -angle
    return (in_screen, pos, angle)


def world_to_screen_ellipse_pos(nd, position, screen_size, screen_angle_limit, is_full_screen, scale_data={}):
    camera = global_data.game_mgr.scene.active_camera
    if not camera:
        return (False, cc.Vec2(0, 0), 0)
    x, y = camera.world_to_screen(position)
    new_x, new_y = limit_pos_in_screen_normal(screen_size, is_full_screen, x, y, scale_data)
    in_screen = new_x == x and new_y == y
    if in_screen:
        new_x, new_y = neox_pos_to_cocos(new_x, new_y)
        pos = nd.getParent().convertToNodeSpace(cc.Vec2(new_x, new_y))
        angle = 0
    else:
        cam_pos = camera.world_to_camera(position)
        mid_point = cc.Vec2(screen_size.width / 2.0, screen_size.height / 2.0)
        angle = math.atan2(cam_pos.y, cam_pos.x)
        angle = angle * 180 / math.pi
        if angle < 0:
            angle += 360
        dist_x, dist_y = get_dist_in_rect_angle(screen_size, screen_angle_limit, angle)
        mid_point.add(cc.Vec2(dist_x, dist_y))
        b_x, t_x, b_y, t_y = get_ellipse_ori_rect(screen_size, is_full_screen, scale_data)
        center_x = (t_x - b_x) / 2.0 + b_x
        center_y = (t_y - b_y) / 2.0 + b_y
        e_a = center_x * 0.65
        e_b = center_y * 0.75
        radian = angle / 180 * math.pi
        t = math.tan(radian)
        x = math.sqrt(e_a * e_a * e_b * e_b / (e_b * e_b + e_a * e_a * t * t))
        if 90 < angle < 270:
            x = -x
        y = x * t
        x += center_x
        y += center_y
        x, y = cocos_screen_pos_to_cocos_design_pos(x, y)
        pos = nd.getParent().convertToNodeSpace(cc.Vec2(x, y))
        angle = -angle
    return (
     in_screen, pos, angle)


def get_ellipse_ori_rect(screen_size, is_full_screen, scale_data):
    scale_left = scale_data.get('scale_left', (0, 0))
    scale_right = scale_data.get('scale_right', (0, 0))
    scale_up = scale_data.get('scale_up', (0, 0))
    scale_low = scale_data.get('scale_low', (0, 0))
    scale_left = scale_left[0] if is_full_screen else scale_left[1]
    scale_right = scale_right[0] if is_full_screen else scale_right[1]
    scale_up = scale_up[0] if is_full_screen else scale_up[1]
    scale_low = scale_low[0] if is_full_screen else scale_low[1]
    return (
     scale_left, screen_size.width - scale_right, scale_up, screen_size.height - scale_low)