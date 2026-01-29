# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/NileSDK/Utils/NileSystemInfo.py
from __future__ import absolute_import
from __future__ import print_function
import game3d
import six.moves.urllib.request
import six.moves.urllib.parse
import six.moves.urllib.error

class NileSystemInfo(object):
    __mac = ''

    def __init__(self):
        pass

    @staticmethod
    def EnsureUTF8Str(raw):
        if NileSystemInfo.GetOsName() == 'windows':
            try:
                import locale
                encode = locale.getdefaultlocale()[1]
                u = six.ensure_text(raw, encode)
                b = six.ensure_binary(u, encoding='utf-8')
                return six.ensure_str(b)
            except Exception as e:
                return six.ensure_str(raw)

        else:
            return six.ensure_str(raw)

    @staticmethod
    def GetOsName():
        if global_data.is_android_pc:
            return 'windows'
        platform = game3d.get_platform()
        if platform == game3d.PLATFORM_ANDROID:
            return 'android'
        if platform == game3d.PLATFORM_IOS:
            return 'ios'
        return 'windows'

    @staticmethod
    def GetOsVersion():
        result = ''
        try:
            result = global_data.deviceinfo.get_os_ver()
        except BaseException as e:
            print(str(e))

        return result

    @staticmethod
    def GetNetworkStatus():
        return game3d.get_network_type()

    @staticmethod
    def GetIpInfo():
        r = game3d.get_ip_infos()
        if len(r) >= 2:
            return game3d.get_ip_infos()[0]
        return str(r)

    @staticmethod
    def GetDeviceInfo():
        result = ''
        try:
            result = six.moves.urllib.parse.quote(global_data.deviceinfo.get_device_model())
        except BaseException as e:
            print(str(e))

        return result

    @staticmethod
    def GetUDID():
        return game3d.get_udid()

    @staticmethod
    def GetEngineVersion():
        return game3d.get_engine_svn_version()

    @staticmethod
    def GetMacAddress():
        return global_data.deviceinfo.get_mac_addr()

    @staticmethod
    def IsInEditor():
        return not game3d.is_release_version()

    @staticmethod
    def GetLocalStorageRoot():
        from common.utils.path import get_neox_dir
        from .NileFileSystem import NileFileSystem
        docDir = NileFileSystem.JoinPath(NileSystemInfo.EnsureUTF8Str(get_neox_dir()), 'Documents')
        return NileFileSystem.JoinPath(docDir, 'NileInternal')

    @staticmethod
    def IsSupportNpk():
        import game3d
        return game3d.is_feature_ready('PATCH_NPK_MERGE')

    @staticmethod
    def IsOnWorkbench():
        macList = [
         'D8-BB-C1-37-61-F9', '2C-F0-5D-3A-C4-ED']
        return NileSystemInfo.GetMacAddress() in macList