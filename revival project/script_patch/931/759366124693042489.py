# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_camera/ComStateTrkCam.py
from __future__ import absolute_import
import six_ex
import six
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.cdata import mecha_status_config
import math3d
import math
from common.framework import Functor
from common.cfg import confmgr
from logic.gcommon.const import HIT_PART_HEAD

class ComStateTrkCam(UnitCom):
    BIND_EVENT = {'E_JET_CAMERA_SHAKE': ('_on_jump', 10),
       'E_HITED_SHOW_HURT_FIREARMS_SCREEN_TRK': '_on_hit_by_firearm',
       'E_HITED_SHOW_HURT_THROW_SCREEN_TRK': '_on_hit_by_throwable',
       'E_HITED_SHOW_HURT_OTHER_SCREEN_TRK': '_on_hit_by_other',
       'E_MECHA_ON_GROUND': '_on_mecha_ground',
       'E_DO_SKILL': ('_do_skill', 10),
       'E_END_SKILL': ('_end_do_skill', 10),
       'E_MODEL_LOADED': ('_on_model_loaded', 30),
       'E_PLAY_CAMERA_TRK': 'play_trk_with_check',
       'E_CANCEL_CAMERA_TRK': 'cancel_trk_with_check',
       'E_PLAY_CAMERA_STATE_TRK': 'on_trigger_cam_trk_animation',
       'E_CANCEL_CAMERA_STATE_TRK': 'on_cancel_cam_trk_animation',
       'SECOND_WEAPON_ATTACK_SUCCESS': 'on_second_weapon_fire',
       'E_LEAVE_STATE': ('_on_leave_states', 20),
       'E_DEATH': 'on_death',
       'E_HIT_TARGET': 'on_hit_target',
       'E_ENTER_STATE': '_enter_states',
       'E_PLAY_TRK_BY_STATE': 'play_trk_by_state'
       }

    def __init__(self):
        super(ComStateTrkCam, self).__init__()
        self.mecha_common_conf = {}
        self.mecha_spe_trk_conf = {}
        self.is_binded_event = False
        self.init_conf()

    def init_conf(self):
        from logic.gcommon.const import NEOX_UNIT_SCALE
        self.GROUND_SPEED_SMALL = 30 * NEOX_UNIT_SCALE
        self.GROUND_SPEED_BIG = 50 * NEOX_UNIT_SCALE
        if not self.mecha_spe_trk_conf:
            self.prepare_table()

    def on_post_init_complete(self, bdict):
        if self.ev_g_model():
            self._on_model_loaded()

    def _on_model_loaded(self, *args):
        self.process_mecha_ani_trk_event(True)
        self.init_mecha_event_trigger_config()

    def destroy(self):
        if self.is_active:
            self.process_mecha_ani_trk_event(False)
        super(ComStateTrkCam, self).destroy()

    def prepare_table(self):
        special_conf_name = [
         'MechaWalkConfig', 'MechaHitConfig']
        from common.cfg import confmgr
        self.prepare_mecha_state_trk()
        trk_conf = confmgr.get('camera_trk_sfx_conf')
        self.mecha_common_conf = trk_conf.get('MechaCommonConfig', {})
        self.mecha_spe_trk_conf = {}
        for conf_name in special_conf_name:
            spe_conf = trk_conf.get(conf_name, {}).get('Content', {})
            for mecha_id, info in six.iteritems(spe_conf):
                if mecha_id in self.mecha_spe_trk_conf:
                    self.mecha_spe_trk_conf[mecha_id].update(info)
                else:
                    self.mecha_spe_trk_conf[mecha_id] = info

    def _on_jump(self, *args):
        self.on_trigger_cam_trk_animation('C_JUMP')

    def _on_hit_by_firearm(self, from_pos, hit_parts, weapon_id, triger_is_mecha):
        if not self.check_is_camera_target():
            return
        scr_effect_lv = self.get_gun_scr_lv(weapon_id, hit_parts, triger_is_mecha)
        if scr_effect_lv != '0':
            show_dir = self.get_show_dir(from_pos)
            trk_state = show_dir + '_' + str(scr_effect_lv)
            self.on_trigger_cam_trk_animation(trk_state)

    def get_gun_scr_lv(self, weapon_id, hit_parts, triger_is_mecha):
        from logic.gutils.hitted_trk_utils import get_gun_scr_lv
        return get_gun_scr_lv(weapon_id, hit_parts, self.is_mecha(), triger_is_mecha, False)

    def get_show_dir(self, from_pos):
        from logic.gutils.hitted_trk_utils import get_show_dir
        return get_show_dir(self.ev_g_position(), from_pos)

    def _on_hit_by_throwable(self, from_pos, weapon_id, triger_is_mecha):
        if not self.check_is_camera_target():
            return
        effect_lv = self.get_throwable_scr_lv(weapon_id, triger_is_mecha)
        if effect_lv != '0':
            show_dir = self.get_show_dir(from_pos)
            trk_state = show_dir + '_' + effect_lv
            self.on_trigger_cam_trk_animation(trk_state)

    def get_throwable_scr_lv(self, weapon_id, triger_is_mecha):
        from logic.gutils.hitted_trk_utils import get_throwable_scr_lv
        return get_throwable_scr_lv(weapon_id, self.is_mecha(), triger_is_mecha, False)

    def _on_hit_by_other(self, from_pos, damage):
        effect_lv = self._get_other_damage_scr_lv(damage)
        if effect_lv:
            show_dir = self.get_show_dir(from_pos)
            trk_state = show_dir + '_' + effect_lv
            self.on_trigger_cam_trk_animation(trk_state)

    def _get_other_damage_scr_lv(self, damage):
        from logic.gutils.hitted_trk_utils import _get_other_damage_scr_lv
        return _get_other_damage_scr_lv(self, damage, self.is_mecha())

    def _on_mecha_ground(self, ground_speed):
        ground_speed = abs(ground_speed)
        if ground_speed <= self.GROUND_SPEED_SMALL:
            camera_trk_state = 'C_SML_GROUND'
        elif ground_speed <= self.GROUND_SPEED_BIG:
            camera_trk_state = 'C_MED_GROUND'
        else:
            camera_trk_state = 'C_BIG_GROUND'
        self.on_trigger_cam_trk_animation(camera_trk_state)

    def check_is_camera_target(self):
        if self.ev_g_is_cam_target():
            return True
        return False

    def _get_mecha_trk_tag_from_camera_state(self, camera_state, mecha_id):
        cam_trk_tag = None
        str_cam_state = str(camera_state)
        if not mecha_id:
            if self.is_unit_obj_type('LAvatar'):
                _bind_mecha_id = self.ev_g_get_bind_mecha()
                from mobile.common.EntityManager import EntityManager
                ent = EntityManager.getentity(_bind_mecha_id)
                if ent and ent.logic:
                    mecha_id = ent.logic.sd.ref_mecha_id
            else:
                mecha_id = self.sd.ref_mecha_id
        if mecha_id:
            cam_trk_tag = self.mecha_spe_trk_conf.get(str(mecha_id), {}).get(str_cam_state, None)
            if not cam_trk_tag:
                cam_trk_tag = self.mecha_common_conf.get('Content').get(str_cam_state, {}).get('trk_tag')
        return cam_trk_tag

    def _get_human_trk_tag_from_camera_state(self, camera_state):
        trk_conf = confmgr.get('camera_trk_sfx_conf', 'HumanConfig').get('Content', {})
        trk_tag = trk_conf.get(str(camera_state), {}).get('trk_tag', '')
        return trk_tag

    def on_trigger_cam_trk_animation(self, camera_state, end_callback=None, mecha_id=None, custom_data=None):
        if not self.check_is_camera_target():
            return
        if self.is_mecha() or mecha_id:
            cam_trk_tag = self._get_mecha_trk_tag_from_camera_state(camera_state, mecha_id)
        else:
            cam_trk_tag = self._get_human_trk_tag_from_camera_state(camera_state)
        if cam_trk_tag:
            self.play_trk(cam_trk_tag, end_callback, custom_data)

    def on_cancel_cam_trk_animation(self, camera_state, mecha_id, run_callback, cancel_failed_cb=None):
        if not self.check_is_camera_target():
            return
        if self.is_mecha() or mecha_id:
            cam_trk_tag = self._get_mecha_trk_tag_from_camera_state(camera_state, mecha_id)
        else:
            cam_trk_tag = self._get_human_trk_tag_from_camera_state(camera_state)
        if cam_trk_tag:
            self.cancel_trk(cam_trk_tag, run_callback, cancel_failed_cb)

    def _do_skill(self, skill_id, *args):
        if not self.check_is_camera_target():
            return
        from common.cfg import confmgr
        trk_conf = confmgr.get('camera_trk_sfx_conf')
        skill_trk_conf = trk_conf.get('SkillTrkConfig', {}).get('Content', {})
        skill_trk_tag = skill_trk_conf.get(str(skill_id), {}).get('trk_tag', '')
        if not skill_trk_tag:
            return
        self.play_trk(skill_trk_tag)

    def _end_do_skill(self, skill_id, *skill_args):
        if not self.check_is_camera_target():
            return
        from common.cfg import confmgr
        trk_conf = confmgr.get('camera_trk_sfx_conf')
        skill_trk_conf = trk_conf.get('SkillTrkConfig', {}).get('Content', {})
        this_skill_trk_conf = skill_trk_conf.get(str(skill_id), {})
        skill_trk_tag = this_skill_trk_conf.get('trk_tag', '')
        is_cancel_on_end_skill = this_skill_trk_conf.get('is_cancel_on_end_skill', 0)
        if skill_trk_tag and is_cancel_on_end_skill:
            self.cancel_trk(skill_trk_tag)

    def _do_animate_trigger(self, trk_tag):
        if not self.check_is_camera_target():
            return
        if trk_tag:
            self.play_trk(trk_tag)

    def _do_cancel_animate_trigger(self, trk_tag):
        if not self.check_is_camera_target():
            return
        global_data.emgr.camera_cancel_added_trk_event.emit(trk_tag)

    def _do_event_trigger(self, event, trk_tag, *args):
        if not self.check_is_camera_target():
            return
        if trk_tag:
            self.play_trk(trk_tag)

    def _do_break_event_trigger(self, break_event, trk_tag, *args):
        if not self.check_is_camera_target():
            return
        global_data.emgr.camera_cancel_added_trk_event.emit(trk_tag)

    def process_mecha_ani_trk_event(self, is_register):
        mecha_id = self.sd.ref_mecha_id
        if not mecha_id:
            return
        trk_conf = confmgr.get('camera_trk_sfx_conf')
        anim_trk_confs = trk_conf.get('AnimateTrkConfig', {}).get('Content', {})
        ani_trk_list = six_ex.values(anim_trk_confs)
        for row_conf in ani_trk_list:
            support_list = row_conf.get('support_mecha_id', [])
            if support_list and mecha_id not in support_list:
                continue
            anim_list = row_conf.get('anim_list', [])
            trigger = row_conf.get('trigger', '')
            trk_tag = row_conf.get('trk_tag', '')
            if not (anim_list and trigger and trk_tag):
                continue
            model = self.ev_g_model()
            for anim_name in anim_list:
                if model and not model.has_anim_event(anim_name, trigger):
                    log_error('model has not ani name %s or anim has no trigger %s' % (anim_name, trigger))
                    continue
                if is_register:
                    self.send_event('E_REGISTER_ANIMATOR_EVENT', anim_name, trigger, self._do_animate_trigger, trk_tag)
                else:
                    self.send_event('E_UNREGISTER_ANIMATOR_EVENT', anim_name, trigger, self._do_animate_trigger)

    def init_mecha_event_trigger_config(self):
        mecha_id = self.sd.ref_mecha_id
        if not mecha_id:
            return
        trk_conf = confmgr.get('camera_trk_sfx_conf')
        anim_event_confs = trk_conf.get('EventConfig', {}).get('Content', {})
        ani_trk_list = six_ex.values(anim_event_confs)
        for row_conf in ani_trk_list:
            support_list = row_conf.get('support_mecha_id', [])
            if support_list and mecha_id not in support_list:
                continue
            trigger_event = row_conf.get('trigger_event', '')
            break_event = row_conf.get('break_event', '')
            trk_tag = row_conf.get('trk_tag', '')
            if trigger_event:
                self.regist_event(trigger_event, Functor(self._do_event_trigger, trigger_event, trk_tag))
            if break_event:
                self.regist_event(break_event, Functor(self._do_break_event_trigger, break_event, trk_tag))

    def play_trk(self, trk_tag, end_callback=None, custom_data=None):
        from common.cfg import confmgr
        row_conf = confmgr.get('camera_trk_sfx_conf', 'TrkConfig').get('Content').get(str(trk_tag), None)
        if not row_conf:
            log_error("Can't find cam trk %s" % trk_tag)
            return
        else:
            is_plot = row_conf.get('is_plot', False)
            if is_plot:
                global_data.emgr.camera_play_plot_trk_event.emit(trk_tag, end_callback, custom_data)
            else:
                global_data.emgr.camera_play_added_trk_event.emit(trk_tag, end_callback, custom_data)
            return

    def cancel_trk(self, trk_tag, run_callback=False, cancel_failed_cb=None):
        from common.cfg import confmgr
        row_conf = confmgr.get('camera_trk_sfx_conf', 'TrkConfig').get('Content').get(str(trk_tag), None)
        if not row_conf:
            log_error("Can't find cam trk %s" % trk_tag)
            return
        else:
            is_plot = row_conf.get('is_plot', False)
            if is_plot:
                global_data.emgr.camera_cancel_plot_trk_event.emit(trk_tag)
            else:
                global_data.emgr.camera_cancel_added_trk_event.emit(trk_tag, run_callback, cancel_failed_cb)
            return

    def on_second_weapon_fire(self):
        self.on_trigger_cam_trk_animation('C_SEC_WEAPON_FIRE')

    def _on_leave_states(self, leave_state, new_state=None):
        if not self.check_is_camera_target():
            return
        else:
            if leave_state == mecha_status_config.MC_MECHA_BOARDING and new_state != mecha_status_config.MC_MECHA_BOARDING:
                global_data.emgr.camera_cancel_added_trk_event.emit('Mount_State_Offset', None)
                global_data.emgr.camera_cancel_added_trk_event.emit('Mount_Step_back', None)
                global_data.emgr.camera_cancel_added_trk_event.emit('Mount_Step_back2', None)

                def cancel_failed_cb(tag, run_callback):
                    global_data.emgr.camera_additional_transformation_event.emit(math3d.matrix(), 0, False, True)

                self.on_cancel_cam_trk_animation('C_MECHA_BOARD', None, True, cancel_failed_cb)
            mecha_id = self.sd.ref_mecha_id
            if not mecha_id:
                return
            if leave_state in self.mecha_state_trk_conf:
                state_conf = self.mecha_state_trk_conf[leave_state]
                trk_tag = state_conf.get('trk_tag', '')
                support_mecha_id = state_conf.get('support_mecha_id', [])
                if mecha_id in support_mecha_id:
                    self.cancel_trk(trk_tag)
            return

    def prepare_mecha_state_trk(self):
        from logic.gcommon.cdata import mecha_status_config
        state_confs = confmgr.get('camera_trk_sfx_conf', 'MechaStateConf').get('Content', {})
        self.mecha_state_trk_conf = {}
        for state_str, state_conf in six.iteritems(state_confs):
            self.mecha_state_trk_conf[mecha_status_config.desc_2_num.get(state_str, '')] = state_conf

    def _enter_states(self, new_state):
        self.play_trk_by_state(new_state)

    def play_trk_by_state(self, new_state):
        if not self.check_is_camera_target():
            return
        mecha_id = self.sd.ref_mecha_id
        if mecha_id and self.is_unit_obj_type('LMecha'):
            if new_state in self.mecha_state_trk_conf:
                state_conf = self.mecha_state_trk_conf[new_state]
                trk_tag = state_conf.get('trk_tag', '')
                support_mecha_id = state_conf.get('support_mecha_id', [])
                if mecha_id in support_mecha_id:
                    self.play_trk(trk_tag)

    def on_death(self, *args):
        if not self.check_is_camera_target():
            return
        else:
            self.on_cancel_cam_trk_animation('C_MECHA_BOARD', None, False)
            return

    def play_trk_with_check(self, cam_trk_tag, end_callback=None, custom_data=None):
        if not self.check_is_camera_target():
            return
        if cam_trk_tag.endswith('.trk'):
            global_data.emgr.camera_play_added_trk_event.emit(cam_trk_tag, end_callback, custom_data)
        else:
            self.play_trk(cam_trk_tag, end_callback, custom_data)

    def cancel_trk_with_check(self, cam_trk_tag, run_callback=False, cancel_failed_cb=None):
        if not self.check_is_camera_target():
            return
        self.cancel_trk(cam_trk_tag, run_callback, cancel_failed_cb)

    def is_mecha(self):
        return self.is_unit_obj_type('LMecha')

    def on_hit_target(self, dmg_parts):
        if not self.check_is_camera_target():
            return
        cam_trk_tag = 'COMMON_HIT_HEAD' if HIT_PART_HEAD in dmg_parts else 'COMMON_HIT'
        self.play_trk(cam_trk_tag)