# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/vscene/parts/camera/CamShake.py
from __future__ import absolute_import
from __future__ import print_function
import six
from common.framework import Singleton
from logic.vscene.parts import PartEffectManager
from logic.comsys.effect.screen_effect import ScreenShakeMeta
DEFAULT_SHAKE_DATA = {'stand.run': {'type': 'action',
                 'shake_sfx': 'effect/fx/renwu/zhendong/jipao_zhengping.sfx',
                 'loop': True
                 },
   'climb.on_ground': {'type': 'action',
                       'shake_sfx': 'effect/fx/renwu/zhendong/luodi_zhengping.sfx',
                       'loop': False
                       },
   'state_on_ground': {'type': 'state',
                       'shake_sfx': 'effect/fx/renwu/zhendong/luodi_zhengping.sfx',
                       'loop': False
                       }
   }
test = {'roll': {'type': 'action',
            'shake_sfx': 'effect/fx/renwu/zhendong/fangunluodi_zhengping.sfx',
            'loop': False
            }
   }

class CamShakeController(Singleton):

    def init(self):
        super(CamShakeController, self).__init__()
        self.init_cam_shake_data()
        self.init_event()

    def init_cam_shake_data(self):
        self.shake_data = DEFAULT_SHAKE_DATA
        for key, sfx_info in six.iteritems(self.shake_data):
            PartEffectManager.ValidEffectNames[key] = type('CameraShake_%s' % key, (ScreenShakeMeta,), dict(EFFECT_FILE_PATH=sfx_info['shake_sfx']))

    def init_event(self):
        emgr = global_data.emgr
        emgr.camera_shake_event_start += self.on_cam_trigger_active

    def clear_all_events(self):
        pass

    def register_cam_shake_event(self, player):
        animator = player.ev_g_animator()
        if not animator:
            return
        for key, sfx_info in six.iteritems(self.shake_data):
            regist_node = animator.find(key)
            if not regist_node:
                continue
            if not sfx_info['type'] == 'action':
                continue
            active_sig = regist_node.activeSig
            print('active sig', active_sig)
            if not active_sig:
                regist_node.activeSig = '%s%s' % (key, '_activate')
            player.send_event('E_REGISTER_ANIM_ACTIVE', regist_node.activeSig, self.on_cam_trigger_active)
            loop = sfx_info['loop']
            if loop:
                deactive_sig = regist_node.deactiveSig
                print('deactive_sig', deactive_sig)
                if not deactive_sig:
                    regist_node.deactiveSig = '%s%s' % (key, '_deactivate')
                player.send_event('E_REGISTER_ANIM_DEACTIVE', regist_node.deactiveSig, self.on_cam_trigger_deactive)

    def unregister_cam_shake_event(self, player):
        pass

    def on_cam_trigger_active(self, sig, node_name, node_idx=-1):
        global_data.emgr.show_screen_effect.emit(node_name, {'loop': self.shake_data[node_name]['loop']})

    def on_cam_trigger_deactive(self, sig, node_name, node_idx=-1):
        global_data.emgr.hide_screen_effect.emit(node_name)

    def get_shake_info_by_node_idx(self):
        pass