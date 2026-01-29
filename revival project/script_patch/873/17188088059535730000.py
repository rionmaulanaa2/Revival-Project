# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComSkillClient.py
from __future__ import absolute_import
import six
from ..UnitCom import UnitCom
from common.cfg import confmgr
from logic.gutils import mecha_utils
import logic.gcommon.const as g_const
from logic.gcommon.common_const.skill_const import FUEL_COST_PER_TIMES_INAIR
from logic.gcommon.common_const import attr_const

class ComSkillClient(UnitCom):
    BIND_EVENT = {'E_ADD_SKILL': '_on_add_skill',
       'E_UPDATE_SKILL': '_on_update_skill',
       'E_MOD_SKILL': '_on_mod_skill',
       'E_REMOVE_SKILL': '_on_remove_skill',
       'E_DO_SKILL': '_do_skill',
       'E_REMOTE_DO_SKILL': '_remote_do_skill',
       'E_END_SKILL': '_end_skill',
       'E_BEGIN_RECOVER_MP': '_begin_recover_mp',
       'E_INTERRUPT_SKILL': '_interrupt_skill',
       'E_HIDE_SKILL': '_on_hide_skill',
       'E_RECOVER_SKILL': '_on_recover_skill',
       'G_SKILL': '_get_skill',
       'E_MOD_ATTR_BY_SKILL_ID': '_mod_attr_by_skill_id',
       'E_SKILL_MP_CHANGE': '_on_mp_change',
       'E_SKILL_ADD_MP': '_add_skill_mp',
       'E_SET_SKILL_TICK_INTERVAL': '_set_skill_tick_interval',
       'E_ON_LEAVE_MECHA': '_on_leave_mecha',
       'G_CAN_CAST_SKILL': '_on_check_cast_skill',
       'G_ENERGY': '_get_energy',
       'G_SKILL_CD_TYPE': '_get_cd_type',
       'G_ENERGY_RECOVER': '_get_energy_recover',
       'G_ENERGY_COST': '_get_energy_cost',
       'G_ENERGY_SEGMENT': '_get_energy_seg',
       'G_SKILL_VALID_CAST_COUNT': '_get_skill_valid_cast_count',
       'G_RECOVER_TIME': '_get_recover_time',
       'E_MOD_SKILL_LEFT_CNT': '_mod_left_cnt',
       'E_SET_SKILL_LEFT_CNT': '_set_left_cnt',
       'E_ON_JOIN_MECHA': '_on_join_mecha',
       'E_DISABLE_BY_MODULE_CARD': '_disable_by_module_card',
       'E_ENABLE_BY_MODULE_CARD': '_enable_by_module_card',
       'E_DISABLE_MOVE_SKILL': '_disable_move_skill',
       'G_IS_MOVE_SKILL_DISABLED': 'is_move_skill_disabled'
       }
    BIND_ATTR_CHANGE = {attr_const.MECHA_ATTR_SKILL_2_RECOVER_FACTOR: 'on_add_attr_changed',
       attr_const.MECHA_ATTR_SKILL_4_RECOVER_FACTOR: 'on_add_attr_changed',
       attr_const.MECHA_ATTR_TMP_SKILL_2_RECOVER_FACTOR: 'on_add_attr_changed',
       attr_const.MECHA_ATTR_TMP_SKILL_4_RECOVER_FACTOR: 'on_add_attr_changed',
       attr_const.ATTR_SKILL_RECOVER_FACTOR: 'on_add_attr_changed',
       attr_const.ATTR_SKILL_CD_ADD: 'on_add_attr_changed'
       }
    ATTR_CD_RATE = 'skill_cd_rate'

    def __init__(self):
        super(ComSkillClient, self).__init__()
        self._skills = {}
        self._skill_request_callback = {}
        self.preload_skill_data = {}
        self.need_update = True
        self._move_skill_disabled = False

    def destroy(self):
        for skill in six.itervalues(self._skills):
            skill.destroy()

        self._skills = {}
        self._skill_request_callback = {}
        self.preload_skill_data = {}
        super(ComSkillClient, self).destroy()

    def on_post_init_complete(self, bdict):
        super(ComSkillClient, self).on_post_init_complete(bdict)
        for skill_id, data in six.iteritems(bdict.get('skills', {})):
            self._on_add_skill(skill_id, data)

        self.send_event('E_SKILL_INIT_COMPLETE')

    def _on_join_mecha(self, *args):
        if self.ev_g_is_avatar():
            self.need_update = True

    def _on_hide_skill(self):
        for skill_obj in six.itervalues(self._skills):
            skill_obj.on_temp_remove()

    def _on_recover_skill(self):
        for skill_obj in six.itervalues(self._skills):
            skill_obj.on_recover()

    def _set_attr_by_key(self, key, value, source_info=None):
        if key in self._mp_attr:
            self._mp_attr[key] = value

    def _mod_attr_by_skill_id(self, skill_id, attr, value):
        if skill_id not in self._skills:
            return
        self._skills[skill_id].mod_attr(attr, value)

    def _on_add_skill(self, skill_id, ext_data=None):
        if ext_data is None:
            ext_data = {}
        if skill_id in self.preload_skill_data:
            ext_data.update(self.preload_skill_data[skill_id])
        if skill_id in self._skills:
            return
        else:
            cur_conf = confmgr.get('skill_conf', str(skill_id))
            if cur_conf is None:
                return
            class_name = cur_conf.get('class')
            class_module = __import__('logic.gcommon.skill.client.%s' % class_name, globals(), locals(), [class_name])
            skill_class = getattr(class_module, class_name, None)
            if skill_class is None:
                return
            skill_obj = skill_class(skill_id, self.unit_obj, cur_conf)
            self._skills[skill_id] = skill_obj
            skill_obj.update_skill(ext_data, False)
            skill_obj.on_add()
            if skill_obj._mp < skill_obj._max_mp:
                self.need_update = True
                skill_obj.need_tick = True
            self.send_event('E_ON_SKILL_ADDED', skill_id)
            return

    def _on_update_skill(self, skill_id, skill_data):
        skill = self._skills.get(skill_id, None)
        if not skill:
            self.preload_skill_data.update({skill_id: skill_data})
            return
        else:
            skill.update_skill(skill_data)
            self.need_update = True
            return

    def _on_mod_skill(self, skill_id, skill_data):
        skill = self._skills.get(skill_id, None)
        if not skill:
            return
        else:
            skill.mod_skill(skill_data)
            return

    def _on_remove_skill(self, skill_id):
        if skill_id not in self._skills:
            return
        skill_obj = self._skills[skill_id]
        skill_obj.on_remove()
        skill_obj.destroy()
        del self._skills[skill_id]

    def _remote_do_skill(self, skill_id, *args):
        if skill_id not in self._skills:
            return
        skill = self._skills[skill_id]
        if not skill:
            return
        skill.remote_do_skill(*args)

    def _do_skill(self, skill_id, *args):
        if skill_id not in self._skills:
            return
        skill = self._skills[skill_id]
        if not skill:
            return
        if not skill.can_do_skill_in_water(*args):
            return
        if self._move_skill_disabled and skill.is_move_skill:
            return
        nocd = getattr(global_data, 'no_cd', False)
        if not nocd and not skill.check_skill():
            return
        self.need_update = True
        skill_args = skill.do_skill(*args) or ()
        self.send_event('E_CALL_SYNC_METHOD', 'do_skill', [skill_id, skill_args], True)
        cost_fuel_in_air = skill.get_cost_fuel_type() == FUEL_COST_PER_TIMES_INAIR and not self.ev_g_on_ground()
        should_cost = skill.get_cost_fuel_type() != FUEL_COST_PER_TIMES_INAIR or cost_fuel_in_air
        cost_fuel = max(0, skill.get_cost_fuel() * (1 - self.ev_g_add_attr('skill_{}_fuel_cost_factor'.format(skill._category)) - self.ev_g_add_attr('skill_fuel_cost_factor', skill_id) + self.ev_g_add_attr(attr_const.MECHA_FUEL_COST_FACTOR)))
        pre_cost_fuel = max(0, skill.get_cost_fuel_pre() * (1 - self.ev_g_add_attr('skill_{}_fuel_cost_factor'.format(skill._category)) - self.ev_g_add_attr('skill_fuel_cost_factor', skill_id) + self.ev_g_add_attr(attr_const.MECHA_FUEL_COST_FACTOR)))
        if should_cost and cost_fuel > 0:
            event = 'E_SPEC_FUEL_DO_SKILL' if skill.has_spec_fuel() else 'E_FUEL_DO_SKILL'
            self.send_event(event, skill_id, cost_fuel, pre_cost_fuel, skill.get_cost_fuel_type())
        if hasattr(g_const, 'SWITCH_LOG_SKILL') and g_const.SWITCH_LOG_SKILL:
            pass

    def _end_skill(self, skill_id, *args):
        skill_obj = self._skills.get(skill_id, None)
        if not skill_obj:
            return
        else:
            skill_args = skill_obj.end_skill(*args) or ()
            self.send_event('E_CALL_SYNC_METHOD', 'end_skill', [skill_id, skill_args], True)
            if skill_obj.get_cost_fuel() > 0:
                event = 'E_SPEC_FUEL_END_SKILL' if skill_obj.has_spec_fuel() else 'E_FUEL_END_SKILL'
                self.send_event(event, skill_id, skill_obj.get_cost_fuel(), skill_obj.get_cost_fuel_type())
            return

    def _begin_recover_mp(self, skill_id, *args):
        skill_obj = self._skills.get(skill_id, None)
        if not skill_obj:
            return
        else:
            skill_args = skill_obj.begin_recover_mp(self, *args) or ()
            self.send_event('E_CALL_SYNC_METHOD', 'begin_recover_mp', [skill_id, skill_args], True)
            self.need_update = True
            return

    def _interrupt_skill(self, skill_id):
        if skill_id not in self._skills:
            return
        self._skills[skill_id].on_interrupt()
        self.send_event('E_CALL_SYNC_METHOD', 'interrupt_skill', [skill_id], True)

    def _get_skill(self, skill_id):
        if skill_id in self._skills:
            return self._skills[skill_id]

    def tick(self, delta):
        all_tick_done = True
        for _, skill_obj in six.iteritems(self._skills):
            if skill_obj.need_tick:
                skill_obj.tick(delta)
                all_tick_done = False

        if all_tick_done:
            self.need_update = False

    def _get_energy_recover(self, skill_id):
        skill_obj = self._skills.get(skill_id)
        if not skill_obj:
            return 0
        return skill_obj._inc_mp * 1.0 / skill_obj._max_mp

    def _get_energy(self, skill_id):
        skill_obj = self._skills.get(skill_id)
        if not skill_obj:
            return 0
        return skill_obj._mp * 1.0 / skill_obj._max_mp

    def _get_cd_type(self, skill_id):
        skill_obj = self._skills.get(skill_id)
        if not skill_obj:
            return None
        else:
            return skill_obj._cd_type

    def _get_energy_cost(self, skill_id):
        skill_obj = self._skills.get(skill_id)
        if not skill_obj:
            return 0
        return skill_obj._cost_mp * 1.0 / skill_obj._max_mp

    def _get_energy_seg(self, skill_id):
        skill_obj = self._skills.get(skill_id)
        if not skill_obj:
            return 0
        return int(skill_obj._max_mp / skill_obj._cost_mp)

    def _get_skill_valid_cast_count(self, skill_id):
        skill_obj = self._skills.get(skill_id)
        if not skill_obj:
            return 0
        return int(1.0 * skill_obj._mp / skill_obj._cost_mp)

    def _on_check_cast_skill(self, skill_id, show_failed_appearance=True):
        if not mecha_utils.enable_mecha_cd:
            return True
        else:
            if getattr(global_data, 'no_cd', False):
                return True
            skill_obj = self._skills.get(skill_id)
            if not skill_obj:
                return False
            can_cast_skill = skill_obj.on_check_cast_skill()
            if not can_cast_skill and show_failed_appearance:
                cur_conf = confmgr.get('skill_conf', str(skill_id))
                cd_effect = cur_conf.get('trigger_cd_effect', None)
                if cd_effect:
                    self.ev_g_show_cd_effect(cd_effect)
                ignore_tip_cd = cur_conf.get('ignore_tip_cd', None)
                if not ignore_tip_cd:
                    self.send_event('E_SOUND_TIP_CD')
            return can_cast_skill

    def _set_skill_tick_interval(self, skill_id, interval):
        skill_obj = self._skills.get(skill_id)
        if not skill_obj:
            return
        skill_obj.set_tick_interval(interval)

    def _on_leave_mecha(self):
        pass

    def _on_mp_change(self, skill_id, mp):
        skill_obj = self._skills.get(skill_id)
        if not skill_obj:
            return
        skill_obj.set_mp(mp)
        self.send_event('E_ENERGY_CHANGE', skill_id, skill_obj._mp * 1.0 / skill_obj._max_mp)

    def _add_skill_mp(self, skill_id, add_mp):
        skill_obj = self._skills.get(skill_id)
        if not skill_obj:
            return
        skill_obj.mod_mp(add_mp)
        self.send_event('E_ENERGY_CHANGE', skill_id, skill_obj._mp * 1.0 / skill_obj._max_mp)

    def _get_recover_time(self, skill_id):
        skill_obj = self._skills.get(skill_id)
        if not skill_obj:
            return 0
        return (skill_obj._max_mp - skill_obj._mp) / skill_obj._inc_mp

    def _mod_left_cnt(self, skill_id, delta_cnt):
        skill_obj = self._skills.get(skill_id)
        if skill_obj:
            skill_obj.mod_left_cnt(delta_cnt)

    def _set_left_cnt(self, skill_id, cnt):
        skill_obj = self._skills.get(skill_id)
        if skill_obj:
            skill_obj.set_left_cnt(cnt)

    def _disable_by_module_card(self, skill_id, removed_card_id):
        self._switch_skill_status_by_module_card(skill_id, removed_card_id, True)

    def _enable_by_module_card(self, skill_id, add_card_id, client_dict):
        skill_obj = self._get_skill(skill_id)
        if not skill_obj:
            return
        if self._switch_skill_status_by_module_card(skill_id, add_card_id, False):
            skill_obj.update_skill(client_dict)

    def _switch_skill_status_by_module_card(self, skill_id, card_id, disable):
        if not skill_id or card_id <= 0:
            return False
        skill_obj = self._get_skill(skill_id)
        if skill_obj and card_id == skill_obj.get_module_card_id():
            skill_obj.disable_by_module_card(disable)
            return True
        return False

    def on_add_attr_changed(self, attr, item_id, pre_value, cur_value, source_info):
        for skill_id, skill_obj in six.iteritems(self._skills):
            if item_id is not None and skill_id != item_id:
                continue
            skill_obj.on_add_attr_changed(attr, pre_value, cur_value)

        return

    def _disable_move_skill(self, disable):
        self._move_skill_disabled = disable

    def is_move_skill_disabled(self):
        return self._move_skill_disabled