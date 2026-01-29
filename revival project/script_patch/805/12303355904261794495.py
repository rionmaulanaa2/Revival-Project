# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/MechaModuleEffectiveUI.py
from __future__ import absolute_import
from six.moves import range
from common.uisys.basepanel import BasePanel
from common.const.uiconst import BASE_LAYER_ZORDER_1, UI_VKB_NO_EFFECT
from logic.gcommon.time_utility import get_server_time_battle
from logic.gutils import template_utils
from logic.gutils.mecha_module_utils import get_module_card_slot, get_module_card_name_and_desc
from logic.gcommon.common_const import mecha_const
from logic.gutils.template_utils import get_module_show_slot_pic
from common.uisys.BaseUIWidget import BaseUIWidget

class ModuleEffectiveInfo(object):

    def __init__(self, module_id, start_ts, duration, lv):
        self.module_id = module_id
        self.lv = lv
        self.set_time(start_ts, duration)

    def set_time(self, start_ts, duration):
        self.duration = duration
        if duration == -1:
            end_ts = -1
        else:
            end_ts = start_ts + duration
        self.end_ts = end_ts

    def update(self, other):
        self.lv = other.lv
        self.end_ts = other.end_ts
        self.duration = other.duration

    def __str__(self):
        return '<ModuleEffectiveInfo: %s, duration: %s, end_ts: %s>' % (self.module_id, self.duration, self.end_ts)

    __repr__ = __str__


class FightModuleTipsUI(BaseUIWidget):
    SLOT_TO_MODULE_TYPE = {mecha_const.MODULE_ATTACK_SLOT: 'atk',
       mecha_const.MODULE_DEFEND_SLOT: 'def',
       mecha_const.MODULE_MOVE_SLOT: 'spd',
       mecha_const.SP_MODULE_SLOT: 'sp'
       }

    def __init__(self, parent, panel):
        super(FightModuleTipsUI, self).__init__(parent, panel)
        self.panel.bar_module.img_core_num.setVisible(False)
        self.panel.lab_name.SetColor('#SW')

    def refresh_module_tip(self, card_id, slot_no, card_lv):
        module_icon_path = self.get_module_icon_path_by_slot_and_lv(slot_no, card_lv)
        self.panel.bar_module.SetDisplayFrameByPath('', module_icon_path)
        card_icon_path = get_module_show_slot_pic(slot_no, card_id, card_lv)
        self.panel.bar_module.img_module.SetDisplayFrameByPath('', card_icon_path)
        card_name_desc, card_effect_desc = get_module_card_name_and_desc(card_id, card_lv)
        self.panel.lab_name.SetString(card_name_desc)
        self.panel.lab_details.SetString(card_effect_desc)

    def get_module_icon_path_by_slot_and_lv(self, slot_no, card_lv):
        card_lv_str = card_lv
        if slot_no == mecha_const.SP_MODULE_SLOT:
            card_lv_str = 'gold'
        if card_lv is None:
            card_lv_str = 'empty'
        module_type = self.SLOT_TO_MODULE_TYPE[slot_no]
        return 'gui/ui_res_2/battle/mech_module/big_bar_module_{}_{}.png'.format(module_type, card_lv_str)


class MechaModuleEffectiveUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_mech/fight_module_buff'
    DLG_ZORDER = BASE_LAYER_ZORDER_1
    UI_VKB_TYPE = UI_VKB_NO_EFFECT
    GLOBAL_EVENT = {'battle_mecha_module_effective_change': '_on_battle_mecha_module_effective_change',
       'scene_camera_target_setted_event': '_on_set_scene_camera_target',
       'on_player_control_target_change': '_on_player_control_target_change',
       'net_reconnect_event': '_on_net_reconnect_event',
       'net_login_reconnect_event': '_on_net_login_reconnect_event'
       }
    SINGLE_MODULE_COUNT_DOWN_TAG = 31415926

    def on_init_panel(self):
        self._init_parameters()
        self._init_views()

    def on_finalize_panel(self):
        if self.mecha_tips_com_0:
            self.mecha_tips_com_0.destroy()
        self.mecha_tips_com_0 = None
        return

    def _init_parameters(self):
        self._module_effective_info_list = []
        self.SLOT_TO_BG_NAME = {mecha_const.MODULE_ATTACK_SLOT: 'atk',
           mecha_const.MODULE_DEFEND_SLOT: 'def',
           mecha_const.MODULE_MOVE_SLOT: 'spd',
           mecha_const.SP_MODULE_SLOT: 'sp'
           }
        self._showing_tips_info = None
        return

    def _init_views(self):
        self.panel.list_moudle_buff.SetInverse(True)
        panel_0 = global_data.uisystem.load_template_create('battle_mech/i_fight_module_tips', parent=self.panel, name='i_fight_module_tips')
        widget_0 = FightModuleTipsUI(self, panel_0)
        self.mecha_tips_com_0 = widget_0
        self.mecha_tips_com_0.hide()
        self._check_and_update(global_data.cam_lplayer)

    def _change_module_effective(self, effective_info, effective):
        if effective:
            for info in self._module_effective_info_list:
                if info.module_id == effective_info.module_id:
                    info.update(effective_info)
                    break
            else:
                self._module_effective_info_list.append(effective_info)

        else:
            deled = False
            if effective_info in self._module_effective_info_list:
                deled = True
            self._module_effective_info_list = [ info for info in self._module_effective_info_list if info.module_id != effective_info.module_id ]
            if deled:
                self._on_info_deled(effective_info)
        self._refresh_status_list()

    def _refresh_status_list(self):
        lst = self.panel.list_moudle_buff
        cnt = len(self._module_effective_info_list)
        lst.SetInitCount(cnt)
        for i in range(cnt):
            info = self._module_effective_info_list[i]
            item = lst.GetItem(i)
            card_id = info.module_id
            card_level = info.lv
            slot = get_module_card_slot(card_id)
            icon_path = get_module_show_slot_pic(slot, card_id, card_level)
            item.img_icon.SetDisplayFrameByPath('', icon_path)
            bg_path = self._get_module_bg_path(slot)
            item.pnl_buff_bg.SetDisplayFrameByPath('', bg_path)
            prog_path = self._get_module_progress_path(slot)
            item.progress_cover.SetProgressTexture(prog_path)
            if info.end_ts == -1:
                item.progress_cover.StopPercentageAni()
                item.progress_cover.SetPercent(0)
            else:
                left_time = info.end_ts - get_server_time_battle()
                left_time = max(0.0, left_time)
                pass_time = info.duration - left_time
                ratio = float(pass_time) / info.duration * 100
                item.progress_cover.StopPercentageAni()
                item.progress_cover.SetPercent(ratio)
                exec_flag = [
                 False]

                def cb(info=info, exec_flag=exec_flag):
                    if info in self._module_effective_info_list:
                        self._module_effective_info_list.remove(info)
                        self._on_info_deled(info)
                    self._refresh_status_list()
                    exec_flag[0] = True

                item.progress_cover.SetPercentageWithAni(100, left_time, end_cb=cb)
                if exec_flag[0]:
                    return

            @item.unique_callback()
            def OnBegin(btn, touch, info=info, slot=slot):
                wpos = touch.getLocation()
                self._show_tips(info, slot, wpos)

            @item.unique_callback()
            def OnEnd(btn, touch):
                self._hide_tips()

        if cnt == 0:
            self.add_hide_count('self_empty')
        else:
            self.add_show_count('self_empty')

    def _on_info_deled(self, info):
        if self._showing_tips_info:
            if self._showing_tips_info.module_id == info.module_id:
                self._hide_tips()

    def _show_tips(self, info, slot, click_wpos):
        if self.mecha_tips_com_0:
            self._showing_tips_info = info
            self.mecha_tips_com_0.refresh_module_tip(info.module_id, slot, info.lv)
            pos_node = self.mecha_tips_com_0.panel
            lpos = pos_node.getParent().convertToNodeSpace(click_wpos)
            MODULE_TIPS_OFFSET_X = 0
            MODULE_TIPS_OFFSET_Y = 95
            pos_node.SetPosition(lpos.x + MODULE_TIPS_OFFSET_X, lpos.y + MODULE_TIPS_OFFSET_Y)
            self.mecha_tips_com_0.show()

    def _hide_tips(self):
        if self.mecha_tips_com_0:
            self.mecha_tips_com_0.hide()
        self._showing_tips_info = None
        return

    def _get_module_bg_path(self, slot):
        name = self.SLOT_TO_BG_NAME.get(slot, 'atk')
        return 'gui/ui_res_2/battle/mech_module/bar_buff_%s.png' % name

    def _get_module_progress_path(self, slot):
        name = self.SLOT_TO_BG_NAME.get(slot, 'atk')
        return 'gui/ui_res_2/battle/mech_module/img_buff_%s_cover.png' % name

    def _on_battle_mecha_module_effective_change(self, module_id, lv, effective, start_ts, duration):
        info = ModuleEffectiveInfo(str(module_id), start_ts, duration, lv)
        self._change_module_effective(info, effective)

    def _on_set_scene_camera_target(self):
        self._check_and_update(global_data.cam_lplayer)

    def _on_player_control_target_change(self, *args, **kw):
        self._check_and_update(global_data.cam_lplayer)

    def _on_net_reconnect_event(self, *args, **kw):
        pass

    def _on_net_login_reconnect_event(self, *args, **kw):
        pass

    def _check_and_update(self, obj_lplayer):
        is_avatar = obj_lplayer and global_data.player and global_data.player.logic == obj_lplayer
        self._remove_all()
        if is_avatar:
            self._on_set_player_logic(obj_lplayer)

    def _on_set_player_logic(self, lp):
        mecha_l = None
        if lp.ev_g_in_mecha_only():
            mecha = lp.ev_g_control_target()
            if mecha and mecha.logic:
                mecha_l = mecha.logic
        if mecha_l:
            self._on_set_mecha_logic(mecha_l)
        return

    def _on_set_mecha_logic(self, mecha_l):
        self._remove_all()
        if mecha_l:
            data_dict = mecha_l.ev_g_mecha_module_effective_data_ro()
            for module_id in data_dict:
                card_lv, buff_params = data_dict[module_id]
                from logic.gcommon.component.client.ComMechaModuleBuff import ComMechaModuleBuff
                start_ts, duration_for_event = ComMechaModuleBuff.to_event_data(buff_params)
                self._on_battle_mecha_module_effective_change(module_id, card_lv, True, start_ts, duration_for_event)

    def _remove_all(self):
        del self._module_effective_info_list[:]
        self._hide_tips()
        self._refresh_status_list()