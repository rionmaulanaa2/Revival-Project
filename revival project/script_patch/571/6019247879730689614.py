# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/tools/json_tools/ReSaveAllJson.py
import threading
to_be_list = []
lock = threading.Lock()

def ReSaveAllJson():
    global to_be_list
    import os

    def work(idx, name_list):
        print (
         'name_list ', idx, len(name_list))
        cmd = 'start/wait K:/g48trunk/common_tools/uieditor%s/cocomate.exe -console enable -lua_cmd @OpenAndSaveByName@%s' % (str(idx), '@'.join(name_list))
        b = os.popen(cmd)
        text2 = b.read()
        print text2
        b.close()

    def walk_dir(path, to_be_list):
        for root, dirs, files in os.walk(path):
            for name in files:
                if name.endswith('.json'):
                    full_path = os.path.join(root, name)
                    full_path = full_path.replace('\\', '/')
                    to_be_list.append(full_path)

    import os.path
    import logic
    import threading
    res_path = os.path.abspath(logic.__path__[0] + os.path.sep + '..' + os.path.sep + '..' + os.path.sep + 'res')
    walk_dir(res_path + '/gui/template', to_be_list)
    res_path = os.path.abspath(logic.__path__[0] + os.path.sep + '..' + os.path.sep + '..' + os.path.sep + 'res_cn')
    walk_dir(res_path + '/gui/template', to_be_list)

    def dispatch_work(idx):
        global lock
        global to_be_list
        print (
         'dispatch_work', idx, len(to_be_list))
        while True:
            lock.acquire()
            num_require = 15
            if len(to_be_list) > num_require:
                sub_list = to_be_list[0:num_require]
                to_be_list = to_be_list[num_require:-1]
            else:
                sub_list = list(to_be_list)
                to_be_list = []
            lock.release()
            print ('after dispatch_work ', idx, len(to_be_list))
            if sub_list:
                print (
                 'work ', idx, len(sub_list))
                work(idx, sub_list)
            else:
                break

    import threading
    threads = []
    for i in xrange(4):
        t1 = threading.Thread(target=dispatch_work, args=[i + 1])
        threads.append(t1)
        t1.setDaemon(True)
        t1.start()

    print 'all over'