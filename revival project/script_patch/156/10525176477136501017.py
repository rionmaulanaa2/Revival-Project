# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/ui_distortor/UIDistortHelper.py
from __future__ import absolute_import
import six
_reload_all = True
from common.utils.ui_utils import s_designWidth, s_designHeight, s_bg_yRate, s_bg_xRate
from common.framework import Singleton
import cc
import math
from common.utils.ui_utils import s_designWidth, s_designHeight
from common.utils.cocos_utils import CCSize
import copy
from common.const import cocos_constant

def linear_inter(x_val, min_val, max_val, x0=0, x1=1):
    return (x_val - x0) / (x1 - x0) * (max_val - min_val) + min_val


def abs_center_percent_linear(x_val, min_val, max_val, x_center=0.5):
    x_val = abs(x_val - x_center) * 2
    return linear_inter(x_val, min_val, max_val)


def sign_sqrt_abs_center_percent_linear(x_val, min_val, max_val, x_center=0.5):
    sign = -1 if x_val - x_center < 0 else 1
    x_val = sign * math.sqrt(abs(x_val - x_center) * 2)
    return linear_inter(x_val, min_val, max_val)


def x_y_center_linear(x, y, min_val, max_val, center_x=0.5, center_y=0.5):
    sign = -1 if x - center_x > 0 else 1
    return sign * linear_inter((x - center_x) / 0.5 * (y - center_y) / 0.5, min_val, max_val)


def x_y_center_linear_no_sign(x, y, min_val, max_val, center_x=0.5, center_y=0.5):
    return linear_inter((x - center_x) / 0.5 * (y - center_y) / 0.5, min_val, max_val)


def x_abs_center_percent_linear_y_center_linear(x, y, min_val, max_val, center_x=0.5, center_y=0.5):
    max_val = abs_center_percent_linear(x, min_val, max_val)
    return linear_inter((y - center_y) / 0.5, min_val, max_val)


def bound_val(val, bottom_val, ceil_val):
    return max(min(val, ceil_val), bottom_val)


def is_can_ui_distort():
    from logic.gutils.judge_utils import is_ob
    return not is_ob()


from logic.gutils.judge_utils import disable_execute_for_judge

class UIDistorter(object):

    def __init__(self):
        self._transform_func_list = []

    def set_conf(self, conf):
        self._conf = conf
        self._parse_conf(conf)

    def get_conf(self):
        return self._conf

    def _parse_conf(self, conf):
        self._transform_func_list = []
        key2attr_func = {'rotation_x': UIDistorter.setRotation3DX,
           'rotation_y': UIDistorter.setRotation3DY,
           'rotation_z': UIDistorter.setRotation3DZ,
           'skew_y': UIDistorter.setSkewY,
           'scale_x': UIDistorter.setScaleX
           }
        for attr_key, cal_conf in six.iteritems(conf):
            attr_func = key2attr_func.get(attr_key, None)
            cal_func = self._parse_cal_conf(cal_conf)
            if attr_func and cal_func:

                def _func(node, x, y, attr_func=attr_func, cal_func=cal_func, **kwargs):
                    attr_func(node, cal_func(x, y, **kwargs))

                self._transform_func_list.append(_func)

        return

    def _parse_cal_conf(self, cal_conf):
        func = None
        cal_type, parameters, res_range = cal_conf
        bottom_val, ceil_val = res_range
        if bottom_val > ceil_val:
            bottom_val, ceil_val = ceil_val, bottom_val

        def add_bound_check(_func):

            def _func_with_bound(x, y, **kwargs):
                return bound_val(_func(x, y, **kwargs), bottom_val, ceil_val)

            return _func_with_bound

        if cal_type == 'X_LINEAR':
            min_val, max_val = parameters

            def func(x, y, **kwargs):
                return linear_inter(x, min_val, max_val)

        elif cal_type == 'X_SIGN_SQRT_ABS_CENTER_LINEAR':
            min_val, max_val = parameters

            def func(x, y, **kwargs):
                return sign_sqrt_abs_center_percent_linear(x, min_val, max_val)

        elif cal_type == 'Y_LINEAR':
            min_val, max_val = parameters

            def func(x, y, **kwargs):
                return linear_inter(y, min_val, max_val)

        elif cal_type == 'X_ABS_CENTER_LINEAR':
            min_val, max_val = parameters

            def func(x, y, **kwargs):
                return abs_center_percent_linear(x, min_val, max_val)

        elif cal_type == 'X_Y_CENTER_LINEAR':
            min_val, max_val = parameters

            def func(x, y, **kwargs):
                return x_y_center_linear(x, y, min_val, max_val)

        elif cal_type == 'X_Y_CENTER_LINEAR_NO_SIGN':
            min_val, max_val = parameters

            def func(x, y, **kwargs):
                return x_y_center_linear_no_sign(x, y, min_val, max_val)

        if func:
            return add_bound_check(func)
        else:
            return

    def get_percent(self, node, pos=None):
        if pos is None:
            pos = node.getPosition()
        node_wpos = node.getParent().convertToWorldSpace(pos)
        x_per = node_wpos.x / s_bg_xRate / s_designWidth
        y_per = node_wpos.y / s_bg_yRate / s_designHeight
        return (
         x_per, y_per)

    def transform_node(self, node, pos=None):
        if pos is None:
            pos = node.getPosition()
        node_wpos = node.getParent().convertToWorldSpace(pos)
        x_per = node_wpos.x / s_bg_xRate / s_designWidth
        y_per = node_wpos.y / s_bg_yRate / s_designHeight
        for func in self._transform_func_list:
            func(node, x_per, y_per)

        return (x_per, y_per)

    @staticmethod
    def setRotation3DY(node, y):
        old_rot = node.getRotation3D()
        old_rot.y = y
        node.setRotation3D(old_rot)

    @staticmethod
    def setRotation3DZ(node, z):
        old_rot = node.getRotation3D()
        old_rot.z = z
        node.setRotation3D(old_rot)

    @staticmethod
    def setRotation3DX(node, x):
        old_rot = node.getRotation3D()
        old_rot.x = x
        node.setRotation3D(old_rot)

    @staticmethod
    def setSkewY(node, skew_y):
        node.setSkewY(skew_y)

    @staticmethod
    def setScaleX(node, scale_x):
        node.setScaleX(scale_x)


