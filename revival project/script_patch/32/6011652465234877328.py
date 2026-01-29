# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComCrystalBloodSimUI.py
from __future__ import absolute_import
from logic.gcommon.component.UnitCom import UnitCom
import world
import math3d
import render
import weakref
import math
from common.uisys.font_utils import GetMultiLangFontFaceName
from logic.gutils.judge_utils import get_player_group_id
from logic.gcommon.const import NEOX_UNIT_SCALE
from logic.gcommon.common_const import battle_const as bconst
A = -12.0 / 51
B = 35 - A * 33

class ComCrystalBloodSimUI(UnitCom):
    BIND_EVENT = {'E_MODEL_LOADED': 'on_model_loaded',
       'E_CRYSTAL_HP_CHANGE': 'on_crystal_hp_change',
       'E_PLAYER_AROUND_CRYSTAL_CHANGE': 'on_player_around_crystal_change'
       }

    def __init__(self):
        super(ComCrystalBloodSimUI, self).__init__()
        self.simui = None
        self.hp_bg_ui = None
        self.hp_ui = None
        self.hp_text_ui = None
        self.hp_text_bg_ui = None
        self.buff_ui = None
        self.max_hp = 0
        self.cur_hp = 0
        self.faction_id = None
        self.need_update = True
        self.crystal_model = None
        self.valid_attack_dis = 0
        return

    def destroy(self):
        self.crystal_model = None
        self.clear_hp_ui()
        super(ComCrystalBloodSimUI, self).destroy()
        return

    def init_from_dict(self, unit_obj, bdict):
        super(ComCrystalBloodSimUI, self).init_from_dict(unit_obj, bdict)
        self.max_hp = int(bdict.get('max_hp', 100))
        self.cur_hp = int(bdict.get('hp', self.max_hp))
        self.faction_id = bdict.get('faction_id')
        play_data = global_data.game_mode.get_cfg_data('play_data')
        self.valid_attack_dis = play_data.get('valid_attack_dis', 100)

    def on_model_loaded(self, model):
        self.crystal_model = weakref.ref(model)
        self.create_hp_ui(model)

    def create_hp_ui(self, model):
        self.scene.simui_enable_post_process(True)
        sim_ui_path = self.get_sim_ui_path()
        self.simui = world.simuiobject(render.texture(sim_ui_path))
        self.hp_bg_ui = self.simui.add_image_ui(0, 18, 70, 59, 0, 0)
        self.hp_ui = self.simui.add_image_ui(69, 18, 70, 59, 0, 0)
        self.hp_text_bg_ui = self.simui.add_image_ui(0, 78, 70, 15, 0, 40)
        self.buff_ui = self.simui.add_image_ui(0, 95, 70, 20, 0, -40)
        hp_percent = self.cur_hp * 1.0 / self.max_hp
        hp_percent = int(min(math.ceil(100.0 * hp_percent), 100))
        hp_percent_str = '{}%'.format(str(hp_percent))
        render.create_font('hp_text', GetMultiLangFontFaceName('HYLingXinJ'), 10, True)
        self.hp_text_ui = self.simui.add_text_ui(hp_percent_str, 'hp_text', 0, 23)
        image_list = (
         self.hp_bg_ui, self.hp_ui, self.hp_text_ui, self.hp_text_bg_ui, self.buff_ui)
        for image in image_list:
            if image:
                self.simui.set_ui_align(image, 0.5, 0.5)
                self.simui.set_ui_fill_z(image, True)

        hp_percent = self.cur_hp * 1.0 / self.max_hp
        self.simui.set_imageui_verpercent(self.hp_bg_ui, 0.0, 1.0)
        self.simui.set_imageui_verpercent(self.hp_text_bg_ui, 0.0, 1.0)
        self.simui.set_imageui_verpercent(self.hp_ui, 1.0 - hp_percent, 1.0)
        self.simui.set_imageui_horpercent(self.buff_ui, 0.0, 0.0)
        self.simui.set_parent(model)
        self.simui.inherit_flag = world.INHERIT_TRANSLATION
        self.simui.position = math3d.vector(0, bconst.CRYSTAL_COVER_H + 50, 0)
        self.simui.visible = True

    def clear_hp_ui(self):
        if self.simui and self.simui.valid:
            try:
                self.simui.destroy()
            except:
                pass

            self.simui = None
        return

    def on_crystal_hp_change(self, hp, hp_percent):
        if not self.simui or not self.simui.valid:
            return
        self.simui.set_imageui_verpercent(self.hp_ui, max(0, 1.0 - hp_percent), 1.0)
        hp_percent = int(min(math.ceil(100.0 * hp_percent), 100))
        hp_percent_str = '{}%'.format(str(hp_percent))
        self.simui.set_text(self.hp_text_ui, hp_percent_str)

    def on_player_around_crystal_change(self, player_cnt):
        if not self.simui or not self.simui.valid:
            return
        right_range = max(0.0, min(1.0, 0.33 * player_cnt))
        self.simui.set_imageui_horpercent(self.buff_ui, 0.0, right_range)

    def get_sim_ui_path(self):
        if self.faction_id == get_player_group_id():
            return 'gui/ui_res_2/battle_crystal/bar_battle_crystal_simui_blue.png'
        else:
            return 'gui/ui_res_2/battle_crystal/bar_battle_crystal_simui_red.png'

    def tick(self, delta):
        if not self.simui or not self.scene or not self.scene.active_camera:
            return
        else:
            if self.crystal_model:
                model = self.crystal_model() if 1 else None
                return model or None
            pos = model.position
            dist = self.scene.active_camera.position - pos
            dist = dist.length / NEOX_UNIT_SCALE
            max_dist = 200
            scale = max(0.1, (max_dist - dist) * 1.0 / max_dist)
            self.simui.scale = (scale, scale)
            if dist <= 33:
                text_ui_y = 35
            elif dist > 84:
                text_ui_y = 23
            else:
                text_ui_y = A * dist + B
            self.simui.set_ui_pos(self.hp_text_ui, 0, text_ui_y)
            return