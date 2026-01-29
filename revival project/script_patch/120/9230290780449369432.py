# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/model_utils.py
from __future__ import absolute_import
from __future__ import print_function
from six.moves import range

def get_socket_objects(model, bind_point):
    if model and model.has_socket(bind_point):
        return model.get_socket_objects(bind_point)
    return ()


def unbind_owner_from_vehicle(self, owner_id):
    is_log = 0
    if not owner_id:
        if is_log:
            print(('test--unbind_owner_from_vehicle--step1--owner_id =', owner_id, '--global_data.cam_lplayer =', global_data.cam_lplayer, '--unit_obj =', self.unit_obj))
        return
    if not global_data.player or not global_data.player.logic or not global_data.cam_lplayer:
        if is_log:
            print(('test--unbind_owner_from_vehicle--step2--owner_id =', owner_id, '--global_data.cam_lplayer =', global_data.cam_lplayer, '--unit_obj =', self.unit_obj))
        return
    from mobile.common.EntityManager import EntityManager
    if owner_id:
        target = EntityManager.getentity(owner_id)
        if target and target.logic:
            passenger_model = target.logic.ev_g_model()
            vehicle_model = self.ev_g_model()
            if vehicle_model and passenger_model and passenger_model.get_parent() == vehicle_model:
                if is_log:
                    print(('test--unbind_owner_from_vehicle--step5--passenger_model.filename =', passenger_model.filename, '--vehicle_model.filename =', vehicle_model.filename, '--passenger_model.get_parent =', passenger_model.get_parent(), '--unit_obj =', self.unit_obj))
                    import traceback
                    traceback.print_stack()
                vehicle_model.unbind(passenger_model)
                scene = self.scene
                if scene:
                    scene.add_object(passenger_model)