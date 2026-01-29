# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/chat/FightChatUI.py
from __future__ import absolute_import
import six
from common.uisys.basepanel import BasePanel
import logic.comsys.common_ui.InputBox as InputBox
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.comsys.common_ui.CommonTips import Tips
from logic.gcommon.common_utils import text_utils
from logic.gutils.team_utils import get_color_hint_pic, get_teammate_colors, get_teammate_num, get_color_pic_path
from logic.gutils.item_utils import get_item_name, get_rare_degree_text_color, get_specific_photo_no
from logic.gutils.template_utils import get_item_quality
from logic.gutils import chat_utils
from cocosui import cc, ccui, ccs
import common.const.uiconst
import time
from logic.vscene.parts.gamemode.GMDecorator import execute_by_mode
from logic.client.const import game_mode_const
from logic.comsys.chat.FightTeamQuickChat import FightTeamQuickChat
from logic.gutils.dress_utils import check_quick_msg_photo_skip
from common.const.property_const import C_NAME, U_ID, U_LV, CLAN_ID
from logic.gutils.role_head_utils import init_role_head, set_role_head_frame, get_head_res_path_by_abs_id
STATE_ALIVE = 1
STATE_AGONY = 2
STATE_DEAD = 3

def set_special_message_bar(img, role_id):
    if role_id == 111:
        path = 'gui/ui_res_2/battle/panel/pnl_teammate_msg_kizunaai.png'
        img.SetDisplayFrameByPath('', path)
    else:
        path = 'gui/ui_res_2/battle/panel/pnl_teammate_msg.png'
        img.SetDisplayFrameByPath('', path)


