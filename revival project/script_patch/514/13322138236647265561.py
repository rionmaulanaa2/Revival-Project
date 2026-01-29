# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/battle_flag_utils.py
from __future__ import absolute_import
from logic.gcommon.item.item_const import DEFAULT_FLAG_FRAME
from logic.gutils.template_utils import update_badge_node, set_ui_show_picture
import logic.gcommon.cdata.dan_data as dan_data
from logic.gutils import item_utils
from logic.gutils import dress_utils
from logic.gutils import role_head_utils
from logic.gutils import career_utils
from common.cfg import confmgr
import game3d
MAX_MEDAL_NUM = 3

def get_battle_info_by_player(player):
    battle_info = {}
    if player:
        cur_role_id = player.get_role()
        clothing_id = dress_utils.get_role_dress_clothing_id(cur_role_id)
        if clothing_id is None:
            clothing_id = confmgr.get('role_info', 'RoleInfo', 'Content', str(cur_role_id), 'default_skin')[0]
        battle_info = {'clan': (
                  player.get_clan_badge(), player.get_clan_name()),
           'skin': clothing_id,
           'name': player.get_name(),
           'dan': player.get_dan_info_by_type(dan_data.DAN_SURVIVAL),
           'frame': player.get_battle_flag_frame(),
           'medal': player.get_battle_flag_medal(),
           'rank_use_title_dict': player.rank_use_title_dict,
           'uid': str(player.uid),
           'mecha_skin': player.get_lobby_mecha_skin(),
           'priv_lv': player.get_privilege_level(),
           'priv_settings': player.get_privilege_setting(),
           'head_frame': player.get_head_frame(),
           'head_photo': player.get_head_photo()
           }
    return battle_info


def init_battle_flag_template(battle_flag_info, nd):
    from logic.gutils import template_utils
    from logic.gcommon.common_const import rank_const
    from logic.gutils.new_template_utils import get_show_uid
    badge, clan_name = battle_flag_info.get('clan', (0, ''))
    player_name = battle_flag_info.get('name', '')
    dan_info = battle_flag_info.get('dan')
    battle_frame = battle_flag_info.get('frame', DEFAULT_FLAG_FRAME())
    medal = battle_flag_info.get('medal', [])
    clothing_id = battle_flag_info.get('skin')
    uid = battle_flag_info.get('uid', None)
    rank_info = rank_const.get_rank_use_title(battle_flag_info.get('rank_use_title_dict', {}))
    rank_title_type = rank_const.get_rank_use_title_type(battle_flag_info.get('rank_use_title_dict', {}))
    if badge:
        nd.temp_crew_logo and update_badge_node(badge, nd.temp_crew_logo)
    nd.temp_crew_logo and nd.temp_crew_logo.setVisible(bool(clan_name))
    nd.lab_crew_name and nd.lab_crew_name.SetString(clan_name)
    nd.lab_role_name and nd.lab_role_name.SetString(player_name)
    if uid is not None:
        nd.lab_role_id and nd.lab_role_id.SetString(get_text_by_id(80623) + get_show_uid(uid))
    else:
        nd.lab_role_id and nd.lab_role_id.SetString('')
    nd.temp_tier and role_head_utils.set_role_dan(nd.temp_tier, dan_info)
    template_utils.init_rank_title(nd.temp_title, rank_title_type, rank_info)
    set_ui_show_picture(clothing_id, nd.img_role, nd.img_mech)
    refresh_battle_frame(battle_frame, nd.img_bar)
    refresh_battle_front_frame(battle_frame, nd.img_front)
    is_avatar = battle_flag_info.get('is_avatar', False)
    refresh_medals(medal, nd, is_avatar)
    return


