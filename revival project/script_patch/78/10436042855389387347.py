# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageImp/DivergeManagers/VariableCheckers.py
_Checkers = {}

def getChecker(comparator):
    return _Checkers.get(comparator, None)


class registerChecker(object):

    def __init__(self, comparator):
        self.comparator = comparator

    def __call__(self, checker):
        _Checkers[self.comparator] = checker
        return checker


@registerChecker('==')
def checkEqual(left, right):
    return left == right


@registerChecker('!=')
def checkNotEqual(left, right):
    return left != right


@registerChecker('>')
def checkGreater(left, right):
    return left > right


@registerChecker('<')
def checkLess(left, right):
    return left < right


@registerChecker('>=')
def checkGreaterEqual(left, right):
    return left >= right


@registerChecker('<=')
def checkLessEqual(left, right):
    return left <= right


@registerChecker('has')
def checkHas(left, right):
    if isinstance(left, (list, set, tuple)):
        return right in left
    return right == left


@registerChecker('in')
def checkIn(left, right):
    if isinstance(right, (list, set, tuple)):
        return left in right
    return left == right