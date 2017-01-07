import os

def _log(s):
    print 'Message: %s' % s

class Message(object):
    def __init__(self, file_name):
        self._file_name = file_name
        self._msgs = []
        try:
            with open(self._file_name, 'r') as f:
                for line in f.readlines():
                    if line.endswith('\n'):
                        line = line[:-1]
                    self._msgs.append(line)
        except:
            pass

    def add(self, msg):
        self._msgs.append(msg)
        _log('Add new message %s' % msg)

    def __getitem__(self, index):
        return self._msg[index]

    def __len__(self):
        return len(self._msgs)

    def flush(self):
        try: 
            with open(self._file_name, 'w') as f:
                for msg in self._msgs:
                    f.write(msg + '\n')
        except:
            pass

class MessageManager(object):
    def __init__(self, dir_name):
        self._dir_name = dir_name
        self._msgs_by_filename = {}

    def __getitem__(self, file_name):
        if file_name not in self._msg_by_filename:
            self._msg_by_filename[file_name] = Message(os.path.join(self._dir_name, file_name))
        return self._msg_by_filename[file_name]

    def flush(self):
        for file_name in self._msgs_by_filename:
            self._msg_by_filename[file_name].flush()