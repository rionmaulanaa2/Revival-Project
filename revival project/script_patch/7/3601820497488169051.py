# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/QTELocalBattleServer.py
from __future__ import absolute_import
import six
from common.cfg import confmgr
from logic.entities.LocalBattleServer import LocalBattleServer, merge_sync_handler_dict
from data.c_guide_data import GetLocalGuideParams, get_qte_local_damage
from logic.gcommon.common_const import mecha_const as mconst
from logic.gcommon import time_utility as tutil
from logic.gcommon.common_const.skill_const import SKILL_ROLL
from logic.gutils import qte_guide_utils
from logic.gcommon import time_utility as tutil
from mobile.common.IdManager import IdManager
from common.utils.timer import CLOCK
from logic.gcommon.common_utils.math3d_utils import tp_to_v3d
from mobile.common.EntityManager import EntityManager
import logic.gcommon.common_utils.idx_utils as idx_utils
from logic.gcommon.common_const import ai_const
import math3d
from logic.gcommon import const

class QTELocalBattleServer(LocalBattleServer):
    SYNC_BATTLE_HANDLER = merge_sync_handler_dict(LocalBattleServer.SYNC_BATTLE_HANDLER, {'on_wpbar_switch': '_lbs_on_wpbar_switch',
       'create_mecha': '_lbs_create_mecha',
       'try_join_mecha': '_lbs_try_join_mecha',
       'try_leave_mecha': '_lbs_try_leave_mecha',
       'reloaded': '_lbs_reloaded',
       'do_shoot': '_lbs_do_shoot',
       'do_skill': '_lbs_do_skill',
       'create_monster': '_lbs_create_monster',
       'destroy_monster': '_lbs_destroy_monster',
       'create_ai_mecha': '_lbs_create_ai_mecha',
       'destroy_ai_mecha': '_lbs_destroy_ai_mecha',
       'ai_mecha_fire': '_lbs_ai_mecha_fire',
       'freeze_ai_mecha_bullet': '_lbs_freeze_ai_mecha_bullet',
       'resume_ai_mecha_bullet': '_lbs_resume_ai_mecha_bullet',
       'show_mecha_locate': '_lbs_show_mecha_locate',
       'qte_start_mecha_shoot': '_lbs_qte_start_mecha_shoot',
       'qte_stop_mecha_logic': '_lbs_qte_stop_mecha_logic'
       })

    def init_from_dict(self, bdict):
        super(QTELocalBattleServer, self).init_from_dict(bdict)
        self.battle_type = 10
        self.battle_config = confmgr.get('battle_config')
        self.map_config = confmgr.get('map_config')
        self.step_2_monster_id = {}
        self.step_2_ai_mecha = {}
        self.summon_mecha_obj = None
        self.ai_mecha_obj = None
        self.qte_robot_mecha_shoot_timer = None
        self._regist_throw_explosion_event_flag = False
        return

    def get_client_dict(self):
        battle_info = self.battle_config[str(self.battle_type)]
        map_id = battle_info['iMapID']
        position, _yaw = qte_guide_utils.get_qte_local_pos_and_yaw()
        cdict = {'battle_type': self.battle_type,
           'battle_data': battle_info,
           'map_data': self.map_config[str(map_id)],
           'map_id': map_id,
           'player_num': 99,
           'prepare_timestamp': tutil.time(),
           'view_position': position,
           'view_range': 1000
           }
        return cdict

    def get_player_init_dict(self):
        position, yaw = qte_guide_utils.get_qte_local_pos_and_yaw()
        yaw = -1.5
        info = {'position': position,
           'role_id': global_data.player.get_role(),
           'mp_attr': {'human_yaw': yaw},'skills': {SKILL_ROLL: {'last_cast_time': 0,'inc_mp': 10.0,'mp': 150.0,'left_cast_cnt': 999999}},'fashion': {'0': int('20100{}00'.format(global_data.player.get_role()))}}
        return info

    def destroy(self):
        for eid in six.itervalues(self.step_2_monster_id):
            self._lbs_destroy_entity(eid)

        self.step_2_monster_id.clear()
        for robot_pilot_eid, robot_mecha_eid in six.itervalues(self.step_2_ai_mecha):
            self._lbs_destroy_entity(robot_pilot_eid)
            self._lbs_destroy_entity(robot_mecha_eid)

        self.step_2_ai_mecha.clear()
        self.unregist_throw_item_explosion_event()

    def regist_throw_item_explosion_event(self):
        scene = global_data.game_mgr.scene
        if not scene:
            return
        part_throwable_mgr = scene.get_com('PartThrowableManager')
        if not part_throwable_mgr:
            return
        if not self._regist_throw_explosion_event_flag:
            global_data.emgr.scene_throw_item_explosion_event -= part_throwable_mgr.throw_item_explosion
            global_data.emgr.scene_throw_item_explosion_event += self._lbs_update_explosive_item_info
            global_data.emgr.scene_throw_item_explosion_event += part_throwable_mgr.throw_item_explosion
            self._regist_throw_explosion_event_flag = True

    def unregist_throw_item_explosion_event(self):
        if self._regist_throw_explosion_event_flag:
            global_data.emgr.scene_throw_item_explosion_event -= self._lbs_update_explosive_item_info
            self._regist_throw_explosion_event_flag = False

    def get_usual_mecha_ids(self):
        role_id = global_data.player.get_role()
        if role_id == 11:
            return (8001, )
        if role_id == 12:
            return (8002, )
        return (8001, )

    def _lbs_reloaded(self, reload_num, wp_pos=None, t_use=0):
        if wp_pos is None:
            wp_pos = self._lbs_get_value('G_WPBAR_CUR_WEAPON_POS')
        mecha = global_data.player.logic.ev_g_bind_mecha_entity()
        if mecha:
            wp = mecha.logic.ev_g_wpbar_cur_weapon()
            mecha.logic.send_event('E_WEAPON_BULLET_CHG', wp_pos, wp.get_bullet_cap())
        else:
            wp = self._lbs_get_value('G_WPBAR_CUR_WEAPON')
            self._lbs_send_event('E_WEAPON_BULLET_CHG', wp_pos, wp.get_bullet_cap())
        return

    def _lbs_on_wpbar_switch(self, cur_pos):
        if cur_pos == 0:
            return
        self._lbs_send_event('E_SWITCHING', cur_pos)

    def _lbs_create_monster(self, step_id, robot_dict):
        monster = self._lbs_add_entity('Monster', robot_dict)
        monster.logic.send_event('E_FORCE_AGENT')
        monster.logic.send_event('E_SET_AI_DATA', 'enemy_id', global_data.player.id)
        setattr(monster, 'step_id', step_id)
        self.step_2_monster_id[step_id] = monster.id
        global_data.player.logic.send_event('E_SET_LOCAL_BATTLE_AIM_ENTITIES', {0: monster.logic}, 'part_point1')

    def _lbs_destroy_monster(self, step_id, args):
        if step_id not in self.step_2_monster_id:
            return
        else:
            monster_id = self.step_2_monster_id.pop(step_id)
            self._lbs_destroy_entity(monster_id)
            global_data.player.logic.send_event('E_SET_LOCAL_BATTLE_AIM_ENTITIES', {}, None)
            return

    def _lbs_do_shoot(self, start=None, end=None, aim=None, scene_pellet=0, target_dict=None, scene_dict=None, shoot_mask=0, ext_dict=None, wp_pos=None, t_use=0):
        if not target_dict:
            return
        else:
            for target_id in target_dict:
                target_obj = EntityManager.getentity(target_id)
                if not target_obj:
                    log_error('!!!Shoot target not found: %r' % target_id)
                    continue
                hit_target_info = target_dict[target_id]
                if not ext_dict:
                    bullet_type = None if 1 else ext_dict.get('bullet_type')
                    dmg_parts = {}
                    total_damage = 0
                    for part in hit_target_info['parts']:
                        dmg = get_qte_local_damage(bullet_type, part)
                        dmg_parts[part] = (1, dmg)
                        total_damage += dmg

                    start_pos = tp_to_v3d(start)
                    end_pos = tp_to_v3d(end)
                    st_target = (end_pos.x, end_pos.y, end_pos.z)
                    lst_from = (start_pos.x, start_pos.y, start_pos.z)
                    parameters = (ext_dict['bullet_type'], dmg_parts, 0, st_target, lst_from, global_data.player.id)
                    method_name = idx_utils.s_method_2_idx('on_hit_shoot')
                    target_obj.logic.send_event('E_DO_SYNC_METHOD', method_name, parameters)
                    self.do_damage(target_id, target_obj, total_damage)

            return

    def _lbs_create_ai_mecha(self, step_id, pos, yaw, hp=None, shield=None):
        robot_init_dict = {'max_hp': 200,
           'is_robot': True,
           'char_name': 'guide_pilot',
           'weapons': {},'position': pos,
           'faction_id': 1
           }
        robot = self._lbs_add_entity('Puppet', robot_init_dict)
        robot_id = robot.id
        mecha_dict = qte_guide_utils.get_npc_mecha_init_dict(robot_id, pos, yaw, hp, shield)
        mecha = self._lbs_add_entity('Mecha', mecha_dict)
        seat = mecha.logic.ev_g_driver_seat()
        mecha.logic.send_event('E_ADD_PASSENGER', robot_id, seat)
        mecha.logic.send_event('E_FORCE_AGENT')
        mecha.logic.send_event('E_SET_AI_DATA', 'enemy_id', global_data.player.id)
        setattr(mecha, 'step_id', step_id)
        setattr(robot, 'step_id', step_id)
        self.step_2_ai_mecha[step_id] = (robot_id, mecha.id)
        self.ai_mecha_obj = mecha

    def _lbs_ai_mecha_fire(self, step_id, mecha_create_step):
        if mecha_create_step not in self.step_2_ai_mecha:
            return
        else:
            robot_id, mecha_id = self.step_2_ai_mecha[mecha_create_step]
            mecha = EntityManager.getentity(mecha_id)
            wp = mecha.logic.ev_g_wpbar_cur_weapon()
            if wp is None:
                return
            wp.set_bullet_num(1)

            def fire_pos(fire_pos, direction):
                import math
                agl = math.radians(-5)
                direction = direction * math3d.matrix.make_rotation_y(agl)
                fire_pos.y = 343.144379
                return (
                 fire_pos, direction)

            def explose_time--- This code section failed: ---

 256       0  LOAD_CONST            1  ''
           3  LOAD_CONST            2  ('time_utility',)
           6  IMPORT_NAME           0  'logic.gcommon'
           9  IMPORT_FROM           1  'time_utility'
          12  STORE_FAST            1  't_util'
          15  POP_TOP          

 257      16  LOAD_CONST            3  1000.0
          19  LOAD_CONST            4  'speed'
          22  STORE_SUBSCR     

 258      23  LOAD_FAST             1  't_util'
          26  LOAD_ATTR             2  'time'
          29  CALL_FUNCTION_0       0 
          32  LOAD_CONST            3  1000.0
          35  BINARY_ADD       
          36  BINARY_ADD       
          37  INPLACE_POWER    
          38  INPLACE_POWER    
          39  STORE_SUBSCR     

