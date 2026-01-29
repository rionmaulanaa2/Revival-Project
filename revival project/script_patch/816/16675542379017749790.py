# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityNews.py
from __future__ import absolute_import
from six.moves import range
import math
from common.cfg import confmgr
from logic.gcommon import time_utility
from logic.gutils.activity_utils import is_news_finished, is_news_enable
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gcommon.time_utility import ONE_WEEK_SECONDS
from logic.gcommon.common_utils.local_text import get_cur_text_lang, get_pic_lang_path_by_lang
import C_file

class ActivityNews(ActivityBase):
    APPEAR_ANIM = 'appear'

    def __init__(self, dlg, activity_type):
        super(ActivityNews, self).__init__(dlg, activity_type)
        self.init_data()
        self.init_panel()

    def init_data(self):
        ui_data = confmgr.get('c_activity_config', self._activity_type, 'cUiData')
        self.big_news_id_lst = self.check_category(ui_data.get('big_news_id', []))
        self.small_news_id_lst = self.check_category(ui_data.get('small_news_id', []))
        self._clicking_btn = None
        begin_date = time_utility.time_str_to_datetime(ui_data.get('begin_date'), '%Y/%m/%d-%H:%M')
        now = time_utility.get_utc8_datetime()
        if now <= begin_date:
            week_cnt = 1
        else:
            week_cnt = (now - begin_date).total_seconds() / ONE_WEEK_SECONDS
            week_cnt = int(math.ceil(week_cnt))
        week_text = get_text_by_id(606094).format(week_cnt)
        self.panel.lab_num.setString(week_text)
        return

    def check_category(self, ids):
        is_pc = global_data.is_pc_mode
        news_conf = confmgr.get('activity_news_config')
        valid_ids = []
        for news_id in ids:
            news_c = news_conf.get(str(news_id))
            if is_pc and news_c.get('category') == 'PC_DISABLE':
                continue
            valid_ids.append(news_id)

        return valid_ids

    def _init_replace_big_news_helper(self, i, yes, replace_json_name, temp_override_info_out):
        if not isinstance(temp_override_info_out, dict):
            return
        if yes:
            while True:
                node_name = 'temp_' + str(i)
                replace_ccb_file_relpath_wo_ext = 'activity/activity_news/' + replace_json_name
                if C_file.find_res_file('gui/template/' + replace_ccb_file_relpath_wo_ext + '.json', '') > 0:
                    temp_override_info_out[node_name] = {'ccbFile': replace_ccb_file_relpath_wo_ext}
                break

    def init_panel(self):
        candidates = [
         1, 2]
        temp_override_info = {}
        sp_news_id_set = set()
        for i in candidates:
            from logic.gutils.jump_to_ui_utils import is_activity_big_news_sp
            yes, replace_json_name = is_activity_big_news_sp(i)
            self._init_replace_big_news_helper(i, yes, replace_json_name, temp_override_info)
            if yes:
                news_id = str(i)
                sp_news_id_set.add(news_id)

        if temp_override_info:
            temp_path = self.panel.nd_content.list_all.GetTemplatePath()
            self.panel.nd_content.list_all.SetTemplate(temp_path, temp_override_info)
        self.panel.nd_content.list_all.SetInitCount(1)
        list_news = self.panel.nd_content.list_all.GetItem(0)
        for idx, news_id in enumerate(self.big_news_id_lst):
            jump_logic_info = self._get_info(news_id, 'jump_logic')
            ui_item = getattr(list_news, 'temp_%s' % (idx + 1))
            self._init_item_jump(ui_item, jump_logic_info)
            if news_id in sp_news_id_set:
                txts_key = 'big_news_txts_sp'
            else:
                txts_key = 'big_news_texts'
            big_news_text_ids = self._get_info(news_id, txts_key)
            if isinstance(big_news_text_ids, list):
                text_leng = len(big_news_text_ids)
                lab_title = getattr(ui_item, 'lab_title')
                if lab_title and text_leng > 0:
                    lab_title.SetString(big_news_text_ids[0])
                scroll_details = getattr(ui_item, 'scroll_details')
                if scroll_details:
                    node_details = scroll_details.GetItem(0)
                    if node_details:
                        lab_details = getattr(node_details, 'lab_details')
                        if lab_details and text_leng > 1:
                            lab_details.SetString(big_news_text_ids[1])
                lab_new = getattr(ui_item, 'lab_new')
                if lab_new and text_leng > 2:
                    lab_new.SetString(big_news_text_ids[2])
            for i in range(ui_item.scroll_details.GetItemCount()):
                _item = ui_item.scroll_details.GetItem(i)
                w, _ = _item.GetContentSize()
                _, h = _item.lab_details.nd_auto_fit.GetContentSize()
                _item.SetContentSize(w, h)
                _item.ChildRecursionRePosition()

            ui_item.scroll_details.RefreshItemPos()

        list_news_small = list_news.list_small
        valid_news_id = []
        for idx, news_id in enumerate(self.small_news_id_lst):
            if is_news_finished(news_id):
                continue
            if not is_news_enable(news_id):
                continue
            valid_news_id.append(news_id)

        list_news_small.SetInitCount(len(valid_news_id))
        for idx, news_id in enumerate(valid_news_id):
            ui_item = list_news_small.GetItem(idx)
            jump_logic_info = self._get_info(news_id, 'jump_logic')
            desc_id = self._get_info(news_id, 'desc_id')
            pic_path = self._get_info(news_id, 'pic_path')
            ui_item.nd_all.lab_title.SetString(desc_id)
            ui_item.nd_all.img_banner.SetDisplayFrameByPath('', pic_path)
            self._init_item_jump(ui_item, jump_logic_info)

        def OnScrollToLeft(*args):
            self.panel.img_left.setVisible(False)

        def OnScrolling(*args):
            self.panel.img_left.setVisible(True)
            self.panel.img_right.setVisible(True)

        def OnScrollToRight(*args):
            self.panel.img_right.setVisible(False)

        self.panel.nd_content.list_all.OnScrolling = OnScrolling
        self.panel.nd_content.list_all.OnScrollToLeft = OnScrollToLeft
        self.panel.nd_content.list_all.OnScrollToRight = OnScrollToRight

    def _get_info(self, news_id, attr):
        news_conf = confmgr.get('activity_news_config', news_id)
        jump_logic_info = news_conf.get(attr, None)
        return jump_logic_info

    def _init_item_jump(self, item, info):
        if not info:
            return

        @item.callback()
        def OnClick(btn, touch, jump_info=info):
            from logic.gutils import jump_to_ui_utils
            func_name = jump_info.get('func')
            args = jump_info.get('args', [])
            kargs = jump_info.get('kargs', {})
            if func_name:
                func = getattr(jump_to_ui_utils, func_name)
                func and func(*args, **kargs)
            self._clicking_btn = None
            return True

        @item.callback()
        def OnCancel(btn, touch):
            self._clicking_btn = None
            return True

        @item.callback()
        def OnBegin(btn, touch):
            if self._clicking_btn:
                return False
            self._clicking_btn = btn
            return True

    def set_show(self, show, is_init=False):
        super(ActivityNews, self).set_show(show)
        self.panel.PlayAnimation(self.APPEAR_ANIM)
        self.panel.PlayAnimation('light')
        self.panel.nd_content.list_all.GetItem(0).PlayAnimation('appear')