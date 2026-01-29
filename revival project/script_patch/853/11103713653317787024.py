# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComNBombDeviceBloodUI.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
import weakref
from logic.gutils.judge_utils import get_player_group_id
from logic.comsys.battle.NBomb.NBombBattleDefines import NBOMB_DEVICE_BLOOD_BLUE, NBOMB_DEVICE_BLOOD_RED

class ComNBombDeviceBloodUI(UnitCom):
    BIND_EVENT = {'E_MODEL_LOADED': 'on_model_loaded',
       'E_HEALTH_HP_CHANGE': '_on_hp_changed',
       'E_MAX_HP_CHANGED': 'on_max_hp_changed'
       }

    def __init__(self):
        super(ComNBombDeviceBloodUI, self).__init__()
        self._hp_cur = 0
        self._hp_max = 100
        self._model_ref = None
        self._percent_txt_id = None
        self._faction_id = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComNBombDeviceBloodUI, self).init_from_dict(unit_obj, bdict)
        self._hp_max = bdict.get('max_hp', 100)
        self._hp_cur = bdict.get('hp', self._hp_max)
        self._faction_id = bdict.get('faction_id', None)
        return

    def cache(self):
        self._clear_ui()
        self._model_ref = None
        super(ComNBombDeviceBloodUI, self).cache()
        return

    def on_max_hp_changed(self, max_hp, hp, *args):
        self._hp_max = max_hp

    def on_model_loaded(self, model, box=None):
        self._model_ref = weakref.ref(model)
        self._create_hp_ui(model, box)

    def get_simui_pos(self):
        pass

    def _on_hp_changed(self, hp, mod=0):
        self._hp_cur = hp
        hp_percent = 1.0 * self._hp_cur / self._hp_max
        ui = global_data.ui_mgr.get_ui('NBombDeviceBloodUI')
        ui and ui.on_update_crystal_hp(hp_percent)

    def _create_hp_ui(self, model, box=None):
        if box is None:
            box = model.bounding_box
        scale_y = model.scale.y
        position = model.position
        t_position = (position.x * model.scale.x, (position.y + 2 * box.y) * scale_y + 15, position.z * model.scale.z)
        global_data.ui_mgr.close_ui('NBombDeviceBloodUI')
        if get_player_group_id() == self._faction_id:
            mark_type = NBOMB_DEVICE_BLOOD_BLUE
            icon_path = 'gui/ui_res_2/battle_bomb/icon_battle_bomb_blue.png'
        else:
            mark_type = NBOMB_DEVICE_BLOOD_RED
            icon_path = 'gui/ui_res_2/battle_bomb/icon_battle_bomb_red.png'
        ui = global_data.ui_mgr.show_ui('NBombDeviceBloodUI', 'logic.comsys.battle.NBomb')
        ui and ui.add_locate_widget(mark_type, t_position)
        ui and ui.set_icon(icon_path)
        self._on_hp_changed(self._hp_cur)
        return

    def _clear_ui(self):
        global_data.ui_mgr.close_ui('NBombDeviceBloodUI')

    def destroy(self):
        self._clear_ui()
        super(ComNBombDeviceBloodUI, self).destroy()