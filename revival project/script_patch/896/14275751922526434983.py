# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartHitHintManager.py
from __future__ import absolute_import
import six_ex
import six
from six.moves import range
from . import ScenePart
import world
import math3d
import random
import math
import time
from common.utils.cocos_utils import neox_pos_to_cocos
from common.cfg import confmgr
import logic.gcommon.common_const.animation_const as animation_const
from copy import copy, deepcopy
from common.uisys.ui_proxy import trans2ProxyObj
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.const import HIT_PART_HEAD, WEAKNESS_ATTACK_TAG, EXECUTE_HIT_HINT
from common.const.uiconst import BATTLE_MESSAGE_ZORDER
import cc
from mobile.common.EntityManager import EntityManager
from logic.client.const import game_mode_const
from logic.units.LPuppet import LPuppet
import data.hit_hint_arg as hit_hint_arg
from logic.gutils.client_unit_tag_utils import register_unit_tag, preregistered_tags
from logic.gcommon.common_utils.local_text import get_cur_pic_lang_name, LANG_CN, LANG_ZHTW, LANG_EN, LANG_JA, LANG_KO, LANG_TH, LANG_ID
MECHA_PREFIX = 'mecha_'
HUMAN_PREFIX = 'human_'
MECHA_MONSTER_TAG_VALUE = register_unit_tag(('LMecha', 'LMechaRobot', 'LMonster'))
NEED_SPECIAL_HANDLER_TAG_VALUE = register_unit_tag(('LDeathDoor', 'LExerciseTarget',
                                                    'LFishHeadTarget'))

