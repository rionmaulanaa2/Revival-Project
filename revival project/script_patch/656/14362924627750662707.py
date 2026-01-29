# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/uisystem.py
from __future__ import absolute_import
from __future__ import print_function
import six
import json
import C_file
import cc
import ccui
from .ui_proxy import trans2ProxyObj
from common.framework import Singleton
from logic.gcommon.common_utils.local_text import get_cur_pic_lang_name, get_cur_text_lang
import re
import os
from common.uisys.UICreatorConfig import UICreatorConfig
from common.platform.dctool import interface
import cocosui

def copy_template(template):
    ret = {}
    for k, v in six.iteritems(template):
        if k != 'child_list':
            ret[k] = v

    childLst = template.get('child_list', None)
    if childLst:
        child_list = []
        ret['child_list'] = child_list
        for v in childLst:
            child_list.append(copy_template(v))

    elif childLst == {}:
        ret['child_list'] = {}
    return ret


class UISystem(Singleton):
    ALIAS_NAME = 'uisystem'
    CONF_SUFFIX = '.json'
    CSB_SUFFIX = '.csb'

    def init(self):
        self._ctrlCfg = {}
        self._template_paths = None
        self._loadTemplateCache = {}
        self._loadCSBTemplateCache = {}
        self._templateInfoCache = {}
        self.init_anim_plist_config()
        self._sub_path_prefix = 'txt_pic/text_pic_'
        path_pattern = self._sub_path_prefix + '(\\w+)'
        self._path_pattern = re.compile(path_pattern)
        self._ignore_plist_cache = set()
        self._creator_check_func = None
        self._specialLayoutGroup = None
        from common.cfg import confmgr
        self._ui_sound_map = confmgr.get('ui_sound_map', default={})
        self._txt_pic_path_map = confmgr.get('txt_pic_path_map', default={})
        self.setup_font_config()
        package_type = interface.get_package_type()
        import social
        channel = social.get_channel()
        is_steam_channel = channel and channel.name == 'steam'
        if is_steam_channel:
            package_type = 'CN'
        _path_dict = confmgr.get('ui_res_replace_conf', str(package_type), 'Content', default={})
        self._path_dict = {}
        for k, v_dict in six.iteritems(_path_dict):
            if is_steam_channel and v_dict['new_path'].startswith('gui/ui_res_2/battle'):
                continue
            self._path_dict[k] = v_dict['new_path']

        self._in_use_sprite_paths = set()
        if global_data.feature_mgr and global_data.feature_mgr.is_support_cocos_csb():
            cc.CSLoader.getInstance().enableCsbDataCache(not global_data.is_low_mem_mode and not global_data.is_debug_mode)
        self.plistUsageCollector = None
        from device_compatibility import get_device_perf_flag, is_not_good_memory_size_device, PERF_FLAG_IOS_HIGH, PERF_FLAG_ANDROID_HIGH
        self._can_collect_sprite_usage = get_device_perf_flag() in (PERF_FLAG_IOS_HIGH, PERF_FLAG_ANDROID_HIGH) and not is_not_good_memory_size_device()
        self._recorded_sprite_info_list = []
        self._unfound_pngs = []
        self.check_fallback_sprite()
        if global_data.is_low_mem_mode:
            inst = cc.SpriteFrameCache.getInstance()
            if hasattr(inst, 'setRemoveUnusedOnlyAsWholePlistRemove'):
                inst.setRemoveUnusedOnlyAsWholePlistRemove(False)
        return

    def init_anim_plist_config(self):
        cc.Director.getInstance().getTextureCache().removeUnusedTextures()
        cc.ResManager.destroyInstance()
        s = C_file.get_res_file('gui/ui_res_plist/plist.json', '')
        plists = json.loads(s)
        for plist_path in plists:
            cc.ResManager.getInstance().loadImgPlistMap(plist_path)

        s = C_file.get_res_file('gui/ui_res_plist/plist_config.json', '')
        plist_config = json.loads(s)
        self._anim_plist_config = plist_config.get('anim', {})

    def SetTemplatePath(self, path_list):
        if isinstance(path_list, str):
            path_list = [
             path_list]
        self._template_paths = path_list

    def SetSpecialLayoutGroup(self, groupName):
        self._specialLayoutGroup = groupName

    def GetSpecialLayoutGroup(self):
        return self._specialLayoutGroup

    def OnLangSetup(self):
        self.OnChangeLang()

    def OnChangeLang(self):
        resManager = cc.ResManager.getInstance()
        if global_data.feature_mgr and global_data.feature_mgr.is_support_cocos_csb():
            resManager.setPathReplaceMap(self._txt_pic_path_map.get(get_cur_pic_lang_name(), {}))
        self.setup_font_config()

    def CheckHasTemplate(self, template_name):
        path_list = self._template_paths
        for prefix in path_list:
            path = '%s%s%s' % (prefix, template_name, self.CONF_SUFFIX)
            has = C_file.find_res_file(path, '')
            if has:
                return True

        return False

    def _findNameConf(self, uiconf, nodeInfo=None):
        if nodeInfo is None:
            nodeInfo = {}
        name = uiconf.get('name', None)
        if name and uiconf.get('assign_root', True):
            nodeInfo[name] = uiconf
        child_list = uiconf.get('child_list', None)
        if child_list:
            for subConf in child_list:
                self._findNameConf(subConf, nodeInfo)

        return nodeInfo

    def gen_root_node_conf(self, template):
        nodeInfo = {}
        nodeInfo = self._findNameConf(template, nodeInfo)
        return nodeInfo

    def load_customize_template(self, template, template_info):
        if template_info:
            import copy
            conf = template_info.get('__template__', None)
            if conf:
                return conf
            conf = copy_template(template)
            nodeInfo = self.gen_root_node_conf(conf)
            for name, attr_list in six.iteritems(template_info):
                nodeConf = nodeInfo.get(name, None)
                if nodeConf:
                    if attr_list:
                        if 'type_name' not in nodeConf:
                            raise KeyError('type name not found ', nodeConf)
                        creator = self._ctrlCfg.get(nodeConf['type_name'])
                        if creator:
                            creator.CheckAttributeName(attr_list)
                    nodeConf.update(attr_list)

            template_info['__template__'] = conf
            return conf
        else:
            return template
            return

    def _modify_template_top_node_attr(self, template, top_info):
        if top_info:
            conf = dict(template)
            for name, attr in six.iteritems(top_info):
                conf[name] = attr

            return conf
        else:
            return template

    def load_template(self, template_name, template_info=None, force_json=False):
        if global_data.feature_mgr.is_support_cocos_csb() and not force_json and template_info is None:
            if template_info is not None:
                raise ValueError('csb not support template_info!')
            return template_name
        else:
            if not global_data.is_debug_mode:
                conf = self._loadTemplateCache.get(template_name)
                if conf is not None:
                    return self.load_customize_template(conf, template_info)
            path_list = self._template_paths
            json_str = ''
            path = ''
            need_suffix = template_name.rfind('.') < 0
            for prefix in path_list:
                path = '%s%s%s' % (prefix, template_name, self.CONF_SUFFIX if need_suffix else '')
                try:
                    json_str = C_file.get_res_file(path, '')
                    break
                except:
                    json_str = ''

            if not json_str:
                import exception_hook
                if path:
                    find_res = C_file.find_res_file(path, '')
                    data_len = -1
                    if find_res:
                        try:
                            data_len = len(C_file.get_res_file(path, ''))
                        except Exception as e:
                            print('[Song] find_res true, get except:', str(e))
                            data_len = -2

                    res_path = C_file.get_res_path(path)
                    except_str = 'template not found: {}, template: {}, find_res: {}, data_len: {} res_path:{}'.format(path, template_name, find_res, data_len, res_path)
                    import traceback
                    exception_hook.post_error(except_str + str(traceback.format_stack()))
                else:
                    exception_hook.post_error('template not found with empty path %s' % template_name)
                msg = 'not exist template %s ' % template_name
                self.post_wizard_trace(msg, None, 'gui/template/%s.json' % template_name)
                raise Exception(msg)
            conf = json.loads(json_str)
            conf['recorded_template_path'] = template_name
            if not global_data.is_low_mem_mode:
                self._loadTemplateCache[template_name] = conf
            return self.load_customize_template(conf, template_info)

    def unload_template(self, template_name):
        if template_name in self._loadTemplateCache:
            del self._loadTemplateCache[template_name]

    def clear_template_cache(self):
        self._loadTemplateCache = {}
        if global_data.feature_mgr.is_support_cocos_csb():
            cc.CSLoader.getInstance().clearCsbDataCache()
            import ccs
            ccs.ActionTimelineCache.getInstance().purge()

    def load_template_create(self, template_name, parent=None, root=None, template_info=None, name=None, force_json=False):
        tconf = self.load_template(template_name, template_info, force_json)
        ret = self.create_item(tconf, parent, root, name=name, force_json=force_json)
        if ret:
            self.BindWidgetSoundName(template_name, ret)
        return ret

    def create_item(self, conf, parent=None, root=None, aniConf=None, name=None, force_json=False):
        if global_data.feature_mgr.is_support_cocos_csb() and type(conf) in (str, six.text_type) and not force_json:
            return self.load_template_create_new(conf, parent, root, name=name)
        else:
            ret = None
            if self._creator_check_func and not self._creator_check_func(conf):
                return
            if isinstance(parent, cc.Node):
                parent = trans2ProxyObj(parent)
            if 'type_name' not in conf:
                raise KeyError('type name not found ', conf)
            creator = self._ctrlCfg.get(conf['type_name'])
            if aniConf is None:
                aniConf = {}
                ret = creator.Create(conf, parent, root, aniConf)
                ret.SetAnimationConf(aniConf)
            else:
                ret = creator.Create(conf, parent, root, aniConf)
            if parent and name:
                parent.AddChildRecord(name, ret)
                ret.widget_name = name
            if root and root != ret and name:
                setattr(root, name, ret)
            return ret

    def re_create_item(self, node, root=None, tmp_path=None):
        widget_name = node.GetName()
        p = node.GetParent()
        node.Destroy()
        ret = global_data.uisystem.load_template_create(tmp_path, parent=p, root=root, name=widget_name)
        return ret

    def create_item_with_check(self, conf, parent=None, root=None, aniConf=None, checkfunc=None):
        self._creator_check_func = checkfunc
        ret = self.create_item(conf, parent, root, aniConf)
        self._creator_check_func = None
        return ret

    def play_template_animation(self, template_name, aniName, parent=None, is_play=True):
        if parent is None:
            parent = cc.Director.getInstance().getRunningScene()
        obj = self.load_template_create(template_name, parent)
        if is_play:
            obj.PlayAnimation(aniName)
        return obj

    def create_ani_info_for_single_node(self, ccnode, template_conf, target_ani_name_list=None, ani_name_prefix=None):
        if not template_conf:
            return (None, None)
        else:
            ani_info = {}
            UICreatorConfig.add_ani_data_2_ani_conf(template_conf, ani_info, ccnode, (lambda ani_name: ani_name_prefix + ani_name) if ani_name_prefix else None, target_ani_name_list=target_ani_name_list)
            if len(ani_info) == 0:
                ani_info = None
            ani_times = None
            if ani_info:
                original_ani_times = template_conf.get('ani_times', None)
                if original_ani_times:
                    ani_times = {}
                    for original_ani_name, times in six.iteritems(original_ani_times):
                        final_ani_name = ani_name_prefix + original_ani_name
                        if final_ani_name in ani_info:
                            ani_times[final_ani_name] = times

            return (
             ani_info, ani_times)

    def regist_uicreator(self, cname, creator):
        self._ctrlCfg[cname] = creator

    def get_creator(self, cname):
        return self._ctrlCfg[cname]

    def get_fixed_template_path(self, template_name, ext_name):
        path_list = self._template_paths
        csb_str = ''
        path = ''
        for prefix in path_list:
            path = '%s%s%s' % (prefix, template_name, ext_name)
            try:
                csb_str = C_file.find_res_file(path, '')
                break
            except:
                csb_str = ''

        if not csb_str:
            import exception_hook
            if path:
                find_res = str(C_file.find_res_file(path, ''))
                exception_str_pattern = 'csb template not found filepath is %s, template name is %s, file find res is %s'
                exception_str = exception_str_pattern % (path, template_name, find_res)
                exception_hook.post_error(exception_str)
            else:
                exception_hook.post_error('csb template not found with empty path %s' % template_name)
            raise Exception('csb not exist template %s ' % template_name)
        return path

    def load_template_new(self, template_name, async_load=False):
        return self._create_template_new(template_name, async_load)

    def _create_template_new(self, template_name, async_load=False):
        path = self.get_fixed_template_path(template_name, '.csb')
        cocosui.modify_engine_args_dict('UI_ASYNC_LOAD_IMAGE', 1 if async_load else 0)
        cocosui.modify_engine_args_dict('UI_SEARCH_FULL_PATH', 0)
        ret = cc.CSLoader.getInstance().createNodeWithFlatBuffersFile(path, True)
        cocosui.modify_engine_args_dict('UI_ASYNC_LOAD_IMAGE', 0)
        cocosui.modify_engine_args_dict('UI_SEARCH_FULL_PATH', 1)
        return ret

    def load_template_create_new(self, template_name, parent=None, root=None, template_info=None, name=None):
        if global_data.is_inner_server:
            if not global_data.feature_mgr.is_support_cocos_csb():
                global_data.game_mgr.show_tip('\xe6\x9a\x82\xe6\x9c\xaa\xe6\x94\xaf\xe6\x8c\x81csb\xef\xbc\x8c\xe8\xaf\xb7\xe6\xa3\x80\xe6\x9f\xa5\xe8\xb0\x83\xe7\x94\xa8\xe6\xb5\x81\xe7\xa8\x8b\xef\xbc\x81')
                return
        async_load = global_data.enable_ui_add_image_async and not global_data.temporary_force_image_sync
        conf_node = self.load_template_new(template_name, async_load=async_load)
        name and conf_node.setName(name)
        from . import cocomate
        parent = cocomate.get_cocomate_node_by_cocos_node(parent, True)
        wrap_node = cocomate.get_cocomate_node_by_cocos_node(conf_node)
        parent and parent.AddChild(name, wrap_node)
        if parent:
            cocomate.do_cocomate_layout(conf_node, True, includeSpecialChildren=True)
        cocomate.bind_names(root, conf_node, parent, None, None)
        wrap_node.SetAnimationConf({})
        self.BindWidgetSoundName(template_name, wrap_node)
        return wrap_node

    def GetSpriteFramePlistByPath(self, path):
        if path in self._ignore_plist_cache:
            return None
        else:
            multilang_path = self.SpritePathReplaceCheck(path)
            if multilang_path in self._ignore_plist_cache:
                return None
            plist = cc.ResManager.getInstance().getImgPlistPath(multilang_path)
            if plist:
                return plist
            plist = cc.ResManager.getInstance().getImgPlistPath(path)
            if plist:
                return plist
            return None

    def LoadSpriteFramesByPath(self, path):
        if self.GetSpriteFramePlistByPath(path):
            if not cc.ResManager.getInstance().loadImgSpriteFrames(path):
                log_error('loadImgSpriteFrames failed', path)
            return ccui.WIDGET_TEXTURERESTYPE_PLIST
        else:
            return ccui.WIDGET_TEXTURERESTYPE_LOCAL

    def GetSpriteFrameByPath(self, path, plist=''):
        plist, path = (plist or '', path or '')
        if plist == '' and path == '':
            if global_data.is_inner_server:
                msg = 'try to get an empty sprite!!!!'
                import traceback
                traceback.print_stack()
                print(msg)
            sprite = self._GetSpriteFrameByPath(self.fallback_sprite, '')
            return sprite
        sprite = self._GetSpriteFrameByPath(self.SpritePathReplaceCheck(path), plist)
        if not sprite:
            sprite = self._GetSpriteFrameByPath(path, plist)
        if sprite:
            return sprite
        msg = 'spriteframe %s %s not found' % (plist, path)
        print(msg)
        self.post_wizard_trace(msg, plist, path)
        sprite = self._GetSpriteFrameByPath(self.fallback_sprite, '')
        return sprite

    def GetSpritePathAndPlist(self, path, plist):
        plist, path = plist or '', path or ''
        if plist == '' and path == '':
            if global_data.is_inner_server:
                msg = 'try to get an empty sprite!!!!'
                import traceback
                traceback.print_stack()
                print(msg)
                self.post_wizard_trace(msg)
            sprite_path_plist = (
             self.fallback_sprite, '')
            return sprite_path_plist
        new_path = self.SpritePathReplaceCheck(path)
        sprite = self._GetSpriteFrameByPath(new_path, plist)
        sprite_path_plist = (new_path, plist or self.GetSpriteFramePlistByPath(new_path) or '')
        if not sprite:
            sprite = self._GetSpriteFrameByPath(path, plist)
            sprite_path_plist = (path, plist or self.GetSpriteFramePlistByPath(path) or '')
        if sprite:
            return sprite_path_plist
        msg = 'spriteframe %s %s not found' % (plist, path)
        print(msg)
        self.post_wizard_trace(msg, plist, path)
        p = self.fallback_sprite
        sprite_path_plist = (p, self.GetSpriteFramePlistByPath(p) or '')
        return sprite_path_plist

    def GetSpritePathAndPlistAsync(self, path, plist, callback):
        plist, path = plist or '', path or ''
        if plist == '' and path == '':
            if global_data.is_inner_server:
                msg = 'try to get an empty sprite!!!!'
                import traceback
                traceback.print_stack()
                print(msg)
            p = self.fallback_sprite
            callback(p, self.GetSpriteFramePlistByPath(p) or '')
            return
        new_path = self.SpritePathReplaceCheck(path)

        def _on_callback_1(sprite, callback):
            if sprite:
                callback(path, plist or self.GetSpriteFramePlistByPath(path) or '')
                return
            msg = 'spriteframe %s %s not found' % (plist, path)
            print(msg)
            self.post_wizard_trace(msg, plist, path)
            p = self.fallback_sprite
            callback(p, self.GetSpriteFramePlistByPath(p) or '')

        def _on_callback_0(sprite, orig_path, callback):
            if sprite:
                callback(new_path, plist or self.GetSpriteFramePlistByPath(new_path) or '')
            else:
                self._GetSpriteFrameByPathAsync(orig_path, plist, lambda sprite, callback=callback: _on_callback_1(sprite, callback))

        self._GetSpriteFrameByPathAsync(new_path, plist, lambda sprite, orig_path=path, callback=callback: _on_callback_0(sprite, orig_path, callback))

    def GetSpriteFrameByPathAsync(self, path, plist='', callback=None):
        if not global_data.enable_ui_add_image_async:
            raise ValueError('Wrong config for enable_ui_add_image_async!')
        plist, path = plist or '', path or ''
        if plist == '' and path == '':
            msg = 'try to get an empty sprite!!!!'
            import traceback
            traceback.print_stack()
            print(msg)
            self.post_wizard_trace(msg)
            self._GetSpriteFrameByPathAsync(self.fallback_sprite, '', callback)
            return

        def _on_callback_1(sprite, callback):
            if sprite:
                callback(sprite)
                return
            msg = 'spriteframe %s %s not found' % (plist, path)
            print(msg)
            self.post_wizard_trace(msg, plist, path)
            self._GetSpriteFrameByPathAsync(self.fallback_sprite, '', callback)

        def _on_callback_0(sprite, orig_path, callback):
            if sprite:
                callback(sprite)
            else:
                self._GetSpriteFrameByPathAsync(orig_path, plist, lambda sprite, callback=callback: _on_callback_1(sprite, callback))

        self._GetSpriteFrameByPathAsync(self.SpritePathReplaceCheck(path), plist, lambda sprite, orig_path=path, callback=callback: _on_callback_0(sprite, orig_path, callback))

    def _GetSpriteFrameByPath(self, path, plist=''):
        if path not in self._ignore_plist_cache and cc.ResManager.getInstance().loadImgSpriteFrames(path):
            tex = cc.SpriteFrameCache.getInstance().getSpriteFrame(path)
            if tex:
                return tex
            if global_data.is_inner_server:
                log_error('_GetSpriteFrameByPath failed to load from plist', path, plist)
        if plist != '':
            cc.SpriteFrameCache.getInstance().addSpriteFrames(plist)
            sprite_frame = cc.SpriteFrameCache.getInstance().getSpriteFrame(path)
            if sprite_frame is not None:
                return sprite_frame
            if global_data.is_inner_server:
                log_error('_GetSpriteFrameByPath failed plist! ', path, plist)
        else:
            texture = cc.Director.getInstance().getTextureCache().addImage(path)
            if texture is not None:
                size = texture.getContentSize()
                rect = cc.Rect(0, 0, size.width, size.height)
                sprite_frame = cc.SpriteFrame.createWithTexture(texture, rect)
                return sprite_frame
        if global_data.is_inner_server:
            log_error('_GetSpriteFrameByPath failed path! ', path, plist)
        if global_data.is_inner_server:
            target = 'gui/ui_res_2/battle/mech_main'
            if path.startswith(target):
                log_error('_GetSpriteFrameByPath path not in self._ignore_plist_cache', path not in self._ignore_plist_cache, plist)
        return

    def _GetSpriteFrameByPathAsync(self, path, plist='', callback=None):
        if path not in self._ignore_plist_cache:

            def _cb(texture):
                tex = cc.SpriteFrameCache.getInstance().getSpriteFrame(path)
                if tex:
                    callback(tex)
                    return
                else:
                    if plist != '':

                        def _cb(texture):
                            sprite_frame = cc.SpriteFrameCache.getInstance().getSpriteFrame(path)
                            if sprite_frame is not None:
                                callback(sprite_frame)
                                return
                            else:
                                return

                        if not cc.SpriteFrameCache.getInstance().isSpriteFramesFileLoaded(plist):
                            cc.SpriteFrameCache.getInstance().addSpriteFramesAsync(plist, _cb)
                        else:
                            _cb(None)
                    else:
                        cc.Director.getInstance().getTextureCache().addImageAsync(path, lambda tex2d, filepath=path, callback=callback: self._OnGetSpriteFrameByPathAsync(tex2d, filepath, callback))
                    return

            if cc.ResManager.getInstance().loadImgSpriteFramesAsync(path, _cb):
                return
        if plist != '':

            def _cb(texture):
                sprite_frame = cc.SpriteFrameCache.getInstance().getSpriteFrame(path)
                if sprite_frame is not None:
                    callback(sprite_frame)
                    return
                else:
                    return

            if not cc.SpriteFrameCache.getInstance().isSpriteFramesFileLoaded(plist):
                cc.SpriteFrameCache.getInstance().addSpriteFramesAsync(plist, _cb)
            else:
                _cb(None)
        else:
            cc.Director.getInstance().getTextureCache().addImageAsync(path, lambda tex2d, filepath=path, callback=callback: self._OnGetSpriteFrameByPathAsync(tex2d, filepath, callback))
        return

    def _OnGetSpriteFrameByPathAsync(self, texture, filepath, callback):
        if texture is not None:
            size = texture.getContentSize()
            rect = cc.Rect(0, 0, size.width, size.height)
            sprite_frame = cc.SpriteFrame.createWithTexture(texture, rect)
            callback(sprite_frame)
            return
        else:
            callback(None)
            return

    def CreateSpriteFrameByPathAsync(self, file_path, plist, cls, cc_type, need_resize=False):
        if not global_data.enable_ui_add_image_async:
            raise ValueError('No CreateSpriteFrameByPathAsync when enable_ui_add_image_async = False!')
            return None
        else:

            def _cb(frame, obj):
                if global_data.enable_ui_add_image_async:
                    if obj and obj.get():
                        obj.ModifyAsyncTaskCount(-1)
                if obj and obj.get() and frame:
                    obj.setSpriteFrame(frame)
                    if need_resize:
                        obj.ResizeAndPosition(include_self=True)
                global_data.uisystem.RecordSpriteUsage(plist, file_path, obj)

            obj = cls(cc_type.create())
            if global_data.enable_ui_add_image_async:
                obj.ModifyAsyncTaskCount(1)
            global_data.uisystem.GetSpriteFrameByPathAsync(file_path, '', lambda sprite, _obj=obj: _cb(sprite, _obj))
            return obj

    def GetSpriteByPath(self, path):
        sprite_frame = self.GetSpriteFrameByPath(path)
        return cc.Sprite.createWithSpriteFrame(sprite_frame)

    def GetAnimPlistByConfig(self, path):
        if path in self._anim_plist_config:
            path = 'gui/ui_res_plist/%s.plist' % self._anim_plist_config[path]
        return path

    def SpritePathReplaceCheck(self, path):
        path = self._path_dict.get(path, path)
        lang_2_path = self._txt_pic_path_map.get(get_cur_pic_lang_name(), {})
        return lang_2_path.get(path, path)

    def IgnoreSpritePath(self, path):
        import C_file
        C_file.enable_filesys_debug()
        self._ignore_plist_cache.add(path)

    def BindWidgetSoundName(self, template_name, root):
        ui_sound_map = self._ui_sound_map.get(template_name)
        if ui_sound_map:
            for widget_path, sound_name in six.iteritems(ui_sound_map):
                cur_widget = root
                paths = widget_path.split('.')
                for widget_name in paths:
                    if widget_name != '':
                        if cur_widget:
                            cur_widget = getattr(cur_widget, widget_name, None)
                        else:
                            break

                if cur_widget:
                    cur_widget._enable_click_sound = True
                    cur_widget.set_click_sound_name2(sound_name)

        return

    def RecordUsedSpritePaths(self):
        if not global_data.enable_sprite_path_record:
            return
        self._RecordUsedSpritePathsInner()

    def _RecordUsedSpritePathsInner(self):
        infos = cc.Director.getInstance().getTextureCache().getCachedTextureInfo()
        import re
        pattern = re.compile('(".*")')
        results = pattern.findall(infos)
        spriteCacheMgr = cc.SpriteFrameCache.getInstance()
        if hasattr(spriteCacheMgr, 'getCurrentSpriteFrameNames') and spriteCacheMgr.getCurrentSpriteFrameNames:
            spriteFrames = spriteCacheMgr.getCurrentSpriteFrameNames()
        else:
            spriteFrames = []
        for res in results:
            self._in_use_sprite_paths.add(res)

        for sp in spriteFrames:
            self._in_use_sprite_paths.add(sp)

    def GetVisibleNodeSprites(self):
        plist_dict = {}
        for plist, sp, node in self._recorded_sprite_info_list:
            if node and node.isValid():
                if node.isVisible() and node.isAncestorsVisible():
                    if not plist:
                        plist = cc.ResManager.getInstance().getImgPlistPath(sp) or ''
                    if plist:
                        plist_dict.setdefault(plist, set())
                        plist_dict[plist].add(sp)
                    else:
                        plist_dict.setdefault('None', set())
                        plist_dict['None'].add(sp)

        for k, v in six.iteritems(plist_dict):
            print('dump_used_sprite_to_files plist dict', k)
            for p in sorted(list(v)):
                print(p)

    def dump_used_sprite_to_files(self):
        self._RecordUsedSpritePathsInner()
        plist_dict = {}
        for sp in self._in_use_sprite_paths:
            plist = cc.ResManager.getInstance().getImgPlistPath(sp)
            plist_dict.setdefault(plist, list())
            plist_dict[plist].append(sp)

        for k, v in six.iteritems(plist_dict):
            print('dump_used_sprite_to_files plist dict', k)
            for p in sorted(v):
                print(p)

    def SaveUsedSpritePaths(self):
        if not global_data.enable_sprite_path_record:
            return
        sprite_path_records = global_data.achi_mgr.get_archive_data('sprite_path_records')
        import datetime
        today_str = str(datetime.date.today())
        for sp in self._in_use_sprite_paths:
            sprite_path_records[str(sp)] = today_str

        sprite_path_records.save(False)

    def setup_font_config(self):
        from data import font_table, font_face_table
        from logic.gcommon.common_utils.local_text import get_force_font_trans, get_cur_lang_shrink_setting, get_extra_vertical_space
        font_table = font_table.data.get(str(get_cur_text_lang()), {})
        from cocosui import ccs
        reader = ccs.GUIReader.getInstance()
        for org_font, target_font in six.iteritems(font_table):
            reader.setFontAlias(org_font, target_font)

        if global_data.feature_mgr and global_data.feature_mgr.is_support_cocos_csb():
            reader.setEditBoxFontTrans(get_force_font_trans())
            lang_conf = get_cur_lang_shrink_setting()
            reader.setFontSizeOffsetConfig(lang_conf.iFontSzOffset, lang_conf.iMinFontSize)
            reader.setFontExtraVerticalSpace(get_extra_vertical_space())

    def RecordSpriteUsage(self, plist, path, node):
        if global_data.enable_collect_ui:
            if global_data.usage_recorder and not global_data.is_low_mem_mode and self._can_collect_sprite_usage:
                global_data.usage_recorder.record_sprite_usage(plist, path)
                if global_data.is_inner_server:
                    self._recorded_sprite_info_list.append([plist, path, node])

    def post_wizard_trace(self, msg, plist=None, path=None):
        try:
            if G_TRUNK_PC:
                if plist:
                    path = plist
                if path:
                    if not global_data._lack_gui_res:
                        global_data._lack_gui_res = set()
                    path = '/res/%s' % path
                    global_data._lack_gui_res.add(path)
        except:
            pass

        import traceback
        error_content = '%s\n' % msg
        error_content += '\n'.join(traceback.format_stack())
        import game3d
        game3d.post_hunter_message('lack sprite', error_content)

    def post_wizard_trace_inner_server(self, msg):
        if global_data.is_inner_server:
            import exception_hook
            exception_hook.post_stack(msg)
            self._unfound_pngs.append(msg)
        try:
            pass
        except:
            pass

    def check_fallback_sprite(self):
        self.fallback_sprite = 'gui/ui_res_2/common/panel/transparent.png'