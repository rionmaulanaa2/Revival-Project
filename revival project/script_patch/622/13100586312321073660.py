# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComShortcut.py
from __future__ import absolute_import
import six
from ..UnitCom import UnitCom
from ...item import item_utility
from common.cfg import confmgr
from logic.gcommon.common_const import mecha_const as mconst
from logic.gcommon.common_const import ui_operation_const as uoc
from logic.gcommon import time_utility
from logic.client.const import game_mode_const
from data.item_use_var import MECHA_USABLE_ID_LIST

class ComShortcut(UnitCom):
    BIND_EVENT = {'E_ITEM_DATA_CHANGED': ('update_shortcut', 100),
       'E_HEALTH_HP_CHANGE': '_on_human_hp_changed',
       'E_MECHA_HEALTH_HP_CHANGE': '_on_mecha_hp_changed',
       'E_ON_JOIN_MECHA': ('_on_join_mecha', 10),
       'E_ON_LEAVE_MECHA': ('_on_leave_mecha', 10),
       'E_SET_SHOW_SHORTCUT': 'set_show_shortcut',
       'G_SHOW_SHORTCUT': 'get_show_shortcut',
       'E_MAX_HP_CHANGED': '_on_human_max_hp_changed',
       'E_MECHA_HEALTH_MAX_HP_CHANGE': '_on_mecha_max_hp_changed',
       'E_SHORT_CUT_REFRESH_STATE': 'referesh_state',
       'E_SIGNAL_CHANGE': '_on_signal_change'
       }
    COOLING_PERCENT = -1
    COOLED_PERCENT = 100

    def __init__(self):
        super(ComShortcut, self).__init__()
        self._shortcut = 0
        self._throw_item_shortcut = 0
        self._human_percent = None
        self._mecha_percent = None
        self._mecha_cd_state = self.COOLING_PERCENT
        self._human_hp_range = None
        self._mecha_hp_range = None
        self._recommend_list = []
        self._human_max_hp = None
        self._mecha_max_hp = None
        self._recall_cd_end_timestamp = 0
        self.sd.ref_throw_item_shortcut = 0
        self.last_is_in_mecha = None
        self.last_is_signal_warning = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComShortcut, self).init_from_dict(unit_obj, bdict)
        self._shortcut = bdict.get('drug_shortcut', 0)
        self.sd.ref_throw_item_shortcut = bdict.get('throw_item_shortcut', 0)
        cur_map_id = global_data.game_mode.get_map_id()
        self._mode_recommend_list = confmgr.get('item_by_mode', str(cur_map_id), 'cRecommendItemList', default=[])

    def on_post_init_complete(self, bdict):
        if self._shortcut:
            self.send_event('E_SET_DRUG_SHORTCUT', self._shortcut, False)
            self.update_state(None, None, False)
        else:
            self.update_state(None, None, True)
        return

    def open_short_cut(self):
        return global_data.player and global_data.player.get_setting_2(uoc.ITEM_SHORT_CUT)

    def update_shortcut(self, item_data=None):
        if self._human_percent is None:
            self.update_state(up_shortcut=False)
        if item_data and not item_data.get('refresh', True):
            return
        else:
            items = self.ev_g_others()
            item_set = set()
            for item in six.itervalues(items):
                item_set.add(item['item_id'])

            if not self.open_short_cut() and self._shortcut and self._shortcut in item_set:
                return
            cur_shortcut = 0
            for item_id in self._recommend_list:
                if item_id in item_set:
                    cur_shortcut = item_id
                    break

            if not cur_shortcut and global_data.game_mode and global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_RANDOM_DEATH):
                for item_id in MECHA_USABLE_ID_LIST:
                    if item_id in item_set:
                        cur_shortcut = item_id
                        break

            self.send_event('E_SET_SHOW_SHORTCUT', cur_shortcut, self._shortcut != cur_shortcut)
            return

    def update_state(self, human_hp=None, mecha_hp=None, up_shortcut=True):
        is_open = self.open_short_cut()
        if is_open or not is_open and not self._recommend_list:
            is_in_mecha = 1 if self.ev_g_in_mecha('Mecha') else 0
            percent = self.ev_g_signal_percent()
            if percent is None:
                is_signal_warning = False
            else:
                percent = percent * 100
                is_signal_warning = is_in_mecha == 0 and percent <= 60
            import copy
            if is_signal_warning:
                if is_signal_warning == self.last_is_signal_warning:
                    self.send_event('E_SET_SHOW_SHORTCUT', self._shortcut, False)
                    return
                self._recommend_list = []
                recommend_conf = confmgr.get('item_recommend')
                self._recommend_list = copy.deepcopy(recommend_conf['1']['cRecommendList'])
            else:
                if human_hp or self._human_percent is None:
                    if self._human_max_hp is None:
                        self._human_max_hp = max(self.ev_g_max_hp(), 1)
                    human_hp = human_hp or self.ev_g_hp()
                    self._human_percent = human_hp * 100.0 / self._human_max_hp
                if mecha_hp or self._mecha_percent is None:
                    mecha = self.ev_g_bind_mecha_entity()
                    if mecha and mecha.__class__.__name__ == 'Mecha' and mecha.logic:
                        if self._mecha_max_hp is None:
                            self._mecha_max_hp = max(mecha.logic.share_data.ref_max_hp, 1)
                        mecha_hp = mecha_hp or mecha.logic.share_data.ref_hp
                        if mecha_hp == None:
                            mecha_hp = 0
                        self._mecha_percent = mecha_hp * 100.0 / self._mecha_max_hp
                    else:
                        self._mecha_percent = self.COOLING_PERCENT
                    if self._mecha_percent > 100.0:
                        log_error('[ComShortcut] mecha_percent = %f', self._mecha_percent)
                        self._mecha_percent = 100.0
                hhp, mhp = self._human_percent, self._mecha_percent
                if self._human_hp_range and self._mecha_hp_range:
                    (hhpl, hhpr), (mhpl, mhpr) = self._human_hp_range, self._mecha_hp_range
                    if hhpl <= hhp <= hhpr and mhpl <= mhp <= mhpr and is_in_mecha == self.last_is_in_mecha:
                        self.send_event('E_SET_SHOW_SHORTCUT', self._shortcut, False)
                        return
                self._recommend_list = []
                recommend_conf = confmgr.get('item_recommend')
                for state, contact in six.iteritems(recommend_conf):
                    (hhpl, hhpr), (mhpl, mhpr), _is_in_mecha = contact['cHumanHpRange'], contact['cMechaHpRange'], contact['cIsInMecha']
                    if hhpl <= hhp <= hhpr and mhpl <= mhp <= mhpr and is_in_mecha == _is_in_mecha:
                        self._human_hp_range = (
                         hhpl, hhpr)
                        self._mecha_hp_range = (mhpl, mhpr)
                        self.last_is_in_mecha = _is_in_mecha
                        self._recommend_list = copy.deepcopy(contact['cRecommendList']) + self._mode_recommend_list
                        break

            self.last_is_signal_warning = is_signal_warning
        if up_shortcut:
            self.update_shortcut()
        return

    def set_show_shortcut(self, item_id, sync=True):
        self._shortcut = item_id
        if sync:
            self.send_event('E_CALL_SYNC_METHOD', 'set_drug_shortchut', (item_id,))

    def get_show_shortcut(self):
        return self._shortcut

    def _on_human_hp_changed(self, hp, mod):
        self.update_state(hp, None, True)
        return

    def _on_mecha_hp_changed(self, hp, mod):
        self.update_state(None, hp, True)
        return

    def _on_human_max_hp_changed(self, max_hp, *args):
        self._human_max_hp = max_hp
        self._human_percent = None
        self.update_state(None, None, True)
        return

    def _on_mecha_max_hp_changed(self, *args):
        self._reset_mecha_state()

    def _on_recall_cd(self, cd_type, total_cd, left_time, up_state=True):
        last_cd_state = self._mecha_cd_state
        if left_time > 0 or cd_type == mconst.RECOVER_CD_TYPE_DISABLE:
            self._mecha_cd_state = self.COOLING_PERCENT
        else:
            self._mecha_cd_state = self.COOLED_PERCENT
        if up_state and self._mecha_cd_state != last_cd_state:
            self._mecha_percent = None
            self.update_state(None, None, True)
        if left_time > 0:
            self._recall_cd_end_timestamp = left_time + time_utility.get_server_time()
            if not self.need_update:
                self.need_update = True
        return

    def _on_join_mecha(self, *args, **kwargs):
        self._reset_mecha_state()

    def _on_leave_mecha(self, *args):
        self._mecha_percent = self.COOLING_PERCENT
        self.update_state(None, None, True)
        return

    def _reset_mecha_state(self, up_state=True):
        self._mecha_percent = None
        self._mecha_max_hp = None
        if up_state:
            self.update_state(None, None, True)
        return

    def referesh_state(self):
        self._human_percent = None
        self._mecha_percent = None
        self.update_state(None, None, True)
        return

    def _on_signal_change(self, *args, **kargs):
        self.update_state(None, None, True)
        return

    def tick(self, delta):
        if time_utility.get_server_time() > self._recall_cd_end_timestamp:
            self.need_update = False
            self._mecha_max_hp = None
            self._on_recall_cd(-1, None, 0)
        return