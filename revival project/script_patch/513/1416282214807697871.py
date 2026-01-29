# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityFirstPay.py
from __future__ import absolute_import
from six.moves import range
from logic.client.const import mall_const
from logic.gutils import activity_utils, bond_utils, role_utils, task_utils
from common.cfg import confmgr
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gutils.item_utils import get_lobby_item_pic_by_item_no, get_lobby_item_name
from logic.gcommon.common_utils.local_text import get_text_by_id
import copy
import logic.gcommon.common_const.activity_const as activity_const
from logic.comsys.charge_ui.ChargeUINew import ACTIVITY_CHARGE_TYPE, ACTIVITY_NEW_ROLE_TYPE
from logic.gutils.jump_to_ui_utils import jump_to_charge
from logic.gutils.mall_utils import has_new_role_page
from logic.gutils.template_utils import init_tempate_mall_i_item
from logic.gutils.dress_utils import battle_id_to_mecha_lobby_id
from logic.gcommon.cdata import bond_config, bond_gift_config
from logic.gcommon.const import FIRST_PAY_ITEM_ID
from logic.gcommon.time_utility import get_server_time
ICON_PREFIX = 'gui/ui_res_2/battle/mech_main/'

class ActivityFirstPay(ActivityBase):
    DELAY_LOOP_TAG = 31415926
    DELAY_LIST_SHOW_TAG = 31415927
    UI_CLICK_SALOG_DIC = {'btn_buy.OnClick': '1'
       }

    def __init__(self, dlg, activity_type):
        super(ActivityFirstPay, self).__init__(dlg, activity_type)

    def refresh_panel(self):
        self.on_init_panel()

    def on_init_panel(self):
        self._conf = confmgr.get('c_activity_config', self._activity_type)
        self._mecha_conf = confmgr.get('mecha_display', 'HangarConfig', 'Content')
        self._first_pay_task_id = self._conf.get('cTask')
        self._btn_list = []
        default_select_index = None
        reward_data = self._conf.get('cUiData').get('reward_data')
        self.panel.list_item.setVisible(True)
        self.panel.list_item.DeleteAllSubItem()
        self._current_role_or_mecha_id = 0
        self._current_state = 0
        for i, reward in enumerate(reward_data):
            reward_item = self.panel.list_item.AddTemplateItem()
            pnl_bg = reward_item.pnl_bg
            role_or_mecha_id = 0
            item_path = ''
            reward_name = ''
            if 'role_id' in reward:
                role_or_mecha_id = reward['role_id']
            elif 'mecha_id' in reward:
                mecha_id = reward['mecha_id']
                role_or_mecha_id = battle_id_to_mecha_lobby_id(mecha_id)
            item_path = get_lobby_item_pic_by_item_no(role_or_mecha_id)
            pnl_bg.nd_cut.img_item.SetDisplayFrameByPath('', item_path)
            own_role_tag = self._get_role_or_mecha_is_own(role_or_mecha_id)
            pnl_bg.img_tag.setVisible(own_role_tag)
            if own_role_tag == False and default_select_index == None:
                default_select_index = i
            reward_name = get_lobby_item_name(role_or_mecha_id)
            pnl_bg.bar_name.lab_name.SetString(reward_name)
            btn_choose = pnl_bg.btn_choose
            btn_choose.EnableCustomState(True)
            self._btn_list.append(btn_choose)

            @btn_choose.unique_callback()
            def OnClick(btn, touch, i=i, reward=reward):
                self._current_select_index = i
                self._on_update_panel(reward)

        default_select_index = default_select_index if default_select_index != None else 0
        self._current_select_index = default_select_index
        self._on_update_panel(reward_data[default_select_index])
        self._init_anim()
        self._init_button()
        return

    def _init_anim(self):
        if not hasattr(self.panel, '_recorded_show__') or not self.panel._recorded_show__:
            self.panel.RecordAnimationNodeState('show')
            self.panel._recorded_show__ = True
        self.panel.StopAnimation('show')
        self.panel.RecoverAnimationNodeState('show')
        self.panel.PlayAnimation('show')

        def cb():
            self.panel.PlayAnimation('loop')

        delay = 0.66
        self.panel.DelayCallWithTag(delay, cb, self.DELAY_LOOP_TAG)

        def cb():
            own_role_tag = self._get_role_or_mecha_is_own(self._current_role_or_mecha_id)
            self.panel.bar_preview.setVisible(own_role_tag)
            bar_tips = self.panel.bar_tips
            if bar_tips:
                bar_tips.setVisible(own_role_tag)
            for item in self.panel.list_reward.GetAllItem():
                item.PlayAnimation('appear_common')

        delay = 0.5
        self.panel.DelayCallWithTag(delay, cb, self.DELAY_LIST_SHOW_TAG)

    def _init_button(self):

        @self.panel.btn_buy.unique_callback()
        def OnClick(btn, touch):
            from logic.gutils.ui_salog_utils import add_uiclick_salog_lobby
            add_uiclick_salog_lobby('jump_to_charge')
            if self._current_state == 0:
                if has_new_role_page():
                    jump_to_charge(ACTIVITY_NEW_ROLE_TYPE)
                else:
                    jump_to_charge(ACTIVITY_CHARGE_TYPE)
            elif self._current_state == 1:
                global_data.player.call_server_method('request_first_charge_reward', (self._current_select_index,))

        @self.panel.btn_show.unique_callback()
        def OnClick(btn, touch):
            if not self._current_role_or_mecha_id:
                return
            from logic.gutils.jump_to_ui_utils import jump_to_display_detail_by_item_no
            jump_to_display_detail_by_item_no(self._current_role_or_mecha_id)

    def _on_update_panel(self, reward):
        for index, btn in enumerate(self._btn_list):
            if index == self._current_select_index:
                btn.SetSelect(True)
            else:
                btn.SetSelect(False)

        is_role = True
        role_or_mecha_id = 0
        if 'role_id' in reward:
            role_or_mecha_id = reward['role_id']
            self._current_role_or_mecha_id = role_or_mecha_id
        elif 'mecha_id' in reward:
            mecha_id = reward['mecha_id']
            role_or_mecha_id = battle_id_to_mecha_lobby_id(mecha_id)
            self._current_role_or_mecha_id = role_or_mecha_id
            is_role = False
        self.panel.list_reward.DeleteAllSubItem()
        reward_list = []
        own_role_tag = self._get_role_or_mecha_is_own(role_or_mecha_id)
        bar_preview = self.panel.bar_preview
        lab_preview = self.panel.lab_preview
        lab_have_tips = self.panel.lab_have_tips
        bar_tips = self.panel.bar_tips
        list_reward = self.panel.list_reward
        if own_role_tag:
            replace_list = reward['replace_list']
            reward_list = replace_list
            bar_preview.setVisible(True)
            lab_preview.setString(get_text_by_id(634657))
            role_or_mecha_name = get_lobby_item_name(role_or_mecha_id)
            lab_have_tips.setVisible(True)
            lab_have_tips.setString(get_text_by_id(634656).format(role_or_mecha_name))
            if G_IS_NA_PROJECT or global_data.channel.is_steam_channel():
                if bar_tips:
                    bar_tips.setVisible(True)
            list_reward.setVisible(True)
        else:
            reward_list.insert(0, [role_or_mecha_id, 1])
            bar_preview.setVisible(False)
            lab_have_tips.setVisible(False)
            if G_IS_NA_PROJECT or global_data.channel.is_steam_channel():
                if bar_tips:
                    bar_tips.setVisible(False)
            list_reward.setVisible(False)
        reward_count = len(reward_list)
        for idx in range(reward_count):
            item_no, item_num = reward_list[idx]
            reward_item = self.panel.list_reward.AddTemplateItem()
            init_tempate_mall_i_item(reward_item, item_no, item_num=item_num, show_tips=True)

        is_finished = global_data.player.is_task_finished(self._first_pay_task_id)
        if is_finished:
            had_first_pay_item = bool(global_data.player.get_item_by_no(FIRST_PAY_ITEM_ID))
            if had_first_pay_item:
                self._current_state = 1
            else:
                self._current_state = 2
        btn = self.panel.btn_buy
        if self._current_state == 0:
            btn.SetText(12015)
        elif self._current_state == 1:
            btn.SetText(80930)
        elif self._current_state == 2:
            btn.SetText(80866)
        nd_skill = self.panel.nd_skill
        nd_mecha = nd_skill.nd_mecha
        nd_driver = nd_skill.nd_driver
        vx_spine = self.panel.nd_content.nd_spine
        lab_describe = self.panel.lab_describe
        lab_descibe = self.panel.nd_content.lab_descibe
        lab_name = self.panel.lab_name
        nd_joanna = self.panel.nd_joanna
        if is_role:
            bar_describe = nd_driver.bar_describe
            nd_mecha.setVisible(False)
            nd_driver.setVisible(True)
            vx_spine.setVisible(True)
            lab_describe.setVisible(False)
            if G_IS_NA_PROJECT or global_data.channel.is_steam_channel():
                if lab_name:
                    lab_name.setVisible(False)
                if nd_joanna:
                    nd_joanna.setVisible(True)
                if lab_descibe:
                    lab_descibe.setVisible(False)
            show_skill_list, role_skill_name_str = self._get_role_show_skill_list(role_or_mecha_id)
            list_skill = bar_describe.list_skill
            list_skill.DeleteAllSubItem()
            for skill_id in show_skill_list:
                skill_item = list_skill.AddTemplateItem()
                base_gift_id = bond_utils.get_base_gift(skill_id)
                gift_conf = bond_gift_config.GetBondGiftBaseDataConfig().get(base_gift_id, {})
                item_no = gift_conf.get('activate_item_no', 0)
                skill_img = get_lobby_item_pic_by_item_no(item_no)
                skill_item.icon_skill_mecha.setVisible(False)
                skill_item.icon_skill_driver.SetDisplayFrameByPath('', skill_img)
                skill_item.icon_skill_driver.setVisible(True)
                skill_item.icon_skill_driver.setScale(0.15)

            bar_describe.lab_skill.SetString(role_skill_name_str)
        else:
            bar_describe = nd_mecha.bar_describe
            mecha_id = reward['mecha_id']
            icon_path = confmgr.get('mecha_conf', 'UIConfig', 'Content', str(mecha_id), 'icon_path')
            nd_mecha.img_pic.SetDisplayFrameByPath('', icon_path[1])
            nd_mecha.setVisible(True)
            nd_driver.setVisible(False)
            vx_spine.setVisible(False)
            if G_IS_NA_PROJECT or global_data.channel.is_steam_channel():
                if lab_name:
                    lab_name.setVisible(True)
                    mache_name = get_lobby_item_name(role_or_mecha_id)
                    lab_name.setString(mache_name.upper())
                if nd_joanna:
                    nd_joanna.setVisible(False)
                if lab_descibe:
                    lab_descibe.setVisible(True)
                    if mecha_id == 8030:
                        lab_descibe.setString(get_text_by_id(634687))
                    elif mecha_id == 8025:
                        lab_descibe.setString(get_text_by_id(634688))
            lab_describe.setVisible(True)
            if mecha_id == 8030:
                lab_describe.setString(get_text_by_id(634683))
            elif mecha_id == 8025:
                lab_describe.setString(get_text_by_id(634684))
            from logic.comsys.mecha_display.MechaDisplay import MechaDisplay
            MechaDisplay.refresh_mecha_tag_list(bar_describe.temp_list_tab, mecha_id)
            show_skill_list = self._get_mecha_show_skill_list(mecha_id)
            skill_conf = confmgr.get('mecha_display', 'HangarConfig_Skills', 'Content')
            list_skill = bar_describe.list_skill
            list_skill.DeleteAllSubItem()
            for skill_id in show_skill_list:
                skill_item = list_skill.AddTemplateItem()
                skill_icon = ''.join([ICON_PREFIX, skill_conf.get(str(skill_id)).get('icon_path'), '.png'])
                skill_item.icon_skill_driver.setVisible(False)
                skill_item.icon_skill_mecha.SetDisplayFrameByPath('', skill_icon)
                skill_item.icon_skill_mecha.setVisible(True)

        if global_data.ui_lifetime_log_mgr:
            activity_type = activity_utils.get_activity_widget_type(self._activity_type)
            global_data.ui_lifetime_log_mgr.start_record_ui_page_life_time(activity_type, self.__class__.__name__)

    def _get_role_show_skill_list(self, role_id):
        role_skill_list = []
        role_skill_name_str = ''
        gift_role_id = role_id
        if role_utils.is_crossover_role(role_id):
            gift_role_id = role_utils.get_crossover_role_id(role_id)
        gift_infos = bond_gift_config.get_role_bond_gift_info(str(gift_role_id), bond_config.get_bond_max_level())
        for gift_info in gift_infos:
            base_gift_id = gift_info['gift_id']
            gift_type = bond_utils.get_gift_type(base_gift_id)
            equipped_gift_id, lv = bond_utils.get_gift_id_level(role_id, gift_type)
            if equipped_gift_id <= 0:
                equipped_gift_id = base_gift_id
            role_skill_list.append(equipped_gift_id)
            text_id = bond_gift_config.GetBondGiftDataConfig().get(equipped_gift_id, {}).get('name_id', '')
            role_skill_name_str = role_skill_name_str + get_text_by_id(text_id) + '/'

        role_skill_name_str = role_skill_name_str[:-1]
        return (
         role_skill_list, role_skill_name_str)

    def _get_mecha_show_skill_list(self, mecha_id):
        mecha_skill_lst = self._mecha_conf[str(mecha_id)].get('mecha_skill_list')
        mecha_sp_skill_lst = self._mecha_conf[str(mecha_id)].get('mecha_sp_skill_list', [])
        show_skill_list = [ x for x in mecha_skill_lst ]
        if mecha_sp_skill_lst:
            show_skill_list.extend(mecha_sp_skill_lst)
        return show_skill_list

    def _get_role_or_mecha_is_own(self, role_or_mecha_id):
        item = global_data.player.get_item_by_no(role_or_mecha_id)
        if not item:
            return False
        else:
            if item.get_expire_time() > get_server_time():
                return False
            return True

    def on_finalize_panel(self):
        if global_data.ui_lifetime_log_mgr:
            activity_type = activity_utils.get_activity_widget_type(self._activity_type)
            global_data.ui_lifetime_log_mgr.finish_record_ui_page_life_time(activity_type, self.__class__.__name__)