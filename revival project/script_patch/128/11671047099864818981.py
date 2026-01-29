# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/http.py
from __future__ import absolute_import
from __future__ import print_function
import re
import base64
import six.moves.urllib.request
import six.moves.urllib.parse
import six.moves.urllib.error
import six.moves.urllib.request
import six.moves.urllib.error
import six.moves.urllib.parse
import hashlib
import six.moves.http_client
import socket
import common.daemon_thread
import urllib3
import json
from Crypto.Cipher import DES
from patch.patch_path import CACERT_PATH
if six.PY3:
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context
USE_URLLIB_VER = 3
REQUEST_TIME_OUT = 20
CHIPER_DICT = {}

def get_chiper(key):
    if key not in CHIPER_DICT:
        chiper = DES.new(key, DES.MODE_ECB)
        CHIPER_DICT[key] = chiper
    return CHIPER_DICT[key]


def des_encrypt(key, content):
    chiper = get_chiper(key)
    if len(content) % 8 != 0:
        toAdd = 8 - len(content) % 8
        content = content.ljust(len(content) + toAdd)
    return base64.b64encode(chiper.encrypt(content))


def des_decrypt(key, content):
    chiper = get_chiper(key)
    return chiper.decrypt(base64.b64decode(content)).rstrip()


def convert_url(url):
    base, host, port = (None, None, None)
    prot = None
    ret = re.search('(https?)://(\\d+\\.\\d+\\.\\d+\\.\\d+)/', url)
    if ret:
        base = ret.group(0)
        prot = ret.group(1)
        host = ret.group(2)
        port = 80
    else:
        ret = re.search('(https?)://(\\d+\\.\\d+\\.\\d+\\.\\d+):(\\d+)/', url)
        if ret:
            base = ret.group(0)
            prot = ret.group(1)
            host = ret.group(2)
            port = int(ret.group(3))
    if not base:
        return url
    else:
        if socket.has_ipv6:
            flags = getattr(socket, 'AI_DEFAULT', socket.AI_ADDRCONFIG) if 1 else 0
            addrinfos = socket.getaddrinfo(host, port, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, flags)
            if not addrinfos:
                return
            addrinfo = addrinfos[0]
            if not addrinfo:
                return
            sockaddr = addrinfo[4]
            return sockaddr or None
        return url.replace(base, '{0}://{1}:{2}/'.format(prot, sockaddr[0], port))


def request--- This code section failed: ---

  91       0  LOAD_GLOBAL           0  'USE_URLLIB_VER'
           3  LOAD_CONST            1  3
           6  COMPARE_OP            2  '=='
           9  POP_JUMP_IF_FALSE    58  'to 58'

  92      12  LOAD_GLOBAL           1  'request_v3'
          15  LOAD_GLOBAL           2  'request_v2'
          18  LOAD_FAST             1  'data'
          21  LOAD_CONST            3  'header'
          24  LOAD_FAST             2  'header'
          27  LOAD_CONST            4  'callback'
          30  LOAD_FAST             3  'callback'
          33  LOAD_CONST            5  'ext_data'
          36  LOAD_FAST             4  'ext_data'
          39  LOAD_CONST            6  'fields'
          42  LOAD_FAST             5  'fields'
          45  LOAD_CONST            7  'require_resbond_obj'
          48  LOAD_FAST             6  'require_resbond_obj'
          51  CALL_FUNCTION_1537  1537 
          54  POP_TOP          
          55  JUMP_FORWARD         31  'to 89'

  94      58  LOAD_GLOBAL           2  'request_v2'
          61  LOAD_GLOBAL           2  'request_v2'
          64  LOAD_FAST             1  'data'
          67  LOAD_CONST            3  'header'
          70  LOAD_FAST             2  'header'
          73  LOAD_CONST            4  'callback'
          76  LOAD_FAST             3  'callback'
          79  LOAD_CONST            5  'ext_data'
          82  LOAD_FAST             4  'ext_data'
          85  CALL_FUNCTION_1025  1025 
          88  POP_TOP          
        89_0  COME_FROM                '55'

