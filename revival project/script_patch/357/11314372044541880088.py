# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/lottery/LotteryGridItemWidget.py
from __future__ import absolute_import
import six
import cc
import render
import game3d
from logic.gutils import item_utils as i_utils
from logic.comsys.effect.ui_effect import create_shader
from logic.manager_agents.manager_decorators import sync_exec
from logic.gutils.lobby_click_interval_utils import global_unique_click
import device_compatibility
from logic.comsys.share.ShareTemplateBase import async_disable_wrapper
GRID_TYPE = {1: 'large',
   2: 'vertical',
   3: 'long',
   4: 'small'
   }

class LotteryGridItemWidget(object):

    def __init__(self, parent, panel, item_list, percent_up_item_id_set, select_cb=None):
        self.parent = parent
        self.panel = panel
        self.item_list = item_list
        self.percent_up_item_id_set = percent_up_item_id_set
        self._selected_callback = select_cb
        self.sprite = None
        self.grid_panel = None
        self.rt = None
        self.min_duration = 0.3
        self.item_dict = {}
        self.main_item = None
        self.init_panel()
        self.create_img()
        return

    @property
    def show_model_id(self):
        return self.parent.show_model_id

    @show_model_id.setter
    def show_model_id(self, value):
        self.parent.show_model_id = value

    def on_resolution_changed(self):
        self.init_panel()
        self.create_img()

    @async_disable_wrapper
    def init_panel(self):
        self.panel.nd_item.DestroyChild('grid_panel')
        self.grid_panel = grid_panel = global_data.uisystem.load_template_create('mall/i_mall_content_lottery_exclusive_grid_img')
        grid_panel.retain()
        self.set_scale(True)
        from logic.comsys.effect.ui_effect import create_shader
        gl_swap_rgb = create_shader('window_clipping', 'window_clipping')
        program_swap_rgb = cc.GLProgramState.getOrCreateWithGLProgram(gl_swap_rgb)
        program_swap_rgb.setUniformFloat('u_cx', 0.0)
        program_swap_rgb.setUniformFloat('u_cy', 0.0)
        program_swap_rgb.setUniformFloat('u_wx', 1.0)
        program_swap_rgb.setUniformFloat('u_wy', 0.5)
        self.item_dict = {}
        self.main_item = None
        for item_id, layout in self.item_list:
            temp_name = GRID_TYPE.get(layout // 100, 'small')
            x = layout % 100 // 10
            y = layout % 10
            path = 'mall/i_exclusive_item_%s' % temp_name
            self.item_dict[item_id] = img_widget = global_data.uisystem.load_template_create(path, parent=grid_panel)
            img_widget.setAnchorPoint(cc.Vec2(0, 1))
            x = str(x * 33.33) + '%'
            y = str((3 - y) * 33.33) + '%'
            img_widget.SetPosition(x, y)
            img_widget.nd_tag.setVisible(str(item_id) in self.percent_up_item_id_set)
            img_widget.nd_tag.img_up.setVisible(False)
            pic_path = i_utils.get_lobby_item_pic_by_item_no(item_id)
            img_widget.item.SetDisplayFrameByPath('', pic_path)
            if temp_name in ('large', 'small'):
                img_widget.item.setGLProgramState(program_swap_rgb)
            i_utils.check_skin_tag(img_widget.temp_quality, item_id)

            @global_unique_click(img_widget.btn_bar)
            def OnClick(btn, touch, item_id=item_id):
                if self.show_model_id != item_id:
                    self.show_model(item_id)

            if temp_name == 'large':
                self.main_item = img_widget

        return

    def set_scale(self, is_render):
        grid_panel = self.grid_panel
        if not is_render:
            grid_panel.setAnchorPoint(cc.Vec2(0.5, 0.5))
            grid_panel.SetPosition('50%', '50%')
            grid_panel.setScale(1)
        else:
            size = grid_panel.GetContentSize()
            grid_panel.setAnchorPoint(cc.Vec2(0, 0))
            if device_compatibility.IS_DX:
                grid_panel.setScale(1)
                grid_panel.SetPosition(0, 0)
            else:
                grid_panel.setScaleX(1)
                grid_panel.setScaleY(-1)
                grid_panel.SetPosition(0, size[1])

    def create_img(self):
        self.panel.nd_item.DestroyChild('img_item')
        from common.uisys.uielment.CCSprite import CCSprite
        self.sprite = CCSprite.Create()
        self.render_img_to_sprite()
        self.panel.nd_item.AddChild('img_item', self.sprite)
        self.sprite.setAnchorPoint(cc.Vec2(0.5, 0.5))
        self.sprite.SetPosition('50%', '50%')
        self.sprite.setVisible(False)
        if game3d.get_render_device() == game3d.DEVICE_METAL:
            self.sprite.setFlippedY(True)
        gl_swap_rgb = create_shader('gradual_opacity', 'gradual_opacity')
        program_swap_rgb = cc.GLProgramState.getOrCreateWithGLProgram(gl_swap_rgb)
        program_swap_rgb.setUniformFloat('u_boundary', 1.0)
        program_swap_rgb.setUniformFloat('u_width', 2.0)
        program_swap_rgb.setUniformFloat('u_cx', 0.0)
        program_swap_rgb.setUniformFloat('u_cy', 0.0)
        self.sprite.setGLProgramState(program_swap_rgb)
        self.panel.SetTimeOut(self.min_duration, lambda *args: self.bind_grid_item())

    @sync_exec
    def render_img_to_sprite(self):
        if not self.sprite:
            return
        from common.utils.cocos_utils import CCRect
        from common.uisys.uielment.CCSprite import CCSprite
        size = self.grid_panel.GetContentSize()
        tex = render.texture.create_empty(int(size[0]), int(size[1]), render.PIXEL_FMT_A8R8G8B8, True)
        if self.rt:
            self.rt.release()
        self.rt = rt = cc.RenderTexture.createWithITexture(tex)
        rt.retain()
        rt.beginWithClear(0, 0, 0, 0)
        self.rt.addCommandsForNode(self.grid_panel.get()) if hasattr(self.rt, 'addCommandsForNode') else self.grid_panel.visit()
        rt.end()
        self.sprite.setTexture(rt.getSprite().getTexture())
        self.sprite.setTextureRect(CCRect(0, 0, *size))
        self.sprite.getGLProgramState().setUniformFloat('u_boundary', 0.0)

    def bind_grid_item(self):
        if not self.panel:
            return
        self.panel.nd_item.AddChild('grid_panel', self.grid_panel)
        self.set_scale(False)

    @sync_exec
    def play_animation(self, duration=1.7):
        if not self.sprite:
            return
        duration = max(duration, self.min_duration + 0.2)

        def tick--- This code section failed: ---

 176       0  LOAD_DEREF            0  'self'
           3  LOAD_ATTR             0  'sprite'
           6  LOAD_ATTR             1  'getGLProgramState'
           9  CALL_FUNCTION_0       0 
          12  LOAD_ATTR             2  'setUniformFloat'
          15  LOAD_CONST            1  'u_boundary'
          18  LOAD_DEREF            1  'duration'
          21  LOAD_CONST            2  3.0
          24  BINARY_MULTIPLY  
          25  LOAD_GLOBAL           3  'max'
          28  LOAD_GLOBAL           3  'max'
          31  BINARY_SUBTRACT  
          32  LOAD_CONST            4  ''
          35  CALL_FUNCTION_2       2 
          38  BINARY_MULTIPLY  
          39  CALL_FUNCTION_2       2 
          42  POP_TOP          

Parse error at or near `CALL_FUNCTION_2' instruction at offset 39

        def finish():
            self.sprite.setVisible(False)
            self.grid_panel.setVisible(True)
            self.main_item and self.main_item.PlayAnimation('loop')

        tick(0)
        self.main_item and self.main_item.PlayAnimation('loop')
        self.grid_panel.setVisible(False)
        self.sprite.setVisible(True)
        tag = 10087
        self.sprite.StopTimerActionByTag(tag)
        self.sprite.TimerActionByTag(tag, tick, duration, finish)

    def refresh_show_model(self, show_model_id=None):
        self.show_model(show_model_id)

    def show_model(self, item_id):
        self.show_model_id = item_id
        for key, widget in six.iteritems(self.item_dict):
            widget.nd_choose.setVisible(key == item_id)

        if self._selected_callback:
            self._selected_callback(item_id)

    def refresh_item_data(self, item_list):
        if item_list == self.item_list:
            return
        self.item_list = item_list
        self.init_panel()
        self.create_img()
        if self.item_list:
            item_id = self.item_list[0][0]
            self.show_model(item_id)

    def destroy(self):
        self._selected_callback = None
        self.item_dict = {}
        self.item_list = []
        self.percent_up_item_id_set = None
        self.main_item = None
        self.panel = None
        self.sprite = None
        self.grid_panel = None
        if self.rt:
            self.rt.release()
            self.rt = None
        return