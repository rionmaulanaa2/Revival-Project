# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gutils/skin_define_utils.py
from __future__ import absolute_import
import six
from common.cfg import confmgr
from logic.gutils.rgb_hsb_utils import hsb_int_2_float_d, hsb_2_rgb
import game3d
import math
import copy
FILTER_SKIN = [
 201800211]
_HASH_TEXDECAL = game3d.calc_string_hash('TexDecal')
_HASH_TEX_INDRECTION = game3d.calc_string_hash('TexDecalIndirection')
_HASH_ORI_TEXTURESIZE = game3d.calc_string_hash('OriTextureSize')
_HASH_TARGET_TEXTURESIZE = game3d.calc_string_hash('TargetTextureSize')
_HASH_INDRECT_SIZE = game3d.calc_string_hash('IndirectSize')
_HASH_INV_INDIRECT_SIZE = game3d.calc_string_hash('InvIndirectSize')
_HASH_TILE_SIZE = game3d.calc_string_hash('TileSize')
_HASH_INV_TILE_SIZE = game3d.calc_string_hash('InvTileSize')
_HASH_TARGET_TEXTURE_ONEPIXEL = game3d.calc_string_hash('TargetTextureOnePixel')
_HASH_TARGET_TEXTURE_TILE = game3d.calc_string_hash('TargetTextureTile')
HASH_COLOR = {'HASH_CHANGE_COLOR_1': game3d.calc_string_hash('changecolor1'),
   'HASH_CHANGE_COLOR_2': game3d.calc_string_hash('changecolor2'),
   'HASH_CHANGE_COLOR_3': game3d.calc_string_hash('changecolor3'),
   'HASH_CHANGE_COLOR_4': game3d.calc_string_hash('changecolor4'),
   'HASH_CHANGE_COLOR_5': game3d.calc_string_hash('changecolor5'),
   'HASH_CHANGE_COLOR_6': game3d.calc_string_hash('changecolor6')
   }
ORIGINAL_SKIN = 1
ADDTIONAL_SKIN = 2
DEFAULT_SKIN = 3
DEFAULT_SKIN_DEFINE_ANIM = {'201800651': 'pose_custome_s01',
   '201800652': 'pose_custome_s01',
   '201800653': 'pose_custome_s01',
   '201802451': 'pose_custome_s02',
   '201802452': 'pose_custome_s02',
   '201802453': 'pose_custome_s02'
   }

def is_default_skin(skin_id):
    conf = confmgr.get('skin_define_color').get(str(skin_id), None)
    if conf:
        skin_type = conf.get('iSkinType')
        if skin_type == DEFAULT_SKIN:
            return True
    return False


def is_main_skin(skin_id):
    conf = confmgr.get('skin_define_color').get(str(skin_id), None)
    if conf:
        skin_type = conf.get('iSkinType')
        if skin_type == ADDTIONAL_SKIN:
            return False
    return True


def is_open_by_clothing_id(clothing_id):
    conf = confmgr.get('skin_define_color').get(str(clothing_id), None)
    return conf is not None


def get_main_skin_id(cur_skin_id):
    cur_skin_conf = confmgr.get('skin_define_color').get(str(cur_skin_id), None)
    if not cur_skin_conf:
        import exception_hook
        msg = 'skin_define_utils----------  =cur_skin_id:%s ' % str(cur_skin_id)
        exception_hook.post_stack(msg)
        return -1
    else:
        skin_type = cur_skin_conf.get('iSkinType')
        if skin_type in (ORIGINAL_SKIN, DEFAULT_SKIN):
            return cur_skin_id
        if skin_type == ADDTIONAL_SKIN:
            return cur_skin_conf.get('iOriginalID')
        return


def get_group_skin_list(cur_skin_id):
    main_skin_id = get_main_skin_id(cur_skin_id)
    main_skin_conf = confmgr.get('skin_define_color').get(str(main_skin_id), None)
    if not main_skin_conf:
        return []
    else:
        group_list = main_skin_conf.get('cOwnList', None)
        own_list = []
        for skin_id in group_list:
            if skin_id in FILTER_SKIN:
                clothing_data = global_data.player.get_item_by_no(skin_id)
                if clothing_data is None:
                    continue
            own_list.append(skin_id)

        return own_list


def get_mecha_skin_rare_degree(skin_id):
    main_skin_id = get_main_skin_id(skin_id)
    return confmgr.get('lobby_item', str(main_skin_id), default={}).get('rare_degree', None)


def get_default_skin_define_anim(skin_id):
    if str(skin_id) in DEFAULT_SKIN_DEFINE_ANIM:
        return DEFAULT_SKIN_DEFINE_ANIM[str(skin_id)]
    return 'pose_custome'


