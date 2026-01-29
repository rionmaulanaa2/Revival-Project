# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/uielment/CCCSBNode.py
from __future__ import absolute_import
from __future__ import print_function
import ccui
import cc
from common.uisys.ui_proxy import ProxyClass, trans2ProxyObj
from .CCNode import CCNode
from .CCLayer import CCLayer
from common.uisys.cocomate import get_cocomate_layout
from common.uisys.uielment.CCNode import hash_mod

class CCCSBNode(object):

    def PlayAnimation(self, aniName, adjust_to_time=-1, force_resume=False, scale=1.0):
        if not self.hasTimelineAnimation(aniName):
            print(__file__, '!!!!!!!!!!!!!!!!!aniName [%s] not exists!' % str(aniName))
            return []
        if not self.getParent():
            self.resumeAllAnimation()
        time_scale = -1
        max_time = self.GetAnimationMaxRunTime(aniName)
        if adjust_to_time > 0:
            if max_time > 0:
                time_scale = max_time / adjust_to_time
        elif scale != 1.0:
            time_scale = scale
        if time_scale != 1.0:
            self.playAnimation(aniName, 0, time_scale)
        else:
            self.playAnimation(aniName, 0)
        if force_resume:
            for node in self.GetAnimationNodes(aniName):
                node.resume()

        return []

    def GetAnimationMaxRunTime(self, aniName):
        return self.getAnimationRunTime(aniName)

    def GetAnimationPlayTimes(self, aniName):
        return self.getAnimationLoopTimes(aniName)

    def StopAnimation(self, aniName, finish_ani=False):
        if finish_ani:
            max_time = self.GetAnimationMaxRunTime(aniName)
            self.FastForwardToAnimationTime(aniName, max_time)
            return
        self.stopAnimation(aniName)

    def IsPlayingAnimation(self, aniName):
        return self.isAnimationPlaying(aniName)

    def RecordAnimationNodeState(self, aniName, black_dict=None):
        node_states = {}
        nodes = self.GetAnimationNodes(aniName)
        for node in nodes:
            node_states[node] = {'pos': node.getPosition(),'scaleX': node.getScaleX(),
               'scaleY': node.getScaleY(),
               'rot': node.getRotation(),
               'opacity': node.getOpacity(),
               'size': node.getContentSize()
               }
            black_set_of_node = None
            if black_dict is not None and node.widget_name in black_dict:
                black_set_of_node = black_dict[node.widget_name]
            if black_set_of_node is None or 'visibility' not in black_set_of_node:
                node_states[node]['visibility'] = node.isVisible()

        self._recorded_ani_node_states.update({aniName: node_states})
        return

    def GetAnimationNodes(self, aniName):
        aniTimeline = self.getTimelineAnimation(aniName)
        ani_nodes = []
        if aniTimeline:
            for timeline in aniTimeline.getTimelines():
                ani_nodes.append(trans2ProxyObj(timeline.getNode()))

            return ani_nodes
        return []

    def HasAnimation(self, aniName):
        return self.hasTimelineAnimation(aniName)

    def FastForwardToAnimationTime(self, aniName, time):
        if self.GetAnimationPlayTimes(aniName) > 1000:
            log_error('FastForwardToAnimationTime dont work!!!!!!!')
            import traceback
            traceback.print_stack()
            return
        if not self.HasAnimation(aniName):
            return
        aniTimeline = self.getTimelineAnimation(aniName)
        startFrame = aniTimeline.getStartFrame()
        endFrame = aniTimeline.getEndFrame()
        max_time = self.GetAnimationMaxRunTime(aniName)
        percent = min(max(float(time) / max_time, 0), 1)
        currentFrame = int(percent * (endFrame - startFrame) + startFrame)
        aniTimeline.gotoFrameAndPause(currentFrame)

    def GetConfUserData(self):
        from common.uisys.cocomate import get_ext_data
        ext_data = get_ext_data(self)
        if ext_data:
            return ext_data
        return {}

    def GetAnimationNameList(self):
        return self.getAnimationNameList() or []

    def GetTypeName(self):
        return self.type_name

    def RecordNodeInfo(self):
        cocomate_layout = get_cocomate_layout(self)
        if cocomate_layout:
            raw_size = cocomate_layout.getRawSizeWithRect()
            raw_pos = cocomate_layout.getRawPositionWithRect()
            self._conf['pos'] = {'x': '%s%%%s' % (raw_pos.xPercent, raw_pos.xOffset),'y': '%s%%%s' % (raw_pos.yPercent, raw_pos.yOffset)}
            self._conf['size'] = {'width': '%s%%%s' % (raw_size.xPercent, raw_size.xOffset),'height': '%s%%%s' % (raw_size.yPercent, raw_size.yOffset)}
        self._conf['hide'] = self.getVisible()
        self._conf['color'] = self.getColor()
        self._conf['scale'] = {'x': self.getScaleX(),'y': self.getScaleY()}
        self._conf['opacity'] = self.getOpacity()

    def RecordNodeInfoRecursion(self):
        self.RecordNodeInfo()
        for child in self.GetChildren():
            child.RecordNodeInfo()

    def GetConfSize(self):
        cocomate_layout = get_cocomate_layout(self)
        if cocomate_layout:
            raw_size = cocomate_layout.getRawSizeWithRect()
            size = {'width': '%s%%%s' % (raw_size.xPercent, raw_size.xOffset),'height': '%s%%%s' % (raw_size.yPercent, raw_size.yOffset)}
            cc_size = self.CalcSize(size['width'], size['height'])
            return cc_size
        else:
            return None