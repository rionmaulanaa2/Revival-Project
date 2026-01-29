# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impQuestion.py
from __future__ import absolute_import
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB
from mobile.common.RpcMethodArgs import List, Dict

class impQuestion(object):

    def _init_question_from_dict(self, bdict):
        self._cur_questions = bdict.get('cur_questions', [])
        self._cur_answers = bdict.get('cur_answers', {})

    def get_cur_question(self):
        return self._cur_questions

    def get_cur_answers(self):
        return self._cur_answers

    @rpc_method(CLIENT_STUB, (List('cur_questions'), Dict('cur_answers')))
    def update_questions(self, cur_questions, cur_answers):
        self._cur_questions = cur_questions
        self._cur_answers = cur_answers
        global_data.emgr.lobby_answering_system_question_updated.emit()

    def commit_answer(self, question_id, answer):
        if question_id not in self._cur_questions:
            return
        if question_id in self._cur_answers:
            return
        self.call_server_method('commit_answer', (question_id, answer))
        self._cur_answers[question_id] = answer