# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComSelector.py
from __future__ import absolute_import
from __future__ import print_function
import six
from ..UnitCom import UnitCom
from logic.gcommon.component.com_factory import UnitComMetaclass
from logic.gutils.client_unit_tag_utils import preregistered_tags
import logic.gcommon.common_utils.target_com_utils as tc_utils
import traceback
import math3d

class ForwardEventMeta(UnitComMetaclass):

    def __init__(cls, name, bases, dic):
        FORWARD_EVENT = cls.FORWARD_EVENT
        DYNAMIC_FORWORD_EVENTS = cls.DYNAMIC_FORWORD_EVENTS

        def _get(evt_name):

            def handler_get(self, *arg, **kwarg):
                if self.ctrl_target and self.ctrl_target.logic:
                    if self.ctrl_target.logic == self.unit_obj:
                        print('get==>', evt_name, arg, kwarg, self.ctrl_target.logic)
                        traceback.print_stack()
                        return None
                    return self.ctrl_target.logic.get_value(evt_name, *arg, **kwarg)
                else:
                    return None

            return handler_get

        def _send(evt_name):

            def handler_send(self, *arg, **kwarg):
                if self.ctrl_target and self.ctrl_target.logic:
                    self.ctrl_target.logic.send_event(evt_name, *arg, **kwarg)

            return handler_send

        for ename in FORWARD_EVENT:
            handler_name = '_handle_%s' % ename.lower()
            if ename.startswith('G_'):
                setattr(cls, handler_name, _get(ename))
            else:
                setattr(cls, handler_name, _send(ename))
            DYNAMIC_FORWORD_EVENTS[ename] = (
             handler_name, -1)

        super(ForwardEventMeta, cls).__init__(name, bases, dic)


