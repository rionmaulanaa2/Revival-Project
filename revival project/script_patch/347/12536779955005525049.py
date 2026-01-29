# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/setting_ui/BattleCustomButtonUI.py
from __future__ import absolute_import
import six_ex
import six
from six.moves import range
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER
from logic.comsys.setting_ui.SimpleLabelUIBase import SimpleLabelUIBase
from logic.gcommon.common_const import ui_operation_const
import common.cfg.confmgr as confmgr
from common.utils.ui_utils import get_scale
from common.utils.cocos_utils import ccp, ccc4fFromHex
from logic.gcommon.common_utils.ui_gameplay_utils import apply_player_custom_setting
import math
import six.moves.cPickle
import copy
from logic.gutils.custom_ui_utils import get_group_all_node_ids, get_custom_node_conf, get_group_names, check_custom_node_group_setting
from logic.gutils.salog import SALog
from logic.gutils.item_utils import get_mecha_name_by_id, get_mecha_role_pic
SHADOW_SPR_PATH = 'gui/ui_res_2/setting/'
DEFAULT_SHADOW_SPR = 'sight_shadow.png'
SELECT_SPR_PATH = 'gui/ui_res_2/setting/custom'
DEFAULT_SELECT_SPR = 'img_yellowlight_04.png'
nine_para = {'img_yellowlight_05.png': (
                            31, 33, 58, 56)
   }
DEFAULT_SELECT_SCALE = 1.2
DEFAULT_OPACITY_RANGE = [0, 1.0]
DEFAULT_SCALE_RANGE = [0.5, 2]
SETTING_NO_TEXT_ID = [
 81101, 81102, 81103]
CUSTOM_PANEL_NAME = 'nd_custom_panel %s %d '
MOVE_STEP = 2
ALL_PAGE_LIST = [
 'mecha', 'human']
COMMON_SETTING_NO_LIST = ui_operation_const.COMMON_SETTING_NO_LIST

