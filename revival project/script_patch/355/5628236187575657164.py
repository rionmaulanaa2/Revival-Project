# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/login/CharacterInfoUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from logic.comsys.common_ui.InputBox import InputBox
from common.utils.cocos_utils import ccp
from logic.gcommon.const import SEX_MALE, SEX_FEMALE
CHARACTER_INFO = {SEX_MALE: {'name': '\xe5\xbc\x97\xe6\xb4\x9b\xe5\xa7\x86',
              'gender_icon': 'gui/ui_res_2/icon/icon_male.png',
              'nation': '\xe8\x8b\xb1\xe5\x9b\xbd',
              'age': '28',
              'height': '180cm',
              'identity': '\xe6\xb1\xbd\xe8\xbd\xa6\xe6\x8a\x80\xe5\xb7\xa5',
              'cv': '\xe6\x94\xbe\xe5\xad\xa6\xe7\xad\x89\xe6\x88\x91',
              'anchor': (1, 1),
              'offset': (-50, -50),
              'ani': 'p1_appear'
              },
   SEX_FEMALE: {'name': '\xe5\xae\x81\xe5\xae\x81',
                'gender_icon': 'gui/ui_res_2/icon/icon_female.png',
                'nation': '\xe6\x97\xa5\xe6\x9c\xac',
                'age': '19',
                'height': '165cm',
                'identity': '\xe5\xad\xa6\xe7\x94\x9f\xe4\xbc\x9a\xe9\x95\xbf',
                'cv': '\xe6\x94\xbe\xe5\xad\xa6\xe7\xad\x89\xe4\xbd\xa0',
                'anchor': (0, 0),
                'offset': (50, 0),
                'ani': 'p2_appear'
                }
   }
from common.const import uiconst

class CharacterInfoUI(BasePanel):
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    PANEL_CONFIG_NAME = 'create/role_info'
    UI_ACTION_EVENT = {'btn_back.OnClick': 'on_click_btn_back',
       'btn_random.OnClick': 'on_click_btn_random',
       'btn_create.OnClick': 'on_click_btn_create'
       }

    def on_init_panel(self, **kwargs):
        pass

    def update_character_info(self, sex, screen_position):
        info = CHARACTER_INFO.get(sex, CHARACTER_INFO[SEX_FEMALE])
        self.panel.lab_name.SetString(info['name'])
        self.panel.lab_age.SetString(info['age'])
        self.panel.lab_tall.SetString(info['height'])
        self.panel.img_sex.SetDisplayFrameByPath('', info['gender_icon'])
        x = screen_position[0] + info['offset'][0]
        y = screen_position[1] + info['offset'][1]
        self.panel.setPosition(ccp(x, y))
        self.panel.PlayAnimation(info['ani'])
        self.panel.setAnchorPoint(ccp(*info['anchor']))