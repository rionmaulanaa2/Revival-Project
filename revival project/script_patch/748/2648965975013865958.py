# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/MonsterBloodUI.py
from __future__ import absolute_import
import six
from common.uisys.basepanel import BasePanel
from common.const.uiconst import SMALL_MAP_ZORDER
from mobile.common.EntityManager import EntityManager
from common.utils.cocos_utils import getScreenSize
from logic.gcommon.const import NEOX_UNIT_SCALE
from common.utils.cocos_utils import neox_pos_to_cocos
import weakref
import world
import cc

class MonsterLocateUI(object):

    def __init__(self, parent):
        self.parent = parent
        self._nd = global_data.uisystem.load_template_create('battle_monster/i_hp_monster')
        self._hit_anim_tag = 1
        self.init_parameters()

    def init_parameters(self):
        self._hp_max = 1
        self._cur_hp = 0
        self.hit_id = 0
        self.screen_size = getScreenSize()
        self._nd.hp_monster.getGLProgramState().setUniformFloat('_Xinterval', 500.0 / 2)
        self._nd.hp_monster.getGLProgramState().setUniformFloat('_Emptyinterval', 2.0)
        self._nd.hp_monster.getGLProgramState().setUniformFloat('_Y', 0.0)
        self._nd.hp_monster.getGLProgramState().setUniformFloat('_YBlood', 0.0)
        self._nd.hp_monster.getGLProgramState().setUniformFloat('_Z', 0.0)
        self._nd.hp_monster.getGLProgramState().setUniformFloat('_ZBlood', 0.0)

    def on_finalize_panel(self):
        self.bind_event(False)
        self._nd.StopTimerAction()
        self._nd and self._nd.Destroy()
        self._nd = None
        return

    def _recycle_wrapper(self):
        self._nd.hp_monster.SetUniformTexture('_TexWhite', 'gui/ui_res_2/battle/monster/hp_monster_hit.png')
        self._nd.nd_hp.setVisible(True)
        self.bind_event(False)
        self._nd.StopTimerAction()
        self.parent.recycle_locate_wrapper(self.hit_id)
        self._hp_max = 1
        self._cur_hp = 0
        self.hit_id = 0

    def get_monster(self):
        monster = EntityManager.getentity(self.hit_id)
        if monster and monster.logic:
            return monster.logic

    def set_monster_info(self, hit_id):
        if self.hit_id == hit_id:
            self.update_nd_pos()
            self.on_delay_recycle()
            return
        else:
            self.bind_event(False)
            self.hit_id = hit_id
            monster = self.get_monster()
            if monster:
                self._hp_max = monster.ev_g_max_hp()
                self._hp = monster.ev_g_hp()
                self._nd.hp_monster.getGLProgramState().setUniformFloat('_X', self._hp_max)
                self._nd.hp_monster.getGLProgramState().setUniformFloat('_XBlood', self._hp)
                level = monster.ev_g_config_data().get('Level', 1)
                self._nd.icon_monster.SetDisplayFrameByPath(None, 'gui/ui_res_2/battle/monster/monster_lv%d.png' % level)
            self.bind_event(True)
            self.update_nd_pos()
            self.on_delay_recycle()
            return

    def bind_event(self, bind=True):
        monster = self.get_monster()
        if not monster:
            return
        if bind:
            regist_func = monster.regist_event
            regist_func('E_HEALTH_HP_CHANGE', self.health_hp_change)
            regist_func('E_HEALTH_HP_EMPTY', self.on_hp_empty)
        else:
            unregist_event = monster.unregist_event
            unregist_event('E_HEALTH_HP_CHANGE', self.health_hp_change)
            unregist_event('E_HEALTH_HP_EMPTY', self.on_hp_empty)

    def health_hp_change(self, hp, mod=0):
        self._cur_hp = hp
        self._nd.hp_monster.getGLProgramState().setUniformFloat('_XBlood', hp)
        if mod < 0:
            self._nd.hp_monster.SetUniformTexture('_TexWhite', 'gui/ui_res_2/battle/monster/hp_monster_hit.png')
            self._nd.stopActionByTag(self._hit_anim_tag)

            def recover_texture():
                self._nd.hp_monster.SetUniformTexture('_TexWhite', 'gui/ui_res_2/battle/monster/hp_monste.png')

            self._nd.DelayCallWithTag(1.0, recover_texture, self._hit_anim_tag)
        self.update_nd_pos()

    def on_hp_empty(self):
        self._nd.PlayAnimation('die')
        self.on_delay_recycle(1.5)

    def update_nd_pos(self):
        monster = self.get_monster()
        cam = global_data.game_mgr.scene.active_camera
        if monster and cam and self._nd:
            model = monster.ev_g_model()
            if model:
                position = monster.ev_g_model_position()
                dist = cam.position - position
                dist = dist.length / NEOX_UNIT_SCALE
                max_dist = 200
                scale = max(0.3, (max_dist - dist) * 1.0 / max_dist)
                self._nd.setScale(scale)
                xuetiao_pos = model.get_socket_matrix('xuetiao', world.SPACE_TYPE_WORLD).translation
                x, y = cam.world_to_screen(xuetiao_pos)
                x, y = neox_pos_to_cocos(x, y)
                lpos = self._nd.getParent().convertToNodeSpace(cc.Vec2(x, y))
                self._nd.setPosition(lpos)
                return
        self._recycle_wrapper()

    def on_delay_recycle(self, revive_time=10):

        def refresh_time(pass_time):
            self.update_nd_pos()

        def refresh_time_finsh():
            self._recycle_wrapper()

        self._nd.StopTimerAction()
        self._nd.TimerAction(refresh_time, revive_time, callback=refresh_time_finsh)


from common.const import uiconst

class MonsterBloodUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_monster/hp_monster'
    DLG_ZORDER = SMALL_MAP_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    MAX_CACHE = 20

    def on_init_panel(self):
        self.init_parameters()
        self.init_event()
        self.panel.setLocalZOrder(1)

    def on_finalize_panel(self):
        for locate_wrapper in self.blood_ui_free:
            locate_wrapper.on_finalize_panel()

        for locate_wrapper in six.itervalues(self.blood_ui_using):
            locate_wrapper.on_finalize_panel()

        self.blood_ui_using = {}
        self.blood_ui_free = []

    def init_parameters(self):
        self.blood_ui_using = {}
        self.blood_ui_free = []

    def init_event(self):
        pass

    def show_monster_hp(self, hit_id):
        if hit_id in self.blood_ui_using:
            locate_wrapper = self.blood_ui_using[hit_id]
        else:
            if self.blood_ui_free:
                locate_wrapper = self.blood_ui_free.pop()
                self.panel.temp_monster_hp.AddChild(None, locate_wrapper._nd)
                locate_wrapper._nd.release()
            else:
                locate_wrapper = MonsterLocateUI(self)
                self.panel.temp_monster_hp.AddChild(None, locate_wrapper._nd)
            self.blood_ui_using[hit_id] = locate_wrapper
        locate_wrapper.set_monster_info(hit_id)
        return

    def recycle_locate_wrapper(self, hit_id):
        if hit_id not in self.blood_ui_using:
            return
        locate_wrapper = self.blood_ui_using[hit_id]
        locate_wrapper._nd.retain()
        locate_wrapper._nd.removeFromParent()
        if len(self.blood_ui_free) > self.MAX_CACHE:
            locate_wrapper.on_finalize_panel()
        else:
            self.blood_ui_free.append(locate_wrapper)
        del self.blood_ui_using[hit_id]