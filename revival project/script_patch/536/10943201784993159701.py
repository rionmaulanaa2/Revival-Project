# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/message/SendLineMessage.py
from __future__ import absolute_import
from __future__ import print_function
import time
from cocosui import cc, ccui, ccs
from common.platform import channel_const
from common.const.uiconst import NORMAL_LAYER_ZORDER
from logic.gcommon.common_const import friend_const
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.comsys.common_ui.WindowSmallBase import WindowSmallBase
from logic.comsys.message import LineGameFriendList

class SendLineMessageCoin(WindowSmallBase):
    PANEL_CONFIG_NAME = 'friend/confirm_line_coin'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    TEMPLATE_NODE_NAME = 'temp_bg'
    UI_ACTION_EVENT = {'btn_done.btn_common.OnClick': 'on_send',
       'btn_cancel.btn_common.OnClick': 'close'
       }

    def on_init_panel(self, *args, **kargs):
        super(SendLineMessageCoin, self).on_init_panel()
        self._social_id = kargs.get('social_id', '')
        self._title = get_text_by_id(609025)
        self._text = kargs.get('text', '')
        self._sub_text = kargs.get('sub_text', '')
        self._link_text = get_text_by_id(609027)
        self.panel.lab_name_title.SetString(self._text)
        self.panel.link_text.SetString(self._sub_text)

    def on_send(self, *args):
        from logic.client.const import share_const
        self.close()

        def share_cb(ret):
            code = global_data.channel.get_prop_str('LINE_ERROR_CODE')
            fail_msg = global_data.channel.get_prop_str('LINE_ERROR_MESSAGE')
            print('>>>>>> share_cb', ret, code, fail_msg)
            if ret:
                global_data.game_mgr.show_tip(609010)

        key_word = '%s=%s' % (share_const.DEEP_LINK_GIVE_COINS, '{}_{}'.format(str(global_data.player.uid), 'linegame'))
        global_data.share_mgr.share_linegame('give_coins', [self._social_id], self._title, self._sub_text, self._link_text, share_cb, a_link_param=key_word)

    def on_login_reconnect(self, *args):
        self.close()

    def on_finalize_panel(self):
        pass


class SendLineMessageInvite(WindowSmallBase):
    PANEL_CONFIG_NAME = 'friend/confirm_line'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    TEMPLATE_NODE_NAME = 'temp_bg'
    UI_ACTION_EVENT = {'btn_done.btn_common.OnClick': 'on_send',
       'btn_cancel.btn_common.OnClick': 'close'
       }

    def on_init_panel(self, *args, **kargs):
        super(SendLineMessageInvite, self).on_init_panel()
        self._social_id = kargs.get('social_id', '')
        self._title = get_text_by_id(609028)
        self._text = get_text_by_id(609029)
        self._link_text = get_text_by_id(609027)
        self.panel.link_text.SetString(self._text)
        linegame_friendinfos = global_data.message_data.get_linegame_friends()
        linegame_data = linegame_friendinfos.get(self._social_id, {})
        self.panel.lab_name.SetString(linegame_data.get('nickname', ''))
        icon_url = linegame_data.get('avatar', '')
        if icon_url:
            LineGameFriendList.set_linegame_icon(icon_url, self.add_linegame_icon)

    def add_linegame_icon(self, file_path):
        elem_panel = self.panel.temp_head
        sprite = cc.Sprite.create(file_path)
        if not sprite:
            return
        sprite.setAnchorPoint(cc.Vec2(0.5, 0.5))
        size = elem_panel.img_head.getContentSize()
        sprite.setPosition(cc.Vec2(size.width * 0.5, size.height * 0.5))
        scale = size.width / sprite.getTextureRect().width
        sprite.setScale(scale)
        elem_panel.img_head.addChild(sprite)

    def on_send(self, *args):
        from logic.gutils import friend_utils
        from logic.client.const import share_const
        self.close()

        def share_cb(ret):
            from logic.comsys.common_ui.NormalConfirmUI import NormalConfirmUI2
            code = global_data.channel.get_prop_str('LINE_ERROR_CODE')
            fail_msg = global_data.channel.get_prop_str('LINE_ERROR_MESSAGE')
            print('>>>>>> share_cb', ret, code, fail_msg)
            if ret:
                NormalConfirmUI2(content=get_text_by_id(609010))

        key_word = '%s=%s' % (share_const.DEEP_LINK_JOIN_TEAM, '{}_{}'.format(str(global_data.player.uid), 'linegame'))
        global_data.share_mgr.share_linegame('invite_jp', [self._social_id], self._title, self._text, self._link_text, share_cb, a_link_param=key_word)
        friend_utils.salog_friend_ui_oper(friend_utils.FRIEND_LOG_KEY_TEAM_SHARE_VIA_LINEGAME)

    def on_login_reconnect(self, *args):
        self.close()

    def on_finalize_panel(self):
        pass


