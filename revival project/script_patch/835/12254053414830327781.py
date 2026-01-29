# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/BattleBuffUI.py
from __future__ import absolute_import
import six
import six_ex
from common.cfg import confmgr
from logic.comsys.effect import ui_effect
from common.uisys.basepanel import BasePanel
from common.const.uiconst import DIALOG_LAYER_ZORDER, DIALOG_LAYER_BAN_ZORDER, NORMAL_LAYER_ZORDER
from logic.gcommon.item import item_const
from logic.gcommon.common_const.buff_const import BUFF_GLOBAL_KEY, BUFF_SET_FIRE, BUFF_ID_ZOMBIEFFA_MECHA_BLOOD, BUFF_ID_ZOMBIEFFA_MECHA_TUFF
from logic.gcommon import time_utility
from common.cfg import confmgr
from logic.gcommon.common_utils import text_utils
from logic.gcommon.common_const.buff_const import BUFF_ID_BOND_GIFT_HP_DOWN_SHIELD_CD
from common.const import uiconst
from mobile.common.EntityManager import EntityManager
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gutils.client_unit_tag_utils import register_unit_tag
import cc
BUFF_TARGET_TAG_VALUE = register_unit_tag(('LAvatar', 'LPuppet', 'LMechaTrans'))

class BattleBuffBaseUI(BasePanel):
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT

    def on_init_panel(self):
        self.init_event()
        self.buff_item_tmpl = None
        self.zombieffa_buff_item_tmpl = None
        self.buff_dict = {}
        self.cur_cam_target_id = None
        self._cur_buff_target_name = None
        self._cur_buff_target_mask = 0
        self._cur_buff_owner = None
        self._wait_add_buff_list = []
        self.add_buff_timer_id = None
        self.on_camera_player_setted()
        return

    def init_event(self):
        econf = {'battle_add_buff': self.add_player_buff,
           'battle_add_mecha_buff': self.add_mecha_buff,
           'battle_remove_buff': self.remove_buff,
           'battle_remove_mecha_buff': self.remove_buff,
           'player_destroy_event': self.remove_all_buff,
           'human_need_update_buff_icon_vis': self.set_buff_icon_vis,
           'scene_camera_target_setted_event': self.on_camera_player_setted,
           'switch_control_target_event': self.on_ctrl_target_changed,
           'battle_update_buff_show_val': self.update_buff_show_val
           }
        emgr = global_data.emgr
        emgr.bind_events(econf)

    def get_buff_item_tmpl(self, buff_id):
        buff_ext_info = confmgr.get('c_buff_data', str(buff_id), 'ExtInfo', default={})
        if 'buff_show_val' in buff_ext_info or 'buff_show_fix_val' in buff_ext_info:
            if not self.zombieffa_buff_item_tmpl:
                self.zombieffa_buff_item_tmpl = global_data.uisystem.load_template('buff/i_buff_item_ffa3')
            return self.zombieffa_buff_item_tmpl
        if not self.buff_item_tmpl:
            self.buff_item_tmpl = global_data.uisystem.load_template('buff/i_buff_item')
        return self.buff_item_tmpl

    def destroy_self(self):
        global_data.ui_mgr.close_ui(self)

    def remove_all_buff(self):
        self.cur_cam_target_id = None
        self._cur_buff_target_name = None
        self._cur_buff_target_mask = 0
        buff_ids = six_ex.keys(self.buff_dict)
        for b_id in buff_ids:
            self.remove_buff(b_id, delay_remove=False)

        return

    def on_finalize_panel(self):
        self.remove_all_buff()

    def add_player_buff(self, buff_id, remain_time, add_time, duration, buff_data):
        if self._cur_buff_target_mask & BUFF_TARGET_TAG_VALUE:
            if global_data.cam_lplayer:
                if not global_data.cam_lplayer.ev_g_buff_icon_visibility(buff_id):
                    return
            self.try_add_buff_count_down(buff_id, remain_time, add_time, duration, buff_data)

    def add_mecha_buff(self, buff_id, remain_time, add_time, duration, buff_data):
        if self._cur_buff_target_name == 'LMecha':
            self.try_add_buff_count_down(buff_id, remain_time, add_time, duration, buff_data)

    def try_add_buff_count_down(self, buff_id, remain_time, add_time, duration, buff_data):
        self._wait_add_buff_list.append((buff_id, remain_time, add_time, duration, buff_data))
        if not self.add_buff_timer_id:
            self.add_buff_timer_id = global_data.game_mgr.register_logic_timer(self.add_buff_tick, 1)

    def add_buff_tick(self):
        if self._wait_add_buff_list:
            self.add_buff_count_down(*self._wait_add_buff_list.pop(0))
        if not self._wait_add_buff_list:
            global_data.game_mgr.unregister_logic_timer(self.add_buff_timer_id)
            self.add_buff_timer_id = None
        return

    def add_buff_count_down(self, buff_id, remain_time, add_time, duration, buff_data):
        if buff_id == 101:
            return
        else:
            conf = confmgr.get('c_buff_data', str(buff_id))
            from logic.gcommon import time_utility
            icon_bar = conf.get('IconPath', None)
            if not icon_bar:
                return
            progress_bar = conf.get('ProgressPath', 'gui/ui_res_2/battle/buff/buff_progress_yellow.png')
            nd_progress = None
            buff_item_list = self.panel.temp_buff.list_buff
            if buff_id in self.buff_dict:
                nd_progress = self.buff_dict[buff_id]
            else:
                nd_progress = buff_item_list.AddItem(self.get_buff_item_tmpl(buff_id))
            progress = nd_progress.progress_buff
            progress.SetProgressTexture(progress_bar)
            bar = nd_progress.buff_bar
            bar.SetDisplayFrameByPath('', icon_bar)
            cur_start_time = time_utility.get_server_time()
            if remain_time and duration:
                if buff_id == BUFF_ID_BOND_GIFT_HP_DOWN_SHIELD_CD:
                    progress.setPercentage(int((duration - remain_time) / duration * 100))
                else:
                    progress.setPercentage(int(remain_time / duration * 100))
            extra_info = conf.get('ExtInfo', {})
            if extra_info.get('icon_gray', False):
                ui_effect.set_gray(bar, True)
            if duration and remain_time > 0:

                def finish():
                    idx = buff_item_list.getIndexByItem(nd_progress)
                    buff_item_list.DeleteItemIndex(idx)
                    del self.buff_dict[buff_id]

                def finish_after_animation():
                    nd_progress.runAction(cc.Sequence.create([
                     cc.CallFunc.create(lambda : nd_progress.img_light.setVisible(True)),
                     cc.CallFunc.create(lambda : nd_progress.PlayAnimation('enough')),
                     cc.DelayTime.create(nd_progress.GetAnimationMaxRunTime('enough') * 2),
                     cc.CallFunc.create(lambda : finish())]))

                def update_progress_time(dt):
                    cur_time = time_utility.get_server_time()
                    cur_percent = min((cur_time - cur_start_time + (duration - remain_time)) / float(duration) * 100, 100)
                    if buff_id == BUFF_ID_BOND_GIFT_HP_DOWN_SHIELD_CD:
                        progress.setPercentage(cur_percent)
                    else:
                        progress.setPercentage(100 - cur_percent)

                progress.stopAllActions()
                timer_cb = finish
                if buff_id == BUFF_ID_BOND_GIFT_HP_DOWN_SHIELD_CD:
                    timer_cb = finish_after_animation
                progress.TimerAction(update_progress_time, remain_time, callback=timer_cb, interval=0.05)
            self.buff_dict[buff_id] = nd_progress
            buff_ext_info = conf.get('ExtInfo', {})
            if 'buff_show_val' in buff_ext_info or 'buff_show_fix_val' in buff_ext_info:
                nd_progress.lab_num.SetString('')
                nd_progress.DelayCall(0.03, lambda : self.update_buff_val(nd_progress, buff_id))
            if buff_id in BUFF_SET_FIRE:
                nd_progress.vx.setVisible(True)
                nd_progress.PlayAnimation('burnning')
            handler = extra_info.get('handle_func', None)
            if handler:
                hdl_name = 'handle_' + handler
                handler_func = getattr(self, hdl_name) if hasattr(self, hdl_name) else None
                handler_func(nd_progress, conf, buff_data)
            return

    def update_buff_val(self, nd_progress, buff_id, val_dict=None):
        if not self._cur_buff_owner:
            return
        else:
            buff_ext_info = confmgr.get('c_buff_data', str(buff_id), 'ExtInfo', default={})
            if 'buff_show_fix_val' in buff_ext_info:
                nd_progress.lab_num.SetString(buff_ext_info['buff_show_fix_val'])
            elif 'buff_show_val' in buff_ext_info:
                buff_show_val_format = buff_ext_info['buff_show_val']
                safe_dict = text_utils.parse_safe_dict(buff_show_val_format)
                if val_dict is not None:
                    safe_dict = {key:val_dict.get(key) for key in six_ex.keys(safe_dict)}
                elif global_data.cam_lplayer:
                    safe_dict = {key:self._cur_buff_owner.ev_g_get_buff_val_by_field(buff_id, key) for key in six_ex.keys(safe_dict)}
                for k in six_ex.keys(safe_dict):
                    if not safe_dict[k]:
                        safe_dict.pop(k)

                nd_progress.lab_num.SetString(text_utils.safe_format(buff_show_val_format, safe_dict))
            return

    def update_buff_show_val(self, buff_id, val_dict):
        if buff_id not in self.buff_dict:
            return
        nd_progress = self.buff_dict[buff_id]
        self.update_buff_val(nd_progress, buff_id, val_dict)

    def remove_buff(self, buff_id, *args, **kwargs):
        if buff_id == 101 or buff_id not in self.buff_dict:
            return
        nd_progress = self.buff_dict[buff_id]
        nd_progress.DelayCall(0.03, lambda : self.on_delay_remove(buff_id))

    def on_delay_remove(self, buff_id):
        if not self._cur_buff_owner:
            return
        buff_cnt = self._cur_buff_owner.ev_g_get_buff_cnt(BUFF_GLOBAL_KEY, buff_id)
        if buff_cnt and buff_cnt > 0:
            return
        nd_progress = self.buff_dict.get(buff_id)
        if not nd_progress:
            return
        nd_progress.stopAllActions()
        buff_item_list = self.panel.temp_buff.list_buff
        idx = buff_item_list.getIndexByItem(nd_progress)
        buff_item_list.DeleteItemIndex(idx)
        del self.buff_dict[buff_id]

    def on_camera_player_setted(self, *args):
        if global_data.cam_lctarget is None:
            self.remove_all_buff()
        elif global_data.cam_lctarget.id != self.cur_cam_target_id:
            self.remove_all_buff()
            self.on_ctrl_target_changed()
            self.cur_cam_target_id = global_data.cam_lctarget.id
        return

    def on_ctrl_target_changed(self, *args):
        from mobile.common.EntityManager import EntityManager
        self.remove_all_buff()
        if not global_data.cam_lctarget or not global_data.cam_lplayer:
            return
        control_target = global_data.cam_lctarget
        target_type = control_target.__class__.__name__
        if target_type == self._cur_buff_target_name:
            return
        self._cur_buff_target_name = target_type
        self._cur_buff_target_mask = control_target.MASK
        buffs_list = []
        if target_type != 'LMechaTrans':
            buffs = control_target.ev_g_get_buff_data() or {}
            buffs_list.append(buffs)
            buff_owner = global_data.cam_lctarget
        else:
            buffs = global_data.cam_lplayer.ev_g_get_buff_data() or {}
            buffs_list.append(buffs)
            buff_owner = global_data.cam_lplayer
            driver_id = control_target.sd.ref_driver_id
            entity = EntityManager.getentity(driver_id)
            if entity:
                buffs_list.append(entity.logic.ev_g_get_buff_data() or {})
        self._cur_buff_owner = buff_owner
        for buffs in buffs_list:
            for buff_key_set in six.itervalues(buffs):
                for buff_id, buff_id_set in six.iteritems(buff_key_set):
                    self.add_buff_helper(buff_owner, buff_id, buff_id_set)

    def add_buff_helper(self, buff_owner, buff_id, buff_id_set):
        if self._cur_buff_target_mask & BUFF_TARGET_TAG_VALUE:
            vis = buff_owner.ev_g_buff_icon_visibility(buff_id)
            if not vis:
                return
        for data in six.itervalues(buff_id_set):
            duration = data.get('duration', 0)
            add_time = data.get('add_time', 0)
            left_time = add_time + duration - time_utility.get_server_time()
            if left_time > duration:
                left_time = duration if 1 else left_time
                self.try_add_buff_count_down(buff_id, left_time, add_time, duration, data)

    def set_buff_icon_vis(self, target_buff_id, vis):
        if not vis:
            self.remove_buff(target_buff_id)
        elif not global_data.cam_lplayer:
            return
        buffs = global_data.cam_lplayer.ev_g_get_buff_data() or {}
        for buff_key_set in six.itervalues(buffs):
            for buff_id, buff_id_set in six.iteritems(buff_key_set):
                if buff_id == target_buff_id:
                    self.add_buff_helper(global_data.cam_lplayer, buff_id, buff_id_set)

    def handle_update_visible(self, nd_progress, conf, buff_data):
        if not nd_progress:
            return

        def on_update(near_dist=buff_data.get('near_dist', 0)):
            if not global_data.death_battle_data or not global_data.player:
                return
            team_crown_id = global_data.death_battle_data.get_team_crown_id()
            if team_crown_id:
                entity = EntityManager.getentity(team_crown_id)
                if entity:
                    crown_pos = entity.logic.ev_g_position()
                    player_pos = global_data.cam_lplayer.ev_g_position()
                    dis_direction = crown_pos - player_pos
                    nd_progress.setVisible(near_dist >= dis_direction.length / NEOX_UNIT_SCALE)
            else:
                nd_progress.setVisible(False)

        nd_progress.runAction(cc.RepeatForever.create(cc.Sequence.create([
         cc.DelayTime.create(0.1),
         cc.CallFunc.create(on_update)])))


class BattleBuffUI(BattleBuffBaseUI):
    PANEL_CONFIG_NAME = 'battle/battle_buff_ui'