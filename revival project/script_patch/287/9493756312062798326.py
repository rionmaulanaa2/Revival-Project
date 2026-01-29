# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lobby/NewSysPrompt/NewSysPromptViewData.py
from __future__ import absolute_import

class ViewContentProvider(object):

    def __init__(self):
        pass

    def get_system_text_pic_path(self):
        raise NotImplementedError

    def get_system_icon_path(self):
        raise NotImplementedError


class ViewContentProviderFactory(object):

    def __init__(self):
        pass

    def peek_next(self):
        raise NotImplementedError

    def pop_next(self):
        raise NotImplementedError


class NewSysPromptProvider(ViewContentProvider):

    def __init__(self, sys_type):
        super(NewSysPromptProvider, self).__init__()
        self._sys_type = sys_type

    def get_system_text_pic_path(self):
        from logic.gcommon.common_const import new_system_prompt_data as sp_const
        if self._sys_type == sp_const.SYSTEM_CAREER:
            return 'gui/ui_res_2/txt_pic/text_pic_en/type_sysopen_career.png'
        else:
            if self._sys_type == sp_const.SYSTEM_BATTLE_FLAG:
                return 'gui/ui_res_2/txt_pic/text_pic_en/type_sysopen_id.png'
            if self._sys_type == sp_const.SYSTEM_INSCRIPTION:
                return 'gui/ui_res_2/txt_pic/text_pic_en/type_sysopen_techsystem.png'
            return ''

    def get_system_icon_path(self):
        from logic.gcommon.common_const import new_system_prompt_data as sp_const
        if self._sys_type == sp_const.SYSTEM_CAREER:
            return 'gui/ui_res_2/main/new_function_tips/img_sysopen_career_icon.png'
        else:
            if self._sys_type == sp_const.SYSTEM_BATTLE_FLAG:
                return 'gui/ui_res_2/main/new_function_tips/img_sysopen_id_icon.png'
            if self._sys_type == sp_const.SYSTEM_INSCRIPTION:
                return 'gui/ui_res_2/main/new_function_tips/icon_opensys_techsystem2.png'
            return ''

    def get_system_type(self):
        return self._sys_type


class NewSysPromptProviderFactory(ViewContentProviderFactory):

    def __init__(self):
        super(NewSysPromptProviderFactory, self).__init__()

    def peek_next(self):
        prompt = global_data.new_sys_open_mgr.peek_next_prompt()
        if prompt is None:
            return
        else:
            return NewSysPromptProvider(prompt)
            return

    def pop_next(self):
        prompt = global_data.new_sys_open_mgr.pop_next_prompt()
        if prompt is None:
            return
        else:
            return NewSysPromptProvider(prompt)
            return


class NewSysMechaSkinDefinePromptProvider(ViewContentProvider):

    def __init__(self):
        super(NewSysMechaSkinDefinePromptProvider, self).__init__()

    def get_system_text_pic_path(self):
        return 'gui/ui_res_2/txt_pic/text_pic_en/sysopen_diy_left.png'

    def get_system_icon_path(self):
        return 'gui/ui_res_2/main/new_function_tips/icon_opensys_paint.png'


class NewSysMSDPromptProviderFactory(ViewContentProviderFactory):

    def __init__(self):
        super(NewSysMSDPromptProviderFactory, self).__init__()
        self.ele = NewSysMechaSkinDefinePromptProvider()

    def peek_next(self):
        return self.ele

    def pop_next(self):
        self.ele = None
        return


class SysUnlockProvider(ViewContentProvider):

    def __init__(self, sys_type):
        super(SysUnlockProvider, self).__init__()
        self._sys_type = sys_type
        from logic.gutils import system_unlock_utils
        self._icon_path, self._text_pic_path = system_unlock_utils.get_sys_unlock_ui_pics(sys_type)

    def get_system_text_pic_path(self):
        return self._text_pic_path

    def get_system_icon_path(self):
        return self._icon_path

    def get_system_type(self):
        return self._sys_type


class SysSysUnlockProviderFactory(ViewContentProviderFactory):

    def __init__(self):
        super(SysSysUnlockProviderFactory, self).__init__()

    def peek_next(self):
        msg = global_data.sys_unlock_mgr.peek_next_msg()
        if msg is None:
            return
        else:
            return SysUnlockProvider(msg)
            return

    def pop_next(self):
        msg = global_data.sys_unlock_mgr.pop_next_msg()
        if msg is None:
            return
        else:
            return SysUnlockProvider(msg)
            return