# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/Activity520/Activity520Princess.py
from __future__ import absolute_import
import six
from six.moves import range
import time
from logic.gutils import task_utils
from logic.gutils import activity_utils
from common.cfg import confmgr
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gutils import template_utils
from logic.gcommon.item.item_const import ITEM_UNRECEIVED, ITEM_RECEIVED, ITEM_UNGAIN
from logic.gutils import item_utils
import logic.gcommon.const as gconst
import logic.gcommon.time_utility as tutil
from cocosui import cc, ccui, ccs
from logic.gutils import mall_utils, dress_utils
from logic.comsys.mall_ui.BuyConfirmUIInterface import groceries_buy_confirmUI
from logic.client.const.mall_const import DARK_PRICE_COLOR, DEF_PRICE_COLOR
from logic.gcommon.common_utils.local_text import get_text_by_id

class Activity520Princess(ActivityBase):
    TIMER_TAG = 210512
    TIMEOUT_TAG = 210514

    def __init__(self, dlg, activity_type):
        super(Activity520Princess, self).__init__(dlg, activity_type)
        self.init_parameters()
        self.init_event()
        self.init_skin_list_show()
        self.select_skin_id(self._skin_list[0])
        self.register_timer()
        self.refresh_time()
        self.panel.RecordAnimationNodeState('loop')
        self.panel.RecordAnimationNodeState('show')
        from logic.gutils.activity_utils import has_activity_520_princess_rp
        if has_activity_520_princess_rp():
            from logic.comsys.archive import archive_key_const
            key = archive_key_const.KEY_LAST_OPEN_520_PRINCESS_TIME
            global_data.achi_mgr.save_general_archive_data_value(key, int(tutil.get_server_time()))
            global_data.emgr.refresh_activity_redpoint.emit()

    def on_finalize_panel(self):
        for _, spine_node in six.iteritems(self._spine_node_dict):
            spine_node.setVisible(False)

        self._spine_node_dict = {}
        self._cur_spine = None
        self._cur_spine_node = None
        self.process_event(False)
        return

    def init_parameters(self):
        activity_type = self._activity_type
        self._cur_skin_id = None
        ui_conf = confmgr.get('c_activity_config', str(self._activity_type), 'cUiData', default={})
        self._skin_list = ui_conf.get('skins', [])
        self._skin_img_dict = ui_conf.get('imgs', {})
        self._coupon_item_no = ui_conf.get('coupon', None)
        conf = confmgr.get('c_activity_config', activity_type)
        self._cur_spine = 'gui/ui_res_2/anim_outside/spine/520spine/gongzhu_02'
        self._cur_spine_node = self.panel.vx_spine.gongzhu
        self._spine_node_dict = {self._cur_spine: self._cur_spine_node}
        for skin_id in self._skin_list:
            spine_node = getattr(self.panel.vx_spine, 'gongzhu_%s' % str(skin_id))
            if spine_node:
                self._spine_node_dict.update({str(skin_id): spine_node})

        act_name_id = conf['cNameTextID']
        rule_name_id = conf.get('cRuleTextID', '')

        @self.panel.btn_help.callback()
        def OnClick(btn, touch):
            dlg = global_data.ui_mgr.show_ui('GameRuleDescUI', 'logic.comsys.common_ui')
            dlg.set_show_rule(get_text_by_id(act_name_id), get_text_by_id(rule_name_id))
            x, y = self.panel.btn_help.GetPosition()
            wpos = self.panel.btn_help.GetParent().ConvertToWorldSpace(x, y)
            dlg.panel.nd_game_describe.setAnchorPoint(cc.Vec2(0.0, 1.0))
            template_utils.set_node_position_in_screen(dlg.panel.nd_game_describe, dlg.panel, wpos)

        @self.panel.btn_detail.callback()
        def OnClick(btn, touch):
            skin_id = self._cur_skin_id
            from logic.gutils import jump_to_ui_utils
            jump_to_ui_utils.jump_to_display_detail_by_item_no(int(skin_id), extra_parameter={'role_info_ui': True})

        return

    def init_skin_list_show(self):
        for idx, skin_id in enumerate(self._skin_list):
            btn = getattr(self.panel, 'btn_skin_%s' % (idx + 1))
            if btn:
                skin_name = item_utils.get_lobby_item_name(skin_id)
                btn.SetText(skin_name)

                @btn.callback()
                def OnClick(btn, touch, skin_id=skin_id):
                    self.select_skin_id(skin_id)

    def select_skin_id(self, target_skin_id):
        for idx, skin_id in enumerate(self._skin_list):
            btn = getattr(self.panel, 'btn_skin_%s' % (idx + 1))
            if btn:
                btn.SetSelect(skin_id == target_skin_id)

        self._cur_skin_id = target_skin_id
        self.panel.lab_skin.SetString(item_utils.get_lobby_item_name(target_skin_id))
        goods_id = dress_utils.get_goods_id_of_role_dress_related_item_no(target_skin_id)
        prices = mall_utils.get_mall_item_price(goods_id, pick_list=('yuanbao', ))
        yuanbao_price = None
        if prices:
            yuanbao_price = prices[0]
        self.panel.lab_price_before.SetString(get_text_by_id(608607, {'price': yuanbao_price.get('real_price', 0)}))
        if yuanbao_price.get('goods_payment') in gconst.CAN_DISCOUNT_PAYMENT:
            mall_utils.refresh_discount_price(yuanbao_price, self._coupon_item_no)
        self.refresh_price(yuanbao_price.get('real_price', 0))
        self.refresh_skin_show()
        spine_dict = {'201001546': 'gui/ui_res_2/anim_outside/spine/520spine/gongzhu_03',
           '201001545': 'gui/ui_res_2/anim_outside/spine/520spine/gongzhu_01',
           '201001544': 'gui/ui_res_2/anim_outside/spine/520spine/gongzhu_02'
           }
        spine_file = spine_dict.get(str(target_skin_id), 'gui/ui_res_2/anim_outside/spine/520spine/gongzhu_03')
        if self._cur_spine != spine_file:
            if self._cur_spine_node and self._cur_spine_node.isValid():
                self._spine_node_dict[self._cur_spine] = self._cur_spine_node
                self._cur_spine_node.setVisible(False)
            if spine_file not in self._spine_node_dict:
                from common.uisys.uielment.CCSkeletonNode import CCSkeletonNode
                obj = CCSkeletonNode.Create(spine_file + '.json', spine_file + '.atlas', 1.0)
                obj.setAnimation(0, 'idle', True)
                self.panel.gongzhuyingzi.setAnimation(0, 'idle', True)
                self.panel.vx_spine.AddChild('gongzhu_%s' % str(target_skin_id), obj)
                obj.setPosition(self.panel.vx_spine.gongzhu.getPosition())
                self._spine_node_dict[spine_file] = obj
            node = self._spine_node_dict.get(spine_file)
            node and node.setVisible(True)
            self._cur_spine = spine_file
            self._cur_spine_node = node
        elif self._cur_spine_node:
            self._cur_spine_node.setVisible(True)
        return

    def refresh_skin_show(self):
        target_skin_id = self._cur_skin_id
        top_skin_id = dress_utils.get_top_skin_id_by_skin_id(target_skin_id)
        has_own_top_skin = mall_utils.item_has_owned_by_item_no(top_skin_id)
        if not has_own_top_skin:
            self.panel.lab_tips.setVisible(str(target_skin_id) != str(top_skin_id))
        else:
            self.panel.lab_tips.setVisible(False)
        self.refresh_btn_show()

    def refresh_btn_show(self):
        has_own_skin = mall_utils.item_has_owned_by_item_no(self._cur_skin_id)
        if has_own_skin:
            self.panel.btn_buy_1.setVisible(False)
            self.panel.btn_buy_2.setVisible(False)
            self.panel.btn_buy_3.setVisible(True)
            self.panel.vx_saoguang.setVisible(False)
            self.panel.btn_buy_3.SetEnable(False)
            self.panel.btn_buy_3.SetTextOffset({'x': '50%20','y': '50%'})
            self.panel.btn_buy_3.img_get.setVisible(True)
            self.panel.btn_buy_3.img_ticket.setVisible(False)
            self.panel.btn_buy_3.img_red.setVisible(False)
            self.panel.btn_buy_3.SetText(80451)
            return
        self.panel.btn_buy_3.img_get.setVisible(False)
        self.panel.btn_buy_3.img_ticket.setVisible(True)
        if self._coupon_item_no:
            has_own = self.check_has_own(self._coupon_item_no)
            if has_own:
                self.panel.btn_buy_1.setVisible(False)
                self.panel.btn_buy_2.setVisible(False)
                self.panel.btn_buy_3.setVisible(True)
                self.panel.vx_saoguang.setVisible(False)
                self.panel.btn_buy_3.SetEnable(True)
                self.panel.btn_buy_3.SetTextOffset({'x': '50%','y': '50%'})
                self.panel.btn_buy_3.img_red.setVisible(True)
                self.panel.btn_buy_3.SetText(608611)
            else:
                self.panel.btn_buy_1.setVisible(True)
                self.panel.btn_buy_2.setVisible(True)
                self.panel.btn_buy_3.setVisible(False)
                self.panel.vx_saoguang.setVisible(True)
                self.panel.btn_buy_3.img_red.setVisible(False)

    def check_has_own(self, item_no):
        return global_data.player and global_data.player.get_item_by_no(int(item_no))

    def init_btn_event(self):

        @self.panel.btn_buy_1.callback()
        def OnClick(btn, touch):
            if self._coupon_item_no:
                has_own = self.check_has_own(self._coupon_item_no)
                if not has_own:
                    from logic.comsys.activity.Activity520.Activity520PrincessTipsUI import Activity520PrincessTipsUI
                    ui = Activity520PrincessTipsUI()
                    goods_id = dress_utils.get_goods_id_of_role_dress_related_item_no(self._cur_skin_id)
                    ui.set_target_goods_id(goods_id)
                else:
                    from logic.comsys.mall_ui.BuyConfirmUIInterface import role_or_skin_buy_confirmUI
                    goods_id = dress_utils.get_goods_id_of_role_dress_related_item_no(self._cur_skin_id)
                    role_or_skin_buy_confirmUI(goods_id, check_top_skin=True)

        @self.panel.btn_buy_2.callback()
        def OnClick(btn, touch):
            from logic.gutils.jump_to_ui_utils import jump_to_activity
            from logic.gcommon.common_const.activity_const import ACTIVITY_520_SHOOTER
            jump_to_activity(ACTIVITY_520_SHOOTER)

        @self.panel.btn_buy_3.callback()
        def OnClick(btn, touch):
            has_own_skin = mall_utils.item_has_owned_by_item_no(self._cur_skin_id)
            if has_own_skin:
                return
            from logic.comsys.mall_ui.BuyConfirmUIInterface import role_or_skin_buy_confirmUI
            goods_id = dress_utils.get_goods_id_of_role_dress_related_item_no(self._cur_skin_id)
            role_or_skin_buy_confirmUI(goods_id, check_top_skin=True)

        @self.panel.layer_spine.callback()
        def OnClick(btn, touch):
            self._cur_spine_node.setAnimation(0, 'atk', False)
            self._cur_spine_node.addAnimation(0, 'idle', True)
            self.panel.gongzhuyingzi.setAnimation(0, 'atk', False)
            self.panel.gongzhuyingzi.addAnimation(0, 'idle', True)

    def refresh_price(self, show_price):
        if show_price < 0:
            return
        price = str(show_price)
        for i in range(3):
            show = i < len(price)
            index = i + 1
            num_nd = getattr(self.panel.nd_num, 'img_num_%d' % index)
            num_nd.setVisible(show)
            if show:
                path = 'gui/ui_res_2/activity/activity_202105/520/img_number_%s.png' % price[i]
                num_nd.SetDisplayFrameByPath('', path)

    def register_timer(self):
        act = cc.RepeatForever.create(cc.Sequence.create([
         cc.DelayTime.create(0.5),
         cc.CallFunc.create(self.refresh_time)]))
        self.panel.runAction(act)
        act.setTag(self.TIMER_TAG)

    def unregister_timer(self):
        self.panel.stopActionByTag(self.TIMER_TAG)

    def get_end_time(self):
        conf = confmgr.get('c_activity_config', self._activity_type)
        return conf.get('cEndTime', 0)

    def refresh_time(self):
        end_time = self.get_end_time()
        if end_time:
            server_time = tutil.get_server_time()
            left_time = end_time - server_time
            if left_time > 0:
                self.panel.lab_time.SetString(get_text_by_id(607014).format(tutil.get_readable_time_2(left_time)))
            else:
                self.panel.lab_time.SetString(81796)
        else:
            self.panel.lab_time.SetString(81796)

    def init_event(self):
        self.process_event(True)
        self.init_btn_event()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'player_item_update_event': self.on_player_item_update
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def refresh_panel(self):
        pass

    def on_init_panel(self):
        pass

    def on_player_item_update(self):
        self.refresh_skin_show()

    def set_show(self, show, is_init=False):
        super(Activity520Princess, self).set_show(show, is_init)
        self.panel.StopAnimation('show')
        self.panel.StopAnimation('loop')
        self.panel.RecoverAnimationNodeState('loop')
        self.panel.RecoverAnimationNodeState('show')
        self.panel.stopActionByTag(self.TIMEOUT_TAG)
        self.panel.PlayAnimation('show')
        self.panel.SetTimeOut(1.0, lambda : self.panel.PlayAnimation('loop'), tag=self.TIMEOUT_TAG)