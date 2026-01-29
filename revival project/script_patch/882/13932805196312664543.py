# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle_pass/season_memory/SeasonMechaMemoryUI.py
from __future__ import absolute_import
import six_ex
import six
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_CLOSE_BY_DEFAULT_FUNC_NAME, UI_VKB_CLOSE
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import item_utils
import logic.gutils.season_utils as season_utils
from common.utils.cocos_utils import ccp, CCRectZero, CCRect
import cc
from logic.gcommon import time_utility
from logic.gcommon.cdata import season_data
from common.cfg import confmgr
from logic.gutils.dress_utils import get_mecha_dress_clothing_id
from logic.gcommon.common_const import chat_const
from logic.gutils.template_utils import update_badge_node, set_ui_show_picture
import logic.gutils.dress_utils as dress_utils

class SeasonMechaMemoryUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_pass/i_battle_pass_memory_mecha'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE_BY_DEFAULT_FUNC_NAME
    UI_ACTION_EVENT = {'btn_click.OnClick': 'on_click_close_btn',
       'btn_right.OnClick': 'on_click_btn_right',
       'btn_left.OnClick': 'on_click_btn_left',
       'btn_share.OnClick': 'on_click_btn_share'
       }
    UI_OPEN_SOUND = 'season_silver_awards'
    UI_EXIT_SOUND = 'season_tickets_next'

    def on_init_panel(self, *args, **kwargs):
        self.regist_main_ui()
        self._is_for_season_pass = False
        self.can_close = False
        self._dan_info_len = 3
        if global_data.player:
            cur_season = global_data.player.get_battle_season()
        else:
            cur_season = season_data.get_cur_battle_season()
        self.show_anim_list = [
         'appear_img', 'appear_img2']
        self.show_anim_index = -1
        self.best_mecha_id = self.get_best_mecha_id()
        self.show_mecha_id = self.best_mecha_id
        self.last_season = max(cur_season - 1, 1)
        self.cur_achi_idx = 0
        self.sorted_other_achievements = []
        self.day_achievement_dict = {}
        self.achi_text_dict = {}
        btn_ani = 'show_btn_quick' if season_utils.SeasonMemoryListTabWidget.has_all_showed() else 'show_btn_slow'
        t = 0.3 if season_utils.SeasonMemoryListTabWidget.has_all_showed() else 1.2
        if 'Share' in self.__class__.__name__:
            t = 0.3
        action_list = [
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('show')),
         cc.CallFunc.create(lambda : self.panel.PlayAnimation(btn_ani)),
         cc.CallFunc.create(lambda : season_utils.play_season_ui_sound(self.UI_OPEN_SOUND)),
         cc.DelayTime.create(t)]

        def animation_end():
            self.can_close = True

        action_list.append(cc.CallFunc.create(animation_end))
        if self.panel.HasAnimation('loop'):
            loop_time = self.panel.GetAnimationMaxRunTime('show') - 1.2
            if loop_time > 0.2:
                action_list.append(cc.DelayTime.create(loop_time))
            action_list.append(cc.CallFunc.create(lambda : self.panel.PlayAnimation('loop')))
        self.panel.runAction(cc.Sequence.create(action_list))
        self.panel.RecordAnimationNodeState('loop_switch')
        self.panel.PlayAnimation('loop_switch')
        season_utils.nd_touch_direction_helper(self.panel.nd_touch, left_func=self.on_click_btn_left, right_func=self.on_click_btn_right)
        self.init_show()

    def init_show(self):
        self.init_memory_data()
        self.init_memory_tab()
        self.init_mecha_list()

    def get_season_stat(self):
        if not global_data.player:
            return {}
        data = global_data.player.season_stat
        if not data:
            return {}
        return data

    def init_memory_tab(self):
        self.mem_tab_list = season_utils.SeasonMemoryListTabWidget(self.panel.list_tab, self.__class__.__name__)

    def init_mecha_list(self):
        if not global_data.player:
            return
        data = self.get_season_stat()
        if not data:
            return
        sst_mecha_stat = data.get('sst_mecha_stat', {})
        valid_keys = [ m_id for m_id in six_ex.keys(sst_mecha_stat) if sst_mecha_stat[m_id].get('sst_mecha_fight_time', 0) > 1800 ]
        if len(valid_keys) <= 1:
            self.panel.btn_list.setVisible(False)
            return
        mecha_list = sorted(valid_keys, key=lambda k: sst_mecha_stat[k].get('sst_mecha_game_cnt', 0), reverse=True)
        mecha_list = mecha_list or [8001]
        mecha_show_list = []
        for mecha_id in mecha_list:
            mecha_show_list.append({'name': item_utils.get_mecha_name_by_id(mecha_id),'mecha_id': mecha_id})

        def choose(index):
            self.show_mecha_id = mecha_show_list[index].get('mecha_id')
            self.cur_achi_idx = 0
            self.init_memory_data()

        from logic.gutils import template_utils
        template_utils.init_common_choose_list_2(self.panel.choose_list_meha, self.panel.btn_list.icon, mecha_show_list, callback=choose, func_btn=self.panel.btn_list, use_widget_max_height=True)

    def on_click_btn_right(self, *args, **kwargs):
        if not self.sorted_other_achievements:
            return
        if self.cur_achi_idx + 1 >= len(self.sorted_other_achievements):
            return
        if self.panel.IsPlayingAnimation('loop_switch'):
            self.panel.StopAnimation('loop_switch')
            self.panel.RecoverAnimationNodeState('loop_switch')
        self.cur_achi_idx += 1
        self.cur_achi_idx %= len(self.sorted_other_achievements)
        self.panel.StopAnimation('lab_left')
        self.panel.StopAnimation('lab_right')
        self.panel.PlayAnimation('lab_right')
        self.show_cur_achi_description()

    def on_click_btn_left(self, *args, **kwargs):
        if not self.sorted_other_achievements:
            return
        if self.cur_achi_idx - 1 < 0:
            return
        if self.panel.IsPlayingAnimation('loop_switch'):
            self.panel.StopAnimation('loop_switch')
            self.panel.RecoverAnimationNodeState('loop_switch')
        self.panel.StopAnimation('lab_left')
        self.panel.StopAnimation('lab_right')
        self.panel.PlayAnimation('lab_left')
        self.cur_achi_idx -= 1
        self.cur_achi_idx %= len(self.sorted_other_achievements)
        self.show_cur_achi_description()

    def on_finalize_panel(self):
        self.sorted_other_achievements = []
        self.day_achievement_dict = {}
        self.achi_text_dict = {}
        self.destroy_widget('mem_tab_list')

    def get_best_mecha_id(self):
        if not global_data.player:
            return 8001
        data = self.get_season_stat()
        if not data:
            return 8001
        sst_mecha_stat = data.get('sst_mecha_stat', {})
        mecha_id = max(six_ex.keys(sst_mecha_stat), key=lambda k: sst_mecha_stat[k].get('sst_mecha_game_cnt', 0))
        return mecha_id or 8001

    def get_show_clothing(self):
        mecha_id = int(self.show_mecha_id)
        c_id = get_mecha_dress_clothing_id(mecha_id) or dress_utils.get_mecha_skin_item_no(mecha_id, -1)
        return c_id

    def init_memory_data(self):
        if not global_data.player:
            return
        else:
            season_last = self.last_season
            self.panel.lab_title.SetString(get_text_by_id(634091, (season_last,)))
            data = self.get_season_stat()
            if not data:
                return
            import logic.gutils.dress_utils as dress_utils
            mecha_id = int(self.show_mecha_id)
            clothing_id = self.get_show_clothing()
            if self.show_anim_index != 0:
                set_ui_show_picture(clothing_id, None, self.panel.img)
            else:
                set_ui_show_picture(clothing_id, None, self.panel.img2)
            if self.show_anim_index >= 0:
                if len(self.show_anim_list) > self.show_anim_index >= 0:
                    anim = self.show_anim_list[self.show_anim_index]
                    self.panel.StopAnimation(anim)
            if self.show_anim_index >= 0:
                self.show_anim_index = (self.show_anim_index + 1) % len(self.show_anim_list)
                anim = self.show_anim_list[self.show_anim_index]
                self.panel.PlayAnimation(anim)
            if self.show_anim_index < 0:
                self.show_anim_index = 0
            name = item_utils.get_mecha_name_by_id(self.show_mecha_id)
            self.panel.lab_mecha.SetString(name)
            mecha_data = data.get('sst_mecha_stat', {}).get(str(mecha_id), {})
            self.sorted_other_achievements, self.day_achievement_dict, self.achi_text_dict = self.get_show_other_achievement(mecha_data, mecha_id)
            self.init_dot_list()
            self.show_cur_achi_description()
            battle_cnt = mecha_data.get('sst_mecha_game_cnt', 0)
            summary_txt = get_text_by_id(634182).format(battle_cnt, mechaname=name)
            self.panel.lab_content_2.SetString(summary_txt)
            return

    def on_resolution_changed(self):
        clothing_id = self.get_show_clothing()
        from logic.gutils.template_utils import update_badge_node, set_ui_show_picture
        set_ui_show_picture(clothing_id, None, self.panel.img)
        set_ui_show_picture(clothing_id, None, self.panel.img2)
        return

    def init_dot_list(self):
        self.panel.list_dot.SetInitCount(len(self.sorted_other_achievements))

    def update_dot_list(self):
        item_list = self.panel.list_dot.GetAllItem()
        _list_dot = self.panel.list_dot
        for index, dot_item in enumerate(item_list):
            dot_item = _list_dot.GetItem(index)
            if index == self.cur_achi_idx:
                dot_item.img_list_dot.SetDisplayFrameByPath('', 'gui/ui_res_2/role_profile/img_skin_list_dot_1.png')
            else:
                dot_item.img_list_dot.SetDisplayFrameByPath('', 'gui/ui_res_2/role_profile/img_skin_list_dot_2.png')

    def on_click_achievement(self, btn, touch, idx):
        if self.cur_achi_idx == idx:
            return
        self.panel.StopAnimation('lab_left')
        self.panel.StopAnimation('lab_right')
        if idx > self.cur_achi_idx:
            self.panel.PlayAnimation('lab_right')
        else:
            self.panel.PlayAnimation('lab_left')
        self.cur_achi_idx = idx
        self.show_cur_achi_description()

    def show_cur_achi_description(self):
        self.panel.btn_left.setVisible(self.cur_achi_idx != 0)
        self.panel.btn_right.setVisible(self.cur_achi_idx != len(self.sorted_other_achievements) - 1)
        if self.cur_achi_idx < len(self.sorted_other_achievements):
            achi_key = self.sorted_other_achievements[self.cur_achi_idx]
            self.panel.lab_content.SetString(self.achi_text_dict[achi_key])
            self.panel.lab_content2.SetString(self.achi_text_dict[achi_key])
            if achi_key in self.day_achievement_dict:
                self.panel.bar_top.setVisible(True)
                start_timestamp = season_data.get_start_timestamp(self.last_season)
                date_time = time_utility.get_utc8_datetime(start_timestamp + self.day_achievement_dict[achi_key] * time_utility.ONE_DAY_SECONDS)
                cur_time_str = get_text_by_id(5280) + '%s.%s.%s' % (date_time.year, date_time.month, date_time.day)
                self.panel.lab_date.SetString(cur_time_str)
            else:
                self.panel.bar_top.setVisible(True)
                name = item_utils.get_mecha_name_by_id(self.show_mecha_id)
                self.panel.lab_date.SetString(get_text_by_id(634180).format(mechaname=name))
        else:
            self.panel.lab_content.SetString('')
            self.panel.lab_content2.SetString('')
            self.panel.bar_top.setVisible(False)
        self.update_dot_list()
        self.update_titles()

    def update_titles(self):
        from logic.gcommon.common_const import rank_const
        from logic.gutils import template_utils
        title_type = rank_const.RANK_TITLE_MECHA_REGION
        self.panel.temp_title.setVisible(False)
        show_rank_info = self.get_show_title()
        if show_rank_info:
            self.panel.temp_title.setVisible(True)
            self.panel.temp_title.SetInitCount(1)
            title_item = self.panel.temp_title.GetItem(0)
            template_utils.init_rank_title(title_item, title_type, show_rank_info)

    def get_show_title(self):
        from logic.gcommon.common_const import rank_const
        from logic.gcommon.common_const import rank_region_const
        title_type = rank_const.RANK_TITLE_MECHA_REGION
        data = self.get_season_stat() or {}
        mecha_data = data.get('sst_mecha_stat', {}).get(str(self.show_mecha_id), {})
        rank_title = mecha_data.get('sst_mecha_max_rank_title', [])
        if rank_title:
            region_type, rank_adcode, rank = rank_title
            show_rank_info = [region_type, str(self.show_mecha_id), rank_adcode, rank, -1]
            return show_rank_info
        else:
            return []

    def get_show_other_achievement(self, mecha_data, mecha_id, max_count=6, require_day_gap=3):
        check_type_table = confmgr.get('season_memory_conf', 'MechaMemoryConf', 'Content', default={})
        name_dict = {'mechaname': item_utils.get_mecha_name_by_id(mecha_id)}
        mecha_memory, day_dict, text_dict = season_utils.get_season_memory_info(check_type_table, mecha_data, {'mecha_id': mecha_id}, name_dict)
        other_achievements = season_utils.filter_and_sort_season_memory(check_type_table, mecha_memory, day_dict, max_count, require_day_gap)
        return (
         other_achievements, day_dict, text_dict)

    def on_click_close_btn(self, *args):
        if not self.can_close:
            return
        self.can_close = False
        action_list = []
        action_list.append(cc.CallFunc.create(lambda : self.panel.PlayAnimation('exit')))
        action_list.append(cc.CallFunc.create(lambda : season_utils.play_season_ui_sound(self.UI_EXIT_SOUND)))
        action_list.append(cc.DelayTime.create(self.panel.GetAnimationMaxRunTime('exit')))

        def animation_end():
            if not global_data.player:
                return
            if global_data.player and global_data.player.season_stat:
                season_stat = self.get_season_stat()
                if sum([ i.get('sst_frd_game_cnt', 0) for i in six.itervalues(season_stat.get('sst_frd_stat', {})) ]) >= 5:
                    from logic.comsys.battle_pass.season_memory.SeasonFriendMemoryUI import SeasonFriendMemoryUI
                    ui = SeasonFriendMemoryUI()
                    if ui and self._is_for_season_pass:
                        ui.play_for_SeasonPassUI()
                elif self._is_for_season_pass:
                    from logic.comsys.battle_pass.NewSeasonReward import NewSeasonReward
                    ui = NewSeasonReward()
                    if ui:
                        ui.play_for_SeasonPassUI()
                else:
                    data = global_data.player.get_last_season_report()
                    if data and not self._is_for_season_pass:
                        from logic.comsys.battle_pass.SeasonFinishedSettleUI import SeasonFinishedSettleUI
                        SeasonFinishedSettleUI()
            else:
                data = global_data.player.get_last_season_report()
                if data and not self._is_for_season_pass:
                    from logic.comsys.battle_pass.SeasonFinishedSettleUI import SeasonFinishedSettleUI
                    SeasonFinishedSettleUI()
                elif self._is_for_season_pass:
                    from logic.comsys.battle_pass.NewSeasonReward import NewSeasonReward
                    ui = NewSeasonReward()
                    if ui:
                        ui.play_for_SeasonPassUI()
            self.close()

        action_list.append(cc.CallFunc.create(animation_end))
        self.panel.runAction(cc.Sequence.create(action_list))

    def on_click_btn_share(self, *args):
        data = self.get_season_stat()
        if not data:
            return
        from logic.comsys.share.ScreenFrameHelper import ScreenFrameHelper
        screen_capture_helper = ScreenFrameHelper()
        self.panel.btn_share.setVisible(False)
        self.panel.btn_click.setVisible(False)
        self.panel.list_tab.setVisible(False)

        def cb(*args):
            if not (self.panel and self.panel.isValid()):
                return
            self.panel.btn_share.setVisible(True)
            self.panel.btn_click.setVisible(True)
            self.panel.list_tab.setVisible(True)
            from logic.comsys.battle_pass.season_memory.SeasonMemoryCommonWidget import SeasonMemoryCommonWidget
            SeasonMemoryCommonWidget.update_share_panel(self.get_chat_data, self.__class__.__name__)

        screen_capture_helper.take_screen_shot(['SeasonBeginBackgroundUI', 'SeasonMechaMemoryUI'], self.panel, custom_cb=cb, head_nd_name='nd_player_info_1')

    def get_chat_data(self):
        data = self.get_season_stat()
        if not data:
            return
        mecha_data = data.get('sst_mecha_stat', {}).get(str(self.show_mecha_id), {})
        mecha_id = self.show_mecha_id
        clothing_id = self.get_show_clothing()
        extra_data = {'type': chat_const.MSG_TYPE_MECHA_SEASON_MEMORY,
           'season': self.last_season,
           'mecha_id': self.show_mecha_id,
           'clothing_id': clothing_id,
           'data': {'sst_mecha_stat': {str(self.show_mecha_id): mecha_data}},'title': self.get_show_title()
           }
        return extra_data

    def play_for_SeasonPassUI(self):
        self._is_for_season_pass = True
        if self.mem_tab_list:
            self.mem_tab_list.set_is_for_season_pass()