Parse error at or near `CALL_FUNCTION_1537' instruction at offset 51


def request_v2(url, data=None, header={}, callback=None, ext_data=None):
    from logic.gcommon import time_utility as tutil
    url = convert_url(url)

    def request_callfunc(url, args):
        data = args['data']
        header = args['header']
        req = six.moves.urllib.request.Request(url, data, header)
        try:
            response = six.moves.urllib.request.urlopen(req)
            ret = response.read()
            return ret
        except Exception as e:
            return None

        return None

    def request_callback(request, result):
        if callback:
            callback(result, url, request.args)

    common.daemon_thread.DaemonThreadPool.get_instance().add_threadpool(request_callfunc, request_callback, url, {'data': data,'header': header,'ext_data': ext_data})


def set_warning_disabled():
    from urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning
    urllib3.disable_warnings(InsecureRequestWarning)
    urllib3.disable_warnings(InsecurePlatformWarning)


def request_v3(url, data=None, header={}, callback=None, ext_data=None, fields=None, require_resbond_obj=False):
    from logic.gcommon import time_utility as tutil
    url = convert_url(url)
    resbond_obj = [None]

    def request_callfunc--- This code section failed: ---

 133       0  LOAD_GLOBAL           0  'urllib3'
           3  LOAD_ATTR             1  'PoolManager'
           6  LOAD_CONST            1  'cert_reqs'
           9  LOAD_CONST            2  'CERT_NONE'
          12  CALL_FUNCTION_256   256 
          15  STORE_FAST            2  'http'

 135      18  LOAD_FAST             1  'args'
          21  LOAD_CONST            3  'data'
          24  BINARY_SUBSCR    
          25  STORE_FAST            3  'data'

 136      28  LOAD_FAST             1  'args'
          31  LOAD_CONST            4  'header'
          34  BINARY_SUBSCR    
          35  STORE_FAST            4  'header'

 137      38  LOAD_FAST             1  'args'
          41  LOAD_CONST            5  'fields'
          44  BINARY_SUBSCR    
          45  STORE_FAST            5  'fields'

 140      48  SETUP_EXCEPT        168  'to 219'

 141      51  LOAD_FAST             5  'fields'
          54  POP_JUMP_IF_FALSE    99  'to 99'

 142      57  LOAD_FAST             2  'http'
          60  LOAD_ATTR             2  'request'
          63  LOAD_CONST            6  'POST'
          66  LOAD_CONST            7  'timeout'
          69  LOAD_GLOBAL           3  'REQUEST_TIME_OUT'
          72  LOAD_CONST            8  'headers'
          75  LOAD_FAST             4  'header'
          78  LOAD_CONST            9  'preload_content'
          81  LOAD_GLOBAL           4  'False'
          84  LOAD_CONST            5  'fields'
          87  LOAD_FAST             5  'fields'
          90  CALL_FUNCTION_1026  1026 
          93  STORE_FAST            6  'response'
          96  JUMP_FORWARD         81  'to 180'

 143      99  LOAD_FAST             3  'data'
         102  POP_JUMP_IF_FALSE   147  'to 147'

 144     105  LOAD_FAST             2  'http'
         108  LOAD_ATTR             2  'request'
         111  LOAD_CONST            6  'POST'
         114  LOAD_CONST            7  'timeout'
         117  LOAD_GLOBAL           3  'REQUEST_TIME_OUT'
         120  LOAD_CONST            8  'headers'
         123  LOAD_FAST             4  'header'
         126  LOAD_CONST            9  'preload_content'
         129  LOAD_GLOBAL           4  'False'
         132  LOAD_CONST           10  'body'
         135  LOAD_FAST             3  'data'
         138  CALL_FUNCTION_1026  1026 
         141  STORE_FAST            6  'response'
         144  JUMP_FORWARD         33  'to 180'

 146     147  LOAD_FAST             2  'http'
         150  LOAD_ATTR             2  'request'
         153  LOAD_CONST           11  'GET'
         156  LOAD_CONST            7  'timeout'
         159  LOAD_GLOBAL           3  'REQUEST_TIME_OUT'
         162  LOAD_CONST            8  'headers'
         165  LOAD_FAST             4  'header'
         168  LOAD_CONST            9  'preload_content'
         171  LOAD_GLOBAL           4  'False'
         174  CALL_FUNCTION_770   770 
         177  STORE_FAST            6  'response'
       180_0  COME_FROM                '144'
       180_1  COME_FROM                '96'

 148     180  LOAD_FAST             6  'response'
         183  LOAD_ATTR             5  'read'
         186  CALL_FUNCTION_0       0 
         189  STORE_FAST            7  'ret'

 150     192  LOAD_DEREF            0  'require_resbond_obj'
         195  POP_JUMP_IF_FALSE   211  'to 211'

 151     198  LOAD_FAST             6  'response'
         201  LOAD_DEREF            1  'resbond_obj'
         204  LOAD_CONST           12  ''
         207  STORE_SUBSCR     
         208  JUMP_FORWARD          0  'to 211'
       211_0  COME_FROM                '208'

 153     211  LOAD_FAST             7  'ret'
         214  RETURN_VALUE     
         215  POP_BLOCK        
         216  JUMP_FORWARD         46  'to 265'
       219_0  COME_FROM                '48'

 154     219  DUP_TOP          
         220  LOAD_GLOBAL           6  'Exception'
         223  COMPARE_OP           10  'exception-match'
         226  POP_JUMP_IF_FALSE   264  'to 264'
         229  POP_TOP          
         230  STORE_FAST            8  'e'
         233  POP_TOP          

 155     234  LOAD_GLOBAL           7  'log_error'
         237  LOAD_CONST           13  '[ERROR] request_v3 http error : %s @url %s'
         240  LOAD_GLOBAL           8  'str'
         243  LOAD_FAST             8  'e'
         246  CALL_FUNCTION_1       1 
         249  LOAD_FAST             0  'url'
         252  BUILD_TUPLE_2         2 
         255  BINARY_MODULO    
         256  CALL_FUNCTION_1       1 
         259  POP_TOP          

 156     260  LOAD_CONST            0  ''
         263  RETURN_VALUE     
         264  END_FINALLY      
       265_0  COME_FROM                '264'
       265_1  COME_FROM                '216'
         265  LOAD_CONST            0  ''
         268  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_1026' instruction at offset 90

    def request_callback(request, result):
        if callback:
            if require_resbond_obj:
                callback(result, url, request.args, resbond_obj[0])
            else:
                callback(result, url, request.args)
        resbond_obj[0] = None
        return

    common.daemon_thread.DaemonThreadPool.get_instance().add_threadpool(request_callfunc, request_callback, url, {'data': data,'header': header,'ext_data': ext_data,'fields': fields})
    return


def request_encrypt(url, encrypt_key, encrypt_dict, callback=None):
    import json
    from common.platform.dctool import interface
    url = convert_url(url)

    def request_callfunc(url, args):
        fields_data = json.dumps(encrypt_dict)
        import six
        sign = hashlib.md5(six.ensure_binary(fields_data + interface.get_project_id())).hexdigest()
        body = {'data': des_encrypt(encrypt_key, fields_data),
           'sign': sign
           }
        try:
            if url.startswith('https'):
                http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=CACERT_PATH)
            else:
                http = urllib3.PoolManager()
            r = http.request('GET', url, body, timeout=urllib3.Timeout(connect=2.0, read=2.0, total=2.0))
            data = r.data if r.status == six.moves.http_client.OK else None
            r.release_conn()
            return data
        except Exception as e:
            log_error('request_encrypt error %s @url %s' % (str(e), url))
            return False

        return

    def request_callback(request, result):
        if callback:
            callback(result, url, request.args)

    common.daemon_thread.DaemonThreadPool().add_threadpool(request_callfunc, request_callback, url, {})


def request_service(url, callback=None, fields=None, tag='GET'):
    raw_data = fields.get('data', None)
    if raw_data:
        fields['data'] = json.dumps(raw_data)
    url = convert_url(url)

    def request_callfunc--- This code section failed: ---

 221       0  LOAD_GLOBAL           0  'urllib3'
           3  LOAD_ATTR             1  'PoolManager'
           6  LOAD_CONST            1  'cert_reqs'
           9  LOAD_CONST            2  'CERT_NONE'
          12  CALL_FUNCTION_256   256 
          15  STORE_FAST            2  'http'

 223      18  LOAD_FAST             1  'args'
          21  LOAD_CONST            3  'fields'
          24  BINARY_SUBSCR    
          25  STORE_FAST            3  'fields'

 224      28  SETUP_EXCEPT        120  'to 151'

 225      31  LOAD_DEREF            0  'tag'
          34  LOAD_CONST            4  'GET'
          37  COMPARE_OP            2  '=='
          40  POP_JUMP_IF_FALSE    79  'to 79'

 226      43  LOAD_FAST             2  'http'
          46  LOAD_ATTR             2  'request'
          49  LOAD_CONST            4  'GET'
          52  LOAD_CONST            5  'timeout'
          55  LOAD_GLOBAL           3  'REQUEST_TIME_OUT'
          58  LOAD_CONST            6  'preload_content'
          61  LOAD_GLOBAL           4  'False'
          64  LOAD_CONST            3  'fields'
          67  LOAD_FAST             3  'fields'
          70  CALL_FUNCTION_770   770 
          73  STORE_FAST            4  'response'
          76  JUMP_FORWARD         52  'to 131'

 227      79  LOAD_DEREF            0  'tag'
          82  LOAD_CONST            7  'POST'
          85  COMPARE_OP            2  '=='
          88  POP_JUMP_IF_FALSE   127  'to 127'

 228      91  LOAD_FAST             2  'http'
          94  LOAD_ATTR             2  'request'
          97  LOAD_CONST            7  'POST'
         100  LOAD_CONST            5  'timeout'
         103  LOAD_GLOBAL           3  'REQUEST_TIME_OUT'
         106  LOAD_CONST            6  'preload_content'
         109  LOAD_GLOBAL           4  'False'
         112  LOAD_CONST            3  'fields'
         115  LOAD_FAST             3  'fields'
         118  CALL_FUNCTION_770   770 
         121  STORE_FAST            4  'response'
         124  JUMP_FORWARD          4  'to 131'

 230     127  LOAD_CONST            0  ''
         130  RETURN_VALUE     
       131_0  COME_FROM                '124'
       131_1  COME_FROM                '76'

 231     131  LOAD_FAST             4  'response'
         134  LOAD_ATTR             5  'read'
         137  CALL_FUNCTION_0       0 
         140  STORE_FAST            5  'ret'

 232     143  LOAD_FAST             5  'ret'
         146  RETURN_VALUE     
         147  POP_BLOCK        
         148  JUMP_FORWARD         46  'to 197'
       151_0  COME_FROM                '28'

 233     151  DUP_TOP          
         152  LOAD_GLOBAL           6  'Exception'
         155  COMPARE_OP           10  'exception-match'
         158  POP_JUMP_IF_FALSE   196  'to 196'
         161  POP_TOP          
         162  STORE_FAST            6  'e'
         165  POP_TOP          

 234     166  LOAD_GLOBAL           7  'log_error'
         169  LOAD_CONST            8  '[ERROR] request_service http error: %s @url %s'
         172  LOAD_GLOBAL           8  'str'
         175  LOAD_FAST             6  'e'
         178  CALL_FUNCTION_1       1 
         181  LOAD_FAST             0  'url'
         184  BUILD_TUPLE_2         2 
         187  BINARY_MODULO    
         188  CALL_FUNCTION_1       1 
         191  POP_TOP          

 235     192  LOAD_CONST            0  ''
         195  RETURN_VALUE     
         196  END_FINALLY      
       197_0  COME_FROM                '196'
       197_1  COME_FROM                '148'
         197  LOAD_CONST            0  ''
         200  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_770' instruction at offset 70

    def request_callback(request, result, raw_data=raw_data):
        if callback:
            if result:
                result = json.loads(result)
                url, args = request.args
                raw_data = raw_data or {} if 1 else raw_data
                raw_data['url'] = url
            callback(result, raw_data)

    common.daemon_thread.DaemonThreadPool.get_instance().add_threadpool(request_callfunc, request_callback, url, {'fields': fields})
    return