# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/share/EndStaticsShareCreator.py
from __future__ import absolute_import
from logic.gutils.end_statics_utils import init_end_person_statistics, init_end_teammate_statics
from logic.comsys.share.ShareTemplateBase import ShareTemplateBase, async_disable_wrapper

class EndStaticsShareCreator(ShareTemplateBase):
    KIND = 'END_STATICS_SHARE'

    def init_end_person_nd(self, teammate_num, group_num, settle_dict):
        init_end_person_statistics(self.panel, teammate_num, group_num, settle_dict)

    def init_end_text(self, rank):
        from common.cfg import confmgr
        conf = confmgr.get_raw('c_share_rank_text')
        if str(rank) in conf:
            text_list = conf[str(rank)].get('cTextList', [''])
        else:
            text_list = conf.get('other', {}).get('cTextList', [''])
        import random
        text = random.choice(text_list) if self.check_need_show_text() else ''

    def init_teammate_nd(self, teaminfo):
        groupmate_info = global_data.player.logic.ev_g_teammate_infos()
        init_end_teammate_statics(self.panel.nd_teammate_statistics, groupmate_info, teaminfo)