class PartHitHintManager(ScenePart.ScenePart):
    CACHE_NUM = 25
    CACHE_TIME = 2.0
    DELAY = 0.03
    CURVE_TRACK_TAG = 1
    ENTER_EVENT = {'target_invincible_event': '_show_invincible_hint',
       'stop_player_damage_event': '_stop_hit_hint',
       'net_login_reconnect_event': '_on_net_reconnect',
       'set_test_damage_font_event': 'set_test_damage_font',
       'pve_element_reaction_event': '_show_pve_element_reaction'
       }

    def __init__(self, scene, name):
        super(PartHitHintManager, self).__init__(scene, name)
        self._entity_data = {}
        self._item_pool = []
        self._displaying_item = {}
        self._key_id = 0
        self._pre_handler = {'normal': self._show_normal_hit_hint,
           'shotgun': self._show_shotgun_hit_hint,
           'tap2': self._show_tap_hit_hint
           }
        self._display_handler = {'parabola': self._display_curve_item,
           'shotgun': self._display_shotgun_item,
           'simple': self._display_simple_item,
           'crowd': self._display_crowd_item
           }
        self._screen_center_pos_dict = {}
        self._update_timer_id = 0
        self._damage_range = {}
        self._scale_range = {}
        self._test_font_path = None
        self.load_range_config()
        self.pve_ele_react_hint_path = 'gui/ui_res_2/txt_pic/text_pic_en/pve_hint/'
        return

    def load_range_config(self):
        self._damage_range = {}
        self._scale_range = {}
        all_prefixes = (
         MECHA_PREFIX, HUMAN_PREFIX)
        for one_prefix in all_prefixes:
            for index in range(1, 20):
                damage_key = one_prefix + 'damage_range_' + str(index)
                one_damage_range = getattr(hit_hint_arg, damage_key, None)
                scale_key = one_prefix + 'scale_range_' + str(index)
                one_scale_range = getattr(hit_hint_arg, scale_key, None)
                if not one_damage_range or not one_scale_range:
                    break
                self._damage_range.setdefault(one_prefix, []).append(one_damage_range)
                self._scale_range.setdefault(one_prefix, []).append(one_scale_range)

        return

    def on_enter(self):
        self._init_data()
        self._init_event()

    def on_exit(self):
        self._end_tick()
        self._destroy_items()

    def _init_event(self):
        global_data.emgr.player_make_damage_event += self._show_hit_hint

    def _stop_hit_hint(self):
        global_data.emgr.player_make_damage_event -= self._show_hit_hint

    def _init_data(self):
        if global_data.game_mode.is_pve():
            player_size_mode = global_data.battle.get_pve_player_size_mode()
            cache_size = self.CACHE_NUM * player_size_mode
            difficulty = global_data.battle.get_cur_pve_difficulty()
            if difficulty > 1:
                cache_size = int(cache_size + cache_size * (difficulty - 1) * 0.2)
        else:
            cache_size = self.CACHE_NUM
        self._item_pool = [ self._create_item() for _ in range(cache_size) ]
        self._start_tick()

    def _destroy_items(self):
        self._entity_data = {}
        self._display_handler = None
        self._pre_handler = None
        for item in self._item_pool:
            if item.isValid():
                item.Destroy()

        self._item_pool = []
        for one_item_info in six.itervalues(self._displaying_item):
            item = one_item_info[0]
            if item.isValid():
                item.Destroy()

        self._displaying_item.clear()
        return

    def _on_update(self, dt):
        for eid in six_ex.keys(self._entity_data):
            entity = EntityManager.getentity(eid)
            unit_obj = entity.logic if entity and entity.logic else None
            if not unit_obj:
                del self._entity_data[eid]
                continue
            info = self._entity_data[eid]
            now = time.time()
            cache_items = info['cache']
            while cache_items:
                hint_type, delay, args = cache_items[0]
                if now >= info['last_time'] + delay:
                    info['last_time'] = now
                    cache_items.pop(0)
                    self._display_item(hint_type, unit_obj, *args)
                else:
                    break

            item_cnt = info.get('cnt', 0)
            if item_cnt > 0 and (not info.get('pos') or now > info.get('next_time', 0)):
                info['pos'] = self._get_2d_pos(unit_obj, info)
                info['next_time'] = now + 0.05
            if info['pos'] is None or not cache_items and item_cnt <= 0:
                del self._entity_data[eid]

        camera = world.get_active_scene().active_camera
        for one_item_info in six.itervalues(self._displaying_item):
            item, eid, target_pos, shield, screen_center = one_item_info
            info = self._entity_data.get(eid, {})
            pos_base_hit_part = info.get('pos_base_hit_part', False)
            pos = info.get('pos')
            if screen_center:
                screen_size = global_data.ui_mgr.design_screen_size
                pos = (screen_size.width / 2, screen_size.height / 2)
            elif pos_base_hit_part and target_pos:
                entity = EntityManager.getentity(eid)
                if entity and entity.logic:
                    unit_obj = entity.logic if 1 else None
                    if not unit_obj:
                        pass
                    continue
                cur_world_pos = target_pos + info.get('diff_translation', math3d.vector(0, 0, 0))
                neox_2d_pos = camera.world_to_screen(cur_world_pos)
                cocos_2d_pos = neox_pos_to_cocos(*neox_2d_pos)
                dy = self._get_vertical_dy(unit_obj)
                pos = [cocos_2d_pos[0], cocos_2d_pos[1] + dy]
            if pos:
                item.setPosition(*pos)
            else:
                item.setVisible(False)

        return

    def _show_hit_hint(self, target_unit, hit_parts, shield_damage=0, weapon_id=None, extra_dict=None):
        if not target_unit:
            return
        else:
            hit_type = confmgr.get('hit_hint', str(weapon_id), 'cHitType', default='normal')
            pre_handler = self._pre_handler.get(hit_type)
            if not pre_handler:
                return
            shield_damage and pre_handler({-1: [1, shield_damage]}, target_unit, weapon_id, True, extra_dict)
            delay = 0 if shield_damage else None
            pre_handler(hit_parts, target_unit, weapon_id, False, extra_dict, delay)
            global_data.emgr.emit('exercise_show_hit_distance_event', target_unit)
            return

    def _show_invincible_hint(self, target_unit, weapon_id, text_id=17019):
        if global_data.game_mode.is_mode_type((game_mode_const.GAME_MODE_MECHA_DEATH, game_mode_const.GAME_MODE_GOOSE_BEAR)):
            if isinstance(target_unit, LPuppet):
                return
        hint_type = 'immune'
        conf = confmgr.get('hit_hint', str(weapon_id), default={})
        delay = conf.get('fInterval', self.DELAY)
        self._cache_item(target_unit, hint_type, delay, (-1, False, {'text_id': text_id}))

    def _show_pve_element_reaction(self, target_unit, reaction_type):
        if not target_unit:
            return
        hint_type = 'pve_react'
        if target_unit:
            target_pos = target_unit.ev_g_position()
            self._cache_item(target_unit, hint_type, self.DELAY, (-1, False, {'reaction_type': reaction_type,'target_pos': target_pos}))

    def _cache_item(self, target_unit, hint_type, delay, args):
        if not target_unit:
            return
        else:
            eid = target_unit.id
            damage, use_shield, c_params = args
            if eid not in self._entity_data:
                pos_base_hit_part = False
                if global_data.cam_lplayer and global_data.cam_lplayer.ev_g_is_human():
                    obj_weapon = global_data.cam_lplayer.share_data.ref_wp_bar_cur_weapon
                    if obj_weapon and target_unit.share_data.ref_is_mecha:
                        fHitHintDist = confmgr.get('firearm_config', str(obj_weapon.get_item_id()), 'fHitHintDist', default=0) * NEOX_UNIT_SCALE
                        if fHitHintDist > 0:
                            self_pos = global_data.cam_lplayer.ev_g_position()
                            target_pos = target_unit.ev_g_position()
                            diff_vec = self_pos - target_pos
                            diff_vec.y = 0
                            if diff_vec.length <= fHitHintDist:
                                pos_base_hit_part = True
                self._entity_data[eid] = {'last_time': 0,
                   'cache': [],'cnt': 0,
                   'pos': None,
                   'next_time': 0,
                   'pos_base_hit_part': pos_base_hit_part,
                   'hint_type': hint_type,
                   'use_shield': use_shield
                   }
            data = self._entity_data[eid]['cache']
            data.append((hint_type, delay, args))
            return

    def _show_normal_hit_hint(self, hit_parts, target_unit, weapon_id, use_shield, extra_params=None, delay=None):
        if not hit_parts:
            return
        else:
            part = six_ex.keys(hit_parts)[0]
            damage = hit_parts[part][1]
            if not damage:
                return
            weapon_id = str(weapon_id)
            conf = confmgr.get('hit_hint', weapon_id, default={})
            if part == HIT_PART_HEAD:
                hint_type = conf.get('cHeadType', 'normal')
                c_params = conf.get('cHeadParams', {})
            else:
                hint_type = conf.get('cBodyType', 'normal')
                c_params = conf.get('cBodyParams', {})
            if extra_params and extra_params.get(WEAKNESS_ATTACK_TAG):
                if 'hit_weakness_type' in c_params:
                    hint_type = c_params['hit_weakness_type']
            c_params = dict(c_params)
            if extra_params:
                c_params.update(extra_params)
            if delay is None:
                delay = conf.get('fInterval', self.DELAY)
            self._cache_item(target_unit, hint_type, delay, (damage, use_shield, c_params))
            return

    def _show_shotgun_hit_hint(self, hit_parts, target_unit, weapon_id, use_shield, extra_params=None, delay=None):
        i = 0
        hit_carry_shield = extra_params.get('hit_carry_shield', False) if extra_params else False
        for hit_part, hit_info in six.iteritems(hit_parts):
            hit_count, hit_damage = hit_info
            format_hit_parts = {hit_part: (1, hit_damage / hit_count)}
            for _ in range(hit_count):
                self._show_normal_hit_hint(format_hit_parts, target_unit, weapon_id, use_shield, {'sub_idx': i,'hit_carry_shield': hit_carry_shield}, 0)
                i += 1

    def _show_tap_hit_hint(self, hit_parts, target_unit, weapon_id, use_shield, extra_params=None, delay=None):
        if not hit_parts:
            return
        conf = confmgr.get('hit_hint', str(weapon_id))
        tap_num = int(conf.get('cHitType', 'tap2')[-1])
        part = six_ex.keys(hit_parts)[0]
        damage = hit_parts[part][1]
        new_hit_parts = {part: [1, damage / tap_num]}
        delay = conf.get('fInterval', 0.2)
        for _ in range(tap_num):
            self._show_normal_hit_hint(new_hit_parts, target_unit, weapon_id, use_shield, extra_params=extra_params, delay=delay)

    def _display_item(self, hint_type, unit_obj, damage, shield, c_params):
        if hint_type == 'pve_submerge':
            pass
        if hint_type == 'pve_fire':
            pass
        if not damage:
            return
        item = self._get_item()
        conf = confmgr.get('hit_hint_type', hint_type)
        if not conf:
            return
        params = dict(conf.get('cCustomParams', {}))
        params.update(c_params)
        self._set_content(item, hint_type, unit_obj, damage, shield, params)
        curve_type = conf['cCurveType']
        self._display_handler[curve_type](item, hint_type, unit_obj, damage, shield, params)
        animation_name = conf['cAnimation']
        if animation_name:
            item.PlayAnimation(animation_name)
        max_frame = conf.get('iFrames', 30)
        delta = max_frame / 30.0
        self._start_display(item, unit_obj.id, delta, hint_type, shield, params)

    def _display_simple_item(self, item, hint_type, unit_obj, damage, shield, params):
        h = 50
        if global_data.cam_lplayer and global_data.cam_lplayer.ev_g_is_in_mecha() and unit_obj.MASK & MECHA_MONSTER_TAG_VALUE:
            h = 70
        if shield:
            h -= 20
        item.nd_track.setPosition(0, h)

    def _display_curve_item(self, item, hint_type, unit_obj, damage, shield, params):
        conf = confmgr.get('hit_hint_type', hint_type)
        max_frame = conf.get('iFrames', 30)
        x_ratio = conf.get('fXRatio', 1.2)
        reverse = params.get('reverse', -1 if shield else 1)
        delta = max_frame / 30.0
        width = random.uniform(*params.get('width', (200, 250))) * reverse
        height = random.uniform(*params.get('height', (100, 200)))
        act = cc.JumpBy.create(delta * x_ratio, cc.Vec2(width, 0), height, 1)
        act.setTag(self.CURVE_TRACK_TAG)
        item.nd_track.setPosition(0, 0)
        item.nd_track.stopActionByTag(self.CURVE_TRACK_TAG)
        item.nd_track.runAction(act)

    def _display_shotgun_item(self, item, hint_type, unit_obj, damage, shield, params):
        track_no = params.get('sub_idx', 0)
        r_random = random.uniform(*params.get('r', (0, 10)))
        rpn = 'rS' if shield else 'rN'
        r1, r2 = params.get(rpn) or [35, 70]
        r2 += r_random
        track_num = params.get('track_num', 11)
        angle = math.pi * 0.75 - math.pi * 2 / track_num * track_no
        angle_sin = math.sin(angle)
        angle_cos = math.cos(angle)
        x_scale = params.get('x_scale', 1.0)
        item.nd_track.setPosition(r1 * angle_cos * x_scale, r1 * angle_sin)
        act = cc.MoveTo.create(0.1, cc.Vec2(r2 * angle_cos * x_scale, r2 * angle_sin))
        act.setTag(self.CURVE_TRACK_TAG)
        item.nd_track.stopActionByTag(self.CURVE_TRACK_TAG)
        item.nd_track.runAction(act)

    def _display_crowd_item(self, item, hint_type, unit_obj, damage, shield, params):
        track_no = params.get('sub_idx', 0)
        r_random = random.uniform(*params.get('r', (0, 10)))
        rpn = 'rS' if shield else 'rN'
        r1, r2 = params.get(rpn) or [35, 70]
        r2 += r_random
        track_num = params.get('track_num', 11)
        if track_no == 0:
            angle = math.pi * 0.5
        else:
            angle = math.pi * 0.75 - math.pi * 2 / track_num * (track_no - 1)
        angle_sin = math.sin(angle)
        angle_cos = math.cos(angle)
        x_scale = params.get('x_scale', 1.0)
        item.nd_track.setPosition(r1 * angle_cos * x_scale, r1 * angle_sin)
        act = cc.MoveTo.create(0.1, cc.Vec2(r2 * angle_cos * x_scale, r2 * angle_sin))
        act.setTag(self.CURVE_TRACK_TAG)
        item.nd_track.stopActionByTag(self.CURVE_TRACK_TAG)
        item.nd_track.runAction(act)

    def _start_display(self, item, eid, lasting_time, hint_type, shield, c_params):
        if eid not in self._entity_data:
            return
        else:
            item.setVisible(True)
            self._key_id += 1
            self._entity_data[eid]['cnt'] += 1
            target_pos = c_params.get('target_pos', None)
            screen_center = c_params.get('screen_center', 0)
            if screen_center:
                x_off, y_off = self._get_valid_screen_center_offset()
                ori_pos = item.nd_track.getPosition()
                item.nd_track.setPosition(ori_pos.x + x_off, ori_pos.y + y_off)
                self._screen_center_pos_dict[self._key_id] = (x_off, y_off)
            self._displaying_item[self._key_id] = (item, eid, target_pos, shield, screen_center)
            item.SetTimeOut(lasting_time, lambda eid=eid, kid=self._key_id: self.recycle(eid, kid))
            return

    def recycle(self, eid, kid):
        if eid in self._entity_data:
            self._entity_data[eid]['cnt'] -= 1
        one_item_info = self._displaying_item.pop(kid)
        item = one_item_info[0]
        item.nd_track.stopActionByTag(self.CURVE_TRACK_TAG)
        item.setVisible(False)
        self._item_pool.append(item)
        self._screen_center_pos_dict.pop(kid, 0)

    def _get_item(self):
        if self._item_pool:
            return self._item_pool.pop()
        return self._create_item()

    def _create_item(self):
        parent = global_data.ui_mgr.get_ui_zorder_layer(BATTLE_MESSAGE_ZORDER) or trans2ProxyObj(global_data.cocos_scene)
        ui_item = global_data.uisystem.load_template_create('battle/i_fight_num_hint', parent=parent)
        ui_item.setVisible(False)
        return ui_item

    def set_test_damage_font(self, font_path):
        self._test_font_path = font_path

    def _set_content(self, item, hint_type, unit_obj, damage, shield, params):
        if hint_type == 'immune':
            item.immune.setVisible(True)
            item.nd_num.setVisible(False)
            text_id = params.get('text_id', 17019)
            item.immune.SetString(text_id)
            return
        if hint_type == 'pve_react':
            item.img.setVisible(True)
            item.nd_num.setVisible(False)
            reaction_type = params.get('reaction_type')
            react_path = self.pve_ele_react_hint_path + confmgr.get('chemical_react_hit_hint', str(reaction_type)).get('path', 'txt_pve_overload') + '.png'
            item.img.SetDisplayFrameByPath('', react_path)
            return
        item.img.setVisible(False)
        item.immune.setVisible(False)
        item.nd_num.setVisible(True)
        item.num.setVisible(True)
        item.num.SetString(str(int(damage * global_data.game_mode.get_mode_scale())))
        color = params.get('color') or self._get_color(unit_obj, shield)
        font_color = '#SW'
        if 'font_path' in params:
            font_path = params['font_path']
            font_color = params.get('font_color', '#SW')
        elif hint_type == 'onfire':
            font_color = '#SR'
            font_path = 'gui/fonts/num_hurt_white.fnt'
        elif isinstance(params, dict) and params.get('hit_carry_shield'):
            font_path = 'gui/fonts/battle_extra_shield_thick.fnt'
        else:
            font_path = 'gui/fonts/num_hurt_%s.fnt' % color
        if self._test_font_path:
            font_path = self._test_font_path
        item.num.SetColor(font_color)
        item.num.setBMFontFilePath(font_path)
        if params.get('show_critical_tag') or params.get(EXECUTE_HIT_HINT):
            item.icon_critical.setVisible(True)
            item.icon_critical.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/attack/icon_sp_injure_%s.png' % color)
        else:
            item.icon_critical.setVisible(False)
        if 'icon_path' in params:
            item.icon_attribute.setVisible(True)
            item.icon_attribute.SetDisplayFrameByPath('', params['icon_path'])
            item.num.SetPosition('50%8', '50%-4')
            weakness_tag_x_offset = 27
        else:
            item.icon_attribute.setVisible(False)
            item.num.SetPosition('50%-19', '50%-4')
            weakness_tag_x_offset = 0
        if params.get('show_weakness_tag') or params.get(WEAKNESS_ATTACK_TAG):
            item.icon_critical_small.setVisible(True)
            item.icon_critical_small.SetDisplayFrameByPath('', 'gui/ui_res_2/battle/attack/icon_sp_injure_small_%s.png' % color)
            bit_count = 0
            while damage > 0:
                damage //= 10
                bit_count += 1

            offset = 18 * (bit_count - 1)
            pos_x_str = '100%{}'.format(-13 + offset + weakness_tag_x_offset)
            item.icon_critical_small.SetPosition(pos_x_str, '50%-12')
        else:
            item.icon_critical_small.setVisible(False)
        prefix = MECHA_PREFIX
        if unit_obj and unit_obj.ev_g_is_human():
            prefix = HUMAN_PREFIX
        damage_range = self._damage_range.get(prefix, [])
        scale_range = self._scale_range.get(prefix, [])
        scale = self._get_num_scale(damage, damage_range, scale_range)
        item.nd_num.setScale(scale)

    def _get_color(self, unit, use_shield):
        if use_shield:
            return 'blue'
        if unit.MASK & preregistered_tags.HUMAN_TAG_VALUE:
            return 'white'
        return 'yellow'

    def _get_num_scale(self, total_damage, damage_range, scale_range):
        range_index = 0
        for index in range(len(damage_range)):
            one_damage_range = damage_range[index]
            if one_damage_range[0] <= total_damage and total_damage <= one_damage_range[1]:
                range_index = index
                break

        damage_range = damage_range[range_index]
        scale_range = scale_range[range_index]
        total_damage = min(total_damage, damage_range[1])
        damage_scale = (total_damage - damage_range[0]) / (damage_range[1] - damage_range[0])
        final_scale = scale_range[0] + (scale_range[1] - scale_range[0]) * damage_scale
        return final_scale

    def _get_vertical_dy(self, unit):
        if unit.MASK & MECHA_MONSTER_TAG_VALUE == 0:
            return 0.0
        if global_data.player and not global_data.player.logic.ev_g_is_in_mecha():
            target_pos = unit.ev_g_position()
            self_pos = global_data.player.logic.ev_g_position()
            if target_pos and self_pos:
                max_interval_bias = 100
                slope = max_interval_bias / 50.0
                dis = (target_pos - self_pos).length / NEOX_UNIT_SCALE
                return max(max_interval_bias - dis * slope, 0.0)
        return 0.0

    def _get_2d_pos--- This code section failed: ---

 609       0  LOAD_FAST             1  'unit_obj'
           3  LOAD_ATTR             0  'ev_g_model'
           6  CALL_FUNCTION_0       0 
           9  STORE_FAST            3  'target_model'

 610      12  LOAD_FAST             3  'target_model'
          15  POP_JUMP_IF_TRUE     22  'to 22'

 611      18  LOAD_CONST            0  ''
          21  RETURN_END_IF    
        22_0  COME_FROM                '15'

 612      22  LOAD_FAST             3  'target_model'
          25  LOAD_ATTR             1  'is_visible_in_this_frame'
          28  CALL_FUNCTION_0       0 
          31  UNARY_NOT        
          32  POP_JUMP_IF_FALSE    52  'to 52'
          35  LOAD_FAST             1  'unit_obj'
          38  LOAD_ATTR             2  'ev_g_is_shield'
          41  CALL_FUNCTION_0       0 
          44  UNARY_NOT        
        45_0  COME_FROM                '32'
          45  POP_JUMP_IF_FALSE    52  'to 52'

 613      48  LOAD_CONST            0  ''
          51  RETURN_END_IF    
        52_0  COME_FROM                '45'

 614      52  LOAD_FAST             1  'unit_obj'
          55  LOAD_ATTR             3  'ev_g_hit_hint_bone'
          58  CALL_FUNCTION_0       0 
          61  JUMP_IF_TRUE_OR_POP    70  'to 70'
          64  LOAD_GLOBAL           4  'animation_const'
          67  LOAD_ATTR             5  'BONE_SPINE2_NAME'
        70_0  COME_FROM                '61'
          70  STORE_FAST            4  'bone_name'

 615      73  LOAD_FAST             3  'target_model'
          76  LOAD_ATTR             6  'get_bone_matrix'
          79  LOAD_FAST             4  'bone_name'
          82  LOAD_GLOBAL           7  'world'
          85  LOAD_ATTR             8  'SPACE_TYPE_WORLD'
          88  CALL_FUNCTION_2       2 
          91  STORE_FAST            5  'target_matrix'

 616      94  LOAD_FAST             5  'target_matrix'
          97  POP_JUMP_IF_TRUE    301  'to 301'

 617     100  LOAD_FAST             1  'unit_obj'
         103  LOAD_ATTR             9  'MASK'
         106  LOAD_GLOBAL          10  'NEED_SPECIAL_HANDLER_TAG_VALUE'
         109  BINARY_AND       
         110  LOAD_CONST            1  ''
         113  COMPARE_OP            2  '=='
         116  POP_JUMP_IF_FALSE   177  'to 177'

 618     119  LOAD_FAST             3  'target_model'
         122  LOAD_ATTR            11  'position'
         125  LOAD_GLOBAL          12  'math3d'
         128  LOAD_ATTR            13  'vector'
         131  LOAD_CONST            1  ''
         134  LOAD_FAST             3  'target_model'
         137  LOAD_ATTR            14  'bounding_box'
         140  LOAD_ATTR            15  'y'
         143  LOAD_CONST            1  ''
         146  CALL_FUNCTION_3       3 
         149  BINARY_ADD       
         150  STORE_FAST            6  'pos'

 619     153  LOAD_GLOBAL          12  'math3d'
         156  LOAD_ATTR            16  'matrix'
         159  CALL_FUNCTION_0       0 
         162  STORE_FAST            5  'target_matrix'

 620     165  LOAD_FAST             6  'pos'
         168  LOAD_FAST             5  'target_matrix'
         171  STORE_ATTR           17  'translation'
         174  JUMP_ABSOLUTE       301  'to 301'

 622     177  LOAD_GLOBAL          18  'getattr'
         180  LOAD_GLOBAL           2  'ev_g_is_shield'
         183  LOAD_FAST             1  'unit_obj'
         186  LOAD_ATTR            19  '__class__'
         189  LOAD_ATTR            20  '__name__'
         192  BINARY_MODULO    
         193  LOAD_CONST            0  ''
         196  CALL_FUNCTION_3       3 
         199  STORE_FAST            7  'handler'

 623     202  LOAD_FAST             7  'handler'
         205  POP_JUMP_IF_FALSE   223  'to 223'

 624     208  LOAD_FAST             7  'handler'
         211  LOAD_FAST             3  'target_model'
         214  CALL_FUNCTION_1       1 
         217  STORE_FAST            5  'target_matrix'
         220  JUMP_ABSOLUTE       301  'to 301'

 626     223  LOAD_GLOBAL          22  'log_error'
         226  LOAD_CONST            3  'PartHitHintMananger: !!!!!!!! need pos handler for %s'
         229  LOAD_FAST             1  'unit_obj'
         232  LOAD_ATTR            19  '__class__'
         235  LOAD_ATTR            20  '__name__'
         238  BINARY_MODULO    
         239  CALL_FUNCTION_1       1 
         242  POP_TOP          

 627     243  LOAD_FAST             3  'target_model'
         246  LOAD_ATTR            11  'position'
         249  LOAD_GLOBAL          12  'math3d'
         252  LOAD_ATTR            13  'vector'
         255  LOAD_CONST            1  ''
         258  LOAD_FAST             3  'target_model'
         261  LOAD_ATTR            14  'bounding_box'
         264  LOAD_ATTR            15  'y'
         267  LOAD_CONST            1  ''
         270  CALL_FUNCTION_3       3 
         273  BINARY_ADD       
         274  STORE_FAST            6  'pos'

 628     277  LOAD_GLOBAL          12  'math3d'
         280  LOAD_ATTR            16  'matrix'
         283  CALL_FUNCTION_0       0 
         286  STORE_FAST            5  'target_matrix'

 629     289  LOAD_FAST             6  'pos'
         292  LOAD_FAST             5  'target_matrix'
         295  STORE_ATTR           17  'translation'
         298  JUMP_FORWARD          0  'to 301'
       301_0  COME_FROM                '298'

 630     301  LOAD_GLOBAL           7  'world'
         304  LOAD_ATTR            23  'get_active_scene'
         307  CALL_FUNCTION_0       0 
         310  LOAD_ATTR            24  'active_camera'
         313  STORE_FAST            8  'camera'

 631     316  LOAD_FAST             2  'info'
         319  LOAD_ATTR            25  'get'
         322  LOAD_CONST            4  'pos_base_hit_part'
         325  LOAD_GLOBAL          26  'False'
         328  CALL_FUNCTION_2       2 
         331  STORE_FAST            9  'pos_base_hit_part'

 632     334  LOAD_FAST             5  'target_matrix'
         337  LOAD_ATTR            17  'translation'
         340  STORE_FAST           10  'cur_world_pos'

 633     343  LOAD_FAST             9  'pos_base_hit_part'
         346  POP_JUMP_IF_FALSE   401  'to 401'

 634     349  LOAD_CONST            5  'base_bone_pos'
         352  LOAD_FAST             2  'info'
         355  COMPARE_OP            7  'not-in'
         358  POP_JUMP_IF_FALSE   374  'to 374'

 635     361  LOAD_FAST            10  'cur_world_pos'
         364  LOAD_FAST             2  'info'
         367  LOAD_CONST            5  'base_bone_pos'
         370  STORE_SUBSCR     
         371  JUMP_FORWARD          0  'to 374'
       374_0  COME_FROM                '371'

 637     374  LOAD_FAST            10  'cur_world_pos'
         377  LOAD_FAST             2  'info'
         380  LOAD_CONST            5  'base_bone_pos'
         383  BINARY_SUBSCR    
         384  BINARY_SUBTRACT  
         385  STORE_FAST           11  'diff_translation'

 638     388  LOAD_FAST            11  'diff_translation'
         391  LOAD_FAST             2  'info'
         394  LOAD_CONST            6  'diff_translation'
         397  STORE_SUBSCR     
         398  JUMP_FORWARD          0  'to 401'
       401_0  COME_FROM                '398'

 641     401  LOAD_FAST             8  'camera'
         404  LOAD_ATTR            27  'world_to_screen'
         407  LOAD_FAST            10  'cur_world_pos'
         410  CALL_FUNCTION_1       1 
         413  STORE_FAST           12  'neox_2d_pos'

 642     416  LOAD_GLOBAL          28  'neox_pos_to_cocos'
         419  LOAD_FAST            12  'neox_2d_pos'
         422  CALL_FUNCTION_VAR_0     0 
         425  STORE_FAST           13  'cocos_2d_pos'

 643     428  LOAD_FAST             0  'self'
         431  LOAD_ATTR            29  '_get_vertical_dy'
         434  LOAD_FAST             1  'unit_obj'
         437  CALL_FUNCTION_1       1 
         440  STORE_FAST           14  'dy'

 644     443  LOAD_FAST            13  'cocos_2d_pos'
         446  LOAD_CONST            1  ''
         449  BINARY_SUBSCR    
         450  LOAD_FAST            13  'cocos_2d_pos'
         453  LOAD_CONST            7  1
         456  BINARY_SUBSCR    
         457  LOAD_FAST            14  'dy'
         460  BINARY_ADD       
         461  BUILD_LIST_2          2 
         464  STORE_FAST           13  'cocos_2d_pos'

 646     467  LOAD_FAST            13  'cocos_2d_pos'
         470  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_3' instruction at offset 196

    def _on_net_reconnect(self, *args):
        self._start_tick()

    def _start_tick(self):
        self._end_tick()
        from common.utils import timer
        self._update_timer_id = global_data.game_mgr.get_post_logic_timer().register(func=self._on_update, interval=0.03333, mode=timer.CLOCK, timedelta=True)

    def _end_tick(self):
        if self._update_timer_id:
            global_data.game_mgr.get_post_logic_timer().unregister(self._update_timer_id)
            self._update_timer_id = 0

    def _get_valid_screen_center_offset(self):
        if not self._screen_center_pos_dict:
            return (0, 0)
        cx, cy = (0, 0)
        for _x, _y in six.itervalues(self._screen_center_pos_dict):
            cx -= _x
            cy += _y

        x_off, y_off = (0, 0)
        for _ in range(5):
            if abs(cx) < 50:
                x_off = random.randint(-150, 150) if 1 else cx + random.randint(-20, 20)
                y_off = random.randint(-20, int(20 - 0.1 * abs(x_off))) if abs(cx) < 50 else cy + random.randint(-5, 5)
                for _x, _y in six.itervalues(self._screen_center_pos_dict):
                    if abs(x_off - _x) + abs(y_off - _y) * 2 < 50:
                        break
                else:
                    return (
                     x_off, y_off)

        return (
         x_off, y_off)

    def _pos_handler_LDeathDoor(self, target_model):
        y_offset = math3d.vector(0, target_model.bounding_box.y, 0) * target_model.scale.y
        y_offset = y_offset * target_model.rotation_matrix
        pos = target_model.position + y_offset
        target_matrix = math3d.matrix()
        target_matrix.translation = pos
        return target_matrix

    def _pos_handler_LExerciseTarget(self, target_model):
        pos = target_model.position + math3d.vector(0, target_model.bounding_box.y, 0) * target_model.scale.y * 1.325
        target_matrix = math3d.matrix()
        target_matrix.translation = pos
        return target_matrix

    def _pos_handler_LFishHeadTarget(self, target_model):
        pos = target_model.position + math3d.vector(0, target_model.bounding_box.y, 0) * target_model.scale.y * 1.325
        target_matrix = math3d.matrix()
        target_matrix.translation = pos
        return target_matrix