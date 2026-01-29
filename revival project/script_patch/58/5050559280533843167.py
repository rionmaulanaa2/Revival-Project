# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartTelevisionManager.py
from __future__ import absolute_import
import six
from . import ScenePart
import render
import cc
import world
import math3d
import game3d
from common.uisys.uielment.CCLayer import CCLayer
from common.utils.cocos_utils import ccp, CCSize
from logic.gcommon.const import NEOX_UNIT_SCALE
from common.cfg import confmgr
from logic.gcommon import time_utility
from common.utilities import clamp
from logic.manager_agents.manager_decorators import sync_exec
from logic.gutils.tv_panel_utils import update_channel_panel, MANUAL, AUTO, init_tv_entity
UPDATE_MIN_TIME = 0.4
LOD_0_DIST_SQR = (80 * NEOX_UNIT_SCALE) ** 2
LOD_1_DIST_SQR = (150 * NEOX_UNIT_SCALE) ** 2
LOD_UPDATE_DELTA = {0: 0.03,
   1: 0.1,
   2: 0.33
   }

class PartTelevisionManager(ScenePart.ScenePart):
    INIT_EVENT = {'scene_add_television_entity': '_add_tv_entity',
       'scene_remove_television_entity': '_del_tv_entity',
       'update_tv_channel': '_update_tv_channel'
       }

    def __init__(self, scene, name):
        super(PartTelevisionManager, self).__init__(scene, name, False)
        w_size = global_data.ui_mgr.design_screen_size
        self.width, self.height = w_size.width, w_size.height
        self._tv_entities = {}
        self._cid_to_entities = {}
        self.channel_resources = {}
        self.channel_lod_info = {}
        self._to_add_dict = {}
        self._to_del_list = []
        self.to_update_list = {}
        self._tv_c_conf = confmgr.get('tv_conf', 'tv_channel', 'Content', default={})

    def _add_tv_entity(self, unit_obj, channel_id, need_up_channel=True, info={}):
        if unit_obj.id in self._tv_entities:
            return
        self._cid_to_entities.setdefault(channel_id, set())
        self._cid_to_entities[channel_id].add(unit_obj.id)
        self._tv_entities[unit_obj.id] = (
         channel_id, unit_obj)
        tex = self._get_channel_resource(unit_obj, channel_id, need_up_channel, info)
        unit_obj.send_event('E_ADD_TO_TV_MANAGER', tex)
        init_tv_entity(unit_obj, channel_id)

    def _del_tv_entity(self, eid):
        if eid not in self._tv_entities:
            return
        channel_id = self._tv_entities[eid][0]
        if channel_id in self._cid_to_entities:
            self._cid_to_entities[channel_id].remove(eid)
        del self._tv_entities[eid]
        self.sub_channel_resource(channel_id)

    def on_enter(self):
        self._tv_entities = {}
        self.channel_resources = {}
        self._cid_to_entities = {}

    def on_exit(self):
        self._tv_entities = {}
        self._cid_to_entities = {}
        self._clear_all_resources()

    def on_update(self, dt):
        if not self._to_add_dict and not self.to_update_list:
            return
        cur_time = time_utility.get_server_time()
        for channel_id in six.iterkeys(self.channel_lod_info):
            self.channel_lod_info[channel_id][0] = []

        for entity_info in six.itervalues(self._tv_entities):
            channel_id, unit_obj = entity_info
            if not unit_obj or not unit_obj.is_valid():
                continue
            model = unit_obj.ev_g_model()
            if not model or not model.valid:
                continue
            if not model.is_visible_in_this_frame():
                self.channel_lod_info[channel_id][0].append(3)
            else:
                dist = model.position - world.get_active_scene().active_camera.position
                if dist.length_sqr < LOD_0_DIST_SQR:
                    self.channel_lod_info[channel_id][0].append(0)
                elif dist.length_sqr < LOD_1_DIST_SQR:
                    self.channel_lod_info[channel_id][0].append(1)
                else:
                    self.channel_lod_info[channel_id][0].append(2)

        for channel_id in self._to_add_dict:
            rt, panel, up_time = self._to_add_dict[channel_id]
            self.to_update_list[channel_id] = [rt, panel, True, up_time]

        self._to_add_dict = {}
        for channel_id, channel_resource in six.iteritems(self.to_update_list):
            rt, panel, valid, force_up_time = channel_resource
            refresh_mode = self._tv_c_conf.get(str(channel_id), {}).get('refresh_mode', AUTO)
            if refresh_mode == MANUAL and force_up_time <= 0:
                continue
            if not valid:
                self._to_del_list.append(channel_id)
                continue
            lod_level_list, last_time = self.channel_lod_info[channel_id]
            if not lod_level_list:
                continue
            lod_level = min(lod_level_list)
            if lod_level == 3 and force_up_time <= 0:
                continue
            if force_up_time >= 0:
                force_up_time -= dt
                self.to_update_list[channel_id][3] = clamp(force_up_time, 0, force_up_time)
            if lod_level not in LOD_UPDATE_DELTA:
                update_delta = LOD_UPDATE_DELTA[2] if 1 else LOD_UPDATE_DELTA[lod_level]
                if cur_time - last_time < update_delta:
                    continue
                self.channel_lod_info[channel_id][1] = cur_time
                self._draw_ui_to_rt(rt, panel)

        for val in self._to_del_list:
            del self.to_update_list[val]

        self._to_del_list = []

    def _get_channel_resource(self, unit_obj, channel_id, need_up_channel=True, info={}):
        if channel_id not in self.channel_resources:
            rt, tex, panel = self._create_channel_resource(channel_id)
            need_up_channel = True and need_up_channel
        else:
            self.channel_resources[channel_id][0] += 1
            rt, tex, panel = self.channel_resources[channel_id][1]
            need_up_channel = False
        add_param = self._to_add_dict.setdefault(channel_id, [rt, panel, 0])
        self._to_add_dict[channel_id][2] = max(add_param[2], 0)
        if need_up_channel:
            self._update_tv_channel([(channel_id, info)], unit_obj.ev_g_is_avatar())
        return tex

    def _create_channel_resource(self, channel_id, **kwargs):
        resource_path = self._tv_c_conf.get(str(channel_id), {}).get('panel_path', 'battle/fight_mech_call')
        panel = global_data.uisystem.load_template_create(resource_path)
        panel.retain()
        size = panel.getContentSize()
        old_design_size = global_data.ui_mgr.design_screen_size
        scale = min(old_design_size.width / size.width, old_design_size.height / size.height)
        if global_data.is_low_mem_mode:
            scale = scale * 0.5
        render_texture_size = (size.width * scale, size.height * scale)
        panel.setAnchorPoint(cc.Vec2(0, 0))
        if game3d.get_render_device() not in (game3d.DEVICE_GLES, game3d.DEVICE_GL):
            panel.setScale(scale)
            panel.SetPosition(0, 0)
        else:
            panel.setScaleX(scale)
            panel.setScaleY(-scale)
            panel.SetPosition(0, size.height * scale)
        tex = render.texture.create_empty(int(render_texture_size[0]), int(render_texture_size[1]), render.PIXEL_FMT_A8R8G8B8, True)
        rt = cc.RenderTexture.createWithITexture(tex)
        rt.retain()
        resource = (
         rt, tex, panel)
        self.channel_resources[channel_id] = [1, resource]
        self.channel_lod_info[channel_id] = [[], 0]
        if not self.need_update:
            self.need_update = True
        return (rt, tex, panel)

    def sub_channel_resource(self, channel_id):
        if channel_id not in self.channel_resources:
            return
        self.channel_resources[channel_id][0] -= 1
        if self.channel_resources[channel_id][0] <= 0:
            if channel_id in self.to_update_list:
                self.to_update_list[channel_id][2] = False
            rt, tex, panel = self.channel_resources[channel_id][1]
            if panel:
                panel.Destroy()
                panel.release()
            rt.release()
            del tex
            del self.channel_resources[channel_id]

    def _clear_all_resources(self):
        for channel_resource in six.itervalues(self.channel_resources):
            rt, tex, panel = channel_resource[1]
            if panel:
                panel.Destroy()
                panel.release()
            rt.release()
            del tex

        self.channel_resources = {}
        self.channel_lod_info = {}

    def _update_tv_channel(self, channel_id_lst, is_avatar=True):
        for channel_id, info in channel_id_lst:
            if channel_id not in self.channel_resources:
                continue
            eid_lst = self._cid_to_entities.get(channel_id, [])
            rt, tex, panel = self.channel_resources[channel_id][1]
            info['is_avatar'] = is_avatar
            count = [1, False]
            if global_data.enable_ui_add_image_async:

                def pic_callback(channel_id=channel_id, count=count):
                    count[0] += 1

                    def return_callback(channel_id=channel_id, count=count):
                        count[0] -= 1
                        if count[0] <= 0 and count[1]:
                            if channel_id in self.channel_resources:
                                rt, tex, panel = self.channel_resources[channel_id][1]
                                self._draw_ui_to_rt(rt, panel)

                    return return_callback

            else:
                pic_callback = lambda : None
            up_time = update_channel_panel(channel_id, panel, eid_lst, info, get_load_callback=pic_callback)
            refresh_mode = self._tv_c_conf.get(str(channel_id), {}).get('refresh_mode', AUTO)
            count[0] -= 1
            count[1] = True if refresh_mode == MANUAL and up_time <= 0 else False
            if refresh_mode == MANUAL:
                if up_time > 0:
                    if channel_id in self.to_update_list:
                        self.to_update_list[channel_id][3] = up_time
                    elif channel_id in self._to_add_dict:
                        up_time = max(up_time, self._to_add_dict[channel_id][2])
                        self._to_add_dict[channel_id][2] = up_time
                elif not global_data.enable_ui_add_image_async:
                    self._draw_ui_to_rt(rt, panel)
                elif count[0] <= 0:
                    self._draw_ui_to_rt(rt, panel)

    @sync_exec
    def _draw_ui_to_rt(self, rt, panel):
        if not panel or not panel.isValid():
            return
        rt.beginWithClear(0, 0, 0, 0, 0, 0)
        if hasattr(rt, 'addCommandsForNode'):
            rt.addCommandsForNode(panel.get())
        else:
            panel.visit()
        rt.end()