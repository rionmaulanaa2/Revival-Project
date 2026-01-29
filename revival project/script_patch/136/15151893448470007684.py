# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/tools/gen_python_stubs.py


def run_gen(stubgen, need_framing=True):

    def generator_callback():
        if not stubgen.generate_one():
            print 'end'

    if need_framing:
        import cc
        director = cc.Director.getInstance()
        gui_scene = director.getRunningScene()
        if not gui_scene:
            gui_scene = cc.Scene.create()
            director.runWithScene(gui_scene)
        gui_scene.runAction(cc.Repeat.create(cc.Sequence.create([
         cc.DelayTime.create(0.1),
         cc.CallFunc.create(generator_callback)]), len(stubgen.modules)))
    else:
        for i in xrange(len(stubgen.modules)):
            generator_callback()


def get_valid_doc(funcdoc):
    if funcdoc:
        try:
            funcdoc = funcdoc.decode('gb18030')
        except UnicodeDecodeError as e:
            pass

    return funcdoc


def gen_code_from_engine(need_framing=True):
    from nxapi_generator.generator import StubGen
    from nxapi_generator.pycharm_generator_utils.constants import IN_ENCODING
    from nxapi_generator.pycharm_generator_utils import constants

    def ensureUnicode(data_in):
        data = data_in
        if type(data) == str:
            try:
                data = data.decode(IN_ENCODING)
            except UnicodeDecodeError as e:
                try:
                    data = data.decode('gb18030')
                except UnicodeDecodeError as e:
                    data = data.decode(IN_ENCODING, 'replace')

            return data
        return unicode(data)

    constants.ensureUnicode = ensureUnicode
    stubgen = StubGen()
    run_gen(stubgen)


def gen_code_from_script(need_framing=True):
    from nxapi_generator.generator import StubGen
    stubgen = StubGen()
    stubgen.modules = []
    targets = [
     ('script/common/uisys', 'common.uisys.'),
     ('script/logic/gutils', 'logic.gutils.')]
    for t in targets:
        import os
        base_dir = os.path.join(os.getcwd(), t[0])
        root_path = base_dir
        for root, dirs, files in os.walk(base_dir):
            for name in files:
                if name.endswith('.py') and not name.startswith('__'):
                    full_path = os.path.join(root, name)
                    rel_p = os.path.relpath(full_path, root_path)
                    module_name = t[1] + rel_p.replace(os.path.sep, '.').replace('.py', '')
                    stubgen.modules.insert(0, (module_name, None))

    run_gen(stubgen)
    return


def gen_main(need_framing=True):
    gen_code_from_script(need_framing)


def test_one():
    from nxapi_generator.generator import StubGen
    stubgen = StubGen()
    stubgen.generate_one()