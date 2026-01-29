# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/concert/ArenaApplyUI.py
from __future__ import absolute_import
from common.uisys.basepanel import BasePanel
from common.const.uiconst import NORMAL_LAYER_ZORDER, UI_VKB_CLOSE
from logic.gutils.template_utils import init_tempate_mall_i_item
from mobile.common.EntityManager import EntityManager
from logic.gutils import role_head_utils
import cc

class ArenaApplyUI(BasePanel):
    PANEL_CONFIG_NAME = 'battle_arena/battle_arena_ready'
    DLG_ZORDER = NORMAL_LAYER_ZORDER
    UI_VKB_TYPE = UI_VKB_CLOSE
    UI_ACTION_EVENT = {'temp_btn_close.btn_back.OnClick': 'on_close',
       'btn_go.btn_common.OnClick': 'on_send',
       'btn_give_up.btn_common_big.OnClick': 'on_give_up'
       }
    MOUSE_CURSOR_TRIGGER_SHOW = True
    GLOBAL_EVENT = {'scene_player_setted_event': 'on_player_setted'
       }
    HOT_KEY_FUNC_MAP = {'scene_interaction': 'keyboard_interaction'
       }

    def on_init_panel(self, *args, **kwargs):
        self.init_parameters()
        self.hide_main_ui(['SceneInteractionUI'])
        self.panel.PlayAnimation('show')
        self.process_event(True)
        self.init_panel()

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'update_battle_data': self.update_battle_data
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_finalize_panel(self):
        self.remove_blocking_ui_list()
        self.process_event(False)
        self.unregister_event()
        self.show_main_ui()

    def init_parameters(self):
        self.lplayer = None
        self.arena_entity_id = None
        return

    def init_panel(self):
        self.add_blocking_ui_list(['ArenaWaitUI'])
        play_data = global_data.game_mode.get_cfg_data('play_data')
        if play_data:
            duel_reward = play_data.get('duel_reward', [])
            winer_reward = duel_reward.get('winer', [])
            loser_reward = duel_reward.get('loser', [])
            self.panel.list_price.SetInitCount(len(winer_reward) + len(loser_reward))
            for i, reward_info in enumerate(winer_reward):
                item_id, num = reward_info
                item = self.panel.list_price.GetItem(i)
                init_tempate_mall_i_item(item, item_id, item_num=num)

            for i, reward_info in enumerate(loser_reward):
                i += len(winer_reward)
                item_id, num = reward_info
                item = self.panel.list_price.GetItem(i)
                init_tempate_mall_i_item(item, item_id, item_num=num)

        from logic.client.const import game_mode_const
        if global_data.game_mode and global_data.game_mode.is_mode_type(game_mode_const.GAME_MODE_CONCERT):
            self.panel.lab_detail_3.SetString(get_text_by_id(83196))
        else:
            self.panel.lab_detail_3.SetString(get_text_by_id(610223))
        self.update_battle_data()

        @self.panel.unique_callback()
        def OnClick(btn, touch):
            self.close()

    def set_arena_entity_id(self, entity_id):
        self.arena_entity_id = entity_id
        self.panel.stopAllActions()
        lplayer = None
        if global_data.player:
            lplayer = global_data.player.logic
        self.on_player_setted(lplayer)
        self.start_check_pos_player()
        return

    def close(self, *args):
        self.panel.PlayAnimation('disappear')
        appear_time = self.panel.GetAnimationMaxRunTime('disappear')

        def cb():
            if self and self.is_valid():
                super(ArenaApplyUI, self).close(*args)

        self.panel.DelayCall(appear_time, cb)

    def keyboard_interaction(self, msg, keycode):
        self.close()

    def on_player_setted(self, lplayer):
        self.unregister_event()
        if lplayer is None:
            return
        else:
            self.lplayer = lplayer
            self.register_event()
            return

    def register_event(self):
        if not self.lplayer:
            return
        register_event = self.lplayer.regist_event

    def unregister_event(self):
        if not self.lplayer:
            return
        unregister_event = self.lplayer.unregist_event

    def on_close(self, btn, touch):
        self.close()

    def on_send(self, btn, touch):
        if not global_data.player:
            return
        bat = global_data.player.get_battle() or global_data.player.get_joining_battle()
        if bat:
            bat.req_duel()

    def on_give_up(self, btn, touch):
        from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2

        def callback():
            bat = global_data.player.get_battle() or global_data.player.get_joining_battle()
            if bat:
                bat.cancel_duel()

        SecondConfirmDlg2().confirm(content=get_text_by_id(609907), confirm_callback=callback)

    def start_check_pos_player(self):
        self.panel.runAction(cc.RepeatForever.create(cc.Sequence.create([
         cc.CallFunc.create(self.check_pos),
         cc.DelayTime.create(1)])))

    def check_pos(self):
        if self.arena_entity_id:
            arena_ent = EntityManager.getentity(self.arena_entity_id)
            if arena_ent and arena_ent.logic and global_data.player and global_data.player.logic:
                pos = global_data.player.logic.ev_g_position()
                if pos:
                    is_enter, _ = arena_ent.logic.ev_g_check_enter_consoloe_zone(pos)
                    if is_enter:
                        return
        self.close()

    def update_battle_data(self):
        if not global_data.player:
            return
        else:
            bat = global_data.player.get_battle() or global_data.player.get_joining_battle()
            if not bat:
                return
            king, defier, duel_queue, king_info = bat.get_battle_data()
            self_id = global_data.player.id
            is_in_queue = bat.is_in_queue()
            self.panel.btn_go.setVisible(not is_in_queue)
            self.panel.btn_give_up.setVisible(is_in_queue)
            has_king = bool(king)
            if has_king:
                self.update_photo(self.panel.temp_boss, king)
            self.panel.temp_boss.nd_empty.setVisible(not has_king)
            self.panel.temp_boss.nd_player.setVisible(has_king)
            if defier:
                all_queue = [
                 defier] + duel_queue
            else:
                all_queue = duel_queue
            self.panel.list_queue.SetInitCount(5)
            if bat.is_full_queue():
                self.panel.btn_go.btn_common.SetText(13114)
                self.panel.btn_go.btn_common.SetEnable(False)
            else:
                self.panel.btn_go.btn_common.SetText(80560)
                self.panel.btn_go.btn_common.SetEnable(True)
            self_index = -1
            new_all_queue = [None, None, None, None, None]
            for i, id in enumerate(all_queue):
                if i < len(new_all_queue):
                    new_all_queue[i] = id
                if self_id == id:
                    self_index = i
                    self.panel.lab_position.setVisible(True)
                    self.panel.lab_number_1.setVisible(True)
                    self.panel.lab_number_1.SetString(str(self_index + 1))

            if self_index == -1:
                self.panel.lab_position.setVisible(False)
                self.panel.lab_number_1.setVisible(False)
            queue_len = len(all_queue)
            if queue_len > 5:
                if self_index < 4:
                    new_all_queue[4] = 'omit'
                else:
                    new_all_queue[3] = 'omit'
                    new_all_queue[4] = self_id
            for i, item in enumerate(self.panel.list_queue.GetAllItem()):
                item.pnl_challenge.setVisible(False)
                item.nd_symbo.setVisible(False)
                if i == 0 and defier:
                    item.pnl_challenge.setVisible(True)
                elif new_all_queue[i] == 'omit':
                    item.nd_empty.setVisible(False)
                    item.nd_player.setVisible(False)
                    item.nd_symbo.setVisible(True)
                    continue
                id = new_all_queue[i]
                if id:
                    self.update_photo(item, id)
                    item.nd_empty.setVisible(False)
                    item.nd_player.setVisible(True)
                else:
                    item.nd_empty.setVisible(True)
                    item.nd_player.setVisible(False)
                if self_id == id:
                    item.lab_name.SetColor(4055551)
                    item.img_blue.setVisible(True)
                    item.temp_head.img_role_bar.SetDisplayFrameByPath('', 'gui\\ui_res_2\\battle_arena\\battle_arena_ready\\img_arena_me.png')
                else:
                    item.lab_name.SetColor(14604536)
                    item.img_blue.setVisible(False)
                    item.temp_head.img_role_bar.SetDisplayFrameByPath('', 'gui\\ui_res_2\\item\\ui_item\\bar30100000.png')

            self.panel.lab_win_num.SetString(str(king_info[0]))
            self.panel.lab_join_num.SetString(str(king_info[1]))
            self.panel.lab_keep_num.SetString(str(king_info[2]))
            return

    def update_photo(self, ui_item, entity_id):
        if not entity_id:
            return
        player = EntityManager.getentity(entity_id)
        if not (player and player.logic):
            return
        char_name = player.logic.ev_g_char_name()
        head_frame = player.logic.ev_g_head_frame()
        head_photo = player.logic.ev_g_head_photo()
        role_head_utils.init_role_head(ui_item.temp_head, head_frame, head_photo)
        ui_item.lab_name.SetString(char_name)