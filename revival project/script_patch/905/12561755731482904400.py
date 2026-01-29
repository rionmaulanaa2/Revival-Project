# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/rpyc_controller.py
from __future__ import absolute_import
from __future__ import print_function
import six_ex
import sys
import time
import rpyc
try:
    import six.moves.queue
except:
    import queue as Queue

import six.moves.builtins
import threading
from threading import Thread
from rpyc.core.service import SlaveService
from rpyc.utils.server import ThreadedServer

def get_lobby_player():
    return global_data.lobby_player


def get_player():
    return global_data.player


def get_cam_lplayer():
    return global_data.cam_lplayer


def get_cam_lctarget():
    return global_data.cam_lctarget


def get_game_mgr():
    return global_data.game_mgr


class Server(Thread):

    def __init__(self, *args, **kwargs):
        super(Server, self).__init__(*args, **kwargs)
        self._rpyc_server = None
        self.dispatch_timer_id = None
        self._rpyc_call_queue = six.moves.queue.Queue()
        six.moves.builtins.__dict__['g_rpyc_server'] = self
        return

    def register_timer(self):
        from common.utils.timer import CLOCK
        self.unregister_timer()
        self.dispatch_timer_id = global_data.game_mgr.get_logic_timer().register(func=self.dispatch_remote_call)

    def unregister_timer(self):
        if self.dispatch_timer_id:
            global_data.game_mgr.get_logic_timer().unregister(self.dispatch_timer_id)
        self.dispatch_timer_id = None
        return

    def rpyc_teleport_callback(self, callback):
        self._rpyc_call_queue.put(callback)

    def dispatch_remote_call(self):
        while not self._rpyc_call_queue.empty():
            callback = self._rpyc_call_queue.get()
            callback()

    def run(self):
        self.register_timer()
        self._rpyc_server = ThreadedServer(SlaveService, auto_register=False, hostname='localhost', port=18812)
        self._rpyc_server.start()


def copy_remote_proxy(proxy):
    return rpyc.classic.obtain(proxy)


def _put_server_callback(callback):
    print('>>> _put_server_callback')
    g_rpyc_server.rpyc_teleport_callback(callback)


def rpyc_teleport(conn, callback, globals=None):
    from rpyc.utils.classic import teleport_function
    command_remote = teleport_function(conn, _put_server_callback)
    command_remote2 = teleport_function(conn, callback, globals=globals)
    command_remote(command_remote2)


def remote_exec(conn, str_code):
    wrap_code = 'from rpyc_controller import *\ndef cb():\n\t{}\ng_rpyc_server.rpyc_teleport_callback(cb)\n'.format(str_code)
    conn.execute(wrap_code)


def create_rpyc_server():
    s = Server()
    s.daemon = True
    s.start()
    return s


def create_rpyc_client():
    conn = rpyc.classic.connect('localhost', 18812)
    return conn


def create_slave_editor():
    import os
    import six.moves._thread
    import render
    import game3d
    from cocosui import cc
    size = global_data.ui_mgr.design_screen_size
    width = int(size.width)
    height = int(size.height)
    tex = render.texture.create_empty_ext(width, height, render.PIXEL_FMT_A8R8G8B8, True, 1, 'py_shared')
    tex.create_shared_handle()
    rt = cc.Texture2D.createWithITexture(tex)
    sprite = cc.Sprite.createWithTexture(rt)
    p = global_data.ui_mgr.create_simple_dialog('battle/empty').panel
    p.addChild(sprite)
    sprite.setPosition(cc.Vec2(width * 0.5, height * 0.5))

    def cb():
        handle = tex.get_shared_handle()
        print(handle)
        os.chdir('F:\\svn\\g93\\develop\\client\\gameplay\\pyfx11')
        six.moves._thread.start_new_thread(os.system, ('python27x64 present_demo.py {}'.format(handle),))

    game3d.delay_exec(500, cb)


if __name__ == '__main__':
    print('__main__', sys.argv)
    side = sys.argv[1]
    if side == 's':
        s = create_rpyc_server()
        import time
        while True:
            time.sleep(0.1)

    else:
        conn = create_rpyc_client()
        orgi_modules = set(six_ex.keys(sys.modules))
        r = conn.modules
        r_b = conn.builtins
        r_c = r.rpyc_controller
        lobby_player = r_c.get_lobby_player()
        p = lobby_player.ev_g_model()
        socket_count = p.get_socket_count()
        mat = p.get_socket_matrix(0, r.world.SPACE_TYPE_WORLD)
        print('>>> lobby_player', p, socket_count, mat.forward, lobby_player.ev_g_model_position().x)

        def delay():
            p = get_lobby_player().ev_g_model()
            p.visible = False


        remote_exec(conn, 'get_lobby_player().ev_g_model().visible = True')
        game_mgr = r_c.get_game_mgr()
        scn = game_mgr.get_cur_scene()
        active_camera = scn.active_camera
        print('>>> scene', scn, active_camera.position, active_camera.fov, active_camera.aspect, active_camera.z_range)