class CustomNode(object):

    def __init__(self, node_id, parent_nd, panel_nd, root_nd, def_range_node, page='human', cur_group_conf=None, cur_id=None):
        self._is_valid = True
        self.is_selected = False
        self.parent_nd = parent_nd
        self.root_nd = root_nd
        self.def_range_node = def_range_node
        self.panel_nd = panel_nd
        self.node_id = node_id
        self.belong_page = page
        self.node_conf = self.get_node_conf(node_id)
        self.arrNodeShow = self.node_conf['arrNodeShow']
        self.node_name = self.node_conf['cNodeName']
        self.copy_source = self.node_conf.get('cCopySource')
        self.node = getattr(self.parent_nd, self.node_name)
        self.force_setting_no = None
        if not self.copy_source:
            self._has_come_to_life = True
            self._is_usable = True
        else:
            self._has_come_to_life = False
            self._is_usable = False
        self.adjust_node_name = self.node_conf['cAdjustNode']
        self.cPostProcessFunc = self.node_conf.get('cPostProcessFunc', None)
        self.cDirectionLimit = self.node_conf.get('cDirectionLimit', {})
        if self.adjust_node_name:
            self.adjust_node = getattr(self.parent_nd, self.adjust_node_name)
        else:
            self.adjust_node = self.node
            self.adjust_node_name = self.node_name
        RangeNodeName = self.node_conf['cRangeNode']
        self.RangeNodeName = RangeNodeName
        if not RangeNodeName:
            RangeNodeName = self.node_name + '_p'
        self.RangeNode = getattr(panel_nd, RangeNodeName)
        if not self.RangeNode:
            self.RangeNode = getattr(parent_nd, RangeNodeName)
        if not self.RangeNode:
            self.RangeNode = def_range_node or root_nd
        cSelCheckNodeName = self.node_conf['cSelCheckNodeName']
        self.cSelCheckNode = None
        if cSelCheckNodeName:
            self.cSelCheckNode = getattr(self.parent_nd, cSelCheckNodeName)
        if not self.node:
            log_error('Error Custom Node, Node id = %s.', str(node_id), self.node_conf, self.parent_nd.GetName(), self.parent_nd.GetNodeBelongingTemplate())
            self._is_valid = False
            import traceback
            traceback.print_stack()
            return
        else:
            if not self.RangeNode:
                log_error('Error Custom Range Node, Node id = %s.', str(node_id), self.node_conf)
                self._is_valid = False
                import traceback
                traceback.print_stack()
                return
            self.shadow_sprite_name = self.node_conf.get('cShadowPng')
            self.select_sprite_name = self.node_conf.get('cSelectPng') or DEFAULT_SELECT_SPR
            self.select_sprite_info = self.node_conf.get('cSelectPngInfo', {})
            if not self.shadow_sprite_name:
                self.shadow_sprite_name = DEFAULT_SHADOW_SPR
            self.shadow_sprite = None
            self.select_sprite = None
            self.custom_conf = {}
            self.ini_custom_conf = {}
            self.is_config_modified = False
            self._belong_group = self.node_conf.get('cGroup', None)
            self._group_rank = self.node_conf.get('iGroupRank', -1)
            self._is_in_group = False
            self._is_top_group_no = self._group_rank == ui_operation_const.CUSTOM_NODE_TOP_GROUP_RANK
            self._cur_setting_no = cur_id
            if self._belong_group:
                node_id_list = cur_group_conf.get(str(cur_id), {}).get(self._belong_group, [])
                self._is_in_group = str(self.node_id) in node_id_list
            self.init()
            self._exclude_area_list = []
            return

    def get_enable_condition_result(self):
        cEnableFunc = self.node_conf.get('cEnableFunc', '')
        if cEnableFunc:
            from . import button_custom_process_func
            func = getattr(button_custom_process_func, cEnableFunc)
            if func and callable(func):
                enable = func(self.node_id)
                if not enable:
                    return False
        return True

    def set_is_usable(self, val):
        self._is_usable = val

    def get_is_usable(self):
        return self._is_usable

    def get_node_conf(self, node_id):
        node_conf = get_custom_node_conf(node_id)
        cCopySource = node_conf.get('cCopySource')
        if cCopySource:
            node_name = node_conf.get('cNodeName', '')
            node_conf.update(dict(get_custom_node_conf(cCopySource)))
            node_conf.update({'cCopySource': cCopySource})
            node_conf.update({'cNodeName': node_name})
            del_list = ['cGroup', 'cSyncNode', 'cCopyNodes']
            for arr in del_list:
                if arr in node_conf:
                    del node_conf[arr]

        return node_conf

    def set_force_setting_no(self, w):
        self.force_setting_no = w

    def is_valid(self):
        return self._is_valid

    def init(self):
        self.init_opacity = self.adjust_node.getOpacity()
        self.init_scale = self.adjust_node.getScale()
        self.init_pos = self.adjust_node.getPosition()
        opacity_range = self.node_conf['arrOpacityRange']
        if not opacity_range:
            opacity_range = DEFAULT_OPACITY_RANGE
        self.opacity_range = [
         opacity_range[0] * self.init_opacity, opacity_range[1] * self.init_opacity]
        scale_range = self.node_conf['arrScaleRange']
        if not scale_range:
            scale_range = DEFAULT_SCALE_RANGE
        self.scale_range = [
         scale_range[0] * self.init_scale, scale_range[1] * self.init_scale]
        self.adjust_node.SetEnableCascadeOpacityRecursion(True)
        self.adjust_node.setOpacity(int(self.init_opacity * 0.7))
        self.set_array_node_to_show(False)
        if self.should_hide():
            self.hide()
        else:
            self.show()

    def should_hide(self):
        cond_1 = self._is_in_group and not self._is_top_group_no
        cond_2 = not self._has_come_to_life or not self._is_usable
        cond_3 = not self.get_enable_condition_result()
        return cond_1 or cond_2 or cond_3

    def set_user_config(self, conf, with_key=True, is_refresh=False):
        if with_key:
            node_conf = conf.get(self.adjust_node_name, {})
        else:
            node_conf = conf
        self.custom_conf = copy.deepcopy(node_conf)
        self.ini_custom_conf = copy.deepcopy(self.custom_conf)
        if not node_conf:
            self.start_opacity = self.init_opacity
            if is_refresh:
                self.adjust_node.ApplyCustomSetting({'pos': {'x': self.init_pos.x,'y': self.init_pos.y},'scale': {'x': self.init_scale,'y': self.init_scale},'opacity': self.init_opacity * 0.7
                   })
                self.check_post_process_func()
            return
        else:
            if is_refresh:
                self.adjust_node.RevertToOrigConf()
                self.init_opacity = self.adjust_node.getOpacity()
            setting_no = self.force_setting_no if self.force_setting_no is not None else self._cur_setting_no
            apply_player_custom_setting(self.adjust_node, node_conf, customize=True, belong_page=self.belong_page, setting_no=setting_no)
            if 'opacity' in node_conf:
                self.start_opacity = node_conf['opacity']
            else:
                self.start_opacity = self.init_opacity
            self.check_node_pos_is_valid()
            self.adjust_node.setOpacity(int(self.get_show_opacity()))
            self.check_post_process_func()
            return

    def check_node_pos_is_valid(self):
        from common.utils.cocos_utils import IsSrcNodeIntersectWithDescNode
        is_in_screen = IsSrcNodeIntersectWithDescNode(global_data.ui_mgr.get_ui_zorder_layer(NORMAL_LAYER_ZORDER), self.adjust_node)
        wpos = self.get_node_center_world_position()
        if not is_in_screen:
            boundary = get_scale('10w')
            valid_x = max(min(global_data.ui_mgr.design_screen_size.width - boundary, wpos.x), boundary)
            valid_y = max(min(global_data.ui_mgr.design_screen_size.height - boundary, wpos.y), boundary)
            new_pos = ccp(valid_x, valid_y)
            global_data.game_mgr.show_tip(get_text_by_id(633908))
            self.sync_to_wpos(new_pos)

    def copy_custom_conf_from_other(self, custom_conf):
        self.set_user_config(custom_conf, with_key=False, is_refresh=True)
        self.is_config_modified = True

    def revert_to_def_config(self):
        if self.custom_conf != {}:
            self.custom_conf = {}
            self.is_config_modified = True
            self.adjust_node.ApplyCustomSetting({'pos': {'x': self.init_pos.x,'y': self.init_pos.y},'scale': {'x': self.init_scale,'y': self.init_scale},'opacity': self.init_opacity * 0.7
               })
            self.start_opacity = self.init_opacity
            self.check_post_process_func()
        if self._belong_group:
            self.set_is_in_group(True, None)
        if self.get_copy_source():
            self.set_is_usable(False)
        return

    def revert_to_previous_version(self):
        self.custom_conf = copy.deepcopy(self.ini_custom_conf)
        if self.ini_custom_conf:
            apply_player_custom_setting(self.adjust_node, self.ini_custom_conf, customize=True, belong_page=self.belong_page, setting_no=self._cur_setting_no)
        else:
            self.adjust_node.ApplyCustomSetting({'pos': {'x': self.init_pos.x,'y': self.init_pos.y},'scale': {'x': self.init_scale,'y': self.init_scale},'opacity': self.init_opacity * 0.7
               })
        self.is_config_modified = False

    def check_post_process_func(self):
        if self.cPostProcessFunc:
            from . import button_custom_process_func
            func = getattr(button_custom_process_func, self.cPostProcessFunc)
            if func and callable(func):
                func(self.adjust_node, self.parent_nd, self.custom_conf)

    def set_array_node_to_show(self, is_visible):
        if self.arrNodeShow:
            for node_name in self.arrNodeShow:
                nd = getattr(self.parent_nd, node_name)
                if nd:
                    nd.setVisible(is_visible)

    def on_select(self):
        self.adjust_node.setOpacity(int(self.start_opacity))
        self.adjust_node.setLocalZOrder(1000)
        self.parent_nd.setLocalZOrder(1000)
        self.parent_nd.GetParent().setLocalZOrder(1000)
        self.is_selected = True
        if self.shadow_sprite:
            self.shadow_sprite.setVisible(True)
        if not self.select_sprite:
            self.show_select_sprite()
        if self.select_sprite:
            self.select_sprite.setVisible(True)
        self.set_array_node_to_show(True)

    def on_unselect(self):
        self.adjust_node.setOpacity(int(self.get_show_opacity()))
        self.adjust_node.setLocalZOrder(10)
        self.parent_nd.setLocalZOrder(10)
        self.parent_nd.GetParent().setLocalZOrder(10)
        self.is_selected = False
        if self.shadow_sprite:
            self.shadow_sprite.setVisible(False)
        if self.select_sprite:
            self.select_sprite.setVisible(False)
        self.set_array_node_to_show(False)

    def get_show_opacity(self):
        return max(self.start_opacity * 0.7, 26)

    def on_move_begin(self, wpos):
        self.start_adjust_pos = self.adjust_node.getPosition()
        if wpos is not None:
            self.move_start_pos = self.adjust_node.getParent().convertToNodeSpace(wpos)
        else:
            import cc
            self.move_start_pos = self.start_adjust_pos
        return

    def get_node_world_position(self):
        lpos = self.adjust_node.getPosition()
        wpos = self.adjust_node.getParent().convertToWorldSpace(lpos)
        return wpos

    def get_node_center_world_position(self):
        wpos = self.adjust_node.ConvertToWorldSpacePercentage(50, 50)
        return wpos

    def sync_to_wpos(self, wpos, is_center_wpos=True):
        lpos = self.adjust_node.getParent().convertToNodeSpace(wpos)
        if is_center_wpos:
            ap = self.adjust_node.getAnchorPoint()
            sz = self.adjust_node.getContentSize()
            scale_x = self.adjust_node.getScaleX()
            scale_y = self.adjust_node.getScaleY()
            offset_x = (ap.x - 0.5) * sz.width * scale_x
            offset_y = (ap.y - 0.5) * sz.height * scale_y
            lpos.x += offset_x
            lpos.y += offset_y
        self.adjust_node.setPosition(lpos)
        lpos = self.adjust_node.getPosition()
        lpos = self.adjust_node.getParent().convertToWorldSpace(lpos)
        self.update_custom_conf({'pos': {'x': int(lpos.x),'y': int(lpos.y)}})

    def on_move_to(self, wpos):
        if self.is_selected:
            self.on_check_first_change()
        lpos = self.adjust_node.getParent().convertToNodeSpace(wpos)
        lpos.subtract(self.move_start_pos)
        if self.cDirectionLimit:
            lpos.x *= self.cDirectionLimit.get('x', 1)
            lpos.y *= self.cDirectionLimit.get('y', 1)
        lpos.add(self.start_adjust_pos)
        self.adjust_node.setPosition(lpos)
        if self.adjust_node != self.node:
            old_node_wpos = self.node.getParent().convertToWorldSpace(self.node.getPosition())
            wpos2 = self.boundary_check(old_node_wpos)
            wpos2.subtract(old_node_wpos)
            diff = wpos2
            if diff.getLength() > 0:
                ad_old_wpos = self.adjust_node.getParent().convertToWorldSpace(self.adjust_node.getPosition())
                ad_old_wpos.add(diff)
                lpos = self.adjust_node.getParent().convertToNodeSpace(ad_old_wpos)
                self.adjust_node.setPosition(lpos)
        else:
            wpos = self.exclude_wpos_from_forbidden_pos(self.boundary_check(self.adjust_node.getParent().convertToWorldSpace(lpos)))
            self.adjust_node.setPosition(self.adjust_node.getParent().convertToNodeSpace(wpos))
        self.check_post_process_func()

    def move_node(self, x, y):
        self.on_move_begin(None)
        import cc
        wpos = cc.Vec2(self.get_node_world_position())
        wpos.x += x
        wpos.y += y
        self.on_move_to(wpos)
        self.on_move_end()
        return

    def boundary_check(self, wpos):

        def PointCheck(pt, left_xb, right_xb, bottom_yb, up_yb):
            node = self.RangeNode
            p = node.convertToNodeSpace(pt)
            w, h = node.GetContentSize()
            return node.ConvertToWorldSpace(max(min(w - right_xb, p.x), left_xb), max(min(h - up_yb, p.y), bottom_yb))

        sz = self.node.getContentSize()
        scale = self.node.getScale()
        anchor = self.node.getAnchorPoint()
        left_boundary = sz.width * anchor.x * scale
        right_boundary = sz.width * (1 - anchor.x) * scale
        bottom_boundary = sz.height * anchor.y * scale
        up_boundary = sz.height * (1 - anchor.y) * scale
        return PointCheck(wpos, left_boundary, right_boundary, bottom_boundary, up_boundary)

    def get_to_root_scale(self, node, root_nd):
        scale = node.getScale()
        if node == root_nd:
            return scale
        for i in range(20):
            parent = node.GetParent()
            if parent != root_nd:
                scale *= parent.getScale()
            else:
                return scale
            node = parent

        return scale

    def on_move_end(self):
        lpos = self.adjust_node.getPosition()
        lpos = self.adjust_node.getParent().convertToWorldSpace(lpos)
        self.update_custom_conf({'pos': {'x': int(lpos.x),'y': int(lpos.y)}})

    def update_pos_for_resolution_before_save(self, setting_no=None):
        common_setting_no = global_data.player.get_cur_setting_no()
        from logic.gcommon.common_const import ui_operation_const as uoc
        if setting_no is not None:
            is_common = int(setting_no) in uoc.COMMON_SETTING_NO_LIST
        else:
            is_common = True
        if not is_common:
            common_width = global_data.player.get_cur_custom_setting_resolution_data(self.belong_page, common_setting_no)
            width = global_data.player.get_cur_custom_setting_resolution_data(self.belong_page, setting_no, default=common_width)
        else:
            width = global_data.player.get_cur_custom_setting_resolution_data(self.belong_page, setting_no)
        real_width = global_data.ui_mgr.design_screen_size.width
        if width != real_width:
            lpos = self.adjust_node.getPosition()
            lpos = self.adjust_node.getParent().convertToWorldSpace(lpos)
            self.update_custom_conf({'pos': {'x': int(lpos.x),'y': int(lpos.y)}})
        return

    def on_change_opacity(self, change_val):
        min_opacity, max_opacity = self.opacity_range
        cur_ope = self.start_opacity
        new_ope = min(max(cur_ope + change_val, min_opacity), max_opacity)
        self.adjust_node.setOpacity(int(new_ope))
        self.start_opacity = new_ope
        self.check_post_process_func()
        return (new_ope - min_opacity) / (max_opacity - min_opacity)

    def on_change_opacity_end(self):
        self.update_custom_conf({'opacity': self.start_opacity})
        self.start_opacity = self.adjust_node.getOpacity()

    def get_cur_opacity(self):
        return self.start_opacity

    def get_cur_scale(self):
        return self.adjust_node.getScale()

    def on_change_scale(self, change_val):
        self.on_check_first_change()
        min_scale, max_scale = self.scale_range
        cur_scale = self.adjust_node.getScale()
        new_scale = min(max(cur_scale + change_val, min_scale), max_scale)
        lpos_x, lpos_y = self.get_node_center_pos(self.adjust_node)
        self.adjust_node.setScale(new_scale)
        from logic.gutils.rocker_utils import center_node_at_point
        center_node_at_point(self.adjust_node, lpos_x, lpos_y)
        self.check_post_process_func()
        return (new_scale - min_scale) / (max_scale - min_scale)

    def on_change_scale_end(self):
        scale = self.adjust_node.getScale()
        self.update_custom_conf({'scale': {'x': scale,'y': scale}})

    def update_custom_conf(self, conf):
        self.custom_conf.update(conf)
        self.is_config_modified = True

    def on_check_first_change(self):
        if not self.shadow_sprite:
            self.show_shadow(opacity=100)

    def show_shadow(self, color=None, opacity=None):
        if self.shadow_sprite_name == 'empty':
            return
        shadow_path = SHADOW_SPR_PATH + self.shadow_sprite_name
        from common.uisys.uielment.CCSprite import CCSprite
        obj = CCSprite.Create('', shadow_path, force_sync=True)
        self.root_nd.shadow_nd.AddChild('', obj)
        self.shadow_sprite = obj
        self.sync_sprite_with_node(self.shadow_sprite, self.cSelCheckNode or self.node)
        if self.shadow_sprite and color:
            self.shadow_sprite.SetColor(color)
        if self.shadow_sprite and opacity:
            self.shadow_sprite.setOpacity(int(opacity))

    def show_select_sprite(self, color=None, opacity=None):
        if self.select_sprite_name == 'empty':
            return
        sel_path = SELECT_SPR_PATH + '/' + self.select_sprite_name
        rect = nine_para.get(self.select_sprite_name)
        if rect:
            from common.utils.cocos_utils import ccc3FromHex, CCRect
            from common.uisys.uielment.CCScale9Sprite import CCScale9Sprite
            obj = CCScale9Sprite.Create('', sel_path, CCRect(*rect))
            self.node.AddChild('', obj)
            obj.setLocalZOrder(10)
            self.select_sprite = obj
            extra_scale = self.select_sprite_info.get('scale', [1.2, 1.2])
            extra_offset = self.select_sprite_info.get('pos', [0, 0])
            self.sync_sprite_with_node(self.select_sprite, self.cSelCheckNode or self.node, extra_scale=extra_scale, extra_offset=extra_offset)
        else:
            from common.uisys.uielment.CCSprite import CCSprite
            obj = CCSprite.Create('', sel_path, force_sync=True)
            self.node.AddChild('', obj)
            obj.setLocalZOrder(10)
            self.select_sprite = obj
            extra_scale = self.select_sprite_info.get('scale', [1.7, 1.7])
            extra_offset = self.select_sprite_info.get('pos', [0, 0])
            self.sync_sprite_with_node(self.select_sprite, self.cSelCheckNode or self.node, extra_scale=extra_scale, extra_offset=extra_offset)
        if self.select_sprite and color:
            self.select_sprite.SetColor(color)
        if self.select_sprite and opacity:
            self.select_sprite.setOpacity(int(opacity))

    def change_select_sprite(self, scale_info):
        self.select_sprite_info = scale_info
        if not self.select_sprite:
            self.show_select_sprite()
        else:
            rect = nine_para.get(self.select_sprite_name)
            if rect:
                extra_scale = self.select_sprite_info.get('scale', [1.2, 1.2])
                extra_offset = self.select_sprite_info.get('pos', [0, 0])
                self.sync_sprite_with_node(self.select_sprite, self.cSelCheckNode or self.node, extra_scale=extra_scale, extra_offset=extra_offset)
            else:
                extra_scale = self.select_sprite_info.get('scale', [1.7, 1.7])
                extra_offset = self.select_sprite_info.get('pos', [0, 0])
                self.sync_sprite_with_node(self.select_sprite, self.cSelCheckNode or self.node, extra_scale=extra_scale, extra_offset=extra_offset)

    def purely_show_shadow(self):
        self.shadow_sprite and self.shadow_sprite.setVisible(True)

    def purely_hide_shadow(self):
        self.shadow_sprite and self.shadow_sprite.setVisible(False)

    def sync_sprite_with_node(self, sprite, node, extra_scale=(1.0, 1.0), extra_offset=(0, 0)):
        if sprite:
            sz = sprite.getContentSize()
            nd_sz = node.getContentSize()
            nd_scale = self.get_to_root_scale(node, self.root_nd)
            sprite_scale = self.get_to_root_scale(sprite, self.root_nd)
            scale_x = nd_sz.width / sz.width
            scale_y = nd_sz.height / sz.height
            from common.uisys.uielment.CCSprite import CCSprite
            if type(sprite) == CCSprite:
                sprite.setScaleX(scale_x * nd_scale / sprite_scale * extra_scale[0])
                sprite.setScaleY(scale_y * nd_scale / sprite_scale * extra_scale[1])
            else:
                sprite.SetContentSize(nd_sz.width * extra_scale[0], nd_sz.height * extra_scale[1])
            wpos = node.ConvertToWorldSpacePercentage(50, 50)
            p = sprite.getParent().convertToNodeSpace(wpos)
            p.x += extra_offset[0]
            p.y += extra_offset[1]
            sprite.setPosition(p)
            sprite.setRotation(node.getRotation())

    def destroy(self):
        self.parent_nd = None
        self.root_nd = None
        self.def_range_node = None
        self.node_id = None
        self.node_conf = None
        self.RangeNode = None
        self.node = None
        return

    def check_is_point_in(self, world_pos):
        if not self.node:
            return False
        if not self.node.isVisible():
            return False
        if self._is_in_group and not self._is_top_group_no:
            return False
        if self.is_selected and self.cSelCheckNode:
            return self.cSelCheckNode.IsPointIn(world_pos)
        return self.node.IsPointIn(world_pos)

    def get_save_info(self):
        if not self._has_come_to_life or not self._is_usable:
            return {}
        name = self.adjust_node_name if self.adjust_node_name else self.node_name
        return {name: self.custom_conf}

    def on_saved(self):
        self.is_config_modified = False
        self.ini_custom_conf = copy.deepcopy(self.custom_conf)

    def get_custom_conf(self):
        return copy.deepcopy(self.custom_conf)

    def show(self):
        self.node.setVisible(True)

    def hide(self):
        self.node.setVisible(False)

    def get_node_center_pos(self, node):
        lpos = node.getPosition()
        sz = node.getContentSize()
        scale = node.getScale()
        anchor_point = node.getAnchorPoint()
        x_offset = (anchor_point.x - 0.5) * sz.width * scale
        y_offset = (anchor_point.y - 0.5) * sz.height * scale
        return (
         lpos.x - x_offset, lpos.y - y_offset)

    def check_is_modified(self):
        return self.is_config_modified

    def is_group_top_node(self):
        return self._is_top_group_no

    def is_copyable_node(self):
        return bool(self.node_conf.get('cCopyNodes', False))

    def get_copy_nodes(self):
        return self.node_conf.get('cCopyNodes')

    def get_copy_source(self):
        return self.copy_source

    def get_group_node_ids(self):
        if self._belong_group:
            cur_group_conf = global_data.player.get_setting(ui_operation_const.CUSTOM_NODE_GROUPS, default={})
            cur_id = self._cur_setting_no
            node_id_list = cur_group_conf.get(str(cur_id), {}).get(self._belong_group, [])
            return node_id_list
        else:
            return []

    def get_node(self):
        return self.node

    def get_group_name(self):
        return self._belong_group

    def get_is_in_group(self):
        return self._is_top_group_no or self._is_in_group

    def set_is_in_group(self, val, group_top_node):
        self._is_in_group = val
        if group_top_node:
            self.sync_config_with_node(group_top_node)
        if self._is_in_group and self._belong_group:
            if self._is_in_group:
                if self._is_top_group_no:
                    self.show()
                else:
                    self.hide()
            else:
                self.hide()
        else:
            self.show()

    def refresh_group_show(self, cur_group_conf):
        if self._belong_group:
            cur_id = self._cur_setting_no
            node_id_list = cur_group_conf.get(str(cur_id), {}).get(self._belong_group, [])
            self.set_is_in_group(str(self.node_id) in node_id_list, None)
        return

    def sync_config_with_node(self, c_node):
        if c_node:
            cus_conf = c_node.get_custom_conf()
            self.copy_custom_conf_from_other(cus_conf)
            import cc
            wpos = cc.Vec2(c_node.get_node_center_world_position())
            self.sync_to_wpos(wpos)

    def set_config_modified(self, val):
        self.is_config_modified = val

    def set_exclude_area_list(self, area_list):
        self._exclude_area_list = area_list

    def exclude_wpos_from_forbidden_pos(self, wpos):
        if not self._exclude_area_list:
            return wpos
        for area_rect in self._exclude_area_list:
            if area_rect.containsPoint(wpos):
                if wpos.y > area_rect.y:
                    wpos.y = area_rect.y

        return wpos

    def come_to_life(self):
        if self.copy_source and not self._has_come_to_life:
            source_conf = self.get_node_conf(self.copy_source)
            source_node = getattr(self.parent_nd, source_conf['cNodeName'])
            for child in source_node.GetChildren():
                if child.GetConf():
                    new_node = child.CreateCopy(self.node, name=child.GetName())

            self._has_come_to_life = True
            if self.node_conf['cAdjustNode']:
                log_error('unsupport function "adjust_node_name"!!!! for copy node')
            else:
                self.adjust_node = self.node
                self.adjust_node_name = self.node_name

    def is_came_to_life(self):
        return self._has_come_to_life


