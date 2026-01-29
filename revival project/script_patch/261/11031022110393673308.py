# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_display/MechaOpSelectUI.py
from __future__ import absolute_import
from __future__ import print_function
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER
import cc
import world
from common.const import uiconst
from common.utils.cocos_utils import neox_pos_to_cocos
from logic.gcommon.const import NEOX_UNIT_SCALE

class MechaOpSelectUI(BasePanel):
    PANEL_CONFIG_NAME = 'lobby/i_mecha_select'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE_BY_DEFAULT_FUNC_NAME
    UI_ACTION_EVENT = {'nd_bg.OnBegin': 'on_close',
       'btn_enter_1.OnClick': 'on_click_btn_enter_1',
       'btn_enter_2.OnClick': 'on_click_btn_enter_2',
       'btn_enter_3.OnClick': 'on_click_btn_enter_3'
       }

    def on_init_panel(self):
        import common.utils.timer as timer
        delay_time = 7
        self._auto_close_timer_id = global_data.game_mgr.register_logic_timer(self.on_close, interval=delay_time, times=1, mode=timer.CLOCK)
        self._update_pos_timer_id = global_data.game_mgr.get_fix_logic_timer().register(func=self.update_pos, interval=1, times=-1, mode=timer.LOGIC)
        self.panel.PlayAnimation('show')

    def on_finalize_panel(self):
        if self._auto_close_timer_id:
            global_data.game_mgr.unregister_logic_timer(self._auto_close_timer_id)
        self._auto_close_timer_id = None
        self.unregister_update_pos_timer()
        return

    def on_close(self, *args):
        aniName = 'disappear'
        max_time = self.GetAnimationMaxRunTime(aniName)
        self.panel.PlayAnimation(aniName)
        self.panel.runAction(cc.Sequence.create([
         cc.DelayTime.create(max_time),
         cc.CallFunc.create(self.close)]))

    def unregister_update_pos_timer(self):
        if self._update_pos_timer_id:
            global_data.game_mgr.get_fix_logic_timer().unregister(self._update_pos_timer_id)
        self._update_pos_timer_id = None
        return

    def update_pos(self, *args):
        if not global_data.lobby_player:
            self.unregister_update_pos_timer()
            return
        mecha_model = global_data.emgr.lobby_cur_display_mecha.emit()[0]
        if not mecha_model:
            return
        camera = world.get_active_scene().active_camera
        if not camera:
            return
        socket_name = 'jiaohu'
        if not mecha_model.has_socket(socket_name):
            self.unregister_update_pos_timer()
            print(('[Error]test--update_pos--step1--mecha_model.filename =', mecha_model.filename, '--do not have scoket =', socket_name))
            import traceback
            traceback.print_stack()
            return
        mat = mecha_model.get_socket_matrix(socket_name, world.SPACE_TYPE_WORLD)
        cur_world_pos = mat.translation
        neox_2d_pos = camera.world_to_screen(cur_world_pos)
        cocos_2d_pos = neox_pos_to_cocos(*neox_2d_pos)
        self.panel.setPosition(*cocos_2d_pos)
        max_pos_z = 1.2
        max_dist = 15 * NEOX_UNIT_SCALE
        player_position = global_data.lobby_player.ev_g_position()
        if not player_position:
            return
        player_position.y = 0
        cur_world_pos.y = 0
        cur_dist = (cur_world_pos - player_position).length
        pos_z = 0
        if cur_dist >= max_dist:
            pos_z = max_pos_z
        else:
            pos_z = max_pos_z * cur_dist / max_dist
        self.panel.setPositionZ(pos_z)

    def on_click_btn_enter_1(self, *args):
        global_data.ui_mgr.show_ui('ChangeMechaUI', 'logic.comsys.mecha_display')
        self.on_close()
        self.panel.PlayAnimation('click_01')

    def on_click_btn_enter_2(self, *args):
        self._on_show_skin_define()
        self.on_close()
        self.panel.PlayAnimation('click_02')

    def on_click_btn_enter_3(self, btn, touch):
        ui = global_data.ui_mgr.show_ui('InscriptionMainUI', 'logic.comsys.mecha_display')
        if ui:
            ui.show_mecha_details()
        global_data.lobby_red_point_data.record_main_rp('tech_info_rp')
        self.panel.PlayAnimation('click_03')
        self.on_close()

    def _get_mecha_model_data(self):
        import logic.gutils.dress_utils as dress_utils
        import logic.gutils.mecha_skin_utils as mecha_skin_utils
        is_in_visit_mode = global_data.player.is_in_visit_mode()
        mecha_item_id = global_data.player.get_lobby_selected_mecha_item_id()
        mecha_id = dress_utils.mecha_lobby_id_2_battle_id(mecha_item_id)
        clothing_id = global_data.player.get_mecha_fashion(mecha_item_id)
        skin_item_id = dress_utils.get_mecha_skin_item_no(mecha_id, clothing_id)
        shiny_id = mecha_skin_utils.get_mecha_skin_shiny_id(skin_item_id)
        return (
         mecha_id, clothing_id, shiny_id)

    def _on_show_skin_define(self):
        mecha_id, clothing_id, shiny_id = self._get_mecha_model_data()
        from logic.gutils.jump_to_ui_utils import jump_to_skin_define
        mecha_id, clothing_id, shiny_id = self._get_mecha_model_data()
        jump_to_skin_define(mecha_id, clothing_id)