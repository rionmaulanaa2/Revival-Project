# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/intimacy/IntimacyBuildChoose.py
from __future__ import absolute_import
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
from common.const.uiconst import NORMAL_LAYER_ZORDER
from logic.gcommon.const import INTIMACY_RELATION_TYPE_SET, INTIMACY_NAME_MAP, INTIMACY_RELATION_NUM_LIMIT
from logic.gutils.intimacy_utils import INTIMACY_PIC

class IntimacyBuildChoose(WindowMediumBase):
    PANEL_CONFIG_NAME = 'friend/intimacy_build_choose'
    TEMPLATE_NODE_NAME = 'temp_bg'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    MOUSE_CURSOR_TRIGGER_SHOW = True

    def on_init_panel(self, *args, **kwargs):
        super(IntimacyBuildChoose, self).on_init_panel(*args, **kwargs)
        self._not_show_cb = None
        self._cur_intimacy = None
        self.type_2_btn = {}
        self.build_callback = None
        self.cur_choose_btn = None
        return

    def choose_intimacy(self, build_callback=None):
        self.build_callback = build_callback
        self.type_2_btn = {}
        panel = self.panel
        panel.list_reward.SetInitCount(len(INTIMACY_RELATION_TYPE_SET))
        relation_data = global_data.player.intimacy_relation_data
        for idx, intimacy_type in enumerate(INTIMACY_RELATION_TYPE_SET):
            item = panel.list_reward.GetItem(idx)
            item.lab_name.SetString(INTIMACY_NAME_MAP[intimacy_type])
            item.img_icon.SetDisplayFrameByPath('', INTIMACY_PIC[intimacy_type])
            cur_relation_count = len(relation_data.get(intimacy_type, []))
            item.lab_limit.SetString('%d/%d' % (cur_relation_count, INTIMACY_RELATION_NUM_LIMIT[intimacy_type]))
            item_locked = cur_relation_count >= INTIMACY_RELATION_NUM_LIMIT[intimacy_type]
            item.img_lock.setVisible(item_locked)
            item.btn_choose.SetEnable(not item_locked)

            @item.btn_choose.callback()
            def OnClick(btn, touch, intimacy_type=intimacy_type):
                self._cur_intimacy = intimacy_type
                panel.btn_accept.btn_common_big.SetEnable(True)
                if self.cur_choose_btn:
                    self.cur_choose_btn.SetSelect(False)
                self.cur_choose_btn = btn
                btn.SetSelect(True)

        @panel.btn_accept.btn_common_big.callback()
        def OnClick(btn, touch):
            if callable(self.build_callback):
                self.build_callback(self._cur_intimacy)
            self.close()

        panel.btn_accept.btn_common_big.SetEnable(False)