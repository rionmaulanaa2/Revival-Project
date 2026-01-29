# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/battle/MechaSummonUI.py
from __future__ import absolute_import
import six_ex
import six
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER
from common.cfg import confmgr
from common.const.uiconst import UI_TYPE_MESSAGE
from logic.gcommon.common_const import mecha_const
from logic.gcommon.common_const import battle_const
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils.mecha_module_utils import init_module_temp_item, get_module_card_name_and_desc
from logic.comsys.battle.MechaChargeWidget import MechaChargeWidget
from logic.client.const import game_mode_const
from logic.gutils.ui_salog_utils import add_uiclick_salog
from logic.gutils.mecha_skill_utils import get_mecha_speciality_desc_str
from logic.gutils.mecha_utils import get_mecha_lst
from logic.gutils import dress_utils, team_utils
from logic.gutils.mecha_utils import has_mecha, is_mecha_enhanced
from logic.gcommon.utility import dummy_cb
from logic.gutils import item_utils
from logic.comsys.battle.DeathRogueGiftDetailWidget import DeathRogueGiftDetailWidget
from logic.comsys.mecha_display.MechaWidget import MechaTypeChooseWidget
from six.moves import range
EXCEPT_HIDE_UI_LIST = []
ICON_PREFIX = 'gui/ui_res_2/battle/mech_main/'
from common.const import uiconst

class SkillDetailsUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_mech/mech_call_details_skill'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT

    def on_init_panel(self):
        self._skill_node_lst = [
         self.panel.temp_skill_1, self.panel.temp_skill_2,
         self.panel.temp_skill_3, self.panel.temp_skill_4, self.panel.temp_skill_5]
        self.panel.setLocalZOrder(1)

    def on_finalize_panel(self):
        self._skill_node_lst = []

    @property
    def _mecha_conf(self):
        return confmgr.get('mecha_display', 'HangarConfig', 'Content')

    @property
    def _skill_conf(self):
        return confmgr.get('mecha_display', 'HangarConfig_Skills', 'Content')

    def refresh_ui(self, mecha_id):
        if not mecha_id:
            return
        show_skill_list = self._get_show_skill_list(mecha_id)
        for index, nd in enumerate(self._skill_node_lst):
            if index >= len(show_skill_list):
                nd.setVisible(False)
                continue
            skill_id = show_skill_list[index]
            skill_conf = self._skill_conf.get(str(skill_id))
            skill_icon = ''.join([ICON_PREFIX, skill_conf.get('icon_path'), '.png'])
            skill_name = skill_conf.get('name_text_id', '')
            skill_desc = skill_conf.get('desc_text_id', '')
            skill_desc_brief = skill_conf.get('desc_text_brief', '')
            nd.lab_name.SetString(skill_name)
            nd.lab_sort.SetString(skill_desc_brief)
            nd.lab_describe.SetString(skill_desc)
            nd.img_skill.SetDisplayFrameByPath('', skill_icon)
            nd.setVisible(True)

        if len(show_skill_list) == 4:
            self.panel.PlayAnimation('show_4')
        else:
            self.panel.PlayAnimation('show_5')

    def _get_show_skill_list(self, mecha_id):
        mecha_skill_lst = self._mecha_conf[str(mecha_id)].get('mecha_skill_list')
        mecha_sp_skill_lst = self._mecha_conf[str(mecha_id)].get('mecha_sp_skill_list', [])
        show_skill_list = [ x for x in mecha_skill_lst ]
        if mecha_sp_skill_lst:
            show_skill_list.extend(mecha_sp_skill_lst)
        return show_skill_list


class ModuleDetailsUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_mech/mech_call_details_module'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_NO_EFFECT

    def on_init_panel(self):
        self.init_parameters()
        self.panel.setLocalZOrder(1)

    def on_finalize_panel(self):
        pass

    def init_parameters(self):
        _mecha_conf = confmgr.get('mecha_default_module_conf', default={})
        self._card_conf = confmgr.get('mecha_reinforce_card', 'ModuleConfig', 'Content')
        self._mecha_pos_card_conf = {}
        get_mecha_module_cur_plan = global_data.player.get_mecha_module_cur_plan
        for mecha_id in six.iterkeys(_mecha_conf):
            mecha_modules = get_mecha_module_cur_plan(int(mecha_id)) or {}
            self._mecha_pos_card_conf.setdefault(mecha_id, {})
            pos_to_card_id = self._mecha_pos_card_conf[mecha_id]
            for slot_pos, slot_conf in six.iteritems(mecha_modules):
                pos_to_card_id.setdefault(slot_pos, [])
                for idx, one_conf in enumerate(slot_conf):
                    card_id = one_conf
                    if card_id not in pos_to_card_id[slot_pos]:
                        pos_to_card_id[slot_pos].append(card_id)

    def refresh_ui(self, mecha_id):
        str_mecha_id = str(mecha_id)
        if not self._mecha_pos_card_conf or str_mecha_id not in self._mecha_pos_card_conf:
            return
        else:
            pos_to_card_id = self._mecha_pos_card_conf[str_mecha_id]
            for slot_pos, card_list in six.iteritems(pos_to_card_id):
                nd = getattr(self.panel, 'temp_module_%d' % slot_pos)
                if slot_pos != mecha_const.SP_MODULE_SLOT:
                    card_id = card_list[0]
                    card_name_desc, card_effect_desc = get_module_card_name_and_desc(card_id, None)
                    nd.lab_name.SetString(card_name_desc)
                    nd.lab_details1.SetString(card_effect_desc)
                    init_module_temp_item(nd.bar_item, slot_pos, card_id, None)
                else:
                    for i, card_id in enumerate(card_list):
                        sp_nd = nd.up if i == 0 else nd.down
                        card_name_desc, card_effect_desc = get_module_card_name_and_desc(card_id, None)
                        if i == 0:
                            sp_nd.lab_name_up.SetString(card_name_desc)
                            sp_nd.lab_details_up.SetString(card_effect_desc)
                        else:
                            sp_nd.lab_name_down.SetString(card_name_desc)
                            sp_nd.lab_details_down.SetString(card_effect_desc)
                        if i == 0:
                            init_module_temp_item(nd.bar_item_1, slot_pos, card_id, None)
                        elif i == 1:
                            init_module_temp_item(nd.bar_item_2, slot_pos, card_id, None)

                    if len(card_list) < 2:
                        nd.down.setVisible(False)
                        nd.nd_lock.setVisible(True)
                    else:
                        nd.down.setVisible(True)
                        nd.nd_lock.setVisible(False)

            return


