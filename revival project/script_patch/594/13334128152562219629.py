# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComExerciseField.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from logic.entities import ExerciseBattle
from logic.client.const import game_mode_const

class ComExerciseField(UnitCom):
    BIND_EVENT = {}

    def init_from_dict(self, uni_obj, bdict):
        super(ComExerciseField, self).init_from_dict(uni_obj, bdict)

    def on_init_complete(self):
        mode_type = global_data.game_mode.get_mode_type()
        if mode_type in (game_mode_const.GAME_MODE_EXERCISE,):
            self._regist_exercise_events()

    def _regist_exercise_events(self):
        self.unit_obj.regist_event('E_OPEN_MAIN_SETTING', self._exercise_open_main_setting)
        self.unit_obj.regist_event('E_QUIT_EXERCISE_FIELD', self._quit_exercise_field)

    def _unregist_exercise_events(self):
        self.unit_obj.unregist_event('E_OPEN_MAIN_SETTING', self._exercise_open_main_setting)
        self.unit_obj.unregist_event('E_QUIT_EXERCISE_FIELD', self._quit_exercise_field)

    def _exercise_open_main_setting(self, ui):
        ui.set_btn_exit_text_id(862008)

    def _quit_exercise_field(self):
        global_data.player.quit_battle(True)

    def _destroy_exercise_field(self):
        self._unregist_exercise_events()

    def destroy(self):
        self._destroy_exercise_field()
        super(ComExerciseField, self).destroy()