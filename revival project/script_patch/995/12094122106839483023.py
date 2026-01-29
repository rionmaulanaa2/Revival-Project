# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/activity/ActivityAccumulateChargeCircle.py
from __future__ import absolute_import
import six
from six.moves import range
from logic.comsys.activity.ActivityTemplate import ActivityBase
from logic.gcommon.common_utils.local_text import get_text_by_id
from logic.gutils import task_utils, template_utils, activity_utils
from common.cfg import confmgr
from logic.gutils.item_utils import get_money_icon, get_lobby_item_name, get_lobby_item_pic_by_item_no, get_skin_rare_degree_icon, get_lobby_item_type
from logic.gcommon.const import SHOP_PAYMENT_YUANBAO
from logic.gcommon.item import lobby_item_type
from logic.gcommon.time_utility import get_readable_time, get_readable_time_day_hour_minitue, ONE_HOUR_SECONS
from common.utils.timer import CLOCK
from logic.client.const import lobby_model_display_const
from logic.gcommon.common_const import scene_const
from logic.gutils import items_book_utils
from logic.gutils import lobby_model_display_utils
COMMON_ITEM_CNT = 7
ONE_COMMON_ITEM_PERCENT = 75.0 / (COMMON_ITEM_CNT - 1)
ONE_SPECIAL_ITEM_PERCENT = 100

def refresh_show_effect(skin_no, effect_id):
    if not skin_no:
        from logic.gcommon.item.item_const import AIRCRAFT_SKIN_TYPE
        parachute_type = AIRCRAFT_SKIN_TYPE
        item_fashion_no = global_data.player.get_glide_show_aircaft_id() or items_book_utils.get_item_fashion_no(parachute_type)
        skin_no = item_fashion_no
    if not skin_no:
        return
    global_data.emgr.change_glide_sfx_tag_effect_event.emit(skin_no, effect_id)


