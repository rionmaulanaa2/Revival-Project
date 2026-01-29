# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/patch/patch_lang.py
from __future__ import absolute_import
from __future__ import print_function
import C_file
import six
if six.PY3:
    import json as json2
else:
    import json2
from patch.font_table import data as font_data
from patch import lang_data
import game3d
import os
LOCAL_LANG_CODE_DICT = {}
LOCAL_LANG_INITED = False
MULTI_LANG_INSTANCE = None
TEXT_PATH_DICT = {lang_data.LANG_CN: 'cn',
   lang_data.LANG_EN: 'en',
   lang_data.LANG_ZHTW: 'ctra',
   lang_data.LANG_JA: 'jp',
   lang_data.LANG_KO: 'ko'
   }
TEXT_FILE_PATTERN = 'confs/text/{}/'
LANG_CONF = 'lang_data'
STEAM_UI_LANGUAGE = None

def init_steam_language(lan):
    global STEAM_UI_LANGUAGE
    STEAM_UI_LANGUAGE = lan


def get_multi_lang_instane():
    global MULTI_LANG_INSTANCE
    if MULTI_LANG_INSTANCE is None:
        MULTI_LANG_INSTANCE = PatchMultiLang()
    return MULTI_LANG_INSTANCE


def get_patch_text_id(text_id, *args):
    try:
        return get_multi_lang_instane().get_patch_text_id(text_id, *args)
    except:
        return ''


def get_patch_text_id_only_exist(text_id, *args):
    try:
        return get_multi_lang_instane().get_patch_text_id_only_exist(text_id, *args)
    except:
        return None

    return None


def init_local_lang():
    global LOCAL_LANG_CODE_DICT
    global LOCAL_LANG_INITED
    try:
        if LOCAL_LANG_INITED:
            return
        conf_dict = {}
        try:
            s = C_file.get_res_file('confs/c_lang_change_config.json', '')
            conf_dict = json2.loads(s)
        except Exception as e:
            log_error('jsonconf load except confs/c_lang_change_config.json', str(e))
            conf_dict = {}

        LOCAL_LANG_CODE_DICT = {}
        for k, v in six.iteritems(conf_dict):
            LOCAL_LANG_CODE_DICT[k.replace('_', '-').lower()] = v

        LOCAL_LANG_INITED = True
    except Exception as e:
        print('[ERROR] @ INIT LOCAL LANG' + str(e))


def get_local_language():
    init_local_lang()
    try:
        lang_str = game3d.get_local_language()
        if not lang_str:
            return lang_data.LANG_CN
        lang_str = lang_str.replace('_', '-').lower()
        if lang_str in LOCAL_LANG_CODE_DICT:
            return LOCAL_LANG_CODE_DICT[lang_str]
        if '-' in lang_str:
            lang_code_list = lang_str.split('-')
            if len(lang_code_list) >= 3:
                sp_str = '%s-%s' % (lang_code_list[0], lang_code_list[1])
                if sp_str in LOCAL_LANG_CODE_DICT:
                    return LOCAL_LANG_CODE_DICT[sp_str]
            lang_code = lang_code_list[0]
            if lang_code in LOCAL_LANG_CODE_DICT:
                return LOCAL_LANG_CODE_DICT[lang_code]
    except Exception as e:
        print('[ERROR] @ GET LOCAL LANG' + str(e))

    return lang_data.LANG_EN


