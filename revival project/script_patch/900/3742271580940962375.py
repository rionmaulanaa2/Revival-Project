# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/NileSDK/Bedrock/NileCookieHelper.py
from .NileLocalDirectoryHelper import NileLocalDirectoryHelper
from .NileLogger import NileLogger
from ..Utils.NileFileSystem import NileFileSystem

class NileCookieHelper(object):

    @staticmethod
    def WriteCookie(roleId, activityName, cookieName, content):
        filePath = NileCookieHelper._GetCookiePath(roleId, activityName, cookieName)
        try:
            NileFileSystem.WriteText(filePath, content)
        except BaseException as e:
            NileLogger.Error('Cookie \xe5\x86\x99\xe5\x85\xa5\xe5\xa4\xb1\xe8\xb4\xa5, roleId: %s activityName: %s, message: %s' % (roleId, activityName, str(e)))

    @staticmethod
    def ReadCookie(roleId, activityName, cookieName):
        filePath = NileCookieHelper._GetCookiePath(roleId, activityName, cookieName)
        try:
            return NileFileSystem.ReadText(filePath)
        except BaseException as e:
            NileLogger.Error('Cookie \xe8\xaf\xbb\xe5\x8f\x96\xe5\xa4\xb1\xe8\xb4\xa5, roleId: %s activityName: %s, message: %s' % (roleId, activityName, str(e)))

        return ''

    @staticmethod
    def _GetCookiePath(roleId, activityName, cookieName):
        fileName = '%s_%s_%s' % (activityName, roleId, cookieName)
        return NileFileSystem.JoinPath(NileLocalDirectoryHelper.GetCookieDirectoryPath(), '%s.txt' % fileName)