# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComBuildingAppearance.py
from __future__ import absolute_import
import six
from .ComBaseModelAppearance import ComBaseModelAppearance
from logic.gcommon.component.share.ComBuildingData import ComBuildingData
from mobile.common.EntityManager import EntityManager
from logic.gcommon.common_const import building_const as b_const
import world
import math3d
from logic.gcommon.common_const import scene_const
from logic.gcommon.common_const import building_const

class ComBuildingAppearance(ComBaseModelAppearance):
    BIND_EVENT = ComBaseModelAppearance.BIND_EVENT.copy()
    BIND_EVENT.update({'E_BUILDING_CHANGE_HP': '_on_hp_change',
       'E_BUILDING_DONE': '_on_building_done',
       'E_HITED': '_on_hited',
       'E_HIT_BLOOD_SFX': '_on_be_hited',
       'E_ADD_THROW_OBJ': '_on_add_throw_obj',
       'E_DEL_THROW_OBJ': '_on_del_throw_obj',
       'G_HP_POSITION': '_on_get_hp_pos',
       'G_BUILDING_NO': '_on_get_building_no',
       'G_BUILD_TIME': '_on_get_birthtime',
       'G_REMAIN_TIME': '_on_get_remaintime',
       'G_IS_CAMPMATE': '_on_get_is_teammate'
       })
    BUILDING_COMPONENT = {b_const.B_MUSIC_PLAYER: ('ComMusicPlayer', 'ComDrivable'),
       b_const.B_BULLET_BOX: ('ComUseable', ),
       b_const.B_REPAIR_BOX: ('ComUseable', ),
       b_const.B_FOOD_BOX: ('ComUseable', ),
       b_const.B_SENTRY_GUN: ('ComSentryGun', 'ComDrivable')
       }
    for building_no in b_const.B_BOUNCER_LIST:
        BUILDING_COMPONENT[building_no] = [
         'ComElasticity', 'ComElasticitySimUI']

    BUILDING_COMPONENT[b_const.B_PVE_SLP_BOUNCER].append('ComPVESlopeBouncer')
    CRASH_EFFECT = {b_const.B_TOWER: 'effect/fx/niudan/daojubeicuihui_baozha_jujita.sfx',
       b_const.B_SHELTER: 'effect/fx/niudan/daojubeicuihui_baozha_shabaodui.sfx'
       }

    def __init__(self):
        super(ComBuildingAppearance, self).__init__()
        self.building_conf = None
        self._building_sfx = None
        self._thow_objs = {}
        return

    def init_from_dict(self, unit_obj, bdict):
        from logic.gcommon.component.share.ComBuildingData import ComBuildingData
        self._build_done = bdict.get('status', building_const.BUILDIND_ST_DONE) == building_const.BUILDIND_ST_DONE
        self._building_no = bdict.get('building_no', None)
        self._birth_time = bdict.get('birthtime', None)
        self._faction_id = bdict.get('faction_id', None)
        self._owner_id = bdict['owner_id']
        self._get_building_conf()
        self._first = not self._build_done
        super(ComBuildingAppearance, self).init_from_dict(unit_obj, bdict)
        return

    def init_functional_components(self, bdict):
        if self._building_no in self.BUILDING_COMPONENT:
            comps = self.BUILDING_COMPONENT[self._building_no]
            for comp_name in comps:
                com_obj = self.unit_obj.add_com(comp_name, 'client.com_building')
                com_obj.init_from_dict(self.unit_obj, bdict)

    def get_model_info(self, unit_obj, bdict):
        pos = bdict.get('position', [0, 0, 0])
        rot = bdict.get('rot', [0, 0, 0, 1])
        rot = [0, 0, 0, 1] if rot is None else rot
        health = bdict.get('health', [0, 1000.0])
        self._cur_blood, self._hp_max = health[0] * 1.0, health[1]
        self._status = bdict.get('status', building_const.BUILDIND_ST_DONE)
        model_path = self.building_conf['ResPath']
        return (
         model_path, None, (pos, rot, bdict))

    def _get_building_conf(self):
        from common.cfg import confmgr
        if self.building_conf:
            return self.building_conf
        self.building_conf = confmgr.get('c_building_res', str(self._building_no))
        return self.building_conf

    def on_load_model_complete(self, model, userdata):
        import math3d
        import collision
        import render
        import game3d
        pos, rot = userdata[0], userdata[1]
        pos = math3d.vector(pos[0], pos[1], pos[2])
        mat = math3d.rotation_to_matrix(math3d.rotation(rot[0], rot[1], rot[2], rot[3]))
        model.world_position = pos
        model.rotation_matrix = mat
        self.init_functional_components(userdata[2])
        if self.need_building():
            self.model.visible = False

            def create_cb(tid, sfx, *args):
                if not self or not self.is_valid():
                    return
                sfx.rotation_matrix = self.model.rotation_matrix
                self._building_sfx = sfx

        extinfo = self.building_conf.get('ExtInfo', {})
        if extinfo.get('hide_model', False):
            self.model.visible = False
        self.appearnce_handler()

    def _on_building_done(self):
        self._build_done = True
        if self._building_sfx:
            self._building_sfx.destroy()
            self._building_sfx = None
        target = EntityManager.getentity(self._owner_id)
        if target and target.logic:
            target.logic.send_event('E_BUILDING_DONE')
        return

    def need_building(self):
        from ...common_utils.building_utils import get_capinfo_by_building
        info = get_capinfo_by_building(self._building_no)
        return not self._build_done and info['AssistAction'] == 'build'

    def _create_bind_sfx(self, model):
        import math3d
        sfx_path = self.building_conf.get('SfxResPath', None)
        if sfx_path:

            def create_cb(tid, sfx, *args):
                if not self or not self.is_valid():
                    return
                sfx.remove_from_parent()
                model.bind('bind_pos', sfx, world.BIND_TYPE_ALL)
                sfx.position = math3d.vector(0, 0, 0)

        return

    def _on_hp_change(self, hp):
        if not self.model or not self.model.valid:
            return
        self._cur_blood = hp * 1.0
        self.send_event('E_HEALTH_HP_CHANGE', hp)
        if hp == 0:
            pos = self.model.position
            if self._building_no == b_const.B_BULLET_BOX:
                sfx_path = 'effect/fx/weapon/huojiantong/huojiantong_damage.sfx'
                global_data.sfx_mgr.create_sfx_in_scene(sfx_path, pos)
            else:
                mat = self.model.get_socket_matrix('fx_boom', world.SPACE_TYPE_WORLD)
                if mat:
                    scale, pos = mat.scale, mat.translation
                    crash_effect = self.CRASH_EFFECT.get(self._building_no, 'effect/fx/niudan/daojubeicuihui_baozha.sfx')

                    def create_cb(sfx):
                        sfx.scale = scale

                    global_data.sfx_mgr.create_sfx_in_scene(crash_effect, pos, on_create_func=create_cb)
                    global_data.sound_mgr.play_sound('Play_grenade', pos, ('grenade',
                                                                           'grenade_explode'))

    def _on_hited(self):
        if self.model and self.model.valid:
            pos = self.model.world_position
            global_data.sound_mgr.play_sound_optimize('Play_bullet_hit', self.unit_obj, pos, ('bullet_hit_material',
                                                                                              'metal'))

    def _on_be_hited(self, begin_pos, end_pos, shot_type, **kwargs):
        if self.ev_g_is_shield():
            return
        if begin_pos and end_pos:
            super(ComBuildingAppearance, self)._on_be_hited(begin_pos, end_pos, shot_type, is_self=kwargs.get('is_self', False), dmg_parts=kwargs.get('dmg_parts', False), col_type=scene_const.COL_STONE)

    def on_model_destroy(self):
        if not self._build_done:
            target = EntityManager.getentity(self._owner_id)
            if target and target.logic:
                target.logic.send_event('E_BUILDING_DONE')
        if self.model:
            player = global_data.player
            target = player.logic if player else None
            if target and target.is_valid() and self._cur_blood != 0:
                mat = self.model.get_socket_matrix('fx_lighting', world.SPACE_TYPE_WORLD)
                if mat:
                    scale, pos = mat.scale, mat.translation

                    def create_cb(sfx):
                        sfx.scale = scale

                    sfx_path = 'effect/fx/niudan/daojubeicuihui.sfx'
                    global_data.sfx_mgr.create_sfx_in_scene(sfx_path, pos, on_create_func=create_cb)
        if self._building_sfx:
            self._building_sfx.destroy()
            self._building_sfx = None
        self.notify_thow_obj()
        return

    def _on_get_building_no(self):
        return self._building_no

    def _on_get_birthtime(self):
        return self._birth_time

    def _on_get_remaintime(self):
        import time
        lifetime = self.building_conf['LifeTime']
        return self._birth_time + lifetime - time.time() + 1

    def _on_get_hp_pos(self):
        if self.model:
            return self.model.position
        else:
            return None
            return None

    def _on_add_throw_obj(self, eid):
        self._thow_objs[eid] = True

    def _on_del_throw_obj(self, eid):
        if eid in self._thow_objs:
            del self._thow_objs[eid]

    def notify_thow_obj(self):
        for eid in six.iterkeys(self._thow_objs):
            obj = EntityManager.getentity(eid)
            if obj and obj.logic:
                obj.logic.send_event('E_RESET_POSITION')

        self._thow_objs = None
        return

    def appearnce_handler(self):
        if self._building_no == b_const.B_FOOD_BOX:
            model = self.model
            if self._first:
                if model and model.valid:
                    model.play_animation('open')

                def cb(*args):
                    if model and model.valid:
                        model.play_animation('openidle')

                model.register_anim_key_event('open', 'end', cb)
            else:
                model.play_animation('openidle')

    def _on_get_is_teammate(self, other_faction_id):
        return self._faction_id == other_faction_id