# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Plugin/RainbowPlugin/Platforms/NeoX/Asset/NeoXResourceManager.py
import json
import os
from functools import partial
import game3d
from .NeoXThumbnailManager import NeoXThumbnailManager

class NeoXResourceManager(object):
    FILE_TYPES = {'default': {'GroupType': 'Unknown',
                   'Type': 'Unknown',
                   'IconType': 'Default'
                   },
       'scn': {'GroupType': 'Scene',
               'Type': 'Scene',
               'IconType': 'Terrain'
               },
       'gim': {'GroupType': 'Model',
               'Type': 'ModelNormal',
               'IconType': 'PrefabNormal'
               },
       'mesh': {'GroupType': 'Mesh',
                'Type': 'Mesh',
                'IconType': 'Default'
                },
       'gis': {'GroupType': 'Animation',
               'Type': 'AnimationConfig',
               'IconType': 'AnimationFile'
               },
       'group': {'GroupType': 'Model',
                 'Type': 'ModelGroup',
                 'IconType': 'GroupFile'
                 },
       'nprefab': {'GroupType': 'Prefab',
                   'Type': 'Prefab',
                   'IconType': 'PrefabFile'
                   },
       'skeleton': {'GroupType': 'Skeleton',
                    'Type': 'Skeleton',
                    'IconType': 'SkeletonFile'
                    },
       'animconfig': {'GroupType': 'Animation',
                      'Type': 'AnimationConfig',
                      'IconType': 'AnimConfigFile'
                      },
       'animation': {'GroupType': 'Animation',
                     'Type': 'AnimationClip',
                     'IconType': 'AnimationFile'
                     },
       'animcomposite': {'GroupType': 'Animation',
                         'Type': 'AnimationCombine',
                         'IconType': 'AnimCompositeFile'
                         },
       'animmontage': {'GroupType': 'Animation',
                       'Type': 'AnimationMontage',
                       'IconType': 'AnimMontageFile'
                       },
       'blendspace1d': {'GroupType': 'Animation',
                        'Type': 'AnimationBlendSpace1d',
                        'IconType': 'BlendSpace1dFile'
                        },
       'blendspace': {'GroupType': 'Animation',
                      'Type': 'AnimationBlendSpace2d',
                      'IconType': 'BlendSpaceFile'
                      },
       'animgraph': {'GroupType': 'Animation',
                     'Type': 'AnimationGraph',
                     'IconType': 'AnimGraphFile'
                     },
       'physics': {'GroupType': 'Physics',
                   'Type': 'Physics',
                   'IconType': 'PhysicsFile'
                   },
       'Vehicle': {'GroupType': 'Vehicle',
                   'Type': 'Vehicle',
                   'IconType': 'VehicleFile'
                   },
       'aircraft': {'GroupType': 'Aircraft',
                    'Type': 'Aircraft',
                    'IconType': 'AircraftFile'
                    },
       'wheel': {'GroupType': 'Wheel',
                 'Type': 'Wheel',
                 'IconType': 'WheelFile'
                 },
       'tire': {'GroupType': 'Tire',
                'Type': 'Tire',
                'IconType': 'TireFile'
                },
       'ragdoll': {'GroupType': 'Physics',
                   'Type': 'NewRagdoll',
                   'IconType': 'PhysicsFile'
                   },
       'stb': {'GroupType': 'Physics',
               'Type': 'SoftBone',
               'IconType': 'SoftBoneFile'
               },
       'mtg': {'GroupType': 'Material',
               'Type': 'MaterialMTG',
               'IconType': 'MaterialGroup'
               },
       'mtl': {'GroupType': 'Material',
               'Type': 'MaterialMTL',
               'IconType': 'Material'
               },
       'gpse': {'GroupType': 'Unknown',
                'Type': 'Unknown',
                'IconType': 'Default'
                },
       'pmg': {'GroupType': 'PhysicalMaterial',
               'Type': 'PhysicalMaterial',
               'IconType': 'PhysicalMtl'
               },
       'image': {'GroupType': 'Texture',
                 'Type': 'Texture',
                 'IconType': 'Texture'
                 },
       'dds': {'GroupType': 'Texture',
               'Type': 'Texture',
               'IconType': 'Texture'
               },
       'vol': {'GroupType': 'Texture',
               'Type': 'Texture',
               'IconType': 'Texture'
               },
       'tga': {'GroupType': 'Texture',
               'Type': 'Texture',
               'IconType': 'Texture'
               },
       'jpg': {'GroupType': 'Texture',
               'Type': 'Texture',
               'IconType': 'Texture'
               },
       'spr': {'GroupType': 'Texture',
               'Type': 'Texture',
               'IconType': 'Texture'
               },
       'png': {'GroupType': 'Texture',
               'Type': 'Texture',
               'IconType': 'Texture'
               },
       'exr': {'GroupType': 'Texture',
               'Type': 'Texture',
               'IconType': 'Texture'
               },
       'bmp': {'GroupType': 'Texture',
               'Type': 'Texture',
               'IconType': 'Texture'
               },
       'cube': {'GroupType': 'Texture',
                'Type': 'Texture',
                'IconType': 'Texture'
                },
       'ktx': {'GroupType': 'Texture',
               'Type': 'Texture',
               'IconType': 'Texture'
               },
       'hdr': {'GroupType': 'Texture',
               'Type': 'Texture',
               'IconType': 'Texture'
               },
       'audio': {'GroupType': 'Audio',
                 'Type': 'Audio',
                 'IconType': 'AudioSource'
                 },
       'fev': {'GroupType': 'Audio',
               'Type': 'Audio',
               'IconType': 'AudioSource'
               },
       'bnk': {'GroupType': 'Audio',
               'Type': 'Audio',
               'IconType': 'AudioSource'
               },
       'wav': {'GroupType': 'Audio',
               'Type': 'Audio',
               'IconType': 'AudioSource'
               },
       'wma': {'GroupType': 'Audio',
               'Type': 'Audio',
               'IconType': 'AudioSource'
               },
       'sfxmusic': {'GroupType': 'Audio',
                    'Type': 'Audio',
                    'IconType': 'AudioSource'
                    },
       'psemusic': {'GroupType': 'Audio',
                    'Type': 'Audio',
                    'IconType': 'AudioSource'
                    },
       'bpsemusic': {'GroupType': 'Audio',
                     'Type': 'Audio',
                     'IconType': 'AudioSource'
                     },
       'ogg': {'GroupType': 'Audio',
               'Type': 'Audio',
               'IconType': 'AudioSource'
               },
       'mp3': {'GroupType': 'Audio',
               'Type': 'Audio',
               'IconType': 'AudioSource'
               },
       'mp4': {'GroupType': 'Video',
               'Type': 'Video',
               'IconType': 'Video'
               },
       'mov': {'GroupType': 'Video',
               'Type': 'Video',
               'IconType': 'Video'
               },
       'flv': {'GroupType': 'Video',
               'Type': 'Video',
               'IconType': 'Video'
               },
       'sfx': {'GroupType': 'Particle',
               'Type': 'ParticleOld',
               'IconType': 'ParticleRenderer'
               },
       'pse': {'GroupType': 'Particle',
               'Type': 'ParticleNew',
               'IconType': 'ParticleRenderer'
               },
       'bpse': {'GroupType': 'Particle',
                'Type': 'ParticleNew',
                'IconType': 'ParticleRenderer'
                },
       'light': {'GroupType': 'Light',
                 'Type': 'Light',
                 'IconType': 'Light'
                 },
       'tlight': {'GroupType': 'Light',
                  'Type': 'Light',
                  'IconType': 'Light'
                  },
       'template': {'GroupType': 'Light',
                    'Type': 'Light',
                    'IconType': 'LightTemplate'
                    },
       'csb': {'GroupType': 'UI',
               'Type': 'UI',
               'IconType': 'UIResource'
               },
       'uiPrefab': {'GroupType': 'UI',
                    'Type': 'UI',
                    'IconType': 'UIResource'
                    },
       'trk': {'GroupType': 'Track',
               'Type': 'Track',
               'IconType': 'UIResource'
               },
       'nfx': {'GroupType': 'Shader',
               'Type': 'ShaderNFX',
               'IconType': 'Nfx'
               },
       'surf': {'GroupType': 'Shader',
                'Type': 'ShaderSurface',
                'IconType': 'Nfx'
                },
       'spx': {'GroupType': 'Shader',
               'Type': 'ShaderNFX',
               'IconType': 'Nfx'
               },
       'seq': {'GroupType': 'Sequence',
               'Type': 'Sequence',
               'IconType': 'SequenceFile'
               },
       'pvr': {'GroupType': 'Unknown',
               'Type': 'Unknown',
               'IconType': 'Default'
               },
       'curve': {'GroupType': 'Curves',
                 'Type': 'Curves',
                 'IconType': 'CurveFile'
                 },
       'mpc': {'GroupType': 'Unknown',
               'Type': 'Unknown',
               'IconType': 'Default'
               },
       'gax': {'GroupType': 'Gaea',
               'Type': 'GaeaConfig',
               'IconType': 'MetaFile'
               },
       'gaj': {'GroupType': 'Gaea',
               'Type': 'GaeaConfig',
               'IconType': 'MetaFile'
               },
       'bson': {'GroupType': 'Gaea',
                'Type': 'GaeaConfig',
                'IconType': 'MetaFile'
                },
       'pti': {'GroupType': 'Gaea',
               'Type': 'GaeaConfig',
               'IconType': 'MetaFile'
               },
       'gvt': {'GroupType': 'Gaea',
               'Type': 'GaeaStreaming',
               'IconType': 'Texture'
               },
       'cpf': {'GroupType': 'Gaea',
               'Type': 'GaeaFoliageType',
               'IconType': 'Foliage'
               },
       'grass': {'GroupType': 'Gaea',
                 'Type': 'GaeaGrassType',
                 'IconType': 'Foliage'
                 },
       'Spline': {'GroupType': 'Spline',
                  'Type': 'Spline',
                  'IconType': 'MetaFile'
                  },
       'lod': {'GroupType': 'Unknown',
               'Type': 'Unknown',
               'IconType': 'Default'
               },
       'col': {'GroupType': 'Physics',
               'Type': 'PhysicsCOL',
               'IconType': 'CollisonFile'
               },
       'blt': {'GroupType': 'Unknown',
               'Type': 'Unknown',
               'IconType': 'Default'
               },
       'decal': {'GroupType': 'Decal',
                 'Type': 'Decal',
                 'IconType': 'DecalFile'
                 },
       'PostProcess': {'GroupType': 'PostProcess',
                       'Type': 'PostProcess',
                       'IconType': 'Default'
                       },
       'timeline': {'GroupType': 'Timeline',
                    'Type': 'Timeline',
                    'IconType': 'TimelineFile'
                    },
       'fld': {'GroupType': 'Unknown',
               'Type': 'Unknown',
               'IconType': 'Default'
               },
       'ramp': {'GroupType': 'Unknown',
                'Type': 'Unknown',
                'IconType': 'Default'
                },
       'json': {'GroupType': 'Unknown',
                'Type': 'Unknown',
                'IconType': 'Default'
                },
       'vapose': {'GroupType': 'Unknown',
                  'Type': 'Unknown',
                  'IconType': 'Default'
                  },
       'cvg': {'GroupType': 'CurveGroup',
               'Type': 'CurveGroup',
               'IconType': 'CurveFile'
               },
       'py': {'GroupType': 'Unknown',
              'Type': 'Unknown',
              'IconType': 'Default'
              },
       'uscn': {'GroupType': 'Unknown',
                'Type': 'Unknown',
                'IconType': 'Default'
                }
       }

    def __init__(self):
        self.resRoot = os.path.join(game3d.get_root_dir(), game3d.get_res_root())
        self.thumbMgr = self.createThumbnailManager()

    def createThumbnailManager(self):
        return NeoXThumbnailManager(self)

    def isSupportedFile(self, filePath):
        _, ext = os.path.splitext(filePath)
        if not ext:
            return False
        return ext[1:].lower() in self.FILE_TYPES

    def getFileType(self, filePath):
        ext = self.getFileExt(filePath)
        return self.FILE_TYPES.get(ext, self.FILE_TYPES['default'])['Type']

    def getFileGroupType(self, filePath):
        ext = self.getFileExt(filePath)
        return self.FILE_TYPES.get(ext, self.FILE_TYPES['default'])['GroupType']

    def getFileExt(self, filePath):
        _, ext = os.path.splitext(filePath)
        if not ext:
            return
        return ext[1:].lower()

    def getThumbnail(self, resPath, width, height, callback):
        self.thumbMgr.getThumbnail(resPath, width, height, callback)

    def cancelGettingThumbnail(self):
        self.thumbMgr.cancelGettingThumbnail()

    def invalidateThumbnails(self, resPaths):
        self.thumbMgr.invalidateThumbnails(resPaths)

    def getResourceData(self):
        result = {}
        for root, dirNames, fileNames in os.walk(self.resRoot):
            for fileName in fileNames:
                fileType = self.getFileType(fileName)
                if not fileType:
                    continue
                resPath = os.path.relpath(os.path.join(root, fileName), self.resRoot).replace('\\', '/')
                result.setdefault(fileType, []).append(resPath)

        return result

    def getFilePath(self, resPath):
        return os.path.join(self.resRoot, resPath).replace('\\', '/')

    def getResPath(self, filePath):
        return os.path.relpath(filePath, self.resRoot).replace('\\', '/')

    def ensureDirExists(self, path):
        if os.path.exists(path):
            return
        self.ensureDirExists(os.path.dirname(path))
        os.mkdir(path)