class FightChatTips(Tips):

    def __init__(self, parent_nd, allow_cb=None, finish_cb=None, check_has_next_cb=None):
        super(FightChatTips, self).__init__(parent_nd, allow_cb, finish_cb, check_has_next_cb)
        self.edge_height = None
        self._teammate_ref = {}
        return

    def _gen_tips_nd(self):
        return global_data.uisystem.load_template_create('battle/i_teammate_message', self._parent_nd)

    def set_role_head(self, nd, data):
        photo_skip = data.get('photo_skip', False)
        if photo_skip:
            nd.temp_head.setVisible(False)
            nd.icon_hint.setVisible(False)
            lab = nd.lab_message
            bar = nd.message_bar
            x, y = lab.GetPosition()
            lab.SetPosition(19, y)
            x = lab.GetTextContentSize().width
            ori_x = x
            x, y = bar.GetPosition()
            bar.SetPosition(-19, y)
            x, y = bar.GetContentSize()
            bar.SetContentSize(ori_x + 26, y)
            return
        else:
            nd.temp_head.setVisible(True)
            lab = nd.lab_message
            bar = nd.message_bar
            x, y = lab.GetPosition()
            lab.SetPosition(59, y)
            x = lab.GetTextContentSize().width
            ori_x = x
            x, y = bar.GetPosition()
            bar.SetPosition(-59, y)
            x, y = bar.GetContentSize()
            bar.SetContentSize(ori_x + 66, y)
            head_photo = data.get('head_photo')
            head_frame = data.get('head_frame', global_data.player.get_head_frame() if global_data.player else None)
            role_id = data.get('role_id', global_data.player.get_role() if global_data.player else None)
            photo_no = data.get('photo_no', None)
            if photo_no:
                init_role_head(nd.temp_head, head_frame, photo_no)
            else:
                set_role_head_frame(nd.temp_head, head_frame)
                unit_id = data.get('unit_id', None)
                head_pic_path = self.get_head_pic(unit_id, role_id, head_photo)
                nd.temp_head.img_head.SetDisplayFrameByPath('', head_pic_path)
            return

    def get_head_pic(self, unit_id, role_id, head_photo):
        from logic.gutils import role_head_utils
        from logic.gcommon.common_const.ui_operation_const import DANMU_SHOW_DEFAULT_HEAD
        if head_photo:
            return role_head_utils.get_head_res_path_by_abs_id(head_photo)
        else:
            if global_data.player:
                is_my = unit_id == global_data.player.id if 1 else False
                danmu_show_default_head = global_data.player.get_setting(DANMU_SHOW_DEFAULT_HEAD) if global_data.player else True
                if is_my and not danmu_show_default_head:
                    abs_id = global_data.player.get_head_photo() if global_data.player else 30200011
                    return role_head_utils.get_head_res_path_by_abs_id(abs_id)
                teammate = self.get_entity(unit_id)
                specific_photo_no = None
                if teammate and teammate.is_valid():
                    role_id = role_id or teammate.ev_g_role_id()
                    fashion_data = teammate.ev_g_fashion()
                    if fashion_data:
                        specific_photo_no = get_specific_photo_no(fashion_data)
                role_id = role_id or 0
            if teammate and teammate.ev_g_in_mecha('Mecha'):
                abs_id = 30210000 + int(teammate.ev_g_get_bind_mecha_type())
            elif str(role_id) == '111':
                abs_id = 30201111
            else:
                abs_id = specific_photo_no or 30200000 + int(role_id)
            return get_head_res_path_by_abs_id(abs_id)
            return

    def get_entity(self, tid):
        t_ent = None
        if tid in self._teammate_ref:
            t_ent = self._teammate_ref[tid]()
            if not (t_ent and t_ent.is_valid()):
                del self._teammate_ref[tid]
                t_ent = None
        if not t_ent:
            import weakref
            from mobile.common.EntityManager import EntityManager
            ent = EntityManager.getentity(tid)
            if ent and ent.logic:
                self._teammate_ref[tid] = weakref.ref(ent.logic)
                t_ent = ent.logic
        return t_ent

    def on_show(self):
        self.set_special_message_bar(self._nd.message_bar)
        msg = self._msg_data['text']
        if type(self._msg_data['text']) is int:
            n_text = get_text_by_id(self._msg_data['text'])
            msg = n_text
        text_args = self._msg_data.get('text_id_args', None)
        color = self._color
        if 'mark_item_id' in self._msg_data:
            item_id = self._msg_data['mark_item_id']
            name = get_item_name(item_id)
            quality = get_item_quality(item_id)
            color = get_rare_degree_text_color(quality, '#BO')
            msg = msg.format(color=color, name=name)
        elif text_args:
            msg = msg.format(**text_args)
        edge_height = self._nd.message_bar.GetContentSize()[1] - self._nd.lab_message.GetContentSize()[1]
        if not self.edge_height:
            self.edge_height = edge_height
        self._nd.lab_message.SetString(msg)
        self._nd.lab_message.formatText()
        size = self._nd.lab_message.getTextContentSize()
        _, h = self._nd.message_bar.GetContentSize()
        if size.height + self.edge_height < h:
            height = h
        else:
            height = size.height + self.edge_height
            posx, _ = self._nd.temp_head.GetPosition()
            _, posy = self._nd.lab_message.GetPosition()
            self._nd.temp_head.SetPosition(posx, posy + h * 0.5)
        self._nd.message_bar.SetContentSize(size.width + 66, height)
        self._nd.icon_hint.SetDisplayFrameByPath('', get_color_hint_pic(color, self._msg_data))

        @self._nd.layer_msg.unique_callback()
        def OnClick(*args):
            if self.is_valid():
                self.on_other_tips_need_show()

        self.set_role_head(self._nd, self._msg_data)
        self._nd.PlayAnimation('show')
        act0 = cc.DelayTime.create(self._nd.GetAnimationMaxRunTime('show'))
        act1 = cc.DelayTime.create(0.4)
        act2 = cc.CallFunc.create(self._cc_check_has_next_cb_callback)
        act2_5 = cc.DelayTime.create(3.0)

        def _cc_play_hide_func():
            if self.is_valid():
                self._nd.PlayAnimation('disappear')

        act3 = cc.CallFunc.create(_cc_play_hide_func)
        act4 = cc.DelayTime.create(self._nd.GetAnimationMaxRunTime('disappear'))
        act5 = cc.CallFunc.create(self._cc_finish_callback)
        self._nd.runAction(cc.Sequence.create([
         act0, act1, act2, act2_5, act3, act4, act5]))
        return

    def on_other_tips_need_show(self):
        self._nd.stopAllActions()
        self._nd.PlayAnimation('disappear')
        act4 = cc.DelayTime.create(self._nd.GetAnimationMaxRunTime('disappear'))
        act5 = cc.CallFunc.create(self._cc_finish_callback)
        self._nd.runAction(cc.Sequence.create([
         act4, act5]))

    def set_special_message_bar(self, img):
        msg_data = self.get_msg_data()
        role_id = msg_data.get('role_id', 0)
        if role_id:
            set_special_message_bar(img, role_id)
        else:
            battle = global_data.battle
            if not battle:
                return
            target = global_data.cam_lctarget
            if target and target.share_data.ref_is_mecha:
                driver_id = target.ev_g_driver()
                target = battle.get_entity(driver_id)
                if target:
                    target = target.logic if 1 else None
                return target or None
            role_id = target.ev_g_role_id()
        set_special_message_bar(img, role_id)
        return


