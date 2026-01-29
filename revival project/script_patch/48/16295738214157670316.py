# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/MechaDeath/MechaDeathChooseMechaUI.py
from __future__ import absolute_import
import six
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_CUSTOM
from common.cfg import confmgr
from logic.client.const import lobby_model_display_const
from logic.gutils import item_utils
from logic.gcommon import time_utility
from logic.gutils import dress_utils
from logic.gutils import lobby_model_display_utils
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.comsys.common_ui import InputBox
from logic.gcommon.item import item_const
from logic.gcommon.common_utils import text_utils
import cc
from logic.gutils import mecha_utils
TEMP_CHAT_CONTINUE_TIME = 3
CHAT_MESSAGE_INTERVAL = 10
CHOOSE_MECHA_TAG = 20200826

class MechaDeathChooseMechaUI(BasePanel):
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    PANEL_CONFIG_NAME = 'battle_tdm2/tdm2_choose_mech'
    UI_VKB_TYPE = UI_VKB_CUSTOM
    UI_ACTION_EVENT = {'btn_skill.OnBegin': 'on_click_skill_begin',
       'btn_skill.OnEnd': 'on_click_skill_end',
       'btn_sure.OnClick': 'on_click_sure',
       'btn_chat_history.OnClick': 'on_click_chat_history',
       'btn_chat_ok.OnClick': 'on_click_chat_ok',
       'nd_tips_close.OnClick': 'on_click_history_close',
       'btn_right_direction.OnClick': 'on_click_expand_btn'
       }

    def on_init_panel(self, *args, **kwargs):
        self.init_parameters()
        self.process_event(True)
        self.init_model_display()
        self.hide()

    def ui_vkb_custom_func(self):
        return True

    def on_finalize_panel(self):
        self.process_event(False)
        global_data.ui_mgr.remove_ui_show_whitelist('MechaDeathChooseMechaUI')
        self.input_box.destroy()
        self.input_box = None
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'mecha_death_choose_mecha_finished': self.on_choose_mecha_finished,
           'refresh_mecha_death_chosen_mecha': self.choose_mecha_result,
           'refresh_mecha_death_confirm_mecha': self.confirm_mecha_result,
           'receive_teammate_message': self.receive_teammate_message
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def init_parameters(self):
        self.is_confirmed = False
        self.selected_mecha_id = None
        self.mecha_ui_conf = confmgr.get('mecha_conf', 'UIConfig', 'Content')
        self.mecha_conf = confmgr.get('mecha_conf', 'MechaConfig', 'Content')
        self.last_send_timestamp = 0
        self.last_msg_timestamp = 0
        self.is_in_expand_mode = False
        self.all_mecha_list, self.own_mecha_list, self.share_mecha_lst = mecha_utils.get_mecha_lst()
        self.usual_mecha_ids = global_data.player.get_usual_mecha_ids()
        return

    def enter_choose_mecha(self, allow_mechas=None):
        self.allow_mechas = allow_mechas
        if allow_mechas:
            self.show_mecha_list = list(allow_mechas)
        else:
            self.show_mecha_list = self.get_reordered_mecha_list()
        if len(self.show_mecha_list) < 10:
            self.panel.nd_dir.setVisible(False)
        self.init_battle_data()
        self.init_top_widget()
        self.init_candidate_mecha_widget()
        self.init_player_index()
        self.init_chosen_mecha_widget()
        self.init_chat_widget()
        self.update_mecha_display()
        self.update_display_mecha_name()
        self.init_confirm_btn()
        self.show()
        global_data.ui_mgr.add_ui_show_whitelist(['MechaDeathChooseMechaUI', 'CloneMechaSkillDetail', 'NoticeUI', 'BattleReconnectUI', 'NormalConfirmUI2'], 'MechaDeathChooseMechaUI')
        self.panel.PlayAnimation('show')
        self.try_choose_mecha(self.selected_mecha_id, force=True)

    def init_battle_data(self):
        battle = global_data.battle
        if not battle:
            return
        self.map_conf = confmgr.get('map_config', str(battle.map_id), default={})
        self.brief_group_data = battle.brief_group_data
        self.chosen_mecha_dict = battle.chosen_mecha_dict
        self.confirmed_soul_list = battle.confirmed_soul_list
        self.chosen_fashion_dict = battle.chosen_fashion_dict
        self.chosen_mecha_list = battle.chosen_mecha_list
        self.is_limit_count = True
        if hasattr(battle, 'is_limit_count'):
            self.is_limit_count = battle.is_limit_count()
        self.is_all_owned = False
        if hasattr(battle, 'is_all_owned'):
            self.is_all_owned = battle.is_all_owned()
        self.selected_mecha_id = self.chosen_mecha_dict.get(global_data.player.id)
        self.is_confirmed = global_data.player.id in self.confirmed_soul_list

    def init_top_widget(self):
        self.init_time_widget()
        self.init_ready_widget(self.get_confirmed_player_cnt(), self.get_team_size())
        self.init_area_info_widget()

    def init_time_widget(self):
        self.start_choose_mecha_count_down()

    def init_ready_widget(self, confirmed_cnt, total_cnt):
        self.panel.nd_title.nd_player.lab_nub.SetString('{0}/{1}'.format(confirmed_cnt, total_cnt))
        self.panel.nd_ready.setVisible(self.is_confirmed)
        self.panel.nd_await.setVisible(not self.is_confirmed)
        if self.is_confirmed:
            self.panel.PlayAnimation('change')

    def init_area_info_widget(self):
        battle = global_data.battle
        map_name_text_ids = self.map_conf.get('cMapNameTextIds', [])
        text_id_index = 0
        prefix_str = ''
        if len(map_name_text_ids) >= 1 and battle and hasattr(battle, 'area_id'):
            text_id_index = min(int(battle.area_id), len(map_name_text_ids)) - 1
            prefix_str = '\xe2\x80\x94'
        self.panel.lab_map_name.setVisible(bool(prefix_str))
        map_text = ''.join([prefix_str, get_text_by_id(map_name_text_ids[text_id_index])])
        self.panel.lab_map_name.SetString(map_text)

    def init_chat_widget(self):

        def send_cb(*args, **kwargs):
            self.panel.btn_chat_ok.OnClick(None)
            return

        self.input_box = InputBox.InputBox(self.panel.input_box, send_callback=send_cb, detach_after_enter=False)
        self.input_box.set_rise_widget(self.panel)
        self.panel.nd_chat_quick.nd_tips_close.setVisible(False)
        self.panel.nd_chat_quick.temp_chat_quick.setVisible(False)
        self.panel.nd_chat_quick.setVisible(False)
        self.panel.nd_chat.list_chat_quick.DeleteAllSubItem()
        chat_history = global_data.battle.group_chat_history
        for player_id, msg in chat_history:
            self.make_one_history_msg(player_id, msg, self.panel.temp_chat_quick.list_chat_quick, player_id == global_data.player.id)

    def make_one_history_msg(self, player_id, message, list_chat, is_me, need_color=False):
        item = list_chat.AddTemplateItem(bRefresh=True)
        user_data = self.brief_group_data.get(player_id)
        name = user_data.get('char_name', '')
        if need_color:
            if not is_me:
                content = '<color=0xdadadaff>%s:#N <color=0xffffffff>%s#N' % (name, message)
            else:
                content = '<color=0x4efff0ff>%s:#N <color=0xffffffff>%s#N' % (name, message)
        else:
            content = '{}: {}'.format(name, message)
        item.lab_text.SetString(content)
        item_w, _ = item.GetContentSize()
        item.lab_text.formatText()
        text_size = item.lab_text.getVirtualRendererSize()
        item.SetContentSize(item_w, text_size.height + CHAT_MESSAGE_INTERVAL)
        item.ChildResizeAndPosition()
        list_chat._container._refreshItemPos()
        list_chat._refreshItemPos()
        list_chat.ScrollToBottom()

    def start_choose_mecha_count_down(self):
        battle = global_data.battle
        if not battle:
            return
        end_timestamp = battle.choose_mecha_end_timpstamp
        if not end_timestamp:
            return
        total_time = end_timestamp - time_utility.time()
        self.start_count_down(total_time)

    def start_count_down(self, total_time):

        def update_count_down(pass_time):
            left_time = int(total_time - int(pass_time))
            time_str = '%02d:%02d' % (left_time / 60, left_time % 60)
            self.panel.nd_title.nd_time.lab_time.SetString(time_str)
            if left_time <= 10:
                self.panel.nd_title.nd_time.lab_time.SetColor(16721472)
                self.panel.PlayAnimation('alarm')
            else:
                self.panel.nd_title.nd_time.lab_time.SetColor('#SW')

        def update_count_down_finished():
            self.panel.nd_title.nd_time.lab_time.SetString('00:00')

        self.panel.nd_title.StopTimerAction()
        if total_time < 0:
            update_count_down_finished()
            return
        update_count_down(pass_time=0)
        self.panel.nd_title.TimerAction(update_count_down, total_time, callback=update_count_down_finished, interval=1)

    def init_candidate_mecha_widget(self):
        from logic.gutils.InfiniteScrollWidget import InfiniteScrollWidget
        self.candi_mecha_list_view = InfiniteScrollWidget(self.panel.list_choose_mecha, self.panel, up_limit=500, down_limit=500)
        self.candi_mecha_list_view.set_template_init_callback(self.init_candi_mecha_btn)
        self.candi_mecha_list_view.enable_item_auto_pool(True)
        self.candi_mecha_list_view.update_data_list(self.show_mecha_list)
        self.candi_mecha_list_view.update_scroll_view()

    def is_allow(self, mecha_id):
        if self.allow_mechas:
            return int(mecha_id) in self.allow_mechas
        return True

    def init_candi_mecha_btn(self, candi_mecha_ui_item, mecha_id):
        lobby_mecha_id = dress_utils.battle_id_to_mecha_lobby_id(int(mecha_id))
        icon_path = 'gui/ui_res_2/item/mecha/%d.png' % lobby_mecha_id
        if not candi_mecha_ui_item:
            ui_item = self.get_candi_mecha_ui_item(mecha_id) if 1 else candi_mecha_ui_item
            if not ui_item:
                return
            ui_item.img_mecha.SetDisplayFrameByPath('', icon_path)
            ui_item.img_mecha_shadow.SetDisplayFrameByPath('', icon_path)
            is_owned = self.is_owned(mecha_id)
            is_usual = mecha_id in self.usual_mecha_ids
            return global_data.player or None
        is_used = mecha_id in global_data.player.get_setting('used_mecha', [])
        show_new = not is_used and is_owned
        show_share = mecha_id in self.share_mecha_lst
        is_free_now = mecha_utils.avatar_is_mecha_limited_free_now(lobby_mecha_id)
        show_free = not show_new and not show_share and is_free_now
        cur_cnt = self.chosen_mecha_list.count(mecha_id)
        is_full = self.is_full(mecha_id)
        should_lock = not is_owned and not is_free_now or is_full or not self.is_allow(mecha_id)
        ui_item.img_new.setVisible(show_new)
        ui_item.nd_share_tips.setVisible(show_share)
        ui_item.nd_mode_tips.setVisible(show_free)
        ui_item.img_always.setVisible(is_usual)
        ui_item.img_lock.setVisible(should_lock)
        ui_item.img_team_5.setVisible(True and self.is_limit_count)
        ui_item.img_team_5.lab_num_5.SetString(str(cur_cnt))
        ui_item.StopAnimation('choose')
        ui_item.RecoverAnimationNodeState('choose')
        ui_item.RecordAnimationNodeState('loop')
        if self.selected_mecha_id and self.selected_mecha_id == mecha_id:
            ui_item.btn_mecha.SetSelect(True)
            ui_item.nd_select.setScale(1.1)
            ui_item.PlayAnimation('choose')
            ui_item.PlayAnimation('loop')
            ui_item.SetTimeOut(0.5, lambda mecha_ui_item=ui_item: self.hide_candi_mecha_ui_item_light(mecha_ui_item), tag=210224)
        else:
            ui_item.btn_mecha.SetSelect(False)
            ui_item.nd_select.setScale(1)

        @ui_item.btn_mecha.callback()
        def OnBegin(*args):
            self.on_btn_mecha_begin(ui_item)

        @ui_item.btn_mecha.callback()
        def OnEnd(*args):
            self.on_btn_mecha_end(ui_item)

        @ui_item.btn_mecha.callback()
        def OnCancel(*args):
            self.on_btn_mecha_cancel(ui_item)

        @ui_item.btn_mecha.callback()
        def OnClick(*args):
            self.on_btn_mecha_click(ui_item, mecha_id, lobby_mecha_id)

        ui_display_conf = confmgr.get('ui_display_conf', 'MechaSummonUIItem', 'Content', default={})
        node_ui_conf = ui_display_conf.get(str(mecha_id))
        if node_ui_conf:
            pos = node_ui_conf.get('NodePos')
            if pos:
                ui_item.img_mecha.SetPosition(*pos)
            else:
                ui_item.img_mecha.ReConfPosition()
            pos = node_ui_conf.get('ShadowPos')
            if pos:
                ui_item.img_mecha_shadow.SetPosition(*pos)
            else:
                ui_item.img_mecha_shadow.ReConfPosition()
            scale = node_ui_conf.get('NodeScale')
            if scale:
                ui_item.img_mecha.setScale(scale)
                ui_item.img_mecha_shadow.setScale(scale)
            else:
                ui_item.img_mecha.ScaleSelfNode()
                ui_item.img_mecha_shadow.ScaleSelfNode()
        else:
            ui_item.img_mecha.ReConfPosition()
            ui_item.img_mecha_shadow.ReConfPosition()
            ui_item.img_mecha.ScaleSelfNode()
            ui_item.img_mecha_shadow.ScaleSelfNode()

    def on_btn_mecha_begin(self, ui_item):
        ui_item.nd_btn.setScale(1 / 0.83)
        ui_item.setLocalZOrder(1)
        ui_item.img_frame_choose.setVisible(True)
        ui_item.img_choose_light.setVisible(True)
        return True

    def on_btn_mecha_end(self, ui_item):
        ui_item.nd_btn.setScale(1)
        ui_item.setLocalZOrder(0)
        ui_item.img_frame_choose.setVisible(False)
        ui_item.img_choose_light.setVisible(False)

    def on_btn_mecha_cancel(self, ui_item):
        ui_item.nd_btn.setScale(1)
        ui_item.setLocalZOrder(0)
        ui_item.img_frame_choose.setVisible(False)
        ui_item.img_choose_light.setVisible(False)

    def is_full(self, mecha_id):
        return self.chosen_mecha_list.count(mecha_id) >= 2 and self.is_limit_count

    def is_owned(self, mecha_id):
        return mecha_id in self.own_mecha_list or self.is_all_owned

    def on_btn_mecha_click(self, ui_item, mecha_id, lobby_mecha_id):
        is_owned = self.is_owned(mecha_id)
        is_free_now = mecha_utils.avatar_is_mecha_limited_free_now(lobby_mecha_id)
        is_full = self.is_full(mecha_id)
        should_lock = not is_owned and not is_free_now or is_full
        if should_lock:
            text_id = 19841
            if is_full:
                return
            global_data.game_mgr.show_tip(get_text_by_id(text_id))
            return
        if not self.is_allow(mecha_id):
            return
        if self.is_confirmed:
            return
        self.try_choose_mecha(mecha_id)

    def init_chosen_mecha_widget(self):
        teammate_cnt = self.get_team_size()
        self.panel.list_duiyou.SetInitCount(teammate_cnt)
        for player_id, player_data in six.iteritems(self.brief_group_data):
            index = player_data['index']
            ui_item = self.panel.list_duiyou.GetItem(index)
            if not ui_item:
                continue
            is_ready = player_id in self.confirmed_soul_list
            is_me = player_id == global_data.player.id
            ui_item.lab_name.SetString(player_data.get('char_name', ''))
            if is_ready:
                ui_item.nd_ready.setVisible(True)
                ui_item.PlayAnimation('ready')
            else:
                ui_item.nd_ready.setVisible(False)
            self.play_chosen_mecha_widget_anim(ui_item, is_me)
            chosen_mecha_id = self.chosen_mecha_dict.get(player_id)
            chosen_fashion = self.chosen_fashion_dict.get(player_id, {})
            fashion_id = chosen_fashion.get(item_const.FASHION_POS_SUIT) or dress_utils.get_mecha_skin_item_no(chosen_mecha_id, -1)
            self.update_chosen_mecha_widget(ui_item, chosen_mecha_id, fashion_id, is_me)
            if player_id in self.confirmed_soul_list:
                ui_item.img_ready.setVisible(True)

        self.panel.list_duiyou.setTouchEnabled(False)

    def init_player_index(self):
        index = 0
        for player_id, data in six.iteritems(self.brief_group_data):
            data['index'] = index
            index += 1

    def play_chosen_mecha_widget_anim(self, widget, is_me):
        if is_me:
            self.panel.runAction(cc.Sequence.create([
             cc.DelayTime.create(widget.GetAnimationMaxRunTime('show')),
             cc.CallFunc.create(lambda : widget.PlayAnimation('me')),
             cc.DelayTime.create(widget.GetAnimationMaxRunTime('me')),
             cc.CallFunc.create(lambda : widget.PlayAnimation('loop'))]))
        else:
            self.panel.runAction(cc.Sequence.create([
             cc.DelayTime.create(widget.GetAnimationMaxRunTime('show')),
             cc.CallFunc.create(lambda : widget.PlayAnimation('team'))]))

    def init_confirm_btn(self):
        if self.is_confirmed:
            self.panel.btn_sure.setVisible(False)
            self.panel.nd_wait.setVisible(True)
            self.panel.PlayAnimation('wait')
        else:
            self.panel.btn_sure.setVisible(True)
            self.panel.nd_wait.setVisible(False)
            self.panel.StopAnimation('wait')

    def on_choose_mecha_finished(self):
        anim_delay = max(0, 3 - self.panel.GetAnimationMaxRunTime('out'))
        self.panel.runAction(cc.Sequence.create([
         cc.DelayTime.create(anim_delay),
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('out'))]))

    def update_candidate_mecha_widget(self, old_mecha_id, new_mecha_id):
        if old_mecha_id in self.show_mecha_list and old_mecha_id != new_mecha_id:
            cur_widget = self.get_candi_mecha_ui_item(old_mecha_id)
            if cur_widget:
                cur_widget.btn_mecha.SetSelect(False)
                cur_widget.StopAnimation('choose')
                cur_widget.RecoverAnimationNodeState('choose')
                cur_widget.StopAnimation('loop')
                cur_widget.RecoverAnimationNodeState('loop')
                cur_widget.nd_select.setScale(1)
                cur_widget.img_choose_light1.setVisible(False)
        if new_mecha_id in self.show_mecha_list:
            sel_widget = self.get_candi_mecha_ui_item(new_mecha_id)
            if sel_widget:
                sel_widget.PlayAnimation('choose')
                sel_widget.PlayAnimation('loop')
                sel_widget.nd_select.setScale(1.1)
                sel_widget.SetTimeOut(0.5, lambda mecha_ui_item=sel_widget: self.hide_candi_mecha_ui_item_light(mecha_ui_item), tag=201117)

    def update_display_mecha_name(self):
        conf = self.mecha_ui_conf[str(self.selected_mecha_id)]
        name_id, _, mecha_positioning = conf['name_text_id']
        self.lab_dingwei.SetString(mecha_positioning)
        self.lab_name.SetString(name_id)

    def update_chosen_mecha_widget(self, widget, mecha_id, fashion_id, is_me):
        if mecha_id is None:
            widget.nd_mech_head.setVisible(False)
            return
        else:
            img_path = confmgr.get('mecha_conf', 'SkinConfig', 'Content', str(fashion_id), 'half_img_path')
            widget.img_mech.SetDisplayFrameByPath('', img_path)
            widget.nd_mech_head.setVisible(True)
            widget.lab_meach.SetString(item_utils.get_mecha_name_by_id(mecha_id))
            if not is_me:
                widget.lab_meach.SetColor(2961525)
                widget.lab_name.SetColor(3881926)
            else:
                widget.lab_meach.SetColor(3026478)
                widget.lab_name.SetColor(5395543)
            return

    def get_available_mecha_list(self):
        mecha_id_list = []
        if global_data.player:
            mecha_open_info = global_data.player.read_mecha_open_info()
            mecha_open_order = mecha_open_info.get('opened_order', [])
            for mecha_id in mecha_open_order:
                if self._avatar_has_mecha(mecha_id):
                    mecha_id_list.append(mecha_id)

        return mecha_id_list

    def get_reordered_mecha_list(self):
        all_mecha_list = list(self.all_mecha_list)
        return sorted(all_mecha_list, key=lambda x: (not self.is_allow(x), x not in self.own_mecha_list, x not in self.usual_mecha_ids, x))

    def get_teammate_chosen_widget(self, player_id):
        player_index = self.brief_group_data.get(player_id, {}).get('index', -1)
        if player_index >= 0:
            return self.panel.list_duiyou.GetItem(player_index)
        else:
            return None
            return None

    def get_team_size(self):
        return len(self.brief_group_data)

    def get_confirmed_player_cnt(self):
        return len(self.confirmed_soul_list)

    def get_candi_mecha_ui_item(self, mecha_id):
        if mecha_id not in self.show_mecha_list:
            return None
        else:
            index = self.show_mecha_list.index(mecha_id)
            return self.candi_mecha_list_view.get_list_item(index)

    def hide_candi_mecha_ui_item_light(self, ui_item):
        ui_item.StopAnimation('choose')
        ui_item.vx_choose_light1.setVisible(False)
        ui_item.vx_choose_light2.setVisible(False)
        ui_item.img_choose_light.setVisible(False)

    def get_is_mecha_owned_curr(self, mecha_id):
        lobby_mecha_id = dress_utils.battle_id_to_mecha_lobby_id(int(mecha_id))
        is_owned = self.is_owned(mecha_id)
        is_free_now = mecha_utils.avatar_is_mecha_limited_free_now(lobby_mecha_id)
        return is_owned or is_free_now

    def try_choose_mecha(self, mecha_id, force=False):
        if not mecha_id:
            return
        if self.selected_mecha_id == mecha_id and not force:
            return
        if not global_data.battle:
            return
        global_data.battle.try_choose_mecha(mecha_id, force)

    def choose_mecha_result(self, player_id, mecha_id, fashion_dict, chosen_mecha_list):
        self.chosen_mecha_list = chosen_mecha_list
        is_me = False
        if player_id == global_data.player.id:
            is_me = True
            self.update_candidate_mecha_widget(self.selected_mecha_id, mecha_id)
            self.selected_mecha_id = mecha_id
            self.update_display_mecha_name()
            self.update_mecha_display()
            ui = global_data.ui_mgr.get_ui('CloneMechaSkillDetail')
            if ui:
                ui.refresh_ui(self.selected_mecha_id)
        self.update_candidate_mecha_list_status()
        fashion_id = fashion_dict.get(item_const.FASHION_POS_SUIT) or dress_utils.get_mecha_skin_item_no(mecha_id, -1)
        self.update_chosen_mecha_widget(self.get_teammate_chosen_widget(player_id), mecha_id, fashion_id, is_me)

    def update_candidate_mecha_list_status(self):
        for mecha_id in self.show_mecha_list:
            ui_item = self.get_candi_mecha_ui_item(mecha_id)
            if not ui_item:
                continue
            cur_cnt = self.chosen_mecha_list.count(mecha_id)
            if self.is_full(mecha_id):
                ui_item.img_lock.setVisible(True)
            else:
                ui_item.img_lock.setVisible(not self.get_is_mecha_owned_curr(mecha_id) or not self.is_allow(mecha_id))
            ui_item.img_team_5.setVisible(True and self.is_limit_count)
            ui_item.img_team_5.lab_num_5.SetString(str(cur_cnt))

    def confirm_mecha_result(self, soul_id, confirmed_soul_list):
        self.confirmed_soul_list = confirmed_soul_list
        if soul_id == global_data.player.id:
            self.is_confirmed = True
            self.panel.nd_wait.setVisible(True)
            self.panel.btn_sure.setVisible(False)
            self.panel.PlayAnimation('wait')
        self.panel.PlayAnimation('player')
        widget = self.get_teammate_chosen_widget(soul_id)
        widget and widget.nd_ready.setVisible(True) and widget.PlayAnimation('ready')
        self.init_ready_widget(self.get_confirmed_player_cnt(), self.get_team_size())

    def receive_teammate_message(self, soul_id, message, add_to_history=True):
        self.last_msg_timestamp = time_utility.time()

        def close_temp_chat():
            if time_utility.time() - self.last_msg_timestamp > TEMP_CHAT_CONTINUE_TIME:
                self.panel.nd_chat.setVisible(False)
                self.panel.nd_chat.list_chat_quick.DeleteAllSubItem()

        if add_to_history:
            self.make_one_history_msg(soul_id, message, self.panel.temp_chat_quick.list_chat_quick, soul_id == global_data.player.id)
            self.panel.temp_chat_quick.list_chat_quick._refreshItemPos()
            if not self.panel.nd_chat_quick.isVisible():
                self.panel.nd_chat.setVisible(True)
                self.make_one_history_msg(soul_id, message, self.panel.nd_chat.list_chat_quick, soul_id == global_data.player.id, need_color=True)
                self.panel.nd_chat.list_chat_quick._refreshItemPos()
                self.panel.SetTimeOut(TEMP_CHAT_CONTINUE_TIME, close_temp_chat)

    def on_click_sure(self, *args):
        if global_data.battle:
            global_data.battle.confirm_choose_mecha()

    def on_click_skill_begin(self, *args):
        ui = global_data.ui_mgr.show_ui('CloneMechaSkillDetail', 'logic.comsys.battle.Clone')
        ui.refresh_ui(self.selected_mecha_id)
        ui.PlayAnimation('appear')
        self.panel.img_shadow.setVisible(True)
        return True

    def on_click_skill_end(self, *args):
        global_data.ui_mgr.close_ui('CloneMechaSkillDetail')
        self.panel.img_shadow.setVisible(False)
        return True

    def on_click_chat_ok(self, *args):
        now = time_utility.time()
        if now - self.last_send_timestamp < 0.5:
            return
        self.last_send_timestamp = now
        text = self.input_box.get_text()
        if text == '':
            global_data.game_mgr.show_tip(get_text_by_id(11055), True)
            return
        self.input_box.set_text('')
        review_pass, msg = text_utils.check_review_words(text)
        if review_pass != text_utils.CHECK_WORDS_PASS:
            global_data.game_mgr.show_tip(get_text_by_id(11009), True)
            return
        global_data.battle.send_message(msg)

    def on_click_chat_history(self, *args):
        is_visible = not self.panel.nd_chat_quick.isVisible()
        self.panel.nd_chat_quick.nd_tips_close.setVisible(is_visible)
        self.panel.nd_chat_quick.temp_chat_quick.setVisible(is_visible)
        self.panel.nd_chat_quick.setVisible(is_visible)
        if is_visible:
            self.panel.nd_chat.setVisible(False)
            self.panel.nd_chat.list_chat_quick.DeleteAllSubItem()

    def on_click_history_close(self, *args):
        self.panel.nd_chat_quick.setVisible(False)

    def on_click_expand_btn(self, *args):
        if self.is_in_expand_mode:
            self.panel.list_choose_mecha.SetNumPerUnit(2)
            self.panel.btn_right_direction.setRotation(0)
            self.panel.img_list_bg.setVisible(True)
            self.panel.img_dw4.setVisible(False)
        else:
            self.panel.list_choose_mecha.SetNumPerUnit(4)
            self.panel.btn_right_direction.setRotation(180)
            self.panel.img_list_bg.setVisible(False)
            self.panel.img_dw4.setVisible(True)
        self.is_in_expand_mode = not self.is_in_expand_mode
        self.panel.list_choose_mecha.InitConfContentSize()
        self.panel.nd_dir.setContentSize(self.panel.list_choose_mecha.getContentSize())
        self.panel.nd_dir.ChildResizeAndPosition()
        self.candi_mecha_list_view.change_num_per_unit()

    def _avatar_has_mecha(self, mecha_id):
        bat = global_data.battle
        if bat:
            return bat.avatar_has_mecha(mecha_id)
        return False

    def init_model_display(self):

        @self.panel.nd_touch.unique_callback()
        def OnDrag(btn, touch):
            delta_pos = touch.getDelta()
            global_data.emgr.rotate_model_display.emit(-delta_pos.x / lobby_model_display_const.ROTATE_FACTOR)

    def update_mecha_display(self):
        lobby_select_id = dress_utils.get_mecha_dress_clothing_id(self.selected_mecha_id) or dress_utils.battle_id_to_mecha_lobby_id(self.selected_mecha_id)
        shiny_weapon_id = dress_utils.get_mecha_dress_shiny_weapon_id(self.selected_mecha_id)
        if lobby_select_id is None:
            global_data.emgr.change_model_display_scene_item.emit(None)
        else:
            display_type = lobby_model_display_const.MECHA_DEATH_CHOOSE_MECHA_SCENE
            global_data.emgr.set_lobby_scene_display_type.emit(display_type)
            model_data = lobby_model_display_utils.get_lobby_model_data(lobby_select_id, consider_second_model=False)
            for data in model_data:
                data['skin_id'] = lobby_select_id
                data['model_scale'] = 3
                data['shiny_weapon_id'] = shiny_weapon_id
                if self.selected_mecha_id == 8028:
                    data['show_anim'] = data['end_anim']

            global_data.emgr.change_model_display_scene_item.emit(model_data)
        return