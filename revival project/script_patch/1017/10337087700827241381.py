# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_character_ctrl/ComAnimMgr.py
from __future__ import absolute_import
from __future__ import print_function
import six
import six_ex
from six.moves import range
import world
import math3d
import C_file
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.common_const.character_anim_const import *
import weakref
import common.utils.timer as timer
import logic.gcommon.common_utils.bcast_utils as bcast
from common.framework import Functor
from common.const.common_const import FORCE_DELTA_TIME
from logic.gcommon.common_const.animation_const import FULL_BODY_NODE_NAME, check_update_position_parameters, check_cache_mecha_animation
from logic.gcommon.item.item_const import FASHION_POS_SUIT, FASHION_POS_WEAPON_SFX
from logic.gutils.client_unit_tag_utils import register_unit_tag
from common.cfg import confmgr
import math
CHECK_ANIM_VALID = True
DEFAULT_ANIM_NAME = 'idle'
DEF_NODES_YAW = {4: [
     -1.57, 1.57, 0, 0]
   }
UP_BODY_NODES = {1: [
     'up_body_action.single'],
   7: [
     '7.up_body_action_fl', '7.up_body_action_fr', '7.up_body_action_f', '7.up_body_action_bl', '7.up_body_action_br', '7.up_body_action_b', '7.up_body_action_o'],
   9: [
     '9.up_body_action_fl', '9.up_body_action_fr', '9.up_body_action_f', '9.up_body_action_bl', '9.up_body_action_br', '9.up_body_action_b', '9.up_body_action_l', '9.up_body_action_r', '9.up_body_action_o']
   }
LOWER_UP_BODY_NODES = {1: [
     'lower.up_body_action.single'],
   6: [
     '6.lower.up_body_action_fl', '6.lower.up_body_action_fr', '6.lower.up_body_action_f', '6.lower.up_body_action_bl', '6.lower.up_body_action_br', '6.lower.up_body_action_b'],
   7: [
     '7.lower.up_body_action_fl', '7.lower.up_body_action_fr', '7.lower.up_body_action_f', '7.lower.up_body_action_bl', '7.lower.up_body_action_br', '7.lower.up_body_action_b', '7.lower.up_body_action_o']
   }
LOW_BODY_NODES = {1: [
     'low_body_action.single'],
   2: [
     '2.low_body_action_f', '2.low_body_action_b'],
   4: [
     '4.low_body_action_l', '4.low_body_action_r', '4.low_body_action_f', '4.low_body_action_b'],
   6: [
     '6.low_body_action_fl', '6.low_body_action_fr', '6.low_body_action_f', '6.low_body_action_bl', '6.low_body_action_br', '6.low_body_action_b'],
   7: [
     '7.low_body_action_fl', '7.low_body_action_fr', '7.low_body_action_f', '7.low_body_action_bl', '7.low_body_action_br', '7.low_body_action_b', '7.low_body_action_o'],
   8: [
     '8.low_body_action_fl', '8.low_body_action_fr', '8.low_body_action_f', '8.low_body_action_bl', '8.low_body_action_br', '8.low_body_action_b', '8.low_body_action_l', '8.low_body_action_r'],
   9: [
     '9.low_body_action_fl', '9.low_body_action_fr', '9.low_body_action_f', '9.low_body_action_bl', '9.low_body_action_br', '9.low_body_action_b', '9.low_body_action_l', '9.low_body_action_r', '9.low_body_action_o']
   }
DIR_SUFIX = {1: [
     ''],
   2: [
     '_f', '_b'],
   4: [
     '_l', '_r', '_f', '_b'],
   6: [
     '_fl', '_fr', '_f', '_bl', '_br', '_b'],
   7: [
     '_fl', '_fr', '_f', '_bl', '_br', '_b', ''],
   8: [
     '_fl', '_fr', '_f', '_bl', '_br', '_b', '_l', '_r'],
   9: [
     '_fl', '_fr', '_f', '_bl', '_br', '_b', '_l', '_r', '']
   }
BLEND_NODE = {2: 'low_body_action.blend_2',
   4: 'low_body_action.blend_4',
   6: 'low_body_action.blend_6',
   8: 'low_body_action.blend_8',
   7: {UP_BODY: 'up_body_action.blend_7',LOW_BODY: 'low_body_action.blend_7',LOWER_UP_BODY: 'lower.up_body_action.blend_7'},9: {UP_BODY: 'up_body_action.blend_9',LOW_BODY: 'low_body_action.blend_9'}}
SINGLE_NODE = {UP_BODY: UP_BODY_NODES[1][0],
   LOW_BODY: LOW_BODY_NODES[1][0],
   LOWER_UP_BODY: LOWER_UP_BODY_NODES[1][0]
   }
UP_BODY_SCALE_NODE = [
 'up_body_action.single', 'up_body_action.blend_7', 'up_body_action.blend_9']
LOW_BODY_SCALE_NODE = ['low_body_action.single', 'low_body_action.blend_2', 'low_body_action.blend_6', 'low_body_action.blend_4', 'low_body_action.blend_7', 'low_body_action.blend_8', 'low_body_action.blend_9']
LOWER_UP_BODY_SCALE_NODE = ['lower.up_body_action.single', 'lower.up_body_action.blend_7']
EXTERN_BODY_1_SCALE_NODE = ['extern_body_action_1']
MASK_BONE_SUBTREE_CONFIG = {FULL_BODY_BONE: FULL_BODY_BONE_CONFIG,
   DEFAULT_UP_BODY_BONE: DEFAULT_UP_BODY_CONFIG,
   3: (
     ('biped root', 0), ('biped spine01', 1)),
   4: (
     ('biped root', 0), ('biped_bone13', 1), ('biped_bone16', 1)),
   5: (('biped root', 0), ),
   6: (
     ('biped root', 0), ('biped_bone24', 1), ('biped_bone17', 1))
   }
PART_2_SELECT_NODE_DICT = {UP_BODY: 'up_body_action',LOW_BODY: 'low_body_action',LOWER_UP_BODY: 'lower_up_body_action'}
PART_2_SCALE_NODE_DICT = {UP_BODY: UP_BODY_SCALE_NODE,LOW_BODY: LOW_BODY_SCALE_NODE,LOWER_UP_BODY: LOWER_UP_BODY_SCALE_NODE,EXTERN_BODY_1: EXTERN_BODY_1_SCALE_NODE}
MAX_TWIST_YAW = 180
UP_ANIM_DIR_UNITS_TAG_VALUE = register_unit_tag(('LMecha', 'LMechaRobot', 'LArtTestMecha',
                                                 'LAvatar', 'LPuppet', 'LPuppetRobot'))
