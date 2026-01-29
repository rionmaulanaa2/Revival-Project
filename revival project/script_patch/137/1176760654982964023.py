# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/UniCineDriver/Movie/DirectorManager.py
from __future__ import absolute_import
from .MovieGroup import CoroutineMgrInstance

class END_BEHAVIOR(object):
    POP_AT_END = 1
    LOOP = 2
    PAUSE_AT_END = 3


class DirectorManager(object):

    def __init__(self):
        self.m_bIsPaused = False
        self.blackBoard = dict()
        self.m_movieGroupMont = None
        self.m_movieGroupDirector = None
        self.previewCamera = ''
        self.montTime = 0
        self.sceneTime = 0
        self.montEndTime = 0
        self.sceneEndTime = 0
        self.playRateEx = 1.0
        self.currentPlayRate = 1.0
        self.blackBoard['_lasttime'] = 0
        self.blackBoard['_targetCamera'] = ''
        self.blackBoard['_branchInfo'] = dict()
        self.blackBoard['_isFrameDrive'] = False
        self.blackBoard['_montFPS'] = 1.0
        self.m_bIsPaused = False
        self.blackBoard['_pause'] = False
        self.m_bIsStarted = False
        self.m_bIsPlaying = False
        self.m_bIsPreparing = False
        self.m_EndBehavior = 0
        self.movie_finish_callback = None
        self.set_director()
        return

    def play(self):
        self.m_bIsStarted = True
        self.m_bIsPreparing = False

    def stop_playing(self, forced=False):
        if callable(self.movie_finish_callback):
            self.movie_finish_callback(self.blackBoard.get('_moviekey', 'Default'), 'POST')
        if not forced:
            if self.blackBoard.get('_moviekey', 'Default') == 'EditorPreview' and self.m_EndBehavior == END_BEHAVIOR.POP_AT_END or self.m_EndBehavior == END_BEHAVIOR.PAUSE_AT_END:
                self.pause_at_end()
                if self.IsMontPlayMode():
                    self.goto(self.montEndTime / self.blackBoard['_montFPS'])
                else:
                    self.goto(self.sceneEndTime / self.blackBoard['_montFPS'])
                return False
        self.m_bIsStarted = False
        self.m_movieGroupMont.stop_playing()
        self.m_movieGroupDirector.stop_playing()
        if callable(self.movie_finish_callback):
            self.movie_finish_callback(self.blackBoard.get('_moviekey', 'Default'), 'POST_POP')
        self.clear_data()
        return True

    def pause_at_end(self):
        self.pause(True)

    def loadMontData(self, data):
        pass

    def loadMontModel(self, montmodel):
        self.loadGlobalSetting(montmodel)
        sceneroot = self._getRootModel(montmodel, 'SceneTrackRoot')
        self.m_movieGroupDirector.addMontChildren(sceneroot.children)
        montroot = self._getRootModel(montmodel, 'MontageTrackRoot')
        self.m_movieGroupMont.addMontChildren(montroot.children)
        self.montEndTime = montroot.properties['endTime'] * self.blackBoard['_montFPS']
        self.sceneEndTime = sceneroot.properties['endTime'] * self.blackBoard['_montFPS']

    def _getRootModel(self, model, rootname):
        for child in model.children:
            if child.properties['name'] == rootname:
                return child

    def _loadTimeline(self, model, director, timelinename):
        for child in model.children:
            if child.properties['name'] == timelinename:
                sceneroot = child
                break
        else:
            return False

        director.addMontChildren(sceneroot.children)

    def loadGlobalSetting(self, model):
        self.previewCamera = model.properties.get('previewCamera', '')
        self.m_EndBehavior = model.properties.get('endBehavior', END_BEHAVIOR.PAUSE_AT_END)
        self.blackBoard['_frameDrive'] = model.properties.get('globalSettings', {}).get('frameDrive', False)
        if self.blackBoard['_frameDrive']:
            self.blackBoard['_montFPS'] = model.properties.get('globalSettings', {}).get('montFPS', 1.0)
        else:
            self.blackBoard['_montFPS'] = 1.0
        self.blackBoard['_recruitByFrame'] = model.properties.get('globalSettings', {}).get('recruitByFrame', False)
        self.blackBoard['_trackPerFrame'] = model.properties.get('globalSettings', {}).get('trackPerFrame', 0)

    def sceneGoto(self, targetTime):
        targetTime = targetTime * self.blackBoard['_montFPS']
        self.m_movieGroupDirector.goto(targetTime, 0)
        self.setCameraByPreviewInfo()
        self.sceneTime = targetTime
        self.blackBoard['_lasttime'] = self.sceneTime
        self.montTime = targetTime

    def clear_data(self):
        self.montTime = 0
        self.sceneTime = 0
        self.currentPlayRate = 1.0
        self.m_bIsStarted = False
        self.m_bIsPlaying = False
        self.m_movieGroupDirector.stop_running_movie_action()
        self.m_movieGroupMont.stop_running_movie_action()
        self.blackBoard.clear()
        self.m_movieGroupDirector.clear_data()
        self.m_movieGroupMont.clear_data()
        self.blackBoard['_lasttime'] = 0

    def IsMontPlayMode(self):
        return self.previewCamera in ('Shot', 'ShotCut')

    def _shotupdate(self, n_cur_time, n_interval_time, force=False):
        self.m_movieGroupMont.update(n_cur_time, n_interval_time)
        if self.previewCamera in ('Shot', 'ShotCut'):
            shottrack = self.blackBoard.get('_Shot')
        else:
            shottrack = None
        trackPlayRate = self.m_movieGroupMont.customData.get('Playrate', 1.0)
        if shottrack and self.IsMontPlayMode():
            if shottrack.playrateUpdated:
                shottrack.playrateUpdated = False
                if trackPlayRate * shottrack.currentPlayRate != self.currentPlayRate:
                    self.currentPlayRate = trackPlayRate * shottrack.currentPlayRate
                    self._updatePlayRate()
            if shottrack.needGoto:
                shottrack.needGoto = False
                self.blackBoard['_lasttime'] = shottrack.currentSceneTime
                self.m_movieGroupDirector.goto(shottrack.currentSceneTime, shottrack.currentSceneInterval)
            else:
                self.m_movieGroupDirector.update(shottrack.currentSceneTime, shottrack.currentSceneInterval)
            self.sceneTime = shottrack.currentSceneTime
        else:
            self.sceneTime = n_cur_time
            self.m_movieGroupDirector.update(n_cur_time, n_interval_time, force=force)
        self.blackBoard['_lasttime'] = self.sceneTime
        if n_interval_time != 0:
            self.setCameraByPreviewInfo()
        return

    def update(self, dt, force=False):
        CoroutineMgrInstance.Excute()
        if not self.m_bIsStarted:
            return
        if self.m_bIsPaused:
            dt = 0
        n_interval_time = dt * self.playRateEx
        if self.IsMontPlayMode():
            n_interval_time *= self.m_movieGroupMont.customData.get('Playrate', 1.0)
        self.montTime += n_interval_time
        result = False
        if self.IsMontPlayMode():
            if self.montTime > self.montEndTime:
                if self.m_EndBehavior == END_BEHAVIOR.LOOP:
                    self.goto(0)
                else:
                    result = self.stop_playing()
        elif self.sceneTime > self.sceneEndTime:
            if self.m_EndBehavior == END_BEHAVIOR.LOOP:
                self.goto(0)
            else:
                result = self.stop_playing()
        self._shotupdate(self.montTime, n_interval_time, force=force)
        return result

    def goto(self, n_cur_time):
        n_cur_time = n_cur_time * self.blackBoard['_montFPS']
        n_interval_time = abs(n_cur_time - self.montTime)
        self.montTime = n_cur_time
        self.m_movieGroupMont.goto(n_cur_time, n_interval_time)
        shottrack = self.m_movieGroupMont.getTrackByName('Shot')
        if shottrack:
            if shottrack.playrateUpdated:
                shottrack.playrateUpdated = False
                self.currentPlayRate = shottrack.currentPlayRate * self.m_movieGroupMont.customData.get('Playrate', 1.0)
                self._updatePlayRate()
            shottrack.needGoto = False
            self.m_movieGroupDirector.goto(shottrack.currentSceneTime, shottrack.currentSceneInterval)
            self.sceneTime = shottrack.currentSceneTime
        else:
            self.sceneTime = n_cur_time
            self.m_movieGroupDirector.goto(n_cur_time, n_interval_time)
        self.setCameraByPreviewInfo()

    def cancel_goto(self, n_cur_time):
        self.m_movieGroupMont.cancel_goto(n_cur_time)
        self.m_movieGroupDirector.cancel_goto(n_cur_time)

    def pause(self, flag):
        if self.m_bIsPaused == flag:
            return
        self.m_bIsPaused = flag
        self.m_movieGroupMont.pause(flag)
        self.m_movieGroupDirector.pause(flag)
        self.blackBoard['_pause'] = flag

    def setPlayRate(self, playRate):
        self.playRateEx = playRate
        self._updatePlayRate()

    def _updatePlayRate(self):
        self.m_movieGroupDirector.updatePlayRate(self.playRateEx * self.currentPlayRate)

    def set_director(self):
        from .DirectorGroup.MovieGroupDirector import MovieGroupDirector
        self.m_movieGroupDirector = MovieGroupDirector(None)
        self.m_movieGroupMont = MovieGroupDirector(None)
        self.m_movieGroupMont.blackBoard = self.blackBoard
        self.m_movieGroupDirector.blackBoard = self.blackBoard
        return

    def setCameraByPreviewInfo(self):
        preview = str(self.previewCamera)
        blackboard = self.blackBoard
        cameramap = blackboard.get('cameramap', {})
        targetcamera = None
        if preview == 'Shot':
            shottrack = self.blackBoard.get('_Shot')
            if shottrack:
                targetcamera = cameramap.get(shottrack.currentCamName)
        elif preview == 'ShotCut':
            pass
        else:
            directormap = blackboard.get('directormap', {})
            if preview in directormap:
                directortrack = directormap[preview]
                if not directortrack._curspans:
                    return
                camname = directortrack._curspans[0]
                targetcamera = cameramap.get(str(camname.properties['name']))
            elif preview in cameramap:
                targetcamera = cameramap[preview]
        self.blackBoard['_targetCamera'] = targetcamera.name if targetcamera else ''
        self._updateCamera(targetcamera)
        return

    @staticmethod
    def setCameraDataNeoX--- This code section failed: ---

 329       0  LOAD_CONST            1  ''
           3  LOAD_CONST            0  ''
           6  IMPORT_NAME           0  'math3d'
           9  STORE_FAST            3  'math3d'

 330      12  LOAD_CONST            1  ''
          15  LOAD_CONST            2  ('set_cur_camera_params',)
          18  IMPORT_NAME           1  'MontageImp.TrackImp.UniGameInterface'
          21  IMPORT_FROM           2  'set_cur_camera_params'
          24  STORE_FAST            4  'set_cur_camera_params'
          27  POP_TOP          

 331      28  LOAD_FAST             3  'math3d'
          31  LOAD_ATTR             3  'vector'
          34  LOAD_FAST             0  'pos'
          37  CALL_FUNCTION_VAR_0     0 
          40  STORE_FAST            0  'pos'

 332      43  LOAD_FAST             3  'math3d'
          46  LOAD_ATTR             3  'vector'
          49  LOAD_FAST             1  'rot'
          52  CALL_FUNCTION_VAR_0     0 
          55  STORE_FAST            1  'rot'

 333      58  LOAD_FAST             4  'set_cur_camera_params'
          61  LOAD_CONST            3  'v3_pos'
          64  LOAD_CONST            4  'v3_rot'
          67  LOAD_FAST             1  'rot'
          70  LOAD_CONST            5  'n_fov'
          73  LOAD_FAST             2  'fov'
          76  CALL_FUNCTION_768   768 
          79  POP_TOP          

Parse error at or near `CALL_FUNCTION_768' instruction at offset 76

    @staticmethod
    def setCameraMatrixNeoX(transform, fov=None):
        from MontageImp.TrackImp.UniGameInterface import set_cur_camera_matrix
        set_cur_camera_matrix(transform, fov)

    def _updateCamera(self, camera):
        if camera:
            fov = camera.customData.get('Fov', 60)
            if getattr(camera, 'quaternionMatrix', None):
                self.setCameraMatrixNeoX(camera.quaternionMatrix, fov)
            elif camera.transform:
                pos = camera.transform.translate()
                rot = (camera.transform.pitch(), camera.transform.yaw(), camera.transform.roll())
                self.setCameraDataNeoX(pos, rot, fov)
        return

    def setTracksEnabled(self, enabletracks, disabletracks):
        self.blackBoard['_branchInfo']['act'] = enabletracks
        self.blackBoard['_branchInfo']['dct'] = disabletracks
        self.m_movieGroupDirector.refreshEnableStatus()