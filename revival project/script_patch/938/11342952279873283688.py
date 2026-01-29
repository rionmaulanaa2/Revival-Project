# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impCheckUpdate.py
from __future__ import absolute_import
import re
import game3d
import version
import common.http
PACKAGE_NAME_PATTERN = 'smc-netease.+\\.apk'

class impCheckUpdate(object):

    def _init_checkupdate_from_dict(self, bdict):
        self._has_remote_new_package = False
        self._cur_remote_version = 0
        self.check_has_remote_new_package()

    def has_remote_new_package(self):
        return self._has_remote_new_package

    def get_cur_remote_version(self):
        return self._cur_remote_version

    def check_has_remote_new_package(self):
        if global_data.is_pc_mode:
            return
        else:
            if global_data.channel.get_name() != 'netease':
                return
            if game3d.get_platform() == game3d.PLATFORM_IOS:
                return

            def callback(ret, url, args):
                try:
                    if not global_data.player:
                        return
                    if type(ret) != str:
                        return
                    package_name = re.search(PACKAGE_NAME_PATTERN, ret)
                    if not package_name:
                        return
                    package_name = package_name.group()
                    ret_list = package_name.split('-')
                    engine_version_with_apk = ret_list[-1]
                    if not engine_version_with_apk.endswith('.apk'):
                        return
                    remote_engine_version_str = engine_version_with_apk[:-4]
                    if not remote_engine_version_str.isdigit():
                        return
                    remote_engine_version = int(remote_engine_version_str)
                    self._cur_remote_version = remote_engine_version
                    c_engine_ver = version.get_npk_version()
                    if c_engine_ver < 0:
                        return
                    if remote_engine_version > c_engine_ver:
                        global_data.player._has_remote_new_package = True
                    else:
                        return
                except Exception as e:
                    log_error('impCheckUpdate check_has_remote_new_package error, except=', repr(e))

            common.http.request('https://adl.netease.com/d/g/ace/c/gw', None, {}, callback)
            return