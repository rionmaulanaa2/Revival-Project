# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_display/MechaBasicSkinWidget.py
from __future__ import absolute_import
import six
import six_ex
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.cfg import confmgr
from logic.comsys.common_ui.ScaleableHorzContainer import ScaleableHorzContainer
from logic.gutils import mecha_skin_utils
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no
from common.uisys.BaseUIWidget import BaseUIWidget
import cc
from logic.gutils import dress_utils
from logic.gutils.dress_utils import battle_id_to_mecha_lobby_id, mecha_lobby_id_2_battle_id
from logic.gutils import item_utils
from logic.gutils.template_utils import show_remain_time, init_skin_tags, init_mecha_buy_btn
from logic.client.const import mall_const
from logic.gcommon.item.item_const import FASHION_POS_SUIT, FASHION_POS_WEAPON_SFX, RARE_DEGREE_5, RARE_DEGREE_4, RARE_DEGREE_7
from logic.comsys.mall_ui.BuyConfirmUIInterface import role_or_skin_buy_confirmUI
from logic.comsys.ui_distortor.UIDistortHelper import DistortScaleCalculator, linear_inter
import math
from logic.gutils.CameraHelper import normalize_angle
import game3d
import math3d
from logic.gutils.CameraHelper import get_reverse_rotation
from logic.gutils import skin_define_utils
from logic.gutils import red_point_utils
from .SkinDefineUI import SkinDefineUI
from common.platform.dctool import interface
from logic.gutils.mecha_utils import get_ex_skin_improve_item_no, set_mecha_honour_view
CARD_SS_FRAME_TEMPLATE = 'role_profile/i_card_skin_frame_ss'

class SSCardsEffect(object):

    def __init__(self, panel, example_nd, panel_scale):
        self.init_gyro_effect()
        self._ss_card_items = []
        self.panel = panel
        self.example_nd = example_nd
        self._stop_rotate = False
        self.panel_scale = panel_scale
        self.create_gyro_effect()

    def destroy(self):
        self.release_ss_card_items()
        self.example_nd = None
        self.stop_gyro_effect()
        self.destroy_gyro_effect()
        self._slerp_act_func = None
        if self._scaleCalculator:
            self._scaleCalculator = None
        return

    def update_ss_card_list(self, cards_items):
        self.release_ss_card_items()
        self._ss_card_items = cards_items
        self._ss_card_acts = []
        self._ss_card_nodes = []
        for card in self._ss_card_items:
            card_acts = []
            card_acts.extend(card.PlayAnimation('shake'))
            act_nds = card.GetAnimationNodes('shake')
            if hasattr(card.nd_frame_ss, 'temp_ss_frame'):
                extra_temp = card.nd_frame_ss.temp_ss_frame
                if extra_temp:
                    card_acts.extend(extra_temp.PlayAnimation('shake'))
                    temp_act_nds = extra_temp.GetAnimationNodes('shake')
                    act_nds.extend(temp_act_nds)
            self._ss_card_acts.append(card_acts)
            self._ss_card_nodes.append(act_nds)
            for act_nd in act_nds:
                act_nd.getActionManager().pauseTarget(act_nd.get())

        if len(self._ss_card_items) > 0:
            any_card = self._ss_card_items[0]
            self._shake_max_time = any_card.GetAnimationMaxRunTime('shake')

    def init_gyro_effect(self):
        self.gyro_com = None
        self._ss_card_ids = []
        self._ss_card_items = []
        self._ss_card_acts = []
        self._ss_card_nodes = []
        self._max_rot_angle = 20
        self._scaleCalculator = None
        self._shake_max_time = 3
        self._start_rotation = None
        self._start_rotation_reverse = None
        self._rotation_flag = None
        self.set_rotate_range((0, 0), (-20, 15))
        self._slerp_act_func = None
        return

    def release_ss_card_items(self):
        for nd in self._ss_card_items:
            nd.nd_rot.setRotation3D(cc.Vec3(0, 0, 0))
            nd.nd_rot.setScale(1)
            nd.img_skin.setPositionZ(0)
            nd.img_skin_0.setPositionZ(0)
            nd.img_bar.setPositionZ(0)
            nd.FastForwardToAnimationTime('shake', 0.001)
            nd.StopAnimation('shake')

        for act_nds in self._ss_card_nodes:
            for act_nd in act_nds:
                act_nd.getActionManager().resumeTarget(act_nd.get())

        for card in self._ss_card_items:
            if hasattr(card.nd_frame_ss, 'temp_ss_frame'):
                extra_temp = card.nd_frame_ss.temp_ss_frame
                if extra_temp:
                    extra_temp.StopAnimation('shake')

        self._ss_card_items = []
        self._ss_card_acts = []
        self._ss_card_nodes = []

    def create_gyro_effect(self):
        from logic.comsys.common_ui.GyroscopeComponent import GyroscopeComponent
        if not self.gyro_com:
            self.gyro_com = GyroscopeComponent(self.panel.nd_skin_choose)
            self.gyro_com.set_args({'gryo_update_cb': self.gyro_callback,'interval': 0.033})

    def destroy_gyro_effect(self):
        if self.gyro_com:
            self.gyro_com.destroy()
            self.gyro_com = None
        return

    def start_gyro_effect(self):
        if self.gyro_com:
            self.gyro_com.set_gyroscope_enable(True)
            self._start_rotation = None
            if game3d.get_platform() == game3d.PLATFORM_WIN32:
                self._start_rotation = math3d.rotation(0, 0, 0, 1)
                self._start_rotation_reverse = get_reverse_rotation(self._start_rotation)
        return

    def stop_gyro_effect(self):
        if self.gyro_com:
            self.gyro_com.set_gyroscope_enable(False)
            self._start_rotation = None
        return

    def gyro_callback(self, smooth_rotate_speed, raw_gyro_vector, rotation_flag):
        if global_data.is_pc_mode:
            return
        else:
            if self._rotation_flag != rotation_flag:
                self._start_rotation = None
                if self._rotation_flag is not None:
                    self._stop_rotate = True

                    def clear_stop():
                        self._stop_rotate = False

                    self.panel.SetTimeOut(2.0, clear_stop, tag=200811)
                self._rotation_flag = rotation_flag
            if self._stop_rotate:
                return
            if self._start_rotation is None:
                if raw_gyro_vector.x != 0 and raw_gyro_vector.y != 0 and raw_gyro_vector.z != 0:
                    self._start_rotation = raw_gyro_vector
                    self._start_rotation_reverse = get_reverse_rotation(self._start_rotation)
                    return
            else:
                diff_gyro_vector = math3d.rotation_to_euler(self._start_rotation_reverse * raw_gyro_vector)
                x_val = normalize_angle(diff_gyro_vector.x) / 2.0 * self._rotation_flag
                y_val = normalize_angle(diff_gyro_vector.y) / 2.0
                if x_val > 0:
                    diff_gyro_vector.x = self.process_slerp_act(x_val, 0, math.pi / 2.0)
                else:
                    diff_gyro_vector.x = self.process_slerp_act(x_val, -math.pi / 2.0, 0)
                x_rot = max(min(diff_gyro_vector.y * 180 / math.pi, self._x_rot_max), self._x_rot_min)
                y_rot = max(min(diff_gyro_vector.x * 180 / math.pi, self._y_rot_max), self._y_rot_min)
                for ind, nd in enumerate(self._ss_card_items):
                    self.nd_distorter(nd, x_rot, y_rot, ind)

            return

    def nd_distorter(self, nd, rot_x, rot_y, index):
        cur_widget = self
        if not self._scaleCalculator:
            width = nd.nd_rot.getContentSize().width
            self._scaleCalculator = DistortScaleCalculator()
            center_pos = cur_widget.panel.ConvertToWorldSpacePercentage(50, 50)
            zeye = self._scaleCalculator.zeye
            self._min_center_size = self._scaleCalculator.get_in_pos_width(width * self.panel_scale, -self._max_rot_angle, center_pos) * zeye
            self._max_center_size = self._scaleCalculator.get_in_pos_width(width * self.panel_scale, 0, center_pos) * zeye
        zeye = self._scaleCalculator.zeye
        wpos = nd.nd_rot.getParent().convertToWorldSpace(nd.nd_rot.getPosition())
        cur_side_size = self._scaleCalculator.get_in_pos_width(nd.nd_rot.getContentSize().width * self.panel_scale, rot_y, wpos) * zeye
        center_size = linear_inter(float(abs(rot_y)), self._max_center_size, self._min_center_size, 0.0, self._max_rot_angle)
        if rot_y > 0:
            percent = abs(rot_y / self._y_rot_max)
        else:
            percent = abs(rot_y / self._y_rot_min)
        percent = min(max(percent, 0.001), 0.99)
        acts = self._ss_card_acts[index]
        for act in acts:
            if act and act.isValid() and not act.isDone():
                act.update(percent)

        nd.nd_rot.setRotation3D(cc.Vec3(rot_x, rot_y, 0))
        percent2 = float(rot_y) / max(abs(self._y_rot_max), abs(self._y_rot_min))
        nd.img_skin.setPositionZ(percent2 * -15 / 2.0 * 2.0)
        nd.img_skin_0.setPositionZ(percent2 * -15 / 2.0 * 2.0)
        nd.img_bar.setPositionZ(percent2 * -30 / 2.0 * 2.0)
        nd.nd_rot.setScaleX(float(center_size) / cur_side_size)

    def set_slerp_action(self, type_str, parameters):
        from logic.vscene.parts.camera.SlerpAction import SlerpActionInst
        self._slerp_act_func = SlerpActionInst.generateAction(type_str, parameters) if SlerpActionInst else None
        return

    def process_slerp_act(self, val, min_val, max_val):
        if not self._slerp_act_func:
            return val
        normalize_val = (val - min_val) / (max_val - min_val)
        normalize_val = max(min(normalize_val, 1.0), 0.0)
        slerp_val = self._slerp_act_func(normalize_val)
        after_val = slerp_val * (max_val - min_val) + min_val
        return after_val

    def set_rotate_range(self, x_rot_range, y_rot_range):
        self._x_rot_min = x_rot_range[0]
        self._x_rot_max = x_rot_range[1]
        self._y_rot_min = y_rot_range[0]
        self._y_rot_max = y_rot_range[1]


