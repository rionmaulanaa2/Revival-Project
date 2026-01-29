# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_effect/ComMechaEffect8010.py
from __future__ import absolute_import
from .ComGenericMechaEffect import ComGenericMechaEffect
from logic.gcommon.common_const.character_anim_const import LOW_BODY
import world
DIAMOND_SS_SKIN_IDS = (201801054, 201801055, 201801056)
CTHULHU_SS_SKIN_IDS = (201801057, 201801058, 201801059)

class ComMechaEffect8010(ComGenericMechaEffect):
    BIND_EVENT = ComGenericMechaEffect.BIND_EVENT.copy()
    BIND_EVENT.update({'E_ON_SKIN_SUB_MODEL_LOADED': 'on_skin_sub_model_loaded'
       })

    def init_from_dict(self, unit_obj, bdict):
        super(ComMechaEffect8010, self).init_from_dict(unit_obj, bdict)
        self.need_handle_anim = False
        self.cur_sub_model_anim_name = ''
        self.handle_sub_model_anim_func = None
        return

    def destroy(self):
        super(ComMechaEffect8010, self).destroy()
        self.handle_sub_model_anim_func = None
        return

    def _handle_sub_model_anim_for_diamond_ss(self, anim_name):
        if anim_name == 's_transform_to_plane':
            sub_model_anim_name = 'transform_to_plane'
            loop_flag = world.PLAY_FLAG_NO_LOOP
        elif anim_name == 's_transform_to_body':
            sub_model_anim_name = 'transform_to_body_01'
            loop_flag = world.PLAY_FLAG_NO_LOOP
        elif self.ev_g_is_flight() or self.ev_g_is_flight_in_server():
            sub_model_anim_name = 'transform_idle'
            loop_flag = world.PLAY_FLAG_LOOP
        else:
            sub_model_anim_name = 'idle'
            loop_flag = world.PLAY_FLAG_LOOP
        if self.cur_sub_model_anim_name != sub_model_anim_name:
            self.sd.ref_socket_res_agent.play_model_res_anim((
             sub_model_anim_name, -1, world.TRANSIT_TYPE_DEFAULT, 0, loop_flag, self.sd.ref_anim_rate[LOW_BODY]), 'plane_only')
            self.cur_sub_model_anim_name = sub_model_anim_name

    def _handle_sub_model_anim_for_cthulhu_ss(self, anim_name):
        if anim_name in 's_transform_to_plane':
            sub_model_anim_name = 'open'
        elif anim_name == 's_transform_to_body':
            sub_model_anim_name = 'idle'
        elif self.ev_g_is_flight() or self.ev_g_is_flight_in_server():
            sub_model_anim_name = 'open'
        else:
            sub_model_anim_name = 'idle'
        if self.cur_sub_model_anim_name != sub_model_anim_name:
            self.sd.ref_socket_res_agent.play_model_res_anim((
             sub_model_anim_name, 300, world.TRANSIT_TYPE_IMM, 0, world.PLAY_FLAG_LOOP, self.sd.ref_anim_rate[LOW_BODY]), 'wing')
            self.cur_sub_model_anim_name = sub_model_anim_name

    def on_skin_sub_model_loaded(self):
        skin_id = self.ev_g_mecha_fashion_id()
        if skin_id in DIAMOND_SS_SKIN_IDS:
            self.handle_sub_model_anim_func = self._handle_sub_model_anim_for_diamond_ss
        elif skin_id in CTHULHU_SS_SKIN_IDS:
            self.handle_sub_model_anim_func = self._handle_sub_model_anim_for_cthulhu_ss
        else:
            self.handle_sub_model_anim_func = None
        if self.handle_sub_model_anim_func:
            anim_name = self.sd.ref_low_body_anim if self.sd.ref_low_body_anim else 'idle'
            self.handle_sub_model_anim_func(anim_name)
        return

    def on_trigger_anim_effect(self, anim_name, part, force_trigger_effect=False, socket_index=-1):
        super(ComMechaEffect8010, self).on_trigger_anim_effect(anim_name, part, force_trigger_effect, socket_index)
        if self.handle_sub_model_anim_func and part == LOW_BODY:
            self.handle_sub_model_anim_func(anim_name)