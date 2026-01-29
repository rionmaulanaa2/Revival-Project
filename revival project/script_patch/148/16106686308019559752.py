# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/common_utils/idx_utils.py
from __future__ import absolute_import
import six
from six.moves import range
from hashlib import md5

class IdxReflect(object):

    def __init__(self, s_type, lst_names, salt=None):
        super(IdxReflect, self).__init__()
        self.type = s_type
        self.salt = str(salt) if salt else None
        self.mp_name_2_idx = {}
        self.mp_idx_2_name = {}
        self.load(lst_names)
        return

    def load(self, lst_names):
        if len(lst_names) != len(list(set(lst_names))):
            raise Exception('Error Method_name duplicate.')
        if self.salt is not None:
            salt = self.salt
            for name in lst_names:
                idx = IdxReflect.calculate_index(name, salt)
                if idx in self.mp_idx_2_name:
                    raise Exception('Error Index duplicate :: {},{}\nPlease generate a new salt for proto:{}'.format(name, idx, self.type))
                self.mp_idx_2_name[idx] = name

            for idx, name in six.iteritems(self.mp_idx_2_name):
                self.mp_name_2_idx[name] = idx

            return
        else:
            for self.salt in range(1, 65535):
                self.reset_mp()
                salt = str(self.salt)
                for name in lst_names:
                    idx = IdxReflect.calculate_index(name, salt)
                    if idx in self.mp_idx_2_name:
                        break
                    self.mp_idx_2_name[idx] = name
                else:
                    for idx, name in six.iteritems(self.mp_idx_2_name):
                        self.mp_name_2_idx[name] = idx

                    break

            else:
                raise Exception('load IdxReflect failed: {}, please'.format(self.type))

            return

    def method_2_idx(self, s_method_name):
        if s_method_name in self.mp_name_2_idx:
            return self.mp_name_2_idx[s_method_name]
        else:
            idx = self.calculate_index(s_method_name, self.salt)
            if idx in self.mp_name_2_idx:
                raise Exception('Error Index duplicate :: {},{}\nPlease generate a new salt for proto:{}'.format(s_method_name, idx, self.type))
            self.mp_name_2_idx[s_method_name] = idx
            self.mp_idx_2_name[idx] = s_method_name
            return idx

    def idx_2_method_name(self, i_idx):
        if i_idx not in self.mp_idx_2_name:
            raise Exception('Error Index not found :: {}\nPlease check {} proto'.format(i_idx, self.type))
        return self.mp_idx_2_name[i_idx]

    def reset_mp(self):
        self.mp_name_2_idx = {}
        self.mp_idx_2_name = {}

    @staticmethod
    def calculate_index(name, salt):
        import six
        m = md5()
        m.update(six.ensure_binary(name + salt))
        b = m.digest()
        if six.PY3:
            return ((b[-4] & 127) << 24) + (b[-3] << 16) + (b[-2] << 8) + b[-1]
        else:
            return ((ord(b[-4]) & 127) << 24) + (ord(b[-3]) << 16) + (ord(b[-2]) << 8) + ord(b[-1])


def c_method_2_idx(s_method_name):
    global g_client
    return g_client.method_2_idx(s_method_name)


def c_idx_2_method_name(i_idx):
    return g_client.idx_2_method_name(i_idx)


def s_method_2_idx(s_method_name):
    global g_server
    return g_server.method_2_idx(s_method_name)


def s_idx_2_method_name(i_idx):
    return g_server.idx_2_method_name(i_idx)


g_client = None
g_server = None

def init_client_proto(method_names, salt):
    global g_client
    g_client = IdxReflect('client', method_names, salt)


def init_server_proto(method_names, salt):
    global g_server
    g_server = IdxReflect('server', method_names, salt)