USE_SAME_PIC_CLOTHING_IDS = {
 201800651, 201800652, 201800653}

class MechaBasicSkinWidget(BaseUIWidget):

    def __init__(self, parent, panel, mecha_type=None):
        self.global_events = {'player_item_update_event': self._on_buy_good_success,
           'role_fashion_chagne': self.on_role_fashion_chagne,
           'refresh_item_red_point': self.refresh_all_items_rp,
           'mecha_skin_improve_ui_closed': self._ss_panel_close_cb,
           'deactivate_guide_by_name_event': self.on_deactivate_guide_by_name,
           'weapon_sfx_change': self.weapon_sfx_change,
           'pay_order_succ_event': self._on_buy_good_success
           }
        super(MechaBasicSkinWidget, self).__init__(parent, panel)
        if global_data.is_pc_mode:
            self.show_ss_card_effect = False
        else:
            self.show_ss_card_effect = True
        self.force_skin_list = []
        self.init_ui_event()
        self.init_param()
        self.init_widget()
        if mecha_type:
            self.on_switch_mecha_type(mecha_type)
        self.guide_skin_define_btn_set()

    def init_ui_event(self):
        self.panel.temp_btn_buy.btn_common.BindMethod('OnClick', self._on_click_btn_buy_skin)
        self.panel.temp_get.btn_common.BindMethod('OnClick', self._on_click_btn_get_skin)
        self.panel.btn_select.BindMethod('OnClick', self._on_click_btn_select)

    def get_skin_id(self):
        return self.cur_clothing_id

    def on_switch_mecha_type(self, mecha_type):
        old_mecha_id = self._cur_mecha_id
        self._cur_mecha_id = mecha_type
        self._cur_rare_degree_limited = None
        self.update_clothing_show_list()
        if self.cur_clothing_id and old_mecha_id == self._cur_mecha_id:
            self.check_valid_clothing_id()
        else:
            self.use_default_skin()
        self.update_clothing_status()
        self.hide_skin_rare_choose_panel()
        self.parent.set_cur_clothing_id(self.cur_clothing_id)
        self.update_mecha_view(self.cur_clothing_id)
        self.update_honour_view(self.cur_clothing_id)
        return

    def on_switch_skin_category(self, skins, clothind_id):
        self.force_skin_list = skins
        self._cur_rare_degree_limited = None
        self.update_clothing_show_list()
        self.cur_clothing_id = clothind_id
        self._cur_mecha_id = self.get_cur_mecha_id(self.cur_clothing_id)
        self.check_valid_clothing_id()
        self.update_clothing_status()
        self.hide_skin_rare_choose_panel()
        self.parent.set_cur_clothing_id(self.cur_clothing_id)
        self.update_mecha_view(self.cur_clothing_id)
        self.update_honour_view(self.cur_clothing_id)
        return

    def on_refresh(self):
        self.update_clothing_show_list()
        self.check_valid_clothing_id()
        self.update_clothing_status()
        self.parent.set_cur_clothing_id(self.cur_clothing_id)
        self.update_mecha_view(self.cur_clothing_id)
        self.update_honour_view(self.cur_clothing_id)

    def update_show_list(self):
        if self._cur_rare_degree_limited is not None:
            self.show_skin_list_cnf = self.rare_degree_groups.get(self._cur_rare_degree_limited, [])
        else:
            self.show_skin_list_cnf = self.skin_list_cnf
        if not self.show_skin_list_cnf:
            self._cur_rare_degree_limited = None
            self.show_skin_list_cnf = self.skin_list_cnf
        return

    def update_rare_show(self):
        self.ss_card_effect.release_ss_card_items()
        ss_items_dict = self.get_ss_card_items()
        for ss_item in six.itervalues(ss_items_dict):
            self.detach_effect_to_ss_card(ss_item)

        self._ss_card_item_no = None
        self._base_clothing_id_to_item = {}
        self.list_skin_ui.RecycleAllItem()
        self.list_skin_dot.RecycleAllItem()
        self.panel.nd_skin_choose.setVisible(False)
        self.list_container.clear()
        self.clothing_selected_index = 0
        self.group_clothing_selected_index = 0
        if self.show_skin_list_cnf is not None and len(self.show_skin_list_cnf) > 0:
            while self.list_skin_dot.GetItemCount() < len(self.show_skin_list_cnf):
                ui_item = self.list_skin_dot.ReuseItem()
                if not ui_item:
                    self.list_skin_dot.AddTemplateItem()

            self.cur_create_skin_index = 0
            self.clear_async_action()
            self._async_action = self.panel.runAction(cc.RepeatForever.create(cc.Sequence.create([
             cc.CallFunc.create(self.create_skin_item),
             cc.DelayTime.create(0.01)])))
        return

    def use_default_skin(self):
        dressed_clothing_id = dress_utils.get_mecha_dress_clothing_id(self._cur_mecha_id)
        self.clothing_selected_index = 0
        self.cur_clothing_id = self.show_skin_list_cnf[self.clothing_selected_index]
        self.group_clothing_selected_index = 0
        if dressed_clothing_id is not None:
            search_clothing_id = self.get_search_clothing_id(dressed_clothing_id)
            if search_clothing_id in self.show_skin_list_cnf:
                self.clothing_selected_index = self.show_skin_list_cnf.index(search_clothing_id)
                self.cur_clothing_id = dressed_clothing_id
                self.group_clothing_selected_index = 0
                group_skin_list = skin_define_utils.get_group_skin_list(dressed_clothing_id)
                if group_skin_list:
                    self.group_clothing_selected_index = group_skin_list.index(dressed_clothing_id)
        return

    def update_clothing_show_list(self):
        self.skin_list_cnf = self.force_skin_list or mecha_skin_utils.get_show_skin_list(self._cur_mecha_id) if 1 else self.force_skin_list
        self.refresh_rare_degree_groups()
        self.refresh_own_count()
        self.init_skin_choose_panel_by_mecha()
        self.update_show_list()
        self.update_rare_show()

    def refresh_rare_degree_groups(self):
        self.rare_degree_groups = {}
        for item_no in self.skin_list_cnf:
            rare_degree = skin_define_utils.get_mecha_skin_rare_degree(item_no)
            if rare_degree:
                self.rare_degree_groups.setdefault(rare_degree, [])
                self.rare_degree_groups[rare_degree].append(item_no)

    def refresh_own_count(self):
        has_func = global_data.player.has_item_by_no if global_data.player else (lambda : 0)
        skin_count_dict = {}
        degree_keys = six_ex.keys(self.rare_degree_groups)
        for rare_degree, rare_list in six.iteritems(self.rare_degree_groups):
            for item_no in rare_list:
                own = has_func(item_no)
                skin_count_dict.setdefault(rare_degree, 0)
                if own:
                    skin_count_dict[rare_degree] += 1

        degree_keys.sort(reverse=True)
        self.mecha_choose_option_list = []
        for degree in degree_keys:
            name = get_text_by_id(81364).format(item_utils.get_rare_degree_name(degree))
            name = [name, '%d/%d' % (skin_count_dict[degree], len(self.rare_degree_groups[degree]))]
            self.mecha_choose_option_list.append({'rare_degree': degree,'name': name})

        name = [
         get_text_by_id(608138), '%d/%d' % (sum(six_ex.values(skin_count_dict)) + 1, len(self.skin_list_cnf))]
        self.mecha_choose_option_list.insert(0, {'rare_degree': None,'name': name})
        self.update_showed_skin_count()
        return

    def update_showed_skin_count(self):
        for info in self.mecha_choose_option_list:
            if info['rare_degree'] == self._cur_rare_degree_limited:
                show_name = info['name'][0] + ' ' + info['name'][1]
                self.panel.lab_select.SetString(show_name)

    def clear_async_action(self):
        if self._async_action is not None:
            self.panel.stopAction(self._async_action)
            self._async_action = None
        return

    def create_skin_item(self):
        import time
        start_time = time.time()
        while self.cur_create_skin_index < len(self.show_skin_list_cnf):
            clothing_id = self.show_skin_list_cnf[self.cur_create_skin_index]
            item_config = confmgr.get('lobby_item', str(clothing_id))
            if item_config is not None:
                clothing_item = self.list_skin_ui.ReuseItem()
                if not clothing_item:
                    clothing_item = self.list_skin_ui.AddTemplateItem()
                clothing_item.SetClipObjectRecursion(self.panel.nd_cut)
            else:
                clothing_item = self.list_skin_ui.AddTemplateItem()
                log_error('clothing_id has not conf', clothing_id)
            self.init_clothing_item(item_config, clothing_item, clothing_id, self.cur_create_skin_index)
            base_skin_id = mecha_skin_utils.get_mecha_base_skin_id(clothing_id)
            if base_skin_id is None:
                base_skin_id = clothing_id
            self._base_clothing_id_to_item[base_skin_id] = clothing_item
            self.cur_create_skin_index = self.cur_create_skin_index + 1
            if time.time() - start_time > 0.015:
                return

        self.clear_async_action()
        self.panel.nd_skin_choose.setVisible(True)
        if self.list_skin_dot.GetItemCount() > 0:
            self.list_container.init_list()
            if self.clothing_selected_index != 0 and self.clothing_selected_index < len(self.show_skin_list_cnf):
                self._force_select_clothing(self.clothing_selected_index)
            else:
                self._force_select_clothing(0)
        self.check_clothing_on_ss_level()
        return

    def destroy(self):
        super(MechaBasicSkinWidget, self).destroy()
        self.force_skin_list = []
        self._cur_mecha_id = None
        self.list_skin_ui = None
        self._base_clothing_id_to_item = None
        self._ss_card_item_no = None
        self.destroy_widget('ss_card_effect')
        if self.list_container:
            self.list_container.release()
            self.list_container = None
        return

    def init_param(self):
        self._mecha_info_conf = confmgr.get('mecha_conf', 'MechaConfig', 'Content')
        self._mecha_skin_conf = confmgr.get('mecha_conf', 'SkinConfig', 'Content')
        self._mecha_conf = confmgr.get('mecha_display', 'HangarConfig', 'Content')
        self._skill_conf = confmgr.get('mecha_display', 'HangarConfig_Skills', 'Content')
        self._timer_id = None
        self._cur_mecha_goods_id = None
        self._base_clothing_id_to_item = {}
        self._ss_card_item_no = None
        self._share_content = None
        self.skin_list_cnf = None
        self.show_skin_list_cnf = None
        self.cur_create_skin_index = 0
        self._async_action = None
        self._open_mecha_lst = [
         8001]
        self._cur_mecha_id = None
        self._cur_mecha_cam_data = None
        self.mecha_prof_widget = None
        self._cur_select_mecha_effect_id = 0
        self._by_role_panel = False
        self.clothing_selected_index = 0
        self.group_clothing_selected_index = 0
        self.cur_clothing_id = 0
        self._cur_rare_degree_limited = None
        return

    def init_widget(self):
        self.list_skin_ui = self.panel.list_skin
        self.list_skin_dot = self.panel.nd_skin_choose.list_skin_dot
        self.list_container = ScaleableHorzContainer(self.list_skin_ui, self.panel.nd_cut, self.list_skin_dot, self._skin_move_select_callback, self._skin_up_select_callback, self._on_begin_callback)
        self.ss_card_effect = SSCardsEffect(self.panel, self.panel.nd_rot_example, self.panel.list_skin.GetNodeToWorldScale().y)

        @self.panel.btn_tags_desc_close.unique_callback()
        def OnBegin(btn, touch):
            wpos = touch.getLocation()
            nd_tags_desc = self.panel.nd_tags_desc
            if nd_tags_desc.isVisible():
                nd_tags_desc.setVisible(False)

    def get_cur_mecha_id(self, skin_id):
        if self.force_skin_list:
            cur_mecha_id = mecha_lobby_id_2_battle_id(item_utils.get_lobby_item_belong_no(skin_id))
        else:
            cur_mecha_id = self._cur_mecha_id
        return cur_mecha_id

    def _skin_move_select_callback(self, selected_index):
        self._skin_up_select_callback(selected_index)

    def _skin_up_select_callback(self, selected_index):
        if not global_data.player:
            return
        if selected_index != self.clothing_selected_index:
            skin_list = self.show_skin_list_cnf
            skin_id = skin_list[selected_index]
            self.clothing_selected_index = selected_index
            cur_mecha_id = self.get_cur_mecha_id(skin_id)
            dressed_clothing_id = dress_utils.get_mecha_dress_clothing_id(cur_mecha_id)
            self.group_clothing_selected_index = 0
            group_skin_list = skin_define_utils.get_group_skin_list(skin_id)
            if group_skin_list:
                if dressed_clothing_id in group_skin_list:
                    self.group_clothing_selected_index = group_skin_list.index(dressed_clothing_id)
                elif skin_id in group_skin_list:
                    self.group_clothing_selected_index = group_skin_list.index(skin_id)
            self.cur_clothing_id = skin_id
            if self.cur_clothing_id and self.force_skin_list:
                self._cur_mecha_id = self.get_cur_mecha_id(self.cur_clothing_id)
            self.req_del_item_redpoint(skin_id)
            self.update_clothing_status()
            self.parent.set_cur_clothing_id(self.cur_clothing_id)
            self.update_mecha_view(skin_id)
            self.update_honour_view(skin_id)
            self.check_clothing_on_ss_level()

    def _on_begin_callback(self):
        if not global_data.video_player.is_in_init_state():
            global_data.video_player.stop_video()

    def get_skin_id_item(self, skin_id):
        base_skin_id = mecha_skin_utils.get_mecha_base_skin_id(skin_id)
        if base_skin_id is None:
            base_skin_id = skin_id
        return self._base_clothing_id_to_item.get(base_skin_id, None)

    def update_clothing_status(self):
        clothing_id, group_skin_list = self.get_rel_clothing()
        self._update_clothing_status(clothing_id)
        list_mecha_nd = self.panel.list_temp_mecha
        skin_num = len(group_skin_list)
        self.panel.nd_mecha_list.setVisible(skin_num > 1)
        if skin_num > 1:
            list_mecha_nd.SetInitCount(skin_num)
            for i, item in enumerate(list_mecha_nd.GetAllItem()):
                skin_id = group_skin_list[i]
                item.skin_id = skin_id
                item.img_icon.SetDisplayFrameByPath('', get_lobby_item_pic_by_item_no(skin_id))
                show_new = global_data.lobby_red_point_data.get_rp_by_no(skin_id)
                red_point_utils.show_red_point_template(item.temp_red, show_new)
                clothing_data = global_data.player.get_item_by_no(skin_id)
                item.img_mask.setVisible(clothing_data is None)
                self.group_item_select(item, False)

                @item.btn_icon.unique_callback()
                def OnClick(_btn, _touch, _index=i, _cid=skin_id):
                    list_mecha_nd = self.panel.list_temp_mecha
                    old_item = list_mecha_nd.GetItem(self.group_clothing_selected_index)
                    self.group_item_select(old_item, False)
                    cur_item = list_mecha_nd.GetItem(_index)
                    self.group_item_select(cur_item, True)
                    self.group_clothing_selected_index = _index
                    self._update_clothing_status(_cid)
                    self.parent.set_cur_clothing_id(_cid)
                    self.update_mecha_view(_cid)
                    self.update_honour_view(_cid)

            first_item = list_mecha_nd.GetItem(self.group_clothing_selected_index)
            list_mecha_nd.LocatePosByItem(self.group_clothing_selected_index)
            self.group_item_select(first_item, True)
            if skin_num == 2:
                cur_w, h = list_mecha_nd.GetContentSize()
                new_w = list_mecha_nd.GetChildren()[0].GetContentSize()[0]
                diff_w = new_w - cur_w
                list_mecha_nd.SetContentSize(new_w, h)
                cur_w, h = self.panel.nd_mecha_list.GetContentSize()
                self.panel.nd_mecha_list.SetContentSize(cur_w + diff_w, h)
            else:
                self.panel.nd_mecha_list.InitConfContentSize()
                list_mecha_nd.InitConfContentSize()
        self.nd_set_adapted()
        return

    def group_item_select(self, item, select):
        if item:
            item.img_frame_choose.setVisible(select)

    def _update_clothing_status(self, clothing_id):
        from logic.gutils.item_utils import update_limit_btn, get_item_need_corner_limited_tag
        if hasattr(self.panel, 'nd_logo') and get_item_need_corner_limited_tag(clothing_id):
            update_limit_btn(clothing_id, self.panel.nd_logo, is_corner=True)
        else:
            self.panel.nd_logo.setVisible(False)
        cur_mecha_item_id = item_utils.get_lobby_item_belong_no(clothing_id)
        mecha_item_data = global_data.player.get_item_by_no(cur_mecha_item_id)
        clothing_data = global_data.player.get_item_by_no(clothing_id)
        item = self.get_skin_id_item(clothing_id)
        cur_skin_cnf = self._mecha_skin_conf.get(str(clothing_id), {})
        if clothing_data is None:
            if item:
                item.nd_lock.setVisible(True)
        elif item:
            item.nd_lock.setVisible(False)
        init_mecha_buy_btn(self.panel, clothing_id, self._cur_mecha_id)
        is_ss = mecha_skin_utils.is_ss_level_skin(clothing_id)
        is_s_upgradable = mecha_skin_utils.is_s_skin_that_can_upgrade(clothing_id)
        is_own = mecha_item_data and clothing_data
        self.update_btn_set_state(is_ss, is_s_upgradable, is_own, clothing_id)
        self.refresh_btn_set_rp(clothing_id)
        for clothing_id, clothing_item in six.iteritems(self._base_clothing_id_to_item):
            if global_data.player:
                clothing_id = global_data.player.get_replace_clothing_id(clothing_id)
            show_remain_time(clothing_item.nd_time, clothing_item.nd_time.lab_time, clothing_id)

        self.panel.nd_tags.InitConfContentSize()
        if is_ss:
            w, h = self.panel.nd_tags.GetContentSize()
            w -= self.panel.btn_play.GetContentSize()[0]
            self.panel.nd_tags.SetContentSize(w, h)
        init_skin_tags(self.panel.nd_tags, self.panel.nd_tags_desc, self.panel.bar_tags, cur_skin_cnf.get('skin_tags', []))
        from logic.gutils import battle_pass_utils
        cur_mecha_item_id = battle_id_to_mecha_lobby_id(self._cur_mecha_id)
        battle_pass_utils.update_battlepass_free_trial_template(self.panel.temp_bp_free, cur_mecha_item_id)
        return

    def refresh_btn_set_rp(self, clothing_id):
        show_rp = False
        ss_skin_lst = mecha_skin_utils.get_mecha_ss_skin_lst(clothing_id)
        if ss_skin_lst:
            for ss_c_id in ss_skin_lst:
                show_new = global_data.lobby_red_point_data.get_rp_by_no(ss_c_id)
                if show_new:
                    show_rp = True
                    break

        else:
            group_skin_list = skin_define_utils.get_group_skin_list(clothing_id)
            for skin_id in group_skin_list:
                show_new = global_data.lobby_red_point_data.get_rp_by_no(skin_id)
                if show_new:
                    show_rp = True
                    break

        if SkinDefineUI.check_red_point():
            show_rp = True
        red_point_utils.show_red_point_template(self.panel.btn_set.img_red, show_rp)

    def refresh_all_items_rp(self):
        for clothing_id, item_widget in six.iteritems(self._base_clothing_id_to_item):
            if global_data.player:
                clothing_id = global_data.player.get_replace_clothing_id(clothing_id)
            show_new = global_data.lobby_red_point_data.get_rp_by_no(clothing_id)
            item_widget and red_point_utils.show_red_point_template(item_widget.nd_new, show_new)

        for item in self.panel.list_temp_mecha.GetAllItem():
            skin_id = getattr(item, 'skin_id', 0)
            show_new = global_data.lobby_red_point_data.get_rp_by_no(skin_id)
            red_point_utils.show_red_point_template(item.temp_red, show_new)

        self.refresh_btn_set_rp(self.cur_clothing_id)

    def jump_to_skin(self, skin_id):
        if skin_id not in self.show_skin_list_cnf:
            self._cur_rare_degree_limited = None
            self.on_rare_degree_refresh()
        if not self.force_skin_list:
            now_skin_lst = self.show_skin_list_cnf
        else:
            now_skin_lst = self.force_skin_list
        main_skin_id = skin_define_utils.get_main_skin_id(skin_id)
        base_skin_id = mecha_skin_utils.get_mecha_base_skin_id(skin_id)
        if skin_id in now_skin_lst:
            clothing_selected_index = now_skin_lst.index(int(skin_id))
        elif main_skin_id in now_skin_lst:
            clothing_selected_index = now_skin_lst.index(int(main_skin_id))
        elif base_skin_id in now_skin_lst:
            clothing_selected_index = now_skin_lst.index(int(base_skin_id))
        else:
            return
        self._skin_up_select_callback(clothing_selected_index)
        if self.list_container.is_init():
            self._force_select_clothing(clothing_selected_index)
        return

    def init_clothing_item(self, item_config, clothing_item, clothing_id, idx_in_skin_lst):
        item_no = item_config.get('item_no')
        name_text = item_utils.get_lobby_item_name(item_no)
        clothing_item.lab_skin_name.setString(name_text)
        item_utils.init_skin_card(clothing_item, clothing_id)
        skin_cfg = confmgr.get('mecha_conf', 'SkinConfig', 'Content', str(clothing_id))
        if skin_cfg:
            item_utils.check_skin_tag(clothing_item.nd_kind, clothing_id)
            skin_half_imge_path = skin_cfg.get('half_img_path', None)
            if skin_half_imge_path != None:
                clothing_item.img_skin.SetDisplayFrameByPath('', skin_half_imge_path)
            if mecha_skin_utils.is_ss_level_skin(clothing_id) and self.check_has_ss_card_effect_res(clothing_id):
                self.attach_effect_to_ss_card(clothing_item, clothing_id)
            else:
                self.detach_effect_to_ss_card(clothing_item)
        show_remain_time(clothing_item.nd_time, clothing_item.nd_time.lab_time, clothing_id)
        show_new = global_data.lobby_red_point_data.get_rp_by_no(clothing_id)
        red_point_utils.show_red_point_template(clothing_item.nd_new, show_new)
        clothing_data = global_data.player.get_item_by_no(clothing_id) if global_data.player else None
        if clothing_data is None:
            clothing_item.nd_lock.setVisible(True)
        else:
            clothing_item.nd_lock.setVisible(False)
        return

    def req_del_item_redpoint(self, skin_id):
        show_new = global_data.lobby_red_point_data.get_rp_by_no(skin_id)
        if show_new:
            global_data.player.req_del_item_redpoint(skin_id)

    def nd_set_adapted(self):
        nd_list = [self.panel.btn_ss, self.panel.btn_s_plus, self.panel.btn_set, self.panel.nd_mecha_list]
        x_off = 0
        for nd in nd_list:
            if nd.isVisible():
                X, Y = nd.GetPosition()
                nd.SetPosition(x_off, Y)
                x_off += nd.GetContentSize()[0]

        nd_set = self.panel.nd_set
        W, H = nd_set.GetContentSize()
        X, Y = nd_set.GetPosition()
        nd_set.SetContentSize(x_off, H)
        nd_set.SetPosition('50%', Y)

    def _force_select_clothing(self, select_index):
        if not self.list_container.is_init():
            return
        skin_list = self.show_skin_list_cnf
        self.list_container.force_select_clothing(select_index)
        select_skin_id = skin_list[select_index]
        item = self.get_skin_id_item(select_skin_id)
        if item and mecha_skin_utils.is_ss_level_skin(select_skin_id):
            item_utils.init_skin_card(item, select_skin_id)
            if self.check_has_ss_card_effect_res(select_skin_id):
                self.attach_effect_to_ss_card(item, select_skin_id)
        elif item and mecha_skin_utils.is_s_skin_that_can_upgrade(select_skin_id):
            pass
        self.check_clothing_on_ss_level()

    def attach_effect_to_ss_card(self, ui_item, skin_id):
        ui_item.img_frame.setVisible(False)
        if self.show_ss_card_effect:
            ui_item.img_skin_0.setVisible(True)
            img_1 = 'gui/ui_res_2/item/mecha_skin/%s_1.png' % skin_id
            if skin_id in USE_SAME_PIC_CLOTHING_IDS or not cc.FileUtils.getInstance().isFileExist(img_1):
                ui_item.img_skin_0.SetDisplayFrameByPath('', 'gui/ui_res_2/item/mecha_skin/%s.png' % skin_id)
            else:
                ui_item.img_skin_0.SetDisplayFrameByPath('', img_1)

        def add_func(cache_ui_item):
            if cache_ui_item:
                ui_item.nd_frame_ss.AddChild('temp_ss_frame', cache_ui_item)

        check_has_node = hasattr(ui_item.nd_frame_ss, 'temp_ss_frame') and ui_item.nd_frame_ss.temp_ss_frame and ui_item.nd_frame_ss.temp_ss_frame.getParent()
        if not check_has_node:
            cache_ret = global_data.item_cache_without_check.pop_item_by_json(CARD_SS_FRAME_TEMPLATE, add_func)
            if cache_ret:
                item_widget = cache_ret
            else:
                item_widget = global_data.uisystem.load_template_create(CARD_SS_FRAME_TEMPLATE)
                add_func(item_widget)
            item_widget.SetPosition('50%', '50%')
            item_widget.img_frame_ss.getGLProgramState().setUniformFloat('Hue', 0.0)
        if not self.show_ss_card_effect:
            return
        check_has_light = hasattr(ui_item.temp_light, 'nd_light') and ui_item.temp_light.nd_light and ui_item.temp_light.nd_light.getParent()
        base_skin_id = mecha_skin_utils.get_mecha_base_skin_id(skin_id)
        light_template_path = 'mech_display/i_light_%s_1' % base_skin_id

        def add_func2(cache_ui_item):
            if cache_ui_item:
                ui_item.temp_light.AddChild('nd_light', cache_ui_item)

        if not check_has_light:
            cache_ret = global_data.item_cache_without_check.pop_item_by_json(light_template_path, add_func2)
            if cache_ret:
                item_widget = cache_ret
            else:
                try:
                    item_widget = global_data.uisystem.load_template_create(light_template_path)
                except:
                    return

                add_func2(item_widget)
            item_widget._ccb_template_path = light_template_path
            item_widget.SetPosition('50%', '50%')
            for child in item_widget.GetChildren():
                if child.widget_name != 'vx_shine_white':
                    child.SetDisplayFrameByPath('', 'gui/ui_res_2/role_profile/light_%s_2.png' % skin_id)
                else:
                    child.SetDisplayFrameByPath('', 'gui/ui_res_2/role_profile/light_%s_1.png' % skin_id)

    def check_has_ss_card_effect_res(self, skin_id):
        base_skin_id = mecha_skin_utils.get_mecha_base_skin_id(skin_id)
        light_template_path = 'mech_display/i_light_%s_1' % base_skin_id
        find_res = global_data.uisystem.CheckHasTemplate(light_template_path)
        return find_res

    def detach_effect_to_ss_card(self, ui_item):
        ui_item.img_frame.setVisible(True)
        ui_item.img_skin_0.setVisible(False)
        item_cache = global_data.item_cache_without_check
        if hasattr(ui_item.nd_frame_ss, 'temp_ss_frame'):
            temp_ss_frame = ui_item.nd_frame_ss.temp_ss_frame
            if temp_ss_frame:
                if item_cache.check_can_put_back(temp_ss_frame, CARD_SS_FRAME_TEMPLATE):
                    item_cache.put_back_item_to_cache(temp_ss_frame, CARD_SS_FRAME_TEMPLATE)
        if hasattr(ui_item.temp_light, 'nd_light'):
            nd_light = ui_item.temp_light.nd_light
            if nd_light:
                if item_cache.check_can_put_back(nd_light, nd_light._ccb_template_path):
                    item_cache.put_back_item_to_cache(nd_light, nd_light._ccb_template_path)

    def update_mecha_view(self, skin_id):
        is_change_skin = True
        self.change_lobby_model_display(self._cur_mecha_id, skin_id, is_change_skin)

    def update_honour_view(self, skin_id):
        set_mecha_honour_view(self.panel.temp_honour, skin_id, True)

    def change_lobby_model_display(self, mecha_id, clothing_id, is_change_skin=False, shiny_id=None):
        if self.parent:
            self.parent.change_lobby_model_display(mecha_id, clothing_id, is_change_skin, shiny_id)
        self.check_clothing_on_ss_level()

    def update_btn_set_state(self, is_ss, is_s_upgradable, is_own, clothing_id):
        self.panel.btn_ss.setVisible(is_ss)
        self.panel.btn_s_plus.setVisible(is_s_upgradable)
        self.panel.btn_play.setVisible(is_ss)
        if is_ss or is_s_upgradable:

            @self.panel.btn_play.unique_callback()
            def OnClick(_btn, _touch, _cid=clothing_id):
                video_conf = confmgr.get('mecha_conf', 'SkinConfig', 'Content', str(_cid), 'shiny_weapon_video_website', default=None)
                if video_conf:
                    video_url = None
                    video_player_type = False
                    if interface.is_steam_channel():
                        from logic.gcommon.common_utils.local_text import get_cur_lang_name
                        lang_name = get_cur_lang_name()
                        if lang_name == 'cn':
                            video_url = video_conf.get('cn', None)
                            video_player_type = False
                        else:
                            video_url = video_conf.get('na', None)
                            video_player_type = True
                    elif G_IS_NA_USER:
                        video_url = video_conf.get('na', None)
                        video_player_type = True
                    else:
                        video_url = video_conf.get('cn', None)
                        video_player_type = False
                    if video_player_type:
                        import game3d
                        game3d.open_url(video_url)
                    else:

                        def func():
                            from logic.comsys.video.VideoUILogicWidget import VideoUILogicWidget
                            VideoUILogicWidget().play_vod(video_url)
                            player = global_data.video_player.get_player()
                            player.set_volume(0.2)

                        from common.utils import network_utils
                        cur_type = network_utils.g93_get_network_type()
                        if cur_type == network_utils.TYPE_MOBILE:
                            from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
                            SecondConfirmDlg2().confirm(content=get_text_by_id(607499), confirm_callback=func)
                        else:
                            func()
                else:
                    global_data.game_mgr.show_tip(10063)
                return

        @self.panel.btn_ss.unique_callback()
        def OnClick(_btn, _touch, _cid=clothing_id):
            if self.parent.cur_clothing_id != _cid:
                return
            ss_skin_lst = mecha_skin_utils.get_mecha_ss_skin_lst(clothing_id)
            for skin_id in ss_skin_lst:
                self.req_del_item_redpoint(skin_id)

            self._on_show_skin_improve(_cid)
            global_data.emgr.set_last_chuchang_id.emit(_cid)

        @self.panel.btn_s_plus.unique_callback()
        def OnClick(_btn, _touch, _cid=clothing_id):
            if self.parent.cur_clothing_id != _cid:
                return
            self._on_show_skin_improve(_cid)
            global_data.emgr.set_last_chuchang_id.emit(_cid)

        is_open = skin_define_utils.is_open_by_clothing_id(self.cur_clothing_id)
        if is_open:
            self.panel.btn_set.SetEnable(True)

            @self.panel.btn_set.unique_callback()
            def OnClick(_btn, _touch):
                self.req_del_item_redpoint(self.cur_clothing_id)
                self._on_show_skin_define()

        else:
            self.panel.btn_set.SetEnable(False)

    def _on_show_skin_improve(self, c_id):
        ui = global_data.ui_mgr.get_ui('SkinImproveWidgetUI')
        if not ui:
            from logic.comsys.mecha_display.SkinImproveWidgetUI import SkinImproveWidgetUI
            ui = SkinImproveWidgetUI(None)
        else:
            ui.clear_show_count_dict()
        if ui:
            ui.on_show_skin_improve(self._cur_mecha_id, c_id)
        return

    def _on_show_skin_define(self):
        from logic.gutils.jump_to_ui_utils import jump_to_skin_define
        if self._cur_mecha_id:
            jump_to_skin_define(self._cur_mecha_id, self.cur_clothing_id)

    def _ss_panel_close_cb(self, mecha_id, skin_id):
        if mecha_id != self._cur_mecha_id:
            return
        else:
            skin_list = self.show_skin_list_cnf
            base_skin_id = mecha_skin_utils.get_mecha_base_skin_id(self.cur_clothing_id)
            if base_skin_id is None:
                return
            if skin_id in skin_list:
                self.parent.first_load_tag = True
                self.change_lobby_model_display(self._cur_mecha_id, skin_id, True)
            return

    def init_skin_choose_panel_by_mecha(self):
        from logic.gutils import template_utils

        def on_sel_opt(index):
            new_rare_degree = self.mecha_choose_option_list[index].get('rare_degree')
            if self._cur_rare_degree_limited == new_rare_degree:
                return
            self._cur_rare_degree_limited = new_rare_degree
            self.on_rare_degree_refresh()
            self.hide_skin_rare_choose_panel()

        template_utils.init_common_choose_list(self.panel.choose_list, self.mecha_choose_option_list, on_sel_opt, close_cb=self.hide_skin_rare_choose_panel)

    def hide_skin_rare_choose_panel(self):
        self.panel.choose_list.setVisible(False)
        self.panel.sp_rot.setRotation(0)

    def get_rel_clothing(self):
        skin_list = self.show_skin_list_cnf
        clothing_id = skin_list[self.clothing_selected_index]
        group_skin_list = skin_define_utils.get_group_skin_list(clothing_id)
        if group_skin_list:
            clothing_id = group_skin_list[self.group_clothing_selected_index]
        return (clothing_id, group_skin_list)

    def _on_click_btn_get_skin(self, *args):
        clothing_id, _ = self.get_rel_clothing()
        if item_utils.can_jump_to_ui(str(clothing_id)):
            item_utils.jump_to_ui(str(clothing_id))

    def _on_click_btn_buy_skin(self, *args):
        clothing_id, _ = self.get_rel_clothing()
        rel_clothing_id = clothing_id
        top_clothing_id = skin_define_utils.get_main_skin_id(clothing_id)
        cur_mecha_item_id = battle_id_to_mecha_lobby_id(self._cur_mecha_id)
        default_skin = confmgr.get('mecha_conf', 'LobbyMechaConfig', 'Content', str(cur_mecha_item_id), 'default_fashion')[0]
        goods_id = self._mecha_skin_conf.get(str(clothing_id), {}).get('goods_id')
        is_default_skin = False
        if int(default_skin) == int(clothing_id):
            clothing_id = cur_mecha_item_id
            is_default_skin = True
        clothing_data = global_data.player.get_item_by_no(clothing_id)
        mecha_item_data = global_data.player.get_item_by_no(cur_mecha_item_id)
        if clothing_data is not None and mecha_item_data is None:
            goods_id = self._mecha_skin_conf.get(str(default_skin), {}).get('goods_id')
            self.buy_skin(is_default_skin, default_skin, None, None, goods_id)
        else:
            self.buy_skin(is_default_skin, rel_clothing_id, top_clothing_id, clothing_data, goods_id)
        return

    def buy_skin(self, is_default_skin, clothing_id, top_clothing_id, clothing_data, goods_id):
        if is_default_skin:
            is_owned = clothing_data and clothing_data.get_expire_time() < 0
        else:
            is_owned = clothing_data
        if not is_owned:
            if item_utils.can_jump_to_ui(str(clothing_id)) and not self.panel.nd_get.isVisible():
                from logic.gutils.mall_utils import get_mall_item_price
                price_list = get_mall_item_price(goods_id)
                if price_list:
                    ui = role_or_skin_buy_confirmUI(goods_id)
                    if hasattr(ui, 'set_buttom_ui_price_nd'):
                        ui.set_buttom_ui_price_nd(self.parent.panel.nd_top)
                else:
                    self._on_click_btn_get_skin()
            else:
                ui = role_or_skin_buy_confirmUI(goods_id)
                if hasattr(ui, 'set_buttom_ui_price_nd'):
                    ui.set_buttom_ui_price_nd(self.parent.panel.nd_top)
        else:
            global_data.player.install_mecha_main_skin_scheme(self._cur_mecha_id, top_clothing_id, {FASHION_POS_SUIT: clothing_id})

    def _on_click_btn_select(self, *args):
        if self.panel.choose_list.isVisible():
            self.panel.choose_list.setVisible(False)
            self.panel.sp_rot.setRotation(0)
        else:
            self.panel.choose_list.setVisible(True)
            self.panel.sp_rot.setRotation(180)

    def _on_buy_good_success(self):
        if not self.panel or self.panel.IsDestroyed():
            return
        self.update_clothing_status()
        self.refresh_own_count()

    def on_role_fashion_chagne(self, item_no, fashion_data):
        from logic.gutils import item_utils
        from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_MECHA
        lobby_item_type = item_utils.get_lobby_item_type(item_no)
        if lobby_item_type != L_ITEM_TYPE_MECHA:
            return
        else:
            dress_utils.show_change_fashion_tips(fashion_data, self.cur_clothing_id)
            from logic.gutils.dress_utils import mecha_lobby_id_2_battle_id
            mecha_id = mecha_lobby_id_2_battle_id(item_no)
            if mecha_id != self._cur_mecha_id:
                return
            if not self.panel:
                return
            dressed_clothing_id = fashion_data.get(FASHION_POS_SUIT)
            if not (self.is_visible() and self.panel.IsVisible()):
                self.cur_clothing_id = dressed_clothing_id
                return
            self.update_clothing_show_list()
            self.use_default_skin()
            self.update_clothing_status()
            self.change_lobby_model_display(self._cur_mecha_id, dressed_clothing_id)
            self.skin_list_cnf = self.force_skin_list or mecha_skin_utils.get_show_skin_list(self._cur_mecha_id) if 1 else self.force_skin_list
            self.show_skin_list_cnf = self.skin_list_cnf
            skin_list = self.show_skin_list_cnf
            search_clothing_id = self.get_search_clothing_id(dressed_clothing_id)
            if search_clothing_id in self.show_skin_list_cnf:
                clothing_selected_index = skin_list.index(int(search_clothing_id))
                self._force_select_clothing(clothing_selected_index)
                if mecha_skin_utils.is_ss_level_skin(dressed_clothing_id):
                    item = self.get_skin_id_item(dressed_clothing_id)
                    if item:
                        item_config = confmgr.get('lobby_item', str(dressed_clothing_id))
                        self.init_clothing_item(item_config, item, dressed_clothing_id, clothing_selected_index)
            else:
                self._cur_rare_degree_limited = None
                self.on_rare_degree_refresh()
            return

    def on_rare_degree_refresh(self):
        old_clothing_id = self.cur_clothing_id
        self.update_show_list()
        self.update_rare_show()
        self.check_valid_clothing_id()
        self.update_clothing_status()
        if old_clothing_id != self.cur_clothing_id:
            self.update_mecha_view(self.cur_clothing_id)
            self.update_honour_view(self.cur_clothing_id)
            self.req_del_item_redpoint(self.cur_clothing_id)
        self.refresh_own_count()

    def get_search_clothing_id(self, cur_clothing_id):
        search_clothing_id = cur_clothing_id
        if self.force_skin_list:
            if cur_clothing_id not in self.show_skin_list_cnf:
                cur_top = skin_define_utils.get_main_skin_id(cur_clothing_id)
                for skin_id in self.show_skin_list_cnf:
                    if skin_define_utils.get_main_skin_id(skin_id) == cur_top:
                        search_clothing_id = skin_id
                        break

        return search_clothing_id

    def check_valid_clothing_id(self):
        search_clothing_id = self.get_search_clothing_id(self.cur_clothing_id)
        if search_clothing_id in self.show_skin_list_cnf:
            self.clothing_selected_index = self.show_skin_list_cnf.index(search_clothing_id)
            self.group_clothing_selected_index = 0
            group_skin_list = skin_define_utils.get_group_skin_list(search_clothing_id)
            if group_skin_list:
                self.group_clothing_selected_index = group_skin_list.index(self.cur_clothing_id)
        else:
            self.cur_clothing_id = self.show_skin_list_cnf[0]
            self.clothing_selected_index = 0
            self.group_clothing_selected_index = 0
        if self.cur_clothing_id and self.force_skin_list:
            self._cur_mecha_id = self.get_cur_mecha_id(self.cur_clothing_id)

    def get_ss_card_items(self):
        if not self.show_skin_list_cnf:
            return {}
        ss_card_item_dict = {}
        for clothing_id in self.show_skin_list_cnf:
            if mecha_skin_utils.is_ss_level_skin(clothing_id) and self.check_has_ss_card_effect_res(clothing_id):
                ui_item = self.get_skin_id_item(clothing_id)
                if ui_item:
                    ss_card_item_dict[clothing_id] = ui_item

        return ss_card_item_dict

    def check_clothing_on_ss_level(self):
        if self.show_ss_card_effect:
            if mecha_skin_utils.is_ss_level_skin(self.cur_clothing_id) and self.check_has_ss_card_effect_res(self.cur_clothing_id):
                if self._ss_card_item_no == self.cur_clothing_id:
                    return
                card_items_dict = self.get_ss_card_items()
                if card_items_dict:
                    self._ss_card_item_no = self.cur_clothing_id
                    self.ss_card_effect.update_ss_card_list(six_ex.values(card_items_dict))
                    self.ss_card_effect.start_gyro_effect()
            else:
                self._ss_card_item_no = None
                self.ss_card_effect.update_ss_card_list([])
                self.ss_card_effect.stop_gyro_effect()
        return

    def guide_skin_define_btn_set(self):
        if global_data.lobby_guide_mgr:
            if global_data.lobby_guide_mgr.check_can_activate_by_guide_name('skin_define_enter'):
                global_data.lobby_guide_mgr.switch_node_guide(self.panel.btn_set, 'skin_define_enter', False)

    def on_deactivate_guide_by_name(self, guide_name):
        if guide_name != 'skin_define_enter':
            return
        if global_data.lobby_guide_mgr:
            if not global_data.lobby_guide_mgr.check_can_activate_by_guide_name('skin_define_enter'):
                global_data.lobby_guide_mgr.switch_node_guide(self.panel.btn_set, 'skin_define_enter', True)

    def on_resolution_changed(self):
        if self.list_container.is_init():
            self.list_container.force_select_clothing(self.clothing_selected_index)

    def weapon_sfx_change(self, item_no, value):
        skin_item = self.get_skin_id_item(item_no)
        if skin_item and mecha_skin_utils.is_s_skin_that_can_upgrade(item_no):
            item_utils.init_skin_card(skin_item, item_no)