# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComHumanMarkView.py
from __future__ import absolute_import
from ..UnitCom import UnitCom
from logic.gcommon.component.client.ComBaseMarkView import ComBaseMarkView
from logic.gcommon.common_utils.local_text import get_text_by_id
import math3d
import render
import world
from logic.gcommon.const import NEOX_UNIT_SCALE
from common.uisys.font_utils import GetMultiLangFontFaceName
from common.uisys.uielment.CCUISpaceNode import CCUISpaceNode

class ComHumanMarkView(ComBaseMarkView):
    BIND_EVENT = dict(ComBaseMarkView.BIND_EVENT)
    BIND_EVENT.update({'E_ON_JOIN_MECHA_START': '_on_join_mecha',
       'E_ON_LEAVE_MECHA_START': '_on_leave_mecha',
       'E_ON_JOIN_MECHA': '_on_join_mecha',
       'E_ON_LEAVE_MECHA': '_on_leave_mecha',
       'E_DEATH': '_on_death',
       'E_DEFEATED': '_on_defeated',
       'E_REVIVE': '_on_revive',
       'E_SHOW_PITY_MSG': '_on_show_pity_msg'
       })

    def init_parameters(self):
        super(ComHumanMarkView, self).init_parameters()
        self._space_node = None
        self.pity_delay_timer = None
        return

    def _is_cam_player(self, entity_id):
        return global_data.cam_lplayer and entity_id == global_data.cam_lplayer.id

    def _on_model_loaded(self, model):
        super(ComHumanMarkView, self)._on_model_loaded(model)
        if self.ev_g_death() or self.ev_g_defeated():
            return
        if self.ev_g_control_target() is self.unit_obj.get_owner():
            self.creat_marks()

    def get_mark_position(self):
        return math3d.vector(0, 25, 0)

    def _on_join_mecha(self, *args, **kargs):
        self.clear_marks()

    def _on_leave_mecha(self, *args, **kargs):
        self.creat_marks()

    def _on_death(self, *args, **kargs):
        self.clear_marks()

    def _on_defeated(self, *args, **kargs):
        self.clear_marks()

    def _on_revive(self, *args, **kargs):
        self.creat_marks()

    def _on_show_pity_msg(self, msg_data):
        if global_data.cam_lplayer and global_data.cam_lplayer.ev_g_is_groupmate(self.unit_obj.id, False):
            return
        else:
            model = self.ev_g_model()
            if model:
                self.release_pity_msg()
                text_id = msg_data.get('text_id')
                voice_trigger_type = msg_data.get('voice_trigger_type')
                if not text_id:
                    txt_lst = None if 1 else get_text_by_id(text_id).split('|')
                    return txt_lst or None
                space_node = CCUISpaceNode.Create()
                nd = global_data.uisystem.load_template_create('battle/fight_end_chat')
                space_node.AddChild('', nd)
                nd.setPosition(0, 0)
                self._space_node = space_node
                all_text = ''
                for index, text in enumerate(txt_lst):
                    if index > 0:
                        all_text = '\n' + all_text
                    all_text += text

                nd.lab_chat.SetString(all_text)
                if voice_trigger_type:
                    global_data.game_voice_mgr.play_game_voice(voice_trigger_type)
                space_node.bind_model(model, 'c_xuetiao')
                self.create_pity_delay_timer()
                self.need_update = True
            return

    def tick(self, dt):
        if not self._space_node or not self._space_node.isValid():
            return
        if not self.scene or not self.scene.active_camera:
            return
        model = self.ev_g_model()
        if not model:
            return
        cam_pos = self.scene.active_camera.world_position
        simui_pos = model.world_position
        dis = (cam_pos - simui_pos).length / NEOX_UNIT_SCALE
        is_visible = dis < 30
        self._space_node.setVisible(is_visible)

    def create_pity_delay_timer(self, *args):
        self.clear_pity_delay_timer()
        from common.utils import timer
        self.pity_delay_timer = global_data.game_mgr.register_logic_timer(self.release_pity_msg, 10, args=args, times=1, mode=timer.CLOCK)

    def clear_pity_delay_timer(self):
        if self.pity_delay_timer:
            global_data.game_mgr.unregister_logic_timer(self.pity_delay_timer)
            self.pity_delay_timer = None
        return

    def release_pity_msg(self):
        if self._space_node and self._space_node.isValid():
            self._space_node.Destroy()
        self._space_node = None
        self.need_update = False
        return

    def clear_marks(self):
        self.release_pity_msg()
        super(ComHumanMarkView, self).clear_marks()

    def destroy(self):
        self.release_pity_msg()
        self.clear_pity_delay_timer()
        super(ComHumanMarkView, self).destroy()