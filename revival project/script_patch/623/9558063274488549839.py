# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageImp/DivergeManagers/VariableOperators.py
_Operators = {}

def getOperator(operation):
    return _Operators.get(operation, None)


class registerOperator(object):

    def __init__(self, operation):
        self.operatorName = operation

    def __call__(self, operator):
        _Operators[self.operatorName] = operator
        return operator


@registerOperator('=')
def operateAssign(left, right):
    return right


@registerOperator('+=')
def operateAddAssign(left, right):
    return left + right


@registerOperator('-=')
def operateSubAssign(left, right):
    return left - right