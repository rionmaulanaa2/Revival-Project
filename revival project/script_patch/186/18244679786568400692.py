# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impGlideEffect.py
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Int, Str, Bool, List, Dict
from logic.gcommon.const import GEV_ONLY_ME, GEV_ONLY_FRIEND, GEV_ALL

class impGlideEffect(object):

    def _init_glideeffect_from_dict(self, bdict):
        self.glide_effect_visibility = bdict.get('glide_effect_visibility', GEV_ALL)
        self.glide_skin_to_effect = bdict.get('glide_skin_to_effect', {})
        self._temp_glide_show_aircaft_id = 0

    def set_aircraft_skin_glide_effect(self, skin_id, effect_id):
        self.call_server_method('set_aircraft_skin_glide_effect', (skin_id, effect_id))

    @rpc_method(CLIENT_STUB, (Dict('notify_details'),))
    def resp_change_glide_effect(self, notify_details):
        update = notify_details.get('update', {})
        remove = notify_details.get('remove', [])
        self.glide_skin_to_effect.update(update)
        for skin_id in remove:
            if skin_id in self.glide_skin_to_effect:
                del self.glide_skin_to_effect[skin_id]

        global_data.emgr.vehicle_sfx_chagne.emit()

    def get_aircraft_skin_glide_effect(self, skin_id):
        from logic.gcommon.item.item_const import DEFAULT_GLIDE_EFFECT
        skin_id = str(skin_id)
        if skin_id in self.glide_skin_to_effect:
            return self.glide_skin_to_effect[skin_id]
        else:
            return self.glide_skin_to_effect.get('0', DEFAULT_GLIDE_EFFECT)

    def change_glide_effect_visibility(self, visibility_option, is_force=False):
        if visibility_option not in (GEV_ONLY_ME, GEV_ONLY_FRIEND, GEV_ALL):
            log_error('change_glide_effect_binding: invalid visiblity_option %s' % visibility_option)
            return
        if is_force:
            self.glide_effect_visibility = visibility_option
        self.call_server_method('change_glide_effect_visibility', (visibility_option,))

    @rpc_method(CLIENT_STUB, (Int('visibility_option'),))
    def resp_change_glide_effect_visibility(self, visibility_option):
        self.glide_effect_visibility = visibility_option

    def _destroy_glideeffect(self):
        pass

    def set_glide_show_aircaft_id(self, aircraft_id):
        self._temp_glide_show_aircaft_id = aircraft_id

    def get_glide_show_aircaft_id(self):
        return self._temp_glide_show_aircaft_id