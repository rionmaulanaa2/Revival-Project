# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComSound.py
from __future__ import absolute_import
import six
from ..UnitCom import UnitCom
import common.utils.timer as timer
import math3d
import world
import logic.gcommon.const as const
import game3d
from logic.gcommon.common_const.scene_const import *
from logic.gcommon.common_const import animation_const
import collision
import wwise
from logic.gcommon.item.item_use_var_name_data import *
from common.cfg import confmgr
from logic.gcommon.common_const import building_const as b_const
from logic.gcommon.const import DEFAULT_ROLE_ID, SEX_FEMALE, HIT_PART_SHIELD, HIT_PART_HEAD
from logic.gcommon.common_const import collision_const
from logic.gcommon.cdata import status_config
import time
from logic.gcommon.common_const import attr_const
import logic.gcommon.common_utils.bcast_utils as bcast_utils
from logic.gutils import sound_utils
from logic.gutils.CameraHelper import check_in_room
from logic.gutils import scene_utils
from logic.gcommon.common_const.weapon_const import WP_SPELL, WP_CONTINUOUS_LASER
sound_speed = const.SOUND_SPEED
person_half_height = math3d.vector(0, 9, 0)
G_SILENCER_LIST = None
BUILDING_SOUND_MAP = {b_const.B_BULLET_BOX: ('danyaoxiang_kaiqi', 'danyaoxiang_chenggong'),
   b_const.B_REPAIR_BOX: ('xiulitai_xiuli', 'xiulitai_chenggong'),
   b_const.B_FOOD_BOX: ('bujitai_jinshi', 'bujitai_chenggong')
   }
INDOOR = 1
OUTDOOR = 0

def get_silencer_list():
    global G_SILENCER_LIST
    if G_SILENCER_LIST == None:
        G_SILENCER_LIST = []
        for item_id, item_data in six.iteritems(confmgr.get('firearm_component')):
            if not isinstance(item_data, str) and item_data['iAttachmentKind'] == 2:
                G_SILENCER_LIST.append(int(item_id))

    return G_SILENCER_LIST


