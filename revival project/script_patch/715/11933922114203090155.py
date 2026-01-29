# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/BattleInfoMessage.py
from __future__ import absolute_import
from logic.comsys.common_ui import CommonInfoUtils
from logic.gcommon.common_const import battle_const
from common.const.uiconst import BATTLE_MESSAGE_ZORDER, UI_TYPE_MESSAGE
from logic.gutils import role_head_utils
from logic.comsys.common_ui.CommonInfoMessage import CommonInfoMessage
import time

class BattleInfoMessage(CommonInfoMessage):
    DLG_ZORDER = BATTLE_MESSAGE_ZORDER
    IGNORE_RESIZE_TYPE = set()

    def on_init_panel(self, on_process_done=None):
        self.message_show_time = {}
        super(BattleInfoMessage, self).on_init_panel(on_process_done)
        self.check_visible('BattleInfoMessageVisibleUI')

    def is_last_message(self):
        ui = global_data.ui_mgr.get_ui('BattleInfoUI')
        if ui:
            return len(ui._main_message_queue) == 0
        return True

    def __refresh_other_mvp_info(self, panel, other_mvp_info):
        head_id = other_mvp_info.get('head')
        msg = other_mvp_info.get('msg')
        panel.lab_1.SetString(msg)
        res_path = role_head_utils.get_head_photo_res_path(head_id)
        panel.icon.img_head.SetDisplayFrameByPath('', res_path)
        panel.lab_1.formatText()
        t_w = panel.lab_1.getTextContentSize().width
        _, h = panel.nd_locate.GetContentSize()
        panel.nd_locate.SetContentSize(t_w, h)
        panel.nd_locate.ResizeAndPosition(include_self=False)

    def _init_msg_ui(self, ui):
        pass

    def main_process_one_message(self, message, finish_cb):
        msg_dict = message[0]
        i_type = msg_dict.get('i_type')
        interval_time = msg_dict.get('interval_time', 0)
        self.content_txt_name = msg_dict.get('content_txt_name', 'lab_1')
        if interval_time > 0:
            cur_time = time.time()
            if i_type not in self.message_show_time:
                self.message_show_time[i_type] = 0
            if cur_time - self.message_show_time[i_type] < interval_time:
                finish_cb()
                return
            self.message_show_time[i_type] = cur_time
        panel_var_name = self.get_panel_var_name()
        cur_panel = self._panel_map.get(panel_var_name, None)
        if cur_panel and cur_panel.isValid():
            CommonInfoUtils.destroy_ui(cur_panel)
        self.set_panel_map(panel_var_name, None)
        b_resize = msg_dict.get('b_resize', False)
        cur_panel = CommonInfoUtils.create_ui(i_type, self.panel.nd_tips, resize=b_resize)
        self.set_panel_map(panel_var_name, cur_panel)
        if not cur_panel:
            finish_cb()
            return
        else:
            self._init_msg_ui(cur_panel)
            content_func_name = msg_dict.get('set_content_func')
            if content_func_name:
                content_func = getattr(CommonInfoUtils, content_func_name, None)
                if content_func:
                    content_args = msg_dict.get('content_args', ())
                    content_func(cur_panel, *content_args)
            num_func_name = msg_dict.get('set_num_func')
            if num_func_name:
                set_num_func = getattr(CommonInfoUtils, num_func_name, CommonInfoUtils.set_show_num)
            else:
                set_num_func = CommonInfoUtils.set_show_num
            if i_type not in self.IGNORE_RESIZE_TYPE:
                self.reset_panel_size_and_position(cur_panel)
            content_txt = msg_dict.get('content_txt')
            content_txt and self.set_content_txt(cur_panel, content_txt, i_type)
            item_id = msg_dict.get('item_id')
            item_id and self.set_icon(cur_panel, item_id)
            icon_path = msg_dict.get('icon_path')
            icon_path and self.set_icon_path(cur_panel, icon_path)
            icon_path2 = msg_dict.get('icon_path2')
            icon_path2 and self.set_icon2_path(cur_panel, icon_path2)
            bar_path = msg_dict.get('bar_path')
            bar_path and self.set_bar_path(cur_panel, bar_path)
            bar_module_path = msg_dict.get('bar_module_path', None)
            bar_module_path and self.set_bar_module_path(cur_panel, bar_module_path)
            icon_module_path = msg_dict.get('icon_module_path', None)
            icon_module_path and self.set_icon_module_path(cur_panel, icon_module_path)
            set_attr_dict = msg_dict.get('set_attr_dict')
            set_attr_dict and self.set_panel_attr(cur_panel, set_attr_dict)
            hide_nodes = msg_dict.get('hide_nodes', [])
            hide_nodes and self.hide_panel_nodes(cur_panel, hide_nodes)
            other_mvp_info = msg_dict.get('other_mvp_info', {})
            other_mvp_info and self.__refresh_other_mvp_info(cur_panel, other_mvp_info)
            panel_self_attr_dict = msg_dict.get('panel_self_attr_dict', None)
            panel_self_attr_dict and self.set_panel_self_attr(cur_panel, panel_self_attr_dict)
            lab_title1_txt = msg_dict.get('lab_title', None)
            lab_title1_txt and self.set_lab_title1_txt(cur_panel, lab_title1_txt)
            lab_title2_txt = msg_dict.get('lab_title2', None)
            lab_title2_txt and self.set_lab_title2_txt(cur_panel, lab_title2_txt)
            voice_dict = msg_dict.get('voice_dict', None)
            voice_dict and self.set_msg_voice(cur_panel, voice_dict)
            self.custom_refresh(cur_panel, i_type, msg_dict)
            show_num = msg_dict.get('show_num')
            if show_num:
                last_show_num = msg_dict.get('last_show_num', 0)
                ext_message_func = msg_dict.get('ext_message_func', None)
                set_num_info = (set_num_func, show_num, last_show_num, ext_message_func)
            else:
                set_num_info = None
            num_list = msg_dict.get('num_list')
            if num_list:
                set_num_list = (
                 set_num_func, num_list)
            else:
                set_num_list = None

            def finish_cd_wrapper(panel_var_name=panel_var_name):
                cur_panel = self._panel_map.get(panel_var_name, None)
                if cur_panel and cur_panel.isValid():
                    CommonInfoUtils.destroy_ui(cur_panel)
                self.set_panel_map(panel_var_name, None)
                finish_cb()
                return

            kw = {'extra_disappear_time': msg_dict.get('extra_disappear_time', None),
               'extra_disappear_func': msg_dict.get('extra_disappear_func', None)
               }
            in_anim = msg_dict.get('in_anim', -1)
            if in_anim != -1:
                kw['in_ani'] = in_anim
            out_anim = msg_dict.get('out_anim', -1)
            if out_anim != -1:
                kw['out_ani'] = out_anim
            self.message_ani(finish_cd_wrapper, cur_panel, set_num_info, set_num_list, **kw)
            is_binding = CommonInfoUtils.VISIBLE_SPECIAL_SETTING.get(i_type, True)
            if is_binding:
                self.check_visible('BattleInfoMessageVisibleUI')
            else:
                self.remove_visible('BattleInfoMessageVisibleUI')
            return