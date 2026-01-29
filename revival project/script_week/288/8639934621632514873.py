# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/PartTravelWorld.py
import time
import math3d
import world
import game3d
from . import ScenePart
from math import floor

class Baker(object):

    def execute(self, scn, start_point, left, right, bottom, up, chunksize):
        self._do_execute(scn, start_point, left, right, bottom, up, chunksize)

    def _do_execute(self, scn, start_point, left, right, bottom, up, chunksize):
        raise NotImplementedError('[Baker]execute not implemented')

    def update(self):
        pass

    def stop(self):
        pass


STEP_HEIGHT = 5
STEP_WIDTH = 5
INVALID_VALUE = 100000
_HASH_CHANGE_COLOR = game3d.calc_string_hash('u_change_color')
_tmp_x_p = math3d.vector(STEP_WIDTH, 0, 0)
_tmp_x_n = math3d.vector(-STEP_WIDTH, 0, 0)
_tmp_z_p = math3d.vector(0, 0, STEP_WIDTH)
_tmp_z_n = math3d.vector(0, 0, -STEP_WIDTH)
_tmp_y_p = math3d.vector(0, STEP_HEIGHT, 0)
_tmp_y_n = math3d.vector(0, -STEP_HEIGHT, 0)

class Node(object):

    def __init__(self, next_point, from_point):
        self.next_point = next_point
        self.from_point = from_point


