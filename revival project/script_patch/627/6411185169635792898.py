# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/logic/comsys/concert/pylrc/parser.py
from __future__ import absolute_import
import re
import six
from .classes import Lyrics, LyricLine
from .utilities import validateTimecode
synced_line_regex = re.compile('^(\\[[0-5]?\\d:[0-5]?\\d(\\.\\d+)?\\])+.*', flags=re.MULTILINE)

def parse(lrc):
    lines = lrc.splitlines()
    lyrics = Lyrics()
    items = []
    for line in lines:
        if line:
            line = six.ensure_str(line)
        if not line:
            continue
        elif line.startswith('[ar:'):
            lyrics.artist = line.rstrip()[4:-1].lstrip()
        elif line.startswith('[ti:'):
            lyrics.title = line.rstrip()[4:-1].lstrip()
        elif line.startswith('[al:'):
            lyrics.album = line.rstrip()[4:-1].lstrip()
        elif line.startswith('[au:'):
            lyrics.author = line.rstrip()[4:-1].lstrip()
        elif line.startswith('[by:'):
            lyrics.lrc_creator = line.rstrip()[4:-1].lstrip()
        elif line.startswith('[length:'):
            lyrics.length = line.rstrip()[8:-1].lstrip()
        elif line.startswith('[offset:'):
            try:
                lyrics.offset = int(line.rstrip()[8:-1].lstrip())
            except ValueError:
                pass

        elif line.startswith('[re:'):
            lyrics.editor = line.rstrip()[4:-1].lstrip()
        elif line.startswith('[ve:'):
            lyrics.version = line.rstrip()[4:-1].lstrip()
        elif synced_line_regex.match(line):
            text = ''
            first = True
            for split in reversed(line.split(']')):
                if validateTimecode(split + ']'):
                    lyric_line = LyricLine(split + ']', text=text)
                    items.append(lyric_line)
                else:
                    if not first:
                        split += ']'
                    else:
                        first = False
                    text = split + text

    lyrics.extend(sorted(items))
    if not lyrics.offset == 0:
        millis = lyrics.offset
        minutes = int(millis / 60000)
        millis -= minutes * 60000
        secs = int(millis / 1000)
        millis -= secs * 1000
        for line in lyrics:
            line.shift(minutes=minutes, seconds=secs, milliseconds=millis)

        lyrics.offset = 0
    return lyrics