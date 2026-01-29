# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartLiftLoad.py
from __future__ import absolute_import
import six
from mobile.common.EntityFactory import EntityFactory
from mobile.common.EntityManager import EntityManager
from mobile.common.IdManager import IdManager
from logic.vscene.parts.PartTelevisionManager import PartTelevisionManager
from logic.gutils import battle_flag_utils
from common.utils.timer import LOGIC
from common.cfg import confmgr
import world
import copy
STATE_MODEL_UP = 1
STATE_LIFT_SCROLL = 2
BATTLE_FLAG_TV = [
 10001, 10002, 10003]

class PartLiftLoad(PartTelevisionManager):
    ENTER_EVENT = {'resolution_changed': 'on_resolution_changed'
       }

    def __init__(self, scene, name):
        super(PartLiftLoad, self).__init__(scene, name)
        self.cockpit_model = None
        self.cockpit_cur_y = None
        self.start_scroll_y = 45
        self.tongdao_model_1 = None
        self.tongdao_model_2 = None
        self.scroll_gap_y = 0
        self.cur_scroll_y = 0
        self.up_speed = 50
        self.state = None
        self._battle_flag_entity_id = []
        self.need_show_entity_id = []
        self._render_timer_id = None
        return

    def on_load(self):
        pass

    def on_resolution_changed(self):
        global_data.ui_mgr.check_layer_by_lift_scene(True)

    def on_enter(self):
        global_data.ui_mgr.check_layer_by_lift_scene(True)
        self.check_loaded()

    def check_loaded(self):
        if self.cockpit_model:
            return
        else:
            self.cockpit_model = self.scene().get_model('cockpit_01_7')
            if self.cockpit_model is None:
                return
            self.cockpit_cur_y = self.cockpit_model.position.y
            tongdao_model_1 = self.scene().get_model('new_jiemian_24_6')
            tongdao_model_2 = self.scene().get_model('new_jiemian_24_8')
            self.scroll_tongdao_list = [tongdao_model_1, tongdao_model_2]
            self.scroll_gap_y = tongdao_model_2.position.y - tongdao_model_1.position.y
            self.need_update = True
            role_id = global_data.player.get_role()
            from logic.gcommon.item.item_const import FASHION_POS_SUIT, FASHION_POS_HEADWEAR
            item_data = global_data.player.get_item_by_no(role_id)
            fashion_data = item_data.get_fashion()
            dressed_clothing_id = fashion_data.get(FASHION_POS_SUIT)
            head_id = fashion_data.get(FASHION_POS_HEADWEAR)
            from logic.gutils import dress_utils
            t_model = dress_utils.create_lobby_driver_model(role_id, dressed_clothing_id)
            self.cockpit_model.bind('renwu', t_model)
            t_model.visible = True
            t_model.play_animation('inside_idle_8001', -1, world.TRANSIT_TYPE_DEFAULT, 0, world.PLAY_FLAG_LOOP)
            self.state = STATE_LIFT_SCROLL
            pos = self.cockpit_model.position
            pos.y = self.start_scroll_y
            self.cockpit_model.position = pos
            self.update_camera()
            return

    def init_battle_flag(self):
        if self._battle_flag_entity_id:
            return
        for tv_id in BATTLE_FLAG_TV:
            self._add_entity(tv_id)

    def refresh_battle_info(self):
        brief_group_data = global_data.battle.get_brief_group_data()
        battle_flags = []
        for data in six.itervalues(brief_group_data):
            battle_flag = data.get('battle_flag')
            if battle_flag:
                battle_flags.append(battle_flag)

        tv_e_conf = confmgr.get('tv_conf', 'cl_tv_entity', 'Content', default={})
        need_show_index = []
        battle_flag_num = len(battle_flags)
        if battle_flag_num >= 3:
            need_show_index = [
             0, 1, 2]
        elif battle_flag_num == 2:
            need_show_index = [
             0, 2]
        elif battle_flag_num == 1:
            need_show_index = [
             1]
        self.need_show_entity_id = []
        for i, index in enumerate(need_show_index):
            tv_id = BATTLE_FLAG_TV[index]
            channel_id = tv_e_conf.get(str(tv_id), {}).get('channel_id', 1)
            global_data.emgr.update_tv_channel.emit([(channel_id, battle_flags[i])])
            entity_id = self._battle_flag_entity_id[index]
            self.need_show_entity_id.append(entity_id)

        self.release_timer()
        tm = global_data.game_mgr.get_render_timer()
        self._render_timer_id = tm.register(func=self.render_func, interval=2, times=1, mode=LOGIC)

    def render_func(self):
        for entity_obj_id in self.need_show_entity_id:
            entity_obj = EntityManager.getentity(entity_obj_id)
            if entity_obj and entity_obj.logic:
                entity_obj.logic.send_event('E_SHOW_MODEL')

    def release_timer(self):
        if self._render_timer_id:
            tm = global_data.game_mgr.get_render_timer()
            tm.unregister(self._render_timer_id)
        self._render_timer_id = None
        return

    def _add_entity(self, tv_id):
        entity_id = IdManager.genid()
        entity_obj = EntityFactory.instance().create_entity('Television', entity_id)
        entity_obj.init_from_dict({'tv_id': tv_id,'is_client': True,'scene': self.scene,'is_show': False})
        entity_obj.on_add_to_battle(entity_id)
        self._battle_flag_entity_id.append(entity_id)

    def _remove_entity(self):
        for entity_id in self._battle_flag_entity_id:
            entity_obj = EntityManager.getentity(entity_id)
            if entity_obj:
                entity_obj.on_remove_from_battle()
                entity_obj.destroy()

        self._battle_flag_entity_id = []
        self.need_show_entity_id = []

    def on_update(self, dt):
        super(PartLiftLoad, self).on_update(dt)
        self.check_loaded()
        if not self.cockpit_model:
            return
        if self.state == STATE_MODEL_UP:
            self.cockpit_cur_y += self.up_speed * dt
            if self.cockpit_cur_y >= self.start_scroll_y:
                self.cockpit_cur_y = self.start_scroll_y
                self.state = STATE_LIFT_SCROLL
                self.scroll_tongdao()
            pos = self.cockpit_model.position
            pos.y = self.cockpit_cur_y
            self.cockpit_model.position = pos
            self.update_camera()
        elif self.state == STATE_LIFT_SCROLL:
            for model in self.scroll_tongdao_list:
                pos = model.position
                pos.y -= self.up_speed * dt
                model.position = pos

            self.cur_scroll_y += self.up_speed * dt
            if self.cur_scroll_y >= self.scroll_gap_y:
                self.cur_scroll_y = 0
                self.scroll_tongdao()

    def scroll_tongdao(self):
        tongdao_model_1 = self.scroll_tongdao_list[0]
        pos = tongdao_model_1.position
        pos.y += 2 * self.scroll_gap_y
        tongdao_model_1.position = pos
        self.scroll_tongdao_list[0] = self.scroll_tongdao_list[1]
        self.scroll_tongdao_list[1] = tongdao_model_1

    def update_camera(self):
        camera = self.scene().active_camera
        trans = self.cockpit_model.get_socket_matrix('camera', world.SPACE_TYPE_WORLD)
        camera.world_position = trans.translation
        camera.world_rotation_matrix = trans.rotation
        camera.fov = 45
        camera.z_range = (0.1, 20000)

    def on_exit(self):
        super(PartLiftLoad, self).on_exit()
        global_data.ui_mgr.check_layer_by_lift_scene(False)
        self._remove_entity()