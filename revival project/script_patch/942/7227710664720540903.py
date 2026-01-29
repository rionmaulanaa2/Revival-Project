# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/behavior/PVEMonsterLinkLogic.py
from __future__ import absolute_import
from .MonsterStateBase import MonsterStateBase
import math3d
from logic.gcommon.common_const.character_anim_const import LOW_BODY
import collision
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gutils.pve_utils import get_aim_pos, get_socket_pos

class MonsterLinkBase(MonsterStateBase):
    BIND_EVENT = {'E_ACTIVE_PARAM_STATE': 'pre_check_param'
       }
    econf = {}
    S_END = 0
    S_PRE = 1
    S_LINK = 2
    S_BAC = 3

    def pre_check_param(self, state, *args):
        if state != self.sid:
            return
        if self.is_active:
            return False
        if not self.check_can_active():
            return False
        self.editor_handle()
        self.skill_id, self.target_id, self.target_pos = args
        self.target_pos = math3d.vector(*self.target_pos)
        self.active_self()

    def init_from_dict(self, unit_obj, bdict, sid, info):
        super(MonsterLinkBase, self).init_from_dict(unit_obj, bdict, sid, info)
        self.init_params()
        self.process_event(True)
        self.sub_state = self.S_END

    def init_params(self):
        self.target_id = None
        self.target_pos = None
        self.link_timer = None
        self.link_sfx = None
        self.link_sfx_id = None
        return

    def editor_handle(self):
        pass

    def process_event(self, is_bind):
        emgr = global_data.emgr
        if is_bind:
            emgr.bind_events(self.econf)
        else:
            emgr.unbind_events(self.econf)

    def on_init_complete(self):
        super(MonsterLinkBase, self).on_init_complete()
        self.register_link_callbacks()

    def register_link_callbacks(self):
        self.register_substate_callback(self.S_PRE, 0, self.start_pre)
        self.register_substate_callback(self.S_PRE, self.pre_anim_dur / self.pre_anim_rate, self.end_pre)
        self.register_substate_callback(self.S_LINK, 0, self.start_link)

    def start_pre(self):
        self.send_event('E_ANIM_RATE', LOW_BODY, self.pre_anim_rate)
        if self.pre_anim:
            self.send_event('E_POST_ACTION', self.pre_anim, LOW_BODY, 1)

    def end_pre(self):
        self.sub_state = self.S_LINK

    def start_link(self):
        self.send_event('E_ANIM_RATE', LOW_BODY, self.link_anim_rate)
        if self.link_anim:
            self.send_event('E_POST_ACTION', self.link_anim, LOW_BODY, 1, loop=True)
        self.init_link_sfx()

    def enter(self, leave_states):
        super(MonsterLinkBase, self).enter(leave_states)
        self.send_event('E_CALL_SYNC_METHOD', 'pve_enter_skill', (self.skill_id,), True)
        self.sub_state = self.S_PRE

    def update(self, dt):
        super(MonsterLinkBase, self).update(dt)
        if self.sub_state == self.S_END:
            self.disable_self()

    def exit(self, enter_states):
        self.clear_sfx()
        self.gen_end_sfx()
        super(MonsterLinkBase, self).exit(enter_states)
        self.sub_state = self.S_END
        self.send_event('E_CALL_SYNC_METHOD', 'pve_end_skill', (self.skill_id,), True)

    def destroy(self):
        self.process_event(False)
        super(MonsterLinkBase, self).destroy()

    def init_link_sfx(self):
        self.gen_link_sfx()
        self.reset_link_timer()
        self.link_timer = global_data.game_mgr.register_logic_timer(self.tick_link_sfx, 1)

    def reset_link_timer(self):
        if self.link_timer:
            global_data.game_mgr.unregister_logic_timer(self.link_timer)
            self.link_timer = None
        return

    def gen_link_sfx(self):
        if self.link_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.link_sfx_id)
        end_pos = get_socket_pos(self.target_id, self.target_socket)

        def cb(sfx):
            if self.link_sfx_scale:
                sfx.scale = math3d.vector(self.link_sfx_scale, self.link_sfx_scale, self.link_sfx_scale)
            self.link_sfx = sfx
            sfx.end_pos = end_pos

        self.link_sfx_id = global_data.sfx_mgr.create_sfx_on_model(self.link_sfx_res, self.ev_g_model(), self.link_socket, on_create_func=cb)

    def tick_link_sfx(self):
        if self.link_sfx:
            end_pos = get_socket_pos(self.target_id, self.target_socket)
            self.link_sfx.end_pos = end_pos

    def clear_link_sfx(self):
        self.reset_link_timer()
        if self.link_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.link_sfx_id)
            self.link_sfx_id = None
            self.link_sfx = None
        return

    def clear_sfx(self):
        self.clear_link_sfx()

    def gen_end_sfx(self):
        if not self.end_sfx_res:
            return
        end_pos = get_socket_pos(self.target_id, self.target_socket)

        def cb(sfx):
            if self.end_sfx_scale:
                sfx.scale = math3d.vector(self.end_sfx_scale, self.end_sfx_scale, self.end_sfx_scale)
            sfx.end_pos = end_pos

        global_data.sfx_mgr.create_sfx_on_model(self.end_sfx_res, self.ev_g_model(), self.end_socket, on_create_func=cb)


class MonsterLink(MonsterLinkBase):

    def init_params(self):
        super(MonsterLink, self).init_params()
        self.skill_id = self.custom_param.get('skill_id', 9015155)
        self.pre_anim = self.custom_param.get('pre_anim', '')
        self.pre_anim_dur = self.custom_param.get('pre_anim_dur', 0)
        self.pre_anim_rate = self.custom_param.get('pre_anim_rate', 1.0)
        self.link_anim = self.custom_param.get('link_anim', '')
        self.link_anim_rate = self.custom_param.get('link_anim_rate', 1.0)
        self.link_socket = self.custom_param.get('link_socket', 'fx_kaihuo')
        self.link_sfx_res = self.custom_param.get('link_sfx_res', '')
        self.link_sfx_scale = self.custom_param.get('link_sfx_scale', None)
        self.end_socket = self.custom_param.get('end_socket', 'fx_kaihuo')
        self.end_sfx_res = self.custom_param.get('end_sfx_res', '')
        self.end_sfx_scale = self.custom_param.get('end_sfx_scale', None)
        self.height_offset = self.custom_param.get('height_offset', 0)
        self.target_socket = self.custom_param.get('target_socket', 'fx_root')
        return

    def editor_handle(self):
        if global_data.use_sunshine:
            self.init_params()
            self.reset_sub_states_callback()
            self.register_link_callbacks()