class ChargeSceneHelper(object):

    def __init__(self, scene_type, scene_path, scene_content_type, display_type=lobby_model_display_const.ART_COLLECTION, texture='', ui_name=''):
        self._is_valid = True
        self._scene_type = scene_type
        self._scene_path = scene_path
        self._scene_content_type = scene_content_type
        self._display_type = display_type
        self._scene_texture = texture
        self._mecha_id = 8001
        self._skin_id = None
        self._models_data = []
        self._boxes = []
        self._support_mirror = []
        self._ui_name = ui_name or self.__class__.__name__
        self.timer = None
        self._load_callback = None
        self._is_model_loaded = False
        self.is_trk_end = False
        return

    def destroy(self):
        self.stop_loop()
        self._is_valid = False
        self._models_data = []
        self._boxes = []
        self._support_mirror = []
        self._ui_name = ''
        self._load_callback = None
        return

    def set_mecha_show_data(self, mecha_id, skin_id=-1, boxes=('box_luckypass_01', ), support_mirror=(True,), load_callback=None):
        self._mecha_id = mecha_id
        self._skin_id = skin_id
        from logic.gutils import dress_utils, lobby_model_display_utils
        item_no = dress_utils.get_mecha_skin_item_no(mecha_id, skin_id)
        model_data = lobby_model_display_utils.get_lobby_model_data(item_no)
        for data in model_data:
            data['show_anim'] = data['end_anim'] or 'idle'

        self._models_data = [
         model_data]
        self._boxes = boxes
        self._support_mirror = support_mirror
        self._load_callback = load_callback

    def set_show_data(self, model_data, boxes=('box_luckypass_01', ), support_mirror=(True,), load_callback=None):
        self._models_data = model_data
        self._boxes = boxes
        self._support_mirror = support_mirror
        self._load_callback = load_callback

    def _change_scene(self):
        if self._scene_path:
            p = self._scene_path
            if self._scene_content_type and self._scene_texture:
                content_scene_res_config = confmgr.get('lobby_model_display_conf', 'SceneConfig', 'Content', str(self._scene_content_type), default={})
                bg_model_name = content_scene_res_config.get('bg_model_name')
                global_data.emgr.show_disposable_lobby_relatived_scene.emit(self._scene_type, p, self._display_type, belong_ui_name=self._ui_name, scene_background_texture=self._scene_texture, bg_model_name=bg_model_name)
            else:
                global_data.emgr.show_disposable_lobby_relatived_scene.emit(self._scene_type, p, self._display_type, belong_ui_name=self._ui_name)
        else:
            global_data.emgr.show_lobby_relatived_scene.emit(self._scene_type, self._display_type, scene_content_type=self._scene_content_type, scene_background_texture=self._scene_texture)

    def _do_show_model(self):
        if not global_data.player:
            return
        models = self._models_data
        boxs = list(self._boxes)
        support_mirror = list(self._support_mirror)
        if boxs:
            if models:
                global_data.emgr.change_model_display_scene_item_customized.emit(models, boxs, support_mirror, create_callback=self._on_load_model_success)
        elif models:
            global_data.emgr.change_model_display_scene_item.emit(models, load_callback=self._on_load_model_success)

    def load_and_show_model(self):
        self._do_show_model()

    def clear_model_show(self):
        off_position = [
         -200, 0, 0]
        global_data.emgr.change_model_display_off_position.emit(off_position, False)

    def recover_model_show(self):
        global_data.emgr.change_model_display_off_position.emit([0, 0, 0], False)

    def leave_scene(self):
        self._is_model_loaded = False
        global_data.emgr.close_model_display_scene.emit()
        global_data.emgr.leave_current_scene.emit()

    def _on_load_model_success(self, model):
        self._is_model_loaded = True
        if self._load_callback:
            self._load_callback()

    def is_model_loaded(self):
        return self._is_model_loaded

    def set_model_loaded_callback(self, load_callback):
        self._load_callback = load_callback

    def on_show(self):
        self._change_scene()

    def on_hide(self):
        self._is_model_loaded = False
        global_data.emgr.close_model_display_scene.emit()

    def show_enter_sfx(self, sfx_item_no):

        def cb():
            self._is_valid and self.change_effect_choose(str(sfx_item_no))

        if not self.is_model_loaded():
            self.load_and_show_model()
            self.set_model_loaded_callback(cb)
        else:
            self.change_effect_choose(str(sfx_item_no))
            self.recover_model_show()

    def change_effect_choose(self, effect_id=None):
        conf = confmgr.get('display_enter_effect')
        conf = conf.get('Content', {})
        display_enter_config = conf.get(effect_id, {})
        sound_name = display_enter_config.get('cSfxSoundName', '')

        def loop_enter_sfx():
            global_data.emgr.change_model_preview_effect.emit(display_enter_config['lobbyCallOutSfxPath'], sound_name)

        loop_enter_sfx()
        self.stop_loop()
        from common.utils.timer import CLOCK
        self.timer = global_data.game_mgr.register_logic_timer(loop_enter_sfx, interval=10, times=-1, mode=CLOCK)

    def show_kill_sfx(self, sfx_item_no, is_loop=True):
        conf = confmgr.get('items_book_conf', 'KillSfxConfig', 'Content', str(sfx_item_no), default={})
        sfx_path = conf.get('sfx_path', '')
        sfx_scale = conf.get('sfx_scale', 1.0)
        one_time = conf.get('time', 5550 / 1000.0)
        offset = conf.get('sfx_offset', None)

        def single_show():
            if not sfx_path:
                return
            global_data.emgr.change_model_display_scene_tag_effect.emit(sfx_path, sfx_scale=sfx_scale, offset=offset)

        single_show()

        def start_loop():
            self.stop_loop()
            from common.utils.timer import CLOCK
            self.timer = global_data.game_mgr.register_logic_timer(single_show, interval=one_time, times=-1, mode=CLOCK)

        if is_loop:
            start_loop()
        return

    def stop_loop(self):
        if self.timer:
            global_data.game_mgr.unregister_logic_timer(self.timer)
            self.timer = None
        return

    def show_glide_sfx(self, effect_id, skin_no=None, is_loop=True):

        def cb(skin_no=skin_no):
            self.play_glide_model_trk(skin_no, effect_id)

        if not self.is_model_loaded():
            self.load_and_show_model()
            self.set_model_loaded_callback(cb)
        else:
            self.recover_model_show()

    def check_replay_glide_model_trk(self, effect_id):
        if self.is_trk_end:
            self.play_glide_model_trk(None, effect_id)
        return

    def play_glide_model_trk(self, skin_no, effect_id):
        if self._is_valid:
            refresh_show_effect(skin_no, effect_id)

            def circle_trk_callback():
                self.is_trk_end = True

            self.is_trk_end = False
            global_data.emgr.play_model_display_track_event.emit('effect/trk/fxq_001.trk', circle_trk_callback, revert=False, time_scale=1.0, is_additive=False)


