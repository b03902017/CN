import select
import socket
import threading

BACKLOG = 1024

class TCPServer(threading.Thread):
    TIMESTAMP = 1e-2
    
    def __init__(self, port, manager):
        super(TCPServer, self).__init__()
        self.daemon = True
        self._port = port
        self._manager = manager
        self._server_socket = None
        self._stop_flag = False
        
    def stop(self):
        self._stop_flag = True
    
    def run(self):
        if self.build_server():
            while not self._stop_flag:
                if select.select([self._server_socket], [], [], self.TIMESTAMP)[0]:
                    connect, address = self._server_socket.accept()
                    self._manager.manage(connect)
        
    def build_server(self):
        try:
            self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._server_socket.bind(('0.0.0.0', self._port))
            self._server_socket.listen(BACKLOG)
            return True
        except socket.error as e:
            print 'socket error: %r' % e
            return False
