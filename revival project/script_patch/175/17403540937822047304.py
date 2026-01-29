# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/share/ShareTierUPCreator.py
from __future__ import absolute_import
from logic.comsys.share.ShareTemplateBase import ShareTemplateBase, async_disable_wrapper
from common.cfg import confmgr
import logic.gcommon.time_utility as tutil

class ShareTierUpCreator(ShareTemplateBase):
    KIND = 'I_SHARE_TIER_UP'

    @async_disable_wrapper
    def create(self, parent=None, tmpl=None):
        super(ShareTierUpCreator, self).create(parent)

    def update_show(self):
        from logic.gutils import template_utils
        import logic.gcommon.cdata.dan_data as dan_data
        _cur_star = global_data.player.get_dan_star(dan_data.DAN_SURVIVAL)
        _cur_dan = global_data.player.get_dan(dan_data.DAN_SURVIVAL)
        _cur_lv = global_data.player.get_dan_lv(dan_data.DAN_SURVIVAL)
        template_utils.init_tier_common(self.panel.temp_tier, _cur_dan, _cur_star)
        from logic.gutils import season_utils
        from logic.gutils import dress_utils
        self.panel.lab_tier_name.SetString(season_utils.get_dan_lv_name(_cur_dan, _cur_lv))
        role_id = global_data.player.get_role()
        role_skin_id = dress_utils.get_role_dress_clothing_id(role_id, check_default=True)
        pic_path = 'gui/ui_res_2/pic/{}.png'.format(role_skin_id)
        self.panel.img_role.SetDisplayFrameByPath('', pic_path)