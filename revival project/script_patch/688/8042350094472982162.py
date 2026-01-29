# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComEmoji.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
import logic.gcommon.common_const.animation_const as animation_const
from common.cfg import confmgr
import common.utils.timer as timer
import logic.gcommon.common_utils.bcast_utils as bcast
from logic.gutils.interaction_utils import get_emoj_path, set_emoj_tex
from logic.gutils.client_unit_tag_utils import register_unit_tag
from common.framework import Functor
import world
import math3d
import game3d
OPEN_ANIM_NAME = 'open'
IDLE_ANIM_NAME = 'open_idle'
CLOSE_ANIM_NAME = 'close'
EMOJ_DIR = 'model_new/others/emoji/'
SFX_DIR = 'effect/fx/niudan/'
EMOJI_TYPE_HUMAN = 1
EMOJI_TYPE_LOBBY_HUMAN = 2
EMOJI_TYPE_MECHA = 3
MECHA_EMOJI_TAG_VALUE = register_unit_tag(('LMecha', 'LMechaTrans', 'LMechaRobot'))
_HASH_scale = game3d.calc_string_hash('Scale')
AVATAR_SCALE = 1.0
LUPPET_SCALE = 2.0

class ComEmoji(UnitCom):
    BIND_EVENT = {'E_ADD_EMOJI': 'add_emoji',
       'E_REMOVE_EMOJI': 'remove_emoji',
       'E_SWITCH_STATUS': 'on_switch_animation',
       'G_CUSTOM_EMOJI': 'on_get_custom_emoji',
       'E_MODEL_LOADED': ('initialize_socket_info', 101),
       'E_TRANS_TO_BALL_FINISH': ('refresh_socket_info', 100),
       'E_TRANS_TO_HUMAN': ('refresh_socket_info', 100),
       'E_SET_MECAH_MODE': ('refresh_socket_info', 100),
       'E_MODEL_SCALE_CHANGED': 'on_model_scale_changed'
       }
    STATE_TO_BIAS = {animation_const.STATE_JUMP: 6,
       animation_const.STATE_SQUAT: -7,
       animation_const.STATE_ROLL: -5,
       animation_const.STATE_CRAWL: -6,
       animation_const.STATE_SQUAT_HELP: -6,
       animation_const.STATE_SWIM: 6
       }

    def init_from_dict(self, unit_obj, bdict):
        super(ComEmoji, self).init_from_dict(unit_obj, bdict)
        self._emoji_model = None
        self._remove_timer_id = None
        self._item_no = None
        self._emoji_type = EMOJI_TYPE_HUMAN
        self._bias_move_speed = 1
        self._target_bias = 0
        self._cur_bias = 0
        self._socket_bias = 0
        self._cur_socket_name = 's_xuetiao'
        self._model_scale_value = 1.0
        self._sfx_id = None
        if self.unit_obj.MASK & MECHA_EMOJI_TAG_VALUE:
            self._emoji_type = EMOJI_TYPE_MECHA
            self._bias_move_speed = 2
            self._cur_socket_name = 'xuetiao'
        self._custom_emoji = bdict.get('custom_emoji', {})
        return

    def on_get_custom_emoji(self):
        return self._custom_emoji

    def tick(self, dt):
        if not self._emoji_model or not self._emoji_model.valid:
            self.need_update = False
            return
        delta = self._target_bias - self._cur_bias
        if delta == 0:
            self.need_update = False
            return
        if delta > 0:
            self._cur_bias += self._bias_move_speed
            if self._cur_bias > self._target_bias:
                self._cur_bias = self._target_bias
        else:
            self._cur_bias -= self._bias_move_speed
            if self._cur_bias < self._target_bias:
                self._cur_bias = self._target_bias
        position = math3d.vector(0, self._cur_bias, 0)
        self._emoji_model.position = position
        if self._sfx_id:
            sfx = global_data.sfx_mgr.get_sfx_by_id(self._sfx_id)
            if sfx:
                sfx.position = position

    def on_switch_animation(self, status, is_sync=True):
        self._target_bias = self.STATE_TO_BIAS.get(status, 0) + self._socket_bias
        if not self._emoji_model or not self._emoji_model.valid:
            self.need_update = False
            self._cur_bias = self._target_bias
            return
        delta = self._target_bias - self._cur_bias
        if delta == 0:
            self.need_update = False
            return
        self.need_update = True

    def get_emoj_open_sfx_path(self):
        is_human = self._emoji_type == EMOJI_TYPE_HUMAN
        path = None
        emoj_config = confmgr.get('emoticon_conf', 'EmoticonConfig', 'Content', str(self._item_no))
        if is_human:
            path = emoj_config.get('human_open_effect_path', None)
        else:
            path = emoj_config.get('mecha_open_effect_path', None)
        if not path:
            return
        else:
            return SFX_DIR + path + '.sfx'

    def get_emoj_idle_sfx_path(self):
        is_human = self._emoji_type == EMOJI_TYPE_HUMAN
        path = None
        emoj_config = confmgr.get('emoticon_conf', 'EmoticonConfig', 'Content', str(self._item_no))
        if is_human:
            path = emoj_config.get('human_idle_effect_path', None)
        else:
            path = emoj_config.get('mecha_idle_effect_path', None)
        if not path:
            return
        else:
            return SFX_DIR + path + '.sfx'

    def get_emoj_duration(self, item_no):
        emoj_config = confmgr.get('emoticon_conf', 'EmoticonConfig', 'Content', str(item_no))
        return emoj_config.get('keep_duration', 0.01)

    def end_open_anim(self, model, *args):
        if self._sfx_id:
            global_data.sfx_mgr.shutdown_sfx_by_id(self._sfx_id)
            self._sfx_id = None
        if self._emoji_model and self._emoji_model.valid:
            self._emoji_model.play_animation(IDLE_ANIM_NAME)
        self._sfx_id = global_data.sfx_mgr.create_sfx_on_model(self.get_emoj_idle_sfx_path(), self.ev_g_model(), self._cur_socket_name, world.BIND_TYPE_TRANSLATE, on_create_func=self.create_effect)
        return

    def load_emoj(self, item_no):
        is_human = self._emoji_type == EMOJI_TYPE_HUMAN
        res_path = get_emoj_path(is_human)
        if not res_path:
            log_error('[ERROR] item_no = %s not have emoj model' % item_no)
            return
        global_data.model_mgr.create_model(res_path, on_create_func=Functor(self._emoji_model_load_callback, item_no))

    def add_emoji(self, item_no):
        player_id = global_data.player.logic.id
        if self.unit_obj.sd.ref_driver_id == global_data.player.logic.id or self.unit_obj.id == player_id:
            global_data.player.logic.send_event('E_SUCCESS_INTERACTION')
        self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_ADD_EMOJI, (item_no,)], False)
        self.remove_emoji()
        self._item_no = item_no
        self.load_emoj(item_no)
        self.send_event('E_ON_ADD_EMOJI', self.unit_obj.id)

    def remove_emoji(self, *args):
        old_sfx_id = self._sfx_id
        if self._sfx_id:
            global_data.sfx_mgr.shutdown_sfx_by_id(self._sfx_id)
            self._sfx_id = None
        if self._emoji_model and self._emoji_model.valid:
            self._emoji_model.destroy()
        if self._remove_timer_id:
            global_data.game_mgr.unregister_logic_timer(self._remove_timer_id)
            self._remove_timer_id = None
        self._emoji_model = None
        self.need_update = False
        if old_sfx_id:
            self.send_event('E_ON_REMOVE_EMOJI', self.unit_obj.id)
        return

    def create_effect(self, sfx, *args):
        scale = AVATAR_SCALE
        if not self.ev_g_is_cam_target():
            scale = LUPPET_SCALE
        sfx.scale = math3d.vector(scale, scale, scale)
        sfx.position = math3d.vector(0, self._cur_bias, 0)

    def _emoji_model_load_callback(self, item_no, emoji_model, *args):
        model = self.ev_g_model()
        if not model:
            return
        self.remove_emoji()
        custom_emoji = self._custom_emoji
        if self.sd.ref_driver_id:
            from mobile.common.EntityManager import EntityManager
            driver_id = self.sd.ref_driver_id
            entity = EntityManager.getentity(driver_id)
            if entity and entity.logic:
                custom_emoji = entity.logic.ev_g_custom_emoji()
        set_emoj_tex(emoji_model, item_no, custom_emoji.get(str(item_no), {}))
        emoji_model.remove_from_parent()
        model.bind(self._cur_socket_name, emoji_model, world.BIND_TYPE_TRANSLATE)
        self._emoji_model = emoji_model
        self._sfx_id = global_data.sfx_mgr.create_sfx_on_model(self.get_emoj_open_sfx_path(), model, self._cur_socket_name, world.BIND_TYPE_TRANSLATE, on_create_func=self.create_effect)
        emoji_model.play_animation(OPEN_ANIM_NAME)
        emoji_model.unregister_event(self.end_open_anim, 'end', OPEN_ANIM_NAME)
        emoji_model.register_anim_key_event(OPEN_ANIM_NAME, 'end', self.end_open_anim)
        keep_duration = self.get_emoj_duration(self._item_no)
        if self._remove_timer_id:
            global_data.game_mgr.unregister_logic_timer(self._remove_timer_id)
        if self.ev_g_is_cam_target():
            emoji_model.all_materials.set_var(_HASH_scale, 'Scale', AVATAR_SCALE)
        else:
            emoji_model.all_materials.set_var(_HASH_scale, 'Scale', LUPPET_SCALE)
        self._remove_timer_id = global_data.game_mgr.register_logic_timer(self.close_emoji, keep_duration, times=1, mode=timer.CLOCK)
        emoji_model.position = math3d.vector(0, self._cur_bias, 0)
        self.need_update = True

    def close_emoji(self):
        self._remove_timer_id = None
        self._emoji_model.play_animation(CLOSE_ANIM_NAME)
        self._emoji_model.unregister_event(self.remove_emoji, 'end', CLOSE_ANIM_NAME)
        self._emoji_model.register_anim_key_event(CLOSE_ANIM_NAME, 'end', self.remove_emoji)
        return

    def destroy(self):
        self._sfx_id = None
        if self._remove_timer_id:
            global_data.game_mgr.unregister_logic_timer(self._remove_timer_id)
            self._remove_timer_id = None
        if self._emoji_model and self._emoji_model.valid:
            self._emoji_model.destroy()
            self._emoji_model = None
        self._item_no = None
        super(ComEmoji, self).destroy()
        return

    def initialize_socket_info(self, *args, **kwargs):
        socket_info = self.ev_g_get_socket()
        if not socket_info:
            return
        self._cur_socket_name, socket_bias = socket_info
        model = self.ev_g_model()
        self._model_scale_value = model.scale.x
        socket_bias *= self._model_scale_value
        if socket_bias != self._socket_bias:
            self._target_bias = self._target_bias - self._socket_bias + socket_bias
            self._socket_bias = socket_bias
        self._cur_bias = self._target_bias

    def refresh_socket_info(self, *args, **kwargs):
        socket_info = self.ev_g_get_socket()
        if not socket_info:
            return
        socket_name, socket_bias = socket_info
        model = self.ev_g_model()
        if model:
            socket_bias *= model.scale.x
            self._model_scale_value = model.scale.x
        if socket_bias != self._socket_bias:
            self._target_bias = self._target_bias - self._socket_bias + socket_bias
            self._socket_bias = socket_bias
        if not self._emoji_model or not self._emoji_model.valid:
            self._cur_bias = self._target_bias
            self._cur_socket_name = socket_name
            return
        if socket_name != self._cur_socket_name:
            if model:
                self._cur_bias = self._target_bias
                local_position = math3d.vector(0, self._cur_bias, 0)
                self._emoji_model.remove_from_parent()
                model.bind(socket_name, self._emoji_model, world.BIND_TYPE_TRANSLATE)
                self._emoji_model.position = local_position
                if self._sfx_id:
                    sfx = global_data.sfx_mgr.get_sfx_by_id(self._sfx_id)
                    if sfx:
                        sfx.remove_from_parent()
                        model.bind(socket_name, sfx)
                        sfx.position = local_position
            self._cur_socket_name = socket_name
            return
        delta = self._target_bias - self._cur_bias
        if delta == 0:
            self.need_update = False
            return
        if delta > 30:
            self._cur_bias = self._target_bias - 30
        else:
            self._cur_bias = self._target_bias + 30
        self.need_update = True

    def on_model_scale_changed(self, scale_value):
        if scale_value != self._model_scale_value:
            unscaled_bias = self._socket_bias / self._model_scale_value
            new_socket_bias = unscaled_bias * scale_value
            self._target_bias = self._target_bias - self._socket_bias + new_socket_bias
            self._socket_bias = new_socket_bias
            self._model_scale_value = scale_value
            if not self._emoji_model or not self._emoji_model.valid:
                self._cur_bias = self._target_bias
            else:
                self.tick(0)