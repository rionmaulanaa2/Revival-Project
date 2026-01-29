# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageImp/MontResourceManagerImp.py
from __future__ import absolute_import
import MontageSDK
from MontageSDK.Lib import MontResourceManager as MRM
from MontageSDK.Lib.MontResourceManager import MontResourceManagerBase, ResGetter, ResourceInstance
from MontageSDK.Lib.MontResourceManager import AudioRes, EffectRes, CueRes, CharacterRes, SubmodelRes, SkeletonAnimationRes, CameraAnimationRes, RepoRes
import os
import game3d
import xml.etree.ElementTree as ET

class MontResourceManager(MontResourceManagerBase):

    def __init__(self):
        super(MontResourceManager, self).__init__()
        self.animationmap = {}

    @staticmethod
    def getResroot():
        return game3d.get_resource_root()

    def _updateSkeletonAnimations(self, skeletonkey, animconfigpath):
        animinfo = []
        if skeletonkey not in self.animationMap:
            self.animationMap[skeletonkey] = animinfo
        else:
            return
        doc = ET.parse(animconfigpath)
        animlist = doc.find('AnimationList')
        if animlist is None:
            return
        else:
            anims = animlist.findall('Animation')
            if anims is None or len(anims) == 0:
                return
            for anim in anims:
                filename = anim.attrib['FileName']
                filepath = os.path.join(os.path.dirname(animconfigpath), filename)
                duration = self._getAnimDuration(filepath)
                animinfo.append({'name': anim.attrib['Name'],
                   'res': anim.attrib['FileName'],
                   'duration': duration * 1000
                   })

            return

    def _getAnimDuration(self, filename):
        doc = ET.parse(filename)
        prop = doc.find('Property')
        if prop is None:
            return 1
        else:
            return float(prop.attrib['EndTime'])

    @ResGetter('Character')
    def getCharacterResList(self):
        charData = []
        rootDir = os.path.join(self.getResroot(), 'model_new')
        for root, dirs, files in os.walk(rootDir):
            for file in files:
                name, ext = os.path.splitext(file)
                resdirpath = os.path.relpath(root, os.path.join(self.getResroot(), 'model_new'))
                dirname = os.path.dirname(root + '\\' + file).split('\\')[-1]
                if ext.lower() == '.gim':
                    gimpath = os.path.relpath(root + '\\' + file, self.getResroot())
                    charData.append(CharacterRes(dirname, resdirpath.replace('\\', '/'), gimpath, dirname))

        return charData

    @ResGetter('Effect')
    def getEffects(self):
        res = []
        packageroot = self.getResroot()
        for root, dirs, files in os.walk(packageroot):
            relroot = os.path.relpath(root, packageroot).replace('\\', '/')
            for name in files:
                base, ext = os.path.splitext(name)
                if ext.lower() in ('.sfx', '.pse'):
                    path = os.path.join(relroot, name)
                    path = path.replace('\\', '/')
                    res.append(EffectRes(base, path))

        return res

    @ResGetter('CameraAnimation')
    def getCamAnim(self):
        res = []
        packageroot = self.getResroot()
        for root, dirs, files in os.walk(packageroot):
            relroot = os.path.relpath(root, packageroot).replace('\\', '/')
            for name in files:
                base, ext = os.path.splitext(name)
                if ext.lower() == '.trk':
                    path = os.path.join(relroot, name)
                    res.append(CameraAnimationRes(base, path, 1))

        return res

    @ResGetter('Music')
    def getMusic(self):
        return []
        from UniCineDriver.GameLogic import load_audio_data
        resdata = {}
        load_audio_data(resdata)
        res = []
        for r in resdata['AudioInfo'].keys():
            res.append(AudioRes(r, r, 'wwise', r, 1, r))

        return res


def getInstance():
    return MRM.getInstance()


def setInstance(instance):
    MRM.setInstance(instance)


MRM.setInstance(MontResourceManager())