import json
import socket


class TYPE:
    SUCC = 'succ'
    FAIL = 'fail'
    REGISTER = 'register'
    LOGIN = 'login'
    LOGOUT = 'logout'
    LIST_USERS = 'list_users'
    LIST_GROUPS = 'list_groups'
    CREATE_GROUP = 'create_group'
    SEND_FILE = 'send_file'
    RECV_FILE = 'recv_file'
    SEND_MSG = 'sned_msg'
    RECV_MSGS = 'recv_msg'

class JSON_TOKEN:
    TYPE = 'type'
    USERNAME = 'username'
    PASSWORD = 'password'
    USERS = 'users'
    GROUPS = 'groups'
    TO_NAME = 'to_name'
    GROUP_NAME = 'group_name'
    FILE_NAME = 'file_name'
    FILE_CONTENT = 'file_content'
    SEND_MESSAGE = 'send_message'
    RECV_MESSAGES = 'recv_messages'




def _log(s):
    print 'Connection: %s' % s

class ConnectionError(Exception):
    pass

class Connection(object):

    def __init__(self, sock):
        self._sock = sock

    def close(self):
        self._sock.close()

    def peername(self):
        try:
            return self._sock.getpeername()
        except:
            return ''

    def send(self, json_obj):
        try:
            json_str = json.dumps(json_obj)
            packet = '%010d%s' % (len(json_str), json_str)
            self._sock.sendall(packet)
        except (ValueError, TypeError, socket.error) as e:
            _log('%r' % e)
            raise ConnectionError('send error')

    def try_recv(self, timeout):
        try:
            orig_timeout = self._sock.gettimeout()
            self._sock.settimeout(timeout)
            data_len = int(self._sock.recv(10))
            data_obj = json.loads(self._sock.recv(data_len))
            self._sock.settimeout(orig_timeout)
            return data_obj
        except socket.timeout as e:
            return None
        except (socket.error, ValueError, TypeError) as e:
            _log('%r' % e)
            raise ConnectionError('recv error')