class SendLineMessageAddFriend(WindowSmallBase):
    PANEL_CONFIG_NAME = 'friend/confirm_line'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    TEMPLATE_NODE_NAME = 'temp_bg'
    UI_ACTION_EVENT = {'btn_done.btn_common.OnClick': 'on_send',
       'btn_cancel.btn_common.OnClick': 'close'
       }

    def on_init_panel(self, *args, **kargs):
        super(SendLineMessageInvite, self).on_init_panel()
        self._social_id = kargs.get('social_id', '')
        self._title = 'SMC\xe9\x9b\x86\xe7\xbb\x93'
        self._text = '\xe6\x9d\xa5\xe7\x9b\xb8\xe7\xba\xa6SMC\xef\xbc\x81'
        self._link_text = '\xe5\x8a\xa0\xe5\x85\xa5'
        self.panel.link_text.SetString(self._text)
        linegame_friendinfos = global_data.message_data.get_linegame_friends()
        linegame_data = linegame_friendinfos.get(self._social_id, {})
        self.panel.lab_name.SetString(linegame_data.get('nickname', ''))
        icon_url = linegame_data.get('avatar', '')
        if icon_url:
            LineGameFriendList.set_linegame_icon(icon_url, self.add_linegame_icon)

    def add_linegame_icon(self, file_path):
        elem_panel = self.panel.temp_head
        sprite = cc.Sprite.create(file_path)
        if not sprite:
            return
        sprite.setAnchorPoint(cc.Vec2(0.5, 0.5))
        size = elem_panel.img_head.getContentSize()
        sprite.setPosition(cc.Vec2(size.width * 0.5, size.height * 0.5))
        scale = size.width / sprite.getTextureRect().width
        sprite.setScale(scale)
        elem_panel.img_head.addChild(sprite)

    def on_send(self, *args):
        from logic.gutils import friend_utils
        from logic.client.const import share_const
        self.close()

        def share_cb(ret):
            from logic.comsys.common_ui.NormalConfirmUI import NormalConfirmUI2
            code = global_data.channel.get_prop_str('LINE_ERROR_CODE')
            fail_msg = global_data.channel.get_prop_str('LINE_ERROR_MESSAGE')
            print('>>>>>> share_cb', ret, code, fail_msg)
            if ret:
                NormalConfirmUI2(content=get_text_by_id(609010))

        key_word = '%s=%s' % (share_const.DEEP_LINK_ADD_FRIEND, '{}_{}'.format(str(global_data.player.uid), 'linegame'))
        global_data.share_mgr.share_linegame('invite_jp', [self._social_id], self._title, self._text, self._link_text, share_cb, a_link_param=key_word)
        friend_utils.salog_friend_ui_oper(friend_utils.FRIEND_LOG_KEY_SHARE_VIA_LINEGAME)

    def on_login_reconnect(self, *args):
        self.close()

    def on_finalize_panel(self):
        pass


class SendTimeLine(WindowSmallBase):
    PANEL_CONFIG_NAME = 'common/common_timeline_confirm'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    TEMPLATE_NODE_NAME = 'temp_bg'
    UI_ACTION_EVENT = {'btn_done.btn_common.OnClick': 'on_send',
       'btn_cancel.btn_common.OnClick': 'close'
       }

    def on_init_panel(self, *args, **kargs):
        super(SendTimeLine, self).on_init_panel()
        self._save_path = kargs.get('save_path', '')
        self._related_path = kargs.get('related_path', '')
        parent = self.panel.img.GetParent()
        w, h = parent.GetContentSize()
        cc.Director.getInstance().getTextureCache().reloadTexture(self._related_path)
        self.panel.img.SetDisplayFrameByPath('', self._related_path)
        w2, h2 = self.panel.img.GetContentSize()
        self.panel.img.setScaleX(float(w) / w2)
        self.panel.img.setScaleY(float(h) / h2)

    def on_login_reconnect(self, *args):
        self.close()

    def on_finalize_panel(self):
        pass

    def on_send(self, *args):
        from logic.gutils import friend_utils
        from logic.client.const import share_const
        self.close()
        global_data.share_mgr.share_linegame_timeline(1, '', '', '', pic_path=self._save_path)