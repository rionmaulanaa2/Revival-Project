# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/role_skin_utils.py
from __future__ import absolute_import
from common.cfg import confmgr
from common.utils.timer import CLOCK
import world
import game3d
ROLE_SKIN_DICT = {}
_SKIN_SFX_VALUE = 0
_SKIN_MODEL_VALUE = 1
_SKIN_TRIGGER_INTERVAL_RES_INFO = 2

def _register_trigger_at_intervals_sfx_timer(sfx_path, model, socket_list, interval):

    def load_sfx():
        if not model or not model.valid:
            return
        parent_scene = model.get_scene()
        if parent_scene and parent_scene.scene_type == 'LobbyMirror':
            parent_model = global_data.emgr.get_parent_model_of_mirror_model.emit(model)[0]
            if parent_model:
                parent_scene = parent_model.get_scene()
        if parent_scene is not world.get_active_scene():
            return
        for socket in socket_list:
            global_data.sfx_mgr.create_sfx_on_model(sfx_path, model, socket)

    interval = global_data.artist_debug_interval or interval if 1 else global_data.artist_debug_interval
    timer_id = global_data.game_mgr.register_logic_timer(load_sfx, interval=interval, times=-1, mode=CLOCK)
    load_sfx()
    return timer_id


def get_improve_skin_body_path(improved_skin_sfx_id, lod='h'):
    conf = confmgr.get('role_info', 'ImprovedSkinInfo', 'Content', str(improved_skin_sfx_id), default={})
    path = conf.get('improve_body_path', '')
    return path.replace('h.gim', '%s.gim' % lod)


def get_improve_skin_head_id(improved_skin_sfx_id):
    conf = confmgr.get('role_info', 'ImprovedSkinInfo', 'Content', str(improved_skin_sfx_id), default={})
    return conf.get('improve_head_id', None)


def get_improve_skin_pendants_id(improved_skin_sfx_id):
    conf = confmgr.get('role_info', 'ImprovedSkinInfo', 'Content', str(improved_skin_sfx_id), default={})
    return conf.get('improve_pendants_list', [])


def check_update_improve_skin_decs(is_enable_improved, preview_decoration, skin_id):
    from logic.gcommon.item.item_const import FASHION_POS_HEADWEAR, FASHION_POS_BACK, FASHION_POS_SUIT_2, FASHION_OTHER_PENDANT_LIST
    import six
    from logic.gutils.dress_utils import get_pendant_conf, get_improve_pendant_id
    new_decoration = {}
    for pos, item_no in six.iteritems(preview_decoration):

        def try_get_improve_pendant_id(s_id, p_id):
            return get_improve_pendant_id(s_id, p_id) or p_id

        new_item_no = try_get_improve_pendant_id(skin_id, item_no)
        new_decoration[pos] = new_item_no

    event_dict = {FASHION_POS_HEADWEAR: 'change_model_display_head',
       FASHION_POS_BACK: 'change_model_display_bag',
       FASHION_POS_SUIT_2: 'change_model_display_suit'
       }
    other_pendant_need_update = False
    for pos, item_no in six.iteritems(preview_decoration):
        if item_no != new_decoration.get(pos, None):
            if pos in event_dict:
                target_item_no = new_decoration.get(pos, None) if is_enable_improved else item_no
                global_data.emgr.emit(event_dict[pos], target_item_no)
            else:
                other_pendant_need_update = True

    if other_pendant_need_update:
        pendant_id_list = [ new_decoration[pos] if 1 else preview_decoration[pos] for pos in FASHION_OTHER_PENDANT_LIST if pos in new_decoration if is_enable_improved ]
        global_data.emgr.emit('change_display_model_other_pendant', pendant_id_list, skin_id)
    return


