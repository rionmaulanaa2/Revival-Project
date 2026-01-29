# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComTitleDisplay.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from logic.gutils import title_utils
import common.utils.timer as timer
import world
import logic.gcommon.common_const.animation_const as animation_const
import math3d
import render
import game3d
from logic.gcommon.common_const import title_const
import logic.gcommon.common_utils.bcast_utils as bcast
_HASH_texture = game3d.calc_string_hash('_Tex')
TITLE_TECH = render.technique(render.TECH_TYPE_EFFECT, 'shader/ui/blood_ui_digit.fx', 'UI_Blood')

class ComTitleDisplay(UnitCom):
    BIND_EVENT = {'E_ACTIVE_SHOW_TITLE': 'active_show_title',
       'E_SHOW_TITLE': 'show_title',
       'E_REMOVE_TITLE': 'remove_title',
       'E_SWITCH_STATUS': 'on_switch_animation'
       }
    STATE_TO_BIAS = {animation_const.STATE_JUMP: 6,
       animation_const.STATE_SQUAT: -6,
       animation_const.STATE_ROLL: -5,
       animation_const.STATE_CRAWL: -6,
       animation_const.STATE_SQUAT_HELP: -6,
       animation_const.STATE_SWIM: 3
       }

    def init_from_dict(self, unit_obj, bdict):
        super(ComTitleDisplay, self).init_from_dict(unit_obj, bdict)
        self._showing_title_item_no = None
        self._remove_timer_id = None
        self._title_pos_dst_offset = 0
        self._cur_title_pos_offset = 0
        self._rect_primitive = None
        return

    def tick(self, dt):
        super(ComTitleDisplay, self).tick(dt)
        if self._showing_title_item_no is None:
            self.remove_title()
            return
        else:
            if not self._rect_primitive or not self._rect_primitive.valid:
                return
            ui = self._get_title_container_ui()
            if not ui:
                return
            delta = self._title_pos_dst_offset - self._cur_title_pos_offset
            if delta != 0:
                if delta > 0:
                    self._cur_title_pos_offset += 1
                else:
                    self._cur_title_pos_offset -= 1
            self._rect_primitive.position = math3d.vector(0, self._cur_title_pos_offset + self._get_base_title_offset(), 0)
            ui.update_title(self.unit_obj.id, self._rect_primitive.world_position)
            return

    def _get_bind_point(self):
        class_name = self.unit_obj.__class__.__name__
        if class_name in ('LMecha', 'LMechaTrans'):
            bind_point = 'xuetiao'
        elif class_name in ('LAvatar', 'LPuppet'):
            bind_point = 's_xuetiao'
        else:
            bind_point = None
        return bind_point

    def _get_base_title_offset(self):
        class_name = self.unit_obj.__class__.__name__
        if class_name == 'LMecha':
            is_showing_blood_ui = self.ev_g_is_showing_blood_ui()
            if is_showing_blood_ui is None:
                is_showing_blood_ui = False
            if not is_showing_blood_ui:
                return 0.0
            else:
                return 5.5

        elif class_name == 'LMechaTrans':
            is_showing_blood_ui = False
            ui = global_data.ui_mgr.get_ui('MechaTransUI')
            if ui:
                is_showing_blood_ui = False
            if not is_showing_blood_ui:
                return 0.0
            else:
                return 6.0

        elif class_name == 'LAvatar' or class_name == 'LPuppet':
            is_showing_blood_ui = self.ev_g_is_showing_blood_ui()
            if is_showing_blood_ui is None:
                is_showing_blood_ui = False
            if not is_showing_blood_ui:
                return 0.0
            else:
                return 11.0

        else:
            return 2.0
        return

    def active_show_title(self, title_item_no):
        result = self.show_title(title_item_no)
        if result is not None:
            self.send_event('E_CALL_SYNC_METHOD', 'bcast_evt', [bcast.E_SHOW_TITLE, (title_item_no,)], False)
        return

    def show_title(self, title_item_no):
        if title_item_no is None:
            return False
        else:
            ui = self._get_title_container_ui()
            if not ui:
                return False
            scn = world.get_active_scene()
            if not scn:
                return False
            model = self.ev_g_model()
            if not model:
                return False
            tex = ui.show_title(title_item_no, self.unit_obj.id)
            if not tex:
                return False
            self._showing_title_item_no = title_item_no
            self._safe_remove_title_primitive()
            obj = world.primitives(scn)
            half_width = title_const.TITLE_MODEL_WIDTH / 2.0
            half_height = half_width * ui.get_title_size_ratio()
            p1 = math3d.vector(-half_width, half_height, 0)
            p2 = math3d.vector(half_width, half_height, 0)
            p3 = math3d.vector(half_width, -half_height, 0)
            p4 = math3d.vector(-half_width, -half_height, 0)
            obj.create_poly4([((p1, 0, 0), (p2, 1, 0), (p3, 1, 1), (p4, 0, 1), 16777215)])
            mat = render.material(TITLE_TECH)
            mat.set_texture(_HASH_texture, '_Tex', tex)
            obj.set_material(mat)
            obj.remove_from_parent()
            model.bind(self._get_bind_point(), obj, world.BIND_TYPE_TRANSLATE)
            self._rect_primitive = obj
            self.need_update = True
            player_id = global_data.player.logic.id
            if self.unit_obj.sd.ref_driver_id == global_data.player.logic.id or self.unit_obj.id == player_id:
                global_data.player.logic.send_event('E_SUCCESS_INTERACTION')
            self._safe_clean_remove_timer()
            self._remove_timer_id = global_data.game_mgr.register_logic_timer(self._remove_timer_cb, title_utils.get_title_duration(self._showing_title_item_no), times=1, mode=timer.CLOCK)
            anim_state = self.ev_g_anim_state()
            self.on_switch_animation(anim_state)
            self._cur_title_pos_offset = self._title_pos_dst_offset
            self._rect_primitive.position = math3d.vector(0, self._cur_title_pos_offset + self._get_base_title_offset(), 0)
            self.send_event('E_REMOVE_EMOJI')
            return True

    def _safe_clean_remove_timer(self):
        if self._remove_timer_id is not None:
            global_data.game_mgr.unregister_logic_timer(self._remove_timer_id)
            self._remove_timer_id = None
        return

    def _remove_timer_cb(self):
        self.remove_title()

    def remove_title(self):
        if self._showing_title_item_no is not None:
            ui = self._get_title_container_ui()
            if ui:
                ui.remove_title(self.unit_obj.id)
            self._showing_title_item_no = None
            self.need_update = False
        self._safe_remove_title_primitive()
        self._safe_clean_remove_timer()
        return

    def on_switch_animation(self, status, is_sync=True):
        self._title_pos_dst_offset = self.STATE_TO_BIAS.get(status, 0)

    def _get_title_container_ui(self):
        return global_data.ui_mgr.get_ui('TitleContainerUI')

    def _safe_remove_title_primitive(self):
        if self._rect_primitive and self._rect_primitive.valid:
            model = self.ev_g_model()
            if model:
                model.unbind(self._rect_primitive)
            self._rect_primitive.destroy()
            self._rect_primitive = None
        return

    def destroy(self):
        self.remove_title()
        super(ComTitleDisplay, self).destroy()