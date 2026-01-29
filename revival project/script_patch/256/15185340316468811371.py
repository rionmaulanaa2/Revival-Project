# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/common_utils/local_text.py
from __future__ import absolute_import
import six_ex
import six
import six.moves.cPickle
import json
from logic.gcommon.common_const.lang_data import *
from logic.gcommon.common_const.voice_lang_data import VOICE_JA
TEXT_PATH_PATTERN = 'text/{}/'
TEXT_PATH_DEFAULT = TEXT_PATH_PATTERN.format(TEXT_PATH_DICT[LANG_CN])
NAME_PATH_DEFAULT = NAME_PATH_DICT[LANG_CN]
LANG_CODE = 'cn'
CUR_TEXT_PATH = TEXT_PATH_DEFAULT
CUR_NAME_PATH = NAME_PATH_DEFAULT
CUR_LANG_CODE = 'cn'
G_TEXT_FOR_PATCH_UI = {}
G_TEXT_LANG = LANG_CN
G_VOICE_LANG = VOICE_JA
G_PIC_TEXT_LANG = LANG_CN
G_EXTRA_VERTICAL_SPACE = 0
G_ENABLE_DEFAULT_LINEBREAK = True
G_FORCE_FONT_TRANS = False
CHINESE_LANGS = (
 LANG_CN, LANG_ZHTW)

class LangShrinkConfig(object):

    def __init__(self, iFontSzOffset, bEnableShrink, iMinFontSz):
        self.iFontSzOffset = iFontSzOffset
        self.bEnableShrink = True if bEnableShrink else False
        self.iMinFontSize = iMinFontSz

    def set_lang(self, lang):
        from common.cfg import confmgr
        shrink_conf = confmgr.get('c_font_shrink_conf', str(lang), default={})
        self.iFontSzOffset = shrink_conf.get('iFontOffset', 0)
        self.bEnableShrink = True if shrink_conf.get('iEnableShrink', 0) else False
        self.iMinFontSize = shrink_conf.get('iMinFontSize', 10)


CUR_LANG_SHRINK_CONF = LangShrinkConfig(0, 0, 10)

def get_item_name_by_type(itemtype):
    from ...gutils import item_utils
    try:
        itemtype = int(itemtype)
    except:
        return '(itemtype \xe9\x94\x99\xe8\xaf\xaf\xef\xbc\x8c\xe8\xaf\xb7\xe4\xbd\xbf\xe7\x94\xa8item id)'

    item_name = item_utils.get_item_name(itemtype)
    if not item_name:
        item_name = item_utils.get_lobby_item_name(itemtype)
    return item_name


def get_capsule_name_by_id(cap_id):
    from ...gutils import item_utils
    try:
        cap_id = int(cap_id)
    except:
        return '(capsule id \xe9\x94\x99\xe8\xaf\xaf)'

    return item_utils.get_capsule_name(cap_id)


def get_buidling_name_by_no(building_no):
    from ...gutils import item_utils
    try:
        building_no = int(building_no)
    except:
        return '(building no. \xe9\x94\x99\xe8\xaf\xaf)'

    return item_utils.get_building_name(building_no)


def get_activity_name_by_id(text_id):
    return get_text_by_id(text_id)


def get_dan_name_by_id(dan_id):
    from logic.gcommon.cdata import dan_data
    text_id = dan_data.get_dan_name_id(dan_id)
    return get_text_by_id(text_id)


def get_dan_lv_by_id(lv):
    from common import utilities
    return utilities.get_rome_num(lv)


def get_battle_name_by_id(battle_type):
    from common.cfg import confmgr
    battle_config = confmgr.get('battle_config', str(battle_type), default={})
    if not battle_config:
        return ''
    iMapID = battle_config.get('iMapID')
    map_config = confmgr.get('map_config', iMapID, default={})
    map_mode_text_id = map_config.get('nameTID')
    return get_text_by_id(map_mode_text_id)


def get_mode_text_by_id(battle_type):
    from common.cfg import confmgr
    battle_config = confmgr.get('battle_config', str(battle_type), default={})
    if not battle_config:
        return ''
    iMapID = battle_config.get('iMapID')
    map_config = confmgr.get('map_config', iMapID, default={})
    map_mode_text_id = map_config.get('cMapModeTextId')
    return get_text_by_id(map_mode_text_id)


