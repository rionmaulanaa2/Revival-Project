# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/gcommon/monster_skill/MonsterAction.py
CO_GENERATOR = 32

class _Action(object):

    def __init__(self, gen):
        self.gen = gen

    def is_running(self):
        return self.gen.gi_running

    def start(self):
        next(self.gen)

    def exit(self):
        self.gen.close()
        self.gen = None
        return

    def is_valid(self):
        return self.gen is None

    def resume(self, param):
        try:
            if param:
                self.gen.send(param)
            else:
                next(self.gen)
        except StopIteration:
            self.gen = None

        return


def Action(func):
    if not func.__code__.co_flags & CO_GENERATOR:
        raise RuntimeError('func must be a generator', func)

    def _inner_(*args, **kwargs):
        return _Action(func(*args, **kwargs))

    return _inner_