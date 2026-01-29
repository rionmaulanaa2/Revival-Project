# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/animate/animator.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
import world
Player = None
SOURCE_NODE_TYPE = 'Source'
BLEND_NODE_TYPE = 'Blend'

class Animator(object):

    def __init__(self, model, assetPath, unit_obj):
        super(Animator, self).__init__()
        self.load_task_id = 0
        self.__rootAnimationNode__ = None
        self._assetPath = assetPath
        self.__animator = model.get_animator()
        self.active = True
        self._load_callback_info = None
        self._param_listener = {}
        self._active_event = {}
        self._deactive_event = {}
        self._state_enter_event = {}
        self._state_exit_event = {}
        self._model = model
        self._unit_obj = unit_obj
        self._anim_key_dict = {}
        self._already_register_anim_keys = set()
        self._already_anim_event_dict = {}
        return

    def set_owner(self, unit_obj):
        self._unit_obj = unit_obj

    def Load(self, use_async=True, callback=None, arg=None):
        loader = world.get_animation_tree_loader()
        if callback:
            self._load_callback_info = (
             callback, arg)
        else:
            self._load_callback_info = None
        self.set_on_activate_clip_callback(self.on_active_clip_node)
        import game3d
        if global_data.is_renderer2:
            if use_async:
                self.load_task_id = loader.LoadTree(self._model, self._assetPath, game3d.ASYNC_ULTIMATE_HIGH, self.onAnimatorLoaded, None)
            else:
                rootNode = loader.LoadTree(self._model, self._assetPath)
                self.onAnimatorLoaded(rootNode)
        elif use_async:
            self.load_task_id = loader.LoadTree(self.__animator, self._assetPath, game3d.ASYNC_ULTIMATE_HIGH, self.onAnimatorLoaded, None)
        else:
            rootNode = loader.LoadTree(self.__animator, self._assetPath)
            self.onAnimatorLoaded(rootNode)
        return

    def pause(self):
        t_animator = self.animator
        if not t_animator:
            return
        root_node = t_animator.GetRootNode()
        root_node.timeScale = 0

    def resume(self):
        t_animator = self.animator
        if not t_animator:
            return
        root_node = t_animator.GetRootNode()
        root_node.timeScale = 1

    def set_is_mainplayer(self, is_main):
        t_animator = self.animator
        if t_animator:
            t_animator.SetIsMainplayer(is_main)

    def clear_anim_events(self):
        self._param_listener = {}
        self._active_event = {}
        self._deactive_event = {}
        self._state_enter_event = {}
        self._state_exit_event = {}
        self._anim_key_dict = {}
        already_register_anim_keys = self._already_register_anim_keys
        self._already_register_anim_keys = set()
        self._already_anim_event_dict = {}
        model = self.model
        if not model:
            return
        if self.animator:
            self.animator.StopAnimTrigger()
        for clip_name in already_register_anim_keys:
            model.clear_anim_key_event(clip_name)

    def is_loaded(self):
        return self.__rootAnimationNode__ != None

    @property
    def model(self):
        if self._model and self._model.valid:
            return self._model
        else:
            return None

    @property
    def animator(self):
        if global_data.is_renderer2:

            class DualWrapper(object):

                def __init__(self, anim_ctrl, animator):
                    self.anim_ctrl = anim_ctrl
                    self.animator = animator

                def __getattr__(self, name):
                    if self.animator and hasattr(self.animator, name):
                        return getattr(self.animator, name)
                    return getattr(self.anim_ctrl, name)

            if self.model:
                return DualWrapper(self.__animator, self.__rootAnimationNode__)
            return None
        else:
            if self.model:
                return self.__animator
            return None

    def add_trigger_clip(self, clip_name, trigger_name, callback, data=None):
        t_animator = self.animator
        if t_animator:
            t_animator.AddTriggerClip(clip_name)
        self.__register_anim_key_event(clip_name, trigger_name, callback, data)

    def show_bones(self, is_show):
        if self.animator:
            self.animator.ShowBones(is_show)

    def _create_clip_event_callback(self, clip_name, trigger_name, callback, data):
        do_real_register = False
        if clip_name not in self._already_anim_event_dict:
            self._already_anim_event_dict[clip_name] = {}
        clip_dict = self._already_anim_event_dict[clip_name]
        if trigger_name not in clip_dict:
            clip_dict[trigger_name] = []
            do_real_register = True
        callback_list = clip_dict[trigger_name]
        callback_list.append((callback, data))
        if do_real_register:

            def clip_event_callback(model, anim_name, trigger_event):
                if clip_name != anim_name or trigger_name != trigger_event:
                    return
                _callback_list = self._already_anim_event_dict.get(anim_name, {}).get(trigger_event, [])
                for _callback, _data in _callback_list:
                    if _data:
                        _callback(model, anim_name, trigger_event, _data)
                    else:
                        _callback(model, anim_name, trigger_event)

            self._model.register_anim_key_event(clip_name, trigger_name, clip_event_callback, None)
        return

    def __register_anim_key_event(self, clip_name, trigger_name, callback, data=None):
        clip_dict = self._anim_key_dict.setdefault(clip_name, {})
        self._already_register_anim_keys.add(clip_name)
        if isinstance(trigger_name, str):
            trigger_name = [
             trigger_name]
        for one_trigger_name in trigger_name:
            if one_trigger_name not in clip_dict:
                clip_dict[one_trigger_name] = [
                 (
                  callback, data)]
            else:
                clip_dict[one_trigger_name].append((callback, data))

    def on_active_clip_node(self, clip_name, *args):
        if not self.model or not self._anim_key_dict:
            return
        else:
            clip_dict = self._anim_key_dict.get(clip_name, None)
            if clip_dict:
                del self._anim_key_dict[clip_name]
                for trigger_name, trigger_configs in six_ex.items(clip_dict):
                    for one_trigger_config in trigger_configs:
                        if self._model.has_anim_event(clip_name, trigger_name):
                            self._create_clip_event_callback(clip_name, trigger_name, one_trigger_config[0], one_trigger_config[1])

            if not self._anim_key_dict:
                self._anim_key_dict = {}
            return

    def set_phase(self, node_name, phase):
        if not node_name:
            return
        else:
            if phase is None:
                return
            animation_node = self.find(node_name)
            if not animation_node:
                return
            animation_node.phase = phase
            if SOURCE_NODE_TYPE in animation_node.nodeType:
                return
            all_child_states = animation_node.GetChildStates()
            for index, one_child_state in enumerate(all_child_states):
                one_source_node = one_child_state.childNode
                one_source_node.phase = phase

            return

    def real_replace_clip_name(self, node_name, clip_name, is_keep_phase, force, is_log=False):
        if isinstance(node_name, str):
            source_node = self.find(node_name)
        else:
            source_node = node_name
        if not source_node:
            return
        if force or clip_name != source_node.clipName:
            phase = source_node.phase
            source_node.clipName = clip_name
            if is_keep_phase:
                source_node.phase = phase
            else:
                source_node.phase = 0
            if is_log:
                print(('test--real_replace_clip_name--step1--clip_name =', clip_name, '--phase =', source_node.phase))
        self.on_active_clip_node(clip_name)

    def replace_clip_name(self, node_name, clip_name, is_keep_phase=False, force=False, is_log=False):
        if not clip_name:
            return
        if global_data.on_post_logic:
            global_data.game_mgr.next_exec(self.real_replace_clip_name, node_name, clip_name, is_keep_phase, force, is_log)
        else:
            self.real_replace_clip_name(node_name, clip_name, is_keep_phase=is_keep_phase, force=force, is_log=is_log)

    def RegisterParamListener(self, param_name, node_name, callback, data=None):
        if param_name not in self._param_listener:
            self._param_listener[param_name] = {}
        param_config = self._param_listener[param_name]
        if node_name not in param_config:
            param_config[node_name] = []
        param_config[node_name].append((callback, data))

    def ClearParamListenerByNode(self, node_name):
        for one_param_config in six_ex.values(self._param_listener):
            if node_name in one_param_config:
                del one_param_config[node_name]

    def OnParamValueChange(self, param_name, value):
        param_config = self._param_listener.get(param_name, None)
        if not param_config:
            return
        else:
            dead_node = []
            for node_name, callback_list in six_ex.items(param_config):
                one_node = self.find(node_name)
                if one_node and not one_node.IsActiveInHierarchy():
                    dead_node.append(node_name)
                    continue
                for callback, data in callback_list:
                    if data is None:
                        callback(node_name, param_name, value)
                    else:
                        callback(node_name, param_name, value, data)

            for node_name in dead_node:
                del param_config[node_name]

            return

    def SetActive(self, flag):
        self.active = flag

    def GetXmlFile(self):
        return self._assetPath

    def SetXmlFile(self, assetPath):
        self._assetPath = assetPath

    def Replace(self, path):
        self.Clear()
        self.SetXmlFile(path)
        self.Load(False)

    def Clear(self):
        if self.load_task_id != 0:
            loader = world.get_animation_tree_loader()
            loader.CancelLoadTask(self.load_task_id)
            self.load_task_id = 0
        self.__rootAnimationNode__ = None
        t_animator = self.animator
        if t_animator:
            t_animator.DeactivateAnimationTree()
            t_animator.SetEmptyTree()
        loader = world.get_animation_tree_loader()
        loader.ClearCache()
        self.SetXmlFile('')
        return

    def Reload(self):
        if self.load_task_id != 0:
            loader = world.get_animation_tree_loader()
            loader.CancelLoadTask(self.load_task_id)
            self.load_task_id = 0
        self.__rootAnimationNode__ = None
        t_animator = self.animator
        if t_animator:
            t_animator.DeactivateAnimationTree()
            t_animator.SetEmptyTree()
        loader = world.get_animation_tree_loader()
        loader.ClearCache()
        self.Load(False)
        return

    def destroy(self):
        if self.load_task_id != 0:
            loader = world.get_animation_tree_loader()
            loader.CancelLoadTask(self.load_task_id)
            self.load_task_id = 0
        self._param_listener = None
        self._active_event = None
        self._deactive_event = None
        self._state_enter_event = None
        self._state_exit_event = None
        self._anim_key_dict = None
        self.__animator = None
        self.__rootAnimationNode__ = None
        self._unit_obj = None
        self._model = None
        self._load_callback_info = None
        return

    def onAnimatorLoaded(self, rootNode, *args):
        if not self._unit_obj or not self._unit_obj.is_valid():
            return
        else:
            if global_data.is_renderer2:
                self.load_task_id = 0
                self.__rootAnimationNode__ = rootNode
                animator = rootNode
                animator.ActivateAnimationTree()
                self.__animator.AddAnimator(animator)
                self.__animator.SetActiveAnimator(animator)
                if self._load_callback_info:
                    callback, arg = self._load_callback_info
                    callback(arg)
                    self._load_callback_info = None
                return
            self.load_task_id = 0
            self.__rootAnimationNode__ = rootNode
            t_animator = self.animator
            if t_animator:
                if global_data.enable_cache_animation:
                    t_animator.PreloadSourceNode()
                t_animator.SetAnimationTree(rootNode)
                t_animator.ActivateAnimationTree()
            if self._load_callback_info:
                callback, arg = self._load_callback_info
                callback(arg)
                self._load_callback_info = None
            return

    def SupportFillEmptyAnim(self):
        if not self.__animator:
            return False
        return hasattr(self.__animator, 'SupportFillEmptyAnim')

    def TrySetAsyncLoad(self, value):
        if self.__animator and hasattr(self.__animator, 'is_asyncload'):
            self.__animator.is_asyncload = value
            return True
        return False

    def SetInt(self, name, value):
        if not self.active or value is None:
            return
        else:
            if self.__rootAnimationNode__:
                old_value = self.GetInt(name)
                t_animator = self.animator
                if t_animator:
                    t_animator.SetInt(name, value)
                if old_value != value:
                    self.OnParamValueChange(name, value)
            return

    def GetInt(self, name):
        if self.__rootAnimationNode__:
            t_animator = self.animator
            if t_animator:
                return t_animator.GetInt(name)

    def SetFloat(self, name, value):
        if not self.active or value is None:
            return
        else:
            if self.__rootAnimationNode__:
                t_animator = self.animator
                if t_animator:
                    t_animator.SetFloat(name, value)
            return

    def GetFloat(self, name):
        if self.__rootAnimationNode__:
            t_animator = self.animator
            if t_animator:
                return t_animator.GetFloat(name)

    def SetBool(self, name, value):
        if not self.active or value is None:
            return
        else:
            if self.__rootAnimationNode__:
                t_animator = self.animator
                if t_animator:
                    t_animator.SetBool(name, value)
            return

    def GetBool(self, name):
        if self.__rootAnimationNode__:
            t_animator = self.animator
            if t_animator:
                return t_animator.GetBool(name)

    def SetTrigger(self, name):
        if not self.active:
            return
        if self.__rootAnimationNode__:
            t_animator = self.animator
            if t_animator:
                t_animator.SetTrigger(name)

    def SetIgnoreParamError(self, enable):
        if not self.active:
            return
        if self.__rootAnimationNode__:
            t_animator = self.animator
            if t_animator:
                t_animator.SetIgnoreParamError(enable)

    def GetIgnoreParamError(self):
        if not self.active:
            return
        if self.__rootAnimationNode__:
            t_animator = self.animator
            if t_animator:
                return t_animator.GetIgnoreParamError()

    def RegSlaveAnimator(self, slave_name, slave_animator):
        if not self.active:
            return
        if self.__rootAnimationNode__:
            t_animator = self.animator
            if t_animator:
                t_animator.RegSlaveAnimator(slave_name, slave_animator.animator)

    def SetEnableUpdateBones(self, enable):
        if not self.active:
            return
        if self.__rootAnimationNode__:
            t_animator = self.animator
            if t_animator:
                t_animator.SetEnableUpdateBones(enable)

    def CopyParamTo(self, dst_animator):
        if not self.active:
            return
        if self.__rootAnimationNode__:
            t_animator = self.animator
            if t_animator:
                t_animator.CopyParamTo(dst_animator)

    def CopyNodeAttrTo(self, dst_animator):
        if not self.active:
            return
        if self.__rootAnimationNode__:
            t_animator = self.animator
            if t_animator:
                t_animator.CopyNodeAttrTo(dst_animator)

    def CopyBoneInfoFrom(self, src_animator):
        if not self.active:
            return
        if self.__rootAnimationNode__:
            t_animator = self.animator
            if t_animator:
                t_animator.CopyBoneInfoFrom(src_animator)

    def GetRootAnimNode(self):
        return self.__rootAnimationNode__

    def SetRootAnimNode(self, rootNode):
        self.__rootAnimationNode__ = rootNode
        t_animator = self.animator
        if t_animator:
            t_animator.SetAnimationTree(rootNode, True)

    def print_parameter(self):
        msg = ''
        if self.__rootAnimationNode__:
            t_animator = self.animator
            if t_animator:
                msg = t_animator.PrintAllParameter()
                msg = msg or ''
        return msg

    def print_node_info(self, name, active=False):
        self.print_parameter()
        node = self.find(name)
        if node:
            node.PrintTree(0, '', active)

    def print_info(self, active=False):
        msg = self.print_parameter()
        if self.__rootAnimationNode__:
            t_animator = self.animator
            if t_animator:
                tree_info = t_animator.PrintTree(active)
                tree_info = tree_info or ''
                msg += tree_info
        return msg

    def set_speed(self, scale):
        t_animator = self.animator
        if t_animator:
            t_animator.SetSpeed(scale)

    def enable_force_update(self, enable):
        t_animator = self.animator
        if t_animator:
            t_animator.EnableForceUpdate(enable)

    def set_on_activate_clip_callback(self, callback):
        t_animator = self.animator
        if t_animator:
            t_animator.SetOnActivateClipCallback(callback)

    def find(self, name):
        if self.__rootAnimationNode__:
            t_animator = self.animator
            if t_animator:
                return t_animator.Find(name)

    def reset(self):
        if self.__rootAnimationNode__:
            t_animator = self.animator
            if t_animator:
                t_animator.ResetAllParameter()

    def register_one_type_event(self, arg, callback, event_dict):
        if not isinstance(arg, (list, tuple)):
            arg = (
             arg,)
        for one_arg in arg:
            event_list = event_dict.setdefault(one_arg, [])
            event_list.append(callback)

    def unregister_one_type_event(self, arg, callback, event_dict):
        if not isinstance(arg, (list, tuple)):
            arg = (
             arg,)
        for one_arg in arg:
            event_list = event_dict.setdefault(one_arg, [])
            if callback in event_list:
                event_list.remove(callback)

    def _on_respond_one_type_node(self, arg, node_name, event_dict):
        if not self._unit_obj or not self._unit_obj.is_valid():
            return
        else:
            event_list = event_dict.get(arg, None)
            if event_list:
                for callback in event_list:
                    callback(arg, node_name)

            return

    def register_active_event(self, arg, callback):
        self.register_one_type_event(arg, callback, self._active_event)

    def unregister_active_event(self, arg, callback):
        self.unregister_one_type_event(arg, callback, self._active_event)

    def register_deactive_event(self, arg, callback):
        self.register_one_type_event(arg, callback, self._deactive_event)

    def unregister_deactive_event(self, arg, callback):
        self.unregister_one_type_event(arg, callback, self._deactive_event)

    def register_state_enter_event(self, arg, callback):
        self.register_one_type_event(arg, callback, self._state_enter_event)

    def unregister_state_enter_event(self, arg, callback):
        self.unregister_one_type_event(arg, callback, self._state_enter_event)

    def register_state_exit_event(self, arg, callback):
        self.register_one_type_event(arg, callback, self._state_exit_event)

    def unregister_state_exit_event(self, arg, callback):
        self.unregister_one_type_event(arg, callback, self._state_exit_event)