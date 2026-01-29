# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityKaixue/ComicBookUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_3, UI_VKB_CLOSE
from logic.gutils import task_utils
from common.cfg import confmgr
from logic.gcommon.common_const.activity_const import ACTIVITY_KAIXUE_KOTONOHA
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no
import cc
IMG_HEAD_PRE = 'gui/ui_res_2/item/role_head/{}.png'
IMG_BOOK_OPEN_PRE = 'gui/ui_res_2/activity/activity_202109/i_activity_term/book/'

class ComicBookUI(BasePanel):
    PANEL_CONFIG_NAME = 'activity/activity_202109/1_comic/i_term_share'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_3
    UI_VKB_TYPE = UI_VKB_CLOSE

    def on_init_panel(self, *args, **kwargs):
        self._idx = None
        self._task_id = None
        self._img_book = None
        self._conversation = None
        self._btn_text = None
        self._item_pic = None
        self.process_event(True)
        ac_list = [
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('show')),
         cc.DelayTime.create(1),
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('loop'))]
        self.panel.runAction(cc.Sequence.create(ac_list))

        @self.panel.nd_middle.btn_share.unique_callback()
        def OnClick(btn, touch):
            self.on_click_btn_share()

        @self.panel.nd_middle.btn_close.unique_callback()
        def OnClick(*args):
            self.on_click_btn_close()

        return

    def on_finalize_panel(self):
        self.process_event(False)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_reward_succ_event': self.update_btn_share
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def update_btn_share(self, task_id):
        is_shared = global_data.player.is_task_finished(task_id)
        if is_shared:
            btn_text = 907133 if 1 else 907134
            self._btn_text = btn_text
            self.panel.nd_middle.btn_share.SetText(btn_text)
            self.panel.nd_middle.btn_share.img_reward.setVisible(not is_shared)
            text_offset = is_shared or {'x': '50%24','y': '50%18'} if 1 else {'x': '50%','y': '50%18'}
            self.panel.nd_middle.btn_share.SetTextOffset(text_offset)
            reward_list = is_shared or task_utils.get_task_reward_list(task_id)
            for lobby_item_no, num in reward_list:
                item_pic = get_lobby_item_pic_by_item_no(lobby_item_no)
                self._item_pic = item_pic
                self.panel.nd_middle.btn_share.img_reward.SetDisplayFrameByPath('', item_pic)
                break

    def set_book_content(self, idx, task_id):
        self._idx = idx
        self._task_id = task_id
        ui_data = confmgr.get('c_activity_config', ACTIVITY_KAIXUE_KOTONOHA).get('cUiData')
        img_book = IMG_BOOK_OPEN_PRE + ui_data.get('img_book')[idx]
        conversation = ui_data.get('conversation')[idx]
        self._img_book = img_book
        self._conversation = conversation
        self.panel.nd_middle.nd_book.temp_book_01.btn_book.nd_comic.img_comic.SetDisplayFrameByPath('', img_book)
        self.panel.nd_middle.nd_book.temp_book_02.btn_book.nd_comic.img_comic.SetDisplayFrameByPath('', img_book)
        self.panel.nd_middle.nd_book.temp_book_01.btn_book.nd_bookcover.lab_num_01.SetString('0%s' % (idx + 1))
        self.panel.nd_middle.nd_book.temp_book_01.btn_book.nd_comic.nd_low.lab_num_02.SetString('0%s' % (idx + 1))
        self.update_btn_share(task_id)
        self.panel.nd_middle.nd_conversation_2.setVisible(False)
        self.panel.nd_middle.nd_conversation_3.setVisible(False)
        nd_conversation = self.panel.nd_middle.nd_conversation_2 if len(conversation) == 2 else self.panel.nd_middle.nd_conversation_3
        nd_conversation.setVisible(True)
        for idx, one_record in enumerate(conversation):
            head_pic_no = one_record[0]
            msg = one_record[1]
            head_pic = IMG_HEAD_PRE.format(head_pic_no)
            nd_role = getattr(nd_conversation, 'nd_role_0%s' % (idx + 1))
            nd_role.cut_head.img_head.SetDisplayFrameByPath('', head_pic)
            nd_role.lab_msg.SetString(msg)

    def on_click_btn_share(self):
        from logic.comsys.share.KaixueComicShareCreator import KaixueComicShareCreator
        share_creator = KaixueComicShareCreator()
        share_creator.create()
        share_creator.set_share_content(self._img_book, self._conversation, self._btn_text, global_data.player.is_task_finished(self._task_id), self._item_pic, self._idx)
        share_content = share_creator
        from logic.comsys.share.ShareUI import ShareUI
        ShareUI().set_share_content_raw(share_content.get_render_texture(), share_content=share_content)
        share_ui = global_data.ui_mgr.get_ui('ShareUI')
        if share_ui:
            share_ui.set_bg_color_visible(False)
        if global_data.is_pc_mode:
            global_data.player and global_data.player.share_activity('share_comic_%s' % (self._idx + 1))
            return
        if share_ui:

            def share_inform_func():
                player = global_data.player
                share_arg = 'share_comic_%s' % (self._idx + 1)
                player and player.share_activity(share_arg)

            share_ui.set_share_inform_func(share_inform_func)

    def on_click_btn_close(self):
        ac_list = [
         cc.CallFunc.create(lambda : self.panel.PlayAnimation('disappear')),
         cc.DelayTime.create(0.3),
         cc.CallFunc.create(self.on_click_btn_close_core)]
        self.panel.runAction(cc.Sequence.create(ac_list))

    def on_click_btn_close_core(self):
        self.close()
        global_data.emgr.comic_book_ui_close_event.emit(self._task_id)