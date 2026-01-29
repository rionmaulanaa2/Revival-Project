# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/pet/PetInteractUI.py
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER
import cc
import world
from common.const import uiconst
from common.utils.cocos_utils import neox_pos_to_cocos
from logic.gcommon.const import NEOX_UNIT_SCALE
ICON_ENTER_IMG = {True: 'gui/ui_res_2/main/select_mecha/btn_main_int_01.png',
   False: 'gui/ui_res_2/main/select_mecha/btn_main_int_01_dark.png'
   }
PNL_BTN_IMG = {True: 'gui/ui_res_2/main/select_mecha/pnl_main_sel_blue.png',
   False: 'gui/ui_res_2/main/select_mecha/pnl_main_sel_blue_dark.png'
   }
IMG_LINE = {True: 'gui/ui_res_2/main/select_mecha/img_blue.png',
   False: 'gui/ui_res_2/main/select_mecha/img_blue_dark.png'
   }
from common.utils.cocos_utils import ccc4FromHex
LAB_OUTLINE = (
 ccc4FromHex(3618180), 1)

class PetInteractUI(BasePanel):
    PANEL_CONFIG_NAME = 'lobby/i_pet_select'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE_BY_DEFAULT_FUNC_NAME
    UI_ACTION_EVENT = {'nd_bg.OnBegin': 'on_close'
       }

    def on_init_panel(self):
        self.pet_logic = None
        if global_data.player_pet and global_data.player_pet.logic:
            self.pet_logic = global_data.player_pet.logic
        elif global_data.lobby_pet:
            self.pet_logic = global_data.lobby_pet
        if self.pet_logic is None:
            self.close()
            return
        else:
            import common.utils.timer as timer
            delay_time = 7
            self._auto_close_timer_id = global_data.game_mgr.register_logic_timer(self.on_close, interval=delay_time, times=1, mode=timer.CLOCK)
            self._update_pos_timer_id = global_data.game_mgr.get_fix_logic_timer().register(func=self.update_pos, interval=1, times=-1, mode=timer.LOGIC)
            self.panel.PlayAnimation('show')
            pet_level = self.pet_logic.ev_g_level()
            anim_info_list = []
            for i in range(1, 4):
                anim_name, _, anim_info = self.pet_logic.ev_g_anim_info('interact_anim{}'.format(i), check_level=False)
                if anim_name:
                    anim_info_list.append(anim_info)

            self.btn_2_anim_idx = [
             None, None, None]

            def init_btn(i, anim_idx):
                btn = getattr(self.panel, 'btn_enter_{}'.format(i))
                btn.BindMethod('OnClick', lambda btn, touch, bid=i, aid=anim_idx + 1: self.on_click_btn_enter(bid, aid))
                anim_info = anim_info_list[anim_idx]
                unlock = pet_level >= anim_info.get('level', 1)
                getattr(self.panel, 'icon_enter_{}'.format(i)).SetDisplayFrameByPath('', ICON_ENTER_IMG[unlock])
                getattr(self.panel, 'pnl_btn_{}'.format(i)).SetDisplayFrameByPath('', PNL_BTN_IMG[unlock])
                getattr(self.panel, 'img_line_{}'.format(i)).SetDisplayFrameByPath('', IMG_LINE[unlock])
                lab_enter = getattr(self.panel, 'lab_enter_{}'.format(i))
                lab_enter.EnableOutline(LAB_OUTLINE[0], LAB_OUTLINE[1] if unlock else 0)
                getattr(self.panel, 'icon_lock_{}'.format(i)).setVisible(not unlock)

            anim_cnt = len(anim_info_list)
            show = anim_cnt > 1
            self.panel.btn_enter_1.setVisible(show)
            if show:
                init_btn(1, 0)
            show = anim_cnt in (1, 3)
            self.panel.btn_enter_2.setVisible(show)
            if show:
                init_btn(2, 0 if anim_cnt == 1 else 1)
            show = anim_cnt > 1
            self.panel.btn_enter_3.setVisible(show)
            if show:
                init_btn(3, 2 if anim_cnt == 3 else 1)
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
        if not self.pet_logic:
            self.unregister_update_pos_timer()
            return
        else:
            player_position = None
            if global_data.player and global_data.player.logic:
                player_position = global_data.player.logic.ev_g_position()
            else:
                if global_data.lobby_player:
                    player_position = global_data.lobby_player.ev_g_position()
                camera = world.get_active_scene().active_camera
                if not camera:
                    return
                cur_world_pos = self.pet_logic.ev_g_position()
                if not cur_world_pos:
                    return
                neox_2d_pos = camera.world_to_screen(cur_world_pos)
                cocos_2d_pos = neox_pos_to_cocos(*neox_2d_pos)
                self.panel.setPosition(*cocos_2d_pos)
                max_pos_z = 1.2
                max_dist = 15 * NEOX_UNIT_SCALE
                if not player_position:
                    return
            player_position.y = 0
            cur_world_pos.y = 0
            cur_dist = (cur_world_pos - player_position).length
            if cur_dist >= max_dist:
                pos_z = max_pos_z
            else:
                pos_z = max_pos_z * cur_dist / max_dist
            self.panel.setPositionZ(pos_z)
            return

    def on_click_btn_enter(self, btn_idx, anim_idx):
        if not self.pet_logic:
            return
        self.pet_logic.send_event('E_PLAY_INTERACT_ANIM', anim_idx)
        self.panel.PlayAnimation('click_0{}'.format(btn_idx))
        self.on_close()