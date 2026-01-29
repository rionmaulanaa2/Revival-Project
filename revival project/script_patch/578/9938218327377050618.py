# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/mecha_display/MechaStoryWidget.py
from __future__ import absolute_import
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.cfg import confmgr
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no, get_lobby_item_rare_degree_pic_by_item_no, get_lobby_item_name, get_lobby_item_desc, update_item_status, jump_to_ui
from logic.gcommon.item import item_const
from logic.gutils.template_utils import init_common_item_head, init_tempate_mall_i_item
from common.utils.timer import CLOCK
from logic.gutils.mall_utils import mecha_has_owned_by_mecha_id
from common.framework import Functor
from logic.comsys.common_ui.ScaleableHorzContainer import ScaleableHorzContainer
from logic.comsys.mecha_display.ExDescibeWidget import ExDescibeWidget
from logic.gutils import mecha_skin_utils
from common.uisys.BaseUIWidget import BaseUIWidget
from logic.gutils import dress_utils
import cc

class MechaStoryWidget(BaseUIWidget):

    def __init__(self, parent, panel, mecha_type):
        super(MechaStoryWidget, self).__init__(parent, panel)
        self._mecha_conf = confmgr.get('mecha_display', 'HangarConfig', 'Content')
        self._story_conf = confmgr.get('mecha_display', 'MechaStory', 'Content')
        self.on_switch_to_mecha_type(mecha_type)

    def destroy(self):
        super(MechaStoryWidget, self).destroy()
        self._mecha_conf = {}
        self._story_conf = {}

    def on_switch_to_mecha_type(self, mecha_type):
        cur_clothing_id = self.parent.cur_clothing_id
        is_normal = True
        if str(cur_clothing_id) in self._story_conf:
            self.panel.nd_normal.setVisible(False)
            self.panel.nd_sp.setVisible(True)
            is_normal = False
        else:
            self.panel.nd_normal.setVisible(True)
            self.panel.nd_sp.setVisible(False)
        stroy_text = self._mecha_conf[str(mecha_type)].get('story_mecha_text_id')
        if is_normal:
            self.panel.nd_content_normal.SetInitCount(1)
            ui_item = self.panel.nd_content_normal.GetItem(0)
            ui_item.lab_content.SetString(stroy_text)
            ui_item.lab_content.formatText()
            sz = ui_item.lab_content.getTextContentSize()
            sz.height += 90
            old_sz = ui_item.getContentSize()
            ui_item.setContentSize(cc.Size(old_sz.width, sz.height))
            ui_item.RecursionReConfPosition()
            old_inner_size = self.panel.nd_content_normal.GetInnerContentSize()
            self.panel.nd_content_normal.SetInnerContentSize(old_inner_size.width, sz.height)
            self.panel.nd_content_normal.GetContainer()._refreshItemPos()
            self.panel.nd_content_normal._refreshItemPos()
        else:
            self.panel.nd_content_sp.SetInitCount(1)
            ui_item = self.panel.nd_content_sp.GetItem(0)
            ui_item.lab_content.SetString(stroy_text)
            cur_conf = self._story_conf[str(cur_clothing_id)]
            name_text = cur_conf.get('clothing_text_id')
            self.panel.lab_name.SetString(name_text)
            skin_text = cur_conf.get('story_clothing_text_id')
            self.panel.nd_content.SetInitCount(1)
            ui_item = self.panel.nd_content.GetItem(0)
            ui_item.lab_content.SetString(skin_text)
            img_path = cur_conf.get('img_path')
            self.panel.img_skin.SetDisplayFrameByPath('', img_path)
            img_pos = cur_conf.get('img_pos')
            self.panel.img_skin.SetPosition(img_pos[0], img_pos[1])
            img_scl = cur_conf.get('img_scl')
            self.panel.img_skin.setScale(img_scl[0], img_scl[1])