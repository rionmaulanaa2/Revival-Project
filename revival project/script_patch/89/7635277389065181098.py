# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComAIDebugUI.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
import math3d
import world
import render
from common.uisys.font_utils import GetMultiLangFontFaceName

class ComAIDebugUI(UnitCom):
    BIND_EVENT = {'E_SHOW_AI_STATE': 'show_ai_state_info'
       }

    def __init__(self):
        super(ComAIDebugUI, self).__init__()
        self.ai_simui = None
        self.ai_simui_ids = None
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComAIDebugUI, self).init_from_dict(unit_obj, bdict)

    def show_ai_state_info(self, state_info):
        if self.ai_simui is None:
            model = self.ev_g_model()
            if model:
                render.create_font('name_txt', GetMultiLangFontFaceName('FZLanTingHei-R-GBK'), 15, True)
                ui_empty = render.texture('gui/ui_res_2/battle/panel/pnl_item_empty.png')
                self.ai_simui = world.simuiobject(ui_empty)
                self.ai_simui.set_parent(model)
                if model.get_socket_matrix('xuetiao', world.SPACE_TYPE_LOCAL):
                    pos = model.get_socket_matrix('xuetiao', world.SPACE_TYPE_LOCAL).translation
                    pos.y = pos.y * model.scale.y
                    self.ai_simui.position = pos
                else:
                    self.ai_simui.position = math3d.vector(0, 25, 0)
                self.ai_simui.inherit_flag = world.INHERIT_TRANSLATION
        if self.ai_simui is None:
            return
        else:
            ai_simui_ids = self.ai_simui_ids
            if ai_simui_ids and len(ai_simui_ids) == 1:
                for i, simui_id in enumerate(ai_simui_ids):
                    self.ai_simui.set_text(simui_id, state_info[0])
                    self.ai_simui.set_ui_color(simui_id, tuple(state_info[1]))

            else:
                if ai_simui_ids:
                    for simui_id in ai_simui_ids:
                        self.ai_simui.remove_ui(simui_id)

                ai_simui_ids = []
                simui_id = self.ai_simui.add_text_ui(state_info[0], 'name_txt', 0, 0)
                self.ai_simui.set_ui_color(simui_id, tuple(state_info[1]))
                self.ai_simui.set_ui_align(simui_id, 0.5, 0.5)
                self.ai_simui.set_ui_skew(simui_id, 0.27, 0)
                self.ai_simui.set_ui_fill_z(simui_id, False)
                ai_simui_ids.append(simui_id)
                self.ai_simui_ids = ai_simui_ids
            return

    def destroy(self):
        if self.ai_simui and self.ai_simui.valid:
            self.ai_simui.destroy()
        self.ai_simui = None
        self.ai_simui_ids = None
        super(ComAIDebugUI, self).destroy()
        return