# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/SpringFestival/SpringCardUI.py
from __future__ import absolute_import
from six.moves import range
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_1
import cc
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no, get_lobby_item_desc
from common.const import uiconst
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
from logic.comsys.common_ui.InputBox import InputBox
from logic.client.const.share_const import TYPE_IMAGE
from logic.gutils.share_utils import ShareHelper

class SpringCardUI(WindowMediumBase):
    PANEL_CONFIG_NAME = 'activity/activity_202101/activity_journal_card'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE
    UI_ACTION_EVENT = {'nd_change_page.OnBegin': 'on_begin_change_page',
       'nd_change_page.OnEnd': 'on_end_change_page'
       }
    TEMPLATE_NODE_NAME = 'temp_sendcard'

    def on_init_panel(self):
        super(SpringCardUI, self).on_init_panel()
        self._cur_sel_postmark = None
        self._share_content = None
        self._cur_postmark_item = None
        self.init_input_box()
        self._share_helper = ShareHelper()
        self.init_share_list()
        self.init_temp_card()
        return

    def on_finalize_panel(self):
        self.destroy_widget('_share_content')
        self.destroy_widget('input_box')
        self.destroy_widget('_share_helper')

    def set_card_list(self, card_list):
        self._card_list = card_list

    def set_card_index(self, index):
        self._card_index = index
        if index < len(self._card_list):
            card = self._card_list[index]
            card_pic = card.get('pic', '')
            card_pic = card_pic.replace('_small_0', '_big')
            self.panel.temp_card.img_postcard.SetDisplayFrameByPath('', card_pic)
        self.panel.lab_page.SetString('%d/%d' % (self._card_index + 1, len(self._card_list)))

    def set_postmark_list(self, ls):
        self._postmark_list = ls
        self.init_list()

    def init_input_box(self):
        max_length = 50

        def detach_callback(text=None):
            is_input = text is not None
            if self.check_input_words(is_input):
                self.set_card_wish(self.input_box.get_text())
            return

        import game3d
        self.input_box = InputBox(self.panel.temp_input, max_length=max_length, placeholder=get_text_by_id(601121), input_callback=detach_callback, detach_callback=detach_callback)
        self.input_box.set_rise_widget(self.panel)
        return

    def init_share_list(self):
        from logic.gutils.share_utils import init_platform_list, share_url

        def share_card(share_args):
            platform = share_args.get('platform_enum', None)
            self.update_share_content()
            if self._share_helper:

                def share_inform_cb():
                    if global_data.player:
                        global_data.player.share_activity('activity_10108')

                rt = self._share_content.get_render_texture()

                def cb():
                    if rt and rt.isValid():
                        self._share_helper.share_by_render_texture(rt, platform, share_inform_cb)

                self.panel.SetTimeOut(0.1, cb, tag=210202)
            return

        init_platform_list(self.panel.list_share_btn, share_card, share_type=TYPE_IMAGE)
        self.panel.btn_send.BindMethod('OnClick', self.on_click_btn_save)

    def on_click_btn_save(self, btn, touch):
        if not global_data.share_mgr:
            from logic.comsys.share.ShareManager import ShareManager
            ShareManager()
        self.update_share_content()
        rt = self._share_content.get_render_texture()

        def callback():
            if rt and rt.isValid():
                self._share_helper.save_render_texture_to_gallery(rt)

        self.panel.SetTimeOut(0.1, callback, tag=210127)

    def update_share_content(self):
        from logic.comsys.share.SpringActivityJournalShare import SpringActivityJournalShareCreator
        if not self._share_content:
            self._share_content = SpringActivityJournalShareCreator()
            self._share_content.create()
        pic_path = get_lobby_item_pic_by_item_no(self._cur_sel_postmark)
        card_pic = self.panel.temp_card.img_postcard.GetDisplayFramePath()
        self._share_content.set_wish_info(self.panel.temp_card.lab_wish.getString(), card_pic, pic_path)

    def check_input_words(self, is_input):
        from logic.gcommon.common_utils import text_utils
        text = self.input_box.get_text()
        if text.strip() == '' and not is_input:
            self.input_box.set_text(get_text_by_id(601121))
        check_code, review_pass, msg = text_utils.check_review_words_chat(text)
        if review_pass != text_utils.CHECK_WORDS_PASS:
            global_data.game_mgr.show_tip(get_text_by_id(11170), True)
            return False
        return True

    def show_transition(self, callback):
        self.panel.stopAllActions()
        action_list = []
        action_list.append(cc.CallFunc.create(lambda : self.panel.PlayAnimation('appear')))
        action_list.append(cc.CallFunc.create(self.show))
        duration = self.panel.GetAnimationMaxRunTime('appear')
        action_list.append(cc.DelayTime.create(duration / 2.0))
        if callback and callable(callback):
            action_list.append(cc.CallFunc.create(callback))
        action_list.append(cc.DelayTime.create(duration / 2.0))
        action_list.append(cc.CallFunc.create(self.hide))
        self.panel.runAction(cc.Sequence.create(action_list))

    def init_list(self):
        self.panel.list_postcard.SetInitCount(len(self._postmark_list))
        for i in range(0, len(self._postmark_list)):
            ui_item = self.panel.list_postcard.GetItem(i)
            if ui_item:
                self.init_template_item(ui_item, self._postmark_list[i])

        ui_item = self.panel.list_postcard.GetItem(0)
        ui_item.btn_choose.OnClick(None)
        return

    def init_template_item(self, ui_item, data):
        item_no = data

        @ui_item.btn_choose.callback()
        def OnClick(btn, touch):
            self._cur_sel_postmark = item_no
            self.set_postmark_btn_sel(self._cur_postmark_item, False)
            self._cur_postmark_item = ui_item
            self.set_postmark_btn_sel(ui_item, True)
            self.set_card_postmark(item_no)

        from logic.gutils import template_utils
        from logic.gcommon.item.item_const import RARE_DEGREE_0, RARE_DEGREE_1
        template_utils.init_tempate_mall_i_item(ui_item, item_no, show_tips=False, force_rare_degree=RARE_DEGREE_0)

    def set_postmark_btn_sel(self, ui_item, is_sel):
        if ui_item and ui_item.isValid():
            ui_item.btn_choose.SetSelect(is_sel)

    def set_card_postmark(self, item_no):
        pic_path = get_lobby_item_pic_by_item_no(item_no)
        self.panel.temp_card.img_postmark.SetDisplayFrameByPath('', pic_path)

    def set_card_wish(self, msg):
        from logic.gutils.live_utils import format_one_line_text_with_size_setted
        new_msg = format_one_line_text_with_size_setted(self.panel.temp_card.lab_wish, msg, self.panel.temp_card.nd_max_length.getContentSize().width)
        self.panel.temp_card.lab_wish.SetString(new_msg)

    def set_card_name(self, name):
        self.panel.temp_card.lab_name.SetString(name)

    def init_card_qr_code(self):
        from logic.gutils.share_utils import get_share_qr_code_pic_path
        qr_path = get_share_qr_code_pic_path()
        if qr_path:
            self.panel.temp_card.img_qr_bg.setVisible(True)
            self.panel.temp_card.img_qr_code.SetDisplayFrameByPath('', qr_path)
        else:
            self.panel.temp_card.img_qr_bg.setVisible(False)

    def on_begin_change_page(self, btn, touch):
        return True

    def on_end_change_page(self, btn, touch):
        from common.utils.ui_utils import get_scale
        s_pos = touch.getStartLocation()
        e_pos = touch.getLocation()
        e_pos.subtract(s_pos)
        lens = e_pos.getLength()
        if lens > get_scale('10w'):
            offset = 1 if e_pos.x < 0 else -1
            new_card_index = (self._card_index + offset) % len(self._card_list)
            self.set_card_index(new_card_index)

    def init_temp_card(self):
        self.set_card_name(global_data.player.get_name())
        self.set_card_wish(get_text_by_id(601121))
        from logic.gutils import role_head_utils
        pl = global_data.player
        role_head_utils.init_role_head(self.panel.temp_card.temp_head, pl.get_head_frame(), pl.get_head_photo())
        self.init_card_qr_code()