class ShadowCustomNode(CustomNode):

    def __init__(self, node_id, parent_nd, panel_nd, root_nd, def_range_node, page='human', cur_group_conf=None, setting_no=None):
        super(ShadowCustomNode, self).__init__(node_id, parent_nd, panel_nd, root_nd, def_range_node, page, cur_group_conf, setting_no)

    def get_node_conf(self, node_id):
        shadow_spe_conf = confmgr.get('c_panel_node_custom_shadow_conf', str(node_id))
        if shadow_spe_conf:
            return shadow_spe_conf
        else:
            old_conf = dict(super(ShadowCustomNode, self).get_node_conf(node_id))
            return old_conf


class CustomPanel(object):

    def __init__(self, panel_name, start_nd, panel_nd, root_nd, def_range_node, page='human', group_conf=None, exclude_areas=(), setting_no=None):
        self.panel_name = panel_name
        self.start_nd = start_nd
        self.root_nd = root_nd
        self.def_range_node = def_range_node
        self.panel_nd = panel_nd
        self.belong_page = page
        self.node_list_key = 'arrConfigList'
        self.custom_node_dict = {}
        self.is_force_modified = False
        self._group_conf = group_conf
        self._setting_no = setting_no
        self.set_val_convert_func_dict = {}
        self._exclude_area_list = exclude_areas
        self.load_from_conf()
        self.init()

    def destroy(self):
        self.start_nd = None
        self.root_nd = None
        self.def_range_node = None
        self.set_val_convert_func_dict = {}
        for node_id, c_node in six.iteritems(self.custom_node_dict):
            c_node.destroy()

        self.custom_node_dict = {}
        self._group_conf = {}
        self._setting_conf = {}
        self._keys = []
        self.node_id_list = []
        return

    def load_from_conf(self):
        from . import button_custom_key_func
        self._setting_conf = confmgr.get('c_panel_custom_key_conf', str(self.panel_name))
        if not self._setting_conf:
            log_error("Can't find panel default conf", self.panel_name)
        self._keys = six_ex.keys(self._setting_conf)
        self.node_id_list = []
        for setting_key, key_conf in six.iteritems(self._setting_conf):
            for val, val_conf in six.iteritems(key_conf):
                self.node_id_list.extend(val_conf.get(self.node_list_key, []))

            if setting_key:
                key_convert_conf = confmgr.get('c_panel_custom_key_convert', str(setting_key), default={})
                convert_func_name = key_convert_conf.get('cKeyConvertFunc', None)
                if convert_func_name:
                    func = getattr(button_custom_key_func, convert_func_name)
                    self.set_val_convert_func_dict = {setting_key: func}

        return

    def init(self):
        self.hide_all_node()
        self.init_panel_node()

    def hide_all_node(self):
        self.switch_show(False)
        self.purely_hide_node_shadow()

    def show_all_node(self):
        self.switch_show(True)

    def show_valid_node(self):
        for node_id in self.node_id_list:
            if node_id not in self.custom_node_dict:
                continue
            c_node = self.custom_node_dict[node_id]
            if c_node.should_hide():
                c_node.hide()
            else:
                c_node.show()

    def switch_show(self, is_vis):
        for node_id in self.node_id_list:
            node_conf = get_custom_node_conf(node_id)
            node_name = node_conf['cNodeName']
            nd = getattr(self.start_nd, node_name)
            if nd:
                nd.setVisible(is_vis)

    def create_custom_node(self, node_id):
        c_node = CustomNode(node_id, self.start_nd, self.panel_nd, self.root_nd, self.def_range_node, self.belong_page, self._group_conf, self._setting_no)
        if c_node.is_valid():
            self.custom_node_dict[node_id] = c_node
            return c_node
        else:
            c_node.destroy()
            return None
            return None

    def init_panel_node(self, is_refresh=False, force_panel_conf=None):
        for set_key in self._keys:
            set_key_conf = self._setting_conf.get(set_key)
            if set_key:
                set_val = global_data.player.get_setting(set_key)
                repr_set_val = str(set_val)
                if set_key in self.set_val_convert_func_dict:
                    repr_set_val = self.set_val_convert_func_dict[set_key](set_val)
            else:
                repr_set_val = ''
            set_val_conf = set_key_conf.get(repr_set_val, {})
            node_id_list = set_val_conf.get(self.node_list_key, [])
            if not node_id_list:
                log_error("Can't find node id list", self.panel_name, set_key, repr_set_val)
            if force_panel_conf is None:
                costom_user_ui_conf = global_data.player.get_setting(ui_operation_const.CUSTOMER_UI_KEY, from_custom_setting_no=self._setting_no)
            else:
                costom_user_ui_conf = force_panel_conf
            if self._setting_no not in COMMON_SETTING_NO_LIST and not costom_user_ui_conf:
                common_costom_user_ui_conf = global_data.player.get_setting(ui_operation_const.CUSTOMER_UI_KEY)
                costom_user_ui_conf = common_costom_user_ui_conf
            import copy
            panel_user_ui_conf = costom_user_ui_conf.get(self.panel_name, {})
            user_setting_conf = panel_user_ui_conf.get(set_key, {}).get(repr_set_val, {})
            if not is_refresh:
                for node_id in node_id_list:
                    node_custom_conf = get_custom_node_conf(node_id)
                    if node_custom_conf.get('bDisable', False):
                        continue
                    c_node = self.create_custom_node(node_id)
                    if c_node:
                        copy_node_id = node_custom_conf.get('cCopySource', None)
                        if copy_node_id:
                            is_node_conf_empty = [ len(each_node_conf) > 0 for each_node_conf in six.itervalues(user_setting_conf.get(str(node_id), {})) ]
                            if not any(is_node_conf_empty):
                                c_node.hide()
                            else:
                                c_node.come_to_life()
                                c_node.set_is_usable(True)
                                c_node.set_user_config(user_setting_conf.get(str(node_id), {}))
                                if not c_node.should_hide():
                                    c_node.show()
                        else:
                            c_node.set_user_config(user_setting_conf.get(str(node_id), {}))
                        c_node.set_exclude_area_list(self._exclude_area_list)

            else:
                for node_id in node_id_list:
                    c_node = self.custom_node_dict.get(node_id, None)
                    if c_node:
                        copy_node_id = c_node.get_copy_source()
                        if copy_node_id:
                            is_node_conf_empty = [ len(each_node_conf) > 0 for each_node_conf in six.itervalues(user_setting_conf.get(str(node_id), {})) ]
                            if not any(is_node_conf_empty):
                                c_node.hide()
                                c_node.set_is_usable(False)
                            else:
                                if not c_node.is_came_to_life():
                                    c_node.come_to_life()
                                if not c_node.get_is_usable():
                                    c_node.set_is_usable(True)
                                c_node.set_user_config(user_setting_conf.get(str(node_id), {}), is_refresh=True)
                                c_node.show()
                        else:
                            c_node.set_user_config(user_setting_conf.get(str(node_id), {}), is_refresh=True)
                        c_node.set_exclude_area_list(self._exclude_area_list)

        return

    def refresh_panel_node(self, force_panel_conf=None):
        self.init_panel_node(is_refresh=True, force_panel_conf=force_panel_conf)
        self.refresh_group_show()

    def check_is_point_in(self, wpos):
        touch_nodes = []
        for c_node in six_ex.values(self.custom_node_dict):
            if c_node.check_is_point_in(wpos):
                touch_nodes.append(c_node)

        return touch_nodes

    def get_custom_node(self, node_id):
        return self.custom_node_dict.get(node_id)

    def get_save_info(self):
        custom_conf = {}
        for set_key in self._keys:
            set_key_conf = self._setting_conf.get(set_key)
            if set_key:
                set_val = global_data.player.get_setting(set_key)
                repr_set_val = str(set_val)
                if set_key in self.set_val_convert_func_dict:
                    repr_set_val = self.set_val_convert_func_dict[set_key](set_val)
            else:
                repr_set_val = ''
            set_val_conf = set_key_conf.get(repr_set_val, {})
            node_id_list = set_val_conf.get('arrConfigList', [])
            custom_conf.setdefault(set_key, {})
            custom_conf[set_key].setdefault(repr_set_val, {})
            for node_id in node_id_list:
                nd = self.get_custom_node(node_id)
                if nd:
                    nd_conf = nd.get_save_info()
                    custom_conf[set_key][repr_set_val].update({str(node_id): nd_conf})

        return {self.panel_name: custom_conf}

    def update_pos_for_resolution_before_save(self, setting_no=None):
        for c_node in six_ex.values(self.custom_node_dict):
            c_node.update_pos_for_resolution_before_save(setting_no)

    def revert_to_def_setting(self):
        for c_node in six_ex.values(self.custom_node_dict):
            c_node.revert_to_def_config()

    def check_is_modified(self):
        if self.is_force_modified:
            return self.is_force_modified
        for c_node in six_ex.values(self.custom_node_dict):
            if c_node.check_is_modified():
                return True

        return False

    def revert_to_previous_version(self):
        for c_node in six_ex.values(self.custom_node_dict):
            c_node.revert_to_previous_version()

    def on_saved(self):
        for c_node in six_ex.values(self.custom_node_dict):
            c_node.on_saved()

        self.is_force_modified = False

    def get_node_ids(self):
        return six_ex.keys(self.custom_node_dict)

    def refresh_group_show(self):
        for c_node in six_ex.values(self.custom_node_dict):
            c_node.refresh_group_show(self._group_conf)

    def on_switch_page(self, new_page):
        self.check_page_show(new_page)

    def refresh_page_show(self, cur_page, ignore_always_show=False):
        self.check_page_show(cur_page, ignore_always_show)

    def check_page_show(self, new_page, ignore_always_show=False):
        panel_conf = confmgr.get('c_panel_custom_conf', str(self.panel_name))
        cAlwaysShow = panel_conf.get('cAlwaysShow', None)
        if cAlwaysShow and not ignore_always_show:
            return
        else:
            if self.belong_page != new_page:
                self.hide_all_node()
            else:
                self.show_valid_node()
            return

    def purely_show_node_shadow(self):
        for c_node in six_ex.values(self.custom_node_dict):
            c_node.purely_show_shadow()

    def purely_hide_node_shadow(self):
        for c_node in six_ex.values(self.custom_node_dict):
            c_node.purely_hide_shadow()

    def get_is_force_modified(self, key):
        return self.is_force_modified

    def set_is_force_modified(self, value):
        self.is_force_modified = value


