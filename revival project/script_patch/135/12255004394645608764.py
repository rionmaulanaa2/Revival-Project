# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impNgPush.py
from __future__ import absolute_import
from __future__ import print_function
from logic.gcommon.cdata import ngpush_tag_data

class impNgPush(object):

    def _init_ngpush_from_dict(self, bdict):
        self.ngpush_device_id = None
        self.ngpush_taglist = bdict.get('ngpush_taglist', [])
        from logic.comsys.push import ngpush_device_token, get_push_service
        if ngpush_device_token:
            self.subscribe(ngpush_device_token, get_push_service())
        return

    def subscribe(self, regid, service):
        self.ngpush_device_id = regid
        print('impNgPush subscribe', regid, service)
        self.call_server_method('subscribe', (regid, service))

    def has_ngpush_tag(self, tag):
        return tag in self.ngpush_taglist

    def add_ngpush_tag(self, tag):
        if not self.ngpush_device_id:
            return False
        if tag not in ngpush_tag_data.NGPUSH_TAG_SET:
            return False
        if tag not in self.ngpush_taglist:
            self.ngpush_taglist.append(tag)
            self.call_server_method('add_ngpush_tag', (tag,))
        return True

    def del_ngpush_tag(self, tag):
        if not self.ngpush_device_id:
            return False
        if tag in self.ngpush_taglist:
            self.ngpush_taglist.remove(tag)
            self.call_server_method('del_ngpush_tag', (tag,))
        return True