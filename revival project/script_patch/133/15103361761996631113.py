# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/debug/debug_util.py
from __future__ import absolute_import
from __future__ import print_function
import six
from six.moves import range
scn = None
player = None

def update_scene(scene):
    global scn
    scn = scene


def update_player(_player):
    global player
    player = _player


def rpyc_server():
    from rpyc.scripts import rpyc_init
    rpyc_init.launch()


def connect_server(ip='192.168.46.53', port=4228):
    from logic.gutils.ConnectHelper import ConnectHelper
    ConnectHelper().connect(ip, port)


def create_character(name, sex):
    global_data.owner_entity.create_character(name, sex)


def select_character(idx):
    global_data.owner_entity.select_character(idx)


def draw_flightline(_lower_left_pos=(-20000, -20000), _upper_right_pos=(20000, 20000), _node_length=5000):
    import cc

    class DrawBoard(object):

        def __init__(self, layer, map_scale):
            self.draw_node = cc.DrawNode.create()
            layer.addChild(self.draw_node, 10, -1)

        def draw_line(self, verts):
            self.draw_node.clear()
            for idx in range(0, len(verts) - 1):
                self.draw_node.drawSegment(verts[idx], verts[idx + 1], 10, cc.Color4F(1, 0, 0, 1))


def camera():
    if global_data.ui_mgr.get_ui('CameraTestUI'):
        global_data.ui_mgr.close_ui('CameraTestUI')
    else:
        from logic.comsys.debug.CameraTestUI import CameraTestUI
        CameraTestUI()


def develop_helper():
    if global_data.ui_mgr.get_ui('DevelopHelperUI'):
        global_data.ui_mgr.close_ui('DevelopHelperUI')
    else:
        global_data.ui_mgr.show_ui('DevelopHelperUI', 'logic.comsys.debug')


def trk(trk_name):
    if trk_name.endswith('trk'):
        import os
        trk_name = os.path.normpath(trk_name)
        import logic
        if trk_name and trk_name.startswith('K:'):
            _src_path = os.path.abspath(logic.__path__[0] + os.path.sep + '..' + os.path.sep + '..')
            res_path = os.path.join(_src_path, 'res')
            if trk_name.startswith(res_path):
                trk_name = os.path.relpath(trk_name, res_path)
        trk_name = trk_name.replace(os.path.sep, '/')
    print('trk_name, ', trk_name)
    global_data.emgr.camera_play_added_trk_event.emit(trk_name)


def need_big_plist(is_need):
    global_data.need_big_plist = is_need
    from logic.gcommon.utility import enhance_class
    import cc

    class enhance_UISystem(object):

        def _GetSpriteFrameByPath(self, path, plist=''):
            if global_data.need_big_plist:
                if path not in self._ignore_plist_cache and cc.ResManager.getInstance().loadImgSpriteFrames(path):
                    return cc.SpriteFrameCache.getInstance().getSpriteFrame(path)
            if plist != '':
                cc.SpriteFrameCache.getInstance().addSpriteFrames(plist)
                sprite_frame = cc.SpriteFrameCache.getInstance().getSpriteFrame(path)
                if sprite_frame is not None:
                    return sprite_frame
            else:
                texture = cc.Director.getInstance().getTextureCache().addImage(path)
                if texture is not None:
                    size = texture.getContentSize()
                    rect = cc.Rect(0, 0, size.width, size.height)
                    sprite_frame = cc.SpriteFrame.createWithTexture(texture, rect)
                    return sprite_frame
            return

        def LoadSpriteFramesByPath(self, path):
            import ccui
            if self.GetSpriteFramePlistByPath(path) and global_data.need_big_plist:
                return ccui.WIDGET_TEXTURERESTYPE_PLIST
            else:
                return ccui.WIDGET_TEXTURERESTYPE_LOCAL

    from common.uisys.uisystem import UISystem
    enhance_class(UISystem, enhance_UISystem)
    cc.SpriteFrameCache.getInstance().removeUnusedSpriteFrames()
    cc.Director.getInstance().getTextureCache().removeUnusedTextures()
    cc.Director.getInstance().getTextureCache().removeAllTextures()


