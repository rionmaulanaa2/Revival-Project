# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComOB.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from logic.client.const import game_mode_const

class ComOB(UnitCom):
    BIND_EVENT = {'G_IS_OB': '_get_is_ob',
       'E_SET_JUDGE_OB_TARGET': '_set_ob_target',
       'E_ON_CONTROL_TARGET_CHANGE': 'on_check_com',
       'E_HUMAN_MODEL_LOADED': 'human_model_loaded'
       }

    def __init__(self):
        super(ComOB, self).__init__()

    def init_from_dict(self, unit_obj, bdict):
        super(ComOB, self).init_from_dict(unit_obj, bdict)
        self._is_ob = bdict.get('is_ob', False)
        self._ob_soul_id = bdict.get('ob_soul_id', None)
        if self.is_unit_obj_type('LAvatar'):
            if global_data.player and global_data.player.id == self.unit_obj.id:
                global_data.emgr.ob_state_set.emit(self.unit_obj.id, self._is_ob)
        return

    def on_init_complete(self):
        if self._is_ob:
            self.send_event('E_HIDE_MODEL')
            scn = global_data.game_mgr.scene
            if scn and scn.valid:
                scn.set_lod_use_player_pos(1, False)
            if self.is_unit_obj_type('LAvatar'):
                if global_data.player and global_data.player.id == self.unit_obj.id:
                    spectate_target = self.ev_g_spectate_target()
                    if spectate_target is None:
                        if global_data.game_mode and global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_SURVIVALS):
                            global_data.emgr.scene_show_big_map_event.emit()
                        else:
                            global_data.ui_mgr.show_ui('JudgeLoadingUI', 'logic.comsys.observe_ui')
                    global_data.emgr.start_judge_scene_part.emit()
        return

    def human_model_loaded(self, *args):
        if self._is_ob:
            self.send_event('E_HIDE_MODEL')

    def on_check_com(self, *args):
        del_com_list = []
        if self._is_ob:
            pass

    def _get_is_ob(self):
        return self._is_ob

    def _set_ob_target(self, target_id):
        self.on_ob_soul(target_id)
        self.send_event('E_SPECTATE_OBJ', target_id)

    def on_ob_soul(self, soul_id):
        self._ob_soul_id = soul_id
        self.send_event('E_CALL_SYNC_METHOD', 'ob_soul', (soul_id,), True)