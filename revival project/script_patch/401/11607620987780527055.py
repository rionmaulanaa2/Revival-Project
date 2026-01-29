# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/share/TrainingCertificateShareCreator.py
from __future__ import absolute_import
from logic.gutils.end_statics_utils import init_end_person_statistics, init_end_teammate_statics
from logic.comsys.share.ShareTemplateBase import ShareTemplateBase, async_disable_wrapper
from logic.gcommon.item import item_const
from common.cfg import confmgr

class TrainingCertificateShareCreator(ShareTemplateBase):
    KIND = 'I_SHARE_TRAINING_CERTIFICATE'

    def destroy(self):
        super(TrainingCertificateShareCreator, self).destroy()

    def set_info(self, task_id, player_name, task_img):
        task_data = confmgr.get('task/task_data', task_id)
        task_name = task_data['name']
        content = task_data.get('arg', {}).get('pass_text_id')
        self.panel.lab_player.SetString(player_name)
        self.panel.lab_detail.SetString(content)
        from logic.gutils.new_template_utils import update_newbee_pass_certificate, set_certificate_reward_data
        update_newbee_pass_certificate(self.panel.card_pass, task_id, task_img)