# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/common_ui/CommonInfoMessage.py
from __future__ import absolute_import
from six.moves import range
from common.uisys.basepanel import BasePanel
from logic.gutils import item_utils
import cc
from common.const import uiconst

class CommonInfoMessage(BasePanel):
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    IGNORE_RESIZE_TYPE = frozenset()

    def on_init_panel(self, on_process_done=None):
        self._playing = False
        self._can_show_multiple_next = True
        self.on_process_done = on_process_done
        self.init_parameters()
        self.init_event()
        self.init_button_event()

    @property
    def playing(self):
        return self._playing

    @playing.setter
    def playing(self, val):
        self._playing = val
        if self._playing:
            self.add_show_count('ON_PLAYING')
        else:
            self.add_hide_count('ON_PLAYING')

    def init_parameters(self):
        self.playing = False
        self.message_sequence = []
        self.is_allow_multiple_show = False
        self._panel_map = {}
        self._ani_default_stay_time = 1
        self.content_txt_name = 'lab_1'

    def set_ani_default_stay_time(self, t):
        self._ani_default_stay_time = t

    def add_message(self, *args):
        self.message_sequence.append(args)
        self.process_next_message()

    def finish_cb(self):
        if self and self.is_valid():
            if not self.is_allow_multiple_show:
                self.playing = False
            if not self._panel_map:
                self.enable_multiple_show()
            self.process_next_message()

    def clear_message(self):
        self.panel.stopAllActions()
        self.message_sequence = []
        self.playing = False
        self.enable_multiple_show()

    def process_next_message(self):
        if self.playing and not self.can_show_next_in_multiple():
            return
        if len(self.message_sequence) > 0:
            message = self.message_sequence.pop(0)
            self.playing = True
            self.disable_multiple_show()
            self.process_one_message(message, self.finish_cb)
        elif not self.is_allow_multiple_show:
            self.playing = False
            if self.on_process_done:
                self.on_process_done()
        elif not self._panel_map:
            self.playing = False
            if self.on_process_done:
                self.on_process_done()

    def check_visible(self, relate_class_name):
        ui_inst = global_data.ui_mgr.get_ui(relate_class_name)
        if ui_inst:
            if ui_inst.panel and ui_inst.panel.isValid():
                ui_inst.add_associate_vis_ui(self.__class__.__name__)
        else:
            log_error('Should have relate_class_name created!', relate_class_name)

    def remove_visible(self, relate_class_name):
        ui_inst = global_data.ui_mgr.get_ui(relate_class_name)
        if ui_inst:
            if ui_inst.panel and ui_inst.panel.isValid():
                ui_inst.remove_associate_vis_ui(self.__class__.__name__)
        else:
            log_error('Should have relate_class_name created!', relate_class_name)

    def message_ani(self, finish_cb, node, set_num_info=None, set_num_list=None, in_ani='show', out_ani='disappear', extra_disappear_time=0, extra_disappear_func=None):
        in_time = node.GetAnimationMaxRunTime(in_ani)
        out_time = node.GetAnimationMaxRunTime(out_ani)
        num_ani = None
        if set_num_info:
            set_num_func, show_num, last_show_num, ext_message_func = set_num_info
            off_num = show_num - last_show_num
            lab_cnt = max(4 if int(abs(off_num)) > 4 else int(abs(off_num)), 0) + 1
            rate = 1.0 * off_num / lab_cnt
            num_ani = 'repeat%d' % lab_cnt
            for i in range(lab_cnt):
                index = i + 1
                lab = getattr(node, 'lab_2_%d' % index)
                if lab:
                    set_num_func(lab, last_show_num + int(i * rate))

            set_num_func(node.lab_2, int(show_num))
            if ext_message_func:
                ext_message_func(node)
        if set_num_list:
            set_num_func, num_list = set_num_list
            for i in range(len(num_list)):
                index = i + 1
                lab = getattr(node, 'lab_value_%d' % index)
                set_num_func(lab, num_list[i])

        def fb():
            node.stopAllActions()
            if self and self.is_valid():
                if not self.is_allow_multiple_show:
                    self.add_hide_count(self.__class__.__name__)
                finish_cb()

        def run_end_ac():
            if not extra_disappear_time or not extra_disappear_func:
                end_ac_list = [cc.CallFunc.create(lambda : node.PlayAnimation(out_ani)),
                 cc.DelayTime.create(out_time),
                 cc.CallFunc.create(fb)]
            else:
                end_ac_list = [cc.CallFunc.create(lambda : node.PlayAnimation(out_ani)),
                 cc.DelayTime.create(out_time + 0.01),
                 cc.CallFunc.create(lambda : extra_disappear_func(node)),
                 cc.DelayTime.create(extra_disappear_time),
                 cc.CallFunc.create(fb)]
            node.stopAllActions()
            node.runAction(cc.Sequence.create(end_ac_list))

        def check_end(pass_time):
            if not self.is_allow_multiple_show:
                if not self.is_last_message():
                    run_end_ac()
            elif self._can_show_multiple_next:
                if len(self.message_sequence) > 0:
                    self.yield_main_node_pos(node)
                    self.process_next_message()

        ac_list = []
        if set_num_info:
            if num_ani:
                ac_list.append(cc.CallFunc.create(lambda : node.PlayAnimation(num_ani)))
        com_ac_list = [cc.CallFunc.create(lambda : node.PlayAnimation(in_ani)),
         cc.CallFunc.create(lambda : self.add_show_count(self.__class__.__name__)),
         cc.DelayTime.create(in_time),
         cc.CallFunc.create(self.enable_multiple_show),
         cc.CallFunc.create(lambda : node.TimerAction(check_end, self._ani_default_stay_time, callback=run_end_ac))]
        ac_list.extend(com_ac_list)
        node.stopAllActions()
        node.runAction(cc.Sequence.create(ac_list))
        return

    def reset_panel_size_and_position(self, node):
        txt_nd = getattr(node, self.content_txt_name)
        if not txt_nd:
            return
        if txt_nd.__class__.__name__ == 'CCRichText':
            txt_nd.formatText()
        if txt_nd.getTextContentSize:
            t_w = txt_nd.getTextContentSize().width
        else:
            t_w, _ = txt_nd.GetContentSize()
        if node.nd_locate:
            _, h = node.nd_locate.GetContentSize()
            node.nd_locate.SetContentSize(t_w, h)
            node.nd_locate.ResetSizeAndPositionWithChildrenUnsafe(include_self=False)

    def set_content_txt(self, node, txt, content_type=None):
        txt_nd = getattr(node, self.content_txt_name)
        if not txt_nd:
            return
        txt_nd.SetString(txt)
        self.reset_panel_size_and_position(node)

    def set_icon(self, node, item_id):
        if item_id:
            icon_path = item_utils.get_item_pic_by_item_no(item_id)
            if icon_path:
                node.icon.SetDisplayFrameByPath('', icon_path)

    def set_icon_path(self, node, icon_path):
        if icon_path:
            node.icon.setVisible(True)
            node.icon.SetDisplayFrameByPath('', icon_path)

    def set_icon2_path(self, node, icon_path):
        if icon_path:
            node.icon2.setVisible(True)
            node.icon2.SetDisplayFrameByPath('', icon_path)

    def set_bar_path(self, node, icon_path):
        if icon_path:
            node.bar.SetDisplayFrameByPath('', icon_path)

    def set_bar_module_path(self, node, bar_module_path):
        if bar_module_path:
            node.bar_module.setVisible(True)
            node.bar_module.SetDisplayFrameByPath('', bar_module_path)

    def set_icon_module_path(self, node, icon_module_path):
        if icon_module_path:
            node.bar_module.setVisible(True)
            node.icon_module.SetDisplayFrameByPath('', icon_module_path)

    def set_lab_title1_txt(self, node, txt):
        if txt:
            node.lab_title.SetString(txt)

    def set_lab_title2_txt(self, node, txt):
        if txt:
            node.lab_title2.SetString(txt)

    def set_msg_voice(self, node, voice_dict):
        if voice_dict:
            tag = voice_dict.get('tag', None)
            if tag:
                global_data.sound_mgr.post_event_2d_non_opt(tag, None)
        return

    def set_panel_attr(self, panel, set_attr_dict):
        if type(set_attr_dict) is list:
            for info in set_attr_dict:
                self.set_panel_one_attr(panel, info)

        else:
            self.set_panel_one_attr(panel, set_attr_dict)

    def set_panel_self_attr(self, panel, set_attr_dict):
        func_name = set_attr_dict.get('func_name')
        args = set_attr_dict.get('args', ())
        if func_name:
            func = getattr(panel, func_name)
            func and func(*args)

    def set_panel_one_attr(self, panel, set_attr_dict):
        node_name = set_attr_dict.get('node_name')
        func_name = set_attr_dict.get('func_name')
        args = set_attr_dict.get('args', ())
        if not node_name:
            return
        node = getattr(panel, node_name)
        if not node:
            return
        if func_name:
            func = getattr(node, func_name)
            func and func(*args)

    def hide_panel_nodes(self, panel, hide_nodes):
        for node_name in hide_nodes:
            node = getattr(panel, node_name)
            if not node:
                continue
            node.setVisible(False)

    def set_panel_map(self, key, val):
        if not val:
            if key in self._panel_map:
                del self._panel_map[key]
        else:
            self._panel_map[key] = val

    def init_button_event(self):
        if hasattr(self.panel, 'bg_layer') and self.panel.bg_layer:

            @self.panel.bg_layer.callback()
            def OnClick(btn, touch):
                self.on_click_bg_layer(btn, touch)

    def on_click_bg_layer(self, btn, touch):
        self.up.setVisible(False)
        self.playing = False
        self.process_next_message()

    def get_panel_var_name(self):
        if self.is_allow_multiple_show:
            return self.get_multiply_show_ani_index()
        else:
            return 'cur_panel'

    def get_multiply_show_ani_index(self):
        pattern = 'cur_panel_%d'
        for i in range(1, 10):
            name = pattern % i
            if name not in self._panel_map:
                return name

        log_error('get_multiply_show_ani_index: too many pattern exist at the same time!!!', self._panel_map)
        return 'cur_panel'

    def can_show_next_in_multiple(self):
        if not self.is_allow_multiple_show:
            return True
        return self._can_show_multiple_next

    def enable_multiple_show(self):
        if self.is_allow_multiple_show:
            self._can_show_multiple_next = True

    def disable_multiple_show(self):
        if self.is_allow_multiple_show:
            self._can_show_multiple_next = False

    def on_finalize_panel(self):
        pass

    def init_event(self):
        pass

    def is_last_message(self):
        pass

    def process_one_message(self, message, finish_cb):
        pass

    def main_process_one_message(self, message, finish_cb):
        pass

    def custom_refresh(self, node, content_type, msg_dict):
        pass

    def yield_main_node_pos(self, node):
        pass