class PatchMultiLang(object):

    def __init__(self):
        super(PatchMultiLang, self).__init__()
        self.init_data()

    def init_data(self):
        self.init_cnt_lang()

    def load_text_file(self, tid):
        conf_dict = {}
        try:
            lang_text_path = TEXT_FILE_PATTERN.format(TEXT_PATH_DICT.get(self.cnt_lang_code, 'en'))
            page_path1 = lang_text_path + 'text_' + str(int(tid) // 10000) + '.json'
            if C_file.find_res_file(page_path1, ''):
                s = C_file.get_res_file(page_path1, '')
            else:
                s = C_file.get_res_file('confs/text/lang_{}.json'.format(TEXT_PATH_DICT.get(self.cnt_lang_code, 'en')), '')
            conf_dict.update(json2.loads(s))
        except Exception as e:
            print(str(e))
            conf_dict = {}

        self.text_dict.update(conf_dict)

    def get_patch_text_id_only_exist(self, text_id, *args):
        text = ''
        try:
            if str(text_id) not in self.text_dict:
                self.load_text_file(text_id)
            if str(text_id) not in self.text_dict:
                return ''
            text = self.text_dict.get(str(text_id), '')
            if args:
                text = text.format(*args)
        except Exception as e:
            text = 'text id %d format error' % text_id
            print(text, str(e))

        return text or 'text id %d undefined' % text_id

    def get_patch_text_id(self, text_id, *args):
        text = ''
        try:
            if str(text_id) not in self.text_dict:
                self.load_text_file(text_id)
            text = self.text_dict.get(str(text_id), '')
            if args:
                text = text.format(*args)
        except Exception as e:
            text = 'text id %d format error' % text_id
            print(text, str(e))

        return text or 'text id %d undefined' % text_id

    def init_font(self):
        font_table = font_data.get(str(self.cnt_lang_code), {})
        self.cnt_font_table = font_table
        from cocosui import ccs
        reader = ccs.GUIReader.getInstance()
        for org_font, target_font in six.iteritems(font_table):
            reader.setFontAlias(org_font, target_font)

    def reset_lang_data(self):
        self.text_dict = {}
        self.cnt_lang_code = 0
        self.cnt_lang_name = 'cn'
        self.cnt_font_table = {}

    def get_local_language(self):
        from patch import patch_dctool
        dctool_instance = patch_dctool.get_dctool_instane()
        if dctool_instance.is_mainland_package():
            return lang_data.LANG_CN
        else:
            local_lang = int(get_local_language())
            if local_lang is None:
                return lang_data.LANG_EN
            return local_lang
            return lang_data.LANG_EN

    def get_multi_lang_font_name(self, font_name):
        try:
            if self.cnt_font_table and font_name in self.cnt_font_table:
                return self.cnt_font_table[font_name]
            return font_name
        except Exception as e:
            print('patch lang get font exception:', str(e))
            return font_name

    def read_lang_conf(self):
        _path = os.path.join(game3d.get_doc_dir(), LANG_CONF)
        import social
        channel = social.get_channel()
        if channel and channel.name and channel.name == 'steam':
            steam_language_path = os.path.join(game3d.get_doc_dir(), 'steam_language')
            steam_lang = None
            try:
                f = open(steam_language_path, 'r')
                s = f.read()
                f.close()
                steam_lang = str(s)
            except:
                pass

            if not steam_lang or steam_lang != STEAM_UI_LANGUAGE:
                try:
                    f = open(steam_language_path, 'w+')
                    f.write(str(STEAM_UI_LANGUAGE))
                    f.close()
                except:
                    pass

                lang_code = lang_data.languagename_2_code.get(STEAM_UI_LANGUAGE)
                lang_code = lang_code if lang_code != None else lang_data.LANG_EN
                try:
                    f = open(_path, 'w+')
                    f.write(str(lang_code))
                    f.close()
                except:
                    pass

                return lang_code
        try:
            f = open(_path, 'r')
            s = f.read()
            f.close()
            lang = int(s)
        except:
            lang = self.get_local_language()
            print('local lang is', lang)

        return lang

    def init_cnt_lang(self):
        self.reset_lang_data()
        try:
            self.cnt_lang_code = self.read_lang_conf()
            self.cnt_lang_name = lang_data.code_2_shorthand.get(self.cnt_lang_code, 'cn')
            self.init_font()
        except:
            self.reset_lang_data()