class ComSelector(six.with_metaclass(ForwardEventMeta, UnitCom)):
    BIND_EVENT = {'E_SET_CONTROL_TARGET': '_set_control_target',
       'G_CONTROL_TARGET': '_get_control_target',
       'E_ROBOT_USE_PHYS': '_on_land',
       'E_SORTIE': '_on_land',
       'E_LAND': '_on_land',
       'E_MODEL_LOADED': '_on_model_loaded',
       'G_IN_AIRSHIP': '_is_in_airship',
       'G_IN_DRONE': '_is_in_drone',
       'G_IN_MECHA': '_is_in_mecha',
       'G_IN_MECHA_ONLY': '_is_in_mecha_only',
       'G_IN_MECHA_TRANS_ONLY': '_is_in_mecha_trans_only',
       'G_CONTROL_HUMAN': '_is_control_human_body'
       }
    DYNAMIC_FORWORD_EVENTS = {}
    FORWARD_EVENT = [
     'G_POSITION',
     'G_ROTATION',
     'G_YAW',
     'E_MOVE_ACC',
     'E_MOVE_FORWARD',
     'E_MOVE_NO_FORCE',
     'E_MOVE_BACK',
     'E_MOVE_BRAKE_START',
     'E_MOVE_BRAKE_END',
     'E_DELTA_YAW',
     'E_DELTA_PITCH',
     'E_VEHICLE_HORN']

    def __init__(self):
        super(ComSelector, self).__init__(False)
        self.cache_bdict = None
        self.ctrl_target = None
        self.sd.ref_ctrl_target = None
        self.default_model = None
        self.control_conf = None
        self.is_forward_event = False
        self._use_phys = 0
        return

    def destroy(self):
        self.cache_bdict = None
        self.ctrl_target = None
        self.sd.ref_ctrl_target = None
        if self.unit_obj and self.unit_obj.get_owner() == global_data.player:
            self.scene.set_player(None)
        super(ComSelector, self).destroy()
        return

    def install_forward_event(self):
        if self.is_forward_event:
            return
        self.is_forward_event = True
        self._bind_event(self.DYNAMIC_FORWORD_EVENTS)

    def uninstall_forward_event(self):
        if self.is_forward_event:
            self._unbind_event(self.DYNAMIC_FORWORD_EVENTS)
        self.is_forward_event = False

    def _lose_control(self, target, bdict):
        mp_com_config = {}
        is_avatar = self.is_control_avatar()
        if is_avatar:
            mp_com_config[tc_utils.KEY_CONTROLLER] = True
        else:
            mp_com_config[tc_utils.KEY_NON_CONTROLLER] = True
        self._re_do_event(target, bdict, 'lose', mp_com_config)
        self.send_event('E_ON_LOSING_SELECTED', self.unit_obj.id)

    def _try_add_com(self, cname, prefix):
        if prefix:
            com = self.unit_obj.add_com(cname, 'client.%s' % prefix)
        else:
            com = self.unit_obj.add_com(cname, 'client')
        return com

    def _re_do_event(self, target, bdict, target_type, mp_com_config):
        mp_res = tc_utils.get_event_config(target_type, mp_com_config)
        lst_complete = []
        enable_event_list = mp_res.get(tc_utils.ACTION_EVENT_ON)
        disable_event_list = mp_res.get(tc_utils.ACTION_EVENT_OFF)
        del_com_list = mp_res.get(tc_utils.ACTION_DEL)
        FORWARD_EVENT = self.FORWARD_EVENT
        for cname in enable_event_list:
            if type(cname) is tuple:
                prefix, cname = cname
            else:
                prefix = None
            com = self.unit_obj.get_com(cname)
            if com is None:
                com = self._try_add_com(cname, prefix)
                com.init_from_dict(self.unit_obj, bdict)
                lst_complete.append(com)
            else:
                com._enable_bind_event(False, FORWARD_EVENT)
                com._enable_bind_event(True, FORWARD_EVENT)

        for cname in disable_event_list:
            if type(cname) is tuple:
                prefix, cname = cname
            else:
                prefix = None
            com = self.unit_obj.get_com(cname)
            if com is None:
                com = self._try_add_com(cname, prefix)
                com.init_from_dict(self.unit_obj, bdict)
                lst_complete.append(com)
            if com:
                com._enable_bind_event(False, FORWARD_EVENT)

        for com in lst_complete:
            com.on_init_complete()

        for cname in del_com_list:
            self.unit_obj.del_com(cname)

        return

    def _on_land(self, *args):
        use_phys = self.ev_g_attr_get('use_phys', 0)
        if use_phys:
            self._set_control_target(None, {'from_on_land': 1,'use_phys': 1})
        return

    def is_robot_parachuting(self, ctrl_conf):
        import logic.gcommon.common_utils.parachute_utils as putil
        parachute_stage = ctrl_conf.get('parachute_stage')
        return putil.is_parachuting(parachute_stage)

    def _get_control_target(self):
        return self.ctrl_target

    def is_control_avatar(self):
        return self.is_unit_obj_type('LAvatar')

    def init_from_dict(self, unit_obj, bdict):
        super(ComSelector, self).init_from_dict(unit_obj, bdict)
        use_phys = bdict.get('mp_attr', {}).get('use_phys', 0)
        self._use_phys = use_phys
        self.cache_bdict = bdict

    def on_init_complete(self):
        if self.cache_bdict:
            ctrl_id = self.cache_bdict.get('ctrl_id', None) if 1 else None
            target = None
            if ctrl_id:
                from mobile.common.EntityManager import EntityManager
                target = EntityManager.getentity(ctrl_id)
                if not target:
                    pass
            if self.is_unit_obj_type('LAvatar') and global_data.player and global_data.player.is_in_global_spectate() and self.unit_obj.id == global_data.player.id:
                self.cache_bdict = None
                return
        is_in_mecha = False
        if 'is_in_mecha' in self.cache_bdict:
            is_in_mecha = self.cache_bdict['is_in_mecha']
        self._set_control_target(target, self.cache_bdict, is_in_mecha)
        self.cache_bdict = None
        g_is_parachute_battle_land = self.ev_g_is_parachute_battle_land()
        if g_is_parachute_battle_land:
            self._on_land()
        return

    def _is_in_airship(self):
        if self.ctrl_target:
            return self.ctrl_target.__class__.__name__ == 'Airship'
        return False

    def _is_in_drone(self):
        if self.ctrl_target:
            return self.ctrl_target.__class__.__name__ == 'Drone'
        return False

    def _is_in_mecha_only(self):
        return self._is_in_mecha('Mecha')

    def _is_in_mecha_trans_only(self):
        return self._is_in_mecha('MechaTrans')

    def _is_in_mecha(self, type_name=None):
        if self.ctrl_target:
            if type_name:
                return self.ctrl_target.__class__.__name__ == type_name
            return bool(self.ctrl_target.logic and self.ctrl_target.logic.MASK & preregistered_tags.MECHA_VEHICLE_TAG_VALUE)
        return False

    def _is_control_human_body(self):
        if self.ctrl_target:
            return bool(self.ctrl_target.logic.MASK & preregistered_tags.HUMAN_TAG_VALUE)
        return True

    def _get_control_target_type(self):
        if self.ctrl_target:
            return self.ctrl_target.__class__.__name__
        else:
            return None

    def _on_model_loaded(self, model):
        if not self.ctrl_target or not self.ctrl_target.logic:
            return
        self.ctrl_target.logic.send_event('E_SELECTOR_MODEL_LOADED', self.unit_obj.id, model)

    def _set_control_target(self, target, ctrl_conf=None, is_in_mecha=False, by_init=False):
        if ctrl_conf is None:
            ctrl_conf = {}
        if target is None or target is self.unit_obj.get_owner():
            self._lose_target(ctrl_conf, is_in_mecha)
            return
        else:
            self._set_control_to_target(target, ctrl_conf, by_init)
            return

    def _lose_target(self, ctrl_conf, is_in_mecha=False):
        if self.unit_obj is None:
            return
        else:
            owner = self.unit_obj.get_owner()
            otarget = self.ctrl_target
            if otarget and otarget.id:
                otarget_id = otarget.id
            else:
                otarget_id = None
            self.uninstall_forward_event()
            if otarget and otarget.logic:
                pos = otarget.logic.ev_g_position()
                otarget.logic.send_event('E_ON_LOSING_SELECTED', self.unit_obj.id)
            else:
                lst_pos = ctrl_conf.get('position')
                pos = math3d.vector(*lst_pos) if lst_pos else None
            self.ctrl_target = owner
            self.sd.ref_ctrl_target = owner
            pos = ctrl_conf.get('reset_pos', None) or pos or math3d.vector(0, 0, 0)
            bdict = ctrl_conf
            bdict['position'] = (pos.x, pos.y, pos.z)
            self.send_event('E_POSITION', pos)
            mp_com_config = {}
            from logic.gutils import judge_utils
            if self.is_control_avatar() and not judge_utils.is_ob() and not self.ev_g_is_outsider():
                mp_com_config[tc_utils.KEY_CONTROLLER] = True
            else:
                mp_com_config[tc_utils.KEY_NON_CONTROLLER] = True
            if self.sd.ref_is_robot or ctrl_conf.get('use_phys', 0):
                if self.sd.ref_is_agent:
                    self._re_do_event(None, bdict, 'robot', mp_com_config)
                else:
                    self._re_do_event(None, bdict, 'human', mp_com_config)
            else:
                self._re_do_event(None, bdict, 'human', mp_com_config)
            self.send_event('E_ON_BEING_SELECTED', owner.id, bdict)
            if owner == global_data.player:
                self.scene.set_player(self.unit_obj)
            self.send_event('E_ON_CONTROL_TARGET_CHANGE', owner.id, math3d.vector(pos), is_in_mecha)
            global_data.emgr.common_control_target_change_event.emit(self.unit_obj.id, owner.id)
            self.send_event('E_ON_CONTROL_TARGET_CHANGE_EX', otarget_id, owner.id, math3d.vector(pos))
            return

    def _set_control_to_target(self, target, ctrl_conf, by_init=False):
        if target is self.ctrl_target:
            return
        else:
            otarget = self.ctrl_target
            if otarget and otarget.id:
                otarget_id = otarget.id
            else:
                otarget_id = None
            self._lose_control(target, ctrl_conf)
            tg = target.logic
            self.install_forward_event()
            tg.send_event('E_ON_BEING_SELECTED', self.unit_obj.id, ctrl_conf)
            self.ctrl_target = target
            self.sd.ref_ctrl_target = target
            self.send_event('E_ON_CONTROL_TARGET_CHANGE', target.id, math3d.vector(0, 0, 0))
            global_data.emgr.common_control_target_change_event.emit(self.unit_obj.id, target.id)
            self.send_event('E_ON_CONTROL_TARGET_CHANGE_EX', otarget_id, target.id, math3d.vector(0, 0, 0))
            pos = target.logic.ev_g_foot_position()
            if not pos or pos.is_zero:
                log_error('ComSelector _set_control_to_target error. target = %s, pos = %s', str(target), pos)
            tg.send_event('E_ON_CONTROL_TARGET_CHANGE', target.id, pos, False, by_init)
            if self.sd.ref_is_robot:
                if G_POS_CHANGE_MGR:
                    self.notify_pos_change(math3d.vector(0, 0, 0), True)
                else:
                    self.send_event('E_POSITION', math3d.vector(0, 0, 0))
            return