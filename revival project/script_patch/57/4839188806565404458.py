# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/patch/patch_announce.py
from __future__ import absolute_import
from __future__ import print_function
import six
from six.moves import range
import json
import game3d
import C_file
from cocosui import cc, ccs, ccui
ANNOUNCE_DATA = ''
ANNOUNCE_INSTANCE = None
DOT_SELECT_PATH = 'gui/patch_ui/uires/patch_loading/img_patch_loading_dot3.png'
DOT_UNSELECT_PATH = 'gui/patch_ui/uires/patch_loading/img_patch_loading_dot2.png'

def is_showing_announce():
    global ANNOUNCE_INSTANCE
    return ANNOUNCE_INSTANCE is not None


def get_patch_announce_instance():
    global ANNOUNCE_INSTANCE
    try:
        if not ANNOUNCE_INSTANCE:
            ANNOUNCE_INSTANCE = PatchAnnounce()
        return ANNOUNCE_INSTANCE
    except Exception as e:
        print('[patch announce] get instance except:', str(e))
        return None

    return None


def destroy_patch_announce_instance(clear_data=True):
    global ANNOUNCE_DATA
    global ANNOUNCE_INSTANCE
    try:
        if ANNOUNCE_INSTANCE:
            ANNOUNCE_INSTANCE.destroy()
        ANNOUNCE_INSTANCE = None
        if clear_data:
            ANNOUNCE_DATA = ''
    except Exception as e:
        print('[patch announce] except:', str(e))

    return


