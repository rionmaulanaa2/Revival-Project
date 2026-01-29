# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageImp/DivergeManagers/VariablesManager.py
from __future__ import absolute_import
import json
from .MontageVariables import MontageVariable

class VariablesManager(object):

    def __init__(self):
        self.variables = {}

    def getVariable(self, name):
        return self.variables.get(name, None)

    def getValue(self, name):
        variable = self.getVariable(name)
        if variable:
            return variable.getValue()

    def operate(self, name, operator, value, tp):
        variable = self.getVariable(name)
        if variable:
            variable.operate(operator, value)
        elif operator == '=':
            variable = MontageVariable.createVariable(tp, value)
            self.variables[name] = variable

    def check(self, data):
        comparator = data['comparator']
        if comparator == 'and':
            for childData in data['children']:
                if not self.check(childData):
                    return False

            return True
        if comparator == 'or':
            for childData in data['children']:
                if self.check(childData):
                    return True

            return False
        if comparator == 'not':
            childData = data['child']
            return not self.check(childData)
        name = data['variable']
        refValue = json.loads(data['ref'])
        variable = self.getVariable(name)
        if variable:
            return variable.check(comparator, refValue)
        raise 'No such variable (%s) exists.' % name