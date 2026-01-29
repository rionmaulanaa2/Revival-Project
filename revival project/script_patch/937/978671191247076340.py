# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_appearance/ComMechaBackWeapon8018.py
from __future__ import absolute_import
import six
from six.moves import range
import weakref
import world
import math3d
from logic.gcommon.component.UnitCom import UnitCom
from logic.gcommon.const import PART_WEAPON_POS_MAIN1
from logic.gutils.mecha_skin_utils import DEFAULT_RES_KEY
from common.utils import timer
MODEL_SHADER_CTRL_SET_ENABLE = hasattr(world.model, 'set_inherit_parent_shaderctrl')

class ComMechaBackWeapon8018(UnitCom):
    BIND_EVENT = {'E_MODEL_LOADED': '_on_model_loaded',
       'E_ON_SKIN_SUB_MODEL_LOADED': 'on_skin_sub_model_loaded',
       'E_WEAPON_DATA_CHANGED': 'weapon_data_changed',
       'E_REFRESH_CUR_WEAPON_BULLET': 'refresh_cur_weapon_bullet',
       'G_FEATHER_INFO_8018': 'get_feather_info',
       'E_BEGIN_RELOAD': 'begin_reload'
       }
    MAX_BULLET = 10

    def __init__(self):
        super(ComMechaBackWeapon8018, self).__init__()
        self.weapon_pos = PART_WEAPON_POS_MAIN1
        self._sub_sfx_ids = {}
        self._back_model = []
        self.process_event(True)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {}
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_from_dict(self, unit_obj, bdict):
        super(ComMechaBackWeapon8018, self).init_from_dict(unit_obj, bdict)
        self.mecha_id = bdict['mecha_id']
        self._back_model = []
        self._visible_id_lst = []
        self.l_each_hide_num = 0
        self.r_each_hide_num = self.MAX_BULLET / 2
        self.anim_reload_timer = None
        return

    def _on_model_loaded(self, model):
        pass

    def on_skin_sub_model_loaded(self):
        if DEFAULT_RES_KEY not in self.sd.ref_socket_res_agent.model_res_map:
            return
        sub_model_list = self.sd.ref_socket_res_agent.model_res_map[DEFAULT_RES_KEY]
        for sub_model in sub_model_list:
            self._back_model.append(weakref.ref(sub_model))
            sub_model.set_submesh_visible(0, True)

        self._visible_id_lst = []
        self.weapon_bullet_changed(self.weapon_pos)

    def get_feather_info(self):
        return (
         self.l_each_hide_num, self.r_each_hide_num, self.MAX_BULLET)

    def _feather_show(self, need_show_num):
        self._visible_id_lst = []
        r_index = self.MAX_BULLET // 2
        each_hide_num = (self.MAX_BULLET - need_show_num) // 2
        is_even_num = need_show_num % 2
        fired_socket_index = self.ev_g_socket_index(self.weapon_pos) % 2
        l_num_off = (1 - fired_socket_index) * is_even_num
        r_num_off = fired_socket_index * is_even_num
        l_each_hide_num = each_hide_num + l_num_off
        r_each_hide_num = each_hide_num + r_index + r_num_off
        self.l_each_hide_num = l_each_hide_num
        self.r_each_hide_num = r_each_hide_num
        for i in range(len(self._back_model)):
            model = self._back_model[i]()
            if model and model.valid:
                if i < r_index:
                    is_show = False if i < l_each_hide_num else True
                else:
                    is_show = False if i < r_each_hide_num else True
                if MODEL_SHADER_CTRL_SET_ENABLE:
                    model.set_inherit_parent_shaderctrl(is_show)
                self._feather_visible(i, model, is_show)
                model.cast_shadow = is_show

        self._visible_id_lst.sort()

    def _feather_model_bind_sfx(self, index, model, sfx, is_visible):
        if is_visible:
            if self._sub_sfx_ids[index][2]:
                model.unbind(sfx)
                self._sub_sfx_ids[index][2] = False
        elif not self._sub_sfx_ids[index][2]:
            model.bind('fx_root', sfx, world.BIND_TYPE_DEFAULT)
            self._sub_sfx_ids[index][2] = True

    def _feather_visible(self, index, model, is_visible):
        if index in self._sub_sfx_ids:
            _sub_sfx_id = self._sub_sfx_ids[index][0]
            sfx = global_data.sfx_mgr.get_sfx_by_id(_sub_sfx_id)
            if sfx:
                self._feather_model_bind_sfx(index, model, sfx, is_visible)
            self._sub_sfx_ids[index][1] = is_visible
            return

        def create_cb(sfx, model=model, index=index):
            self._sub_sfx_ids[index][2] = True
            self._feather_model_bind_sfx(index, model, sfx, self._sub_sfx_ids[index][1])

        self._sub_sfx_ids[index] = [
         0, is_visible, False]
        _sub_sfx_id = global_data.sfx_mgr.create_sfx_on_model('effect/fx/mecha/8018/8018_main_yumao_shader.sfx', model, 'fx_root', on_create_func=create_cb)
        self._sub_sfx_ids[index][0] = _sub_sfx_id

    def clear_all_sfx(self):
        for _sub_sfx_id, _, _ in six.itervalues(self._sub_sfx_ids):
            _sub_sfx_id and global_data.sfx_mgr.remove_sfx_by_id(_sub_sfx_id)

        self._sub_sfx_ids = {}

    def weapon_data_changed(self, pos, *args):
        if pos != PART_WEAPON_POS_MAIN1:
            return
        self.weapon_bullet_changed(pos)

    def refresh_cur_weapon_bullet(self, pos):
        if pos != PART_WEAPON_POS_MAIN1:
            return
        self.weapon_bullet_changed(pos)

    def weapon_bullet_changed(self, weapon_key):
        weapon = self.ev_g_wpbar_get_by_pos(weapon_key)
        cur_bullet = weapon.get_bullet_num()
        show_ratio = weapon.get_show_ratio()
        cur_bullet = min(int(cur_bullet * show_ratio), self.MAX_BULLET)
        self._feather_show(cur_bullet)

    def clear_anim_reload_timer(self):
        self.anim_reload_timer and global_data.game_mgr.get_logic_timer().unregister(self.anim_reload_timer)
        self.anim_reload_timer = None
        return

    def begin_reload(self):
        self.clear_anim_reload_timer()

        def _reload():
            self._feather_show(self.MAX_BULLET)
            self.send_event('E_RESET_CAMP_OUTLINE')

        self.anim_reload_timer = global_data.game_mgr.get_logic_timer().register(func=lambda : _reload(), mode=timer.CLOCK, interval=0.8, times=1)

    def get_back_model(self):
        return self._back_model

    def destroy(self):
        super(ComMechaBackWeapon8018, self).destroy()
        self.clear_anim_reload_timer()
        self.clear_all_sfx()
        mecha_model = self.ev_g_model()
        for model in self._back_model:
            model = model()
            if not model or not model.valid:
                continue
            if mecha_model and mecha_model.valid:
                mecha_model.unbind(model)
            model.destroy()

        self._back_model = []
        self.process_event(False)