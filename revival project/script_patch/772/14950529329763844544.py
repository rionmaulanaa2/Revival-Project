# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_building/ComLightShield.py
from __future__ import absolute_import
import six
from logic.gcommon.component.UnitCom import UnitCom
import logic.gcommon.common_const.ai_const as ai_const
from logic.gutils.mecha_skin_utils import get_accurate_mecha_skin_info_from_owner_keys, get_mecha_skin_res_readonly_info
from common.utils.sfxmgr import CREATE_SRC_SIMPLE
from mobile.common.EntityManager import EntityManager
from logic.gutils.dress_utils import DEFAULT_CLOTHING_ID
from logic.gutils.effect_utils import check_need_ignore_effect_behind_camera
from common.cfg import confmgr
import math3d
START = 0
END = 1
DESTROY = 2
DAMAGED_LITTLE = 3
DAMAGED_MIDDLE = 4
DAMAGED_LARGE = 5
EFFECT_ID_MAP = {START: '115',
   END: '116',
   DESTROY: '117',
   DAMAGED_LITTLE: '118',
   DAMAGED_MIDDLE: '119',
   DAMAGED_LARGE: '120'
   }

class ComLightShield(UnitCom):
    BIND_EVENT = {'E_COLLSION_LOADED': 'on_col_loaded',
       'E_BUILDING_CHANGE_HP': 'on_change_hp',
       'E_HIT_BLOOD_SFX': 'on_be_hited_by_ray',
       'E_HIT_SHIELD_SFX': 'on_be_hited_by_bomb',
       'G_IS_SHIELD': 'on_get_shield',
       'G_AI_CAN_ATK_TYPE': '_get_ai_can_atk_type'
       }

    def __init__(self):
        super(ComLightShield, self).__init__()
        self.state_effects = {}
        self.destroyed = False
        self.last_hp = 0
        self.max_hp = 100

    def init_from_dict(self, unit_obj, bdict):
        super(ComLightShield, self).init_from_dict(unit_obj, bdict)
        self.pos = bdict.get('position', [0, 0, 0])
        self.rot = bdict.get('rot', [0, 0, 0, 1])
        self.max_hp = bdict.get('max_hp', 100)
        self.owner_id = bdict['owner_id']
        self.owner_mecha_fashion_id, self.owner_mecha_shiny_weapon_id = get_accurate_mecha_skin_info_from_owner_keys(8008, bdict)
        self.effect_map = {}
        self.state_effects = {}
        self.last_damaged_state = None
        rot = self.rot
        self.rot_mat = math3d.rotation_to_matrix(math3d.rotation(rot[0], rot[1], rot[2], rot[3]))
        self.pos = math3d.vector(*self.pos)
        self.item_id = bdict.get('building_no')
        self.conf = confmgr.get('c_building_res', str(self.item_id))
        params = self.conf.get('ExtInfo', {})
        self.extra_scale = params.get('extra_scale', 1.0)
        self.breakthrough_size_up_factor = bdict.get('size_up_factor', 0)
        return

    def on_init_complete(self):
        parent = EntityManager.getentity(self.owner_id)
        effect_infos = {}
        if parent and parent.logic:
            mecha = parent.logic.ev_g_bind_mecha_entity()
            if mecha and mecha.logic:
                effect_infos = mecha.logic.ev_g_mecha_readonly_effect_info()
        if not effect_infos:
            effect_infos = get_mecha_skin_res_readonly_info(8008, self.owner_mecha_fashion_id, self.owner_mecha_shiny_weapon_id)
        for key, effect_id in six.iteritems(EFFECT_ID_MAP):
            self.effect_map[key] = effect_infos[effect_id][0]['final_correspond_path']

    def cache(self):
        self._clear_light_shield()
        super(ComLightShield, self).cache()

    def on_col_loaded(self, m, col):
        m.visible = False
        self.last_hp = self.ev_g_hp() * 1.0 / self.max_hp
        self.show_state_effect(START)

    def on_change_hp(self, hp):
        cur_hp = hp * 1.0 / self.max_hp
        if cur_hp < 0.6 <= self.last_hp:
            self.del_state_effect(self.last_damaged_state)
            self.show_state_effect(DAMAGED_LITTLE)
            self.last_damaged_state = DAMAGED_LITTLE
        elif cur_hp < 0.4 <= self.last_hp:
            self.del_state_effect(self.last_damaged_state)
            self.show_state_effect(DAMAGED_MIDDLE)
            self.last_damaged_state = DAMAGED_MIDDLE
        elif cur_hp < 0.2 <= self.last_hp:
            self.del_state_effect(self.last_damaged_state)
            self.show_state_effect(DAMAGED_LARGE)
            self.last_damaged_state = DAMAGED_LARGE
        self.last_hp = cur_hp
        if hp <= 0:
            self.show_state_effect(DESTROY, 2.0)
            global_data.sound_mgr.play_event('m_8008_shield_break_3p', self.pos)
            self.destroyed = True

    def _clear_light_shield(self):
        if self.ev_g_remain_time() <= 1 and not self.destroyed:
            self.show_state_effect(END, 2.0)
            global_data.sound_mgr.play_event('m_8008_shield_off_3p', self.pos)
        self.del_state_effect(self.last_damaged_state)
        self.del_state_effect(START)
        self.state_effects.clear()

    def destroy(self):
        self._clear_light_shield()
        super(ComLightShield, self).destroy()

    def show_state_effect(self, state, duration=-1):

        def create_cb(sfx):
            sfx.rotation_matrix = self.rot_mat
            sfx.scale = sfx.scale * (self.extra_scale + self.breakthrough_size_up_factor)

        sfx_path = self.effect_map[state]
        self.state_effects[state] = global_data.sfx_mgr.create_sfx_in_scene(sfx_path, self.pos, duration=duration, on_create_func=create_cb)

    def del_state_effect(self, state):
        if state in self.state_effects:
            global_data.sfx_mgr.remove_sfx_by_id(self.state_effects[state])

    def on_get_shield(self):
        return True

    def _get_ai_can_atk_type(self):
        return ai_const.AI_CAN_ATK_TYPE_BUILDING

    def on_be_hited_by_ray(self, begin_pos, end_pos, shot_type, **kwargs):
        self.show_hit_effect(end_pos, shot_type)

    def on_be_hited_by_bomb(self, begin=None, end=None, itype=None):
        self.show_hit_effect(end, itype)

    def show_hit_effect(self, end_pos, shot_type):
        if end_pos is None:
            return
        else:
            if check_need_ignore_effect_behind_camera(shot_type, end_pos):
                return

            def create_cb(sfx):
                sfx.rotation_matrix = self.rot_mat

            global_data.sfx_mgr.create_sfx_in_scene('effect/fx/weapon/other/dun_hit.sfx', end_pos, on_create_func=create_cb, int_check_type=CREATE_SRC_SIMPLE)
            return