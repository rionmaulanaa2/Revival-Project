# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/PickUI.py
from __future__ import absolute_import
import six
from six.moves import range
import cc
import queue
import world
from logic.gutils.hot_key_utils import is_down_msg
from common.const.uiconst import NORMAL_LAYER_ZORDER
from common.uisys.basepanel import BasePanel
from common.uisys.uielment.CCLabel import CCLabel
from logic.gcommon.cdata.status_config import ST_PICK, ST_RELOAD, ST_RELOAD_LOOP, ST_LOAD, ST_USE_ITEM
from logic.gcommon.cdata import mecha_status_config
from logic.gcommon.item.backpack_item_type import B_ITEM_TYPE_BULLET
from logic.comsys.battle.PickUIListView import CListViewMgr
from logic.comsys.archive.archive_manager import ArchiveManager
from logic.gcommon.common_const.battle_const import MARK_RES, MARK_WAY_DOUBLE_CLICK
from logic.gutils.hot_key_utils import set_hot_key_common_tip
from data.hot_key_def import PICK_THING, MARK_ITEM
from logic.gutils import item_utils
from logic.gcommon import const
from mobile.common.EntityManager import EntityManager
import weakref
import game3d
from common.utils.cocos_utils import CCSizeZero, CCPointZero, ccp
from data import hot_key_def
from logic.gcommon.common_const.ui_operation_const import WEAPON_PICK_DIRECTLY_REPLACE_KEY
DX_TO_DY = 1.3
WEAPON_POS_LIST = [
 const.PART_WEAPON_POS_MAIN1, const.PART_WEAPON_POS_MAIN2, const.PART_WEAPON_POS_MAIN3]
REPLACE_ITEM_IDX_END = 3

def hot_key_wrapper_for_pickui(func):

    def wrapped--- This code section failed: ---

  37       0  LOAD_GLOBAL           0  'len'
           3  LOAD_FAST             0  'args'
           6  CALL_FUNCTION_1       1 
           9  LOAD_CONST            1  1
          12  COMPARE_OP            5  '>='
          15  POP_JUMP_IF_FALSE    88  'to 88'

  38      18  POP_JUMP_IF_FALSE     2  'to 2'
          21  BINARY_SUBSCR    
          22  STORE_FAST            2  'self'

  39      25  LOAD_GLOBAL           1  'isinstance'
          28  LOAD_FAST             2  'self'
          31  LOAD_GLOBAL           2  'PickUI'
          34  CALL_FUNCTION_2       2 
          37  POP_JUMP_IF_FALSE    72  'to 72'

  40      40  LOAD_FAST             2  'self'
          43  LOAD_ATTR             3  'is_on_show'
          46  CALL_FUNCTION_0       0 
          49  POP_JUMP_IF_TRUE     56  'to 56'

  41      52  LOAD_GLOBAL           4  'False'
          55  RETURN_END_IF    
        56_0  COME_FROM                '49'

  43      56  LOAD_DEREF            0  'func'
          59  LOAD_FAST             0  'args'
          62  LOAD_FAST             1  'kwargs'
          65  CALL_FUNCTION_VAR_KW_0     0 
          68  RETURN_VALUE     
          69  JUMP_ABSOLUTE       101  'to 101'

  45      72  LOAD_DEREF            0  'func'
          75  LOAD_FAST             0  'args'
          78  LOAD_FAST             1  'kwargs'
          81  CALL_FUNCTION_VAR_KW_0     0 
          84  RETURN_END_IF    
        85_0  COME_FROM                '18'
          85  JUMP_FORWARD         13  'to 101'

  47      88  LOAD_DEREF            0  'func'
          91  LOAD_FAST             0  'args'
          94  LOAD_FAST             1  'kwargs'
          97  CALL_FUNCTION_VAR_KW_0     0 
         100  RETURN_VALUE     
       101_0  COME_FROM                '85'