class ActivityAccumulateChargeCircle(ActivityBase):

    def __init__(self, dlg, activity_type):
        super(ActivityAccumulateChargeCircle, self).__init__(dlg, activity_type)
        self.init_parameters()
        self.process_event(True)
        self.register_timer()
        self.init_scene()

    def on_init_panel(self):
        super(ActivityAccumulateChargeCircle, self).on_init_panel()
        self.init_all_items()
        self.update_all_items()
        self.update_progress_bar()
        self.init_charge_btn()
        self.init_question_btn()
        self.update_charge_desc()
        self.init_time_widget()
        self.init_switch_preview_btn()
        self.show_preview_item(self.ui_data.get('preview_item', [])[0])
        if self.panel.btn_play:

            @self.panel.btn_play.callback()
            def OnClick(btn, touch):
                if self._scene_helper:
                    self._scene_helper.check_replay_glide_model_trk(self._cur_preview_item)

    def on_finalize_panel(self):
        self.process_event(False)
        self.unregister_timer()
        super(ActivityAccumulateChargeCircle, self).on_finalize_panel()
        self.prog_2_reward_id = {}
        self.rewards_progs = []
        self.destroy_preview_item()
        self._scene_helper.leave_scene()
        self._scene_helper.destroy()
        self._scene_helper = None
        return

    def init_parameters(self):
        conf = confmgr.get('c_activity_config', self._activity_type)
        self.ui_data = conf.get('cUiData', {})
        self.desc_id = conf.get('cRuleTextID')
        self.task_id = conf.get('cTask')
        self.rewards_progs = task_utils.get_prog_rewards_progs(self.task_id)
        self.prog_2_reward_id = task_utils.get_prog_rewards_in_dict(self.task_id)
        self._timer = 0
        self._timer_cb = {}
        self._cur_preview_item = None
        return

    def need_bg(self):
        return False

    def on_main_ui_reshow(self):
        self.set_show(True)

    def on_main_ui_hide(self):
        self.set_show(False)

    def set_show(self, show, is_init=False):
        super(ActivityAccumulateChargeCircle, self).set_show(show)
        if not show:
            self.destroy_preview_item()
            self._scene_helper.on_hide()
        else:
            if not self.panel or not self.panel.isVisible():
                return
            self._scene_helper.on_show()
            self.show_preview_item(self.ui_data.get('preview_item', [])[0])

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'receive_task_prog_reward_succ_event': self.on_receive_task_prog_reward,
           'task_prog_changed': self.on_task_prog_changed
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def register_timer(self):
        self.unregister_timer()
        self._timer = global_data.game_mgr.get_logic_timer().register(func=self.second_callback, interval=1, mode=CLOCK)

    def unregister_timer(self):
        if self._timer > 0:
            global_data.game_mgr.get_logic_timer().unregister(self._timer)
        self._timer = 0
        self._timer_cb = {}

    def second_callback(self):
        for key, cb in six.iteritems(self._timer_cb):
            cb()

    def init_scene(self):
        scene_background_texture = 'model_new/xuanjue/xuanjue_new/textures/zhanshi_beijing_s5_01.tga'
        cur_scene_content_type = scene_const.SCENE_ACTIVITY_LEICHONG
        self._scene_helper = ChargeSceneHelper(scene_const.SCENE_JIEMIAN_COMMON, '', cur_scene_content_type, lobby_model_display_const.LUCKY_HOUSE, texture=scene_background_texture, ui_name=self.__class__.__name__)
        from logic.gutils.dress_utils import battle_id_to_mecha_lobby_id
        from logic.gcommon.item.item_const import FASHION_POS_SUIT
        first_preview_item = self.ui_data.get('preview_item', [])[0]
        item_type = get_lobby_item_type(first_preview_item)
        if not global_data.player:
            return
        if item_type in [lobby_item_type.L_ITEM_KILL_SFX, lobby_item_type.L_ITEM_MECHA_SFX]:
            lobby_mecha_id = global_data.player.get_lobby_selected_mecha_id()
            mecha_item_id = battle_id_to_mecha_lobby_id(lobby_mecha_id)
            mecha = global_data.player.get_item_by_no(mecha_item_id)
            if not mecha:
                return
            fashion = mecha.get_fashion()
            skin_id = fashion.get(FASHION_POS_SUIT, -1)
            self._scene_helper.set_mecha_show_data(mecha_item_id, skin_id)
        elif item_type == lobby_item_type.L_ITEM_GLIDE_EFFECT:
            from logic.gcommon.item.item_const import AIRCRAFT_SKIN_TYPE
            parachute_type = AIRCRAFT_SKIN_TYPE
            item_fashion_no = global_data.player.get_glide_show_aircaft_id() or items_book_utils.get_item_fashion_no(parachute_type)
            model_data = lobby_model_display_utils.get_lobby_model_data(item_fashion_no)
            self._scene_helper.set_show_data(model_data, boxes=[])

    def init_question_btn(self):

        @self.panel.btn_question.unique_callback()
        def OnClick(btn, touch):
            self.on_click_question_btn()

    def init_charge_btn(self):

        @self.panel.btn_get.unique_callback()
        def OnClick(btn, touch):
            self.on_click_charge_btn()

    def update_charge_desc(self):
        cur_prog = global_data.player.get_task_prog(self.task_id)
        btn_text = '<color=0XFFFFFFFF><img ="%s",scale=0.0></color>%d' % (get_money_icon(SHOP_PAYMENT_YUANBAO), cur_prog * 10)
        self.panel.btn_get.lab_now.SetString(''.join([get_text_by_id(81943), ':', btn_text]))
        need_yuanbao = 0
        reward_id = 0
        for prog in self.rewards_progs:
            if cur_prog >= prog:
                continue
            else:
                need_yuanbao = prog - cur_prog
                reward_id = self.prog_2_reward_id[prog]
                break

        reward_conf = confmgr.get('common_reward_data', str(reward_id), default={})
        reward_list = reward_conf.get('reward_list', [])
        if global_data.player.is_task_finished(self.task_id):
            self.panel.lab_rules and self.panel.lab_rules.SetString(609976)
            self.panel.lab_rules.setVisible(True)
            return
        if not reward_list:
            self.panel.lab_rules.setVisible(False)
            return
        item_no, item_num = reward_list[0]
        params = (need_yuanbao * 10, get_lobby_item_name(item_no, need_part_name=False))
        self.panel.lab_rules.setVisible(True)
        self.panel.lab_rules.SetString(get_text_by_id(609972).format(*params))

    def update_one_item(self, idx):
        player = global_data.player
        if not player:
            return
        prog = self.rewards_progs[idx]
        can_receive = player.is_prog_reward_receivable(self.task_id, prog) and not player.has_receive_prog_reward(self.task_id, prog)
        is_received = player.has_receive_prog_reward(self.task_id, prog)
        ui_item = getattr(self.panel.temp_list, 'temp_item_{}'.format(idx + 1))
        ui_item.nd_get_tips.setVisible(can_receive)
        ui_item.nd_get.setVisible(is_received)
        show_special = idx == COMMON_ITEM_CNT
        ui_item.img_get_tips_bar_special.setVisible(show_special)
        ui_item.img_get_tips_bar.setVisible(not show_special)
        if can_receive:
            ui_item.PlayAnimation('get_tips')
        else:
            ui_item.StopAnimation('get_tips')

    def init_one_item(self, idx):
        ui_item = getattr(self.panel.temp_list, 'temp_item_{}'.format(idx + 1))
        prog = self.rewards_progs[idx]
        reward_id = self.prog_2_reward_id[prog]
        reward_conf = confmgr.get('common_reward_data', str(reward_id))
        reward_list = reward_conf.get('reward_list', [])
        item_no, item_num = reward_list[0]
        yuanbao_num = prog * 10
        ui_item.lab_cell_name.SetString(str(yuanbao_num))

        def show_tips_cb(item_no=item_no):
            self.show_preview_item(item_no)

        template_utils.init_template_i_collection_charge_item(ui_item, item_no, item_num=item_num, show_rare_degree=False, show_tips=True, show_tips_cb=show_tips_cb)

        @ui_item.btn_click.unique_callback()
        def OnClick(btn, touch, _prog=prog):
            self.on_click_receive_btn(_prog)

    def update_all_items(self):
        if not self.task_id:
            return
        for idx in range(COMMON_ITEM_CNT + 1):
            self.update_one_item(idx)

    def init_all_items(self):
        if not self.task_id:
            return
        for idx in range(COMMON_ITEM_CNT + 1):
            self.init_one_item(idx)

    def init_switch_preview_btn(self):
        if len(self.ui_data.get('preview_item', [])) <= 1:
            return
        else:
            for i in range(10):
                btn_show = getattr(self.panel, 'btn_show_' + str(i + 1), None)
                if not btn_show:
                    return
                item_no = self.ui_data.get('preview_item', [])[i]
                img_path = get_lobby_item_pic_by_item_no(item_no)
                btn_show.item.SetDisplayFrameByPath('', img_path)

                @btn_show.callback()
                def OnClick(btn, touch, item_no=item_no):
                    self.show_preview_item(item_no)

            return

    def refresh_switch_preview_btn(self, shown_item_no):
        if len(self.ui_data.get('preview_item', [])) <= 1:
            return
        else:
            for i in range(10):
                btn_show = getattr(self.panel, 'btn_show_' + str(i + 1), None)
                if not btn_show:
                    return
                item_no = self.ui_data.get('preview_item', [])[i]
                btn_show.img_select.setVisible(item_no == shown_item_no)

            return

    def init_time_widget(self):
        self._timer_cb[0] = lambda : self.refresh_time(self.task_id)
        self.refresh_time(self.task_id)

    def refresh_time(self, parent_task):
        if not self.panel or not self.panel.lab_time:
            return
        left_time = task_utils.get_raw_left_open_time(parent_task)
        if left_time > 0:
            if left_time > ONE_HOUR_SECONS:
                self.panel.lab_time.SetString(get_text_by_id(607014).format(get_readable_time_day_hour_minitue(left_time)))
            else:
                self.panel.lab_time.SetString(get_text_by_id(607014).format(get_readable_time(left_time)))
        else:
            close_left_time = 0
            self.panel.lab_time.SetString(get_readable_time(close_left_time))

    def update_progress_bar(self):
        percent_0 = 0
        percent_1 = 0
        cur_prog = global_data.player.get_task_prog(self.task_id)
        prog_percent_list = [0, 16, 18, 17, 25]
        percent_0 = 0
        percent_1 = 0
        if cur_prog >= self.rewards_progs[-1]:
            percent_0 = 100
            percent_1 = 100
        elif cur_prog >= self.rewards_progs[-2]:
            percent_0 = 100
            percent_1 = (cur_prog - self.rewards_progs[-2]) / float(self.rewards_progs[-1] - self.rewards_progs[-2]) * 100
        elif cur_prog < self.rewards_progs[0]:
            percent_0 = 0
            percent_1 = 0
        else:
            for idx, prog in enumerate(self.rewards_progs):
                if cur_prog < prog:
                    inner_percent = (cur_prog - self.rewards_progs[idx - 1]) / float(self.rewards_progs[idx] - self.rewards_progs[idx - 1])
                    percent_0 = ONE_COMMON_ITEM_PERCENT * (idx - 1 + inner_percent)
                    break

        percent_0 = int(percent_0)
        percent_1 = int(percent_1)
        self.set_progress_node_percent(self.panel.temp_list.progress_bar, percent_0)
        self.set_progress_node_percent(self.panel.temp_list.progress_bar_01, percent_1)

    def set_progress_node_percent(self, progress_node, percent):
        if hasattr(progress_node, 'SetPercentage') and progress_node.SetPercentage:
            progress_node.SetPercentage(percent)
        else:
            progress_node.SetPercent(percent)

    def on_task_prog_changed(self, changes):
        for change in changes:
            if self.task_id == change.task_id:
                self.update_progress_bar()
                self.update_all_items()
                self.update_charge_desc()
                break

    def on_receive_task_prog_reward(self, task_id, prog):
        if task_id != self.task_id:
            return
        self.update_all_items()

    def on_click_charge_btn(self, *args):
        player = global_data.player
        if not player:
            return
        from logic.gutils import jump_to_ui_utils
        jump_to_ui_utils.jump_to_charge(tab_idx=0)

    def on_click_question_btn(self, *args):
        from logic.comsys.common_ui.GameRuleDescUI import GameRuleDescUI
        dlg = GameRuleDescUI()
        dlg.set_show_rule(get_text_by_id(607171), get_text_by_id(int(self.desc_id)))

    def on_click_receive_btn(self, prog):
        if not activity_utils.is_activity_in_limit_time(self._activity_type):
            return
        player = global_data.player
        if not player:
            return
        player.receive_task_prog_reward(self.task_id, prog)

    def show_preview_item(self, item_no):
        if not (self.panel and self.panel.isValid()):
            return
        if item_no == self._cur_preview_item:
            return
        if item_no not in self.ui_data.get('preview_item', []):
            return
        self.destroy_preview_item()
        self._cur_preview_item = item_no
        self.refresh_switch_preview_btn(item_no)
        self.panel.lab_name.SetString(get_lobby_item_name(item_no, need_part_name=False))
        self.panel.temp_s.bar_level.SetDisplayFrameByPath('', get_skin_rare_degree_icon(item_no))
        item_type = get_lobby_item_type(self._cur_preview_item)
        if item_type == lobby_item_type.L_ITEM_KILL_SFX:
            self._scene_helper.show_kill_sfx(str(item_no), is_loop=True)
        elif item_type == lobby_item_type.L_ITEM_MECHA_SFX:
            self._scene_helper.show_enter_sfx(item_no)
        elif item_type == lobby_item_type.L_ITEM_GLIDE_EFFECT:
            self._scene_helper.show_glide_sfx(str(item_no))

    def destroy_preview_item(self):
        if not self._cur_preview_item:
            return
        else:
            self._scene_helper.clear_model_show()
            item_type = get_lobby_item_type(self._cur_preview_item)
            if item_type == lobby_item_type.L_ITEM_KILL_SFX:
                global_data.emgr.change_model_display_scene_tag_effect.emit('')
                self._scene_helper.stop_loop()
            self._cur_preview_item = None
            return