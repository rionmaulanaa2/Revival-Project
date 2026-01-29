# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_ui/MechaAutoAimWidget.py
from __future__ import absolute_import
import six
from six.moves import range
from logic.gcommon.common_const.animation_const import BONE_BIPED_NAME
from common.utils.cocos_utils import neox_pos_to_cocos
from mobile.common.EntityManager import EntityManager
from logic.gcommon.const import PART_WEAPON_POS_MAIN1
from logic.gutils.CameraHelper import get_mecha_camera_type
from logic.client.const.camera_const import POSTURE_STAND
from logic.gcommon.common_const.weapon_const import AUTO_AIM_KIND_UNIQUE, AUTO_AIM_KIND_MULTIPLE
from common.utils.timer import RELEASE
from common.cfg import confmgr
from math import atan, tan, radians, pi
import world
import cc
DEFAULT_FOV = 90.0

def empty_func(*args, **kwargs):
    pass


def default_play_lock_sound_func():
    global_data.sound_mgr.play_sound_2d('Play_ui_notice', ('ui_notice', 'locked_target'))


class MechaAutoAimWidget(object):

    def __init__(self, panel, auto_aim_fov_map=None, show_anim_name='sample_visable_auto', hide_anim_name='', target_refreshed_anim_map=None, miss_target_anim=None, lock_count_refreshed_anim_map=None, play_lock_sound_func=default_play_lock_sound_func, need_play_lock_sound_map=None, lock_node_map=None, reset_node_map=None, lock_node_parent_map=None, update_callback=empty_func, get_target_pos_func=None):
        self.panel = panel
        self.auto_aim_node = self.panel.auto
        self.show_anim_name = show_anim_name
        self.hide_anim_name = hide_anim_name
        self.cur_weapon_pos = PART_WEAPON_POS_MAIN1
        self.auto_aim_fov_map = auto_aim_fov_map if auto_aim_fov_map else {}
        self.default_fov = DEFAULT_FOV
        self.target_refreshed_anim_map = target_refreshed_anim_map if target_refreshed_anim_map else {}
        self.default_target_refreshed_anim = self.target_refreshed_anim_map.get('default', 'auto_lock')
        self.cur_target_refreshed_anim_name = self.target_refreshed_anim_map.get(self.cur_weapon_pos, self.default_target_refreshed_anim)
        self.miss_target_anim = miss_target_anim
        self.lock_count_refreshed_anim_map = lock_count_refreshed_anim_map if lock_count_refreshed_anim_map else {}
        self.cur_lock_count_refreshed_anim_map = self.lock_count_refreshed_anim_map.get(self.cur_weapon_pos, None)
        self.play_lock_sound_func = play_lock_sound_func
        self.need_play_lock_sound_map = need_play_lock_sound_map if need_play_lock_sound_map else {}
        self.cur_need_play_lock_sound = self.need_play_lock_sound_map.get(self.cur_weapon_pos, False)
        self.lock_node_map = lock_node_map if lock_node_map else {}
        for weapon_pos, lock_node in six.iteritems(self.lock_node_map):
            if not isinstance(lock_node, (list, tuple)):
                self.lock_node_map[weapon_pos] = (
                 lock_node,)

        self.default_lock_node = self.lock_node_map.get('default', (self.panel.nd_aim.nd_lock if self.panel.nd_aim else None,))
        self.cur_lock_node = self.lock_node_map.get(self.cur_weapon_pos, self.default_lock_node)
        self.reset_node_map = reset_node_map if reset_node_map else {}
        self.default_reset_node = self.reset_node_map.get('default', self.panel.img_aim)
        self.cur_reset_node = self.reset_node_map.get(self.cur_weapon_pos, self.default_reset_node)
        self.lock_node_parent_map = lock_node_parent_map if lock_node_parent_map else {}
        self.default_lock_node_parent = self.lock_node_parent_map.get('default', self.panel.nd_aim)
        self.cur_lock_node_parent = self.lock_node_parent_map.get(self.cur_weapon_pos, self.default_lock_node_parent)
        self.update_callback = update_callback
        if get_target_pos_func:
            self.get_target_pos_func = get_target_pos_func
        else:
            self.get_target_pos_func = self.default_get_target_pos_func
        self.auto_aim_kind = AUTO_AIM_KIND_UNIQUE
        self.eid_to_free_node_index_map = {}
        self.eid_to_aim_count = {}
        self.max_aim_count = 1
        self.multiple_aim_usable_node_index_set = set()
        for anim_name in six.itervalues(self.target_refreshed_anim_map):
            if isinstance(anim_name, str):
                self.panel.RecordAnimationNodeState(anim_name)
            else:
                for _anim_name in anim_name:
                    self.panel.RecordAnimationNodeState(_anim_name)

        self.miss_target_anim and self.panel.RecordAnimationNodeState(self.miss_target_anim)
        self.aim_target = None
        self.aim_target_compared = None
        self.aim_target_validating = None
        self.update_aim_node_position_timer = None
        self.check_aim_unit_valid_timer = None
        self.lmecha = None
        return

    def on_mecha_set(self, mecha):
        if self.lmecha:
            self.unbind_ui_event()
            self.lmecha = mecha
        if mecha:
            self.lmecha = mecha
            mecha_id = mecha.sd.ref_mecha_id
            skin_id = mecha.ev_g_mecha_fashion_id()
            cam_type = get_mecha_camera_type(mecha_id, skin_id)
            self.default_fov = confmgr.get('camera_config', cam_type, POSTURE_STAND, 'fov', default=self.default_fov)
            mecha.regist_event('E_MECHA_AIM_TARGET', self.update_aim_target)

    def unbind_ui_event(self):
        if self.lmecha and self.lmecha.is_valid():
            self.lmecha.unregist_event('E_MECHA_AIM_TARGET', self.update_aim_target)

    def destroy(self):
        self.panel = None
        self.unbind_ui_event()
        self.lmecha = None
        self.auto_aim_node = None
        self.aim_target = None
        self.aim_target_compared = None
        self.aim_target_validating = None
        self.target_refreshed_anim_map = {}
        self.cur_target_refreshed_anim_name = {}
        self.lock_count_refreshed_anim_map = {}
        self.cur_lock_count_refreshed_anim_map = {}
        self.play_lock_sound_func = None
        self.need_play_lock_sound_map = {}
        self.lock_node_map = {}
        self.default_lock_node = None
        self.cur_lock_node = None
        self.reset_node_map = {}
        self.default_reset_node = None
        self.cur_reset_node = None
        self.lock_node_parent_map = {}
        self.default_lock_node_parent = None
        self.cur_lock_node_parent = None
        self.update_callback = None
        self.get_target_pos_func = None
        self._unregister_check_timer()
        self._unregister_update_timer()
        return

    def refresh_auto_aim_parameters(self, weapon_pos):
        self._unregister_check_timer()
        self.cur_weapon_pos = weapon_pos
        weapon = self.lmecha.share_data.ref_wp_bar_mp_weapons.get(weapon_pos)
        self.auto_aim_kind = weapon.conf('iAutoAimKind', AUTO_AIM_KIND_UNIQUE)
        if self.auto_aim_kind == AUTO_AIM_KIND_MULTIPLE:
            self.max_aim_count = weapon.conf('cCustomParam', {}).get('max_aim_count', 1)
            if self.aim_target is None:
                self.aim_target = []
                self.multiple_aim_usable_node_index_set = set([ i for i in range(0, self.max_aim_count) ])
        elif not self.aim_target:
            self.aim_target = None
        self.cur_target_refreshed_anim_name = self.target_refreshed_anim_map.get(weapon_pos, self.default_target_refreshed_anim)
        self.cur_lock_count_refreshed_anim_map = self.lock_count_refreshed_anim_map.get(weapon_pos)
        self.cur_need_play_lock_sound = self.need_play_lock_sound_map.get(weapon_pos, False)
        self.cur_lock_node = self.lock_node_map.get(weapon_pos, self.default_lock_node)
        self.cur_reset_node = self.reset_node_map.get(weapon_pos, self.default_reset_node)
        self.cur_lock_node_parent = self.lock_node_parent_map.get(weapon_pos, self.default_lock_node_parent)
        return

    def refresh_auto_aim_range_appearance(self, weapon_pos, set_size_directly=False, size_offset=0, use_center_scale=False):
        if not self.auto_aim_node:
            return False
        weapon = self.lmecha.share_data.ref_wp_bar_mp_weapons.get(weapon_pos)
        conf = weapon.conf
        auto_aim_yaw = conf('fAutoAimYaw', 0.0)
        auto_aim_pitch = conf('fAutoAimPitch', 0.0)
        if not (auto_aim_yaw and auto_aim_pitch):
            return False
        width, height = self.panel.GetContentSize()
        x_fov = self.auto_aim_fov_map.get(weapon_pos, self.default_fov)
        d = width / 2.0 / tan(radians(x_fov / 2.0))
        cell = 30
        y_fov = atan(cell / 2.0 / d) * 180 / pi * 2.0
        scale_value = cell / y_fov
        zhunxin = self.auto_aim_node.frame
        if set_size_directly:
            if use_center_scale:
                center_scale_x = zhunxin.center.getScaleX()
                center_scale_y = zhunxin.center.getScaleY()
            else:
                center_scale_x = 1.0
                center_scale_y = 1.0
            width = auto_aim_yaw * scale_value * 2.0 / center_scale_x + size_offset
            height = auto_aim_pitch * scale_value * 2.0 / center_scale_y + size_offset
            zhunxin.center.SetContentSize(width, height)
            zhunxin.center.RecursionReConfPosition()
        else:
            center_pos = zhunxin.center.getPosition()
            offset_list = [
             (
              zhunxin.frame_left_up, (-auto_aim_yaw, auto_aim_pitch)),
             (
              zhunxin.frame_right_up, (auto_aim_yaw, auto_aim_pitch)),
             (
              zhunxin.frame_left_down, (-auto_aim_yaw, -auto_aim_pitch)),
             (
              zhunxin.frame_right_down, (auto_aim_yaw, -auto_aim_pitch)),
             (
              zhunxin.frame_left, (-auto_aim_yaw, 0)),
             (
              zhunxin.frame_right, (auto_aim_yaw, 0))]
            for node, offset in offset_list:
                node.stopAllActions()
                x_offset, y_offset = offset
                pos = cc.Vec2(center_pos.x + x_offset * scale_value, center_pos.y + y_offset * scale_value)
                node.runAction(cc.Sequence.create([
                 cc.MoveTo.create(0.3, pos),
                 cc.CallFunc.create(lambda node=node, pos=pos: node.setPosition(pos))]))

        return True

    def show(self):
        if self.hide_anim_name:
            self.panel.StopAnimation(self.hide_anim_name)
        if self.show_anim_name:
            self.panel.PlayAnimation(self.show_anim_name)
        else:
            self.auto_aim_node and self.auto_aim_node.setVisible(True)

    def hide(self):
        if self.show_anim_name:
            self.panel.StopAnimation(self.show_anim_name)
        if self.hide_anim_name:
            self.panel.PlayAnimation(self.hide_anim_name)
        else:
            if self.auto_aim_kind == AUTO_AIM_KIND_MULTIPLE:
                for anim_name in self.cur_target_refreshed_anim_name:
                    self.panel.StopAnimation(anim_name)
                    self.panel.RecoverAnimationNodeState(anim_name)

            else:
                self.panel.StopAnimation(self.cur_target_refreshed_anim_name)
                self.panel.RecoverAnimationNodeState(self.cur_target_refreshed_anim_name)
            self.auto_aim_node and self.auto_aim_node.setVisible(False)

    def _register_update_timer_uniquely(self):
        self._unregister_update_timer()
        self.update_aim_node_position_timer = global_data.game_mgr.register_logic_timer(self._update_aim_node_position_uniquely, interval=1, times=-1)

    def _register_update_timer_multiply(self):
        self._unregister_update_timer()
        self.update_aim_node_position_timer = global_data.game_mgr.register_logic_timer(self._update_aim_node_position_multiply, interval=1, times=-1)

    def _unregister_update_timer(self):
        if self.update_aim_node_position_timer:
            global_data.game_mgr.unregister_logic_timer(self.update_aim_node_position_timer)
            self.update_aim_node_position_timer = None
        return

    def _validate_aim_target_uniquely(self):
        if isinstance(self.aim_target_validating, str):
            entity = EntityManager.getentity(self.aim_target_validating)
            if entity and entity.logic:
                self.aim_target_validating = entity.logic
                self._update_aim_target_uniquely(entity.logic)
                self.check_aim_unit_valid_timer = None
                return RELEASE
        else:
            self._update_aim_target_uniquely(self.aim_target_validating)
            self.check_aim_unit_valid_timer = None
            return RELEASE
        return

    def _validate_aim_target_multiply(self):
        for index, target in enumerate(self.aim_target_validating):
            if isinstance(target, str):
                entity = EntityManager.getentity(target)
                if not (entity and entity.logic):
                    break
                self.aim_target_validating[index] = target
        else:
            self._update_aim_target_multiply(self.aim_target_validating)
            self.check_aim_unit_valid_timer = None
            return RELEASE

        return

    def _register_check_timer_uniquely(self):
        self._unregister_check_timer()
        self.check_aim_unit_valid_timer = global_data.game_mgr.register_logic_timer(self._validate_aim_target_uniquely, interval=1, times=-1)

    def _register_check_timer_multiply(self):
        self._unregister_check_timer()
        self.check_aim_unit_valid_timer = global_data.game_mgr.register_logic_timer(self._validate_aim_target_multiply, interval=1, times=-1)

    def _unregister_check_timer(self):
        if self.check_aim_unit_valid_timer:
            global_data.game_mgr.unregister_logic_timer(self.check_aim_unit_valid_timer)
            self.check_aim_unit_valid_timer = None
        return

    def _update_aim_target_uniquely(self, target):
        if target == self.aim_target:
            return
        old_aim_target = self.aim_target
        self.aim_target = target
        if target:
            if self.miss_target_anim:
                self.panel.StopAnimation(self.miss_target_anim)
                self.panel.RecoverAnimationNodeState(self.miss_target_anim)
            self.panel.PlayAnimation(self.cur_target_refreshed_anim_name)
            for lock_node in self.cur_lock_node:
                lock_node.setVisible(True)

            self._register_update_timer_uniquely()
            self._update_aim_node_position_uniquely()
            if not old_aim_target and self.cur_need_play_lock_sound:
                self.play_lock_sound_func()
        elif old_aim_target:
            self.panel.StopAnimation(self.cur_target_refreshed_anim_name)
            if self.miss_target_anim:
                self.panel.PlayAnimation(self.miss_target_anim)
            else:
                self.panel.RecoverAnimationNodeState(self.cur_target_refreshed_anim_name)
            pos = self.cur_reset_node.getPosition()
            for lock_node in self.cur_lock_node:
                lock_node.setPosition(pos)
                lock_node.setVisible(False)

            self._unregister_update_timer()

    def _get_free_node_index(self):
        for index in self.multiple_aim_usable_node_index_set:
            self.multiple_aim_usable_node_index_set.remove(index)
            return index

    def _add_free_node_index(self, index):
        self.multiple_aim_usable_node_index_set.add(index)
        self.cur_lock_node[index].lab_lock_count.SetString('0')

    def _update_aim_target_multiply(self, target_list):
        if target_list == self.aim_target:
            return
        old_eid_set = set([ target.id for target in self.aim_target ])
        cur_eid_set = set([ target.id for target in target_list ])
        self.aim_target = target_list
        remove_eid_set = old_eid_set - cur_eid_set
        add_eid_set = cur_eid_set - old_eid_set
        for remove_eid in remove_eid_set:
            index = self.eid_to_free_node_index_map[remove_eid]
            self.panel.StopAnimation(self.cur_target_refreshed_anim_name[index])
            if self.miss_target_anim:
                self.panel.PlayAnimation(self.miss_target_anim[index])
            else:
                self.panel.RecoverAnimationNodeState(self.cur_target_refreshed_anim_name[index])
            pos = self.cur_reset_node.getPosition()
            self.cur_lock_node[index].setPosition(pos)
            self.cur_lock_node[index].setVisible(False)
            self._add_free_node_index(index)
            self.eid_to_free_node_index_map.pop(remove_eid)

        for add_eid in add_eid_set:
            index = self._get_free_node_index()
            self.eid_to_free_node_index_map[add_eid] = index
            if self.miss_target_anim:
                self.panel.StopAnimation(self.miss_target_anim[index])
                self.panel.RecoverAnimationNodeState(self.miss_target_anim[index])
            self.panel.PlayAnimation(self.cur_target_refreshed_anim_name[index])
            self.cur_lock_node[index].setVisible(True)

        if target_list and self.cur_need_play_lock_sound:
            self.play_lock_sound_func()
        self.eid_to_aim_count = {}
        for target in target_list:
            eid = target.id
            if eid not in self.eid_to_aim_count:
                self.eid_to_aim_count[eid] = 1
            else:
                self.eid_to_aim_count[eid] += 1

        if cur_eid_set:
            not old_eid_set and self._register_update_timer_multiply()
            add_eid_set and self._update_aim_node_position_multiply()
        else:
            self._unregister_update_timer()

    @staticmethod
    def default_get_target_pos_func(target):
        model = target.ev_g_model()
        if model:
            matrix = model.get_socket_matrix('part_point1', world.SPACE_TYPE_WORLD)
            if matrix:
                return matrix.translation
            else:
                return model.world_position

        return None

    def _update_aim_node_position_uniquely(self):
        if self.aim_target and self.aim_target.is_valid():
            scn = global_data.game_mgr.scene
            if not scn:
                return
            camera = scn.active_camera
            if not camera:
                return
            aim_pos = self.get_target_pos_func(self.aim_target)
            if aim_pos is None:
                return
            x, y = camera.world_to_screen(aim_pos)
            pos = cc.Vec2(*neox_pos_to_cocos(x, y))
            pos = self.cur_lock_node_parent.convertToNodeSpace(pos)
            for lock_node in self.cur_lock_node:
                lock_node.setPosition(pos)

            self.update_callback(aim_pos)
        return

    def _update_aim_node_position_multiply(self):
        updated_eid_set = set()
        for target in self.aim_target:
            eid = target.id
            if target.is_valid() and eid not in updated_eid_set:
                scn = global_data.game_mgr.scene
                if not scn:
                    return
                camera = scn.active_camera
                if not camera:
                    return
                aim_pos = self.get_target_pos_func(target)
                if aim_pos is None:
                    continue
                x, y = camera.world_to_screen(aim_pos)
                pos = cc.Vec2(*neox_pos_to_cocos(x, y))
                pos = self.cur_lock_node_parent.convertToNodeSpace(pos)
                node_index = self.eid_to_free_node_index_map[target.id]
                self.cur_lock_node[node_index].setPosition(pos)
                aim_count = self.eid_to_aim_count[eid]
                nd_lab = self.cur_lock_node[node_index].lab_lock_count
                new_text = '%d' % aim_count
                if aim_count > 1:
                    if new_text != nd_lab.getString():
                        self.panel.PlayAnimation(self.cur_lock_count_refreshed_anim_map[node_index])
                    nd_lab.setVisible(True)
                else:
                    nd_lab.setVisible(False)
                nd_lab.SetString(new_text)
                updated_eid_set.add(eid)

        return

    def update_aim_target(self, target, weapon_pos=PART_WEAPON_POS_MAIN1, **kwargs):
        if weapon_pos != self.cur_weapon_pos:
            return
        else:
            if target != self.aim_target_compared:
                self.aim_target_compared = target
                self.aim_target_validating = target
                if self.auto_aim_kind == AUTO_AIM_KIND_UNIQUE:
                    if self._validate_aim_target_uniquely() is None:
                        self._register_check_timer_uniquely()
                elif self._validate_aim_target_multiply() is None:
                    self._register_check_timer_multiply()
            return