# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComPreviewAppearance.py
from __future__ import absolute_import
import six
import six_ex
from .ComAnimatorAppearance import ComAnimatorAppearance
import world
import math3d

class ComPreviewAppearance(ComAnimatorAppearance):

    def __init__(self):
        super(ComPreviewAppearance, self).__init__()

    def init_from_dict(self, unit_obj, bdict):
        super(ComPreviewAppearance, self).init_from_dict(unit_obj, bdict)
        self.model_id = bdict.get('model_id')
        global_data.emgr.change_action_preview += self.on_change_action_preview

    def get_model_info(self, unit_obj, bdict):
        path = bdict.get('model')
        self.DEFAULT_XML = bdict.get('animator')
        return (
         path, None, None)

    def on_load_animator_complete(self, *args):
        super(ComPreviewAppearance, self).on_load_animator_complete(*args)
        self.send_event('E_HUMAN_MODEL_LOADED', self.get_model())
        self.on_change_action_preview()

    def on_change_action_preview(self, action_id=None):
        from common.cfg import confmgr
        conf = confmgr.get('action_preview')
        conf = conf.get(self.model_id, {}).get('Content', {})
        if not action_id:
            action_id = sorted(six_ex.keys(conf))[0]
        info = conf[action_id]
        low_body = info.get('low_body')
        if low_body:
            if low_body[0] == '1':
                action_name = low_body[1]
                src_node = self._animator.find('low_body.single')
                src_node.clipName = action_name
                self._animator.SetInt('low_body_select_type', 2)
            elif low_body[0] == '4':
                action_name = low_body[1]
                dic = {'low_body.four_dir.src_l': action_name + '_l',
                   'low_body.four_dir.src_r': action_name + '_r',
                   'low_body.four_dir.src_f': action_name + '_f',
                   'low_body.four_dir.src_b': action_name + '_b'
                   }
                for key, value in six.iteritems(dic):
                    src_node = self._animator.find(key)
                    src_node.clipName = value

                self._animator.SetInt('low_body_select_type', 1)
            elif low_body[0] == '6':
                action_name = low_body[1]
                dic = {'low_body.six_dir.src_fl': action_name + '_fl',
                   'low_body.six_dir.src_fr': action_name + '_fr',
                   'low_body.six_dir.src_f': action_name + '_f',
                   'low_body.six_dir.src_bl': action_name + '_bl',
                   'low_body.six_dir.src_br': action_name + '_br',
                   'low_body.six_dir.src_b': action_name + '_b'
                   }
                for key, value in six.iteritems(dic):
                    src_node = self._animator.find(key)
                    src_node.clipName = value

                self._animator.SetInt('low_body_select_type', 0)
        up_body = info.get('up_body')
        if up_body:
            if up_body[0] == '1':
                action_name = up_body[1]
                src_node = self._animator.find('up_body.single')
                src_node.clipName = action_name
                self._animator.SetInt('up_body_select_type', 2)
            elif up_body[0] == '4':
                action_name = up_body[1]
                dic = {'up_body.four_dir.src_l': action_name + '_l',
                   'up_body.four_dir.src_r': action_name + '_r',
                   'up_body.four_dir.src_f': action_name + '_f',
                   'up_body.four_dir.src_b': action_name + '_b'
                   }
                for key, value in six.iteritems(dic):
                    src_node = self._animator.find(key)
                    src_node.clipName = value

                self._animator.SetInt('up_body_select_type', 1)
            elif up_body[0] == '6':
                action_name = up_body[1]
                dic = {'up_body.six_dir.src_fl': action_name + '_fl',
                   'up_body.six_dir.src_fr': action_name + '_fr',
                   'up_body.six_dir.src_f': action_name + '_f',
                   'up_body.six_dir.src_bl': action_name + '_bl',
                   'up_body.six_dir.src_br': action_name + '_br',
                   'up_body.six_dir.src_b': action_name + '_b'
                   }
                for key, value in six.iteritems(dic):
                    src_node = self._animator.find(key)
                    src_node.clipName = value

                self._animator.SetInt('up_body_select_type', 0)
        if low_body and info.get('root_bone_translate'):
            if low_body[0] == '1':
                self.send_event('E_MOVE_BY_CLIP', action_name)
            else:
                self.send_event('E_MOVE_BY_CLIP', action_name + '_f')