class ShadowCustomPanel(CustomPanel):

    def show_all_node_shadow(self, color):
        self.hide_all_node()
        for c_node in six_ex.values(self.custom_node_dict):
            c_node.show_shadow(color, 50)

    def create_custom_node(self, node_id):
        c_node = ShadowCustomNode(node_id, self.start_nd, self.panel_nd, self.root_nd, self.def_range_node, cur_group_conf=self._group_conf, setting_no=self._setting_no)
        if c_node.is_valid():
            self.custom_node_dict[node_id] = c_node
            return c_node
        else:
            c_node.destroy()
            return None
            return None


from common.const import uiconst

class BattleCustomButtonUI(BasePanel):
    PANEL_CONFIG_NAME = 'setting/setting_custom'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE_BY_DEFAULT_FUNC_NAME
    OPACITY_MODE = 1
    SCALE_MODE = 2
    NONE_MODE = 3
    OPACITY_MODE_ANGLE_THRES = math.sin(math.radians(60))
    UI_ACTION_EVENT = {'btn_save_list.OnClick': 'on_click_save_list_btn',
       'btn_save.OnClick': 'on_click_save_btn',
       'btn_exit.OnClick': 'on_click_close_btn',
       'btn_default.OnClick': 'on_click_default_btn',
       'touch_layer.OnBegin': 'on_begin_touch_layer',
       'touch_layer.OnDrag': 'on_drag_touch_layer',
       'touch_layer.OnEnd': 'on_end_touch_layer',
       'touch_layer.OnCancel': 'on_cancel_touch_layer',
       'btn_mecha.OnClick': 'on_click_jump_mecha_btn',
       'btn_driver.OnClick': 'on_click_jump_human_btn',
       'btn_up.OnClick': 'on_click_btn_up',
       'btn_down.OnClick': 'on_click_btn_down',
       'btn_left.OnClick': 'on_click_btn_left',
       'btn_right.OnClick': 'on_click_btn_right',
       'btn_pull.OnClick': 'on_click_btn_pull',
       'btn_rename.OnClick': 'on_click_btn_rename',
       'btn_copy.OnClick': 'on_click_btn_copy',
       'btn_delete.OnClick': 'on_click_btn_delete'
       }

    def on_init_panel(self, page, **kwargs):
        check_custom_node_group_setting()
        self._cur_mecha_id = None
        self.cur_page = page
        self._mecha_only = False
        self._need_del_cur_mecha_setting_no = False
        self._is_just_reverted = True
        self.all_used_page_set = {self.cur_page}
        self.page_panel_list = []
        self.custom_panel_dict = {}
        self.shadow_panel_dict = {}
        self.mecha_panel_common_setting_no = {}
        self.cur_sel_node = None
        self._temp_touch_node_list = []
        self._multiple_select_index = None
        self.is_multiple_sel = False
        self.has_select_in_this_touch = False
        self._drag_mode = self.NONE_MODE
        from common.utils.cocos_utils import getScreenSize
        self._screen_size = getScreenSize()
        self._node_id_2_node_dict = {}
        self._group_conf = copy.deepcopy(global_data.player.get_setting(ui_operation_const.CUSTOM_NODE_GROUPS, {}))
        self._group_setting_btn = None
        self._has_touch_btn_combine = False
        self._need_check_node_sync = True
        ban_area_bl = self.panel.nd_forbidden_area.ConvertToWorldSpace(0, 0)
        ban_area_rt = self.panel.nd_forbidden_area.ConvertToWorldSpacePercentage(100, 100)
        self._cur_save_list = self.panel.temp_save_list
        open_mecha_list = global_data.player.read_mecha_open_info()['opened_order']
        self._common_setting_no_list = [0, 1, 2]
        self._setting_no_list = self._common_setting_no_list + list(open_mecha_list)
        self.mecha_id_list = open_mecha_list
        import cc
        self._exclude_area_list = (cc.Rect(ban_area_bl.x, ban_area_bl.y, ban_area_rt.x - ban_area_bl.x, ban_area_rt.y - ban_area_bl.y),)
        self._group_names = get_group_names()
        self._group_dict = {}
        for group_name in self._group_names:
            self._group_dict[group_name] = get_group_all_node_ids(group_name)

        self.init_custom_ui()
        self.hide_main_ui(ui_list=['MainSettingUI'])
        for btn, dir_tuple in [(self.panel.btn_up, (0, 1)), (self.panel.btn_down, (0, -1)),
         (
          self.panel.btn_left, (-1, 0)), (self.panel.btn_right, (1, 0))]:
            self.set_move_press_func(btn, dir_tuple[0], dir_tuple[1])

        self.update_page_related_show()
        return

    def switch_mecha_only_state(self, val):
        self._mecha_only = val
        self.panel.btn_driver.setVisible(not val)
        self.panel.btn_mecha.setVisible(not val)
        self.panel.btn_switch.setVisible(val)
        self.panel.btn_rename.setVisible(not val)
        self.panel.btn_default.SetText(val or 870054 if 1 else 2339)
        if self._mecha_only:
            self.cur_page = 'mecha'
        if not self._mecha_only:
            self._need_del_cur_mecha_setting_no = False

    def on_finalize_panel(self):
        if self._group_setting_btn:
            self._group_setting_btn.release()
            self._group_setting_btn.Destroy()
            self._group_setting_btn = None
        self._node_id_2_node_dict = {}
        for setting_no, panel_list in six.iteritems(self.custom_panel_dict):
            for c_panel in panel_list:
                c_panel.destroy()

        self.custom_panel_dict = {}
        self.cur_sel_node = None
        self._temp_touch_node_list = []
        self._multiple_select_index = None
        self.is_multiple_sel = False
        self.has_select_in_this_touch = False
        self.show_main_ui()
        return

    def on_click_save_list_btn(self, btn, touch):
        list_visible = self._cur_save_list.isVisible()
        self._cur_save_list.setVisible(not list_visible)
        if not list_visible:
            self.refresh_save_list(self.get_cur_setting_no())
            if self._mecha_only:
                setting_no = self.get_cur_setting_no()
                if setting_no in self._setting_no_list:
                    ui_item = self._cur_save_list.option_list.GetItem(self._setting_no_list.index(setting_no))
                    self._cur_save_list.option_list.TopWithNode(ui_item)

    def switch_to_page(self, new_page):
        setting_no = self.get_cur_setting_no()
        old_page = self.cur_page
        self.select_node(None)
        self.cur_page = new_page
        page_nd_custom = getattr(self.panel, CUSTOM_PANEL_NAME % (new_page, setting_no), None)
        if not page_nd_custom:
            self.create_custom_panel_page_for_setting_no(page=new_page)
            page_nd_custom = getattr(self.panel, CUSTOM_PANEL_NAME % (new_page, setting_no), None)
        page_nd_custom and page_nd_custom.setVisible(True)
        for c_panel in self.custom_panel_dict.get(setting_no, []):
            c_panel.on_switch_page(new_page)

        self.all_used_page_set.add(new_page)
        self.update_page_related_show()
        if self._need_check_node_sync:
            self.check_page_node_sync()
        return

    def check_page_node_sync(self):
        sync_dict = {}
        setting_no = int(self.get_cur_setting_no())
        for c_panel in self.custom_panel_dict[setting_no]:
            node_ids = c_panel.get_node_ids()
            for node_id in node_ids:
                c_node = c_panel.get_custom_node(node_id)
                if c_node.check_is_modified():
                    node_conf = get_custom_node_conf(node_id)
                    cSyncNode = node_conf.get('cSyncNode', [])
                    if cSyncNode:
                        sync_dict[node_id] = cSyncNode

        def sync_to_other_page():
            for node_id, cSyncNode in six.iteritems(sync_dict):
                c_node = self.get_node_by_id_and_index(setting_no, node_id)
                for sync_node_id in cSyncNode:
                    c_sync_node = self.get_node_by_id_and_index(setting_no, sync_node_id)
                    if c_sync_node:
                        c_sync_node.sync_config_with_node(c_node)

        if sync_dict:
            from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2

            def confirm_callback():
                if not (self.panel and self.panel.isValid()):
                    return
                sync_to_other_page()
                self._need_check_node_sync = False

            def cancel_callback():
                self._need_check_node_sync = False

            SecondConfirmDlg2().confirm(content=get_text_local_content(82247), confirm_callback=confirm_callback, cancel_callback=cancel_callback)

    def on_click_jump_mecha_btn(self, *args):
        if self.cur_page == 'human':
            self.switch_to_page('mecha')

    def on_click_jump_human_btn(self, *args):
        if self.cur_page == 'mecha':
            self.switch_to_page('human')

    def update_page_related_show(self):
        self.panel.btn_mecha.SetSelect(self.cur_page == 'mecha')
        self.panel.btn_driver.SetSelect(self.cur_page == 'human')

    def on_click_save_btn(self, btn, touch):
        if not global_data.player:
            return
        else:
            self.select_node(None)
            self.save_cur_setting()
            self.check_save_button_state()
            return

    def on_click_close_btn(self, *args):
        if self.check_has_modified():
            from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2

            def confirm_callback():
                if not (self.panel and self.panel.isValid()):
                    return
                self.save_cur_setting()
                self.close()

            def cancel_callback():
                self.close()

            SecondConfirmDlg2().confirm(content=get_text_local_content(2001), confirm_callback=confirm_callback, cancel_callback=cancel_callback)
        else:
            self.close()

    def on_click_default_btn(self, btn, touch):
        from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2

        def confirm_callback():
            if not (self.panel and self.panel.isValid()):
                return
            else:
                self.select_node(None)
                global_data.game_mgr.show_tip(get_text_local_content(2002))
                self.revert_to_default_setting()
                self.check_save_button_state()
                return

        SecondConfirmDlg2().confirm(content=get_text_local_content(2223), confirm_callback=confirm_callback)

    def on_click_btn_up(self, btn, touch):
        self.move_sel_node(0, 1 * MOVE_STEP)
        if self._mecha_only:
            self._need_del_cur_mecha_setting_no = False
        if self._is_just_reverted:
            self._is_just_reverted = False

    def on_click_btn_down(self, btn, touch):
        self.move_sel_node(0, -1 * MOVE_STEP)
        if self._mecha_only:
            self._need_del_cur_mecha_setting_no = False
        if self._is_just_reverted:
            self._is_just_reverted = False

    def on_click_btn_left(self, btn, touch):
        self.move_sel_node(-1 * MOVE_STEP, 0)
        if self._mecha_only:
            self._need_del_cur_mecha_setting_no = False
        if self._is_just_reverted:
            self._is_just_reverted = False

    def on_click_btn_right(self, btn, touch):
        self.move_sel_node(1 * MOVE_STEP, 0)
        if self._mecha_only:
            self._need_del_cur_mecha_setting_no = False
        if self._is_just_reverted:
            self._is_just_reverted = False

    def on_click_btn_pull(self, btn, touch):
        self.panel.nd_control.setVisible(not self.panel.nd_control.isVisible())
        self.refresh_bar_show()

    def refresh_bar_show(self):
        import cc
        isvis = self.panel.nd_control.isVisible()
        old_size = self.panel.img_bar.getContentSize()
        if isvis:
            self.panel.img_bar.setContentSize(cc.Size(old_size.width, 275))
            self.panel.nd_bar.setContentSize(cc.Size(old_size.width, 275))
            self.panel.img_pull.setRotation(0)
        else:
            self.panel.img_bar.setContentSize(cc.Size(old_size.width, 130))
            self.panel.nd_bar.setContentSize(cc.Size(old_size.width, 130))
            self.panel.img_pull.setRotation(180)

    def on_click_btn_rename(self, btn, touch):

        def change_name(input=''):
            cur_id = self.get_cur_setting_no()
            self.change_setting_no_page_name(cur_id, input)
            return True

        cur_id = self.get_cur_setting_no()
        from logic.comsys.message.CommonInputDialog import CommonInputDialog
        CommonInputDialog(title=get_text_by_id(81817), desc_text=get_text_by_id(81817), cost_text='', placeholder=self.get_setting_no_page_name(cur_id), max_length=5, send_callback=change_name)

    def show_multiple_node_select(self, touch_pos, sel_index):
        self._multiple_select_index = sel_index
        is_show_in_left = touch_pos.x > self._screen_size.width / 2.0
        if is_show_in_left:
            cur_sel_menu = self.panel.nd_choose_left
            self.panel.nd_choose_right.setVisible(False)
        else:
            cur_sel_menu = self.panel.nd_choose_right
            self.panel.nd_choose_right.setVisible(True)
        cur_sel_menu.setPosition(cur_sel_menu.getParent().convertToNodeSpace(touch_pos))
        cur_sel_menu.setVisible(True)

        @cur_sel_menu.btn_last.unique_callback()
        def OnClick(btn, touch):
            if self._multiple_select_index is not None:
                self.select_node_on_node_list(self._multiple_select_index - 1)
            return

        @cur_sel_menu.btn_next.unique_callback()
        def OnClick(btn, touch):
            if self._multiple_select_index is not None:
                self.select_node_on_node_list(self._multiple_select_index + 1)
            return

    def cancel_multiple_node_select(self):
        self._multiple_select_index = None
        self.is_multiple_sel = False
        self._temp_touch_node_list = []
        self.panel.nd_choose_left.setVisible(False)
        self.panel.nd_choose_right.setVisible(False)
        return

    def select_node_on_node_list(self, index):
        if not self._temp_touch_node_list:
            return
        if index < 0:
            index = len(self._temp_touch_node_list) - 1
        if index >= len(self._temp_touch_node_list):
            index = 0
        self.select_node(self._temp_touch_node_list[index])
        self._multiple_select_index = index

    def select_node(self, node):
        if self.cur_sel_node == node:
            return
        if self.cur_sel_node:
            self.cur_sel_node.on_unselect()
        self.cur_sel_node = node
        if self.cur_sel_node:
            self.cur_sel_node.on_select()
        self.on_node_selected(self.cur_sel_node)

    def on_node_selected(self, node):
        if node is None:
            self.panel.nd_tips.setVisible(False)
        else:
            self.panel.nd_tips.setVisible(True)
        self.refresh_bar_show()
        self.init_opacity_slider()
        self.init_scale_slider()
        if self.cur_sel_node and self.cur_sel_node.is_group_top_node():
            self.show_group_setting_btn()
        else:
            self.hide_group_setting_btn()
        if self.cur_sel_node and (self.cur_sel_node.is_copyable_node() or self.cur_sel_node.get_copy_source()):
            wpos = self.cur_sel_node.get_node_world_position()
            lpos = self.panel.nd_function.GetParent().convertToNodeSpace(wpos)
            size = global_data.ui_mgr.design_screen_size
            x_offset = 100
            y_offset = 200
            if wpos.x > size.width / 2.0:
                x_offset *= -1
            if wpos.y > size.height / 2.0:
                y_offset *= -1
            self.panel.nd_function.SetPosition(lpos.x + x_offset, lpos.y + y_offset)
        self.refresh_copy_delete_show()
        return

    def refresh_copy_delete_show(self, force_hide=False):
        if self.cur_sel_node and not force_hide:
            self.panel.btn_copy.setVisible(self.is_select_node_can_copy())
            self.panel.btn_delete.setVisible(self.is_select_node_can_delete())
        else:
            self.panel.btn_copy.setVisible(False)
            self.panel.btn_delete.setVisible(False)

    def on_begin_touch_layer(self, btn, touch):
        if not (self.panel and self.panel.isValid()):
            return
        if not global_data.player:
            log_error('on_begin_touch_layer:global_data.player is None!')
            return
        touch_pos = touch.getLocation()
        has_touch_btn_combine = self.check_touch_btn_combine(touch_pos)
        if has_touch_btn_combine:
            if self.cur_sel_node and self.cur_sel_node.is_group_top_node():
                self._has_touch_btn_combine = True
                return True
        self._has_touch_btn_combine = False
        touch_nodes = self.check_touch_node(touch_pos)
        self._temp_touch_node_list = touch_nodes
        self.has_select_in_this_touch = False
        if len(touch_nodes) > 0:
            if self.cur_sel_node not in self._temp_touch_node_list:
                self.select_node(touch_nodes[0])
            if self.cur_sel_node:
                self.cur_sel_node.on_move_begin(touch_pos)
            self.has_select_in_this_touch = True
            if len(self._temp_touch_node_list) > 1:
                self.is_multiple_sel = True
        return True

    def on_end_touch_layer(self, btn, touch):
        if self._has_touch_btn_combine:
            wpos = touch.getLocation()
            self.show_group_setting_panel(wpos)
            self._has_touch_btn_combine = False
            return
        else:
            is_has_changed = False
            cur_pos = touch.getLocation()
            if self.has_select_in_this_touch:
                if len(self._temp_touch_node_list) > 1:
                    if self.cur_sel_node in self._temp_touch_node_list:
                        sel_index = self._temp_touch_node_list.index(self.cur_sel_node)
                        self.show_multiple_node_select(cur_pos, sel_index)
                else:
                    self.cancel_multiple_node_select()
                if self.cur_sel_node:
                    self.cur_sel_node.on_move_end()
                    is_has_changed = True
            else:
                if self.is_multiple_sel:
                    self.cancel_multiple_node_select()
                if self._drag_mode == self.NONE_MODE:
                    self.select_node(None)
                elif self._drag_mode == self.OPACITY_MODE:
                    self.on_change_opacity_end()
                    is_has_changed = True
                elif self._drag_mode == self.SCALE_MODE:
                    self.on_change_scale_end()
                    is_has_changed = True
                self._drag_mode = self.NONE_MODE
            self.has_select_in_this_touch = False
            if is_has_changed:
                self.check_save_button_state()
                if self._mecha_only:
                    self._need_del_cur_mecha_setting_no = False
                if self._is_just_reverted:
                    self._is_just_reverted = False
            return

    def on_cancel_touch_layer(self, btn, touch):
        self._has_touch_btn_combine = False

    def on_drag_touch_layer(self, btn, touch):
        cur_pos = touch.getLocation()
        start_pos = touch.getStartLocation()
        if self.has_select_in_this_touch:
            if self.is_multiple_sel:
                start_pos.subtract(cur_pos)
                lens = start_pos.getLength()
                if lens > get_scale('10w'):
                    self.cancel_multiple_node_select()
            elif self.cur_sel_node:
                self.cur_sel_node.on_move_to(cur_pos)
        elif self.cur_sel_node:
            if self._drag_mode == self.NONE_MODE:
                self._drag_mode = self.check_drag_mode(start_pos, cur_pos)
            elif self._drag_mode == self.OPACITY_MODE:
                self.on_change_opacity(touch.getDelta().y)
            elif self._drag_mode == self.SCALE_MODE:
                self.on_change_scale(touch.getDelta().x)

    def move_sel_node(self, x, y):
        if self.cur_sel_node:
            self.cur_sel_node.on_move_begin(None)
            import cc
            wpos = cc.Vec2(self.cur_sel_node.get_node_world_position())
            wpos.x += x
            wpos.y += y
            self.cur_sel_node.on_move_to(wpos)
            self.cur_sel_node.on_move_end()
        return

    def check_touch_btn_combine(self, wpos):
        if self._group_setting_btn:
            return self._group_setting_btn.btn_combine.IsPointIn(wpos)
        return False

    def set_move_press_func(self, btn, x, y):
        btn.SetPressEnable(True)
        btn.SetPressNeedTime(0.1)

        @btn.unique_callback()
        def OnPressedWithNum(_btn, _num, *args):
            self.move_sel_node(x, y)
            if self._mecha_only:
                self._need_del_cur_mecha_setting_no = False
            if self._is_just_reverted:
                self._is_just_reverted = False

    def check_drag_mode(self, start_pos, end_pos):
        import cc
        start_pos = cc.Vec2(start_pos)
        end_pos = cc.Vec2(end_pos)
        end_pos.subtract(start_pos)
        if end_pos.getLength() > 0:
            end_pos.normalize()
            if abs(end_pos.y) > self.OPACITY_MODE_ANGLE_THRES:
                return self.OPACITY_MODE
            else:
                return self.SCALE_MODE

        return self.NONE_MODE

    def show_group_setting_btn(self):
        if not self.cur_sel_node:
            return
        if not self._group_setting_btn:
            self._group_setting_btn = global_data.uisystem.load_template_create('setting/i_group_open_btn', self.cur_sel_node.get_node())
            self._group_setting_btn.retain()
        elif self._group_setting_btn.isValid():
            if self._group_setting_btn.GetParent() != self.cur_sel_node.get_node():
                self._group_setting_btn.RemoveFromParent()
                self.cur_sel_node.get_node().AddChild('', self._group_setting_btn)
                self._group_setting_btn.ReConfPosition()
        else:
            self._group_setting_btn = global_data.uisystem.load_template_create('setting/i_group_open_btn', self.cur_sel_node.get_node())
            self._group_setting_btn.retain()
        self._group_setting_btn.setVisible(True)

    def show_group_setting_panel(self, touch_pos):
        if not (self.cur_sel_node and self.cur_sel_node.is_group_top_node()):
            return
        import cc
        is_show_in_left = touch_pos.x > self._screen_size.width / 2.0
        if is_show_in_left:
            self.panel.temp_combine.setAnchorPoint(cc.Vec2(1, 1))
        else:
            self.panel.temp_combine.setAnchorPoint(cc.Vec2(0, 1))
        self.panel.nd_tips.setVisible(False)
        from logic.gutils import template_utils
        template_utils.set_node_position_in_screen(self.panel.temp_combine, self.panel, touch_pos)

        @self.panel.temp_combine.nd_close.callback()
        def OnEnd(btn, touch):
            if self.panel.temp_combine.bar.IsPointIn(touch.getLocation()):
                return
            self.panel.temp_combine.setVisible(False)
            if self.cur_sel_node:
                self.panel.nd_tips.setVisible(True)

        self.panel.temp_combine.setVisible(True)
        cur_id = str(self.get_cur_setting_no())
        group_name = self.cur_sel_node.get_group_name()
        node_ids = get_group_all_node_ids(group_name)
        nd = self.panel.temp_combine
        nd.option_list.SetInitCount(len(node_ids))
        nd.bar.SetContentSize(300, nd.option_list.getContentSize().height + 10)
        for i in range(len(node_ids)):
            cur_node_id = node_ids[i]
            ui_item = nd.option_list.GetItem(i)
            node_conf = get_custom_node_conf(cur_node_id)
            ui_item.lab_title.SetString(node_conf.get('iGroupMemberName', ''))
            group_conf = self._group_conf
            is_in_group = cur_node_id in group_conf.get(cur_id, {}).get(group_name, {})
            ui_item.btn_combine.SetText(is_in_group or 860190 if 1 else 860189)

            @ui_item.btn_combine.callback()
            def OnClick(btn, touch, cur_node_id=cur_node_id, i=i):
                self.change_group_info(group_name, node_ids, cur_node_id)
                group_conf = self._group_conf
                is_in_group = cur_node_id in group_conf.get(cur_id, {}).get(group_name, {})
                ui_item = nd.option_list.GetItem(i)
                ui_item.btn_combine.SetText(is_in_group or 860190 if 1 else 860189)

    def change_group_info(self, group_name, node_ids, node_id):
        cur_id = int(self.get_cur_setting_no())
        c_node = self.get_node_by_id_and_index(cur_id, node_id)
        c_top_node = self.get_node_by_id_and_index(cur_id, node_ids[0])
        if c_node and c_top_node:
            is_in_group = c_node.get_is_in_group()
            new_is_in_group = not is_in_group
            c_node.set_is_in_group(new_is_in_group, c_top_node)
            c_node.set_config_modified(True)
            group_conf = self._group_conf
            if str(cur_id) in group_conf:
                group_node_ids = group_conf[str(cur_id)].get(group_name, [])
                if not new_is_in_group:
                    if node_id in group_node_ids:
                        group_node_ids.remove(node_id)
                elif group_node_ids and node_id not in group_node_ids:
                    group_node_ids.append(node_id)

    def sync_node_to_node(self, setting_no, from_node_id, to_node_id):
        c_node = self.get_node_by_id_and_index(setting_no, to_node_id)
        c_top_node = self.get_node_by_id_and_index(setting_no, from_node_id)
        if c_node and c_top_node:
            c_node.sync_config_with_node(c_top_node)

    def hide_group_setting_btn(self):
        if self._group_setting_btn:
            self._group_setting_btn.setVisible(False)

    def on_change_opacity(self, dist):
        if not self.cur_sel_node:
            return
        import math
        change_opacity = int(round(dist / (self._screen_size.height * 0.8) * 255))
        self.on_change_opacity_val(change_opacity)

    def on_change_opacity_val(self, changed_opacity):
        res_percent = self.cur_sel_node.on_change_opacity(changed_opacity)
        res_percent = round(res_percent * 100)
        self.panel.nd_progress_opacity.setVisible(True)
        self.panel.nd_tips.setVisible(False)
        self.panel.progress_opacity.SetPercent(res_percent)
        self.panel.quantity_opacity.SetString(str(res_percent) + '%')
        self.panel.temp_slider_transparency.slider.setPercent(res_percent)
        self.update_slider_percent_text(self.panel.temp_slider_transparency, get_text_local_content(80370))

    def on_change_to_opacity(self, to_val):
        if not self.cur_sel_node:
            return
        cur_opacity = self.cur_sel_node.get_cur_opacity()
        return self.on_change_opacity_val(to_val - cur_opacity)

    def on_change_opacity_end(self):
        self.panel.nd_progress_opacity.setVisible(False)
        if self.cur_sel_node:
            self.cur_sel_node.on_change_opacity_end()
            self.panel.nd_tips.setVisible(True)

    def on_change_scale_end(self):
        self.panel.nd_progress_size.setVisible(False)
        if self.cur_sel_node:
            self.cur_sel_node.on_change_scale_end()
            self.panel.nd_tips.setVisible(True)

    def on_change_scale(self, dist):
        if not self.cur_sel_node:
            return
        change_scale = dist / (self._screen_size.width * 0.4)
        self.on_change_scale_helper(change_scale)

    def on_change_scale_helper(self, change_scale):
        if not self.cur_sel_node:
            return
        res_percent = self.cur_sel_node.on_change_scale(change_scale)
        res_percent = round(res_percent * 100)
        self.panel.nd_progress_size.setVisible(True)
        self.panel.nd_tips.setVisible(False)
        self.panel.progress_size.SetPercent(res_percent)
        self.panel.temp_slider_scale.slider.setPercent(res_percent)
        self.panel.quantity_size.SetString(str(res_percent) + '%')
        self.update_slider_percent_text(self.panel.temp_slider_scale, get_text_local_content(80659))

    def on_change_to_scale(self, res_scale):
        if not self.cur_sel_node:
            return
        cur_scale = self.cur_sel_node.get_cur_scale()
        change_scale = res_scale - cur_scale
        self.on_change_scale_helper(change_scale)

    def create_custom_panel(self, panel_name, parent_nd, cls, page):
        panel_conf = confmgr.get('c_panel_custom_conf', str(panel_name))
        start_node_name = panel_conf.get('cStartNode')
        start_node = getattr(parent_nd, start_node_name)
        if not start_node:
            log_error('Unexist node! panel name:%s node :%s' % (panel_name, start_node_name))
        c_panel = cls(panel_name, start_node, parent_nd, self.panel, self.panel.def_range_node, page, self._group_conf, self._exclude_area_list, self.get_cur_setting_no())
        return c_panel

    def init_custom_ui(self):
        self.check_default_setting_no()
        self.init_default_range_node()
        self.init_save_list()
        self.init_opacity_slider()
        self.init_scale_slider()
        self.panel.nd_choose_left.setVisible(False)
        self.panel.nd_choose_right.setVisible(False)
        self.panel.nd_progress_opacity.setVisible(False)
        self.panel.nd_progress_size.setVisible(False)
        self.panel.nd_tips.setVisible(False)
        self.panel.nd_ope.setLocalZOrder(2000)
        self.panel.touch_layer.setLocalZOrder(1500)
        self.on_switch_setting_no(-1, self.get_cur_setting_no(), is_init=True)

    def check_default_setting_no(self):
        if global_data.mecha and global_data.mecha.logic:
            mecha_id = global_data.mecha.share_data.ref_mecha_id
            mecha_conf = global_data.player.get_setting(ui_operation_const.CUSTOMER_UI_KEY, from_custom_setting_no=mecha_id)
            has_value = bool(mecha_conf)
            if has_value:
                setting_no = mecha_id
                self._cur_mecha_id = setting_no
                self.switch_mecha_only_state(True)
                self.all_used_page_set = {self.cur_page}
            else:
                self.cur_page = 'mecha'
                self.all_used_page_set = {self.cur_page}

    def init_default_range_node(self):
        size = global_data.ui_mgr.design_screen_size
        self.panel.def_range_node.setContentSize(size)
        self.panel.def_range_node.SetPosition('50%', '50%')

    def create_custom_panel_page_for_setting_no(self, setting_no=None, page=None):
        if setting_no is None:
            setting_no = self.get_cur_setting_no()
        if not page:
            page = self.cur_page
        nd = self.generate_custom_page(page, self.panel.nd_content)
        if not nd:
            log_error("Can't find page setting", page)
        else:
            setattr(self.panel, CUSTOM_PANEL_NAME % (page, setting_no), nd)
        if page == 'mecha':
            nd.setLocalZOrder(1)
        nd_custom_panel = getattr(self.panel, CUSTOM_PANEL_NAME % (page, setting_no), None)
        custom_name_list = confmgr.get('c_panel_custom_conf')
        for ui_name, conf in six.iteritems(custom_name_list):
            ui_page = conf['cPage']
            if conf['cIsEnable'] and (page == ui_page or ui_page == ''):
                c_panel = self.create_custom_panel(ui_name, nd_custom_panel, CustomPanel, page)
                if setting_no not in self.custom_panel_dict:
                    self.custom_panel_dict[setting_no] = list()
                self.custom_panel_dict[setting_no].append(c_panel)
                self.page_panel_list.append(ui_name)
            if not conf['cIsEnable']:
                panel_conf = confmgr.get('c_panel_custom_conf', str(ui_name))
                start_node_name = panel_conf.get('cStartNode')
                start_node = getattr(nd_custom_panel, start_node_name)
                if start_node:
                    start_node.setVisible(False)

        self._node_id_2_node_dict.setdefault(setting_no, {})
        panel_list = self.custom_panel_dict.get(setting_no, [])
        for c_panel in panel_list:
            node_ids = c_panel.get_node_ids()
            for node_id in node_ids:
                self._node_id_2_node_dict[setting_no].setdefault(str(node_id), [])
                self._node_id_2_node_dict[setting_no][str(node_id)].append(c_panel.get_custom_node(int(node_id)))

        return

    def generate_custom_page(self, page_name, page_parent, template_info=None):
        pages_conf = confmgr.get('c_panel_custom_page')
        page_conf = pages_conf.get(page_name, {})
        page_json = page_conf.get('cPageJson')
        if page_json:
            tconf = global_data.uisystem.load_template(page_json, template_info)

            def checkfunc(conf):
                if conf and conf.get('hide'):
                    return False
                if conf and conf.get('type_name') in ('CCAnimateSprite', 'CCParticleSystemQuad'):
                    return False
                return True

            nd = global_data.uisystem.create_item_with_check(tconf, page_parent, None, checkfunc=checkfunc)
            return nd
        else:
            return

    def save_cur_setting(self):
        if not (self.panel and self.panel.isValid()):
            return
        else:
            if not global_data.player:
                log_error('save_cur_setting:global_data.player is None!')
                return
            global_data.game_mgr.show_tip(get_text_local_content(2003))
            is_modified = self.check_has_modified()
            setting_no = self.get_cur_setting_no()
            self.set_panel_force_setting_no(self.get_cur_setting_no(), None)
            if not is_modified:
                if self._need_del_cur_mecha_setting_no and self._mecha_only:
                    global_data.player.revert_custom_setting_resolution_data(self.get_cur_setting_no(), True)
                    self._need_del_cur_mecha_setting_no = False
                    self.save_custom_ui_config({}, to_custom_setting_no=setting_no)
                return
            if self._is_just_reverted:
                global_data.player.revert_custom_setting_resolution_data(setting_no)
                self._is_just_reverted = False
            self.sync_group_top_node_setting_to_member()
            save_info = {}
            for c_panel in self.custom_panel_dict[setting_no]:
                c_panel.update_pos_for_resolution_before_save(setting_no)
                save_info.update(c_panel.get_save_info())

            for c_panel in self.custom_panel_dict[setting_no]:
                c_panel.on_saved()

            global_data.player.write_setting(ui_operation_const.CUSTOM_NODE_GROUPS, self._group_conf)
            save_info = copy.deepcopy(save_info)
            old_costom_user_ui_conf = global_data.player.get_setting(ui_operation_const.CUSTOMER_UI_KEY, from_custom_setting_no=setting_no)
            self.merge_two_custom_info(old_costom_user_ui_conf, save_info)
            if self._mecha_only and self._need_del_cur_mecha_setting_no:
                save_info = {}
                self._need_del_cur_mecha_setting_no = False
            global_data.player.write_setting(ui_operation_const.CUSTOMER_UI_KEY, save_info, page=list(self.all_used_page_set), to_custom_setting_no=setting_no)
            salog_writer = SALog.get_instance()
            salog_writer.write(SALog.BATTLE_CTRL_UI, save_info)
            self.save_custom_ui_config(save_info, to_custom_setting_no=setting_no)
            if is_modified:
                global_data.emgr.ui_change_custom_arrange_event.emit()
            self.refresh_save_list(None)
            return

    def merge_two_custom_info(self, old_info, new_info):
        for ui_name, ui_conf in six.iteritems(old_info):
            for set_key, set_key_conf in six.iteritems(ui_conf):
                for set_val, set_val_conf in six.iteritems(set_key_conf):
                    is_page_content = ui_name in self.page_panel_list
                    if is_page_content:
                        if ui_name not in new_info or set_key not in new_info[ui_name]:
                            continue
                    else:
                        new_info.setdefault(ui_name, {})
                        new_info[ui_name].setdefault(set_key, {})
                    new_info[ui_name][set_key].setdefault(set_val, {})
                    new_set_val_conf = new_info.get(ui_name, {}).get(set_key, {}).get(set_val, {})
                    if not new_set_val_conf:
                        new_info[ui_name][set_key][set_val] = set_val_conf

    def save_custom_ui_config(self, _save_info, to_custom_setting_no=None):
        save_info = copy.deepcopy(_save_info)
        for key, value in six.iteritems(save_info):
            if six.PY2:
                save_info[key] = six.moves.cPickle.dumps(value)
            else:
                save_info[key] = value

        global_data.player.save_custom_ui_config(save_info, to_custom_setting_no=to_custom_setting_no)

    def check_has_modified(self, setting_no=None):
        if setting_no is None:
            setting_no = self.get_cur_setting_no()
        if setting_no is None:
            return False
        else:
            for c_panel in self.custom_panel_dict[setting_no]:
                if c_panel.check_is_modified():
                    return True

            return False

    def revert_to_default_setting(self, setting_no=None):
        if self._mecha_only:
            self._need_del_cur_mecha_setting_no = True
        else:
            self._is_just_reverted = True
        if setting_no is None:
            setting_no = self.get_cur_setting_no()
        if not self._mecha_only:
            for c_panel in self.custom_panel_dict.get(setting_no, []):
                c_panel.revert_to_def_setting()
                c_panel.refresh_page_show(self.cur_page, ignore_always_show=self._mecha_only)

        else:
            mecha_conf = global_data.player.get_setting(ui_operation_const.CUSTOMER_UI_KEY, from_custom_setting_no=setting_no)
            is_modified = bool(mecha_conf)
            common_setting_no = global_data.player.get_cur_setting_no()
            self.set_panel_force_setting_no(setting_no, common_setting_no)
            panel_list = self.custom_panel_dict.get(setting_no, [])
            for c_panel in panel_list:
                c_panel.refresh_panel_node(force_panel_conf={})
                if is_modified:
                    c_panel.set_is_force_modified(is_modified)

        if str(setting_no) in self._group_conf:
            new_setting_no_group_conf = {}
            for group_name, group_node_ids in six.iteritems(self._group_conf.get(str(setting_no), {})):
                new_group_node_ids = get_group_all_node_ids(group_name)
                new_setting_no_group_conf[group_name] = new_group_node_ids

            self._group_conf[str(setting_no)] = new_setting_no_group_conf
        return

    def set_panel_force_setting_no(self, setting_no, force_setting_no):
        panel_list = self.custom_panel_dict.get(setting_no, [])
        for c_panel in panel_list:
            node_ids = c_panel.get_node_ids()
            for node_id in node_ids:
                c_node = c_panel.get_custom_node(node_id)
                c_node.set_force_setting_no(force_setting_no)

    def check_touch_node(self, wpos, setting_no=None):
        if setting_no is None:
            setting_no = self.get_cur_setting_no()
        touched_nodes = []
        for c_panel in self.custom_panel_dict[setting_no]:
            c_node = c_panel.check_is_point_in(wpos)
            touched_nodes.extend(c_node)

        return touched_nodes

    def check_save_button_state(self):
        is_modified = self.check_has_modified()
        if is_modified:
            self.panel.btn_save.SetSelect(True)
        else:
            self.panel.btn_save.SetSelect(False)
            if hasattr(self.panel, 'btn_save_2') and self.panel.btn_save_2:
                self.panel.btn_save_2.setVisible(False)

    def check_add_save_button_2(self):
        if hasattr(self.panel, 'btn_save_2') and self.panel.btn_save_2:
            return
        new_button = global_data.uisystem.load_template_create('common/i_common_button_small')
        if new_button:
            self.panel.btn_save.GetParent().AddChild('btn_save_2', new_button)
            new_button.setPosition(self.panel.btn_save.getPosition())
            new_button.setScale(self.panel.btn_save.getScale())
            new_button.setAnchorPoint(self.panel.btn_save.getAnchorPoint())
            new_button.btn_common.SetText(80049)
            new_button.SetContentSize(self.panel.btn_save.getContentSize().width, self.panel.btn_save.getContentSize().height)
            pic = 'gui/ui_res_2/common/button/btn_small_minor_sel.png'
            from common.utils.cocos_utils import CCRect
            new_button.btn_common.SetFrames('', [pic, pic, pic], True, CCRect(17, 24, 22, 20))
            new_button.ChildResizeAndPosition()
            self.panel.btn_save_2 = new_button

            @new_button.btn_common.unique_callback()
            def OnClick(btn, touch):
                self.on_click_save_btn(btn, touch)

    def init_save_list(self, is_refresh=False):
        cur_id = self.get_cur_setting_no()
        nd_list = self.panel.temp_save_list.option_list
        if not is_refresh:
            nd_list.DeleteAllSubItem()
        nd_list.SetInitCount(len(self._setting_no_list))
        for i, _setting_no in enumerate(self._setting_no_list):
            nd = nd_list.GetItem(i)
            if _setting_no in self.mecha_id_list:
                nd.nd_1.setVisible(False)
                nd.nd_2.setVisible(True)
                nd.lab_mecha.SetString(self.get_setting_no_page_name(_setting_no))
                from logic.gutils.item_utils import get_locate_pic_path
                from logic.gcommon.common_const.battle_const import LOCATE_MECHA
                nd.img_mecha.SetDisplayFrameByPath('', get_locate_pic_path(LOCATE_MECHA, None, mecha_id=_setting_no))
                mecha_conf = global_data.player.get_setting(ui_operation_const.CUSTOMER_UI_KEY, from_custom_setting_no=_setting_no)
                nd.lab_type.setVisible(bool(mecha_conf))
                nd.btn_copy.setVisible(_setting_no != cur_id and cur_id in self.mecha_id_list)
            else:
                nd.nd_1.setVisible(True)
                nd.nd_2.setVisible(False)
                nd.lab_content.SetString(self.get_setting_no_page_name(_setting_no))
                nd.btn_copy.setVisible(cur_id not in self.mecha_id_list and _setting_no != cur_id)
            self._register_save_list_item_click(nd.button, _setting_no)

            @nd.btn_copy.callback()
            def OnClick(btn, touch, new_i=_setting_no):
                self.on_copy_between_page(new_i)

        self.panel.btn_save_list.SetText(self.get_setting_no_page_name(cur_id))
        return

    def on_copy_between_page(self, new_setting_no):
        if self.check_has_modified():
            from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2

            def confirm_callback():
                if not (self.panel and self.panel.isValid()):
                    return
                self.save_cur_setting()
                _cur_id = self.get_cur_setting_no()
                self.on_copy_setting_no(_cur_id, new_setting_no)

            def cancel_callback():
                if not (self.panel and self.panel.isValid()):
                    return
                else:
                    _cur_id = self.get_cur_setting_no()
                    for panel in self.custom_panel_dict[_cur_id]:
                        panel.revert_to_previous_version()

                    if self._mecha_only:
                        self.set_panel_force_setting_no(_cur_id, None)
                    self.on_copy_setting_no(_cur_id, new_setting_no)
                    return

            SecondConfirmDlg2().confirm(content=get_text_local_content(2001), confirm_callback=confirm_callback, cancel_callback=cancel_callback)
        else:
            _cur_id = self.get_cur_setting_no()
            self.on_copy_setting_no(_cur_id, new_setting_no)

    def _register_save_list_item_click(self, btn, setting_no):

        @btn.unique_callback()
        def OnClick(*args):
            self._click_save_list_item(setting_no)

    def _click_save_list_item(self, setting_no):
        old_setting_no = self.get_cur_setting_no()
        if setting_no == old_setting_no:
            self._cur_save_list.setVisible(False)
            return
        if self.check_has_modified():
            from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2

            def confirm_callback():
                if not (self.panel and self.panel.isValid()):
                    return
                self.save_cur_setting()
                self.on_switch_setting_no(old_setting_no, setting_no)

            def cancel_callback():
                if not (self.panel and self.panel.isValid()):
                    return
                else:
                    for panel in self.custom_panel_dict[old_setting_no]:
                        panel.revert_to_previous_version()

                    if self._mecha_only:
                        self.set_panel_force_setting_no(old_setting_no, None)
                    self.on_switch_setting_no(old_setting_no, setting_no)
                    return

            SecondConfirmDlg2().confirm(content=get_text_local_content(2001), confirm_callback=confirm_callback, cancel_callback=cancel_callback)
        else:
            self.on_switch_setting_no(old_setting_no, setting_no)

    def refresh_save_list(self, setting_no):
        if setting_no is None:
            setting_no = self.get_cur_setting_no()
        common_setting_no = global_data.player.get_cur_setting_no()
        for i, _setting_no in enumerate(self._setting_no_list):
            nd = self._cur_save_list.option_list.GetItem(i)
            nd.button.SetSelect(setting_no == _setting_no)
            if _setting_no in self.mecha_id_list:
                nd.btn_copy.setVisible(setting_no != _setting_no and setting_no in self.mecha_id_list)
            else:
                nd.btn_copy.setVisible(setting_no != _setting_no and setting_no in self._common_setting_no_list)
            if common_setting_no == _setting_no and setting_no not in self._common_setting_no_list:
                nd.img_choose.setVisible(True)
            else:
                nd.img_choose.setVisible(False)
            if _setting_no in self.mecha_id_list:
                mecha_conf = global_data.player.get_setting(ui_operation_const.CUSTOMER_UI_KEY, from_custom_setting_no=_setting_no)
                nd.lab_type.setVisible(bool(mecha_conf))

        return

    def on_switch_setting_no(self, old_setting_no, setting_no, is_init=False):
        self.refresh_save_list(setting_no)
        old_mecha_only = self._mecha_only
        if setting_no in self.mecha_id_list:
            self.switch_mecha_only_state(True)
        else:
            self.switch_mecha_only_state(False)
        self._need_del_cur_mecha_setting_no = False
        self._is_just_reverted = False
        if not self._mecha_only:
            global_data.player.set_cur_setting_no(setting_no)
        else:
            self._cur_mecha_id = setting_no
        common_setting_no = global_data.player.get_cur_setting_no()
        self._cur_save_list.setVisible(False)
        self.panel.btn_save_list.SetText(self.get_setting_no_page_name(setting_no))
        if not old_mecha_only:
            all_page_list = ALL_PAGE_LIST if 1 else [self.cur_page]
            for page in all_page_list:
                old_nd_custom = getattr(self.panel, CUSTOM_PANEL_NAME % (page, old_setting_no), None)
                old_nd_custom and old_nd_custom.setVisible(False)

            if not self._mecha_only:
                if self.cur_page == 'mecha':
                    all_page_list = ALL_PAGE_LIST
                else:
                    all_page_list = {
                     self.cur_page}
            else:
                all_page_list = {
                 self.cur_page}
            for page in all_page_list:
                new_nd_custom = getattr(self.panel, CUSTOM_PANEL_NAME % (page, setting_no), None)
                if not new_nd_custom:
                    self.create_custom_panel_page_for_setting_no(setting_no=setting_no, page=page)
                    new_nd_custom = getattr(self.panel, CUSTOM_PANEL_NAME % (page, setting_no), None)
                    if self._mecha_only:
                        self.mecha_panel_common_setting_no[setting_no] = common_setting_no
                new_nd_custom and new_nd_custom.setVisible(True)

            for c_panel in self.custom_panel_dict.get(setting_no, []):
                c_panel.refresh_page_show(self.cur_page, ignore_always_show=self._mecha_only)

            if self._mecha_only:
                mecha_conf = global_data.player.get_setting(ui_operation_const.CUSTOMER_UI_KEY, from_custom_setting_no=setting_no)
                if not bool(mecha_conf):
                    panel_list = self.custom_panel_dict.get(setting_no, [])
                    for c_panel in panel_list:
                        c_panel.refresh_panel_node()

                    self.mecha_panel_common_setting_no[setting_no] = common_setting_no
            self.select_node(None)
            self.check_save_button_state()
            is_init or global_data.emgr.ui_change_custom_arrange_event.emit()
        self._need_check_node_sync = True
        self.update_page_related_show()
        self.all_used_page_set = set(all_page_list)
        return

    def on_copy_setting_no(self, from_no, to_no):
        self._cur_save_list.setVisible(False)
        from_user_ui_conf = global_data.player.get_setting(ui_operation_const.CUSTOMER_UI_KEY, from_custom_setting_no=from_no)
        conf = copy.deepcopy(from_user_ui_conf)
        all_used_page_set = self._mecha_only or ALL_PAGE_LIST if 1 else {'mecha'}
        global_data.player.write_setting(ui_operation_const.CUSTOMER_UI_KEY, conf, page=list(all_used_page_set), to_custom_setting_no=to_no)
        for page in all_used_page_set:
            global_data.player.copy_custom_setting_resolution_data(page, from_no, to_no)

        if str(from_no) in self._group_conf:
            self._group_conf[str(to_no)] = copy.deepcopy(self._group_conf[str(from_no)])
        elif not self._mecha_only:
            log_error('group node should have data in it!!!', self._group_conf)
        global_data.player.write_setting(ui_operation_const.CUSTOM_NODE_GROUPS, self._group_conf)
        self.save_custom_ui_config(conf, to_custom_setting_no=to_no)
        panel_list = self.custom_panel_dict.get(to_no, [])
        for c_panel in panel_list:
            c_panel.refresh_panel_node()

        global_data.game_mgr.show_tip(get_text_by_id(860183, {'scheme': self.get_setting_no_page_name(to_no)}))
        self.refresh_save_list(None)
        if to_no in self.mecha_id_list:
            target_mecha_id = None
            if global_data.cam_lctarget and global_data.cam_lctarget.sd.ref_is_mecha:
                target_mecha_id = global_data.cam_lctarget.share_data.ref_mecha_id
            elif global_data.mecha and global_data.mecha.logic:
                target_mecha_id = global_data.mecha.share_data.ref_mecha_id
            if str(target_mecha_id) == str(to_no):
                global_data.emgr.ui_change_custom_arrange_event.emit()
        return

    def init_opacity_slider(self):
        cur_percent = 50
        if self.cur_sel_node:
            min_opacity, max_opacity = self.cur_sel_node.opacity_range
            init_opacity = self.cur_sel_node.init_opacity
            cur_opacity = self.cur_sel_node.start_opacity
            cur_percent = round(float(cur_opacity - min_opacity) / (max_opacity - min_opacity) * 100)
        self.panel.temp_slider_transparency.slider.setPercent(cur_percent)
        from logic.gutils.template_utils import init_setting_slider1

        def call_back(val):
            if self.cur_sel_node:
                min_opacity, max_opacity = self.cur_sel_node.opacity_range
                res_opacity = (max_opacity - min_opacity) * val / 100.0 + min_opacity
                self.on_change_to_opacity(res_opacity)
                self.on_change_opacity_end()

        init_setting_slider1(self.panel.temp_slider_transparency, get_text_local_content(80370), call_back)

    def init_scale_slider(self):
        cur_percent = 50
        if self.cur_sel_node:
            min_scale, max_scale = self.cur_sel_node.scale_range
            cur_scale = self.cur_sel_node.get_cur_scale()
            cur_percent = round(float(cur_scale - min_scale) / (max_scale - min_scale) * 100)
        self.panel.temp_slider_scale.slider.setPercent(cur_percent)
        from logic.gutils.template_utils import init_setting_slider1

        def call_back(val):
            if self.cur_sel_node:
                min_scale, max_scale = self.cur_sel_node.scale_range
                res_scale = (max_scale - min_scale) * val / 100.0 + min_scale
                self.on_change_to_scale(res_scale)
                self.on_change_scale_end()

        init_setting_slider1(self.panel.temp_slider_scale, get_text_local_content(80659), call_back)

    def update_slider_percent_text(self, slider_widget, name):
        val = slider_widget.slider.getPercent()
        slider_widget.name.SetString('{0}({1}%)'.format(name, val))

    def get_setting_no_page_name(self, setting_no):
        if int(setting_no) in self.mecha_id_list:
            return get_mecha_name_by_id(setting_no)
        else:
            setting_no = int(setting_no)
            name = global_data.player.get_setting(ui_operation_const.CUSTOM_PAGE_NAME_PREFIX + str(setting_no + 1))
            if not name:
                return get_text_by_id(SETTING_NO_TEXT_ID[setting_no])
            return name

    def change_setting_no_page_name(self, setting_no, name):
        if not self.panel:
            return
        setting_no = int(setting_no)
        global_data.player.write_setting(ui_operation_const.CUSTOM_PAGE_NAME_PREFIX + str(setting_no + 1), name)
        cur_id = self.get_cur_setting_no()
        if str(setting_no) == str(cur_id):
            self.panel.btn_save_list.SetText(self.get_setting_no_page_name(cur_id))
        nd_list = self._cur_save_list.option_list
        nd = nd_list.GetItem(setting_no)
        if nd:
            nd.button.SetText(name)

    def sync_group_top_node_setting_to_member(self):
        if self._mecha_only:
            return
        cur_group_conf = self._group_conf
        cur_id = self.get_cur_setting_no()
        for group_name, node_ids in six.iteritems(self._group_dict):
            group_node_id_list = cur_group_conf.get(str(cur_id), {}).get(group_name, [])
            if group_node_id_list:
                top_node_id = group_node_id_list[0]
                for node_id in group_node_id_list[1:]:
                    self.sync_node_to_node(cur_id, top_node_id, node_id)

    def get_node_by_id_and_index(self, setting_no, node_id, index=0):
        c_node_list = self._node_id_2_node_dict.get(setting_no, {}).get(str(node_id), [])
        if index < len(c_node_list):
            return c_node_list[index]
        else:
            return None

    def test_hide_shadow(self, setting_no):
        for setting_no, panel_list in six.iteritems(self.custom_panel_dict):
            for c_panel in panel_list:
                for c_node in six_ex.values(c_panel.custom_node_dict):
                    c_node.purely_hide_shadow()

    def test_show_shadow(self, setting_no):
        for setting_no, panel_list in six.iteritems(self.custom_panel_dict):
            for c_panel in panel_list:
                for c_node in six_ex.values(c_panel.custom_node_dict):
                    if c_node.shadow_sprite:
                        continue

    def on_click_btn_copy(self, btn, touch):
        if self.cur_sel_node and self.cur_sel_node.is_copyable_node():
            copy_nodes = self.cur_sel_node.get_copy_nodes()
            if copy_nodes:
                setting_no = self.get_cur_setting_no()
                for node_id in copy_nodes:
                    c_node = self.get_node_by_id_and_index(setting_no, node_id)
                    if c_node:
                        if not c_node.is_came_to_life():
                            c_node.come_to_life()
                            c_node.set_user_config({})
                        if not c_node.get_is_usable():
                            c_node.set_is_usable(True)
                            cus_conf = self.cur_sel_node.get_custom_conf()
                            c_node.copy_custom_conf_from_other(cus_conf)
                            if not c_node.should_hide():
                                c_node.show()
                                c_node.sync_to_wpos(self.cur_sel_node.get_node_world_position())
                                c_node.move_node(50, 50)
                            break

            self.refresh_copy_delete_show()

    def is_select_node_can_copy(self):
        if self.cur_sel_node and self.cur_sel_node.is_copyable_node():
            copy_nodes = self.cur_sel_node.get_copy_nodes()
            if copy_nodes:
                setting_no = self.get_cur_setting_no()
                for node_id in copy_nodes:
                    c_node = self.get_node_by_id_and_index(setting_no, node_id)
                    if c_node and not (c_node.is_came_to_life() and c_node.get_is_usable()):
                        return True

        return False

    def is_select_node_can_delete(self):
        if self.cur_sel_node and self.cur_sel_node.get_copy_source():
            return True
        return False

    def on_click_btn_delete(self, btn, touch):
        if self.cur_sel_node and self.cur_sel_node.get_copy_source():
            cur_sel_node = self.cur_sel_node
            self.select_node(None)
            cur_sel_node.hide()
            cur_sel_node.set_is_usable(False)
        self.refresh_copy_delete_show()
        return

    def get_cur_setting_no(self):
        if not self._mecha_only and global_data.player:
            return global_data.player.get_cur_setting_no()
        else:
            return self._cur_mecha_id