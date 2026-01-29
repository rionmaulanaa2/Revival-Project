# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComTrainAppearance.py
from __future__ import absolute_import
import six
from six.moves import range
from .ComBaseModelAppearance import ComBaseModelAppearance
import math3d
from common.cfg import confmgr
from logic.gcommon.trk.TrkManager import TrkManager
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const import battle_const
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode
from logic.client.const import game_mode_const
SFX_DICT = {battle_const.CTRL_TRAIN_STATE_FORCE_STOP: {'socket': 'fx_lightning','sfx_list': ['effect/fx/scenes/common/map/tuihuoche_shandian_red.sfx']},battle_const.CTRL_TRAIN_STATE_FORCE_FORWARD: {'socket': 'fx_lightning','sfx_list': ['effect/fx/scenes/common/map/tuihuoche_shandian_blue.sfx']},battle_const.CTRL_TRAIN_STATE_HEAL: {'socket': 'fx_lightning','sfx_list': ['effect/fx/scenes/common/map/liechebaowei_green.sfx']},battle_const.CTRL_TRAIN_STATE_DAMAGE: {'socket': 'fx_lightning','sfx_list': ['effect/fx/scenes/common/map/liechebaowei_yellow.sfx']}}
SFX_RANGE = [
 'effect/fx/scenes/common/map/tuihuoche_warning_gray.sfx',
 'effect/fx/scenes/common/map/tuihuoche_warning_red.sfx',
 'effect/fx/scenes/common/map/tuihuoche_warning_blue.sfx',
 'effect/fx/scenes/common/map/tuihuoche_warning_gold.sfx']