class UIDistorterHelper(Singleton):
    ALIAS_NAME = 'ui_distorter_helper'

    def init(self):
        self._distorter_dict = {}
        self._scaleCalculator = DistortScaleCalculator()
        self._is_enable = True
        self._scale_x_cache = {}
        self._node_world_pos_cache = {}
        global_data.emgr.reconf_all_ui_before += self.on_resolution_changed

    def on_finalize(self):
        global_data.emgr.reconf_all_ui_before -= self.on_resolution_changed

    def record_ui_parameters(self, ui_name):
        if ui_name in self._node_world_pos_cache:
            return
        ui_inst = global_data.ui_mgr.get_ui(ui_name)
        if not ui_inst:
            return
        distort_type, node_list = self.get_ui_parameter(ui_name)
        if distort_type:
            self._node_world_pos_cache.setdefault(ui_name, {})
            for node_name in node_list:
                node = getattr(ui_inst.panel, node_name)
                if not node:
                    continue
                wpos = node.GetParent().convertToWorldSpace(node.getPosition())
                self._node_world_pos_cache[ui_name][node_name] = wpos

    def get_ui_parameter(self, ui_name):
        from common.cfg import confmgr
        distort_ui_conf = confmgr.get('distort_ui_conf', 'MechaUIConf', 'Content')
        conf = distort_ui_conf.get(ui_name, {})
        if not conf:
            return (None, None)
        else:
            distort_type = conf.get('distort_type', '')
            node_list = conf.get('node_list', [])
            return (
             distort_type, node_list)

    @disable_execute_for_judge()
    def apply_ui_distort(self, ui_name):
        ui_inst = global_data.ui_mgr.get_ui(ui_name)
        if not ui_inst:
            return
        distort_type, node_list = self.get_ui_parameter(ui_name)
        if distort_type:
            for node_name in node_list:
                node = getattr(ui_inst.panel, node_name)
                if not node:
                    continue
                node_key = '-'.join([ui_name, node_name])
                self.apply_node_distort(distort_type, node, ui_inst.panel, node_key, ui_name, node_name)

    def cancel_ui_distort(self, ui_name):
        if not self._is_enable:
            return
        ui_inst = global_data.ui_mgr.get_ui(ui_name)
        if not ui_inst:
            return
        distort_type, node_list = self.get_ui_parameter(ui_name)
        if not distort_type:
            return
        for node_name in node_list:
            node = getattr(ui_inst.panel, node_name)
            if not node or not node.isValid():
                continue
            node.setScaleX(1.0)
            node.setRotation3D(cc.Vec3(0, 0, 0))
            node.setSkewY(0)
            node.ChangeAllChildrenClippingType(cocos_constant.CLIPPING_SCISSOR)

    def apply_node_distort(self, distort_type, node, panel, node_key=None, ui_name=None, node_name=None):
        if not self._is_enable:
            return
        else:
            if distort_type not in self._distorter_dict:
                distorter = self._generate_distorter(distort_type)
                if distorter:
                    self._distorter_dict[distort_type] = distorter
            if distort_type not in self._distorter_dict:
                return
            node.ChangeAllChildrenClippingType(cocos_constant.CLIPPING_STENCIL)
            distorter = self._distorter_dict[distort_type]
            x_per, y_per = distorter.get_percent(node)
            if distort_type == 'MECHA_BUTTON':
                if node_key and node_key in self._scale_x_cache:
                    init_scale_x, min_val, max_val = self._scale_x_cache[node_key]
                else:
                    node_ori_wpos = None
                    if node_name and ui_name:
                        node_ori_wpos = self._node_world_pos_cache.get(ui_name, {}).get(node_name, None)
                    init_scale_x = self._scaleCalculator.get_resolution_size_scale(node, panel, node_ori_wpos)
                    min_val, max_val = (1.0, 1.0)
                    if init_scale_x > 1.0:
                        min_val = 1 / init_scale_x
                        max_val = (1 - min_val) / max(abs(x_per - 0.5), 0.001) * 0.5 + min_val
                    if node_key:
                        self._scale_x_cache[node_key] = (
                         init_scale_x, min_val, max_val)
                distorter.transform_node(node)
                modify_scale_x = abs_center_percent_linear(x_per, min_val, max_val, x_center=0.5)
                scale_x = init_scale_x * modify_scale_x
                node.setScaleX(1.0 / scale_x)
            else:
                distorter.transform_node(node)
            return

    def _generate_distorter(self, distort_type):
        from common.cfg import confmgr
        distort_type_conf = confmgr.get('distort_ui_conf', 'DistortConf', 'Content')
        conf = distort_type_conf.get(distort_type, {})
        if conf:
            distorter = UIDistorter()
            distorter.set_conf(conf)
            return distorter
        else:
            return None

    def _apply_ui_z_distort(self, ui_name):
        ui_inst = global_data.ui_mgr.get_ui(ui_name)
        if not ui_inst:
            return
        z_dict = self.get_ui_z_parameter(ui_name)
        for height, nd_list in six.iteritems(z_dict):
            for nd_name in nd_list:
                ctrl = ui_inst.panel
                ctrlnamelist = nd_name.split('.')
                for name in ctrlnamelist:
                    ctrl = getattr(ctrl, name)
                    if not ctrl:
                        break

                if ctrl:
                    ctrl.setPositionZ(height)

    def _cancel_ui_z_distort(self, ui_name):
        ui_inst = global_data.ui_mgr.get_ui(ui_name)
        if not ui_inst:
            return
        z_dict = self.get_ui_z_parameter(ui_name)
        for height, nd_list in six.iteritems(z_dict):
            for nd_name in nd_list:
                nd = getattr(ui_inst, nd_name)
                if nd:
                    nd.setPositionZ(0)

    def get_ui_z_parameter(self, ui_name):
        from common.cfg import confmgr
        ui_z_conf = confmgr.get('distort_ui_conf', 'MechaUIZConf', 'Content')
        conf = ui_z_conf.get(ui_name, {})
        level_heights = conf.get('level_height', [])
        z_dict = {}
        for idx, height in enumerate(level_heights):
            nd_list = conf.get('level_%d' % (idx + 1), [])
            if nd_list:
                z_dict[height] = nd_list

        return z_dict

    def on_resolution_changed(self):
        self._scale_x_cache = {}
        self._node_world_pos_cache = {}
        if self._scaleCalculator:
            self._scaleCalculator.update_screen_config()