def clear_role_skin_model_and_effect(model, clear_trigger_interval=False, improved_skin_id=None):
    model_key = str(model)
    if model_key in ROLE_SKIN_DICT:
        res_list = ROLE_SKIN_DICT[model_key]
        for sub_model in res_list[_SKIN_MODEL_VALUE]:
            if model and model.valid and sub_model and sub_model.valid:
                model.unbind(sub_model)

        res_list[_SKIN_MODEL_VALUE] = []
        for sfx_id in res_list[_SKIN_SFX_VALUE]:
            global_data.sfx_mgr.remove_sfx_by_id(sfx_id)

        res_list[_SKIN_SFX_VALUE] = []
        if clear_trigger_interval:
            for timer_id in res_list[_SKIN_TRIGGER_INTERVAL_RES_INFO]:
                global_data.game_mgr.unregister_logic_timer(timer_id)

            res_list[_SKIN_TRIGGER_INTERVAL_RES_INFO] = []
            clear_trigger_at_intervals_res(model, improved_skin_id)
            ROLE_SKIN_DICT.pop(model_key)


_HASH_light_info = game3d.calc_string_hash('light_info')

def load_role_skin_model_for_shadow(shadow_model, skin_id, light_info):
    conf = confmgr.get('role_info', 'SkinNormalInfo', 'Content', str(skin_id), default={})
    model_key = str(shadow_model)
    sub_model_list = []
    if model_key not in ROLE_SKIN_DICT:
        ROLE_SKIN_DICT[model_key] = [[], [], []]
    for res_info in conf.get('res_info', []):
        only_on = res_info.get('only_on', False)
        if only_on == 'l':
            continue
        socket_list = res_info['socket_list']
        res_path = res_info.get('res_path', '')
        for socket in socket_list:
            if not shadow_model.has_socket(socket):
                continue
            if isinstance(res_path, str) and res_path.endswith('.gim'):
                try:
                    bound_models = shadow_model.get_socket_objects(socket)
                except:
                    continue

                if bound_models:
                    for bound_model in bound_models:
                        shadow_model.unbind(bound_model)

                sub_model = world.model(res_path, None)
                shadow_model.bind(socket, sub_model)
                sub_model.all_materials.set_technique(1, 'shader/plane_shadow.nfx::TShader')
                sub_model.set_rendergroup_and_priority(world.RENDER_GROUP_TRANSPARENT, 10)
                sub_model.visible = True
                sub_model_list.append(sub_model)
                if hasattr(sub_model, 'set_inherit_parent_shaderctrl'):
                    sub_model.set_inherit_parent_shaderctrl(False)
                sub_model.all_materials.set_var(_HASH_light_info, 'light_info', light_info)

    return sub_model_list


def load_normal_skin_model_and_effect(model, skin_id, lod_level):
    conf = confmgr.get('role_info', 'SkinNormalInfo', 'Content', str(skin_id), default={})
    sfx_id_list, sub_model_list = [], []
    model_key = str(model)
    if model_key not in ROLE_SKIN_DICT:
        ROLE_SKIN_DICT[model_key] = [[], [], []]

    def create_sfx_callback(sfx):
        if model and model.valid:
            if not model.visible:
                sfx.visible = False

    for res_info in conf.get('res_info', []):
        only_on = res_info.get('only_on', False)
        if only_on == 'l' and lod_level == 'h':
            continue
        if only_on == 'h' and not lod_level == 'h':
            continue
        sub_socket = res_info.get('sub_socket', None)
        socket_list = res_info['socket_list']
        res_path = res_info.get('res_path', '')
        for socket in socket_list:
            if not sub_socket and not model.has_socket(socket):
                continue
            if isinstance(res_path, str) and res_path.endswith('.gim'):
                if res_path.endswith('h.gim'):
                    res_path = res_path.replace('h.gim', '%s.gim' % lod_level)
                else:
                    res_path = res_path.replace('h_', '%s_' % lod_level)
                if sub_socket == 'head' and lod_level == 'h' or sub_socket and sub_socket != 'head':
                    if model.has_socket(sub_socket):
                        socket_objects = model.get_socket_objects(sub_socket)
                        if socket_objects:
                            socket_obj = socket_objects[0]
                            try:
                                bound_models = socket_obj.get_socket_objects(socket)
                            except:
                                continue

                            if bound_models:
                                for bound_model in bound_models:
                                    socket_obj.unbind(bound_model)

                            sub_model = world.model(res_path, None)
                            socket_obj.bind(socket, sub_model)
                            sub_model_list.append(sub_model)
                else:
                    try:
                        bound_models = model.get_socket_objects(socket)
                    except:
                        continue

                    if bound_models:
                        for bound_model in bound_models:
                            model.unbind(bound_model)

                    sub_model = world.model(res_path, None)
                    model.bind(socket, sub_model)
                    sub_model_list.append(sub_model)
            else:
                sfx_id = global_data.sfx_mgr.create_sfx_on_model(res_path, model, socket, on_create_func=create_sfx_callback)
                sfx_id_list.append(sfx_id)

    for sub_model in sub_model_list:
        if not model.visible:
            sub_model.visible = False

    ROLE_SKIN_DICT[model_key][_SKIN_MODEL_VALUE] = sub_model_list
    ROLE_SKIN_DICT[model_key][_SKIN_SFX_VALUE] = sfx_id_list
    return sub_model_list