def get_mecha_name_by_id(mecha_type):
    from ...gutils import item_utils
    return item_utils.get_mecha_name_by_id(mecha_type)


def get_inner_text_by_id(text_id):
    return get_text_by_id(text_id)


def get_pve_chapter_name(chapter):
    from common.cfg import confmgr
    conf = confmgr.get('pve_level_conf', 'ChapterConf', 'Content', str(chapter))
    chapter_str = get_text_by_id(conf.get('title_text'))
    return chapter_str


def get_pve_chapter_title(chapter):
    from common.cfg import confmgr
    conf = confmgr.get('pve_level_conf', 'ChapterConf', 'Content', str(chapter))
    sub_level_str = get_text_by_id(conf.get('sub_title_text'))
    return sub_level_str


def get_pve_refresh_type(refresh_type):
    from logic.gcommon.common_const import rank_const
    if int(refresh_type) == rank_const.SEASON_REFRESH:
        return get_text_by_id(635371)
    else:
        return get_text_by_id(635372)


def get_pve_difficulty(difficulty):
    from logic.gcommon.common_const.pve_const import DIFFICULTY_TEXT_LIST
    difficulty_str = get_text_by_id(DIFFICULTY_TEXT_LIST[int(difficulty)])
    return difficulty_str


def get_pve_titles(pve_titles):
    contents = []
    try:
        for rank_type, title_data in six.iteritems(pve_titles):
            rank, expire_time = title_data
            rank_str = get_text_by_id(635421).format(rank=rank)
            chapter, difficulty, refresh_type, mecha_id = rank_type.split('_')
            if int(mecha_id) > 0:
                contents.append(get_pve_chapter_name(chapter) + get_mecha_name_by_id(mecha_id) + rank_str)
            else:
                contents.append(get_pve_chapter_name(chapter) + get_pve_refresh_type(refresh_type) + rank_str)

        if contents:
            contents_str = '\n'.join(contents)
        else:
            contents_str = ''
    except:
        contents_str = ''

    return contents_str


def get_pve_rank_titles(pve_titles):
    title_text = [
     635606, 635599, 83512, 635600]
    contents = []
    for rank_type, title_data in six.iteritems(pve_titles):
        rank, expire_time = title_data
        player_size = 1
        split_ret = rank_type.split('_')
        if len(split_ret) == 4:
            chapter, difficulty, refresh_type, mecha_id = split_ret
        else:
            chapter, difficulty, refresh_type, mecha_id, player_size = split_ret
        data_1 = get_pve_chapter_name(chapter)
        data_2 = str(player_size)
        data_3 = get_pve_difficulty(difficulty)
        data_4 = str(rank)
        contents.extend([data_1, data_2, data_3, data_4])

    text = '<node=2>show_pve_rank_list_imp:titles=%s@#@contents=%s</node>' % (json.dumps(title_text), json.dumps(contents))
    return text


def get_pve_mecha_rank_titles(pve_titles):
    title_text = [
     635606, 635404, 635600]
    contents = []
    for rank_type, title_data in six.iteritems(pve_titles):
        rank, expire_time = title_data
        chapter, difficulty, refresh_type, mecha_id = rank_type.split('_')
        data_1 = get_pve_chapter_name(chapter)
        data_3 = get_mecha_name_by_id(mecha_id)
        data_4 = str(rank)
        contents.extend([data_1, data_3, data_4])

    text = '<node=2>show_pve_mecha_rank_list_imp:titles=%s@#@contents=%s</node>' % (json.dumps(title_text), json.dumps(contents))
    return text


def get_mecha_region_titles(titles):
    from logic.gcommon.common_const import rank_region_const
    from logic.gcommon.common_const import rank_const
    text = ''
    title_texts = [
     634692, 634697]
    contents = []
    if rank_const.is_world_mecha_region_rank():
        for mecha_type, title_data in six.iteritems(titles):
            if not title_data:
                continue
            mecha_name = get_mecha_name_by_id(mecha_type)
            rank = title_data.get(rank_region_const.REGION_RANK_TYPE_PROVINCE, '*')
            contents.extend([mecha_name, str(rank)])

    else:
        title_texts = [
         634692, 634693, 634694, 634695]
        for mecha_type, title_data in six.iteritems(titles):
            if not title_data:
                continue
            mecha_name = get_mecha_name_by_id(mecha_type)
            rank_1 = title_data.get(rank_region_const.REGION_RANK_TYPE_CITY, '*')
            rank_2 = title_data.get(rank_region_const.REGION_RANK_TYPE_PROVINCE, '*')
            rank_3 = title_data.get(rank_region_const.REGION_RANK_TYPE_COUNTRY, '*')
            mecha_contents = [mecha_name, str(rank_1), str(rank_2), str(rank_3)]
            contents.extend(mecha_contents)

    text = '<node=1>show_rank_list:titles=%s@#@contents=%s</node>' % (json.dumps(title_texts), json.dumps(contents))
    return text


