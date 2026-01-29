# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/PlatformAPI/EditAPI.py


class EngineEditAPI(object):

    @classmethod
    def AddTimer(cls, delay, func, *args, **kwargs):
        try:
            import Timer
            return Timer.AddTimer(delay, func, *args, **kwargs)
        except ImportError:
            raise NotImplementedError

    @classmethod
    def AddRepeatTimer(cls, delay, func, *args, **kwargs):
        try:
            import Timer
            return Timer.AddRepeatTimer(delay, func, *args, **kwargs)
        except ImportError:
            raise NotImplementedError

    @classmethod
    def CancelTimer(cls, timerID):
        try:
            import Timer
            return Timer.CancelTimer(timerID)
        except ImportError:
            raise NotImplementedError

    @classmethod
    def RegisterKeyboardListener(cls, listener):
        try:
            from Input import Input
            keys = []
            for v in dir(Input):
                if v.startswith('KEY_'):
                    keys.append(getattr(Input, v))

            Input().listenKeyDown(listener.OnKeyDown, *keys)
            Input().listenKeyUp(listener.OnKeyUp, *keys)
        except ImportError:
            raise NotImplementedError

    @classmethod
    def RegisterMouseListener(cls, listener):
        try:
            from Input import Input
            Input().listenMouseWheelDown(listener.OnMouseWheelDown)
            Input().listenMouseWheelUp(listener.OnMouseWheelUp)
        except ImportError:
            raise NotImplementedError

    @classmethod
    def RegisterTouchListener(cls, listener):
        try:
            from Input import Input
            Input().listenTouchDragBegin(listener.OnTouchDragBegin)
            Input().listenTouchDragMove(listener.OnTouchDragMove)
            Input().listenTouchDragEnd(listener.OnTouchDragEnd)
        except ImportError:
            raise NotImplementedError

    def RegisterPlayerAvatarReadyCallback(self, callback):
        raise NotImplementedError

    def RegisterBeforeChangeSceneCallback(self, callback):
        raise NotImplementedError

    def RegisterSceneChangedCallback(self, callback):
        raise NotImplementedError

    def IsGameReady(self):
        raise NotImplementedError

    def GetPlayerAvatar(self):
        raise NotImplementedError

    def HideAllGui(self):
        raise NotImplementedError

    def RestoreGui(self):
        raise NotImplementedError

    def GetSpaceNo(self):
        player = self.GetPlayerAvatar()
        if player:
            if hasattr(player, 'space'):
                return player.space.spaceno
            if hasattr(player, 'Space'):
                return player.Space.spaceno
        raise NotImplementedError

    def TriggerFreeview(self):
        try:
            import GlobalData
            GlobalData.camera.TriggerFreeview()
        except ImportError:
            raise NotImplementedError

    def CloseFreeview(self):
        try:
            import GlobalData
            GlobalData.camera.CloseFreeview()
        except ImportError:
            raise NotImplementedError

    def OnEnterSpace(self):
        pass

    def InitEditorTouch(self, owner):
        return None

    @classmethod
    def IsGizmoVisible(cls):
        return True


_EngineEditAPIImpl = None

def SetEngineEditAPI(editAPI):
    global _EngineEditAPIImpl
    _EngineEditAPIImpl = editAPI


def GetEngineEditAPI():
    return _EngineEditAPIImpl