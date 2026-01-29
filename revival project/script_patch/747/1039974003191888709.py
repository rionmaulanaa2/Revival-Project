# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/cfg/jsonconf.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
from six.moves import range
import game3d
import six
if six.PY3:
    import json
else:
    import json2 as json
import time
import traceback
import C_file
import os
import taggeddict
import re
import threading
import six.moves._thread
from logic.gcommon.utility import recursive_update
try:
    from data.na_json_conf import na_json_conf
    from data.na_json_conf_manual import na_json_conf_manual
    na_json_conf.update(na_json_conf_manual)
except:
    log_error('load NA conf falied.')

JSON_LOCK = threading.Lock()
USE_TAGGEDDICT = False

def _convert_list(l):
    for i, v in enumerate(l):
        tv = type(v)
        if tv in (six.text_type, six.binary_type):
            l[i] = six.ensure_str(v)
        elif tv == list:
            _convert_list(v)
        elif tv == taggeddict.taggeddict:
            _convert_dict(v)
        elif tv == dict:
            _convert_dict(v)


def _convert_dict(d):
    for k, v in six.iteritems(d):
        tv = type(v)
        if tv == list:
            _convert_list(v)
        elif tv == taggeddict.taggeddict:
            _convert_dict(v)
        elif tv == dict:
            _convert_dict(v)


def _convert(conf):
    if type(conf) == taggeddict.taggeddict:
        _convert_dict(conf)
    elif type(conf) == dict:
        _convert_dict(conf)
    elif type(conf) == list:
        _convert_list(conf)
    return conf


def _json_object_hook_tagged(d):
    td = taggeddict.taggeddict()
    for k, v in six.iteritems(d):
        td[k] = v

    del d
    return td


def _json_object_hook_normal(d):
    td = {}
    for k, v in six.iteritems(d):
        if type(k) in (six.text_type, six.binary_type):
            k = six.ensure_str(k)
        if type(v) in (six.text_type, six.binary_type):
            v = six.ensure_str(v)
        td[k] = v

    del d
    return td


def convert(d):
    t = type(d)
    if t is list:
        newlist = []
        for data in d:
            newlist.append(convert(data))

        return newlist
    else:
        if t is dict:
            newdict = {}
            for k, v in six.iteritems(d):
                k = six.ensure_str(k)
                newdict[k] = convert(v)

            return newdict
        if t in (six.text_type, six.binary_type):
            return six.ensure_str(d)
        return d


def convert_byte(d):
    t = type(d)
    if t is list:
        newlist = []
        for i in range(len(d)):
            newlist.append(convert_byte(d[i]))

        return newlist
    else:
        if t is dict:
            newdict = {}
            for k, v in six.iteritems(d):
                if type(k) is bytes:
                    k = six.ensure_str(k)
                newdict[k] = convert_byte(v)

            return newdict
        if t is bytes:
            return six.ensure_str(d)
        return d


def get_conf_data(ctype, raw):
    original_c_type = ctype
    try:
        if G_IS_NA_PROJECT:
            json_conf = None
            try:
                ctype = na_json_conf.get(ctype, ctype)
                json_conf = JsonConf('confs/%s.json' % ctype, raw=raw)
            except:
                json_conf = None

            if not json_conf:
                json_conf = JsonConf('confs/%s.json' % original_c_type, raw=raw)
            return json_conf
    except:
        print('[WARN] %s not suppert na diff' % ctype)

    return JsonConf('confs/%s.json' % ctype, raw=raw)


def get_pve_conf_data(ctype, raw):
    original_c_type = ctype
    try:
        if G_IS_NA_PROJECT:
            json_conf = None
            try:
                ctype = na_json_conf.get(ctype, ctype)
                json_conf = JsonConf('confs/pve/%s.json' % ctype, raw=raw)
            except:
                json_conf = None

            if not json_conf:
                json_conf = JsonConf('confs/pve/%s.json' % original_c_type, raw=raw)
            return json_conf
    except:
        print('[WARN] %s not suppert na diff' % ctype)

    return JsonConf('confs/pve/%s.json' % ctype, raw=raw)


def get_pve_diff_conf_data(ctype, raw):
    original_c_type = ctype
    try:
        if G_IS_NA_PROJECT:
            json_conf = None
            try:
                ctype = na_json_conf.get(ctype, ctype)
                json_conf = JsonConf('confs/pve/diff/%s.json' % ctype, raw=raw)
            except:
                json_conf = None

            if not json_conf:
                json_conf = JsonConf('confs/pve/diff/%s.json' % original_c_type, raw=raw)
            return json_conf
    except:
        print('[WARN] %s not suppert na diff' % ctype)

    return JsonConf('confs/pve/diff/%s.json' % ctype, raw=raw)


