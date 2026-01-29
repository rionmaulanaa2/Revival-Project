# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComSkillWallAppearance.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
from logic.gutils.mecha_skin_utils import get_accurate_mecha_skin_info_from_owner_keys, get_mecha_skin_res_readonly_info
from common.utils.sfxmgr import CREATE_SRC_OTHER_SYNC
from mobile.common.EntityManager import EntityManager
from common.framework import Functor
from common.cfg import confmgr
import math3d
APPEAR_LOOP_EFFECT_ID = '103'
HIT_EFFECT_ID = '104'
BROKEN_EFFECT_ID = '105'
HIT_COL_EFFECT_ID = '106'
CRACK_EFFECT_ID_INFO = ((0.75, '107'), (0.5, '108'), (0.25, '109'))
ATTACH_EFFECT_ID = '114'
APPEAR_LOOP_SOUND = 'm_8037_panyan_core_build_3p'
BROKEN_SOUND = 'm_8037_panyan_core_break_3p'
EXPLODE_SOUND = 'm_8037_panyan_core_exp_3p'
HIT_SOUND = 'm_8037_panyan_core_hit_3p'
ATTACH_SOUND = 'm_8037_panyan_core_attack_3p'

class ComSkillWallAppearance(UnitCom):
    BIND_EVENT = {'E_BUILDING_CHANGE_HP': 'on_hp_change',
       'G_IS_CAMPMATE': 'on_get_is_campmate',
       'G_IS_SHIELD': 'on_get_is_shield',
       'G_POSITION': 'get_position',
       'E_ATTACH_BY_GRENADE': 'on_attach_by_grenade',
       'E_HIT_BLOOD_SFX': 'on_be_hit',
       'E_BUILDING_EXPLODE': 'on_explode'
       }

    def init_from_dict(self, unit_obj, bdict):
        super(ComSkillWallAppearance, self).init_from_dict(unit_obj, bdict)
        self.sd.ref_pos = math3d.vector(*bdict.get('position', [0, 0, 0]))
        self.sd.ref_rotation_matrix = math3d.rotation_to_matrix(math3d.rotation(*bdict.get('rot', [0, 0, 0, 1])))
        self.birth_time = bdict.get('birthtime', None)
        self.faction_id = bdict.get('faction_id', None)
        self.owner_id = bdict['owner_id']
        self.owner_camp_id = None
        self.owner_unit = None
        self.max_hp = bdict.get('max_hp', 100)
        self.ori_hp = bdict.get('hp', self.max_hp)
        self.owner_mecha_fashion_id, self.owner_mecha_shiny_weapon_id = get_accurate_mecha_skin_info_from_owner_keys(8037, bdict)
        building_no = bdict.get('building_no', None)
        conf = confmgr.get('c_building_res', str(building_no))
        self.life_time = conf['LifeTime']
        self.effect_datas = {}
        self.cur_effects = {}
        self.cur_crack_effect_id = None
        self.permanent_effect_removed = False
        self.ignore_broken_sound = False
        return

    def on_init_complete(self):
        super(ComSkillWallAppearance, self).on_init_complete()
        owner_entity = EntityManager.getentity(self.owner_id)
        effect_datas = {}
        if owner_entity and owner_entity.logic:
            effect_datas = owner_entity.logic.ev_g_mecha_readonly_effect_info()
            self.owner_camp_id = owner_entity.logic.ev_g_camp_id()
            self.owner_unit = owner_entity.logic
        if not effect_datas:
            effect_datas = get_mecha_skin_res_readonly_info(8037, self.owner_mecha_fashion_id, self.owner_mecha_shiny_weapon_id)
        for effect_id, effect_info_list in effect_datas.items():
            self.effect_datas[effect_id] = []
            for effect_info in effect_info_list:
                self.effect_datas[effect_id].append(effect_info['final_correspond_path'])

        self.create_effect(APPEAR_LOOP_EFFECT_ID, campmate_appearance=True)
        global_data.sound_mgr.play_sound(APPEAR_LOOP_SOUND, self.sd.ref_pos)
        self.on_hp_change(self.ori_hp)
        self.send_event('E_MODEL_LOADED', self.effect_datas[HIT_COL_EFFECT_ID][0])

    def _remove_permanent_effect(self, show_broken_effect=True):
        if self.permanent_effect_removed:
            return
        self.permanent_effect_removed = True
        if self.cur_crack_effect_id:
            self.remove_effect(self.cur_crack_effect_id)
        self.remove_effect(APPEAR_LOOP_EFFECT_ID)
        if show_broken_effect:
            for sfx_path in self.effect_datas[BROKEN_EFFECT_ID]:
                self._create_sfx_in_scene(sfx_path, campmate_appearance=True)

        if not self.ignore_broken_sound:
            global_data.sound_mgr.play_sound(BROKEN_SOUND, self.sd.ref_pos)

    def cache(self):
        self._remove_permanent_effect()
        self.owner_unit = None
        super(ComSkillWallAppearance, self).cache()
        return

    def destroy(self):
        self._remove_permanent_effect()
        self.owner_unit = None
        super(ComSkillWallAppearance, self).destroy()
        return

    @staticmethod
    def on_create_effect_callback(sfx, rotation_matrix):
        sfx.rotation_matrix = rotation_matrix

    def remove_effect(self, effect_id):
        if effect_id in self.cur_effects:
            for sfx_id in self.cur_effects[effect_id]:
                global_data.sfx_mgr.remove_sfx_by_id(sfx_id)

            del self.cur_effects[effect_id]

    def _create_sfx_in_scene(self, sfx_path, pos=None, int_check_type=None, campmate_appearance=False):
        sfx_pos = pos if pos else self.sd.ref_pos
        ex_data = {}
        if global_data.cam_lplayer:
            if global_data.cam_lplayer.ev_g_camp_id() != self.owner_camp_id:
                ex_data['need_diff_process'] = True
            elif campmate_appearance:
                if not self.owner_unit or not self.owner_unit.ev_g_is_avatar():
                    sfx_path = sfx_path[:sfx_path.rfind('.')] + '_blue.sfx'
        elif campmate_appearance:
            if not self.owner_unit or not self.owner_unit.ev_g_is_avatar():
                sfx_path = sfx_path[:sfx_path.rfind('.')] + '_blue.sfx'
        return global_data.sfx_mgr.create_sfx_in_scene(sfx_path, sfx_pos, on_create_func=Functor(self.on_create_effect_callback, rotation_matrix=self.sd.ref_rotation_matrix), ex_data=ex_data, int_check_type=int_check_type)

    def create_effect(self, effect_id, campmate_appearance=False):
        if effect_id not in self.cur_effects:
            self.cur_effects[effect_id] = []
            for sfx_path in self.effect_datas[effect_id]:
                self.cur_effects[effect_id].append(self._create_sfx_in_scene(sfx_path, campmate_appearance=campmate_appearance))

    def on_hp_change(self, hp):
        if self.permanent_effect_removed:
            return
        else:
            percent = hp / self.max_hp
            cur_effect_id = None
            for hp_percent_threshold, effect_id in CRACK_EFFECT_ID_INFO:
                if percent < hp_percent_threshold:
                    cur_effect_id = effect_id
                    break

            if cur_effect_id != self.cur_crack_effect_id:
                if self.cur_crack_effect_id:
                    self.remove_effect(self.cur_crack_effect_id)
                self.create_effect(cur_effect_id)
                self.cur_crack_effect_id = cur_effect_id
            return

    def on_get_is_campmate(self, other_faction_id):
        return self.faction_id == other_faction_id

    def on_get_is_shield(self):
        return True

    def get_position(self):
        return self.sd.ref_pos

    def on_attach_by_grenade(self, grenade_owner_id):
        if self.owner_id == grenade_owner_id:
            for sfx_path in self.effect_datas[ATTACH_EFFECT_ID]:
                self._create_sfx_in_scene(sfx_path, campmate_appearance=True)

            global_data.sound_mgr.play_sound(ATTACH_SOUND, self.sd.ref_pos)

    def on_be_hit(self, start_pos, target_pos, bullet_type, **kwargs):
        if kwargs.get('trigger_is_self', False) and global_data.player and global_data.player.logic and global_data.player.logic.ev_g_camp_id() == self.owner_camp_id:
            return
        for sfx_path in self.effect_datas[HIT_EFFECT_ID]:
            self._create_sfx_in_scene(sfx_path, pos=target_pos, int_check_type=CREATE_SRC_OTHER_SYNC, campmate_appearance=True)

        global_data.sound_mgr.play_sound(HIT_SOUND, self.sd.ref_pos)

    def on_explode(self, is_explode):
        if is_explode:
            self._remove_permanent_effect()
            self.on_attach_by_grenade(self.owner_id)
            self.ignore_broken_sound = True
            global_data.sound_mgr.play_sound(EXPLODE_SOUND, self.sd.ref_pos)