def get_assault_rank_titles(titles):
    from logic.gcommon.common_const import rank_const
    title_texts = [
     634692, 18363, 18364, 18365, 18366]
    contents = []
    for mecha_type, title_data in six.iteritems(titles):
        if not title_data:
            continue
        mecha_name = get_mecha_name_by_id(mecha_type)
        data_1 = '%.2f' % title_data.get(rank_const.SCORE_PER_MINUTE, 0)
        data_2 = '%.2f' % title_data.get(rank_const.ASSIST_PER_MINUTE, 0)
        data_3 = int(title_data.get(rank_const.DAMAGE_PER_MINUTE, 0))
        data_4 = int(title_data.get(rank_const.HURT_PER_MINUTE, 0))
        mecha_contents = [mecha_name, str(data_1), str(data_2), str(data_3), str(data_4)]
        contents.extend(mecha_contents)

    text = '<node=2>show_assault_rank_list:titles=%s@#@contents=%s</node>' % (json.dumps(title_texts), json.dumps(contents))
    return text


def get_mecha_score_settlement(data):
    text = ''
    for mecha_type, (old_score, new_score) in six.iteritems(data):
        mecha_name = get_mecha_name_by_id(mecha_type)
        text += get_text_by_id(11180, {'mecha_name': mecha_name,'score_last': old_score,'score_new': new_score})

    return text


def get_veteran_item(data):
    text = ''
    for item_no in data:
        text += get_item_name_by_type(item_no) + ', '

    return text


def get_match_name(match_adcode_rank):
    from common.cfg import confmgr
    from logic.gcommon.cdata import match_adcode_data
    match_adcode, match_rank = match_adcode_rank
    if match_adcode not in match_adcode_data.data:
        title = ''
    else:
        title = get_text_by_id(int(match_adcode))
    rank_text = ''
    try:
        from common import utilities
        cRankMap = confmgr.get('match_adcode_data', str(match_adcode), 'cRankMap', default={})
        if not cRankMap:
            rank_text = '{}{}'.format(get_text_by_id(860131), utilities.get_ch_num(match_rank))
        elif str(match_rank) in cRankMap:
            rank_text = get_text_by_id(cRankMap[str(match_rank)])
        elif cRankMap.get('default'):
            rank_text = get_text_by_id(cRankMap.get('default'), {'rank': match_rank})
        else:
            rank_text = '{}{}'.format(get_text_by_id(860131), utilities.get_ch_num(match_rank))
    except:
        pass

    rank_text_is_whole = confmgr.get('match_adcode_data', str(match_adcode), 'cRankMap', 'title_is_whole', default=False)
    if not rank_text_is_whole:
        return title + rank_text
    else:
        return rank_text


def get_charm_rank_title(charm_rank_data):
    title_text, rank = charm_rank_data
    return get_text_by_id(int(title_text)).format(rank=rank)


def get_province_name(province_id):
    if isinstance(province_id, int):
        return get_text_by_id(province_id)
    else:
        return province_id


SPECIAL_KEY = {'itemtype': get_item_name_by_type,
   'itemname': get_item_name_by_type,
   'rewardname': get_item_name_by_type,
   'capsule': get_capsule_name_by_id,
   'building': get_buidling_name_by_no,
   'activityname': get_activity_name_by_id,
   'dan': get_dan_name_by_id,
   'dan_lv': get_dan_lv_by_id,
   'other_dan': get_dan_name_by_id,
   'other_dan_lv': get_dan_lv_by_id,
   'battle_name': get_battle_name_by_id,
   'mecha_region_titles': get_mecha_region_titles,
   'assault_rank_titles': get_assault_rank_titles,
   'mecha_scores': get_mecha_score_settlement,
   'veteran_item': get_veteran_item,
   'match_adcode_rank': get_match_name,
   'province': get_province_name,
   'charm_rank_title': get_charm_rank_title,
   'mechaname': get_mecha_name_by_id,
   'inner_text_id': get_inner_text_by_id,
   'nileitemname': get_inner_text_by_id,
   'bless': get_inner_text_by_id,
   'bless0': get_inner_text_by_id,
   'bless1': get_inner_text_by_id,
   'pve_chapter_name': get_pve_chapter_name,
   'pve_chapter_title': get_pve_chapter_title,
   'pve_refresh_type': get_pve_refresh_type,
   'pve_difficulty': get_pve_difficulty,
   'pve_titles': get_pve_rank_titles,
   'pve_mecha_titles': get_pve_mecha_rank_titles
   }

