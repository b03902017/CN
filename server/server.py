#! /usr/bin/env python

import os
import sys

from tcp_server import TCPServer
from manager import Manager

DATA_DIR = 'data'
MSG_DIR = 'msg'
FILE_DIR = 'file'
ACCOUNT_FILE = 'account'
GROUP_FILE = 'group'


class Server(object):
    def __init__(self, port, msg_dir, file_dir, account_file, group_file):
        self._manager = Manager(msg_dir, file_dir, account_file, group_file)
        self._tcp_server = TCPServer(port, self._manager)

    def start(self):
        self._manager.start()
        self._tcp_server.start()

    def stop(self):
        self._manager.stop()
        self._tcp_server.stop()

    def join(self):
        self._manager.join()
        self._tcp_server.join()


def main():
    if len(sys.argv) != 2:
        print '[USAGE]'
        print '    %r [listen port]' % sys.argv[0]
        return 1
    try:
        port = int(sys.argv[1])
        msg_dir = os.path.join(DATA_DIR, MSG_DIR)
        file_dir = os.path.join(DATA_DIR, FILE_DIR)
        if not os.path.exists(DATA_DIR):
            os.mkdir(DATA_DIR)
        try:
            os.mkdir(msg_dir)
            os.mkdir(file_dir)
        except:
            pass
        account_file = os.path.join(DATA_DIR, ACCOUNT_FILE)
        group_file = os.path.join(DATA_DIR, GROUP_FILE)
    except Exception as e:
        print 'Argument with wrong format: %r' % e
        return 1

    server = Server(port, msg_dir, file_dir, account_file, group_file)
    server.start()
    QUIT = False
    while QUIT is not True:
        try:
            input_str = raw_input()
            if input_str == 'QUIT':
                QUIT = True
            else:
                print 'use QUIT to stop server'
        except:
            pass
    server.stop()
    server.join()
    return 0

if __name__ == '__main__':
    sys.exit(main())
