# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/part_sys/SysMapQuickMark.py
from __future__ import absolute_import
from __future__ import print_function
import six
from logic.vscene.part_sys.ScenePartSysBase import ScenePartSysBase
from common.algorithm import resloader
import math3d
LEADING_LINE_PATH = 'effect/fx/scenes/common/biaozhi/yindaoxian.sfx'
QUICK_MARK_PATH = 'effect/fx/scenes/common/biaozhi/yindaoxian_01.sfx'
MAKR_TYPE_GO = 'effect/fx/scenes/common/biaozhi/yindaoxian_01.sfx'

class SysMapQuickMark(ScenePartSysBase):

    def __init__(self):
        super(SysMapQuickMark, self).__init__()
        self.init_leading_line()
        self.init_event()

    def init_leading_line(self):
        self.leading_line_sfx_task = None
        self.leading_line_sfx = None
        self.leading_line_pts = None
        self.leading_line_visible = False
        self.team_mark_sfx_info = {}
        return

    def init_event(self):
        global_data.emgr.scene_draw_leading_line_event += self.draw_leading_line
        global_data.emgr.scene_remove_leading_line_event += self.remove_leading_line
        global_data.emgr.show_scene_quick_mark += self.show_scene_quick_mark
        global_data.emgr.add_scene_mark += self.show_scene_team_mark
        global_data.emgr.remove_scene_mark += self.remove_scene_mark
        global_data.emgr.remove_scene_mark_by_type += self.remove_scene_mark_by_type

    def show_scene_quick_mark(self, position):
        pass

    def show_scene_team_mark(self, eid, i_type, v3d_pos, extra_args=None):
        if eid in self.team_mark_sfx_info:
            if i_type in self.team_mark_sfx_info[eid]:
                infos = self.team_mark_sfx_info[eid][i_type]
                for id_sfx, pos in infos:
                    if pos == v3d_pos:
                        return

        def create_cb(sfx):
            sfx.scale = math3d.vector(0.2, 0.2, 0.2)

        sid = global_data.sfx_mgr.create_sfx_in_scene(MAKR_TYPE_GO, v3d_pos, on_create_func=create_cb)
        if eid not in self.team_mark_sfx_info:
            self.team_mark_sfx_info[eid] = {}
        if i_type not in self.team_mark_sfx_info[eid]:
            self.team_mark_sfx_info[eid][i_type] = []
        self.team_mark_sfx_info[eid][i_type].append((sid, v3d_pos))

    def remove_scene_mark_by_type(self, eid, i_type):
        if eid in self.team_mark_sfx_info:
            if i_type in self.team_mark_sfx_info[eid] and self.team_mark_sfx_info[eid][i_type]:
                id_sfx, _ = self.team_mark_sfx_info[eid][i_type].pop(0)
                global_data.sfx_mgr.remove_sfx_by_id(id_sfx)
                if not self.team_mark_sfx_info[eid][i_type]:
                    del self.team_mark_sfx_info[eid][i_type]
            if not self.team_mark_sfx_info[eid]:
                del self.team_mark_sfx_info[eid]

    def remove_scene_mark(self, eid):
        if eid in self.team_mark_sfx_info:
            for i_type, infos in six.iteritems(self.team_mark_sfx_info[eid]):
                for id_sfx, _ in infos:
                    global_data.sfx_mgr.remove_sfx_by_id(id_sfx)

            del self.team_mark_sfx_info[eid]

    def show_leading_line(self):
        print('show leading line')
        sfx = self.leading_line_sfx
        sfx.visible = True
        sfx.restart()
        sfx.position = self.leading_line_pts[0]
        sfx.end_pos = self.leading_line_pts[1]

    def hide_leading_line(self):
        if self.leading_line_sfx:
            self.leading_line_sfx.visible = False
            self.leading_line_sfx.shutdown()

    def leading_line_load_cb(self, sfx, *args):
        self.get_scene().add_object(sfx)
        if self.leading_line_visible:
            self.show_leading_line()
        else:
            self.hide_leading_line()

    def draw_leading_line--- This code section failed: ---

  99       0  LOAD_GLOBAL           0  'True'
           3  LOAD_FAST             0  'self'
           6  STORE_ATTR            1  'leading_line_visible'

 100       9  LOAD_FAST             1  'pts'
          12  LOAD_FAST             0  'self'
          15  STORE_ATTR            2  'leading_line_pts'

 101      18  LOAD_FAST             0  'self'
          21  LOAD_ATTR             3  'leading_line_sfx'
          24  POP_JUMP_IF_FALSE    40  'to 40'

 102      27  LOAD_FAST             0  'self'
          30  LOAD_ATTR             4  'show_leading_line'
          33  CALL_FUNCTION_0       0 
          36  POP_TOP          
          37  JUMP_FORWARD         40  'to 80'

 103      40  LOAD_FAST             0  'self'
          43  LOAD_ATTR             5  'leading_line_sfx_task'
          46  POP_JUMP_IF_TRUE     80  'to 80'

 104      49  LOAD_GLOBAL           6  'resloader'
          52  LOAD_ATTR             7  'load_res_attr'
          55  LOAD_ATTR             1  'leading_line_visible'
          58  LOAD_GLOBAL           8  'LEADING_LINE_PATH'
          61  LOAD_FAST             0  'self'
          64  LOAD_ATTR             9  'leading_line_load_cb'
          67  LOAD_CONST            0  ''
          70  LOAD_CONST            2  'SFX'
          73  CALL_FUNCTION_6       6 
          76  POP_TOP          
          77  JUMP_FORWARD          0  'to 80'
        80_0  COME_FROM                '77'
        80_1  COME_FROM                '37'
          80  LOAD_CONST            0  ''
          83  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_6' instruction at offset 73

    def remove_leading_line(self):
        self.leading_line_visible = False
        self.hide_leading_line()

    def destroy--- This code section failed: ---

 111       0  LOAD_GLOBAL           0  'resloader'
           3  LOAD_ATTR             1  'del_res_attr'
           6  LOAD_ATTR             1  'del_res_attr'
           9  CALL_FUNCTION_2       2 
          12  POP_TOP          

Parse error at or near `CALL_FUNCTION_2' instruction at offset 9