def load_improved_skin_model_and_effect(model, improved_skin_sfx_id, auto_load_trigger_at_intervals_res=False, lod_level='l'):
    if not model or not model.valid:
        return []
    else:
        conf = confmgr.get('role_info', 'ImprovedSkinInfo', 'Content', str(improved_skin_sfx_id), default={})
        sfx_id_list, sub_model_list, timer_id_list = [], [], []
        model_key = str(model)
        if model_key not in ROLE_SKIN_DICT:
            ROLE_SKIN_DICT[model_key] = [[], [], []]

        def create_sfx_callback(sfx):
            if model and model.valid:
                if not model.visible:
                    sfx.visible = False

        for res_info in conf.get('permanent_res_info', []):
            sub_socket = res_info.get('sub_socket', None)
            socket_list = res_info.get('socket_list', None)
            res_path = res_info.get('res_path', '')
            res_path_l = res_info.get('res_path_l', '')
            only_on = res_info.get('only_on', None)
            if only_on is not None and (only_on == 'l') ^ (lod_level != 'h'):
                continue
            if lod_level != 'h' and res_path_l:
                res_path = res_path_l
            if not res_path:
                continue
            if socket_list:
                for socket in socket_list:
                    if isinstance(res_path, str) and res_path.endswith('.gim'):
                        if res_path.endswith('h.gim'):
                            res_path = res_path.replace('h.gim', '%s.gim' % lod_level)
                        else:
                            res_path = res_path.replace('h_', '%s_' % lod_level)
                        if sub_socket == 'head' and lod_level == 'h' or sub_socket and sub_socket != 'head':
                            if model.has_socket(sub_socket):
                                socket_objects = model.get_socket_objects(sub_socket)
                                if socket_objects:
                                    socket_obj = socket_objects[0]
                                    try:
                                        bound_models = socket_obj.get_socket_objects(socket)
                                    except:
                                        continue

                                    if bound_models:
                                        for bound_model in bound_models:
                                            socket_obj.unbind(bound_model)

                                    sub_model = world.model(res_path, None)
                                    socket_obj.bind(socket, sub_model)
                                    sub_model_list.append(sub_model)
                        else:
                            try:
                                bound_models = model.get_socket_objects(socket)
                            except:
                                continue

                            if bound_models:
                                for bound_model in bound_models:
                                    model.unbind(bound_model)

                            sub_model = world.model(res_path, None)
                            model.bind(socket, sub_model)
                            sub_model_list.append(sub_model)
                            if 'follow_same_bone' in res_info:
                                sub_model.follow_same_bone_model(model)
                    else:
                        socket_model_name = str(res_info.get('sub_socket', ''))
                        if socket_model_name:
                            socket_models = []
                            if model.has_socket(socket_model_name):
                                socket_models = model.get_socket_objects(socket_model_name)
                            if socket_models:
                                socket_model = socket_models[0]
                                if socket_model:
                                    if isinstance(res_path, dict):
                                        socket_model_path = socket_model.filename.replace('\\', '/')
                                        final_split_char_index = socket_model_path.rfind('/')
                                        socket_model_dir = socket_model_path[:final_split_char_index + 1]
                                        socket_model_filename = socket_model_path[final_split_char_index + 1:]
                                        h_socket_model_filename = 'h' + socket_model_filename[socket_model_filename.find('_'):]
                                        socket_model_h_path = socket_model_dir + h_socket_model_filename
                                        if socket_model_h_path in res_path:
                                            sfx_path = res_path[socket_model_h_path]
                                        else:
                                            continue
                                    else:
                                        sfx_path = res_path
                                    sfx_id = global_data.sfx_mgr.create_sfx_on_model(sfx_path, socket_model, socket, on_create_func=create_sfx_callback, ex_data={'priority': game3d.ASYNC_VERY_HIGH})
                                    sfx_id_list.append(sfx_id)
                            elif lod_level != 'h' and socket_model_name == 'head':
                                sfx_id = global_data.sfx_mgr.create_sfx_on_model(res_path, model, socket, on_create_func=create_sfx_callback, ex_data={'priority': game3d.ASYNC_VERY_HIGH})
                                sfx_id_list.append(sfx_id)
                        else:
                            sfx_id = global_data.sfx_mgr.create_sfx_on_model(res_path, model, socket, on_create_func=create_sfx_callback, ex_data={'priority': game3d.ASYNC_VERY_HIGH})
                            sfx_id_list.append(sfx_id)

            elif isinstance(res_path, str) and res_path.endswith('.gim'):
                if res_path.endswith('h.gim'):
                    res_path = res_path.replace('h.gim', '%s.gim' % lod_level)
                else:
                    res_path = res_path.replace('h_', '%s_' % lod_level)
                if sub_socket and model.has_socket(sub_socket):
                    socket_objects = model.get_socket_objects(sub_socket)
                    if socket_objects:
                        socket_obj = socket_objects[0]
                        socket_obj.add_mesh(res_path)
                else:
                    model.add_mesh(res_path)
            else:
                log_error('')

        ROLE_SKIN_DICT[model_key][_SKIN_MODEL_VALUE] = sub_model_list
        ROLE_SKIN_DICT[model_key][_SKIN_SFX_VALUE] = sfx_id_list
        for sub_model in sub_model_list:
            if not model.visible:
                sub_model.visible = False

        if auto_load_trigger_at_intervals_res:
            for res_info in conf.get('trigger_at_intervals_res_info', []):
                socket_list = res_info['socket_list']
                res_path = res_info['res_path']
                interval = res_info['interval']
                if res_path.endswith('.sfx'):
                    timer_id_list.append(_register_trigger_at_intervals_sfx_timer(res_path, model, socket_list, interval))
                ROLE_SKIN_DICT[model_key][_SKIN_TRIGGER_INTERVAL_RES_INFO] = timer_id_list

        return sub_model_list


