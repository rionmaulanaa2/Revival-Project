# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/manager_agents/DebugManagerAgent.py
from __future__ import absolute_import
from __future__ import print_function
from logic.manager_agents import ManagerAgentBase
from common.platform import is_win32
import six.moves.builtins
import render
import game3d
import os
import shutil

class DebugManagerAgent(ManagerAgentBase.ManagerAgentBase):
    ALIAS_NAME = 'debug_mgr_agent'

    def init(self, *args):
        super(DebugManagerAgent, self).init()
        if is_win32():
            from common.debug import dcommand
            dcommand.init()
            import profiling
            six.moves.builtins.__dict__['profiling'] = profiling
            import logic.gutils.gen_diffuse_utils as gdu
            gdu.init_global_function()
        from common.utils.reloadshader import reload_one
        six.moves.builtins.__dict__['reload_shader'] = reload_one
        try:
            from common.debug import debug_util
            self.map_skin = debug_util.map_skin
        except:
            pass

        self.prof_framenum = 0
        self.prof_tottime = 0
        self.prof_avetime = 0
        self._profiler = None
        self._dump_stream = None
        import logic.comsys.profile_logger.PerfSys as PS
        PS.PerfSys()
        six.moves.builtins.__dict__['lift'] = self.lift
        return

    def start_gtrace_profile(self, duration=600, interval=20, path='/sdcard/prof.gt'):
        import gtrace
        gtrace.start(interval, duration)
        global_data.game_mgr.show_tip('Begin gtrace profile')

        def _on_gtrace_timeout():
            gtrace.stop(path)
            global_data.game_mgr.show_tip('Finish gtrace profile with file: {}'.format(path))

        game3d.delay_exec(duration * 1000, _on_gtrace_timeout)

    def start_profile(self):
        import cProfile
        global_data.game_mgr.show_tip('Begin Profile')
        self.stop_profile()
        self._profiler = cProfile.Profile()
        self._profiler.enable()

    def stop_profile--- This code section failed: ---

  70       0  LOAD_GLOBAL           0  'hasattr'
           3  LOAD_GLOBAL           1  'pstats'
           6  CALL_FUNCTION_2       2 
           9  POP_JUMP_IF_TRUE     16  'to 16'

  71      12  LOAD_CONST            0  ''
          15  RETURN_END_IF    
        16_0  COME_FROM                '9'

  72      16  LOAD_CONST            2  ''
          19  LOAD_CONST            0  ''
          22  IMPORT_NAME           1  'pstats'
          25  STORE_FAST            2  'pstats'

  73      28  LOAD_CONST            2  ''
          31  LOAD_CONST            0  ''
          34  IMPORT_NAME           2  'time'
          37  STORE_FAST            3  'time'

  74      40  LOAD_CONST            2  ''
          43  LOAD_CONST            0  ''
          46  IMPORT_NAME           3  'six_ex.moves.StringIO'
          49  STORE_FAST            4  'six_ex'

  75      52  LOAD_FAST             0  'self'
          55  LOAD_ATTR             4  '_profiler'
          58  LOAD_ATTR             5  'disable'
          61  CALL_FUNCTION_0       0 
          64  POP_TOP          

  76      65  LOAD_FAST             4  'six_ex'
          68  LOAD_ATTR             6  'moves'
          71  LOAD_ATTR             7  'StringIO'
          74  LOAD_ATTR             7  'StringIO'
          77  CALL_FUNCTION_0       0 
          80  STORE_FAST            5  's'

  77      83  LOAD_FAST             2  'pstats'
          86  LOAD_ATTR             8  'Stats'
          89  LOAD_FAST             0  'self'
          92  LOAD_ATTR             4  '_profiler'
          95  LOAD_CONST            3  'stream'
          98  LOAD_FAST             5  's'
         101  CALL_FUNCTION_257   257 
         104  STORE_FAST            6  'ps'

  78     107  LOAD_FAST             6  'ps'
         110  LOAD_ATTR             9  'sort_stats'
         113  LOAD_CONST            4  'cumulative'
         116  LOAD_CONST            5  'calls'
         119  CALL_FUNCTION_2       2 
         122  POP_TOP          

  79     123  LOAD_GLOBAL          10  'print'
         126  LOAD_CONST            6  'profile end by cumulative '
         129  LOAD_FAST             3  'time'
         132  LOAD_ATTR            11  'asctime'
         135  LOAD_FAST             3  'time'
         138  LOAD_ATTR            12  'localtime'
         141  LOAD_FAST             3  'time'
         144  LOAD_ATTR             2  'time'
         147  CALL_FUNCTION_0       0 
         150  CALL_FUNCTION_1       1 
         153  CALL_FUNCTION_1       1 
         156  CALL_FUNCTION_2       2 
         159  POP_TOP          

  80     160  LOAD_FAST             6  'ps'
         163  LOAD_ATTR            13  'print_stats'
         166  LOAD_FAST             1  'count'
         169  CALL_FUNCTION_1       1 
         172  POP_TOP          

  81     173  LOAD_GLOBAL          10  'print'
         176  LOAD_FAST             5  's'
         179  LOAD_ATTR            14  'getvalue'
         182  CALL_FUNCTION_0       0 
         185  CALL_FUNCTION_1       1 
         188  POP_TOP          

  82     189  LOAD_FAST             4  'six_ex'
         192  LOAD_ATTR             6  'moves'
         195  LOAD_ATTR             7  'StringIO'
         198  LOAD_ATTR             7  'StringIO'
         201  CALL_FUNCTION_0       0 
         204  STORE_FAST            5  's'

  83     207  LOAD_FAST             5  's'
         210  LOAD_FAST             6  'ps'
         213  STORE_ATTR           15  'stream'

  84     216  LOAD_GLOBAL          10  'print'
         219  LOAD_CONST            7  'profile end by time '
         222  LOAD_FAST             3  'time'
         225  LOAD_ATTR            11  'asctime'
         228  LOAD_FAST             3  'time'
         231  LOAD_ATTR            12  'localtime'
         234  LOAD_FAST             3  'time'
         237  LOAD_ATTR             2  'time'
         240  CALL_FUNCTION_0       0 
         243  CALL_FUNCTION_1       1 
         246  CALL_FUNCTION_1       1 
         249  CALL_FUNCTION_2       2 
         252  POP_TOP          

  85     253  LOAD_FAST             6  'ps'
         256  LOAD_ATTR             9  'sort_stats'
         259  LOAD_CONST            8  'time'
         262  CALL_FUNCTION_1       1 
         265  POP_TOP          

  86     266  LOAD_FAST             6  'ps'
         269  LOAD_ATTR            13  'print_stats'
         272  LOAD_FAST             1  'count'
         275  CALL_FUNCTION_1       1 
         278  POP_TOP          

  87     279  LOAD_GLOBAL          10  'print'
         282  LOAD_FAST             5  's'
         285  LOAD_ATTR            14  'getvalue'
         288  CALL_FUNCTION_0       0 
         291  CALL_FUNCTION_1       1 
         294  POP_TOP          

  88     295  LOAD_GLOBAL          16  'global_data'
         298  LOAD_ATTR            17  'game_mgr'
         301  LOAD_ATTR            18  'show_tip'
         304  LOAD_CONST            9  'Finished Profile'
         307  CALL_FUNCTION_1       1 
         310  POP_TOP          

  89     311  LOAD_FAST             0  'self'
         314  DELETE_ATTR           4  '_profiler'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 6

    def start_cprofile_dump(self):
        import cProfile
        self._profiler = cProfile.Profile()
        self.reset_cprofile_dump()

    def reset_cprofile_dump(self):
        doc_dir = game3d.get_doc_dir()
        dump_dir = '%s/profiles' % doc_dir
        if os.path.exists(dump_dir):
            shutil.rmtree(dump_dir)
        os.makedirs(dump_dir)
        self.prof_framenum = 0
        self.prof_tottime = 0
        self.prof_avetime = 0

    def stop_cprofile_dump(self):
        pass

    def single_frame_update_dump(self, game_mgr_instance):
        from common.utils.time_utils import get_time
        import cProfile
        import pstats
        import os
        import six_ex.moves.cStringIO
        t = get_time()
        _doc_dir = game3d.get_doc_dir()
        if not os.path.exists(_doc_dir):
            os.mkdir(_doc_dir)
        cProfile.runctx('game_mgr_instance.logic_update()', globals(), locals(), _doc_dir + '/' + 'dump_logic_%f.prof' % t)
        if not self._dump_stream:
            self._dump_stream = six_ex.moves.cStringIO.StringIO()
        self._dump_stream.reset()
        p = pstats.Stats(_doc_dir + '/' + 'dump_logic_%f.prof' % t, stream=self._dump_stream)
        p.strip_dirs().sort_stats('tottime', 'cumtime').print_stats(10)
        str_tottime = self._dump_stream.getvalue()
        self._dump_stream.reset()
        p.strip_dirs().sort_stats('cumtime', 'tottime').print_stats(20)
        str_cumtime = self._dump_stream.getvalue()
        if self._dump_cb:
            self._dump_cb((str_tottime, str_cumtime))
            self._dump_cb = None
        return

    def avrg_frame_update_dump(self, game_mgr_instance):
        self._profiler.runctx('game_mgr_instance.logic_update()', None, {'self': game_mgr_instance})
        doc_dir = game3d.get_doc_dir()
        totaltime = 0
        for s in self._profiler.getstats():
            totaltime += s.inlinetime

        self.prof_tottime += totaltime
        self.prof_framenum += 1
        if totaltime > self.prof_avetime:
            self._profiler.dump_stats('%s/profiles/g93_%07d.prof' % (doc_dir, int(totaltime * 10000000)))
        self.prof_avetime = self.prof_tottime / self.prof_framenum
        self._profiler.clear()
        return

    def dump_one_frame(self, cb=None):
        self._dump_cb = cb
        global_data.game_mgr.start_cprofile_dump()

    def lift(self, height=2000):
        if global_data.player and global_data.player.logic:
            pos = global_data.player.logic.ev_g_position()
            global_data.player.wiz_command('goto {} {} {}'.format(pos.x, pos.y + height, pos.z))