#! /usr/bin/env python

import os
import sys

from tcp_server import TCPServer
from manager import Manager


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
    if len(sys.argv) != 3:
        print '[USAGE]'
        print '    %r <listen_port> <data_dir_name>' % sys.argv[0]
        return 1
    try:
        port = int(sys.argv[1])
        msg_dir = os.path.join(sys.argv[2], MSG_DIR)
        file_dir = os.path.join(sys.argv[2], FILE_DIR)
        if not os.path.exists(sys.argv[2]):
            os.mkdir(sys.argv[2])
        try:
            os.mkdir(msg_dir)
            os.mkdir(file_dir)
        except:
            pass
        account_file = os.path.join(sys.argv[2], ACCOUNT_FILE)
        group_file = os.path.join(sys.argv[2], GROUP_FILE)
    except Exception as e:
        print 'Argument with wrong format: %r' % e
        return 1
    server = Server(port, msg_dir, file_dir, account_file, group_file)
    server.start()
    try:
        _ = raw_input()
    except:
        pass
    server.stop()
    server.join()
    return 0
    
        
if __name__ == '__main__':
    sys.exit(main())
    