class FightChatTipsPC(FightChatTips):

    def _gen_tips_nd(self):
        return global_data.uisystem.load_template_create('battle/i_teammate_message_pc', self._parent_nd)


class FightChatBaseUI(BasePanel):
    DLG_ZORDER = common.const.uiconst.NORMAL_LAYER_ZORDER_1
    SEND_CD = 4.0
    UI_VKB_TYPE = common.const.uiconst.UI_VKB_CUSTOM
    GLOBAL_EVENT = {'open_fight_chat_ui_event': 'on_fight_chat_ui',
       'scene_observed_player_setted_event': 'on_enter_observe'
       }
    ENABLE_HOT_KEY_SUPPORT = True

    def on_init_panel(self, *args, **kargs):
        self._is_chat_open = False
        self._last_send_time = 0
        self.is_in_send_cd = False
        self.init_bottom()
        self.cur_state = None
        self.chat_close()
        if self.panel.btn_pc:
            self.panel.btn_pc.setVisible(True)
            sz = self.panel.nd_diy.input_box.getContentSize()
            import cc
            self.panel.nd_diy.input_box.setContentSize(cc.Size(170, sz.height))
            self._input_box.change_input_width()
        self._history_msg = None
        self.invite_item = self.panel.nd_invite
        self.invite_item.btn_agree.btn_common.BindMethod('OnClick', self.on_click_agree)
        self.invite_item.btn_refuse.btn_common.BindMethod('OnClick', self.on_click_refuse)
        self.invite_list = []
        self.invite_timer = None
        return

    def on_finalize_panel(self):
        if self._input_box:
            self._input_box.destroy()
            self._input_box = None
        if self.invite_timer:
            global_data.game_mgr.unregister_logic_timer(self.invite_timer)
            self.invite_timer = None
        return

    def init_bottom(self):
        nd_bottom = self.panel.nd_diy
        self._input_box = InputBox.InputBox(nd_bottom.input_box, max_length=20, placeholder=get_text_by_id(15816), send_callback=self.on_edit_box_send_callback, input_callback=self.on_edit_box_changed_callback)
        self._input_box.set_rise_widget(self.panel)
        self.panel.btn_title_1.lab_title.SetString(get_text_by_id(80236))
        self.panel.btn_title_2.lab_title.SetString(get_text_by_id(19767))
        self.panel.btn_title_1.BindMethod('OnClick', lambda *args: self.on_tag_change('quick'))
        self.panel.btn_title_2.BindMethod('OnClick', lambda *args: self.on_tag_change('record'))
        self.on_tag_change('quick')

    def on_enter_observe(self, target):
        pass

    def check_can_send(self):
        import math
        MIN_SEND_TIME = self.SEND_CD
        cur_time = time.time()
        pass_time = cur_time - self._last_send_time
        from logic.gcommon.common_const import ui_operation_const as uoc
        if global_data.player and global_data.player.get_setting_2(uoc.BLOCK_ALL_MSG_KEY):
            return False
        if pass_time < MIN_SEND_TIME:
            global_data.game_mgr.show_tip(get_text_by_id(11008, {'time': str(int(math.ceil(MIN_SEND_TIME - pass_time)))}))
            return False
        return True

    def on_edit_box_send_callback(self, *args):
        msg = self._input_box.get_text()
        if not msg:
            return
        check_code, flag, msg = text_utils.check_review_words_chat(msg)
        if flag != text_utils.CHECK_WORDS_PASS:
            global_data.player.notify_client_message((get_text_by_id(11009),))
            global_data.player.sa_log_forbidden_msg('fight_chat', msg, check_code, hint=3, input_type='shortcut')
            return
        if not self.check_can_send():
            return
        if not global_data.player or not global_data.player.logic:
            return
        self._last_send_time = time.time()
        global_data.player.logic.send_event('E_SEND_BATTLE_GROUP_MSG', {'text': msg,'is_self_send': True})
        self._input_box.set_text('')
        self.chat_close()

    def on_edit_box_changed_callback(self, text):
        if text.endswith('\n') or text.endswith('\r'):
            text = text.rstrip('\n')
            text = text.rstrip('\r')
            self._input_box.set_text(text)
            self._input_box.detachWithIME()

    def on_fight_chat_ui(self, *args):
        if not self.panel.pnl_chat_list.isVisible():
            self.chat_open()
        else:
            self.chat_close()

    @execute_by_mode(True, game_mode_const.Open_ChatCoreUI)
    def chat_open(self):
        self.chat_open_core()
        if self.invite_list:
            self.on_tag_change('record')

    QUICK_LIST_REFRESH_TIMER_TAG = 2162953

    def chat_open_core(self):
        self.panel.pnl_chat_list.setVisible(True)
        self.panel.bg_layer.setVisible(True)
        repeat_action = [
         cc.CallFunc.create(self.update_cur_quick_list),
         cc.DelayTime.create(0.3)]
        action = self.panel.runAction(cc.RepeatForever.create(cc.Sequence.create(repeat_action)))
        action.setTag(self.QUICK_LIST_REFRESH_TIMER_TAG)
        if global_data.mouse_mgr:
            global_data.mouse_mgr.add_cursor_show_count(self.__class__.__name__)
        self.init_history_msg()

    def chat_close(self):
        self.panel.pnl_chat_list.setVisible(False)
        self.panel.bg_layer.setVisible(False)
        self.stopActionByTag(self.QUICK_LIST_REFRESH_TIMER_TAG)
        if global_data.mouse_mgr:
            global_data.mouse_mgr.add_cursor_hide_count(self.__class__.__name__)

    def update_cur_quick_list(self):
        choose_chat_list = FightTeamQuickChat.get_choose_chat_list()
        if self.panel.lv_chat_list.GetItemCount() != len(choose_chat_list):
            self.panel.lv_chat_list.SetInitCount(len(choose_chat_list))
        for idx, (chat_id, chat_content) in enumerate(choose_chat_list):
            choose_item = self.panel.lv_chat_list.GetItem(idx)
            self.init_choose_item(choose_item, chat_id, chat_content)

    def init_choose_item(self, ui_item, chat_id, content):
        btn = ui_item.btn_chat
        lab_content = ui_item.lab_content
        item_chat_id = getattr(btn, 'chat_id', None)
        lab_content.SetString(content)
        if item_chat_id == chat_id:
            return
        else:
            btn.chat_id = chat_id

            @btn.unique_callback()
            def OnClick(btn, touch):
                if not self.check_can_send():
                    return
                self._last_send_time = time.time()
                btn_chat_id = btn.chat_id
                self.send_battle_quick_group_msg(btn_chat_id)
                self.chat_close()

            return

    def send_battle_quick_group_msg(self, chat_id):
        if global_data.player and global_data.player.logic:
            text_id, args = FightTeamQuickChat.get_role_chat_str(global_data.player.get_role(), chat_id)
            voice_trigger_type = FightTeamQuickChat.get_role_chat_trigger_type(global_data.player.get_role(), chat_id)
            msg_dict = {'text': text_id,'is_self_send': True,'text_id_args': args}
            if voice_trigger_type:
                msg_dict['voice_trigger_type'] = voice_trigger_type
            photo_skip = check_quick_msg_photo_skip(global_data.player.logic.ev_g_fashion().get('0', -1))
            msg_dict['photo_skip'] = photo_skip
            global_data.player.logic.send_event('E_SEND_BATTLE_GROUP_MSG', msg_dict, True)

    def on_bg_layer_begin(self, btn, touch):
        is_click_in_chat_btn = global_data.emgr.is_click_in_chat_btn_event.emit(touch)
        if is_click_in_chat_btn and len(is_click_in_chat_btn) > 0:
            if is_click_in_chat_btn[0]:
                return
        self.chat_close()

    def on_click_btn_send(self, btn, touch):
        self._input_box.detachWithIMEWithSendCallback()

    def ui_vkb_custom_func(self):
        if self.panel.pnl_chat_list.isVisible():
            self.chat_close()
            return True
        else:
            return False

    def do_hide_panel(self):
        super(FightChatBaseUI, self).do_hide_panel()
        self._input_box and self._input_box.hide()

    def on_tag_change(self, tag):
        is_quick = tag == 'quick'
        self.panel.lv_chat_list.setVisible(is_quick)
        self.panel.btn_title_1.SetSelect(is_quick)
        is_record = tag == 'record'
        self.panel.nd_tab_record.setVisible(is_record)
        self.panel.btn_title_2.SetSelect(is_record)
        if is_record:
            self.init_history_msg()

    def init_history_msg(self, msg_list=None):
        if not self.panel.nd_tab_record.isVisible():
            return
        else:
            if not global_data.player or not global_data.player.logic:
                return
            if msg_list is None:
                msg_list = global_data.player.logic.ev_g_group_history_msg() or []
            if global_data.battle.get_max_teammate_num() > 3:
                icon_visible = False
                mate_color = {}
            else:
                icon_visible = True
                mate_id = global_data.player.logic.ev_g_groupmate()
                mate_color = get_teammate_colors(mate_id)
                mate_color = {eid:get_color_pic_path('gui/ui_res_2/battle/icon/icon_teammate_num_', color) for eid, color in six.iteritems(mate_color)}
            container = self.panel.list_chat_record
            container.SetInitCount(len(msg_list))
            for i, info in enumerate(msg_list):
                item = container.GetItem(i)
                eid, name, msg = info
                item.sp_locate.setVisible(icon_visible)
                if icon_visible:
                    if eid in mate_color:
                        pic_path = mate_color[eid] if 1 else 'gui/ui_res_2/battle/icon/icon_teammate_num_gray.png'
                        item.sp_locate.SetDisplayFrameByPath('', pic_path)
                        item.lab_num.setVisible(False)
                    item.teamate_name.SetString(name + ': ' + msg)

            _, H = container.GetContentSize()
            _, CH = container.GetContainer().GetContentSize()
            if H > CH:
                container.ScrollToTop()
            else:
                container.ScrollToBottom()
            return

    def add_invitation(self, confirm_id, extra_info):
        uid = extra_info.get('uid', None)
        if self.invite_list:
            for c, e in self.invite_list:
                if uid == e.get('uid', None):
                    return

        self.invite_list.append((confirm_id, extra_info))
        if len(self.invite_list) == 1:
            self.try_show_next_invitation()
        return

    def try_show_next_invitation(self):
        if not self.invite_list:
            self.destroy_invite()
            return
        else:
            confirm_id, extra_info = self.invite_list[0]
            if not self.invite_timer:
                from common.utils.timer import CLOCK
                self.invite_timer = global_data.game_mgr.register_logic_timer(self.update_invite_count_down, interval=1, times=-1, mode=CLOCK)
            self.invite_item.setVisible(True)
            self.resize_record_list(True)
            name = extra_info.get('char_name', '')
            self.invite_item.name.SetString(name)
            global_data.emgr.on_recv_danmu_msg.emit(get_text_by_id(13155, {'name': '<color=0XFECD40FF>%s</color>' % name}))
            from logic.gutils.role_head_utils import init_role_head
            init_role_head(self.invite_item.head, extra_info.get('head_frame', None), extra_info.get('head_photo', None))
            self.invite_item.lab_tips.SetString(extra_info.get('msg', ''))
            ui = global_data.ui_mgr.get_ui('QuickMarkBtn')
            ui and ui.show_img_tips(True)
            return

    def update_invite_count_down(self):
        if not self.invite_list:
            self.destroy_invite()
            return
        confirm_id, extra_info = self.invite_list[0]
        ts = extra_info.get('timestamp', 0)
        from logic.gcommon.time_utility import get_server_time
        cur_time = get_server_time()
        left_time = 30 - int(cur_time - ts)
        if left_time <= 0:
            self.on_click_refuse()
        else:
            self.invite_item.btn_refuse.btn_common.SetText('%s(%ds)' % (get_text_by_id(80563), left_time))

    def send_private_msg(self, uid, msg):
        if not uid or not msg:
            return
        friends = global_data.message_data.get_friends()
        if not friends:
            return
        fd_info = friends.get(uid)
        if not fd_info:
            return
        chat_name = fd_info.get(C_NAME, '')
        chat_lv = fd_info.get(U_LV, 1)
        frd_cid = fd_info.get(CLAN_ID, -1)
        global_data.message_data.recv_to_friend_msg(uid, chat_name, msg, chat_lv)
        global_data.player.req_friend_msg(uid, chat_lv, frd_cid, msg)

    def on_click_refuse(self, *args):
        if not self.invite_list:
            self.destroy_invite()
            return
        confirm_id, extra_info = self.invite_list[0]
        global_data.player.req_confirm(confirm_id, 1)
        uid = extra_info.get('uid')
        msg = get_text_by_id(10385)
        self.send_private_msg(uid, msg)
        self.invite_list.pop(0)
        self.try_show_next_invitation()

    def on_click_agree(self, *args):
        if not self.invite_list:
            self.destroy_invite()
            return
        confirm_id, extra_info = self.invite_list[0]
        global_data.player.req_confirm(confirm_id, 0)
        for confirm_id, extra_info in self.invite_list:
            global_data.player.req_confirm(confirm_id, 1)
            uid = extra_info.get('uid')
            msg = get_text_by_id(10384)
            self.send_private_msg(uid, msg)

        self.invite_list = []
        self.destroy_invite()

    def destroy_invite(self):
        self.invite_item.setVisible(False)
        if self.invite_timer:
            global_data.game_mgr.unregister_logic_timer(self.invite_timer)
            self.invite_timer = None
        ui = global_data.ui_mgr.get_ui('QuickMarkBtn')
        ui and ui.show_img_tips(False)
        self.resize_record_list(False)
        return

    def resize_record_list(self, small):
        self.panel.list_chat_record.SetContentSize(296, 170 if small else 321)


class FightChatUI(FightChatBaseUI):
    PANEL_CONFIG_NAME = 'observe/fight_chat'
    UI_ACTION_EVENT = {'bg_layer.OnBegin': 'on_bg_layer_begin',
       'btn_pc.OnEnd': 'on_click_btn_send'
       }

    def on_hot_key_closed_state(self):
        super(FightChatUI, self).on_hot_key_closed_state()

    def on_hot_key_opened_state(self):
        super(FightChatUI, self).on_hot_key_opened_state()