class PatchAnnounce(object):

    def __init__(self):
        super(PatchAnnounce, self).__init__()
        self._is_valid = True
        self._msg = None
        self._widget = None
        self._last_idx = -1
        self._all_num = 0
        self._cur_platform = game3d.get_platform()
        self._get_announce_data()
        return

    def _get_announce_data(self):
        if not ANNOUNCE_DATA:
            announce_url = self._get_announcement_url()
            if not announce_url:
                print('[patch announce] has no announce url')
                destroy_patch_announce_instance(False)
                return
            self._download_single_file(announce_url, self._on_get_announce_data)
        else:
            self.create_announce_ui(ANNOUNCE_DATA)

    def _get_announcement_url(self):
        try:
            from patch import patch_dctool
            dc_tool_inst = patch_dctool.get_dctool_instane()
            game_id = dc_tool_inst.get_game_id()
            server_conf = C_file.get_res_file('confs/server.json', '')
            server_conf = json.loads(server_conf)
            platform_map = {game3d.PLATFORM_IOS: 'ios',
               game3d.PLATFORM_ANDROID: 'android',
               game3d.PLATFORM_WIN32: 'win32'
               }
            if game_id == 'g93':
                platform_type = platform_map.get(self._cur_platform)
                url = server_conf['notice_platform'][game_id][platform_type]['cn']
            else:
                from patch.patch_lang import get_multi_lang_instane
                lang_name = get_multi_lang_instane().cnt_lang_name
                if dc_tool_inst.is_steam_channel():
                    platform_type = 'win32_steam'
                elif self._cur_platform in (game3d.PLATFORM_IOS, game3d.PLATFORM_ANDROID):
                    platform_type = 'mobile'
                else:
                    platform_type = 'win32'
                url_conf = server_conf['notice_platform'][game_id][platform_type]
                if lang_name in url_conf:
                    url = url_conf[lang_name]
                else:
                    url = url_conf['en']
            return url
        except Exception as e:
            print('patch announce get url except:', str(e))
            return None

        return None

    def _on_get_announce_data(self, dl_data):
        global ANNOUNCE_DATA
        if not self._is_valid:
            return
        if not dl_data:
            destroy_patch_announce_instance(False)
            return
        dl_data = six.ensure_str(dl_data)
        ANNOUNCE_DATA = dl_data
        self.create_announce_ui(dl_data)

    def create_announce_ui(self, data):
        ret = self._create_ui()
        if not ret:
            destroy_patch_announce_instance(False)
            return
        else:
            self._all_num = 0
            try:
                self._msg = '<color=0x18192EFF>%s</color>' % data
                self._init_event()
                nd_scroll_list = self._widget.pnl_content.list_content
                nd_scroll_list.setBlockScrolling(True)
                list_size = nd_scroll_list.getContentSize()
                from . import patch_richtext
                scroll_view = ccui.ScrollView.create()
                scroll_view.setContentSize(list_size)
                msg_size = cc.Size(list_size.width, 0)
                rt_msg = patch_richtext.richtext(self._msg, 16, msg_size)
                if not rt_msg:
                    destroy_patch_announce_instance(False)
                    return
                rt_msg.formatText()
                rt_size = rt_msg.getVirtualRendererSize()
                scroll_view.setInnerContainerSize(rt_size)
                rt_msg.setAnchorPoint(cc.Vec2(0.0, 0.0))
                rt_msg.setHorizontalAlign(0)
                rt_msg.setContentSize(rt_size)
                if rt_size.height < list_size.height:
                    rt_msg.setPosition(cc.Vec2(0, list_size.height - rt_size.height))
                else:
                    rt_msg.setPosition(cc.Vec2(0, 0))
                scroll_view.addChild(rt_msg)
                scroll_view.jumpToTop()
                nd_scroll_list.pushBackCustomItem(scroll_view)
                self._all_num += 1
            except Exception as e:
                print('[patch announce] create ui with except:', str(e))
                destroy_patch_announce_instance(False)
                return

            try:
                from . import announce_data
                from patch.patch_lang import get_multi_lang_instane
                lang_name = get_multi_lang_instane().cnt_lang_name
                pic_path_lst = announce_data.GetAnnouncePic().get(lang_name, {}).get('pic_lst', [])

                def set_sprite_scale(in_sprite, in_size):
                    spr_size = in_sprite.getContentSize()
                    width_ratio = in_size.width / spr_size.width
                    height_ratio = in_size.height / spr_size.height
                    max_ratio = max(width_ratio, height_ratio)
                    in_sprite.setScale(max_ratio)

                need_ktx = self._cur_platform in (game3d.PLATFORM_IOS, game3d.PLATFORM_ANDROID)
                for res_pic in pic_path_lst:
                    if need_ktx:
                        find_res_path = res_pic[:-4] + '.ktx' if 1 else res_pic
                        if not C_file.find_res_file(find_res_path, ''):
                            continue
                        nd_sprite = cc.Sprite.create(res_pic)
                        set_sprite_scale(nd_sprite, list_size)
                        widget_sprite = ccui.Widget.create()
                        widget_sprite.setContentSize(list_size)
                        nd_sprite.setAnchorPoint(cc.Vec2(0.0, 0.0))
                        nd_sprite.setPosition(cc.Vec2(0, 0))
                        widget_sprite.addChild(nd_sprite)
                        nd_scroll_list.pushBackCustomItem(widget_sprite)
                        self._all_num += 1

                game3d.delay_exec(1, lambda : nd_scroll_list and nd_scroll_list.isValid() and nd_scroll_list.jumpToLeft())
            except Exception as e:
                print('[patch announce] add pic node except:', str(e))
                destroy_patch_announce_instance(False)
                return

            try:
                nd_list_dot = self._widget.pnl_content.list_dot
                nd_list_dot.setBlockScrolling(True)
                img_size = None
                all_item_num = self._all_num
                for idx in range(all_item_num):
                    if idx == 0:
                        dot_path = DOT_SELECT_PATH if 1 else DOT_UNSELECT_PATH
                        node_img = ccui.ImageView.create(dot_path)
                        img_size = node_img.getContentSize()
                        nd_list_dot.pushBackCustomItem(node_img)

                if all_item_num > 0:
                    list_dot_width = img_size.width * all_item_num
                    nd_list_dot.setContentSize(cc.Size(list_dot_width, img_size.height))
                    nd_list_dot.setAnchorPoint(cc.Vec2(0.5, 0))
                    org_pos = nd_list_dot.getPosition()
                    parent_size = self._widget.pnl_content.getContentSize()
                    nd_list_dot.setPosition(cc.Vec2(parent_size.width / 2.0, org_pos.y))
            except Exception as e:
                print('[patch announce] create pic with except:', str(e))
                destroy_patch_announce_instance(False)
                return

            self._set_now_select(0)
            return

    def _set_now_select(self, now_idx):
        try:
            if not self._widget or not self._widget.isValid():
                return
            nd_pnl_content = self._widget.pnl_content
            if self._all_num <= 1:
                nd_pnl_content.btn_next.setVisible(False)
                nd_pnl_content.btn_before.setVisible(False)
            else:
                nd_pnl_content.btn_next.setVisible(True)
                nd_pnl_content.btn_before.setVisible(True)
            if now_idx <= 0:
                now_idx = 0
                nd_pnl_content.btn_before.setVisible(False)
            elif now_idx >= self._all_num - 1:
                now_idx = self._all_num - 1
                nd_pnl_content.btn_next.setVisible(False)
        except Exception as e:
            print('[patch announce] set_now_select except:', str(e))

        if self._last_idx == now_idx:
            return
        try:
            node_lst_dot = self._widget.pnl_content.list_dot
            if self._last_idx >= 0:
                last_dot_item = node_lst_dot.getItem(self._last_idx)
                if last_dot_item:
                    last_dot_item.loadTexture(DOT_UNSELECT_PATH)
            if now_idx >= 0:
                now_dot_item = node_lst_dot.getItem(now_idx)
                if now_dot_item:
                    now_dot_item.loadTexture(DOT_SELECT_PATH)
        except Exception as e:
            print('[patch announce] set dot pic except:', str(e))

        self._last_idx = now_idx

    def _download_single_file(self, in_url, callback):

        def thread_download_single_file--- This code section failed: ---

 280       0  LOAD_CONST            0  ''
           3  STORE_DEREF           0  'data'

 281       6  SETUP_EXCEPT        192  'to 201'

 282       9  LOAD_CONST            1  ''
          12  LOAD_CONST            0  ''
          15  IMPORT_NAME           1  'urllib3'
          18  STORE_FAST            1  'urllib3'

 283      21  LOAD_CONST            1  ''
          24  LOAD_CONST            0  ''
          27  IMPORT_NAME           2  'six.moves.http_client'
          30  STORE_FAST            2  'six'

 284      33  LOAD_FAST             0  'url'
          36  LOAD_ATTR             3  'startswith'
          39  LOAD_CONST            2  'https'
          42  CALL_FUNCTION_1       1 
          45  POP_JUMP_IF_FALSE    91  'to 91'

 285      48  LOAD_CONST            1  ''
          51  LOAD_CONST            3  ('CACERT_PATH',)
          54  IMPORT_NAME           4  'patch.patch_path'
          57  IMPORT_FROM           5  'CACERT_PATH'
          60  STORE_FAST            3  'CACERT_PATH'
          63  POP_TOP          

 286      64  LOAD_FAST             1  'urllib3'
          67  LOAD_ATTR             6  'PoolManager'
          70  LOAD_CONST            4  'cert_reqs'
          73  LOAD_CONST            5  'CERT_REQUIRED'
          76  LOAD_CONST            6  'ca_certs'
          79  LOAD_FAST             3  'CACERT_PATH'
          82  CALL_FUNCTION_512   512 
          85  STORE_FAST            4  'http'
          88  JUMP_FORWARD         12  'to 103'

 288      91  LOAD_FAST             1  'urllib3'
          94  LOAD_ATTR             6  'PoolManager'
          97  CALL_FUNCTION_0       0 
         100  STORE_FAST            4  'http'
       103_0  COME_FROM                '88'

 289     103  LOAD_FAST             4  'http'
         106  LOAD_ATTR             7  'request'
         109  LOAD_CONST            7  'GET'
         112  LOAD_CONST            8  'timeout'
         115  LOAD_FAST             1  'urllib3'
         118  LOAD_ATTR             8  'Timeout'
         121  LOAD_CONST            9  'connect'
         124  LOAD_CONST           10  2.0
         127  LOAD_CONST           11  'read'
         130  LOAD_CONST           10  2.0
         133  LOAD_CONST           12  'total'
         136  LOAD_CONST           13  4
         139  CALL_FUNCTION_768   768 
         142  CALL_FUNCTION_258   258 
         145  STORE_FAST            5  'r'

 290     148  LOAD_FAST             5  'r'
         151  LOAD_ATTR             9  'status'
         154  LOAD_FAST             2  'six'
         157  LOAD_ATTR            10  'moves'
         160  LOAD_ATTR            11  'http_client'
         163  LOAD_ATTR            12  'OK'
         166  COMPARE_OP            2  '=='
         169  POP_JUMP_IF_FALSE   181  'to 181'
         172  LOAD_FAST             5  'r'
         175  LOAD_ATTR            13  'data'
         178  JUMP_FORWARD          3  'to 184'
         181  LOAD_CONST            0  ''
       184_0  COME_FROM                '178'
         184  STORE_DEREF           0  'data'

 291     187  LOAD_FAST             5  'r'
         190  LOAD_ATTR            14  'release_conn'
         193  CALL_FUNCTION_0       0 
         196  POP_TOP          
         197  POP_BLOCK        
         198  JUMP_FORWARD         38  'to 239'
       201_0  COME_FROM                '6'

 292     201  DUP_TOP          
         202  LOAD_GLOBAL          15  'Exception'
         205  COMPARE_OP           10  'exception-match'
         208  POP_JUMP_IF_FALSE   238  'to 238'
         211  POP_TOP          
         212  STORE_FAST            6  'e'
         215  POP_TOP          

 293     216  LOAD_GLOBAL          16  'print'
         219  LOAD_CONST           14  '[patch announce] download exception:'
         222  LOAD_GLOBAL          17  'str'
         225  LOAD_FAST             6  'e'
         228  CALL_FUNCTION_1       1 
         231  CALL_FUNCTION_2       2 
         234  POP_TOP          
         235  JUMP_FORWARD          1  'to 239'
         238  END_FINALLY      
       239_0  COME_FROM                '238'
       239_1  COME_FROM                '198'

 294     239  LOAD_GLOBAL          18  'game3d'
         242  LOAD_ATTR            19  'delay_exec'
         245  LOAD_CONST           15  1
         248  LOAD_CLOSURE          1  'callback'
         251  LOAD_CLOSURE          0  'data'
         257  LOAD_LAMBDA              '<code_object <lambda>>'
         260  MAKE_CLOSURE_0        0 
         263  CALL_FUNCTION_2       2 
         266  POP_TOP          
         267  LOAD_CONST            0  ''
         270  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_258' instruction at offset 142

        import threading
        t = threading.Thread(target=thread_download_single_file, args=(in_url,))
        t.setDaemon(True)
        t.start()

    def _create_ui(self):
        try:
            reader = ccs.GUIReader.getInstance()
            widget = reader.widgetFromJsonFile('gui/patch_ui/patch_loading.json')
            from .patch_utils import PATCH_UI_LAYER, normalize_widget
            widget = normalize_widget(widget)
            self._widget = widget
            from patch.patch_lang import get_patch_text_id
            widget.pnl_content.lab_content_title.setString(get_patch_text_id(80161))
            director = cc.Director.getInstance()
            scene = director.getRunningScene()
            scene.addChild(widget, PATCH_UI_LAYER + 2)
            self.set_scale_and_pos()
            return True
        except Exception as e:
            print('patch announce create ui error:', str(e))
            return False

    def set_scale_and_pos(self):
        if not self._widget or not self._widget.isValid():
            return
        try:
            director = cc.Director.getInstance()
            view = director.getOpenGLView()
            v_size = view.getVisibleSize()
            widget_size = self._widget.getContentSize()
            width_ratio = v_size.width / widget_size.width
            height_ratio = v_size.height / widget_size.height
            max_ratio = min(width_ratio, height_ratio)
            self._widget.setScale(max_ratio)
            self._widget.setAnchorPoint(cc.Vec2(0.5, 0.5))
            self._widget.setPosition(cc.Vec2(v_size.width * 0.5, v_size.height * 0.5))
            self.update_strange_screen_pos(v_size)
        except Exception as e:
            print('patch video set scale and pos except:', str(e))

    def update_strange_screen_pos(self, v_size):
        if not self._widget or not self._widget.isValid():
            return
        try:
            import profiling
            model_name = profiling.get_device_model() or ''
            model_name = model_name.lower()
            adjust_config = json.loads(C_file.get_res_file('confs/c_screen_adapt.json', ''))
            final_config = {}
            if adjust_config:
                for k, v in six.iteritems(adjust_config):
                    final_config[k.lower()] = v

            model_config = final_config.get(model_name, {})
            if not model_config:
                res = game3d.is_notch_screen()
                if not isinstance(res, bool):
                    is_notch, left, right, top, down = res
                else:
                    is_notch = res
                if is_notch:
                    if self._cur_platform == game3d.PLATFORM_ANDROID:
                        model_config = final_config.get('android_default', {})
                    else:
                        model_config = final_config.get('iphone_default', {})
            offset = model_config.get('WIDTH_EDGE_OFFSET', 0.0)
            margin = self._widget.btn_close.getLayoutParameter().getMargin()
            margin.right = margin.right + offset * v_size.width
            self._widget.btn_close.getLayoutParameter().setMargin(margin)
        except Exception as e:
            print('[patch announce] strange screen except:', str(e))

    def _init_event(self):
        if not self._widget or not self._widget.isValid():
            return
        try:
            self._widget.btn_close.addTouchEventListener(self._on_click_btn_close)
            self._widget.pnl_content.btn_before.addTouchEventListener(self._on_click_btn_before)
            self._widget.pnl_content.btn_next.addTouchEventListener(self._on_click_btn_next)
        except Exception as e:
            print('[patch announce] init event except:', str(e))

    def _on_click_btn_before(self, widget, event):
        if not self._widget or not self._widget.isValid():
            return
        if event not in (ccui.WIDGET_TOUCHEVENTTYPE_ENDED,):
            return
        new_idx = self._last_idx - 1
        if new_idx < 0:
            new_idx = 0
        self._set_now_select(new_idx)
        try:
            if self._all_num <= 1:
                return
            ver_percent = float(new_idx) / float(self._all_num - 1) * 100
            self._widget.pnl_content.list_content.scrollToPercentHorizontal(ver_percent, 0.2, False)
        except Exception as e:
            print('[patch announce] click before except:', str(e))

    def _on_click_btn_next(self, widget, event):
        if not self._widget or not self._widget.isValid():
            return
        if event not in (ccui.WIDGET_TOUCHEVENTTYPE_ENDED,):
            return
        new_idx = self._last_idx + 1
        if new_idx > self._all_num - 1:
            new_idx = self._all_num - 1
        self._set_now_select(new_idx)
        try:
            if self._all_num <= 1:
                return
            ver_percent = float(new_idx) / float(self._all_num - 1) * 100
            self._widget.pnl_content.list_content.scrollToPercentHorizontal(ver_percent, 0.2, False)
        except Exception as e:
            print('[patch announce] click next except:', str(e))

    def _on_click_btn_close(self, *args):
        destroy_patch_announce_instance(False)

    def destroy(self):
        try:
            self._is_valid = False
            self._msg = None
            self._last_idx = -1
            self._all_num = 0
            if self._widget:
                self._widget.removeFromParent()
            self._widget = None
        except Exception as e:
            print('patch announce remove except:', str(e))

        return