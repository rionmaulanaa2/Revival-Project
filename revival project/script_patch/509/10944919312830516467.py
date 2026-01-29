# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/uisys/font_utils.py
from __future__ import absolute_import
import cc
from data import font_table, font_face_table
from logic.gcommon.common_const.lang_data import LANG_CN, LANG_TH, LANG_KO
from logic.gcommon.common_utils.local_text import get_force_font_trans, get_cur_text_lang
import game3d
import version
cur_font_table = font_table.data.get(str(LANG_CN))
from logic.client.const.version_const import IOS_ENGINE_6_23_VER
cur_font_face_table = font_face_table.data.get(str(LANG_CN))
LOW_MEM_FONT_MAP = {'gui/fonts/fzdys.ttf': 'gui/fonts/fzy4jw.ttf'
   }

def GetLowMemFontName(fontName):
    if global_data.is_low_mem_mode:
        fontName = LOW_MEM_FONT_MAP.get(fontName, fontName)
    return fontName


def GetMultiLangFontName(fontName, fontTrans=True):
    global cur_font_table
    if global_data.is_low_mem_mode:
        fontName = LOW_MEM_FONT_MAP.get(fontName, fontName)
    fontTrans = fontTrans or hasattr(cc, 'FontAtlasFallbackSetting') and cc.FontAtlasFallbackSetting
    if cur_font_table and (fontTrans or get_force_font_trans()):
        return cur_font_table.get(fontName, fontName)
    return fontName


def GetMultiLangFontFaceName(face_name, fontTrans=True):
    global cur_font_face_table
    c_engine_ver = version.get_engine_svn()
    if game3d.get_platform() == game3d.PLATFORM_IOS:
        if get_cur_text_lang() == LANG_TH and c_engine_ver <= IOS_ENGINE_6_23_VER:
            return 'Thonburi'
        if get_cur_text_lang() == LANG_KO:
            return 'Apple SD Gothic Neo'
    if cur_font_face_table and fontTrans:
        return cur_font_face_table.get(face_name, face_name)
    return face_name


def SetFontTableLang(lang_id):
    global cur_font_table
    cur_font_table = font_table.data.get(str(lang_id), {})


def SetFontFaceTableLang(lang_id):
    global cur_font_face_table
    cur_font_face_table = font_face_table.data.get(str(lang_id), {})


def GetFontTableByLang(lang_id):
    return font_table.data.get(str(lang_id), {})