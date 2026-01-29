# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComBackpackClient.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import item_utils
from mobile.common.EntityManager import EntityManager
from logic.gcommon.cdata import status_config as st_const
from logic.gcommon.const import NEOX_UNIT_SCALE

class ComBackpackClient(UnitCom):
    BIND_EVENT = {'E_SET_CONTROL_TARGET': '_set_control_target',
       'G_TRY_OPEN_BOX': 'try_open_box',
       'E_ON_CARRY_BULLET_MERGED': '_on_carry_bullet_merged'
       }

    def __init__(self):
        super(ComBackpackClient, self).__init__()

    def init_from_dict(self, unit_obj, bdict):
        super(ComBackpackClient, self).init_from_dict(unit_obj, bdict)
        self._ctrl_target = None
        self._unlocking_paradrop = bdict.get('unlocking_item', None)
        self._opening_box = bdict.get('opening_box', None)
        self._cur_singing_id = bdict.get('last_try_item', None)
        self._start_pos = None
        return

    def on_init_complete(self):
        if self._opening_box:
            self.send_event('E_CLOSE_PROGRESS', self._opening_box)
        self._opening_box = None
        return

    def get_cur_pos(self):
        target = self.ev_g_control_target().logic
        return target.ev_g_position()

    def try_open_box(self, item_eid):
        box = EntityManager.getentity(item_eid)
        if not box or not box.logic or box.logic.ev_g_is_opened():
            return True
        else:
            consume_time = box.logic.ev_g_open_time()
            item_id = box.logic.ev_g_item_id()
            if not self.ev_g_status_check_pass(st_const.ST_USE_ITEM):
                return False
            if item_utils.is_rouge_box(item_id) and box and box.logic and not box.logic.ev_g_can_open_box(self.unit_obj):
                return False
            if self._opening_box is None:
                if consume_time > 0:
                    self._opening_box = item_eid
                    self.bind_interrupt_events()
                    from logic.gutils.item_utils import get_item_pic_by_item_no, get_item_singing_progress_text
                    item_pic = get_item_pic_by_item_no(item_id)
                    consume_time = consume_time * (1 + self.ev_g_use_item_cost_time_factor(item_id))
                    progress_text_id = get_item_singing_progress_text(item_id)
                    self.send_event('E_SHOW_PROGRESS', consume_time, item_eid, get_text_by_id(progress_text_id), callback=self.stop_open_box, cancel_callback=self.cancel_open_box, icon_path=item_pic)
                    self.send_event('E_CALL_SYNC_METHOD', 'try_open_scenebox', (item_eid,))
                    self.play_opening_sound(item_eid, item_id)
                    self._start_pos = self.get_cur_pos()
                else:
                    self.open_box(item_eid)
                if box.logic.ev_g_is_scenebox():
                    global_data.emgr.play_game_voice.emit('open')
            if box.logic.ev_g_is_deadbox():
                return True
            return False

    def canel_open_box_by_hit(self, need_close_ui=True, reason='break'):
        box = EntityManager.getentity(self._opening_box)
        if box and box.logic:
            item_id = box.logic.ev_g_item_id()
            if not item_utils.box_need_interrupt_by_hit(item_id):
                return
        self.cancel_open_box(need_close_ui, reason)

    def cancel_open_box(self, need_close_ui=True, reason='break'):
        if not self.is_valid():
            return
        self.stop_opening_sound()
        self.stop_open_box(False, need_close_ui, reason=reason)

    def stop_open_box(self, success=True, need_close_ui=True, reason='break'):
        if not self.is_valid():
            return
        else:
            if self._opening_box:
                if success:
                    self.open_box(self._opening_box)
                else:
                    self.send_event('E_CALL_SYNC_METHOD', 'stop_open_scenebox', (self._opening_box, reason))
                if need_close_ui:
                    self.send_event('E_CLOSE_PROGRESS', self._opening_box)
                self._opening_box = None
                self.unbind_interrupt_events()
            return

    def open_box(self, box_eid):
        box = EntityManager.getentity(box_eid)
        if box and box.logic:
            model = box.logic.ev_g_model()
            item_number = box.logic.ev_g_item_num()
            cur_pos = self.ev_g_position()
            area_id = self.scene.get_scene_area_info(cur_pos.x, cur_pos.z)
            pos_list = item_utils.get_valid_pos_list(self.scene, model, item_number, cur_pos)
            if pos_list:
                self.send_event('E_CALL_SYNC_METHOD', 'open_scenebox_success', (box_eid, pos_list, area_id))

    def bind_interrupt_events(self):
        if self._ctrl_target and self._ctrl_target.logic:
            regist_event = self._ctrl_target.logic.regist_event
            regist_event('E_ON_DEL_SHEILD', self.canel_open_box_by_hit, -999)
        else:
            regist_event = self.regist_event
        if G_POS_CHANGE_MGR:
            if self._ctrl_target and self._ctrl_target.logic:
                self._ctrl_target.logic.regist_pos_change(self.on_pos_changed, 0.2)
            else:
                self.regist_pos_change(self.on_pos_changed, 0.2)
        else:
            regist_event('E_POSITION', self.on_pos_changed, -999)
        regist_event('E_ON_HIT', self.canel_open_box_by_hit, -999)

    def unbind_interrupt_events(self):
        if self._ctrl_target and self._ctrl_target.logic:
            unregist_event = self._ctrl_target.logic.unregist_event
            unregist_event('E_ON_DEL_SHEILD', self.canel_open_box_by_hit)
        else:
            unregist_event = self.unregist_event
        if G_POS_CHANGE_MGR:
            if self._ctrl_target and self._ctrl_target.logic:
                self._ctrl_target.logic.unregist_pos_change(self.on_pos_changed)
            else:
                self.unregist_pos_change(self.on_pos_changed)
        else:
            unregist_event('E_POSITION', self.on_pos_changed)
        unregist_event('E_ON_HIT', self.canel_open_box_by_hit)

    def on_pos_changed(self, pos):
        if not self._start_pos:
            self._start_pos = self.get_cur_pos()
            return
        delta = pos - self._start_pos
        if not delta.is_zero and delta.length > 0.5 * NEOX_UNIT_SCALE:
            self.cancel_open_box(reason='move')

    def _set_control_target(self, target, *args):
        self.cancel_open_box()
        self._ctrl_target = target

    def play_opening_sound(self, item_eid, item_id):
        box = EntityManager.getentity(item_eid)
        if not box or not box.logic or box.logic.ev_g_is_opened():
            return
        box.logic.send_event('E_PLAY_OPENING_SOUND', item_id)

    def stop_opening_sound(self):
        if not self._opening_box:
            return
        box = EntityManager.getentity(self._opening_box)
        if box and box.logic:
            box.logic.send_event('E_STOP_OPENING_SOUND')

    def _on_carry_bullet_merged(self, transfer_num, put_pos):
        if global_data.player and global_data.player.logic:
            if put_pos == global_data.player.logic.ev_g_wpbar_cur_weapon_pos():
                wp = global_data.player.logic.ev_g_wpbar_cur_weapon()
                show_ratio = wp.get_show_ratio()
                add_num = show_ratio * transfer_num
                global_data.emgr.on_carry_bullet_merged.emit(add_num)