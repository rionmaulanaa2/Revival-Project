# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Sep 12 2025, 12:48:39) 
# [GCC Android (13624864, +pgo, +bolt, +lto, +mlgo, based on r530567e) Clang 19.0
# Embedded file name: /Users/netease/Documents/work/battlegrounds/gameplay/releases/rel_current/tools/patch/temp/script/mobile/common/TelnetHandler.py
from __future__ import absolute_import
from __future__ import print_function
import six
import copy
DONT = six.int2byte(254)
DO = six.int2byte(253)
WILL = six.int2byte(251)
WONT = six.int2byte(252)
ECHO = six.int2byte(1)
SGA = six.int2byte(3)
LINEMODE = six.int2byte(34)
ESC = six.int2byte(27)
BSP = six.int2byte(8)
DEL = six.int2byte(127)
SE = six.int2byte(240)
NOP = six.int2byte(241)
SB = six.int2byte(250)
BELL = six.int2byte(7)
NOOPT = six.int2byte(0)
TTYPE = six.int2byte(24)
IAC = six.int2byte(255)
IS = six.int2byte(0)
SEND = six.int2byte(1)
DEFAULT = -1

def log(lg):
    print(lg)


class TelnetHandler(object):
    USEFUL_CMDS = frozenset([DO, DONT, WILL, WONT])
    DOACK = {ECHO: WILL,
       SGA: WILL
       }
    WILLACK = {ECHO: DONT,
       SGA: DO,
       LINEMODE: DONT
       }
    CODES = {'DEL': '\x1b[K',
       'CSRLEFT': '\x1b[D',
       'CSRRIGHT': '\x1b[C'
       }

    def __init__(self, conn):
        self.connection = conn
        self.DOOPTS = {}
        self.WILLOPTS = {}
        self.current_line = []
        self.cursor_ptr = 0
        self.history = []
        self.history_ptr = -1
        self.max_history = 10
        self.sb = 0
        self.sbdataq = ''
        self.iac_sq = ''
        self.ARROW_CMD = {'\x1b[A': self.handle_up,
           '\x1b[B': self.handle_down,
           '\x1b[D': self.handle_left,
           '\x1b[C': self.handle_right
           }
        self.CHAR_HANDLER = {ESC: self.handle_esc,
           BSP: self.handle_backspace,
           DEL: self.handle_del,
           DEFAULT: self.handle_default_char
           }
        self.CMD_HANDLER = {NOP: self.handle_nop,
           WILL: self.handle_will_wont,
           WONT: self.handle_will_wont,
           DO: self.handle_do_dont,
           DONT: self.handle_do_dont,
           SE: self.handle_se,
           SB: self.handle_sb
           }
        self.setup()

    def setup(self):
        for k in self.DOACK:
            self.send_command(self.DOACK[k], k)

        for k in self.WILLACK:
            self.send_command(self.WILLACK[k], k)

    def handle_input(self, data):
        is_complete_line = False
        if data.find('\r\n') >= 0:
            raw_data_lines = data.split('\r\n')
            if data.endswith('\r\n'):
                is_complete_line = True
                raw_data_lines = raw_data_lines[:-1]
        elif data.find('\r\x00') >= 0:
            raw_data_lines = data.split('\r\x00')
            if data.endswith('\r\x00'):
                is_complete_line = True
                raw_data_lines = raw_data_lines[:-1]
        else:
            raw_data_lines = [
             data]
        raw_line_idx = 0
        for raw_line in raw_data_lines:
            raw_line_idx += 1
            self.process_raw_line(raw_line)
            if is_complete_line or raw_line_idx < len(raw_data_lines):
                if len(self.current_line) > 0:
                    self.history.append(self.current_line)
                    self.history_ptr = len(self.history)
                else:
                    self.current_line.append('\n')
                self.write_text('\r\n')
                self.connection.receive_handler(self.connection, ''.join(self.current_line))
                self.current_line = []
                self.cursor_ptr = 0
                while len(self.history) > self.max_history:
                    self.history = self.history[1:]
                    self.history_ptr -= 1

    def process_raw_line(self, raw_line):
        idx = 0
        while idx < len(raw_line):
            ch = raw_line[idx]
            if ch == IAC or len(self.iac_sq) > 0 or self.sb == 1:
                idx_offset = self.process_cmd(raw_line)
                idx += idx_offset
                continue
            if ch in self.CHAR_HANDLER:
                idx_offset = self.CHAR_HANDLER[ch](raw_line, idx)
            else:
                idx_offset = self.CHAR_HANDLER[DEFAULT](ch)
            idx += idx_offset

    def negotiation_handler(self, cmd, opt):
        if cmd in self.CMD_HANDLER:
            self.CMD_HANDLER[cmd](cmd, opt)
        else:
            log('Unhandled option: %s %s' % (ord(cmd), ord(opt)))

    def read_sb_data(self):
        buf = self.sbdataq
        self.sbdataq = ''
        return buf

    def process_cmd(self, iac_str):
        idx = 0
        while idx < len(iac_str):
            c = iac_str[idx]
            if not self.iac_sq:
                if c == IAC:
                    self.iac_sq += c
                elif self.sb == 1:
                    self.sbdataq += c
                idx += 1
                continue
            elif len(self.iac_sq) == 1:
                if c in self.USEFUL_CMDS:
                    self.iac_sq += c
                    idx += 1
                    continue
                self.iac_sq = ''
                if c == SB:
                    self.sb = 1
                    self.sbdataq = ''
                    idx += 1
                    continue
                elif c == SE:
                    self.sb = 0
                    self.negotiation_handler(c, NOOPT)
                    idx += 1
                    break
                else:
                    log('Unknown Comand: ', ord(c))
                    idx += 1
                    break
            elif len(self.iac_sq) == 2:
                cmd = self.iac_sq[1]
                self.iac_sq = ''
                if cmd in self.USEFUL_CMDS:
                    self.negotiation_handler(cmd, c)
                    idx += 1
                    break

        return idx

    def handle_up(self):
        if self.history_ptr > 0:
            right_of_cursor = len(self.current_line) - self.cursor_ptr
            self.write_text(self.CODES['CSRRIGHT'] * right_of_cursor)
            self.write_text((self.CODES['CSRLEFT'] + self.CODES['DEL']) * len(self.current_line))
            self.history_ptr -= 1
            last_cmd = copy.deepcopy(self.history[self.history_ptr])
            self.write_text(''.join(last_cmd))
            self.current_line = last_cmd
            self.cursor_ptr = len(self.current_line)
        else:
            self.write_text(BELL)

    def handle_down(self):
        if self.history_ptr < len(self.history):
            right_of_cursor = len(self.current_line) - self.cursor_ptr
            self.write_text(self.CODES['CSRRIGHT'] * right_of_cursor)
            self.write_text((self.CODES['CSRLEFT'] + self.CODES['DEL']) * len(self.current_line))
            self.history_ptr += 1
            if self.history_ptr >= len(self.history):
                next_cmd = []
            else:
                next_cmd = copy.deepcopy(self.history[self.history_ptr])
            self.write_text(''.join(next_cmd))
            self.current_line = next_cmd
            self.cursor_ptr = len(self.current_line)
        else:
            self.write_text(BELL)

    def handle_left(self):
        if self.cursor_ptr > 0:
            self.cursor_ptr -= 1
            self.write_text(self.CODES['CSRLEFT'])
        else:
            self.write_text(BELL)

    def handle_right(self):
        if self.cursor_ptr < len(self.current_line):
            self.cursor_ptr += 1
            self.write_text(self.CODES['CSRRIGHT'])
        else:
            self.write_text(BELL)

    def handle_default_char(self, ch):
        self.current_line.insert(self.cursor_ptr, ch)
        self.cursor_ptr += 1
        self.write_text(ch)
        self.restore_right_half_line()
        return 1

    def handle_esc(self, raw_line, idx):
        if raw_line[idx:idx + 3] in self.ARROW_CMD:
            self.ARROW_CMD[raw_line[idx:idx + 3]]()
        return 3

    def handle_backspace(self, raw_line, idx):
        if self.cursor_ptr > 0:
            self.write_text(self.CODES['CSRLEFT'] + self.CODES['DEL'])
            self.cursor_ptr -= 1
            del self.current_line[self.cursor_ptr]
            self.restore_right_half_line()
        return 1

    def handle_del(self, raw_line, idx):
        if self.cursor_ptr < len(self.current_line):
            self.write_text(self.CODES['DEL'])
            del self.current_line[self.cursor_ptr]
            self.restore_right_half_line()
        return 1

    def handle_nop(self, cmd, opt):
        self.send_command(NOP)

    def handle_will_wont(self, cmd, opt):
        if opt in self.WILLACK:
            self.send_command(self.WILLACK[opt], opt)
        else:
            self.send_command(DONT, opt)
        if cmd == WILL and opt == TTYPE:
            self.write_cooked(IAC + SB + TTYPE + SEND + IAC + SE)

    def handle_do_dont(self, cmd, opt):
        if opt in self.DOACK:
            self.send_command(self.DOACK[opt], opt)
        else:
            self.send_command(WONT, opt)

    def handle_se(self, cmd, opt):
        subreq = self.read_sb_data()
        if subreq[0] == TTYPE and subreq[1] == IS:
            pass

    def handle_sb(self, cmd, opt):
        pass

    def restore_right_half_line(self):
        if self.cursor_ptr < len(self.current_line):
            self.write_text(''.join(self.current_line[self.cursor_ptr:]))
            cursor_offset = len(self.current_line) - self.cursor_ptr
            self.write_text(self.CODES['CSRLEFT'] * cursor_offset)

    def send_command(self, cmd, opt=None):
        if cmd in [DO, DONT]:
            if opt not in self.DOOPTS:
                self.DOOPTS[opt] = None
            if cmd == DO and self.DOOPTS[opt] != True or cmd == DONT and self.DOOPTS[opt] != False:
                self.DOOPTS[opt] = cmd == DO
                self.write_cooked(IAC + cmd + opt)
        elif cmd in [WILL, WONT]:
            if opt not in self.WILLOPTS:
                self.WILLOPTS[opt] = None
            if cmd == WILL and self.WILLOPTS[opt] != True or cmd == WONT and self.WILLOPTS != False:
                self.WILLOPTS[opt] = cmd == WILL
                self.write_cooked(IAC + cmd + opt)
        else:
            self.write_cooked(IAC + cmd)
        return

    def write_text(self, text):
        text = str(text)
        text = text.replace(IAC, IAC + IAC)
        text = text.replace(six.int2byte(10), six.int2byte(13) + six.int2byte(10))
        self.write_cooked(text)

    def write_cooked(self, text):
        self.connection.send_data(text)