def set_text_lang(lang):
    global CUR_LANG_CODE
    global G_TEXT_LANG
    global CUR_TEXT_PATH
    global G_FORCE_FONT_TRANS
    global G_EXTRA_VERTICAL_SPACE
    global G_ENABLE_DEFAULT_LINEBREAK
    G_TEXT_LANG = lang
    CUR_TEXT_PATH = TEXT_PATH_PATTERN.format(TEXT_PATH_DICT[lang])
    CUR_LANG_CODE = code_2_shorthand.get(int(lang), 'cn')
    if global_data.channel:
        sdk_short_hand = code_2_sdk.get(int(lang), 'EN')
        global_data.channel.set_prop_str('LANGUAGE_CODE', sdk_short_hand)
        global_data.channel.extend_func('{"methodId":"setLanguage"}')
        if global_data.channel.get_app_channel() == 'netease_global' and global_data.deviceinfo.get_os_name() == 'windows' and hasattr(global_data.channel, 'mpay_set_option'):
            mpay_short_hand = code_2_mpay.get(int(lang), 'EN-US')
            global_data.channel.mpay_set_option('mpay_option_set_language', mpay_short_hand)
    if global_data.player:
        global_data.player.notify_text_lang(G_TEXT_LANG)
    from common.uisys.font_utils import SetFontTableLang, SetFontFaceTableLang
    SetFontTableLang(lang)
    SetFontFaceTableLang(lang)
    CUR_LANG_SHRINK_CONF.set_lang(lang)
    from common.platform.device_info import DeviceInfo
    DeviceInfo().on_lang_changed()
    if global_data.player:
        global_data.player.get_custom_service_token()
        global_data.player.request_share_url()
    set_cur_pic_lang_name(PIC_LANG_PATH_DICT.get(G_TEXT_LANG, LANG_CN))
    from common.cfg import confmgr
    conf = confmgr.get('lang_conf', str(G_TEXT_LANG), default={})
    G_EXTRA_VERTICAL_SPACE = conf.get('iExtraVerticalSpace', 0)
    G_ENABLE_DEFAULT_LINEBREAK = bool(conf.get('bDefLineBreak', 1))
    if G_TEXT_LANG == LANG_TH:
        if global_data.feature_mgr and global_data.feature_mgr.is_support_boundary_word():
            G_ENABLE_DEFAULT_LINEBREAK = True
    G_FORCE_FONT_TRANS = bool(conf.get('bForceFontTrans', 0))
    if global_data.nile_sdk:
        global_data.nile_sdk.on_lang_changed()


def set_voice_lang(voice_lang):
    global G_VOICE_LANG
    G_VOICE_LANG = voice_lang


def get_cur_text_lang():
    return G_TEXT_LANG


def get_cur_text_lang_shorthand(default='en'):
    return code_2_shorthand.get(G_TEXT_LANG, default)


def get_cur_voice_lang():
    return G_VOICE_LANG


def get_default_lang_name():
    if G_IS_NA_USER:
        return 'en'
    else:
        return 'cn'


def get_cur_lang_name():
    return CUR_LANG_CODE


def set_cur_pic_lang_name(new_pic_text_lang):
    global G_PIC_TEXT_LANG
    G_PIC_TEXT_LANG = new_pic_text_lang


def get_cur_pic_lang_name():
    return G_PIC_TEXT_LANG


def get_extra_vertical_space():
    return G_EXTRA_VERTICAL_SPACE


def get_enable_def_linebreak():
    return G_ENABLE_DEFAULT_LINEBREAK


def get_force_font_trans():
    return G_FORCE_FONT_TRANS


