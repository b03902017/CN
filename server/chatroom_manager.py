import re


def _log(s):
    print 'Permission: %s' % s


class ChatroomManager(object):
    def __init__(self, file_name, account_manager):
        self._file_name = file_name
        self._groups = {}
        self._account_manager = account_manager
        try:
            with open(self._file_name, 'r') as f:
                for line in f.readlines():
                    words = [w for w in re.split(r'[.\n\r]', line) if w]
                    self._groups[words[0]] = words[1:]
                    _log('add groups %r' % words)
        except Exception:
            pass

    def flush(self):
        try:
            with open(self._file_name, 'w') as f:
                for name in self._groups:
                    f.write('.'.join([name] + self._groups[name]) + '\n')
        except Exception:
            pass

    def get_chatroom_name(self, name, username):
        if name.startswith('g_'):
            return name
        return '.'.join(sorted([name, username]))

    def new_group(self, name, users):
        name = 'g_' + name
        #print users
        if name in self._groups or users == None:
            return False
        _log('New group %r:%r' % (name, users))
        self._groups[name] = users
        return True

    def permit(self, name, user):
        if name in self._groups and user in self._groups[name]:
            _log('group, valid permission %r:%r' % (name, user))
            return True
        elif name in self._account_manager._users.keys():
            _log('chat, valid permission %r:%r' % (name, user))
            return True
        else:
            _log('invalid permission %r:%r' % (name, user))
            return False
