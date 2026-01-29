# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComAtkThrowTrackGun.py
from __future__ import absolute_import
END_STRIP_SFX = 'effect/fx/weapon/other/touzhi_biaoshi.sfx'
from logic.gcommon.cdata.status_config import ST_SHOOT
from .ComAtkGun import ComAtkGun
UPDATE_TIME = 2

class ComAtkThrowTrackGun(ComAtkGun):
    BIND_EVENT = dict(ComAtkGun.BIND_EVENT)
    BIND_EVENT.update({'E_SUCCESS_RIGHT_AIM': 'on_right_aim',
       'E_FINISH_QUIT_RIGHT_AIM': 'on_quit_right_aim'
       })

    def __init__(self):
        super(ComAtkThrowTrackGun, self).__init__()
        self.throw_track_visible = False

    def on_right_aim(self):
        if global_data.player and self.unit_obj != global_data.player.logic:
            return
        position = self.get_fire_pos()
        if not self.cur_wp:
            return
        from common.cfg import confmgr
        conf = confmgr.get('grenade_config', str(self.cur_wp.iType))
        speed = conf['fSpeed']
        g = -conf.get('fGravity', 98)
        up_angle = conf.get('fUpAngle', 0)
        mass = conf.get('fMass', 1.0)
        linear_damp = conf.get('fLinearDamp', 0.0)
        self.send_event('E_SHOW_PARABOLA_TRACK', END_STRIP_SFX, position, speed, g, up_angle, mass=mass, linear_damping=linear_damp)
        self.throw_track_visible = True
        self.need_update = True

    def on_quit_right_aim(self):
        if global_data.player and self.unit_obj != global_data.player.logic:
            return
        self.need_update = False
        self.send_event('E_HIDE_PARABOLA_TRACK')
        self.throw_track_visible = False

    def tick(self, delta):
        if not self.need_update:
            return
        position = self.get_fire_pos()
        if not self.ev_g_status_check_pass(ST_SHOOT):
            if self.throw_track_visible:
                self.send_event('E_HIDE_PARABOLA_TRACK')
                self.throw_track_visible = False
        else:
            if not self.throw_track_visible:
                self.send_event('E_SET_PARA_LINE_VISIBLE', True)
                self.throw_track_visible = True
            self.send_event('E_UPDATE_PARABOLA_TRACK', position)

    def get_gun_auxiliary_component(self, weapon):
        cur_com_list = super(ComAtkThrowTrackGun, self).get_gun_auxiliary_component(weapon)
        cur_com_list.append('ComParabolaTrackAppearance')
        return cur_com_list