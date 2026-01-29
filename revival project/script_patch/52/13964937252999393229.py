# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/manager_agents/BasicManagerAgent.py
from __future__ import absolute_import
from __future__ import print_function
from logic.manager_agents import ManagerAgentBase
from logic.gcommon.common_utils.local_text import get_text_by_id
import game3d
from project_config import PROJECT_NAME
import version
from common.platform.device_info import DeviceInfo
import device_compatibility
import render
import logic.vscene.DisplayAgent
from common.audio.sound_mgr import SoundMgr
from common.cfg import confmgr
from common.platform.dctool import interface
from common.platform import is_win32
from common.crashhunter import crashhunter_utils
from logic.comsys.battle.survival.CarryManager import CarryManager
from cocosui import cc
import six.moves.builtins
reg_timer = None
reg_idx = 0
REG_DUR = 100

class BasicManagerAgent(ManagerAgentBase.ManagerAgentBase):
    ALIAS_NAME = 'baisc_mgr_agent'
    INIT_FUNC = ('ui', 'basic_event', 'env_sdk', 'crashhunter', 'device', 'display',
                 'sound', 'dctool', 'reloader', 'carry')

    def init(self, *args):
        super(BasicManagerAgent, self).init()
        self.end_tag = False
        self._title = ''
        self.set_window_title()
        self.init_basic_module()

    def init_basic_module(self):
        global reg_timer
        global reg_idx
        if reg_timer:
            game3d.cancel_delay_exec(reg_timer)
            reg_timer = None
        reg_idx = 0
        reg_timer = game3d.delay_exec(REG_DUR, self.init_tick)
        return

    def init_tick(self):
        global reg_idx
        global reg_timer
        try:
            reg_attr = 'init_{}'.format(self.INIT_FUNC[reg_idx])
            reg_func = getattr(self, reg_attr, None)
            if reg_func and callable(reg_func):
                reg_func()
        except Exception as e:
            print('[Except] [BasicManagerAgent] tick init except:[{}]'.format(str(e)))
            import traceback
            traceback.print_exc()
            import exception_hook
            exception_hook.post_error('[BasicManagerAgent] except upload: ' + traceback.format_exc())

        reg_idx += 1
        if reg_idx < len(self.INIT_FUNC):
            game3d.delay_exec(REG_DUR, self.init_tick)
        else:
            game3d.unregister_timer(reg_timer)
            reg_timer = None
            self.init_cb()
        return

    def init_cb(self):
        self._need_resize_ui = False
        global_data.emgr.avatar_finish_create_event_global += self.on_avatar_finish_create
        self.end_tag = True
        if not global_data.ui_mgr:
            game3d.post_hunter_message('BasicManagerAgent- ui_mgr', 'mznb: BasicManagerAgent, missing ui_mgr')
        if not global_data.deviceinfo:
            game3d.post_hunter_message('BasicManagerAgent- deviceinfo', 'mznb: BasicManagerAgent, missing deviceinfo')

    def init_device(self):
        DeviceInfo().init_device_info()
        device_compatibility.configure_device_setting()

    def init_basic_event(self):
        from common import event
        import game
        game.on_window_resize = self.on_window_resize

    def init_display(self):
        from common.utils import package_type
        if package_type.is_android_dds_package():
            render.set_texture_suffix('.dds')
        elif game3d.get_platform() == game3d.PLATFORM_IOS:
            render.set_texture_suffix('.ktx')
        logic.vscene.DisplayAgent.DisplayAgent()

    def init_sound(self):
        SoundMgr()

    def init_carry(self):
        CarryManager()

    def init_dctool(self):
        from common.platform.dctool.mgr import DctoolMgr
        DctoolMgr()

    def init_env_sdk(self):
        channel_conf = confmgr.get('channel_conf', interface.get_game_id())
        env_sdk_key = channel_conf['ENV_SDK_KEY']
        env_sdk_url = channel_conf['ENV_SDK_URL']
        game3d.env_init_sdk(interface.get_project_id(), env_sdk_key, env_sdk_url)

    def init_crashhunter(self):
        channel_conf = confmgr.get('channel_conf', interface.get_game_id())
        dump_app_key = channel_conf['DUMP_APP_KEY']
        crashhunter_utils.init_project(interface.get_project_id())
        crashhunter_utils.init_dump_appkey(dump_app_key)
        crashhunter_utils.init_dump_version()

    def init_reloader(self):
        if is_win32():
            from common.utils import reloadall
            reloadall.init_reload()

    def init_ui(self):
        game3d.add_font_resource('gui/fonts/fzdys.ttf')
        game3d.add_font_resource('gui/fonts/fzy4jw.ttf')
        from common.uisys.UIManager import UIManager
        UIManager()
        self.rescale_patch_ui()

    def rescale_patch_ui(self):
        patch_ui_instance = six.moves.builtins.__dict__.get('PATCH_UI_INSTANCE', None)
        try:
            if patch_ui_instance and patch_ui_instance.widget:
                widget = patch_ui_instance.widget
                widget_size = widget.getContentSize()
                director = cc.Director.getInstance()
                view = director.getOpenGLView()
                vsize = view.getVisibleSize()
                width_ratio = vsize.width / widget_size.width
                height_ratio = vsize.height / widget_size.height
                max_ratio = max(width_ratio, height_ratio)
                widget.setScale(max_ratio)
                if 'PATCH_BG_LAYER' in six.moves.builtins.__dict__:
                    patch_bg_layer = six.moves.builtins.__dict__.get('PATCH_BG_LAYER', None)
                    if patch_bg_layer:
                        patch_bg_layer.setContentSize(cc.Size(vsize.width, vsize.height))
                        patch_bg_layer.setPosition(cc.Vec2(vsize.width * 0.5, vsize.height * 0.5))
        except Exception as e:
            print('[Except] rescale patch ui or bg except:', str(e))

        return

    def set_window_title(self, inf=None):
        if game3d.get_platform() != game3d.PLATFORM_WIN32:
            return
        svn = version.get_cur_version_str()
        title = PROJECT_NAME
        import social
        channel = social.get_channel()
        if channel and channel.name == 'netease':
            title = '\xe6\x9c\xba\xe5\x8a\xa8\xe9\x83\xbd\xe5\xb8\x82\xe9\x98\xbf\xe5\xb0\x94\xe6\xb3\x95'
        game3d.show_error_hint(False)
        game3d.set_window_title(title)
        self._title = title

    def add_title_extra(self, s_txt):
        game3d.set_window_title('{}  {}'.format(self._title, s_txt))

    def on_window_resize(self, w, h, force=False):
        from common.const import common_const
        if game3d.get_platform() == game3d.PLATFORM_ANDROID or force:
            if common_const.WINDOW_WIDTH == w and h == common_const.WINDOW_HEIGHT:
                return
            print('android window resize from', common_const.WINDOW_WIDTH, common_const.WINDOW_HEIGHT, 'to', w, h)
            hw_original = common_const.WINDOW_HEIGHT * 1.0 / common_const.WINDOW_WIDTH
            hw_new = h * 1.0 / w
            common_const.WINDOW_WIDTH = w
            common_const.WINDOW_HEIGHT = h
            global_data.really_window_ratio = 1.0 / hw_new
            print('old sfx size', global_data.really_sfx_window_size)
            import world
            if hasattr(world, 'get_2d_sfx_window_size'):
                global_data.really_sfx_window_size = tuple([ int(x) for x in world.get_2d_sfx_window_size() ]) + game3d.get_window_size()[2:]
            else:
                global_data.really_sfx_window_size = game3d.get_window_size()
            from logic.gutils.screen_effect_utils import refresh_screen_effect_scale_value
            refresh_screen_effect_scale_value(global_data.really_sfx_window_size)
            print('new sfx size', global_data.really_sfx_window_size)
            print('new windows size', game3d.get_window_size())
            global_data.really_window_size = game3d.get_window_size()
            if abs(1.0 - hw_new / hw_original) <= 0.05 and abs(1.0 - hw_original / hw_new) < 0.05:
                return
            logic.vscene.DisplayAgent.DisplayAgent().on_resume()

            def refresh_ui():
                if global_data.player and global_data.ui_mgr and global_data.emgr:
                    global_data.ui_mgr.on_window_size_changed()
                    global_data.emgr.resolution_changed.emit()
                    global_data.emgr.resolution_changed_end.emit()
                else:
                    specific_uis = {
                     'MainLoginUI', 'LoginFunctionUI', 'LoginBgUI'}
                    if global_data.ui_mgr:
                        global_data.ui_mgr.on_window_size_changed(specific_uis)
                    self._need_resize_ui = True

            game3d.delay_exec(500, refresh_ui)

    def on_avatar_finish_create(self):
        if self._need_resize_ui:
            self._need_resize_ui = False
            global_data.ui_mgr.on_window_size_changed()
            global_data.emgr.resolution_changed.emit()
            global_data.emgr.resolution_changed_end.emit()