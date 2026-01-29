# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageImp/TrackImp/GlobalTracks.py
from __future__ import absolute_import
import json
import MontageSDK
from UniCineDriver.Movie.MovieObject import MovieTrackCls
from UniCineDriver.Movie.MovieActionSpan import MovieActionSpan
from UniCineDriver.Movie.MovieActionKeyframe import MovieActionKeyframe, MovieActionTriggerKeyframe
from MontageImp.DivergeManagers.DivergeManager import DivergeManagerIns
import math3d
from .UniGameInterface import set_cur_camera_params
from UniCineDriver.Utils.Formula import binarySearchLeft

@MovieTrackCls('\xe5\xad\x97\xe5\xb9\x95\xe8\xbd\xa8\xe9\x81\x93')
class SubTitle(MovieActionSpan):

    def onSpanFrameEnter(self, frame):
        _text = str(frame.properties['text'])
        _pos = frame.properties['pos']
        _color = frame.properties['color']
        _fontSize = frame.properties['size']
        global_data.montage_editor.uiHelper.showText(_text, color=_color, fontSize=_fontSize)

    def onSpanFrameLeave(self, frame):
        _text = str(frame.properties['text'])
        global_data.montage_editor.uiHelper.hideText()


@MovieTrackCls('\xe5\x9b\xbe\xe7\x89\x87')
class MonTexture(MovieActionTriggerKeyframe):

    def __init__(self, *args, **kwargs):
        super(MonTexture, self).__init__(*args, **kwargs)
        self.activate = False
        self.filename = None
        return

    def trigger(self, data):
        self.filename = str(data['filename'])
        self.activate = data['activate']
        self.size = data['size']
        self.position = data['pos']
        self.origin = data['origin']
        if self.activate:
            global_data.montage_editor.uiHelper.showImage(self.filename, self.position, self.size, self.origin)
        else:
            global_data.montage_editor.uiHelper.hideImage()

    def reset(self):
        if self.activate:
            global_data.montage_editor.uiHelper.hideImage()
        else:
            global_data.montage_editor.uiHelper.showImage(self.filename, self.position, self.size, self.origin)


@MovieTrackCls('Director')
class DirectorKeySpan(MovieActionSpan):

    def __init__(self, model, parent_movie_group):
        super(DirectorKeySpan, self).__init__(model, parent_movie_group)
        self.m_parentMovieGroup().blackBoard.setdefault('directormap', {})[str(self.name)] = self


class ImprogedMovieActionTriggerKeyframe(MovieActionTriggerKeyframe):

    def update(self, n_cur_time, n_interval_time, force=False):
        CurNodeIndex = binarySearchLeft(self.frames, n_cur_time, lambda x: x.time) - 1
        if CurNodeIndex != self.m_nCurNodeIndex:
            self.m_nCurNodeIndex = CurNodeIndex
            if self.m_nCurNodeIndex < 0:
                self.reset()
            elif self.m_nCurNodeIndex < len(self.frames):
                node = self.frames[self.m_nCurNodeIndex]
                framebuffer = []
                for keyframe in self.frames:
                    if keyframe is node:
                        framebuffer.append(keyframe)
                        break
                    triggerTime = keyframe.time
                    if triggerTime == node.time:
                        framebuffer.append(keyframe)

                for node in framebuffer:
                    if n_cur_time - n_interval_time <= node.time:
                        self.trigger(node.properties)


class Diverge(ImprogedMovieActionTriggerKeyframe):
    ORDER = 50

    def switchBranch(self, branchName=None, time=0.0, *args):
        branchName = branchName or '_master'
        groupName = MontageSDK.Interface.getDefaultGroupName()
        MontageSDK.Interface.SwitchToBranch(groupName, branchName)
        MontageSDK.Interface.PauseCinematics(False)


@MovieTrackCls('\xe9\x80\x89\xe6\x8b\xa9\xe5\x88\x86\xe6\xad\xa7')
class SelectDiverge(Diverge):

    def trigger(self, data):
        groupName = MontageSDK.Interface.getDefaultGroupName()
        result = MontageSDK.Interface.GetScenePlayingStatus(groupName)
        if not result['isPaused']:
            DivergeManagerIns.handleSelectDiverge(data, switchFunc=self.switchBranch, optionsFunc=global_data.montage_editor.uiHelper.showOptions)

    def reset(self):
        global_data.montage_editor.uiHelper.hideOptions()

    def stop_playing(self):
        global_data.montage_editor.uiHelper.hideOptions()

    def switchBranch(self, branchName=None, time=0.0, *args):
        super(SelectDiverge, self).switchBranch(branchName)
        global_data.montage_editor.uiHelper.hideOptions()


@MovieTrackCls('\xe6\x9d\xa1\xe4\xbb\xb6\xe5\x88\x86\xe6\xad\xa7')
class ConditionDiverge(Diverge):

    def trigger(self, data):
        groupName = MontageSDK.Interface.getDefaultGroupName()
        result = MontageSDK.Interface.GetScenePlayingStatus(groupName)
        if not result['isPaused']:
            DivergeManagerIns.handleConditionDiverge(data, switchFunc=self.switchBranch)


@MovieTrackCls('\xe8\xae\xbe\xe7\xbd\xae\xe5\x8f\x98\xe9\x87\x8f')
class SetVar(ImprogedMovieActionTriggerKeyframe):

    def trigger(self, data):
        groupname = MontageSDK.Interface.getDefaultGroupName()
        result = MontageSDK.Interface.GetScenePlayingStatus(groupname)
        if not result['isPaused']:
            DivergeManagerIns.handleSetVar(data)


@MovieTrackCls('\xe8\xb7\xb3\xe8\xbf\x87')
class Leap(MovieActionSpan):

    def onSpanFrameEnter(self, frame):
        t = frame.time + frame.duration
        groupname = MontageSDK.Interface.getDefaultGroupName()
        result = MontageSDK.Interface.GetScenePlayingStatus(groupname)
        if not result['isPaused']:
            MontageSDK.Interface.setCineEpisodeTime(t, False, groupname)