# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/archive/archivedata.py
from __future__ import absolute_import
import six_ex
import os
import base64
import game3d
import json
from common.cfg import jsonconf
import six

class ArchiveData(object):

    def __init__(self, archive_name):
        super(ArchiveData, self).__init__()
        self._key = 'SMC-2019@Copyright'
        self.filename = archive_name
        self.load()

    def load(self):
        from mobile.common.SessionEncrypter import ARC4Crypter
        doc_dir = game3d.get_doc_dir()
        if not os.path.exists(doc_dir):
            os.makedirs(doc_dir)
        self._path = os.path.join(doc_dir, self.filename)
        try:
            f = open(self._path)
            s = f.read()
            f.close()
            if s[-1] == '*':
                encoder = ARC4Crypter(self._key)
                s = s[:-1]
                s = base64.b64decode(s)
                s = encoder.decrypt(s)
            self._conf = jsonconf.convert(json.loads(s))
        except:
            self._conf = {}

    def save(self, encrypt=True):
        from mobile.common.SessionEncrypter import ARC4Crypter
        try:
            s = json.dumps(self._conf)
            if encrypt:
                encoder = ARC4Crypter(self._key)
                s = encoder.encrypt(s)
                s = base64.b64encode(s)
                s = six.ensure_str(s)
                s += '*'
            with open(self._path, 'w') as f:
                f.write(s)
        except Exception as e:
            log_error('ArchiveData failed to save file=%s, except=%s', self._path, repr(e))

    def __getitem__(self, key):
        return self._conf[key]

    def __setitem__(self, key, value):
        self._conf[key] = value

    def __contains__(self, key):
        return key in self._conf

    def __iter__(self):
        return six.iteritems(self._conf)

    def keys(self):
        return six_ex.keys(self._conf)

    def iteritems(self):
        return six.iteritems(self._conf)

    def items(self):
        return six_ex.items(self._conf)

    def values(self):
        return six_ex.values(self._conf)

    def get_conf(self):
        return self._conf

    def __len__(self):
        return len(self._conf)

    def get(self, field, default=None):
        return self.get_field(field, default)

    def set(self, field, value, save=True):
        self.set_field(field, value, save)

    def has_field(self, field):
        return field in self._conf

    def get_field(self, field, default=None):
        return self._conf.get(field, default)

    def set_field(self, field, value, save=True):
        self._conf[field] = value
        if save:
            self.save()

    def del_field(self, field, save=True):
        if field in self._conf:
            del self._conf[field]
            if save:
                self.save()

    def clear(self):
        self._conf = {}
        self.save()

    def get_items(self):
        for key, value in six_ex.items(self._conf):
            yield (key, value)

    def is_file_exist(self):
        if not os.path.isfile(self._path):
            return False
        return True

    def del_data(self):
        if self.is_file_exist():
            try:
                os.remove(self._path)
            except Exception as e:
                log_error('ArchiveData failed to remove file=%s, except=%s', self._path, repr(e))