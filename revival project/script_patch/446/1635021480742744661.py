# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/role/PlayerOpSelectUI.py
from __future__ import absolute_import
from __future__ import print_function
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER
import cc
import world
from common.const import uiconst
from common.utils.cocos_utils import neox_pos_to_cocos
from logic.gcommon.const import NEOX_UNIT_SCALE

class PlayerOpSelectUI(BasePanel):
    PANEL_CONFIG_NAME = 'lobby/i_computer_select'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE_BY_DEFAULT_FUNC_NAME
    UI_ACTION_EVENT = {'nd_bg.OnBegin': 'on_close',
       'btn_enter_1.OnClick': 'on_click_btn_enter_1',
       'btn_enter_2.OnClick': 'on_click_btn_enter_2',
       'btn_enter_3.OnClick': 'on_click_btn_enter_3'
       }

    def on_init_panel(self):
        import common.utils.timer as timer
        self._auto_close_timer_id = None
        self._update_pos_timer_id = None
        self.panel.PlayAnimation('show')
        self._ui_pos_base_model = world.get_active_scene().get_model('box_computer1')
        if self._ui_pos_base_model:
            self._update_pos_timer_id = global_data.game_mgr.get_fix_logic_timer().register(func=self.update_pos, interval=1, times=-1, mode=timer.LOGIC)
        else:
            print(('test--PlayerOpSelectUI.on_init_panel--_ui_pos_base_model =', self._ui_pos_base_model, '--need add by liang yi'))
            import traceback
            traceback.print_stack()
        return

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
        camera = world.get_active_scene().active_camera
        if not camera:
            return
        cur_world_pos = self._ui_pos_base_model.world_position
        neox_2d_pos = camera.world_to_screen(cur_world_pos)
        cocos_2d_pos = neox_pos_to_cocos(*neox_2d_pos)
        self.panel.setPosition(*cocos_2d_pos)
        max_pos_z = 1.2
        max_dist = 15 * NEOX_UNIT_SCALE
        player_position = global_data.lobby_player.ev_g_position()
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
        global_data.ui_mgr.show_ui('LobbyBagUI', 'logic.comsys.lobby')
        self.on_close()
        self.panel.PlayAnimation('click_01')

    def on_click_btn_enter_2(self, *args):
        global_data.ui_mgr.show_ui('MainEmail', 'logic.comsys.message')
        self.on_close()
        self.panel.PlayAnimation('click_02')

    def on_click_btn_enter_3(self, btn, touch):
        global_data.ui_mgr.show_ui('MainFriend', 'logic.comsys.message')
        self.on_close()
        self.panel.PlayAnimation('click_03')