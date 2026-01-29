# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/sunshine/SunshineSDK/Plugin/HunterPlugin/safaia/build_qa_test2.py
base = open('safaia_base.py').read().decode('utf-8').encode('gbk')
qatest = open('qa_test2.py').read().decode('utf-8').encode('gbk')
output = open('qa_test2.py.build', 'w')
output.write(qatest.replace('from safaia_base import SafaiaBase', base))
output.close()