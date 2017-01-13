import threading
import time
import os

from account_manager import AccountManager
from file_manager import FileManager
from message_manager import MessageManager
from chatroom_manager import ChatroomManager

import sys
sys.path.append("../common")
from connection import Connection
from connection import JSON_TOKEN
from connection import TYPE

def _log(s):
    print 'Manager: %s' % s

class UnloginManager(object):
    TIMESTAMP = 1e-2

    def __init__(self, accounts_manage):
        self._accounts_manage = accounts_manage
        self._conns = []
        self._login_conns = []

    def add(self, conn):
        self._conns.append(conn)
        _log('NEW unlogin_connection from %r' % (conn.peername))

    def get_logins(self):
        temp = self._login_conns
        self._login_conns = []
        return temp

    def handle_all(self):
        i = 0
        while i < len(self._conns):
            try:
                pkt = self._conns[i].try_recv(self.TIMESTAMP)
            except Exception as e:
                _log('Remove connection from %r for %r' % (self._conns[i].peername, e))
                del self._conns[i]
                continue
            if pkt:
                if pkt.get(JSON_TOKEN.TYPE) == TYPE.LOGIN:
                    i = self._handler_login(i, pkt)
                elif pkt.get(JSON_TOKEN.TYPE) == TYPE.REGISTER:
                    i = self._handler_register(i, pkt)
            i += 1

    def _handler_login(self, i, pkt):
        username = pkt.get(JSON_TOKEN.USERNAME, '')
        password = pkt.get(JSON_TOKEN.PASSWORD, '')
        if self._accounts_manage.valid(username, password):
            temp = self._safe_send(i, {JASON_TOKEN.TYPE : TYPE.SUCC})
            if temp == i:
                self._login_conns.append((username, self._conns[i]))
                _log('User %s login success' % username)
                del self._conns[i]
                temp = i - 1
            return temp
        else:
            return self._safe_send(i, {JASON_TOKEN.TYPE : TYPE.FAIL})

    def _handler_register(self, i, pkt):
        username = pkt.get(JSON_TOKEN.USERNAME, '')
        password = pkt.get(JSON_TOKEN.PASSWORD, '')
        if self._accounts_manage.register(username, password):
            return self._safe_send(i, {JSON_TOKEN.TYPE : TYPE.SUCC})
        else:
            return self._safe_send(i, {JSON_TOKEN.TYPE : TYPE.FAIL})

    def _safe_send(self, i, json_obj):
        try:
            self._conns[i].send(json_obj)
            return i
        except Exception as e:
            _log('Send exception: %r' % e)
            del self._conns[i]
            return i - 1

