# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/OnHookUI.py
from __future__ import absolute_import
import six
import math3d
import world
from common.uisys.basepanel import BasePanel
from common.const import uiconst
from common.uisys.uielment.CCUISpaceNode import CCUISpaceNode
from logic.gcommon.common_const.mecha_const import MECHA_MODE_BLOOD_SOCKET_POS_OFFSET
from logic.comsys.common_ui.NormalConfirmUI import NormalConfirmUI2
from mobile.common.EntityManager import EntityManager
from logic.gcommon.common_utils import battle_utils
from logic.gcommon.const import NEOX_UNIT_SCALE
from common.utils import timer

class OnHookNormalConfirmUI(NormalConfirmUI2):

    def on_finalize_panel(self):
        super(OnHookNormalConfirmUI, self).on_finalize_panel()
        battle_utils.set_block_control(False, 'ON_HOOK')


class OnHookLocateUI(object):

    def __init__(self, parent, eid):
        self.parent = parent
        self.tick_timer = None
        self.model = None
        self.eid = eid
        self._nd = global_data.uisystem.load_template_create('battle_tips/status_tag/i_battle_status_tag_afk')
        self._nd.SetEnableCascadeOpacityRecursion(True)
        self._space_node = CCUISpaceNode.Create()
        self._space_node.AddChild('', self._nd)
        self._nd.setPosition(0, 0)
        self._nd.setScale(1.0)
        self._nd_visible = False
        self._cur_need_draw = False
        self._show_hit = False
        self._show_hit_time = -1
        self._nd.setVisible(self.get_nd_visible())

        def vis_callback(last_need_draw, cur_need_draw):
            self._cur_need_draw = bool(cur_need_draw)
            if self._nd and self._nd.isValid():
                self._nd.setVisible(True if self.get_nd_visible() else False)

        self._space_node.set_visible_callback(vis_callback)
        self.refresh_info()
        return

    def get_nd_visible(self):
        return self._cur_need_draw and self._nd_visible or self._show_hit

    def clear_timer(self):
        self.tick_timer and global_data.game_mgr.get_logic_timer().unregister(self.tick_timer)
        self.tick_timer = None
        return

    def create_timer(self):
        self.clear_timer()
        self.tick_timer = global_data.game_mgr.get_logic_timer().register(func=self.refresh_simui_scale, mode=timer.LOGIC, timedelta=True)

    def show_hit_mark(self):
        self._show_hit_time = -1
        self.set_show_hit()

    def set_show_hit(self):
        self._show_hit = self._show_hit_time < 2

    def refresh_info(self):
        ent = EntityManager.getentity(self.eid)
        if ent and ent.logic:
            model = ent.logic.ev_g_model()
            if ent.__class__.__name__ == 'Mecha':
                mecha_mode = ent.logic.ev_g_mecha_mode()
                mecha_id = ent.logic.ev_g_mecha_id()
                pos_offset = MECHA_MODE_BLOOD_SOCKET_POS_OFFSET.get(mecha_id, {}).get(mecha_mode, 0)
                socket_name = 'xuetiao'
            else:
                pos_offset = 0
                socket_name = 's_xuetiao'
            if model and model.valid and self._nd and self._nd.isValid():
                self.create_timer()
                self._space_node.bind_model(model, socket_name)
                self._space_node.set_fix_xz(False)
                self._space_node.set_pos_offset(math3d.vector(0, pos_offset * model.scale.y, 0))
                self._cur_need_draw = self._space_node.get_is_in_screen()
                self._nd_visible = model.visible
                self._nd.setVisible(self.get_nd_visible())
                self.model = model
                self.refresh_simui_scale()

    def refresh_simui_scale(self, dt=0.0):
        self._show_hit_time += dt
        self._show_hit_time = min(10, self._show_hit_time)
        self.set_show_hit()
        scn = world.get_active_scene()
        if self._nd and self._nd.isValid():
            self._cur_need_draw = self._space_node.get_is_in_screen()
            self._nd.setVisible(self.get_nd_visible())
        if scn and scn.active_camera and self.model and self.model.valid and self._nd and self._nd.isValid() and self._nd.isVisible():
            player_position = scn.active_camera.position
            cam_lplayer = global_data.cam_lplayer
            if cam_lplayer:
                player_position = cam_lplayer.ev_g_position()
            pos = self.model.position
            new_cam_pos = math3d.vector(player_position.x, pos.y, player_position.z)
            dist = new_cam_pos - pos
            dist = dist.length / NEOX_UNIT_SCALE
            max_dist = 40
            mix_dist = 30
            if dist > mix_dist:
                alpha = 1.0 if self._show_hit else max(0, (max_dist - dist) * 1.0 / (max_dist - mix_dist))
                self._nd.setOpacity(int(255 * alpha))
            else:
                self._nd.setOpacity(255)
            mix_dist = 20
            if dist > mix_dist:
                scale = max(0.5, (max_dist - dist) * 1.0 / (max_dist - mix_dist))
                self._nd.setScale(scale)
            else:
                self._nd.setScale(1.0)

    def on_finalize_panel(self):
        self._nd and self._nd.Destroy()
        self._nd = None
        self._space_node and self._space_node.Destroy()
        self._space_node = None
        self.clear_timer()
        return


class OnHookUI(BasePanel):
    DLG_ZORDER = uiconst.LOW_MESSAGE_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    PANEL_CONFIG_NAME = 'battle/empty'
    GLOBAL_EVENT = {'battle_afk_invincible_event': 'on_battle_afk_invincible',
       'settle_stage_event': 'on_settle_stage',
       'target_invincible_event': 'show_hit_mark'
       }

    def on_init_panel(self, *args, **kargs):
        self.on_hook_obj = {}
        self.game_over = False

    def on_settle_stage(self, *args):
        self.game_over = True

    def on_finalize_panel(self):
        for ui_nd in six.itervalues(self.on_hook_obj):
            ui_nd and ui_nd.on_finalize_panel()

        self.on_hook_obj = {}

    def on_battle_afk_invincible(self, is_add, eid):
        if is_add:
            self.add_on_hook(eid)
        else:
            self.del_on_hook(eid)

    def add_on_hook(self, eid):
        if eid not in self.on_hook_obj:
            self.on_hook_obj[eid] = OnHookLocateUI(self, eid)
        else:
            self.on_hook_obj[eid].refresh_info()
        if global_data.player and eid == global_data.player.id:
            self.on_show_hang_up()
            battle_utils.set_block_control(True, 'ON_HOOK')

    def del_on_hook(self, eid):
        if eid in self.on_hook_obj:
            self.on_hook_obj[eid].on_finalize_panel()
            del self.on_hook_obj[eid]
        if global_data.player and eid == global_data.player.id:
            global_data.ui_mgr.close_ui('OnHookNormalConfirmUI')
            battle_utils.set_block_control(False, 'ON_HOOK')

    def on_show_hang_up(self):
        if self.game_over:
            global_data.ui_mgr.close_ui('OnHookNormalConfirmUI')
            return

        def _confirm():
            if global_data.battle:
                global_data.battle.finish_akf_status()

        OnHookNormalConfirmUI(zorder=uiconst.GUIDE_LAYER_ZORDER, on_confirm=_confirm, content=get_text_by_id(900028), confirm_text=get_text_by_id(83517))
        from logic.comsys.battle.BattleUtils import stop_self_fire_and_movement
        stop_self_fire_and_movement(only_move=True)

    def show_hit_mark(self, unit_obj, *args, **kargs):
        if not unit_obj:
            return
        eid = unit_obj.id
        if eid in self.on_hook_obj:
            self.on_hook_obj[eid].show_hit_mark()