def set_ui_show_whitelist(whitelist, tag):
    from common.const.uiconst import BASE_LAYER_ZORDER
    from logic.gcommon.utility import enhance_class
    import cc

    class enhance_UIManager(object):

        def create_dialog(self, dlg, template_name, zorder=None, ui_name=None, is_full_screen=False, template_info=None, exception_ignore_zorder=False):
            dlg_name = dlg.get_name()
            if dlg_name in self.dialogs:
                raise Exception('dumplicate dlg with name %s ' % dlg_name)
            if zorder is None:
                zorder = BASE_LAYER_ZORDER
            ui_layer_dict = self.ui_layer_dict
            if zorder in ui_layer_dict:
                if is_full_screen:
                    parent = ui_layer_dict[zorder].nd_bg
                else:
                    parent = ui_layer_dict[zorder].nd_canvas
            elif not exception_ignore_zorder:
                raise Exception('InCorrect panel zorder')
            cocos_item = self.uis.load_template_create(template_name, parent, None, template_info=template_info)
            self.dialogs[dlg_name] = dlg
            self.dlg_stack.append(dlg_name)
            if dlg_name in self.blocking_ui_list:
                tag_list = self.blocking_ui_list[dlg_name]
                for tag in tag_list:
                    dlg.add_hide_count(tag)

            if self.ui_show_whitelist and dlg_name not in self.ui_show_whitelist:
                dlg.add_hide_count(self.ui_show_whitelist_tag)
            return cocos_item

        def set_ui_show_whitelist(self, ui_show_whitelist, tag):
            if tag:
                self.ui_show_whitelist = ui_show_whitelist
                self.ui_show_whitelist_tag = tag
                for dlg_name, dlg in six.iteritems(self.dialogs):
                    if dlg_name not in self.ui_show_whitelist:
                        dlg.add_hide_count(self.ui_show_whitelist_tag)

            else:
                for dlg_name, dlg in six.iteritems(self.dialogs):
                    if dlg_name not in self.ui_show_whitelist:
                        dlg.add_show_count(self.ui_show_whitelist_tag)

                self.ui_show_whitelist = []
                self.ui_show_whitelist_tag = None
            return

    from common.uisys.UIManager import UIManager
    enhance_class(UIManager, enhance_UIManager)
    global_data.ui_mgr.set_ui_show_whitelist(whitelist, tag)


def set_show_base_state_tips():
    from logic.gcommon.utility import enhance_class
    from logic.gcommon.cdata.mecha_status_config import num_2_desc

    class enhance_StateBase(object):

        def enter_camera(self, state_camera):
            cur_state_str = num_2_desc.get(self.sid)
            sub_state_str = self.sub_state
            print('\xe5\x88\x87\xe5\x85\xa5\xe9\x95\x9c\xe5\xa4\xb4\xef\xbc\x9a' + str(state_camera) + '\xe7\x8e\xb0\xe7\x8a\xb6\xe6\x80\x81' + str(cur_state_str) + '\xe5\xad\x90\xe7\x8a\xb6\xe6\x80\x81' + str(sub_state_str))
            self.send_event('E_TRY_SWITCH_TO_CAMERA_STATE', str(state_camera))

    from logic.gcommon.behavior.StateBase import StateBase
    enhance_class(StateBase, enhance_StateBase)


def ui(lang=None):
    global_data.is_debug_mode = True
    need_big_plist(False)
    from logic.gcommon.common_const.lang_data import LANG_ZHTW, LANG_CN, LANG_EN
    global_data.ui_mgr.change_lang(LANG_CN if lang is None else lang)
    return


def noui():
    if global_data.cocos_scene:
        global_data.ui_mgr.set_all_ui_visible(not global_data.cocos_scene.isVisible())