def get_skin_trigger_at_intervals_res_info(improved_skin_sfx_id):
    return confmgr.get('role_info', 'ImprovedSkinInfo', 'Content', str(improved_skin_sfx_id), 'trigger_at_intervals_res_info', default=[])


def clear_trigger_at_intervals_res(model, improved_skin_sfx_id):
    if improved_skin_sfx_id is None:
        return
    else:
        if not model or not model.valid:
            return
        conf = get_skin_trigger_at_intervals_res_info(improved_skin_sfx_id)
        for res_info in conf:
            socket_list = res_info['socket_list']
            for socket in socket_list:
                try:
                    bound_res = model.get_socket_objects(socket)
                except:
                    continue

                if bound_res:
                    for res in bound_res:
                        if getattr(res, 'name', None) and res.name.startswith('sfx'):
                            global_data.sfx_mgr.remove_sfx(res)
                        else:
                            model.unbind(res)

        return


def get_skin_improved_sfx_item_id(skin_id):
    return confmgr.get('role_info', 'RoleSkin', 'Content', str(skin_id), 'improved_skin_sfx_item', default=None)


def show_jump_to_improve_skin_dlg(reward_list):
    if not global_data.lobby_player:
        return
    from logic.comsys.common_ui.NormalConfirmUI import SecondConfirmDlg2
    from logic.gcommon.item.item_const import FASHION_POS_SUIT
    from logic.gcommon.common_utils.local_text import get_text_by_id
    from logic.gutils.jump_to_ui_utils import jump_to_skin_improve_ui

    def confirm():
        if global_data.lobby_player:
            fashion_data = global_data.lobby_player.ev_g_fashion_info()
            cur_skin_id = fashion_data.get(FASHION_POS_SUIT, -1)
        else:
            cur_skin_id = -1
        improved_skin_conf = confmgr.get('role_info', 'ImprovedSkinInfo', 'Content')
        jump_skin_id = None
        for item_id, item_count in reward_list:
            correspond_skin_id = improved_skin_conf.get(str(item_id), {}).get('skin_id', None)
            if correspond_skin_id:
                if correspond_skin_id == cur_skin_id:
                    jump_skin_id = cur_skin_id
                    break
                elif jump_skin_id is None:
                    jump_skin_id = correspond_skin_id
                    break

        jump_to_skin_improve_ui(jump_skin_id)
        return

    SecondConfirmDlg2().confirm(content=get_text_by_id(82277), confirm_callback=confirm, cancel_text=get_text_by_id(19002), confirm_text=get_text_by_id(81331), unique_key='improve_skin')


