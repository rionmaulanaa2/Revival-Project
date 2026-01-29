# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/component/client/ComTowerGrenadeAppearance.py
from __future__ import absolute_import
from .ComGrenadeAppearance import ComGrenadeAppearance
from common.cfg import confmgr

class ComTowerGrenadeAppearance(ComGrenadeAppearance):

    def __init__(self):
        super(ComTowerGrenadeAppearance, self).__init__()

    def get_model_info(self, unit_obj, bdict):
        mpath, merge_info, udata = super(ComTowerGrenadeAppearance, self).get_model_info(unit_obj, bdict)
        if 'fashion_id' in bdict:
            fashion_id = bdict['fashion_id']
            if fashion_id is not None:
                from logic.gutils.dress_utils import get_mecha_model_path
                mpath = get_mecha_model_path(8008, fashion_id)
                mpath = mpath.replace('empty.gim', 'tower/l.gim')
        return (mpath, merge_info, udata)