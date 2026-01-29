# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/pve/PVEBuffUI.py
from __future__ import absolute_import
import six
import six_ex
from common.uisys.basepanel import BasePanel
from common.const.uiconst import DIALOG_LAYER_ZORDER, DIALOG_LAYER_BAN_ZORDER, NORMAL_LAYER_ZORDER
from logic.gcommon.common_const.pve_const import EFFECT_TYPE_BLESS, EFFECT_TYPE_ITEM
from common.const import uiconst
from logic.gcommon.time_utility import get_server_time
from logic.gcommon.common_const.buff_const import BUFF_GLOBAL_KEY
from common.utils.timer import CLOCK

class PVEBuffBaseUI(BasePanel):
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT

    def on_init_panel(self):
        self.init_event()
        self.buff_item_tmpl = None
        self.buff_dict = {}
        self.need_update_layer_buff = {}
        self.timer_id = None
        self.on_camera_player_setted()
        return

    def init_event(self):
        econf = {'battle_add_pve_buff': self.add_pve_buff,
           'battle_remove_pve_buff': self.remove_buff,
           'player_destroy_event': self.remove_all_buff,
           'scene_camera_player_setted_event': self.on_camera_player_setted
           }
        emgr = global_data.emgr
        emgr.bind_events(econf)

    def get_buff_item_tmpl(self, buff_id):
        if not self.buff_item_tmpl:
            self.buff_item_tmpl = global_data.uisystem.load_template('buff/i_battle_buff_pve')
        return self.buff_item_tmpl

    def destroy_self(self):
        global_data.ui_mgr.close_ui(self)

    def remove_all_buff(self):
        self.need_update_layer_buff = {}
        if self.timer_id:
            global_data.game_mgr.unregister_logic_timer(self.timer_id)
            self.timer_id = None
        buff_ids = six_ex.keys(self.buff_dict)
        for b_id in buff_ids:
            self.remove_buff(self.buff_dict[b_id].effect_type, b_id)

        return

    def on_finalize_panel(self):
        self.remove_all_buff()

    def add_pve_buff(self, effect_type, buff_id, start_time, end_time):
        from common.cfg import confmgr
        if effect_type == EFFECT_TYPE_BLESS:
            conf = confmgr.get('bless_data', str(buff_id), default={})
        else:
            conf = confmgr.get('pve_shop_data', str(buff_id), default={})
        icon_bar = conf.get('buff_icon', None)
        if not icon_bar:
            return
        else:
            nd_progress = None
            buff_item_list = self.panel.list_buff_pve
            if buff_id in self.buff_dict:
                nd_progress = self.buff_dict[buff_id]
            else:
                nd_progress = buff_item_list.AddItem(self.get_buff_item_tmpl(buff_id))
            nd_progress.effect_type = effect_type
            bar = nd_progress.buff_bar
            bar.SetDisplayFrameByPath('', icon_bar)
            elem_id = confmgr.get('bless_data', str(buff_id), 'elem_id', default=None)
            elem_conf = confmgr.get('bless_element_data', elem_id, default={})
            progress = nd_progress.progress_buff
            has_progress = not elem_id and end_time > 0
            progress.setVisible(bool(not elem_id))
            elem_panel = elem_conf.get('buff_panel', None)
            has_elem_panel = bool(elem_panel)
            nd_progress.bar.setVisible(not has_elem_panel)
            nd_progress.elem_bar.setVisible(has_elem_panel)
            if has_elem_panel:
                nd_progress.elem_bar.SetDisplayFrameByPath('', 'gui/ui_res_2/pve/{}'.format(elem_panel))
            self.buff_dict[buff_id] = nd_progress
            if has_progress:
                cur_start_time = get_server_time()
                remain_time = end_time - cur_start_time
                duration = end_time - start_time
                progress.setPercentage(int(remain_time / duration * 100))
                if duration and remain_time > 0:

                    def update_progress_time(dt, progress=progress):
                        cur_time = get_server_time()
                        cur_percent = min((cur_time - cur_start_time + (duration - remain_time)) / float(duration) * 100, 100)
                        progress.setPercentage(100 - cur_percent)

                    progress.stopAllActions()
                    progress.TimerAction(update_progress_time, remain_time, callback=lambda : self.on_delay_remove(buff_id), interval=0.05)
                else:
                    self.on_delay_remove(buff_id)
                    return
            show_buff_layer = conf.get('show_buff_layer', None)
            nd_progress.lab_layer.setVisible(False)
            nd_progress.buff_bar.setVisible(True)
            if show_buff_layer:
                self.need_update_layer_buff[buff_id] = show_buff_layer
                if not self.timer_id:
                    self.timer_id = global_data.game_mgr.register_logic_timer(self.update_buff_layer, 0.1, mode=CLOCK)
            return

    def update_buff_layer(self):
        from common.cfg import confmgr
        for buff_id, show_buff_layer in six.iteritems(self.need_update_layer_buff):
            layer = 0
            if global_data.cam_lctarget:
                layer = global_data.cam_lctarget.ev_g_get_buff_cnt(BUFF_GLOBAL_KEY, show_buff_layer)
            if layer > 0:
                if buff_id not in self.buff_dict:
                    self.add_pve_buff(EFFECT_TYPE_BLESS, buff_id, 0, 0)
                nd_progress = self.buff_dict.get(buff_id, None)
                if nd_progress:
                    elem_id = confmgr.get('bless_data', str(buff_id), 'elem_id', default=None)
                    show_layer = layer > 1 and elem_id is not None
                    nd_progress.lab_layer.setVisible(show_layer)
                    nd_progress.buff_bar.setVisible(not show_layer)
                    nd_progress.lab_layer.SetString(str(layer))
            elif buff_id in self.buff_dict:
                self.on_delay_remove(buff_id, remove_from_update_list=False)

        return

    def remove_buff(self, effect_type, effect_id):
        if effect_id in self.buff_dict:
            self.on_delay_remove(effect_id)

    def on_delay_remove(self, buff_id, remove_from_update_list=True):
        nd_progress = self.buff_dict.get(buff_id)
        if not nd_progress:
            return
        else:
            nd_progress.stopAllActions()
            buff_item_list = self.panel.list_buff_pve
            idx = buff_item_list.getIndexByItem(nd_progress)
            buff_item_list.DeleteItemIndex(idx)
            del self.buff_dict[buff_id]
            if remove_from_update_list and buff_id in self.need_update_layer_buff:
                del self.need_update_layer_buff[buff_id]
                if self.timer_id and not self.need_update_layer_buff:
                    global_data.game_mgr.unregister_logic_timer(self.timer_id)
                    self.timer_id = None
            return

    def on_camera_player_setted(self, *args):
        self.remove_all_buff()
        self.on_ctrl_target_changed()

    def on_ctrl_target_changed(self):
        self.remove_all_buff()
        if not global_data.cam_lplayer:
            return
        control_target = global_data.cam_lplayer
        pve_effect_data = control_target.ev_g_pve_effect_data()
        if not pve_effect_data:
            return
        for effect_type, buffs in six.iteritems(pve_effect_data):
            for buff_id, info in six.iteritems(buffs):
                start_time, end_time = info
                self.add_pve_buff(effect_type, buff_id, start_time, end_time)


class PVEBuffUI(PVEBuffBaseUI):
    PANEL_CONFIG_NAME = 'buff/battle_buff_pve'