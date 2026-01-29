# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/DeathRogueGiftDetailWidget.py
from __future__ import absolute_import
from common.uisys.BaseUIWidget import BaseUIWidget
from logic.gcommon.cdata.rogue_gift_config import get_survival_gift_data, get_gift_quality
from logic.gutils import rogue_utils as r_u

class DeathRogueGiftDetailWidget(BaseUIWidget):
    INTRO_SETTINGS = {1: [
         'gui/ui_res_2/battle_tdm/rogue/pnl_battle_tdm_rogue_introduce_blue.png', 5668604],
       2: [
         'gui/ui_res_2/battle_tdm/rogue/pnl_battle_tdm_rogue_introduce_purple.png', 10368244],
       3: [
         'gui/ui_res_2/battle_tdm/rogue/pnl_battle_tdm_rogue_introduce_yellow.png', 14520587]
       }

    def __init__(self, parent, parent_panel):
        panel = global_data.uisystem.load_template_create('battle_tdm/i_battle_rogue_introduce', parent=parent_panel, name='battle_rogue_tips')
        super(DeathRogueGiftDetailWidget, self).__init__(parent, panel)

    def refresh_view(self, gift_id):
        self.panel.img_firm.SetDisplayFrameByPath('', r_u.get_gift_icon(gift_id))
        gift_quality = get_gift_quality(gift_id)
        bg, color = self.INTRO_SETTINGS[gift_quality]
        self.panel.bg.SetDisplayFrameByPath('', bg)
        self.panel.lab_firm_name.SetColor(color)
        self.panel.lab_firm_name.SetString(r_u.get_gift_name_text(gift_id))
        self.panel.lab_firm_name.SetColor(r_u.get_brand_name_color(gift_id))
        self.panel.lab_firm.SetString(r_u.get_gift_desc_text(gift_id))

    def _get_image_line_path(self, gift_id):
        brand = r_u.get_gift_brand(gift_id)
        return 'gui/ui_res_2/battle/rogue/img_sponsor_%s.png' % brand