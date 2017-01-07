import re

def _log(s):
    print 'Account: %s' % s

class AccountManager(object):
    def __init__(self, file_name):
        self._file_name = file_name
        self._users = {}
        try:
            with open(self._file_name, 'r') as f:
                for line in f.readlines():
                    try:
                        u, p = [w for w in re.split(r'[ \n\r]', line) if w]
                        _log('Init existing accounts <%s, %s>' % (u, p))
                        self._users[u] = p
                    except Exception:
                        pass
        except Exception:
            pass

    def valid(self, user, password):
        if user in self._users and self._users[user] == password:
            _log('Valid account <%s, %s>' % (user, password))
            return True
        else:
            _log('Invalid account <%s, %s>' % (user, password))
            return False

    def register(self, user, password):
        if user in self._users:
            _log('User %s exists already' % user)
            return False
        self._users[user] = password
        _log('Add new account <%s, %s>' % (user, password))
        return True

    def flush(self):
        try:
            with open(self._file_name, 'w') as f:
                for user in self._users:
                    f.write('%s %s\n' % (user, self._users[user]))
        except Exception:
            pass