class DistortScaleCalculator(object):

    def __init__(self):
        self.update_screen_config()

    PREFER_SIZE = (s_designWidth, s_designHeight)

    def update_screen_config(self):
        self.cur_center_x = global_data.ui_mgr.design_screen_size.width / 2.0
        self.def_center_x = self.PREFER_SIZE[0] / 2.0
        director = cc.Director.getInstance()
        self.zeye = director.getZEye()

    def get_resolution_size_scale(self, nd, panel, node_ori_wpos=None):
        dsize = global_data.ui_mgr.design_screen_size
        ratio = float(dsize.width) / dsize.height
        design_ratio = float(s_designWidth) / s_designHeight
        if ratio <= design_ratio:
            return 1.0
        if node_ori_wpos:
            wpos = node_ori_wpos
        else:
            wpos = nd.GetParent().convertToWorldSpace(nd.getPosition())
        def_pos = self.CalcConfPositionInSize(nd, panel, self.PREFER_SIZE[0], self.PREFER_SIZE[1])
        if not def_pos:
            return 1.0
        def_pos_x = def_pos.x
        w_len = nd.getContentSize().width
        cur_rot = nd.getRotation3D()
        theta_y = math.radians(cur_rot.y)
        cos_y = math.cos(theta_y)
        sin_y = math.sin(theta_y)
        new_x1 = (wpos.x - self.cur_center_x + 0.5 * w_len * cos_y) / (self.zeye + 0.5 * w_len * sin_y)
        new_x2 = (wpos.x - self.cur_center_x - 0.5 * w_len * cos_y) / (self.zeye - 0.5 * w_len * sin_y)
        new_x_size = abs(new_x1 - new_x2)
        old_x1 = (def_pos_x - self.def_center_x + 0.5 * w_len * cos_y) / (self.zeye + 0.5 * w_len * sin_y)
        old_x2 = (def_pos_x - self.def_center_x - 0.5 * w_len * cos_y) / (self.zeye - 0.5 * w_len * sin_y)
        old_x_size = abs(old_x1 - old_x2)
        if old_x_size > 0:
            new_scale_x = new_x_size / old_x_size
        else:
            new_scale_x = 1
        return new_scale_x

    def CalcConfPositionInSize(self, nd, panel, width, height):
        widget_name = nd.GetName()
        nd_tracks = [nd]
        nd_var = nd
        while nd_var and nd_var.GetParent() != panel:
            parent = nd_var.GetParent()
            nd_tracks.append(parent)
            nd_var = parent

        top_nd = nd_tracks[-1]
        if top_nd.GetParent() != panel:
            log_error('panel is not the ancestor of nd!')
            return None
        else:
            from_size = cc.Size(width, height)
            from common.uisys.uielment.CCNode import CCNode
            screen_nd = CCNode.Create()
            screen_nd.setContentSize(from_size)
            screen_nd.setPosition(cc.Vec2(0, 0))
            screen_nd.setAnchorPoint(cc.Vec2(0, 0))
            if not panel.IsCSBNode():
                top_nd = panel
                conf = top_nd.GetConf() or {}
                nd_conf = dict(conf)
                nd_conf['child_list'] = []
                top_child_conf = nd_conf
                for old_nd in reversed(nd_tracks):
                    conf = dict(old_nd.GetConf())
                    conf['child_list'] = []
                    nd_conf['child_list'].append(conf)
                    nd_conf = conf

                final_nd = global_data.uisystem.create_item(top_child_conf, screen_nd)
            else:
                top_nd = panel.cloneNode()
                screen_nd.addChild(top_nd)
                for old_nd in reversed(nd_tracks):
                    top_nd.addChild(old_nd.cloneNode())

                final_nd = top_nd
                from common.uisys.cocomate import do_cocomate_layout
                do_cocomate_layout(final_nd)
            nd = getattr(final_nd, widget_name)
            if nd:
                lpos = nd.getPosition()
                wpos = nd.getParent().convertToWorldSpace(lpos)
                return final_nd.convertToNodeSpace(wpos)
            return None

    def get_in_pos_width(self, w_len, rot_y, node_ori_wpos=None):
        theta_y = math.radians(rot_y)
        cos_y = math.cos(theta_y)
        sin_y = math.sin(theta_y)
        wpos = node_ori_wpos
        new_x1 = (wpos.x - self.cur_center_x + 0.5 * w_len * cos_y) / (self.zeye + 0.5 * w_len * sin_y)
        new_x2 = (wpos.x - self.cur_center_x - 0.5 * w_len * cos_y) / (self.zeye - 0.5 * w_len * sin_y)
        new_x_size = abs(new_x1 - new_x2)
        return new_x_size