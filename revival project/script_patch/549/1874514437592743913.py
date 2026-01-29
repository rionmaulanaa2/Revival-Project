# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/common/algorithm/quadtree.py
from __future__ import absolute_import
from six.moves import range

class Rect(object):

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def clone(self, rect2):
        self.x = rect2.x
        self.y = rect2.y
        self.width = rect2.width
        self.height = rect2.height

    def union(self, rect2, rectout):
        rectout.x = min(self.x, rect2.x)
        rectout.y = min(self.y, rect2.y)
        rectout.width = max(self.x + self.width, rect2.x + rect2.width) - rectout.x
        rectout.height = max(self.y + self.height, rect2.y + rect2.height) - rectout.y
        return rectout

    def intersect(self, rect2):
        intersect = not (self.x > rect2.x + rect2.width or self.x + self.width < rect2.x or self.y > rect2.y + rect2.height or self.y + self.height < rect2.y)
        return intersect

    def contain(self, rect2):
        return self.x <= rect2.x and self.y <= rect2.y and rect2.x + rect2.width <= self.x + self.width and rect2.y + rect2.height <= self.y + self.height

    def contain_point(self, x, y):
        return x >= self.x and x <= self.x + self.width and y >= self.y and y <= self.y + self.height

    def __str__(self):
        return 'Rect:[{0}, {1}, {2}, {3}]'.format(self.x, self.y, self.width, self.height)


BOUND_NONE = 0
BOUND_INTERSECT = 1
BOUND_CONTAIN = 2

class QuadNode(object):

    def __init__(self):
        self.objects = None
        self.bound = None
        self.height = -1
        self.children = None
        return


class StaticQuadtree(object):

    def __init__(self, boundObjectArray, splitThreshold=10, maxHeight=10):
        self.splitThreshold = splitThreshold
        self.maxHeight = maxHeight
        self.root = QuadNode()
        boundTotal = Rect(0, 0, 0, 0)
        boundTotal.clone(boundObjectArray[0].bound)
        for boundObject in boundObjectArray:
            boundTotal.union(boundObject.bound, boundTotal)

        self.root.objects = boundObjectArray
        self.root.bound = boundTotal
        self.root.height = 1
        self.split(self.root)

    def split(self, quadNode):
        global BOUND_NONE
        global BOUND_CONTAIN
        global BOUND_INTERSECT
        if quadNode.height >= self.maxHeight or not quadNode.objects or len(quadNode.objects) < self.splitThreshold:
            return
        else:
            for obj in quadNode.objects:
                obj.intersectType = BOUND_NONE

            children = []
            halfW, halfH = quadNode.bound.width / 2, quadNode.bound.height / 2
            for i in range(2):
                for j in range(2):
                    childBound = Rect(quadNode.bound.x + j * halfW, quadNode.bound.y + i * halfH, halfW, halfH)
                    childObjects = []
                    for obj in quadNode.objects:
                        if childBound.intersect(obj.bound):
                            childObjects.append(obj)
                            obj.intersectType = childBound.contain(obj.bound) and BOUND_CONTAIN or BOUND_INTERSECT

                    node = QuadNode()
                    node.bound = childBound
                    node.objects = childObjects
                    node.height = quadNode.height + 1
                    children.append(node)

            quadNode.children = children
            quadNode.objects = None
            for child in children:
                self.split(child)

            return

    def quary_by_rect(self, rect):
        ret = {}
        self.__quary_by_rect(self.root, rect, ret)
        return ret

    def __quary_by_rect(self, node, rect, arrayOut):
        if node.bound.intersect(rect):
            if node.objects:
                for obj in node.objects:
                    if rect.intersect(obj.bound):
                        arrayOut[obj] = 1

            if node.children:
                for child in node.children:
                    self.__quary_by_rect(child, rect, arrayOut)

    def __quary_by_rect2(self, rect, arrayOut):
        searchArray = [self.root]
        searchStartIdx = 1
        while searchStartIdx < len(searchArray):
            node = searchArray[searchStartIdx]
            if node.bound.intersect(rect):
                if node.objects:
                    for obj in node.objects:
                        if rect.intersect(obj.bound):
                            arrayOut[obj] = 1

                if node.children:
                    for child in node.children:
                        searchArray.append(child)

            searchStartIdx += 1


class GridQuery(object):
    GRID_SIZE = 1024

    def __init__(self, sceneArray):
        min_x = min_y = max_x = max_y = 1
        grid_size = GridQuery.GRID_SIZE
        for item in sceneArray:
            start_x, start_y = item.bound.x, item.bound.y
            min_x = min(min_x, start_x)
            min_y = min(min_y, start_y)
            max_x = max(max_x, start_x + grid_size)
            max_y = max(max_y, start_y + grid_size)

        row_offset = (1 - min_y) / grid_size
        col_offset = (1 - min_x) / grid_size
        row_count = max_y / grid_size + row_offset
        col_count = max_x / grid_size + col_offset
        self.row_count = row_count
        self.col_count = col_count
        self.col_offset = col_offset
        self.row_offset = row_offset
        self.grids = [ [None] * col_count for i in range(row_count) ]
        for item in sceneArray:
            start_x, start_y = item.bound.x, item.bound.y
            row = start_y / grid_size + row_offset
            col = start_x / grid_size + col_offset
            self.grids[row][col] = item

        return

    def quary_by_rect(self, rect):
        ret = []
        row_count = self.row_count
        col_count = self.col_count
        grid_size = GridQuery.GRID_SIZE
        mid_col = (rect.x + rect.width / 2) / grid_size + self.col_offset
        mid_row = (rect.y + rect.height / 2) / grid_size + self.row_offset
        if 0 <= mid_row < row_count and 0 <= mid_col < col_count:
            mid_scene = self.grids[mid_row][mid_col]
            if mid_scene:
                ret.append(mid_scene)
                if mid_scene.bound.contain(rect):
                    return ret
        for offset_x in range(-1, 2):
            for offset_y in range(-1, 2):
                if offset_y == offset_x == 0:
                    continue
                x = mid_col + offset_x
                y = mid_row + offset_y
                if 0 <= x < col_count and 0 <= y < row_count:
                    scene = self.grids[y][x]
                    if scene and scene.bound.intersect(rect):
                        ret.append(scene)

    def get_data_by_xy(self, x, y):
        row = y / GridQuery.GRID_SIZE + self.row_offset
        col = x / GridQuery.GRID_SIZE + self.col_offset
        return self.grids[row][col]