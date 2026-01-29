# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/debug/DummyTestUI.py
from __future__ import absolute_import
import six
import six_ex
from six.moves import range
from common.uisys.basepanel import BasePanel
from common.const.uiconst import TOP_ZORDER
from common.const import uiconst
from logic.comsys.battle.ArmorBuffWidget import ARMOR_BUFF_PRIORITY_LIST
from logic.gcommon.item import item_const
from logic.gutils.camera_utils import get_camera_position
from logic.gutils.hot_key_utils import human_fire

class DummyTestUI(BasePanel):
    PANEL_CONFIG_NAME = 'test/test_dummy'
    DLG_ZORDER = TOP_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    TAG = 180718
    SHOW_TIME = 999.0
    KEY_TO_SHOW_FUNC = {'armor': 'update_armor_data','client_dist': 'set_client_dist_timer'
       }
    KEY_FORMAT_FUNC = {'time': 'format_to_two_digit_data',
       'dist': ('_neox_dist_to_meter', 'format_to_two_digit_data', '_add_meter_postfix'),
       'client_dist': ('_neox_dist_to_meter', 'format_to_two_digit_data', '_add_meter_postfix')
       }
    QUALITY_PIC = {item_const.NONE_WHITE: 'gui/ui_res_2/battle/buff/frame_lv1.png',
       item_const.NORMAL_GREEN: 'gui/ui_res_2/battle/buff/defend_bar_green.png',
       item_const.SUPERIOR_BLUE: 'gui/ui_res_2/battle/buff/defend_bar_blue.png',
       item_const.EPIC_PURPLE: 'gui/ui_res_2/battle/buff/defend_bar_purple.png'
       }
    MID_HUMAN_HEIGHT = 13
    MID_MECHA_HETGHT = 26

    def on_init_panel(self, *args, **kwargs):
        self.panel.list_armor.SetInitCount(max(six_ex.values(ARMOR_BUFF_PRIORITY_LIST)) + 1)
        self.client_aim_angle_lab = None
        self.robot_eid = None
        self.robot_killable = False
        self.init_parameters()
        self.init_equip_choose_panel()
        self.is_auto_shooting = False
        self.target_pos = None
        self.run_timer = None

        @self.panel.btn_reset.callback()
        def OnClick(btn, touch):
            if global_data.player and global_data.player.logic:
                global_data.player.logic.send_event('E_CALL_SYNC_METHOD', 'reset_dummy_state', (self.robot_eid,), True)

        @self.panel.btn_close.callback()
        def OnClick(btn, touch):
            if self.is_auto_shooting:
                return
            self.add_hide_count(key=self.__class__.__name__)
            self.panel.ccb_client_dist.StopTimerAction()

        @self.panel.btn_robot_killable.callback()
        def OnClick(btn, touch):
            target_entity = global_data.battle.get_entity(self.robot_eid)
            if target_entity:
                if target_entity.sd.ref_hp < 100000:
                    self.panel.btn_robot_killable.robot_killable_label.SetString('\xe5\x85\xb3\xe9\x97\xad\xe6\x97\xa0\xe6\x95\x8c')
                else:
                    self.panel.btn_robot_killable.robot_killable_label.SetString('\xe5\xbc\x80\xe5\x90\xaf\xe6\x97\xa0\xe6\x95\x8c')
                if global_data.player and global_data.player.logic:
                    global_data.player.logic.send_event('E_CALL_SYNC_METHOD', 'switch_dummy_robot_killable', (self.robot_eid,), True)

        @self.panel.btn_choose_equip.callback()
        def OnClick(btn, touch):
            equip_panel = self.panel.EquipPanel
            showing = equip_panel.isVisible()
            if showing:
                equip_panel.setVisible(False)
                self.panel.btn_choose_equip.choose_equip_label.SetString('\xe5\xbc\x80\xe5\x90\xaf\xe6\x8d\xa2\xe8\xa3\x85\xe9\x9d\xa2\xe6\x9d\xbf')
            else:
                equip_panel.setVisible(True)
                self.panel.btn_choose_equip.choose_equip_label.SetString('\xe5\x85\xb3\xe9\x97\xad\xe6\x8d\xa2\xe8\xa3\x85\xe9\x9d\xa2\xe6\x9d\xbf')

        @self.panel.btn_auto_shoot.callback()
        def OnClick(btn, touch):
            if not self.is_auto_shooting:
                self.start_auto_shoot()
                self.panel.btn_auto_shoot.auto_shoot_label.SetString('\xe5\x81\x9c\xe6\xad\xa2\xe5\xb0\x84\xe5\x87\xbb')
                self.is_auto_shooting = True
            else:
                self.stop_auto_shoot()
                self.panel.btn_auto_shoot.auto_shoot_label.SetString('\xe8\x87\xaa\xe5\x8a\xa8\xe5\xb0\x84\xe5\x87\xbb')
                self.is_auto_shooting = False

        return

    def init_parameters(self):
        self.head_equip_btns = [
         self.panel.EquipPanel.ep_0.btn_equip1, self.panel.EquipPanel.ep_0.btn_equip2, self.panel.EquipPanel.ep_0.btn_equip3]
        self.body_equip_btns = [
         self.panel.EquipPanel.ep_1.btn_equip1, self.panel.EquipPanel.ep_1.btn_equip2, self.panel.EquipPanel.ep_1.btn_equip3]
        self.foot_equip_btns = [
         self.panel.EquipPanel.ep_2.btn_equip1, self.panel.EquipPanel.ep_2.btn_equip2, self.panel.EquipPanel.ep_2.btn_equip3]

    def on_finalize_panel(self):
        self.clear_run_timer()
        self.client_aim_angle_lab = None
        return

    def update_data(self, data_dict):
        self.clear_show_count_dict()
        data_dict.update(self.client_attr_display(data_dict))
        items = sorted(six_ex.keys(data_dict))
        normal_text_item_list = []
        for desc in items:
            if desc in self.KEY_TO_SHOW_FUNC:
                show_func = getattr(self, self.KEY_TO_SHOW_FUNC[desc], None)
                if show_func:
                    show_func(data_dict[desc])
            else:
                normal_text_item_list.append((desc, data_dict[desc]))

        self.show_normal_text_item(normal_text_item_list)
        return

    def show_normal_text_item(self, data_list):
        self.panel.lv_data.SetInitCount(len(data_list))
        ui_items = self.panel.lv_data.GetAllItem()
        for idx, ui_item in enumerate(ui_items):
            desc, stat = data_list[idx]
            if desc == 'client_aim_angle':
                ui_item.lab_title.SetString('\xe6\xad\xa6\xe5\x99\xa8\xe5\xa4\xbe\xe8\xa7\x92')
                self.client_aim_angle_lab = ui_item
            else:
                ui_item.lab_title.SetString(self.get_title_show_text(desc))
            if desc in self.KEY_FORMAT_FUNC:
                if isinstance(self.KEY_FORMAT_FUNC[desc], tuple):
                    func_name_list = self.KEY_FORMAT_FUNC[desc]
                    for func_name in func_name_list:
                        format_func = getattr(self, func_name, None)
                        stat = format_func(stat)

                else:
                    format_func = getattr(self, self.KEY_FORMAT_FUNC[desc], None)
                    stat = format_func(stat)
            ui_item.lab_stat.SetString(str(stat))

        return

    def format_to_two_digit_data(self, data):
        formated_data = data
        if isinstance(data, float):
            formated_data = '%.2f' % data
        return formated_data

    def update_armor_data(self, armor_data_dict):
        pos_dict = {}
        from logic.gcommon.item import item_utility as iutil
        for armor_item_id, cur_dur in six.iteritems(armor_data_dict):
            armor_pos = iutil.get_clothing_dress_pos(armor_item_id)
            import common.cfg.confmgr as confmgr
            import copy
            conf = confmgr.get('armor_config', str(armor_item_id))
            armor_conf = copy.deepcopy(conf)
            armor_conf['cur_Dur'] = cur_dur
            pos_dict[armor_pos] = armor_conf

        has_data_index_set = set()
        for armor_pos in six.iterkeys(ARMOR_BUFF_PRIORITY_LIST):
            if armor_pos in pos_dict:
                armor_conf = pos_dict[armor_pos]
                index = ARMOR_BUFF_PRIORITY_LIST[armor_pos]
                has_data_index_set.add(index)
                ui_item = self.panel.list_armor.GetItem(index)
                self._update_armor_data_helper(armor_pos, armor_conf, ui_item)
            else:
                index = ARMOR_BUFF_PRIORITY_LIST[armor_pos]
                if index not in has_data_index_set:
                    ui_item = self.panel.list_armor.GetItem(index)
                    self._update_armor_data_helper(armor_pos, None, ui_item)

        return

    def _update_armor_data_helper(self, pos, armor_conf, uiobj):
        if armor_conf is not None:
            armor_level = armor_conf.get('iLevel', 1)
            from logic.gutils.template_utils import get_armor_buff_pic
            buff_pic = get_armor_buff_pic(pos, armor_level)
            quality_pic = self.QUALITY_PIC.get(armor_level, None)
            if buff_pic and quality_pic:
                uiobj.buff_bar.SetDisplayFrameByPath('', buff_pic)
                uiobj.quality_bar.SetDisplayFrameByPath('', quality_pic)
            uiobj.buff_bar.setVisible(True)
        else:
            from logic.gutils.template_utils import get_armor_empty_buff_pic
            buff_pic = get_armor_empty_buff_pic(pos)
            quality_pic = self.QUALITY_PIC.get(item_const.NONE_WHITE, None)
            if buff_pic and quality_pic:
                uiobj.buff_bar.SetDisplayFrameByPath('', buff_pic)
                uiobj.quality_bar.SetDisplayFrameByPath('', quality_pic)
            uiobj.buff_bar.setVisible(True)
        return

    def get_title_show_text(self, label):
        from common.cfg import confmgr
        return confmgr.get('dummy_conf', str(label), default={}).get('name_cn', 'Unknowed!')

    def hide_self_timer(self):

        def hide_act():
            self.add_hide_count(key=self.__class__.__name__)

        self.panel.SetTimeOut(self.SHOW_TIME, hide_act, tag=self.TAG)

    def _neox_dist_to_meter(self, neox_dist):
        from logic.gcommon.const import NEOX_UNIT_SCALE
        return neox_dist / NEOX_UNIT_SCALE

    def _add_meter_postfix(self, dist):
        return str(dist) + 'm'

    def client_attr_display(self, dict):
        entity_id = dict.get('entity_id', None)
        if self.robot_eid != entity_id:
            self.robot_eid = entity_id
        client_attr = {'client_dist': entity_id,'client_aim_angle': self.get_client_aim_angle(entity_id)
           }
        return client_attr

    def get_client_aim_angle(self, entity_id):
        from mobile.common.EntityManager import EntityManager
        ent = EntityManager.getentity(entity_id)
        if ent and ent.logic:
            model = ent.logic.ev_g_model()
            if model is None:
                return
            import logic.gcommon.common_const.animation_const as animation_const
            import world
            if ent.logic.sd.ref_is_mecha:
                matrix = model.get_bone_matrix('biped spine1', world.SPACE_TYPE_WORLD)
            else:
                matrix = model.get_bone_matrix(animation_const.BONE_SPINE2_NAME, world.SPACE_TYPE_WORLD)
            if not matrix:
                return
            aim_pos = matrix.translation
            scn = world.get_active_scene()
            partcamera = scn.get_com('PartCamera')
            camera = partcamera.cam
            camera_pos = camera.world_position
            camera_direction = camera.world_rotation_matrix.forward
            direction = aim_pos - camera_pos
            direction.y = 0
            direction.normalize()
            camera_direction.y = 0
            camera_direction.normalize()
            angle = abs(direction.yaw - camera_direction.yaw)
            import math
            angle = math.degrees(angle)
            angle = '%.2f' % angle
            return angle
        else:
            return

    def get_distance(self, entity_id):
        from mobile.common.EntityManager import EntityManager
        ent = EntityManager.getentity(entity_id)
        if ent and ent.logic:
            if global_data.cam_lplayer:
                player_pos = global_data.cam_lplayer.ev_g_position()
                ent_pos = ent.logic.ev_g_position()
                if player_pos and ent_pos:
                    neo_dist = (ent_pos - player_pos).length
                    return neo_dist
        return None

    def set_client_dist_timer(self, entity_id):

        def func(dt):
            self.update_client_dist_data(entity_id)

        self.panel.ccb_client_dist.StopTimerAction()
        self.panel.ccb_client_dist.TimerAction(func, self.SHOW_TIME, None)
        return

    def update_client_dist_data(self, entity_id):
        dist = self.get_distance(entity_id)
        if dist:
            dist_str = self._add_meter_postfix(self.format_to_two_digit_data(self._neox_dist_to_meter(dist)))
        else:
            dist_str = '\xe6\x9a\x82\xe6\x97\xa0'
        self.panel.ccb_client_dist.lab_title.SetString('\xe5\xae\xa2\xe6\x88\xb7\xe7\xab\xaf\xe8\xb7\x9d\xe7\xa6\xbb')
        self.panel.ccb_client_dist.lab_stat.SetString(dist_str)
        if self.client_aim_angle_lab:
            self.client_aim_angle_lab.lab_title.SetString('\xe6\xad\xa6\xe5\x99\xa8\xe5\xa4\xbe\xe8\xa7\x92')
            angle = self.get_client_aim_angle(entity_id)
            self.client_aim_angle_lab.lab_stat.SetString(str(angle))

    def init_equip_choose_panel(self):
        self.panel.EquipPanel.setVisible(False)
        self.panel.EquipPanel.btn_equip_clear.BindMethod('OnClick', lambda b, t: self.clear_dummy_equip())
        for i in range(3):
            head_idx = 16541 + i
            body_idx = 16511 + i
            foot_idx = 16601 + i
            self.head_equip_btns[i].BindMethod('OnClick', lambda b, t, idx=head_idx: self.set_dummy_equip(idx))
            self.body_equip_btns[i].BindMethod('OnClick', lambda b, t, idx=body_idx: self.set_dummy_equip(idx))
            self.foot_equip_btns[i].BindMethod('OnClick', lambda b, t, idx=foot_idx: self.set_dummy_equip(idx))

    def set_dummy_equip(self, equip_idx):
        target_entity = global_data.battle.get_entity(self.robot_eid)
        if target_entity:
            global_data.player.logic.send_event('E_CALL_SYNC_METHOD', 'set_dummy_equip', (self.robot_eid, equip_idx), True)

    def clear_dummy_equip(self):
        target_entity = global_data.battle.get_entity(self.robot_eid)
        if target_entity:
            global_data.player.logic.send_event('E_CALL_SYNC_METHOD', 'clear_dummy_equip', (self.robot_eid,), True)

    def start_auto_shoot(self):
        target_entity = global_data.battle.get_entity(self.robot_eid)
        if target_entity:
            self.target_pos = target_entity.logic.ev_g_position()
            if target_entity.sd.ref_is_mecha:
                self.target_pos.y += 26
            else:
                self.target_pos.y += 13
            for i in range(5):
                if i < 4:
                    self.panel.SetTimeOut(i * 0.1, lambda : self.rotate_to_target())
                else:
                    self.panel.SetTimeOut(i * 0.1, lambda : self.start_auto_shoot_tick())

    def rotate_to_target(self):
        player = global_data.player.logic
        if not player:
            return
        lpos = get_camera_position()
        if lpos and self.target_pos:
            diff_vec = self.target_pos - lpos
            if diff_vec.length > 0:
                target_yaw = diff_vec.yaw
                target_pitch = diff_vec.pitch
                cur_yaw = player.ev_g_yaw() or 0
                global_data.emgr.fireEvent('camera_set_yaw_event', target_yaw)
                global_data.emgr.fireEvent('camera_set_pitch_event', target_pitch)
                player.send_event('E_DELTA_YAW', target_yaw - cur_yaw)

    def do_auto_shoot(self):
        lplayer = global_data.player.logic
        mecha = lplayer.ev_g_ctrl_mecha_obj()
        self.rotate_to_target()
        if mecha:
            mecha.logic.ev_g_action_down('action1')
        else:
            lplayer.send_event('E_START_AUTO_FIRE')

    def start_auto_shoot_tick(self):
        self.stop_auto_shoot()
        self.run_timer = global_data.game_mgr.get_logic_timer().register(func=self.do_auto_shoot, interval=10)

    def stop_auto_shoot(self):
        self.clear_run_timer()
        lplayer = global_data.player.logic
        mecha = lplayer.ev_g_ctrl_mecha_obj()
        if mecha:
            mecha.logic.send_event('E_ACTION_UP', 'action1')
        else:
            lplayer.send_event('E_STOP_AUTO_FIRE')

    def clear_run_timer(self):
        self.run_timer and global_data.game_mgr.get_logic_timer().unregister(self.run_timer)
        self.run_timer = None
        return