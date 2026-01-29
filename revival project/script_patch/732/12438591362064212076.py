# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComNBombDeviceAppearance.py
from __future__ import absolute_import
from .ComBaseModelAppearance import ComBaseModelAppearance
import math3d
import math
import collision
from logic.gutils.judge_utils import get_player_group_id
from logic.gcommon.const import NEOX_UNIT_SCALE
E_NBOMB_TARGET_LOW_HP = 0.5

class ComNBombDeviceAppearance(ComBaseModelAppearance):
    BIND_EVENT = ComBaseModelAppearance.BIND_EVENT.copy()
    BIND_EVENT.update({'E_NBOMB_HP_PERCENT_CHANGE': 'on_nbomb_hp_percent_change',
       'E_UPDATE_NBOMB_STATUS': 'create_alert_sfx',
       'E_HEALTH_HP_CHANGE': '_on_hp_changed'
       })
    AFFECT_RANGE_BASIC = 54 * NEOX_UNIT_SCALE

    def __init__(self):
        super(ComNBombDeviceAppearance, self).__init__()
        self.faction_id = None
        self.affect_range = self.AFFECT_RANGE_BASIC
        self.nbomb_pos = None
        self.col_offset = None
        self.sky_resume_sfx_id = None
        self.bomb_sfx_id = None
        self.reset_sfx_id()
        self.process_event(True)
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComNBombDeviceAppearance, self).init_from_dict(unit_obj, bdict)
        pos = bdict.get('position')
        self.faction_id = bdict.get('faction_id')
        self.affect_range = bdict.get('affect_range', self.AFFECT_RANGE_BASIC)
        self.nbomb_pos = math3d.vector(*pos)
        self.hp_status = bdict.get('hp_status')
        self.create_alert_sfx(self.hp_status)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'nbomb_play_sky_resume_sfx': self.create_sky_resume_sfx,
           'scene_camera_player_setted_event': self.refresh_alert_sfx
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def is_teammate(self):
        if global_data.cam_lplayer:
            return global_data.cam_lplayer.ev_g_group_id() == self.faction_id
        return get_player_group_id() == self.faction_id

    def reset_sfx_id(self):
        self.guangzhu_sfx_id = None
        self.sky_break_sfx_id = None
        self.alert_sfx_id = None
        return

    def get_model_info(self, unit_obj, bdict):
        model_path = 'model_new/items/items/bombdevice.gim'
        return (
         model_path, None, None)

    def on_load_model_complete(self, model, user_data):
        model.world_position = self.nbomb_pos
        self.create_bind_sfxs()

    def destroy(self):
        self.remove_bind_sfxs()
        self.process_event(False)
        super(ComNBombDeviceAppearance, self).destroy()

    def create_bind_sfxs(self):
        if not self.guangzhu_sfx_id:
            screen_sfx_path = 'effect/fx/niudan/hedanwanfa/hd_xk_guangzhu_zise.sfx'
            self.guangzhu_sfx_id = global_data.sfx_mgr.create_sfx_in_scene(screen_sfx_path, self.nbomb_pos, on_create_func=self.create_sky_break_sfx)

    def create_sky_break_sfx(self, *args):
        if not self.sky_break_sfx_id:
            screen_sfx_path = 'effect/fx/niudan/hedanwanfa/hd_sky_start.sfx'
            self.sky_break_sfx_id = global_data.sfx_mgr.create_sfx_in_scene(screen_sfx_path, self.nbomb_pos)

    def remove_sky_break_sfx(self):
        if self.sky_break_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.sky_break_sfx_id)
            self.sky_break_sfx_id = None
        return

    def create_sky_resume_sfx(self):
        self.remove_sky_break_sfx()
        if not self.sky_resume_sfx_id:
            screen_sfx_path = 'effect/fx/niudan/hedanwanfa/hd_sky_end.sfx'
            self.sky_resume_sfx_id = global_data.sfx_mgr.create_sfx_in_scene(screen_sfx_path, self.nbomb_pos, on_remove_func=self.remove_sky_resume_sfx)

    def remove_sky_resume_sfx(self, *args):
        if self.sky_resume_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.sky_resume_sfx_id)
            self.sky_resume_sfx_id = None
        return

    def create_alert_sfx(self, status):
        self.hp_status = status
        YELLOW_SFX_PATH = 'effect/fx/niudan/hedanwanfa/hd_quyu_yellow.sfx'
        RED_SFX_PATH = 'effect/fx/niudan/hedanwanfa/hd_quyu_red.sfx'
        BLUE_SFX_PATH = 'effect/fx/niudan/hedanwanfa/hd_quyu_blue.sfx'
        self.remove_alert_sfx()
        sfx_path = BLUE_SFX_PATH
        if status == 'hp_unchange':
            sfx_path = YELLOW_SFX_PATH
        elif status == 'hp_reduce':
            sfx_path = RED_SFX_PATH if self.is_teammate() else BLUE_SFX_PATH
        else:
            sfx_path = BLUE_SFX_PATH if self.is_teammate() else RED_SFX_PATH

        def _on_create_func(sfx_obj):
            sfx_scale = self.affect_range / self.AFFECT_RANGE_BASIC
            sfx_obj.scale = math3d.vector(sfx_scale, sfx_scale, sfx_scale)

        self.alert_sfx_id = global_data.sfx_mgr.create_sfx_in_scene(sfx_path, self.nbomb_pos, on_create_func=_on_create_func)

    def remove_alert_sfx(self):
        if self.alert_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.alert_sfx_id)
        self.alert_sfx_id = None
        return

    def refresh_alert_sfx(self, *args):
        self.create_alert_sfx(self.hp_status)

    def create_nbomb_sfx(self):
        if not self.bomb_sfx_id:
            from logic.gutils.screen_effect_utils import create_screen_effect_directly
            screen_sfx_path = 'effect/fx/niudan/hedanwanfa/hd_boom_pm_01.sfx'
            self.bomb_sfx_id = create_screen_effect_directly(screen_sfx_path, on_remove_func=self.remove_bomb_sfx)

    def remove_bomb_sfx(self, *args):
        print ('\xe5\x88\xa0\xe9\x99\xa4\xe7\x88\x86\xe7\x82\xb8\xe7\x89\xb9\xe6\x95\x88', self.bomb_sfx_id)
        if self.bomb_sfx_id:
            global_data.sfx_mgr.remove_sfx_by_id(self.bomb_sfx_id)
        self.bomb_sfx_id = None
        return

    def remove_bind_sfxs(self):
        for sfx_id in [self.alert_sfx_id, self.guangzhu_sfx_id, self.sky_break_sfx_id]:
            sfx_id and global_data.sfx_mgr.remove_sfx_by_id(sfx_id)

        self.reset_sfx_id()

    def on_nbomb_hp_percent_change(self, hp_percent):
        pass