# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/ctypes/clan/ClanRequest.py


class ClanRequest(object):
    __slots__ = ('_size', '_request_list', '_request_dict', '_handle_set', '_request_message_dict',
                 'init_from_dict', 'get_persistent_dict', 'get_request', 'add_request',
                 'pop_request', 'get_handle', 'add_handle', 'pop_handle', 'clear_handle')

    def __init__(self, size):
        self._size = size
        self._request_list = []
        self._request_dict = {}
        self._request_message_dict = {}
        self._handle_set = set()

    def init_from_dict(self, bdict):
        self._request_list = bdict.get('request_list', [])
        self._request_dict = bdict.get('request_dict', {})
        self._request_message_dict = bdict.get('request_message_dict', {})
        self._handle_set = set([ (uid, aid) for uid, aid in bdict.get('handle_list', []) ])

    def get_persistent_dict(self):
        return {'request_list': self._request_list,
           'request_dict': self._request_dict,
           'handle_list': list(self._handle_set),
           'request_message_dict': self._request_message_dict
           }

    def get_request(self):
        return (
         self._request_list, self._request_message_dict)

    def add_request(self, uid, aid, request_data):
        str_uid = str(uid)
        pop_uid = None
        if str_uid not in self._request_dict:
            self._request_list.append(uid)
            self._request_dict[str_uid] = aid
            self._request_message_dict[str_uid] = request_data
            if len(self._request_list) >= self._size:
                pop_uid = self._request_list.pop(0)
                self._request_dict.pop(str(pop_uid), None)
                self._request_message_dict.pop(str(pop_uid), None)
        return pop_uid

    def pop_request(self, uid):
        str_uid = str(uid)
        aid = None
        if str_uid in self._request_dict:
            aid = self._request_dict.pop(str_uid, None)
            self._request_message_dict.pop(str_uid, None)
            self._request_list.remove(uid)
        return aid

    def get_handle(self):
        return self._handle_set

    def add_handle(self, uid, aid):
        self._handle_set.add((uid, aid))

    def pop_handle(self, uid, aid):
        try:
            self._handle_set.remove((uid, aid))
        except:
            pass

    def clear_handle(self):
        handling_set = self._handle_set
        self._handle_set = set()
        return handling_set