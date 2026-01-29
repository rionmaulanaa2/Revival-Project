# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/DrugUIPC.py
from __future__ import absolute_import
import six_ex
import six
from six.moves import range
import time
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, BG_ZORDER, UI_VKB_CUSTOM, UI_VKB_NO_EFFECT
from data.item_use_var import USABLE_ID_LIST, MECHA_USABLE_ID_LIST, THROW_ID_LIST
from logic.gutils import item_utils
import cc
import math
import game
from logic.gcommon.cdata.status_config import ST_USE_ITEM, ST_SKATE_MOVE, ST_SKATE, ST_JUMP_1
from logic.gcommon.cdata import mecha_status_config
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.utils.cocos_utils import neox_pos_to_cocos
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode
from logic.client.const import game_mode_const
from logic.gutils import pc_utils
from common.cfg import confmgr
from logic.comsys.effect import ui_effect
import nxapp
from logic.gutils.new_template_utils import is_human_mecha_item
import logic.gcommon.time_utility as tutil
import math
DURG_NODE_OFFSET_X = 10

class DrugWheelWidget(object):
    DRUG_ITEM_CNT = 12

    def __init__(self, nd_wheel):
        self.nd_wheel = nd_wheel
        self.item_ui_list = []
        self.cur_sel_btn = None
        self.cur_sel_item = None
        self.wheel_center = None
        self.init_wheel_center()
        self.list_id_to_drug_id_dict = {}
        self.drug_id_to_list_id_dict = {}
        self.init_item_ui_list()
        self.angle_list = []
        self.init_angle_list()
        self.sel_drug_id = None
        return

    def init_angle_list(self):
        per_item_angle = math.pi * 2 / self.DRUG_ITEM_CNT
        half_item_angle = per_item_angle / 2
        for idx in range(self.DRUG_ITEM_CNT):
            if idx == 0:
                angle_range = [
                 (
                  -half_item_angle, 0), (0, half_item_angle)]
            elif 0 < idx < self.DRUG_ITEM_CNT / 2:
                start_angle = half_item_angle + per_item_angle * (idx - 1)
                end_angle = start_angle + per_item_angle
                angle_range = [(start_angle, end_angle)]
            elif idx == self.DRUG_ITEM_CNT / 2:
                start_angle = half_item_angle + per_item_angle * (idx - 1)
                end_angle = math.pi
                angle_range = [(start_angle, end_angle), (-end_angle, -start_angle)]
            else:
                start_angle = half_item_angle + per_item_angle * (idx - 1) - math.pi * 2
                end_angle = start_angle + per_item_angle
                angle_range = [(start_angle, end_angle)]
            self.angle_list.append(angle_range)

    def init_item_ui_list(self, is_mecha=False):
        self.item_ui_list = []
        for idx in range(self.DRUG_ITEM_CNT):
            nd_item = getattr(self.nd_wheel, 'nd_item_%d' % (idx + 1))
            self.item_ui_list.append(nd_item)

        cur_map_id = global_data.game_mode.get_map_id()
        fixed_item_list = confmgr.get('item_by_mode', str(cur_map_id), 'cFixedItemList', default=[])
        all_item_list = fixed_item_list
        if is_mecha:
            throwable_item_list = confmgr.get('item_by_mode', str(cur_map_id), 'cThrowableItemList', default=[])
            all_item_list = fixed_item_list + throwable_item_list
        for idx, item_id in enumerate(all_item_list):
            if not 0 <= idx < len(self.item_ui_list):
                continue
            item_ui = self.item_ui_list[idx]
            pic_path = item_utils.get_item_pic_by_item_no(item_id)
            item_ui.item_sel.img.SetDisplayFrameByPath('', pic_path)
            item_ui.item_sel.lab.SetString('0')
            item_ui.item.img.SetDisplayFrameByPath('', pic_path)
            item_ui.item.lab.SetString('0')
            ui_effect.set_dark(item_ui.item_sel.img, True)
            ui_effect.set_dark(item_ui.item.img, True)
            item_ui.item_sel.setVisible(False)
            item_ui.item_sel.img.setVisible(False)
            item_ui.item_sel.lab.setVisible(False)
            item_ui.item.setVisible(True)
            item_ui.item.img.setVisible(True)
            item_ui.item.lab.setVisible(True)
            self.list_id_to_drug_id_dict[idx] = item_id
            self.drug_id_to_list_id_dict[item_id] = idx

    def reset_item_ui_list(self):
        for item in self.item_ui_list:
            item.btn_item.SetSelect(False)
            item.item_sel.setVisible(False)
            item.item_sel.img.setVisible(False)
            item.item_sel.lab.setVisible(False)
            item.item.setVisible(True)
            item.item.img.setVisible(False)
            item.item.lab.setVisible(False)

        self.nd_wheel.lab_item.SetString('')

    def select_item_ui(self, angle):
        list_id = self.cal_list_id_by_angle(angle)
        if list_id is None:
            return
        else:
            drug_id = self.list_id_to_drug_id_dict.get(list_id, -1)
            cur_sel_item = self.item_ui_list[list_id]
            drug_name = item_utils.get_item_name(drug_id)
            self.nd_wheel.lab_item.SetString(drug_name)
            if self.cur_sel_btn:
                self.cur_sel_btn.SetSelect(False)
            if self.cur_sel_item and self.sel_drug_id:
                self.cur_sel_item.btn_item.SetSelect(False)
                self.cur_sel_item.item_sel.setVisible(False)
                self.cur_sel_item.item_sel.img.setVisible(False)
                self.cur_sel_item.item_sel.lab.setVisible(False)
                self.cur_sel_item.item.setVisible(True)
                self.cur_sel_item.item.img.setVisible(self.sel_drug_id != -1)
                self.cur_sel_item.item.lab.setVisible(self.sel_drug_id != -1)
            self.sel_drug_id = drug_id
            if drug_id != -1:
                cur_sel_item.item_sel.setVisible(True)
                cur_sel_item.item_sel.img.setVisible(True)
                cur_sel_item.item_sel.lab.setVisible(True)
                cur_sel_item.item.setVisible(False)
                cur_sel_item.item.img.setVisible(False)
                cur_sel_item.item.lab.setVisible(False)
                cur_sel_item.btn_item.SetSelect(True)
                self.cur_sel_btn = cur_sel_item.btn_item
                self.cur_sel_item = cur_sel_item
            else:
                cur_sel_item.item_sel.setVisible(False)
                cur_sel_item.item_sel.img.setVisible(False)
                cur_sel_item.item_sel.lab.setVisible(False)
                cur_sel_item.item.setVisible(True)
                cur_sel_item.item.img.setVisible(False)
                cur_sel_item.item.lab.setVisible(False)
                cur_sel_item.btn_item.SetSelect(False)
                self.cur_sel_btn = cur_sel_item.btn_item
                self.cur_sel_item = cur_sel_item
            return

    def cal_list_id_by_angle(self, angle):
        for idx, angle_range_list in enumerate(self.angle_list):
            for angle_range in angle_range_list:
                if angle_range[0] <= angle < angle_range[1]:
                    return idx

    def populate_item_ui_list(self, drug_dict):
        drug_items = six_ex.items(drug_dict)
        for drug_id, count in drug_items:
            list_id = self.drug_id_to_list_id_dict.get(drug_id)
            if list_id is None:
                continue
            if list_id >= len(self.item_ui_list) or list_id < 0:
                return
            item_ui = self.item_ui_list[list_id]
            item_ui.item_sel.lab.SetString(str(count))
            item_ui.item.lab.SetString(str(count))
            dark = count == 0
            ui_effect.set_dark(item_ui.item_sel.img, dark)
            ui_effect.set_dark(item_ui.item.img, dark)
            item_ui.item_sel.setVisible(False)
            item_ui.item_sel.img.setVisible(False)
            item_ui.item_sel.lab.setVisible(False)
            item_ui.item.setVisible(True)
            item_ui.item.img.setVisible(True)
            item_ui.item.lab.setVisible(True)

        return

    def init_wheel_center(self):
        pos_x, pos_y = self.nd_wheel.nd_choose_mark.GetPosition()
        self.wheel_center = self.nd_wheel.ConvertToWorldSpace(pos_x, pos_y)

    def update_pointer(self, angle):
        self.nd_wheel.nd_select.setRotation(math.degrees(angle))

    def on_begin(self, drug_dict, is_mecha=False):
        self.init_item_ui_list(is_mecha)
        self.reset_item_ui_list()
        self.populate_item_ui_list(drug_dict)
        self.nd_wheel.setVisible(True)

    def on_drag(self, wpos):
        wpos = cc.Vec2(*neox_pos_to_cocos(wpos.x, wpos.y))
        wpos.subtract(self.wheel_center)
        angle = wpos.getAngle(cc.Vec2(0, 1))
        self.select_item_ui(angle)
        self.update_pointer(angle)

    def on_end(self):
        self.nd_wheel.setVisible(False)
        return self.sel_drug_id

    def hide_wheel(self):
        self.nd_wheel.setVisible(False)


class DrugWheelUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/i_fight_medicine_select_pc'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_NO_EFFECT
    HOT_KEY_FUNC_MAP = {'close_wheel_panel': 'mouse_close_wheel_panel'
       }
    HOT_KEY_FUNC_MAP_SHOW = {'open_drug_panel': {'node': 'nd_hint.nd_hint_1.temp_pc'},'close_wheel_panel': {'node': 'nd_hint.nd_hint_2.temp_pc'}}
    DRUG_ITEM_CNT = 17

    def on_init_panel(self, *args, **kwargs):
        self.nd_wheel = self.panel
        self.item_ui_list = []
        self.cur_sel_btn = None
        self.cur_sel_item = None
        self.wheel_center = None
        self.is_in_team = False
        self.init_wheel_center()
        self.list_id_to_drug_id_dict = {}
        self.drug_id_to_list_id_dict = {}
        self.init_item_ui_list()
        self.angle_list = []
        self.init_angle_list()
        self.sel_drug_id = None
        self.init_tips()
        self.hide_wheel()
        return

    def init_angle_list(self):
        per_item_angle = math.pi * 2 / self.DRUG_ITEM_CNT
        mid_item = self.DRUG_ITEM_CNT / 2
        for idx in range(self.DRUG_ITEM_CNT):
            idx -= 1
            if idx < 0:
                idx = self.DRUG_ITEM_CNT - 1
            if idx > mid_item:
                start_angle = per_item_angle * idx - math.pi * 2
                end_angle = start_angle + per_item_angle
                angle_range = [(start_angle, end_angle)]
            elif idx < mid_item:
                start_angle = per_item_angle * idx
                end_angle = start_angle + per_item_angle
                angle_range = [(start_angle, end_angle)]
            else:
                start_angle = mid_item * per_item_angle
                angle_range = [(start_angle, math.pi), (-math.pi, -start_angle)]
            self.angle_list.append(angle_range)

    def init_item_ui_list(self, is_mecha=False):
        self.item_ui_list = []
        for idx in range(self.DRUG_ITEM_CNT):
            nd_item = getattr(self.nd_wheel, 'nd_item_%d' % (idx + 1))
            nd_item.btn_item_empty.setVisible(False)
            self.item_ui_list.append(nd_item)

        cur_map_id = global_data.game_mode.get_map_id()
        fixed_item_list = confmgr.get('item_by_mode', str(cur_map_id), 'cFixedItemList', default=[])
        all_item_list = fixed_item_list
        for idx, item_id in enumerate(all_item_list):
            if not 0 <= idx < len(self.item_ui_list):
                continue
            item_ui = self.item_ui_list[idx]
            pic_path = item_utils.get_item_pic_by_item_no(item_id)
            item_ui.item_sel.img.SetDisplayFrameByPath('', pic_path)
            item_ui.item_sel.lab.SetString('0')
            item_ui.item.img.SetDisplayFrameByPath('', pic_path)
            item_ui.item.lab.SetString('0')
            ui_effect.set_dark(item_ui.item_sel.img, True)
            ui_effect.set_dark(item_ui.item.img, True)
            item_ui.item_sel.setVisible(False)
            item_ui.item_sel.img.setVisible(False)
            item_ui.item_sel.lab.setVisible(False)
            item_ui.item.setVisible(True)
            item_ui.item.img.setVisible(True)
            item_ui.item.lab.setVisible(True)
            self.list_id_to_drug_id_dict[idx] = item_id
            self.drug_id_to_list_id_dict[item_id] = idx

    def reset_item_ui_list(self):
        for item in self.item_ui_list:
            item.btn_item.SetSelect(False)
            item.item_sel.setVisible(False)
            item.item_sel.img.setVisible(False)
            item.item_sel.lab.setVisible(False)
            item.item.setVisible(True)
            item.item.img.setVisible(False)
            item.item.lab.setVisible(False)

        self.nd_wheel.lab_item.SetString('')

    def select_item_ui(self, angle):
        list_id = self.cal_list_id_by_angle(angle)
        if list_id is None:
            return
        else:
            drug_id = self.list_id_to_drug_id_dict.get(list_id, -1)
            cur_sel_item = self.item_ui_list[list_id]
            drug_name = item_utils.get_item_name(drug_id)
            self.nd_wheel.lab_item.SetString(drug_name)
            if self.cur_sel_btn:
                self.cur_sel_btn.SetSelect(False)
            if self.cur_sel_item and self.sel_drug_id:
                self.cur_sel_item.btn_item.SetSelect(False)
                self.cur_sel_item.item_sel.setVisible(False)
                self.cur_sel_item.item_sel.img.setVisible(False)
                self.cur_sel_item.item_sel.lab.setVisible(False)
                self.cur_sel_item.item.setVisible(True)
                self.cur_sel_item.item.img.setVisible(self.sel_drug_id != -1)
                self.cur_sel_item.item.lab.setVisible(self.sel_drug_id != -1)
                cur_sel_item_cnt = self.cur_sel_item.item_sel.lab.GetString()
                self.cur_sel_item.btn_item_empty.setVisible(self.sel_drug_id != -1 and cur_sel_item_cnt == '0')
            self.sel_drug_id = drug_id
            if drug_id != -1:
                cur_sel_item.item_sel.setVisible(True)
                cur_sel_item.item_sel.img.setVisible(True)
                cur_sel_item.item_sel.lab.setVisible(True)
                cur_sel_item.item.setVisible(False)
                cur_sel_item.item.img.setVisible(False)
                cur_sel_item.item.lab.setVisible(False)
                cur_sel_item.btn_item.SetSelect(True)
                cur_sel_item.btn_item_empty.setVisible(False)
                self.cur_sel_btn = cur_sel_item.btn_item
                self.cur_sel_item = cur_sel_item
            else:
                cur_sel_item.item_sel.setVisible(False)
                cur_sel_item.item_sel.img.setVisible(False)
                cur_sel_item.item_sel.lab.setVisible(False)
                cur_sel_item.item.setVisible(True)
                cur_sel_item.item.img.setVisible(False)
                cur_sel_item.item.lab.setVisible(False)
                cur_sel_item.btn_item.SetSelect(False)
                self.cur_sel_btn = cur_sel_item.btn_item
                self.cur_sel_item = cur_sel_item
            return

    def cal_list_id_by_angle(self, angle):
        for idx, angle_range_list in enumerate(self.angle_list):
            for angle_range in angle_range_list:
                if angle_range[0] <= angle < angle_range[1]:
                    return idx

    def populate_item_ui_list(self, drug_dict):
        drug_items = six_ex.items(drug_dict)
        for drug_id, count in drug_items:
            list_id = self.drug_id_to_list_id_dict.get(drug_id)
            if list_id is None:
                continue
            if list_id >= len(self.item_ui_list) or list_id < 0:
                return
            item_ui = self.item_ui_list[list_id]
            item_ui.item_sel.lab.SetString(str(count))
            item_ui.item.lab.SetString(str(count))
            if count == 0:
                item_ui.item_sel.lab.SetColor('#SR')
                item_ui.item.lab.SetColor('#SR')
            else:
                item_ui.item_sel.lab.SetColor('#SW')
                item_ui.item.lab.SetColor('#SW')
            dark = count == 0
            ui_effect.set_dark(item_ui.item_sel.img, dark)
            ui_effect.set_dark(item_ui.item.img, dark)
            item_ui.btn_item_empty.setVisible(dark)
            item_ui.item_sel.setVisible(False)
            item_ui.item_sel.img.setVisible(False)
            item_ui.item_sel.lab.setVisible(False)
            item_ui.item.setVisible(True)
            item_ui.item.img.setVisible(True)
            item_ui.item.lab.setVisible(True)

        return

    def init_wheel_center(self):
        pos_x, pos_y = self.nd_wheel.nd_choose_mark.GetPosition()
        self.wheel_center = self.nd_wheel.ConvertToWorldSpace(pos_x, pos_y)

    def update_pointer(self, angle):
        self.nd_wheel.nd_select.setRotation(math.degrees(angle))

    def on_begin(self, drug_dict, is_mecha=False):
        self.init_item_ui_list(is_mecha)
        self.reset_item_ui_list()
        self.populate_item_ui_list(drug_dict)
        self.nd_wheel.setVisible(True)

    def on_drag(self, wpos):
        wpos = cc.Vec2(*neox_pos_to_cocos(wpos.x, wpos.y))
        wpos.subtract(self.wheel_center)
        angle = wpos.getAngle(cc.Vec2(0, 1))
        self.select_item_ui(angle)
        self.update_pointer(angle)
        self.update_tips(self.sel_drug_id)

    def on_end(self):
        self.nd_wheel.setVisible(False)
        return self.sel_drug_id

    def hide_wheel(self):
        self.nd_wheel.setVisible(False)

    def mouse_close_wheel_panel(self, *args):
        self.close()

    def init_tips(self):
        self.is_in_team = global_data.player and global_data.player.is_in_team()
        tip_1 = self.nd_wheel.nd_hint.nd_hint_1.temp_pc.pc_tip_list.GetItem(0)
        tip_2 = self.nd_wheel.nd_hint.nd_hint_2.temp_pc.pc_tip_list.GetItem(0)
        if tip_1:
            tip_1.lab_hint1.SetString(get_text_by_id(920823))
        if tip_2:
            tip_2.lab_hint1.SetString(get_text_by_id(920824))
            tip_2.lab_pc.setVisible(True)
            tip_2.lab_pc.nd_auto_fit.setVisible(False)
            tip_2.lab_pc.SetString('')

    def update_tips(self, drug_id):
        tip_1 = self.nd_wheel.nd_hint.nd_hint_1.temp_pc.pc_tip_list.GetItem(0)
        tip_2 = self.nd_wheel.nd_hint.nd_hint_2.temp_pc.pc_tip_list.GetItem(0)
        if not tip_1 or not tip_2:
            self.nd_wheel.nd_hint.nd_hint_1.setVisible(False)
            self.nd_wheel.nd_hint.nd_hint_2.setVisible(False)
            return
        if drug_id == -1:
            self.nd_wheel.nd_hint.nd_hint_1.setVisible(False)
            self.nd_wheel.nd_hint.nd_hint_2.setVisible(True)
            return
        if not global_data.cam_lplayer:
            return
        count = global_data.cam_lplayer.ev_g_item_count(drug_id)
        if count > 0:
            tip_1.lab_hint2.SetString(get_text_by_id(80338))
            self.nd_wheel.nd_hint.nd_hint_1.setVisible(True)
            self.nd_wheel.nd_hint.nd_hint_2.setVisible(True)
            tip_2.lab_pc.setVisible(True)
            tip_2.lab_pc.nd_auto_fit.setVisible(False)
            tip_2.lab_pc.SetString('')
        else:
            if self.is_in_team:
                tip_1.lab_hint2.SetString(get_text_by_id(19744))
                self.nd_wheel.nd_hint.nd_hint_1.setVisible(True)
            else:
                self.nd_wheel.nd_hint.nd_hint_1.setVisible(False)
            self.nd_wheel.nd_hint.nd_hint_2.setVisible(True)
            tip_2.lab_pc.setVisible(True)
            tip_2.lab_pc.nd_auto_fit.setVisible(False)
            tip_2.lab_pc.SetString('')

    def on_hot_key_closed_state(self):
        pass


