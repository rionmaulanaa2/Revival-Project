# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/UniCineDriver/UniCineManager.py
from __future__ import absolute_import
from .Movie.DirectorManager import DirectorManager, END_BEHAVIOR
from .UniGameInterfaceBase import UniGameInterfaceBase

def GetGameFPS():
    try:
        from MontageImp.TrackImp.UniGameInterface import getGameFPS
        return getGameFPS()
    except ImportError:
        return 60


class UniCineManager(object):

    def __init__(self):
        self.interface = UniGameInterfaceBase
        self.movies = dict()
        self.movie_finish_callback = None
        return

    def registerInterface(self, interface):
        if issubclass(interface, UniGameInterfaceBase):
            self.interface = interface

    @property
    def DefaultDirector(self):
        return self.movies.get('Default')

    def goto(self, t, moviekey='Default'):
        if moviekey in self.movies:
            self.movies[moviekey].goto(t)

    def sceneGoto(self, t, moviekey='Default'):
        if moviekey in self.movies:
            self.movies[moviekey].sceneGoto(t)

    def update(self, dtsecond):
        for moviekey, director in self.movies.items():
            if director.blackBoard['_frameDrive']:
                gameFPS = GetGameFPS()
                montFPS = director.blackBoard['_montFPS']
                if gameFPS > montFPS:
                    director.update(float(montFPS) * dtsecond)
                else:
                    director.update(1)
            else:
                director.update(dtsecond)
            if director.m_EndBehavior == END_BEHAVIOR.POP_AT_END and not director.m_bIsPreparing and not director.m_bIsStarted:
                self.movies.pop(moviekey)

    def play(self, data, moviekey='Default'):
        if moviekey in self.movies:
            director = self.movies[moviekey]
        else:
            director = self.movies[moviekey] = DirectorManager()
        director.blackBoard['_moviekey'] = moviekey
        director.loadMontModel(data)
        director.movie_finish_callback = self.movie_finish_callback
        if self.interface.needWarmUp():
            self.interface.registerWarmUpFinishCb(director.play)
            director.m_bIsPreparing = True
        else:
            director.play()

    def stop_playing(self, moviekey='Default'):
        if moviekey in self.movies:
            director = self.movies[moviekey]
            director.stop_playing(True)
            if director.m_EndBehavior == END_BEHAVIOR.POP_AT_END and not director.m_bIsStarted:
                self.movies.pop(moviekey)

    def pause(self, flag, moviekey='Default'):
        if moviekey in self.movies:
            self.movies[moviekey].pause(flag)

    def getMontTime(self, moviekey='Default'):
        if moviekey not in self.movies:
            return 0
        montFPS = self.movies[moviekey].blackBoard['_montFPS']
        return self.movies[moviekey].montTime / float(montFPS)

    def getSceneTime(self, moviekey='Default'):
        if moviekey not in self.movies:
            return 0
        montFPS = self.movies[moviekey].blackBoard['_montFPS']
        return self.movies[moviekey].sceneTime / float(montFPS)

    def isPaused(self, moviekey='Default'):
        if moviekey not in self.movies:
            return None
        else:
            return self.movies[moviekey].m_bIsPaused

    def setPlayRate(self, moviekey='Default', playRate=1.0):
        if moviekey not in self.movies:
            return 0
        self.movies[moviekey].setPlayRate(playRate)

    def setTracksEnabled(self, moviekey='Default', enabletracks=None, disabletracks=None):
        if moviekey not in self.movies:
            return 0
        return self.movies[moviekey].setTracksEnabled(enabletracks, disabletracks)