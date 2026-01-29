# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/UIManager.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
from six.moves import range
from functools import cmp_to_key
import os
import cc
import C_file
import json
import six
from common.framework import Singleton
from common.utils.cocos_utils import getScreenSize
from common.const import uiconst
import game3d
from common.const.uiconst import BETWEEN_BG_AND_BSCALE_PLATE_ZORDER, SCALE_PLATE_ZORDER, SMALL_MAP_ZORDER, BASE_LAYER_ZORDER, BASE_LAYER_ZORDER_1, BATTLE_MESSAGE_ZORDER, NORMAL_LAYER_ZORDER, TOP_ZORDER, GUIDE_LAYER_ZORDER, AIM_ZORDER, HP_ZORDER, LOW_MESSAGE_ZORDER, DIALOG_LAYER_BAN_ZORDER, DIALOG_LAYER_ZORDER, DIALOG_LAYER_ZORDER_1, DIALOG_LAYER_ZORDER_2, TOP_MSG_ZORDER, UI_TYPE_NORMAL, ROCKER_LAYER_ZORDER, NORMAL_LAYER_ZORDER_00, NORMAL_LAYER_ZORDER_0, NORMAL_LAYER_ZORDER_1, NORMAL_LAYER_ZORDER_2, SECOND_CONFIRM_LAYER, SCREEN_LOCKER_ZORDER, DISCONNECT_ZORDER, LOADING_BG_ZORDER, LOADING_ZORDER, LOADING_ZORDER_ABOVE, NORMAL_LAYER_ZORDER_3, DIALOG_LAYER_ZORDER_0
from logic.gcommon.common_utils import local_text
from logic.gcommon.common_const.lang_data import LANG_ZHTW, LANG_CN, LANG_EN, lang_data
from logic.gcommon.common_const.voice_lang_data import VOICE_JA, VOICE_CN
from logic.gutils.salog import SALog
from common.utils.cocos_utils import ccp, CCSize
from logic.gutils import system_unlock_utils
from logic.gutils.pc_ui_utils import MOBILE_2_PC_UI_DICT, PC_2_MOBILE_UI_DICT
from common.utils.timer import CLOCK, LOGIC
import version
SPECIAL_UIS = ('SceneSnapShotUI', 'ScreenSnapShotUI', 'ScreenSnapShotLoadingBgUI')

