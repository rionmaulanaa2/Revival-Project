# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/ScenePart.py
from __future__ import absolute_import
from __future__ import print_function
import six
from six.moves import range

class ScenePart(object):
    REMOVE_UPDATE_AFTER_LOOP = 'remove'
    INIT_EVENT = {}
    ENTER_EVENT = {}

    def __init__(self, scene, name, need_update=False):
        if name in scene.parts:
            print('[ERROR] scene parts has same name: {0}.'.format(name))
            name = id(self)
        self._need_update = need_update
        self._is_event_binded = [
         False, False]
        import weakref
        self.scene = weakref.ref(scene)
        scene.parts[name] = self
        if need_update:
            scene.update_part_list.add(self)
        self._sub_sys = {}
        self._bind_event(self.INIT_EVENT)
        self.init_ui()

    def _bind_event(self, events):
        if events is self.INIT_EVENT:
            idx = 0 if 1 else 1
            is_event_binded = self._is_event_binded
            einfo = is_event_binded[idx] or {}
            for event_name, func_name in six.iteritems(events):
                einfo[event_name] = getattr(self, func_name)

            global_data.emgr.bind_events(einfo)
            is_event_binded[idx] = True

    def _unbind_event(self, events):
        idx = 0 if events is self.INIT_EVENT else 1
        is_event_binded = self._is_event_binded
        if is_event_binded[idx]:
            einfo = {}
            for event_name, func_name in six.iteritems(events):
                einfo[event_name] = getattr(self, func_name)

            global_data.emgr.unbind_events(einfo)
            is_event_binded[idx] = False

    def get_scene(self):
        scn = self.scene()
        if scn and scn.valid:
            return scn

    @property
    def need_update(self):
        return self._need_update

    @need_update.setter
    def need_update(self, val):
        self._need_update = val
        scn = self.scene()
        if scn:
            if val:
                scn.update_part_list.add(self)
            elif self in scn.update_part_list:
                scn.update_part_list.remove(self)

    def on_before_load(self):
        pass

    def on_pre_load(self):
        pass

    def on_load(self):
        pass

    def register_sub_sys(self, cls_name):
        import logic.vscene.parts.factory as factory
        sub_sys = factory.load_sub_sys(cls_name)
        if sub_sys:
            self._sub_sys[cls_name] = sub_sys

    def on_enter(self):
        pass

    def enter(self):
        self._bind_event(self.ENTER_EVENT)
        self.on_enter()

    def on_exit(self):
        pass

    def exit(self):
        for k, v in six.iteritems(self._sub_sys):
            v.destroy()

        self._sub_sys = {}
        self.on_exit()
        self._part_ui_list = []
        self._todo_ui_index = 0

    def after_exit(self):
        self._unbind_event(self.INIT_EVENT)
        self._unbind_event(self.ENTER_EVENT)

    def pause(self, flag):
        if flag:
            self._unbind_event(self.ENTER_EVENT)
        else:
            self._bind_event(self.ENTER_EVENT)
        self.on_pause(flag)

    def on_pause(self, flag):
        pass

    def on_update(self, dt):
        pass

    def get_scene_objs(self):
        return []

    def on_touch_begin(self, touches):
        pass

    def on_touch_slide(self, dx, dy, touches, touch_pos, *args):
        pass

    def on_touch_end(self, touches):
        pass

    def on_touch_scale(self, delta, touches):
        pass

    def on_touch_tap(self, touches):
        pass

    def on_touch_doubletap(self, touches):
        pass

    def on_mouse_wheel(self, msg, delta, key_state):
        pass

    def init_ui(self):
        self._part_ui_list = []
        self._todo_ui_index = 0

    def add_to_loading_wrapper(self):
        self.scene().loading_wrapper.add_frame_load_ui_part(self)

    def load_ui_per_frame(self, dont_load=False):
        if self._todo_ui_index >= len(self._part_ui_list):
            return 1.0
        if not dont_load:
            is_show, name, module_path, args = self._part_ui_list[self._todo_ui_index]
            self._todo_ui_index += 1
            ui = global_data.ui_mgr.show_ui(name, module_path, *args)
            if ui:
                if is_show:
                    ui.enter_screen()
                else:
                    ui.leave_screen()
        return min(1.0, max(0.0, self._todo_ui_index / len(self._part_ui_list)))

    def on_create_part_ui(self):
        return
        for i in range(self._todo_ui_index, len(self._part_ui_list)):
            is_show, name, module_path, args = self._part_ui_list[i]
            ui = global_data.ui_mgr.show_ui(name, module_path, *args)
            if not ui:
                continue
            if is_show:
                ui.enter_screen()
            else:
                ui.leave_screen()

        self._todo_ui_index = len(self._part_ui_list)

    def on_destroy_part_ui(self):
        for is_show, name, module_path, args in self._part_ui_list:
            global_data.ui_mgr.close_ui(name)