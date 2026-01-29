# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/cdata/competition_def.py
_reload_all = True
data = {1: {'promotion_pic_path': 'gui/ui_res_2/live/img_bar_match.png',
       'cMatchName': 860208,
       'cTag': 860209
       },
   2: {'promotion_pic_path': 'gui/ui_res_2/live/img_bar_match.png',
       'cMatchName': 860208,
       'cTag': 860209
       },
   3: {'promotion_pic_path': 'gui/ui_res_2/live/img_bar_match.png',
       'cMatchName': 860208,
       'cPromotionPicIcon': {'icon': 'gui/ui_res_2/rank/badge/badge_32000000.png','scale': 0.3,'pos': ['50%-101', '50%134']},'cTag': 860209
       },
   4: {'promotion_pic_path': 'gui/ui_res_2/live/img_bar_match_summer.png',
       'cMatchName': 860208,
       'cTag': 860209
       },
   -1: {'promotion_pic_path': 'gui/ui_res_2/live/img_bar_match_summer.png',
        'cMatchName': 860208,
        'cTag': 860209
        }
   }
import six

def get_competition_region_list():
    return six.iterkeys(data)


def get_promotion_pic_path(competition_id):
    return data.get(competition_id, {}).get('promotion_pic_path', None)


def get_competition_conf(competition_id):
    return data.get(competition_id, {})