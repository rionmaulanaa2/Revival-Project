# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/survey/SatisfactionSurveyUI.py
from __future__ import absolute_import
import six
from common.cfg import confmgr
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER_2
from logic.gcommon.common_utils.local_text import get_text_by_id
from common.const import uiconst

class SatisfactionSurveyUI(BasePanel):
    PANEL_CONFIG_NAME = 'common/satisfaction_survey'
    DLG_ZORDER = NORMAL_LAYER_ZORDER_2
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT
    IS_FULLSCREEN = True
    UI_ACTION_EVENT = {}
    GLOBAL_EVENT = {'net_disconnect_event': 'close',
       'net_reconnect_event': 'close',
       'net_login_reconnect_event': 'close'
       }

    def on_init_panel(self, survey_id, context_info):
        self._survey_id = str(survey_id)
        self._battle_context_info = context_info
        self._question_id = 0
        self._options = []
        self.init_widget()

    def on_finalize_panel(self):
        pass

    def commit_answer(self, selected_id):
        answer_data = {'question': get_text_by_id(self._question_id),
           'options': self._options,
           'selected': get_text_by_id(selected_id)
           }
        answer_data = self.get_commit_result_text(answer_data)
        global_data.player.commit_custom_survey(self._survey_id, answer_data, self._battle_context_info)

    def get_commit_result_text(self, answer_data):
        formatted_result = {}
        for question_name, answer_text in six.iteritems(answer_data):
            if not answer_text:
                continue
            if type(answer_text) is list:
                formatted_result[question_name] = [ six.ensure_str(text) for text in answer_text if text ]
            else:
                formatted_result[question_name] = six.ensure_str(answer_text)

        return formatted_result

    def init_widget(self):
        survey_conf = confmgr.get('custom_survey_config', 'SurveyConfig', 'Content', self._survey_id)
        questions = survey_conf['questions'][0]
        self._question_id = questions['title_text_id']
        self.panel.lab_content.SetString(self._question_id)
        btns = [
         self.panel.bth_yes, self.panel.btn_no, self.panel.btn_skip]
        for i, btn in enumerate(btns):
            text_id = questions['options'][i]['text_id']
            self._options.append(get_text_by_id(text_id))

            @btn.unique_callback()
            def OnClick(b, touch, text_id=text_id):
                self.close()
                self.commit_answer(text_id)

            btn.SetText(text_id)