DEFAULT_RES_PATH = '../res/'

class ConfigBase(object):

    def __init__(self, path, *args, **kwarg):
        super(ConfigBase, self).__init__()
        self._conf = {}
        self.load(path, *args, **kwarg)

    def load(self, path, *args, **kwarg):
        raise Exception('must implement load')

    def __getitem__(self, key):
        return self._conf[key]

    def __setitem__(self, key, value):
        self._conf[key] = value

    def __contains__(self, key):
        return key in self._conf

    def __iter__(self):
        return six.iteritems(self._conf)

    def __del__(self):
        del self._conf

    def iteritems(self):
        return six.iteritems(self._conf)

    def items(self):
        return self._conf.items()

    def keys(self):
        return self._conf.keys()

    def values(self):
        return self._conf.values()

    def get_conf(self):
        return self._conf

    def __len__(self):
        return len(self._conf)


class JsonConf(ConfigBase):

    def _load_json(self, s, raw):
        conf = json.loads(s)
        if USE_TAGGEDDICT and type(conf) == dict:
            self._conf = taggeddict.taggeddict(conf)
        else:
            self._conf = conf

    def load(self, path, s=None, raw=False):
        try:
            s = C_file.get_res_file(path, '')
        except:
            log_error('JsonConf cannot open', path)
            s = '{}'

        try:
            try:
                with JSON_LOCK:
                    self._load_json(s, raw)
            except Exception as e:
                import sys
                import exception_hook
                exception_hook.upload_exception(*sys.exc_info())
                log_error('jsonconf load except', path, str(e))
                import traceback
                traceback.print_exc()
                self._conf = {}

        finally:
            self.last_use_time = time.time()

    def get(self, key, default=None):
        return self._conf.get(key, default)

    def update(self, d):
        recursive_update(self._conf, d._conf)


class PyConf(ConfigBase):

    def load(self, path):
        try:
            self._conf = py_data_map[path]()
        except:
            self._conf = {}
            log_error('PyConf loads error', path)
            print(traceback.format_exc())

        self.last_use_time = time.time()


class FlatConf(ConfigBase):

    def load(self, filename):
        self.filename = filename
        if filename:
            self.open(filename)

    def __setitem__(self, key, value):
        self._conf[key] = value
        self.save()

    def open(self, filename):
        if not filename:
            return False
        if not os.path.isfile(filename):
            return False
        try:
            self.filename = filename
            self._conf = {}
            lines = open(filename).readlines()
            for line in lines:
                m = re.match('\\[(\\w)\\](.+)=(.*)', line)
                if m and len(m.groups()) == 3:
                    t = m.groups()[0]
                    k = m.groups()[1]
                    v = m.groups()[2]
                    if t == 'i':
                        v = int(v)
                    elif t == 'f':
                        v = float(v)
                    elif t == 's':
                        v = str(v)
                    self._conf[k] = v

        except:
            print(traceback.format_exc())
            return False

        return True

    def save(self):
        if not self.filename:
            return False
        if not self._conf:
            return False
        try:
            f = open(self.filename, 'w')
            lines = []
            for k, v in six.iteritems(self._conf):
                if type(v) == int:
                    lines.append('[i]%s=%d\n' % (k, v))
                elif type(v) == float:
                    lines.append('[f]%s=%f\n' % (k, v))
                elif type(v) == str:
                    lines.append('[s]%s=%s\n' % (k, v))

            f.writelines(lines)
            f.close()
        except:
            return False

        return True


class JsonUserConf(ConfigBase):

    def load(self, filename):
        self.filename = filename
        if filename:
            self.open(filename)

    def __setitem__(self, key, value):
        self._conf[key] = value

    def get(self, key, default_value):
        return self._conf.get(key, default_value)

    def open(self, filename, raw=False):
        if not filename:
            return False
        if not os.path.isfile(filename):
            return False
        self.filename = filename
        self._conf = {}
        configfile = open(filename)
        lines = configfile.read()
        configfile.close()
        try:
            conf = json.loads(lines)
            self._conf = conf
        except Exception as e:
            self._conf = {}
            log_error('JsonConf loads error, file:%s error:%s' % (self.filename, str(e)))

        return True

    def save(self):
        if not self.filename:
            return False
        if not self._conf:
            return False
        configFile = open(self.filename, 'w')
        json.dump(self._conf, configFile)
        configFile.close()
        return True