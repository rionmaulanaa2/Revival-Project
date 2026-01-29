# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/version.py
from __future__ import absolute_import
from __future__ import print_function
import game3d
import zlib
import C_file
import json
import six
NPK_VERSION_FILE_NAME = 'npk_version.config'
EXCEPT_NPK_VERSION = -2

def get_engine_version():
    return game3d.get_engine_version()


def get_engine_svn():
    return game3d.get_engine_svn_version()


def get_script_version():
    try:
        version_conf = C_file.get_res_file('confs/version.json', '')
        version_conf = json.loads(version_conf)
        return version_conf.get('svn_version', '0')
    except:
        return '0'


def get_cur_version_str():
    engine_v = get_engine_version()
    engine_svn = get_engine_svn()
    script_v = get_script_version()
    return '{0}.{1}.{2}'.format(engine_v, engine_svn, script_v)


def get_tag():
    try:
        version_conf = C_file.get_res_file('confs/version.json', '')
        version_conf = json.loads(version_conf)
        return version_conf.get('tag', 'None')
    except:
        return 'None'


def get_server_version():
    import C_file
    filename = 'logic/gcommon/cdata/server_version'
    py_filename = filename + '.py'
    nxs_filename = filename + '.nxs'
    import marshal
    try:
        VERSION = 0
        if C_file.find_file(py_filename, ''):
            data = C_file.get_file(py_filename, '')
            if six.PY2:
                exec data
            else:
                my_locals = {'VERSION': 0}
                exec (
                 data, my_locals, my_locals)
                VERSION = my_locals['VERSION']
        elif C_file.find_file(nxs_filename, ''):
            data = C_file.get_file(nxs_filename, '')
            if six.PY2:
                import redirect
                data = redirect.NpkImporter.rotor.decrypt(data)
                data = zlib.decompress(data)
                data = redirect._reverse_string(data)
                data = marshal.loads(data)
                exec data
            else:
                if len(data) > 12 and data.startswith('NXS\x03G93\x01'):
                    uncompress_len = int.from_bytes(data[8:12], byteorder='little')
                    data = C_file.make_funny_thing(data[12:])
                    data = C_file.lz4_decompress(data, uncompress_len)
                my_locals = {'VERSION': 0}
                data = marshal.loads(data)
                exec (
                 data, my_locals, my_locals)
                VERSION = my_locals['VERSION']
        else:
            return 0
        return VERSION
    except Exception as e:
        print('[Version] get_server_version except:', str(e))
        return 0


def get_npk_version():
    try:
        if not C_file.find_res_file(NPK_VERSION_FILE_NAME, ''):
            return -1
        str_npk_version = C_file.get_res_file(NPK_VERSION_FILE_NAME, '')
        return int(str_npk_version)
    except Exception as e:
        print('get_npk ver except', str(e))
        return -1