def get_mecha_model_default_scale():
    scene = global_data.game_mgr.scene
    part = scene and scene.get_com('PartModelDisplay')
    model = part and part.model_objs[0].get_model()
    ret = model and model.scale.y
    if not ret:
        return 0.28
    return ret


MAT_IDX = {8009: (201800931, ),
   8025: (201802521, 201802522)
   }

def has_spec_mat_idx(mecha_id):
    return mecha_id in MAT_IDX


def is_spec_mat_idx(mecha_id, skin_id):
    return skin_id in MAT_IDX.get(mecha_id, {})


def get_decal_text_by_item_id(item_id):
    ids = confmgr.get('lobby_item', str(item_id), 'name_id', default=None)
    if ids:
        return ids[0]
    else:
        return


def get_decal_item_id_by_path(path):
    conf = confmgr.get('skin_define_path_decal')._conf
    return int(conf.get(path).get('iItemID'))


def get_decal_path_by_item_id(item_id):
    conf = confmgr.get('skin_define_pure_decal')._conf
    return conf.get(str(item_id)).get('cResPath')


def calc_cur_color_from_hsb(skin_id, tunnel_idx, hsb_value):
    cur_skin_conf = confmgr.get('skin_define_color').get(str(skin_id), {})
    open_tunnel = cur_skin_conf.get('cOpenTunnel', None)
    default_hsb = copy.deepcopy(cur_skin_conf.get('cDefaultHSB', None))
    range_hsb = cur_skin_conf.get('cRangeHSB', None)
    if open_tunnel and default_hsb and range_hsb:
        try:
            idx = open_tunnel.index(tunnel_idx)
            hsb_tunnel = range_hsb[idx][0]
            hsb = default_hsb[idx]
            hsb[hsb_tunnel] = hsb_value
            rgb = hsb_2_rgb(hsb_int_2_float_d(hsb))
            return rgb
        except Exception as e:
            log_error(e)
            return False

    return False


def calc_hash(idx):
    return HASH_COLOR['HASH_CHANGE_COLOR_%d' % idx]


def set_high_quality_model_decal_param(model, indrect_tex, high_decal_tex, ori_texture_size):
    InvIndirectSize = 1 / 256.0
    TileSize = ori_texture_size * InvIndirectSize
    InvTileSize = 1.0 / TileSize
    TargetTextureOnePixel = 1.0 / high_decal_tex.size[0]
    TargetTextureTile = TargetTextureOnePixel * (TileSize + 2.0)
    model.all_materials.set_macro('DECAL_INDIRECT_ENABLE', 'TRUE')
    model.all_materials.set_texture(_HASH_TEXDECAL, 'TexDecal', high_decal_tex)
    model.all_materials.set_texture(_HASH_TEX_INDRECTION, 'TexDecalIndirection', indrect_tex)
    model.all_materials.set_var(_HASH_ORI_TEXTURESIZE, 'OriTextureSize', ori_texture_size * 1.0)
    model.all_materials.set_var(_HASH_INDRECT_SIZE, 'IndirectSize', 256.0)
    model.all_materials.set_var(_HASH_INV_INDIRECT_SIZE, 'InvIndirectSize', InvIndirectSize)
    model.all_materials.set_var(_HASH_TILE_SIZE, 'TileSize', TileSize)
    model.all_materials.set_var(_HASH_INV_TILE_SIZE, 'InvTileSize', InvTileSize)
    model.all_materials.set_var(_HASH_TARGET_TEXTURESIZE, 'TargetTextureSize', high_decal_tex.size[0] * 1.0)
    model.all_materials.set_var(_HASH_TARGET_TEXTURE_ONEPIXEL, 'TargetTextureOnePixel', TargetTextureOnePixel)
    model.all_materials.set_var(_HASH_TARGET_TEXTURE_TILE, 'TargetTextureTile', TargetTextureTile)
    model.all_materials.rebuild_tech()


def load_model_decal_high_quality(model, skin_id, decal_list):
    if not global_data.feature_mgr.is_support_model_decal():
        return

    def high_quality_load_cb(indrect_tex, high_decal_tex, ori_texture_size):
        if not model or not model.valid:
            return
        set_high_quality_model_decal_param(model, indrect_tex, high_decal_tex, ori_texture_size)

    global_data.emgr.create_high_quality_decal.emit(model, decal_list, skin_id, high_quality_load_cb)


