# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageImp/DivergeManagers/MontageVariables.py
from .VariableCheckers import getChecker
from .VariableOperators import getOperator
_VariableClses = {}

class registerVariableCls(object):

    def __init__(self, variableType):
        self.variableType = variableType

    def __call__(self, variableCls):
        _VariableClses[self.variableType] = variableCls
        return variableCls


class MontageVariable(object):

    def __init__(self, value):
        self.value = value

    def operate(self, operation, value):
        operator = getOperator(operation)
        if operator:
            self.value = operator(self.value, value)
        else:
            raise 'No such operator (%s) exists.' % operation

    def getValue(self):
        return self.value

    def check(self, comparator, refValue):
        checker = getChecker(comparator)
        if checker:
            return checker(self.value, refValue)
        raise 'No such checker (%s) exists.' % comparator

    @staticmethod
    def createVariable(variableType, data):
        variableCls = _VariableClses.get(variableType, None)
        if variableCls:
            return variableCls(data)
        else:
            return

    @staticmethod
    def fromValue(value):
        return MontageVariable.createVariable('Int', value)


@registerVariableCls('Int')
class IntVariable(MontageVariable):

    def __init__(self, value):
        super(IntVariable, self).__init__(value)
        self.value = int(value)

    def operate(self, operation, value):
        super(IntVariable, self).operate(operation, int(value))

    def check(self, comparator, refValue):
        return super(IntVariable, self).check(comparator, int(refValue))


@registerVariableCls('Float')
class FloatVariable(MontageVariable):

    def __init__(self, value):
        super(FloatVariable, self).__init__(value)
        self.value = float(value)

    def operate(self, operation, value):
        super(FloatVariable, self).operate(operation, float(value))

    def check(self, comparator, refValue):
        return super(FloatVariable, self).check(comparator, float(refValue))


@registerVariableCls('Str')
class StrVariable(MontageVariable):

    def __init__(self, value):
        super(StrVariable, self).__init__(value)
        self.value = str(value)

    def operate(self, operation, value):
        super(StrVariable, self).operate(operation, str(value))

    def check(self, comparator, refValue):
        return super(StrVariable, self).check(comparator, str(refValue))