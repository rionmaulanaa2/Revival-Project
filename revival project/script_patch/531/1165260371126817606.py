# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/intimacy/IntimacyOrderEdit.py
from __future__ import absolute_import
import six
from six.moves import range
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
from common.const.uiconst import NORMAL_LAYER_ZORDER
from logic.gcommon.const import INTIMACY_RELATION_TYPE_SET, INTIMACY_NAME_MAP
from logic.gutils.intimacy_utils import INTIMACY_PIC

class IntimacyOrderEdit(WindowMediumBase):
    PANEL_CONFIG_NAME = 'friend/intimacy_build_choose'
    TEMPLATE_NODE_NAME = 'temp_bg'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    MOUSE_CURSOR_TRIGGER_SHOW = True

    def on_init_panel(self, *args, **kwargs):
        super(IntimacyOrderEdit, self).on_init_panel(*args, **kwargs)
        self.template_node.lab_title.SetString(get_text_by_id(3236))
        self.panel.lab_describe.setVisible(True)
        self.panel.lab_describe.SetString(get_text_by_id(3235))

    def edit_order(self, confirm_callback=None):
        cur_order = global_data.player.intimacy_relation_order
        self.order_dict = {intimacy_type:idx for idx, intimacy_type in enumerate(cur_order)}
        self.type_2_item = {}
        self.cur_idx = len(self.order_dict)
        panel = self.panel
        panel.list_reward.SetInitCount(len(INTIMACY_RELATION_TYPE_SET))
        for idx, intimacy_type in enumerate(INTIMACY_RELATION_TYPE_SET):
            item = panel.list_reward.GetItem(idx)
            self.type_2_item[intimacy_type] = item
            item.lab_name.SetString(INTIMACY_NAME_MAP[intimacy_type])
            item.img_icon.SetDisplayFrameByPath('', INTIMACY_PIC[intimacy_type])
            item.lab_limit.SetString(str(self.order_dict[intimacy_type] + 1))

            @item.btn_choose.callback()
            def OnClick(btn, touch, intimacy_type=intimacy_type):
                self._cur_intimacy = intimacy_type
                cur_idx = self.order_dict[intimacy_type]
                if cur_idx is None:
                    self.order_dict[intimacy_type] = self.cur_idx
                    self.cur_idx += 1
                else:
                    for other_type in six.iterkeys(self.order_dict):
                        if other_type == intimacy_type:
                            self.order_dict[other_type] = None
                        elif self.order_dict[other_type] is not None and self.order_dict[other_type] > cur_idx:
                            self.order_dict[other_type] -= 1

                    self.cur_idx -= 1
                for i_type, item in six.iteritems(self.type_2_item):
                    idx = self.order_dict[i_type]
                    if idx is None:
                        item.lab_limit.setVisible(False)
                    else:
                        item.lab_limit.setVisible(True)
                        item.lab_limit.SetString(str(idx + 1))

                self.panel.btn_accept.btn_common_big.SetEnable(self.cur_idx == len(self.order_dict))
                return

        @panel.btn_accept.btn_common_big.callback()
        def OnClick(btn, touch):
            if callable(confirm_callback):
                order = [ None for i in range(len(self.order_dict)) ]
                for intimacy_type, idx in six.iteritems(self.order_dict):
                    order[idx] = intimacy_type

                confirm_callback(order)
            self.close()
            return

        self.panel.btn_accept.btn_common_big.SetText(80305)