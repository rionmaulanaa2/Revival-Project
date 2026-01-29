# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/pet/PetInteractUIPC.py
from .PetInteractUI import PetInteractUI

class PetInteractUIPC(PetInteractUI):
    HOT_KEY_FUNC_MAP = {'pet_interact_1': 'on_click_btn_enter_1',
       'pet_interact_2': 'on_click_btn_enter_2'
       }

    def on_init_panel(self):
        super(PetInteractUIPC, self).on_init_panel()
        self.panel.img_key_1.setVisible(True)
        self.panel.img_key_2.setVisible(True)
        self.panel.img_key_3.setVisible(True)

    def on_click_btn_enter_1(self, *args):
        self.panel.btn_enter_1.OnClick(0, 0)
        self.panel.btn_enter_2.OnClick(0, 0)

    def on_click_btn_enter_2(self, *args):
        self.panel.btn_enter_3.OnClick(0, 0)