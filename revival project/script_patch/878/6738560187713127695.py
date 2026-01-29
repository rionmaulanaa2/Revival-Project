# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/PveEditBattle.py
from __future__ import absolute_import
import six
from logic.entities.Battle import Battle
from common.cfg import confmgr
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Float, Tuple, Int, Dict, Str, Bool
from logic.comsys.battle.pve.PVETipsMgr import PVETipsMgr
import math3d
import world

class PveEditBattle(six.with_metaclass(Battle.meta_class('impSunshineEdit', 'impStoryline', 'impLevelMgr', 'impSceneSwitcher', 'impPvePlay', 'impPveAmbSound', 'impPveDropItemMgr', 'impPosMarker'), Battle)):
    _meta_battle = True
    pve_ui = ('PVETipsUI', 'PVERadarMapUI', 'PVEResUI', 'PVEBuffUI', 'PVEElementUI',
              'PVEIceBulletUI')
    ui_to_hide = ('BattleInfoPlayerNumber', 'BattleInfoAreaInfo', 'RogueGiftTopRightUI',
                  'DeathRogueGiftTopRightUI')
    ui_to_close = ('SmallMapUI', 'FightStateUI', 'BattleFightCapacity', 'FightKillNumberUI',
                   'BattleFightMeow', 'ScalePlateUI', 'BagUI')
    ui_to_close_ext = ()

    def __init__(self, entityid):
        self._exit_timestamp = 0
        self._pve_boss_cleared = False
        super(PveEditBattle, self).__init__(entityid)

    def init_from_dict(self, bdict):
        super(PveEditBattle, self).init_from_dict(bdict)
        global_data.sound_mgr.load_pve_bnk()
        global_data.emgr.switch_game_voice.emit(False)

    def destroy(self, clear_cache=True):
        self.clear_extra_ui()
        global_data.sound_mgr.unload_pve_bnk()
        global_data.emgr.switch_game_voice.emit(True)
        super(PveEditBattle, self).destroy()

    def init_battle_scene(self, scene_data):
        bdict = self._save_init_bdict
        scene_name = bdict.get('scene_name')
        scene_path = bdict.get('scene_path')
        map_id = bdict.get('map_id')
        scene_info = {'scene_name': scene_name,'scene_path': scene_path,'map_id': map_id}
        scene_data = self.gen_scene_data(scene_info)
        super(PveEditBattle, self).init_battle_scene(scene_data)

    def update_exit_timestamp(self, exit_timestamp):
        self._exit_timestamp = exit_timestamp
        global_data.emgr.update_exit_timestamp.emit(exit_timestamp)

    def boarding_movie_data(self):
        return None

    def load_finish(self):
        self.init_extra_ui()
        super(PveEditBattle, self).load_finish()

    def init_extra_ui(self):
        ui_mgr = global_data.ui_mgr
        for ui in self.ui_to_hide:
            ui_mgr.hide_ui(ui)

        for ui in self.ui_to_close:
            ui_mgr.close_ui(ui)

        if not global_data.use_sunshine:
            for ui in self.ui_to_close_ext:
                ui_mgr.close_ui(ui)

        for ui in self.pve_ui:
            ui_mgr.show_ui(ui, module_path='logic.comsys.battle.pve')

    def clear_extra_ui(self):
        ui_mgr = global_data.ui_mgr
        for ui in self.pve_ui:
            ui_mgr.close_ui(ui)

    @rpc_method(CLIENT_STUB, (Dict('battle_data'),))
    def update_battle_data(self, battle_data):
        exit_timestamp = battle_data.get('exit_timestamp', None)
        if exit_timestamp is not None:
            self.update_exit_timestamp(exit_timestamp)
        return

    @rpc_method(CLIENT_STUB, (Dict('report_dict'),))
    def battle_report(self, report_dict):
        if not global_data.cam_lplayer:
            return
        else:
            eid = report_dict.get('trigger_id', None)
            if eid and eid == global_data.cam_lplayer.id:
                ui = global_data.ui_mgr.get_ui('BattleHitFeedBack')
                ui and ui.deal_message(report_dict['event_type'])
                global_data.sound_mgr.play_sound_2d('Play_ui_notice', ('ui_notice',
                                                                       'achievement_level2'))
            return

    @rpc_method(CLIENT_STUB, (Bool('pve_boss_cleared'),))
    def notify_pve_boss_cleared(self, pve_boss_cleared):
        self._pve_boss_cleared = pve_boss_cleared
        if self._pve_boss_cleared:
            global_data.ui_mgr.close_ui('PVESellUI')
            global_data.emgr.on_pve_boss_cleared_event.emit()

    def get_pve_boss_cleared(self):
        return self._pve_boss_cleared