class ComTrainAppearance(ComBaseModelAppearance):
    BIND_EVENT = ComBaseModelAppearance.BIND_EVENT.copy()
    BIND_EVENT.update({'E_CHANGE_CARRIAGE_CTRL_STATE': '_change_carriage_ctrl_state',
       'E_UPDATE_RANGE_SFX_STATE': 'update_range_sfx_state',
       'E_CHANGE_CARRIAGE_HEAL': '_change_carriage_heal_state',
       'E_CHANGE_CARRIAGE_DAMAGE': '_change_carriage_damage_state',
       'E_TRAIN_DO_SKILL': '_train_do_skill'
       })

    def __init__(self):
        super(ComTrainAppearance, self).__init__()

    def init_from_dict(self, unit_obj, bdict):
        super(ComTrainAppearance, self).init_from_dict(unit_obj, bdict)
        self.carriage_no = bdict.get('carriage_no')
        self.train_no = bdict.get('train_no')
        self.dis = None
        self.sfx_dict = {}
        self.model_dict = {}
        self._carriage_ctrl_state = None
        return

    def get_model_info(self, unit_obj, bdict):
        res_path = confmgr.get('train_res')[str(self.carriage_no)]['res_path']
        return (
         res_path, None, (bdict,))

    def on_load_model_complete(self, model, userdata):
        super(ComTrainAppearance, self).on_load_model_complete(model, userdata)
        model.lod_config = (200 * NEOX_UNIT_SCALE, -1)

    def _change_carriage_ctrl_state(self, state):
        if state == self._carriage_ctrl_state:
            return
        else:
            self._carriage_ctrl_state = state
            sfx_data = None
            if self._carriage_ctrl_state == battle_const.CTRL_TRAIN_STATE_FORCE_FORWARD:
                self.clear_sfx_by_id(battle_const.CTRL_TRAIN_STATE_FORCE_STOP)
                sfx_data = SFX_DICT.get(battle_const.CTRL_TRAIN_STATE_FORCE_FORWARD)
            elif self._carriage_ctrl_state == battle_const.CTRL_TRAIN_STATE_FORCE_STOP:
                self.clear_sfx_by_id(battle_const.CTRL_TRAIN_STATE_FORCE_FORWARD)
                sfx_data = SFX_DICT.get(battle_const.CTRL_TRAIN_STATE_FORCE_STOP)
            else:
                self.clear_sfx_by_id(battle_const.CTRL_TRAIN_STATE_FORCE_FORWARD)
                self.clear_sfx_by_id(battle_const.CTRL_TRAIN_STATE_FORCE_STOP)
            if sfx_data:
                for sfx_path in sfx_data.get('sfx_list', []):
                    self.create_sfx_on_carriage(self._carriage_ctrl_state, sfx_path, sfx_data.get('socket'))

            return

    def _change_carriage_heal_state(self, state, group):
        self.sd.ref_heal_state = state
        self.sd.ref_heal_group = group

        def create_cb(sfx):
            play_data = global_data.game_mode.get_cfg_data('play_data')
            if not play_data:
                return
            train_check_range = play_data.get('train_check_range', 30)
            sfx.visible = True
            scale = train_check_range / 10.0
            sfx.scale = math3d.vector(scale, 1.0, scale)

        if state:
            sfx_data = SFX_DICT.get(battle_const.CTRL_TRAIN_STATE_HEAL)
            if sfx_data:
                for sfx_path in sfx_data.get('sfx_list', []):
                    self.create_sfx_on_carriage(battle_const.CTRL_TRAIN_STATE_HEAL, sfx_path, sfx_data.get('socket'), create_cb)

        else:
            self.clear_sfx_by_id(battle_const.CTRL_TRAIN_STATE_HEAL)

    def _change_carriage_damage_state(self, state, group):
        self.sd.ref_damage_state = state
        self.sd.ref_damage_group = group

        def create_cb(sfx):
            play_data = global_data.game_mode.get_cfg_data('play_data')
            if not play_data:
                return
            train_check_range = play_data.get('train_check_range', 30)
            sfx.visible = True
            scale = train_check_range / 10.0
            sfx.scale = math3d.vector(scale, 1.0, scale)

        if state:
            sfx_data = SFX_DICT.get(battle_const.CTRL_TRAIN_STATE_DAMAGE)
            if sfx_data:
                for sfx_path in sfx_data.get('sfx_list', []):
                    self.create_sfx_on_carriage(battle_const.CTRL_TRAIN_STATE_DAMAGE, sfx_path, sfx_data.get('socket'), create_cb)

        else:
            self.clear_sfx_by_id(battle_const.CTRL_TRAIN_STATE_DAMAGE)

    def _train_do_skill(self, skill_id):
        if int(skill_id) == 9:
            if not self.sd.ref_carriage_pos:
                return
            global_data.sfx_mgr.create_sfx_in_scene('effect/fx/mecha/8005/8005_fx_transform_shoot_damage.sfx', self.sd.ref_carriage_pos)

    def create_sfx_on_carriage(self, state, sfx_path, socket, on_create_cb=None):
        if not sfx_path or not socket or not self._model:
            return
        else:

            def create_cb(sfx):
                if on_create_cb:
                    on_create_cb(sfx)

            sfx_id = global_data.sfx_mgr.create_sfx_on_model(sfx_path, self._model, socket, on_create_func=create_cb)
            if self.sfx_dict.get(state, None) is None:
                self.sfx_dict[state] = [
                 sfx_id]
            else:
                self.sfx_dict[state].append(sfx_id)
            return

    def create_model_on_carriage(self, state, model_path, socket, on_create_cb=None):
        if not model_path or not socket:
            return

        def create_cb(model):
            if on_create_cb:
                on_create_cb(model)

        model_id = global_data.model_mgr.create_model(model_path, on_create_func=create_cb)
        if not self.model_dict.get(state):
            self.model_dict[state] = [
             model_id]
        else:
            self.model_dict[state].append(model_id)

    def clear_sfx_by_id(self, id):
        if not self.sfx_dict.get(id):
            return
        for sfx_id in self.sfx_dict[id]:
            global_data.sfx_mgr.remove_sfx_by_id(sfx_id)

        self.sfx_dict[id] = []

    def clear_all_sfx(self):
        for idx, sfx_list in six.iteritems(self.sfx_dict):
            for sfx_id in sfx_list:
                global_data.sfx_mgr.remove_sfx_by_id(sfx_id)

        self.sfx_dict = {}

    @execute_by_mode(True, (game_mode_const.GAME_MODE_TRAIN,))
    def _create_train_push_range_sfx(self):
        play_data = global_data.game_mode.get_cfg_data('play_data')
        if not play_data:
            return
        train_check_range = play_data.get('train_check_range', 30)

        def create_cb(sfx):
            sfx.visible = True
            scale = train_check_range / 10.0
            sfx.scale = math3d.vector(scale, 1.0, scale)

        for sfx_path in SFX_RANGE:
            self.create_sfx_on_carriage(-1, sfx_path, 'fx_lightning', on_create_cb=create_cb)

    def update_range_sfx_state(self, show_idx):
        if not self.sfx_dict.get(-1):
            self._create_train_push_range_sfx()
            return
        sfx_list = self.sfx_dict[-1]
        for idx in range(len(sfx_list)):
            sfx = global_data.sfx_mgr.get_sfx_by_id(sfx_list[idx])
            if sfx:
                sfx.visible = bool(show_idx == idx)