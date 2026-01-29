# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_effect/ComMechaBuffShieldEffect.py
from __future__ import absolute_import
import six_ex
import six
from six.moves import range
from logic.gcommon.component.UnitCom import UnitCom
from logic.gutils.screen_effect_utils import create_screen_effect_with_auto_refresh, remove_screen_effect_with_auto_refresh, remove_all_screen_effect_with_auto_refresh
from logic.gcommon.item.item_const import FASHION_POS_SUIT, FASHION_POS_WEAPON_SFX, MECHA_FASHION_KEY
from logic.gutils.mecha_skin_utils import get_accurate_mecha_skin_info_from_fasion_data
from logic.gutils.dress_utils import DEFAULT_CLOTHING_ID
from common.utils.timer import CLOCK
from common.cfg import confmgr
import math3d
import time
MECHA_CONDITION_FORMAT = 'mecha_{}'
SKIN_CONDITION_FORMAT = 'skin_{}'
BUFF_CONDITION_FORMAT = 'buff_{}'

class ComMechaBuffShieldEffect(UnitCom):
    BIND_EVENT = {'E_MODEL_LOADED': 'on_model_loaded',
       'E_GLOBAL_MECHA_BUFF_ADD': 'on_add_mecha_buff',
       'E_GLOBAL_MECHA_BUFF_DEL': 'on_del_mecha_buff',
       'E_NOTIFY_PASSENGER_LEAVE': 'on_notify_leave',
       'E_ON_DRIVER_CHANGE': 'on_driver_change',
       'E_HIDE_SHIELD_SFX': 'hide_shield_sfx',
       'E_SWITCH_MODEL': 'on_switch_model'
       }

    def __init__(self):
        super(ComMechaBuffShieldEffect, self).__init__()
        shield_effect_conf = confmgr.get('mecha_shield_sfx_config')
        self.effect_index_map = shield_effect_conf['buff_index']
        self.effect_info_map = shield_effect_conf['shield_effect']
        self.direct_effect_info_map = dict()
        self.mecha_condition = None
        self.own_shield_effect_ref_count = dict()
        self.own_shield_effect_info = dict()
        self.need_check_refresh_buff_id_info = dict()
        self.cur_buff_info = dict()
        self.is_screen_model_effect = dict()
        self.driver_id = None
        self._show_sfx = True
        return

    def _init_direct_effect_info_map(self):
        for effect_index, effect_info_list in six.iteritems(self.effect_info_map):
            self.direct_effect_info_map[effect_index] = list()
            for effect_info in effect_info_list:
                new_effect_info = {}
                for key, specific_effect_info in six.iteritems(effect_info):
                    if self.skin_condition not in specific_effect_info:
                        if self.mecha_condition not in specific_effect_info:
                            real_info_key = 'default'
                        else:
                            real_info_key = self.mecha_condition
                    else:
                        real_info_key = self.skin_condition
                    new_effect_info[key] = specific_effect_info[real_info_key]

                self.direct_effect_info_map[effect_index].append(new_effect_info)

    def _init_check_refresh_buff_id_info(self):
        for effect_index, effect_info_list in six.iteritems(self.effect_info_map):
            for effect_info in effect_info_list:
                for key, specific_effect_info in six_ex.items(effect_info):
                    if self.skin_condition not in specific_effect_info:
                        if self.mecha_condition not in specific_effect_info:
                            continue
                        else:
                            real_info_key = self.mecha_condition
                    else:
                        real_info_key = self.skin_condition
                    effect_data = specific_effect_info[real_info_key]
                    if type(effect_data) != dict:
                        continue
                    for sub_key in six.iterkeys(effect_data):
                        if sub_key == 'default':
                            continue
                        buff_id = sub_key.split('_')[1]
                        if buff_id not in self.need_check_refresh_buff_id_info:
                            self.need_check_refresh_buff_id_info[buff_id] = set()
                        self.need_check_refresh_buff_id_info[buff_id].add(effect_index)

    def init_from_dict(self, unit_obj, bdict):
        super(ComMechaBuffShieldEffect, self).init_from_dict(unit_obj, bdict)
        self.mecha_id = bdict.get('mecha_id', 8001)
        self.mecha_condition = ''
        self.skin_condition = ''
        self._skin_id, self._shiny_weapon_id = get_accurate_mecha_skin_info_from_fasion_data(self.sd.ref_mecha_id, bdict.get(MECHA_FASHION_KEY, {}))
        self._init_condition()
        self._init_direct_effect_info_map()
        self._init_check_refresh_buff_id_info()

    def _init_condition(self):
        if self._shiny_weapon_id != '':
            self.skin_condition = SKIN_CONDITION_FORMAT.format(self._shiny_weapon_id)
        elif self._skin_id != DEFAULT_CLOTHING_ID:
            self.skin_condition = SKIN_CONDITION_FORMAT.format(self._skin_id)
        self.mecha_condition = MECHA_CONDITION_FORMAT.format(self.mecha_id)

    def on_post_init_complete(self, bdict):
        self.driver_id = self.sd.ref_driver_id

    def destroy(self):
        remove_all_screen_effect_with_auto_refresh(self.driver_id)
        for effect_info_list in six.itervalues(self.own_shield_effect_info):
            for effect_info in effect_info_list:
                if effect_info.get('timer_id'):
                    global_data.game_mgr.unregister_logic_timer(effect_info['timer_id'])

        self.effect_index_map = None
        self.effect_info_map = None
        return

    def on_model_loaded(self, model):
        for effect_index, effect_info_list in six.iteritems(self.own_shield_effect_info):
            for info in effect_info_list:
                if info.get('socket'):
                    if info.get('sfx_id'):
                        global_data.sfx_mgr.remove_sfx_by_id(info['sfx_id'])

                    def on_create_cb(sfx, scale=info['scale'], offset=info['offset']):
                        if scale:
                            sfx.scale = math3d.vector(scale, scale, scale)
                        if offset:
                            sfx.position = math3d.vector(*offset)

                    info['sfx_id'] = global_data.sfx_mgr.create_sfx_on_model(info['path'], model, info['socket'], on_create_func=on_create_cb)

    def _get_specific_effect_info(self, effect_info, key):
        if key not in effect_info:
            return
        else:
            value = effect_info[key]
            if type(value) == dict:
                default_value = None
                for condition_key, correspond_value in six.iteritems(value):
                    if condition_key == 'default':
                        default_value = correspond_value
                    else:
                        buff_id = condition_key.split('_')[1]
                        if self.cur_buff_info.get(buff_id, {}).get('count', 0) > 0:
                            if key == 'start_effect_delay_create_interval':
                                cur_time_stamp = time.time()
                                passed_time = cur_time_stamp - self.cur_buff_info[buff_id]['time_stamp']
                                return max(0, correspond_value - passed_time)
                            else:
                                return correspond_value

                return default_value
            return value
            return

    def _do_create_screen_effect(self, effect_index, info_index, path, need_set_timer=True):
        create_screen_effect_with_auto_refresh(self.driver_id, path)
        info = self.own_shield_effect_info[effect_index][info_index]
        info['path'] = path
        if need_set_timer:
            info['timer_id'] = None
        return

    def _create_screen_effect(self, effect_index, info_index, path, delay_interval):
        if delay_interval > 0:
            timer_id = global_data.game_mgr.register_logic_timer(self._do_create_screen_effect, interval=delay_interval, args=(effect_index, info_index, path), times=1, mode=CLOCK)
            return timer_id
        else:
            self._do_create_screen_effect(effect_index, info_index, path, False)
            return None
            return None

    def _do_create_model_effect(self, effect_index, info_index, socket, path, scale, offset, need_set_timer=True):
        info = self.own_shield_effect_info[effect_index][info_index]
        info['scale'] = scale
        info['offset'] = offset
        model = self.ev_g_model()
        if not model:
            info['socket'] = socket
            info['path'] = path
            info['sfx_id'] = None
            return
        else:

            def on_create_cb(sfx):
                if scale:
                    sfx.scale = math3d.vector(scale, scale, scale)
                if offset:
                    sfx.position = math3d.vector(*offset)
                sfx.visible = self._show_sfx

            is_same_sfx = False
            if info.get('sfx_id'):
                if info.get('path') == path:
                    sfx = global_data.sfx_mgr.get_sfx_by_id(info['sfx_id'])
                    if sfx:
                        if info.get('socket') != socket:
                            sfx.remove_from_parent()
                            model.bind(socket, sfx)
                            info['socket'] = socket
                        on_create_cb(sfx)
                        is_same_sfx = True
                else:
                    global_data.sfx_mgr.remove_sfx_by_id(info['sfx_id'])
            if not is_same_sfx:
                info['socket'] = socket
                info['path'] = path
                sfx_id = global_data.sfx_mgr.create_sfx_on_model(path, model, socket, on_create_func=on_create_cb)
                info['sfx_id'] = sfx_id
            if need_set_timer:
                info['timer_id'] = None
            return

    def _create_model_effect(self, effect_index, info_index, socket, path, delay_interval, scale, offset):
        if delay_interval > 0:
            timer_id = global_data.game_mgr.register_logic_timer(self._do_create_model_effect, interval=delay_interval, args=(
             effect_index, info_index, socket, path, scale, offset), times=1, mode=CLOCK)
            return timer_id
        else:
            self._do_create_model_effect(effect_index, info_index, socket, path, scale, offset, False)
            return None
            return None

    def _create_shield_effect(self, effect_index, info_index, socket, path, delay_interval, scale, offset):
        if socket:
            return self._create_model_effect(effect_index, info_index, socket, path, delay_interval, scale, offset)
        return self._create_screen_effect(effect_index, info_index, path, delay_interval)

    def _remove_old_effect_with_effect_info(self, effect_info):
        if effect_info.get('timer_id'):
            global_data.game_mgr.unregister_logic_timer(effect_info['timer_id'])
            effect_info['timer_id'] = None
        elif effect_info.get('socket'):
            if effect_info.get('sfx_id'):
                global_data.sfx_mgr.remove_sfx_by_id(effect_info['sfx_id'])
                effect_info['sfx_id'] = None
        else:
            effect_info.get('path') and remove_screen_effect_with_auto_refresh(self.driver_id, effect_info['path'])
        return

    def _remove_old_effect_with_effect_index(self, effect_index):
        for info in self.own_shield_effect_info[effect_index]:
            info and self._remove_old_effect_with_effect_info(info)

    def refresh_effect_according_for_buff_updated(self, buff_id):
        if buff_id in self.need_check_refresh_buff_id_info:
            check_refresh_effect_index_set = self.need_check_refresh_buff_id_info[buff_id]
            for effect_index in check_refresh_effect_index_set:
                if self.own_shield_effect_ref_count.get(effect_index, 0) > 0:
                    effect_info_list = self.direct_effect_info_map[effect_index]
                    for info_index, effect_info in enumerate(effect_info_list):
                        socket = self._get_specific_effect_info(effect_info, 'effect_socket')
                        start_effect_path = self._get_specific_effect_info(effect_info, 'start_effect_path')
                        cur_effect_info = self.own_shield_effect_info[effect_index][info_index]
                        if socket == cur_effect_info.get('socket') and start_effect_path == cur_effect_info.get('path'):
                            continue
                        if cur_effect_info.get('timer_id'):
                            global_data.game_mgr.unregister_logic_timer(cur_effect_info['timer_id'])
                        delay_create_interval = self._get_specific_effect_info(effect_info, 'start_effect_delay_create_interval')
                        scale = self._get_specific_effect_info(effect_info, 'effect_scale')
                        offset = self._get_specific_effect_info(effect_info, 'effect_offset')
                        timer_id = self._create_shield_effect(effect_index, info_index, socket, start_effect_path, delay_create_interval, scale, offset)
                        self.own_shield_effect_info[effect_index][info_index]['timer_id'] = timer_id

    def on_add_mecha_buff(self, buff_id, left_time, add_time, duration, data):
        buff_id = str(buff_id)
        buff_idx = data['buff_idx']
        if buff_id not in self.cur_buff_info:
            self.cur_buff_info[buff_id] = {'count': 0,'time_stamp': None,'buff_idx_set': set()}
        if self.cur_buff_info[buff_id]['count'] == 0:
            self.cur_buff_info[buff_id]['time_stamp'] = time.time()
        if buff_idx in self.cur_buff_info[buff_id]['buff_idx_set']:
            return
        else:
            self.cur_buff_info[buff_id]['buff_idx_set'].add(buff_idx)
            self.cur_buff_info[buff_id]['count'] += 1
            self.refresh_effect_according_for_buff_updated(buff_id)
            if buff_id not in self.effect_index_map:
                return
            effect_index = self.effect_index_map[buff_id]
            if effect_index not in self.own_shield_effect_ref_count:
                self.own_shield_effect_ref_count[effect_index] = 0
                self.own_shield_effect_info[effect_index] = [ dict() for i in range(len(self.direct_effect_info_map[effect_index])) ]
            self.own_shield_effect_ref_count[effect_index] += 1
            if self.own_shield_effect_ref_count[effect_index] > 1:
                return
            self._remove_old_effect_with_effect_index(effect_index)
            effect_info_list = self.direct_effect_info_map[effect_index]
            for info_index, effect_info in enumerate(effect_info_list):
                if 'sfx_id' in self.own_shield_effect_info[effect_index][info_index]:
                    sfx_id = self.own_shield_effect_info[effect_index][info_index]['sfx_id']
                    if sfx_id:
                        global_data.sfx_mgr.remove_sfx_by_id(sfx_id)
                socket = self._get_specific_effect_info(effect_info, 'effect_socket')
                start_effect_path = self._get_specific_effect_info(effect_info, 'start_effect_path')
                delay_create_interval = self._get_specific_effect_info(effect_info, 'start_effect_delay_create_interval')
                scale = self._get_specific_effect_info(effect_info, 'effect_scale')
                offset = self._get_specific_effect_info(effect_info, 'effect_offset')
                timer_id = self._create_shield_effect(effect_index, info_index, socket, start_effect_path, delay_create_interval, scale, offset)
                self.own_shield_effect_info[effect_index][info_index]['timer_id'] = timer_id

            return

    def on_del_mecha_buff(self, buff_id, buff_idx):
        buff_id = str(buff_id)
        if buff_id not in self.cur_buff_info:
            return
        if buff_idx not in self.cur_buff_info[buff_id]['buff_idx_set']:
            return
        self.cur_buff_info[buff_id]['buff_idx_set'].remove(buff_idx)
        self.cur_buff_info[buff_id]['count'] -= 1
        self.refresh_effect_according_for_buff_updated(buff_id)
        if buff_id not in self.effect_index_map:
            return
        effect_index = self.effect_index_map[buff_id]
        if self.own_shield_effect_ref_count.get(effect_index, 0) <= 0:
            return
        self.own_shield_effect_ref_count[effect_index] -= 1
        if self.own_shield_effect_ref_count[effect_index] > 0:
            return
        self._remove_old_effect_with_effect_index(effect_index)
        effect_info_list = self.direct_effect_info_map[effect_index]
        for info_index, effect_info in enumerate(effect_info_list):
            socket = self._get_specific_effect_info(effect_info, 'effect_socket')
            end_effect_path = self._get_specific_effect_info(effect_info, 'end_effect_path')
            if not end_effect_path:
                continue
            scale = self._get_specific_effect_info(effect_info, 'effect_scale')
            offset = self._get_specific_effect_info(effect_info, 'effect_offset')
            timer_id = self._create_shield_effect(effect_index, info_index, socket, end_effect_path, 0, scale, offset)
            self.own_shield_effect_info[effect_index][info_index]['timer_id'] = timer_id

    def on_notify_leave(self, *args, **kwargs):
        remove_all_screen_effect_with_auto_refresh(self.driver_id)

    def on_driver_change(self, new_driver_id):
        if new_driver_id:
            self.driver_id = new_driver_id

    def hide_shield_sfx(self, hide):
        self._show_sfx = not hide
        for effect_index, info_list in six.iteritems(self.own_shield_effect_info):
            for effect_info in info_list:
                if effect_info.get('socket'):
                    sfx = global_data.sfx_mgr.get_sfx_by_id(effect_info.get('sfx_id', None))
                    if sfx and sfx.valid:
                        sfx.visible = not hide

        return

    def on_switch_model(self, model):
        for effect_index, info_list in six.iteritems(self.own_shield_effect_info):
            for effect_info in info_list:
                socket_name = effect_info.get('socket')
                if socket_name:
                    sfx_id = effect_info.get('sfx_id')
                    sfx = global_data.sfx_mgr.get_sfx_by_id(sfx_id)
                    if sfx and sfx.valid:
                        sfx.remove_from_parent()
                        model.bind(socket_name, sfx)
                        sfx.visible = True