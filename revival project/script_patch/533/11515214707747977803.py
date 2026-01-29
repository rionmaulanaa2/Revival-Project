# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/TitleContainerUI.py
from __future__ import absolute_import
from six.moves import range
from common.const.uiconst import BASE_LAYER_ZORDER, UI_VKB_NO_EFFECT
from common.uisys.basepanel import BasePanel
from logic.gutils.template_utils import refresh_career_title_node
from common.utils.cocos_utils import neox_pos_to_cocos
from cocosui import cc
from logic.gcommon.const import NEOX_UNIT_SCALE
import math3d
from logic.gutils import title_utils
from logic.gcommon.common_const import title_const
import render
from common.uisys.uielment.CCLayer import CCLayer
from common.utils.cocos_utils import ccp, CCSize
from logic.manager_agents.manager_decorators import sync_exec
TITLE_VISIBLE_MAX_DIS_METER = 50.0
TITLE_VISIBLE_MAX_DIS = TITLE_VISIBLE_MAX_DIS_METER * NEOX_UNIT_SCALE

class TitleContainerUI(BasePanel):
    PANEL_CONFIG_NAME = 'role/fight_life_name_container'
    DLG_ZORDER = BASE_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_NO_EFFECT
    CACHE_INIT_CNT = 6
    CACHE_MAX_CNT = 15
    TITLE_NODE_TEMP_PATH = 'role/i_role_life_name_item'

    def on_init_panel(self, *args, **kargs):
        node = global_data.uisystem.load_template_create(self.TITLE_NODE_TEMP_PATH, None, name='title_node')
        self._title_temp_width, self._title_temp_height = node.GetContentSize()
        node.Destroy()
        self._title_node_bundle_pool = []
        for _ in range(self.CACHE_INIT_CNT):
            title_node, rt, tex = self._new_title_node()
            self._recycle_title_node(title_node, rt, tex)

        self._active_title_map = {}
        return

    def on_finalize_panel(self):
        if self._title_node_bundle_pool:
            for node_bundle in self._title_node_bundle_pool:
                title_node, rt, tex = node_bundle
                parent = title_node.GetParent()
                if parent is not None:
                    parent.Destroy()
                rt.release()

        self._title_node_bundle_pool = None
        self._active_title_map = None
        return

    def get_title_size_ratio(self):
        return float(self._title_temp_height) / self._title_temp_width

    def show_title(self, title_item_no, unit_id):
        if unit_id is None:
            return
        else:
            if title_item_no is None:
                return
            if unit_id in self._active_title_map:
                title_node, rt, tex = self._active_title_map[unit_id]
            else:
                title_node, rt, tex = self._fetch_title_node()
                self._active_title_map[unit_id] = (title_node, rt, tex)
            refresh_career_title_node(title_node, title_item_no)
            return tex

    def remove_title(self, unit_id):
        if unit_id is None:
            return
        else:
            node_bundle = self._active_title_map.get(unit_id, None)
            if node_bundle is None:
                return
            title_node, rt, tex = node_bundle
            if title_node is None:
                return
            del self._active_title_map[unit_id]
            self._recycle_title_node(title_node, rt, tex)
            return

    @sync_exec
    def update_title(self, unit_id, title_world_pos):
        if unit_id is None:
            return
        else:
            node_bundle = self._active_title_map.get(unit_id, None)
            if node_bundle is None:
                return
            title_node, rt, tex = node_bundle
            if title_node is None:
                return
            if rt is None or not rt.isValid():
                return
            scene = global_data.game_mgr.scene
            if not (scene and scene.valid):
                return
            cam = scene.active_camera
            world_dis_sqr = (cam.position - title_world_pos).length_sqr
            x, y = cam.world_to_screen(title_world_pos)
            title_in_cam = cam.world_to_camera(title_world_pos)
            if self._is_in_screen(x, y) and world_dis_sqr <= TITLE_VISIBLE_MAX_DIS * TITLE_VISIBLE_MAX_DIS:
                title_node.setVisible(True)
            else:
                title_node.setVisible(False)
            rt.clear(1.0, 1.0, 1.0, 0.0)
            parent_raw = title_node.getParent()
            if parent_raw is not None:
                rt.begin()
                rt.addCommandsForNode(parent_raw)
                rt.end()
            return

    def _is_in_screen(self, screen_x, screen_y):
        screen_width = global_data.ui_mgr.screen_size.width
        screen_height = global_data.ui_mgr.screen_size.height
        if screen_x >= 0 and screen_x <= screen_width and screen_y >= 0 and screen_y <= screen_height:
            return True
        return False

    def _fetch_title_node(self):
        if len(self._title_node_bundle_pool) <= 0:
            title_node, rt, tex = self._new_title_node()
        else:
            title_node, rt, tex = self._title_node_bundle_pool.pop()
        title_node.setVisible(True)
        return (
         title_node, rt, tex)

    def _recycle_title_node(self, title_node, rt, tex):
        if title_node is None:
            return
        else:
            if len(self._title_node_bundle_pool) >= self.CACHE_MAX_CNT:
                parent = title_node.GetParent()
                if parent is None:
                    title_node.Destroy()
                else:
                    parent.Destroy()
                rt.release()
            else:
                title_node.setVisible(False)
                self._title_node_bundle_pool.append((title_node, rt, tex))
            return

    def _new_title_node(self):
        node = global_data.uisystem.load_template_create(self.TITLE_NODE_TEMP_PATH, None, name='title_node')
        node.setScaleX(-1)
        node.setScaleY(-1)
        node.SetTouchEnabledRecursion(False, cclayer_only=False)
        w, h = self._title_temp_width, self._title_temp_height
        layer = CCLayer.Create()
        layer.setPosition(ccp(w / 2, h / 2))
        layer.ignoreAnchorPointForPosition(False)
        layer.setAnchorPoint(ccp(0.5, 0.5))
        layer.setContentSize(CCSize(w, h))
        layer.setVisible(True)
        layer.SetEnableTouch(False)
        layer.retain()
        layer.AddChild('real_title_node', node)
        node.setPosition(ccp(w / 2, h / 2))
        tex = render.texture.create_empty(int(self._title_temp_width), int(self._title_temp_height), render.PIXEL_FMT_A8R8G8B8, True)
        rt = cc.RenderTexture.createWithITexture(tex)
        rt.retain()
        return (
         node, rt, tex)