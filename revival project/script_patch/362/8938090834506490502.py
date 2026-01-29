# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/com_parachute/ComParachuteMecha.py
from __future__ import absolute_import
from __future__ import print_function
from logic.gcommon.component.UnitCom import UnitCom
import world
import game3d
import math3d
from logic.gutils import mecha_utils
from logic.gcommon.cdata import status_config
DEFAULT_MECHA_ID = 'XXXX'
MECHA_MODEL_DICT = {8001: 'model_new/mecha/8001/8001/l.gim',
   8002: 'model_new/mecha/8002/8002/l.gim'
   }
from logic.gcommon.common_utils import parachute_utils
from logic.gcommon.common_utils.parachute_utils import STATE_FLY, STATE_FLY_TO_LAND, STATE_LAND_LOOP, STATE_COME, STATE_LEAVE
from time import time
MOVE_ANI_DICT = {parachute_utils.CONTROL_STATE_FORWARD: 'fly',
   parachute_utils.CONTROL_STATE_RIGHT: 'fly',
   parachute_utils.CONTROL_STATE_LEFT: 'fly',
   parachute_utils.CONTROL_STATE_NONE: 'fly',
   parachute_utils.CONTROL_STATE_BACK: 'fly_to_land'
   }

class ComParachuteMecha(UnitCom):
    DEFAULT_XML = 'animator_conf/mecha/parachute.xml'
    BIND_EVENT = {'G_PARACHUTE_MECHA_MODEL': '_get_parachute_mecha_model',
       'E_OPEN_PARACHUTE': '_on_parachute_open',
       'E_LAND': '_on_land',
       'E_START_PARACHUTE': '_on_start_parachute_stage',
       'E_MODEL_LOADED': '_on_main_model_loaded',
       'E_PARACHUTE_LAND_EJECT': '_on_parachute_land_eject',
       'E_CHARACTER_ATTR': '_change_character_attr'
       }

    def __init__(self):
        super(ComParachuteMecha, self).__init__()
        self._mecha_model = None
        self._load_tid = None
        self.parachute_mecha_id = None
        self.parachute_mecha_res = None
        self.cnt_move_ani_name = None
        self.load_mecha_callback = None
        self.need_update = False
        self._mecha_animator = None
        self._parachute_state = None
        return

    def init_config(self):
        pass

    def _change_character_attr(self, name, *arg):
        if name == 'animator_info':
            only_active = arg[0]
            if self._mecha_animator:
                print('test--ComParachuteMecha--animator_info--self.unit_obj =', self.unit_obj)
                self._mecha_animator.print_info(active=only_active)

    def _set_parachute_state(self, parachute_state):
        if self._parachute_state == parachute_state:
            return
        self._parachute_state = parachute_state
        if self._mecha_animator:
            self._mecha_animator.SetInt('parachute_state', parachute_state)

    def get_mecha_model_res(self, mecha_id):
        return MECHA_MODEL_DICT.get(mecha_id, MECHA_MODEL_DICT[8001])

    def _on_main_model_loaded(self, *args):
        if self.load_mecha_callback:
            self.load_mecha_callback()
            self.load_mecha_callback = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComParachuteMecha, self).init_from_dict(unit_obj, bdict)
        self.parachute_mecha_id = int(bdict.get('parachute_mecha_id', 0))
        self.parachute_mecha_res = self.get_mecha_model_res(self.parachute_mecha_id)

    def on_load_mecha_model_complete(self, model, *args):
        self._mecha_model = model
        main_model = self.ev_g_model()
        if not main_model:
            self.load_mecha_callback = self.do_on_mecha_model_complete
        else:
            self.do_on_mecha_model_complete()

    def do_on_mecha_model_complete(self):
        from common.animate import animator
        self._mecha_animator = animator.Animator(self.mecha_model, self.DEFAULT_XML, self.unit_obj)
        self._mecha_animator.Load(False)
        self.ev_g_status_try_trans(status_config.ST_PARACHUTE)
        self.scene.add_object(self.mecha_model)
        start_pos, end_pos = self.ev_g_launch_pos()
        direction = end_pos - start_pos
        if direction.is_zero:
            direction = math3d.vector(0, 1, 0)
        else:
            direction.normalize()
        self.mecha_model.world_rotation_matrix = math3d.matrix.make_orient(direction, math3d.vector(0, 1, 0))
        self.need_update = True
        self._load_tid = None
        self._set_parachute_state(STATE_FLY)
        self.play_move_ani('fly')
        self.play_fly_screen_effect()
        self.send_event('E_HIDE_MODEL')
        return

    def play_fly_screen_effect(self):
        model = self.ev_g_model()
        if model:
            model.set_socket_bound_obj_active('fx_root', 1, False)

    def play_move_ani(self, anim_name):
        if not self.mecha_model:
            return
        if self.cnt_move_ani_name == anim_name:
            return
        self.cnt_move_ani_name = anim_name
        parachute_state = STATE_FLY
        self._set_parachute_state(parachute_state)

    def load_mecha_model(self):
        if not self.ev_g_is_avatar():
            loading_priority = game3d.ASYNC_MID
            if not self._load_tid and not self.mecha_model:
                self._load_tid = self.ev_g_load_model(self.parachute_mecha_res, self.on_load_mecha_model_complete, None, None, loading_priority, self.DEFAULT_XML)
        return

    def destroy(self):
        self.del_res()
        super(ComParachuteMecha, self).destroy()

    def _get_parachute_mecha_model(self):
        return self.mecha_model

    def _on_start_parachute_stage(self, *args):
        return
        self.send_event('E_HIDE_MODEL')
        if self.mecha_model:
            self.do_on_mecha_model_complete()
        else:
            self.load_mecha_model()

    def _on_parachute_open(self, *args):
        self.del_res()
        self.send_event('E_SHOW_MODEL')

    def _on_land(self, *args):
        self._on_parachute_open()

    @property
    def mecha_model(self):
        if self._mecha_model and self._mecha_model.valid:
            return self._mecha_model
        else:
            return None

    def del_res(self):
        self.load_mecha_callback = None
        if self.mecha_model:
            self.scene.remove_object(self.mecha_model)
            self.send_event('E_UNLOAD_MODEL', self.mecha_model, self._mecha_animator, False)
            self._mecha_model = None
        if self._mecha_animator:
            self._mecha_animator.destroy()
            self._mecha_animator = None
        if self._load_tid:
            self.send_event('E_CANCEL_LOAD_TASK', self._load_tid)
            self._load_tid = None
        self.need_update = False
        return

    def tick(self, dt):
        model = self.ev_g_model()
        if not (model and self.mecha_model):
            return
        model_world_trans = model.world_transformation
        mecha_pos = model_world_trans.translation
        self.mecha_model.world_position = mecha_pos