def init_battle_flag_template_new(battle_flag_info, nd, enable_click=True, from_battle=False):
    from logic.gcommon.common_const import rank_const
    from logic.gutils import template_utils
    from logic.gcommon.const import PRIV_SHOW_BADGE
    from logic.gutils.role_head_utils import init_privilege_badge, init_role_head
    from logic.gutils.new_template_utils import get_show_uid
    badge, clan_name = battle_flag_info.get('clan', (0, ''))
    dan_info = battle_flag_info.get('dan')
    battle_frame = battle_flag_info.get('frame', DEFAULT_FLAG_FRAME())
    role_skin = battle_flag_info.get('skin')
    mecha_skin = battle_flag_info.get('mecha_skin', 201800100)
    priv_lv = battle_flag_info.get('priv_lv', 0) or 0
    priv_settings = battle_flag_info.get('priv_settings', {}) or {}
    show_badge = priv_settings.get(PRIV_SHOW_BADGE, False)
    rank_info = rank_const.get_rank_use_title(battle_flag_info.get('rank_use_title_dict', {}))
    rank_title_type = rank_const.get_rank_use_title_type(battle_flag_info.get('rank_use_title_dict', {}))
    head_photo = battle_flag_info.get('head_photo', 0)
    head_frame = battle_flag_info.get('head_frame', 0)
    player_name = battle_flag_info.get('name', '')
    uid = battle_flag_info.get('uid', None)
    if battle_flag_info.get('show_uid') and uid is not None:
        nd.lab_role_id and nd.lab_role_id.SetString(get_text_by_id(80623) + get_show_uid(uid))
        nd.lab_role_id and nd.lab_role_id.setVisible(True)
    else:
        nd.lab_role_id and nd.lab_role_id.SetString('')
        nd.lab_role_id and nd.lab_role_id.setVisible(False)
    if battle_flag_info.get('hide_head'):
        nd.temp_head.setVisible(False)
    else:
        init_role_head(nd.temp_head, head_frame, head_photo)

        @nd.temp_head.unique_callback()
        def OnClick(*args):
            if not enable_click:
                return
            ui = global_data.ui_mgr.show_ui('ChangeHeadUI', 'logic.comsys.role')
            ui.on_tab_selected(1)

    if badge:
        nd.temp_crew_logo and update_badge_node(badge, nd.temp_crew_logo)
    nd.temp_crew_logo and nd.temp_crew_logo.setVisible(bool(clan_name))
    nd.temp_tier and role_head_utils.set_role_dan(nd.temp_tier, dan_info)
    template_utils.init_rank_title(nd.temp_title, rank_title_type, rank_info)
    forbid_img_flag = False
    if global_data.is_32bit and from_battle:
        forbid_img_flag = True
    set_ui_show_picture(role_skin, role_nd=nd.img_role, forbid_img=forbid_img_flag)
    set_ui_show_picture(mecha_skin, mecha_nd=nd.img_mech, forbid_img=forbid_img_flag)
    refresh_battle_frame(battle_frame, nd.img_bar, forbid_img=forbid_img_flag)
    refresh_battle_front_frame(battle_frame, nd.img_front, forbid_img=forbid_img_flag)
    if battle_flag_info.get('show_name'):
        nd.lab_role_name.SetString(player_name)
        nd.lab_role_skin_name.setVisible(False)
        nd.lab_role_name.setVisible(True)
    else:
        nd.lab_role_skin_name.SetString(player_name)
        nd.lab_role_skin_name.setVisible(True)
        nd.lab_role_name.setVisible(False)
    if priv_lv > 0 and show_badge:
        init_privilege_badge(nd.temp_badge, priv_lv, show_badge)
        nd.temp_badge.setVisible(True)
    else:
        nd.temp_badge.setVisible(False)

    @nd.nd_touch.unique_callback()
    def OnClick(*args):
        if not enable_click:
            return
        role_visible = not nd.nd_role_locate.isVisible()
        mecha_visible = not role_visible
        nd.nd_role_locate.setVisible(role_visible)
        nd.nd_mech_locate.setVisible(mecha_visible)

    nd.nd_role_locate.setVisible(False)
    nd.nd_mech_locate.setVisible(True)
    nd.lab_mecha_skin_name.setVisible(False)
    return


def init_battle_flag_tempate_share(battle_flag_info, nd, is_role):
    from logic.gcommon.common_const import rank_const
    from logic.gutils import template_utils
    from logic.gcommon.const import PRIV_SHOW_BADGE
    from logic.gutils.role_head_utils import init_privilege_badge, init_role_head
    from logic.gutils.item_utils import get_lobby_item_name
    badge, clan_name = battle_flag_info.get('clan', (0, ''))
    dan_info = battle_flag_info.get('dan')
    battle_frame = battle_flag_info.get('frame', DEFAULT_FLAG_FRAME())
    role_skin = battle_flag_info.get('skin')
    mecha_skin = battle_flag_info.get('mecha_skin')
    priv_lv = battle_flag_info.get('priv_lv', 0) or 0
    priv_settings = battle_flag_info.get('priv_settings', {}) or {}
    show_badge = priv_settings.get(PRIV_SHOW_BADGE, False)
    rank_info = rank_const.get_rank_use_title(battle_flag_info.get('rank_use_title_dict', {}))
    rank_title_type = rank_const.get_rank_use_title_type(battle_flag_info.get('rank_use_title_dict', {}))
    head_photo = battle_flag_info.get('head_photo')
    head_frame = battle_flag_info.get('head_frame')
    player_name = battle_flag_info.get('name', '')
    init_role_head(nd.temp_head, head_frame, head_photo)
    if badge:
        nd.temp_crew_logo and update_badge_node(badge, nd.temp_crew_logo)
    nd.temp_crew_logo and nd.temp_crew_logo.setVisible(bool(clan_name))
    nd.temp_tier and role_head_utils.set_role_dan(nd.temp_tier, dan_info)
    template_utils.init_rank_title(nd.temp_title, rank_title_type, rank_info)
    set_ui_show_picture(role_skin, role_nd=nd.img_role)
    set_ui_show_picture(mecha_skin, mecha_nd=nd.img_mech)
    refresh_battle_frame(battle_frame, nd.img_bar)
    refresh_battle_front_frame(battle_frame, nd.img_front)
    nd.lab_role_skin_name.SetString(player_name)
    if priv_lv > 0 and show_badge:
        init_privilege_badge(nd.temp_badge, priv_lv, show_badge)
        nd.temp_badge.setVisible(True)
    else:
        nd.temp_badge.setVisible(False)
    nd.nd_role_locate.setVisible(is_role)
    nd.nd_mech_locate.setVisible(not is_role)
    nd.lab_role_skin_name.setVisible(True)
    nd.lab_mecha_skin_name.setVisible(False)


