# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/exception_hook.py
from __future__ import absolute_import
from __future__ import print_function
import sys
import traceback
import game3d
import hashlib
import render
import six
import six.moves.builtins
ERROR_DICT = {}
GAME_VERSION = None
REVERT_WHEN_EXCEPTION = True

def dump_exception_hook(exc_type, exc_value, exc_tb):
    global REVERT_WHEN_EXCEPTION
    try:
        try:
            if exc_type == KeyboardInterrupt:
                game3d.exit()
            else:
                upload_exception(exc_type, exc_value, exc_tb)
        except:
            pass

    finally:
        if exc_type == KeyboardInterrupt:
            return
        if REVERT_WHEN_EXCEPTION:
            print('exception @ patch')
            cancel_revert_when_exception()
            import package_utils
            package_utils.reset_package_info()
            print('revert when error')

            def show_error_box():

                def on_click_ok():
                    game3d.exit()

                game3d.show_msg_box('Error', 'Error', on_click_ok, None, 'Exit', 'cancel')
                render.set_post_logic(None)
                return

            render.set_logic(None)
            render.set_post_logic(show_error_box)
        sys.__excepthook__(exc_type, exc_value, exc_tb)

    return


def post_stack(err_msg):
    import traceback
    error_content = '%s\n' % err_msg
    error_content += '\n'.join(traceback.format_stack())
    post_error(error_content)


def post_error(err_msg, appendix_info='', post_msg=None):
    global ERROR_DICT
    m = hashlib.md5()
    import six
    m.update(six.ensure_binary(err_msg))
    mid = m.hexdigest()
    if mid in ERROR_DICT:
        return False
    ERROR_DICT[mid] = 1
    if appendix_info:
        err_msg = '{} {}'.format(err_msg, appendix_info)
    post_msg = post_msg or err_msg
    game3d.post_script_error(mid, post_msg)
    try:
        pass
    except:
        pass


def get_bit_name():
    try:
        import sys
        if sys.maxsize > 4294967296:
            return '64bit'
        return '32bit'
    except:
        return 'except'


def update_game_version():
    global GAME_VERSION
    import version
    ev = version.get_engine_version()
    sv = version.get_script_version()
    GAME_VERSION = int(sv)
    if not game3d.is_feature_ready('CrashHunter_AbolishClientV'):
        game3d.set_dump_game_version('{0}'.format(ev))
        game3d.set_dump_info('client_v', '{0}({1})'.format(ev, sv))
        if game3d.get_platform() == game3d.PLATFORM_ANDROID:
            game3d.set_dump_basicinfo('client_v:%s(%s),' % (str(ev), str(sv)))
    else:
        game3d.set_dump_game_version('{0}'.format(sv))
    try:
        import social
        channel = social.get_channel()
        if channel:
            app_channel = channel.distribution_channel
            if not app_channel:
                app_channel = channel.name
        else:
            app_channel = 'unknown'
        user = six.moves.builtins.__dict__.get('user', None)
        python_version = 'p2' if six.PY2 else 'p3'
        if user:
            condition_str = '{"sys_arch":["%s",], "channel_name":["%s", ], "user":["%s",],"py_ver":["%s", ]}' % (get_bit_name(), app_channel, user, python_version)
        else:
            condition_str = '{"sys_arch":["%s",], "channel_name":["%s", ],"py_ver":["%s", ]}' % (get_bit_name(), app_channel, python_version)
        game3d.set_dump_info('conditions', condition_str)
    except Exception as e:
        print('[update_game_version ] except: {0}'.format(e))

    return


def cancel_revert_when_exception():
    global REVERT_WHEN_EXCEPTION
    REVERT_WHEN_EXCEPTION = False


def convert_python_tb_to_str(t, v, tb, limit=None):
    tbinfo = []
    tb_local_info = []
    tbinfo_simple = []
    if tb == None:
        return
    else:
        n = 0
        unused_path = '/Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/'
        while tb and (limit is None or n < limit):
            frame = tb.tb_frame
            try:
                local_str = str(frame.f_locals)
            except:
                local_str = 'Cannot print locals'

            if len(local_str) > 5000:
                local_str = 'Exceed max length:' + local_str[:5000]
            line = [
             'File ' + frame.f_code.co_filename, 'line ' + str(tb.tb_lineno), 'in ' + frame.f_code.co_name]
            line_data = ','.join(line)
            tbinfo_simple.append(line_data)
            tbinfo.append(line_data.replace(unused_path, '') + ' (Locals[{}])'.format(len(tb_local_info)))
            tb_local_info.append('Locals[{}]\t\t{}'.format(len(tb_local_info), local_str))
            tb = tb.tb_next
            n = n + 1

        final_tb_info = '\n'.join(tbinfo) + '\n\n' + '\n'.join(tb_local_info)
        return (
         '%s\n%s\n%s' % (str(t), str(v), '\n'.join(tbinfo_simple)), '%s\n%s\n%s' % (str(t), str(v), final_tb_info))


def upload_exception(exc_type, exc_value, exc_tb):
    global GAME_VERSION
    import version
    if GAME_VERSION is None:
        GAME_VERSION = int(version.get_script_version())
    if GAME_VERSION:
        try:
            err_msg, post_msg = convert_python_tb_to_str(exc_type, exc_value, exc_tb, 30)
        except:
            err_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_tb, 30))
            post_msg = None

        post_error(err_msg, post_msg=post_msg)
        return True
    else:
        return True
        return False


def register_hook():
    sys.excepthook = dump_exception_hook


def traceback_uploader():
    dump_exception_hook(*sys.exc_info())


def traceback_post_simple():
    post_error(traceback.format_exc())