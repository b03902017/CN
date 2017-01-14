# python2.7
import socket
import sys
sys.path.append("../common")
from connection import Connection
from connection import JSON_TOKEN
from connection import TYPE

TIMEOUT = 0.01

class ServerError(Exception):
    pass

def _get_pkt(conn):
    pkt = None
    while pkt is None:
        try:
            pkt = conn.try_recv(TIMEOUT)
        except:
            raise ServerError('')
    return pkt

def connect(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #sock.settimeout(TIMEOUT)
        sock.connect((ip, port))
        #sock.settimeout(None)
        return Connection(sock)
    except:
        return None

def register(conn, username, password):
    # return succced or not
    conn.send({JSON_TOKEN.TYPE : TYPE.REGISTER,
               JSON_TOKEN.USERNAME : username,
               JSON_TOKEN.PASSWORD : password})
    pkt = _get_pkt(conn)
    return pkt.get(JSON_TOKEN.TYPE) == TYPE.SUCC

def login(conn, username, password):
    # return succced or not
    conn.send({JSON_TOKEN.TYPE : TYPE.LOGIN,
               JSON_TOKEN.USERNAME : username,
               JSON_TOKEN.PASSWORD : password})
    pkt = _get_pkt(conn)
    return pkt.get(JSON_TOKEN.TYPE) == TYPE.SUCC

def logout(conn):
    # return succced or not
    conn.send({JSON_TOKEN.TYPE : TYPE.LOGOUT})
    pkt = _get_pkt(conn)
    return pkt.get(JSON_TOKEN.TYPE) == TYPE.SUCC

def list_users(conn):
    # return [(username, True/False), (username, True/False), ...]
    conn.send({JSON_TOKEN.TYPE : TYPE.LIST_USERS})
    pkt = _get_pkt(conn)
    user_list = [(usr, online) for usr, online in pkt.get(JSON_TOKEN.USERS, [])]
    return user_list

def list_groups(conn):
    # return [group_name, group_name, ......]
    conn.send({JSON_TOKEN.TYPE : TYPE.LIST_GROUPS})
    pkt = _get_pkt(conn)
    return pkt.get(JSON_TOKEN.GROUPS, [])

def create_groups(conn, groupname, users):
    # return succced or not
    conn.send({JSON_TOKEN.TYPE : TYPE.CREATE_GROUP,
               JSON_TOKEN.GROUP_NAME : groupname,
               JSON_TOKEN.USERS : users})
    pkt = _get_pkt(conn)
    return pkt.get(JSON_TOKEN.TYPE) == TYPE.SUCC

def send_files(conn, to_name, files):
    # return succced or not
    for filename, content in files:
        conn.send({JSON_TOKEN.TYPE : TYPE.SEND_FILE,
                   JSON_TOKEN.TO_NAME : to_name,
                   JSON_TOKEN.FILE_NAME : filename,
                   JSON_TOKEN.FILE_CONTENT : content})
        pkt = _get_pkt(conn)
    return pkt.get(JSON_TOKEN.TYPE) == TYPE.SUCC

def recv_file(conn, to_name, file_name):
    conn.send({JSON_TOKEN.TYPE : TYPE.RECV_FILE,
               JSON_TOKEN.TO_NAME : to_name,
               JSON_TOKEN.FILE_NAME : file_name})
    pkt = _get_pkt(conn)
    if pkt.get(JSON_TOKEN.TYPE) != TYPE.SUCC:
        return False
    return pkt.get(JSON_TOKEN.FILE_CONTENT, '')

def send_msg(conn, to_name, msg):
    # return succced or not
    conn.send({JSON_TOKEN.TYPE : TYPE.SEND_MSG,
               JSON_TOKEN.TO_NAME : to_name,
               JSON_TOKEN.SEND_MESSAGE : msg})
    pkt = _get_pkt(conn)
    return pkt.get(JSON_TOKEN.TYPE) == TYPE.SUCC

def recv_msgs(conn, to_name):
    # return msgs = [line1, line2, line3, ...]
    conn.send({JSON_TOKEN.TYPE : TYPE.RECV_MSGS,
               JSON_TOKEN.TO_NAME : to_name})
    pkt = _get_pkt(conn)
    if pkt.get(JSON_TOKEN.TYPE) != TYPE.SUCC:
        return False
    return pkt.get(JSON_TOKEN.RECV_MESSAGES)
