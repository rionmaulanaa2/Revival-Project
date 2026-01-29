# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/MontageSDK/utils/Algorithm.py


def TopoSort(graph):
    inDegrees = dict(((u, 0) for u in graph))
    num = len(inDegrees)
    for u in graph:
        for v in graph[u]:
            inDegrees[v] += 1

    Q = [ u for u in inDegrees if inDegrees[u] == 0 ]
    Seq = []
    while Q:
        u = Q.pop()
        Seq.append(u)
        for v in graph[u]:
            inDegrees[v] -= 1
            if inDegrees[v] == 0:
                Q.append(v)

    if len(Seq) == num:
        return reversed(Seq)
    else:
        return None
        return None