class CMechaBtn(object):

    def __init__(self, parent_panel, id, in_usual_mecha_mode=False):
        self.parent_panel = parent_panel
        self.select_id = id
        self.btn_nds = {}
        self.btn_cbs = {}
        self.in_usual_mecha_mode = in_usual_mecha_mode
        self.init_parameters()

    def destroy(self):
        for nd in six.itervalues(self.btn_nds):
            if nd.getParent():
                nd.Destroy()
            else:
                nd.release()

        self.parent_panel = None
        self.select_id = None
        self.btn_nds = {}
        self.btn_cbs = {}
        return

    @property
    def mecha_conf(self):
        return confmgr.get('mecha_conf', 'UIConfig', 'Content')

    def open_ui(self):
        for k in ('normal_nd', 'unable_nd'):
            if k in self.btn_nds:
                self.btn_nds[k].PlayAnimation('open')

    def removeFromParent(self):
        for nd in six.itervalues(self.btn_nds):
            nd.retain()
            nd.removeFromParent()

        self.parent_panel = None
        return

    def reAddParent(self, parent_panel):
        self.parent_panel = parent_panel
        for nd in six.itervalues(self.btn_nds):
            parent_panel.AddChild(None, nd)
            nd.release()

        return

    def is_enable(self):
        return self.enable

    def init_parameters(self):
        self.nd_template_path = {'normal_nd': 'battle_mech/i_mech_item_active','select_nd': 'battle_mech/i_mech_item_sel',
           'unable_nd': 'battle_mech/i_mech_item_lock'
           }
        self.select = False
        self.enable = True
        self.mecha_id = 8001
        self.is_created = False

    def set_mecha_btn_data(self, mecha_id, is_owned):
        self.mecha_id = mecha_id
        self.is_owned = is_owned
        conf = self.mecha_conf[str(mecha_id)]
        icon_path = conf.get('icon_path', [])
        for nd in six.itervalues(self.btn_nds):
            nd.img_mech_icon.SetDisplayFrameByPath('', icon_path[0])

        self.update_mecha_state()

    def show_selection_info(self, is_show):
        for k in ['normal_nd', 'select_nd', 'unable_nd']:
            if k in self.btn_nds:
                if getattr(self.btn_nds[k], 'temp_teammate_choose'):
                    self.btn_nds[k].temp_teammate_choose.setVisible(is_show)
                    self.btn_nds[k].temp_teammate_choose.nd_chosen.setVisible(is_show)

    def update_mecha_state(self):
        self.set_enable(self.is_owned)
        if not global_data.player:
            return
        is_used = self.mecha_id in global_data.player.get_setting('used_mecha', [])
        for k in ['normal_nd', 'select_nd']:
            if k not in self.btn_nds:
                continue
            self.btn_nds[k].lab_new.setVisible(not is_used and self.is_owned)

    def set_select(self, select):
        if select:
            self.creat_btn_nd('select_nd')
        else:
            self.creat_btn_nd('normal_nd')
        if not self.enable or self.select == select:
            return
        self.select = select
        ruler = {'normal_nd': not select,'select_nd': select,'unable_nd': False}
        for k, nd in six.iteritems(self.btn_nds):
            nd.setVisible(ruler.get(k, False))

    def set_enable(self, enable):
        if enable:
            self.creat_btn_nd('normal_nd')
        else:
            self.creat_btn_nd('unable_nd')
        if self.enable == enable:
            return
        self.enable = enable
        ruler = {'normal_nd': enable,'select_nd': False,'unable_nd': not enable}
        for k, nd in six.iteritems(self.btn_nds):
            nd.setVisible(ruler.get(k, False))

    def set_unique_callback(self, nd_type, cb):
        self.btn_cbs[nd_type] = cb

    def creat_btn_nd(self, nd_type):
        if not self.parent_panel:
            return
        if nd_type not in self.btn_nds and nd_type in self.nd_template_path:
            nd = global_data.uisystem.load_template_create(self.nd_template_path[nd_type], self.parent_panel)
            conf = self.mecha_conf[str(self.mecha_id)]
            icon_path = conf.get('icon_path', [])
            nd.img_mech_icon.SetDisplayFrameByPath('', icon_path[0])
            self.btn_nds[nd_type] = nd

            @nd.btn_item.unique_callback()
            def OnClick(btn, touch, nd_type=nd_type, select_id=self.select_id):
                cb = self.btn_cbs.get(nd_type)
                cb and cb(select_id, self.in_usual_mecha_mode)

    def get_btn_nd(self, nd_type):
        return self.btn_nds.get(nd_type)


class MechaSummonUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_mech/mech_call_clone'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = uiconst.UI_VKB_CLOSE_BY_DEFAULT_FUNC_NAME
    MOUSE_CURSOR_TRIGGER_SHOW = True
    UNBOUGHT_TYPE = [10000, -1, -1]
    MECHA_OFFSET_X = 108
    MECHA_OFFSET_Y = 135
    TIMER_TAG = 200107
    UI_ACTION_EVENT = {'btn_close.OnClick': 'on_click_close_btn',
       'btn_sure.OnClick': 'on_btn_call',
       'btn_describe.OnClick': 'on_btn_describe',
       'btn_right_direction.OnClick': 'on_click_expand_btn'
       }
    HOT_KEY_FUNC_MAP = {'summon_call_mecha_confirm': 'keyboard_summon_call_mecha_confirm'
       }
    HOT_KEY_FUNC_MAP_SHOW = {'summon_call_mecha_confirm': {'node': 'btn_sure.temp_pc'}}

    def on_resolution_changed(self):
        self.panel.StopAnimation('details_tips')
        self.panel.PlayAnimation('details_tips')
        self.update_nd_dir_pos()

    def on_init_panel(self, player):
        self.player = player
        self.disappearing = False
        self._show_mecha_list = []
        self._recorded_ui_item_set = set()
        self.init_parameters()
        self.init_event()
        self.init_panel()
        self.hide_main_ui(exceptions=EXCEPT_HIDE_UI_LIST, exception_types=(UI_TYPE_MESSAGE,))
        global_data.emgr.show_screen_effect.emit('GaussanBlurEffect', {})
        self.panel.PlayAnimation('open')
        global_data.sound_mgr.play_sound_2d('Play_ui_notice', ('ui_notice', 'mecha_select_window'))
        self.player.send_event('E_GUIDE_MECHA_UI_SHOW', self)
        self.mecha_sp_type_widget = MechaTypeChooseWidget(self, self.panel)
        self.init_node_view()
        self.init_rogue()
        self.init_groupmate_mecha()
        self.init_mecha_list()
        self.init_other_content()
        self.mecha_charge_widget = MechaChargeWidget(self.panel.nd_call_progress)
        self.mecha_charge_widget.on_show()
        self.init_tech_and_module_choose_widget()
        self.on_finished_created()

    def init_rogue(self):
        self._rogue_tips_widget = DeathRogueGiftDetailWidget(self, self.panel)
        self._rogue_tips_widget.hide()

    def init_tech_and_module_choose_widget(self):
        from logic.comsys.battle.TechAndModuleChooseWidget import TechAndModuleChooseWidget
        self.tech_and_module_choose_widget = TechAndModuleChooseWidget(self.panel)

    def init_other_content(self):
        if global_data.player and global_data.player.in_local_battle():
            self.panel.btn_skill.setVisible(False)
            self.btn_module.setVisible(False)
        else:
            self.btn_module.setVisible(True)

    def on_finished_created(self):
        self.select_default_mecha()
        if self.battle_type in [game_mode_const.GAME_MODE_ASSAULT]:
            self.panel.nd_tip.setVisible(False)
        else:
            self.panel.nd_tip.setVisible(True)
            if self.battle_type not in [game_mode_const.GAME_MODE_CROWN, game_mode_const.GAME_MODE_DEATH,
             game_mode_const.GAME_MODE_MECHA_DEATH, game_mode_const.GAME_MODE_RANDOM_DEATH,
             game_mode_const.GAME_MODE_CONTROL, game_mode_const.GAME_MODE_FLAG,
             game_mode_const.GAME_MODE_CRYSTAL, game_mode_const.GAME_MODE_ADCRYSTAL,
             game_mode_const.GAME_MODE_TRAIN, game_mode_const.GAME_MODE_FLAG2, game_mode_const.GAME_MODE_GOOSE_BEAR]:
                self.panel.lab_tips.SetString(1035)
            else:
                self.panel.lab_tips.SetString(19797)

    def init_node_view(self):
        if self.battle_type == game_mode_const.GAME_MODE_RANDOM_DEATH:
            self.panel.list_choose_mecha.setVisible(False)
            self.panel.nd_dir.setVisible(False)
            self.panel.img_tab.setVisible(False)
            self.panel.nd_change.setVisible(False)
            self.panel.lab_title.setVisible(True)
            self.panel.list_choose_mecha_random.setVisible(True)
            self.panel.nd_tip.setVisible(False)
        if global_data.battle and global_data.battle.is_customed_no_multi_mecha_limit():
            self.panel.nd_tip.setVisible(False)

    def init_mecha_list(self):
        from logic.gutils.InfiniteScrollWidget import InfiniteScrollWidget
        if self.battle_type == game_mode_const.GAME_MODE_RANDOM_DEATH:
            list_mecha_node = self.panel.list_choose_mecha_random
        else:
            list_mecha_node = self.panel.list_choose_mecha
        self._list_sview = InfiniteScrollWidget(list_mecha_node, self.panel.nd_mech, up_limit=500, down_limit=500)
        self._list_sview.set_template_init_callback(self.init_mecha_btn)
        self._list_sview.enable_item_auto_pool(True)
        self.init_ui_show()

    def init_ui_show(self):
        self._show_mecha_list = self.get_show_data()
        self._list_sview.update_data_list(self._show_mecha_list)
        self._list_sview.update_scroll_view()

    def refresh_ui_show(self):
        self._show_mecha_list = self.get_show_data()
        self._list_sview.update_data_list(self._show_mecha_list)
        self._list_sview.refresh_showed_item()
        self._list_sview.update_scroll_view()
        if len(self._show_mecha_list) < 10:
            self.panel.btn_right_direction.setVisible(False)
            if self.is_in_expand_mode:
                self.on_click_expand_btn(None, None)
        else:
            self.panel.btn_right_direction.setVisible(True)
        to_be_removed = []
        for ui_item in self._recorded_ui_item_set:
            if not ui_item or not ui_item.isValid():
                to_be_removed.append(ui_item)

        for i in to_be_removed:
            self._recorded_ui_item_set.remove(i)

        return

    def get_show_data(self):
        if self.battle_type == game_mode_const.GAME_MODE_RANDOM_DEATH:
            ls = global_data.death_battle_data.get_mecha_list()
        else:
            ls = self.mecha_sp_type_widget.get_sp_type_mecha_list()
            ls = sorted(ls, key=lambda x: (
             x not in self.own_mecha_lst, x not in self.usual_mecha_ids, x not in self.exclusive_mecha_ids, x not in self.share_mecha_lst, x))
        return ls

    def on_finalize_panel(self):
        if self._list_sview:
            self._list_sview.destroy()
            self._list_sview = None
        self.destroy_widget('mecha_sp_type_widget')
        self.destroy_widget('mecha_charge_widget')
        self.unbind_ui_event(self.player)
        self.show_main_ui()
        if not global_data.ui_mgr.get_ui('ExerciseWeaponListUI'):
            global_data.emgr.hide_screen_effect.emit('GaussanBlurEffect')
        self.skill_detail and self.skill_detail.close()
        self.module_detail and self.module_detail.close()
        if global_data.player:
            global_data.player.logic.send_event('E_GUIDE_MECHA_UI_FINAL')
        self._recorded_ui_item_set = set()
        self.init_groupmate_mecha = dummy_cb
        self.update_selection = dummy_cb
        self.update_selection_single = dummy_cb
        self.get_mecha_is_chooseable = dummy_cb
        self.on_select_mecha = dummy_cb
        self.check_btn_call = dummy_cb
        return

    def on_switch_sp_type(self, sp_type):
        self.mecha_sp_type_widget.switch_sp_type(sp_type)
        self.refresh_ui_show()

    def init_mecha_btn(self, ui_item, data):
        mecha_id = data
        lobby_mecha_id = dress_utils.battle_id_to_mecha_lobby_id(int(mecha_id))
        icon_path = 'gui/ui_res_2/item/mecha/%d.png' % lobby_mecha_id
        ui_item.img_mecha.SetDisplayFrameByPath('', icon_path)
        ui_item.img_mecha_shadow.SetDisplayFrameByPath('', icon_path)
        if mecha_id in self.exclusive_mecha_ids:
            ui_item.nd_rogue.setVisible(True)
        else:
            ui_item.nd_rogue.setVisible(False)
        is_owned = mecha_id in self.own_mecha_lst
        is_usual = mecha_id in self.usual_mecha_ids
        if not global_data.player:
            return
        is_used = mecha_id in global_data.player.get_setting('used_mecha', [])
        is_enable = self.get_mecha_is_enable(mecha_id)
        chooseable = self.get_mecha_is_chooseable(mecha_id)
        ui_item.img_lock.setVisible(not is_enable or not chooseable)
        show_new = not is_used and is_owned
        ui_item.img_new.setVisible(show_new)
        show_share = mecha_id in self.share_mecha_lst
        ui_item.nd_share_tips.setVisible(show_share)
        from logic.gutils.mecha_utils import avatar_is_mecha_limited_free_now
        show_free = not show_new and not show_share and avatar_is_mecha_limited_free_now(lobby_mecha_id)
        ui_item.nd_mode_tips.setVisible(show_free)
        ui_item.img_always.setVisible(is_usual)
        ui_item.nd_enhance_tips.setVisible(is_mecha_enhanced(mecha_id))
        ui_item.StopAnimation('choose')
        ui_item.RecoverAnimationNodeState('choose')
        if ui_item not in self._recorded_ui_item_set:
            ui_item.RecordAnimationNodeState('choose')
            ui_item.RecordAnimationNodeState('loop')
            self._recorded_ui_item_set.add(ui_item)
        if self.select_id and self.select_id == mecha_id:
            ui_item.btn_mecha.SetSelect(True)
            ui_item.PlayAnimation('choose')
            ui_item.PlayAnimation('loop')
        else:
            ui_item.btn_mecha.SetSelect(False)
            ui_item.StopAnimation('loop')
            ui_item.RecoverAnimationNodeState('loop')

        @ui_item.btn_mecha.callback()
        def OnBegin(btn, touch):
            global_data.emgr.hide_tech_and_module_choose_widget.emit()
            ui_item.nd_btn.setScale(1 / 0.83)
            ui_item.setLocalZOrder(1)
            ui_item.img_frame_choose.setVisible(True)
            ui_item.img_choose_light.setVisible(True)
            return True

        @ui_item.btn_mecha.callback()
        def OnEnd(btn, touch):
            ui_item.nd_btn.setScale(1)
            ui_item.setLocalZOrder(0)
            ui_item.img_frame_choose.setVisible(False)
            ui_item.img_choose_light.setVisible(False)

        @ui_item.btn_mecha.callback()
        def OnCancel(btn, touch):
            ui_item.nd_btn.setScale(1)
            ui_item.setLocalZOrder(0)
            ui_item.img_frame_choose.setVisible(False)
            ui_item.img_choose_light.setVisible(False)

        @ui_item.btn_mecha.callback()
        def OnClick(btn, touch):
            is_enable = self.get_mecha_is_enable(mecha_id)
            is_chooseable = self.get_mecha_is_chooseable(mecha_id)
            if not (is_enable and is_chooseable):
                in_local_battle = global_data.player and global_data.player.in_local_battle()
                if not in_local_battle:
                    text = 19841
                    if not is_chooseable:
                        text = 19870
                    global_data.game_mgr.show_tip(get_text_by_id(text))
                return
            self.set_mecha_btn_select(mecha_id, ui_item)
            global_data.emgr.click_mecha_btn_in_summon_ui.emit(mecha_id)
            if self.skill_detail and self.skill_detail.isVisible():
                self.skill_detail.refresh_ui(self.select_id)

        self.update_selection_single(mecha_id, ui_item)
        ui_display_conf = confmgr.get('ui_display_conf', 'MechaSummonUIItem', 'Content', default={})
        node_ui_conf = ui_display_conf.get(str(mecha_id))
        if node_ui_conf:
            pos = node_ui_conf.get('NodePos')
            if pos:
                ui_item.img_mecha.SetPosition(*pos)
            else:
                ui_item.img_mecha.ReConfPosition()
            pos = node_ui_conf.get('ShadowPos')
            if pos:
                ui_item.img_mecha_shadow.SetPosition(*pos)
            else:
                ui_item.img_mecha_shadow.ReConfPosition()
            scale = node_ui_conf.get('NodeScale')
            if scale:
                ui_item.img_mecha.SetScaleCheckRecord(scale)
                ui_item.img_mecha_shadow.SetScaleCheckRecord(scale)
            else:
                ui_item.img_mecha.ScaleSelfNode()
                ui_item.img_mecha_shadow.ScaleSelfNode()
        else:
            ui_item.img_mecha.ReConfPosition()
            ui_item.img_mecha_shadow.ReConfPosition()
            ui_item.img_mecha.ScaleSelfNode()
            ui_item.img_mecha_shadow.ScaleSelfNode()

    def get_mecha_ui_item(self, mecha_id):
        if mecha_id not in self._show_mecha_list:
            return None
        else:
            index = self._show_mecha_list.index(mecha_id)
            mecha_ui_item = self._list_sview.get_list_item(index)
            return mecha_ui_item

    def bind_ui_event(self, target):
        regist_func = target.regist_event
        regist_func('E_STATE_CHANGE_CD', self.on_update_change_cd)
        regist_func('E_ADD_TEAMMATE', self._on_add_teammate, 999)
        regist_func('E_DELETE_TEAMMATE', self._on_delete_teammate, 999)
        regist_func('E_UPDATE_TEAMMATE_INFO', self._on_update_teammate, 999)

    def unbind_ui_event(self, target):
        if target and target.is_valid():
            unregist_func = target.unregist_event
            unregist_func('E_STATE_CHANGE_CD', self.on_update_change_cd)
            unregist_func('E_ADD_TEAMMATE', self._on_add_teammate)
            unregist_func('E_DELETE_TEAMMATE', self._on_delete_teammate)
            unregist_func('E_UPDATE_TEAMMATE_INFO', self._on_update_teammate)

    def init_event(self):
        econf = {'scene_player_setted_event': self.on_camera_player_setted,
           'close_mecha_summon_ui_event': self.on_click_close_btn,
           'hide_skill_detail_event': self.hide_detail_nd
           }
        emgr = global_data.emgr
        emgr.bind_events(econf)
        self.bind_ui_event(self.player)
        ui = global_data.ui_mgr.get_ui('MechaUI')
        if ui:
            left_time = min(ui.get_mecha_count_down_progress, ui.get_mecha_count_down)
            total_cd = ui.get_mecha_total_cd
        else:
            cd_type, total_cd, left_time = self.player.ev_g_get_change_state()
        self.on_update_change_cd(None, total_cd, left_time)
        if self.battle_type != game_mode_const.GAME_MODE_RANDOM_DEATH:
            self.panel.btn_sure.SetEnable(left_time <= 0)
        if self.play_type == battle_const.PLAY_TYPE_DEATH_IMBA:
            self.panel.btn_describe.SetEnable(True)
            self.panel.btn_describe.setVisible(True)
            battle_play_guide = global_data.achi_mgr.get_cur_user_archive_data('battle_play_guide', {})
            guid_key = str(self.play_type)
            if not battle_play_guide.get(guid_key, False):
                battle_play_guide.update({guid_key: True})
                global_data.ui_mgr.show_ui('BattleImbaGuideUI', 'logic.comsys.battle')
                global_data.achi_mgr.set_cur_user_archive_data('battle_play_guide', battle_play_guide)
        else:
            self.panel.btn_describe.SetEnable(False)
            self.panel.btn_describe.setVisible(False)
        return

    @property
    def mecha_conf(self):
        return confmgr.get('mecha_conf', 'UIConfig', 'Content')

    def init_parameters(self):
        self.all_mecha_lst, self.own_mecha_lst, self.share_mecha_lst = get_mecha_lst()
        self.skill_detail = None
        self.module_detail = None
        self.mecha_order = []
        self.mecha_btn = {}
        self.usual_mecha_btn = {}
        self.get_mecha_cd_timer = None
        self.get_mecha_count_down = 0
        self.get_mecha_count_down_progress = 0
        self.speed_up = mecha_const.RECALL_MAXCD_TYPE_GETMECHA / 2
        in_local_battle = global_data.player.in_local_battle()
        self.select_id = None
        self.chosen_mecha = {}
        self.created_mecha = {}
        self.chosen_mecha_id_2_color_list = {}
        self.created_mecha_id_2_color = {}
        self.mecha_creation_num = {}
        self.eid_2_color = None
        self.is_in_expand_mode = False
        self.battle_type = global_data.game_mode.get_mode_type()
        self.play_type = global_data.battle.get_battle_play_type() if global_data.battle else None
        init_groupmate_mecha_func = {game_mode_const.GAME_MODE_DEATH: self.init_groupmate_mecha_death,
           game_mode_const.GAME_MODE_EXERCISE: self.init_groupmate_mecha_exercise,
           game_mode_const.GAME_MODE_MECHA_DEATH: self.init_groupmate_mecha_death,
           game_mode_const.GAME_MODE_FFA: self.init_groupmate_mecha_ffa,
           game_mode_const.GAME_MODE_RANDOM_DEATH: self.init_groupmate_mecha_death,
           game_mode_const.GAME_MODE_CONTROL: self.init_groupmate_mecha_death,
           game_mode_const.GAME_MODE_FLAG: self.init_groupmate_mecha_death,
           game_mode_const.GAME_MODE_CROWN: self.init_groupmate_mecha_death,
           game_mode_const.GAME_MODE_CRYSTAL: self.init_groupmate_mecha_death,
           game_mode_const.GAME_MODE_ADCRYSTAL: self.init_groupmate_mecha_death,
           game_mode_const.GAME_MODE_TRAIN: self.init_groupmate_mecha_death,
           game_mode_const.GAME_MODE_GOOSE_BEAR: self.init_groupmate_mecha_death,
           game_mode_const.GAME_MODE_ASSAULT: self.init_groupmate_mecha_assault
           }
        self.init_groupmate_mecha = init_groupmate_mecha_func.get(self.battle_type, self.init_groupmate_mecha_normal)
        update_selection_func = {game_mode_const.GAME_MODE_DEATH: self.update_selection_death,
           game_mode_const.GAME_MODE_MECHA_DEATH: self.update_selection_death,
           game_mode_const.GAME_MODE_RANDOM_DEATH: self.update_selection_death,
           game_mode_const.GAME_MODE_CONTROL: self.update_selection_death,
           game_mode_const.GAME_MODE_FLAG: self.update_selection_death,
           game_mode_const.GAME_MODE_CROWN: self.update_selection_death,
           game_mode_const.GAME_MODE_CRYSTAL: self.update_selection_death,
           game_mode_const.GAME_MODE_ADCRYSTAL: self.update_selection_death,
           game_mode_const.GAME_MODE_TRAIN: self.update_selection_death,
           game_mode_const.GAME_MODE_GOOSE_BEAR: self.update_selection_death
           }
        self.update_selection = update_selection_func.get(self.battle_type, self.update_selection_normal)
        update_selection_single_func = {game_mode_const.GAME_MODE_DEATH: self.update_selection_single_death,
           game_mode_const.GAME_MODE_MECHA_DEATH: self.update_selection_single_death,
           game_mode_const.GAME_MODE_RANDOM_DEATH: self.update_selection_single_death,
           game_mode_const.GAME_MODE_CONTROL: self.update_selection_single_death,
           game_mode_const.GAME_MODE_FLAG: self.update_selection_single_death,
           game_mode_const.GAME_MODE_CROWN: self.update_selection_single_death,
           game_mode_const.GAME_MODE_CRYSTAL: self.update_selection_single_death,
           game_mode_const.GAME_MODE_ADCRYSTAL: self.update_selection_single_death,
           game_mode_const.GAME_MODE_TRAIN: self.update_selection_single_death,
           game_mode_const.GAME_MODE_GOOSE_BEAR: self.update_selection_single_death
           }
        self.update_selection_single = update_selection_single_func.get(self.battle_type, self.update_selection_single_normal)
        get_mecha_is_choosable_func = {game_mode_const.GAME_MODE_DEATH: self.get_mecha_is_chooseable_death,
           game_mode_const.GAME_MODE_MECHA_DEATH: self.get_mecha_is_chooseable_death,
           game_mode_const.GAME_MODE_FFA: self.get_mecha_is_chooseable_mecha_death,
           game_mode_const.GAME_MODE_RANDOM_DEATH: self.get_mecha_is_chooseable_death,
           game_mode_const.GAME_MODE_CONTROL: self.get_mecha_is_chooseable_death,
           game_mode_const.GAME_MODE_FLAG: self.get_mecha_is_chooseable_death,
           game_mode_const.GAME_MODE_CROWN: self.get_mecha_is_chooseable_death,
           game_mode_const.GAME_MODE_CRYSTAL: self.get_mecha_is_chooseable_death,
           game_mode_const.GAME_MODE_ADCRYSTAL: self.get_mecha_is_chooseable_death,
           game_mode_const.GAME_MODE_TRAIN: self.get_mecha_is_chooseable_death,
           game_mode_const.GAME_MODE_GOOSE_BEAR: self.get_mecha_is_chooseable_death,
           game_mode_const.GAME_MODE_ASSAULT: self.get_mecha_is_chooseable_death
           }
        self.get_mecha_is_chooseable = get_mecha_is_choosable_func.get(self.battle_type, self.get_mecha_is_chooseable_normal)
        on_select_mecha_func = {game_mode_const.GAME_MODE_DEATH: self.on_select_mecha_death,
           game_mode_const.GAME_MODE_MECHA_DEATH: self.on_select_mecha_death,
           game_mode_const.GAME_MODE_RANDOM_DEATH: self.on_select_mecha_death,
           game_mode_const.GAME_MODE_CONTROL: self.on_select_mecha_death,
           game_mode_const.GAME_MODE_FLAG: self.on_select_mecha_death,
           game_mode_const.GAME_MODE_CROWN: self.on_select_mecha_death,
           game_mode_const.GAME_MODE_CRYSTAL: self.on_select_mecha_death,
           game_mode_const.GAME_MODE_ADCRYSTAL: self.on_select_mecha_death,
           game_mode_const.GAME_MODE_TRAIN: self.on_select_mecha_death,
           game_mode_const.GAME_MODE_GOOSE_BEAR: self.on_select_mecha_death
           }
        self.on_select_mecha = on_select_mecha_func.get(self.battle_type, self.on_select_mecha_normal)
        on_reset_mecha_func = {game_mode_const.GAME_MODE_DEATH: self.on_reset_mecha_death,
           game_mode_const.GAME_MODE_MECHA_DEATH: self.on_reset_mecha_death,
           game_mode_const.GAME_MODE_RANDOM_DEATH: self.on_reset_mecha_death,
           game_mode_const.GAME_MODE_CONTROL: self.on_reset_mecha_death,
           game_mode_const.GAME_MODE_FLAG: self.on_reset_mecha_death,
           game_mode_const.GAME_MODE_CRYSTAL: self.on_reset_mecha_death,
           game_mode_const.GAME_MODE_ADCRYSTAL: self.on_reset_mecha_death,
           game_mode_const.GAME_MODE_TRAIN: self.on_reset_mecha_death,
           game_mode_const.GAME_MODE_GOOSE_BEAR: self.on_reset_mecha_death
           }
        self.on_reset_mecha = on_reset_mecha_func.get(self.battle_type, self.on_reset_mecha_normal)
        check_call_func = {game_mode_const.GAME_MODE_DEATH: self.check_call_btn_death,
           game_mode_const.GAME_MODE_MECHA_DEATH: self.check_call_btn_mecha_death,
           game_mode_const.GAME_MODE_FFA: self.check_call_btn_mecha_death,
           game_mode_const.GAME_MODE_RANDOM_DEATH: self.check_call_btn_death,
           game_mode_const.GAME_MODE_CONTROL: self.check_call_btn_death,
           game_mode_const.GAME_MODE_FLAG: self.check_call_btn_death,
           game_mode_const.GAME_MODE_CROWN: self.check_call_btn_death,
           game_mode_const.GAME_MODE_CRYSTAL: self.check_call_btn_death,
           game_mode_const.GAME_MODE_ADCRYSTAL: self.check_call_btn_death,
           game_mode_const.GAME_MODE_TRAIN: self.check_call_btn_death,
           game_mode_const.GAME_MODE_GOOSE_BEAR: self.check_call_btn_mecha_death,
           game_mode_const.GAME_MODE_ASSAULT: self.check_call_btn_mecha_death
           }
        self.check_btn_call = check_call_func.get(self.battle_type, self.check_call_btn_normal)
        self._call_from_usual_mecha = False
        self._mecha_groupmate_mutex = self.player.ev_g_mecha_groupmate_mutex()
        self.usual_mecha_ids = global_data.player.get_usual_mecha_ids()
        self.exclusive_mecha_ids = global_data.cam_lplayer.ev_g_all_exclusive_mecha_id()
        return

    def init_panel(self):
        self.init_detail_nd()
        mecha_open_info = self.player.get_owner().read_mecha_open_info()
        self.update_mecha_info(mecha_open_info)
        self.panel.PlayAnimation('open')
        self.panel.PlayAnimation('details_tips')
        exc_gift = global_data.cam_lplayer.ev_g_lst_exclusive_gift()
        if not exc_gift:
            self.panel.lab_tips_rogue.setVisible(False)
        else:
            self.panel.lab_tips_rogue.setVisible(True)
            lab_tips_rogue = self.panel.lab_tips_rogue
            lab_tips_rogue.setVisible(True)
            mecha_name = item_utils.get_mecha_name_by_id(exc_gift['mecha_id'])
            lab_tips_rogue.SetString(get_text_by_id(365, {'mecha': mecha_name}))
            pic = exc_gift['small_icon_path']
            btn_rogue = lab_tips_rogue.nd_auto_fit.temp_rogue.btn_rogue
            btn_rogue.SetFrames('', [pic, pic, pic], True, None)

            @btn_rogue.unique_callback()
            def OnBegin(btn, touch, gift_id=exc_gift['gift_id']):
                wpos = touch.getLocation()
                self._show_rogue_tips(gift_id, wpos)
                return True

            @btn_rogue.unique_callback()
            def OnEnd(btn, touch):
                self._hide_rogue_tips()

        return

    def select_default_mecha(self):
        selected_mecha_id = None
        if self.exclusive_mecha_ids:
            for i in range(len(self.exclusive_mecha_ids) - 1, -1, -1):
                mecha_id = self.exclusive_mecha_ids[i]
                if mecha_id in self.own_mecha_lst:
                    selected_mecha_id = mecha_id
                    break

        in_local_battle = selected_mecha_id or global_data.player.in_local_battle()
        if in_local_battle:
            selected_mecha_id = 8001 if 1 else self.get_default_select_mecha_id()
        if selected_mecha_id not in self._show_mecha_list:
            log_error('can not find default node!!!!')
        else:
            btn = self.get_mecha_ui_item(selected_mecha_id)
            if not btn:
                index = self._show_mecha_list.index(selected_mecha_id)
                self._list_sview.center_with_index(index, self.init_mecha_btn)
        if selected_mecha_id not in six_ex.values(self.created_mecha):
            btn = self.get_mecha_ui_item(selected_mecha_id)
            if btn:
                btn.btn_mecha.OnClick(btn.btn_mecha)
        for index, id in enumerate(self.mecha_order):
            if not self.select_id:
                btn = self.get_mecha_ui_item(id)
                if btn:
                    btn.btn_mecha.OnClick(btn.btn_mecha)
            else:
                break

        return

    def init_detail_nd(self):
        detail_nd = {self.panel.btn_skill: [
                                'skill_detail', SkillDetailsUI]
           }
        for btn, widget_info in six.iteritems(detail_nd):

            @btn.unique_callback()
            def OnClick(btn, touch, widget_info=widget_info):
                global_data.emgr.hide_tech_and_module_choose_widget.emit()
                widget_name, widget_cls = widget_info
                widget = getattr(self, widget_name)
                if not widget:
                    widget = widget_cls()
                    setattr(self, widget_name, widget)
                widget.setVisible(True)
                widget.refresh_ui(self.select_id)
                if not self.select_id:
                    return
                else:
                    self.panel.img_shadow.setVisible(True)
                    self.panel.nd_close_detail.setVisible(True)
                    widget.PlayAnimation('appear')
                    if self.is_in_expand_mode:
                        self.on_click_expand_btn(None, None)

                    @self.panel.nd_close_detail.callback()
                    def OnClick(btn, touch, widget_info=widget_info):
                        self.hide_detail_nd(widget_info)
                        return True

                    return True

    def hide_detail_nd(self, widget_info):
        self.panel.nd_close_detail.setVisible(False)
        self.btn_close.setVisible(True)
        self.panel.img_shadow.setVisible(False)
        self.panel.StopAnimation('details_tips')
        self.panel.PlayAnimation('details_tips')
        widget_name, widget_cls = widget_info
        widget = getattr(self, widget_name)
        if widget:
            widget.setVisible(False)

    def update_mecha_info(self, result):
        mecha_open_order = result.get('opened_order', [])
        self.mecha_order = []
        mecha_closed = []
        for mecha_id in mecha_open_order:
            if has_mecha(global_data.player.logic, mecha_id):
                self.mecha_order.append(mecha_id)
            else:
                mecha_closed.append(mecha_id)

        self.mecha_order.extend(mecha_closed)

    def get_mecha_is_enable(self, mecha_id):
        in_local_battle = global_data.player.in_local_battle()
        if in_local_battle:
            return mecha_id == 8001
        in_exercise = self.battle_type == game_mode_const.GAME_MODE_EXERCISE
        is_competition = global_data.battle and global_data.battle.get_is_competition()
        if self.battle_type == game_mode_const.GAME_MODE_RANDOM_DEATH:
            can_use = False
            if global_data.death_battle_data:
                can_use = global_data.death_battle_data.get_mecha_is_enable(mecha_id)
        else:
            can_use = has_mecha(global_data.player.logic, mecha_id) or mecha_id in self.share_mecha_lst
        return in_exercise or can_use or is_competition

    def get_mecha_is_created(self, mecha_id):
        return mecha_id in six.itervalues(self.created_mecha)

    def get_mecha_btn_pos_by_index(self, index):
        offset_x = index * self.MECHA_OFFSET_X
        offset_y = -(index % 2) * self.MECHA_OFFSET_Y
        return (
         self._first_mecha_button_pos.x + offset_x, self._first_mecha_button_pos.y + offset_y)

    def get_default_select_mecha_id(self):
        lobby_selected_mecha_id = self.player.get_owner().get_lobby_selected_mecha_id()
        created_mechas = six_ex.values(self.created_mecha)
        if lobby_selected_mecha_id in created_mechas:
            for index, mecha_id in enumerate(self.mecha_order):
                if mecha_id not in created_mechas:
                    return mecha_id

        else:
            return lobby_selected_mecha_id

    def set_mecha_btn_select(self, select_id, ui_item):
        if select_id == self.select_id:
            return
        if not ui_item:
            mecha_ui_item = self.get_mecha_ui_item(select_id) if 1 else ui_item
            return mecha_ui_item or None
        is_created = not self.get_mecha_is_chooseable(select_id)
        if is_created:
            return
        if self.panel.vx_img_mech_switch.GetDisplayFramePath() and not self.panel.IsPlayingAnimation('open'):
            self.panel.PlayAnimation('choose_pic')
        mecha_ui_item.btn_mecha.SetSelect(True)
        mecha_ui_item.PlayAnimation('choose')
        mecha_ui_item.PlayAnimation('loop')
        mecha_ui_item.nd_select.setScale(1.1)

        def hide_light():
            mecha_ui_item.StopAnimation('choose')
            mecha_ui_item.vx_choose_light1.setVisible(False)
            mecha_ui_item.vx_choose_light2.setVisible(False)
            mecha_ui_item.img_choose_light.setVisible(False)

        mecha_ui_item.SetTimeOut(0.5, lambda : hide_light(), tag=201117)
        conf = self.mecha_conf[str(select_id)]
        name = conf.get('name_text_id', '')
        self.panel.lab_name.SetString(name[0])
        self.panel.lab_mech_type.SetString(get_mecha_speciality_desc_str(select_id))
        if global_data.player:
            self.on_select_mecha(global_data.player.id, select_id, False)
        self.update_mecha_picture(select_id)
        if self.select_id:
            btn = self.get_mecha_ui_item(self.select_id)
            if btn:
                btn.btn_mecha.SetSelect(False)
                btn.StopAnimation('choose')
                btn.RecoverAnimationNodeState('choose')
                btn.StopAnimation('loop')
                btn.RecoverAnimationNodeState('loop')
                btn.nd_select.setScale(1)
        self.select_id = select_id
        self.check_btn_call()

    def update_mecha_picture(self, select_id, clothing_id=None):
        img_path = None
        from logic.gutils import dress_utils
        if clothing_id:
            dressed_clothing_id = clothing_id
        else:
            dressed_clothing_id = dress_utils.get_mecha_dress_clothing_id(select_id)
        if dressed_clothing_id is not None:
            img_path = confmgr.get('mecha_conf', 'SkinConfig', 'Content', str(dressed_clothing_id), 'img_path')
        if img_path is None:
            lobby_select_id = dress_utils.battle_id_to_mecha_lobby_id(select_id)
            default_skin = confmgr.get('mecha_conf', 'LobbyMechaConfig', 'Content', str(lobby_select_id), 'default_fashion')
            default_skin_id = default_skin[0]
            img_path = confmgr.get('mecha_conf', 'SkinConfig', 'Content', str(default_skin_id), 'img_path')
        self.panel.nd_mech.img_mech.SetDisplayFrameByPath('', img_path)
        self.panel.vx_img_mech_switch.SetDisplayFrameByPath('', img_path, force_sync=True)
        self.panel.vx_img_mech_switch.SetUniformTexture('CC_Texture0', img_path)
        ui_display_conf = confmgr.get('ui_display_conf', 'MechaSummonUI', 'Content', default={})
        skin_ui_conf = ui_display_conf.get(str(dressed_clothing_id))
        if not skin_ui_conf:
            skin_ui_conf = ui_display_conf.get(str(select_id))
        if skin_ui_conf:
            pos = skin_ui_conf.get('NodePos')
            if pos:
                self.panel.nd_mech.img_mech.SetPosition(*pos)
                self.panel.vx_img_mech_switch.SetPosition(*pos)
            else:
                self.panel.nd_mech.img_mech.ReConfPosition()
                self.panel.vx_img_mech_switch.ReConfPosition()
            scale = skin_ui_conf.get('NodeScale')
            if scale:
                self.panel.nd_mech.img_mech.SetScaleCheckRecord(scale)
                self.panel.vx_img_mech_switch.SetScaleCheckRecord(scale)
            else:
                self.panel.nd_mech.img_mech.ScaleSelfNode()
                self.panel.vx_img_mech_switch.ScaleSelfNode()
        else:
            self.panel.nd_mech.img_mech.ReConfPosition()
            self.panel.vx_img_mech_switch.ReConfPosition()
            self.panel.nd_mech.img_mech.ScaleSelfNode()
            self.panel.vx_img_mech_switch.ScaleSelfNode()
        return

    def on_camera_player_setted(self, *args):
        if global_data.cam_lplayer is None:
            self.close()
        return

    def on_click_close_btn(self, *args):
        if self.disappearing:
            return
        self.disappearing = True
        self.panel.PlayAnimation('quit')
        delay = self.panel.GetAnimationMaxRunTime('quit')
        self.panel.SetTimeOut(delay, lambda : self.close())

    def on_btn_describe(self, *args):
        if self.play_type == battle_const.PLAY_TYPE_DEATH_IMBA:
            global_data.ui_mgr.show_ui('BattleImbaGuideUI', 'logic.comsys.battle')

    def on_btn_call(self, *args):
        from logic.gutils.mecha_utils import try_call_mecha_in_mecha_trans, summon_mecha_call_back
        global_data.emgr.hide_tech_and_module_choose_widget.emit()
        mecha_id = self.select_id
        if not mecha_id:
            return
        else:
            is_created = not self.get_mecha_is_chooseable(mecha_id)
            if is_created:
                global_data.emgr.battle_show_message_event.emit(get_text_by_id(18221))
                self.panel.btn_sure.SetShowEnable(False)
                return
            if self.battle_type == game_mode_const.GAME_MODE_RANDOM_DEATH:
                skin_data = self.get_chosen_skin_data()
                self.player.send_event('E_CALL_SYNC_METHOD', 'select_random_mecha', (mecha_id,), True)
                try_call_mecha_in_mecha_trans(self.player, lambda ui_obj=self, call_mecha_id=mecha_id, force=False, valid_pos=None, specify_skin=skin_data: summon_mecha_call_back(ui_obj, call_mecha_id, force, valid_pos, specify_skin))
                self.close()
            else:
                skin_data = self.get_chosen_skin_data()
                try_call_mecha_in_mecha_trans(self.player, lambda ui_obj=self, call_mecha_id=mecha_id, force=False, valid_pos=None, specify_skin=skin_data: summon_mecha_call_back(ui_obj, call_mecha_id, force, valid_pos, specify_skin))
                add_uiclick_salog('call_mecha', 'from_usual_mecha_list' if self._call_from_usual_mecha else 'from_all_mecha_list')
            return

    def get_chosen_skin_data(self):
        return None

    def update_nd_dir_pos(self):
        self.panel.nd_dir.setContentSize(self.panel.list_choose_mecha.getContentSize())
        self.panel.nd_dir.ChildResizeAndPosition()

    def on_click_expand_btn(self, btn, touch):
        global_data.emgr.hide_tech_and_module_choose_widget.emit()
        if self.is_in_expand_mode:
            self.panel.list_choose_mecha.SetNumPerUnit(2)
            self.panel.btn_right_direction.setRotation(0)
        else:
            self.panel.list_choose_mecha.SetNumPerUnit(5)
            self.panel.btn_right_direction.setRotation(180)
        self.is_in_expand_mode = not self.is_in_expand_mode
        self.panel.list_choose_mecha.FitViewSizeToContainerSize()
        self.update_nd_dir_pos()
        self._list_sview.change_num_per_unit()

    def _on_add_teammate(self, member_id, info):
        self.init_groupmate_mecha()

    def _on_delete_teammate(self, member_id):
        self.on_reset_mecha(member_id, False)
        self.init_groupmate_mecha()

    def _on_update_teammate(self, member_id, info):
        from mobile.common.EntityManager import EntityManager
        from logic.gcommon.common_const.battle_const import ST_IDLE
        if 'created_mecha_type' in info and member_id != self.player.id:
            if info['created_mecha_type']:
                gulag_state = self.player.ev_g_gulag_status()
                if gulag_state is not None and gulag_state != ST_IDLE:
                    return
                ent = EntityManager.getentity(member_id)
                if ent and ent.logic:
                    gulag_state = ent.logic.ev_g_gulag_status()
                    if gulag_state is not None and gulag_state != ST_IDLE:
                        return
                self.on_select_mecha(member_id, info['created_mecha_type'], True)
            else:
                self.on_reset_mecha(member_id)
        return

    def init_groupmate_mecha_normal(self):
        from logic.gutils.mecha_utils import get_groupmate_choosen_mecha_normal
        eid_2_mecha = {}
        if self.eid_2_color:
            for eid, color in six.iteritems(self.eid_2_color):
                mecha_id = self.chosen_mecha.get(color, 0)
                if mecha_id:
                    eid_2_mecha[eid] = mecha_id

        self.eid_2_color, self.created_mecha = get_groupmate_choosen_mecha_normal(self.player, self.mecha_order)
        self.chosen_mecha = {}
        for eid, mecha_id in six.iteritems(eid_2_mecha):
            color = self.eid_2_color.get(eid, None)
            if color is not None:
                self.chosen_mecha[color] = mecha_id

        self.update_groupmate_color_info()
        self.update_selection()
        return

    def update_groupmate_color_info(self):
        created_mecha = {}
        for color, mecha_id in six.iteritems(self.created_mecha):
            if mecha_id:
                created_mecha[mecha_id] = color

        chosen_mecha = {}
        for color, mecha_id in six.iteritems(self.chosen_mecha):
            if mecha_id:
                chosen_mecha.setdefault(mecha_id, set())
                chosen_mecha[mecha_id].add(color)

        self.created_mecha_id_2_color = created_mecha
        self.chosen_mecha_id_2_color_list = chosen_mecha

    def on_select_mecha_normal(self, player_id, mecha_id, is_create):
        if not self.eid_2_color or player_id not in self.eid_2_color:
            return
        else:
            if mecha_id and mecha_id not in self.mecha_order:
                return
            color = self.eid_2_color[player_id]
            clear_mecha_ids = [
             self.chosen_mecha.get(color, 0), self.created_mecha.get(color, 0)]
            self.chosen_mecha[color] = 0 if is_create else mecha_id
            self.created_mecha[color] = mecha_id if is_create else 0
            for mecha_no in clear_mecha_ids:
                if mecha_no is None or mecha_no <= 0:
                    continue
                self.show_selection_info(mecha_no, False)

            self.update_groupmate_color_info()
            self.update_selection()
            return

    def on_reset_mecha_normal(self, player_id, need_refresh=True):
        if not self.eid_2_color or player_id not in self.eid_2_color:
            return
        color = self.eid_2_color[player_id]
        clear_mecha_ids = [
         self.chosen_mecha.get(color, 0), self.created_mecha.get(color, 0)]
        self.chosen_mecha[color] = 0
        self.created_mecha[color] = 0
        for mecha_no in clear_mecha_ids:
            if not mecha_no or mecha_no <= 0:
                continue
            self.show_selection_info(mecha_no, False)

        if need_refresh:
            self.update_groupmate_color_info()
            self.update_selection()

    def update_selection_info(self, mecha_id, creator_color=-1, color_list=(), ui_item=None):
        is_created = creator_color >= 0
        if mecha_id not in self._show_mecha_list:
            return
        else:
            if ui_item is None:
                mecha_ui_item = self.get_mecha_ui_item(mecha_id) if 1 else ui_item
                if not mecha_ui_item:
                    return
                nd_name_list = ('temp_green', 'temp_blue', 'temp_yellow', 'temp_red')
                show_color_list = list(color_list)
                if creator_color != -1 and creator_color not in color_list:
                    show_color_list.append(creator_color)
                max_index = None
                if show_color_list:
                    max_index = min(show_color_list)
                for name in nd_name_list:
                    nd = getattr(mecha_ui_item, name)
                    nd.setVisible(False)

                show_color_list or mecha_ui_item.img_multi_frame.setVisible(False)
            else:
                mecha_ui_item.img_multi_frame.setVisible(True)
            color_to_num = ('1', '3', '4', '2')
            len_num = len(color_to_num)
            for i, color in enumerate(show_color_list):
                name = nd_name_list[i]
                nd = getattr(mecha_ui_item, name)
                nd.setVisible(True)
                nd.lab_num.SetString(color_to_num[color] if color < len_num else '1')
                pic = team_utils.get_mecha_summon_color_pic('gui/ui_res_2/battle_mech/frame_team_%s_2.png', color)
                nd.img_frame_bar.SetDisplayFrameByPath('', pic)
                if color == max_index:
                    frame_pic = team_utils.get_mecha_summon_color_pic('gui/ui_res_2/battle_mech/frame_team_%s.png', color)
                    mecha_ui_item.img_multi_frame.SetDisplayFrameByPath('', frame_pic)

            self.show_selection_info(mecha_id, True, ui_item)
            return

    def show_selection_info(self, mecha_id, is_show, ui_item=None):
        if ui_item is None:
            mecha_ui_item = self.get_mecha_ui_item(mecha_id) if 1 else ui_item
            if mecha_ui_item:
                mecha_ui_item.temp_teammate_choose.setVisible(is_show)
                mecha_ui_item.nd_multi_player.setVisible(is_show)
                is_visible = False
                is_visible = self.get_mecha_is_chooseable(mecha_id) or True
            elif not self.get_mecha_is_enable(mecha_id):
                is_visible = True
            mecha_ui_item.img_lock.setVisible(is_visible)
        return

    def update_selection_normal(self):
        for color, mecha_id in six.iteritems(self.created_mecha):
            if mecha_id:
                self.update_selection_info(mecha_id, color)
                if mecha_id == self.select_id:
                    self.set_call_btn_state(False)

        for mecha_id, color_list in six.iteritems(self.chosen_mecha_id_2_color_list):
            creator_color = self.created_mecha_id_2_color.get(mecha_id, -1)
            self.update_selection_info(mecha_id, creator_color, color_list)

    def update_selection_single_normal(self, mecha_id, ui_item):
        creator_color = self.created_mecha_id_2_color.get(mecha_id, -1)
        color_list = self.chosen_mecha_id_2_color_list.get(mecha_id, [])
        self.update_selection_info(mecha_id, creator_color, color_list, ui_item)

    def get_mecha_is_chooseable_normal(self, mecha_id):
        if self.check_no_multi_mecha_limit():
            return True
        return not self.get_mecha_is_created(mecha_id)

    def check_no_multi_mecha_limit(self):
        if global_data.battle and global_data.battle.is_customed_no_multi_mecha_limit():
            return True
        return False

    def check_call_btn_normal(self):
        is_created = not self.get_mecha_is_chooseable(self.select_id)
        enable = self.get_mecha_is_enable(self.select_id)
        self.set_call_btn_state(enable and not is_created and not bool(self.get_mecha_cd_timer))

    def __check_call_btn_state(self):
        if self._mecha_groupmate_mutex <= 0:
            state = True
        else:
            state = self.mecha_creation_num.get(self.select_id, 0) < self._mecha_groupmate_mutex
        self.set_call_btn_state(state)

    def init_groupmate_mecha_death(self):
        from logic.gutils.mecha_utils import get_groupmate_choosen_mecha_death
        self.mecha_creation_num = get_groupmate_choosen_mecha_death(self.player, self.mecha_order)
        for mecha_id in self._show_mecha_list:
            create_num = self.mecha_creation_num.get(mecha_id, 0)
            self.update_selection_info_death(mecha_id, create_num)

        self.__check_call_btn_state()

    def on_select_mecha_death(self, player_id, mecha_id, is_create):
        if mecha_id not in self.mecha_order:
            return
        num = self.mecha_creation_num.setdefault(mecha_id, 0)
        if is_create:
            num += 1
            self.mecha_creation_num[mecha_id] = num
            self.update_selection_info_death(mecha_id, num)
        self.__check_call_btn_state()

    def on_reset_mecha_death(self, player_id, need_refresh=True):
        if not need_refresh:
            return
        from logic.gutils.mecha_utils import get_groupmate_choosen_mecha_death
        mecha_creation_num = get_groupmate_choosen_mecha_death(self.player, self.mecha_order)
        for mecha_id, mecha_num in six.iteritems(self.mecha_creation_num):
            cur_mecha_num = mecha_creation_num.get(mecha_id, 0)
            if mecha_num != cur_mecha_num:
                self.mecha_creation_num[mecha_id] = cur_mecha_num
                self.update_selection_info_death(mecha_id, cur_mecha_num)

        self.__check_call_btn_state()

    def update_selection_info_death(self, mecha_id, num, ui_item=None):
        if mecha_id not in self._show_mecha_list:
            return
        else:
            if self.battle_type == game_mode_const.GAME_MODE_RANDOM_DEATH:
                return
            if ui_item is None:
                mecha_ui_item = self.get_mecha_ui_item(mecha_id) if 1 else ui_item
                return mecha_ui_item or None
            mecha_ui_item.img_team_5.setVisible(True)
            mecha_ui_item.img_team_5.lab_num_5.SetString(str(num))
            if global_data.battle and global_data.battle.is_customed_no_multi_mecha_limit():
                mecha_ui_item.img_team_5.lab_num.SetString('/-')
            is_enable = self.get_mecha_is_enable(mecha_id)
            chooseable = self.get_mecha_is_chooseable(mecha_id)
            mecha_ui_item.img_lock.setVisible(not is_enable or not chooseable)
            return

    def update_selection_death(self):
        for mecha_id in self._show_mecha_list:
            create_num = self.mecha_creation_num.get(mecha_id, 0)
            self.update_selection_info_death(mecha_id, create_num)

    def update_selection_single_death(self, mecha_id, ui_item):
        create_num = self.mecha_creation_num.get(mecha_id, 0)
        self.update_selection_info_death(mecha_id, create_num, ui_item)

    def get_mecha_is_chooseable_death(self, mecha_id):
        if self.check_no_multi_mecha_limit():
            return True
        else:
            create_num = self.mecha_creation_num.get(mecha_id, 0)
            if self._mecha_groupmate_mutex <= 0:
                return True
            return create_num < self._mecha_groupmate_mutex

    def get_mecha_is_chooseable_mecha_death(self, mecha_id):
        return self.get_mecha_is_chooseable_death(mecha_id)

    def check_call_btn_death(self):
        enable = self.get_mecha_is_enable(self.select_id)
        if self._mecha_groupmate_mutex <= 0:
            state = True
        else:
            check_num = self.mecha_creation_num.get(self.select_id, 0)
            state = check_num < self._mecha_groupmate_mutex
        self.set_call_btn_state(enable and state and not bool(self.get_mecha_cd_timer))

    def check_call_btn_mecha_death(self):
        if self.check_no_multi_mecha_limit():
            self.set_call_btn_state(True)
            return
        bind_mecha_id = global_data.player.logic.ev_g_get_bind_mecha_type()
        if bind_mecha_id and bind_mecha_id == self.select_id:
            self.set_call_btn_state(False)
            return
        self.check_call_btn_death()

    def get_select_mecha_id(self):
        return self.select_id

    def init_groupmate_mecha_exercise(self):
        pass

    def init_groupmate_mecha_ffa(self):
        pass

    def init_groupmate_mecha_assault(self):
        pass

    def set_call_btn_state(self, enable):
        if self.battle_type == game_mode_const.GAME_MODE_RANDOM_DEATH:
            self.panel.btn_sure.SetShowEnable(True)
        else:
            self.panel.btn_sure.SetShowEnable(enable)
        if enable:
            self.panel.PlayAnimation('btn_loop')
        else:
            self.panel.StopAnimation('btn_loop')
            self.panel.vx_btn_sure.setVisible(False)

    def on_update_change_cd(self, cd_type, total_cd, left_time):
        left_time = min(left_time, total_cd)
        self.get_mecha_count_down = left_time
        if self.get_mecha_cd_timer:
            return
        if left_time > 0:

            def reset():
                self.panel.btn_sure.SetEnable(True)
                global_data.emgr.summon_btn_sure_ready_event.emit()
                if self and self.is_valid():
                    self.get_mecha_count_down = 0
                    self.get_mecha_count_down_progress = 0
                    if self.get_mecha_cd_timer:
                        self.panel.btn_sure.stopAction(self.get_mecha_cd_timer)
                        self.get_mecha_cd_timer = None
                return

            def cb(dt):
                if self.get_mecha_count_down < self.get_mecha_count_down_progress:
                    self.get_mecha_count_down_progress -= 0.03 * self.speed_up
                else:
                    self.get_mecha_count_down_progress -= 0.03
                if self.get_mecha_count_down_progress <= 0:
                    reset()

            self.get_mecha_count_down_progress = left_time
            self.get_mecha_cd_timer = self.panel.btn_sure.TimerAction(cb, left_time, reset, interval=0.03)

    def _show_rogue_tips(self, gift_id, click_wpos, x_offset=80):
        if not self._rogue_tips_widget:
            return
        self._rogue_tips_widget.refresh_view(gift_id)
        pos_node = self._rogue_tips_widget.panel
        OFFSET_X = x_offset
        OFFSET_Y = -100
        lpos = pos_node.getParent().convertToNodeSpace(click_wpos)
        pos_node.SetPosition(lpos.x + OFFSET_X, lpos.y + OFFSET_Y)
        self._rogue_tips_widget.show()

    def _hide_rogue_tips(self):
        if not self._rogue_tips_widget:
            return
        self._rogue_tips_widget.hide()

    def keyboard_summon_call_mecha_confirm(self, msg, keycode):
        self.panel.btn_sure.OnClick(self.panel.btn_sure)

    def keyboard_quick_summon(self, index, msg, keycode):
        if not (global_data.player and global_data.player.logic):
            return
        else:
            usual_mecha_ids = global_data.player.get_usual_mecha_ids()
            sel_index = index - 1
            if len(usual_mecha_ids) > sel_index >= 0:
                select_id = usual_mecha_ids[sel_index]
                from logic.gutils.mecha_utils import try_call_mecha_in_mecha_trans, summon_mecha_call_back
                try_call_mecha_in_mecha_trans(global_data.player.logic, lambda ui_obj=self, call_mecha_id=select_id, force=False, valid_pos=None: summon_mecha_call_back(ui_obj, call_mecha_id, force, valid_pos))
            return