class RayTestHeightMapBaker(Baker):

    def __init__(self):
        super(RayTestHeightMapBaker, self).__init__()
        self._chunk_size = 1
        self._debug_models = []
        self._debug_models_lut = {}
        self._job_args = ()
        self._job_args_backup = None
        self._job_queue = None
        self._job_lut = None
        self._job_trace = None
        self._last_highlight_objects = []
        self._hight_obj_pools = []
        self._model_pools = [[], []]
        self._visit_counts = None
        self._visit_set = None
        self._stop = False
        self._this_frame_i = 0
        self._this_frame_min_max = (0, 0)
        return

    def _do_execute(self, scn, start_point, left, right, bottom, up, chunksize):
        from collections import deque
        import collections
        self._stop = False
        for m in scn.get_models():
            if ('ty_down' in m.name or 'rock_ty_' in m.name or 'rock_scp_b01_yellow24433131' in m.name) and m.position.y < 0:
                m.active_collision = False

        global_data.game_mgr.show_tip('Start baking')
        print ('start baking', start_point, left, right, bottom, up, chunksize)
        start_point.x = (floor(start_point.x / 13) + 0.5) * 13
        start_point.z = (floor(start_point.z / 13) + 0.5) * 13
        self._job_args = (
         scn, start_point, left, right, bottom, up, chunksize)
        self._job_args_backup = (scn, start_point, left, right, bottom, up, chunksize)
        scene_col = scn.scene_col
        lut = [INVALID_VALUE] * 4096 * 4096
        self._job_lut = lut
        self._visit_counts = collections.defaultdict(int)
        self._visit_set = collections.defaultdict(set)
        self._job_trace = []
        ret = scene_col.hit_by_ray(start_point + math3d.vector(0, 100, 0), start_point + math3d.vector(0, -100, 0))
        if ret[0]:
            point = ret[1]
        else:
            raise ValueError('Invalid Start point')
        queue = deque(maxlen=len(lut))
        queue.append((point, point))
        self._job_queue = queue

    def update(self):
        if self._job_args:
            if self._do_update(*self._job_args):
                self._job_args = ()
        elif self._job_args_backup:
            scn = self._job_args_backup[0]
            self._update_draw_range(scn.active_camera.position)

    def is_idle(self):
        return not self._job_args

    def stop(self):
        self._stop = True

    def _do_update(self, scn, start_point, left, right, bottom, up, chunksize):
        for m in scn.get_models():
            if ('ty_down' in m.name or 'rock_ty_' in m.name or 'rock_scp_b01_yellow24433131' in m.name) and m.position.y < 0:
                m.active_collision = False

        queue = self._job_queue
        lut = self._job_lut
        scene_col = scn.scene_col
        trace_vec = self._job_trace
        visit_set = self._visit_set
        visit_count = self._visit_counts
        ray_test_func = self._sample_1m
        to_grid = self._to_grid
        iter_adj = self._iter_adj
        left_nx = (left - 0.5) * chunksize + chunksize / 64
        right_nx = (right + 0.5) * chunksize - chunksize / 64
        bottom_nx = (bottom - 0.5) * chunksize + chunksize / 64
        up_nx = (up + 0.5) * chunksize - chunksize / 64
        iter_count = 0
        while queue:
            point, from_point = queue.popleft()
            height = ray_test_func(scene_col, point, from_point)
            if height is not None:
                iheight = int(height)
                _id = to_grid(point, left, right, bottom, up, chunksize)
                if iheight not in visit_set[_id]:
                    point.y = height
                    visit_set[_id].add(iheight)
                    for new_point in iter_adj(point, left_nx, right_nx, bottom_nx, up_nx, chunksize):
                        queue.append((new_point, point))

                    if len(visit_set[_id]) > 100:
                        print (
                         'something wrong, break and check:', _id)
                        queue.clear()
                        break
                if lut[_id] > iheight:
                    lut[_id] = iheight
                    visit_count[_id] += 1
                    if visit_count[_id] > 10:
                        print (
                         'something wrong, break and check:', _id)
                        queue.clear()
                        break
            iter_count += 1
            if iter_count == 50000:
                break
            if len(queue) == len(lut):
                print 'queue full, break'
                queue.clear()
                break

        print (
         'iter times', iter_count, 'queue size', len(queue))
        if not queue:
            import struct
            with open('heightmap.bin', 'wb') as f:
                f.write(struct.pack('{}i'.format(len(lut)), *lut))
            global_data.game_mgr.show_tip('Finish baking')
            print 'Finish baking'
            self._draw_debug(scn, start_point, lut, left, right, bottom, up, chunksize)
            return True
        else:
            return

    def _sample_1m(self, scene_col, point, from_point):
        origin_height = from_point.y
        step_height = STEP_HEIGHT
        top_height = 10000
        ver_raytest = self._ver_raytest
        hor_raytest = self._hor_raytest
        ret = ver_raytest(scene_col, from_point, from_point + math3d.vector(0, top_height, 0))
        if ret:
            top_height = ret.y - origin_height - STEP_HEIGHT
            if top_height < 0:
                return None
        step_height = min(step_height, top_height)
        from_point.y = origin_height + step_height
        point.y = origin_height + step_height
        is_hit = hor_raytest(scene_col, from_point, point)
        iter = 0
        aggressive_try = 0
        loop = is_hit
        while loop and iter < 20 and step_height < top_height:
            iter += 1
            from_point.y = origin_height + step_height
            point.y = origin_height + step_height
            step_height += STEP_HEIGHT
            is_hit = hor_raytest(scene_col, from_point, point)
            loop = is_hit
            if is_hit is False:
                loop = aggressive_try == 0
                aggressive_try += 1

        check_point = math3d.vector(point)
        from_point.y = origin_height
        point.y = origin_height
        if is_hit:
            return None
        else:
            ret = ver_raytest(scene_col, check_point, math3d.vector(point.x, origin_height - 10000, point.z), 0)
            if ret:
                return ret.y
            return None

    def _ver_raytest(self, scene_col, from_point, point, min_dist=STEP_WIDTH):
        hit_by_ray = scene_col.hit_by_ray
        ret_0 = hit_by_ray(from_point, point)
        ret_1 = hit_by_ray(from_point + _tmp_x_n, point + _tmp_x_n)
        ret_2 = hit_by_ray(from_point + _tmp_x_p, point + _tmp_x_p)
        ret_3 = hit_by_ray(from_point + _tmp_z_n, point + _tmp_z_n)
        ret_4 = hit_by_ray(from_point + _tmp_z_p, point + _tmp_z_p)
        frac = None
        for ret in [ret_0, ret_1, ret_2, ret_3, ret_4]:
            if ret[0]:
                frac = min(ret[3], frac) if frac is not None else ret[3]

        if frac is None:
            return
        else:
            dist = point - from_point
            frac = frac - min_dist / abs(dist.y)
            if frac <= 0:
                return from_point
            return from_point + dist * frac

    def _hor_raytest(self, scene_col, from_point, point, threshold_hit=2):
        hit_by_ray = scene_col.hit_by_ray
        ret_0 = hit_by_ray(from_point, point)
        if ret_0[0]:
            return True
        ret_1 = hit_by_ray(from_point + _tmp_x_n + _tmp_y_p, point + _tmp_x_n + _tmp_y_p)
        ret_2 = hit_by_ray(from_point + _tmp_x_p + _tmp_y_p, point + _tmp_x_p + _tmp_y_p)
        ret_3 = hit_by_ray(from_point + _tmp_z_n + _tmp_y_p, point + _tmp_z_n + _tmp_y_p)
        ret_4 = hit_by_ray(from_point + _tmp_z_p + _tmp_y_p, point + _tmp_z_p + _tmp_y_p)
        hit_count = 0
        for ret in [ret_1, ret_2, ret_3, ret_4]:
            if ret[0]:
                hit_count += 1

        return hit_count >= threshold_hit

    def _to_grid(self, point, left, right, bottom, up, chunk_size):
        grid_x = floor(point.x / chunk_size + 0.5)
        grid_z = floor(point.z / chunk_size + 0.5)
        origin_x = (grid_x - 0.5) * chunk_size
        origin_z = (grid_z - 0.5) * chunk_size
        sub_size = chunk_size / 64
        sub_x = floor((point.x - origin_x) / sub_size)
        sub_z = floor((point.z - origin_z) / sub_size)
        val = int(((grid_z - bottom) * 64 + (grid_x - left)) * 4096 + sub_z * 64 + sub_x)
        x_z = val // 4096
        test_grid_x, test_grid_z = x_z % 64 + left, x_z // 64 + bottom
        sub_x_z = val % 4096
        test_sub_x, test_sub_z = sub_x_z % 64, sub_x_z // 64
        if test_grid_x == grid_x and test_grid_z == grid_z and test_sub_x == sub_x and test_sub_z == sub_z:
            pass
        else:
            print 'grid_x: {}, grid_z: {}, sub_x: {}, sub_z: {}'.format(grid_x, grid_z, sub_x, sub_z)
        return val

    def _iter_adj(self, point, left_nx, right_nx, bottom_nx, up_nx, chunksize):
        sub_size = chunksize / 64
        if left_nx < point.x < right_nx and bottom_nx < point.z < up_nx:
            yield point + math3d.vector(sub_size, 0, 0)
            yield point + math3d.vector(-sub_size, 0, 0)
            yield point + math3d.vector(0, 0, sub_size)
            yield point + math3d.vector(0, 0, -sub_size)
        if right_nx > point.x + sub_size * 5:
            yield point + math3d.vector(sub_size * 5, 0, 0)
        if left_nx < point.x - sub_size * 5:
            yield point + math3d.vector(-sub_size * 5, 0, 0)
        if bottom_nx < point.z - sub_size * 5:
            yield point + math3d.vector(0, 0, sub_size * 5)
        if up_nx > point.z + sub_size * 5:
            yield point + math3d.vector(0, 0, -sub_size * 5)

    def update_draw_debug(self, start_point):
        scn, _, left, right, bottom, up, chunksize = self._job_args_backup
        self._draw_debug(scn, start_point, self._job_lut, left, right, bottom, up, chunksize)

    def _draw_debug(self, scn, start_point, lut, left, right, bottom, up, chunk_size):
        self._reset_debug_data()
        min_i = len(lut)
        max_i = 0
        self._this_frame_i = 0
        self._update_draw_range(start_point)

    def _update_draw_range(self, view_pos):
        scn, start_point, left, right, bottom, up, chunk_size = self._job_args_backup
        grid_x = floor(view_pos.x / chunk_size + 0.5)
        grid_z = floor(view_pos.z / chunk_size + 0.5)
        if grid_x < left or grid_x > right or grid_z < bottom or grid_z > up:
            return
        grids_to_draw = [
         (
          grid_x - 1, grid_z - 1),
         (
          grid_x + 1, grid_z - 1),
         (
          grid_x - 1, grid_z + 1),
         (
          grid_x + 1, grid_z + 1),
         (
          grid_x - 1, grid_z),
         (
          grid_x + 1, grid_z),
         (
          grid_x, grid_z - 1),
         (
          grid_x, grid_z + 1),
         (
          grid_x, grid_z)]
        segments_to_draw = []
        debug_models_ids = []
        tmp_model_pool_blue = []
        for grid_x, grid_z in grids_to_draw:
            start_id = int(((grid_z - bottom) * 64 + (grid_x - left)) * 4096)
            end_id = start_id + 4096
            segments_to_draw.append((start_id, end_id))
            debug_models_ids += list(range(start_id, end_id))

        debug_models_created = self._debug_models_lut
        to_reuse = []
        for _id, m in self._debug_models_lut.items():
            is_insert = False
            for segment in segments_to_draw:
                if segment[0] <= _id and _id < segment[1]:
                    is_insert = True

            if not is_insert:
                to_reuse.append(_id)

        for _id in to_reuse:
            tmp_model_pool_blue.append(debug_models_created.pop(_id))

        lut = self._job_lut
        res_obj_blue = world.create_res_object('model_new/others/look_dev/box.gim')
        sub_size = chunk_size / 64
        global_model_pool_blue, global_model_pool_red = self._model_pools[0], self._model_pools[1]
        max_i = len(debug_models_ids)
        t = 100
        t2 = 10000
        i = self._this_frame_i
        while t and t2:
            t -= 1
            t2 -= 1
            i += 1
            if i >= max_i:
                i = 0
            ids = debug_models_ids[i]
            height = lut[ids]
            x_z = ids // 4096
            grid_x, grid_z = x_z % 64 + left, x_z // 64 + bottom
            sub_x_z = ids % 4096
            sub_x, sub_z = sub_x_z % 64, sub_x_z // 64
            x = (sub_x + 0.5) * sub_size + (grid_x - 0.5) * chunk_size
            z = (sub_z + 0.5) * sub_size + (grid_z - 0.5) * chunk_size
            if height != INVALID_VALUE:
                pos = math3d.vector(x, height, z)
                tmp_model_pool = tmp_model_pool_blue
                global_model_pool = global_model_pool_blue
                res_obj = res_obj_blue
                has_created = ids in self._debug_models_lut
                dist = pos - view_pos
                dist.y = 0
                if dist.length_sqr < 4000000:
                    if not has_created:
                        if tmp_model_pool:
                            m = tmp_model_pool.pop()
                        elif global_model_pool:
                            m = global_model_pool.pop()
                            scn.add_object(m)
                        else:
                            m = world.model(res_obj, scn)
                        m.position = math3d.vector(x, height, z)
                        m.pickable = True
                        m.set_attr('ID', str(ids))
                        self._debug_models_lut[ids] = m
                elif has_created:
                    tmp_model_pool.append(self._debug_models_lut.pop(ids))
                else:
                    t += 1

        for m in tmp_model_pool_blue:
            m.remove_from_parent()
            global_model_pool_blue.append(m)

        self._this_frame_i = i

    def on_pick_model(self, model):
        self._reset_debug_data()
        trace_vec = self._job_trace
        trace_id = int(model.get_attr('ID'))
        scn = model.get_scene()
        _tmp_last = self._add_debug_data(scn, model.position)
        print (
         'trace_id', trace_id, model.position)
        trace_deep = 100
        pos = model.position
        scale_one = math3d.vector(1.3, 1.3, 1.3)
        for p, fp in reversed(trace_vec):
            if abs(p.x - pos.x) < 0.1 and abs(p.z - pos.z) < 0.1:
                _tmp_last.scale = scale_one
                _tmp_last = self._add_debug_data(scn, fp, scale=2.0)
                pos = fp
                trace_deep -= 1
                if trace_deep == 0:
                    break

    def _add_debug_data(self, scn, pos, scale=1.3):
        _hight_obj_pools = self._hight_obj_pools
        if _hight_obj_pools:
            model = _hight_obj_pools.pop()
            scn.add_object(model)
        else:
            model = world.model('model_new/others/look_dev/box2.gim', scn)
        model.position = pos
        model.all_materials.set_var(_HASH_CHANGE_COLOR, 'u_change_color', (1.0, 0.0,
                                                                           0.0, 1.0))
        model.scale = math3d.vector(scale, scale, scale)
        self._last_highlight_objects.append(model)
        return model

    def _reset_debug_data(self):
        if self._last_highlight_objects:
            pool = self._hight_obj_pools
            for m in self._last_highlight_objects:
                m.remove_from_parent()
                pool.append(m)

            self._last_highlight_objects = []

    def draw_trace(self, trace_id):
        model = self._debug_models_lut.get(trace_id)
        if model is None:
            print "can't find {} type {}".format(trace_id, type(trace_id))
            return
        else:
            self.on_pick_model(model)
            return

    def load(self, scene):
        lut = None
        import struct
        with open('bw_all06.bin', 'rb') as f:
            lut = struct.unpack('{}i'.format(16777216), f.read())
        if lut:
            self._job_lut = lut
            left, right, bottom, up, chunksize = scene.get_scene_map_uv_parameters()
            self._job_args_backup = (scene, scene.viewer_position, left, right, bottom, up, chunksize)
        return


