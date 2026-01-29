# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComCamp.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from mobile.common.EntityManager import EntityManager
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode
from logic.client.const import game_mode_const
import game3d
import render
from common.utils import timer
import world
import render
from logic.gcommon.common_const import ui_operation_const as uoc
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const import battle_const as bconst
from logic.gutils.client_unit_tag_utils import register_unit_tag
_HASH_outline_alpha = game3d.calc_string_hash('outline_alpha')
_HASH_u_color = game3d.calc_string_hash('u_color')
OPEN_SEE_THROUGHT = True
RENDER_GROUP_DYOCC_OBJ = 28
DELAY_RESET = 2000
CLOSE_XRAY_QUALITY_LEVEL = 2
REAL_HUMAN_TAG_VALUE = register_unit_tag(('LAvatar', 'LPuppet'))

class ComCamp(UnitCom):
    BIND_EVENT = {'G_IS_CAMPMATE': '_is_campmate',
       'G_IS_CAMPMATE_BY_EID': '_is_campmate_by_eid',
       'G_CAMP_ID': '_get_camp_id',
       'E_CLEAR_CAMP': '_clear_camp',
       'E_SET_CAMP': '_set_camp',
       'E_MODEL_LOADED': 'on_model_loaded',
       'E_MECHA_LOD_LOADED_FIRST': 'on_lod_loaded_first',
       'E_RESET_CAMP_OUTLINE': 'reset_outline_state',
       'E_ENABLE_SEE_THROUGHT': 'enable_see_throught',
       'E_ENABLE_SEE_THROUGHT_FROM_OUTSIDE': 'enable_see_throught_from_outside',
       'G_CAMP_SHOW_SIDE': 'get_show_side',
       'E_ADD_RANGE_SEE_THROUGHT': 'add_range_see_throught',
       'E_DEL_RANGE_SEE_THROUGHT': 'del_range_see_throught',
       'E_ADD_RANGE_OUTLINE': 'add_range_outline',
       'E_DEL_RANGE_OUTLINE': 'del_range_outline',
       'E_DEATH': '_on_death',
       'E_PAUSE_OUTLINE': '_on_pause_outline',
       'G_IS_PAUSE_OUTLINE': '_is_pause_outline',
       'E_TRANS_CREATE_MECHA_TO_SHARE_NOTIFY': 'on_trans_to_share',
       'E_REFRESH_CAMP_SIDE_SHOW': 'refresh_camp_side_show',
       'E_ON_BEING_OBSERVE': 'on_begin_observe',
       'E_ENABLE_MODEL_OUTLINE_ONLY': 'enable_model_outline_only'
       }

    def __init__(self):
        super(ComCamp, self).__init__()

    def init_from_dict(self, unit_obj, bdict):
        super(ComCamp, self).init_from_dict(unit_obj, bdict)
        self._camp_id = bdict.get('faction_id', 0)
        self.share = bdict.get('share', False)
        self._model = None
        self._group_id = None
        self._is_outline = False
        self._alphas = 2.0
        self._side = None
        self._is_add_xray_model = False
        self._is_see_throught = False
        self._is_see_throught_external = False
        self._is_add_xray_and_outline = False
        self._has_add_xray_and_outline = False
        self.enable_model_outline_only = False
        self.delay_exec_id = None
        self._range_radius = 0
        self._last_acc_time = 0
        self._can_add_model_outline_only = False
        self._range_radius_outline = 0
        self._outline_last_acc_time = 0
        self._is_die = False
        self._is_blind = False
        self._is_covered = False
        self._pause_outline = False
        self._external_material_status = set()
        self.enable_see_throught_lock = {}
        global_data.emgr.scene_cam_observe_player_setted += self._on_scene_cam_observe_player_setted
        return

    def _is_campmate(self, camp_id):
        if self._camp_id in bconst.DUEL_FACTION_IDS and camp_id == bconst.COMMON_FACTION_ID or camp_id in bconst.DUEL_FACTION_IDS and self._camp_id == bconst.COMMON_FACTION_ID:
            return True
        return camp_id == self._camp_id

    def _is_campmate_by_eid(self, eid):
        entity = EntityManager.getentity(eid)
        if not (entity and entity.logic):
            return False
        return self._is_campmate(entity.logic.ev_g_camp_id())

    def _get_camp_id(self):
        if not self._camp_id:
            driver = EntityManager.getentity(self.sd.ref_driver_id)
            if driver and driver.logic:
                self._camp_id = driver.logic.ev_g_camp_id()
        elif self.sd.ref_is_mecha and not self.ev_g_passenger_info():
            self._camp_id = 0
        return self._camp_id

    def _set_camp(self, camp_id):
        old_camp_id = self._camp_id
        self._camp_id = camp_id
        self.reset_outline_state()
        self.send_event('E_REFRESH_COLLISION')
        if global_data.battle and hasattr(global_data.battle, 'get_other_duel_player'):
            id = global_data.battle.get_other_duel_player()
            if id:
                entity = EntityManager.getentity(id)
                if entity and entity.logic:
                    entity.logic.send_event('E_RESET_CAMP_OUTLINE')
                    entity.logic.send_event('E_REFRESH_COLLISION')
        if global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_SURVIVALS):
            if self.unit_obj.MASK & REAL_HUMAN_TAG_VALUE:
                if old_camp_id is not None and self._camp_id != old_camp_id:
                    if self.ev_g_is_avatar():
                        self.refresh_former_teammate_material()
                    else:
                        self._refresh_existing_material_statuses()
        return

    def refresh_former_teammate_material(self):
        from mobile.common.EntityManager import EntityManager
        former_teammate_set = self.ev_g_cached_former_teammate_set()
        need_refresh_set = former_teammate_set
        for t_id in need_refresh_set:
            _teammate = EntityManager.getentity(t_id)
            if _teammate and _teammate.logic:
                _teammate.logic.send_event('E_REFRESH_CAMP_SIDE_SHOW')
                control_target = _teammate.logic.ev_g_control_target()
                if control_target and control_target.logic and control_target != _teammate:
                    control_target.logic.send_event('E_REFRESH_CAMP_SIDE_SHOW')

    def refresh_camp_side_show(self):
        self._refresh_existing_material_statuses()

    def _clear_camp(self):
        if self.sd.ref_is_mecha and not self.ev_g_is_mechatran():
            return
        self._camp_id = 0

    def on_model_loaded(self, model):
        self._model = model
        if self.delay_exec_id:
            game3d.cancel_delay_exec(self.delay_exec_id)
        self.reset_outline_state()

        def callback():
            self._can_add_model_outline_only = True
            self.reset_outline_state()
            self.delay_exec_id = None
            return

        self.delay_exec_id = game3d.delay_exec(DELAY_RESET, callback)

    def on_lod_loaded_first(self, *args):
        if self._is_add_xray_model:
            self.add_see_throught()
        self.check_range_buff()
        if self._is_add_xray_and_outline:
            self.add_xray_and_outline()
        if self.delay_exec_id:
            game3d.cancel_delay_exec(self.delay_exec_id)
        self.reset_outline_state()

        def callback():
            self._can_add_model_outline_only = True
            self.reset_outline_state()

        self.delay_exec_id = game3d.delay_exec(DELAY_RESET, callback)

    def is_other_entity(self):
        driver_id = self.sd.ref_driver_id
        alphas = 2.0
        if global_data.cam_lctarget and (global_data.cam_lctarget.id == driver_id or global_data.cam_lctarget.id == self.unit_obj.id) or global_data.cam_lplayer and global_data.cam_lplayer.id == self.unit_obj.id:
            return False
        return True

    def _get_outline_side_color(self, side=None):
        if side is None:
            side = self.get_show_side()
        return self.get_outline_color(side)

    def get_outline_color(self, side):
        outline_alphas = [
         0.0, 0.3333, 0.6666, 1.0]
        if side == None or side > len(outline_alphas) - 1:
            side = 0
        return outline_alphas[side]

    def enable_model_outline_only(self, enable):
        self.enable_model_outline_only = enable
        self.reset_outline_state()

    def reset_outline_state(self, *args):
        if self._is_die:
            return
        else:
            driver_id = self.sd.ref_driver_id
            self._alphas = 2.0
            self._side = None
            if global_data.cam_lctarget and (global_data.cam_lctarget.id == driver_id or global_data.cam_lctarget.id == self.unit_obj.id) or self.unit_obj.sd.ref_is_mecha and self.share and driver_id == None or global_data.cam_lplayer and global_data.cam_lplayer.id == self.unit_obj.id or self._pause_outline:
                self._alphas = 2.0
                self._is_outline = False
            else:
                self._side = self.get_show_side()
                self._is_outline = False
                if self._side is not None:
                    self._alphas = self._get_outline_side_color(self._side)
                    self._is_outline = True
            if self._has_add_xray_and_outline:
                self.del_xray_and_outline()
            if not self.has_range_see_throught():
                if self._is_see_throught:
                    self.del_see_throught()
            self.del_model_outline_only()
            if self._side == 0:
                if global_data.game_mode and global_data.game_mode.is_mode_type(game_mode_const.Add_Friend_OutLineOnly):
                    self.refresh_model_outline_only()
                elif global_data.game_mode and global_data.game_mode.is_mode_type(game_mode_const.Add_Friend_XrayAndOutLine):
                    self._is_add_xray_and_outline = True
                    self.add_xray_and_outline()
                else:
                    self._is_add_xray_model = True
                    self.add_see_throught()
            elif self._side == 1:
                show_outline = False
                if self.enable_model_outline_only or global_data.game_mode and global_data.game_mode.is_mode_type(game_mode_const.Add_Enemy_OutLineOnly):
                    show_outline = True
                elif global_data.game_mode and global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_GULAG_SURVIVAL):
                    from logic.gcommon.common_const.battle_const import REVIVE_NONE, REVIVE_WAIT
                    cam_gulag_game_id = global_data.cam_lplayer and global_data.cam_lplayer.ev_g_gulag_game_id()
                    if cam_gulag_game_id not in (REVIVE_NONE, REVIVE_WAIT):
                        my_gulag_game_id = self.ev_g_gulag_game_id()
                        show_outline = my_gulag_game_id == cam_gulag_game_id
                if show_outline:
                    self.refresh_model_outline_only()
            elif self._side is None:
                pass
            if self._is_see_throught_external:
                self.send_event('E_DEL_MATERIAL_STATUS', 'ComCamp_xray_and_outline')
                self._is_see_throught_external = False
                self.enable_see_throught(True)
            return

    def refresh_model_outline_only(self):
        if not self._model or not self._model.valid:
            return
        if self._is_outline:
            if self._can_add_model_outline_only:
                self.send_event('E_ADD_MATERIAL_STATUS', 'ComCamp_always_outline', param={'status_type': 'OUTLINE_ONLY',
                   'outline_alpha': self._alphas,
                   'update_interval': 2.0
                   }, prority=0, update_when_exist=True)
        else:
            self.send_event('E_DEL_MATERIAL_STATUS', 'ComCamp_always_outline')

    def del_model_outline_only(self):
        self.send_event('E_DEL_MATERIAL_STATUS', 'ComCamp_always_outline')

    def add_model_outline(self, force=False):
        if not self._model or not self._model.valid:
            return
        if not force:
            if self._is_outline:
                return
        self._side = self.get_show_side()
        self._alphas = self._get_outline_side_color(self._side)
        self._is_outline = True
        self.send_event('E_ADD_MATERIAL_STATUS', 'ComCamp_outline', param={'status_type': 'XRAY_AND_OUTLINE',
           'outline_alpha': self._alphas,
           'update_interval': 5.0
           })

    def del_model_outline(self, force=False):
        if not self._model or not self._model.valid:
            return
        if not force:
            if not self._is_outline:
                return
        self._is_outline = False
        self.send_event('E_DEL_MATERIAL_STATUS', 'ComCamp_outline')

    XRAY_AND_OUTLINE_SIDE_COLOR = {0: (0.0625, 0.3359, 1.0, 1.0),
       1: (1.0, 0.0, 0.0, 1.0)
       }

    def _get_xray_and_outline_side_color(self):
        side = self.get_show_side()
        return self.XRAY_AND_OUTLINE_SIDE_COLOR.get(side, (0.0625, 0.3359, 1.0, 1.0))

    def add_xray_and_outline(self, force=False):
        if not self._model or not self._model.valid:
            return
        else:
            if not OPEN_SEE_THROUGHT:
                return
            if not force and self._has_add_xray_and_outline:
                return
            self._has_add_xray_and_outline = True
            if self._is_add_xray_and_outline:
                self._is_add_xray_and_outline = False
            self._side = self.get_show_side()
            self._alphas = self._get_outline_side_color(self._side)
            param = {'status_type': 'XRAY_AND_OUTLINE',
               'u_color': self._get_xray_and_outline_side_color(),
               'outline_alpha': self._alphas,
               'update_interval': 5.0
               }
            quality_level = global_data.gsetting.get_seting_quality()
            if quality_level is None:
                quality_level = 0
            if not force and quality_level < CLOSE_XRAY_QUALITY_LEVEL:
                param['status_type'] = 'OUTLINE_ONLY'
            if global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_NORMAL):
                param['team_outline_tick'] = 1
                param['update_interval'] = 1.0
            self.send_event('E_ADD_MATERIAL_STATUS', 'ComCamp_com_xray_and_outline', param, prority=0)
            return

    def del_xray_and_outline(self):
        self._is_add_xray_and_outline = False
        self._has_add_xray_and_outline = False
        self.send_event('E_DEL_MATERIAL_STATUS', 'ComCamp_com_xray_and_outline')

    def add_see_throught(self, force=False):
        if not self._model or not self._model.valid:
            return
        if self._is_add_xray_model:
            self._is_add_xray_model = False
        if not OPEN_SEE_THROUGHT:
            return
        quality_level = global_data.gsetting.get_seting_quality()
        if not force and quality_level < CLOSE_XRAY_QUALITY_LEVEL:
            return
        if self._is_see_throught:
            return
        self._is_see_throught = True
        self._side = self.get_show_side()
        self.send_event('E_ADD_MATERIAL_STATUS', 'ComCamp_xray', param={'status_type': 'XRAY_ONLY',
           'u_color': self._get_xray_and_outline_side_color(),
           'update_interval': 5.0
           }, prority=0)

    def del_see_throught(self):
        if not self._model or not self._model.valid:
            return
        if not self._is_see_throught:
            return
        self._is_see_throught = False
        self.send_event('E_DEL_MATERIAL_STATUS', 'ComCamp_xray')

    def check_range_buff(self):
        if not global_data.cam_lplayer or not global_data.cam_lctarget:
            return
        if self.is_other_entity():
            range_info = global_data.cam_lctarget.ev_g_xray_range_info()
            if not range_info:
                return
            radius = range_info['radius']
            if radius > 0:
                self.add_range_outline(radius)

    def is_need_update(self):
        if self.has_range_see_throught() or self.has_range_outline():
            return True
        return False

    def has_range_see_throught(self):
        return self._range_radius > 0

    def add_range_see_throught(self, radius):
        self._range_radius = radius
        self.need_update = True
        self.scene.enable_hero_outline(True, self.unit_obj.id)
        self.check_range_see_throught(0.5)

    def del_range_see_throught(self):
        self.del_see_throught()
        self._range_radius = 0
        self.need_update = self.is_need_update()
        self.scene.enable_hero_outline(False, self.unit_obj.id)

    def has_range_outline(self):
        return self._range_radius_outline > 0

    def add_range_outline(self, radius):
        self._range_radius_outline = radius
        self.need_update = True
        self.check_range_outline(0.5)
        self.scene.enable_hero_outline(True, self.unit_obj.id)

    def del_range_outline(self):
        self._range_radius_outline = 0
        self.del_model_outline()
        self.need_update = self.is_need_update()
        self.scene.enable_hero_outline(False, self.unit_obj.id)

    def check_range_see_throught(self, delta):
        if not self.has_range_see_throught():
            return
        self._last_acc_time += delta
        if self._last_acc_time < 0.5:
            return
        self._last_acc_time = 0
        if not global_data.cam_lctarget:
            return
        dir_dis = self.ev_g_position() - global_data.cam_lctarget.ev_g_position()
        if int(dir_dis.length / NEOX_UNIT_SCALE) <= self._range_radius:
            self.add_see_throught(force=True)
        else:
            self.del_see_throught()

    def check_range_outline(self, delta):
        if not self.has_range_outline():
            return
        else:
            self._outline_last_acc_time += delta
            if self._outline_last_acc_time < 0.5:
                return
            self._outline_last_acc_time = 0
            if not global_data.cam_lctarget:
                return
            driver_id = self.sd.ref_driver_id
            if self.unit_obj.ev_g_is_mechatran() and driver_id == None:
                self.del_model_outline(force=True)
                return
            dir_dis = self.ev_g_position() - global_data.cam_lctarget.ev_g_position()
            if int(dir_dis.length / NEOX_UNIT_SCALE) <= self._range_radius_outline:
                self.add_model_outline(force=False)
            else:
                self.del_model_outline(force=False)
            return

    def tick(self, delta):
        self.check_range_see_throught(delta)
        self.check_range_outline(delta)

    def destroy(self):
        if self.delay_exec_id:
            game3d.cancel_delay_exec(self.delay_exec_id)
        global_data.emgr.scene_cam_observe_player_setted -= self._on_scene_cam_observe_player_setted
        super(ComCamp, self).destroy()

    def _on_scene_cam_observe_player_setted(self):
        self._refresh_existing_material_statuses()

    def _refresh_existing_material_statuses(self, *args):
        self.reset_outline_state()
        self.send_event('E_UPDATE_MATERIAL_STATUS_PARAM', 'ComCamp_always_outline', param={'outline_alpha': self._alphas
           }, partial=True)
        self.send_event('E_UPDATE_MATERIAL_STATUS_PARAM', 'ComCamp_outline', param={'outline_alpha': self._get_outline_side_color()
           }, partial=True)
        self.send_event('E_UPDATE_MATERIAL_STATUS_PARAM', 'ComCamp_com_xray_and_outline', param={'u_color': self._get_xray_and_outline_side_color(),
           'outline_alpha': self._get_outline_side_color()
           }, partial=True)
        self.send_event('E_UPDATE_MATERIAL_STATUS_PARAM', 'ComCamp_xray', param={'u_color': self._get_xray_and_outline_side_color()
           }, partial=True)
        self.send_event('E_UPDATE_MATERIAL_STATUS_PARAM', 'ComCamp_xray_and_outline', param={'u_color': self._get_xray_and_outline_side_color(),
           'outline_alpha': 0.3333
           }, partial=True)
        for status_key in self._external_material_status:
            self.send_event('E_UPDATE_MATERIAL_STATUS_PARAM', status_key, param={'u_color': self._get_xray_and_outline_side_color(),
               'outline_alpha': self._get_outline_side_color()
               }, partial=True)

        self.send_event('E_UPDATE_CURRENT_MATERIAL_STATUS')

    def get_show_side(self):
        if global_data.player and global_data.player.in_local_battle():
            if self._camp_id is not None and self._camp_id > 0:
                return 1
            else:
                return

        if not self._get_camp_id():
            return
        else:
            if global_data.is_judge_ob:
                if global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_GVG, game_mode_const.GAME_MODE_DUEL)):
                    if self._get_camp_id() == 1:
                        return 0
                    else:
                        return 1

            if not global_data.cam_lplayer:
                if global_data.player:
                    eid = global_data.player.get_global_spectate_player_id()
                    if eid:
                        from mobile.common.EntityManager import EntityManager
                        ent = EntityManager.getentity(eid)
                        if ent and ent.logic:
                            if ent.logic.ev_g_is_campmate(self._get_camp_id()):
                                return 0
                            else:
                                return 1

                return
            if global_data.cam_lplayer.ev_g_is_campmate(self._get_camp_id()):
                return 0
            return 1
            return

    def _g_group_id(self):
        if not self._group_id:
            driver = EntityManager.getentity(self.sd.ref_driver_id)
            if driver and driver.logic:
                self._group_id = driver.logic.ev_g_group_id()
            else:
                self._group_id = self.ev_g_group_id()
        return self._group_id

    def enable_see_throught(self, enable, key_lock=None):
        if enable:
            if key_lock and key_lock not in self.enable_see_throught_lock:
                self.enable_see_throught_lock[key_lock] = True
        else:
            if key_lock and key_lock in self.enable_see_throught_lock:
                del self.enable_see_throught_lock[key_lock]
            if self.enable_see_throught_lock:
                return
        if not OPEN_SEE_THROUGHT:
            return
        if not self._model or not self._model.valid:
            return
        if self._is_see_throught_external and enable or not self._is_see_throught_external and not enable:
            return
        self._is_see_throught_external = enable
        if enable:
            self.send_event('E_ADD_MATERIAL_STATUS', 'ComCamp_xray_and_outline', param={'status_type': 'XRAY_AND_OUTLINE',
               'u_color': self._get_xray_and_outline_side_color(),
               'outline_alpha': 0.3333,
               'update_interval': 0.5
               })
        else:
            self.send_event('E_DEL_MATERIAL_STATUS', 'ComCamp_xray_and_outline')

    def enable_see_throught_from_outside(self, key, enable, priority=1):
        if not OPEN_SEE_THROUGHT:
            return
        status_key = 'ComCamp_external_' + str(key)
        if enable:
            self.send_event('E_ADD_MATERIAL_STATUS', status_key, param={'status_type': 'XRAY_AND_OUTLINE',
               'u_color': self._get_xray_and_outline_side_color(),
               'outline_alpha': self._get_outline_side_color(),
               'update_interval': 1.0
               }, prority=priority)
            self._external_material_status.add(status_key)
        else:
            self.send_event('E_DEL_MATERIAL_STATUS', status_key)
            if status_key in self._external_material_status:
                self._external_material_status.remove(status_key)

    def _on_death(self, *args):
        self._is_die = True
        if self._is_outline:
            self.send_event('E_DEL_MATERIAL_STATUS', 'ComCamp_always_outline')
        if self._is_see_throught_external:
            self.send_event('E_DEL_MATERIAL_STATUS', 'ComCamp_xray_and_outline')
        self.del_see_throught()
        self.del_xray_and_outline()
        for status_key in self._external_material_status:
            self.send_event('E_DEL_MATERIAL_STATUS', status_key)

    def _on_pause_outline(self, flag):
        self._pause_outline = flag
        self.reset_outline_state()

    def _is_pause_outline(self):
        return self._pause_outline

    def on_trans_to_share(self):
        self.share = True

    def on_begin_observe(self, flag):
        if not self._model or not self._model.valid:
            return
        if flag:
            self._model.all_materials.set_var(_HASH_outline_alpha, 'outline_alpha', 2.0)