def set_focus_trk():
    if global_data.cam_lplayer:
        if 'help' in kwargs:
            print('\n\t\t\tthe usage is like that:\n\t\t\t\tset_focus_trk(_target_dist=[20, 80], _target_y_offset=[0, -20])\n\t\t\tposible attr and default value is list below:\n\t\t\t\t_target_dist = [20, 80]\n\t\t\t\t_target_y_offset = [0, -20]\n\t\t\t\t_angle = -0.3\n\t\t\t\t_action_type = "CubicBezier"\n\t\t\t\t_action_parameter = [0.16,-0.01,0.23,0.89]\n\t\t\t\t_rot_time = 0.6\n\t\t\t\t_translate_time = 1.0\n\n\n\t\t\t')
        fo_trk = global_data.cam_lplayer.get_com('ComKillerCamera')._focus_track
        for key, attr in six.iteritems(kwargs):
            setattr(fo_trk, str(key), attr)


def test2():
    from common.const.uiconst import BASE_LAYER_ZORDER
    from logic.gcommon.utility import enhance_class
    from logic.gcommon.common_utils.local_text import get_text_by_id
    from common.cfg import confmgr
    from logic.comsys.common_ui.ScaleableHorzContainer import ScaleableHorzContainer
    from logic.comsys.mecha_display.ExDescibeWidget import ExDescibeWidget
    from logic.gutils import mecha_skin_utils
    from logic.client.const.lobby_model_display_const import CAM_MODE_NEAR, CAM_MODE_FAR, CAM_DISPLAY_PIC, ROTATE_FACTOR
    from common.uisys.BaseUIWidget import BaseUIWidget
    import cc
    from logic.gutils import dress_utils
    from logic.gutils.dress_utils import mecha_lobby_id_2_battle_id, battle_id_to_mecha_lobby_id
    from logic.gutils import mall_utils
    from logic.gutils import item_utils
    from logic.gutils.template_utils import init_price_view, show_remain_time
    from logic.client.const import mall_const
    from logic.gcommon.item.item_const import FASHION_POS_SUIT
    from logic.gutils.item_utils import get_item_rare_degree, get_rare_degree_name
    from logic.comsys.mall_ui.BuyConfirmUIInterface import role_or_skin_buy_confirmUI
    from logic.comsys.ui_distortor.UIDistortHelper import DistortScaleCalculator, linear_inter
    import math
    from logic.gutils.CameraHelper import normalize_angle
    import game3d
    import math3d
    CARD_SS_FRAME_TEMPLATE = 'role_profile/i_card_skin_frame_ss'
    global_data.show_ss_card_effect = True
    import cc

    class enhance_skin(object):

        def check_clothing_on_ss_level(self):
            global_data.test_ss_card_effect = True
            if global_data.test_ss_card_effect:
                if mecha_skin_utils.is_ss_level_skin(self.cur_clothing_id):
                    card_items = self.get_ss_card_items()
                    self.ss_card_effect.update_ss_card_list(list(card_items.values()))
                    self.ss_card_effect.start_gyro_effect()
                else:
                    self.ss_card_effect.update_ss_card_list([])
                    self.ss_card_effect.stop_gyro_effect()

    class enhance_ss(object):

        def gyro_callback(self, smooth_rotate_speed, raw_gyro_vector, rotation_flag):
            if self._start_rotation is None:
                if raw_gyro_vector.x != 0 and raw_gyro_vector.y != 0 and raw_gyro_vector.z != 0:
                    self._start_rotation = raw_gyro_vector
                    return
            else:
                diff_gyro_vector = raw_gyro_vector - self._start_rotation
                x_val = normalize_angle(diff_gyro_vector.x)
                y_val = normalize_angle(diff_gyro_vector.y)
                if x_val > 0:
                    diff_gyro_vector.x = self.process_slerp_act(x_val, 0, math.pi / 2.0)
                else:
                    diff_gyro_vector.x = self.process_slerp_act(x_val, -math.pi / 2.0, 0)
                x_rot = -max(min(diff_gyro_vector.y * 180 / math.pi, self._x_rot_max), self._x_rot_min)
                y_rot = max(min(diff_gyro_vector.x * 180 / math.pi, self._y_rot_max), self._y_rot_min)
                for ind, nd in enumerate(self._ss_card_items):
                    self.nd_distorter(nd, x_rot, y_rot, ind)

            return

    from logic.comsys.mecha_display.MechaBasicSkinWidget import MechaBasicSkinWidget, SSCardsEffect
    enhance_class(MechaBasicSkinWidget, enhance_skin)
    enhance_class(SSCardsEffect, enhance_ss)


