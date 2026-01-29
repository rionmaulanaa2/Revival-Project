# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_human_appearance/ComWeaponAnimation.py
from __future__ import absolute_import
from __future__ import print_function
from six.moves import range
from logic.gcommon.component.UnitCom import UnitCom
from common.animate import animator
import logic.gcommon.common_const.animation_const as animation_const
import world
import data.weapon_action_config as weapon_action_config
from common.cfg import confmgr
from logic.gcommon.const import SEX_MALE, SEX_FEMALE
import logic.gcommon.cdata.status_config as status_config
ROOT_NODE_NAME = 'weapon'
SINGLE_NODE_NAME = 'single'
BLEND_NODE_NAME = 'blend'
BEGIN_BLEND_EVENT = 'begin_blend'
BEGIN_SINGLE_EVENT = 'begin_single'
DEFAULT_ANIM_NAME = 'idle'

class ComWeaponAnimation(UnitCom):
    SINGLE_WEAPON_ACTION_TYPE = set([animation_const.WEAPON_TYPE_SHIELD, animation_const.WEAPON_TYPE_FLAMER, animation_const.WEAPON_TYPE_BAZOOKA, animation_const.WEAPON_TYPE_BLAST])
    LACK_ANIM_USE_IDLE_WEAPON = set([animation_const.WEAPON_TYPE_LMG])
    HEAVY_WEAPON_ACTION_TYPE = set([animation_const.WEAPON_TYPE_SHIELD, animation_const.WEAPON_TYPE_FLAMER, animation_const.WEAPON_TYPE_BAZOOKA,
     animation_const.WEAPON_TYPE_GRENADE, animation_const.WEAPON_TYPE_GRENADE, animation_const.WEAPON_TYPE_SNIPER_RIFLE,
     animation_const.WEAPON_TYPE_LMG, animation_const.WEAPON_TYPE_BLAST, animation_const.WEAPON_TYPE_M4, animation_const.WEAPON_TYPE_MP5, animation_const.WEAPON_TYPE_DJFD])
    SEX_POSTFIX = {SEX_MALE: '_man',SEX_FEMALE: '_woman'}
    SEX_ANIMATION = {animation_const.WEAPON_TYPE_SNIPER_RIFLE: [
                                                'snipe_change', 'snipe_load', 'snipe_reload', 'snipe_aim'],
       animation_const.WEAPON_TYPE_LMG: [
                                       'lmg_change', 'lmg_shoot', 'lmg_reload'],
       animation_const.WEAPON_TYPE_BLAST: [
                                         'c_blast_reload', 's_blast_reload'],
       animation_const.WEAPON_TYPE_DJFD: [
                                        's_djfd_reload', 's_bazooka_stop', 'skate_djfd_reload', 'c_djfd_reload', 'c_bazooka_stop', 'skate_bazooka_stop']
       }
    WEAPON_ANIMATION_SMOOTH_DURATION = {animation_const.WEAPON_TYPE_MP5: 0.0
       }
    PRELOAD_INFO = {}
    BIND_EVENT = {'E_CHANGE_WEAPON_MODEL': 'change_weapon',
       'E_DESTROY_WEAPON_MODEL': 'destroy_weapon',
       'E_CHANGE_WEAPON_ANIMATION': 'change_weapon_animation',
       'E_CHANGE_WEAPON_IDLE': 'change_weapon_idle',
       'E_CHARACTER_ATTR': 'change_character_attr',
       'E_CHANGE_ANIM_MOVE_DIR': 'set_dir_x_y',
       'E_TEST_WEAPON_ANIMATION': 'test_weapon_animation',
       'E_SWITCHED_WP_MODE': 'switch_gun_mode'
       }

    def __init__(self):
        super(ComWeaponAnimation, self).__init__()
        self._left_weapon_animator = None
        self._right_weapon_animator = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComWeaponAnimation, self).init_from_dict(unit_obj, bdict)

    def destroy(self):
        if self._left_weapon_animator:
            self._left_weapon_animator.destroy()
            self._left_weapon_animator = None
        if self._right_weapon_animator:
            self._right_weapon_animator.destroy()
            self._right_weapon_animator = None
        super(ComWeaponAnimation, self).destroy()
        return

    def change_character_attr(self, name, *arg):
        if name == 'animator_info':
            print(('test--ComWeaponAnimation.animator_info--self.unit_obj =', self.unit_obj))
            only_active = arg[0]
            is_have_animator = False
            if self._left_weapon_animator:
                left_hand_model = self.sd.ref_left_hand_weapon_model
                left_model_file_list = self.ev_g_main_and_sub_model(left_hand_model)
                print(('test--ComWeaponAnimation.left_weapon_animator--left_model_file_list =', left_model_file_list, '--xml_path =', self._left_weapon_animator.GetXmlFile()))
                self._left_weapon_animator.print_info(active=only_active)
            if self._right_weapon_animator:
                right_weapon_model = self.sd.ref_hand_weapon_model
                right_model_file_list = self.ev_g_main_and_sub_model(right_weapon_model)
                print(('test--ComWeaponAnimation.right_weapon_animator--right_model_file_list =', right_model_file_list, '--xml_path =', self._right_weapon_animator.GetXmlFile()))
                self._right_weapon_animator.print_info(active=only_active)
            if not is_have_animator:
                left_hand_model = self.sd.ref_left_hand_weapon_model
                if left_hand_model:
                    print(('test--ComWeaponAnimation.left_hand_model--cur_anim_name =', left_hand_model.cur_anim_name))
                right_weapon_model = self.sd.ref_hand_weapon_model
                if right_weapon_model:
                    print(('test--ComWeaponAnimation.right_weapon_model--cur_anim_name =', right_weapon_model.cur_anim_name))

    def switch_gun_mode(self, *args):
        self.play_gun_default_animation()

    def play_gun_default_animation(self):
        action_id = self.ev_g_weapon_action_id()
        if action_id != animation_const.WEAPON_TYPE_FROZEN:
            return
        weapon_obj = self.sd.ref_wp_bar_cur_weapon
        if not weapon_obj:
            return
        is_ball_mode = weapon_obj.is_in_multi_mode()
        anim_name = 'idle_fog'
        if is_ball_mode:
            anim_name = 'idle_ball'
        right_weapon_model = self.sd.ref_hand_weapon_model
        if right_weapon_model:
            right_weapon_model.play_animation(anim_name)
        left_hand_model = self.sd.ref_left_hand_weapon_model
        if left_hand_model:
            left_hand_model.play_animation(anim_name)

    def change_weapon(self, weapon_model, hand_pos, weapon_id):
        from logic.gcommon.common_const.character_anim_const import UP_BODY
        weapon_obj = self.sd.ref_wp_bar_cur_weapon
        if not weapon_obj:
            return
        action_id = animation_const.WEAPON_TYPE_EMPTY_HAND
        if weapon_id:
            action_id = confmgr.get('firearm_res_config', str(weapon_id), 'iActionType')
        if action_id in self.WEAPON_ANIMATION_SMOOTH_DURATION:
            self.send_event('E_SET_SMOOTH_DURATION', UP_BODY, self.WEAPON_ANIMATION_SMOOTH_DURATION[action_id])
        self.play_gun_default_animation()
        if action_id not in self.HEAVY_WEAPON_ACTION_TYPE:
            return
        diff_pos_preload_info = ComWeaponAnimation.PRELOAD_INFO.setdefault(action_id, {})
        is_preload = diff_pos_preload_info.setdefault(hand_pos, False)
        if not is_preload:
            diff_pos_preload_info[hand_pos] = True
            if global_data.enable_cache_animation:
                clip_list = weapon_model.get_anim_names()
                for clip_name in clip_list:
                    weapon_model.cache_animation(clip_name, world.CACHE_ANIM_ALWAYS)

        xml_path = 'animator_conf/weapon.xml'
        if hand_pos == animation_const.WEAPON_POS_LEFT:
            try:
                self._left_weapon_animator = animator.Animator(weapon_model, xml_path, self.unit_obj)
                self._left_weapon_animator.Load(False)
            except Exception as e:
                self.get_weapon_error_desc()
                import traceback
                traceback.print_stack()

            self.on_load_animator_complete(self._left_weapon_animator)
        elif hand_pos == animation_const.WEAPON_POS_RIGHT:
            try:
                self._right_weapon_animator = animator.Animator(weapon_model, xml_path, self.unit_obj)
                self._right_weapon_animator.Load(False)
            except Exception as e:
                self.get_weapon_error_desc()
                import traceback
                traceback.print_stack()

            self.on_load_animator_complete(self._right_weapon_animator)

    def get_weapon_error_desc(self):
        weapon_obj = self.sd.ref_wp_bar_cur_weapon
        if not weapon_obj:
            return
        else:
            from logic.gcommon.item.item_const import FASHION_POS_SUIT
            from logic.gutils.mode_utils import get_mapped_res_path
            from logic.gutils import dress_utils
            weapon_id = weapon_obj.get_item_id()
            weapon_res_def = confmgr.get('firearm_res_config', str(weapon_id))
            left_res = weapon_res_def['cResLeft']
            right_res = get_mapped_res_path(weapon_res_def['cRes'])
            fashion = weapon_obj.get_fashion()
            fashion_id = fashion.get(FASHION_POS_SUIT, None)
            if fashion_id is not None:
                tmp_right_res, tmp_left_res = dress_utils.get_weapon_skin_res(fashion_id)
                if tmp_left_res is not None:
                    left_res = tmp_left_res
                if tmp_right_res is not None:
                    right_res = tmp_right_res
            print(('test--get_weapon_error_desc--weapon_id =', weapon_id, '--left_res =', left_res, '--right_res =', right_res))
            return

    def on_load_animator_complete(self, animator):
        pass

    def destroy_weapon(self, hand_pos):
        if hand_pos == animation_const.WEAPON_POS_LEFT:
            if self._left_weapon_animator:
                self._left_weapon_animator.destroy()
                self._left_weapon_animator = None
        elif hand_pos == animation_const.WEAPON_POS_RIGHT:
            if self._right_weapon_animator:
                self._right_weapon_animator.destroy()
                self._right_weapon_animator = None
        return

    def test_weapon_animation(self, key=None):
        if key is None:
            key = '7,s_lmg_reload'
        clip_list = self.ev_g_convert_str_to_anim_list(key)
        self.change_weapon_animation(clip_list, False, True)
        dir_x = 0.1
        dir_y = 0.3
        self.set_dir_x_y(dir_x, dir_y)
        return

    def change_weapon_animation(self, clip_list, is_keep_phase, loop=False, time_scale=1, blend_time=0.2):
        action_id = self.ev_g_weapon_action_id()
        weapon_obj = self.sd.ref_wp_bar_cur_weapon
        weapon_id = 0
        if weapon_obj:
            weapon_id = weapon_obj.get_item_id()
        if not clip_list:
            print('test--weapon_id =', weapon_id, '--clip_list =', clip_list, '--action_id =', action_id)
            import traceback
            traceback.print_stack()
            return
        if action_id in self.SINGLE_WEAPON_ACTION_TYPE:
            clip_list = [
             clip_list[-1]]
        sex_anim = False
        clip_name = clip_list[-1]
        if clip_name == 's_ak_stop':
            return
        anims = self.SEX_ANIMATION.get(action_id, [])
        for ainm in anims:
            if ainm in clip_name:
                sex_anim = True

        if sex_anim:
            sex = self.ev_g_sex()
            action_postfix = self.SEX_POSTFIX.get(sex, '')
            for index in range(len(clip_list)):
                clip_name = clip_list[index]
                clip_list[index] = clip_name + action_postfix

        right_weapon_model = self.sd.ref_hand_weapon_model
        if not right_weapon_model:
            return
        if clip_list[-1].startswith(animation_const.CROUCH_REPLACE_PREFIX) and not right_weapon_model.has_anim(clip_list[-1]):
            for index in range(len(clip_list)):
                clip_list[index] = clip_list[index].replace(animation_const.CROUCH_REPLACE_PREFIX, animation_const.STAND_REPLACE_PREFIX, 1)

        if not right_weapon_model.has_anim(clip_list[-1]):
            lack_anim_use_idle = action_id in self.LACK_ANIM_USE_IDLE_WEAPON
            if lack_anim_use_idle:
                clip_list = [
                 DEFAULT_ANIM_NAME]
            else:
                self.send_event('E_CHANGE_ZERO_WEAPON_ANIMATION', animation_const.WEAPON_POS_RIGHT, clip_list, loop=loop, time_scale=time_scale, blend_time=blend_time)
                return
        if self.ev_g_get_state(status_config.ST_SKATE):
            skate_clip_list = []
            for one_clip_name in clip_list:
                one_skate_clip_name = 'skate_' + one_clip_name
                if right_weapon_model.has_anim(one_skate_clip_name):
                    skate_clip_list.append(one_skate_clip_name)
                if len(skate_clip_list) == len(clip_list):
                    clip_list = skate_clip_list

        if self._left_weapon_animator:
            left_clip_list = clip_list
            if self.ev_g_get_state(status_config.ST_SKATE):
                left_hand_model = self.sd.ref_left_hand_weapon_model
                left_clip_list = self.get_skate_clip_list(left_hand_model, left_clip_list)
            self.change_one_weapon_animation(self._left_weapon_animator, left_clip_list, is_keep_phase, loop, time_scale, blend_time)
            self.send_event('E_CHANGE_ONE_WEAPON_ANIMATION', animation_const.WEAPON_POS_LEFT, left_clip_list, loop=loop, time_scale=time_scale, blend_time=blend_time)
        if self._right_weapon_animator:
            right_clip_list = clip_list
            if self.ev_g_get_state(status_config.ST_SKATE):
                right_clip_list = self.get_skate_clip_list(right_weapon_model, right_clip_list)
            self.change_one_weapon_animation(self._right_weapon_animator, right_clip_list, is_keep_phase, loop, time_scale, blend_time)
            self.send_event('E_CHANGE_ONE_WEAPON_ANIMATION', animation_const.WEAPON_POS_RIGHT, right_clip_list, loop=loop, time_scale=time_scale, blend_time=blend_time)

    def get_skate_clip_list(self, model, clip_list):
        if not model:
            return clip_list
        skate_clip_list = []
        for one_clip_name in clip_list:
            one_skate_clip_name = 'skate_' + one_clip_name
            if model.has_anim(one_skate_clip_name):
                skate_clip_list.append(one_skate_clip_name)
            if len(skate_clip_list) == len(clip_list):
                clip_list = skate_clip_list

        return clip_list

    def change_one_weapon_animation(self, animator, clip_list, is_keep_phase, loop, time_scale, blend_time):
        if not animator:
            return
        root_node = animator.find(ROOT_NODE_NAME)
        if not root_node:
            return
        root_node.timeScale = time_scale
        is_single = False
        if len(clip_list) == 1:
            is_single = True
        move_action = self.ev_g_move_state()
        if move_action == animation_const.MOVE_STATE_STAND:
            is_single = True
        if is_single:
            animation_node = animator.find(SINGLE_NODE_NAME)
            if not animation_node:
                return
            if not is_keep_phase:
                animation_node.phase = 0
            animator.SetInt('blend_mode', 0)
            animation_node.timeScale = 1
            animation_node.SetMaxBlendOutTime(blend_time)
            clip_name = clip_list[-1]
            animator.replace_clip_name(SINGLE_NODE_NAME, clip_name, is_keep_phase, force=True)
            animation_node.loop = loop
        else:
            animation_node = animator.find(BLEND_NODE_NAME)
            if not animation_node:
                return
            animation_node.timeScale = 1
            single_animation_node = animator.find(SINGLE_NODE_NAME)
            blend_state = single_animation_node.GetBlendState()
            if not is_keep_phase:
                animation_node.phase = 0
            animator.SetInt('blend_mode', 1)
            all_child_states = animation_node.GetChildStates()
            for index, one_child_state in enumerate(all_child_states):
                one_source_node = one_child_state.childNode
                if animation_const.SOURCE_NODE_TYPE not in one_source_node.nodeType:
                    continue
                clip_name = clip_list[index]
                one_source_node.SetMaxBlendOutTime(0)
                animator.replace_clip_name(one_source_node, clip_name, is_keep_phase, force=True)
                one_source_node.loop = loop

            rocker_dir = self.sd.ref_rocker_dir
            dir_x = 0
            dir_y = 0
            if rocker_dir:
                dir_x = rocker_dir.x
                dir_y = rocker_dir.z
            self.set_dir_x_y(dir_x, dir_y)

    def get_idle_clip(self):
        weapon_type = self.ev_g_weapon_type()
        weapon_config = weapon_action_config.weapon_type_2_action.get(weapon_type, None)
        if not weapon_config:
            print('[Error] weapon_type =', weapon_type, '--do not have weapon action')
            import traceback
            traceback.print_stack()
            return
        else:
            action_key = 'idle'
            current_posture_state = self.ev_g_anim_state()
            if current_posture_state == animation_const.STATE_SQUAT:
                action_key = 'crouch_idle'
            idle_clip_list = weapon_config[action_key]
            if not idle_clip_list:
                idle_clip_list = weapon_action_config.weapon_type_2_action[animation_const.WEAPON_TYPE_NORMAL][action_key]
            clip_name = ''
            if self.ev_g_is_in_any_state((status_config.ST_STAND, status_config.ST_TURN)):
                if len(idle_clip_list) > 1:
                    clip_name = idle_clip_list[1]
                else:
                    clip_name = idle_clip_list[0]
            else:
                clip_name = idle_clip_list[0]
            return clip_name

    def change_weapon_idle(self):
        clip_name = self.get_idle_clip()
        if not clip_name:
            return
        blend_time = 0.2
        action_id = self.ev_g_weapon_action_id()
        if action_id == animation_const.WEAPON_TYPE_SHIELD:
            blend_time = 0
        self.change_weapon_animation([clip_name], False, True, blend_time=blend_time)

    def set_dir_x_y(self, dir_x, dir_y, *args):
        if self._left_weapon_animator:
            self._left_weapon_animator.SetFloat('dir_x', dir_x)
            self._left_weapon_animator.SetFloat('dir_y', dir_y)
        if self._right_weapon_animator:
            self._right_weapon_animator.SetFloat('dir_x', dir_x)
            self._right_weapon_animator.SetFloat('dir_y', dir_y)