g_baker = RayTestHeightMapBaker()
global_data.g_baker = g_baker

class PartTravelWorld(ScenePart.ScenePart):

    def __init__(self, scene, name):
        super(PartTravelWorld, self).__init__(scene, name, True)
        self._is_loaded = True
        self._total_time = 0
        self._last_report_time = 0
        self._start_point = math3d.vector(0, 0, 0)
        self._args = (-1, 1, -1, 1, 832)
        self._chunksize = 1

    def on_enter(self):
        left, right, bottom, up, chunksize = self.scene().get_scene_map_uv_parameters()
        load_range = max(abs(left), abs(right), abs(up), abs(bottom)) * chunksize
        landscape = self.scene().landscape
        if landscape:
            landscape.set_dis_param(chunksize, load_range)
        self._start_point = math3d.vector(0, 250, 0)
        self._args = (left, right, bottom, up, chunksize)
        self.register_keys()

    def on_debug_baker(self, start_point):
        ret = self.scene().scene_col.hit_by_ray(start_point, start_point - math3d.vector(0, 1000, 0))
        if ret[0]:
            start_point = ret[1]
            self._start_point = start_point
            left, right, bottom, up, chunksize = self.scene().get_scene_map_uv_parameters()
            bake_range = 3
            grid_x = floor(start_point.x / chunksize + 0.5)
            grid_z = floor(start_point.z / chunksize + 0.5)
            self._args = (
             max(left, grid_x - bake_range), min(right, grid_x + bake_range), max(bottom, grid_z - bake_range),
             min(up, grid_z + bake_range), chunksize)
            left, right, bottom, up, _ = self._args
            load_range = bake_range * chunksize
            print ('load_range:', load_range)
            global_data.game_mgr.show_tip('Prepare baking')
            self.scene().set_view_range(0, load_range)
            landscape = self.scene().landscape
            if landscape:
                landscape.set_dis_param(chunksize, load_range)
                landscape.set_LandscapeViewRange(load_range)
                landscape.set_LandscapeColRange(load_range)
                landscape.screen_space_error_bound = 150.0

            def delay_start():
                self._is_loaded = False

            game3d.delay_exec(1000, delay_start)
        else:
            print (
             'invalid start point', start_point)
            global_data.game_mgr.show_tip('Invalid start point')

    def on_update(self, dt):
        super(PartTravelWorld, self).on_update(dt)
        if self._is_loaded:
            g_baker.update()
            return
        self._total_time += dt
        self._last_report_time += dt
        scn = self.scene()
        landscape = scn.landscape
        p = scn.get_progress()
        if landscape:
            p = p * 0.5 + landscape.getLoadingProgress() * 0.5
            if landscape.is_loading_detail_collision():
                p = p * 0.5
        if p >= 1.0 and g_baker.is_idle():
            print '[LOADING] loading complete, total time:{}s'.format(self._total_time)
            g_baker.execute(scn, self._start_point, *self._args)
            self._is_loaded = True
            self._total_time = 0
        if self._last_report_time > 10:
            self._last_report_time = 0
            print ('[LOADING] loading progress:', p)

    def register_keys(self):
        import game
        game.add_key_handler(game.MSG_KEY_DOWN, (
         game.VK_B, game.VK_V, game.VK_M, game.VK_L), self._key_handler)

    def unregister_keys(self):
        import game
        game.remove_key_handler(game.MSG_KEY_DOWN, (
         game.VK_B, game.VK_V, game.VK_M, game.VK_L), self._key_handler)

    def _key_handler(self, msg, keycode):
        import game
        if keycode == game.VK_B:
            self.on_debug_baker(self.scene().viewer_position)
        if keycode == game.VK_V:
            g_baker.update_draw_debug(self.scene().viewer_position)
        if keycode == game.VK_M:
            g_baker.stop()
        if keycode == game.VK_L:
            g_baker.load(self.scene())

    def on_touch_tap(self, touch):
        from common.utils.cocos_utils import cocos_pos_to_neox
        lo = touch.getLocation()
        x, y = cocos_pos_to_neox(lo.x, lo.y)
        model, _, _ = self.scene().pick(x, y, None, 1)
        if model:
            g_baker.on_pick_model(model)
        return