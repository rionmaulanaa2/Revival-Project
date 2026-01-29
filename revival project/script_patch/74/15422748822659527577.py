# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/GooseBearBattle.py
from __future__ import absolute_import
import six
import six_ex
from logic.entities.Battle import Battle
from logic.entities.DeathBattle import DeathBattle
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Int, Uuid, Dict, List, Float, Str, Bool, Tuple
import math3d
from logic.gcommon.common_const import scene_const
from logic.gutils.CameraHelper import get_adaptive_camera_fov
from logic.client.const import lobby_model_display_const
from logic.gutils import lobby_model_display_utils
from logic.gcommon import time_utility
from logic.gutils import gravity_mode_utils
from logic.gcommon.common_const import battle_const
from common.cfg import confmgr
import world
SHELTER_MODEL_NAME = ('items_yanti_m_3', 'items_yanti_m_4', 'items_yanti_m_1', 'items_yanti_m_2')
MAP_MODEL_NAME = ('building_tuituile_dimian01_3', 'building_tuituile_dimian01_4', 'building_tuituile_dimian01_1',
                  'building_tuituile_dimian01_2')

class GooseBearBattle(DeathBattle):

    def __init__(self, entityid):
        super(GooseBearBattle, self).__init__(entityid)
        self.process_event(True)
        self.collapse_sfx = confmgr.get('script_gim_ref')['goose_bear_collapse_sfx']
        self.map_sfx = {}
        self.shelter_sfx = {}

    def clear_all_sfx(self):
        for sfxes in six.itervalues(self.map_sfx):
            for sfx in sfxes:
                global_data.sfx_mgr.remove_sfx_by_id(sfx)

        for sfxes in six.itervalues(self.shelter_sfx):
            for sfx in sfxes:
                global_data.sfx_mgr.remove_sfx_by_id(sfx)

        self.map_sfx = {}
        self.shelter_sfx = {}

    def destroy(self, clear_cache=True):
        self.process_event(False)
        super(GooseBearBattle, self).destroy(clear_cache)
        self.clear_map_collapse_timer()
        self.clear_all_sfx()

    def init_from_dict(self, bdict):
        self.reconnect_handle_data(bdict)
        self.sync_battle_time(bdict)
        self.init_parameters(bdict)

    def init_parameters(self, bdict):
        self.battle_bdict = bdict
        self.map_id = bdict.get('map_id')
        self.area_id = bdict.get('area_id')
        self.brief_group_data = bdict.get('brief_group_data', {})
        self.chosen_mecha_dict = bdict.get('chosen_mecha_dict', {})
        self.chosen_fashion_dict = bdict.get('chosen_fashion_dict', {})
        self.confirmed_soul_list = bdict.get('confirmed_soul_list', [])
        self.chosen_mecha_list = six_ex.values(self.chosen_mecha_dict)
        self.choose_mecha_end_timpstamp = bdict.get('choose_mecha_end_timestamp', 0)
        self.is_choose_finished = bdict.get('is_choose_finished', False)
        self.rechoose_mecha_end_timestamp = bdict.get('rechoose_mecha_end_timestamp', 0)
        self.rechoose_mecha_flag = bdict.get('rechoose_mecha_flag', False)
        self.rechoose_mecha_enable_timestamp = -1
        self.group_chat_history = bdict.get('group_chat_history', [])
        self._avatar_mecha_dict = bdict.get('mecha_dict', {})
        self._settle_point = bdict.get('settle_point', 50)
        self.collapse_timestamp_info = bdict.get('collapse_timestamp')
        self.collapse_region = bdict.get('collapse_region', [])
        self.settle_timestamp = 0
        if self.is_choose_finished:
            self.mecha_death_enter_battle()
        else:
            self.load_choose_mecha_scene()
        self.map_collapse_timer = None
        self._show_tip_cache = False
        self._timestamp_cache = 0
        self._cache_valid = False
        self.on_loading_end()
        return

    def on_loading_end(self):
        will_collapse_region, collapse_timestamp = (None, None)
        if self.collapse_timestamp_info:
            will_collapse_region, collapse_timestamp = self.collapse_timestamp_info
        if self.collapse_region and will_collapse_region is not None and will_collapse_region not in self.collapse_region:
            self._warn_collapse(will_collapse_region, collapse_timestamp)
        self.init_map_mode()
        return

    def init_map_mode(self):
        if self.collapse_region:
            scn = self.get_scene()
            if not scn:
                self.clear_map_collapse_timer()
                return
            self.clear_map_collapse_timer()
            for region_idx in self.collapse_region:
                region_idx -= 1
                shelter_model = scn.get_model(SHELTER_MODEL_NAME[region_idx])
                if shelter_model:
                    shelter_model.visible = False
                    shelter_pos = shelter_model.position
                    shelter_model.position = math3d.vector(shelter_pos.x, -1080, shelter_pos.z)
                map_model = scn.get_model(MAP_MODEL_NAME[region_idx])
                if map_model:
                    map_model.visible = False
                    map_pos = map_model.position
                    map_model.position = math3d.vector(map_pos.x, -1080, map_pos.z)

    def get_allow_mechas(self):
        return {
         8005, 8024}

    def is_limit_count(self):
        return False

    def is_all_owned(self):
        return True

    def get_settle_point(self):
        return self._settle_point

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'scene_observed_player_setted_event': self.update_observed,
           'resolution_changed': self.on_resolution_changed,
           'loading_end_event': self.on_loading_end
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def update_observed(self, ltarget):
        if not ltarget:
            return

    def load_finish(self):
        super(GooseBearBattle, self).load_finish()
        self.reconnect_handle_gravity_region()
        self.reconnect_handle_region_timestamp()
        self.reconnect_handle_pc()

    def on_resolution_changed(self):
        if self._cache_valid:
            self.update_gravity_region_timestamp(self._timestamp_cache, self._show_tip_cache)

    @rpc_method(CLIENT_STUB, (Float('init_timestamp'), Bool('show_tip')))
    def init_gravity_region_refresh_tips(self, init_timestamp, show_tip):
        self.update_gravity_region_timestamp(init_timestamp, show_tip)

    @rpc_method(CLIENT_STUB, (List('region_pos'), Float('region_r'), Int('region_level')))
    def init_less_gravity_region(self, region_pos, region_r, region_level):
        infos = []
        for pos in region_pos:
            infos.append((pos, region_r, region_level))

        global_data.gravity_sur_battle_mgr.set_region_param(gravity_mode_utils.LESS_GRAVITY, infos)
        global_data.emgr.init_gravity_region.emit(gravity_mode_utils.LESS_GRAVITY)
        self.notify_less_gravity_region(region_level)

    @rpc_method(CLIENT_STUB, (List('region_pos'), Float('region_r'), Int('region_level')))
    def init_over_gravity_region(self, region_pos, region_r, region_level):
        infos = []
        for pos in region_pos:
            infos.append((pos, region_r, region_level))

        global_data.gravity_sur_battle_mgr.set_region_param(gravity_mode_utils.OVER_GRAVITY, infos)
        global_data.emgr.init_gravity_region.emit(gravity_mode_utils.OVER_GRAVITY)
        self.notify_over_gravity_region(region_level)

    @rpc_method(CLIENT_STUB, (Int('region_level'),))
    def remove_gravity_region(self, region_level):
        self.remove_gravity_region_by_type(gravity_mode_utils.LESS_GRAVITY)
        self.remove_gravity_region_by_type(gravity_mode_utils.OVER_GRAVITY)

    def remove_gravity_region_by_type(self, type):
        global_data.gravity_sur_battle_mgr.set_region_param()
        global_data.emgr.remove_gravity_region.emit(type)

    @rpc_method(CLIENT_STUB, (Dict('stage_dict'),))
    def fight_stage(self, stage_dict):
        player_num = stage_dict.get('fighter_num', 0)
        poison_circle = stage_dict.get('poison_dict', {})
        battle_mark = stage_dict.get('mark_dict', {})
        self.update_player_num((player_num,))
        self.on_battle_status_changed(Battle.BATTLE_STATUS_FIGHT)
        global_data.player.logic and global_data.player.logic.send_event('E_START_POSITION_CHECKER')
        self.init_poison_circle(poison_circle)
        global_mark_dict = battle_mark.get('global_mark_dict', {})
        group_mark_dict = battle_mark.get('group_mark_dict', {})
        soul_mark_dict = battle_mark.get('soul_mark_dict', {})
        for mark_id, (mark_no, point, is_deep, state, create_timestamp, deep_timestamp) in six.iteritems(global_mark_dict):
            self.add_mark_imp(mark_id, mark_no, point, is_deep, state, create_timestamp, deep_timestamp)

        for mark_id, (mark_no, point, is_deep, state, create_timestamp, deep_timestamp) in six.iteritems(group_mark_dict):
            self.add_mark_imp(mark_id, mark_no, point, is_deep, state, create_timestamp, deep_timestamp)

        for mark_id, (mark_no, point, is_deep, state, create_timestamp, deep_timestamp) in six.iteritems(soul_mark_dict):
            self.add_mark_imp(mark_id, mark_no, point, is_deep, state, create_timestamp, deep_timestamp)

        gravity_region_dict = stage_dict.get('gravity_region_dict')
        if gravity_region_dict:
            self.set_gravity_region_dict(gravity_region_dict)
            timestamp = stage_dict.get('gravity_region_refresh_timestamp')
            show_tip = stage_dict.get('gravity_region_show_tip')
            if timestamp:
                self.update_gravity_region_timestamp(timestamp, show_tip)

    def set_gravity_region_dict(self, gravity_region_dict):
        if not gravity_region_dict:
            return
        less_region_centers = gravity_region_dict.get('less_region_center')
        less_region_radius = gravity_region_dict.get('less_region_radius')
        over_region_centers = gravity_region_dict.get('over_region_center')
        over_region_radius = gravity_region_dict.get('over_region_radius')
        region_level = gravity_region_dict.get('region_level')
        if less_region_centers and less_region_radius and not global_data.gravity_sur_battle_mgr.get_region_param(gravity_mode_utils.LESS_GRAVITY):
            infos = []
            for less_region_center in less_region_centers:
                infos.append((less_region_center, less_region_radius, region_level))

            global_data.gravity_sur_battle_mgr.set_region_param(gravity_mode_utils.LESS_GRAVITY, infos)
            global_data.emgr.init_gravity_region.emit(gravity_mode_utils.LESS_GRAVITY)
            self.notify_less_gravity_region(region_level)
        if over_region_centers and over_region_radius and not global_data.gravity_sur_battle_mgr.get_region_param(gravity_mode_utils.OVER_GRAVITY):
            infos = []
            for over_region_center in over_region_centers:
                infos.append((over_region_center, over_region_radius, region_level))

            global_data.gravity_sur_battle_mgr.set_region_param(gravity_mode_utils.OVER_GRAVITY, infos)
            global_data.emgr.init_gravity_region.emit(gravity_mode_utils.OVER_GRAVITY)
            self.notify_over_gravity_region(region_level)

    def notify_over_gravity_region(self, region_level):
        if not region_level:
            return
        msg = {'i_type': battle_const.GOOSEBEAR_OVER_GRAVITY_FIRST_TIP if region_level == 1 else battle_const.GOOSEBEAR_OVER_GRAVITY_REFRESH_TIP,'b_resize': True}
        global_data.emgr.show_battle_main_message.emit(msg, battle_const.MAIN_NODE_COMMON_INFO)

    def notify_less_gravity_region(self, region_level):
        if not region_level:
            return
        msg = {'i_type': battle_const.GOOSEBEAR_LESS_GRAVITY_FIRST_TIP if region_level == 1 else battle_const.GOOSEBEAR_LESS_GRAVITY_REFRESH_TIP,'b_resize': True}
        global_data.emgr.show_battle_main_message.emit(msg, battle_const.MAIN_NODE_COMMON_INFO)

    def reconnect_handle_data(self, bdict):
        self.reconnect_data = {'gravity_region_dict': bdict.get('gravity_region_dict'),
           'gravity_region_refresh_timestamp': bdict.get('gravity_region_refresh_timestamp'),
           'gravity_region_show_tip': bdict.get('gravity_region_show_tip')
           }

    def reconnect_handle_gravity_region(self):
        gravity_region_dict = self.reconnect_data.get('gravity_region_dict')
        if gravity_region_dict:
            self.set_gravity_region_dict(gravity_region_dict)

    def reconnect_handle_region_timestamp(self):
        timestamp = self.reconnect_data.get('gravity_region_refresh_timestamp')
        show_tip = self.reconnect_data.get('gravity_region_show_tip')
        if timestamp:
            self.update_gravity_region_timestamp(timestamp, show_tip)

    def reconnect_handle_pc(self):
        if global_data.pc_ctrl_mgr:
            global_data.pc_ctrl_mgr.enable_keyboard_control(True)

    def update_gravity_region_timestamp(self, timestamp, show_tip):
        self._cache_valid = True
        self._timestamp_cache = timestamp
        self._show_tip_cache = show_tip
        global_data.emgr.update_gravity_region_timestamp.emit(timestamp, show_tip)

    @rpc_method(CLIENT_STUB, ())
    def notify_gravity_refresh(self):
        pass

    def boarding_movie_data(self):
        return None

    def sync_battle_time(self, bdict):
        battle_srv_time = bdict.get('battle_srv_time', None)
        if battle_srv_time and time_utility.TYPE_BATTLE not in time_utility.g_success_flag:
            time_utility.on_sync_time(time_utility.TYPE_BATTLE, battle_srv_time)
        return

    def load_choose_mecha_scene(self):
        scene = global_data.game_mgr.scene
        scene_type = scene.get_type() if scene else None
        if scene_type == scene_const.SCENE_MECHA_DEATH_CHOOSE_MECHA:
            global_data.emgr.enter_mecha_death_choose_mecha.emit()
            return
        else:
            if scene_type == scene_const.SCENE_LOBBY:
                part_mecha_display = scene.get_com('PartMechaDisplay')
                if part_mecha_display:
                    part_mecha_display.hide_all_teammate_tip_ui()

            def enable_mirror():
                scene = world.get_active_scene()
                scene_type = scene.get_type() if scene else None
                global_data.emgr.check_cur_scene_mirror_model_event.emit((scene, scene_type))
                return

            def switch_scene_cb(_scene_type):
                enable_mirror()
                global_data.emgr.enter_mecha_death_choose_mecha.emit()
                self.ask_is_choose_finished()

            if scene_type is None or scene_type == scene_const.SCENE_MAIN:

                def _scene_cb():
                    scene = global_data.game_mgr.scene
                    enable_mirror()
                    scene_data = lobby_model_display_utils.get_display_scene_data(lobby_model_display_const.MECHA_DEATH_CHOOSE_MECHA_SCENE)
                    cam_hanger = scene.get_preset_camera(scene_data.get('cam_key'))
                    cam = scene.active_camera
                    cam.rotation_matrix = math3d.rotation_to_matrix(math3d.matrix_to_rotation(cam_hanger.rotation))
                    cam.world_position = cam_hanger.translation
                    fov = scene_data.get('fov', 55)
                    fov, aspect = get_adaptive_camera_fov(fov)
                    cam.fov = fov
                    cam.aspect = aspect
                    global_data.emgr.camera_inited_event.emit()
                    global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_MECHA_DEATH_CHOOSE_MECHA, lobby_model_display_const.MECHA_DEATH_CHOOSE_MECHA_SCENE, finish_callback=switch_scene_cb)

                global_data.game_mgr.load_scene(scene_const.SCENE_MECHA_DEATH_PREPARE_CHOOSE_MECHA, callback=_scene_cb, async_load=False)
            else:
                global_data.emgr.show_lobby_relatived_scene.emit(scene_const.SCENE_MECHA_DEATH_CHOOSE_MECHA, lobby_model_display_const.MECHA_DEATH_CHOOSE_MECHA_SCENE, finish_callback=switch_scene_cb)
            return

    def mecha_death_enter_battle(self):
        global_data.ui_mgr.close_ui('MechaDeathChooseMechaUI')
        global_data.ui_mgr.close_ui('MechaDeathSkillDetail')
        super(GooseBearBattle, self).init_from_dict(self.battle_bdict)

    def init_rechoose_mecha_ui(self):
        now = time_utility.get_server_time()
        if now < self.rechoose_mecha_end_timestamp and not self.rechoose_mecha_flag:
            from logic.comsys.battle.MechaDeath.MechaDeathRechooseMechaUI import MechaDeathRechooseMechaUI
            MechaDeathRechooseMechaUI(None, global_data.cam_lplayer)
        return

    def try_choose_mecha(self, mecha_id, force=False):
        self.call_soul_method('try_choose_mecha', (mecha_id, force))

    def confirm_choose_mecha(self):
        self.call_soul_method('confirm_choose_mecha', ())

    def try_rechoose_mecha(self):
        self.call_soul_method('try_rechoose_mecha', ())

    def do_rechoose_mecha(self, mecha_id):
        self.call_soul_method('do_rechoose_mecha', (mecha_id,))

    def give_up_rechoose_mecha(self):
        self.rechoose_mecha_end_timestamp = 0
        self.call_soul_method('give_up_rechoose_mecha', ())

    def send_message(self, message):
        self.call_soul_method('send_message', (message,))

    def ask_is_choose_finished(self):
        self.call_soul_method('ask_is_choose_finished', ())

    @rpc_method(CLIENT_STUB, (Bool('result'),))
    def start_combat_result(self, result):
        if result:
            global_data.ui_mgr.close_ui('MechaDeathPlayBackUI')

    @rpc_method(CLIENT_STUB, (Int('end_timestamp'),))
    def on_start_choose_mecha(self, end_timestamp):
        self.choose_mecha_end_timpstamp = end_timestamp

    @rpc_method(CLIENT_STUB, (Uuid('soul_id'), Int('mecha_id'), Dict('fashion_dict'), List('chosen_mecha_list')))
    def choose_mecha_result(self, soul_id, mecha_id, fashion_dict, chosen_mecha_list):
        global_data.emgr.refresh_mecha_death_chosen_mecha.emit(soul_id, mecha_id, fashion_dict, chosen_mecha_list)

    @rpc_method(CLIENT_STUB, (Uuid('soul_id'), List('confirmed_soul_list')))
    def confirm_mecha_result(self, soul_id, confirmed_soul_list):
        self.confirmed_soul_list = confirmed_soul_list
        global_data.emgr.refresh_mecha_death_confirm_mecha.emit(soul_id, self.confirmed_soul_list)

    @rpc_method(CLIENT_STUB, (Uuid('soul_id'), Str('message')))
    def receive_teammate_message(self, soul_id, message):
        global_data.emgr.receive_teammate_message.emit(soul_id, message)

    @rpc_method(CLIENT_STUB, (Dict('stage_dict'),))
    def prepare_stage(self, stage_dict):
        prepare_timestamp = stage_dict.get('prepare_timestamp')
        if prepare_timestamp:
            self.battle_bdict['prepare_timestamp'] = prepare_timestamp
        super(GooseBearBattle, self).prepare_stage((stage_dict,))

    @rpc_method(CLIENT_STUB, (Bool('ret'), Dict('group_loading_dict')))
    def on_goosebear_choose_mecha_finished(self, ret, group_loading_dict):
        self.is_choose_finished = ret
        if ret:
            self.group_loading_dict = group_loading_dict
            self.battle_bdict['group_loading_dict'] = group_loading_dict
            global_data.emgr.mecha_death_choose_mecha_finished.emit()

    @rpc_method(CLIENT_STUB, (Uuid('soul_id'), Dict('killer_info'), Float('mecha_revice_ts')))
    def on_mecha_destroy(self, soul_id, killer_info, mecha_revice_ts):
        global_data.emgr.mecha_death_mecha_destroyed.emit(soul_id, killer_info, mecha_revice_ts)

    @rpc_method(CLIENT_STUB, (Bool('result'), Int('rechoose_mecha_end_timestamp')))
    def rechoose_mecha_result(self, result, rechoose_mecha_end_timestamp):
        if result:
            self.rechoose_mecha_end_timestamp = rechoose_mecha_end_timestamp
            player = global_data.cam_lplayer
            if player:
                cur_mecha_id = player.ev_g_get_bind_mecha_type()
                for mecha_id in self.get_allow_mechas():
                    if cur_mecha_id == mecha_id:
                        continue
                    cur_mecha_id = mecha_id
                    break

                self.do_rechoose_mecha(cur_mecha_id)

    @rpc_method(CLIENT_STUB, ())
    def rechoose_mecha_succ(self):
        self.rechoose_mecha_flag = True
        self.rechoose_mecha_end_timestamp = 0
        global_data.ui_mgr.close_ui('MechaDeathPlayBackUI')

    @rpc_method(CLIENT_STUB, (Int('spawn_id'), Int('faction_id'), Float('rebirth_ts')))
    def update_spawn_rebirth(self, spawn_id, faction_id, rebirth_ts):
        global_data.death_battle_data.update_spawn_rebirth_data({spawn_id: (faction_id, rebirth_ts)})
        global_data.emgr.update_spawn_rebirth_data_event.emit([spawn_id])

    def clear_map_collapse_timer(self):
        self.map_collapse_timer and global_data.game_mgr.get_logic_timer().unregister(self.map_collapse_timer)
        self.map_collapse_timer = None
        return

    @rpc_method(CLIENT_STUB, (Int('region_idx'),))
    def do_collapse(self, region_idx):
        self.collapse_region.append(region_idx)
        self.map_collapse()
        global_data.emgr.goosebear_do_collapse_event.emit()
        scn = self.get_scene()
        if not scn:
            return
        else:
            if region_idx not in self.map_sfx:
                self.map_sfx[region_idx] = [
                 None, None]
            sfx_id, _ = self.map_sfx[region_idx]
            if sfx_id:
                global_data.sfx_mgr.remove_sfx_by_id(sfx_id)
                self.map_sfx[region_idx][1] = None
            map_model = scn.get_model(MAP_MODEL_NAME[region_idx - 1])
            if map_model:
                sfx_id = global_data.sfx_mgr.create_sfx_on_model(self.collapse_sfx[1], map_model, 'fx_root')
                self.map_sfx[region_idx][1] = sfx_id
            if region_idx not in self.shelter_sfx:
                self.shelter_sfx[region_idx] = [
                 None, None]
            sfx_id, _ = self.shelter_sfx[region_idx]
            if sfx_id:
                global_data.sfx_mgr.remove_sfx_by_id(sfx_id)
                self.shelter_sfx[region_idx][1] = None
            shelter_model = scn.get_model(SHELTER_MODEL_NAME[region_idx - 1])
            if shelter_model:
                sfx_id = global_data.sfx_mgr.create_sfx_on_model(self.collapse_sfx[1], shelter_model, 'fx_root')
                self.shelter_sfx[region_idx][1] = sfx_id
            return

    def map_collapse(self):
        from common.utils import timer
        import time
        speed = 1000
        self.cur_time = time.time()

        def on_check():
            cur_time = time.time()
            y_offset = speed * (cur_time - self.cur_time)
            self.cur_time = cur_time
            scn = self.get_scene()
            if not scn:
                self.clear_map_collapse_timer()
                return
            end_count = 0
            for region_idx in self.collapse_region:
                region_idx -= 1
                map_model = scn.get_model(MAP_MODEL_NAME[region_idx])
                shelter_model = scn.get_model(SHELTER_MODEL_NAME[region_idx])
                if not map_model:
                    self.clear_map_collapse_timer()
                    continue
                if map_model.position.y < -1080:
                    map_model.visible = False
                    if shelter_model:
                        shelter_model.visible = False
                    end_count += 1
                    if end_count >= len(self.collapse_region):
                        self.clear_map_collapse_timer()
                    continue
                pos = map_model.position
                map_model.position = math3d.vector(pos.x, pos.y - y_offset, pos.z)
                if shelter_model:
                    shelter_pos = shelter_model.position
                    shelter_model.position = math3d.vector(shelter_pos.x, shelter_pos.y - y_offset, shelter_pos.z)

        self.clear_map_collapse_timer()
        self.map_collapse_timer = global_data.game_mgr.get_logic_timer().register(func=on_check, mode=timer.LOGIC, interval=1)

    @rpc_method(CLIENT_STUB, ())
    def notify_collapse(self):
        pass

    @rpc_method(CLIENT_STUB, (Int('region_idx'), Float('collapse_timestamp')))
    def warn_collapse(self, region_idx, collapse_timestamp):
        self.collapse_timestamp_info = (region_idx, collapse_timestamp)
        self._warn_collapse(region_idx, collapse_timestamp)

    def _warn_collapse(self, region_idx, collapse_timestamp):
        if collapse_timestamp is None:
            return
        else:
            msg = {'i_type': battle_const.GOOSEBEAR_MAP_COLLAPSE_TIP,'in_anim': 'appear','out_anim': 'disappear','b_resize': True}
            global_data.emgr.show_battle_main_message.emit(msg, battle_const.MAIN_NODE_COMMON_INFO)
            from logic.gcommon.time_utility import get_server_time_battle
            import math
            delay_time = int(math.ceil(collapse_timestamp - get_server_time_battle()))
            if delay_time > 0:
                message_data = {'content_txt': get_text_by_id(19446),'delay_time': delay_time}
                global_data.emgr.battle_event_message.emit(message_data, message_type=battle_const.UP_NODE_GOOSEBEAR_RIKO_TIPS)
                global_data.emgr.goosebear_warn_collapse_event.emit()
            scn = self.get_scene()
            if not scn:
                return
            if region_idx not in self.map_sfx:
                self.map_sfx[region_idx] = [
                 None, None]
            sfx_id, _ = self.map_sfx[region_idx]
            if sfx_id:
                global_data.sfx_mgr.remove_sfx_by_id(sfx_id)
                self.map_sfx[region_idx][0] = None
            map_model = scn.get_model(MAP_MODEL_NAME[region_idx - 1])
            if map_model:
                sfx_id = global_data.sfx_mgr.create_sfx_on_model(self.collapse_sfx[0], map_model, 'fx_root')
                self.map_sfx[region_idx][0] = sfx_id
            if region_idx not in self.shelter_sfx:
                self.shelter_sfx[region_idx] = [
                 None, None]
            sfx_id, _ = self.shelter_sfx[region_idx]
            if sfx_id:
                global_data.sfx_mgr.remove_sfx_by_id(sfx_id)
                self.shelter_sfx[region_idx][0] = None
            shelter_model = scn.get_model(SHELTER_MODEL_NAME[region_idx - 1])
            if shelter_model:
                sfx_id = global_data.sfx_mgr.create_sfx_on_model(self.collapse_sfx[0], shelter_model, 'fx_root')
                self.shelter_sfx[region_idx][0] = sfx_id
            return

    @rpc_method(CLIENT_STUB, (Bool('_first_launch_special_items'),))
    def notify_launch_items(self, _first_launch_special_items):
        if _first_launch_special_items:
            i_type = battle_const.GOOSEBEAR_PROP_FIRST_TIP
        else:
            i_type = battle_const.GOOSEBEAR_PROP_REFRESH_TIP
        msg = {'i_type': i_type,'in_anim': 'appear','out_anim': 'disappear','b_resize': True}
        global_data.emgr.show_battle_main_message.emit(msg, battle_const.MAIN_NODE_COMMON_INFO)