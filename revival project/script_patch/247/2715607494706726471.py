# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_mecha_effect/ComMechaEffect8501.py
from __future__ import absolute_import
import time
from logic.gcommon.component.UnitCom import UnitCom
from common.cfg import confmgr
FIRE_CD_TIME = 0.1
SFX_BULLET_SOCKET = 'fx_danke'
SFX_FIRE_SOCKET = 'fx_jiatelin_kaihuo'
SFX_BULLET_PATH = 'effect/fx/robot/autobot/autobot_jiatelin_danke.sfx'
SFX_FIRE_PATH = 'effect/fx/weapon/tujibuqiang/tujibuqiang_muzzleflash.sfx'
SHOOT_ACTION_LST = [
 'shoot', 'shoot_b', 'shoot_bl', 'shoot_br', 'shoot_f', 'shoot_fl', 'shoot_fr', 'shoot_frozen']

class ComMechaEffect8501(UnitCom):
    BIND_EVENT = {'E_MODEL_LOADED': 'on_model_loaded'
       }

    def init_from_dict(self, unit_obj, bdict):
        super(ComMechaEffect8501, self).init_from_dict(unit_obj, bdict)
        self._model = None
        self._fire_sfx_time = 0
        return

    def on_model_loaded(self, model):
        self._model = model
        self._init_shoot_action_sfx()

    def _init_shoot_action_sfx(self):
        mecha_id = self.sd.ref_mecha_id
        guns = confmgr.get('mecha_conf', 'MechaConfig', 'Content', str(mecha_id), 'guns', default=[])
        if not guns:
            return
        weapon_id = guns[0]
        conf = confmgr.get('firearm_res_config', str(weapon_id), default={})
        if not conf:
            return
        fire_sockets = conf.get('cBindPointEmission', [])
        fire_socket = ''
        if fire_sockets:
            fire_socket = fire_sockets[0]
        fire_sfx_path = conf.get('cSfx', '')
        bullet_socket = conf.get('cBindPointBullet', '')
        bullet_sfx_path = conf.get('cSfxBullet', '')

        def sfx_callback(*args):
            if not self._model or not self._model.valid:
                return
            if time.time() - self._fire_sfx_time < FIRE_CD_TIME:
                return
            self._fire_sfx_time = time.time()
            if fire_sockets and fire_sfx_path:
                global_data.sfx_mgr.create_sfx_on_model(fire_sfx_path, self._model, fire_socket)
            if bullet_socket and bullet_sfx_path:
                global_data.sfx_mgr.create_sfx_on_model(bullet_sfx_path, self._model, bullet_socket)

        for action in SHOOT_ACTION_LST:
            self._model.register_anim_key_event(action, 'start', sfx_callback)

    def destroy(self):
        self._model = None
        return