# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComAgentCapsule.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from logic.gcommon import const
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gcommon.common_const.assistant_const import BUSY
from logic.gcommon.cdata import status_config as st_const

class ComAgentCapsule(UnitCom):
    BIND_EVENT = {'E_AGENT_COIN_CHANGED': ('_on_agent_coin_changed', -1),
       'E_TWIST_EGG': '_on_twist_egg',
       'E_CANCEL_TWIST': '_cancel_twist',
       'E_GET_CAPSULE': ('_on_get_capsule', -1),
       'E_CAPSULE_PREVIEW': ('_on_get_capsule_preview', -1),
       'E_DEL_CAPSULE': '_on_del_capsule',
       'E_USE_CAPSULE': '_on_use_capsule',
       'E_USE_BUILDING': '_on_use_building',
       'E_CANCEL_CALLING': '_on_cancel_calling',
       'E_TRY_BUILD': '_start_build_preview',
       'E_BUILD_CONFIRM': '_confirm_building',
       'E_BUILD_CANCEL': '_clear_building_status',
       'E_AGONY': '_clear_building_status',
       'G_IS_TWISTING': '_on_get_twisting',
       'G_TWIST_COST': '_on_get_next_coin_cost',
       'G_CUR_CAPSULE': '_on_cur_capsule',
       'G_BUILD_VALID': '_on_get_build_valid',
       'G_CALLING_CAPSULE': '_on_get_calling_capsule',
       'G_GET_PREVIEW_CAPSULE': '_on_get_preview_capsule',
       'G_GET_PREVIEW_TIME': '_on_get_preview_time'
       }

    def init_from_dict(self, unit_obj, bdict):
        super(ComAgentCapsule, self).init_from_dict(unit_obj, bdict)
        self._coin = bdict.get('coin', 0)
        self._twisted_cnt = bdict.get('capsule_cnt', 0)
        self._cur_capsule = bdict.get('cur_capsule', None)
        self._preview_capsule = bdict.get('cur_capsule_list', None)
        self._gen_capsule_time = bdict.get('gen_capsule_time', None)
        self._calling_capsule = None
        self._twisting = False
        self._cur_action = None
        self._is_register_cancel_event = False
        self._is_building = False
        self._preview_building = None
        self._start_use_pos = None
        global_data.emgr.scene_player_setted_event += self.on_player_setted
        return

    def _on_agent_coin_changed(self, coin_cnt, reason=None):
        delta = coin_cnt - self._coin
        self._coin = coin_cnt
        if delta > 0:
            if reason == const.SYS_ADD_COIN:
                global_data.emgr.sys_award_coin_event.emit(delta)
            else:
                global_data.emgr.agent_coin_get_event.emit(delta, reason)

    def _on_twist_egg(self):
        if self._twisting:
            return
        else:
            if self._calling_capsule:
                return
            if self._cur_capsule:
                self._on_del_capsule()
            if self is not None and self.is_valid():
                self._twisting = False
                self._twisted_cnt += 1
                self.send_event('E_CALL_SYNC_METHOD', 'gen_capsule', (), True)
            return

    def _on_get_capsule(self, capsule_id):
        self._cur_capsule = capsule_id
        self._preview_capsule = None
        if capsule_id:
            self.use_capsule()
        return

    def _on_get_capsule_preview(self, cap_list):
        from logic.gcommon import time_utility
        self._preview_capsule = cap_list
        self._gen_capsule_time = time_utility.get_server_time()

    def _on_del_capsule(self):
        self.send_event('E_CALL_SYNC_METHOD', 'del_capsule', (self._cur_capsule,), False)
        self._cur_capsule = None
        self._reset_capsule_status()
        return

    def _on_use_capsule(self, *args):
        if self._cur_capsule is None:
            return
        else:
            self._calling_capsule = self._cur_capsule
            self._cur_capsule = None
            self._reset_capsule_status()

            def finish():
                if self is not None and self.unit_obj.is_valid():
                    if self._calling_capsule is None:
                        return
                    self.send_event('E_CALL_SYNC_METHOD', 'use_capsule', (self._calling_capsule, args), True)
                    self._calling_capsule = None
                return

            if self.ev_g_assistant_status() == BUSY:
                self.send_event('E_ASSIST_GET_OFF', True)
            self.send_event('E_ADD_WORK_EVENT', self._calling_capsule, cb=finish)
            return

    def _on_cancel_calling(self):
        self._cur_capsule = self._calling_capsule
        self._calling_capsule = None
        if self._cur_capsule:
            self._reset_capsule_status()
        return

    def _on_use_building(self, building_id, building_no):
        if self._twisting:
            return

        def finish():
            if self is not None and self.unit_obj.is_valid():
                self._unregister_cancel_event()
                self.send_event('E_CALL_SYNC_METHOD', 'use_building', (building_id,), True)
            return

        def cancel():
            if self is not None and self.unit_obj.is_valid():
                self._unregister_cancel_event()
                self.send_event('E_STOP_TWIST')
            return

        from common.cfg import confmgr
        building_conf = confmgr.get('c_building_res', str(building_no))
        cap_id = building_conf['CapsuleId']
        capsule_conf = confmgr.get('c_capsule_info', str(cap_id))
        sing_time = capsule_conf.get('SingTime', 2)
        sing_time = 1 if sing_time <= 0 else sing_time
        self.send_event('E_ITEMUSE_CANCEL')
        global_data.emgr.capsule_show_progress_event.emit(sing_time, get_text_by_id(19014), cap_id, finish, 0, cancel)
        self._cur_action = const.ACTION_USE_CAPSULE
        self._register_cancel_event(sing_time)
        self.send_event('E_START_USE_BUILDING', building_no)

    def _on_get_next_coin_cost(self):
        from logic.gcommon import utility
        return (
         utility.calc_capsule_need_coin(self._twisted_cnt), self._coin)

    def _on_cur_capsule(self):
        return self._cur_capsule

    def _start_build_preview(self, building_no):
        if self._is_building:
            return
        else:
            self._is_building = True
            from logic.gcommon.common_utils.building_utils import PreviewBuilding, PreviewDrop
            if building_no is not None:
                self._preview_building = PreviewBuilding(building_no, self.unit_obj)
            else:
                self._preview_building = PreviewDrop(self._cur_capsule, self.unit_obj)
            self.need_update = True
            return

    def tick(self, delta):
        if self._is_building:
            self._preview_building.update()

    def _confirm_building(self, pos=None, rot=None):
        if self._cur_capsule is None:
            return
        else:
            self._calling_capsule = self._cur_capsule
            self._cur_capsule = None
            if self._calling_capsule == 7006:
                com_driver = self.unit_obj.get_com('ComHumanDriver')
                com_appearance = self.unit_obj.get_com('ComHumanAppearance')
                if com_driver:
                    com_driver._enable_bind_event(False, elist=['E_MOVE', 'E_CTRL_JUMP'])
                if com_appearance:
                    com_appearance._enable_bind_event(False, elist=['E_CTRL_SQUAT', 'E_CTRL_GROUND', 'E_MOVE', 'E_CTRL_JUMP', 'E_SET_MOVE_STATE', 'E_CHANGE_MOVE_STATE'])
                global_data.emgr.hide_scene_interaction_ui_event.emit('drone')
            if pos is None and rot is None:
                pos, rot = self._preview_building.get_valid_pos()

            def finish():
                if self is not None and self.unit_obj.is_valid():
                    if self._calling_capsule is None:
                        return
                    args = [
                     (
                      pos.x, pos.y, pos.z)]
                    if rot is not None:
                        args.append((rot.x, rot.y, rot.z, rot.w))
                    self.send_event('E_CALL_SYNC_METHOD', 'use_capsule', (self._calling_capsule, args), True)
                    self._calling_capsule = None
                return

            if self.ev_g_assistant_status() == BUSY:
                self.send_event('E_ASSIST_GET_OFF', True)
            self.send_event('E_ADD_WORK_EVENT', self._calling_capsule, pos, cb=finish)
            self._clear_building_status()
            return

    def _clear_building_status(self):
        self._is_building = False
        self.need_update = False
        if self._preview_building is not None:
            self._preview_building.destroy()
            self._preview_building = None
        return

    def _on_get_build_valid(self):
        if self._is_building:
            return self._preview_building.is_valid_pos()

    def _on_get_twisting(self):
        return self._twisting

    def _on_get_calling_capsule(self):
        return self._calling_capsule

    def _on_get_preview_capsule(self):
        return self._preview_capsule

    def _on_get_preview_time(self):
        return self._gen_capsule_time

    def destroy(self):
        global_data.emgr.scene_player_setted_event -= self.on_player_setted
        self._clear_building_status()
        super(ComAgentCapsule, self).destroy()

    def _register_cancel_event(self, sing_time):
        if self._is_register_cancel_event:
            return
        if not self._cur_action:
            return
        self.send_event('E_START_CAPSULE_ACTION', self._cur_action, sing_time)
        self._twisting = True
        self._is_register_cancel_event = True
        self._start_use_pos = self.ev_g_position()
        regist_event = self.regist_event
        regist_event('E_TRY_FIRE', self._cancel_twist)
        regist_event('E_POSITION', self._move_detect)
        regist_event('E_START_AUTO_FIRE', self._cancel_twist)
        regist_event('E_TRY_AIM', self._cancel_twist)
        regist_event('E_CTRL_JUMP', self._cancel_twist)
        regist_event('E_TRY_SWITCH', self._try_switch)
        regist_event('E_TRY_RELOAD', self._cancel_twist)
        regist_event('E_ENTER_DOOR_INTERACTION_ZONE', self._cancel_twist)
        regist_event('E_LEAVE_DOOR_INTERACTION_ZONE', self._cancel_twist)
        regist_event('E_DEATH', self._cancel_twist)
        regist_event('E_AGONY', self._cancel_twist)
        global_data.emgr.scene_pick_obj_event += self._cancel_twist

    def _unregister_cancel_event(self):
        if not self._is_register_cancel_event:
            return
        else:
            self.send_event('E_STOP_CAPSULE_ACTION')
            self._cur_action = None
            self._twisting = False
            self._is_register_cancel_event = False
            unregist_event = self.unregist_event
            unregist_event('E_TRY_FIRE', self._cancel_twist)
            unregist_event('E_POSITION', self._move_detect)
            unregist_event('E_START_AUTO_FIRE', self._cancel_twist)
            unregist_event('E_TRY_AIM', self._cancel_twist)
            unregist_event('E_CTRL_JUMP', self._cancel_twist)
            unregist_event('E_TRY_SWITCH', self._try_switch)
            unregist_event('E_TRY_RELOAD', self._cancel_twist)
            unregist_event('E_ENTER_DOOR_INTERACTION_ZONE', self._cancel_twist)
            unregist_event('E_LEAVE_DOOR_INTERACTION_ZONE', self._cancel_twist)
            unregist_event('E_DEATH', self._cancel_twist)
            unregist_event('E_AGONY', self._cancel_twist)
            global_data.emgr.scene_pick_obj_event -= self._cancel_twist
            return

    def _cancel_twist(self, *args, **kwargs):
        self.send_event('E_STOP_TWIST')
        self._reset_capsule_status()
        self._unregister_cancel_event()

    def _try_switch(self, weapon_pos, switch_status=True):
        if switch_status:
            self._cancel_twist()

    def _move_detect(self, new_pos, interrupt_dist=10):
        if self._start_use_pos:
            if (new_pos - self._start_use_pos).length > interrupt_dist:
                self._cancel_twist()
        else:
            self._start_use_pos = new_pos

    def on_player_setted(self, player):
        if player is None and self._twisting:
            global_data.emgr.battle_close_progress_event.emit(None)
            self._unregister_cancel_event()
        return

    def _reset_capsule_status(self):
        self.send_event('E_GET_CAPSULE', self._cur_capsule)

    def use_capsule(self):

        def check_result(res, pos=None, rot=None):
            if not self.is_valid():
                return
            self._checking = False
            if res:
                self.send_event('E_BUILD_CONFIRM', pos, rot)
            else:
                global_data.emgr.battle_show_message_event.emit(get_text_by_id(19012))

        from logic.gcommon.common_utils.building_utils import QuickUseBuilding, QuickUseDrop
        from common.cfg import confmgr
        capsule = self._cur_capsule
        capsule_conf = confmgr.get('c_capsule_info', str(capsule))
        cap_type = capsule_conf.get('CapType', 'common')
        if cap_type == 'common':
            self.send_event('E_USE_CAPSULE')
        elif cap_type == 'signal':
            self._checking = True
            QuickUseDrop(capsule, check_result)
        elif cap_type == 'building':
            self._checking = True
            QuickUseBuilding(capsule, check_result)
        else:
            log_error('Invalid capsule type {0}:{1}!!!!!!!!!!!!!!!!!!!!'.format(capsule, cap_type))
        return