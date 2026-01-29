# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/caches.py
from __future__ import absolute_import
import world
from common.framework import SingletonBase

def fun_cache(max_size=128):

    def decorator(func):
        caches = {}

        def wrapper(*args):
            if args in caches:
                return caches[args]
            result = func(*args)
            if len(caches) > max_size:
                caches.clear()
            caches[args] = result
            return result

        wrapper.cache_clear = lambda : caches.clear()
        return wrapper

    return decorator


class TrackCache(SingletonBase):
    ALIAS_NAME = 'track_cache'

    def __init__(self):
        self.cache = {}

    def create_track(self, track_path):
        if track_path in self.cache:
            return self.cache[track_path]
        track = world.track(track_path)
        self.cache[track_path] = track
        return track

    def create_track_default_none(self, track_path):
        if track_path in self.cache:
            return self.cache[track_path]
        else:
            try:
                track = world.track(track_path)
            except:
                track = None

            self.cache[track_path] = track
            return track

    def create_track_spline(self, key):
        track = world.track(world.TRACK_TYPE_SPLINE)
        return track

    def clear_cache(self):
        self.cache = {}