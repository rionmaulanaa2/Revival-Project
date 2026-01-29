# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/message/ChangeSexUI.py
from __future__ import absolute_import
import common.const.uiconst
from logic.comsys.common_ui.WindowSmallBase import WindowSmallBase
from logic.gcommon.const import AVATAR_SEX_NONE, AVATAR_SEX_FEMALE, AVATAR_SEX_MALE

class ChangeSexUI(WindowSmallBase):
    PANEL_CONFIG_NAME = 'role/setting_gender'
    DLG_ZORDER = common.const.uiconst.NORMAL_LAYER_ZORDER
    TEMPLATE_NODE_NAME = 'panel'
    UI_ACTION_EVENT = {'panel.nd_choose.temp_1.btn.OnClick': '_on_click_sex_choose',
       'panel.nd_choose.temp_2.btn.OnClick': '_on_click_sex_choose',
       'panel.panel.confirm.btn_common_big.OnClick': '_on_set_sex'
       }
    GLOBAL_EVENT = {'player_on_change_sex': 'close'
       }

    def set_original_sex(self, sex):
        self.panel.nd_choose.temp_1.btn.bar.choose.setVisible(False)
        self.panel.nd_choose.temp_2.btn.bar.choose.setVisible(False)
        choose_node = {AVATAR_SEX_NONE: None,
           AVATAR_SEX_MALE: self.panel.nd_choose.temp_1.btn.bar.choose,
           AVATAR_SEX_FEMALE: self.panel.nd_choose.temp_2.btn.bar.choose
           }
        node = choose_node.get(sex, None)
        if node:
            node.setVisible(True)
        return

    def on_init_panel(self, *args, **kargs):
        super(ChangeSexUI, self).on_init_panel()
        self.set_original_sex(AVATAR_SEX_NONE)

    def _get_set_sex(self):
        male_chosen = self.panel.nd_choose.temp_1.btn.bar.choose.isVisible()
        female_chosen = self.panel.nd_choose.temp_2.btn.bar.choose.isVisible()
        if not male_chosen and not female_chosen:
            return AVATAR_SEX_NONE
        else:
            if male_chosen:
                return AVATAR_SEX_MALE
            return AVATAR_SEX_FEMALE

    def _on_click_sex_choose(self, btn, touch):
        temp1_show = True if btn == self.panel.nd_choose.temp_1.btn else False
        self.panel.nd_choose.temp_1.btn.bar.choose.setVisible(temp1_show)
        self.panel.nd_choose.temp_2.btn.bar.choose.setVisible(not temp1_show)

    def _on_set_sex(self, *args):
        sex = self._get_set_sex()
        if sex == AVATAR_SEX_NONE:
            global_data.game_mgr.show_tip(862001)
            return
        if not global_data.player.req_change_sex(sex):
            self.close()