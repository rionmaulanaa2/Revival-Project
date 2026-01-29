# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/utils/emulator_check.py
from __future__ import absolute_import

def is_running_on_emulator():
    import game3d
    if game3d.get_platform() != game3d.PLATFORM_ANDROID:
        return False
    try:
        nTemperature = game3d.get_hunter_device_info('Battery_Temperature')
        if nTemperature == '':
            nTemperature = '0'
        nTemperature = float(nTemperature)
        szCPU = game3d.get_hunter_device_info('CPU').strip().lower()
        szCPUABI = game3d.get_hunter_device_info('CPU_ABI').strip().lower()
        szGPU = game3d.get_hunter_device_info('GPU').strip().lower()
        szGLVendor = game3d.get_hunter_device_info('GL_VENDOR').strip().lower()
        bHasBattery = bool(game3d.get_hunter_device_info('Is_Battery_Present'))
        bHasRooted = bool(game3d.get_hunter_device_info('is_rooted'))
        nScore = 0
        if nTemperature < 10.0:
            nScore += 1
        if 'armv7 processor rev 1 (v7l)' in szCPU or szCPU == '0' or '' == szCPU:
            nScore += 1
        if szCPUABI == 'x86' or '' == szCPUABI:
            nScore += 1
        if 'opengl es translator' in szGPU or 'angle' in szGPU or szGPU in ('yiwan',
                                                                            'bluestacks',
                                                                            'powervrg6400',
                                                                            'imagination',
                                                                            ''):
            nScore += 1
        if 'google' in szGLVendor or 'yiwan' == szGLVendor or 'bluestacks' == szGLVendor or '' == szGLVendor:
            nScore += 1
        if not bHasBattery:
            nScore += 1
        if bHasRooted:
            nScore += 1
        return nScore >= 4
    except:
        return False