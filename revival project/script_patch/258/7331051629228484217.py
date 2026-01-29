# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_meow_postbox/ComMeowPostboxAppearance.py
from __future__ import absolute_import
from logic.gcommon.component.client.ComBaseModelAppearance import ComBaseModelAppearance
from mobile.common.EntityManager import EntityManager
import world
import math3d
from logic.gcommon.const import NEOX_UNIT_SCALE
from common.cfg import confmgr

class ComMeowPostboxAppearance(ComBaseModelAppearance):
    TRI_RADIUS = 5
    BIND_EVENT = ComBaseModelAppearance.BIND_EVENT.copy()
    BIND_EVENT.update({'G_CHECK_ENTER_CONSOLOE_ZONE': '_check_enter_zone'
       })

    def __init__(self):
        super(ComMeowPostboxAppearance, self).__init__()
        self._trigger_radius = self.TRI_RADIUS * NEOX_UNIT_SCALE
        self.lplayer = None
        self._sub_sfx_id = None
        self.process_event(True)
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'scene_player_setted_event': self.on_player_setted,
           'on_meow_coin_change_event': self._meow_coin_change
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def destroy(self):
        super(ComMeowPostboxAppearance, self).destroy()
        self.process_event(False)

    def init_from_dict(self, unit_obj, bdict):
        super(ComMeowPostboxAppearance, self).init_from_dict(unit_obj, bdict)
        self.on_player_setted(global_data.cam_lplayer)

    def on_player_setted(self, lplayer):
        if lplayer is None:
            return
        else:
            self.lplayer = lplayer
            self.open_meow_sfx()
            return

    def get_model_info(self, unit_obj, bdict):
        pos = bdict.get('position', [0, 0, 0])
        rot = bdict.get('rot', [0, 0, 0, 1])
        model_path = confmgr.get('script_gim_ref')['item_meow_postbox']
        return (
         model_path, None, (pos, rot, bdict))

    def on_load_model_complete(self, model, userdata):
        import math3d
        import collision
        import render
        import game3d
        pos, rot = userdata[0], userdata[1]
        pos = math3d.vector(pos[0], pos[1], pos[2])
        model.world_position = pos
        from logic.gcommon.common_utils.building_utils import get_bounding_box_slope_rot_mat
        rot_mat = get_bounding_box_slope_rot_mat(model, 1.0)
        model.rotation_matrix = rot_mat
        model.active_collision = True
        global_data.emgr.scene_add_console.emit(self.unit_obj.id, self.unit_obj.get_owner())
        self.open_meow_sfx()

    def on_model_destroy(self):
        global_data.emgr.scene_del_console.emit(self.unit_obj.id)
        self._sub_sfx_id and global_data.sfx_mgr.remove_sfx_by_id(self._sub_sfx_id)
        self._sub_sfx_id = None
        return

    def _check_enter_zone(self, pos):
        if self.model:
            model_pos = self.model.world_position
            lpos = pos - model_pos
            length = lpos.length
            if length <= self._trigger_radius:
                return (True, length)
        return (False, None)

    def _show_meow_sfx(self):
        if not self.lplayer:
            return
        from logic.gcommon.cdata import meow_capacity_config
        _, _, mail_box_times = self.lplayer.ev_g_meow_mail_box_info() or (0, 0, 0)
        is_show = True
        if meow_capacity_config.meow_mail_max_times - mail_box_times <= 0:
            is_show = False
        elif self.lplayer.ev_g_have_sent_mail(self.unit_obj.id):
            is_show = False
        return is_show

    def open_meow_sfx(self):
        if self._show_meow_sfx():
            if not self._sub_sfx_id:
                self.create_meow_sfx()
        elif self._sub_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self._sub_sfx_id)
            self._sub_sfx_id = None
        return

    def create_meow_sfx(self):

        def create_sfx_cb(sfx):
            pass

        self._sub_sfx_id and global_data.sfx_mgr.remove_sfx_by_id(self._sub_sfx_id)
        self._sub_sfx_id = global_data.sfx_mgr.create_sfx_on_model('effect/fx/scenes/common/map/mao_youxiang_01.sfx', self.model, 'fx_root', on_create_func=create_sfx_cb)

    def _meow_coin_change(self):
        self.open_meow_sfx()