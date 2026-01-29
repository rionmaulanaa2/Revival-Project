# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/Activity202201/SpringShoutFriendsRedPackagesUI.py
from __future__ import absolute_import
from __future__ import print_function
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_1
import cc
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no, get_lobby_item_desc
from common.const import uiconst
from logic.comsys.common_ui.WindowMediumBase import WindowMediumBase
from logic.comsys.common_ui.InputBox import InputBox
from logic.client.const.share_const import TYPE_IMAGE
from logic.gutils.share_utils import ShareHelper
from common.uisys.basepanel import BasePanel
from logic.gcommon.time_utility import get_server_time, get_readable_time_day_hour_minitue
from logic.comsys.share.CommonShareBubbleUI import CommonShareBubbleUI
from logic.client.const import share_const
from common.cfg import confmgr

class RedPackageShareBubbleUI(CommonShareBubbleUI):
    pass


class SpringShoutFriendsRedPackagesUI(BasePanel):
    PANEL_CONFIG_NAME = 'activity/activity_202201/spring_shout_friends/open_acticity_red_packet'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_1
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE
    UI_ACTION_EVENT = {'btn_close.OnClick': 'on_click_close_btn'
       }
    COUNT_DOWN_TAG = 220111
    SHARE_URL_MAP = {}
    MAX_HONGBAO_REWARD_COUNT = 4

    def on_init_panel(self):
        super(SpringShoutFriendsRedPackagesUI, self).on_init_panel()
        action = cc.RepeatForever.create(cc.Sequence.create([
         cc.DelayTime.create(30),
         cc.CallFunc.create(self.update_count_down)]))
        action.setTag(self.COUNT_DOWN_TAG)
        self.panel.runAction(action)
        self.refresh_all_red_packages()

    def refresh_all_red_packages(self):
        share_list = [{'data_id': 'spring2023_1'}, {'data_id': 'spring2023_2'}, {'data_id': 'spring2023_3'}]
        temp_list = [
         self.panel.temp_1, self.panel.temp_2, self.panel.temp_3]
        for idx, share_data_dict in enumerate(share_list):
            temp = temp_list[idx]
            self.init_red_package(temp, idx, share_data_dict)

    def on_finalize_panel(self):
        pass

    def on_click_close_btn(self, btn, touch):
        self.close()

    def init_red_package(self, temp, idx, data_dict):
        from logic.gcommon.common_const import activity_const as acconst
        cUiData = confmgr.get('c_activity_config', str(acconst.ACTIVITY_SPRING_CALL_FRIENDS), 'cUiData')
        time_list = cUiData.get('time_list', [])
        open_time = time_list[idx] if len(time_list) > idx else 0
        data_id = data_dict['data_id']
        hongbao_draw_cnt = global_data.player.get_newyear_hongbao_draw_cnt(data_id)
        is_share_reward_all_claimed = self.MAX_HONGBAO_REWARD_COUNT <= hongbao_draw_cnt
        cur_time = get_server_time()
        temp.lab_tips.setVisible(True)
        if open_time > cur_time:
            temp.lab_tips.SetString(get_readable_time_day_hour_minitue(open_time - cur_time))
            temp.btn_share.SetText(604026)
            temp.btn_share.SetEnable(False)
        elif not is_share_reward_all_claimed:
            temp.lab_tips.SetString('')
            temp.btn_share.SetText(610523)
            temp.btn_share.SetEnable(True)
        else:
            temp.lab_tips.SetString(610529 if is_share_reward_all_claimed else '')
            temp.btn_share.SetText(610523)
            temp.btn_share.SetEnable(True)

        @temp.btn_share.callback()
        def OnClick(btn, touch):
            from logic.comsys.share.CommonShareBubbleUI import CommonShareBubbleUI
            share_message = get_text_by_id(610517)
            share_title = get_text_by_id(610298)

            def share_cb(*argv):
                global_data.player.on_enlist_share()

            def ready_share--- This code section failed: ---

  98       0  LOAD_FAST             0  'url'
           3  POP_JUMP_IF_FALSE   183  'to 183'

  99       6  LOAD_DEREF            0  'CommonShareBubbleUI'
           9  LOAD_CONST            1  'share_link'
          12  LOAD_CONST            2  'share_title'
          15  LOAD_DEREF            1  'share_title'
          18  LOAD_CONST            3  'share_message'
          21  LOAD_DEREF            2  'share_message'
          24  LOAD_CONST            4  'desc'

 100      27  LOAD_DEREF            2  'share_message'
          30  LOAD_CONST            5  'share_cb'
          33  LOAD_DEREF            3  'share_cb'
          36  CALL_FUNCTION_1280  1280 
          39  STORE_FAST            1  'ui'

 101      42  LOAD_FAST             1  'ui'
          45  LOAD_ATTR             0  'panel'
          48  LOAD_ATTR             1  'setRotation'
          51  LOAD_DEREF            4  'temp'
          54  LOAD_ATTR             2  'getRotation'
          57  CALL_FUNCTION_0       0 
          60  CALL_FUNCTION_1       1 
          63  POP_TOP          

 102      64  LOAD_FAST             1  'ui'
          67  LOAD_ATTR             0  'panel'
          70  LOAD_ATTR             3  'lab_tips'
          73  LOAD_ATTR             4  'SetString'
          76  LOAD_CONST            6  610298
          79  CALL_FUNCTION_1       1 
          82  POP_TOP          

 103      83  LOAD_DEREF            4  'temp'
          86  LOAD_ATTR             5  'btn_share'
          89  STORE_FAST            2  'nd'

 104      92  LOAD_FAST             2  'nd'
          95  LOAD_ATTR             6  'getPosition'
          98  CALL_FUNCTION_0       0 
         101  STORE_FAST            3  'lpos'

 105     104  LOAD_FAST             2  'nd'
         107  LOAD_ATTR             7  'getParent'
         110  CALL_FUNCTION_0       0 
         113  LOAD_ATTR             8  'convertToWorldSpace'
         116  LOAD_FAST             3  'lpos'
         119  CALL_FUNCTION_1       1 
         122  STORE_FAST            4  'world_pos'

 106     125  LOAD_FAST             4  'world_pos'
         128  DUP_TOP          
         129  LOAD_ATTR             9  'y'
         132  LOAD_CONST            7  20
         135  INPLACE_ADD      
         136  ROT_TWO          
         137  STORE_ATTR            9  'y'

 107     140  LOAD_FAST             1  'ui'
         143  LOAD_ATTR             7  'getParent'
         146  CALL_FUNCTION_0       0 
         149  LOAD_ATTR            10  'convertToNodeSpace'
         152  LOAD_FAST             4  'world_pos'
         155  CALL_FUNCTION_1       1 
         158  STORE_FAST            3  'lpos'

 108     161  LOAD_FAST             1  'ui'
         164  JUMP_IF_FALSE_OR_POP   179  'to 179'
         167  LOAD_FAST             1  'ui'
         170  LOAD_ATTR            11  'setPosition'
         173  LOAD_FAST             3  'lpos'
         176  CALL_FUNCTION_1       1 
       179_0  COME_FROM                '164'
         179  POP_TOP          
         180  JUMP_FORWARD         22  'to 205'

 110     183  LOAD_GLOBAL          12  'global_data'
         186  LOAD_ATTR            13  'game_mgr'
         189  LOAD_ATTR            14  'show_tip'
         192  LOAD_GLOBAL          15  'get_text_by_id'
         195  LOAD_CONST            8  193
         198  CALL_FUNCTION_1       1 
         201  CALL_FUNCTION_1       1 
         204  POP_TOP          
       205_0  COME_FROM                '180'