class LoginManager(object):
    TIMESTAMP = 1e-2

    def __init__(self, msg_dir, file_dir, group_file, accounts_manage):
        self._accounts_manage = accounts_manage
        self._messages_manage = MessageManager(msg_dir)
        self._files_manage = FileManager(file_dir)
        self._chatrooms_manage = ChatroomManager(group_file, self._accounts_manage)
        self._users = {}
        self._unlogin_conns = []

    def add(self, username, conn):
        self._users.setdefault(username, []).append(conn)

    def get_unlogins(self):
        temp = self._unlogin_conns
        self._unlogin_conns = []
        return temp

    def flush(self):
        self._messages_manage.flush()
        self._chatrooms_manage.flush()
        self._accounts_manage.flush()

    def handle_all(self):
        for username in self._users.keys():
            i = 0
            while i < len(self._users.get(username, [])):
                try:
                    pkt = self._users[username][i].try_recv(self.TIMESTAMP)
                except Expection as e:
                    _log('Remove connection %r for %r' % (self._usres[username][i].peername, e))
                    del self._users[username][i]
                    continue
                if pkt:
                    i = self._select_handler(username, i, pkt)
                i += 1

    def _select_handler(self, username, i, pkt):
        if pkt.get(JSON_TOKEN.TYPE) == TYPE.LOGOUT:
            return self._handler_logout(username, i, pkt)
        elif pkt.get(JSON_TOKEN.TYPE) == TYPE.LIST_USERS:
            return self._handler_list_users(username, i, pkt)
        elif pkt.get(JSON_TOKEN.TYPE) == TYPE.LIST_GROUPS:
            return self._handler_list_groups(username, i, pkt)
        elif pkt.get(JSON_TOKEN.TYPE) == TYPE.CREATE_GROUP:
            return self._handler_create_group(username, i, pkt)
        elif pkt.get(JSON_TOKEN.TYPE) == TYPE.SEND_FILE:
            return self._handler_send_file(username, i, pkt)
        elif pkt.get(JSON_TOKEN.TYPE) == TYPE.RECV_FILE:
            return self._handler_recv_file(username, i, pkt)
        elif pkt.get(JSON_TOKEN.TYPE) == TYPE.SEND_MSG:
            return self._handler_send_msg(username, i, pkt)
        elif pkt.get(JSON_TOKEN.TYPE) == TYPE.RECV_MSGS:
            return self._handler_recv_msgs(username, i, pkt)
        else:
            return self._safe_send(username, i, {JSON_TOKEN.TYPE : TYPE.FAIL})

    def _handler_logout(self, username, i, pkt):
        temp = self._safe_send(username, i, {JSON_TOKEN.TYPE : TYPE.SUCC})
        if temp == i:
            self._unlogin_conns.append(self._users[username][i])
            _log('User %r logouted' % username)
            temp = self._remove_conn(username, i)
        return temp

    def _handler_list_users(self, username, i, pkt):
        users = [(user, user in self._users) for user in self._accounts_manage._users.keys()]
        return self._safe_send(username, i, {JSON_TOKEN.TYPE : TYPE.SUCC, JSON_TOKEN.USERS : users})

    def _handler_list_groups(self, username, i, pkt):
        groups = [group for group in self._chatrooms_manage._groups.keys() if self._chatrooms_manage.permit(group, username)]
        return self._safe_send(username, i, {JSON_TOKEN.TYPE : TYPE.SUCC, JSON_TOKEN.GROUPS : groups})

    def _handler_create_group(self, username, i, pkt):
        group_name = pkt.get(JSON_TOKEN.GROUP_NAME, '')
        if self._chatrooms_manage.new_group(group_name, pkt.get(JSON_TOKEN.USERS, []).append(username)):
            return self._safe_send(username, i, {JSON_TOKEN.TYPE : TYPE.SUCC})
        else:
            return self._safe_send(username, i, {JSON_TOKEN.TYPE : TYPE.FAIL})

    def _handler_send_file(self, username, i, pkt):
        to_name = pkt.get(JSON_TOKEN.TO_NAME, '')
        if not self._chatrooms_manage.permit(to_name, username):
            return self._safe_send(username, i, {JSON_TOKEN.TYPE : TYPE.FAIL})
        chatroom_name = self._chatrooms_manage.get_chatroom_name(to_name, username)
        file_processed_name = self._files_manage.upload_to_server(chatroom_name, pkt.get(JSON_TOKEN.FILE_NAME, ''), pkt.get(JSON_TOKEN.FILE_CONTENT, ''))
        return self._handler_send_msg(username, i, {JSON_TOKEN.TO_NAME : to_name, JSON_TOKEN.SEND_MESSAGE : '[%s]upload. Please download by the processed name if processed' % file_processed_name})

    def _handler_recv_file(self, username, i, pkt):
        to_name = pkt.get(JSON_TOKEN.TO_NAME, '')
        if not self._chatrooms_manage.permit(to_name, username):
            return self._safe_send(username, i, {JSON_TOKEN.TYPE : TYPE.FAIL})
        chatroom_name = self._chatrooms_manage.get_chatroom_name(to_name, username)
        content = self._files_manage.get_from_server(chatroom_name, pkt.get(JSON_TOKEN.FILE_NAME, ''))
        if content is None:
            return self._safe_send(username, i, {JSON_TOKEN.TYPE : TYPE.FAIL})
        return self._safe_send(username, i, {JSON_TOKEN.TYPE : TYPE.SUCC, JSON_TOKEN.FILE_CONTENT : content})

    def _handler_send_msg(self, username, i, pkt):
        to_name = pkt.get(JSON_TOKEN.TO_NAME, '')
        if not self._chatrooms_manage.permit(to_name, username):
            return self._safe_send(username, i, {JSON_TOKEN.TYPE : TYPE.FAIL})
        chatroom_name = self._chatrooms_manage.get_chatroom_name(to_name, username)
        self._messages_manage[chatroom_name].add('[%s] %s' % (username, pkt.get(JSON_TOKEN.SEND_MESSAGE, '')))
        return self._safe_send(username, i, {JSON_TOKEN.TYPE : TYPE.SUCC})

    def _handler_recv_msgs(self, username, i, pkt):
        to_name = pkt.get(JSON_TOKEN.TO_NAME, '')
        if not self._chatrooms_manage.permit(to_name, username):
            return self._safe_send(username, i, {JSON_TOKEN.TYPE : TYPE.FAIL})
        chatroom_name = self._chatrooms_manage.get_chatroom_name(to_name, username)
        try:
            msgs = [self._messages_manage[chatroom_name][ind] for ind in range(0, len(self._messages_manage[chatroom_name]))]
            return self._safe_send(username, i, {JSON_TOKEN.TYPE : TYPE.SUCC, JSON_TOKEN.RECV_MESSAGES : msgs})
        except:
            return self._safe_send(username, i, {JSON_TOKEN.TYPE : TYPE.FAIL})

    def _remove_conn(self, username, i):
        del self._users[username][i]
        if not self._users[username]:
            del self._users[username]
        return i - 1

    def _safe_send(self, username, i, json_obj):
        try:
            self._users[username][i].send(json_obj)
            return i
        except Exception as e:
            _log('Send error: %r' % e)
            return self._remove_conn(username, i)
class Manager(threading.Thread):
    TIMESTAMP = 1e-2

    def __init__(self, msg_dir, file_dir, account_file, group_file):
        super(Manager, self).__init__()
        self._accounts_manage = AccountManager(account_file)
        self._unlogins_manage = UnloginManager(self._accounts_manage)
        self._logins_manage = LoginManager(msg_dir, file_dir, group_file, self._accounts_manage)
        self._stop_flag = False

    def stop(self):
        self._stop_flag = True

    def run(self):
        while not self._stop_flag:
            self._unlogins_manage.handle_all()
            for username, conn in self._unlogins_manage.get_logins():
                self._logins_manage.add(username, conn)
            self._logins_manage.handle_all()
            for conn in self._logins_manage.get_unlogins():
                self._unlogins_manage.add(conn)
            time.sleep(self.TIMESTAMP)
        self._logins_manage.flush()

    def manage(self, conn):
        self._unlogins_manage.add(Connection(conn))