def get_unfold_role_skin_list(role_id):
    ori_skin_list = confmgr.get('role_info', 'RoleInfo', 'Content', str(role_id), 'skin_list')
    conf = confmgr.get('top_role_skin_conf')
    ret_skin_list = set([])
    for skin_id in ori_skin_list:
        fold_skin_list = conf.get(str(skin_id))
        for fold_skin_id in fold_skin_list:
            ret_skin_list.add(fold_skin_id)

    return list(ret_skin_list)


def filter_publish_role_skins(role_id, skin_list):
    role_skin_set = set(confmgr.get('role_info', 'RoleInfo', 'Content', str(role_id), 'skin_list', default=[]))
    role_skins = confmgr.get('role_info', 'RoleSkin', 'Content', default={})
    publish_skin_list = [ skin_id for skin_id in skin_list if skin_id in role_skin_set or role_skins.get(str(skin_id), {}).get('belonging_top_skin_id', None) in role_skin_set ]
    return publish_skin_list


def is_default_role_skin(item_no, role_id):
    default_skin = confmgr.get('role_info', 'RoleInfo', 'Content', str(role_id), 'default_skin') or []
    return item_no in default_skin


EDITOR_SKIN_DICT = {}

def clear_editor_model_effect_and_model(model):
    if not model or not model.valid:
        return
    model_key = str(model)
    if model_key not in EDITOR_SKIN_DICT:
        return
    res_data = EDITOR_SKIN_DICT[model_key]
    for sub_model in res_data[0]:
        model.unbind(sub_model)

    res_data[0] = []
    for sfx_id in res_data[1]:
        global_data.sfx_mgr.remove_sfx_by_id(sfx_id)

    res_data[1] = []
    EDITOR_SKIN_DICT.pop(model_key)