UNUSUAL_UP_BODY_NODES = [
 [
  '5.up_body_unusual_action_f', '5.up_body_unusual_action_b'], ['5.up_body_unusual_action_r', '5.up_body_unusual_action_l']]
UNUSUAL_BLEND_NODES = 'up_body_unusual_action.blend_5'
UNUSUAL_DIR_SUFIX = ['_1', '_2']
UNUSUAL_CENTER_NODE = '5.up_body_unusual_action'
UNUSUAL_UP_PARAMETERS = 50

class ComAnimMgr(UnitCom):
    BIND_EVENT = {'E_ANIMATOR_LOADED': 'on_load_animator_complete',
       'E_ENABLE_ANIM': 'install_anim_event',
       'E_POST_ANIM_LIST_ACTION': 'post_anim_list_to_animator',
       'E_POST_ACTION': 'post_anim_to_animator',
       'E_CLEAR_UP_BODY_ANIM': 'clear_up_body_anim',
       'E_ENABLE_ANIM_LOG': 'enable_log',
       'E_SWITCH_MODEL': 'on_switch_model'
       }
    UPBODY_DICT = {UP_BODY: ['up_body_action.blend_9', 'up_body_action.blend_7', 'up_body_action.single'],EXTERN_BODY_1: ['extern_body_action_1']}
    ADD_NODE_LIST = set(('add.up_body.diff', 'add.up_body.base'))
    PART_2_NODE_DICT = {UP_BODY: 'Entry.up_body',LOWER_UP_BODY: 'Entry.lower.up_body',LOW_BODY: 'Entry.low_body',EXTERN_BODY_1: 'Entry.extern_body_1',UP_BODY_SELECT: 'up_body_action',LOW_BODY_SELECT: 'low_body_action'}

    def __init__(self):
        super(ComAnimMgr, self).__init__()
        self._animator = None
        self._action_list = []
        self._last_action = None
        self.sd.ref_up_body_anim = None
        self.sd.ref_low_body_anim = None
        self.sd.ref_low_body_anim_dir_type = 1
        self.sd.ref_anim_rate = {UP_BODY: 1.0,LOW_BODY: 1.0}
        self.sd.ref_lower_up_body_anim = None
        self.sd.ref_up_body_mask_index = DEFAULT_UP_BODY_BONE
        self.sd.ref_tmp_forbid_anim_dir = False
        self.sd.ref_forbid_zero_anim_dir = True
        self._default_up_body_anim = None
        self._default_up_body_anim_param = {'anim_dir': 1,'anim_rate': 1.0}
        self.anim_name_set = set()
        self.sd.ref_anim_param = {}
        self._disable_intrp_mode = True
        self._enable_log = False
        self._enable_event = False
        self._twist_yaw_enable = False
        self._twist_yaw_register = False
        self._twist_pitch_enable = False
        self._twist_pitch_register = False
        self._twist_root_yaw_enable = False
        self._twist_root_yaw_register = False
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComAnimMgr, self).init_from_dict(unit_obj, bdict)
        if 'last_action' in bdict:
            self._last_action = bdict['last_action']
        self.use_skin_anim_map = False
        self.skin_anim_map = {}
        mecha_fashion = bdict.get('mecha_fashion', {})
        skin_id = mecha_fashion.get(FASHION_POS_SUIT, None)
        if not skin_id:
            from logic.gutils.dress_utils import DEFAULT_CLOTHING_ID
            skin_id = DEFAULT_CLOTHING_ID
        skin_anim_conf = confmgr.get('mecha_skin_anim')
        anim_index = skin_anim_conf['skin_anim_index'].get(str(skin_id), None)
        if anim_index:
            self.use_skin_anim_map = True
            self.skin_anim_map = skin_anim_conf['skin_anim_info'][anim_index]
        self._disable_intrp_mode = not global_data.low_fps_switch_on or self.ev_g_is_avatar()
        self.sd.ref_forbid_zero_anim_dir = True
        return

    def on_init_complete(self):
        pass

    def is_same(self, a, b):
        if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
            if len(a) != len(b):
                return False
            for i in range(len(a)):
                if not self.is_same(a[i], b[i]):
                    return False

            return True
        else:
            return a == b

    def get_subtree_index(self, subtree):
        for index, one_config_subtree in six.iteritems(MASK_BONE_SUBTREE_CONFIG):
            if self.is_same(one_config_subtree, subtree):
                return index

        return 1

    def _reset_anim_map(self):
        skin_id = self.ev_g_mecha_fashion_id()
        skin_anim_conf = confmgr.get('mecha_skin_anim')
        anim_index = skin_anim_conf['skin_anim_index'].get(str(skin_id), None)
        if anim_index:
            self.use_skin_anim_map = True
            self.skin_anim_map = skin_anim_conf['skin_anim_info'][anim_index]
        return

    def on_load_animator_complete(self, *args):
        animator = self.ev_g_animator()
        if not animator:
            return
        else:
            model = self.ev_g_model()
            if model:
                self.anim_name_set = set(model.get_anim_names())
            self._reset_anim_map()
            self._animator = animator
            _y_twist_node = animator.find('turn_y_up_body')
            if _y_twist_node and not self.sd.ref_is_refreshing_whole_model:
                self.regist_event('E_TWIST_YAW', self.on_set_y_twistnode)
                self.regist_event('G_TWIST_YAW', self.on_get_y_twistnode)
                self._twist_yaw_enable = True
                self._twist_yaw_register = True
            _x_twist_node = animator.find('turn_x_up_body')
            if _x_twist_node and not self.sd.ref_is_refreshing_whole_model:
                self.regist_event('E_TWIST_PITCH', self.on_set_x_twistnode)
                self.regist_event('G_TWIST_PITCH', self.on_get_x_twistnode)
                self._twist_pitch_enable = True
                self._twist_pitch_register = True
            _y_root_twist_node = animator.find('turn_y_full_body')
            if _y_root_twist_node and not self.sd.ref_is_refreshing_whole_model:
                self.regist_event('E_TWIST_ROOT_YAW', self.on_set_y_root_twistnode)
                self.regist_event('G_TWIST_ROOT_YAW', self.on_get_y_root_twistnode)
                self._twist_root_yaw_enable = True
                self._twist_root_yaw_register = True
            is_avatar = self.ev_g_is_avatar()
            if self.sd.ref_mecha_id:
                check_update_position_parameters(animator, self.sd.ref_mecha_id)
                check_cache_mecha_animation(is_avatar, animator, self.sd.ref_mecha_id, model)
            elif is_avatar:
                animator.TrySetAsyncLoad(False)
            self.on_change_anim_move_dir(0, 0)
            self.send_event('E_SUPPORT_TWIST_YAW', _y_twist_node is not None)
            self.send_event('E_SUPPORT_TWIST_PITCH', _x_twist_node is not None)
            not self.sd.ref_is_refreshing_whole_model and self.install_anim_event()
            self.post_anim_to_animator(DEFAULT_ANIM_NAME, LOW_BODY, 1, loop=True)
            self.send_event('E_ANIM_MGR_INIT')
            self.restore_last_action()
            return

    def on_switch_model(self, model):
        animator = self.ev_g_animator()
        if not animator:
            return
        old_animator = self.ev_g_mecha_original_animator() if self.sd.ref_using_second_model else self.ev_g_mecha_second_animator()
        old_node = old_animator.find(FULL_BODY_NODE_NAME)
        if old_node:
            cur_node = animator.find(FULL_BODY_NODE_NAME)
            if cur_node:
                cur_node.timeScale = old_node.timeScale
        self.anim_name_set = set(model.get_anim_names())
        self._reset_anim_map()
        self._animator = animator

    def restore_last_action(self):
        if global_data.player and global_data.player.id == self.unit_obj.sd.ref_driver_id:
            return
        if self._last_action:
            for action in self._last_action:
                if not action:
                    continue
                args, kwargs = action
                self.send_event('E_POST_ACTION', *args, **kwargs)

    def restore_anim_trigger_effect(self):
        if global_data.player and global_data.player.id == self.unit_obj.sd.ref_driver_id:
            return
        if self._last_action:
            for action in self._last_action:
                if not action:
                    continue
                args, kwargs = action
                anim_name, part, dir_type = args
                if kwargs.get('need_trigger_anim_effect', True):
                    force_trigger_effect = kwargs.get('force_trigger_effect', False)
                    socket_index = kwargs.get('socket_index', -1)
                    self.send_event('E_TRIGGER_ANIM_EFFECT', anim_name, part, force_trigger_effect, socket_index)

    def install_anim_event(self):
        animator = self.ev_g_animator()
        if not animator:
            return
        if self._enable_event:
            return
        self._enable_event = True
        self.regist_event('E_POST_BIND_OBJ_ACTION', self.post_anim_to_bind_obj_animator)
        self.regist_event('E_CHANGE_ANIM_BLEND_SCALE', self.on_change_anim_blend_scale)
        self.regist_event('E_CHANGE_ANIM_MOVE_DIR', self.on_change_anim_move_dir)
        self.regist_event('G_EIGHT_DIR', self.calculate_eight_dir)
        self.regist_event('E_ANIM_RATE', self.on_change_anim_rate)
        self.regist_event('E_ANIM_PHASE', self.on_change_anim_phase)
        self.regist_event('G_ANIM_PHASE', self.get_anim_phase)
        self.regist_event('E_TWIST_PITCH_PARAM', self.on_set_x_twistnode_param)
        self.regist_event('E_TWIST_YAW_PARAM', self.on_set_y_twistnode_param)
        self.regist_event('E_UPBODY_BONE', self.on_set_upbody_bone)
        self.regist_event('E_SET_SMOOTH_DURATION', self.set_smooth_duration)
        self.regist_event('E_SET_SMOOTH_SPEED', self.set_smooth_speed)
        self.regist_event('E_POST_EXTERN_ACTION', self.on_post_extern_action)
        self.regist_event('E_POST_ADD_ANIMATION', self.on_post_add_anim)
        self.regist_event('E_SET_BLEND_NODE_SMOOTH_DURATION', self.set_blend_node_smooth_duration)
        self.regist_event('E_SET_DEFAULT_UP_BODY_ANIM', self.set_default_up_body_anim)
        self.regist_event('G_DEFAULT_UP_BODY_ANIM', self.get_default_up_body_anim)
        self.regist_event('G_IS_SHOWING_DEFAULT_UP_BODY_ANIM', self.is_playing_default_up_body_anim)
        self.regist_event('E_DISABLE_ANIM', self.uninstall_anim_event)
        self.regist_event('E_USE_CACHE_POS', self.use_cache_pos)
        self.regist_event('E_PAUSE_ANIM', self.pause)
        self.regist_event('E_RESUME_ANIM', self.resume)
        self.regist_event('E_RESTORE_ANIM_TRIGGER_EFFECT', self.restore_anim_trigger_effect)
        if self._twist_yaw_enable and not self._twist_yaw_register:
            self.regist_event('E_TWIST_YAW', self.on_set_y_twistnode)
            self.regist_event('G_TWIST_YAW', self.on_get_y_twistnode)
            self._twist_yaw_register = True
        if self._twist_pitch_enable and not self._twist_pitch_register:
            self.regist_event('E_TWIST_PITCH', self.on_set_x_twistnode)
            self.regist_event('G_TWIST_PITCH', self.on_get_x_twistnode)
            self._twist_pitch_register = True
        if self._twist_root_yaw_enable and not self._twist_root_yaw_register:
            self.regist_event('E_TWIST_ROOT_YAW', self.on_set_y_root_twistnode)
            self.regist_event('G_TWIST_ROOT_YAW', self.on_get_y_root_twistnode)
            self._twist_root_yaw_register = True

    def uninstall_anim_event(self):
        self._enable_event = False
        self.unregist_event('E_POST_BIND_OBJ_ACTION', self.post_anim_to_bind_obj_animator)
        self.unregist_event('E_CHANGE_ANIM_BLEND_SCALE', self.on_change_anim_blend_scale)
        self.unregist_event('E_CHANGE_ANIM_MOVE_DIR', self.on_change_anim_move_dir)
        self.unregist_event('G_EIGHT_DIR', self.calculate_eight_dir)
        self.unregist_event('E_ANIM_RATE', self.on_change_anim_rate)
        self.unregist_event('E_ANIM_PHASE', self.on_change_anim_phase)
        self.unregist_event('G_ANIM_PHASE', self.get_anim_phase)
        self.unregist_event('E_TWIST_PITCH_PARAM', self.on_set_x_twistnode_param)
        self.unregist_event('E_TWIST_YAW_PARAM', self.on_set_y_twistnode_param)
        self.unregist_event('E_UPBODY_BONE', self.on_set_upbody_bone)
        self.unregist_event('E_SET_SMOOTH_DURATION', self.set_smooth_duration)
        self.unregist_event('E_SET_SMOOTH_SPEED', self.set_smooth_speed)
        self.unregist_event('E_POST_EXTERN_ACTION', self.on_post_extern_action)
        self.unregist_event('E_POST_ADD_ANIMATION', self.on_post_add_anim)
        self.unregist_event('E_SET_BLEND_NODE_SMOOTH_DURATION', self.set_blend_node_smooth_duration)
        self.unregist_event('E_SET_DEFAULT_UP_BODY_ANIM', self.set_default_up_body_anim)
        self.unregist_event('G_DEFAULT_UP_BODY_ANIM', self.get_default_up_body_anim)
        self.unregist_event('G_IS_SHOWING_DEFAULT_UP_BODY_ANIM', self.is_playing_default_up_body_anim)
        if self._twist_yaw_register:
            self.unregist_event('E_TWIST_YAW', self.on_set_y_twistnode)
            self.unregist_event('G_TWIST_YAW', self.on_get_y_twistnode)
            self._twist_yaw_register = False
        if self._twist_pitch_register:
            self.unregist_event('E_TWIST_PITCH', self.on_set_x_twistnode)
            self.unregist_event('G_TWIST_PITCH', self.on_get_x_twistnode)
            self._twist_pitch_register = False
        if self._twist_root_yaw_register:
            self.unregist_event('E_TWIST_ROOT_YAW', self.on_set_y_root_twistnode)
            self.unregist_event('G_TWIST_ROOT_YAW', self.on_get_y_root_twistnode)
            self._twist_root_yaw_register = False
        self.unregist_event('E_DISABLE_ANIM', self.uninstall_anim_event)
        self.unregist_event('E_USE_CACHE_POS', self.use_cache_pos)
        self.unregist_event('E_PAUSE_ANIM', self.pause)
        self.unregist_event('E_RESUME_ANIM', self.resume)
        self.unregist_event('E_RESTORE_ANIM_TRIGGER_EFFECT', self.restore_anim_trigger_effect)

    def destroy(self):
        super(ComAnimMgr, self).destroy()
        self.uninstall_anim_event()
        self._animator = None
        return

    def pause(self):
        if not self._animator:
            return
        self._animator.pause()

    def resume(self):
        if not self._animator:
            return
        self._animator.resume()

    def use_cache_pos(self, part, dir_type, **kwargs):
        anim_nodes = UP_BODY_NODES
        if part == LOWER_UP_BODY:
            anim_nodes = LOWER_UP_BODY_NODES
        elif part == LOW_BODY:
            anim_nodes = LOW_BODY_NODES
        if dir_type not in anim_nodes:
            log_error('Invalid dir_type {0} for {1} body anim!!!!!!!!!'.format(dir_type, 'up' if part == UP_BODY else 'low'))
            return
        else:
            anim_nodes = anim_nodes[dir_type]
            if dir_type in BLEND_NODE:
                node_name = BLEND_NODE[dir_type]
                if isinstance(node_name, dict):
                    node_name = node_name.get(part, '')
                node = self._animator.find(node_name)
                if not node:
                    return
                cache_pos_blend_time = kwargs.get('cache_pos_blend_time', 0.2)
                node.SetMaxBlendOutTime(cache_pos_blend_time)
                if getattr(node, 'UseCachedPosInterpolate', None):
                    node.UseCachedPosInterpolate()
            return

    def enable_log(self, enable):
        self._enable_log = enable

    def post_anim_list_to_animator(self, anim_list, dir_x, dir_y, **kwargs):
        if not self._animator:
            return
        if not anim_list:
            return
        self.sd.ref_up_body_anim = anim_list[0]
        for i, anim_name in enumerate(anim_list):
            extra_nodes = UNUSUAL_UP_BODY_NODES[i]
            for j, node_name in enumerate(extra_nodes):
                node = self._animator.find(node_name)
                if not node:
                    continue
                node.phase = 0
                final_anim_name = anim_name + UNUSUAL_DIR_SUFIX[j]
                self._animator.replace_clip_name(node_name, final_anim_name, False, force=True)

        self._animator.replace_clip_name(UNUSUAL_CENTER_NODE, anim_list[0], False, force=True)
        self._animator.SetInt(UP_BODY_ENABLE, 1)
        self._animator.SetInt(UP_BODY_DIR_TYPE, UNUSUAL_UP_PARAMETERS)
        self._animator.SetFloat('up_extra_x', dir_x)
        self._animator.SetFloat('up_extra_y', dir_y)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', (bcast.E_POST_ANIM_LIST_ACTION, (anim_list, dir_x, dir_y), kwargs), True, False, True)

    def post_anim_to_animator(self, anim_name, part, dir_type, **kwargs):
        if self.use_skin_anim_map and anim_name in self.skin_anim_map:
            anim_name = self.skin_anim_map[anim_name]
        if not self._animator:
            if not self._last_action:
                self._last_action = []
            else:
                not_add_on_have_server_action = kwargs.get('not_add_on_have_server_action', False)
                if not_add_on_have_server_action:
                    return
            args = [
             anim_name, part, dir_type]
            action = [args, kwargs]
            self._last_action.append(action)
            return
        if not anim_name:
            return
        anim_nodes = UP_BODY_NODES
        if part == LOWER_UP_BODY:
            anim_nodes = LOWER_UP_BODY_NODES
        elif part == LOW_BODY:
            anim_nodes = LOW_BODY_NODES
        if dir_type not in anim_nodes:
            log_error('Invalid dir_type {0} for {1} body anim!!!!!!!!!'.format(dir_type, 'up' if part == UP_BODY else 'low'))
            return
        else:
            if part == UP_BODY:
                self.sd.ref_up_body_anim = anim_name
            elif part == LOWER_UP_BODY:
                self.sd.ref_lower_up_body_anim = anim_name
            elif part == LOW_BODY:
                self.sd.ref_low_body_anim = anim_name
                self.sd.ref_low_body_anim_dir_type = dir_type
            anim_nodes = anim_nodes[dir_type]
            keep_phase = kwargs.get('keep_phase', False)
            if dir_type in BLEND_NODE:
                node_name = BLEND_NODE[dir_type]
                if isinstance(node_name, dict):
                    node_name = node_name.get(part, '')
                if not node_name:
                    log_error('Invalid dir_type {0} for {1} node name!!!!!!!!!'.format(dir_type, 'up' if part == UP_BODY else ('lower_up' if part == LOWER_UP_BODY else 'low')))
                node = self._animator.find(node_name)
                if node:
                    use_cache_pos = kwargs.get('use_cache_pos', False)
                    if use_cache_pos:
                        self.use_cache_pos(part, dir_type, **kwargs)
                    if not keep_phase:
                        phase = kwargs.get('phase', 0) or 0
                        node.phase = phase
            if 'timeScale' in kwargs:
                self.on_change_anim_rate(part, kwargs['timeScale'])
                del kwargs['timeScale']
            ignore_sufix = kwargs.get('ignore_sufix', False)
            blend_time = kwargs.get('blend_time', 0.2)
            force_upate_anim = kwargs.get('force_upate_anim', True)
            yaw_list = kwargs.get('yaw_list', [])
            need_set_yaw = bool(yaw_list)
            def_node_yaw = DEF_NODES_YAW.get(dir_type)
            has_def_yaw = bool(def_node_yaw)
            for idx, node_name in enumerate(anim_nodes):
                node = self._animator.find(node_name)
                if node:
                    yaw = 0
                    if need_set_yaw:
                        yaw = yaw_list[idx]
                    elif has_def_yaw:
                        yaw = def_node_yaw[idx]
                    else:
                        yaw = 0
                    node.SetMaxBlendOutTime(blend_time)
                    dir_anim_name = anim_name
                    if not ignore_sufix:
                        dir_anim_name = anim_name + DIR_SUFIX[dir_type][idx]
                    dir_anim_name = self.check_anim_name(dir_anim_name)
                    self._animator.replace_clip_name(node_name, dir_anim_name, keep_phase, force=force_upate_anim)
                    node.loop = False
                    node.yaw = yaw
                    for k, v in six.iteritems(kwargs):
                        if hasattr(node, k):
                            if v is None:
                                print(('test--post_anim_to_animator--error--anim_name =', anim_name, '--part =', DEBUG_PART_DESC.get(part, part), '--dir_type =', dir_type, '--k =', k, '--v =', v))
                                continue
                            setattr(node, k, v)

            part_enable = UP_BODY_ENABLE
            if part == LOWER_UP_BODY:
                part_enable = LOWER_UP_BODY_ENABLE
            elif part == LOW_BODY:
                part_enable = LOW_BODY_ENABLE
            self._animator.SetInt(part_enable, 1)
            part_dir = UP_BODY_DIR_TYPE
            if part == LOWER_UP_BODY:
                part_dir = LOWER_UP_BODY_DIR_TYPE
            elif part == LOW_BODY:
                part_dir = LOW_BODY_DIR_TYPE
            self._animator.SetInt(part_dir, dir_type)
            if 'blend_time' in kwargs:
                if part == UP_BODY or part == LOWER_UP_BODY:
                    node_name = self.PART_2_NODE_DICT.get(part, '')
                    if node_name:
                        node = self._animator.find(node_name)
                        if node:
                            blend_time = kwargs['blend_time']
                            self.set_smooth_speed(part, blend_time)
            if kwargs.get('need_trigger_anim_effect', True):
                force_trigger_effect = kwargs.get('force_trigger_effect', False)
                socket_index = kwargs.get('socket_index', -1)
                self.send_event('E_TRIGGER_ANIM_EFFECT', anim_name, part, force_trigger_effect, socket_index)
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt_crs_server', (bcast.E_POST_ACTION, (anim_name, part, dir_type), dict(kwargs)), True, False, True)
            return

    def post_anim_to_bind_obj_animator(self, bind_obj_type, anim_name, dir_type, **kwargs):
        if not anim_name:
            return
        else:
            animator = None
            model = None
            if bind_obj_type == BIND_OBJ_TYPE_SKATE:
                animator = self.ev_g_skate_animator()
                model = self.ev_g_skate_model()
            else:
                if bind_obj_type == BIND_OBJ_TYPE_PARACHUTE:
                    animator = self.ev_g_parachute_animator()
                    model = self.ev_g_parachute_model()
                if not animator or not model:
                    return
                anim_nodes = LOW_BODY_NODES
                if dir_type not in anim_nodes:
                    log_error('test--post_anim_to_bind_obj_animator--Invalid dir_type {0} for {1} body anim!!!!!!!!!'.format(dir_type, 'up' if part == UP_BODY else 'low'))
                    return
            anim_nodes = anim_nodes[dir_type]
            if dir_type in BLEND_NODE:
                node_name = BLEND_NODE[dir_type]
                if not node_name:
                    log_error('Invalid dir_type {0} !!!!!!!!!'.format(dir_type))
                node = animator.find(node_name)
                if node:
                    node.phase = 0
            if 'timeScale' in kwargs:
                anim_rate = kwargs['timeScale']
                for node_name in LOW_BODY_SCALE_NODE:
                    node = animator.find(node_name)
                    if node:
                        node.timeScale = anim_rate

            ignore_sufix = kwargs.get('ignore_sufix', False)
            blend_time = kwargs.get('blend_time', 0.2)
            keep_phase = kwargs.get('keep_phase', False)
            yaw_list = kwargs.get('yaw_list', [])
            postfix_id = kwargs.get('postfix_id', 0)
            force_upate_anim = kwargs.get('force_upate_anim', True)
            for idx, node_name in enumerate(anim_nodes):
                node = animator.find(node_name)
                yaw = 0
                if yaw_list:
                    yaw = yaw_list[idx]
                if node:
                    node.yaw = yaw
                    node.SetMaxBlendOutTime(blend_time)
                    dir_anim_name = anim_name
                    if not ignore_sufix:
                        dir_anim_name = anim_name + DIR_SUFIX[dir_type][idx]
                    if postfix_id:
                        new_anim_name = dir_anim_name + '_' + str(postfix_id)
                        if model.has_anim(new_anim_name):
                            dir_anim_name = new_anim_name
                    old_phase = node.phase
                    animator.replace_clip_name(node_name, dir_anim_name, keep_phase, force=force_upate_anim)
                    node.loop = False
                    for k, v in six.iteritems(kwargs):
                        if hasattr(node, k):
                            setattr(node, k, v)

            animator.SetInt(LOW_BODY_DIR_TYPE, dir_type)
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt_crs_server', (bcast.E_POST_BIND_OBJ_ACTION, (bind_obj_type, anim_name, dir_type), kwargs), True, False, True)
            return

    def set_smooth_speed(self, part, smoothWeightsDuration):
        node_name = self.PART_2_NODE_DICT.get(part, None)
        if not node_name:
            log_error('test--set_smooth_speed--[error] part = ' + str(part) + '--not have node')
            return
        else:
            if not self._animator:
                return
            node = self._animator.find(node_name)
            if not node:
                return
            if node.nodeType not in ('StateMachineNode', 'Select', 'Blend'):
                return
            if smoothWeightsDuration <= 0:
                smoothWeightsDuration = 0.0001
            all_child_states = node.GetChildStates()
            for index, one_child_state in enumerate(all_child_states):
                speed = (one_child_state.targetWeight - one_child_state.currentWeight) / smoothWeightsDuration
                one_child_state.SetSmoothWeightSpeed(speed)

            return

    def set_smooth_duration(self, part, smoothWeightsDuration):
        node_name = self.PART_2_NODE_DICT.get(part, None)
        if not node_name:
            log_error('[error] part = ' + str(part) + '--not have node')
            return
        else:
            node = self._animator.find(node_name)
            if node:
                node.smoothWeightsDuration = smoothWeightsDuration
            if LOW_BODY_SELECT == part or UP_BODY_SELECT == part or LOW_UP_BODY_SELECT == part:
                global_data.game_mgr.register_logic_timer(lambda : self.recover_smooth_duration(part, 0.2), 0.1, times=1, mode=timer.CLOCK)
            return

    def recover_smooth_duration(self, part, smoothWeightsDuration):
        node_name = self.PART_2_NODE_DICT.get(part, None)
        if not node_name:
            log_error('[error] part = ' + str(part) + '--not have node')
            return
        else:
            if not self._animator:
                return
            node = self._animator.find(node_name)
            if node:
                node.smoothWeightsDuration = smoothWeightsDuration
            return

    def set_blend_node_smooth_duration(self, part, dir_type, smooth_duration):
        node_name = BLEND_NODE.get(dir_type, '')
        if isinstance(node_name, dict):
            node_name = node_name.get(part, '')
        if not node_name:
            return
        if not self._animator:
            return
        node = self._animator.find(node_name)
        if node:
            node.smoothWeightsDuration = smooth_duration

    def _transform_list_to_tuple(self, lt):
        for i in range(len(lt)):
            if type(lt[i]) == list:
                lt[i] = self._transform_list_to_tuple(lt[i])

        return tuple(lt)

    def on_post_extern_action(self, anim_name, enable, level=1, subtree=None, **kwargs):
        if self.use_skin_anim_map and anim_name in self.skin_anim_map:
            anim_name = self.skin_anim_map[anim_name]
        node_name = 'extern_body_action_%d' % level
        condition_name = 'extern_body_action_%d' % level
        state_machine_node_name = 'Entry.extern_body_%d' % level
        blend_time = kwargs.get('blend_time', 0.5)
        if blend_time is None:
            blend_time = 0.5
        if enable:
            node = self._animator.find(node_name)
            anim_name = self.check_anim_name(anim_name)
            if subtree is not None:
                if type(subtree) == list:
                    subtree = self._transform_list_to_tuple(subtree)
                node.SetBoneTreeWeightChain(subtree, False)
            self._animator.replace_clip_name(node_name, anim_name)
            node.loop = bool(kwargs.get('loop', False))
            node.phase = 0
            for k, v in six.iteritems(kwargs):
                if hasattr(node, k):
                    setattr(node, k, v)

            self._animator.find(state_machine_node_name).smoothWeightsDuration = blend_time
            self._animator.SetInt(condition_name, 1)
        else:
            self._animator.find(state_machine_node_name).smoothWeightsDuration = blend_time
            self._animator.SetInt(condition_name, 0)
        force_trigger_effect = kwargs.get('force_trigger_effect', False)
        socket_index = kwargs.get('socket_index', -1)
        self.send_event('E_TRIGGER_ANIM_EFFECT', anim_name, 'extern%d' % level, force_trigger_effect, socket_index)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', (bcast.E_POST_EXTERN_ACTION, (anim_name, enable, level, subtree), kwargs), True, False, True)
        return

    def on_post_add_anim(self, enable, diff_anim_name=None, base_anim_name=None, is_base_first_frame=True, **kwargs):
        blend_time = kwargs.get('blend_time', 0.2)
        add_node = self._animator.find('add.up_body')
        add_node.smoothWeightsDuration = blend_time
        if enable:
            blend_time = kwargs.get('blend_time', 0.2)
            add_node = self._animator.find('add.up_body')
            add_node.smoothWeightsDuration = blend_time
            self._animator.SetInt('is_add_blend', 1)
            node_name = 'add.up_body.diff'
            node = self._animator.find(node_name)
            anim_name = self.check_anim_name(diff_anim_name)
            self._animator.replace_clip_name(node_name, anim_name)
            node.phase = 0
            node_name = 'add.up_body.base'
            node = self._animator.find(node_name)
            anim_name = self.check_anim_name(base_anim_name)
            self._animator.replace_clip_name(node_name, anim_name)
            node.phase = 0
            if is_base_first_frame:
                add_node.SetBasePhase(0)
            else:
                add_node.SetBasePhase(-1)
            node = self._animator.find('Entry.up_body')
            for node_name in self.ADD_NODE_LIST:
                node = self._animator.find(node_name)
                node.phase = 0
                for k, v in six.iteritems(kwargs):
                    if hasattr(node, k):
                        setattr(node, k, v)

        else:
            self._animator.SetInt('is_add_blend', 0)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', (bcast.E_POST_ADD_ANIMATION, (enable, diff_anim_name, base_anim_name, is_base_first_frame), kwargs), True, False, True)

    def clear_up_body_anim(self, subtree=None, is_on_zero_weight=False, force=False, blend_time=0.2, part=UP_BODY, **kwargs):
        if not self._animator:
            if not self.ev_g_is_human():
                if self._last_action:
                    for i in range(len(self._last_action) - 1, -1, -1):
                        action = self._last_action[i]
                        if not action:
                            continue
                        args, kwargs = action
                        anim_name, part, dir_type = args
                        upbody_anim = part == UP_BODY
                        if upbody_anim:
                            del self._last_action[i]

            return
        else:
            if self._enable_log:
                print(('test--clear_up_body_anim--step1---part =', DEBUG_PART_DESC.get(part, part), '--subtree =', subtree, '--_default_up_body_anim =', self._default_up_body_anim, '--is_on_zero_weight =', is_on_zero_weight, '--force =', force, '--blend_time =', blend_time))
            root_node_name = 'Entry.up_body'
            if part == LOWER_UP_BODY:
                root_node_name = 'Entry.lower.up_body'
            if self._default_up_body_anim is not None and not force:
                self.send_event('E_ANIM_RATE', UP_BODY, self._default_up_body_anim_param['anim_rate'])
                self.send_event('E_POST_ACTION', self._default_up_body_anim, UP_BODY, self._default_up_body_anim_param['anim_dir'], blend_time=self._default_up_body_anim_param['blend_time'], loop=self._default_up_body_anim_param['loop'])
                return
            if part == UP_BODY:
                self.sd.ref_up_body_anim = None
            else:
                self.sd.ref_lower_up_body_anim = None
            part_enable = UP_BODY_ENABLE
            select_node_name = 'up_body_action'
            if part == LOWER_UP_BODY:
                part_enable = LOWER_UP_BODY_ENABLE
                select_node_name = 'lower_up_body_action'
            self._animator.SetInt(part_enable, 0)
            self.set_smooth_speed(part, blend_time)
            up_body_node = self._animator.find(select_node_name)
            if up_body_node:
                if subtree:
                    if isinstance(subtree, int):
                        subtree_index = subtree
                        subtree = MASK_BONE_SUBTREE_CONFIG.get(subtree_index, MASK_BONE_SUBTREE_CONFIG[1])
                    func = lambda *args: global_data.game_mgr.register_logic_timer(Functor(self.reset_up_body_node_bone, subtree, is_on_zero_weight), 1.0 / 33.0, times=1, mode=timer.CLOCK)
                    if is_on_zero_weight:
                        up_body_node.SetOnZeroWeightCallback(func)
                    else:
                        up_body_node.SetOnDeactivateCallback(func)
            self.send_event('E_TRIGGER_ANIM_EFFECT', None, part, False, -1)
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt_crs_server', (bcast.E_CLEAR_UP_BODY_ANIM, (subtree, is_on_zero_weight, force, blend_time, part)), True, False, True)
            return

    def reset_up_body_node_bone(self, subtree, is_on_zero_weight):
        if not self._animator:
            return
        else:
            up_body_node = self._animator.find('up_body_action')
            if not up_body_node:
                return
            if is_on_zero_weight:
                up_body_node.SetOnZeroWeightCallback(None)
            else:
                up_body_node.SetOnDeactivateCallback(None)
            self.on_set_upbody_bone(subtree, UP_BODY, True)
            return

    def on_change_anim_blend_scale(self, blend_scale, part=LOW_BODY):
        self._animator.SetFloat('low_blend_scale', blend_scale)

    def on_change_anim_move_dir(self, dir_x, dir_y):
        if not self._animator:
            return
        if abs(dir_x) <= 0.01:
            dir_x = 0
        elif dir_x >= 0.99:
            dir_x = 1
        elif dir_x <= -0.99:
            dir_x = -1
        if abs(dir_y) <= 0.01:
            dir_y = 0
        elif dir_y >= 0.99:
            dir_y = 1
        elif dir_y <= -0.99:
            dir_y = -1
        if self.sd.ref_tmp_forbid_anim_dir:
            dir_x = 0
            dir_y = 0
        if self.unit_obj.MASK & UP_ANIM_DIR_UNITS_TAG_VALUE:
            self._animator.SetFloat('up_dir_x', dir_x)
            self._animator.SetFloat('up_dir_y', dir_y)
        if self.sd.ref_forbid_zero_anim_dir:
            if dir_x == 0 and dir_y == 0:
                dir_y = 1
        self._animator.SetFloat('dir_x', dir_x)
        self._animator.SetFloat('dir_y', dir_y)
        self.sd.ref_anim_param['dir_x'] = dir_x
        self.sd.ref_anim_param['dir_y'] = dir_y
        if self.ev_g_is_human():
            radian = math.atan2(dir_x, dir_y)
            degrees = math.degrees(radian)
            self._animator.SetFloat('direction', degrees)

    def calculate_eight_dir(self, dir_x, dir_y):
        radian = math.atan2(dir_y, dir_x)
        angle = math.degrees(radian)
        if angle == 0:
            if dir_x == 0.0:
                return 0
        if angle < 0:
            angle += 360.0
        tolerant_angle = 22.5
        convert_angle = angle + tolerant_angle
        if convert_angle >= 360.0:
            convert_angle -= 360.0
        section_index = math.ceil(convert_angle / tolerant_angle)
        move_dir = math.ceil(section_index / 2)
        return move_dir

    def on_change_anim_rate(self, part, anim_rate, **kwargs):
        self.send_event('E_ACTION_SYNC_ANIM_RATE', part, anim_rate)
        self.sd.ref_anim_rate[part] = anim_rate
        if self._animator:
            nodes = PART_2_SCALE_NODE_DICT.get(part, UP_BODY)
            for node_name in nodes:
                node = self._animator.find(node_name)
                if node:
                    node.timeScale = anim_rate

    def get_anim_rate(self, part):
        return self.sd.ref_anim_rate.get(part, 1.0)

    def get_anim_phase(self, part):
        if part == EXTERN_BODY_1:
            print('test--get_anim_phase--step1--error--not support--************')
            return
        else:
            dir_type = LOW_BODY_DIR_TYPE
            if part == UP_BODY:
                dir_type = UP_BODY_DIR_TYPE
            else:
                if part == LOWER_UP_BODY:
                    dir_type = LOWER_UP_BODY_DIR_TYPE
                dir_value = self._animator.GetInt(dir_type)
                if not dir_value:
                    print(('test--get_anim_phase--step2--error--dir_type =', dir_type, '--dir_value =', dir_value))
                    return
                node_name = ''
                if dir_value > 1:
                    node_name = BLEND_NODE.get(dir_value, None)
                    if not node_name:
                        print(('test--get_anim_phase--step3--error--dir_value =', dir_value, '--have not node'))
                        return 0
                    if isinstance(node_name, dict):
                        new_node_name = node_name.get(part, None)
                        if not new_node_name:
                            print(('test--get_anim_phase--step4--error--part =', part, '--node_dict =', node_name, '--have not node'))
                            return 0
                        node_name = new_node_name
                else:
                    node_name = SINGLE_NODE.get(part, None)
                    if not node_name:
                        print(('test--get_anim_phase--step5--error--part =', part, '--dir_value =', dir_value, '--have not single node'))
                        return 0
                node = self._animator.find(node_name)
                if node:
                    return node.phase
            return 0

    def on_change_anim_phase(self, part, phase):
        if not self._animator:
            return
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', (bcast.E_ANIM_PHASE, (part, phase)), True, False, True)
        nodes = PART_2_SCALE_NODE_DICT.get(part, UP_BODY)
        for index, node_name in enumerate(nodes):
            node = self._animator.find(node_name)
            if node:
                node.phase = phase
                if index:
                    all_child_states = node.GetChildStates()
                    for index, one_child_state in enumerate(all_child_states):
                        one_child_node = one_child_state.childNode
                        one_child_node.phase = phase

    def on_set_y_twistnode(self, val, sync=False):
        _y_twist_node = self._animator.find('turn_y_up_body')
        if not _y_twist_node:
            return
        if val > MAX_TWIST_YAW:
            val -= 2 * MAX_TWIST_YAW
        elif val < -MAX_TWIST_YAW:
            val += 2 * MAX_TWIST_YAW
        if self._disable_intrp_mode:
            _y_twist_node.twistAngle = val
        else:
            self._set_y_twistnode_intrp(val, FORCE_DELTA_TIME)
        if sync:
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_TWIST_YAW, (val,)], False, True, True)

    def _set_y_twistnode_intrp(self, end_y, duration):
        _y_twist_node = self._animator.find('turn_y_up_body')
        if not _y_twist_node:
            return
        _y_twist_node.smoothDuration = duration
        _y_twist_node.twistAngle = end_y

    def on_set_y_twistnode_param(self, startBone, endBone):
        _y_twist_node = self._animator.find('turn_y_up_body')
        if not _y_twist_node:
            return
        _y_twist_node.startBone = startBone
        _y_twist_node.endBone = endBone
        self.send_event('E_SUPPORT_TWIST_YAW', True)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', (bcast.E_TWIST_YAW_PARAM, (startBone, endBone)), True, False, True)

    def on_get_y_twistnode(self):
        _y_twist_node = self._animator.find('turn_y_up_body')
        if not _y_twist_node:
            return 0
        return _y_twist_node.twistAngle

    def on_set_y_root_twistnode(self, val):
        _y_twist_node = self._animator.find('turn_y_full_body')
        if not _y_twist_node:
            return
        if val > MAX_TWIST_YAW:
            val -= 2 * MAX_TWIST_YAW
        elif val < -MAX_TWIST_YAW:
            val += 2 * MAX_TWIST_YAW
        if self._disable_intrp_mode:
            _y_twist_node.twistAngle = val
        else:
            self._set_y_root_twistnode_intrp(val, FORCE_DELTA_TIME)

    def _set_y_root_twistnode_intrp(self, end_y, duration):
        _y_twist_node = self._animator.find('turn_y_full_body')
        if not _y_twist_node:
            return
        _y_twist_node.smoothDuration = duration
        _y_twist_node.twistAngle = end_y

    def on_get_y_root_twistnode(self):
        _y_twist_node = self._animator.find('turn_y_full_body')
        if not _y_twist_node:
            return 0
        return _y_twist_node.twistAngle

    def on_set_x_twistnode(self, val):
        _x_twist_node = self._animator.find('turn_x_up_body')
        if not _x_twist_node:
            return
        if self._disable_intrp_mode:
            _x_twist_node.twistAngle = val
        else:
            self._set_x_twistnode_intrp(val, FORCE_DELTA_TIME)

    def _set_x_twistnode_intrp(self, end_x, duration):
        _x_twist_node = self._animator.find('turn_x_up_body')
        if not _x_twist_node:
            return
        _x_twist_node.smoothDuration = duration
        _x_twist_node.twistAngle = end_x

    def on_set_x_twistnode_param(self, startBone, endBone):
        _x_twist_node = self._animator.find('turn_x_up_body')
        if not _x_twist_node:
            return
        _x_twist_node.startBone = startBone
        _x_twist_node.endBone = endBone
        self.send_event('E_SUPPORT_TWIST_PITCH', True)
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', (bcast.E_TWIST_PITCH_PARAM, (startBone, endBone)), True, False, True)

    def on_get_x_twistnode(self):
        _x_twist_node = self._animator.find('turn_x_up_body')
        if not _x_twist_node:
            return 0
        return _x_twist_node.twistAngle

    def on_set_upbody_bone(self, subtree, part=UP_BODY, is_interpolate=False, **kwargs):
        if not self._animator:
            return
        if isinstance(subtree, int):
            subtree_index = subtree
            subtree = MASK_BONE_SUBTREE_CONFIG.get(subtree_index, MASK_BONE_SUBTREE_CONFIG[1])
        else:
            subtree_index = self.get_subtree_index(subtree)
        self.sd.ref_up_body_mask_index = subtree_index
        node_list = self.UPBODY_DICT.get(part, self.UPBODY_DICT[UP_BODY])
        blend_time = kwargs.get('blend_time', 0)
        for node_name in node_list:
            node = self._animator.find(node_name)
            if node:
                if blend_time > 0:
                    node.SetMaxBlendOutTime(blend_time)
                if not isinstance(subtree, tuple):
                    subtree = tuple(subtree)
                node.SetBoneTreeWeightChain(subtree, is_interpolate)

        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', (bcast.E_UPBODY_BONE, (subtree_index, part, is_interpolate), kwargs), True, False, True)

    def check_anim_name(self, name):
        if not CHECK_ANIM_VALID or name in self.anim_name_set:
            return name
        else:
            log_error('[Resource error] Animation Name (' + name + ') not in model resource')
            return DEFAULT_ANIM_NAME

    def set_default_up_body_anim(self, anim_name, anim_dir=1, anim_rate=1.0, blend_time=0.2, loop=True):
        self._default_up_body_anim = anim_name
        self._default_up_body_anim_param['anim_dir'] = anim_dir
        self._default_up_body_anim_param['anim_rate'] = anim_rate
        self._default_up_body_anim_param['blend_time'] = blend_time
        self._default_up_body_anim_param['loop'] = loop

    def is_playing_default_up_body_anim(self):
        return self._default_up_body_anim and self._default_up_body_anim == self.sd.ref_up_body_anim

    def get_default_up_body_anim(self):
        return self._default_up_body_anim