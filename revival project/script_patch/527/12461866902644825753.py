# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/common_ui/JapanShoppingTips.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
import common.const.uiconst
import common.utilities
from common.const import uiconst

def _is_jp_lang():
    from logic.gcommon.const import SERVER_JK
    server_range = [
     179, SERVER_JK]
    if server_range:
        if global_data.channel.get_login_host() in server_range:
            return True
    return False


def show_with_japan_shopping_tips(ui_cls):
    name = 'JapanShoppingTips_%s' % ui_cls.__name__
    generatedClass = type(name, (JapanShoppingTips,), {'func': lambda self: None,
       'DLG_ZORDER': ui_cls.DLG_ZORDER})
    globals()[name] = generatedClass
    for ass_info in ui_cls.ASSOCIATE_PANEL_PATHS:
        _, ass_name, _, _, _ = ass_info
        if ass_name in ui_cls.ASSOCIATE_PANEL_PATHS:
            return ui_cls

    if ui_cls.ASSOCIATE_PANEL_PATHS:
        ui_cls.ASSOCIATE_PANEL_PATHS = list(ui_cls.ASSOCIATE_PANEL_PATHS)
        ui_cls.ASSOCIATE_PANEL_PATHS.append([_is_jp_lang, name, 'logic.comsys.common_ui.JapanShoppingTips', [None], {}])
    else:
        ui_cls.ASSOCIATE_PANEL_PATHS = [
         [
          _is_jp_lang, name, 'logic.comsys.common_ui.JapanShoppingTips', [None], {}]]
    return ui_cls


class JapanShoppingTips(BasePanel):
    PANEL_CONFIG_NAME = 'common/i_common_tips_lab'
    DLG_ZORDER = common.const.uiconst.DIALOG_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE
    UI_ACTION_EVENT = {'nd_touch.OnClick': 'on_click_nd_touch'
       }
    GLOBAL_EVENT = {}

    def on_click_nd_touch(self, *args, **kargs):
        import game3d
        game3d.open_url('https://www.supermechachampions.com/20190724/31252_824715.html')