def get_cur_name_path():
    from common.platform.dctool import interface
    if interface.is_global_package():
        return NAME_PATH_DICT[LANG_EN]
    if interface.is_tw_package():
        return NAME_PATH_DICT[LANG_EN]
    if interface.is_mainland_package():
        return NAME_PATH_DICT[LANG_CN]
    return NAME_PATH_DEFAULT


def get_cur_lang_shrink_setting():
    return CUR_LANG_SHRINK_CONF


def get_lang_shrink_font_size(old_font_sz):
    if old_font_sz <= CUR_LANG_SHRINK_CONF.iMinFontSize:
        return old_font_sz
    return max(old_font_sz + CUR_LANG_SHRINK_CONF.iFontSzOffset, CUR_LANG_SHRINK_CONF.iMinFontSize)


def get_text_local_content(tid, page=None):
    from common.cfg import confmgr
    if not tid:
        return ''
    else:
        text = None
        page_path = CUR_TEXT_PATH + 'text_' + str(int(tid) // 10000)
        text = confmgr.get(page_path, str(tid), default=None)
        if text is None:
            page_path = 'text/lang_{}'.format(TEXT_PATH_DICT[G_TEXT_LANG])
            text = confmgr.get(page_path, str(tid), default=None)
        if text:
            return text
        return '\xe6\x96\x87\xe6\x9c\xac\xe8\xa1\xa8{0}\xe6\x9c\xaa\xe5\xa1\xab\xe5\x86\x99\xef\xbc\x8c\xe8\xaf\xb7\xe5\xa1\xab\xe8\xa1\xa8'.format(tid)
        return


def get_text_local_content_ex(tid, page=None, lang=None):
    from common.cfg import confmgr
    if not tid:
        return ''
    else:
        lang = lang if lang is not None else G_TEXT_LANG
        text = None
        cur_text_path = TEXT_PATH_PATTERN.format(TEXT_PATH_DICT[lang])
        page_path = cur_text_path + 'text_' + str(int(tid) // 10000)
        text = confmgr.get(page_path, str(tid), default=None)
        if text is None:
            page_path = 'text/lang_{}'.format(TEXT_PATH_DICT[lang])
            text = confmgr.get(page_path, str(tid), default=None)
        if text:
            return text
        return '\xe6\x96\x87\xe6\x9c\xac\xe8\xa1\xa8{0}\xe6\x9c\xaa\xe5\xa1\xab\xe5\x86\x99\xef\xbc\x8c\xe8\xaf\xb7\xe5\xa1\xab\xe8\xa1\xa8'.format(tid)
        return


def special_value_change(dict_data):
    for key, value in six_ex.items(dict_data):
        if key in SPECIAL_KEY:
            dict_data[key] = SPECIAL_KEY[key](value)

    return dict_data


def get_text_by_id(tid, args=None):
    text = get_text_local_content(tid)
    arg_type = type(args)
    if arg_type is dict and len(args):
        args = special_value_change(args)
        text = text.format(**args)
    elif arg_type is tuple and len(args):
        text = text.format(*args)
    elif arg_type is list and len(args):
        text = text.format(*args)
    return text


def pack_text(tid, args=None):
    if args is not None:
        try:
            return '^${0}#${1}'.format(tid, json.dumps(args))
        except:
            return '#${0}#${1}'.format(tid, six.moves.cPickle.dumps(args))

    else:
        return '#${0}'.format(tid)
    return


def unpack_text--- This code section failed: ---

 523       0  LOAD_FAST             0  'text'
           3  LOAD_CONST            0  ''
           6  COMPARE_OP            8  'is'
           9  POP_JUMP_IF_FALSE    16  'to 16'

 524      12  LOAD_FAST             0  'text'
          15  RETURN_END_IF    
        16_0  COME_FROM                '9'

 526      16  RETURN_VALUE     
          17  RETURN_VALUE     
          18  RETURN_VALUE     
          19  LOAD_CONST            2  2
          22  SLICE+3          
          23  STORE_FAST            1  'pre_text'

 528      26  LOAD_FAST             1  'pre_text'
          29  LOAD_CONST            3  '^$'
          32  COMPARE_OP            2  '=='
          35  POP_JUMP_IF_FALSE    50  'to 50'

 529      38  LOAD_GLOBAL           1  'json'
          41  LOAD_ATTR             2  'loads'
          44  STORE_FAST            2  'decode'
          47  JUMP_FORWARD         34  'to 84'

 530      50  LOAD_FAST             1  'pre_text'
          53  LOAD_CONST            4  '#$'
          56  COMPARE_OP            2  '=='
          59  POP_JUMP_IF_FALSE    80  'to 80'

 531      62  LOAD_GLOBAL           3  'six'
          65  LOAD_ATTR             4  'moves'
          68  LOAD_ATTR             5  'cPickle'
          71  LOAD_ATTR             2  'loads'
          74  STORE_FAST            2  'decode'
          77  JUMP_FORWARD          4  'to 84'

 533      80  LOAD_FAST             0  'text'
          83  RETURN_VALUE     
        84_0  COME_FROM                '77'
        84_1  COME_FROM                '47'

 535      84  SETUP_EXCEPT         36  'to 123'

 536      87  SETUP_EXCEPT          2  'to 92'
          90  SLICE+1          
          91  LOAD_ATTR             6  'split'
          94  LOAD_CONST            4  '#$'
          97  CALL_FUNCTION_1       1 
         100  STORE_FAST            3  'text_args'

 537     103  LOAD_GLOBAL           7  'int'
         106  LOAD_FAST             3  'text_args'
         109  LOAD_CONST            1  ''
         112  BINARY_SUBSCR    
         113  CALL_FUNCTION_1       1 
         116  STORE_FAST            4  'tid'
         119  POP_BLOCK        
         120  JUMP_FORWARD          8  'to 131'
       123_0  COME_FROM                '84'

 538     123  POP_TOP          
         124  POP_TOP          
         125  POP_TOP          

 539     126  LOAD_FAST             0  'text'
         129  RETURN_VALUE     
         130  END_FINALLY      
       131_0  COME_FROM                '130'
       131_1  COME_FROM                '120'

 541     131  LOAD_CONST            0  ''
         134  STORE_FAST            5  'args'

 543     137  LOAD_GLOBAL           8  'len'
         140  LOAD_FAST             3  'text_args'
         143  CALL_FUNCTION_1       1 
         146  LOAD_CONST            2  2
         149  COMPARE_OP            5  '>='
         152  POP_JUMP_IF_FALSE   194  'to 194'

 544     155  SETUP_EXCEPT         26  'to 184'

 545     158  LOAD_FAST             2  'decode'
         161  LOAD_GLOBAL           9  'str'
         164  LOAD_FAST             3  'text_args'
         167  LOAD_CONST            5  1
         170  BINARY_SUBSCR    
         171  CALL_FUNCTION_1       1 
         174  CALL_FUNCTION_1       1 
         177  STORE_FAST            5  'args'
         180  POP_BLOCK        
         181  JUMP_ABSOLUTE       194  'to 194'
       184_0  COME_FROM                '155'

 546     184  POP_TOP          
         185  POP_TOP          
         186  POP_TOP          

 547     187  JUMP_ABSOLUTE       194  'to 194'
         190  END_FINALLY      
       191_0  COME_FROM                '190'
         191  JUMP_FORWARD          0  'to 194'
       194_0  COME_FROM                '191'

 549     194  LOAD_GLOBAL          10  'get_text_by_id'
         197  LOAD_FAST             4  'tid'
         200  LOAD_FAST             5  'args'
         203  CALL_FUNCTION_2       2 
         206  STORE_FAST            6  'text_content'

 551     209  LOAD_FAST             6  'text_content'
         212  RETURN_VALUE     

Parse error at or near `RETURN_VALUE' instruction at offset 16


def unpack_text_data--- This code section failed: ---

 555       0  LOAD_FAST             0  'text'
           3  LOAD_CONST            0  ''
           6  COMPARE_OP            8  'is'
           9  POP_JUMP_IF_FALSE    22  'to 22'

 556      12  LOAD_FAST             0  'text'
          15  LOAD_CONST            0  ''
          18  BUILD_TUPLE_2         2 
          21  RETURN_END_IF    
        22_0  COME_FROM                '9'

 558      22  RETURN_VALUE     
          23  RETURN_VALUE     
          24  RETURN_VALUE     
          25  LOAD_CONST            2  2
          28  SLICE+3          
          29  STORE_FAST            1  'pre_text'

 560      32  LOAD_FAST             1  'pre_text'
          35  LOAD_CONST            3  '^$'
          38  COMPARE_OP            2  '=='
          41  POP_JUMP_IF_FALSE    56  'to 56'

 561      44  LOAD_GLOBAL           1  'json'
          47  LOAD_ATTR             2  'loads'
          50  STORE_FAST            2  'decode'
          53  JUMP_FORWARD         40  'to 96'

 562      56  LOAD_FAST             1  'pre_text'
          59  LOAD_CONST            4  '#$'
          62  COMPARE_OP            2  '=='
          65  POP_JUMP_IF_FALSE    86  'to 86'

 563      68  LOAD_GLOBAL           3  'six'
          71  LOAD_ATTR             4  'moves'
          74  LOAD_ATTR             5  'cPickle'
          77  LOAD_ATTR             2  'loads'
          80  STORE_FAST            2  'decode'
          83  JUMP_FORWARD         10  'to 96'

 565      86  LOAD_FAST             0  'text'
          89  LOAD_CONST            0  ''
          92  BUILD_TUPLE_2         2 
          95  RETURN_VALUE     
        96_0  COME_FROM                '83'
        96_1  COME_FROM                '53'

 567      96  SETUP_EXCEPT         36  'to 135'

 568      99  SETUP_EXCEPT          2  'to 104'
         102  SLICE+1          
         103  LOAD_ATTR             6  'split'
         106  LOAD_CONST            4  '#$'
         109  CALL_FUNCTION_1       1 
         112  STORE_FAST            3  'text_args'

 569     115  LOAD_GLOBAL           7  'int'
         118  LOAD_FAST             3  'text_args'
         121  LOAD_CONST            1  ''
         124  BINARY_SUBSCR    
         125  CALL_FUNCTION_1       1 
         128  STORE_FAST            4  'tid'
         131  POP_BLOCK        
         132  JUMP_FORWARD         14  'to 149'
       135_0  COME_FROM                '96'

 570     135  POP_TOP          
         136  POP_TOP          
         137  POP_TOP          

 571     138  LOAD_FAST             0  'text'
         141  LOAD_CONST            0  ''
         144  BUILD_TUPLE_2         2 
         147  RETURN_VALUE     
         148  END_FINALLY      
       149_0  COME_FROM                '148'
       149_1  COME_FROM                '132'

 573     149  LOAD_CONST            0  ''
         152  STORE_FAST            5  'args'

 575     155  LOAD_GLOBAL           8  'len'
         158  LOAD_FAST             3  'text_args'
         161  CALL_FUNCTION_1       1 
         164  LOAD_CONST            2  2
         167  COMPARE_OP            5  '>='
         170  POP_JUMP_IF_FALSE   212  'to 212'

 576     173  SETUP_EXCEPT         26  'to 202'

 577     176  LOAD_FAST             2  'decode'
         179  LOAD_GLOBAL           9  'str'
         182  LOAD_FAST             3  'text_args'
         185  LOAD_CONST            5  1
         188  BINARY_SUBSCR    
         189  CALL_FUNCTION_1       1 
         192  CALL_FUNCTION_1       1 
         195  STORE_FAST            5  'args'
         198  POP_BLOCK        
         199  JUMP_ABSOLUTE       212  'to 212'
       202_0  COME_FROM                '173'

 578     202  POP_TOP          
         203  POP_TOP          
         204  POP_TOP          

 579     205  JUMP_ABSOLUTE       212  'to 212'
         208  END_FINALLY      
       209_0  COME_FROM                '208'
         209  JUMP_FORWARD          0  'to 212'
       212_0  COME_FROM                '209'

 581     212  LOAD_FAST             4  'tid'
         215  LOAD_FAST             5  'args'
         218  BUILD_TUPLE_2         2 
         221  RETURN_VALUE     

Parse error at or near `RETURN_VALUE' instruction at offset 22


def get_server_text(data):
    if isinstance(data, dict):
        text = data.get(str(G_TEXT_LANG), None)
        if text is None:
            text = data.get(str(LANG_EN), None)
        if text is None:
            return ''
        return unpack_text(text)
    else:
        return unpack_text(data)
        return


def get_lang_code_by_lang_name(lang_name):
    for code, name in six.iteritems(TEXT_PATH_DICT):
        if name == lang_name:
            return code

    return LANG_EN


def get_pic_lang_path_by_lang(lang):
    return PIC_LANG_PATH_DICT.get(lang, None)