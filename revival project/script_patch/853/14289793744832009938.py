# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageImp/DivergeManagers/DivergeManager.py
from __future__ import absolute_import
from functools import partial
import MontageSDK
from MontageImp.DivergeManagers.VariablesManager import VariablesManager

class DivergeManager(object):

    def __init__(self):
        self.variableManager = VariablesManager()

    def handleSelectDiverge(self, data, switchFunc=None, optionsFunc=None):
        switchBranch = switchFunc or self.switchBranch
        showOptions = optionsFunc or self.showOptions
        title = data['title']
        timeLimit = data['timeLimit']
        branches = data['branches']
        time = data.get('time', 0)
        if timeLimit:
            limitSecond = data['limitSecond']
            overtimeBranch = data['overtimeBranch']
            hidden = data['hidden']
            if hidden:
                options = [ (branch['title'], partial(switchBranch, branch['branch'], time)) for branch in branches if branch['branch'] != overtimeBranch ]
            else:
                options = [ (branch['title'], partial(switchBranch, branch['branch'], time)) for branch in branches ]
            MontageSDK.Interface.PauseCinematics(True)
            showOptions(title=title, options=options, waitTime=limitSecond, overtimeCallback=partial(switchBranch, overtimeBranch, time))
        else:
            options = [ (branch['title'], partial(switchBranch, branch['branch'], time)) for branch in branches ]
            MontageSDK.Interface.PauseCinematics(True)
            showOptions(title=title, options=options)

    def handleConditionDiverge(self, data, switchFunc=None):
        switchBranch = switchFunc or self.switchBranch
        branches = data['branches']
        time = data.get('time', 0)
        for branch in branches:
            data = {'comparator': 'and','children': branch.get('conditions', [])
               }
            if self.variableManager.check(data):
                switchBranch(branch['branch'], time)
                break

    def handleSetVar(self, data):
        name = data['name']
        operator = data['operator']
        tp = data['type']
        value = data['value%s' % tp]
        self.variableManager.operate(name, operator, value, tp)

    def switchBranch(self, branchName=None, time=0.0, *args):
        branchName = branchName or '_master'
        groupName = MontageSDK.Interface.getDefaultGroupName()
        MontageSDK.Interface.SwitchToBranch(groupName, branchName)
        MontageSDK.Interface.PauseCinematics(False)

    def showOptions(self, title, options, waitTime=None, overtimeCallback=None):
        pass


DivergeManagerIns = DivergeManager()