Parse error at or near `STORE_SUBSCR' instruction at offset 22

            mecha.logic._coms['ComMechaAtkGun']._special_exec = fire_pos
            mecha.logic._coms['ComThrowableDriver']._special_exec = explose_time
            if mecha.logic.sd.ref_aim_target is None:
                target = global_data.player
                if target.logic.ev_g_in_mecha('Mecha'):
                    target = target.logic.ev_g_bind_mecha_entity()
                mecha.logic.send_event('E_ATK_TARGET', target.logic)
            if not mecha.logic.sd.ref_is_agent:
                mecha.logic.send_event('E_FORCE_AGENT')
            m_pos = self._lbs_get_value('G_POSITION')
            end_pos = m_pos + math3d.vector(0, 50, 0)

            def stop_fire():
                mecha.logic._coms['ComMechaAtkGun']._special_exec = None
                mecha.logic._coms['ComThrowableDriver']._special_exec = None
                mecha.logic.send_event('E_CTRL_ACTION_STOP', ai_const.CTRL_ACTION_MAIN)
                return

            mecha.logic.send_event('E_SET_AI_DATA', 'enemy_id', global_data.player.id)
            mecha.logic.send_event('E_CTRL_ACTION_START', ai_const.CTRL_ACTION_MAIN, self.id, (end_pos.x, end_pos.y, end_pos.z), False)
            global_data.game_mgr.delay_exec(0.3, stop_fire)
            return

    def _lbs_freeze_ai_mecha_bullet(self, step_id):
        pass

    def _lbs_resume_ai_mecha_bullet(self, step_id):
        pass

    def _lbs_qte_start_mecha_shoot(self, step_id, mecha_create_step):
        if not self.qte_robot_mecha_shoot_timer:
            _, mecha_id = self.step_2_ai_mecha[mecha_create_step]
            mecha = EntityManager.getentity(mecha_id)
            if not mecha.logic._coms['ComMechaAtkGun']._special_exec:

                def fire_pos(fire_pos, direction):
                    import math
                    agl = math.radians(-5)
                    direction = direction * math3d.matrix.make_rotation_y(agl)
                    fire_pos.y = 343.144379
                    return (
                     fire_pos, direction)

                mecha.logic._coms['ComMechaAtkGun']._special_exec = fire_pos
            wp = mecha.logic.ev_g_wpbar_cur_weapon()
            if wp:

                def get_fire_cd():
                    return 2.0

                wp.get_fire_cd = get_fire_cd
            mecha.logic._coms['ComMechaEffect8004'].on_trigger_state_effect('max_heat', '20')
            self.qte_robot_mecha_shoot_timer = global_data.game_mgr.register_logic_timer(lambda m=mecha_create_step: self._qte_mecha_shoot(m), interval=2.0, mode=CLOCK)

    def _lbs_qte_stop_mecha_logic(self, step_id, mecha_create_step):
        if self.qte_robot_mecha_shoot_timer:
            global_data.game_mgr.unregister_logic_timer(self.qte_robot_mecha_shoot_timer)
            self.qte_robot_mecha_shoot_timer = None
        if mecha_create_step in self.step_2_ai_mecha:
            _, mecha_id = self.step_2_ai_mecha[mecha_create_step]
            mecha = EntityManager.getentity(mecha_id)
            mecha.logic.send_event('E_CTRL_ACTION_STOP', ai_const.CTRL_ACTION_MAIN)
        return

    def _qte_mecha_shoot(self, mecha_create_step):
        if mecha_create_step in self.step_2_ai_mecha:
            _, mecha_id = self.step_2_ai_mecha[mecha_create_step]
            mecha = EntityManager.getentity(mecha_id)
            if mecha.logic.sd.ref_aim_target is None:
                target = global_data.player.logic.ev_g_bind_mecha_entity()
                if target:
                    mecha.logic.send_event('E_ATK_TARGET', target.logic)
                else:
                    mecha.logic.send_event('E_ATK_TARGET', self.logic)
            if not mecha.logic.sd.ref_is_agent:
                mecha.logic.send_event('E_FORCE_AGENT')
            if not mecha.logic.ev_g_attack_pos():
                mecha.logic.send_event('E_SET_AI_DATA', 'enemy_id', global_data.player.id)
            wp = mecha.logic.ev_g_wpbar_cur_weapon()
            wp.set_bullet_num(1)
            m_pos = self._lbs_get_value('G_POSITION')
            end_pos = m_pos + math3d.vector(0, 20, 0)
            mecha.logic.send_event('E_CTRL_ACTION_START', ai_const.CTRL_ACTION_MAIN, self.id, (end_pos.x, end_pos.y, end_pos.z), False)
            mecha.logic.send_event('E_CTRL_FACE_TO', end_pos, False)
        return

    def _lbs_update_explosive_item_info(self, explosion_info):
        if not explosion_info:
            return
        else:
            for uniq_key in explosion_info:
                _, item_info = global_data.emgr.scene_find_throw_item_event.emit(uniq_key)[0]
                if not item_info:
                    continue
                owner_id = item_info['owner_id']
                owner = self.local_battle.get_entity(owner_id)
                if not owner or not owner.logic:
                    continue
                info = explosion_info[uniq_key].get('item', {})
                if not global_data.mecha:
                    target = None
                elif owner.id == global_data.mecha.id:
                    if not self.ai_mecha_obj:
                        return
                    target = self.ai_mecha_obj
                elif self.ai_mecha_obj and owner.id == self.ai_mecha_obj.id:
                    target = global_data.mecha
                else:
                    target = None
                if not target or not target.logic:
                    return
                target_pos = target.logic.ev_g_position()
                owner_pos = info.get('position')
                if not owner_pos:
                    return
                owner_pos = math3d.vector(*owner_pos)
                dist = target_pos - owner_pos
                if dist.length > 10 * const.NEOX_UNIT_SCALE:
                    return
                if owner.id == global_data.mecha.id:
                    skill_id = item_info.get('skill_id', None)
                    damage = get_qte_local_damage(skill_id, 0)
                    bomb_id = owner.logic.ev_g_wpbar_cur_weapon().get_item_id()
                    parameters = (bomb_id, 0, 0, owner.logic.ev_g_driver(), info['position'], None)
                    method_name = idx_utils.s_method_2_idx('on_hit_bomb')
                    target.logic.send_event('E_DO_SYNC_METHOD', method_name, parameters)
                    self.do_damage(target.id, target, damage)
                elif self.ai_mecha_obj and owner.id == self.ai_mecha_obj.id:
                    self.qte_mecha_damage(target)

            return

    def qte_mecha_damage(self, mecha):
        shield = mecha.logic.ev_g_shield()
        if shield > 0:
            mecha.logic.send_event('E_SET_SHIELD', shield - 100)
        elif mecha.logic.ev_g_hp() * 1.2 > mecha.logic.ev_g_max_hp():
            mecha.logic.ev_g_damage(50)

    def _lbs_create_mecha(self, mecha_type, pos, yaw, *args):
        mecha_init_dict = qte_guide_utils.get_summon_mecha_init_dict(mecha_type, pos, yaw)
        self.summon_mecha_obj = self._lbs_add_entity('Mecha', mecha_init_dict)
        MECHA_RECALL_CD = 10
        seat = self.summon_mecha_obj.logic.ev_g_driver_seat()
        self._lbs_send_event('E_ON_JOIN_MECHA_START', self.summon_mecha_obj.id, 1, tutil.time(), False, None, seat)
        self.summon_mecha_obj.logic.send_event('E_ADD_PASSENGER', global_data.player.id, seat)
        self._lbs_send_event('E_RECALL_SUCESS', True)
        self._lbs_send_event('E_STATE_CHANGE_CD', mconst.RECALL_CD_TYPE_NORMAL, MECHA_RECALL_CD, MECHA_RECALL_CD)
        ui = global_data.ui_mgr.get_ui('PostureControlUI')
        if ui:
            ui.panel.setVisible(False)
        return

    def _lbs_show_mecha_locate(self, mecha_create_stepid):
        pos = (0, 0, 0)
        if mecha_create_stepid in self.step_2_ai_mecha:
            _, mecha_eid = self.step_2_ai_mecha.get(mecha_create_stepid)
            mecha = self.get_local_battle().get_entity(mecha_eid)
            if mecha and mecha.logic:
                mecha_pos = mecha.logic.ev_g_position()
                pos = (mecha_pos.x, mecha_pos.y, mecha_pos.z)
        global_data.player.logic.send_event('E_QTE_MECHA_POS', pos)

    KNIGHT_THROWABLE_SKILL = 800251

    def _lbs_do_skill(self, skill_id, skill_args):
        if skill_id == 800251:
            self.do_knight_throwable_skill(*skill_args)
            return

    def do_damage(self, target_id, target_obj, damage):
        from logic.gcommon.common_const.battle_const import FIGHT_EVENT_DEATH
        is_mecha = target_obj.__class__.__name__ == 'Mecha'
        if not is_mecha:
            if target_obj.logic.ev_g_hp() < 0:
                return
            target_obj.logic.ev_g_damage(damage)
            if target_obj.logic.ev_g_hp() <= 0:
                target_obj.logic.send_event('T_DEATH', global_data.player.id)
                ui = global_data.ui_mgr.get_ui('BattleHitFeedBack')
                ui and ui._handle_death_event(FIGHT_EVENT_DEATH)
                self.stop_robot_ai(target_id, target_obj)
                step_id = getattr(target_obj, 'step_id', None)
                if step_id:
                    global_data.player.logic.send_event('E_GUIDE_ROBOT_DEAD')
        else:
            if target_obj.logic.ev_g_hp() < 0:
                return
            shield = target_obj.logic.ev_g_shield()
            left_damage = damage
            if shield > 0:
                left_damage = max(0, damage - shield)
                left_shield = max(0, shield - damage)
                target_obj.logic.send_event('E_SET_SHIELD', left_shield)
            if not left_damage:
                return
            hp = target_obj.logic.ev_g_hp()
            left_hp = hp - left_damage
            agony_hp = target_obj.logic.ev_g_max_hp() * 0.2
            if left_hp <= agony_hp:
                self._lbs_send_event('E_GUIDE_MECHA_AGONY')
                return
            target_obj.logic.ev_g_damage(left_damage)
        return

    def stop_robot_ai(self, target_id, target_obj):
        pass

    def do_knight_throwable_skill(self, item_info, stage):
        ITEM_DATA = {'iType': 6,
           'iTriggerType': 2,
           'className': 'ExploderByCollisionItem',
           'fRange': 10.0,
           'fSpeed': 1650.0,
           'iDifferentPartDamage': 0,
           'fGravity': 0.0,
           'fTimeFly': 3.0,
           'fDamage': 1.0,
           'iBuffAdd': [
                      329],
           'iBuffCondition': 1,
           'fMass': 1.0,
           'cCustomParam': {'energy_width': 3.5}}
        item_info.update(ITEM_DATA)
        item_info['skill_id'] = self.KNIGHT_THROWABLE_SKILL
        item_info['mass'] = ITEM_DATA['fMass']
        item_info['gravity'] = ITEM_DATA['fGravity']
        item_info['last_time'] = ITEM_DATA['fTimeFly']
        item_info['u_fSpeed'] = ITEM_DATA['fSpeed']
        item_info['speed'] = ITEM_DATA['fSpeed']
        item_info['fSpeed'] = ITEM_DATA['fSpeed']
        item_info['trigger_type'] = ITEM_DATA['iTriggerType']
        item_info['max_dist'] = ITEM_DATA.get('fMaxDistance', None)
        item_info['custom_param'] = ITEM_DATA.get('cCustomParam', {})
        item_info['damage_type'] = ITEM_DATA['fDamage']
        item_info['buff_add'] = ITEM_DATA['iBuffAdd']
        item_info['buff_cond'] = ITEM_DATA['iBuffCondition']
        item_info['trigger_id'] = global_data.player.id
        item_info['owner'] = global_data.mecha.id
        item_info['mecha_id'] = global_data.mecha.id
        item_info['owner_name'] = ''
        item_info['faction_id'] = 0
        global_data.mecha.logic.send_event('E_THROW_EXPLOSIVE_ITEM', item_info)
        return