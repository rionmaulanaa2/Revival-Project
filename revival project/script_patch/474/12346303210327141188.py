# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/share/KaixueComicShareCreator.py
from __future__ import absolute_import
from logic.comsys.share.ShareTemplateBase import ShareTemplateBase, async_disable_wrapper
from logic.gutils import task_utils
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no
head_pic_pre = 'gui/ui_res_2/item/role_head/{}.png'

class KaixueComicShareCreator(ShareTemplateBase):
    KIND = 'I_SHARE_KAIXUE_COMIC_SHARE'

    def get_ui_bg_sprite(self):
        return self.panel.nd_bg.img_bg

    def update_ui_bg_sprite(self):
        from common.utils.ui_utils import get_scale
        scale = get_scale('1w')
        self.panel.setScale(scale)
        self.panel.setContentSize(global_data.ui_mgr.design_screen_size)
        self.panel.ChildResizeAndPosition()
        self.panel.nd_bg.img_bg.SetPosition('50%', '50%')
        bg_scale = global_data.ui_mgr.design_screen_size.width / self.panel.nd_bg.img_bg.getContentSize().width
        self.panel.nd_bg.img_bg.setScale(bg_scale)

    def set_share_content(self, book_pic, conversation, btn_text, is_shared, item_pic, idx):
        self.panel.temp_comic.temp_book_01.btn_book.nd_comic.img_comic.SetDisplayFrameByPath('', book_pic)
        self.panel.temp_comic.temp_book_02.btn_book.nd_comic.img_comic.SetDisplayFrameByPath('', book_pic)
        self.panel.temp_comic.temp_book_01.btn_book.nd_bookcover.lab_num_01.SetString('0%s' % (idx + 1))
        self.panel.temp_comic.temp_book_01.btn_book.nd_comic.nd_low.lab_num_02.SetString('0%s' % (idx + 1))
        self.panel.temp_comic.nd_middle.btn_share.SetText(btn_text)
        self.panel.temp_comic.nd_middle.btn_share.img_reward.setVisible(not is_shared)
        if not is_shared:
            text_offset = {'x': '50%24','y': '50%18'} if 1 else {'x': '50%','y': '50%18'}
            self.panel.temp_comic.nd_middle.btn_share.SetTextOffset(text_offset)
            is_shared or self.panel.temp_comic.nd_middle.btn_share.img_reward.SetDisplayFrameByPath('', item_pic)
        self.panel.temp_comic.nd_middle.nd_conversation_2.setVisible(False)
        self.panel.temp_comic.nd_middle.nd_conversation_3.setVisible(False)
        self.panel.temp_comic.nd_bg.vx_mask_03.setClippingEnabled(False)
        if len(conversation) == 2:
            nd_conversation = self.panel.temp_comic.nd_middle.nd_conversation_2
        else:
            nd_conversation = self.panel.temp_comic.nd_middle.nd_conversation_3
        nd_conversation.setVisible(True)
        for idx, one_record in enumerate(conversation):
            head_pic_no = one_record[0]
            msg = one_record[1]
            head_pic = head_pic_pre.format(head_pic_no)
            nd_role = getattr(nd_conversation, 'nd_role_0%s' % (idx + 1))
            nd_role.cut_head.img_head.SetDisplayFrameByPath('', head_pic)
            nd_role.lab_msg.SetString(msg)