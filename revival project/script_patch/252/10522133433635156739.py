# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/platform/thread_downloader_utils.py
from __future__ import absolute_import
from __future__ import print_function
from six.moves import range
import six.moves.http_client
import urllib3
from patch import patch_const
from common.framework import WeakMethod2, Singleton
import threading

class ThreaderDownloaderHelper(Singleton):

    def init(self):
        self.download_request_list = []

    def add_request(self, url, filename, callback):
        self.download_request_list.append([WeakMethod2(callback), url, filename])
        if len(self.download_request_list) == 1:
            self.execute_downloader()

    def execute_downloader(self):
        callback, url, filename = self.download_request_list[0]
        download_single_file(url, filename, self.on_download_callback)

    def on_download_callback(self, data):
        self.download_request_list[0][0](data)
        self.download_request_list = self.download_request_list[1:]
        if len(self.download_request_list) > 0:
            self.execute_downloader()


def download_single_file(url, filename, callback):

    def thread_download_single_file(url):
        data = http_download_file(url)
        global_data.game_mgr.next_exec(lambda : callback(data))

    t = threading.Thread(target=thread_download_single_file, args=(url,))
    t.setDaemon(True)
    t.start()


def http_download_file--- This code section failed: ---

  49       0  SETUP_LOOP          313  'to 316'
           3  LOAD_GLOBAL           0  'range'
           6  LOAD_CONST            1  3
           9  CALL_FUNCTION_1       1 
          12  GET_ITER         
          13  FOR_ITER            299  'to 315'
          16  STORE_FAST            1  'trycount'

  50      19  SETUP_EXCEPT        224  'to 246'

  51      22  LOAD_CONST            0  ''
          25  STORE_FAST            2  'data'

  52      28  LOAD_GLOBAL           2  'urllib3'
          31  LOAD_ATTR             3  'PoolManager'
          34  CALL_FUNCTION_0       0 
          37  STORE_FAST            3  'http'

  53      40  LOAD_FAST             3  'http'
          43  LOAD_ATTR             4  'request'
          46  LOAD_CONST            2  'GET'
          49  LOAD_CONST            3  'preload_content'
          52  LOAD_GLOBAL           5  'False'
          55  LOAD_CONST            4  'timeout'
          58  LOAD_GLOBAL           2  'urllib3'
          61  LOAD_ATTR             6  'Timeout'
          64  LOAD_CONST            5  'connect'
          67  LOAD_GLOBAL           7  'patch_const'
          70  LOAD_ATTR             8  'CONNECT_TIMEOUT'
          73  LOAD_CONST            6  'read'
          76  LOAD_GLOBAL           7  'patch_const'
          79  LOAD_ATTR             9  'DOWNLOAD_TIMEOUT'
          82  CALL_FUNCTION_512   512 
          85  CALL_FUNCTION_514   514 
          88  STORE_FAST            4  'r'

  54      91  LOAD_FAST             4  'r'
          94  LOAD_ATTR            10  'status'
          97  LOAD_GLOBAL          11  'six'
         100  LOAD_ATTR            12  'moves'
         103  LOAD_ATTR            13  'http_client'
         106  LOAD_ATTR            14  'OK'
         109  COMPARE_OP            3  '!='
         112  POP_JUMP_IF_FALSE   147  'to 147'

  55     115  LOAD_GLOBAL          15  'hasattr'
         118  LOAD_FAST             4  'r'
         121  LOAD_CONST            7  'release_con'
         124  CALL_FUNCTION_2       2 
         127  POP_JUMP_IF_FALSE   143  'to 143'

  56     130  LOAD_FAST             4  'r'
         133  LOAD_ATTR            16  'release_con'
         136  CALL_FUNCTION_0       0 
         139  POP_TOP          
         140  JUMP_FORWARD          0  'to 143'
       143_0  COME_FROM                '140'

  57     143  LOAD_FAST             2  'data'
         146  RETURN_END_IF    
       147_0  COME_FROM                '112'

  59     147  BUILD_LIST_0          0 
         150  STORE_FAST            5  'buff'

  60     153  SETUP_LOOP           39  'to 195'
         156  LOAD_FAST             4  'r'
         159  LOAD_ATTR            17  'stream'
         162  LOAD_GLOBAL           7  'patch_const'
         165  LOAD_ATTR            18  'CHUNK_SIZE'
         168  CALL_FUNCTION_1       1 
         171  GET_ITER         
         172  FOR_ITER             19  'to 194'
         175  STORE_FAST            6  'chunk'

  61     178  LOAD_FAST             5  'buff'
         181  LOAD_ATTR            19  'append'
         184  LOAD_FAST             6  'chunk'
         187  CALL_FUNCTION_1       1 
         190  POP_TOP          
         191  JUMP_BACK           172  'to 172'
         194  POP_BLOCK        
       195_0  COME_FROM                '153'

  62     195  LOAD_CONST            8  ''
         198  LOAD_ATTR            20  'join'
         201  LOAD_FAST             5  'buff'
         204  CALL_FUNCTION_1       1 
         207  STORE_FAST            2  'data'

  63     210  LOAD_GLOBAL          15  'hasattr'
         213  LOAD_FAST             4  'r'
         216  LOAD_CONST            7  'release_con'
         219  CALL_FUNCTION_2       2 
         222  POP_JUMP_IF_FALSE   238  'to 238'

  64     225  LOAD_FAST             4  'r'
         228  LOAD_ATTR            16  'release_con'
         231  CALL_FUNCTION_0       0 
         234  POP_TOP          
         235  JUMP_FORWARD          0  'to 238'
       238_0  COME_FROM                '235'

  65     238  LOAD_FAST             2  'data'
         241  RETURN_VALUE     
         242  POP_BLOCK        
         243  JUMP_BACK            13  'to 13'
       246_0  COME_FROM                '19'

  66     246  DUP_TOP          
         247  LOAD_GLOBAL           2  'urllib3'
         250  LOAD_ATTR            21  'exceptions'
         253  LOAD_ATTR            22  'TimeoutError'
         256  COMPARE_OP           10  'exception-match'
         259  POP_JUMP_IF_FALSE   271  'to 271'
         262  POP_TOP          
         263  POP_TOP          
         264  POP_TOP          

  67     265  CONTINUE             13  'to 13'
         268  JUMP_BACK            13  'to 13'

  68     271  DUP_TOP          
         272  LOAD_GLOBAL          23  'Exception'
         275  COMPARE_OP           10  'exception-match'
         278  POP_JUMP_IF_FALSE   311  'to 311'
         281  POP_TOP          
         282  STORE_FAST            7  'e'
         285  POP_TOP          

  69     286  LOAD_GLOBAL          24  'print'
         289  LOAD_CONST            9  'downlaod file with exception'
         292  LOAD_GLOBAL          25  'str'
         295  LOAD_FAST             7  'e'
         298  CALL_FUNCTION_1       1 
         301  CALL_FUNCTION_2       2 
         304  POP_TOP          

  71     305  CONTINUE             13  'to 13'
         308  JUMP_BACK            13  'to 13'
         311  END_FINALLY      
       312_0  COME_FROM                '311'
         312  JUMP_BACK            13  'to 13'
         315  POP_BLOCK        
       316_0  COME_FROM                '0'

  72     316  LOAD_CONST            0  ''
         319  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_514' instruction at offset 85