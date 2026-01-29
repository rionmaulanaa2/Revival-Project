# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/entities/avatarmembers/impMail.py
from __future__ import absolute_import
import six
from mobile.common.RpcMethodArgs import Str, Dict, Int, List
from mobile.common.rpcdecorator import rpc_method, CLIENT_STUB

class impMail(object):

    def _init_mail_from_dict(self, bdict):
        pass

    def req_sys_email(self, last_email_id, local_email_scope):
        self.call_server_method('get_mails', (last_email_id, False))

    def req_del_email(self, email_id):
        self.call_server_method('del_mail', (email_id,))

    def req_del_more_mail(self, mail_ids):
        self.call_server_method('del_more_mail', (mail_ids,))

    def req_read_more_mail(self, mail_ids):
        self.call_server_method('req_read_more_mail', (mail_ids,))

    def req_get_reward(self, email_ids):
        self.call_server_method('req_get_reward', (email_ids,))

    @rpc_method(CLIENT_STUB, (Dict('mails'),))
    def on_sys_email(self, mails):
        global_data.message_data.set_sys_email(mails)

    @rpc_method(CLIENT_STUB, (List('mail_ids'),))
    def on_del_email(self, mail_ids):
        global_data.message_data.del_sys_email(mail_ids)

    @rpc_method(CLIENT_STUB, (List('claimed_mails'),))
    def on_get_attachment(self, claimed_mails):
        global_data.message_data.email_get_reward(claimed_mails, 1)

    @rpc_method(CLIENT_STUB, (Dict('result'),))
    def on_get_more_attachment(self, result):
        mail_ids = []
        for mail_id, info in six.iteritems(result):
            reward_dict, result = info
            if result == 1:
                self.offer_reward_imp(reward_dict, 'MAIL')
                mail_ids.append(mail_id)

        if mail_ids:
            global_data.message_data.email_get_reward(mail_ids, 1)

    @rpc_method(CLIENT_STUB, (Int('max_mail_id'), Dict('mails_state')))
    def on_update_email_state(self, max_mail_id, mails_state):
        global_data.message_data.update_email_state(max_mail_id, mails_state)