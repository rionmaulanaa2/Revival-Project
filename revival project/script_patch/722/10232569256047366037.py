# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/micro_webservice_utils.py
from __future__ import absolute_import
from __future__ import print_function
import json
from common import http
import hashlib
from logic.gcommon.common_const.web_const import MICRO_SERVICES
import six_ex
import six

def get_micros_service_url(service_name, hostnum=None, micro_service_url=None):
    is_inner_test = global_data.achi_mgr.get_login_account_data_value('service_url_inner_test', False)
    if global_data.is_inner_server or is_inner_test:
        return __dev_server_url(service_name, hostnum, micro_service_url)
    else:
        return __prd_server_url(service_name, hostnum)


def __prd_server_url(service_name, hostnum=None):
    if not global_data.channel:
        return
    else:
        if hostnum is None:
            hostnum = global_data.channel.get_service_hostnum()
        if global_data.channel.is_china_server():
            return 'https://g93-ms-web.nie.netease.com/%s/%s' % (hostnum, service_name)
        return 'https://g93na-ms-web.nie.netease.com/%s/%s' % (hostnum, service_name)
        return


def __dev_server_url(service_name, hostnum=None, micro_service_url=None):
    if not global_data.channel:
        return
    else:
        if hostnum is None:
            hostnum = global_data.channel.get_host_num()
        if micro_service_url is None:
            micro_service_url = global_data.micro_service_url
        return '{}/{}/{}'.format(micro_service_url, hostnum, service_name)


def test(doc, args):
    print(doc)
    print(args)


def micro_service_request(service_name, data, cb=test, hostnum=None, uid=None, token=None):
    micro_service(service_name, data, 'GET', cb, hostnum, uid, token)


def micro_service_post(service_name, data, cb=None, hostnum=None, uid=None, token=None, micro_service_url=None):
    micro_service(service_name, data, 'POST', cb, hostnum, uid, token, micro_service_url)


def micro_service(service_name, data, tag, cb=None, hostnum=None, uid=None, token=None, micro_service_url=None):
    url = get_micros_service_url(service_name, hostnum, micro_service_url)
    if not url:
        return
    else:
        if uid is None:
            uid = global_data.player.uid
        if token is None:
            token = global_data.player.web_token
        doc = {'data': data,
           'sign': __gen_service_sign(data),
           'uid': uid
           }
        if token:
            doc['token'] = token
        print('micro_service url:', url)
        http.request_service(url, cb, doc, tag=tag)
        return


def _sign_encode_params(params):
    sign_string = []
    for k, v in sorted(six_ex.items(params)):
        sign_string.append(str(k))
        if type(v) in [list, tuple]:
            new_v = []
            for item in v:
                if type(item) is six.text_type:
                    new_v.append(str(item))
                else:
                    new_v.append(item)

            v = str(new_v)
        elif type(v) is dict:
            v = _sign_encode_params(v)
        elif type(v) is bytes:
            v = six.ensure_str(v)
        else:
            v = str(v)
        sign_string.append(v)

    return sign_string


def __gen_service_sign(params):
    sign_string = []
    sign_string = _sign_encode_params(params)
    sign_md5 = hashlib.md5()
    import six
    sign_md5.update(six.ensure_binary(''.join(sign_string).replace("'", '"')))
    sign = sign_md5.hexdigest().upper()
    return sign