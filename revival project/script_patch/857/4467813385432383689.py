# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impSurvey.py
from __future__ import absolute_import
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import Str, Int, Dict, List
from common.cfg import confmgr

class impSurvey(object):

    def _init_survey_from_dict(self, bdict):
        self._mp_survey = bdict.get('survey', {})
        self._finished_activity_surverys = bdict.get('finished_activity_surverys', [])
        self._last_mode_satisfaction_survey_record = None
        self._pending_survey = []
        return

    def get_survey_info(self):
        return self._mp_survey

    def has_finished_activity_survey(self, survey_id):
        return survey_id in self._finished_activity_surverys

    def do_pending_survey(self):
        if not self._pending_survey:
            return
        survey_id, battle_context_info = self._pending_survey.pop(0)
        survey_conf = confmgr.get('custom_survey_config', 'SurveyConfig', 'Content')
        ui_class = survey_conf.get(str(survey_id), {}).get('ui_class')
        if ui_class == 'SatisfactionSurveyUI':
            from logic.comsys.survey.SatisfactionSurveyUI import SatisfactionSurveyUI
            SatisfactionSurveyUI(survey_id=survey_id, context_info=battle_context_info)

    @rpc_method(CLIENT_STUB, (Int('ret_code'), Str('c_survey_id')))
    def on_finish_survey_ret(self, ret_code, c_survey_id):
        if ret_code >= 0 and 'cSurveyID' in self._mp_survey and c_survey_id == self._mp_survey.get('cSurveyID'):
            self._mp_survey.pop('cSurveyID')
            global_data.emgr.on_finish_survey.emit()

    def do_commit_survey_finish(self, c_survey_id):
        self.call_server_method('finish_survey', (str(c_survey_id),))

    @rpc_method(CLIENT_STUB, (Dict('mp_survey'),))
    def update_survey(self, mp_survey):
        self._mp_survey = mp_survey
        global_data.emgr.avatar_survey_update.emit()

    @rpc_method(CLIENT_STUB, (List('finished_activity_surverys'),))
    def update_activity_finished_survey(self, finished_activity_surverys):
        if self._finished_activity_surverys != finished_activity_surverys:
            self._finished_activity_surverys = finished_activity_surverys
            global_data.emgr.refresh_activity_list.emit()

    @rpc_method(CLIENT_STUB, (Int('survey_id'), Dict('battle_context_info')))
    def add_custom_survey(self, survey_id, battle_context_info):
        self._pending_survey.append((survey_id, battle_context_info))

    def commit_custom_survey(self, survey_id, answer_data, battle_context_info):
        self.call_server_method('commit_custom_survey', (survey_id, answer_data, battle_context_info))

    def set_last_mode_sat_survey_record(self, battle_context_info):
        self._last_mode_satisfaction_survey_record = dict(battle_context_info)
        global_data.emgr.on_mode_sat_survey_setted_event.emit()

    def is_committed_mode_sat_survey(self, battle_context_info):
        return self._last_mode_satisfaction_survey_record == battle_context_info