def load_editor_model_effect_and_model(model, sockets_data, lod_level='l'):
    import json
    if not (model and model.valid) or not sockets_data:
        return
    else:
        model_key = str(model)
        sub_model_list, sub_sfx_list = [], []
        for res_info in sockets_data:
            res_info = json.loads(res_info)
            res_path = str(res_info['res_path'])
            socket_list = res_info['socket_list']
            sub_socket = str(res_info.get('sub_socket', ''))
            for socket in socket_list:
                socket = str(socket)
                if res_path.endswith('.gim'):
                    if res_path.endswith('h.gim'):
                        res_path = res_path.replace('h.gim', '%s.gim' % lod_level)
                    else:
                        res_path = res_path.replace('h_', '%s_' % lod_level)
                    if sub_socket and sub_socket != 'head':
                        socket_objects = model.get_socket_objects(sub_socket)
                        if socket_objects:
                            socket_obj = socket_objects[0]
                            bound_models = socket_obj.get_socket_objects(socket)
                            if bound_models:
                                for bound_model in bound_models:
                                    socket_obj.unbind(bound_model)

                                sub_model = world.model(res_path, None)
                                socket_obj.bind(socket, sub_model)
                                sub_model_list.append(sub_model)
                    else:
                        if not model.has_socket(socket):
                            global_data.game_mgr.show_tip('\xe7\xbc\xba\xe5\xb0\x91\xe6\x8c\x82\xe6\x8e\xa5\xe7\x82\xb9{},\xe8\xb5\x84\xe6\xba\x90{}\xe6\x97\xa0\xe6\xb3\x95\xe6\x8c\x82\xe6\x8e\xa5'.format(socket, res_path))
                            continue
                        bound_models = model.get_socket_objects(socket)
                        if bound_models:
                            for bound_model in bound_models:
                                model.unbind(bound_model)

                        sub_model = world.model(res_path, None)
                        model.bind(socket, sub_model)
                        sub_model_list.append(sub_model)
                elif sub_socket and sub_socket != 'head':
                    socket_models = []
                    if model.has_socket(sub_socket):
                        socket_models = model.get_socket_objects(sub_socket)
                        sub_model = socket_models[0]
                        sfx_id = global_data.sfx_mgr.create_sfx_on_model(res_path, sub_model, socket)
                        sub_sfx_list.append(sfx_id)
                else:
                    if not model.has_socket(socket):
                        global_data.game_mgr.show_tip('\xe7\xbc\xba\xe5\xb0\x91\xe6\x8c\x82\xe6\x8e\xa5\xe7\x82\xb9{},\xe8\xb5\x84\xe6\xba\x90{}\xe6\x97\xa0\xe6\xb3\x95\xe6\x8c\x82\xe6\x8e\xa5'.format(socket, res_path))
                        continue
                    sfx_id = global_data.sfx_mgr.create_sfx_on_model(res_path, model, socket)
                    sub_sfx_list.append(sfx_id)

        EDITOR_SKIN_DICT[model_key] = [
         sub_model_list, sub_sfx_list]
        return


def get_glide_effect_socket_data(skin_id, glide_fx_id, key='permanent_res_info'):
    from logic.gcommon.item.item_const import DEFAULT_GLIDE_EFFECT
    skin_id = skin_id or DEFAULT_GLIDE_EFFECT
    isinglepoint = confmgr.get('items_skin_conf', 'VehicleSkinConfig', 'Content', str(skin_id), 'iSinglePoint', default=False)
    sockets_data = confmgr.get('glide_effect_conf', 'GlideSkinInfo', 'Content', str(glide_fx_id), key, default=[])
    new_sockets_data = []
    if isinglepoint:
        for data in sockets_data:
            new_data = dict(data)
            new_data['socket_list'] = new_data['single_socket_list']
            new_sockets_data.append(new_data)

    else:
        new_sockets_data = sockets_data
    return new_sockets_data


GLIDE_SKIN_DICT = {}