def refresh_battle_frame(frame_id, nd, forbid_img=False):
    if forbid_img:
        return
    nd.SetDisplayFrameByPath('', 'gui/ui_res_2/battle_flag/flag_bar/%d.png' % int(frame_id))


def refresh_battle_front_frame(frame_id, nd, forbid_img=False):
    if forbid_img:
        return
    nd.SetDisplayFrameByPath('', 'gui/ui_res_2/battle_flag/flag_bar/front_%d.png' % int(frame_id))


def refresh_medals(medal, nd, is_avatar=True):
    nd.list_achi.SetInitCount(MAX_MEDAL_NUM)
    all_items = nd.list_achi.GetAllItem()
    for index, item_widget in enumerate(all_items):
        show = index < len(medal)
        item_widget.nd_life_icon.setVisible(True)
        item_widget.nd_medal.setVisible(show)
        item_widget.nd_content.setVisible(show)
        item_widget.img_empty.setVisible(not show)
        if show:
            if type(medal[index]) is list:
                level = 1
                progress = 0
                cp_reward_idx = None
                if len(medal[index]) == 1:
                    medal_task_id = medal[index]
                elif len(medal[index]) == 2:
                    medal_task_id, level = medal[index]
                elif len(medal[index]) == 3:
                    medal_task_id, level, progress = medal[index]
                else:
                    medal_task_id, level, progress, cp_reward_idx = medal[index]
                    cp_reward_idx = career_utils.badge_cp_reward_idx_ongoing_to_got(cp_reward_idx)
            else:
                medal_task_id = str(medal[index])
                level = career_utils.get_badge_level(medal_task_id)
                progress = career_utils.get_badge_ongoing_max_cur_prog(medal_task_id)
                cp_reward_idx = career_utils.get_badge_got_cp_reward_idx(medal_task_id)
            career_utils.refresh_badge_item(item_widget, medal_task_id, level, cp_reward_idx=cp_reward_idx, check_got=False, ban_anim=True, is_avatar=is_avatar)

            @item_widget.btn.unique_callback()
            def OnClick(btn, touch, medal_task_id=medal_task_id, level=level, cp_reward_idx=cp_reward_idx, progress=progress):
                position = touch.getLocation()
                extra_info = {'name_txt': career_utils.get_badge_name_text(medal_task_id),'desc_txt': ''.join([get_text_by_id(81755), ':', str(progress)]),
                   'show_desc': career_utils.get_badge_desc_text_by_lv(medal_task_id, level),
                   'is_flag': True,
                   'level': level,
                   'cp_reward_idx': cp_reward_idx,
                   'show_jump': False
                   }
                global_data.emgr.show_item_desc_ui_event.emit(medal_task_id, None, position, extra_info)
                return True

    return


def init_projection_kill_template(projection_info, nd):
    mecha_skin_no = projection_info.get('mecha_skin_no')
    set_ui_show_picture(mecha_skin_no, mecha_nd=nd.img_pic)
    char_name = projection_info.get('char_name', '')
    nd.lab_name.SetString(char_name)
    total_kill = projection_info.get('total_kill', 0)
    nd.lab_honour.SetString(get_text_by_id(634747) + str(total_kill))


_HASH = game3d.calc_string_hash('Tex0')

def play_projection_kill_sfx(model, tex):

    def cb(*args):
        if tex and model and model.valid:
            model.all_materials.set_technique(1, 'shader/battle_flag.nfx::TShader')
            model.all_materials.set_texture(_HASH, 'Tex0', tex)

    def cb2(*args):
        if tex and model and model.valid:
            model.all_materials.set_texture(_HASH, 'Tex0', tex)

    global_data.sfx_mgr.create_sfx_on_model('effect/fx/niudan/quanxi/quanxi_002.sfx', model, 'fx_root', on_create_func=cb2, on_remove_func=cb)