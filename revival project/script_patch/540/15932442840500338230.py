# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComWeaponBarClient.py
from __future__ import absolute_import
import six
import six_ex
from ..UnitCom import UnitCom
from logic.gcommon.const import PART_WEAPON_POS_NONE, PART_WEAPON_POS_MAIN_DF, PART_WEAPON_POS_MAIN1, PART_WEAPON_POS_MAIN2, PART_WEAPON_POS_MAIN3, MAIN_WEAPON_LIST
from ...cdata.status_config import ST_SWITCH, ST_SWIM, ST_PARACHUTE, ST_DOWN_TRANSMIT_STAND, ST_MECHA_DRIVER, ST_MECHA_PASSENGER, ST_DOWN, ST_MECHA_BOARDING
from logic.gcommon.ctypes.WeaponBarConst import WeaponBarConst
import logic.gcommon.common_utils.bcast_utils as bcast
import logic.gcommon.common_const.water_const as water_const
from logic.gcommon.cdata import status_config
from common.utils.time_utils import get_time
from logic.vscene.parts.camera.CamAimModelComponent import CamAimModelPreload
from logic.gcommon.const import ATTACHEMNT_AIM_POS
from logic.client.const import game_mode_const
from ...item import item_utility as iutil

class ComWeaponBarClient(UnitCom, WeaponBarConst):
    BIND_EVENT = {'G_WPBAR_GET_BY_POS': 'get_weapon_by_pos',
       'G_WPBAR_CUR_WEAPON': '_get_cur_weapon',
       'G_WPBAR_ALL_WEAPON': '_get_all_weapons_in_bar',
       'G_SAME_TYPE_WEAPON_EQUIPPED_POS_BY_ITEMID': 'get_same_type_weapon_equipped_pos_by_itemid',
       'E_SWITCHING': ('_switch_cur_weapon', 10),
       'E_FINISH_SWITCH_GUN': '_finish_switch_weapon',
       'E_SIMU_WEAPON_DATA_CHANGED': ('_on_weapon_changed', -10),
       'E_WEAPON_DATA_CHANGED': ('_on_weapon_changed', -10),
       'E_WEAPON_DATA_SWITCHED': ('_on_weapon_data_switched', -10),
       'E_ON_PICK_UP_WEAPON': 'on_pick_up_weapon',
       'G_WPBAR_CUR_WEAPON_POS': ('_get_cur_weapon_pos', -10),
       'G_WPBAR_CUR_GUN_POS': ('_get_cur_gun_pos', -10),
       'G_BULLET_NUM': '_get_bullet_num',
       'G_ATTACHMENT_ATTR': '_get_attachment_attr',
       'G_AIM_LENS_TYPE': '_get_cnt_aim_lens_type',
       'G_LAST_WEAPON_POS': '_get_last_weapon_pos',
       'E_AGONY': '_on_agony',
       'E_SWITCH_LAST_GUN': '_switch_to_last_pos',
       'E_LEAVE_STATE': '_on_leave_state',
       'E_CTRL_SWIM': '_swim_set_empty_hand',
       'E_EQUIP_PARACHUTE': '_set_empty_hand',
       'E_SET_EMPTY_HAND': '_set_empty_hand',
       'E_WEAPON_BULLET_MAX_CHG': 'weapon_bullet_max_change',
       'E_BUFF_ADD_DATA': ('_update_buff_count', 10),
       'E_BUFF_DEL_DATA': ('_update_buff_count', 10),
       'E_SET_WEAPON_ENABLE': '_set_weapon_enable',
       'E_ALL_WEAPON_ENABLE': '_set_all_weapon_enable',
       'E_TRY_RESTORE_CUR_WEAPON': '_try_restore_cur_weapon',
       'G_SCOPE_TIMES': '_get_scope_times',
       'E_CHANGE_SCOPE_TIMES': '_change_scope_times'
       }
    EMPTY_HAND_STATUS = [
     ST_SWIM, ST_PARACHUTE, ST_DOWN_TRANSMIT_STAND, ST_MECHA_DRIVER, ST_MECHA_PASSENGER, ST_DOWN, ST_MECHA_BOARDING, status_config.ST_VEHICLE_GUNNER]
    LEAVE_STATUS = [ST_SWIM, ST_MECHA_DRIVER, ST_MECHA_PASSENGER, status_config.ST_VEHICLE_GUNNER, ST_DOWN]
    SYNC_SCOPE_TIMES_MIN_INTERVAL = 0.07

    def __init__(self):
        super(ComWeaponBarClient, self).__init__()
        self._cur_pos = PART_WEAPON_POS_NONE
        self.sd.ref_wp_bar_cur_weapon = None
        self._last_weapon_pos = PART_WEAPON_POS_NONE
        self._cur_gun_pos = PART_WEAPON_POS_NONE
        self._is_avatar = False
        self.mp_weapons = {}
        self.sd.ref_wp_bar_mp_weapons = self.mp_weapons
        self.player_attr = {}
        self.buff_count = {}
        self._scope_data = {}
        self._prev_sync_scope_times_time = 0
        return

    @property
    def cur_pos(self):
        return self._cur_pos

    @cur_pos.setter
    def cur_pos(self, value):
        self._cur_pos = value
        self.sd.ref_wp_bar_cur_pos = value
        self.sd.ref_wp_bar_cur_weapon = self.mp_weapons.get(value)

    def destroy(self):
        self.sd.ref_wp_bar_cur_weapon = None
        for wp in six.itervalues(self.mp_weapons):
            wp and wp.destroy()

        self.mp_weapons = {}
        self.sd.ref_wp_bar_mp_weapons = {}
        self.player_attr = {}
        self.buff_count = {}
        super(ComWeaponBarClient, self).destroy()
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComWeaponBarClient, self).init_from_dict(unit_obj, bdict)
        self.cur_pos = bdict.get('wp_bar_cur_pos', PART_WEAPON_POS_NONE)
        self._cur_gun_pos = bdict.get('wp_bar_cur_gun_pos', PART_WEAPON_POS_NONE)
        self._last_weapon_pos = bdict.get('wp_bar_last_pos', PART_WEAPON_POS_NONE)
        self._scope_data = bdict.get('scope_data', {})
        self.init_buff_count(bdict.get('buff_data', {}))
        self._is_avatar = self.is_unit_obj_type('LAvatar')

    def init_buff_count(self, buff_data):
        buff_count = self.buff_count
        from common.cfg import confmgr
        for buff_info in six.itervalues(buff_data):
            for buff_id in buff_info:
                if buff_id in buff_count:
                    buff_count[buff_id] += 1
                elif confmgr.get('c_buff_data', str(buff_id), 'ExtInfo', 'buff_info', default=0) == 1:
                    buff_count[buff_id] = 1

        self.init_player_attr()

    def init_player_attr(self):
        player_attr = {}
        from common.cfg import confmgr
        for buff_id, count in six.iteritems(self.buff_count):
            buff_info = confmgr.get('c_buff_info', '{0}_{1}'.format(buff_id, count), default={})
            for key, value in six.iteritems(buff_info):
                player_attr[key] = player_attr.get(key, 0) + value

        self.player_attr = player_attr
        for wp in six.itervalues(self.mp_weapons):
            wp.set_player_attr(player_attr)

    def _update_buff_count(self, buff_key, buff_id, *args):
        count = self.ev_g_get_buff_cnt(buff_key, buff_id)
        if self.buff_count.get(buff_id, 0) != count:
            self.buff_count[buff_id] = count
            self.init_player_attr()

    def on_init_complete(self):
        self.init_obj()
        if self.cur_pos == PART_WEAPON_POS_NONE:
            self.send_event('E_TRY_SWITCH', PART_WEAPON_POS_NONE, False)
        self.send_event('E_WPBAR_INIT')

    def reset(self):
        self.send_event('E_CHECK_REMOVE_GUN_SHIELD')
        self.cur_pos = PART_WEAPON_POS_NONE
        self.mp_weapons = {}
        self.sd.ref_wp_bar_mp_weapons = self.mp_weapons

    def _set_weapon_enable(self, wp_pos, enable):
        wp = self.mp_weapons.get(wp_pos)
        if wp is None:
            return
        else:
            wp.set_enable(enable)
            return

    def _set_all_weapon_enable(self, enable):
        for wp_pos in self.POS_ARR:
            self._set_weapon_enable(wp_pos, enable)

    def init_obj(self):
        for i, wp_pos in enumerate(self.POS_ARR):
            self.load_weapon_obj(wp_pos, self.ev_g_weapon_data(wp_pos))

    def check_gun_pos(self):
        if self._cur_gun_pos in self.mp_weapons:
            if self.cur_pos not in self.mp_weapons:
                self.send_event('E_TRY_SWITCH', self._cur_gun_pos, True)
            elif self.cur_pos != self._cur_gun_pos and self.cur_pos in MAIN_WEAPON_LIST:
                self._cur_gun_pos = self.cur_pos
            return
        if self.cur_pos in self.mp_weapons and self.cur_pos in MAIN_WEAPON_LIST:
            self._cur_gun_pos = self.cur_pos
            return
        self._cur_gun_pos = PART_WEAPON_POS_NONE
        for pos in MAIN_WEAPON_LIST:
            if pos in self.mp_weapons:
                self._cur_gun_pos = pos
                break

        if self.cur_pos not in self.mp_weapons:
            self.send_event('E_TRY_SWITCH', self._cur_gun_pos, True)

    def load_weapon_obj(self, wp_pos, wp_data):
        if not wp_data:
            if wp_pos in self.mp_weapons:
                self.unload_weapon(wp_pos)
                if self.cur_pos == wp_pos:
                    self.check_gun_pos()
                    return True
            return False
        else:
            clss = self.MP_CLS.get(wp_pos)
            if not clss:
                return False
            wp_obj = clss(wp_data)
            wp_obj.set_pos(wp_pos)
            wp_obj.set_player_attr(self.player_attr)
            wp_obj.set_host_player(self)
            self.send_event('E_CHECK_REMOVE_GUN_SHIELD')
            self.mp_weapons[wp_pos] = wp_obj
            self.sd.ref_wp_bar_cur_weapon = self.mp_weapons.get(self.cur_pos)
            if global_data.player and global_data.player.id == self.unit_obj.id:
                attr = wp_obj.get_attachment_attr(ATTACHEMNT_AIM_POS)
                if attr and 'cModel' in attr:
                    model_res = attr['cModel']
                    fashion = wp_obj.get_fashion()
                    from logic.gcommon.item.item_const import FASHION_POS_SUIT
                    fashion_id = fashion.get(FASHION_POS_SUIT, None)
                    if fashion_id is not None:
                        from logic.gutils import dress_utils
                        tmp_right_res, tmp_left_res = dress_utils.get_weapon_skin_res(fashion_id)
                        model_res = tmp_right_res.replace('h.gim', 'aim/h.gim')
                    CamAimModelPreload(model_res, attr)
            if self.cur_pos == wp_pos:
                self.send_event('E_TRY_SWITCH', wp_pos, False, is_init=True)
                self.send_event('E_CHECK_ADD_GUN_SHIELD')
                return True
            self.send_event('E_CHECK_ADD_GUN_SHIELD')
            return False

    def weapon_bullet_max_change(self, weapon_pos, cur_bullet_max_cnt):
        wp = self.mp_weapons.get(weapon_pos)
        if not wp:
            return
        wp.set_bullet_cap(cur_bullet_max_cnt)
        pos_list = wp.get_related_weapon_pos() or (weapon_pos,)
        for pos in pos_list:
            self.send_event('E_WEAPON_DATA_CHANGED', pos)

    def _get_cur_weapon(self):
        return self.get_weapon_by_pos(self.cur_pos)

    def _get_cur_weapon_pos(self):
        return self.cur_pos

    def _get_cur_gun_pos(self):
        return self._cur_gun_pos

    def unload_weapon(self, wp_pos):
        if wp_pos in self.mp_weapons:
            self.mp_weapons.pop(wp_pos)

    def get_weapon_by_pos(self, wp_pos):
        return self.mp_weapons.get(wp_pos, None)

    def _get_all_weapons_in_bar(self):
        return self.mp_weapons

    def get_same_type_weapon_equipped_pos_by_itemid(self, item_id):
        for pos, obj in six.iteritems(self.mp_weapons):
            obj_id = obj.get_item_id()
            if iutil.is_same_type_weapon(obj_id, item_id):
                return (pos, obj_id)

        return (-1, None)

    def _get_bullet_num(self):
        if self.cur_pos in [PART_WEAPON_POS_MAIN1, PART_WEAPON_POS_MAIN2, PART_WEAPON_POS_MAIN3]:
            weapon = self._get_cur_weapon()
            if weapon:
                return weapon.get_bullet_num()
        return 0

    def _get_cnt_aim_lens_type(self):
        attachment = self._get_attachment_attr(1)
        if attachment:
            return attachment.get('iType')
        else:
            return None

    def _get_attachment_attr(self, pos):
        if self.cur_pos in [PART_WEAPON_POS_MAIN_DF, PART_WEAPON_POS_MAIN1, PART_WEAPON_POS_MAIN2, PART_WEAPON_POS_MAIN3]:
            weapon = self._get_cur_weapon()
            if weapon:
                return weapon.get_attachment_attr(pos)
        return None

    def _get_last_weapon_pos(self):
        return self._last_weapon_pos

    def _on_agony(self, *args):
        if self.cur_pos != PART_WEAPON_POS_NONE:
            self.send_event('E_CHECK_REMOVE_GUN_SHIELD')
            self._last_weapon_pos = self.cur_pos
            self.cur_pos = PART_WEAPON_POS_NONE
            self.send_event('E_TRY_SWITCH', PART_WEAPON_POS_NONE, False)

    def _on_weapon_changed(self, wp_pos):
        if wp_pos is None:
            pos = six_ex.keys(self.MP_CLS)
        else:
            pos = [
             wp_pos]
        changed = False
        for wp_pos in pos:
            wp_data = self.ev_g_weapon_data(wp_pos)
            wp_obj = self.mp_weapons.get(wp_pos)
            if wp_data and wp_obj and wp_data is wp_obj.get_data():
                continue
            changed = changed or self.load_weapon_obj(wp_pos, self.ev_g_weapon_data(wp_pos))

        if changed:
            self.send_event('E_WEAPON_DATA_CHANGED_SUCCESS', wp_pos)
        return

    def _on_weapon_data_switched(self, pos1, pos2):
        if pos1 not in MAIN_WEAPON_LIST or pos2 not in MAIN_WEAPON_LIST:
            return
        self.send_event('E_CHECK_REMOVE_GUN_SHIELD')
        if self.cur_pos == pos1:
            self.cur_pos = pos2
            self._cur_gun_pos = pos2
        elif self.cur_pos == pos2:
            self.cur_pos = pos1
            self._cur_gun_pos = pos1
        wp1 = self.mp_weapons.get(pos1)
        if pos2 in self.mp_weapons:
            wp2 = self.mp_weapons[pos2]
            wp2.set_pos(pos1)
            self.mp_weapons[pos1] = wp2
            del self.mp_weapons[pos2]
        elif wp1:
            del self.mp_weapons[pos1]
        if wp1:
            self.mp_weapons[pos2] = wp1
            wp1.set_pos(pos2)
        self.sd.ref_wp_bar_cur_weapon = self.mp_weapons.get(self.cur_pos)
        self.send_event('E_CHECK_ADD_GUN_SHIELD')

    def on_pick_up_weapon(self, wp_pos, is_throw, switch=True):
        if not switch:
            return
        if not is_throw and self.cur_pos == PART_WEAPON_POS_NONE and wp_pos in self.mp_weapons:
            if self.ev_g_is_in_any_state(self.EMPTY_HAND_STATUS):
                return
            self.send_event('E_TRY_SWITCH', wp_pos, False)

    def _switch_cur_weapon(self, pos):
        if pos == self.cur_pos:
            self.send_event('E_WPBAR_REFRESH', pos)
            return
        self.send_event('E_CHECK_REMOVE_GUN_SHIELD')
        self._last_weapon_pos = self.cur_pos
        self.cur_pos = pos
        if pos in MAIN_WEAPON_LIST:
            self._cur_gun_pos = pos
        if not (self.ev_g_get_state(ST_SWIM) and pos == 0):
            self.send_event('E_WPBAR_SWITCH_CUR', pos)
        self.send_event('E_ACTION_SWITCHING', pos, self._last_weapon_pos)
        if self.ev_g_get_state(ST_SWIM):
            self._swim_set_empty_hand()
        self.send_event('E_SWITCH_WEAPON_COMPONENT', pos)
        self.send_event('E_WPBAR_SWITCHED', pos)
        self.send_event('E_CHECK_ADD_GUN_SHIELD')

    def _finish_switch_weapon(self, *args):
        self.send_event('E_WPBAR_SWITCH_CUR', self.cur_pos)
        self.send_event('E_WPBAR_SWITCHED', self.cur_pos)

    def update_clothing_attr(self, clothing):
        if G_IS_CLIENT and clothing is not None:
            import common.cfg.confmgr as confmgr
            total_speed_rate = 0
            for value in six.itervalues(clothing):
                item_id = value.get('item_id', None)
                if item_id is not None:
                    clothing_conf = confmgr.get('armor_config', str(item_id))
                    if clothing_conf:
                        total_speed_rate += clothing_conf.get('fSpdRate', 0)

            self.send_event('E_SPD_RATE_CHANGE', total_speed_rate)
        return

    def _on_leave_state(self, leave_state, new_st=None):
        water_status = self.sd.ref_water_status
        if water_status != water_const.WATER_DEEP_LEVEL or new_st == status_config.ST_SKATE or leave_state == status_config.ST_SWIM:
            if isinstance(leave_state, (set, list, tuple)):
                for status in self.LEAVE_STATUS:
                    if status in leave_state:
                        return self._switch_to_last_pos()

                if ST_MECHA_DRIVER in self.LEAVE_STATUS:
                    self.ev_g_cancel_state(ST_SWITCH)
            else:
                if leave_state == ST_DOWN:
                    self.send_event('E_CTRL_STAND', is_break_run=False, ignore_col=True, is_saved=True)
                if leave_state in self.LEAVE_STATUS:
                    self._switch_to_last_pos()
                if ST_MECHA_DRIVER == leave_state:
                    self.ev_g_cancel_state(ST_SWITCH)

    def _switch_to_last_pos(self, *args, **kwargs):
        if self._last_weapon_pos != self.cur_pos:
            switch_status = kwargs.get('switch_status', True)
            if self._last_weapon_pos in self.mp_weapons:
                self.send_event('E_TRY_SWITCH', self._last_weapon_pos, switch_status)
            elif self._last_weapon_pos == PART_WEAPON_POS_NONE:
                self.send_event('E_TRY_SWITCH', self.cur_pos, switch_status)
            else:
                self.check_gun_pos()

    def _swim_set_empty_hand(self):
        self._set_empty_hand(False)

    def _set_empty_hand(self, switch_status=True):
        self.send_event('E_TRY_SWITCH', PART_WEAPON_POS_NONE, switch_status=switch_status)

    def _on_vehicle(self, *args):
        if True or self.ev_g_get_state(ST_MECHA_DRIVER):
            self._set_empty_hand()

    def do_sa_switch_log(self, pos_pre, pos_cur):
        _wp_0 = self.mp_weapons.get(self._last_weapon_pos) if self._last_weapon_pos else None
        _wp_1 = self.mp_weapons.get(self.cur_pos) if self.cur_pos else None
        _item_0 = _wp_0.get_item_id() if _wp_0 else 0
        _item_1 = _wp_1.get_item_id() if _wp_1 else 0
        self.unit_obj.get_owner().sa_log_switch_item(_item_0, _item_1)
        return

    def _try_restore_cur_weapon(self):
        if self.cur_pos > 0:
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', (bcast.E_TRY_SWITCH, (self.cur_pos, True)), False, False, True)

    def _get_scope_times(self, item_id):
        return self._scope_data.get(item_id, 0)

    def _change_scope_times(self, item_id, value):
        if self._get_scope_times(item_id) == value:
            return
        self._scope_data[item_id] = value
        if self._is_avatar:
            if get_time() - self._prev_sync_scope_times_time > self.SYNC_SCOPE_TIMES_MIN_INTERVAL:
                self.send_event('E_CALL_SYNC_METHOD', 'change_scope_times', (item_id, value), True)
                self._prev_sync_scope_times_time = get_time()
        if global_data.cam_lplayer is self.unit_obj:
            if not self._is_avatar:
                global_data.emgr.update_aim_scope_times_event.emit(item_id, value)
            part_cam = global_data.game_mgr.scene.get_com('PartCamera')
            if part_cam and part_cam.get_cur_camera_aim_scope_id() == item_id:
                global_data.emgr.update_camera_viewer_event.emit()
                global_data.emgr.tell_update_camera_fov_event.emit()
                global_data.emgr.refresh_cur_aim_scope_times_event.emit(item_id, value)