class UIManager(Singleton):
    ALIAS_NAME = 'ui_mgr'
    SIMPLE_DLG_INDEX = 0
    LANG_CONF = 'lang_data'
    VOICE_LANG_CONF = 'voice_lang_data'

    def init(self):
        self.layer_zorder_list = sorted([
         AIM_ZORDER,
         BETWEEN_BG_AND_BSCALE_PLATE_ZORDER,
         SCALE_PLATE_ZORDER,
         SMALL_MAP_ZORDER,
         HP_ZORDER,
         LOW_MESSAGE_ZORDER,
         ROCKER_LAYER_ZORDER,
         BASE_LAYER_ZORDER,
         BASE_LAYER_ZORDER_1,
         BATTLE_MESSAGE_ZORDER,
         NORMAL_LAYER_ZORDER_00,
         NORMAL_LAYER_ZORDER_0,
         NORMAL_LAYER_ZORDER,
         NORMAL_LAYER_ZORDER_1,
         NORMAL_LAYER_ZORDER_2,
         NORMAL_LAYER_ZORDER_3,
         DIALOG_LAYER_BAN_ZORDER,
         GUIDE_LAYER_ZORDER,
         DIALOG_LAYER_ZORDER_0,
         DIALOG_LAYER_ZORDER,
         DIALOG_LAYER_ZORDER_1,
         DIALOG_LAYER_ZORDER_2,
         SECOND_CONFIRM_LAYER,
         TOP_ZORDER,
         TOP_MSG_ZORDER,
         LOADING_BG_ZORDER,
         LOADING_ZORDER,
         LOADING_ZORDER_ABOVE,
         SCREEN_LOCKER_ZORDER,
         DISCONNECT_ZORDER])
        self.local_lang_dict = {}
        self.local_lang_inited = False
        self.slide_screen_size = None
        self.init_data()
        self.init_cocos()
        from common.uisys.uisystem import UISystem
        self.uis = UISystem()
        self.uis.SetTemplatePath(['gui/template/'])
        self.uis.OnLangSetup()
        self.init_ui_layer()
        self.render_target_holder_list = []
        self.ui_show_whitelist = []
        self.ui_show_whitelist_tag = None
        self.enable_profile_init_panel = False
        self.blocking_ui_list = {}
        self.init_special_layout()
        self.init_panel_and_item_cache()
        self._clear_tex_timer = None
        self.reset_clear_tex_timer()
        return

    def init_local_lang(self):
        try:
            if self.local_lang_inited:
                return
            conf_dict = {}
            try:
                s = C_file.get_res_file('confs/c_lang_change_config.json', '')
                conf_dict = json.loads(s)
            except Exception as e:
                log_error('jsonconf load except confs/c_lang_change_config.json', str(e))
                conf_dict = {}

            self.local_lang_dict = {}
            for k, v in six.iteritems(conf_dict):
                self.local_lang_dict[k.replace('_', '-').lower()] = v

            self.local_lang_inited = True
        except Exception as e:
            print('[ERROR] @ INIT LOCAL LANG' + str(e))
            import traceback
            traceback.print_stack()

    def get_local_language_code(self, use_default=True):
        self.init_local_lang()
        lang_str = game3d.get_local_language()
        if not lang_str:
            return None
        else:
            lang_str = lang_str.lower()
            if lang_str in self.local_lang_dict:
                return self.local_lang_dict[lang_str]
            if '-' in lang_str:
                lang_code_list = lang_str.split('-')
                if len(lang_code_list) >= 3:
                    sp_str = '%s-%s' % (lang_code_list[0], lang_code_list[1])
                    if sp_str in self.local_lang_dict:
                        return self.local_lang_dict[sp_str]
                lang_code = lang_code_list[0]
                if lang_code in self.local_lang_dict:
                    return self.local_lang_dict[lang_code]
            if use_default:
                return LANG_EN
            return None
            return None

    def init_cocos(self):
        CC_LOG_LEVEL_WARNING = 30
        cc.Director.getInstance().getConsole().setLogLevel(CC_LOG_LEVEL_WARNING)
        from common.const import common_const
        if global_data.feature_mgr.is_support_cocos_tex_async_load():
            print('[COCOS] is_support_cocos_tex_async_load enable_ui_add_image_async = False')
            global_data.enable_ui_add_image_async = True
        else:
            print('[COCOS] is_support_cocos_tex_async_load enable_ui_add_image_async = False')
            global_data.enable_ui_add_image_async = False
        if version.get_tag() != 'trunk':
            global_data.enable_cocos_csb = False
        director = cc.Director.getInstance()
        if global_data.cocos_scene is None:
            gui_scene = director.getRunningScene()
            if not gui_scene:
                gui_scene = cc.Scene.create()
                director.runWithScene(gui_scene)
            global_data.cocos_scene = gui_scene
        self.update_cocos_design_screen_resolution()
        self.init_space_node()
        self.init_lang()
        self.init_fallback_font()
        self.init_word_boundary_chars()
        self.blocking_ui_list = {}
        return

    def update_cocos_design_screen_resolution(self):
        from common.utils.cocos_utils import CCSize
        director = cc.Director.getInstance()
        view = director.getOpenGLView()
        self.screen_size = getScreenSize()
        w = 0
        h = 0
        w, h, _, _, _ = game3d.get_window_size()
        if self.slide_screen_size is None or game3d.get_platform() in [game3d.PLATFORM_WIN32]:
            self.slide_screen_size = self.screen_size
        from common.utils.ui_utils import s_showDesignSize, s_fixDesignResolution
        if not s_fixDesignResolution:
            self.design_screen_size = CCSize(w, h)
            view.setDesignResolutionSize(w, h, cc.RESOLUTIONPOLICY_NO_BORDER)
        else:
            self.design_screen_size = cc.Size(s_showDesignSize)
            view.setDesignResolutionSize(s_showDesignSize.width, s_showDesignSize.height, cc.RESOLUTIONPOLICY_NO_BORDER)
        if global_data.is_enable_slide_screen_size:
            self.slide_screen_size = self.design_screen_size
        return

    def enable_slide_screen_size(self):
        global_data.is_enable_slide_screen_size = True
        self.slide_screen_size = self.design_screen_size

    def init_lang(self):
        lang = self.read_lang_conf()
        voice_lang = self.read_voice_lang_conf(lang)
        local_text.set_text_lang(lang)
        local_text.set_voice_lang(voice_lang)
        self.install_simui_font()

    def install_simui_font(self):
        lang = local_text.get_cur_text_lang()
        from common.uisys.font_utils import GetFontTableByLang
        font_table = GetFontTableByLang(str(lang))
        if font_table:
            unique_fonts = set(six_ex.values(font_table))
            for font in unique_fonts:
                game3d.add_font_resource(font)

    def init_fallback_font(self):
        import cc
        if global_data.feature_mgr.is_support_fallback_font_list():
            fallback_font_list = [
             'gui/fonts/fzdys_tw.ttf', 'gui/fonts/fzy4jw.ttf', 'gui/fonts/g93_kr_thick.ttf', 'gui/fonts/font_tha.ttc']
        else:
            fallback_font_list = [
             'gui/fonts/fzy4jw.ttf']
        if hasattr(cc, 'FontAtlasFallbackSetting') and cc.FontAtlasFallbackSetting:
            cc.FontAtlasFallbackSetting.setFallbackFontNames(fallback_font_list)

    def init_word_boundary_chars(self):
        import cc
        if six.PY3:
            boundary_chars = '\\u200a'
        else:
            boundary_chars = '\\u200a'.decode('raw_unicode_escape')
        if hasattr(cc, 'LabelTextBoundarySetting') and cc.LabelTextBoundarySetting:
            cc.LabelTextBoundarySetting.setBoundaryChars(boundary_chars)

    def init_space_node(self):
        import cocosui
        cocosui.SpaceNode.init_root()
        if hasattr(cocosui, 'enable_font_cold_cache'):
            cocosui.enable_font_cold_cache(False)
        root = cocosui.SpaceNode.get_root()
        if not root.getParent() and global_data.cocos_scene:
            global_data.cocos_scene.addChild(root)

    def reset_layer_wh(self, layer, w, h):
        layer.setPosition(ccp(w / 2, h / 2))
        layer.ignoreAnchorPointForPosition(False)
        layer.setAnchorPoint(ccp(0.5, 0.5))
        layer.setVisible(False)
        layer.setContentSize(CCSize(w, h))
        layer.setVisible(True)
        layer.SetEnableTouch(False)
        return True

    def reset_canvas_and_bg_for_layer(self, zorder_layer):
        from common.utils.cocos_utils import ccp
        w, h = self.design_screen_size.width, self.design_screen_size.height
        nd_bg_node = zorder_layer.nd_bg
        self.reset_layer_wh(nd_bg_node, w, h)
        self.reset_canvas_for_layer(zorder_layer)

    def reset_canvas_for_layer(self, zorder_layer):
        from common.platform.device_info import DeviceInfo
        device_info = DeviceInfo()
        w, h = self.design_screen_size.width, self.design_screen_size.height
        if not device_info.is_can_full_screen():
            margins_conf = device_info.get_screen_adapt_margins()
            WIDTH_EDGE_OFFSET = int(w * margins_conf.get('WIDTH_EDGE_OFFSET', 0))
            BOTTOM_EDGE_OFFSET = int(h * margins_conf.get('BOTTOM_EDGE_OFFSET', 0))
            TOP_EDGE_OFFSET = int(h * margins_conf.get('TOP_EDGE_OFFSET', 0))
            canvas_width = w - WIDTH_EDGE_OFFSET * 2
            canvas_height = h - BOTTOM_EDGE_OFFSET - TOP_EDGE_OFFSET
            layer = self._get_or_create_adapt_layer(canvas_width, canvas_height, zorder_layer, name='nd_canvas')
            layer.setPosition(ccp(w / 2, canvas_height / 2 + BOTTOM_EDGE_OFFSET))
        else:
            self._get_or_create_adapt_layer(w, h, zorder_layer, name='nd_canvas')

    def _get_or_create_adapt_layer(self, w, h, parent, name, zorder=0):
        from common.uisys.uielment.CCNode import CCNode
        layer = None
        if not isinstance(parent, CCNode):
            layer = parent.getChildByName(name)
        elif hasattr(parent, name):
            layer = getattr(parent, name, None)
        if not layer:
            layer = self._create_adapt_layer(w, h, parent, name, zorder)
        else:
            self.reset_layer_wh(layer, w, h)
        return layer

    def _create_adapt_layer(self, w, h, parent, name=None, zorder=0):
        from common.uisys.uielment.CCLayer import CCLayer
        from common.uisys.uielment.CCNode import CCNode
        layer = CCLayer.Create()
        if not isinstance(parent, CCNode):
            parent.addChild(layer.get(), zorder)
        else:
            parent.AddChild(name, layer, zorder)
        self.reset_layer_wh(layer, w, h)
        return layer

    def create_canvas_and_bg_for_layer(self, zorder_layer):
        w, h = self.design_screen_size.width, self.design_screen_size.height
        self._create_adapt_layer(w, h, zorder_layer, name='nd_bg')
        self.reset_canvas_for_layer(zorder_layer)

    def check_layer_by_lift_scene(self, enter_lift_scene=False):
        if enter_lift_scene:
            show_layer = [
             GUIDE_LAYER_ZORDER, TOP_ZORDER, TOP_MSG_ZORDER, LOADING_ZORDER]
            for order in self.layer_zorder_list:
                if order in show_layer:
                    show = True if 1 else False
                    layer = self.ui_layer_dict[order]
                    layer.setVisible(show)

        else:
            for order in self.layer_zorder_list:
                layer = self.ui_layer_dict[order]
                layer.setVisible(True)

    def init_render_target(self):
        from common.uisys.render_target import RenderTarget
        RenderTarget()

    def start_render_target(self):
        from common.uisys.render_target import RenderTarget
        RenderTarget().start_render_target_timer()

    def stop_render_target(self):
        from common.uisys.render_target import RenderTarget
        RenderTarget().stop_render_target_timer()

    def add_render_target_holder(self, holder):
        if holder not in self.render_target_holder_list:
            self.render_target_holder_list.append(holder)
        else:
            log_error('render_target already in list!!!')
        self.start_render_target()

    def remove_render_target_holder(self, holder):
        if holder in self.render_target_holder_list:
            self.render_target_holder_list.remove(holder)
        if not self.render_target_holder_list:
            self.stop_render_target()

    def init_data(self):
        self.dialogs = {}
        self.dlg_stack = []
        self.ui_layer_dict = {}

    def create_simple_dialog(self, template_name, zorder=None, **kwargs):
        from .basepanel import BasePanel
        attrs = {'PANEL_CONFIG_NAME': template_name,
           'DLG_ZORDER': zorder,
           'UI_VKB_TYPE': uiconst.UI_VKB_CLOSE
           }
        attrs.update(kwargs)
        cls_name = '_SimpleDialog%d' % UIManager.SIMPLE_DLG_INDEX
        UIManager.SIMPLE_DLG_INDEX += 1
        cls = type(cls_name, (BasePanel,), attrs)
        return cls()

    def create_dialog(self, dlg, template_name, zorder=None, ui_name=None, is_full_screen=False, template_info=None, exception_ignore_zorder=False):
        dlg_name = dlg.get_name()
        if dlg_name in self.dialogs:
            raise Exception('dumplicate dlg with name %s ' % dlg_name)
        if zorder is None:
            zorder = BASE_LAYER_ZORDER
        if global_data.is_inner_server:
            if global_data.player and global_data.player.is_in_battle():
                if global_data.game_mgr.scene.is_loaded():
                    msg = 'tmp cr n bttl: %s, %s' % (dlg_name, template_name)
                    game3d.post_hunter_message('tmp cr n bttl:' + msg, msg)
        ui_layer_dict = self.ui_layer_dict
        if zorder in ui_layer_dict:
            if is_full_screen:
                parent = ui_layer_dict[zorder].nd_bg
            else:
                parent = ui_layer_dict[zorder].nd_canvas
        elif not exception_ignore_zorder:
            raise Exception('InCorrect panel zorder')
        global_data.temporary_force_image_sync = not getattr(dlg, 'ASYNC_LOAD_IMAGE', True)
        cocos_item = self.uis.load_template_create(template_name, parent, None, template_info=template_info)
        global_data.temporary_force_image_sync = False
        self.dialogs[dlg_name] = dlg
        self.dlg_stack.append(dlg_name)
        is_need_check_dlg = False
        if dlg_name in self.blocking_ui_list:
            tag_list = self.blocking_ui_list[dlg_name]
            for tag in tag_list:
                dlg.add_hide_count(tag, is_check=False)
                is_need_check_dlg = True

        if self.ui_show_whitelist and dlg_name not in self.ui_show_whitelist:
            if not (dlg_name and dlg_name.startswith('_SimpleDialog')):
                dlg.add_hide_count(self.ui_show_whitelist_tag, is_check=False)
            is_need_check_dlg = True
        if is_need_check_dlg:
            dlg.check_show_count_dict()
        return cocos_item

    def set_dialog_zorder(self, dlg, zorder=None, is_full_screen=False):
        ui_layer_dict = self.ui_layer_dict
        if zorder in ui_layer_dict:
            if is_full_screen:
                parent = ui_layer_dict[zorder].nd_bg
            else:
                parent = ui_layer_dict[zorder].nd_canvas
            dlg.removeFromParent()
            parent.AddChild('', dlg)

    def get_ui_zorder_layer(self, zorder):
        return self.ui_layer_dict.get(zorder, None)

    def close_ui(self, dlg_or_name, show_main_ui=True):
        dlg = dlg_or_name
        if isinstance(dlg_or_name, str):
            dlg = self.get_ui(dlg_or_name)
        if dlg is None:
            return
        else:
            dname = dlg.get_name()
            widget = dlg.get_widget()
            if dname in self.dialogs:
                del self.dialogs[dname]
                self.dlg_stack.remove(dname)
                if not widget:
                    raise Exception('try close dlg %s in uimanager but interanl cocos obj not valid' % dname)
            print('[DEBUG FOR UI] close_ui:%s =====' % dlg)
            if not show_main_ui:
                dlg.clear_hide_set()
            dlg.finalize()
            global_data.emgr.ui_close_event.emit(dname)
            return

    def reset_clear_tex_timer(self):
        if self._clear_tex_timer:
            global_data.game_mgr.unregister_logic_timer(self._clear_tex_timer)
            self._clear_tex_timer = None
        if global_data.is_32bit:
            clear_interval = 20
        else:
            clear_interval = 60
        self._clear_tex_timer = global_data.game_mgr.register_logic_timer(self.clear_unused_render_res, interval=clear_interval, times=-1, mode=CLOCK)
        return

    def get_ui(self, dname):
        if global_data.is_pc_mode and dname in MOBILE_2_PC_UI_DICT:
            dname = MOBILE_2_PC_UI_DICT[dname]
        return self.dialogs.get(dname, None)

    def show_ui(self, dname, module_path='logic.dialog'):
        if global_data.game_mode:
            mode_type = global_data.game_mode.get_mode_type()
            from logic.client.const import game_mode_const
            ui_names = game_mode_const.FORBID_UI.get(mode_type)
            if ui_names and dname in ui_names:
                return
        if not system_unlock_utils.can_open_ui(dname):
            return
        else:
            if global_data.is_pc_mode and dname in MOBILE_2_PC_UI_DICT:
                dname = MOBILE_2_PC_UI_DICT[dname]
            mconf = __import__(module_path, globals(), locals(), [dname], 0)
            if not mconf:
                raise Exception('no ui dialog class %s in %s' % (dname, module_path))
            module = getattr(mconf, dname, None)
            dlg_cls = getattr(module, dname, None)
            if not dlg_cls:
                raise Exception('dialog file name not match dialog class name %s' % dname)
            return dlg_cls()

    def show_ui_with_args(self, dname, module_path='logic.dialog', *args, **kwargs):
        if global_data.game_mode:
            mode_type = global_data.game_mode.get_mode_type()
            from logic.client.const import game_mode_const
            ui_names = game_mode_const.FORBID_UI.get(mode_type)
            if ui_names and dname in ui_names:
                return
        if not system_unlock_utils.can_open_ui(dname):
            return
        else:
            if global_data.is_pc_mode and dname in MOBILE_2_PC_UI_DICT:
                dname = MOBILE_2_PC_UI_DICT[dname]
            module = __import__(module_path, fromlist=[dname])
            if not module:
                raise Exception('no ui dialog class %s in %s' % (dname, module_path))
            dlg_cls = getattr(module, dname, None)
            if not dlg_cls:
                raise Exception('dialog file name not match dialog class name %s' % dname)
            return dlg_cls(*args, **kwargs)

    def hide_ui(self, dname):
        ui = self.get_ui(dname)
        if ui:
            ui.hide()

    def clear_unused_render_res(self):
        import render
        self.remove_unused_textures()

    def remove_unused_textures(self):
        cc.SpriteFrameCache.getInstance().removeUnusedSpriteFrames()
        cc.Director.getInstance().getTextureCache().removeUnusedTextures()

    def change_lang(self, lang, voice=None):
        self.save_lang_conf(lang)
        local_text.set_text_lang(lang)
        voice = voice if voice is not None else self.get_default_voice_lang(lang)
        self.save_voice_conf(voice)
        local_text.set_voice_lang(voice)
        self.install_simui_font()
        global_data.uisystem.OnChangeLang()
        player = global_data.player
        if player and player.in_local_battle():
            player.logic.send_event('E_GUIDE_DESTROY')
            global_data.ui_mgr.close_ui('MainSettingUI')
            global_data.ui_mgr.close_ui('LanguageSettingUI')
            player.logic.send_event('E_GUIDE_RESET')
        else:
            global_data.ui_mgr.close_all_ui()
            global_data.game_mgr.reload_scene()
            if global_data.game_voice_mgr is not None:
                global_data.game_voice_mgr.unload_bank(True)
            from logic.gutils.ConnectHelper import ConnectHelper
            ConnectHelper().disconnect()
        return

    def read_lang_conf_from_setting(self, use_local=True):
        try:
            _path = os.path.join(game3d.get_doc_dir(), self.LANG_CONF)
            f = open(_path, 'r')
            s = f.read()
            f.close()
            return int(s)
        except:
            if use_local:
                return self.get_local_language()
            return None

        return None

    def get_local_language(self):
        from common.platform.dctool import interface
        if interface.is_mainland_package():
            return LANG_CN
        else:
            local_lang = self.get_local_language_code()
            if local_lang is None:
                return LANG_EN
            return int(local_lang)
            return LANG_EN

    def read_lang_conf(self):
        setting_lang = self.read_lang_conf_from_setting()
        if setting_lang is None:
            setting_lang = LANG_ZHTW
        return setting_lang

    def save_lang_conf(self, lang):
        cur_lang = self.read_lang_conf_from_setting(False)
        if cur_lang is None and lang is not None:
            salog_writer = SALog.get_instance()
            salog_writer.write(SALog.LANGUAGE_SELECTED, lang)
        import os
        _path = os.path.join(game3d.get_doc_dir(), self.LANG_CONF)
        try:
            f = open(_path, 'w+')
            f.write(str(lang))
            f.close()
        except:
            pass

        return

    def read_voice_lang_conf_from_setting(self):
        try:
            _path = os.path.join(game3d.get_doc_dir(), self.VOICE_LANG_CONF)
            f = open(_path, 'r')
            s = f.read()
            f.close()
            return int(s)
        except:
            return None

        return None

    def get_default_voice_lang(self, lang):
        default_voice = VOICE_JA
        from common.platform.dctool import interface
        if interface.is_mainland_package():
            default_voice = VOICE_CN
        print('default_voice', default_voice)
        ret_lang = lang_data.get(lang, {}).get('cVoiceLang', default_voice)
        print('ret_lang', ret_lang)
        return ret_lang

    def read_voice_lang_conf(self, lang):
        setting_voice = self.read_voice_lang_conf_from_setting()
        if setting_voice is None:
            setting_voice = self.get_default_voice_lang(lang)
        return setting_voice

    def save_voice_conf(self, voice):
        import os
        _path = os.path.join(game3d.get_doc_dir(), self.VOICE_LANG_CONF)
        try:
            f = open(_path, 'w+')
            f.write(str(voice))
            f.close()
        except:
            pass

    def close_all_ui_by_type(self, target_ui_types=(
 UI_TYPE_NORMAL,), exceptions=()):
        to_be_close_ui_list = self.get_all_ui_by_type(target_ui_types, exceptions)
        for dialog in to_be_close_ui_list:
            if dialog.__class__.__name__ in SPECIAL_UIS:
                continue
            self.close_ui(dialog)

        to_be_close_ui_list = []

    def close_all_ui(self, exceptions=()):
        all_uis = six_ex.keys(self.dialogs)
        for dialog_name in all_uis:
            if dialog_name in exceptions:
                continue
            if dialog_name.startswith('_SimpleDialog'):
                continue
            if dialog_name in PC_2_MOBILE_UI_DICT and PC_2_MOBILE_UI_DICT[dialog_name] in exceptions:
                continue
            if dialog_name in SPECIAL_UIS:
                continue
            self.close_ui(dialog_name, False)

    def close_list_ui(self, list_ui_to_be_close):
        _type = type(list_ui_to_be_close)
        if _type is tuple or _type is list:
            for ui_to_be_close in list_ui_to_be_close:
                self.close_ui(ui_to_be_close)

    def get_all_ui_by_type(self, target_ui_types=(
 UI_TYPE_NORMAL,), exceptions=()):
        to_be_ui_list = []
        for dialog_name, dialog in six.iteritems(self.dialogs):
            if dialog.UI_TYPE in target_ui_types:
                if dialog_name in exceptions:
                    continue
                if dialog_name in PC_2_MOBILE_UI_DICT and PC_2_MOBILE_UI_DICT[dialog_name] in exceptions:
                    continue
                to_be_ui_list.append(dialog)

        return to_be_ui_list

    def hide_all_ui_by_type(self, key, target_ui_types=(
 UI_TYPE_NORMAL,), exceptions=()):
        to_be_hide_ui_list = self.get_all_ui_by_type(target_ui_types, exceptions)
        for dialog in to_be_hide_ui_list:
            dialog.add_hide_count(key, is_check=False)

        for ui in to_be_hide_ui_list:
            ui.check_show_count_dict()

        hide_name_list = [ dialog.__class__.__name__ for dialog in to_be_hide_ui_list ]
        return hide_name_list

    def hide_all_ui_by_key(self, key, ui_list, exceptions=()):
        hide_name_list = []
        if not ui_list:
            ui_list = six_ex.keys(self.dialogs)
        need_check_ui = []
        for dialog_name in ui_list:
            if dialog_name in exceptions or dialog_name.startswith('_SimpleDialog'):
                continue
            if dialog_name in PC_2_MOBILE_UI_DICT and PC_2_MOBILE_UI_DICT[dialog_name] in exceptions:
                continue
            dlg = self.dialogs.get(dialog_name, None)
            if dlg:
                dlg.add_hide_count(key, is_check=False)
                need_check_ui.append(dlg)
                hide_name_list.append(dialog_name)

        for ui in need_check_ui:
            ui.check_show_count_dict()

        return hide_name_list

    def revert_hide_all_ui_by_key_action(self, key, hide_name_list):
        need_check_ui = []
        for name in hide_name_list:
            ui_inst = self.get_ui(name)
            if ui_inst:
                need_check_ui.append(ui_inst)
                ui_inst.add_show_count(key, is_check=False)

        for ui in need_check_ui:
            ui.check_show_count_dict()

    def set_all_ui_visible(self, vis):
        if global_data.cocos_scene:
            global_data.cocos_scene.setVisible(vis)
            global_data.emgr.all_ui_visibility_changed_event.emit()

    def get_all_ui_visible(self):
        if global_data.cocos_scene:
            return global_data.cocos_scene.isVisible()
        return False

    def rec(self, node, uname):
        if not node:
            return
        try:
            print('rec', uname, node.GetPosition(), node.getPosition(), node.GetContentSize(), node.getContentSize(), node.getScale())
            children = six_ex.keys(node.coms)
            children.sort()
            for child in children:
                item = getattr(node, child)
                self.rec(item, child)

        except:
            pass

    def reconf_all_ui(self, specific_uis=None):
        all_uis = six_ex.keys(self.dialogs)
        all_uis.sort()
        if specific_uis:
            all_uis = set(all_uis) & specific_uis
        show_count_dict_record = {}
        for uname in all_uis:
            ui = self.get_ui(uname)
            if ui:
                show_count_dict_record[uname] = {}
                show_count_dict_record[uname].update(ui._show_count_dict)

        for uname in all_uis:
            ui = self.get_ui(uname)
            if not ui:
                continue
            if ui.RECREATE_WHEN_RESOLUTION_CHANGE:
                self.close_ui(uname)
                if getattr(ui, 'RECONNECT_CHECK_BATTLE', None):
                    if not global_data.battle:
                        return
                ui = ui.__class__(None, *ui.recreate_tuple_args, **ui.recreate_args)
            else:
                self.recursive_check_node_scale(ui.panel)
                ui.ResizeAndPosition()
                if getattr(ui, 'init_custom_com', False):
                    if hasattr(ui, 'custom_ui_com') and ui.custom_ui_com:
                        ui.custom_ui_com.on_resolution_changed()
                    ui.init_custom_com()
                    if hasattr(ui, 'custom_ui_com') and ui.custom_ui_com:
                        ui.custom_ui_com.refresh_all_custom_ui_conf()

        for uname in all_uis:
            ui = self.get_ui(uname)
            if ui:
                ui._show_count_dict = show_count_dict_record[uname]
                ui.ClearAllNodeActionCache()
                ui.check_show_count_dict()
                ui.on_resolution_changed()
                ui._init_reused_ani_info()
                ui._check_play_reused_anim_on_init()

        global_data.emgr.reconf_all_ui_end.emit()
        return

    def recursive_check_node_scale(self, root):
        scale_node = self.check_node_scale(root)
        if scale_node:
            scale_node.ScaleSelfNode()
            return True
        for node in root.GetChildren():
            self.recursive_check_node_scale(node)

    def check_node_scale(self, node):
        if not node:
            return None
        else:
            scale = node.GetConfScale()
            if scale and type(scale['x']) in [six.text_type, str] and scale['x'][-1] in ('w',
                                                                                         's',
                                                                                         'q',
                                                                                         'k',
                                                                                         'g'):
                return node
            return None
            return None

    def rec_all_ui(self):
        all_uis = six_ex.keys(self.dialogs)
        all_uis.sort()
        for uname in all_uis:
            ui = self.get_ui(uname)
            self.rec(ui, uname)

    def on_window_size_changed(self, specific_uis=None):
        from common.utils.ui_utils import on_window_size_changed
        on_window_size_changed()
        self.update_cocos_design_screen_resolution()
        self.reset_ui_layer()
        global_data.emgr.reconf_all_ui_before.emit()
        self.reconf_all_ui(specific_uis)

    def force_show_notch_screen(self):
        global_data.force_notch_screen = True
        self.on_window_size_changed()
        global_data.emgr.resolution_changed.emit()
        global_data.emgr.resolution_changed_end.emit()

    def clear_ui_layer(self):
        ui_layer_dict = self.ui_layer_dict
        for zorder, layer in six.iteritems(ui_layer_dict):
            layer.Destroy()

        self.ui_layer_dict = {}

    def init_ui_layer(self):
        scene = global_data.cocos_scene
        w, h = self.design_screen_size.width, self.design_screen_size.height
        ui_layer_dict = self.ui_layer_dict
        for zorder in self.layer_zorder_list:
            layer = self._create_adapt_layer(w, h, scene, zorder)
            ui_layer_dict[zorder] = layer
            self.create_canvas_and_bg_for_layer(layer)

    def reset_ui_layer(self):
        w, h = self.design_screen_size.width, self.design_screen_size.height
        for zorder in self.layer_zorder_list:
            layer = self.get_ui_zorder_layer(zorder)
            if not layer:
                log_error('layer {} not exist'.format(zorder))
            else:
                self.reset_layer_wh(layer, w, h)
                self.reset_canvas_and_bg_for_layer(layer)

    def add_blocking_tag(self, ui_name_list, tag):
        for ui_name in ui_name_list:
            if ui_name not in self.blocking_ui_list:
                self.blocking_ui_list[ui_name] = set()
            self.blocking_ui_list[ui_name].add(tag)

    def remove_blocking_tag(self, ui_name_list, tag):
        for ui_name in ui_name_list:
            if ui_name in self.blocking_ui_list:
                if tag in self.blocking_ui_list[ui_name]:
                    self.blocking_ui_list[ui_name].remove(tag)

    def init_special_layout(self):
        self.uis.SetSpecialLayoutGroup('iPhone X')
        return
        from common.platform.device_info import DeviceInfo
        device_info = DeviceInfo()
        import game3d
        if not device_info.is_can_full_screen() and game3d.PLATFORM_IOS:
            self.uis.SetSpecialLayoutGroup('iPhone X')

    def init_panel_and_item_cache(self):
        from common.uisys.UIPool import UIPool
        UIPool()
        from common.uisys.item_caches_without_check import ItemCacheWithOutCheck
        ItemCacheWithOutCheck()

    def get_dlg_stack_by_zorder(self):
        visible_dlg_stack = []
        for ui_name in global_data.ui_mgr.dlg_stack:
            ui_inst = global_data.ui_mgr.get_ui(ui_name)
            if ui_inst:
                ui_inst.isPanelVisible()
                visible_dlg_stack.append(ui_name)

        def zorder_cmp(name_a, name_b):
            ui_inst_a = global_data.ui_mgr.get_ui(name_a)
            ui_inst_b = global_data.ui_mgr.get_ui(name_b)
            if ui_inst_a:
                zorder_a = ui_inst_a.on_get_template_zorder()
            else:
                zorder_a = 0
            if ui_inst_b:
                zorder_b = ui_inst_b.on_get_template_zorder()
            else:
                zorder_b = 0
            return six_ex.compare(zorder_a, zorder_b)

        visible_dlg_stack = sorted(visible_dlg_stack, key=cmp_to_key(zorder_cmp))
        return visible_dlg_stack

    def add_blocking_ui_list(self, ui_name_list, key):
        global_data.ui_mgr.add_blocking_tag(ui_name_list, key)
        need_check_ui = []
        for ui_name in ui_name_list:
            ui = global_data.ui_mgr.get_ui(ui_name)
            if ui:
                ui.add_hide_count(key, is_check=False)
                need_check_ui.append(ui)

        for ui in need_check_ui:
            ui.check_show_count_dict()

    def remove_blocking_ui_list(self, ui_name_list, key):
        need_check_ui = []
        for ui_name in ui_name_list:
            ui = global_data.ui_mgr.get_ui(ui_name)
            if ui:
                ui.add_show_count(key, is_check=False)
                need_check_ui.append(ui)

        global_data.ui_mgr.remove_blocking_tag(ui_name_list, key)
        for ui in need_check_ui:
            ui.check_show_count_dict()

    def add_ui_show_whitelist(self, ui_show_whitelist, tag):
        if not tag:
            return
        if self.ui_show_whitelist_tag == tag:
            return
        need_check_ui = []
        for dlg_name, dlg in six.iteritems(self.dialogs):
            is_need_check_dlg = False
            if self.ui_show_whitelist_tag and self.ui_show_whitelist_tag != tag:
                if dlg_name not in self.ui_show_whitelist and dlg.add_hide_count_before(self.ui_show_whitelist_tag):
                    dlg.add_show_count(self.ui_show_whitelist_tag, is_check=False)
                    is_need_check_dlg = True
            if dlg_name not in ui_show_whitelist and not dlg_name.startswith('_SimpleDialog'):
                dlg.add_hide_count(tag, is_check=False)
                is_need_check_dlg = True
            if is_need_check_dlg:
                need_check_ui.append(dlg)

        self.ui_show_whitelist = ui_show_whitelist
        self.ui_show_whitelist_tag = tag
        for ui in need_check_ui:
            ui.check_show_count_dict()

    def remove_ui_show_whitelist(self, tag):
        if self.ui_show_whitelist_tag != tag:
            return
        else:
            need_check_ui = []
            for dlg_name, dlg in six.iteritems(self.dialogs):
                if dlg_name not in self.ui_show_whitelist and dlg.add_hide_count_before(self.ui_show_whitelist_tag):
                    dlg.add_show_count(self.ui_show_whitelist_tag, is_check=False)
                    need_check_ui.append(dlg)

            self.ui_show_whitelist = []
            self.ui_show_whitelist_tag = None
            for ui in need_check_ui:
                ui.check_show_count_dict()

            return

    def get_all_basepanel_subclass(self, only_direct_child=False):

        def inheritors(klass):
            subclasses = set()
            work = [klass]
            while work:
                parent = work.pop()
                for child in parent.__subclasses__():
                    if child not in subclasses:
                        subclasses.add(child)
                        work.append(child)

            return subclasses

        import os
        import logic

        def walk_dir(path):
            root_path = path
            for root, dirs, files in os.walk(path):
                for name in files:
                    if name.endswith('.py') and not name.startswith('__'):
                        full_path = os.path.join(root, name)
                        rel_p = os.path.relpath(full_path, root_path)
                        module_name = 'logic.' + rel_p.replace(os.path.sep, '.').replace('.py', '')
                        if '.' in module_name:
                            idx = module_name.rindex('.')
                            A = module_name[0:idx]
                            B = module_name[idx + 1:]
                            try:
                                __import__(A, fromlist=[B])
                            except:
                                print('Failed ', module_name)

                        else:
                            try:
                                __import__(module_name)
                            except:
                                pass

        walk_dir(logic.__path__[0])
        from common.uisys.basepanel import BasePanel
        if only_direct_child:
            return set(BasePanel.__subclasses__())
        subclasses = inheritors(BasePanel)
        return subclasses

    def check_ui_vkb_type(self, only_direct_child):
        sub_classes = self.get_all_basepanel_subclass(only_direct_child)
        print('check_ui_vkb_type', len(sub_classes))
        for sub_c in sub_classes:
            self.process_basepanel_subclass(sub_c)

    def process_basepanel_subclass(self, sub_c):
        BACK_BTN_NAME = ('on_click_close_btn', 'on_click_back_btn')
        import re
        m = __import__(sub_c.__module__, fromlist=[sub_c])
        file_path = m.__file__
        from inspect import getargspec
        if sub_c.UI_VKB_TYPE is None:
            content = '\r\n\tUI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT\r\n'
            for name in BACK_BTN_NAME:
                func = getattr(sub_c, name, None)
                if func:
                    args, varargs, varkw, defaults = getargspec(func)
                    if len(args) == 1 or defaults and len(args) == len(defaults) + 1:
                        content = '\r\n\tUI_VKB_TYPE = uiconst.UI_VKB_CLOSE\r\n'
                        break

            f = open(os.path.abspath(file_path), 'rb')
            if not f:
                print('open file failed', os.path.abspath(file_path))
                return False
            lines = f.readlines()
            class_start_index = -1
            for idx, line in enumerate(lines):
                if re.match('^class[ ].*%s\\(' % sub_c.__name__, line):
                    class_start_index = idx
                    break

            dlg_zorder_line_index = -1
            if class_start_index >= 0:
                for i in range(class_start_index, len(lines)):
                    if re.match('\tDLG_ZORDER[ ].*=', lines[i]):
                        dlg_zorder_line_index = i
                        break

            else:
                print("can't find class", sub_c)
            if dlg_zorder_line_index >= 1:
                if 'uiconst' in m.__dict__:
                    lines.insert(dlg_zorder_line_index + 1, content)
                else:
                    lines.insert(class_start_index - 1, 'from common.const import uiconst\r\n')
                    lines.insert(dlg_zorder_line_index + 2, content)
            elif 'uiconst' in m.__dict__:
                lines.insert(class_start_index + 1, content)
            else:
                lines.insert(class_start_index - 1, 'from common.const import uiconst\r\n')
                lines.insert(class_start_index + 2, content)
            if content == '\r\n\tUI_VKB_TYPE = uiconst.UI_VKB_CLOSE\r\n':
                print('Sub_C is close!!!', sub_c)
            f.close()
            fw = open(os.path.abspath(file_path), 'wb')
            fw.write(''.join(lines))
            fw.close()
            reload(m)
            return True
        else:
            return True
            return