Parse error at or near `POP_JUMP_IF_FALSE' instruction at offset 18

    return wrapped


from common.const import uiconst

class PickUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle/fight_pick'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    AUTO_PICK_INTERVAL = 0.3
    MAXITEMNUM = 10
    HOT_KEY_FUNC_MAP = {'pick_thing': 'keyboard_pick_thing',
       'mark_item.DOWN_UP': 'keyboard_mark_item',
       hot_key_def.PICK_SCROLL_UP: 'keyboard_pick_scroll_up',
       hot_key_def.PICK_SCROLL_DOWN: 'keyboard_pick_scroll_down',
       'pick_item_replace_1': ('keyboard_replace_item_down', 0),
       'pick_item_replace_2': ('keyboard_replace_item_down', 1),
       'pick_item_replace_3': ('keyboard_replace_item_down', 2)
       }
    HOT_KEY_FUNC_MAP_SHOW = {hot_key_def.PICK_SCROLL_UP: {'node': 'arrow_up_pc'},hot_key_def.PICK_SCROLL_DOWN: {'node': 'arrow_down_pc'},hot_key_def.MOUSE_WHEEL_MSG: {'node': 'nd_mouse_pc'}}

    def on_init_panel(self):
        from logic.gcommon.common_const.ui_operation_const import PICK_ZORDER
        self.panel.middle.setVisible(False)
        self.panel.setLocalZOrder(PICK_ZORDER)
        self.init_parameters()
        self.process_event(True)
        self.init_mouse_keyboard_parameter()
        self.init_panel()

    def init_parameters(self):
        self._has_no_near_item = True
        self.player = None
        self.is_play_pick_ani = False
        self._pickable_info_list = []
        self._pick_entity_id_list = []
        self._open_package = None
        self.is_opened_deadbox = False
        self.list_scroll_to_top = True
        self._pickable_list_width, _ = self.panel.lv_pickable_list.GetContentSize()
        self._begin_time = 0
        self._touch_pos = None
        self._touch_tick = 0
        self._auto_pick_enable = False
        self._pick_time = 0
        self._auto_pick_timer = None
        self._is_list_bar_visible = True
        self._item_queue = queue.Queue()
        self._update_timer = None
        self._old_package_list = []
        self.cur_open_weapon_entity_id = None
        self._sview_index = 0
        self._is_check_sview = False
        self.all_item_data_list = []
        self.pre_all_item_type = []
        self.cur_open_weapon_item = None
        self.cur_camera_state_type = None
        self.archive_data = ArchiveManager().get_archive_data('guide')
        self.has_show_pick_guide = True if self.archive_data.get_field('has_show_pick_guide_effect') else False
        self.listview_mgr = CListViewMgr(weakref.ref(self.panel))
        self._enable_weapon_directly_replace = False
        self._last_try_pick_item_id = None
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'scene_player_setted_event': self.on_player_setted,
           'scene_update_pick_info_event': self.show_pickable_ui,
           'camera_switch_to_state_event': self.on_camera_switch_to_state,
           'player_enable_auto_pick_event': self.on_auto_pick_event,
           'avatar_mecha_main_or_sub_atk_start': self.on_avatar_mecha_main_or_sub_atk_start,
           'player_user_setting_changed_event': self.on_user_setting_changed
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_panel(self):
        from logic.comsys.setting_ui.CustomUIProxy import init_custom_com
        init_custom_com(self, {})
        scn = world.get_active_scene()
        player = scn.get_player()
        if player:
            self.on_player_setted(player)
        if global_data.ui_mgr.get_ui('BigMapUI'):
            self.add_hide_count('BigMapUI')
        self.show_pickable_ui(self._pickable_info_list)

        @self.panel.box.unique_callback()
        def OnClick(btn, touch):
            if self._has_no_near_item:
                return
            self.panel.box.setVisible(self._is_list_bar_visible)
            self._is_list_bar_visible = not self._is_list_bar_visible
            self.panel.list_bar.setVisible(self._is_list_bar_visible)
            self.panel.list_bar_title.setVisible(self._is_list_bar_visible)
            if self._is_list_bar_visible:
                self.on_show_pick_list()
            else:
                self.on_hide_pick_list()

        if global_data.cam_data:
            self.on_camera_switch_to_state(global_data.cam_data.camera_state_type)

        @self.panel.lv_pickable_list.unique_callback()
        def OnScrolling(sender):
            self.check_bounding()
            if self._is_check_sview == False:
                self._is_check_sview = True
                self.SetTimeOut(0.2, self.check_sview)

        self.panel.lv_pickable_list.DeleteAllSubItem()

    def is_on_show(self):
        return (self.panel.box.isVisible() or self.panel.list_bar_title.isVisible()) and self.panel.isVisible()

    def check_bounding(self):
        pickable_list = self.panel.lv_pickable_list
        count = pickable_list.GetItemCount()
        self.panel.icon_up.setVisible(False)
        self.panel.icon_down.setVisible(False)
        if not count:
            return
        top_widget = pickable_list.GetItem(0)
        bottom_widget = pickable_list.GetItem(count - 1)
        iw, ih = top_widget.GetContentSize()
        w, h = pickable_list.GetContentSize()
        inner_size = pickable_list.GetInnerContentSize()
        off_pos = pickable_list.GetContentOffset()
        self.panel.icon_down.setVisible(abs(off_pos.y) > ih * 0.8)
        self.panel.icon_up.setVisible(inner_size.height - h - abs(off_pos.y) > ih * 0.8)

    def on_finalize_panel(self):
        self.clear_auto_pick()
        self.player_regist_event(False)
        self.player = None
        if self.custom_ui_com:
            self.custom_ui_com.destroy()
            self.custom_ui_com = None
        self.listview_mgr and self.listview_mgr.on_destroy()
        self.listview_mgr = None
        self.process_event(False)
        return

    def do_hide_panel(self):
        super(PickUI, self).do_hide_panel()
        self.clear_auto_pick()
        global_data.emgr.scene_pick_show_item_list.emit(False)

    def do_show_panel(self):
        super(PickUI, self).do_show_panel()
        self.show_pickable_ui(self._pickable_info_list)

    def player_regist_event(self, is_regist):
        if not self.player:
            return
        player = self.player
        if is_regist:
            player.regist_event('E_ITEM_DATA_CHANGED', self.on_item_data_changed)
            player.regist_event('E_CLOTHING_CHANGED', self.on_item_data_changed)
            player.regist_event('E_WEAPON_DATA_DELETED_SUCCESS', self.on_item_data_changed)
            player.regist_event('E_WPBAR_SWITCH_CUR', self.on_item_data_changed)
            player.regist_event('E_SUCCESS_RIGHT_AIM', self.on_success_right_aim)
            player.regist_event('E_SUCCESS_AIM', self.on_success_aim)
            player.regist_event('E_ATTACK_START', self.on_attack_start)
            player.regist_event('E_SUCCESS_SAVED', self.on_saved)
            player.regist_event('E_DEATH', self.on_died)
        else:
            player.unregist_event('E_ITEM_DATA_CHANGED', self.on_item_data_changed)
            player.unregist_event('E_CLOTHING_CHANGED', self.on_item_data_changed)
            player.unregist_event('E_WEAPON_DATA_DELETED_SUCCESS', self.on_item_data_changed)
            player.unregist_event('E_WPBAR_SWITCH_CUR', self.on_item_data_changed)
            player.unregist_event('E_SUCCESS_RIGHT_AIM', self.on_success_right_aim)
            player.unregist_event('E_SUCCESS_AIM', self.on_success_aim)
            player.unregist_event('E_ATTACK_START', self.on_attack_start)
            player.unregist_event('E_SUCCESS_SAVED', self.on_saved)
            player.unregist_event('E_DEATH', self.on_died)

    def on_player_setted(self, player):
        self.player_regist_event(False)
        self.player = player
        if player is None:
            self.panel.middle.setVisible(False)
            return
        else:
            self.panel.middle.setVisible(True)
            self._open_package = None
            self.player_regist_event(True)
            self.on_item_data_changed()
            from logic.gcommon.common_const.ui_operation_const import AUTO_PICK_KEY, WEAPON_PICK_DIRECTLY_REPLACE_KEY
            self.on_auto_pick_event(global_data.player.get_setting(AUTO_PICK_KEY))
            self.on_user_setting_changed(WEAPON_PICK_DIRECTLY_REPLACE_KEY, global_data.player.get_setting(WEAPON_PICK_DIRECTLY_REPLACE_KEY))
            self.check_player_alive()
            return

    def refresh_pickable_list(self, *args):
        self.show_pickable_ui(self._pickable_info_list)

    def on_item_data_changed(self, *args):
        if not self.player:
            return
        else:
            in_mecha = self.player.ev_g_in_mecha()
            cur_weapon_pos = self.player.share_data.ref_wp_bar_cur_pos
            is_empty_hand_or_main_weapon = cur_weapon_pos in (const.PART_WEAPON_POS_NONE, const.PART_WEAPON_POS_MAIN_DF)
            if not (item_utils.is_weapon_full(self.player) and (in_mecha or not in_mecha and is_empty_hand_or_main_weapon)):
                if self.cur_open_weapon_item:
                    self.cur_open_weapon_item.PlayAnimation('recover')
                    self.cur_open_weapon_entity_id = None
                    self.cur_open_weapon_item = None
            self.refresh_pickable_list()
            return

    def on_success_right_aim(self, *args):
        self.reroll_package_ui()

    def on_success_aim(self, *args):
        self.reroll_package_ui()

    def on_attack_start(self, *args):
        self.reroll_package_ui()

    def on_avatar_mecha_main_or_sub_atk_start(self, *args):
        self.reroll_package_ui()

    def get_all_item_in_pickable(self, pickable_info_list):
        pickable_list = []
        for item_info in pickable_info_list:
            entity_id, item_data = item_info
            pickable_list.append((entity_id, None, item_data))
            attachments = item_data.get('attachment', {})
            for attachment in six.itervalues(attachments):
                pickable_list.append((attachment['entity_id'], entity_id, attachment))

        return pickable_list

    def init_package(self):
        from logic.gutils import template_utils
        package = self.panel

        @package.btn_close.unique_callback()
        def OnClick(btn, touch):
            if self._has_no_near_item:
                return
            self._is_list_bar_visible = False
            self.panel.box.setVisible(True)
            self.panel.list_bar.setVisible(False)
            self.panel.list_bar_title.setVisible(False)
            self.on_hide_pick_list()

    def clear_auto_pick(self):
        tm = global_data.game_mgr.get_logic_timer()
        if self._auto_pick_timer:
            tm.unregister(self._auto_pick_timer)
            self._auto_pick_timer = None
        return

    def check_auto_pick(self, pickable_list, unavailable_list):
        if pickable_list or unavailable_list:
            import time
            now = time.time()
            if now - self._pick_time > self.AUTO_PICK_INTERVAL - 0.01:
                self.clear_auto_pick()
                self.auto_pick(pickable_list, unavailable_list)
            else:
                self.regist_pick_timer(pickable_list, unavailable_list)
            param = ('E_GUIDE_PICK_SHOW', 2)
        else:
            self.clear_auto_pick()
            param = ('E_GUIDE_PICK_SHOW', 1)
        logic = global_data.player.logic if global_data.player else None
        if logic:
            logic.send_event(*param)
        return

    def regist_pick_timer(self, pickable_list, unavailable_list):
        self.clear_auto_pick()
        tm = global_data.game_mgr.get_logic_timer()
        from common.utils.timer import CLOCK
        self._auto_pick_timer = tm.register(func=self.auto_pick, interval=self.AUTO_PICK_INTERVAL, times=-1, args=(
         pickable_list, unavailable_list), mode=CLOCK)

    def auto_pick(self, pickable_list, unavailable_list):
        if not global_data.player or not self.player:
            return
        else:
            import time
            now = time.time()
            if now - self._pick_time < self.AUTO_PICK_INTERVAL - 0.01:
                return
            if not self._auto_pick_enable:
                self.clear_auto_pick()
                return
            if self.is_play_pick_ani:
                return
            is_bag_full = self.check_is_bag_full()
            ctarget = self.player.ev_g_control_target()
            if ctarget and ctarget.logic:
                if ctarget.logic.ev_g_is_in_any_state([ST_RELOAD, ST_RELOAD_LOOP, ST_LOAD, ST_USE_ITEM]) or ctarget.logic.ev_g_is_in_any_state([mecha_status_config.MC_USE_ITEM, mecha_status_config.MC_RELOAD]):
                    self.regist_pick_timer(pickable_list, unavailable_list)
                    return
            if not self.player.ev_g_status_check_pass(ST_PICK):
                self.regist_pick_timer(pickable_list, unavailable_list)
                return
            from logic.gcommon.item import item_utility as iutil
            from common.cfg import confmgr
            need_weapon = not item_utils.is_weapon_full(self.player)
            for entity_id, weapon_entity_id, item_data in pickable_list:
                item_no = item_data['item_id']
                if self.check_is_full_cnt(item_no) and is_bag_full:
                    continue
                if 'thrower' in item_data and global_data.player.id == item_data['thrower']:
                    continue
                if item_utils.is_gun(item_no):
                    weapons = self.player.ev_g_all_weapons()
                    upgrade_level = confmgr.get('item', str(item_data['item_id']), 'level')
                    iShader = confmgr.get('item', str(item_data['item_id']), 'iShader')
                    if need_weapon:
                        if not global_data.battle or global_data.battle._can_pick_same_weapon:
                            self._pick_time = now
                            self.on_pickable_item_pickup(entity_id, weapon_entity_id, item_no, item_data.get('house_entity_id'))
                            return
                        same_type_wp_pos, same_type_wp_id = self.player.ev_g_same_type_weapon_equipped_pos_by_itemid(item_no)
                        if not same_type_wp_id:
                            self._pick_time = now
                            self.on_pickable_item_pickup(entity_id, weapon_entity_id, item_no, item_data.get('house_entity_id'))
                            return
                    for pos, weapon_data in six.iteritems(weapons):
                        weapon_id = weapon_data.get('item_id')
                        weapon_shader = confmgr.get('item', str(weapon_id), 'iShader')
                        weapon_level = confmgr.get('item', str(weapon_id), 'level')
                        if weapon_shader == iShader:
                            if weapon_level < upgrade_level:
                                self._pick_time = now
                                self.on_pickable_item_pickup(entity_id, weapon_entity_id, item_no, item_data.get('house_entity_id'), put_pos=pos)
                                return

                iType = confmgr.get('item', str(item_no), 'type', default=None)
                if iType == B_ITEM_TYPE_BULLET:
                    self._pick_time = now
                    self.on_pickable_item_pickup(entity_id, weapon_entity_id, item_no, item_data.get('house_entity_id'))
                    return
                if not iutil.is_auto_pick_item(str(item_no)):
                    continue
                if is_bag_full:
                    continue
                self._pick_time = now
                self.on_pickable_item_pickup(entity_id, weapon_entity_id, item_no, item_data.get('house_entity_id'))
                return

            self.clear_auto_pick()
            return

    def get_pick_succ(self):
        if not self.player:
            return
        return self.player.ev_g_pick_succ()

    def play_pickup_ani(self, pick_item_list):
        if not self.player:
            return
        else:
            _pick_entity_id_list = []
            for pick_items in pick_item_list:
                key, item_list = pick_items
                pickable_items, unavailable_list = item_utils.get_available_list(self.player, item_list)
                all_pickable_items = pickable_items + unavailable_list
                for id, data in enumerate(all_pickable_items):
                    _pick_entity_id_list.append(data[0])

            del_entity_list = list(set(self._pick_entity_id_list) - set(_pick_entity_id_list))
            self._pick_entity_id_list = _pick_entity_id_list
            if not del_entity_list:
                return
            if not set(del_entity_list).intersection(set(self.get_pick_succ())):
                return
            pickable_list = self.panel.lv_pickable_list
            max_time = 0
            for entity_id in del_entity_list:
                item_widget = None
                for item in pickable_list.GetAllItem():
                    if hasattr(item, 'pick_item_entity_id') and item.pick_item_entity_id == entity_id:
                        item_widget = item
                        break

                if item_widget:
                    ani_name = 'pick'
                    if item_widget.data_index_tag < len(self.pre_all_item_type):
                        if self.pre_all_item_type[item_widget.data_index_tag] == 'empty':
                            ani_name = 'pick2'
                    item_widget.PlayAnimation(ani_name)
                    time = item_widget.GetAnimationMaxRunTime(ani_name)
                    max_time = max(time, max_time)

            if not max_time:
                return

            def _end_cb():
                self._last_try_pick_item_id = None
                self.is_play_pick_ani = False
                self.refresh_pickable_list()
                return

            def _cb(pass_time):
                self.panel.lv_pickable_list._container._refreshItemPos(is_cal_scale=True)
                self.check_bounding()

            self.is_play_pick_ani = True
            self.panel.StopTimerAction()
            _cb(0)
            self.panel.TimerAction(_cb, max_time, callback=_end_cb, interval=0.033)
            return

    def pre_pickable_item_type_list(self, package_list, pick_item_list):
        if not self.player:
            return
        else:
            self.pre_all_item_type = []
            for package_items in package_list:
                self.pre_all_item_type.append('package')

            for pick_items in pick_item_list:
                key, item_list = pick_items
                pickable_items, unavailable_list = item_utils.get_available_list(self.player, item_list)
                all_pickable_items = pickable_items + unavailable_list
                if key is not None:
                    self.pre_all_item_type.append('title')
                if not all_pickable_items:
                    self.pre_all_item_type.append('empty')
                for id, data in enumerate(all_pickable_items):
                    self.pre_all_item_type.append('item')

            return

    def init_pickable_item_list(self, package_list, pick_item_list):
        visible_end_info = self.listview_mgr.get_list_position_y(self.all_item_data_list)
        if not self.player:
            if not global_data.is_judge_ob:
                return
        pickable_list = self.panel.lv_pickable_list
        self.listview_mgr.recycle_item()
        self.all_item_data_list = []
        all_available_items = []
        all_unavailable_list = []
        for package_items in package_list:
            self.all_item_data_list.append(('package', 'battle/i_item_4', False, package_items))

        for pick_items in pick_item_list:
            key, item_list = pick_items
            if self.player:
                pickable_items, unavailable_list = item_utils.get_available_list(self.player, item_list)
            else:
                pickable_items, unavailable_list = item_list, []
            all_available_items = pickable_items + all_available_items
            all_unavailable_list = unavailable_list + all_unavailable_list
            unavailable_count = len(unavailable_list)
            all_pickable_items = pickable_items + unavailable_list
            pickable_items = unavailable_list = None
            if key is not None:
                self.all_item_data_list.append(('pick', 'battle/i_pick_title', False, (key,)))
            if not all_pickable_items:
                self.all_item_data_list.append(('pick', 'battle/i_item_empty', False, ()))
            for id, data in enumerate(all_pickable_items):
                self.all_item_data_list.append(('pick', 'battle/i_item_4', id >= unavailable_count, data))

        visible_end_data_index = min(visible_end_info[1], len(self.all_item_data_list) - 1)
        if self.list_scroll_to_top:
            visible_end_data_index = 0
            self.list_scroll_to_top = False
        index = 0
        self.cur_open_weapon_item = None
        data_count = min(len(self.all_item_data_list) - visible_end_data_index, self.MAXITEMNUM)
        height = 0
        while index < data_count:
            item_widget = self.add_item_elem(self.all_item_data_list[visible_end_data_index + index])
            item_widget.data_index_tag = visible_end_data_index + index
            height += item_widget.getContentSize().height
            index += 1

        self._sview_index = visible_end_data_index + index
        self.check_auto_pick(all_available_items, all_unavailable_list)
        if visible_end_info[2] is None:
            pickable_list.ScrollToTop()
        elif height < visible_end_info[2]:
            pickable_list.ScrollToBottom()
        else:
            pickable_list.getInnerContainer().setPositionY(visible_end_info[2] - height)
        self.check_sview()
        return

    def check_sview(self):
        self._sview_index = self.listview_mgr.auto_additem(self._sview_index, self.all_item_data_list, len(self.all_item_data_list), self.add_item_elem, 300, 300)
        self._is_check_sview = False

    def mark_pick_item(self, entity_id, parent_entity_id=None, house_entity_id=None, mark_item_no=None):
        from logic.gutils import item_utils, map_utils
        if not map_utils.check_can_draw_mark_or_route():
            return
        player = global_data.cam_lplayer
        if not player:
            return
        model, extra_args = item_utils.get_mark_pick_info(entity_id, parent_entity_id, house_entity_id, mark_item_no)
        if model:
            mark_type = MARK_RES
            hit_pos = model.world_position
            if hit_pos:
                player.send_event('E_TRY_DRAW_MAP_MARK', mark_type, hit_pos, extra_args, MARK_WAY_DOUBLE_CLICK)
                map_utils.send_mark_group_msg(mark_type, extra_args)

    def add_item_elem(self, data, is_back_item=True):
        from logic.gutils import template_utils
        pickable_list = self.panel.lv_pickable_list
        key, ui, available, itemdata = data
        if key == 'package':
            entity_id, package_data = itemdata
            if is_back_item:
                item_widget = self.listview_mgr.get_free_item(ui)
            else:
                item_widget = self.listview_mgr.get_free_item(ui, 0)
            item_widget.PlayAnimation('recover')
            template_utils.init_item4_new(item_widget, package_data)
            item_widget.img_ban.setVisible(False)
            item_widget.btn_bar.SetSwallowTouch(False)
            item_widget.btn_recourse_mark.setVisible(True)

            @item_widget.btn_bar.unique_callback()
            def OnBegin(btn, touch, pickable_list=pickable_list):
                import time
                self._begin_time = time.time()
                self._touch_pos = touch.getLocation()
                self._touch_tick = 0
                return True

            @item_widget.btn_recourse_mark.unique_callback()
            def OnClick(btn, touch, entity_id=entity_id):
                self.mark_pick_item(entity_id)

            @item_widget.btn_bar.unique_callback()
            def OnClick(btn, touch, entity_id=entity_id):
                import time
                if time.time() - self._begin_time > btn.PRESS_NEED_TIME:
                    return
                if global_data.is_judge_ob:
                    self.unroll_package(entity_id)
                    return
                player = global_data.player
                if player and player.logic and not player.logic.ev_g_death() and player.logic.ev_g_try_open_box(entity_id):
                    self.unroll_package(entity_id)

            item_widget.btn_bar.set_sound_enable(False)

            @item_widget.btn_bar.unique_callback()
            def OnEnd(btn, touch, pickable_list=pickable_list):
                pass

            return item_widget
        else:
            if key == 'pick':
                if ui == 'battle/i_pick_title':
                    strkey, = itemdata
                    if is_back_item:
                        item_widget = self.listview_mgr.get_free_item(ui)
                    else:
                        item_widget = self.listview_mgr.get_free_item(ui, 0)
                    item_widget.lab_titile.SetString(strkey)
                    return item_widget
                if ui == 'battle/i_item_empty':
                    if is_back_item:
                        item_widget = self.listview_mgr.get_free_item(ui)
                    else:
                        item_widget = self.listview_mgr.get_free_item(ui, 0)
                    return item_widget
                if ui == 'battle/i_item_4':
                    entity_id, parent_entity_id, item_data = itemdata
                    if is_back_item:
                        item_widget = self.listview_mgr.get_free_item(ui)
                    else:
                        item_widget = self.listview_mgr.get_free_item(ui, 0)
                    item_widget.item_sel.setVisible(False)
                    item_widget.item_sel_1.setVisible(False)
                    item_widget.item_sel_2.setVisible(False)
                    item_widget.item_sel_3.setVisible(False)
                    item_no = item_data.get('item_id')
                    house_entity_id = item_data.get('house_entity_id')
                    if self.cur_open_weapon_entity_id == entity_id and global_data.player and global_data.player.logic:
                        self.cur_open_weapon_item = item_widget
                        item_widget.PlayAnimation('show_weapon')
                        item_utils.show_weapon_choose(item_widget, entity_id, parent_entity_id, item_no, house_entity_id, global_data.player.logic)
                    else:
                        item_widget.PlayAnimation('recover')
                    self._init_replace_item_list_hotkey_tips(item_widget)
                    from logic.gutils.pc_utils import is_pc_control_enable
                    self._set_replace_item_list_hotkey_tip_visible(item_widget, is_pc_control_enable())
                    template_utils.init_item4_new(item_widget, item_data, available)
                    is_pickable = item_utils.is_item_pickable(self.player, item_no)
                    need_show_ban = not is_pickable
                    wid = is_pickable or item_data.get('wid')
                    if wid:
                        player_item_data = self.player.ev_g_item_data(const.BACKPACK_PART_CLOTHING, wid) if self.player else None
                        if player_item_data:
                            _cloth_item_data = player_item_data[0] if 1 else None
                            if _cloth_item_data or str(self._last_try_pick_item_id) == str(wid):
                                need_show_ban = False
                    item_widget.img_ban.setVisible(need_show_ban)
                    item_widget.pick_item_entity_id = entity_id
                    item_widget.btn_bar.SetSwallowTouch(False)
                    item_widget.btn_recourse_mark.setVisible(True)

                    @item_widget.btn_bar.unique_callback()
                    def OnBegin(btn, touch):
                        import time
                        self._begin_time = time.time()
                        self._touch_pos = touch.getLocation()
                        self._touch_tick = 0
                        return True

                    @item_widget.btn_recourse_mark.unique_callback()
                    def OnClick(btn, touch, entity_id=entity_id, parent_entity_id=parent_entity_id, house_entity_id=house_entity_id):
                        self.mark_pick_item(entity_id, parent_entity_id, house_entity_id, mark_item_no=item_no)

                    @item_widget.btn_bar.unique_callback()
                    def OnClick(btn, touch, entity_id=entity_id, parent_entity_id=parent_entity_id, item_no=item_no, house_entity_id=house_entity_id):
                        import time
                        if time.time() - self._begin_time > btn.PRESS_NEED_TIME:
                            return
                        if global_data.player and global_data.player.logic:
                            player_logic = global_data.player.logic
                            need_check_weapon = True
                            if not self._enable_weapon_directly_replace:
                                in_mecha = player_logic.ev_g_in_mecha()
                                cur_weapon_pos = player_logic.share_data.ref_wp_bar_cur_pos
                                is_empty_hand_or_main_weapon = cur_weapon_pos in (const.PART_WEAPON_POS_NONE, const.PART_WEAPON_POS_MAIN_DF)
                                need_check_weapon = in_mecha or not in_mecha and is_empty_hand_or_main_weapon
                            if item_utils.is_gun(item_no) and item_utils.is_weapon_full(player_logic) and need_check_weapon:
                                if self.cur_open_weapon_item:
                                    self.cur_open_weapon_item.PlayAnimation('recover')
                                self.cur_open_weapon_item = item_widget
                                self.cur_open_weapon_entity_id = entity_id
                                item_widget.PlayAnimation('show_change_weapon')
                                item_utils.show_weapon_choose(item_widget, entity_id, parent_entity_id, item_no, house_entity_id, player_logic)
                            else:
                                self.on_pickable_item_pickup(entity_id, parent_entity_id, item_no, house_entity_id)

                    item_widget.btn_bar.set_sound_enable(False)

                    @item_widget.btn_bar.unique_callback()
                    def OnEnd(btn, touch, pickable_list=pickable_list):
                        pass

                    return item_widget
            return

    def unroll_package(self, entity_id):
        self.open_package(entity_id)
        self.show_pickable_ui(self._pickable_info_list)
        if self.player:
            self.player.send_event('E_GUIDE_PICK_UNROLL_PACKAGE')

    def reroll_package_ui(self):
        self.open_package(None)
        self.show_pickable_ui(self._pickable_info_list)
        return

    def open_package(self, entity_id):
        self._open_package = entity_id

    def open_all_box(self, package_list):
        entity_id_list = [ package[0] for package in self._old_package_list ]
        self._old_package_list = package_list[:]
        from logic.gcommon.item import item_utility
        for entity_id, package_data in package_list:
            if entity_id in entity_id_list:
                continue

    def show_pickable_ui(self, pickable_info_list):
        self._pickable_info_list = pickable_info_list or []
        panel = self.panel
        if not panel.isVisible():
            return
        else:
            if not global_data.is_judge_ob:
                if not self.player:
                    return
            if not self.is_play_pick_ani:
                self.mouse_ctrl_on_before_refresh()
            if not self._pickable_info_list:
                self.clear_auto_pick()
                panel.list_bar.setVisible(False)
                panel.list_bar_title.setVisible(False)
                panel.box.setVisible(False)
                self.on_hide_pick_list()
                self.open_package(None)
                self._has_no_near_item = True
                self.all_item_data_list = []
                self.pre_all_item_type = []
                self._pick_entity_id_list = []
                self.cur_open_weapon_entity_id = None
                if not global_data.is_judge_ob:
                    self.player.send_event('E_GUIDE_PICK_SHOW', 0)
                return
            self._has_no_near_item = False
            panel.list_bar.setVisible(self._is_list_bar_visible)
            panel.list_bar_title.setVisible(self._is_list_bar_visible)
            panel.box.setVisible(not self._is_list_bar_visible)
            if self._is_list_bar_visible:
                self.on_show_pick_list()
            else:
                self.on_hide_pick_list()
            if panel.box.IsVisible() and not self.has_show_pick_guide:
                self.has_show_pick_guide = True
                self.archive_data.set_field('has_show_pick_guide_effect', True)
                nd_widget = global_data.uisystem.load_template_create('guide/i_guide_pick_small', parent=panel.box)

                def finished():
                    nd_widget.Destroy()

                animation_time = nd_widget.GetAnimationMaxRunTime('show_pick')
                nd_widget.StopAnimation('show_pick')
                nd_widget.SetTimeOut(animation_time, finished)
                nd_widget.PlayAnimation('show_pick')
            from logic.gutils import item_utils
            package_list1, package_list2, item_list = item_utils.package_list_split(self._pickable_info_list, None)
            if not package_list2:
                self.open_package(None)
                self.all_item_data_list = []
                self.pre_all_item_type = []
                self._pick_entity_id_list = []
                global_data.game_mgr.next_exec(self.show_pickable_ui, self._pickable_info_list)
                return
            if self._open_package is not None and package_list1:
                package_list1.pop(0)
            else:
                package_list2.pop(0)
            pick_item_list = []
            is_opened_deadbox = False
            if self._open_package is None:
                if item_list:
                    pick_item_list.append((None, item_list))
                package_list1.extend(package_list2)
            else:
                package_list1.extend(package_list2)
                open_box = []
                close_box = []
                from logic.gutils.item_utils import get_item_name
                for package_eid, package_data in package_list1:
                    package_item = EntityManager.getentity(package_eid)
                    if not global_data.is_judge_ob:
                        if package_item and package_item.logic and not package_item.logic.ev_g_is_opened() and not package_item.logic.ev_g_is_deadbox():
                            close_box.append((package_eid, package_data))
                            continue
                    is_opened_deadbox = True
                    self.list_scroll_to_top = not self.is_opened_deadbox
                    open_box.append((package_eid, package_data))
                    all_item = package_data.get('all_item', {})
                    package_item_list = [ (_entity_id, package_eid, _item_data) for _entity_id, _item_data in six.iteritems(all_item) ]
                    package_item_list = item_utils.pick_item_sort(package_item_list)
                    if package_eid == self._open_package:
                        pick_item_list.insert(0, (get_item_name(package_data['item_id']), package_item_list))
                    else:
                        pick_item_list.append((get_item_name(package_data['item_id']), package_item_list))

                if item_list:
                    pick_item_list.append((get_text_local_content(18023), item_list))
                self.open_all_box(open_box)
                package_list1 = close_box
            self.is_opened_deadbox = is_opened_deadbox
            self.pre_pickable_item_type_list(package_list1, pick_item_list)
            self.play_pickup_ani(pick_item_list)
            if self.is_play_pick_ani:
                return
            self.init_package()
            self.init_pickable_item_list(package_list1, pick_item_list)
            self.check_sview()
            pos = panel.lv_pickable_list.GetContentOffset()
            self._update_pickable_pos(pos)
            self._adjuest_list_pos()
            self.check_bounding()
            self.mouse_ctrl_on_after_refresh()
            return

    def _update_pickable_pos(self, offset=None):
        pickable_list = self.panel.lv_pickable_list
        min_height = 84
        max_height = 220
        if self._open_package is not None:
            max_height = 500
        width, height = self.panel.list_bar.GetContentSize()
        x, y = self.panel.list_bar.GetPosition()
        width, pickable_list_height = pickable_list.GetContainer().GetContentSize()
        total_height = pickable_list_height
        total_height = min(max_height, max(min_height, total_height))
        if pickable_list.GetItemCount() <= 0:
            total_height = 0
        bar_width, _ = self.panel.list_bar.GetContentSize()
        self.panel.list_bar.SetContentSize(bar_width, total_height + 20)
        self.panel.icon_down.ReConfPosition()
        pickable_list.SetContentSize(width, total_height)
        if offset is None:
            pickable_list.ScrollToTop()
        else:
            pickable_list.SetContentOffset(offset)
        return

    def _adjuest_list_pos(self):
        pickable_list = self.panel.lv_pickable_list
        contentSize = pickable_list.GetInnerContentSize()
        viewSize = pickable_list.GetContentSize()
        offset = pickable_list.GetContentOffset()
        if contentSize.height <= viewSize[1]:
            pickable_list.ScrollToTop()
            return
        if offset.y > 0:
            pickable_list.ScrollToBottom()
            return
        if offset.y < 0 and offset.y + contentSize.height <= viewSize[1]:
            pickable_list.ScrollToTop()

    def on_drag_pickbale_item(self, btn, touch, pickable_list):
        self._touch_tick += 1
        if self._touch_tick < 3:
            return
        cur_pos = touch.getLocation()
        if self._touch_pos:
            pre_pos = self._touch_pos
            delta_x = pre_pos.x - cur_pos.x
            delta_y = pre_pos.y - cur_pos.y
            if not self.panel.list_drag.IsPointIn(cur_pos) or delta_y == 0 or abs(delta_x / delta_y) >= DX_TO_DY:
                pickable_list.setTouchEnabled(False)
                btn.SetEnableTouch(False)
                btn.SetEnableTouch(True)
                btn.SetSelect(False)
                pickable_list.setTouchEnabled(True)
        self._touch_pos = cur_pos
        self._touch_tick = 0

    def on_pickable_item_pickup(self, entity_id, parent_entity_id, item_no, house_entity_id, put_pos=-1):
        from logic.gutils import item_utils
        from logic.gcommon.item import item_utility as iutil
        from common.cfg import confmgr
        if not self.player or not self.player.ev_g_status_check_pass(ST_PICK):
            global_data.emgr.battle_show_message_event.emit(get_text_local_content(18132))
            return
        if not item_utils.can_pick_obj(item_no):
            limit_text_id = item_utils.get_item_pick_limit_text_id(item_no)
            global_data.emgr.battle_show_message_event.emit(get_text_local_content(limit_text_id))
            return
        global_data.emgr.scene_pick_model.emit(parent_entity_id or entity_id)
        if parent_entity_id:
            package_item = EntityManager.getentity(parent_entity_id)
            if package_item and package_item.logic and package_item.logic.ev_g_is_deadbox() and not package_item.logic.ev_g_is_opened():
                self.player.ev_g_try_open_box(parent_entity_id)
        global_data.player.logic.send_event('E_PICK_UP_SOUND', item_no)
        if item_utils.is_gun(item_no):
            global_data.emgr.scene_pick_obj_event.emit(entity_id, house_entity_id=house_entity_id, parent_entity_id=parent_entity_id, put_pos=put_pos)
            return
        global_data.emgr.scene_pick_obj_event.emit(entity_id, house_entity_id=house_entity_id, parent_entity_id=parent_entity_id)
        self._last_try_pick_item_id = entity_id

    def show_up_message(self, msg):
        mdl = self.panel.hint
        wg = CCLabel.Create(msg, 25, CCSizeZero, cc.TEXTHALIGNMENT_LEFT, cc.TEXTVALIGNMENT_TOP)
        self.panel.AddChild(None, wg, 1)
        wg.SetPosition(*mdl.GetPosition())
        wg.SetString(msg)

        def _real_destroy():
            wg.Destroy()

        wg.runAction(cc.Sequence.create([
         cc.Spawn.create([cc.FadeOut.create(2.0), cc.MoveBy.create(1.0, cc.Vec2(0, 320))]),
         cc.CallFunc.create(_real_destroy)]))
        return

    def get_weapon_pic_path(self, weapon_id):
        from logic.gutils.item_utils import get_item_pic_by_item_no
        return get_item_pic_by_item_no(weapon_id)

    def is_heavy_machine_exchange_ui_visible(self):
        return self.panel.nd_exchange_gun.isVisible()

    def exchange_weapon_data(self, abandon_wid, pick_weapon_data):
        self.remove_weapon(abandon_wid)
        self.add_weapon(pick_weapon_data)

    def on_camera_switch_to_state(self, state, *args):
        from logic.client.const import camera_const
        if state == camera_const.AIM_MODE:
            self.add_hide_count('AIM_CAMERA')
        elif self.cur_camera_state_type == camera_const.AIM_MODE and state != camera_const.AIM_MODE:
            self.add_show_count('AIM_CAMERA')
        self.cur_camera_state_type = state

    def on_auto_pick_event(self, enable):
        if not self.player:
            return
        else:
            self._auto_pick_enable = bool(enable)
            if self._auto_pick_enable and self._open_package is None:
                from logic.gutils import item_utils
                package_list1, package_list2, item_list = item_utils.package_list_split(self._pickable_info_list, None)
                pickable_items, unavailable_list = item_utils.get_available_list(self.player, item_list)
                self.check_auto_pick(pickable_items, unavailable_list)
            else:
                self.clear_auto_pick()
            return

    def check_is_bag_full(self):
        if not self.player:
            return False
        total_capacity, cur_capacity = self.player.ev_g_capacity()
        return cur_capacity >= total_capacity

    def check_is_full_cnt(self, item_no):
        return item_utils.check_is_full_cnt(self.player, item_no)

    def change_ui_data(self):
        nd = getattr(self.panel, 'box')
        scale = nd.getScale()
        w_pos = nd.getParent().convertToWorldSpace(nd.getPosition())
        w_pos.x = w_pos.x - 10
        w_pos.y = w_pos.y + 10
        return (
         w_pos, None, ['nd_step_5', 'nd_step_5_1'])

    def on_user_setting_changed(self, key, value):
        if key == WEAPON_PICK_DIRECTLY_REPLACE_KEY:
            self._enable_weapon_directly_replace = value

    def on_hide_pick_list(self):
        self.unreg_mouse_event()
        self._target_mouse_select_index = None
        self._mouse_select_index = None
        global_data.emgr.scene_pick_show_item_list.emit(False)
        return

    def on_show_pick_list(self):
        self.reg_mouse_event()
        global_data.emgr.scene_pick_show_item_list.emit(True)

    def init_mouse_keyboard_parameter(self):
        self._mouse_listener = None
        self._mouse_select_index = None
        self._target_mouse_select_index = None
        self._cur_mouse_dist = 0
        from common.cfg import confmgr
        hot_key_par = confmgr.get('c_hot_key_parameter')
        self.pick_scroll_sensitivity = hot_key_par.get('pick_scroll_sensitivity', 220)
        self.panel.lv_pickable_list.DisableDefaultMouseEvent()
        return

    def reg_mouse_event(self):
        if not global_data.is_pc_mode:
            return
        if not global_data.pc_ctrl_mgr:
            return
        if not global_data.pc_ctrl_mgr.is_pc_control_enable():
            return
        self.register_mouse_scroll_event()

    def unreg_mouse_event(self):
        self.unregister_mouse_scroll_event()

    def check_can_mouse_scroll(self):
        if not self.is_on_show():
            return False
        if not self.panel.lv_pickable_list.IsVisible():
            return False
        if self.is_play_pick_ani:
            return False
        return True

    @hot_key_wrapper_for_pickui
    def keyboard_pick_scroll_up(self, *args):
        if not self.check_can_mouse_scroll():
            return False
        else:
            self.on_hot_key_mouse_scroll(None, self.pick_scroll_sensitivity, None)
            return

    @hot_key_wrapper_for_pickui
    def keyboard_pick_scroll_down(self, *args):
        if not self.check_can_mouse_scroll():
            return False
        else:
            self.on_hot_key_mouse_scroll(None, -self.pick_scroll_sensitivity, None)
            return

    def on_hot_key_mouse_scroll(self, msg, delta, key_state):
        dist = -delta
        self._cur_mouse_dist += dist
        changed_index = 0
        if abs(self._cur_mouse_dist) >= self.pick_scroll_sensitivity:
            changed_index = int(self._cur_mouse_dist / self.pick_scroll_sensitivity)
            self._cur_mouse_dist = 0
        if self._mouse_select_index is None:
            self._mouse_select_index = (0, 0)
            self.set_pick_item_index_select(self._mouse_select_index, True)
            self._cur_mouse_dist = 0
            return
        else:
            if changed_index != 0:
                step = 1 if changed_index > 0 else -1
                new_mouse_select_index = self.advance_selectable_item(self._mouse_select_index, changed_index, step)
                if new_mouse_select_index != self._mouse_select_index:
                    self.set_pick_item_index_select(self._mouse_select_index, False)
                    self.set_pick_item_index_select(new_mouse_select_index, True)
                    self._mouse_select_index = new_mouse_select_index
                    self.check_selected_item_is_in_view(self._mouse_select_index)
            return

    def advance_selectable_item(self, cur_item_index, var_step, step):
        list_index, inner_index = cur_item_index
        inner_list_size = len(WEAPON_POS_LIST)
        inner_default_index = 0 if var_step > 0 else inner_list_size - 1
        item_widget = self.get_pick_list_item(list_index)
        nearest_sel_list_index = item_widget or self.get_nearest_selectable_exist_list_index(list_index)
        n_item_widget = self.get_pick_list_item(nearest_sel_list_index)
        n_inner_index = 0
        if n_item_widget:
            if n_item_widget.nd_change_weapon.isVisible() and not n_item_widget.item.isVisible():
                if step < 0:
                    n_inner_index = 0 if 1 else inner_list_size - 1
            return (
             nearest_sel_list_index, n_inner_index)
        data_list = self.all_item_data_list
        data = data_list[list_index]
        key, ui, available, itemdata = data
        var_step = int(var_step)
        if key in ('pick', 'package') and ui == 'battle/i_item_4':
            if var_step != 0:
                if item_widget.nd_change_weapon.isVisible() and not item_widget.item.isVisible():
                    if 0 <= var_step + inner_index < inner_list_size:
                        return (list_index, var_step + inner_index)
                    else:
                        if step >= 1:
                            new_var_step = var_step - (inner_list_size - inner_index)
                        else:
                            new_var_step = var_step + inner_index + 1
                        return self.advance_selectable_item([list_index + step, inner_default_index], new_var_step, step)

                else:
                    return self.advance_selectable_item([list_index + step, inner_default_index], var_step - step, step)
            elif item_widget.nd_change_weapon.isVisible() and not item_widget.item.isVisible():
                return cur_item_index
            else:
                return (
                 list_index, 0)

        else:
            if var_step != 0:
                return self.advance_selectable_item([list_index + step, inner_default_index], var_step - step, step)
            return self.advance_selectable_item([list_index + step, inner_default_index], var_step, step)

    def get_nearest_selectable_exist_list_index(self, list_index):
        count = self.panel.lv_pickable_list.GetItemCount()
        if count == 0:
            return -1
        valid_end_index = self._sview_index
        valid_start_index = self._sview_index - count
        if abs(valid_end_index - list_index - 1) >= abs(valid_start_index - list_index):
            seq_start = valid_start_index
            seq_end = valid_end_index
            direction = 1
        else:
            seq_start = valid_end_index - 1
            seq_end = valid_start_index - 1
            direction = -1
        for idx in range(seq_start, seq_end, direction):
            data_list = self.all_item_data_list
            data = data_list[idx]
            key, ui, available, itemdata = data
            if key in ('pick', 'package') and ui == 'battle/i_item_4':
                return idx

        return -1

    def on_switch_on_hot_key(self):
        super(PickUI, self).on_switch_on_hot_key()
        self.reg_mouse_event()
        self._is_list_bar_visible = True
        self.panel.btn_close.setVisible(False)

    def on_switch_off_hot_key(self):
        super(PickUI, self).on_switch_off_hot_key()
        self.unreg_mouse_event()
        self.panel.btn_close.setVisible(True)

    def on_hot_key_opened_state(self):
        super(PickUI, self).on_hot_key_opened_state()
        if self._mouse_select_index:
            self.set_pick_item_index_select(self._mouse_select_index, True)
        for item_widget in self.panel.lv_pickable_list.GetAllItem():
            self._set_replace_item_list_hotkey_tip_visible(item_widget, True)

    def on_hot_key_closed_state(self):
        super(PickUI, self).on_hot_key_closed_state()
        if self._mouse_select_index:
            self.set_pick_item_index_select(self._mouse_select_index, False)
        for item_widget in self.panel.lv_pickable_list.GetAllItem():
            self._set_replace_item_list_hotkey_tip_visible(item_widget, False)

    def mouse_ctrl_on_before_refresh(self):
        if self._mouse_select_index:
            self.set_pick_item_index_select(self._mouse_select_index, False)
            self._target_mouse_select_index = self._mouse_select_index or self._target_mouse_select_index
            self._mouse_select_index = None
        return

    def mouse_ctrl_on_after_refresh(self):
        if not global_data.is_pc_mode:
            return
        else:
            if self._target_mouse_select_index is None:
                self._target_mouse_select_index = (0, 0)
                self._cur_mouse_dist = 0
            if self._target_mouse_select_index:
                new_select_index = self.advance_selectable_item(self._target_mouse_select_index, 0, 1)
                start_index, end_index = self.get_visible_range()
                if start_index is not None:
                    new_list_sel_index, _ = new_select_index
                    if not start_index <= new_list_sel_index < end_index:
                        new_select_index = (
                         start_index, 0)
                        new_select_index = self.advance_selectable_item(new_select_index, 0, 1)
                self._target_mouse_select_index = new_select_index
                if global_data.pc_ctrl_mgr and global_data.pc_ctrl_mgr.is_pc_control_enable():
                    self.set_pick_item_index_select(self._target_mouse_select_index, True)
            self._mouse_select_index = self._target_mouse_select_index
            return

    def set_pick_item_index_select(self, index, is_select):
        list_index, inner_index = index
        ui_item = self.get_pick_list_item(list_index)
        if ui_item:
            if not ui_item.item_sel:
                return
            if ui_item.nd_change_weapon:
                list_item = getattr(ui_item, 'item_sel_%d' % (inner_index + 1))
                if list_item:
                    list_item.setVisible(is_select)
                    if is_select:
                        set_hot_key_common_tip(list_item.temp_pc, PICK_THING)
                ui_item.item.temp_pc.setVisible(False)
                ui_item.item_sel.setVisible(is_select)
                ui_item.item_sel.temp_pc.setVisible(is_select)
                ui_item.pnl_right.setVisible(not is_select)
                ui_item.pnl_right_choose.setVisible(is_select)
                if is_select:
                    set_hot_key_common_tip(ui_item.item_sel.temp_pc, PICK_THING)
                    set_hot_key_common_tip(ui_item.item.temp_pc, MARK_ITEM)

    def check_selected_item_is_in_view(self, index):
        list_index, inner_index = index
        ui_item = self.get_pick_list_item(list_index)
        sv = self.panel.lv_pickable_list
        if ui_item:
            cur_offset = self.panel.lv_pickable_list.GetContentOffset()
            view_h = sv.getContentSize().height
            lb = ui_item.convertToWorldSpace(CCPointZero)
            rt = ui_item.convertToWorldSpace(ccp(*ui_item.GetContentSize()))
            sv_item_lb = sv.convertToNodeSpace(lb)
            sv_item_rt = sv.convertToNodeSpace(rt)
            bottom_offset = sv_item_lb.y - 0
            top_offset = sv_item_rt.y - view_h
            if bottom_offset < 0:
                cur_offset.y -= bottom_offset
                self.panel.lv_pickable_list.SetContentOffsetInDuration(cur_offset, 0.09, False)
            elif top_offset > 0:
                cur_offset.y -= top_offset
                self.panel.lv_pickable_list.SetContentOffsetInDuration(cur_offset, 0.09, False)

    @hot_key_wrapper_for_pickui
    def keyboard_pick_thing(self, msg, keycode):
        from logic.vscene.parts.ctrl.InputMockHelper import TouchMock
        if not self._mouse_select_index:
            return
        else:
            if not self.panel.lv_pickable_list.IsVisible():
                return
            list_index, inner_index = self._mouse_select_index
            item_widget = self.get_pick_list_item(list_index)
            if not item_widget:
                return
            if not item_widget.nd_change_weapon:
                return
            if item_widget.nd_change_weapon.isVisible():
                inner_item = getattr(item_widget, 'weapon_%d' % (inner_index + 1))
                if inner_item:
                    inner_item.OnClick(None)
            else:
                t = TouchMock()
                item_widget.btn_bar.OnBegin(t)
                item_widget.btn_bar.OnClick(t)
                item_widget.btn_bar.OnEnd(t)
            return

    @hot_key_wrapper_for_pickui
    def keyboard_mark_item(self, msg, keycode):
        if not is_down_msg(msg):
            return
        from logic.vscene.parts.ctrl.InputMockHelper import TouchMock
        if not self._mouse_select_index:
            return
        if not self.panel.lv_pickable_list.IsVisible():
            return
        list_index, inner_index = self._mouse_select_index
        item_widget = self.get_pick_list_item(list_index)
        if not item_widget:
            return
        if not item_widget.nd_change_weapon:
            return
        if item_widget.nd_change_weapon.isVisible():
            return
        t = TouchMock()
        item_widget.btn_recourse_mark.OnClick(t)

    def get_pick_list_item(self, list_index):
        count = self.panel.lv_pickable_list.GetItemCount()
        if count == 0:
            return None
        else:
            valid_end_index = self._sview_index
            valid_start_index = self._sview_index - count
            if valid_start_index <= list_index < valid_end_index:
                return self.panel.lv_pickable_list.GetItem(list_index - valid_start_index)
            return None
            return None

    def get_visible_range(self):
        listobj = self.panel.lv_pickable_list
        s_count = listobj.GetItemCount()
        if not s_count:
            return (None, None)
        else:
            pos_y = listobj.getInnerContainer().getPositionY()
            visible_start_index = 0
            in_height = listobj.getInnerContainerSize().height
            top_y = pos_y + in_height
            view_h = listobj.GetContentSize()[1]
            while view_h < top_y:
                height = listobj.GetItem(visible_start_index).getContentSize().height
                top_y -= height
                visible_start_index += 1

            visible_end_index = visible_start_index
            bottom_y = 0
            while bottom_y < top_y and visible_end_index < s_count:
                height = listobj.GetItem(visible_start_index).getContentSize().height
                top_y -= height
                visible_end_index += 1

            if visible_end_index:
                visible_end_index -= 1
            valid_start_index = self._sview_index - s_count
            if visible_start_index <= visible_end_index:
                return (visible_start_index + valid_start_index, visible_end_index + 1 + valid_start_index)
            return (None, None)

    @hot_key_wrapper_for_pickui
    def keyboard_replace_item_down(self, idx, msg, keycode):
        ok = self._replace_item(idx)
        return ok

    def _replace_item(self, idx):
        if not self.panel.lv_pickable_list.IsVisible():
            return False
        else:
            if not self.cur_open_weapon_item:
                return False
            start_index, end_index = self.get_visible_range()
            if start_index is None or end_index is None:
                return False
            for i in range(start_index, end_index):
                item_widget = self.get_pick_list_item(i)
                if not item_widget:
                    continue
                if item_widget == self.cur_open_weapon_item:
                    inner_item = getattr(item_widget, 'weapon_%d' % (idx + 1), None)
                    if inner_item and inner_item.isVisible():
                        inner_item.OnClick(None)
                        return True
            else:
                return False

            return

    def _set_replace_item_list_hotkey_tip_visible(self, item_widget, on):
        if not item_widget:
            return
        else:
            for i in range(REPLACE_ITEM_IDX_END):
                weapon_node = getattr(item_widget, 'weapon_%d' % (i + 1), None)
                if not weapon_node:
                    continue
                weapon_node.temp_pc.setVisible(on)

            return

    def _init_replace_item_list_hotkey_tips(self, item_widget):
        if not item_widget:
            return
        else:
            for i in range(REPLACE_ITEM_IDX_END):
                weapon_node = getattr(item_widget, 'weapon_%d' % (i + 1), None)
                if not weapon_node:
                    continue
                definition = getattr(hot_key_def, 'PICK_ITEM_REPLACE_%d' % (i + 1,), None)
                set_hot_key_common_tip(weapon_node.temp_pc, definition)

            return

    def check_player_alive(self):
        if self.player:
            if self.player.ev_g_death():
                self.add_hide_count('AVATAR_DEATH')
            else:
                self.add_show_count('AVATAR_DEATH')

    def on_saved(self):
        self.add_show_count('AVATAR_DEATH')

    def on_died(self, *args):
        self.add_hide_count('AVATAR_DEATH')