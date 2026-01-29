# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/MontageEditor/MontageEditor.py
import game
import game3d
import MontageSDK
from common.framework import Singleton

def addMath3dMethodForCompatibility():
    import math3d
    math3d.Vector3 = math3d.vector

    def matrix_rotation_zxy(pitch, yaw, roll):
        m4_rot_x = math3d.matrix.make_rotation_x(pitch)
        m4_rot_y = math3d.matrix.make_rotation_y(yaw)
        m4_rot_z = math3d.matrix.make_rotation_z(roll)
        return m4_rot_z * m4_rot_x * m4_rot_y

    math3d.matrix_rotation_zxy = matrix_rotation_zxy


class MontageEditor(Singleton):
    ALIAS_NAME = 'montage_editor'

    def init(self):
        super(MontageEditor, self).init()
        self.sunshine_client = None
        self.has_binded_event = False
        self.uiHelper = None
        self._update_sunshine_timer_id = None
        self.init_montage_parameters()
        addMath3dMethodForCompatibility()
        return

    def init_montage_parameters(self):
        self._is_active_montage = False
        self._is_inited_montage = False
        self._cocos_mouse_listener = None
        self._update_func_list = []
        self._mouse_msg_func_list = []
        self.uniman = None
        return

    def closeMontage(self):
        self.uiHelper = None
        self._update_func_list = []
        self._mouse_msg_func_list = []
        self.uniman = None
        global_data.sunshine_uniman = None
        return

    def on_finalize(self):
        super(MontageEditor, self).on_finalize()
        self.unregister_cocos_mouse_support()
        if self.has_binded_event:
            self.process_event(False)
            self.has_binded_event = False
        if self._update_sunshine_timer_id:
            global_data.game_mgr.unregister_logic_timer(self._update_sunshine_timer_id)
            self._update_sunshine_timer_id = None
        self.closeMontage()
        return

    def setup_montage(self):
        import MontageSDK
        self.init_cocos_mouse_event()
        if not self.has_binded_event:
            self.process_event(True)
            self.has_binded_event = True
        if not self.uiHelper:
            from sunshine.MontageEditor import EditorUIHelper
            self.uiHelper = EditorUIHelper.UIHelper(global_data.cocos_scene)

    def add_editor_update_func(self, func):
        if func not in self._update_func_list:
            self._update_func_list.append(func)

    def remove_editor_update_func(self, func):
        if func in self._update_func_list:
            self._update_func_list.remove(func)

    def process_event(self, is_bind):
        emgr = global_data.emgr
        econf = {'net_login_reconnect_event': self.start_timer,
           'net_reconnect_event': self.start_timer
           }
        if is_bind:
            emgr.bind_events(econf)
        else:
            emgr.unbind_events(econf)

    def on_scene_ready(self):
        if not self.uniman:
            from UniCineDriver.UniCineManager import UniCineManager
            self.setUniMan(UniCineManager())
        from MontageImp.MontGameInterfaceImp import getGameInterface
        from MontageImp.MontCastManagerImp import MontCastManager
        gameInterface = getGameInterface()
        if not self._is_inited_montage:
            gameInterface.RuntimeInit(MontCastManager())
            self._is_inited_montage = True
        if not self._is_active_montage:
            self.setActiveMontage(True)
        if global_data.sunshine_editor:
            if hasattr(global_data.sunshine_editor, 'montage_plugin'):
                global_data.sunshine_editor.montage_plugin.Server.SceneReady()

    def on_scene_destroy(self):
        self.setActiveMontage(False)

    def init_cocos_mouse_event(self):
        import cc
        if global_data.use_sunshine:
            listener = cc.EventListenerMouse.create()
            listener.setOnMouseDownCallback(self.on_mouse_down)
            listener.setOnMouseUpCallback(self.on_mouse_up)
            cc.Director.getInstance().getEventDispatcher().addEventListenerWithFixedPriority(listener, 999999)
            self._cocos_mouse_listener = listener

    def unregister_cocos_mouse_support(self):
        import cc
        if self._cocos_mouse_listener:
            cc.Director.getInstance().getEventDispatcher().removeEventListener(self._cocos_mouse_listener)
            self._cocos_mouse_listener = None
        return

    def on_mouse_down(self, event):
        mouse_type = event.getMouseButton()
        if mouse_type == 0:
            self.on_mouse_msg(game.MSG_MOUSE_DOWN, game.MOUSE_BUTTON_LEFT)
        elif mouse_type == 1:
            self.on_mouse_msg(game.MSG_MOUSE_DOWN, game.MOUSE_BUTTON_RIGHT)
        elif mouse_type == 2:
            self.on_mouse_msg(game.MSG_MOUSE_DOWN, game.MOUSE_BUTTON_MIDDLE)
        else:
            log_error('Unsupported Mouse KEY!', mouse_type)

    def on_mouse_up(self, event):
        mouse_type = event.getMouseButton()
        if mouse_type == 0:
            self.on_mouse_msg(game.MSG_MOUSE_UP, game.MOUSE_BUTTON_LEFT)
        elif mouse_type == 1:
            self.on_mouse_msg(game.MSG_MOUSE_UP, game.MOUSE_BUTTON_RIGHT)
        elif mouse_type == 2:
            self.on_mouse_msg(game.MSG_MOUSE_UP, game.MOUSE_BUTTON_MIDDLE)
        else:
            log_error('Unsupported Mouse KEY!', mouse_type)

    def on_mouse_msg(self, msg, key):
        if not self._is_active_montage:
            return
        for func in self._mouse_msg_func_list:
            func(msg, key)

    def add_mousemsg_listener(self, func):
        if not self._is_active_montage:
            return
        self._mouse_msg_func_list.append(func)

    def setActiveMontage(self, enable):
        if not self._is_inited_montage:
            return
        else:
            self._is_active_montage = enable
            if enable:
                from MontageImp.MontGameInterfaceImp import getGameInterface
                gameInterface = getGameInterface()
                if gameInterface:
                    gameInterface.gizmo.scn = global_data.game_mgr.scene
                    if gameInterface.gizmo.scn and gameInterface.gizmo.scn.valid:
                        gameInterface.gizmo.scn.gizmo_init()
            else:
                from MontageImp.MontGameInterfaceImp import getGameInterface
                gameInterface = getGameInterface()
                if gameInterface:
                    gameInterface.gizmo.scn = None
                from MontageSDK.Lib.MontPathManager import managers
                for name, cls_ins in managers.iteritems():
                    if hasattr(cls_ins, 'clear'):
                        cls_ins.clear()

            return

    def start_timer(self):
        if self._update_sunshine_timer_id:
            global_data.game_mgr.unregister_logic_timer(self._update_sunshine_timer_id)
        import common.utils.timer as timer
        self._update_sunshine_timer_id = global_data.game_mgr.register_logic_timer(self.loop, 1.0 / game3d.get_frame_rate(), times=-1, mode=timer.CLOCK, timedelta=True)

    def loop(self, dt):
        if self.sunshine_client:
            self.sunshine_client.Update()
        for func in self._update_func_list:
            func(dt)

    def setUniMan(self, uniman):
        self.uniman = uniman
        global_data.sunshine_uniman = uniman