def clear_glide_model_effect_and_model(model):
    if not model or not model.valid:
        return
    model_key = str(model)
    if model_key not in GLIDE_SKIN_DICT:
        return
    res_data = GLIDE_SKIN_DICT[model_key]
    for sub_model in res_data[0]:
        model.unbind(sub_model)

    res_data[0] = []
    for sfx_id in res_data[1]:
        global_data.sfx_mgr.remove_sfx_by_id(sfx_id)

    res_data[1] = []
    GLIDE_SKIN_DICT.pop(model_key)


def get_glide_model_effect_and_model(model):
    if not model or not model.valid:
        return
    else:
        model_key = str(model)
        if model_key in GLIDE_SKIN_DICT:
            return GLIDE_SKIN_DICT[model_key]
        return [[], []]


def load_glide_model_effect_and_model(model, sockets_data, lod_level='l', callback=None):
    if not (model and model.valid) or not sockets_data:
        return
    else:
        model_key = str(model)
        sub_model_list, sub_sfx_list = [], []
        for res_info in sockets_data:
            res_path = str(res_info['res_path'])
            socket_list = res_info['socket_list']
            opt_sockets = res_info.get('opt_sockets', ['fx_root'])
            for socket in socket_list:
                socket = str(socket)
                if res_path.endswith('.gim'):
                    if res_path.endswith('h.gim'):
                        res_path = res_path.replace('h.gim', '%s.gim' % lod_level)
                    else:
                        res_path = res_path.replace('h_', '%s_' % lod_level)
                    if not model.has_socket(socket):
                        global_data.game_mgr.show_tip('\xe7\xbc\xba\xe5\xb0\x91\xe6\x8c\x82\xe6\x8e\xa5\xe7\x82\xb9{},\xe8\xb5\x84\xe6\xba\x90{}\xe6\x97\xa0\xe6\xb3\x95\xe6\x8c\x82\xe6\x8e\xa5'.format(socket, res_path))
                        continue
                    bound_models = model.get_socket_objects(socket)
                    if bound_models:
                        for bound_model in bound_models:
                            model.unbind(bound_model)

                    sub_model = world.model(res_path, None)
                    model.bind(socket, sub_model)
                    sub_model_list.append(sub_model)
                else:

                    def unbind_model_socket(sub_model, socket):
                        bound_models = sub_model.get_socket_objects(socket)
                        if bound_models:
                            for bound_model in bound_models:
                                sub_model.unbind(bound_model)
                                bound_model.destroy()

                    def create_sfx_callback(sfx, *args):
                        if callback:
                            callback(sfx)

                    if not model.has_socket(socket):
                        found_in_opt = False
                        for opt_socket in opt_sockets:
                            if model.has_socket(opt_socket):
                                socket_models = model.get_socket_objects(opt_socket)
                                if socket_models:
                                    sub_model = socket_models[0]
                                    if sub_model.has_socket(socket):
                                        unbind_model_socket(sub_model, socket)
                                        if res_path:
                                            sfx_id = global_data.sfx_mgr.create_sfx_on_model(res_path, sub_model, socket, on_create_func=create_sfx_callback)
                                            sub_sfx_list.append(sfx_id)
                                        found_in_opt = True

                        if not found_in_opt:
                            global_data.game_mgr.show_tip('\xe7\xbc\xba\xe5\xb0\x91\xe6\x8c\x82\xe6\x8e\xa5\xe7\x82\xb9{},\xe8\xb5\x84\xe6\xba\x90{}\xe6\x97\xa0\xe6\xb3\x95\xe6\x8c\x82\xe6\x8e\xa5'.format(socket, res_path))
                            continue
                    else:
                        unbind_model_socket(model, socket)
                        if res_path:
                            sfx_id = global_data.sfx_mgr.create_sfx_on_model(res_path, model, socket, on_create_func=create_sfx_callback)
                            sub_sfx_list.append(sfx_id)

        GLIDE_SKIN_DICT[model_key] = [
         sub_model_list, sub_sfx_list]
        return