# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComAnimatorAppearance.py
from __future__ import absolute_import
import six
import six_ex
from six.moves import range
from .ComBaseModelAppearance import ComBaseModelAppearance
import math
import world
import math3d
import common.utils.timer as timer
import logic.gcommon.common_const.animation_const as animation_const
import time
from logic.gcommon.common_utils.func_utils import bound_func_id
from logic.gcommon.const import NEOX_UNIT_SCALE
import logic.gcommon.common_utils.bcast_utils as bcast

class ComAnimatorAppearance(ComBaseModelAppearance):
    DEFAULT_XML = ''
    DYNAMIC_MASK_BONE_CLIP = {}
    SUB_COMPONENT_DIR_PATH = ''
    SUB_COMPONENT = ()
    FULL_BODY_ROOT_NODE_NAME = 'full_body'
    BLEND_ADD_ROOT_NODE_NAME = 'blend_add'
    BIND_EVENT = ComBaseModelAppearance.BIND_EVENT.copy()
    BIND_EVENT.update({'E_CLEAR_ANIM_PARAM_LISTENER_BY_NODE': 'clear_anim_param_listener_by_node',
       'G_MASK_SUBTREE': 'get_mask_subtree',
       'E_REGISTER_MASK_SUBTREE_EVENT': 'register_mask_subtree_event',
       'E_REGISTER_CHANGE_CLIP_EVENT': 'register_change_clip_event',
       'E_REGISTER_ANIM_PARAM_LISTENER_EVENT': 'register_anim_param_listener',
       'E_REGISTER_ANIM_KEY_EVENT': 'register_anim_key_event',
       'G_ANIMATOR': 'get_animator',
       'G_IS_MODEL_LOADED': 'is_model_loaded',
       'E_CHARACTER_ATTR': 'change_character_attr',
       'E_REGISTER_ANIM_ACTIVE': 'register_active_event',
       'E_UNREGISTER_ANIM_ACTIVE': 'unregister_active_event',
       'E_REGISTER_ANIM_DEACTIVE': 'register_deactive_event',
       'E_UNREGISTER_ANIM_DEACTIVE': 'unregister_deactive_event',
       'E_REGISTER_ANIM_STATE_ENTER': 'register_state_enter_event',
       'E_UNREGISTER_ANIM_STATE_ENTER': 'unregister_state_enter_event',
       'E_REGISTER_ANIM_STATE_EXIT': 'register_state_exit_event',
       'E_UNREGISTER_ANIM_STATE_EXIT': 'unregister_state_exit_event',
       'E_HAND_ACTION': 'set_hand_action',
       'G_HAND_ACTION': 'get_hand_action',
       'G_MODEL_DIR': 'get_model_dir_path',
       'G_GET_NODE_RELATE_CLIP': 'get_node_relate_clip',
       'E_HIDE_MODEL': 'hide_model',
       'E_SHOW_MODEL': 'show_model',
       'E_UNREGISTER_ANIMATOR_EVENT': 'unregister_animator_event',
       'E_CLEAR_ANIMATOR_XML': 'clear_animator_xml',
       'E_LOAD_NEW_ANIMATOR_XML': 'load_new_animator_xml',
       'G_MODEL_VISIBILITY': 'get_model_visibility',
       'G_GEN_CLIP_LIST': 'gen_clip_list',
       'E_SHWO_DEBUG_BONES': 'show_debug_bones',
       'G_IS_MECHA': 'is_mecha',
       'G_GET_ANIM_LENGTH': 'get_anim_length',
       'E_RESTART_SFX_ON_TRIGGER': 'restart_sfx_on_trigger',
       'G_GET_BONE_INVALID_TRANSLATION': 'get_bone_invalid_translation',
       'G_GET_BONE_INVALID_SCALE': 'get_bone_invalid_scale',
       'G_ALL_ANIMTION_EVENT': 'get_all_animtion_event'
       })
    BIND_LOAD_FINISH_EVENT = ComBaseModelAppearance.BIND_LOAD_FINISH_EVENT.copy()
    BIND_LOAD_FINISH_EVENT.update({'E_MOVE_BY_CLIP': 'move_by_clip',
       'G_MODEL_SOCKET_POS': 'get_model_socket_matrix',
       'G_HEAD_POSITION': 'get_head_position',
       'E_REGISTER_ANIMATOR_EVENT': 'register_animator_event',
       'E_SHOW_FULLBODY_ANIMATION': 'show_fullbody_animation',
       'E_HIDE_FULLBODY_ANIMATION': 'hide_fullbody_animation',
       'E_REVERT_FULLBODY_ANIMATION': 'revert_fullbody_animation_tick',
       'G_ANIMATOR_STATE_DESC': 'get_animator_state_desc'
       })

    def __init__(self):
        super(ComAnimatorAppearance, self).__init__()
        self.model_visible = True
        self.animation_callback = {}
        self.animation_active_callback = {}
        self._active_event = {}
        self._deactive_event = {}
        self._state_enter_event = {}
        self._state_exit_event = {}
        self._clip_move_timer_id = None
        self._clip_move_start_time = None
        self._clip_move_duration_ms = None
        self._clip_move_last_pass_time = None
        self.sd.ref_is_mecha = False
        self._is_debug_anim = False
        self._debug_anim_timer = None
        return

    def get_bone_valid_scale(self):
        return (0, 3)

    def get_bone_invalid_scale(self):
        model = self.model
        if not model:
            return
        valid_min_scale, valid_max_scale = self.get_bone_valid_scale()
        min_scale = valid_min_scale
        max_scale = valid_max_scale
        min_invalid_bone_name = ''
        max_invalid_bone_name = ''
        bone_count = model.get_bone_count()
        for bone_index in range(bone_count):
            bone_name = model.get_bone_name(bone_index)
            one_bone_matrix = model.get_bone_matrix(bone_index, world.SPACE_TYPE_WORLD)
            scale = one_bone_matrix.scale
            all_scale = (scale.x, scale.y, scale.z)
            one_min_scale_value = min(all_scale)
            one_max_scale_value = max(all_scale)
            if one_min_scale_value < min_scale:
                min_scale = one_min_scale_value
                min_invalid_bone_name = bone_name
            if one_max_scale_value > max_scale:
                max_scale = one_max_scale_value
                max_invalid_bone_name = bone_name

        invalid_bone_info = {}
        if max_invalid_bone_name:
            invalid_bone_info['max'] = (
             max_invalid_bone_name, max_scale)
        return invalid_bone_info

    def get_bone_valid_translation(self):
        return math3d.vector(1.5 * NEOX_UNIT_SCALE, 2.5 * NEOX_UNIT_SCALE, 1.5 * NEOX_UNIT_SCALE)

    def get_bone_invalid_translation(self):
        model = self.model
        if not model:
            return
        base_bone_name = 'biped root'
        base_bone_matrix = model.get_bone_matrix(base_bone_name, world.SPACE_TYPE_WORLD)
        base_translation = base_bone_matrix.translation
        valid_max_translation = self.get_bone_valid_translation()
        max_translation = valid_max_translation
        invalid_bone_info = {}
        bone_count = model.get_bone_count()
        for bone_index in range(bone_count):
            bone_name = model.get_bone_name(bone_index)
            one_bone_matrix = model.get_bone_matrix(bone_index, world.SPACE_TYPE_WORLD)
            one_translation = one_bone_matrix.translation
            offset = one_translation - base_translation
            if abs(offset.x) > max_translation.x:
                max_translation.x = abs(offset.x)
                invalid_bone_info['x'] = (bone_name, offset.x)
            if abs(offset.y) > max_translation.y:
                max_translation.y = abs(offset.y)
                invalid_bone_info['y'] = (bone_name, offset.y)
            if abs(offset.z) > max_translation.z:
                max_translation.z = abs(offset.z)
                invalid_bone_info['z'] = (bone_name, offset.z)

        return invalid_bone_info

    def gen_clip_list(self, clip_config):
        if not isinstance(clip_config, (list, tuple)):
            return clip_config
        clip_num = clip_config[0]
        clip_list = []
        base_clip_name = clip_config[1]
        if clip_num <= 5:
            clip_list.append(base_clip_name + '_l')
            clip_list.append(base_clip_name + '_r')
            clip_list.append(base_clip_name + '_f')
            clip_list.append(base_clip_name + '_b')
        else:
            clip_list.append(base_clip_name + '_fl')
            clip_list.append(base_clip_name + '_fr')
            clip_list.append(base_clip_name + '_f')
            clip_list.append(base_clip_name + '_bl')
            clip_list.append(base_clip_name + '_br')
            clip_list.append(base_clip_name + '_b')
        if clip_num % 2 != 0:
            clip_list.append(base_clip_name)
        return clip_list

    def get_animator(self):
        return self._animator

    def get_animator_state_desc(self):
        if not self._animator:
            return ''
        return self._animator.print_info(True)

    def show_debug_bones(self, is_show):
        is_show = bool(is_show)
        animator = self.ev_g_animator()
        if animator:
            animator.show_bones(is_show)

    def validate_file(self):
        import C_file
        data = C_file.get_res_file('model_new/mecha/8002/skeleton/8002_mecha_gis/whirlwind_n_1.gis', '')
        import zlib

    def restart_sfx_on_trigger(self, anim_name, trigger_name):
        model = self.model
        if not model:
            return
        bind_obj_count = model.get_anim_trigger_socket_obj_count(anim_name, trigger_name)
        for index in range(bind_obj_count):
            sfx = model.get_anim_trigger_socket_obj(anim_name, trigger_name, index)
            if sfx:
                sfx.restart()

    def recursive_get_clip(self, animation_node, all_clip_list):
        if not animation_node or not animation_node.active:
            return
        if animation_const.SOURCE_NODE_TYPE in animation_node.nodeType:
            all_clip_list.append(animation_node.clipName)
        elif animation_const.DUMMY_NODE_TYPE in animation_node.nodeType:
            pass
        else:
            all_child_states = animation_node.GetChildStates()
            for index, one_child_state in enumerate(all_child_states):
                one_child_node = one_child_state.childNode
                self.recursive_get_clip(one_child_node, all_clip_list)

    def get_lowbody_animation(self):
        animator = self.ev_g_animator()
        if not animator:
            return
        root_node = animator.find(self.FULL_BODY_ROOT_NODE_NAME)
        if not root_node:
            return
        all_child_states = root_node.GetChildStates()
        low_root_node = all_child_states[0].childNode
        clip_list = []
        self.recursive_get_clip(low_root_node, clip_list)
        return tuple(clip_list)

    def get_upbody_animation(self):
        animator = self.ev_g_animator()
        if not animator:
            return
        root_node = animator.find(self.FULL_BODY_ROOT_NODE_NAME)
        if not root_node:
            return
        all_child_states = root_node.GetChildStates()
        all_child_states = list(all_child_states)
        all_child_states.reverse()
        clip_list = []
        for one_child_states in all_child_states:
            up_root_node = one_child_states.childNode
            self.recursive_get_clip(up_root_node, clip_list)
            if clip_list:
                break

        return tuple(clip_list)

    def get_add_animation(self):
        animator = self.ev_g_animator()
        if not animator:
            return
        root_node = animator.find('add.up_body.weapon')
        if not root_node:
            return
        clip_list = []
        self.recursive_get_clip(root_node, clip_list)
        clip_list = tuple(clip_list)
        text = '\xe7\xac\xac1\xe5\xb1\x82\xe5\x8a\xa0\xe6\xb3\x95\xe5\x8a\xa8\xe4\xbd\x9c: ' + ', '.join(clip_list) + '\n'
        root_node = animator.find('add.up_body.move')
        if root_node:
            clip_list = []
            self.recursive_get_clip(root_node, clip_list)
            clip_list = tuple(clip_list)
            text = text + '\xe7\xac\xac2\xe5\xb1\x82\xe5\x8a\xa0\xe6\xb3\x95\xe5\x8a\xa8\xe4\xbd\x9c: ' + ', '.join(clip_list) + '\n'
        return text

    def revert_fullbody_animation_tick(self):
        if not self._is_debug_anim:
            return
        is_tick = self._debug_anim_timer
        is_tick = not is_tick
        self.show_fullbody_animation(is_tick)

    def show_fullbody_animation_tick(self):
        self.show_fullbody_animation(True)

    def show_fullbody_animation(self, is_tick=False):
        upbody_anim_list = self.get_upbody_animation() or []
        text = '\xe4\xb8\x8a\xe5\x8d\x8a\xe8\xba\xab\xe5\x8a\xa8\xe4\xbd\x9c: ' + ', '.join(upbody_anim_list) + '\n\n\n'
        lowbody_anim_list = self.get_lowbody_animation() or []
        text = text + '\xe4\xb8\x8b\xe5\x8d\x8a\xe8\xba\xab\xe5\x8a\xa8\xe4\xbd\x9c: ' + ', '.join(lowbody_anim_list) + '\n'
        lowbody_anim_list = self.get_lowbody_animation() or []
        add_text = self.get_add_animation()
        if add_text:
            text = text + add_text
        self._is_debug_anim = True
        global_data.emgr.update_animation_info.emit(text)
        if is_tick:
            if self._debug_anim_timer:
                return
            self._debug_anim_timer = global_data.game_mgr.register_logic_timer(self.show_fullbody_animation_tick, interval=1.0 / 30.0, times=-1)
        elif self._debug_anim_timer:
            global_data.game_mgr.unregister_logic_timer(self._debug_anim_timer)
            self._debug_anim_timer = None
        return

    def hide_fullbody_animation(self):
        self._is_debug_anim = False
        global_data.emgr.update_animation_info.emit('')
        if self._debug_anim_timer:
            global_data.game_mgr.unregister_logic_timer(self._debug_anim_timer)
            self._debug_anim_timer = None
        return

    def move_by_clip(self, clip_name):
        model = self.ev_g_model()
        if self._clip_move_timer_id:
            global_data.game_mgr.unregister_logic_timer(self._clip_move_timer_id)
        self._clip_move_timer_id = global_data.game_mgr.register_logic_timer(self.move_by_clip_tick, 1.0 / 33.0, [
         clip_name], times=-1, mode=timer.CLOCK, timedelta=True)
        self._clip_move_start_time = time.time()
        self._clip_move_duration_ms = model.get_anim_length(clip_name)
        self._clip_move_last_pass_time = 0
        model.lock_bone('biped root', world.BONE_LOCK_X | world.BONE_LOCK_Y | world.BONE_LOCK_Z)

    def get_anim_length(self, clip_name):
        model = self.get_model()
        if not model:
            return 0
        return model.get_anim_length(clip_name) / 1000.0

    def move_by_clip_tick(self, dt, clip_name, *args):
        model = self.model
        if not model:
            self.send_event('E_SET_WALK_DIRECTION', math3d.vector(0, 0, 0))
            return timer.RELEASE
        pass_time = time.time() - self._clip_move_start_time
        pass_time *= 1000
        pass_time = min(pass_time, self._clip_move_duration_ms)
        if self._clip_move_last_pass_time >= self._clip_move_duration_ms:
            model.lock_bone('biped root', 0)
            self.send_event('E_SET_WALK_DIRECTION', math3d.vector(0, 0, 0))
            return timer.RELEASE
        last_pass_time = self._clip_move_last_pass_time
        self._clip_move_last_pass_time = pass_time
        duration = pass_time - last_pass_time
        if duration <= 0:
            return
        duration /= 1000.0
        last_key_matrix = model.get_bone_trans_info(clip_name, 'biped root', last_pass_time)
        cur_key_matrix = model.get_bone_trans_info(clip_name, 'biped root', pass_time)
        last_key_pos = last_key_matrix.translation
        cur_key_pos = cur_key_matrix.translation
        dist_dir = cur_key_pos - last_key_pos
        dist_dir.x /= duration
        dist_dir.z /= duration
        speed = dist_dir
        yaw = self.ev_g_yaw()
        walk_direction = self.ev_g_walk_direction()
        if not walk_direction or walk_direction.is_zero:
            walk_direction = math3d.vector(0, 0, 1)
        else:
            walk_direction.normalize()
        speed = walk_direction * speed.length
        move_dir = speed * math3d.matrix.make_rotation_y(yaw)
        self.send_event('E_SET_WALK_DIRECTION', move_dir)

    def register_animator_event(self, clip_name, trigger_name, callback, data, auto_delete=False):
        model = self.model
        animation_callback = self.animation_callback
        ani_name = clip_name
        key = '%s_%s' % (ani_name, trigger_name)
        if key not in animation_callback:
            animation_callback[key] = {'handler': None,'callback': []}

            def _handler(model, anim_name, _key):
                if key not in animation_callback:
                    return
                callbacks = animation_callback[key]['callback']
                remove_idx = []
                for idx, (func, _data, auto_del) in enumerate(callbacks):
                    func(_data)
                    if auto_del:
                        remove_idx.append(idx)

                if remove_idx:
                    remove_idx.reverse()
                    for idx in remove_idx:
                        callbacks.pop(idx)

            animator = self._animator
            if global_data.enable_animator_reg_event and animator:
                animator.add_trigger_clip(ani_name, trigger_name, _handler)
            else:
                model.register_anim_key_event(ani_name, trigger_name, _handler)
            animation_callback[key] = {'handler': _handler,
               'callback': [
                          (
                           callback, data, auto_delete)],
               'ani_name': ani_name,
               'trigger_name': trigger_name
               }
        else:
            callbacks = animation_callback[key]['callback']
            for func, _data, auto_delete in callbacks:
                if bound_func_id(func) == bound_func_id(callback) and str(data) == str(_data):
                    return

            callbacks.append((callback, data, auto_delete))
        return

    def _clean_all_animator_events(self):
        model = self.model
        if model:
            for key, infos in six.iteritems(self.animation_callback):
                model.unregister_event(infos['handler'], infos['trigger_name'], infos['ani_name'])

        self.animation_callback.clear()

    def unregister_animator_event(self, clip_name, trigger_name, callback):
        ani_name = clip_name
        key = '%s_%s' % (ani_name, trigger_name)
        if key not in self.animation_callback:
            return
        infos = self.animation_callback[key]
        callbacks = infos['callback']
        remove_idx = []
        for idx, (func, _data, auto_del) in enumerate(callbacks):
            if bound_func_id(func) == bound_func_id(callback):
                remove_idx.append(idx)

        if remove_idx:
            remove_idx.reverse()
            for idx in remove_idx:
                callbacks.pop(idx)

    def clear_animator_xml(self):
        self._animator.Clear()

    def load_new_animator_xml(self, path):
        if not path:
            return
        self._animator.Replace(path)

    def _on_control_target_change(self, target_id, position, *args):
        pass

    def init_from_dict(self, unit_obj, bdict):
        super(ComAnimatorAppearance, self).init_from_dict(unit_obj, bdict)
        for comp_name in self.SUB_COMPONENT:
            com_obj = self.unit_obj.add_com(comp_name, self.SUB_COMPONENT_DIR_PATH)
            com_obj.init_from_dict(self.unit_obj, bdict)

    def on_init_complete(self):
        pass

    def get_model_dir_path(self):
        return ''

    def register_change_clip_event(self, node_name, params, callback, data=None, ignore_active=False):
        animator = self._animator
        if not animator:
            return
        source_node = animator.find(node_name)
        if not source_node:
            return
        if not ignore_active:
            if not source_node.IsActiveInHierarchy():
                return
        for param_name in params:
            self.register_anim_param_listener(param_name, node_name, callback, data)

    def register_mask_subtree_event(self, node_name, data=None, ignore_active=False):
        animator = self._animator
        if not animator:
            return
        source_node = animator.find(node_name)
        if not source_node:
            return
        if not ignore_active:
            if not source_node.IsActiveInHierarchy():
                return
        subtree, params = self.get_mask_subtree(source_node.clipName)
        if not subtree:
            return
        source_node.SetBoneTreeWeightChain(subtree)
        if not params:
            return

        def _on_anim_param_value_change(node_name, param_name, value):
            subtree, params = self.ev_g_mask_subtree(source_node.clipName)
            if not subtree:
                return
            source_node.SetBoneTreeWeightChain(subtree)

        for param_name in params:
            self.register_anim_param_listener(param_name, node_name, _on_anim_param_value_change, data)

    def get_mask_subtree(self, clip_name):
        animator = self.ev_g_animator()
        if not animator:
            return (animation_const.ENABLE_FULL_BODY_BONE, None)
        else:
            param_config_list = self.DYNAMIC_MASK_BONE_CLIP.get(clip_name)
            if not param_config_list:
                return (animation_const.ENABLE_FULL_BODY_BONE, None)
            subtree = None
            for one_param_config in param_config_list:
                parameters = one_param_config['param']
                if parameters != animation_const.NO_LIMIT_PARAM:
                    for param_name, def_value in six_ex.items(parameters):
                        cur_value = animator.GetInt(param_name)
                        if isinstance(def_value, int):
                            if def_value == cur_value:
                                return (one_param_config['subtree'], one_param_config['param'])
                        elif cur_value in def_value:
                            return (one_param_config['subtree'], one_param_config['param'])

                else:
                    return (
                     one_param_config['subtree'], one_param_config['param'])

            return (animation_const.ENABLE_FULL_BODY_BONE, None)

    def get_all_animtion_event(self):
        return {}

    def register_anim_key_event(self, clip_name, trigger_name, callback, data=None, immediate=False):
        animator = self.ev_g_animator()
        if not animator:
            return
        model = self.ev_g_model()
        if not model:
            return
        animtion_event = self.get_all_animtion_event()
        if trigger_name in animtion_event.get(clip_name, []) or model.has_anim_event(clip_name, trigger_name):
            if immediate:
                if global_data.enable_animator_reg_event and animator and clip_name not in ('run',
                                                                                            'sword_core_run'):
                    animator.add_trigger_clip(clip_name, trigger_name, callback, data)
                else:
                    model.register_anim_key_event(clip_name, trigger_name, callback, data)
            else:
                animator.add_trigger_clip(clip_name, trigger_name, callback, data)

    def register_anim_param_listener(self, param_name, node_name, callback, data=None):
        animator = self.ev_g_animator()
        if not animator:
            return
        animator.RegisterParamListener(param_name, node_name, callback, data)

    def clear_anim_param_listener_by_node(self, node_name):
        animator = self.ev_g_animator()
        if not animator:
            return
        animator.ClearParamListenerByNode(node_name)

    def get_model_visibility(self):
        return self.model_visible

    def _set_model_visible(self, visible):
        model = self.ev_g_model()
        if model:
            model.visible = visible

    def show_model(self, *args):
        if self.ev_g_is_pure_mecha() is True:
            return
        self.model_visible = True
        if not self._animator or not self._animator.is_loaded():
            return
        self._set_model_visible(True)

    def hide_model(self, *args):
        self.model_visible = False
        if not self._animator or not self._animator.is_loaded():
            return
        self._set_model_visible(False)

    def destroy(self):
        self._clean_all_animator_events()
        if self._animator:
            self._animator.destroy()
            self._animator = None
        if self._debug_anim_timer:
            self.hide_fullbody_animation()
        super(ComAnimatorAppearance, self).destroy()
        return

    def get_hand_action(self):
        pass

    def set_hand_action(self, hand_action, force=False):
        pass

    def add_camera_trigger_events(self):
        from logic.vscene.parts.camera.CamShake import CamShakeController
        CamShakeController().register_cam_shake_event(self.unit_obj)

    def on_load_model_complete(self, model, user_data):
        model.visible = False
        self.do_load_animator(model, user_data)

    def get_xml_path(self):
        return self.DEFAULT_XML

    def do_load_animator(self, model, user_data):
        if self._animator:
            self.on_load_animator_complete(user_data)
        else:
            from common.animate import animator
            self._animator = animator.Animator(model, self.get_xml_path(), self.unit_obj)
            self._animator.Load(True, self.on_load_animator_complete, user_data)

    def test_async_load(self):
        if self.unit_obj:
            self.unit_obj.destroy()

    def is_model_loaded(self):
        return self.model and self._animator

    def on_load_animator_complete(self, *args):
        if not self._animator:
            return
        self.send_event('E_ANIMATOR_LOADED', *args)
        for arg, callback_list in six.iteritems(self._active_event):
            for callback in callback_list:
                self._animator.register_active_event(arg, callback)

        for arg, callback_list in six.iteritems(self._deactive_event):
            for callback in callback_list:
                self._animator.register_deactive_event(arg, callback)

        for arg, callback_list in six.iteritems(self._state_enter_event):
            for callback in callback_list:
                self._animator.register_state_enter_event(arg, callback)

        for arg, callback_list in six.iteritems(self._state_exit_event):
            for callback in callback_list:
                self._animator.register_state_exit_event(arg, callback)

        self._active_event = {}
        self._deactive_event = {}
        self._state_enter_event = {}
        self._state_exit_event = {}
        self.show_model() if self.model_visible else self.hide_model()

    def register_one_type_event(self, arg, callback, event_dict):
        if not isinstance(arg, (list, tuple)):
            arg = (
             arg,)
        for one_arg in arg:
            event_list = event_dict.setdefault(one_arg, [])
            event_list.append(callback)

    def register_state_enter_event(self, arg, callback):
        if self._animator:
            self._animator.register_state_enter_event(arg, callback)
        else:
            self.register_one_type_event(arg, callback, self._state_enter_event)

    def unregister_state_enter_event(self, arg, callback):
        if self._animator:
            self._animator.unregister_state_enter_event(arg, callback)

    def register_active_event(self, arg, callback):
        if self._animator:
            self._animator.register_active_event(arg, callback)
        else:
            self.register_one_type_event(arg, callback, self._active_event)

    def unregister_active_event(self, arg, callback):
        if self._animator:
            self._animator.unregister_active_event(arg, callback)

    def register_deactive_event(self, arg, callback):
        if self._animator:
            self._animator.register_deactive_event(arg, callback)
        else:
            self.register_one_type_event(arg, callback, self._deactive_event)

    def unregister_deactive_event(self, arg, callback):
        if self._animator:
            self._animator.unregister_deactive_event(arg, callback)

    def register_state_exit_event(self, arg, callback):
        if self._animator:
            self._animator.register_state_exit_event(arg, callback)
        else:
            self.register_one_type_event(arg, callback, self._state_exit_event)

    def unregister_state_exit_event(self, arg, callback):
        if self._animator:
            self._animator.unregister_state_exit_event(arg, callback)

    def _on_state_leave(self, arg):
        pass

    def change_character_attr(self, name, *arg):
        if name == 'node_all_info':
            active = bool(arg[1])
            self._animator.print_node_info(arg[0], active=active)
        elif name == 'animator_info_for_duration':
            duration = arg[0]
            only_active = True
            if len(arg) > 1:
                only_active = arg[1]
            show_anim = True
            if len(arg) > 2:
                show_anim = arg[2]
            self._debug_anim_nodes(duration, only_active, show_anim)
        elif name == 'bone_info_for_duration':
            duration = arg[0]
            bone_name = arg[1]
            self._debug_bone_info(duration, bone_name)
        elif name == 'bone_info':
            bone_name = arg[0]
            self._debug_one_bone(bone_name)
        elif name == 'reset_animator':
            self._animator.reset()
        elif name == 'param_info':
            self._animator.print_parameter()
        elif name == 'animator_info':
            model = self.model
            if model:
                world_bone_yaw = model.world_rotation_matrix.yaw
                model_file_list = self.get_main_and_sub_model(model)
                rotation_matrix = model.rotation_matrix
                only_active = arg[0]
                if self._animator:
                    self._animator.print_info(active=only_active)
                global_data.emgr.cam_aim_animation_info.emit(only_active)
        elif name == 'reload_animator':
            self._animator.Reload()
        elif name == 'clear_animator':
            self.clear_animator_xml()
        elif name == 'replace_animator':
            path = 'animator_conf/test.xml'
            self.send_event('E_LOAD_NEW_ANIMATOR_XML', path)
        elif name == 'low_body_action':
            self.switch_to_status(arg[0])
        elif name == 'up_body_action':
            self.set_hand_action(arg[0])
        elif name == 'int_animator_arg':
            self._animator.SetInt(arg[0], arg[1])
        elif name == 'float_animator_arg':
            self._animator.SetFloat(arg[0], arg[1])

    def _get_bone_yaw(self, bone_name, space_type):
        model = self.ev_g_model()
        if not model:
            return 0
        local_bone_matrix = model.get_bone_matrix(bone_name, space_type)
        return local_bone_matrix.yaw

    def _get_bone_pitch(self, bone_name, space_type):
        model = self.ev_g_model()
        if not model:
            return 0
        local_bone_matrix = model.get_bone_matrix(bone_name, space_type)
        return local_bone_matrix.pitch

    def _get_bone_roll(self, bone_name, space_type):
        model = self.ev_g_model()
        if not model:
            return 0
        local_bone_matrix = model.get_bone_matrix(bone_name, space_type)
        return local_bone_matrix.roll

    def _get_bone_position(self, bone_name, space_type):
        model = self.ev_g_model()
        if not model:
            return 0
        local_bone_matrix = model.get_bone_matrix(bone_name, space_type)
        return local_bone_matrix.translation

    def _debug_one_anim_node--- This code section failed: ---

 901       0  LOAD_CONST            1  ''
           3  LOAD_FAST             0  'self'
           6  STORE_ATTR            0  'debug_anim_times'

 902       9  LOAD_CONST            2  1.0
          12  LOAD_CONST            3  30.0
          15  BINARY_DIVIDE    
          16  STORE_FAST            3  'interval'

 903      19  LOAD_GLOBAL           1  'math'
          22  LOAD_ATTR             2  'ceil'
          25  LOAD_FAST             2  'duration'
          28  LOAD_FAST             3  'interval'
          31  BINARY_DIVIDE    
          32  CALL_FUNCTION_1       1 
          35  STORE_FAST            4  'times'

 905      38  LOAD_FAST             0  'self'
          41  LOAD_ATTR             3  'send_event'
          44  LOAD_CONST            4  'E_CHARACTER_ATTR'
          47  LOAD_CONST            5  'node_all_info'
          50  LOAD_DEREF            0  'name'
          53  CALL_FUNCTION_3       3 
          56  POP_TOP          

 907      57  LOAD_CLOSURE          0  'name'
          63  LOAD_CONST               '<code_object _print_one_node_info>'
          66  MAKE_CLOSURE_0        0 
          69  STORE_FAST            5  '_print_one_node_info'

 912      72  LOAD_GLOBAL           4  'getattr'
          75  LOAD_GLOBAL           7  'game_mgr'
          78  LOAD_CONST            0  ''
          81  CALL_FUNCTION_3       3 
          84  STORE_FAST            6  '_debug_one_anim_node_timer_id'

 913      87  LOAD_FAST             6  '_debug_one_anim_node_timer_id'
          90  POP_JUMP_IF_FALSE   112  'to 112'

 914      93  LOAD_GLOBAL           6  'global_data'
          96  LOAD_ATTR             7  'game_mgr'
          99  LOAD_ATTR             8  'unregister_logic_timer'
         102  LOAD_FAST             6  '_debug_one_anim_node_timer_id'
         105  CALL_FUNCTION_1       1 
         108  POP_TOP          
         109  JUMP_FORWARD          0  'to 112'
       112_0  COME_FROM                '109'

 916     112  LOAD_GLOBAL           6  'global_data'
         115  LOAD_ATTR             7  'game_mgr'
         118  LOAD_ATTR             9  'register_logic_timer'

 917     121  LOAD_FAST             5  '_print_one_node_info'
         124  LOAD_FAST             3  'interval'
         127  LOAD_FAST             0  'self'
         130  BUILD_LIST_1          1 
         133  LOAD_CONST            8  'times'

 918     136  LOAD_FAST             4  'times'
         139  LOAD_CONST            9  'mode'
         142  LOAD_GLOBAL          10  'timer'
         145  LOAD_ATTR            11  'CLOCK'
         148  CALL_FUNCTION_515   515 
         151  LOAD_FAST             0  'self'
         154  STORE_ATTR           12  '_debug_one_anim_node_timer_id'
         157  LOAD_CONST            0  ''
         160  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 81

    def _debug_one_bone(self, bone_name):
        local_bone_yaw = self._get_bone_yaw(bone_name, world.SPACE_TYPE_LOCAL)
        world_bone_yaw = self._get_bone_yaw(bone_name, world.SPACE_TYPE_WORLD)
        local_bone_pitch = self._get_bone_pitch(bone_name, world.SPACE_TYPE_LOCAL)
        world_bone_pitch = self._get_bone_pitch(bone_name, world.SPACE_TYPE_WORLD)
        local_bone_roll = self._get_bone_roll(bone_name, world.SPACE_TYPE_LOCAL)
        world_bone_roll = self._get_bone_roll(bone_name, world.SPACE_TYPE_WORLD)
        local_bone_position = self._get_bone_position(bone_name, world.SPACE_TYPE_LOCAL)
        world_bone_position = self._get_bone_position(bone_name, world.SPACE_TYPE_WORLD)
        model_yaw = self.model.rotation_matrix.yaw

    def _debug_bone_info--- This code section failed: ---

 942       0  LOAD_CONST            1  ''
           3  LOAD_FAST             0  'self'
           6  STORE_ATTR            0  'debug_bone_times'

 943       9  LOAD_CONST            2  1.0
          12  LOAD_CONST            3  30.0
          15  BINARY_DIVIDE    
          16  STORE_FAST            3  'interval'

 944      19  LOAD_GLOBAL           1  'math'
          22  LOAD_ATTR             2  'ceil'
          25  LOAD_FAST             1  'duration'
          28  LOAD_FAST             3  'interval'
          31  BINARY_DIVIDE    
          32  CALL_FUNCTION_1       1 
          35  STORE_FAST            4  'times'

 946      38  LOAD_FAST             0  'self'
          41  LOAD_ATTR             3  'send_event'
          44  LOAD_CONST            4  'E_CHARACTER_ATTR'
          47  LOAD_CONST            5  'bone_info'
          50  LOAD_DEREF            0  'bone_name'
          53  CALL_FUNCTION_3       3 
          56  POP_TOP          

 948      57  LOAD_CLOSURE          0  'bone_name'
          63  LOAD_CONST               '<code_object _print_one_bone>'
          66  MAKE_CLOSURE_0        0 
          69  STORE_FAST            5  '_print_one_bone'

 953      72  LOAD_GLOBAL           4  'getattr'
          75  LOAD_GLOBAL           7  'game_mgr'
          78  LOAD_CONST            0  ''
          81  CALL_FUNCTION_3       3 
          84  STORE_FAST            6  '_debug_bone_nodes_timer_id'

 954      87  LOAD_FAST             6  '_debug_bone_nodes_timer_id'
          90  POP_JUMP_IF_FALSE   112  'to 112'

 955      93  LOAD_GLOBAL           6  'global_data'
          96  LOAD_ATTR             7  'game_mgr'
          99  LOAD_ATTR             8  'unregister_logic_timer'
         102  LOAD_FAST             6  '_debug_bone_nodes_timer_id'
         105  CALL_FUNCTION_1       1 
         108  POP_TOP          
         109  JUMP_FORWARD          0  'to 112'
       112_0  COME_FROM                '109'

 957     112  LOAD_GLOBAL           6  'global_data'
         115  LOAD_ATTR             7  'game_mgr'
         118  LOAD_ATTR             9  'register_logic_timer'
         121  LOAD_FAST             5  '_print_one_bone'
         124  LOAD_FAST             3  'interval'
         127  LOAD_FAST             0  'self'
         130  BUILD_LIST_1          1 
         133  LOAD_CONST            8  'times'
         136  LOAD_FAST             4  'times'
         139  LOAD_CONST            9  'mode'

 958     142  LOAD_GLOBAL          10  'timer'
         145  LOAD_ATTR            11  'CLOCK'
         148  CALL_FUNCTION_515   515 
         151  LOAD_FAST             0  'self'
         154  STORE_ATTR           12  '_debug_bone_nodes_timer_id'
         157  LOAD_CONST            0  ''
         160  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 81

    def _print_active_nodes(self, only_active, show_anim):
        self.debug_anim_times += 1
        self.send_event('E_DUMP_STATE')
        if show_anim:
            self.send_event('E_CHARACTER_ATTR', 'animator_info', only_active)
        self.send_event('E_CHARACTER_ATTR', 'dump_character', 1)
        self.send_event('E_DEBUG_RAGDOLL')

    def _debug_anim_nodes--- This code section failed: ---

 971       0  LOAD_CONST            1  ''
           3  LOAD_FAST             0  'self'
           6  STORE_ATTR            0  'debug_anim_times'

 972       9  LOAD_CONST            2  1.0
          12  LOAD_CONST            3  30.0
          15  BINARY_DIVIDE    
          16  STORE_FAST            4  'interval'

 973      19  LOAD_GLOBAL           1  'math'
          22  LOAD_ATTR             2  'ceil'
          25  LOAD_FAST             1  'duration'
          28  LOAD_FAST             4  'interval'
          31  BINARY_DIVIDE    
          32  CALL_FUNCTION_1       1 
          35  STORE_FAST            5  'times'

 975      38  LOAD_FAST             0  'self'
          41  LOAD_ATTR             3  'send_event'
          44  LOAD_CONST            4  'E_DUMP_STATE'
          47  CALL_FUNCTION_1       1 
          50  POP_TOP          

 976      51  LOAD_FAST             3  'show_anim'
          54  POP_JUMP_IF_FALSE    79  'to 79'

 977      57  LOAD_FAST             0  'self'
          60  LOAD_ATTR             3  'send_event'
          63  LOAD_CONST            5  'E_CHARACTER_ATTR'
          66  LOAD_CONST            6  'animator_info'
          69  LOAD_FAST             2  'only_active'
          72  CALL_FUNCTION_3       3 
          75  POP_TOP          
          76  JUMP_FORWARD          0  'to 79'
        79_0  COME_FROM                '76'

 978      79  LOAD_FAST             0  'self'
          82  LOAD_ATTR             3  'send_event'
          85  LOAD_CONST            5  'E_CHARACTER_ATTR'
          88  LOAD_CONST            7  'dump_character'
          91  LOAD_CONST            8  1
          94  CALL_FUNCTION_3       3 
          97  POP_TOP          

 979      98  LOAD_FAST             0  'self'
         101  LOAD_ATTR             3  'send_event'
         104  LOAD_CONST            9  'E_DEBUG_RAGDOLL'
         107  CALL_FUNCTION_1       1 
         110  POP_TOP          

 983     111  LOAD_GLOBAL           4  'getattr'
         114  LOAD_GLOBAL          10  '_print_active_nodes'
         117  LOAD_CONST            0  ''
         120  CALL_FUNCTION_3       3 
         123  STORE_FAST            6  '_debug_anim_nodes_timer_id'

 984     126  LOAD_FAST             6  '_debug_anim_nodes_timer_id'
         129  POP_JUMP_IF_FALSE   151  'to 151'

 985     132  LOAD_GLOBAL           6  'global_data'
         135  LOAD_ATTR             7  'game_mgr'
         138  LOAD_ATTR             8  'unregister_logic_timer'
         141  LOAD_FAST             6  '_debug_anim_nodes_timer_id'
         144  CALL_FUNCTION_1       1 
         147  POP_TOP          
         148  JUMP_FORWARD          0  'to 151'
       151_0  COME_FROM                '148'

 987     151  LOAD_GLOBAL           6  'global_data'
         154  LOAD_ATTR             7  'game_mgr'
         157  LOAD_ATTR             9  'register_logic_timer'
         160  LOAD_FAST             0  'self'
         163  LOAD_ATTR            10  '_print_active_nodes'
         166  LOAD_FAST             4  'interval'
         169  LOAD_FAST             2  'only_active'
         172  LOAD_FAST             3  'show_anim'
         175  BUILD_LIST_2          2 
         178  LOAD_CONST           11  'times'
         181  LOAD_FAST             5  'times'
         184  LOAD_CONST           12  'mode'

 988     187  LOAD_GLOBAL          11  'timer'
         190  LOAD_ATTR            12  'CLOCK'
         193  CALL_FUNCTION_515   515 
         196  LOAD_FAST             0  'self'
         199  STORE_ATTR           13  '_debug_anim_nodes_timer_id'
         202  LOAD_CONST            0  ''
         205  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 120

    def get_node_relate_clip(self, node_name):
        animator = self.ev_g_animator()
        if not animator:
            return
        source_node = animator.find(node_name)
        clip_list = []
        root_node = animator.find(node_name)
        if animation_const.SOURCE_NODE_TYPE in root_node.nodeType:
            clip_list.append(root_node.clipName)
        else:
            all_child_states = root_node.GetChildStates()
            for one_child_state in all_child_states:
                one_child_node = one_child_state.childNode
                if animation_const.SOURCE_NODE_TYPE in one_child_node.nodeType:
                    clip_list.append(one_child_node.clipName)
                else:
                    sub_clip_list = self.get_node_relate_clip(one_child_node.nodeName)
                    clip_list.extend(sub_clip_list)

        return clip_list

    def switch_to_status(self, status):
        pass

    def reset(self):
        if self._animator:
            self._animator.reset()

    def get_model_socket_matrix(self, socket_name):
        if not self.model:
            return
        return self.model.get_socket_matrix(socket_name, world.SPACE_TYPE_WORLD)

    def get_head_position(self):
        model = self.model
        if model:
            matrix = model.get_bone_matrix(animation_const.BONE_HEAD_NAME, world.SPACE_TYPE_WORLD)
            if matrix:
                return matrix.translation
        return None

    def is_mecha(self):
        return False