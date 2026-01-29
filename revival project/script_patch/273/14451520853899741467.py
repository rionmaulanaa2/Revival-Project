# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/behavior_utils.py
from __future__ import absolute_import
import six_ex
from logic.gcommon import behavior
from logic.gcommon.behavior.module_path_of_states import state_name_to_module_path_map, module_path_to_state_name_list_map
from logic.gcommon.behavior.StateBase import StateBase
import inspect
import sys
import os
state_name_to_cls_map = {}

def reload_state_name_to_module_path_map():
    return
    behavior_dir_path = os.path.dirname(behavior.__file__)
    state_name_to_module_path_map.clear()
    module_path_to_state_name_list_map.clear()
    mpath_list = []
    module_list = []
    for file_name in os.listdir(behavior_dir_path):
        if file_name == '__init__.py':
            continue
        mpath = 'logic.gcommon.behavior.%s' % file_name[:-3]
        mpath_list.append(mpath)
        mod = sys.modules.get(mpath)
        if not mod:
            mod = __import__(mpath, globals(), locals())
        module_list.append(mod)

    for mpath in mpath_list:
        mod = sys.modules.get(mpath)
        classes = inspect.getmembers(mod, inspect.isclass)
        for name, cls in classes:
            if hasattr(cls, '__module__') and cls.__module__ == mpath and issubclass(cls, StateBase):
                state_name_to_module_path_map[name] = mpath
                if mpath not in module_path_to_state_name_list_map:
                    module_path_to_state_name_list_map[mpath] = []
                module_path_to_state_name_list_map[mpath].append(name)

    name_list = six_ex.keys(state_name_to_module_path_map)
    name_list.sort()
    output_str_list = ['# -*- coding:utf-8 -*-\n\nstate_name_to_module_path_map = {']
    for name in name_list:
        output_str_list.append("\t'%s': '%s'," % (name, state_name_to_module_path_map[name]))

    output_str_list.append('}\n')
    module_path_list = six_ex.keys(module_path_to_state_name_list_map)
    module_path_list.sort()
    output_str_list.append('module_path_to_state_name_list_map = {')
    for module_path in module_path_list:
        output_str_list.append("\t'%s': %s," % (module_path, str(tuple(module_path_to_state_name_list_map[module_path]))))

    output_str_list.append('}\n')
    with open('%s/module_path_of_states.py' % behavior_dir_path, 'w') as f:
        f.write('\n'.join(output_str_list))


CHILDLESS_EVER_STATE_CLASS_INFO = {'AccumulateShoot': {
                     'AccumulateShoot', 'AccumulateShootHover', 'AccumulateShoot8006', 'AccumulateShoot8011', 'AccumulateShoot8013',
                     'AccumulateShoot8017', 'AccumulateShoot8019', 'AccumulateShoot8020', 'AccumulateShoot8029'},
   'JumpUp': {
            'JumpUp', 'HumanJumpUp', 'HumanSuperJumpUp', 'MultipleJumpUp', 'JumpUp8003', 'JumpUp8006',
            'RisingDragon', 'JumpUp8013', 'JumpUp8019', 'JumpUp8020', 'JumpUp8025', 'JumpUp8030',
            'JumpUpWithForceDec', 'JumpUp8033', 'JumpUp8034'},
   'Fall': {
          'Fall', 'HumanFall', 'Fall4108', 'Fall8004', 'Fall8007', 'Fall8008', 'Fall8010',
          'Fall8019', 'Fall8020', 'CarFall', 'Fall8022', 'DashFall8022', 'Fall8024', 'SprintFall',
          'FallWithForceDec'},
   'SuperJumpUp': {
                 'SuperJumpUp', 'SuperJumpUp8007', 'SuperJumpUp8010', 'SuperJumpUp8020',
                 'CarSuperJumpUp', 'SprintSuperJumpUp', 'SuperJumpUpWithForceDec'},
   'OnGround': {
              'OnGround', 'OnGround8004', 'OnGround8007', 'OnGround8008', 'OnGround8010',
              'OnGround8019', 'OnGround8020', 'CarOnGround', 'OnGround8032', 'SprintOnGround', 'OnGround8033', 'OnGround8034',
              'OnGround4108', 'HumanOnGround'}
   }

def _warn_about_using_childless_ever_class(state_name):
    cls = state_name_to_cls_map[state_name]
    all_parent_classes = inspect.getmro(cls)
    for parent_cls in all_parent_classes:
        if parent_cls.__name__ in CHILDLESS_EVER_STATE_CLASS_INFO:
            if state_name not in CHILDLESS_EVER_STATE_CLASS_INFO[parent_cls.__name__]:
                global_data.game_mgr.show_tip('\xe5\x88\xab\xe5\x86\x8d\xe7\x94\xa8{}\xe5\x95\xa6\xef\xbc\x81\xef\xbc\x81\xe8\xae\xa9{}\xe6\x94\xb9\xe7\x94\xa8\xe5\xaf\xb9\xe5\xba\x94\xe7\x9a\x84pure\xe7\xb1\xbb\xe5\x90\xa7\xef\xbc\x81\xef\xbc\x81'.format(parent_cls.__name__, state_name))
                print '\xe5\x88\xab\xe5\x86\x8d\xe7\x94\xa8{}\xe5\x95\xa6\xef\xbc\x81\xef\xbc\x81\xe8\xae\xa9{}\xe6\x94\xb9\xe7\x94\xa8\xe5\xaf\xb9\xe5\xba\x94\xe7\x9a\x84pure\xe7\xb1\xbb\xe5\x90\xa7\xef\xbc\x81\xef\xbc\x81'.format(parent_cls.__name__, state_name)
            return


def get_state(state_name):
    if state_name in state_name_to_cls_map:
        return state_name_to_cls_map[state_name]()
    else:
        if state_name not in state_name_to_module_path_map:
            reload_state_name_to_module_path_map()
            if state_name not in state_name_to_module_path_map:
                log_error('Can not find class -- %s' % state_name)
                return get_state('StateBase')
        mpath = state_name_to_module_path_map[state_name]
        mod = sys.modules.get(mpath)
        if not mod:
            __import__(mpath, globals(), locals())
            mod = sys.modules.get(mpath)
        for cls_name in module_path_to_state_name_list_map[mpath]:
            cls = getattr(mod, cls_name, None)
            if not cls:
                cls = StateBase
            state_name_to_cls_map[cls_name] = cls

        return state_name_to_cls_map[state_name]()