# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/platform/hubble.py
from __future__ import absolute_import
from __future__ import print_function
import device_compatibility
from common.framework import Singleton
from common.cfg import confmgr
from mobile.mobilerpc import SimpleHttpClient2, HttpBase
import json
import six.moves.urllib.request
import six.moves.urllib.error
import six.moves.urllib.parse
import json
import profiling
import time
from logic.gcommon import time_utility
from logic.comsys.login.LoginSetting import LoginSetting
from logic.gcommon.common_const import ui_operation_const as uoc
import version
from common.utils import timer
import random
from device_compatibility import is_ios_support_astc
import game3d
import render
FRAME_MODE = {0: '30\xe5\xb8\xa7',1: '60\xe5\xb8\xa7',2: '144\xe5\xb8\xa7',3: '90\xe5\xb8\xa7',4: '45\xe5\xb8\xa7'}

class Hubble(Singleton):
    ALIAS_NAME = 'hubble'
    CD_TIME = 1

    def init(self):
        self._timer = None
        self._statistics_clock_timer = None
        self._statistics_logic_timer = None
        self.login_time = 0
        self._data = {}
        self._statistics_data = {}
        self.httpclient = SimpleHttpClient2.SimpleAsyncHTTPClient2(max_clients=1)
        self.process_event(True)
        self.is_statistics_check = True
        return

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'avatar_finish_create_event': self.start_normal_check,
           'on_login_success_event': self.on_login_success,
           'loading_begin_event': self.loading_begin_func,
           'loading_end_event': self.loading_end_func
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def loading_begin_func(self):
        self.is_statistics_check = False

    def loading_end_func(self):
        self.is_statistics_check = True

    def on_finalize(self):
        self.stop_normal_check()
        self._statistics_clock_timer and global_data.game_mgr.get_logic_timer().unregister(self._statistics_clock_timer)
        self._statistics_clock_timer = None
        self._statistics_logic_timer and global_data.game_mgr.get_logic_timer().unregister(self._statistics_logic_timer)
        self._statistics_logic_timer = None
        self.process_event(False)
        return

    def get_enable(self):
        return confmgr.get('setting', 'hubble', default=False)

    def on_login_success(self):
        self.login_time = time.time()

    def get_login_time(self):
        return self.login_time

    def init_data(self):
        self._data = {'scope': 'test' if global_data.is_inner_server else 'release',
           'host_name': LoginSetting().last_logined_server.get('svr_name', 'None'),
           'host_id': global_data.channel._hostnum,
           'user_id': str(global_data.player.uid),
           'user_name': global_data.player.char_name,
           'platform': global_data.deviceinfo.get_os_name(),
           'engine_version': version.get_engine_version(),
           'script_version': version.get_script_version(),
           'device_model': global_data.deviceinfo.get_device_model(),
           'gpu_name': profiling.get_video_card_name(),
           'os_version': global_data.deviceinfo.get_os_ver(),
           'device_id': global_data.channel.get_udid(),
           'channel': global_data.channel.get_app_channel()
           }
        try:
            support_astc = False
            if game3d.get_platform() == game3d.PLATFORM_ANDROID:
                support_astc = device_compatibility.is_support_astc()
            elif game3d.get_platform() == game3d.PLATFORM_IOS:
                support_astc = is_ios_support_astc()
            self._data['support_astc'] = str(support_astc)
        except:
            pass

        if global_data.channel and global_data.channel.is_musdk():
            if 'nemud_player_uuid' not in self._data:
                import subprocess
                uuid_process = subprocess.Popen('getprop | grep nemud.player_uuid', shell=True, stdout=subprocess.PIPE)
                uuid_output = uuid_process.stdout.read().decode('utf-8')
                version_process = subprocess.Popen('getprop | grep nemud.player_version', shell=True, stdout=subprocess.PIPE)
                version_output = version_process.stdout.read().decode('utf-8')
                self._data['nemud_player_uuid'] = uuid_output
                self._data['nemud_player_version'] = version_output

    def can_statistics_check(self):
        player = global_data.player
        if not player:
            return
        is_in_battle = player.is_in_battle()

    def start_statistics_check(self):
        self._statistics_data = {}

        def on_clock_check--- This code section failed: ---

 130       0  LOAD_DEREF            0  'self'
           3  LOAD_ATTR             0  'is_statistics_check'
           6  POP_JUMP_IF_TRUE     13  'to 13'

 131       9  LOAD_CONST            0  ''
          12  RETURN_END_IF    
        13_0  COME_FROM                '6'

 132      13  LOAD_CONST            1  'multiple_fps'
          16  LOAD_DEREF            0  'self'
          19  LOAD_ATTR             1  '_statistics_data'
          22  COMPARE_OP            7  'not-in'
          25  POP_JUMP_IF_FALSE    44  'to 44'

 133      28  BUILD_MAP_0           0 
          31  LOAD_DEREF            0  'self'
          34  LOAD_ATTR             1  '_statistics_data'
          37  LOAD_CONST            1  'multiple_fps'
          40  STORE_SUBSCR     
          41  JUMP_FORWARD          0  'to 44'
        44_0  COME_FROM                '41'

 134      44  LOAD_DEREF            0  'self'
          47  LOAD_ATTR             1  '_statistics_data'
          50  LOAD_CONST            1  'multiple_fps'
          53  BINARY_SUBSCR    
          54  STORE_FAST            0  'multiple_fps'

 135      57  LOAD_GLOBAL           2  'profiling'
          60  LOAD_ATTR             3  'get_render_rate'
          63  CALL_FUNCTION_0       0 
          66  STORE_FAST            1  'fps'

 136      69  SETUP_LOOP          104  'to 176'
          72  LOAD_GLOBAL           4  'range'
          75  LOAD_CONST            2  12
          78  CALL_FUNCTION_1       1 
          81  GET_ITER         
          82  FOR_ITER             90  'to 175'
          85  STORE_FAST            2  'i'

 137      88  LOAD_FAST             1  'fps'
          91  LOAD_CONST            3  5
          94  LOAD_FAST             2  'i'
          97  LOAD_CONST            4  1
         100  BINARY_ADD       
         101  BINARY_MULTIPLY  
         102  COMPARE_OP            1  '<='
         105  POP_JUMP_IF_FALSE    82  'to 82'
         108  LOAD_FAST             1  'fps'
         111  LOAD_CONST            3  5
         114  LOAD_FAST             2  'i'
         117  BINARY_MULTIPLY  
         118  COMPARE_OP            4  '>'
       121_0  COME_FROM                '105'
         121  POP_JUMP_IF_FALSE    82  'to 82'

 138     124  LOAD_CONST            5  'fps_%d'
         127  LOAD_CONST            3  5
         130  LOAD_FAST             2  'i'
         133  LOAD_CONST            4  1
         136  BINARY_ADD       
         137  BINARY_MULTIPLY  
         138  BINARY_MODULO    
         139  STORE_FAST            3  'fps_key'

 139     142  LOAD_FAST             0  'multiple_fps'
         145  LOAD_ATTR             5  'get'
         148  LOAD_FAST             3  'fps_key'
         151  LOAD_CONST            6  ''
         154  CALL_FUNCTION_2       2 
         157  LOAD_CONST            4  1
         160  BINARY_ADD       
         161  LOAD_FAST             0  'multiple_fps'
         164  LOAD_FAST             3  'fps_key'
         167  STORE_SUBSCR     

 140     168  BREAK_LOOP       
         169  JUMP_BACK            82  'to 82'
         172  JUMP_BACK            82  'to 82'
         175  POP_BLOCK        
       176_0  COME_FROM                '69'

 141     176  LOAD_FAST             1  'fps'
         179  LOAD_CONST            7  60
         182  COMPARE_OP            4  '>'
         185  POP_JUMP_IF_FALSE   214  'to 214'

 142     188  LOAD_FAST             0  'multiple_fps'
         191  LOAD_ATTR             5  'get'
         194  LOAD_CONST            8  'fps_over_60'
         197  LOAD_CONST            6  ''
         200  CALL_FUNCTION_2       2 
         203  LOAD_CONST            4  1
         206  BINARY_ADD       
         207  BINARY_ADD       
         208  STORE_MAP        
         209  STORE_MAP        
         210  STORE_SUBSCR     
         211  JUMP_FORWARD          0  'to 214'
       214_0  COME_FROM                '211'

 143     214  LOAD_DEREF            0  'self'
         217  LOAD_ATTR             1  '_statistics_data'
         220  LOAD_ATTR             5  'get'
         223  LOAD_CONST            9  'mem_usage'
         226  LOAD_CONST            6  ''
         229  CALL_FUNCTION_2       2 
         232  LOAD_GLOBAL           2  'profiling'
         235  LOAD_ATTR             6  'get_process_mem_used'
         238  CALL_FUNCTION_0       0 
         241  BINARY_ADD       
         242  LOAD_DEREF            0  'self'
         245  LOAD_ATTR             1  '_statistics_data'
         248  LOAD_CONST            9  'mem_usage'
         251  STORE_SUBSCR     

 144     252  LOAD_DEREF            0  'self'
         255  LOAD_ATTR             1  '_statistics_data'
         258  LOAD_ATTR             5  'get'
         261  LOAD_CONST           10  'mem_available'
         264  LOAD_CONST            6  ''
         267  CALL_FUNCTION_2       2 
         270  LOAD_GLOBAL           2  'profiling'
         273  LOAD_ATTR             7  'get_total_memory'
         276  CALL_FUNCTION_0       0 
         279  LOAD_CONST           11  1024
         282  BINARY_MULTIPLY  
         283  LOAD_CONST           11  1024
         286  BINARY_MULTIPLY  
         287  LOAD_GLOBAL           2  'profiling'
         290  LOAD_ATTR             6  'get_process_mem_used'
         293  CALL_FUNCTION_0       0 
         296  BINARY_SUBTRACT  
         297  BINARY_ADD       
         298  LOAD_DEREF            0  'self'
         301  LOAD_ATTR             1  '_statistics_data'
         304  LOAD_CONST           10  'mem_available'
         307  STORE_SUBSCR     

 145     308  LOAD_DEREF            0  'self'
         311  LOAD_ATTR             1  '_statistics_data'
         314  LOAD_ATTR             5  'get'
         317  LOAD_CONST           12  'draw_call'
         320  LOAD_CONST            6  ''
         323  CALL_FUNCTION_2       2 
         326  LOAD_GLOBAL           2  'profiling'
         329  LOAD_ATTR             8  'get_dp_num'
         332  CALL_FUNCTION_0       0 
         335  BINARY_ADD       
         336  LOAD_DEREF            0  'self'
         339  LOAD_ATTR             1  '_statistics_data'
         342  LOAD_CONST           12  'draw_call'
         345  STORE_SUBSCR     

 146     346  LOAD_DEREF            0  'self'
         349  LOAD_ATTR             1  '_statistics_data'
         352  LOAD_ATTR             5  'get'
         355  LOAD_CONST           13  'fps'
         358  LOAD_CONST            6  ''
         361  CALL_FUNCTION_2       2 
         364  LOAD_FAST             1  'fps'
         367  BINARY_ADD       
         368  LOAD_DEREF            0  'self'
         371  LOAD_ATTR             1  '_statistics_data'
         374  LOAD_CONST           13  'fps'
         377  STORE_SUBSCR     

 147     378  LOAD_DEREF            0  'self'
         381  LOAD_ATTR             1  '_statistics_data'
         384  LOAD_ATTR             5  'get'
         387  LOAD_CONST           14  'vertex_count'
         390  LOAD_CONST            6  ''
         393  CALL_FUNCTION_2       2 
         396  LOAD_GLOBAL           2  'profiling'
         399  LOAD_ATTR             9  'get_prim_num'
         402  CALL_FUNCTION_0       0 
         405  BINARY_ADD       
         406  LOAD_DEREF            0  'self'
         409  LOAD_ATTR             1  '_statistics_data'
         412  LOAD_CONST           14  'vertex_count'
         415  STORE_SUBSCR     

 148     416  LOAD_DEREF            0  'self'
         419  LOAD_ATTR             1  '_statistics_data'
         422  LOAD_ATTR             5  'get'
         425  LOAD_CONST           15  'statistics_clock_times'
         428  LOAD_CONST            6  ''
         431  CALL_FUNCTION_2       2 
         434  LOAD_CONST            4  1
         437  BINARY_ADD       
         438  LOAD_DEREF            0  'self'
         441  LOAD_ATTR             1  '_statistics_data'
         444  LOAD_CONST           15  'statistics_clock_times'
         447  STORE_SUBSCR     