def map_skin(from_id, to_id):
    import world
    backup_dict = global_data.debug_replace_res_dict
    from_id = from_id.replace('/', '\\')
    to_id = to_id.replace('/', '\\')
    character_files = [
     'empty.gim',
     'h.gim',
     'l.gim',
     'l1.gim',
     'l2.gim',
     'l3.gim',
     'parts\\h_head.gim',
     'parts\\l_head.gim',
     'parts\\l1_head.gim',
     'parts\\l2_head.gim',
     'parts\\h_head.gim']
    for k in character_files:
        src = 'character\\{}\\{}'.format(from_id, k)
        dst = 'character\\{}\\{}'.format(to_id, k)
        world.set_res_object_filemap(src, dst)
        world.set_res_object_filemap(src.replace('\\', '/'), dst.replace('\\', '/'))
        backup_dict[src] = dst
        backup_dict[src.replace('\\', '/')] = dst.replace('\\', '/')

    from_character_id, _ = from_id.split('\\')
    to_character_id, _ = to_id.split('\\')
    if from_character_id != to_character_id:
        hit_files = ['hit.gim',
         'hit_lobby.gim']
        for k in hit_files:
            src = 'character\\{}\\{}'.format(from_character_id, k)
            dst = 'character\\{}\\{}'.format(to_character_id, k)
            world.set_res_object_filemap(src.replace('\\', '/'), dst.replace('\\', '/'))
            backup_dict[src] = dst
            backup_dict[src.replace('\\', '/')] = dst.replace('\\', '/')


def map_mecha_skin(from_id, to_id):
    import world
    backup_dict = global_data.debug_replace_res_dict
    from_id = from_id.replace('/', '\\')
    to_id = to_id.replace('/', '\\')
    character_files = [
     'empty.gim',
     'h.gim',
     'l.gim',
     'l1.gim',
     'l2.gim',
     'l3.gim',
     'hit.gim']
    for k in character_files:
        src = 'model_new\\mecha\\{}\\{}'.format(from_id, k)
        dst = 'model_new\\mecha\\{}\\{}'.format(to_id, k)
        world.set_res_object_filemap(src, dst)
        world.set_res_object_filemap(src.replace('\\', '/'), dst.replace('\\', '/'))
        backup_dict[src] = dst
        backup_dict[src.replace('\\', '/')] = dst.replace('\\', '/')


def ad(aid):
    from common.cfg import confmgr
    from logic.gutils import advance_utils
    advance_conf = confmgr.get('advance_config', str(aid), default={})
    if not advance_conf:
        return
    else:
        ui_name, ui_path = advance_conf['ui_name']
        ui = global_data.ui_mgr.show_ui(ui_name, ui_path)
        show_func_name = advance_conf.get('show_func', '')
        if show_func_name:
            show_func = getattr(advance_utils, show_func_name, None)
            if show_func:
                custom_data = advance_conf.get('custom_params', {})
                show_func(ui, custom_data)
        return


def gui(issue, user=None, branch=None):
    if user:
        global_data.gui_exporter(user, issue, branch)
    else:
        global_data.gui_exporter_issue(issue, branch)


def cb_pos(x, y, z):
    import world
    import math3d
    import json
    scn = world.get_active_scene()
    background_model = scn.get_model('zhanshi_pifu_chunjie')
    if background_model:
        background_model.world_position = math3d.vector(*[float(x), float(y), float(z)])


def cb_scale(x, y, z):
    import world
    import math3d
    import json
    scn = world.get_active_scene()
    background_model = scn.get_model('zhanshi_pifu_chunjie')
    if background_model:
        background_model.scale = math3d.vector(*[float(x), float(y), float(z)])


def task(task_id):
    from logic.gutils import task_utils
    global_data.player.wiz_command('reset_all_task')
    for task_id in task_utils.get_children_task(task_id):
        global_data.player.wiz_command('task_prog %s 100000' % task_id)