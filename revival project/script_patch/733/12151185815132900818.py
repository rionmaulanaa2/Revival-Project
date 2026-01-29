# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/share/IntimacyHistoricalEventShareCreator.py
from logic.comsys.share.ShareTemplateBase import ShareTemplateBase, async_disable_wrapper
from logic.gcommon.const import IDX_INTIMACY_TYPE, IDX_INTIMACY_NAME, INTIMACY_NAME_MAP
from logic.gcommon import time_utility as tutil
from logic.gutils.role_head_utils import PlayerInfoManager, init_role_head
from common.const.property_const import C_NAME
from logic.gutils.intimacy_utils import init_intimacy_event_frame, init_intimacy_pic
from common.cfg import confmgr
import copy

class IntimacyHistoricalEventShareCreator(ShareTemplateBase):
    KIND = 'INTIMACY_HISTORICAL_EVENT_SHARE'

    @async_disable_wrapper
    def create(self, parent=None, tmpl=None, intimacy_event_data=[], intimacy_info={}, friend_info={}, date_time=0):
        super(IntimacyHistoricalEventShareCreator, self).create(parent, tmpl)
        self.intimacy_event_data = intimacy_event_data[:]
        self.intimacy_info = copy.deepcopy(intimacy_info)
        self.friend_info = copy.deepcopy(friend_info)
        self.date_time = date_time
        intimacy_type = self.intimacy_info[IDX_INTIMACY_TYPE]
        nd = self.panel.nd_content
        nd.setVisible(True)
        frame_color = nd.frame_color
        frame_color.lab_date.SetString(self.date_time)
        mine_head = nd.temp_head_mine
        init_role_head(mine_head, global_data.player.get_head_frame(), global_data.player.get_head_photo())
        mine_head.lab_name.SetString(global_data.player.get_name())
        player_info_manager = PlayerInfoManager()
        others_head = nd.temp_head_others
        friend_uid = int(self.friend_info.get('uid'))
        update_head_info = global_data.message_data.get_role_head_info(friend_uid)
        frame = update_head_info.get('head_frame', None)
        photo = update_head_info.get('head_photo', None)
        if frame and photo:
            self.friend_info['head_frame'] = frame
            self.friend_info['head_photo'] = photo
        player_info_manager.add_head_item_auto(others_head, friend_uid, 0, self.friend_info)
        friend_name = str(self.friend_info[C_NAME])
        others_head.lab_name.SetString(friend_name)
        init_intimacy_event_frame(frame_color, intimacy_type)
        init_intimacy_pic(frame_color.icon_relationship, intimacy_type)
        conf = confmgr.get('intimacy_memory_data', self.intimacy_event_data[0])
        text_id = conf.get('text_id')
        value_num = str(self.intimacy_event_data[1])
        intimacy_name = self.intimacy_info[IDX_INTIMACY_NAME]
        if intimacy_name is None:
            intimacy_name = get_text_by_id(INTIMACY_NAME_MAP[intimacy_type])
        value_str = get_text_by_id(text_id).format(value_num, time=value_num, rela=intimacy_name, lv=value_num)
        frame_color.lab_share.SetString(get_text_by_id(634624) + value_str + get_text_by_id(634625))
        return

    def recreate_panel(self):
        self.destroy_panel()
        self.create(intimacy_event_data=self.intimacy_event_data, intimacy_info=self.intimacy_info, friend_info=self.friend_info, date_time=self.date_time)

    def update_ui_bg_sprite(self):
        pass