class ComSound(UnitCom):
    BIND_EVENT = {'E_MODEL_LOADED': 'on_model_loaded',
       'E_ANIMATOR_LOADED': 'on_load_animator_complete',
       'E_ATTACK_START': '_play_fire_sound_single',
       'E_ATTACK_END': '_stop_fire_sound_auto',
       'E_ATK_GUN_DESTROY': '_stop_fire_sound_auto',
       'E_ARMOR_ATTACK_END': '_stop_fire_sound_auto',
       'E_PLAY_FOOTSTEP_SOUND': '_play_footstep_sound',
       'E_WPBAR_SWITCH_CUR': '_weapon_change',
       'E_FINISH_SWITCH_GUN': '_weapon_change',
       'E_SWITCHED_WP_MODE': '_weapon_change',
       'E_AIR_SHOOT': '_play_sound_bullet_hit',
       'E_HIT_BLOOD_SFX': '_play_sound_hit_body',
       'E_HIT_BOMB_SOUND': '_play_sound_bomb_hit',
       'E_HIT_SPELL_SOUND': '_play_sound_hit_body',
       'E_PALY_SKILL_HIT_SOUND': '_play_sound_skill_hit',
       'E_HIT_LIGHTING_21': '_play_sound_lightning_21_hit',
       'E_HIT_BUFF_SOUND': '_play_sound_buff_hit',
       'E_WEAPON_SHIELD_GUN_BROKEN': 'shield_gun_broken',
       'E_SYNC_HIT_SOUND': '_play_sync_hit_sound',
       'E_OPEN_PARACHUTE_SOUND': '_player_open_parachute',
       'E_START_PARACHUTE': '_player_fall_whistle',
       'E_PARACHUTE_MOVE_SOUND': '_player_move_parachute',
       'E_LAND': '_player_land',
       'E_SUCCESS_BOARD': '_on_skate',
       'E_LEAVE_ATTACHABLE_ENTITY': '_off_skate',
       'E_ACTION_JUMP_WITH_SKATE': '_jump_skate',
       'E_ACTION_SKATE_MOVE_STOP': '_stop_skate',
       'E_SKATE_CHANGE_DIR_SOUND': '_change_dir_skate',
       'E_SKATE_CHANGE_SPEED': '_change_dir_skate',
       'E_CTRL_ROLL': '_roll_sound',
       'E_PLAY_RUSH_SOUND': '_rush_sound',
       'E_PLAY_JUMP_SOUND': '_player_jump',
       'E_ON_GROUND': '_player_ground',
       'E_CLIMB': '_player_climb',
       'E_ACTION_SWITCHING': '_play_change_weapon',
       'E_PICK_UP_SOUND': '_play_pick_up',
       'E_ON_EQUIP_ATTACHMENT': '_play_equip_item',
       'E_THROW_ITEM_SOUND': '_play_throw_item',
       'E_WEAPON_TACKOFF_SOUND': '_play_throw_item',
       'E_START_BOMB_ROCKER': '_play_wait_throw',
       'E_THROW_BOMB': '_play_throw',
       'E_RELOADING': '_play_reload_nf',
       'E_CANCEL_RELOAD': '_on_cancel_reload',
       'E_NEARBY_SESSION_MIC_STATE': '_on_nearby_session_mic_state',
       'E_NEARBY_VOICE_INFO': '_on_nearby_voice_info',
       'E_ITEMUSE_PRE': '_on_use_prop',
       'E_SUPER_JUMP': '_on_super_jump',
       'E_START_USE_BUILDING': '_on_start_use_building',
       'E_USE_BUILDING_SUCCESS': '_on_use_building_success',
       'E_GET_SUPPLY': '_on_get_supply',
       'E_HUMAN_MODEL_LOADED': 'register_weapon_sound',
       'E_DEATH': '_on_death',
       'G_CAM_PLAYER_POS': 'get_cam_player_pos',
       'E_PLAY_WATER_EFFECT_BY_PATH': '_play_jump_water',
       'E_ENTER_STATE': '_enter_states',
       'E_LEAVE_STATE': '_leave_states',
       'E_DEFEATED': '_on_defeated',
       'E_SUCCESS_AIM': '_play_open_aim',
       'E_QUIT_AIM': '_play_close_aim',
       'E_ITEMUSE_END': '_on_cancel_use_item',
       'E_PLAY_ON_USED_SOUND': '_play_on_used_sound',
       'E_BC_RTPC': 'set_bc_rtpc',
       'E_SOUND_TIP_CD': '_play_tip_cd_sound'
       }

    def __init__(self):
        super(ComSound, self).__init__()
        self.sound_mgr = global_data.sound_mgr
        self._human_sound_id = self.sound_mgr.register_game_obj('human')
        self._hit_sound_id = self.sound_mgr.register_game_obj('hit')
        self._fly_sound_id = self.sound_mgr.register_game_obj('hit_fly')
        self._fall_whistle_player_id = None
        self._fire_auto_player_id = None
        self._skate_player_id = None
        self._skate_jump_land_tag = False
        self._fire_auto_timer = None
        self._skate_timer = None
        self._is_fly_sound = 0
        self._is_continue_sound = 0
        self._scene = world.get_active_scene()
        self._cur_weapon = None
        self._wp_nf = False
        self._fire_sound = None
        self._reload_sound = None
        self._ex_fire_sound = None
        self.is_1p = False
        global_data.emgr.settle_stage_event += self.battle_end
        global_data.emgr.scene_camera_target_setted_event += self.on_player_setted
        self._env_type = ENV_TYPE_OUTSIDE
        self._indoor_revb1_value = 0
        self._footstep_type_name = ''
        self._footstep_material_type = ''
        self._gun_option = ''
        self._reload_callback_handler = None
        self.play_water_soundt_time = time.time()
        self.footsetp_event_namme = ''
        self.play_weapon_name = 'Play_weapon_fire'
        self.play_footstep_name = 'Play_footstep'
        self._silencer_list = get_silencer_list()
        self._use_prop_play_id = None
        self.indoor_timer = None
        self.indoor_state = OUTDOOR
        global_data.sound_mgr.set_state('revb_indoor', 'outdoor')
        self._stop_fire_sound_delay_id = None
        self._is_spell_wp = False
        self._is_laser_wp = False
        self.tip_cd_tag = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComSound, self).init_from_dict(unit_obj, bdict)
        role_id = bdict.get('role_id', DEFAULT_ROLE_ID)
        role_sex = confmgr.get('role_info', 'RoleInfo', 'Content', str(role_id), 'sex')
        self._role_sex = role_sex
        self.sd.ref_nearby_streamid = bdict.get('nearby_streamid', None)
        self._nearby_session_mic = bdict.get('nearby_state', 0)
        self.on_player_setted()
        return

    def on_init_complete(self):
        near_mic = global_data.message_data.get_seting_inf('ccmini_near_mic')
        self.send_event('E_CALL_SYNC_METHOD', 'set_nearby_session_mic', (near_mic,))

    def register_weapon_sound(self, model, *arg):
        pass

    def on_load_animator_complete(self, *args):
        self._register_sound_event()

    def _register_sound_event(self):
        animator = self.ev_g_animator()
        if not animator:
            return
        else:
            model = self.ev_g_model()
            if not model:
                return
            animate_sound_map = confmgr.get('animate_sound', 'human', default=None)
            if animate_sound_map:
                for _, datas in six.iteritems(animate_sound_map['Content']):
                    anima = datas['anima']
                    event = datas['event']
                    sound_name = datas['sound_name']
                    is_immediate = datas.get('is_immediate', False)
                    if model.has_anim_event(anima, event):
                        if global_data.enable_animator_reg_event and animator:
                            animator.add_trigger_clip(anima, event, self.on_animate_sound, [sound_name, is_immediate])
                        else:
                            model.register_anim_key_event(anima, event, self.on_animate_sound, [sound_name, is_immediate])

            return

    def on_model_loaded(self, model):
        pass

    def on_animate_sound(self, model, anima, enent, data):
        if self._wp_nf:
            return
        else:
            sound_name = data[0]
            is_immediate = data[1]
            is_need_switch = False
            if global_data.cam_lctarget and self.unit_obj != global_data.cam_lctarget:
                return
            pos = self.ev_g_model_position()
            if not pos:
                return
            if isinstance(sound_name, str):
                self.set_gun_option(sound_name)
                if not is_immediate:
                    self.sound_mgr.post_event(self.play_weapon_name, self._human_sound_id, pos)
                else:
                    self.sound_mgr.post_event_non_optimization(self.play_weapon_name, self._human_sound_id, pos)
            else:
                if isinstance(sound_name, list):
                    sound_name = tuple(sound_name)
                for data in sound_name[1:]:
                    if data[0] == 'gun_option':
                        self.set_gun_option(data[1])
                    else:
                        self.sound_mgr.set_switch(data[0], data[1], self._human_sound_id)
                        is_need_switch = True

                self.sound_mgr.post_event(sound_name[0], self._human_sound_id, pos)
            if is_need_switch and self._cur_weapon:
                name = self._cur_weapon.get_key_config_value('cSoundName', default=None)
                if name and isinstance(name, str):
                    self.sound_mgr.set_switch('gun', name, self._human_sound_id)
            return

    def play_weapon_sound(self, *args):
        pos = self.ev_g_model_position()
        if not pos:
            return
        sound_name = args[3]
        self.sound_mgr.set_switch('gun_reload', sound_name, self._human_sound_id)
        self.sound_mgr.post_event('Play_gun_reload', self._human_sound_id, pos + person_half_height)

    def shield_gun_broken(self, *args):
        self.play_weapon_sound('', '', '', 'shield_break')

    def on_player_setted(self, *args):
        _player = global_data.cam_lplayer
        self._is_clien_player = True if _player == self.unit_obj else False
        if self._is_clien_player:
            self.is_1p = True
        else:
            self.is_1p = False
        if self._is_clien_player and global_data.sound_mgr.is_high_default_pool():
            self.play_weapon_name = 'Play_weapon_fire_1p'
            self.play_footstep_name = 'Play_footstep_1p'
            self.footsetp_event_namme = 'Play_footstep_1p' if self._role_sex == SEX_FEMALE else 'Play_footstep_male_1p'
        else:
            self.play_weapon_name = 'Play_weapon_fire'
            self.play_footstep_name = 'Play_footstep'
            self.footsetp_event_namme = 'Play_footstep' if self._role_sex == SEX_FEMALE else 'Play_footstep_male'
        if self.indoor_timer:
            global_data.game_mgr.unregister_logic_timer(self.indoor_timer)
        self.indoor_timer = global_data.game_mgr.register_logic_timer(self.check_indoor, interval=0.3, times=-1, mode=timer.CLOCK)
        if self.is_1p:
            global_data.emgr.player_open_sound_tip_cd += self.set_open_sound_tip_cd
            self.set_open_sound_tip_cd()

    def check_indoor(self):
        pos = self.get_cam_player_pos()
        scn = global_data.game_mgr.scene
        if not pos or not scn:
            return
        state = INDOOR if check_in_room(pos, scn, 50) else OUTDOOR
        if self.indoor_state != state:
            tag = 'indoor' if state == INDOOR else 'outdoor'
            global_data.sound_mgr.set_state('revb_indoor', tag)
            self.indoor_state = state

    def _on_nearby_voice_info(self, nearby_streamid, nearby_eid):
        self.sd.ref_nearby_streamid = nearby_streamid

    def _on_nearby_session_mic_state(self, state):
        self.sd.ref_nearby_session_mic = state

    def _play_footstep_sound(self, *args):
        sound_name = animation_const.sound_name_map.get(args[0], 'run')
        self.footstep_sound(sound_name)

    def _player_ground(self, *args):
        self.footstep_sound('jump')

    def footstep_sound(self, foot_type):
        type_name = foot_type
        player_pos = self.get_cam_player_pos()
        if not player_pos:
            return
        unit_pos = self.ev_g_model_position()
        if not unit_pos:
            return
        vect = unit_pos - player_pos
        dis_factor = self.ev_g_add_attr(attr_const.ATTR_FOOTSTEP_SOUND_DIS_FACTOR)
        factor_sqr = (1 - dis_factor) ** 2
        sound_length_sqr = vect.length_sqr * factor_sqr
        listen_dis_sqr = global_data.cam_lplayer.ev_g_addition_effect(const.WWISE_FOOTSTEP_MAX_DIS_SQR, factor_attrs=[attr_const.ATTR_LISTEN_RANGE_FACTOR])
        if sound_length_sqr > listen_dis_sqr:
            return
        if type_name != 'swim':
            offset = math3d.vector(0, -2.0 * const.NEOX_UNIT_SCALE, 0)
            result = self._scene.scene_col.hit_by_ray(unit_pos - offset, unit_pos + offset, 0, collision_const.GROUP_CHARACTER_INCLUDE, collision_const.GROUP_CHARACTER_INCLUDE, collision.INCLUDE_FILTER, False)
            if result[0]:
                cobj = result[5]
                is_chunk_mesh = scene_utils.is_chunk_mesh(cobj)
                group_id = cobj.group
                if is_chunk_mesh or group_id == collision_const.TERRAIN_GROUP:
                    material_index = self._scene.get_scene_info_2d(unit_pos.x, unit_pos.z)
                    material_type = material_dic.get(material_index, 'dirt')
                else:
                    material_type = collision_material_to_sound.get(group_id, 'dirt')
                if self._footstep_material_type != material_type:
                    self._footstep_material_type = material_type
                    self.sound_mgr.set_switch('materials', material_type, self._human_sound_id)
                self.send_event('E_FOOTSTEP_SMOKE', material_type, unit_pos, sound_length_sqr)
        else:
            material_type = 'water'
            if self._footstep_material_type != material_type:
                self._footstep_material_type = material_type
                self.sound_mgr.set_switch('materials', material_type, self._human_sound_id)
            if type_name == 'run':
                sound_visible_type = const.SOUND_TYPE_FOOTSTEP
            else:
                sound_visible_type = const.SOUND_TYPE_SLOW_FOOTSTEP
            if self._footstep_type_name != type_name:
                self._footstep_type_name = type_name
                self.sound_mgr.set_switch('fs_type', self._footstep_type_name, self._human_sound_id)
            if self.ev_g_get_state(status_config.ST_SKATE):
                self._land_skate()
            else:
                self.sound_mgr.post_event(self.footsetp_event_namme, self._human_sound_id, unit_pos)
            if not global_data.cam_lplayer:
                return
        if not global_data.cam_lplayer.ev_g_is_campmate(self.unit_obj.ev_g_camp_id()) and foot_type != animation_const.SOUND_TYPE_CRAWL:
            global_data.emgr.sound_visible_add.emit(self.unit_obj, unit_pos, sound_visible_type, sound_length_sqr)

    def _weapon_change(self, *args):
        self._cur_weapon = self.sd.ref_wp_bar_cur_weapon
        if self._cur_weapon:
            name = self._cur_weapon.get_key_config_value('cSoundName', default=None)
            if isinstance(name, str):
                self._wp_nf = False
                self.sound_mgr.set_switch('gun', name, self._human_sound_id)
                self.sound_mgr.set_switch('weapon', name, self._human_sound_id)
            elif isinstance(name, list) and name[1] == 'nf':
                self._wp_nf = True
                self._fire_sound = name[0]
            self._ex_fire_sound = self._cur_weapon.get_key_config_value('cExFireSound', None)
            self._is_fly_sound = self._cur_weapon.get_key_config_value('iIsFlySound')
            self._is_continue_sound = self._cur_weapon.get_key_config_value('iIsContinueSound')
            atk_spd = self._cur_weapon.get_key_config_value('fCDTime', default=None)
            if atk_spd:
                self.sound_mgr.set_rtpc('attack_speed', atk_spd * 100, self._human_sound_id)
            tails_sound = self._cur_weapon.get_key_config_value('cTailsSound', default=None)
            if tails_sound:
                self.sound_mgr.set_switch('gun_tails', tails_sound, self._human_sound_id)
            self._reload_sound = self._cur_weapon.get_key_config_value('cReloadSound', default=None)
            wp_type = self._cur_weapon.get_key_config_value('iKind', default=None)
            self._is_spell_wp = wp_type == WP_SPELL
            self._is_laser_wp = wp_type == WP_CONTINUOUS_LASER
        return

    def _play_fire_sound_single(self, *args):
        if args:
            return
        if not self._cur_weapon:
            return
        bullet_num = self._cur_weapon.get_bullet_num()
        player_pos = self.get_cam_player_pos()
        if not player_pos:
            return
        pos = self.ev_g_model_position()
        if not pos:
            return
        vect = pos - player_pos
        sound_length_sqr = vect.length_sqr
        if sound_length_sqr > const.WWISE_FIRE_MAX_DIS_SQR:
            return
        item_data = self.ev_g_attachment_attr(const.ATTACHEMNT_MUZZLE_POS)
        if self._ex_fire_sound:
            post_fix = '1p' if self.is_1p else '3p'
            event_name = '{}_{}'.format(self._ex_fire_sound, post_fix)
            self.sound_mgr.post_event(event_name, self._human_sound_id, pos + person_half_height)
        if self._is_continue_sound:
            if self._stop_fire_sound_delay_id:
                game3d.cancel_delay_exec(self._stop_fire_sound_delay_id)
            if not self._is_spell_wp and not self._is_laser_wp:
                self._stop_fire_sound_delay_id = game3d.delay_exec(500, self.fire_sound_time_out)
            self._play_fire_sound_auto(pos, bullet_num)
            if item_data and item_data['iType'] in self._silencer_list:
                sound_visible_type = const.SOUND_TYPE_SILENCER_FIRE
            else:
                sound_visible_type = const.SOUND_TYPE_FIRE
            if global_data.cam_lplayer and not global_data.cam_lplayer.ev_g_is_groupmate(self.unit_obj.id):
                global_data.emgr.sound_visible_add.emit(self.unit_obj, pos, sound_visible_type, sound_length_sqr)
        else:
            delay_time = (pos - global_data.sound_mgr.get_listener_pos()).length / sound_speed

            def callback():
                if self._human_sound_id:
                    if item_data and item_data['iType'] in self._silencer_list:
                        gun_option = 'silencer'
                        sound_visible_type = const.SOUND_TYPE_SILENCER_FIRE
                    else:
                        gun_option = 'single'
                        sound_visible_type = const.SOUND_TYPE_FIRE
                    self.sound_mgr.set_rtpc('bullet_count', bullet_num, self._human_sound_id)
                    if self._wp_nf:
                        post_fix = '1p' if self.is_1p else '3p'
                        event_name = '{}_{}'.format(self._fire_sound, post_fix)
                        self.sound_mgr.post_event(event_name, self._human_sound_id, pos + person_half_height)
                    else:
                        self.set_gun_option(gun_option)
                        self.sound_mgr.post_event(self.play_weapon_name, self._human_sound_id, pos + person_half_height)
                    if global_data.cam_lplayer and not global_data.cam_lplayer.ev_g_is_groupmate(self.unit_obj.id):
                        global_data.emgr.sound_visible_add.emit(self.unit_obj, pos, sound_visible_type, sound_length_sqr)

            game3d.delay_exec(delay_time * 1000, callback)

    def _play_fire_sound_auto(self, pos, bullet_num):
        if self._fire_auto_player_id:
            self.sound_mgr.set_rtpc('bullet_count', bullet_num, self._human_sound_id)
            return
        self.sound_mgr.set_rtpc('bullet_count', bullet_num, self._human_sound_id)
        if self._wp_nf:
            post_fix = 'start_1p' if self.is_1p else 'start_3p'
            event_name = '{}_{}'.format(self._fire_sound, post_fix)
            self._fire_auto_player_id = self.sound_mgr.post_event(event_name, self._human_sound_id, pos + person_half_height)
        else:
            self.set_gun_option('continuous')
            self._fire_auto_player_id = self.sound_mgr.post_event(self.play_weapon_name, self._human_sound_id, pos + person_half_height)
        if self._fire_auto_timer:
            global_data.game_mgr.unregister_logic_timer(self._fire_auto_timer)
        self._fire_auto_timer = global_data.game_mgr.register_logic_timer(self._updata_pos, interval=1, times=-1, mode=timer.LOGIC)

    def _stop_fire_sound_auto(self, *args):
        if self._fire_auto_timer:
            global_data.game_mgr.unregister_logic_timer(self._fire_auto_timer)
            self._fire_auto_timer = None
        else:
            return
        if self._cur_weapon:
            bullet_num = self._cur_weapon.get_bullet_num()
            self.sound_mgr.set_rtpc('bullet_count', bullet_num, self._human_sound_id)
        pos = self.ev_g_model_position()
        if not pos:
            pos = math3d.vector(0, 0, 0)
        if self._wp_nf:
            if self._is_laser_wp:
                if self._fire_auto_player_id:
                    self.sound_mgr.stop_playing_id(self._fire_auto_player_id)
                    self._fire_auto_player_id = None
            else:
                post_fix = 'stop_1p' if self.is_1p else 'stop_3p'
                event_name = '{}_{}'.format(self._fire_sound, post_fix)
                self.sound_mgr.post_event_non_optimization(event_name, self._human_sound_id, pos + person_half_height)
                self._fire_auto_player_id = None
        else:
            self.set_gun_option('end')
            self.sound_mgr.post_event(self.play_weapon_name, self._human_sound_id, pos + person_half_height)
            if self._fire_auto_player_id:
                self.sound_mgr.stop_playing_id(self._fire_auto_player_id)
                self._fire_auto_player_id = None
        return

    def fire_sound_time_out(self):
        if self._fire_auto_timer:
            global_data.game_mgr.unregister_logic_timer(self._fire_auto_timer)
            self._fire_auto_timer = None
        if self._fire_auto_player_id:
            self.sound_mgr.stop_playing_id(self._fire_auto_player_id)
            self._fire_auto_player_id = None
        self._stop_fire_sound_delay_id = None
        return

    def set_gun_option(self, gun_option):
        if self._gun_option != gun_option:
            self._gun_option = gun_option
            self.sound_mgr.set_switch('gun_option', self._gun_option, self._human_sound_id)

    def set_bc_rtpc(self, bullet_num):
        self.sound_mgr.set_rtpc('bullet_count', bullet_num, self._human_sound_id)

    def _player_fall_whistle(self, *args):
        if self.unit_obj == global_data.cam_lplayer:
            if self._fall_whistle_player_id:
                self.sound_mgr.stop_playing_id(self._fall_whistle_player_id)
                self._fall_whistle_player_id = None
            self.sound_mgr.set_switch('parachute', 'ch_fly1', self._human_sound_id)
            self._fall_whistle_player_id = self.sound_mgr.post_event('Play_parachute', self._human_sound_id)
            self.sound_mgr.set_switch('parachute', 'jump_out', self._human_sound_id)
            self.sound_mgr.post_event('Play_parachute', self._human_sound_id)
        return

    def _player_open_parachute(self, *args):
        if self._fall_whistle_player_id:
            self.sound_mgr.stop_playing_id(self._fall_whistle_player_id)
            self._fall_whistle_player_id = None
        if self.unit_obj == global_data.cam_lplayer:
            self.sound_mgr.set_switch('parachute', 'aircraft_fly', self._human_sound_id)
            self._fall_whistle_player_id = self.sound_mgr.post_event('Play_parachute', self._human_sound_id)
        if self.unit_obj == global_data.cam_lplayer:
            self.sound_mgr.set_switch('parachute', 'aircraft_open', self._human_sound_id)
            self.sound_mgr.post_event('Play_parachute', self._human_sound_id)
        return

    def play_mecha_land(self):
        player_pos = self.get_cam_player_pos()
        if not player_pos:
            return
        pos = self.ev_g_model_position()
        if not pos:
            return
        vect = pos - player_pos
        sound_length_sqr = vect.length_sqr
        listen_dis_sqr = global_data.cam_lplayer.ev_g_addition_effect(const.WWISE_FOOTSTEP_MAX_DIS_SQR, factor_attrs=[attr_const.ATTR_LISTEN_RANGE_FACTOR])
        if sound_length_sqr > listen_dis_sqr:
            return
        offset = math3d.vector(0, -10.0 * const.NEOX_UNIT_SCALE, 0)
        start_pos = pos + offset
        end_pos = pos - offset
        result = self._scene.scene_col.hit_by_ray(start_pos, end_pos, 0, collision_const.GROUP_CHARACTER_INCLUDE, collision_const.GROUP_CHARACTER_INCLUDE, collision.INCLUDE_FILTER, False)
        material_type = '_normal'
        if result[0]:
            cobj = result[5]
            group_id = cobj.group
            is_chunk_mesh = scene_utils.is_chunk_mesh(cobj)
            if is_chunk_mesh or group_id == collision_const.TERRAIN_GROUP:
                material_index = self._scene.get_scene_info_2d(pos.x, pos.z)
                if material_index == MTL_WATER or material_index == MTL_DEEP_WATER:
                    material_type = '_water'
            elif group_id == COL_WATER:
                material_type = '_water'
            if self._footstep_material_type != material_type:
                self._footstep_material_type = material_type
        if not self._human_sound_id:
            return
        sound_name = 'mecha8002_jump_down_hurt' + material_type
        self.sound_mgr.set_switch('parachute', sound_name, self._human_sound_id)
        self.sound_mgr.post_event('Play_parachute', self._human_sound_id, pos)

    def _player_land(self, *args):
        mecha_model = self.ev_g_parachute_mecha_model()
        if mecha_model:
            if self.unit_obj == global_data.cam_lplayer:
                self.play_mecha_land()
        elif self.unit_obj == global_data.cam_lplayer:
            self.sound_mgr.set_switch('parachute', 'aircraft_close', self._human_sound_id)
            self.sound_mgr.post_event('Play_parachute', self._human_sound_id)
        if self._fall_whistle_player_id:
            self.sound_mgr.stop_playing_id(self._fall_whistle_player_id)
            self._fall_whistle_player_id = None
        return

    def _player_move_parachute(self, *args):
        pass

    def _on_skate(self, *args):
        pos = self.ev_g_model_position()
        if pos:
            self.sound_mgr.set_switch('skateboard', 'skateboard_on', self._human_sound_id)
            self.sound_mgr.post_event('Play_skateboard', self._human_sound_id, pos)
            self.sound_mgr.set_switch('skateboard', 'skateboard_idle', self._human_sound_id)
            self._skate_player_id = self.sound_mgr.post_event_non_optimization('Play_skateboard', self._human_sound_id, pos)

    def _off_skate(self, *args):
        pos = self.ev_g_model_position()
        if pos:
            self.sound_mgr.set_switch('skateboard', 'skateboard_off', self._human_sound_id)
            self.sound_mgr.post_event('Play_skateboard', self._human_sound_id, pos)
        if self._skate_player_id:
            self.sound_mgr.stop_playing_id(self._skate_player_id)
            self._skate_player_id = None
        return

    def _jump_skate(self, *args):
        pos = self.ev_g_model_position()
        if pos and not self._skate_jump_land_tag:
            self.sound_mgr.set_switch('skateboard', 'skateboard_jump', self._human_sound_id)
            self.sound_mgr.post_event('Play_skateboard', self._human_sound_id, pos)
            self._skate_jump_land_tag = True

    def _land_skate(self, *args):
        pos = self.ev_g_model_position()
        if pos and self._skate_jump_land_tag:
            self.sound_mgr.set_switch('skateboard', 'skateboard_landing', self._human_sound_id)
            self.sound_mgr.post_event('Play_skateboard', self._human_sound_id, pos)
            self._skate_jump_land_tag = False

    def _stop_skate(self, *args):
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast_utils.E_ACTION_SKATE_MOVE_STOP, tuple(args)], False)
        if self._skate_timer:
            global_data.game_mgr.unregister_logic_timer(self._skate_timer)
            self._skate_timer = None
        if self._skate_player_id:
            self.sound_mgr.stop_playing_id(self._skate_player_id)
            self._skate_player_id = None
        pos = self.ev_g_model_position()
        if pos:
            self.sound_mgr.set_switch('skateboard', 'skateboard_idle', self._human_sound_id)
            self._skate_player_id = self.sound_mgr.post_event_non_optimization('Play_skateboard', self._human_sound_id, pos)
        return

    def _change_dir_skate(self, *args):
        pos = self.ev_g_model_position()
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast_utils.E_SKATE_CHANGE_DIR_SOUND, tuple(args)], False)
        if not self._skate_timer:
            if self._skate_player_id:
                self.sound_mgr.stop_playing_id(self._skate_player_id)
                self._skate_player_id = None
            if pos:
                self.sound_mgr.set_switch('skateboard', 'skateboard_run', self._human_sound_id)
                self._skate_player_id = self.sound_mgr.post_event_non_optimization('Play_skateboard', self._human_sound_id, pos)
            self._skate_timer = global_data.game_mgr.register_logic_timer(self._updata_pos_skate, interval=1, times=-1, mode=timer.LOGIC)
        return

    def _roll_sound(self, *args):
        pos = self.ev_g_model_position()
        if pos:
            self.sound_mgr.set_switch('character_action', 'ch_roll', self._human_sound_id)
            self.sound_mgr.post_event('Play_character_action', self._human_sound_id, pos)
            self.add_action_sound_visible(pos)

    def _player_climb(self, *args):
        pos = self.ev_g_model_position()
        if pos:
            self.add_action_sound_visible(pos)

    def _rush_sound(self, *args):
        pos = self.ev_g_model_position()
        if pos:
            self.sound_mgr.set_switch('character_action', 'ch_sprint', self._human_sound_id)
            self.sound_mgr.post_event('Play_character_action', self._human_sound_id, pos)
            self.add_action_sound_visible(pos)

    def _play_jump_water(self, *args):
        now = time.time()
        if now - self.play_water_soundt_time < 1.0:
            return
        pos = self.ev_g_model_position()
        if pos:
            self.sound_mgr.set_switch('character_action', 'ch_jump_water', self._human_sound_id)
            self.sound_mgr.post_event('Play_character_action', self._human_sound_id, pos)
            self.add_action_sound_visible(pos)
            self.play_water_soundt_time = now

    def _enter_states(self, new_state):
        if new_state == status_config.ST_SWIM:
            now = time.time()
            if now - self.play_water_soundt_time < 1.0:
                return
            pos = self.ev_g_model_position()
            if pos:
                self.sound_mgr.set_switch('character_action', 'ch_into_water', self._human_sound_id)
                self.sound_mgr.post_event('Play_character_action', self._human_sound_id, pos)
                self.add_action_sound_visible(pos)
                self.play_water_soundt_time = now

    def _leave_states(self, leave_state, new_state=None):
        if leave_state == status_config.ST_SWIM:
            now = time.time()
            if now - self.play_water_soundt_time < 1.0:
                return
            pos = self.ev_g_model_position()
            if pos:
                self.sound_mgr.set_switch('character_action', 'ch_on_water', self._human_sound_id)
                self.sound_mgr.post_event('Play_character_action', self._human_sound_id, pos)
                self.add_action_sound_visible(pos)
                self.play_water_soundt_time = now

    def _player_jump(self, stage):
        pos = self.ev_g_model_position()
        if not pos:
            return
        jump_name = 'ch_jump' if stage == 1 else 'ch_jump2'
        self.sound_mgr.set_switch('character_action', jump_name, self._human_sound_id)
        self.sound_mgr.post_event('Play_character_action', self._human_sound_id, pos)
        self.add_action_sound_visible(pos)

    def _play_change_weapon(self, *args):
        if args[0] == 0:
            return
        else:
            pos = self.ev_g_model_position()
            if not pos:
                return
            wp = self.sd.ref_wp_bar_cur_weapon
            if wp:
                event = wp.get_key_config_value('cSwitchSound', None) if 1 else None
                event = event or 'Play_switch'
            else:
                post_fix = '1p' if self.is_1p else '3p'
                event = '{}_{}'.format(event, post_fix)
            pos -= math3d.vector(0, 9.0, 0)
            self.sound_mgr.post_event(event, self._human_sound_id, pos + person_half_height)
            return

    def _play_pick_up(self, item, pos=None):
        pick_sound = confmgr.get('item', str(item), 'pick_sound', default=None)
        if pick_sound:
            if self.unit_obj.ev_g_in_mecha():
                pos = global_data.sound_mgr.get_listener_pos()
            else:
                pos = self.ev_g_model_position()
            if pos:
                global_data.sound_mgr.play_sound('Play_get_equipment', pos, ('get_equipment', pick_sound))
        return

    def _play_throw_item(self, *args):
        pos = self.ev_g_model_position()
        if pos:
            global_data.sound_mgr.play_sound('Play_get_equipment', pos, ('get_equipment',
                                                                         'throw'))

    def _play_equip_item(self, *args):
        if self.unit_obj != global_data.cam_lplayer:
            return
        pos = self.ev_g_model_position()
        if pos:
            global_data.sound_mgr.play_sound('Play_ui_click', pos, ('ui_click', 'equipment'))

    def _play_wait_throw(self, *args):
        pos = self.ev_g_model_position()
        if pos:
            self.sound_mgr.set_switch('throw_stand', 'throw_stand_01', self._human_sound_id)
            self.sound_mgr.post_event('Play_throw_stand', self._human_sound_id, pos + person_half_height)

    def _play_throw(self, *args):
        pos = self.ev_g_model_position()
        if pos:
            self.sound_mgr.set_switch('throw_stand', 'throw_stand_03', self._human_sound_id)
            self.sound_mgr.post_event('Play_throw_stand', self._human_sound_id, pos + person_half_height)

    def _updata_pos(self):
        pos = self.ev_g_model_position()
        if pos:
            self.sound_mgr.set_position(self._human_sound_id, pos + person_half_height)

    def _updata_pos_skate(self):
        pos = self.ev_g_model_position()
        if pos:
            self.sound_mgr.set_position(self._human_sound_id, pos + person_half_height)
            player_pos = self.get_cam_player_pos()
            if not player_pos:
                return
            vect = pos - player_pos
            sound_length_sqr = vect.length_sqr
            listen_dis_sqr = global_data.cam_lplayer.ev_g_addition_effect(const.WWISE_FOOTSTEP_MAX_DIS_SQR, factor_attrs=[attr_const.ATTR_LISTEN_RANGE_FACTOR])
            if sound_length_sqr > listen_dis_sqr:
                return
            if global_data.cam_lplayer and not global_data.cam_lplayer.ev_g_is_groupmate(self.unit_obj.id):
                global_data.emgr.sound_visible_add.emit(self.unit_obj, pos, const.SOUND_TYPE_SKATE, sound_length_sqr)
        if not self.unit_obj.ev_g_get_state(status_config.ST_SKATE):
            if self._skate_timer:
                global_data.game_mgr.unregister_logic_timer(self._skate_timer)
                self._skate_timer = None
            if self._skate_player_id:
                self.sound_mgr.stop_playing_id(self._skate_player_id)
                self._skate_player_id = None
        return

    def _play_on_used_sound(self, item_id, sound_name):
        if sound_name:
            self.sound_mgr.post_event_2d_non_opt(sound_name, None)
        return

    def _play_sound_bullet_hit(self, start_pos, end_pos, scene_pellet, shoot_mask, ext_dict=None):
        from logic.gcommon.common_const.collision_const import GROUP_CAN_SHOOT
        direction = end_pos - start_pos
        if direction.is_zero:
            direction = math3d.vector(0, 0, 1)
        else:
            direction.normalize()
        chack_start = end_pos - direction * 5.0
        chack_end = end_pos + direction * 15.0
        result = self._scene.scene_col.hit_by_ray(chack_start, chack_end, 0, GROUP_CAN_SHOOT, GROUP_CAN_SHOOT, collision.INCLUDE_FILTER, False)
        if result[0]:
            cobj = result[5]
            is_chunk_mesh = scene_utils.is_chunk_mesh(cobj)
            material_type = None
            if not is_chunk_mesh:
                material_type = collision_material_to_sound.get(cobj.group, None)
            if not material_type:
                material_index = self._scene.get_scene_info_2d(end_pos.x, end_pos.z)
                material_type = material_dic.get(material_index, None)
                if not material_type:
                    material_type = 'dirt'
            self.sound_mgr.set_switch('bullet_hit_material', material_type, self._hit_sound_id)
            self.sound_mgr.post_event('Play_bullet_hit', self._hit_sound_id, end_pos)
        if self._is_fly_sound and self.unit_obj != global_data.cam_lplayer:
            vect1 = end_pos - start_pos
            distance = vect1.length
            if distance < 1 * const.NEOX_UNIT_SCALE:
                return
            vect1.normalize()
            vect2 = self.sound_mgr.get_listener_pos() - start_pos
            distance2 = vect1.x * vect2.x + vect1.y * vect2.y + vect1.z * vect2.z
            if distance2 < 1 * const.NEOX_UNIT_SCALE:
                return
            if distance2 < distance:
                pos = start_pos + vect1 * distance2
            else:
                pos = end_pos
            if (pos - self.sound_mgr.get_listener_pos()).length_sqr > (5 * const.NEOX_UNIT_SCALE) ** 2:
                return
            self.sound_mgr.set_switch('ammo', 'bullet_fly', self._fly_sound_id)
            self.sound_mgr.post_event('Play_ammo', self._fly_sound_id, pos)
            if global_data.cam_lplayer and not global_data.cam_lplayer.ev_g_is_groupmate(self.unit_obj.id):
                global_data.emgr.play_tips_voice.emit('tips_02', entity_id=self.unit_obj.id)
        return

    def _play_sound_hit_body(self, begin_pos, hit_pos, shot_type, **kwargs):
        import random
        dmg_parts = kwargs.get('dmg_parts', {})
        if self.unit_obj == global_data.cam_lplayer:
            if kwargs.get('triger_is_mecha', False):
                global_data.sound_mgr.play_sound_2d('Play_ui_notice', ('ui_notice',
                                                                       'human_body_hit_by_mecha'))
            else:
                global_data.sound_mgr.play_sound_2d('Play_ui_notice', ('ui_notice',
                                                                       'human_body_hit_by_bullet'))
        is_hit_shield = bool(dmg_parts and dmg_parts.get(HIT_PART_SHIELD))
        if is_hit_shield:
            self.sound_mgr.set_switch('bullet_hit_material', 'metal', self._hit_sound_id)
            self.sound_mgr.post_event('Play_bullet_hit', self._hit_sound_id, hit_pos)
        elif random.randint(0, 99) < 30:
            if self._role_sex == const.SEX_MALE:
                sound_name = 'men_head_shot'
            else:
                sound_name = 'girl_head_shot'
            self.sound_mgr.set_switch('ammo', sound_name, self._human_sound_id)
            self.sound_mgr.post_event('Play_ammo', self._human_sound_id, hit_pos)
        else:
            sound_path = sound_utils.get_hitted_sound(shot_type, 'human')
            if sound_path:
                sound_utils.play_sound(sound_path, self._hit_sound_id, hit_pos)
            else:
                sound_utils.play_sound(['Play_bullet_hit', ['bullet_hit_material', 'body_hit']], self._hit_sound_id, hit_pos)

    def _play_sound_bomb_hit(self, hit_pos, wp_id, trigger_is_self, dmg_parts):
        if trigger_is_self:
            is_head = bool(dmg_parts and HIT_PART_HEAD in dmg_parts)
            sound_utils.play_hit_sound_2d(wp_id, True, is_head)
        sound_path = sound_utils.get_hitted_sound(wp_id, 'human')
        if sound_path:
            sound_utils.play_sound(sound_path, self._hit_sound_id, hit_pos)

    def _play_sync_hit_sound(self, hit_pos, event):
        self.sound_mgr.post_event(event, self._hit_sound_id, hit_pos)

    def _play_sound_skill_hit(self, skill_id, trigger_is_self):
        skill_data = confmgr.get('skill_conf', str(skill_id), default={})
        if trigger_is_self:
            ext_info = skill_data.get('ext_info', {})
            play_tag = ext_info.get('play_hit_sound_2d', 0)
            if play_tag:
                sound_utils.play_hit_sound_2d(-1, True, False)

    def _play_sound_lightning_21_hit(self):
        self.sound_mgr.post_event('universal_skill_lightning', self._hit_sound_id, self.ev_g_position())

    def _play_sound_buff_hit(self, buff_id, trigger_is_self):
        buff_data = confmgr.get('c_buff_data', str(buff_id), default={})
        conf = buff_data.get('ExtInfo', {})
        if trigger_is_self:
            play_tag = conf.get('play_hit_sound_2d', 0)
            if play_tag:
                sound_utils.play_hit_sound_2d(-1, False, False)

    def _play_reload_nf(self, *args):
        if self._wp_nf:
            pos = self.ev_g_model_position()
            if pos:
                post_fix = '1p' if self.is_1p else '3p'
                event_name = '{}_{}'.format(self._reload_sound, post_fix)
                self.sound_mgr.post_event_non_optimization(event_name, self._human_sound_id, pos + person_half_height)

    def _play_reload(self, last_time, times, *args):
        pass

    def _on_cancel_reload(self, *args):
        if self._reload_callback_handler:
            game3d.cancel_delay_exec(self._reload_callback_handler)

    def _on_use_prop(self, *args):
        if not self._is_clien_player:
            return
        else:
            sound_name = confmgr.get('item_use', str(args[0]), 'cUseSound', default=None)
            if sound_name:
                if self.unit_obj.ev_g_in_mecha():
                    pos = global_data.sound_mgr.get_listener_pos()
                else:
                    pos = self.ev_g_model_position()
                if pos:
                    self.sound_mgr.set_switch('props_option', sound_name, self._human_sound_id)
                    self._use_prop_play_id = self.sound_mgr.post_event('Play_props', self._human_sound_id, pos + person_half_height)
            return

    def _on_cancel_use_item(self, *args):
        if self._use_prop_play_id:
            self.sound_mgr.stop_playing_id(self._use_prop_play_id)
            self._use_prop_play_id = None
        return

    def _on_super_jump(self, *args):
        pos = self.ev_g_model_position()
        if pos:
            self.sound_mgr.set_switch('props_option', 'launcher', self._human_sound_id)
            self.sound_mgr.post_event('Play_props', self._human_sound_id, pos)

    def _on_start_use_building(self, building_no):
        pos = self.ev_g_model_position()
        if pos:
            self.sound_mgr.set_switch('character', BUILDING_SOUND_MAP[building_no][0], self._human_sound_id)
            self.sound_mgr.post_event('Play_character', self._human_sound_id, pos)

    def _on_use_building_success(self, building_no):
        pos = self.ev_g_model_position()
        if pos:
            self.sound_mgr.set_switch('character', BUILDING_SOUND_MAP[building_no][1], self._human_sound_id)
            self.sound_mgr.post_event('Play_character', self._human_sound_id, pos)

    def _on_get_supply(self, item_id):
        pick_sound = confmgr.get('item', str(item_id), 'pick_sound', default=None)
        if not pick_sound:
            return
        else:
            pos = self.ev_g_model_position()
            if pos:
                self.sound_mgr.set_switch('get_equipment', pick_sound, self._human_sound_id)
                self.sound_mgr.post_event('Play_get_equipment', self._human_sound_id, pos)
            return

    def _play_open_aim(self, *args):
        if self.unit_obj == global_data.cam_lplayer:
            global_data.sound_mgr.play_sound(self.play_weapon_name, None, ('gun', 'pulse_gun'), ('gun_option',
                                                                                                 'open_sight'))
        return

    def _play_close_aim(self, *args):
        if self.unit_obj == global_data.cam_lplayer:
            global_data.sound_mgr.play_sound(self.play_weapon_name, None, ('gun', 'pulse_gun'), ('gun_option',
                                                                                                 'close_sight'))
        return

    def add_action_sound_visible(self, pos):
        player_pos = self.get_cam_player_pos()
        if not player_pos:
            return
        else:
            vect = pos - player_pos
            sound_length_sqr = vect.length_sqr
            listen_dis_sqr = global_data.cam_lplayer.ev_g_add_effection(const.WWISE_FOOTSTEP_MAX_DIS_SQR, factor_attrs=[attr_const.ATTR_LISTEN_RANGE_FACTOR])
            if listen_dis_sqr is not None and sound_length_sqr > listen_dis_sqr:
                return
            if global_data.cam_lplayer and not global_data.cam_lplayer.ev_g_is_groupmate(self.unit_obj.id):
                global_data.emgr.sound_visible_add.emit(self.unit_obj, pos, const.SOUND_TYPE_FOOTSTEP, sound_length_sqr)
            return

    def _on_death(self, *args):
        pos = self.ev_g_model_position()
        if pos:
            self.sound_mgr.set_switch('ui_notice', 'kill_gone', self._hit_sound_id)
            self.sound_mgr.post_event('Play_ui_notice', self._hit_sound_id, pos)
        self.stop_run_sound()
        if self.unit_obj == global_data.cam_lplayer and global_data.sound_mgr._cur_music_name == 'flight':
            global_data.sound_mgr.play_music('stop')

    def _on_defeated(self, *args):
        self.stop_run_sound()

    def set_open_sound_tip_cd(self, *args):
        from logic.gcommon.common_const.ui_operation_const import SOUND_TIP_CD
        self.tip_cd_tag = global_data.player.get_setting(SOUND_TIP_CD)

    def _play_tip_cd_sound(self):
        if self.is_1p and self.tip_cd_tag:
            global_data.sound_mgr.post_event_2d_with_opt('Play_ui_tip_cd', None, 0.66)
        return

    def change_client_env_type(self):
        if self._is_clien_player:
            if self._env_type != self.sound_mgr.get_listener_env_type():
                self.sound_mgr.set_listener_env_type(self._env_type)

    def get_cam_player_pos(self):
        cam_lplayer = global_data.cam_lplayer
        if not cam_lplayer:
            return None
        else:
            if cam_lplayer.ev_g_in_mecha():
                enable_mecha_or_player = cam_lplayer.ev_g_control_target().logic if 1 else cam_lplayer
                return enable_mecha_or_player or None
            return enable_mecha_or_player.ev_g_model_position()

    def battle_end(self, *args):
        if self.unit_obj == global_data.cam_lctarget:
            self.stop_run_sound()

    def stop_run_sound(self):
        if self._fall_whistle_player_id:
            self.sound_mgr.stop_playing_id(self._fall_whistle_player_id)
            self._fall_whistle_player_id = None
        if self._skate_player_id:
            self.sound_mgr.stop_playing_id(self._skate_player_id)
            self._skate_player_id = None
        if self._fire_auto_player_id:
            self.sound_mgr.stop_playing_id(self._fire_auto_player_id)
            self._fire_auto_player_id = None
        if self._skate_timer:
            global_data.game_mgr.unregister_logic_timer(self._skate_timer)
            self._skate_timer = None
        if self._fire_auto_timer:
            global_data.game_mgr.unregister_logic_timer(self._fire_auto_timer)
            self._fire_auto_timer = None
        return

    def destroy(self):
        self.stop_run_sound()
        if self.sound_mgr:
            self.sound_mgr.unregister_game_obj(self._human_sound_id)
            self.sound_mgr.unregister_game_obj(self._hit_sound_id)
            self.sound_mgr.unregister_game_obj(self._fly_sound_id)
            self.sound_mgr = None
        self._human_sound_id = None
        self._hit_sound_id = None
        self._fly_sound_id = None
        if self.indoor_timer:
            global_data.game_mgr.unregister_logic_timer(self.indoor_timer)
            self.indoor_timer = None
        if self.is_1p:
            global_data.emgr.player_open_sound_tip_cd -= self.set_open_sound_tip_cd
        super(ComSound, self).destroy()
        return