# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/proto/client/__init__.py
from __future__ import absolute_import
import six
import six_ex
methods = {}

def _load_proto_modules():
    global methods
    import inspect
    methods = {}
    protos = ('action_proto', 'armor_proto', 'assistant_proto', 'buff_proto', 'building_proto',
              'capsule_proto', 'common_proto', 'control_proto', 'crash_proto', 'fight_proto',
              'group_proto', 'health_proto', 'hiding_proto', 'house_proto', 'item_proto',
              'message_proto', 'parachute_proto', 'record_proto', 'spectate_proto',
              'throwable_proto', 'vehicle_proto', 'train_proto', 'weapon_proto',
              'attach_proto', 'status_proto', 'mecha_proto', 'dy_box_proto', 'explosive_robot_proto',
              'sync_data_proto', 'skill_proto', 'charger_proto', 'beacon_tower_proto',
              'battle_sound_ai_proto', 'firepower_proto', 'shop_proto', 'granbelm_proto',
              'ai_log_proto', 'gulag_proto', 'pve_proto')
    for package_name in protos:
        module = __import__(package_name, globals(), locals(), fromlist=[''], level=1)
        for method_name, method in inspect.getmembers(module, inspect.isfunction):
            if method_name in methods:
                raise Exception('[nca_method %s] has been defined' % method_name)
            methods[method_name] = method

    import logic.gcommon.common_utils.idx_utils as idx_utils
    from logic.gcommon.component.proto.proto_salt import client_proto as salt_client
    idx_utils.init_client_proto(six_ex.keys(methods), salt_client)
    new_methods = {}
    for method_name, method in six.iteritems(methods):
        idx = idx_utils.c_method_2_idx(method_name)
        new_methods[idx] = method

    methods = new_methods
    if G_IS_CLIENT:
        from logic.gcommon.component.proto.proto_salt import server_proto as salt_server
        idx_utils.init_server_proto([], salt_server)


_load_proto_modules()

def call(method_name, synchronizer, parameters):
    methods[method_name](synchronizer, *parameters)