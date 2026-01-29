# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/BattleImbaGuideUI.py
from __future__ import absolute_import
from six.moves import range
from common.uisys.basepanel import BasePanel
from common.const.uiconst import DIALOG_LAYER_BAN_ZORDER
from common.cfg import confmgr
from common.const import uiconst

class BattleImbaGuideUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_merfolk/open_merfolk_choose'
    DLG_ZORDER = DIALOG_LAYER_BAN_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT

    def on_init_panel(self):

        @self.panel.btn_close.unique_callback()
        def OnClick(btn, touch):
            self.close()

        guide_data = confmgr.get('game_mode/death_imba/guide_data', default={})
        mecha_types = guide_data['mecha_types']
        len_mecha_types = len(mecha_types)
        for idx in range(len_mecha_types):
            mecha_type = str(idx + 1)
            mecha_list, mecha_introduce = mecha_types[mecha_type]
            widget = self.panel.list_item.GetItem(idx)
            widget.SetTouchEnabledRecursion(False)
            widget.list_mecha.SetInitCount(len(mecha_list))
            for mecha_idx, mecha_id in enumerate(mecha_list):
                mecha_widget = widget.list_mecha.GetItem(mecha_idx)
                mecha_pic_path = 'gui/ui_res_2/mall/10100%s_2.png' % mecha_id
                mecha_widget.bar.img_mech.SetDisplayFrameByPath('', mecha_pic_path)

            widget.lab_introduce.SetString(mecha_introduce)