def load_model_decal_data(model, skin_id, decal_list, lod_level=0, is_avatar_model=False, complete_cb=None, create_high_quality_decal=False):
    if not global_data.feature_mgr.is_support_model_decal():
        return
    if not model or not model.valid:
        return

    def load_cb(decal_tex):
        if not model or not model.valid:
            return
        model.all_materials.set_macro('DECAL_ENABLE', 'TRUE')
        model.all_materials.set_macro('DECAL_INDIRECT_ENABLE', 'FALSE')
        model.all_materials.set_texture(_HASH_TEXDECAL, 'TexDecal', decal_tex)

        def rebuild_tech():
            if model and model.valid:
                model.all_materials.rebuild_tech()

        global_data.game_mgr.next_exec(rebuild_tech)
        if complete_cb:
            complete_cb()
        if create_high_quality_decal:

            def high_quality_load_cb(indrect_tex, high_decal_tex, ori_texture_size):
                if not model or not model.valid:
                    return
                set_high_quality_model_decal_param(model, indrect_tex, high_decal_tex, ori_texture_size)

            def load_high_quality_data():
                if not model or not model.valid:
                    return
                global_data.emgr.create_high_quality_decal.emit(model, decal_list, skin_id, high_quality_load_cb, lod_level)

            global_data.game_mgr.next_exec(load_high_quality_data)

    if decal_list:
        global_data.emgr.load_decal_data.emit(model, decal_list, skin_id, load_cb, lod_level, is_avatar_model)
    else:
        _HASH_TEX1 = game3d.calc_string_hash('TexDecal')
        model.all_materials.set_macro('DECAL_ENABLE', 'FALSE')
        model.all_materials.rebuild_tech()


def load_model_color_data(model, skin_id, color):
    if not global_data.feature_mgr.is_support_model_decal():
        return
    if not model or not model.valid:
        return
    if color and isinstance(color, dict):
        for tunnel_idx, hsb_value in six.iteritems(color):
            _hash = calc_hash(tunnel_idx)
            _attr = 'changecolor%d' % tunnel_idx
            _val = calc_cur_color_from_hsb(skin_id, tunnel_idx, hsb_value)
            if not _val:
                continue
            _val.append(1.0)
            if _val:
                model.all_materials.set_var(_hash, _attr, tuple(_val))


ASSURE_SOCKET = {201001645: 'cangxiu'
   }

def get_assure_socket(skin_id):
    return ASSURE_SOCKET.get(skin_id, None)


def init_action_list(self, action_list):
    from logic.gutils.template_utils import init_common_choose_list
    self.action_option = [ {'anim': action[0],'name': action[1],'func_info': action[2:][0] if action[2:] else {}} for action in action_list ]

    def call_back(index):
        action = self.action_option[index]
        anim = action['anim']
        global_data.emgr.change_model_display_anim_directly.emit(anim, -1)

    def close_callback():
        self.hide_action_lsit()

    init_common_choose_list(self.panel.actione_list, self.action_option, callback=call_back, close_cb=close_callback)


def delete_action_list(self, need_reset_anim=True):
    if need_reset_anim:
        anim_name = get_default_skin_define_anim(self.skin_id)
        global_data.emgr.change_model_display_anim_directly.emit(anim_name, -1)
    self.action_option = None
    return


def get_mecha_pose_conf(mecha_id):
    conf = confmgr.get('skin_define_pose')
    ret = conf.get(str(mecha_id), {})
    return ret.get('cPose', [])


def get_mecha_pose_anim(item_id, skin_id=None):
    conf = confmgr.get('lobby_item', str(item_id), default={})
    res = conf.get('res', '')
    if skin_id is not None:
        skin_res = conf.get('skin_res', {}).get(str(skin_id), None)
        if skin_res is not None:
            res = skin_res
    return res


def get_mecha_gesture_pose(mecha_item_id, is_apply, mecha_pose_dict):
    from logic.gutils import item_utils
    from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_MECHA_GESTURE
    _mecha_pose = mecha_pose_dict.get(str(mecha_item_id), None)
    if _mecha_pose is None:
        return
    else:
        item_type = item_utils.get_lobby_item_type(_mecha_pose)
        is_show_pose = item_type == L_ITEM_TYPE_MECHA_GESTURE and is_apply
        mecha_pose = _mecha_pose if is_show_pose else None
        return mecha_pose


def is_mecha_gesture_pose(mecha_pose):
    from logic.gutils import item_utils
    from logic.gcommon.item.lobby_item_type import L_ITEM_TYPE_MECHA_GESTURE
    if not mecha_pose:
        return False
    item_type = item_utils.get_lobby_item_type(mecha_pose)
    return item_type == L_ITEM_TYPE_MECHA_GESTURE