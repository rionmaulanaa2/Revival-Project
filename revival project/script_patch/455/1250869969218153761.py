# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/UniCineDriver/Movie/MovieGroup.py
from __future__ import absolute_import
from .MovieObject import MovieObject, getMovieCls

class MovieGroup(MovieObject):
    s_dictMovieAction = {}
    trackCount = 0

    def __init__(self, data=None, blackBoard=None):
        super(MovieGroup, self).__init__()
        self.chilrenGroups = []
        self.tracks = []
        self.runningAction = set()
        self.blackBoard = blackBoard
        self.m_dictRunningAction = {}
        self.m_bHasFinishOneTurn = False
        self.name = ''
        self.uuid = ''
        self.customData = {}
        self.loadFromMontModel(data)

    def updatePlayRate(self, rate):
        for group in self.chilrenGroups:
            group.updatePlayRate(rate)

        for track in self.tracks:
            track.updatePlayRate(rate)

    def afterinit(self):
        pass

    def __getitem__(self, item):
        return self.getTrackByName(item)

    def getTrackByName(self, name):
        for track in self.tracks:
            if track.properties['name'] == name:
                return track

    def addMontChildren(self, children):

        def trackGenerator():
            recruitByFrame = self.blackBoard.get('_recruitByFrame', False)
            trackPerFrame = self.blackBoard.get('_trackPerFrame', 0)
            if self.blackBoard['_moviekey'] == 'EditorPreview':
                trackPerFrame = 0
            for child in children:
                typename = str(child.properties['type'])
                cls, clstype = getMovieCls(typename, self.properties.get('type', '_root'))
                if clstype == 'Track':
                    track = cls(child, self)
                    track._pathname = typename
                    self.tracks.append(track)
                elif clstype == 'Group':
                    group = cls(child, self.blackBoard)
                    group.afterinit()
                    self.chilrenGroups.append(group)
                    MovieGroup.trackCount += 1
                else:
                    self._tryAddTrackRecursive(child, [])
                if recruitByFrame and MovieGroup.trackCount >= trackPerFrame > 0:
                    MovieGroup.trackCount = 0
                    yield

        CoroutineMgrInstance.StartCoroutine(trackGenerator())

    def _tryAddTrackRecursive(self, model, pathlist):
        metatype = model.properties['_metacls']
        tracktype = str(model.properties['type'])
        cls, clstype = getMovieCls(metatype)
        if clstype == 'Track':
            track = cls(model, self)
            self.tracks.append(track)
            track._pathname = '/'.join(pathlist + [tracktype])
        else:
            pathlist.append(tracktype)
            for child in model.children:
                self._tryAddTrackRecursive(child, list(pathlist))

    def AddMontChild(self, child):
        typename = str(child.properties['type'])
        cls, clstype = getMovieCls(typename, self.properties.get('type', '_root'))
        if clstype == 'Track':
            track = cls(child, self)
            track._pathname = typename
            self.tracks.append(track)
        elif clstype == 'Group':
            group = cls(child, self.blackBoard)
            group.afterinit()
            self.chilrenGroups.append(group)
        else:
            self._tryAddTrackRecursive(child, [])

    def DeleteChildGroup(self, group):
        if group in self.chilrenGroups:
            self.chilrenGroups.remove(group)

    def DeleteChildTrack(self, track):
        if track in self.tracks:
            self.tracks.remove(track)

    def loadFromMontModel(self, model):
        from copy import deepcopy
        if model is None:
            return
        else:
            self.uuid = model.uuid
            self.properties = deepcopy(model.properties)
            self.name = str(self.properties['name'])
            self.addMontChildren(model.children)
            return

    def setCustomData(self, pathlist, value):
        if len(pathlist) == 0:
            return
        currentdict = self.customData
        for p in pathlist[:-1]:
            currentdict = currentdict.setdefault(p, {})

        currentdict[pathlist[-1]] = value

    @property
    def type(self):
        return ''

    def clear_data(self):
        self.m_dictRunningAction.clear()
        for group in self.chilrenGroups:
            group.clear_data()

        for track in self.tracks:
            track.clear_data()

        self.tracks = []
        self.chilrenGroups = []

    def applyCustomData(self, data):
        pass

    def update(self, n_cur_time, n_interval_time, force=False):
        for movie_action in sorted(self.tracks, key=lambda movie_action: movie_action.ORDER):
            if movie_action.ACTION_TYPE == 'Key':
                if not movie_action.properties.get('disabled', False):
                    movie_action.update(n_cur_time, n_interval_time, force=force)
            elif movie_action.ACTION_TYPE == 'Span':
                if not movie_action.properties.get('disabled', False):
                    if not movie_action.is_started() and movie_action.is_in_range(n_cur_time):
                        self.runningAction.add(movie_action)

        toremove = set()
        for movie_action in list(self.runningAction):
            if movie_action.properties.get('disabled', False):
                continue
            if movie_action.is_in_range(n_cur_time):
                movie_action.update(n_cur_time, n_interval_time)
            else:
                movie_action.on_end()
                toremove.add(movie_action)

        for action in toremove:
            self.runningAction.remove(action)

        self.applyCustomData(self.customData)
        if self.m_bHasFinishOneTurn is False:
            self.m_bHasFinishOneTurn = True
            self.on_finish_one_turn()
        shottrack = self.blackBoard.get('_Shot', None)
        for group in self.chilrenGroups:
            if group.properties['type'] == 'CameraActor' and group.name != self.blackBoard.get('_targetCamera'):
                if not shottrack or not shottrack.cameraChange:
                    continue
            group.update(n_cur_time, n_interval_time, force=force)

        return

    def goto(self, n_cur_time, n_interval_time):
        for movie_action in self.tracks:
            if movie_action.ACTION_TYPE == 'Key':
                if not movie_action.properties.get('disabled', False):
                    movie_action.goto(n_cur_time, n_interval_time)
            elif movie_action.ACTION_TYPE == 'Span':
                if movie_action.properties.get('disabled', False):
                    continue
                if not movie_action.properties.get('disabled', False):
                    if movie_action.is_in_range(n_cur_time) and not movie_action.is_started():
                        self.runningAction.add(movie_action)

        toremove = set()
        toenter = set()
        for movie_action in self.runningAction:
            if movie_action.is_in_range(n_cur_time):
                toenter.add(movie_action)
            else:
                toremove.add(movie_action)

        for action in toremove:
            action.on_end()
            self.runningAction.remove(action)

        for action in toenter:
            action.goto(n_cur_time, n_interval_time)

        self.applyCustomData(self.customData)
        for group in self.chilrenGroups:
            group.goto(n_cur_time, n_interval_time)

    def pause(self, flag):
        for movie_action in self.runningAction:
            if not movie_action.properties.get('disabled', False):
                movie_action.pause(flag)

        for group in self.chilrenGroups:
            group.pause(flag)

    def stop_playing(self):
        self.m_bHasFinishOneTurn = False
        for movie_action in self.tracks:
            movie_action.stop_playing()

        self.runningAction.clear()
        for group in self.chilrenGroups:
            group.stop_playing()

    def stop_running_movie_action(self):
        for movie_action in self.runningAction:
            movie_action.on_end()

        self.runningAction.clear()
        for group in self.chilrenGroups:
            group.stop_running_movie_action()

    def on_finish_one_turn(self):
        for group in self.chilrenGroups:
            group.on_finish_one_turn()


class CoroutineMgr(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        super(CoroutineMgr, self).__init__()
        self._Generators = []

    def StartCoroutine(self, generator):
        import types
        if not isinstance(generator, types.GeneratorType) or generator in self._Generators:
            return
        try:
            next(generator)
        except StopIteration:
            pass
        else:
            self._Generators.append(generator)

    def StopAllCoroutine(self):
        self._Generators = []

    def Excute(self):
        todel = []
        for generator in self._Generators:
            try:
                next(generator)
            except StopIteration:
                todel.append(generator)

        for gen in todel:
            self._Generators.remove(gen)


CoroutineMgrInstance = CoroutineMgr()