# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/live/LiveTVUI.py
from __future__ import absolute_import
from __future__ import print_function
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_3, UI_VKB_CLOSE
from common.live.live_agent_mgr import LiveAgentMgr
from logic.gcommon.common_utils.local_text import get_text_by_id
import time
import game3d
import render
from cocosui import cc
from logic.gcommon.common_utils.text_utils import check_review_words
VBR_OP_CD = 10.0
VBR_CHN_NAME = {'standard': 2171,
   'high': 2172,
   'ultra': 2173,
   'blueray': 2174,
   'super': 2173
   }

class LiveTVUI(BasePanel):
    PANEL_CONFIG_NAME = 'live/live_showing'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_3
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'temp_close.btn_back.OnClick': 'on_click_close_btn',
       'touch_layer.OnClick': 'on_click_touch_layer',
       'touch_layer_front.OnClick': 'on_click_touch_layer_front',
       'btn_send.OnClick': 'on_click_send_btn',
       'layer_choose_list.OnClick': 'on_click_layer_choose_list',
       'btn_follow.OnClick': 'on_click_follow_btn',
       'btn_fuchuang.OnClick': 'on_click_fuchuang_btn'
       }
    GLOBAL_EVENT = {'receive_live_room_data_event': 'receive_live_room_data'
       }

    def on_init_panel(self, *args, **kwargs):
        self.init_play_data()
        self.panel.setLocalZOrder(1)
        self._float_nd = None
        self._liveFloatingWidget = None
        self.is_in_float = False
        self._channel_id = None
        self._video_player = None
        self._is_bar_show = False
        self._bottom_show_pos = self.panel.nd_bottom.getPosition()
        self._input_bottom_wpos = self.panel.temp_input_danmu.ConvertToWorldSpace(0, 0)
        self._max_retry_play_time = 2
        self._input_box = None
        self._vbr_options = []
        self.play_connecting_animation()
        self.process_events(True)
        self.show_ope_bar()
        self.init_danmu()
        self.init_status()
        global_data.sound_mgr.set_mute(True)
        self.hide_main_ui(['LiveMainUI'])
        self._is_in_input = False
        self.panel.nd_connecting.setCascadeColorEnabled(True)
        self.panel.nd_off_line.setCascadeColorEnabled(True)
        return

    def init_play_data(self):
        self._live_data = None
        self._player = None
        self._cur_vbr_choose = None
        self._vbr_init = False
        self._subing_msg = False
        self.is_danmu_enable = False
        self._video_ready = False
        self._video_complete = False
        self._last_send_time = 0
        self._in_request_room_uid = None
        self._live_url = None
        self._anchor_id = None
        self._retry_play_time = 0
        return

    def on_finalize_panel(self):
        self.set_danmu_enable(False)
        if self._input_box:
            self._input_box.destroy()
            self._input_box = None
        global_data.sound_mgr.set_mute(False)
        self.process_events(False)
        if self._player:
            self._player.clear_live_room_msg()
            self._player.stop()
        self._player = None
        if self.status_timer:
            tm = global_data.game_mgr.get_logic_timer()
            tm.unregister(self.status_timer)
            self.status_timer = None
        self._float_nd = None
        self.destroy_widget('_liveFloatingWidget')
        self.show_main_ui()
        return

    def on_click_close_btn(self, btn, touch):
        global_data.ui_mgr.close_ui('DanmuLinesUI')
        self.close()

    def init_vbr_mode_list(self, all_vbr_list):
        self._vbr_options = [ {'name': VBR_CHN_NAME.get(vbr, vbr),'mode': vbr} for vbr in all_vbr_list ]
        self.refresh_vbr_mode_list_show()

    def refresh_vbr_mode_list_show(self):
        if not self._vbr_init:
            return
        from logic.gutils import template_utils

        @self.panel.btn_definition.unique_callback()
        def OnClick(btn, touch):
            if not self._video_ready:
                self.show_tips(get_text_by_id(15810))
                return
            if not self.panel.choose_list.isVisible():
                self.panel.choose_list.setVisible(True)
                self.panel.img_point.setRotation(180)
                self.panel.layer_choose_list.setVisible(True)
            else:
                self.hide_choose_list()

        def call_back(index):
            option = self._vbr_options[index]
            self._cur_vbr_choose = option['mode']
            self.panel.btn_definition.SetText(option['name'])
            self.hide_choose_list()
            if self._player:
                self._player.set_vbr(self._cur_vbr_choose)

        self.hide_choose_list()
        template_utils.init_common_choose_list(self.panel.choose_list, self._vbr_options, call_back)

    def set_play_data(self, live_type, data):
        if self._live_data is not None:
            if str(self._live_data.get('uid')) != str(data.get('uid')):
                self.init_play_data()
                self.init_danmu()
                if self._player:
                    self._player.stop()
        self._live_data = data
        self._live_type = live_type
        from logic.vscene.part_sys.live.LivePlatformManager import LivePlatformManager
        is_support_dammu = LivePlatformManager().get_cur_platform().is_support_dammu()
        self.panel.nd_danmu.setVisible(is_support_dammu)
        self._channel_id = data.get('channel_id', None)
        need_request = data.get('need_request', False)
        self._start_play(live_type, data)
        self.setup_anchor_data(data)
        if need_request and not self._live_url and not self._in_request_room_uid:
            uid = data.get('uid', None)
            self._in_request_room_uid = uid
            from logic.vscene.part_sys.live.LivePlatformManager import LivePlatformManager
            LivePlatformManager().get_cur_platform().request_live_room_data(data)
        else:
            self._player.get_vbr_list()
        return

    def setup_anchor_data(self, data):
        from logic.gutils.live_utils import format_one_line_text, format_view_person
        nickname = data.get('nickname', '')
        title = data.get('title', '') or ''
        hot_score = data.get('hot_score', 0)
        node = self.panel.nd_top
        formated_title = format_one_line_text(node.lab_title, title, self.panel.nd_title_max_length.getContentSize().width)
        node.lab_title.SetString(formated_title)
        formated_name = format_one_line_text(node.lab_name, nickname, self.panel.nd_max_name_length.getContentSize().width)
        node.lab_name.SetString(formated_name)
        self.panel.lab_pop.SetString(format_view_person(hot_score))
        head_img = data.get('head')
        uid = data.get('uid')
        sp_head_name = '%s_%s_head' % (str(self._live_type), str(uid))
        if head_img:
            from logic.vscene.part_sys.live.LiveSpriteManager import LiveSpriteManager
            LiveSpriteManager().SetSpriteByLink(self.panel.img_head, head_img, sp_head_name)
        self.init_follow_data()
        self.refresh_float_show()

    def _start_play(self, live_type, live_data):
        LiveAgentMgr().switch_live_agent(live_type, live_data)
        self._player = LiveAgentMgr().get_live_agent()
        url = self.get_live_url(live_data)
        if url:
            self._player.play_live(url)
            self._live_url = url
        self.play_connecting_animation()

    def get_live_url(self, live_data):
        if game3d.get_platform() == game3d.PLATFORM_WIN32:
            url = live_data.get('video_url', '')
        else:
            url = live_data.get('mobile_url', '')
        return url

    def play_connecting_animation(self):
        self.panel.nd_connecting.setVisible(True)
        self.panel.PlayAnimation('connecting')

    def stop_connecting_animation(self):
        self.panel.nd_connecting.setVisible(False)
        self.panel.StopAnimation('connecting')

    def on_live_online(self):
        self.panel.nd_off_line.setVisible(False)
        self.panel.nd_connecting.setVisible(True)

    def on_live_offline(self):
        self.panel.nd_off_line.setVisible(True)
        self.panel.nd_connecting.setVisible(False)

    def _set_vbr_info(self, cur_vbr, vbr_list):
        self.panel.btn_definition.SetText(VBR_CHN_NAME.get(cur_vbr, cur_vbr))
        if self._vbr_init:
            self._vbr_op_time = time.time()
            if cur_vbr in VBR_CHN_NAME:
                vbr_name = get_text_by_id(VBR_CHN_NAME[cur_vbr])
            else:
                vbr_name = cur_vbr
            tips = get_text_by_id(15812, (vbr_name, ''))
            self.show_tips(tips)
        if self._vbr_init:
            return
        self._vbr_init = True
        self.init_vbr_mode_list(vbr_list)

    def set_up_play_sprite(self):
        if self.panel.nd_live.live_spr:
            self.panel.nd_live.live_spr.Destroy()
        provider = LiveAgentMgr().get_live_agent().fetch_data_provider()
        render_tex = render.texture('cclive', data_provider=provider)
        from common.uisys.uielment.CCSprite import CCSprite
        spr_cc = CCSprite.CreateWithTexture(cc.Texture2D.createWithITexture(render_tex))
        self.panel.nd_live.AddChild('live_spr', spr_cc)
        self.check_spr_pos_size()
        self.check_spr_shader(spr_cc)

    def check_spr_pos_size(self):
        spr_cc = self.panel.nd_live.live_spr
        if not spr_cc:
            return
        if not self.is_in_float:
            spr_cc.setAnchorPoint(cc.Vec2(0.5, 0.5))
            spr_cc.SetPosition('50%', '50%')
            self._adjust_spr_scale(reverse_scale=self.panel.getScale())
        elif self._float_nd:
            self._adjust_spr_scale(self._float_nd.nd_show.getContentSize())
            wpos = self._float_nd.nd_show.getParent().convertToWorldSpace(self._float_nd.nd_show.getPosition())
            lpos = self.panel.nd_live.live_spr.getParent().convertToNodeSpace(wpos)
            self.panel.nd_live.live_spr.setPosition(lpos)

    def _adjust_spr_scale(self, full_size=None, reverse_scale=1.0):
        spr = getattr(self.panel.nd_live, 'live_spr')
        if spr:
            if not full_size:
                full_size = global_data.ui_mgr.design_screen_size
            spr_size = spr.getContentSize()
            scale = min(float(full_size.width / spr_size.width), float(full_size.height / spr_size.height))
            spr.setScale(scale / reverse_scale)

    def process_events(self, is_bind=True):
        emgr = global_data.emgr
        econf = {'live_ready_event': self._video_ready_callback,
           'live_report_stat_event': self._report_stat_callback,
           'live_seek_complete_event': self._seek_complete_callback,
           'live_error_event': self._error_callback,
           'live_get_vbr_list_event': self._get_vbr_list_callback,
           'live_danmu_msg_event': self._on_msg_pub,
           'notify_follow_anchor_change_event': self.platform_update_follow_show,
           'live_url_change_event': self.on_live_url_changed,
           'live_vbr_change_event': self.on_live_vbr_changed,
           'textfield_eventtype_attach_with_ime_event': self.on_attach_input,
           'textfield_eventtype_detach_with_ime_event': self.on_detach_input
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def _video_ready_callback(self):
        self.stop_connecting_animation()
        self.set_up_play_sprite()
        self._video_ready = True
        self.check_sub_states()

    def _video_complete_callback(self):
        self.on_live_offline()
        self._video_complete = True

    def _report_stat_callback(self):
        pass

    def _seek_complete_callback(self):
        pass

    def _error_callback(self):
        if self._video_complete:
            return
        if self._retry_play_time < self._max_retry_play_time:
            self._player.stop()
            self._player.play_live(self._live_url)
            self._retry_play_time += 1
            return

        def _do_close():
            global_data.ui_mgr.close_ui('LiveTVUI')

        from logic.comsys.common_ui.NormalConfirmUI import NormalConfirmUI2
        NormalConfirmUI2(content=get_text_by_id(15813), on_confirm=_do_close)

    def _get_vbr_list_callback(self, cur_vbr, vbr_list):
        self._set_vbr_info(cur_vbr, vbr_list)

    def on_live_url_changed(self, url):
        if url:
            if self._player:
                if self._live_url != url:
                    self._player.stop()
                self._player.play_live(url)
                self._live_url = url

    def on_live_vbr_changed(self, cur_vbr):
        if cur_vbr in VBR_CHN_NAME:
            vbr_name = get_text_by_id(VBR_CHN_NAME[cur_vbr])
        else:
            vbr_name = cur_vbr
        tips = get_text_by_id(15812, (vbr_name, ''))
        self.show_tips(tips)

    def on_click_touch_layer(self, layer, touch):
        if self.is_in_float:
            return
        if self._is_bar_show:
            self.hide_ope_bar()
        else:
            self.show_ope_bar()

    def on_click_touch_layer_front(self, btn, touch):
        if self.is_in_float:
            return
        if self._is_bar_show:
            self.panel.SetTimeOut(5.0, self.hide_ope_bar, tag=69)

    def show_ope_bar(self):
        self.panel.StopAnimation('function_disappear')
        self.panel.PlayAnimation('function_show')
        self._is_bar_show = True
        self.panel.SetTimeOut(5.0, self.hide_ope_bar, tag=69)

    def hide_ope_bar(self):
        if self.is_in_float:
            return
        if self._is_in_input:
            return
        self.panel.StopAnimation('function_show')
        self.panel.PlayAnimation('function_disappear')
        self.panel.stopActionByTag(69)
        self._is_bar_show = False

    def _on_btn_vbr_click(self, widget):
        if not self._video_ready:
            self.show_tips(get_text_by_id(15814))
            return
        if time.time() - self._vbr_op_time < VBR_OP_CD:
            self.show_tips(get_text_by_id(15815))
            return
        self._frame_vbr.set_visible(True)
        self._has_drop_down_box = True

    def show_tips(self, msg):
        global_data.game_mgr.show_tip(msg)

    def init_danmu(self):
        import logic.comsys.common_ui.InputBox as InputBox
        from logic.gutils.template_utils import init_common_single_choose
        nd_input = self.panel.temp_input_danmu
        self._input_box = InputBox.InputBox(nd_input)
        self._input_box.set_rise_widget(self.panel.nd_bottom, self._bottom_show_pos, self._input_bottom_wpos)
        init_dammu_enable = True
        init_common_single_choose(self.panel.temp_choose_danmu, self.set_danmu_enable, init_dammu_enable)
        self.set_danmu_enable(init_dammu_enable)

    def set_danmu_enable(self, is_enable):
        if is_enable:
            global_data.ui_mgr.show_ui('DanmuLinesUI', 'logic.comsys.observe_ui')
        dlg = global_data.ui_mgr.get_ui('DanmuLinesUI')
        if dlg is not None:
            dlg.enable_danmu(is_enable)
        self.is_danmu_enable = is_enable
        self.check_sub_states()
        return

    def check_sub_states(self):
        if self.is_danmu_enable:
            self._sub_msg()
        else:
            self._unsub_msg()

    def on_click_send_btn(self, btn, touch):
        if not self._video_ready:
            self.show_tips(get_text_by_id(15814))
            return
        cur_time = time.time()
        if cur_time - self._last_send_time < 0.5:
            return
        self._last_send_time = cur_time
        msg = self._input_box.get_text()
        if not msg:
            self.show_tips(get_text_by_id(2175))
            return
        flag, msg = check_review_words(msg)
        if not flag:
            global_data.player.notify_client_message((get_text_by_id(11009),))
            return
        if global_data.player:
            self._player.send_live_dammu(msg)
            self._input_box.set_text('')

    def _sub_msg(self):
        if not self._video_ready or self._subing_msg:
            return
        self._subing_msg = True
        self._player.sub_msg()

    def _unsub_msg(self):
        if not self._video_ready or not self._subing_msg:
            return
        self._subing_msg = False
        self._player.unsub_msg()

    def _on_msg_pub(self, channel_id, data):
        if not self._subing_msg:
            return
        if channel_id and channel_id != self._channel_id:
            return
        for msg_detail in data['list']:
            msg_str = '[%s]:%s' % (msg_detail['nick'], msg_detail['msg_body'])
            global_data.emgr.on_recv_danmu_msg.emit(msg_str, 0)

    def on_click_layer_choose_list(self, btn, touch):
        self.hide_choose_list()

    def hide_choose_list(self):
        self.panel.choose_list.setVisible(False)
        self.panel.img_point.setRotation(0)
        self.panel.layer_choose_list.setVisible(False)

    def init_follow_data(self):
        self.update_follow_show()

    def update_follow_show(self):
        urs = str(self._live_data.get('follow_uid', None))
        from logic.vscene.part_sys.live.LivePlatformManager import LivePlatformManager
        is_follow = LivePlatformManager().get_cur_platform().check_is_anchor_followed(urs)
        self.panel.btn_follow.SetText(get_text_by_id(15817) if is_follow else get_text_by_id(15818))
        if not is_follow:
            self.panel.btn_follow.SetTextColor('#SW', '#SW', '#SW')
            self.panel.btn_follow.SetSelect(True)
        else:
            self.panel.btn_follow.SetTextColor(16770607, 16770607, 16770607)
            self.panel.btn_follow.SetSelect(False)
        self.panel.btn_follow.img_follow_0.setVisible(not is_follow)
        self.panel.btn_follow.img_follow_1.setVisible(is_follow)
        support_follow = LivePlatformManager().get_cur_platform().is_support_follow_anchor()
        self.panel.btn_follow.setVisible(support_follow)
        return

    def platform_update_follow_show(self, platform, follow_uid, is_follow):
        if platform == self._live_type:
            self.update_follow_show()

    def on_click_follow_btn(self, btn, touch):
        follow_uid = self._live_data.get('follow_uid')
        if not follow_uid:
            return
        from logic.vscene.part_sys.live.LivePlatformManager import LivePlatformManager
        is_follow = LivePlatformManager().get_cur_platform().check_is_anchor_followed(follow_uid)
        if is_follow:
            from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2

            def follow_func():
                LivePlatformManager().require_unfollow_anchor(self._live_type, follow_uid)

            SecondConfirmDlg2().confirm(content=15850, confirm_callback=follow_func)
        elif not LivePlatformManager().check_is_follow_list_full(self._live_type):
            LivePlatformManager().require_follow_anchor(self._live_type, follow_uid, self._live_data)
        else:
            global_data.game_mgr.show_tip(get_text_by_id(15854))

    def init_status(self):
        self.is_wifi = False
        import game3d
        from common.platform.device_info import DeviceInfo

        def update_status():
            device_info = DeviceInfo.get_instance()
            net_work_status = device_info.get_network()
            platform = game3d.get_platform()
            if platform in (game3d.PLATFORM_ANDROID, game3d.PLATFORM_IOS):
                is_wifi = net_work_status == 'wifi'
                if is_wifi != self.is_wifi:
                    if not is_wifi:

                        def cancel_callback():
                            self.close()

                        from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
                        SecondConfirmDlg2().confirm(content=get_text_by_id(2165), confirm_text=get_text_by_id(2166), cancel_text=get_text_by_id(2176), cancel_callback=cancel_callback)
                    self.is_wifi = is_wifi
            else:
                self.is_wifi = True

        from common.utils.timer import CLOCK
        tm = global_data.game_mgr.get_logic_timer()
        self.status_timer = tm.register(func=update_status, interval=1, times=-1, mode=CLOCK)
        update_status()

    def check_spr_shader(self, sp):
        import cclive
        if game3d.get_platform() == game3d.PLATFORM_ANDROID and self._player is not None and cclive.support_hardware_decoder():
            from logic.comsys.effect.ui_effect import create_shader
            gl_yuv = create_shader('yuv_texture', 'yuv_texture')
            program_yuv = cc.GLProgramState.getOrCreateWithGLProgram(gl_yuv)
            sp.setGLProgramState(program_yuv)
        return

    def receive_live_room_data(self, live_type, live_data):
        print('receive_live_room_data', live_data.get('uid'), self._in_request_room_uid)
        if str(live_data.get('uid')) == str(self._in_request_room_uid):
            islive = live_data.get('islive', True)
            print('islive', islive)
            if not islive:
                global_data.game_mgr.show_tip(get_text_by_id(2167))
                self.on_live_offline()
            else:
                self.set_play_data(live_type, live_data)

    def on_click_fuchuang_btn(self, btn, touch):
        self.scale_to_floating_windows(True)

    def scale_to_floating_windows(self, is_floating):
        if is_floating:
            if not self._float_nd:
                self._float_nd = global_data.uisystem.load_template_create('live/i_live_fuchuang', self.panel.nd_float)
                from logic.comsys.live.LiveFloatingWidget import LiveFloatingWidget
                self._liveFloatingWidget = LiveFloatingWidget(self, self._float_nd)
                self._liveFloatingWidget.setup_anchor_data(self._live_type, self._live_data)
            self.is_in_float = True
            self.panel.nd_float.setVisible(True)
            self.panel.nd_top.setVisible(False)
            self.panel.nd_bottom.setVisible(False)
            self.panel.layer_big_bg.setVisible(False)
            self.panel.touch_layer.setVisible(False)
            self.panel.img_small_bg.setVisible(True)
            self.panel.nd_show.setContentSize(self._float_nd.getContentSize())
            self.panel.nd_show.ChildRecursionRePosition()
            self._float_nd.img_bg.setOpacity(0)
            self._liveFloatingWidget.refresh_danmu_show()
            self._liveFloatingWidget.switch_danmu_to_float(True)
            self.set_anim_node_color(7829367)
        else:
            if self._float_nd:
                self.panel.nd_float.setVisible(False)
            self.is_in_float = False
            self.panel.nd_top.setVisible(True)
            self.panel.nd_bottom.setVisible(True)
            self.panel.layer_big_bg.setVisible(True)
            self.panel.img_small_bg.setVisible(False)
            self.panel.touch_layer.setVisible(True)
            self.panel.nd_show.SetContentSize('100%', '100%')
            self.panel.nd_show.ChildRecursionRePosition()
            self.set_anim_node_color('#SW')
            self.panel.nd_move.SetPosition('50%', '50%')
            if self._liveFloatingWidget:
                self._liveFloatingWidget.switch_danmu_to_float(False)
        self.check_spr_pos_size()

    def refresh_float_show(self):
        if self._liveFloatingWidget:
            self._liveFloatingWidget.setup_anchor_data(self._live_type, self._live_data)

    def on_resolution_changed(self):
        self.refresh_vbr_mode_list_show()
        self.scale_to_floating_windows(self.is_in_float)

    def on_attach_input(self):
        self.panel.stopActionByTag(69)
        self._is_in_input = True

    def on_detach_input(self):
        self._is_in_input = False

    def set_anim_node_color(self, color):
        nd_list = [
         self.panel.nd_connecting, self.panel.nd_off_line]
        for nd in nd_list:
            self.SetColorRecursion(nd, color)

    def SetColorRecursion(self, nd, color):
        nd.SetColor(color)
        for child in nd.GetChildren():
            self.SetColorRecursion(child, color)