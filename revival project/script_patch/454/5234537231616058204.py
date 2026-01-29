# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/UniCineDriver/Movie/DirectorGroup/MovieGroupDirector.py
from ..MovieGroup import MovieGroup

class MovieGroupDirector(MovieGroup):

    def __init__(self, data):
        super(MovieGroupDirector, self).__init__(data)
        self.m_bIsAudioFirstLoaded = False

    @property
    def type(self):
        return 'Director'

    def getAllMovieActions(self):
        tracks = []
        curGroups = self.chilrenGroups
        while len(curGroups) > 0:
            childGroups = []
            for group in curGroups:
                tracks.extend(group.tracks)
                childGroups.extend(group.chilrenGroups)

            curGroups = childGroups

        tracks.extend(self.tracks)
        return tracks

    def traverseGroup(self, filterCb):
        if not callable(filterCb):
            return
        groups = self.chilrenGroups
        while len(groups) > 0:
            childrenGroups = []
            for group in groups:
                ret = filterCb(group)
                if ret is True:
                    return
                childrenGroups.extend(group.chilrenGroups)

            groups = childrenGroups

    def refreshEnableStatus(self):
        alltracks = self.getAllMovieActions()
        acts = self.blackBoard['_branchInfo'].get('act', [])
        dcts = self.blackBoard['_branchInfo'].get('dct', [])
        for dct in dcts:
            for track in alltracks:
                if track.uuid == dct:
                    track.change_disabled(True)

        for act in acts:
            for track in alltracks:
                if track.uuid == act:
                    track.change_disabled(False)

    def DeleteTrackByUuid(self, uuid):
        allTracks = self.getAllMovieActions()
        for track in allTracks:
            if track.uuid == uuid:
                track.clear_data()
                return True
        else:
            movieGroup = []
            parentMovieGroup = []

            def filterCb(group):
                groupMap = {g.uuid:g for g in group.chilrenGroups}
                if uuid in groupMap.keys():
                    parentMovieGroup.append(group)
                    movieGroup.append(groupMap[uuid])
                if group.uuid == uuid:
                    movieGroup.append(group)
                    if group in self.chilrenGroups:
                        parentMovieGroup.append(self)
                if not parentMovieGroup and group.uuid == uuid:
                    parentMovieGroup.append(group)
                if movieGroup and parentMovieGroup:
                    return True

            self.traverseGroup(filterCb)
            if movieGroup and parentMovieGroup:
                movieGroup[0].clear_data()
                parentMovieGroup[0].chilrenGroups.remove(movieGroup[0])
                return True

        return False

    def GetActionByUuid(self, uuid):
        allTracks = self.getAllMovieActions()
        for track in allTracks:
            if track.uuid == uuid:
                return track

        return None

    def SetTrackProperty(self, uuid, key, value):
        for action in self.getAllMovieActions():
            if action.uuid == uuid:
                action.SetProperty(key, value)
                return True
        else:
            movieGroup = []

            def filterCb(group):
                if group.uuid == uuid:
                    movieGroup.append(group)
                    return True

            self.traverseGroup(filterCb)
            if movieGroup:
                movieGroup[0].properties[key] = value
                return True

        return False

    def AddGroupChild(self, parentUuid, model):
        parentMovieGroup = []

        def filterCb(group):
            if group.uuid == parentUuid:
                parentMovieGroup.append(group)
                return True

        if parentUuid == self.uuid:
            parentMovieGroup.append(self)
        else:
            self.traverseGroup(filterCb)
        if parentMovieGroup:
            parentMovieGroup[0].AddMontChild(model)