class DrugUIPC(BasePanel):
    PANEL_CONFIG_NAME = 'battle/fight_medicine_pc'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_ACTION_EVENT = {'bg_layer.OnBegin': 'on_begin_bg_layer'
       }
    IS_PLAY_OPEN_SOUND = False
    UI_VKB_TYPE = UI_VKB_CUSTOM
    HOT_KEY_FUNC_MAP = {'open_drug_panel.DOWN_UP': 'keyboard_open_drug_wheel'
       }
    HOT_KEY_FUNC_MAP_SHOW = {'open_drug_panel': {'node': 'medicine_button.btn_more.nd_hint_open.temp_pc'},'use_cur_item': {'node': 'medicine_button.temp_pc'}}
    GLOBAL_EVENT = {'improvise_highlight_on_time': '_on_play_improvise_highlight_ui_efx'
       }
    DELAY_IMPROVISE_HIGHLIGHT_ALL_DONE_TAG = 31415926
    DELAY_IMPROVISE_HIGHLIGHT_PLAY_LOOP_TAG = 31415927
    SEND_CD = 5.0

    def on_init_panel(self):
        self._cur_shot_cut = None
        self._mecha_state = False
        self.cur_drug_button = self.panel.medicine_button
        self.cur_drug_data = None
        self.in_using_drug = None
        self.tmp_drug_data_dict = {}
        self.usable_item_id_list = USABLE_ID_LIST
        self._is_on_changed_player_or_state = False
        self.player = None
        self.listen_obj = None
        self.next_tip_time = 0
        self._last_send_time = 0
        self.init_custom_com()
        self.add_hide_count(self.__class__.__name__)
        global_data.emgr.scene_camera_target_setted_event += self.on_player_setted
        global_data.emgr.update_item_lost_time += self._update_item_lost_time
        self.on_player_setted()
        ui = DrugWheelUI()
        ui.hide()
        self.panel.RecordAnimationNodeState('renovate')
        self.panel.RecordAnimationNodeState('renovate_loop')
        self.init_drug_btn()
        self._mouse_listener = None
        self._init_panel_pos_x = self.panel.left.GetPosition()[0]
        self.hide_btn_more()
        return

    def init_custom_com(self):
        from logic.comsys.setting_ui.CustomUIProxy import init_custom_com
        init_custom_com(self, {})

    def on_player_setted(self):
        player = global_data.cam_lplayer
        self.unbind_player()
        if player:
            is_player_changed = self.player == player
            self.player = player
            control_target = self.player.ev_g_control_target()
            mecha_trans_state = control_target and control_target.logic and control_target.logic.ev_g_is_mechatran()
            if control_target and control_target.logic.sd.ref_is_mecha and not mecha_trans_state:
                mecha_state = True
                self.usable_item_id_list = MECHA_USABLE_ID_LIST
            else:
                mecha_state = False
                self.usable_item_id_list = USABLE_ID_LIST + THROW_ID_LIST
            is_mecha_stated_changed = mecha_state != self._mecha_state
            self._is_on_changed_player_or_state = is_player_changed or is_mecha_stated_changed
            self._mecha_state = mecha_state
            self.on_change_state(mecha_state is True)
            self.add_show_count(self.__class__.__name__)
            self.bind_drug_event(player)
            self.init_drug_event()
            if global_data.player and global_data.player.in_local_battle():
                self.in_using_drug = None
        else:
            self.player = None
            self._is_on_changed_player_or_state = False
        if self.player and global_data.player and global_data.player.logic:
            if self.player.id != global_data.player.logic.id:
                self.on_switch_off_hot_key()
        return

    def on_resolution_changed(self):
        node_offset_x = DURG_NODE_OFFSET_X if self._mecha_state else 0
        self.panel.left.SetPosition(self._init_panel_pos_x + node_offset_x, self.panel.left.GetPosition()[1])

    def unbind_player(self):
        self.listen_hp_change(0)
        if self.player and self.player.is_valid():
            self.unbind_drug_event(self.player)
        self.player = None
        return

    def init_drug_event(self):
        self.update_shortcut()

    def update_shortcut(self, *args):
        cur_shot_cut_id = self.player.ev_g_show_shortcut()
        item_count = self.player.ev_g_item_count(cur_shot_cut_id) if cur_shot_cut_id else 0
        cur_shot_cut = (cur_shot_cut_id, item_count)
        if cur_shot_cut != self._cur_shot_cut or self._is_on_changed_player_or_state:
            self.on_drug_shortcut_changed(cur_shot_cut_id)
            self.update_temp_drug_data()
            self._cur_shot_cut = (cur_shot_cut, item_count)

    def init_drug_btn(self):

        @self.panel.medicine_button.unique_callback()
        def OnClick(btn, touch):
            if not self._can_interact():
                return
            drug_id = self.cur_drug_data.get('item_id')
            self.try_use_medicine(drug_id)

        @self.panel.medicine_button.btn_more.unique_callback()
        def OnBegin(btn, touch):
            self._register_mouse_event()
            self.button_open_drug_wheel()

        @self.panel.medicine_button.btn_more.unique_callback()
        def OnEnd(btn, touch):
            self._unregister_mouse_event()
            self.button_close_drug_wheel()

    def update_temp_drug_data(self):
        self.drug_data_dict = self.get_drug_data()
        self.tmp_drug_data_dict = dict(self.drug_data_dict)

    def on_drug_shortcut_changed(self, item_id, *args):
        if item_id:
            item_count = self.player.ev_g_item_count(item_id)
            self.set_quick_drug_item({'item_id': item_id,'num': item_count})
        else:
            self.cur_drug_data = None
        self.listen_hp_change(item_id)
        visible = self.cur_drug_data and self.cur_drug_data.get('item_id') in self.usable_item_id_list
        self.cur_drug_button.setVisible(bool(visible))
        return

    def on_item_data_changed(self, item_data):
        need_refresh = False
        if item_data is None:
            need_refresh = True
        elif item_data['item_id'] in self.usable_item_id_list:
            need_refresh = True
            drug_data = self.tmp_drug_data_dict
            item_id = item_data['item_id']
            pic_path = item_utils.get_item_pic_by_item_no(item_id)
            if item_id in drug_data and drug_data[item_id] < item_data.get('count', 0) and item_id not in THROW_ID_LIST:
                self.panel.vx_item.SetDisplayFrameByPath('', pic_path)
                self.panel.PlayAnimation('get_tools')
        if need_refresh:
            self.update_temp_drug_data()
            if self.cur_drug_data and item_data['item_id'] == self.cur_drug_data.get('item_id'):
                self.on_drug_shortcut_changed(self.cur_drug_data.get('item_id'))
        drug_type_cnt = 0
        if self.tmp_drug_data_dict:
            for drug_cnt in six.itervalues(self.tmp_drug_data_dict):
                if drug_cnt > 0:
                    drug_type_cnt += 1

        self.panel.medicine_button.btn_more.setVisible(drug_type_cnt > 1)
        return

    def set_quick_drug_item(self, drug_data):
        item_no = drug_data.get('item_id')
        num = drug_data.get('num', 0)
        self.cur_drug_data = {'item_id': item_no,'num': num}
        pic_path = item_utils.get_item_pic_by_item_no(item_no)
        self.cur_drug_button.sp_cur_drug.SetDisplayFrameByPath('', pic_path)
        from logic.gcommon.item.item_utility import is_mecha_battery
        if not self.player or not self.player.ev_g_ctrl_mecha() and is_mecha_battery(item_no) and not is_human_mecha_item(item_no):
            self.cur_drug_button.sp_cur_drug.SetColor('#DH')
        else:
            self.cur_drug_button.sp_cur_drug.SetColor('#SW')
        self.cur_drug_button.quantity.setString(str(num))

    def on_change_state(self, mecha_state=True):
        self.panel.pnl_mecha.setVisible(mecha_state)
        self.panel.pnl_human.setVisible(not mecha_state)
        if not mecha_state:
            hint_pic = 'gui/ui_res_2/battle/button/frame_tools_sel.png'
            node_offset_x = 0
        else:
            hint_pic = 'gui/ui_res_2_pc/battle/mech_main/pnl_mech_vx_pc.png'
            node_offset_x = DURG_NODE_OFFSET_X
        self.panel.img_hint.SetDisplayFrameByPath('', hint_pic)
        self.panel.img_hint2.SetDisplayFrameByPath('', hint_pic)
        self.panel.vx_hint.SetDisplayFrameByPath('', hint_pic)
        self.panel.left.SetPosition(self._init_panel_pos_x + node_offset_x, self.panel.left.GetPosition()[1])
        item_id = self.cur_drug_data or 0 if 1 else self.cur_drug_data.get('item_id', 0)
        self.listen_hp_change(item_id)

    def listen_hp_change(self, item_id):
        new_listen_obj = None
        if item_id in (1612, ):
            new_listen_obj = self.player
        elif item_id in (9902, 9904):
            if self.player:
                control_target = self.player.ev_g_control_target()
                if control_target.__class__.__name__ == 'Mecha':
                    new_listen_obj = control_target.logic
        if new_listen_obj == self.listen_obj:
            return
        else:
            if self.listen_obj:
                self.listen_obj.unregist_event('E_HEALTH_HP_CHANGE', self.on_hp_changed)
                self.panel.StopAnimation('hint')
                self.panel.img_hint.setVisible(False)
            self.listen_obj = new_listen_obj
            if self.listen_obj:
                self.listen_obj.regist_event('E_HEALTH_HP_CHANGE', self.on_hp_changed)
                self.on_hp_changed()
            return

    def on_hp_changed(self, hp=0, mod=0):
        if not self.listen_obj:
            return
        percent = self.listen_obj.ev_g_health_percent()
        if percent > 0.4:
            self.panel.StopAnimation('hint')
            self.panel.img_hint.setVisible(False)
        else:
            if not self.panel.IsPlayingAnimation('hint'):
                self.panel.PlayAnimation('hint')
                self.panel.img_hint.vx_hint.SetPosition('50%', '50%')
            if mod <= 0 and time.time() > self.next_tip_time:
                self.next_tip_time = time.time() + 10
                global_data.emgr.play_tips_voice.emit('tips_05')

    def get_drug_data(self):
        medical_ids = {}
        for did in self.usable_item_id_list:
            medical_ids[did] = 0

        if self.player:
            for mid in six.iterkeys(medical_ids):
                count = self.player.ev_g_item_count(mid)
                medical_ids[mid] = count

        return medical_ids

    def set_drug_shortcut(self, drug_item_id):
        if drug_item_id is not None and self.player and self.player.is_valid():
            if self.cur_drug_data is not None:
                self.player.send_event('E_SET_SHOW_SHORTCUT', drug_item_id)
        return

    def on_finalize_panel(self):
        super(DrugUIPC, self).on_finalize_panel()
        self.unbind_player()
        self.destroy_widget('custom_ui_com')

    def bind_drug_event(self, target):
        target.regist_event('E_SET_SHOW_SHORTCUT', self.update_shortcut, 10)
        target.regist_event('E_ITEM_DATA_CHANGED', self.on_item_data_changed)
        target.regist_event('E_SHOW_USE_PROGRESS', self.on_item_use_progress)
        target.regist_event('E_ITEMUSE_CANCEL_RES', self.on_item_use_cancel)
        target.regist_event('E_ITEMUSE_ON', self.on_item_used)
        target.regist_event('E_FIGHT_STATE_CHANGED', self.on_change_state)

    def unbind_drug_event(self, target):
        if target.unregist_event:
            target.unregist_event('E_SET_SHOW_SHORTCUT', self.update_shortcut)
            target.unregist_event('E_ITEM_DATA_CHANGED', self.on_item_data_changed)
            target.unregist_event('E_SHOW_USE_PROGRESS', self.on_item_use_progress)
            target.unregist_event('E_ITEMUSE_CANCEL_RES', self.on_item_use_cancel)
            target.unregist_event('E_ITEMUSE_ON', self.on_item_used)
            target.unregist_event('E_FIGHT_STATE_CHANGED', self.on_change_state)

    def on_item_use_progress(self, item_id, *arg):
        from logic.gutils.item_utils import is_food_item, is_health_item
        from logic.gcommon.item import item_utility
        if not is_health_item(item_id) and not is_food_item(item_id) and not item_utility.is_mecha_battery(item_id) and not item_utility.is_summon_item(item_id) and not item_utility.is_charger_item(item_id):
            return
        self.in_using_drug = item_id
        item_count = self.player.ev_g_item_count(item_id)
        self.set_quick_drug_item({'item_id': item_id,'num': item_count})

    def on_item_use_cancel(self, item_id=None):
        self.in_using_drug = None
        if not self.player:
            return
        else:
            self.update_shortcut()
            return

    def on_item_used(self, item_id, item_cd=None, item_limit=None):
        self.on_item_use_cancel(item_id)

    def _can_interact(self):
        if not global_data.player or not global_data.player.logic:
            return False
        if not self.player:
            return False
        return global_data.player.logic.id == self.player.id

    def keyboard_use_cur_item(self):
        if not self.cur_drug_data:
            return
        drug_id = self.cur_drug_data.get('item_id')
        self.try_use_medicine(drug_id)

    def try_use_medicine(self, drug_item_id):
        if not self.player:
            return
        if not self._can_interact():
            return
        if not self.player.ev_g_status_check_pass(ST_USE_ITEM):
            if self.player.ev_g_get_state(ST_SKATE_MOVE):
                self.player.send_event('E_TRY_STOP_SKATE')
            return
        control_target = self.player.ev_g_control_target()
        if control_target:
            target_type = control_target.logic.__class__.__name__
            if target_type == 'LMecha':
                if not control_target.logic.ev_g_status_check_pass(mecha_status_config.MC_USE_ITEM):
                    return
            elif target_type == 'LMechaTrans':
                if control_target.logic.ev_g_shape_shift() and not control_target.logic.ev_g_status_check_pass(mecha_status_config.MC_USE_ITEM):
                    return
        if self.in_using_drug and drug_item_id == self.in_using_drug:
            return
        if self.in_using_drug:
            self.player.send_event('E_ITEMUSE_CANCEL', self.in_using_drug)
        elif drug_item_id:
            count = self.player.ev_g_item_count(drug_item_id)
            if count <= 0:
                self.send_needed_drug_msg(drug_item_id)
                return
            from logic.gcommon.item import item_utility
            if item_utility.is_mecha_battery(drug_item_id) and not is_human_mecha_item(drug_item_id):
                mecha = self.player.ev_g_ctrl_mecha()
                if not mecha:
                    self.player.send_event('E_SHOW_MESSAGE', get_text_by_id(19055))
                    return
            if item_utility.is_summon_item(drug_item_id):
                if self.player.ev_g_is_in_any_state((ST_JUMP_1,)):
                    return
                if not self.player.ev_g_control_human() or self.player.ev_g_get_state(ST_SKATE) and not item_utility.is_mechatran_card(drug_item_id):
                    self.player.send_event('E_SHOW_MESSAGE', get_text_by_id(19055))
                    return
            if item_utility.is_charger_item(drug_item_id):
                if self.player.ev_g_in_mecha('Mecha'):
                    self.player.send_event('E_SHOW_MESSAGE', get_text_by_id(18196))
                    return
            if item_utility.is_mechatran_card(drug_item_id):
                import world
                pos = self.player.ev_g_position()
                scn = world.get_active_scene()
                exclude_ids = self.player.ev_g_human_col_id()
                is_valid = False
                if scn and pos:
                    is_valid, pos = item_utils.check_use_mechatran_card_valid(scn, pos, exclude_ids)
                if not is_valid:
                    self.player.send_event('E_SHOW_MESSAGE', get_text_by_id(18225))
                    return
            if drug_item_id == 9956 and not global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_ASSAULT):
                if not global_data.magic_sur_battle_mgr.applied_magic_rune_id:
                    global_data.ui_mgr.show_ui('MagicRuneListUI', 'logic.comsys.battle.Magic')
                else:
                    from logic.gcommon.common_const.battle_const import MAGIC_USE_RUNE, MAIN_NODE_COMMON_INFO
                    message = {'i_type': MAGIC_USE_RUNE,'content_txt': get_text_by_id(17547)}
                    message_type = MAIN_NODE_COMMON_INFO
                    global_data.emgr.show_battle_main_message.emit(message, message_type, True, False)
                return
            self.player.send_event('E_CTRL_USE_DRUG', drug_item_id)
            self.player.send_event('E_ITEMUSE_TRY', drug_item_id)

    def _register_mouse_event(self):
        if self._mouse_listener:
            return
        self._mouse_listener = cc.EventListenerMouse.create()
        self._mouse_listener.setOnMouseMoveCallback(self._on_mouse_move)
        cc.Director.getInstance().getEventDispatcher().addEventListenerWithSceneGraphPriority(self._mouse_listener, self.panel.get())

    def _unregister_mouse_event(self):
        if self._mouse_listener:
            cc.Director.getInstance().getEventDispatcher().removeEventListener(self._mouse_listener)
            self._mouse_listener = None
        return

    def _on_mouse_move(self, event):
        pos = event.getLocationInView()
        ui = global_data.ui_mgr.get_ui('DrugWheelUI')
        if ui:
            ui.on_drag(pos)

    def keyboard_open_drug_wheel(self, msg, keycode):
        if not self._can_interact():
            return
        if not self.can_show_drug_wheel():
            return
        pc_op_mode = pc_utils.is_pc_control_enable()
        if msg in [game.MSG_KEY_DOWN, game.MSG_MOUSE_DOWN]:
            if global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_CONCERT,)):
                if global_data.player and global_data.player.logic and global_data.player.logic.ev_g_in_mecha('Mecha'):
                    return
            self.do_open_drug_wheel()
            if pc_op_mode:
                global_data.mouse_mgr.set_cursor_move_enable(True)
                nxapp.clip_cursor(True)
            self._register_mouse_event()
        else:
            self.do_close_drug_wheel()
            if pc_op_mode:
                global_data.mouse_mgr.set_cursor_move_enable(False)
                nxapp.clip_cursor(False)
            self._unregister_mouse_event()
            self.unregister_mouse_scroll_event()

    def keyboard_close_drug_wheel(self):
        pc_op_mode = pc_utils.is_pc_control_enable()
        from logic.vscene.parts.ctrl.InputMockHelper import trigger_ui_btn_event
        trigger_ui_btn_event(self.__class__.__name__, 'medicine_button', 'OnEnd')
        if pc_op_mode:
            global_data.mouse_mgr.set_cursor_move_enable(False)
        self.unregister_mouse_scroll_event()
        self._unregister_mouse_event()

    def button_open_drug_wheel(self):
        if not self.can_show_drug_wheel():
            return
        self.do_open_drug_wheel()

    def button_close_drug_wheel(self):
        self.do_close_drug_wheel()

    def do_open_drug_wheel(self):
        ui = global_data.ui_mgr.get_ui('DrugWheelUI')
        if ui:
            ui.on_begin(self.get_drug_data())
            ui.show()
        else:
            ui = DrugWheelUI()
            ui.on_begin(self.get_drug_data())
            ui.show()

    def do_close_drug_wheel(self):
        ui = global_data.ui_mgr.get_ui('DrugWheelUI')
        if ui:
            drug_id = ui.on_end()
            ui.hide()
            if not self._can_interact():
                return
            self.try_use_medicine(drug_id)

    def can_show_drug_wheel(self):
        cur_map_id = global_data.game_mode.get_map_id()
        fixed_item_list = confmgr.get('item_by_mode', str(cur_map_id), 'cFixedItemList', default=[])
        return len(fixed_item_list) > 1

    def send_needed_drug_msg(self, drug_id):
        if global_data.player and not global_data.player.is_in_team():
            return
        drug_name = item_utils.get_item_name(drug_id)
        if not drug_name:
            return
        if not self.check_can_send():
            return
        if not self.player:
            return
        msg_text = get_text_by_id(19743).format(drug_name)
        self._last_send_time = time.time()
        self.player.send_event('E_SEND_BATTLE_GROUP_MSG', {'text': msg_text,'is_self_send': True}, True)

    def check_can_send(self):
        import math
        passed_time = time.time() - self._last_send_time
        if passed_time < self.SEND_CD:
            global_data.game_mgr.show_tip(get_text_by_id(11008, {'time': str(int(math.ceil(self.SEND_CD - passed_time)))}))
            return False
        return True

    def on_hot_key_opened_state(self):
        if self.player and global_data.player and global_data.player.logic:
            if self.player.id != global_data.player.logic.id:
                return
        super(DrugUIPC, self).on_hot_key_opened_state()

    @execute_by_mode(True, game_mode_const.Hide_DrugUIPCMoreBtn)
    def hide_btn_more(self):
        self.panel.medicine_button.btn_more.setVisible(False)
        self.panel.medicine_button.btn_more.SetEnable(False)

    def _stop_all_improvise_highlight_ui_efx(self):
        if not self.panel.HasAnimation('renovate') or not self.panel.HasAnimation('renovate_loop'):
            return
        self.panel.StopAnimation('renovate')
        self.panel.StopAnimation('renovate_loop')
        self.panel.RecoverAnimationNodeState('renovate')
        self.panel.RecoverAnimationNodeState('renovate_loop')

    def _on_play_improvise_highlight_ui_efx(self, left_ready_time):
        if not self.panel.HasAnimation('renovate') or not self.panel.HasAnimation('renovate_loop'):
            return
        self.panel.stopActionByTag(self.DELAY_IMPROVISE_HIGHLIGHT_ALL_DONE_TAG)
        self.panel.stopActionByTag(self.DELAY_IMPROVISE_HIGHLIGHT_PLAY_LOOP_TAG)
        self._stop_all_improvise_highlight_ui_efx()
        self.panel.PlayAnimation('renovate')
        renovate_time = self.panel.GetAnimationMaxRunTime('renovate')
        if renovate_time > 0 and renovate_time < left_ready_time:

            def continue_play_loop_cb():
                self.panel.StopAnimation('renovate')
                self.panel.PlayAnimation('renovate_loop')

            self.panel.DelayCallWithTag(renovate_time, continue_play_loop_cb, self.DELAY_IMPROVISE_HIGHLIGHT_PLAY_LOOP_TAG)

        def all_done_cb():
            self._stop_all_improvise_highlight_ui_efx()

        self.panel.DelayCallWithTag(left_ready_time, all_done_cb, self.DELAY_IMPROVISE_HIGHLIGHT_ALL_DONE_TAG)

    def _update_item_lost_time(self):
        if global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_RANDOM_DEATH):
            item_lost_time = global_data.death_battle_data.get_item_lost_time()
            delay_time = item_lost_time - int(tutil.get_time())
            if delay_time > 0:
                self.on_time_conut(delay_time)

    def on_time_conut(self, delay_time):

        def refresh_time_finsh():
            text = '{}s'.format(str(0))
            self.panel.lab_rest_time.SetString(text)
            self.panel.lab_rest_time.setVisible(False)

        def refresh_time(pass_time):
            left_time = int(math.ceil(delay_time - pass_time))
            text = '{}s'.format(str(left_time))
            self.panel.lab_rest_time.SetString(text)
            if left_time <= 0:
                self.panel.lab_rest_time.StopTimerAction()
                refresh_time_finsh()
                return

        self.panel.lab_rest_time.StopTimerAction()
        if delay_time <= 0:
            refresh_time_finsh()
            return
        refresh_time(0)
        self.panel.lab_rest_time.setVisible(True)
        self.panel.lab_rest_time.TimerAction(refresh_time, delay_time, interval=0.1)