Parse error at or near `BINARY_ADD' instruction at offset 207

        self._statistics_clock_timer and global_data.game_mgr.get_logic_timer().unregister(self._statistics_clock_timer)
        self._statistics_clock_timer = global_data.game_mgr.get_logic_timer().register(func=on_clock_check, mode=timer.CLOCK, interval=0.5)
        on_clock_check()

        def on_logic_check--- This code section failed: ---

 154       0  LOAD_DEREF            0  'self'
           3  LOAD_ATTR             0  'is_statistics_check'
           6  POP_JUMP_IF_TRUE     13  'to 13'

 155       9  LOAD_CONST            0  ''
          12  RETURN_END_IF    
        13_0  COME_FROM                '6'

 156      13  RETURN_VALUE     
          14  RETURN_VALUE     
          15  RETURN_VALUE     
          16  COMPARE_OP            4  '>'
          19  POP_JUMP_IF_FALSE    66  'to 66'
          22  POP_JUMP_IF_FALSE     2  'to 2'
          25  COMPARE_OP            0  '<'
        28_0  COME_FROM                '19'
          28  POP_JUMP_IF_FALSE    66  'to 66'

 157      31  LOAD_DEREF            0  'self'
          34  LOAD_ATTR             1  '_statistics_data'
          37  LOAD_ATTR             2  'get'
          40  LOAD_CONST            3  'mild_stuck_times'
          43  LOAD_CONST            4  ''
          46  CALL_FUNCTION_2       2 
          49  LOAD_CONST            5  1
          52  BINARY_ADD       
          53  LOAD_DEREF            0  'self'
          56  LOAD_ATTR             1  '_statistics_data'
          59  LOAD_CONST            3  'mild_stuck_times'
          62  STORE_SUBSCR     
          63  JUMP_FORWARD         44  'to 110'

 158      66  JUMP_FORWARD          2  'to 71'
          69  COMPARE_OP            4  '>'
          72  POP_JUMP_IF_FALSE   110  'to 110'

 159      75  LOAD_DEREF            0  'self'
          78  LOAD_ATTR             1  '_statistics_data'
          81  LOAD_ATTR             2  'get'
          84  LOAD_CONST            6  'serious_stuck_times'
          87  LOAD_CONST            4  ''
          90  CALL_FUNCTION_2       2 
          93  LOAD_CONST            5  1
          96  BINARY_ADD       
          97  LOAD_DEREF            0  'self'
         100  LOAD_ATTR             1  '_statistics_data'
         103  LOAD_CONST            6  'serious_stuck_times'
         106  STORE_SUBSCR     
         107  JUMP_FORWARD          0  'to 110'
       110_0  COME_FROM                '107'
       110_1  COME_FROM                '63'

 160     110  LOAD_DEREF            0  'self'
         113  LOAD_ATTR             1  '_statistics_data'
         116  LOAD_ATTR             2  'get'
         119  LOAD_CONST            7  'statistics_logic_times'
         122  LOAD_CONST            4  ''
         125  CALL_FUNCTION_2       2 
         128  LOAD_CONST            5  1
         131  BINARY_ADD       
         132  LOAD_DEREF            0  'self'
         135  LOAD_ATTR             1  '_statistics_data'
         138  LOAD_CONST            7  'statistics_logic_times'
         141  STORE_SUBSCR     

Parse error at or near `RETURN_VALUE' instruction at offset 13

        self._statistics_logic_timer and global_data.game_mgr.get_logic_timer().unregister(self._statistics_logic_timer)
        self._statistics_logic_timer = global_data.game_mgr.get_logic_timer().register(func=on_logic_check, mode=timer.LOGIC, interval=1, timedelta=True)
        on_logic_check(0)

    def start_check(self):
        if not self.get_enable():
            return
        if not global_data.player:
            return
        x, y, z = (0, 0, 0)
        if global_data.player.logic:
            pos = global_data.player.logic.get_value('G_POSITION')
            if pos:
                x, y, z = pos.x, pos.y, pos.z
        battle = global_data.player.get_battle()
        game_mode_name = ''
        is_in_lobby = False
        if battle:
            map_config = confmgr.get('map_config') or {}
            game_mode_name = map_config.get(str(battle.map_id), {}).get('cCMode', 'unknown_mode')
        else:
            is_in_lobby = True
        quality_level = global_data.player.get_setting(uoc.QUALITY_LEVEL_KEY)
        pve_quality_level = global_data.player.get_setting(uoc.PVE_QUALITY_LEVEL_KEY)
        quality_resolution = global_data.player.get_setting(uoc.QUALITY_RESOLUTION_KEY)
        quality_resolution_kongdao = global_data.player.get_setting(uoc.QUALITY_RESOLUTION_KEY_KONGDAO)
        quality_shadowmap = global_data.player.get_setting(uoc.QUALITY_SHADOWMAP_KEY)
        quality_hdr = global_data.player.get_setting(uoc.QUALITY_HDR_KEY)
        quality_msaa = global_data.player.get_setting(uoc.QUALITY_MSAA_KEY)
        qulity_high_frame = global_data.player.get_setting(uoc.QUALITY_HIGH_FRAME_RATE_KEY)
        quality_dynamic_fuzzy = global_data.player.get_setting(uoc.QUALITY_RADIAL_BLUR_KEY)
        thermal_state = 0
        if game3d.get_platform() == game3d.PLATFORM_IOS:
            if hasattr(profiling, 'get_thermal_state'):
                thermal_state = profiling.get_thermal_state()
        elif game3d.get_platform() == game3d.PLATFORM_ANDROID:
            if hasattr(game3d, 'get_current_thermal_status'):
                thermal_state = game3d.get_current_thermal_status()
        print('[Thermal State] === %s ===' % thermal_state)
        draw_call = profiling.get_dp_num()
        vertex_count = profiling.get_prim_num()
        fps = profiling.get_render_rate()
        mem_usage = profiling.get_process_mem_used()
        mem_available = profiling.get_total_memory() * 1024 * 1024 - profiling.get_process_mem_used()
        statistics_clock_times = self._statistics_data.get('statistics_clock_times', 1)
        statistics_logic_times = self._statistics_data.get('statistics_logic_times', 1)
        percent_fps = {}
        for k, v in six.iteritems(self._statistics_data.get('multiple_fps', {})):
            percent_fps[k] = '{:.2f}%'.format(v * 100.0 / statistics_clock_times)

        data = {'time': time_utility.get_server_time(),'location': json.dumps({'x': x,'y': y,'z': z}),
           'map_id': str(battle.map_id) if battle else '-1',
           'online_time': time.time() - self.login_time,
           'draw_call': draw_call,
           'fps': fps,
           'vertex_count': vertex_count,
           'mem_usage': mem_usage,
           'mem_available': mem_available,
           'actor_count': battle.get_actors_frame_visible_count() if battle else 0,
           'game_mode_name': game_mode_name,
           'is_in_lobby': is_in_lobby,
           'quality_level': quality_level,
           'pve_quality_level': pve_quality_level,
           'quality_resolution': quality_resolution,
           'quality_resolution_kongdao': quality_resolution_kongdao,
           'quality_shadowmap': quality_shadowmap,
           'quality_hdr': quality_hdr,
           'quality_msaa': quality_msaa,
           'qulity_high_frame': qulity_high_frame,
           'qulity_high_frame_txt': FRAME_MODE.get(qulity_high_frame, qulity_high_frame),
           'thermal_state': thermal_state,
           'high_fps_mode': int(global_data.enable_high_fps),
           'average_draw_call': self._statistics_data.get('draw_call', draw_call) / statistics_clock_times,
           'average_fps': self._statistics_data.get('fps', fps) / statistics_clock_times,
           'average_vertex_count': self._statistics_data.get('vertex_count', vertex_count) / statistics_clock_times,
           'average_mem_usage': self._statistics_data.get('mem_usage', mem_usage) / statistics_clock_times,
           'average_mem_available': self._statistics_data.get('mem_available', mem_available) / statistics_clock_times,
           'mild_stuck_times': self._statistics_data.get('mild_stuck_times', 0),
           'serious_stuck_times': self._statistics_data.get('serious_stuck_times', 0),
           'multiple_fps': json.dumps(percent_fps),
           'statistics_clock_times': statistics_clock_times,
           'statistics_logic_times': statistics_logic_times
           }
        data.update(self._data)
        headers = {'Content-Type': 'application/json'}
        try:

            def cb(req, rep):
                pass

            from common.platform.dctool import interface
            hubble_url = confmgr.get('channel_conf', interface.get_game_id(), 'HUBBLE_URL')
            request = HttpBase.HttpRequest(hubble_url, 'POST', url='/', body=json.dumps(data), headers=headers, usessl=True)
            self.httpclient.http_request(request, 3, lambda req, rep: cb(req, rep))
        except Exception as e:
            print('Hubble urlopen error:', e)

        self.start_statistics_check()

    def start_normal_check(self, interval=-1):
        if not self.get_enable():
            return
        self.init_data()
        self.stop_normal_check()
        if interval == -1:
            interval = confmgr.get('setting', 'hubble_time', default=1800)

        def on_check():
            self.start_check()

        def first_check():
            self.start_check()
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
            self._timer = global_data.game_mgr.get_logic_timer().register(func=on_check, mode=timer.CLOCK, interval=interval)

        self._timer = global_data.game_mgr.get_logic_timer().register(func=first_check, mode=timer.CLOCK, interval=int(interval * random.random() + 1), times=1)
        self.start_statistics_check()

    def stop_normal_check(self):
        if self._timer:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
            self._timer = None
        return