Parse error at or near `CALL_FUNCTION_1280' instruction at offset 36

            self.get_spring_shout_friends_share_url('', data_id, ready_share)

    def get_spring_shout_friends_share_url(self, kw, data_id, ret_callback):
        import json
        import six
        import six.moves.urllib.request
        import six.moves.urllib.parse
        import six.moves.urllib.error
        import hashlib
        import version
        from common import http
        from common.utils import package_type
        role_id = str(global_data.player.uid)
        ret_url = self.SHARE_URL_MAP.get(data_id, None)
        if ret_url and ret_callback:
            ret_callback(ret_url)
            return
        else:
            key = 'W0kss6ptiXPvSZ4lWLVX99smpjU4agfe'
            channel = global_data.channel.get_app_channel()
            etc_info = json.dumps({})
            headimg = str(global_data.player.get_head_photo())
            hostnum = str(global_data.channel.get_host_num())
            lang = global_data.player.get_login_country().lower()
            nick = global_data.player.get_name()
            sign_key = channel + data_id + etc_info + headimg + hostnum + kw + lang + nick + role_id + key
            sign = hashlib.sha1(six.ensure_binary(sign_key)).hexdigest()
            params = {'channel': channel,
               'data_id': data_id,
               'etc_info': etc_info,
               'headimg': global_data.player.get_head_photo(),
               'hostnum': hostnum,
               'kw': kw,
               'lang': lang,
               'nick': nick,
               'role_id': role_id,
               'sign': sign
               }
            if G_IS_NA_PROJECT:
                if global_data.is_inner_server:
                    interface_url = 'https://test-interact2.webapp.easebar.com/g93newyear23'
                else:
                    interface_url = 'https://interact2.webapp.easebar.com/g93newyear23'
            elif global_data.is_inner_server:
                interface_url = 'https://test-interact2.webapp.163.com/g93newyear23'
            else:
                interface_url = 'https://interact2.webapp.163.com/g93newyear23'
            param_text = six.moves.urllib.parse.urlencode(params).encode(encoding='UTF8')
            url = '%s/get_share_url?%s' % (interface_url, param_text)
            print('>>> spring_get_share_url', url)

            def cb(ret, url, args):
                print('>>> kizunai_callback', ret, args)
                ret_url = ''
                try:
                    result = json.loads(ret)
                    ret_url = result['share_url']
                    ret_callback and ret_callback(ret_url)
                    print('>>> hongbao_share_url-----1', ret_url)
                except:
                    ret_callback and ret_callback(ret_url)
                    print('>>> hongbao_share_url-----2', ret_url)

                if ret_url:
                    self.SHARE_URL_MAP[role_id] = ret_url

            http.request(url, callback=cb)
            return

    def update_count_down(self):
        if global_data.player:
            self.refresh_all_red_packages()
        else:
            self.close()