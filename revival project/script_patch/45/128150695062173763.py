# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComHumanCollison.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from logic.gcommon.common_const.collision_const import GROUP_DYNAMIC_SHOOTUNIT, GROUP_AUTO_AIM, GROUP_GRENADE
from logic.gcommon.const import COLOR_MASK, COLOR_PART_MAP, LEG_COLOR
from logic.gutils.model_collision_utils import ModelCollisionAgent
import logic.gcommon.common_const.animation_const as animation_const
import collision
import math3d
import weakref

class ComHumanCollison(UnitCom):
    BIND_EVENT = {'E_HUMAN_MODEL_LOADED': 'on_human_model_load',
       'E_TRY_LOAD_HIT_MODEL': 'try_load_hit_model',
       'G_HUMAN_COL_ID': 'get_human_col_id',
       'G_HUMAN_COL': 'get_human_col',
       'G_HUMAN_BASE_COL_ID': 'get_human_base_col_id',
       'G_HUMAN_COL_INFO': 'get_human_col_info',
       'E_DEATH': 'die',
       'E_DEFEATED': 'die',
       'E_REVIVE': ('revive', -5),
       'G_MODEL_HIT_RAY': 'get_hit_by_ray_color',
       'G_SHOOT_PART': 'be_shoot_check',
       'G_HIT_MODEL': 'get_hit_model',
       'E_MARK_GROUPMATE': 'mark_groupmate',
       'E_ON_ACTION_LEAVE_VEHICLE': 'leave_vehicle',
       'E_ON_ACTION_ON_VEHICLE': 'join_vehicle',
       'E_COLLISION_ENABLE': '_set_collision_enable',
       'G_HUMAN_COL_OBJ': 'get_human_col_obj',
       'E_ON_JOIN_MECHA': '_on_join_mecha',
       'E_ON_LEAVE_MECHA': '_on_leave_mecha',
       'E_RESUME_HUMAN_COLLISION': '_on_resume_human_collision',
       'G_IS_PIERCED': 'on_is_pierced',
       'E_REFRESH_COLLISION': 'on_refresh_collision',
       'E_NOTIFY_GUN_SHIELD_COL_BOUND': 'on_gun_shield_col_bound'
       }

    def __init__(self):
        super(ComHumanCollison, self).__init__()
        self.col = None
        self.col_head = None
        self.model = None
        self.col_hided = False
        bat = global_data.battle
        self.is_duel = bat and hasattr(bat, 'is_duel_player')
        self.gun_shield_cols = set()
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComHumanCollison, self).init_from_dict(unit_obj, bdict)
        self.col = None
        self.col_head = None
        self.model_col_agent = ModelCollisionAgent(self, self.on_hit_model_loaded)
        return

    def get_human_col_id(self):
        col_id_list = []
        for col in [self.col, self.col_head]:
            if col:
                col_id_list.append(col.cid)

        for col in self.gun_shield_cols:
            col_id_list.append(col.cid)

        control_target = self.ev_g_control_target()
        if control_target and control_target.logic.__class__.__name__ == 'LMotorcycle':
            control_target_col_id = control_target.logic.ev_g_human_col_id()
            if control_target_col_id:
                col_id_list.extend(control_target_col_id)
        return col_id_list

    def get_human_col(self):
        col_list = []
        for col in [self.col, self.col_head]:
            if col:
                col_list.append(col)

        for col in self.gun_shield_cols:
            col_list.append(col)

        control_target = self.ev_g_control_target()
        if control_target and control_target.logic.__class__.__name__ == 'LMotorcycle':
            control_target_col = control_target.logic.ev_g_human_col()
            if control_target_col:
                col_list.extend(control_target_col)
        return col_list

    def get_human_col_obj(self):
        return self.col

    def die(self, *args):
        self.clear_collison()

    def revive(self, *args):
        if self.model and self.model() and self.model().valid:
            self.create_collision(self.model())

    def get_hit_model(self):
        if not self.model:
            return None
        else:
            return self.model()

    def join_vehicle(self, *args, **kwargs):
        if self.col:
            self.col.car_ishurt = False
        if self.col_head:
            self.col_head.car_ishurt = False

    def leave_vehicle(self):
        if self.col:
            self.col.car_ishurt = True
        if self.col_head:
            self.col_head.car_ishurt = True

    def mark_groupmate(self):
        if self.col:
            self.col.mask = GROUP_GRENADE
            self.col.group = GROUP_DYNAMIC_SHOOTUNIT
            self.model_col_agent.set_mask_and_group(self.col.mask, self.col.group)

    def on_gun_shield_col_bound(self, col, flag):
        if flag:
            self.gun_shield_cols.add(col)
        else:
            col in self.gun_shield_cols and self.gun_shield_cols.remove(col)

    def create_collision(self, model, big_col=True):
        if not self.is_enable():
            return
        if self.ev_g_is_pure_mecha() is True:
            return
        if self.ev_g_death():
            return
        self.del_col()
        self.del_col_head()
        scale = self.unit_obj.get_battle()._ai_hit_box if self.sd.ref_is_robot else 1.0
        self.col = collision.col_object(collision.BOX, math3d.vector(3 * scale, 9 * scale, 3 * scale))
        self.col_head = collision.col_object(collision.CAPSULE, math3d.vector(4 * scale, 2 * scale, 0))
        self.scene.scene_col.add_object(self.col)
        if self.is_friend():
            self.col.mask = GROUP_GRENADE
            self.col.group = GROUP_DYNAMIC_SHOOTUNIT
            self.col_head.mask = GROUP_GRENADE
            self.col_head.group = GROUP_DYNAMIC_SHOOTUNIT
            self.col.ignore_collision = True
            self.col_head.ignore_collision = True
        else:
            group = GROUP_DYNAMIC_SHOOTUNIT | GROUP_AUTO_AIM
            self.col.mask = GROUP_GRENADE
            self.col.group = group
            self.col_head.mask = GROUP_GRENADE
            self.col_head.group = group
        self.col.car_ishurt = True
        self.col_head.car_ishurt = True
        self.model_col_agent.set_mask_and_group(self.col.mask, self.col.group)
        self.scene.scene_col.add_object(self.col)
        self.scene.scene_col.add_object(self.col_head)
        model.bind_col_obj(self.col_head, animation_const.BONE_HEAD_NAME)
        model.bind_col_obj(self.col, animation_const.BONE_BIPED_NAME)
        global_data.emgr.scene_add_shoot_body_event.emit(self.col.cid, self.unit_obj)
        global_data.emgr.scene_add_shoot_body_event.emit(self.col_head.cid, self.unit_obj)

    def _set_collision_enable(self, flag):
        if flag:
            if self.is_friend():
                self.col.mask = GROUP_GRENADE
                self.col.group = GROUP_DYNAMIC_SHOOTUNIT
                self.col_head.mask = GROUP_GRENADE
                self.col_head.group = GROUP_DYNAMIC_SHOOTUNIT
            else:
                group = GROUP_DYNAMIC_SHOOTUNIT | GROUP_AUTO_AIM
                self.col.mask = GROUP_GRENADE
                self.col.group = group
                self.col_head.mask = GROUP_GRENADE
                self.col_head.group = group
        else:
            self.col.mask = 0
            self.col.group = 0
            self.col_head.mask = 0
            self.col_head.group = 0
        self.model_col_agent.set_mask_and_group(self.col.mask, self.col.group)

    def is_friend(self):
        if self.is_duel:
            return global_data.player and global_data.player.logic and global_data.player.logic.ev_g_is_campmate(self.unit_obj.ev_g_camp_id())
        return global_data.player and global_data.player.logic and global_data.player.logic.ev_g_is_groupmate(self.unit_obj.id)

    def on_refresh_collision(self, *args):
        if not self.col:
            return
        if not self.col.group:
            return
        if self.is_friend():
            self.col.mask = GROUP_GRENADE
            self.col.group = GROUP_DYNAMIC_SHOOTUNIT
            self.col_head.mask = GROUP_GRENADE
            self.col_head.group = GROUP_DYNAMIC_SHOOTUNIT
        else:
            group = GROUP_DYNAMIC_SHOOTUNIT | GROUP_AUTO_AIM
            self.col.mask = GROUP_GRENADE
            self.col.group = group
            self.col_head.mask = GROUP_GRENADE
            self.col_head.group = group
        self.model_col_agent.set_mask_and_group(self.col.mask, self.col.group)

    def tick(self, delta):
        if self.col is None:
            return
        else:
            coll_list = self.scene.scene_col.get_interest_contacts(self.col.cid)
            if coll_list:
                for cid in coll_list:
                    global_data.emgr.scene_break_event.emit(cid)

            return

    def on_human_model_load(self, model, *arg):
        if not self.is_enable():
            return
        self.model = weakref.ref(model)
        self.create_collision(model)

    def try_load_hit_model(self, model, hit_model_path):
        if self.col:
            self.model_col_agent.set_mask_and_group(self.col.mask, self.col.group)
        self.model_col_agent.load(model, hit_model_path)
        self.model_col_agent.set_cur_model(model)

    def on_hit_model_loaded(self):
        self.send_event('E_HIT_MODEL_LOADED')

    def destroy(self):
        self.clear_collison()
        self.model = None
        if self.model_col_agent:
            self.model_col_agent.destroy()
            self.model_col_agent = None
        super(ComHumanCollison, self).destroy()
        return

    def clear_collison(self):
        self.del_col()
        self.del_col_head()
        self.gun_shield_cols.clear()

    def del_col(self):
        if self.col:
            if self.col_hided == False:
                model = self.model()
                if model and model.valid:
                    model.unbind_col_obj(self.col)
            global_data.emgr.scene_remove_shoot_body_event.emit(self.col.cid)
            self.scene.scene_col.remove_object(self.col)
            self.col = None
        return

    def del_col_head(self):
        if self.col_head:
            if self.col_hided == False:
                model = self.model()
                if model and model.valid:
                    model.unbind_col_obj(self.col_head)
            global_data.emgr.scene_remove_shoot_body_event.emit(self.col_head.cid)
            self.scene.scene_col.remove_object(self.col_head)
            self.col_head = None
        return

    def _on_pos_changed(self, pos):
        if self.col and pos:
            pos.y += 10
            self.col.position = pos

    def get_hit_by_ray_color(self, begin, pdir):
        if not self.model:
            return None
        else:
            return self.model_col_agent.check_shoot_part(begin, pdir)

    def be_shoot_check(self, color):
        color = color & COLOR_MASK
        color = color if color in COLOR_PART_MAP else LEG_COLOR
        return COLOR_PART_MAP[color]

    def get_human_col_info(self):
        return (
         self.col.group, self.col.mask)

    def get_human_base_col_id(self):
        if self.col:
            return self.col.cid
        else:
            return None

    def _on_join_mecha(self, *args, **kwargs):
        if self.col_hided:
            return
        rm_list = [
         self.col, self.col_head]
        for col in rm_list:
            if col:
                model = self.model()
                if model and model.valid:
                    model.unbind_col_obj(col)
                global_data.emgr.scene_remove_shoot_body_event.emit(col.cid)
                global_data.emgr.scene_remove_common_shoot_obj.emit(col.cid)

        self.col_hided = True

    def _on_leave_mecha(self, *args):
        self._do_resume_collision()

    def _do_resume_collision(self):
        if not self.col_hided:
            return
        if self.col and self.col_head and self.model:
            model = self.model()
            if model and model.valid:
                model.bind_col_obj(self.col, animation_const.BONE_BIPED_NAME)
                model.bind_col_obj(self.col_head, animation_const.BONE_HEAD_NAME)
                global_data.emgr.scene_add_shoot_body_event.emit(self.col.cid, self.unit_obj)
                global_data.emgr.scene_add_shoot_body_event.emit(self.col_head.cid, self.unit_obj)
        self.col_hided = False

    def _on_resume_human_collision(self):
        self._do_resume_collision()

    def on_is_pierced(self):
        return False