class SeasonMechaMemoryShareUI(SeasonMechaMemoryUI):
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE

    def on_init_panel(self, *args, **kwargs):
        self._data_dict = kwargs.get('data_dict', {})
        super(SeasonMechaMemoryShareUI, self).on_init_panel()
        self.panel.bg.setVisible(False)
        self.panel.pnl_mask.setVisible(True)
        self.panel.btn_click.setVisible(False)
        self.panel.btn_list.setVisible(False)
        self.panel.btn_share.setVisible(False)
        self.panel.list_tab.setVisible(False)
        self.panel.BindMethod('OnClick', self.on_click_close_btn)
        from common.utils.ui_utils import get_scale
        self.panel.nd_content.setScale(get_scale('0.9w'))
        self.init_memory_data()
        _uid = kwargs.get('uid')
        name = kwargs.get('name')
        if _uid:
            from logic.comsys.battle_pass.season_memory.SeasonMemoryCommonWidget import SeasonMemoryCommonWidget
            SeasonMemoryCommonWidget.init_share_head(self.panel.nd_player_info_1, _uid, name)

    def init_show(self):
        pass

    def init_mecha_list(self):
        pass

    def get_season_stat(self):
        return self._data_dict.get('data', {})

    def test(self):
        test_mecha_id = 8001
        self.show_mecha_id = test_mecha_id
        mecha_id = int(self.show_mecha_id)
        data = global_data.player.season_stat
        clothing_id = get_mecha_dress_clothing_id(mecha_id) or dress_utils.get_mecha_skin_item_no(mecha_id, -1)
        mecha_data = data.get('sst_mecha_stat', {}).get(str(self.show_mecha_id), {})
        data_dict = {'type': chat_const.MSG_TYPE_MECHA_SEASON_MEMORY,
           'season': self.last_season,
           'mecha_id': self.show_mecha_id,
           'clothing_id': clothing_id,
           'data': {'sst_mecha_stat': {str(self.show_mecha_id): mecha_data}},'title': super(SeasonMechaMemoryShareUI, self).get_show_title()
           }
        self._data_dict = data_dict

    def on_click_close_btn(self, *args):
        if not self.can_close:
            return
        self.can_close = False
        action_list = []
        action_list.append(cc.CallFunc.create(lambda : self.panel.PlayAnimation('exit')))
        action_list.append(cc.CallFunc.create(lambda : season_utils.play_season_ui_sound(self.UI_EXIT_SOUND)))
        action_list.append(cc.DelayTime.create(self.panel.GetAnimationMaxRunTime('exit')))

        def animation_end():
            self.close()

        action_list.append(cc.CallFunc.create(animation_end))
        self.panel.runAction(cc.Sequence.create(action_list))

    def get_show_title(self):
        return self._data_dict.get('title', [])

    def get_show_clothing(self):
        mecha_id = int(self.show_mecha_id)
        return self._data_dict.get('clothing_id', None) or dress_utils.get_mecha_skin_item_no(mecha_id, -1)