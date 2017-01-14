import Tkinter as tk
import time
import client_api

Login_FONT = ("Helvetica", 18, "bold")
user = ""
password = ""
ip = ""
port = ""
chat_target = ""
users = []
groups = []
users_str = ""
groups_str = ""
group_name = ""
group_users = []
msgs = []
msgs_str = ""
connect = None
logined = False
is_chatting = False

class Window(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        self.title("Client UI")
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        self.frames = {}
        for F in (ConnectPage, LoginPage, WelcomePage, ChatroomPage, CreategroupPage):
            page_name = F.__name__
            frame = F(parent=container, controller = self)
            self.frames[page_name] = frame
            frame.grid(row = 0, column = 0, sticky = "nsew")
        self.show_frame("ConnectPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class ConnectPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.login = tk.Label(self, text = "Connect to Server", height = 2, width = 15 ,font = Login_FONT)
        self.login.grid(row = 0, column = 1, columnspan = 20)

        self.spacegrid = tk.Label(self, text = "", height = 3)
        self.spacegrid.grid(row = 1, column = 1)

        self.ip = tk.Label(self, text = "IP : ")
        self.ip.grid(row = 2, column = 0)
        self.ipInput = tk.Entry(self)
        self.ipInput.grid(row = 2, column = 1, columnspan = 20)
        self.port = tk.Label(self, text = "Port : ")
        self.port.grid(row = 3, column = 0)
        self.portInput = tk.Entry(self)
        self.portInput.grid(row = 3, column = 1 ,columnspan = 20)

        self.connectButton = tk.Button(self, text = "connect", width = 7, command = self.connect_event)
        self.connectButton.grid(row = 3, column = 22)

        self.spacegrid1 = tk.Label(self, text = "", height = 10)
        self.spacegrid1.grid(row = 4)
        self.systemlog = tk.Label(self, text = "syslog :")
        self.systemlog.grid(row = 5, column = 2, columnspan = 10)

    def connect_event(self):
        global connect
        global ip, port
        ip = self.ipInput.get()
        port = int(self.portInput.get())
        if connect:
            conn.close()
        connect = client_api.connect(ip, port)
        if connect:
            self.controller.show_frame("LoginPage")
        else:
            self.ipInput.delete(0, 'end')
            self.portInput.delete(0, 'end')
            self.systemlog["text"] = "Connect fail."

class CreategroupPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.spacegrid = tk.Label(self, text = "", height = 3)
        self.spacegrid.grid(row = 0, column = 0)

        self.title = tk.Label(self, text = "Create Group", height = 2, width = 15 ,font = Login_FONT)
        self.title.grid(row = 0, column = 1, columnspan = 20)

        self.spacegrid1 = tk.Label(self, text = "", height = 3)
        self.spacegrid1.grid(row = 1, column = 1)

        self.groupname = tk.Label(self, text = "Grp Name : ")
        self.groupname.grid(row=2, column = 0)
        self.groupnameInput = tk.Entry(self, width = 20)
        self.groupnameInput.grid(row = 2, column = 1)
        self.groupnameButton = tk.Button(self, text = "enter", command = self.groupname_event)
        self.groupnameButton.grid(row = 2, column = 2)

        self.addtarget = tk.Label(self, text = "Add User : ")
        self.addtarget.grid(row = 3, column = 0)
        self.addtargetInput = tk.Entry(self, width = 20)
        self.addtargetInput.grid(row = 3, column = 1)

        self.addButton = tk.Button(self, text = "add", height = 1, command = self.add_event)
        self.addButton.grid(row = 3, column = 2)

        self.systemlog = tk.Label(self, text = "syslog :")
        self.systemlog.grid(row = 4, column = 1, columnspan = 5, sticky = "w")

        self.finishButton = tk.Button(self, text = "finish" ,command = self.finish_creategroup_event)
        self.finishButton.grid(row = 3, column = 3)

    def groupname_event(self):
        global group_name
        if self.groupnameInput.get() == "":
            self.systemlog["text"] = "Groupname can't be empty."
        else:
            group_name = self.groupnameInput.get()
            self.systemlog["text"] = "Groupname = " + group_name

    def add_event(self):
        global group_users
        valid_target = False
        target = self.addtargetInput.get()
        for user, online in users:
            if target == user:
                valid_target = True
                break;
        if valid_target:
            group_users.append(target)
            self.systemlog["text"] = "add " + target + " to group success."
        else:
            self.systemlog["text"] = "user or group not exist."
        self.addtargetInput.delete(0, 'end')

    def finish_creategroup_event(self):
        succ = False
        if group_name == "":
            self.systemlog["text"] = "Groupname can't be empty."
        else:
            try:
                succ = client_api.create_group(connect, group_name, group_users)
                if succ:
                    self.systemlog["text"] = "syslog :"
                    self.controller.show_frame("WelcomePage")
                else:
                    self.systemlog["text"] = "Create group fail."
            except:
                self.systemlog["text"] = "Create group fail."

class LoginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.login = tk.Label(self, text = "Welcome", height = 2, width = 15 ,font = Login_FONT)
        self.login.grid(row = 0, column = 1, columnspan = 20)

        self.welcome = tk.Label(self, text = "", height = 3, font = Login_FONT)
        self.welcome.grid(row = 1, column = 1)

        self.user = tk.Label(self, text = "Username : ")
        self.user.grid(row = 2, column = 0)
        self.userInput = tk.Entry(self)
        self.userInput.grid(row = 2, column = 1, columnspan = 20)
        self.password = tk.Label(self, text = "Password : ")
        self.password.grid(row = 3, column = 0)
        self.passwordInput = tk.Entry(self, show = "*")
        self.passwordInput.grid(row = 3, column = 1 ,columnspan = 20)
        self.passconfirm = tk.Label(self, text = "Pass Confirm: ")
        self.passconfirm.grid(row = 4, column = 0)
        self.passconfirmInput = tk.Entry(self, show = "*")
        self.passconfirmInput.grid(row = 4, column = 1 ,columnspan = 20)

        self.loginButton = tk.Button(self, text = "login", width = 5, command = self.login_event)
        self.loginButton.grid(row = 3, column = 22)

        self.registerButton = tk.Button(self, text = "regis", width = 5, command = self.register_event)
        self.registerButton.grid(row = 2, column = 22)

        self.spacegrid = tk.Label(self, text = "", height = 10)
        self.spacegrid.grid(row = 5)
        self.systemlog = tk.Label(self, text = "syslog :")
        self.systemlog.grid(row = 6, column = 2, columnspan = 10, sticky='w')

    def register_event(self):
        succ = False
        global user, password
        user = self.userInput.get()
        password = self.passwordInput.get()
        passconfirm = self.passconfirmInput.get()
        if password != passconfirm:
            self.systemlog["text"] = "Password differs from confirm."
        else:
            try:
                succ = client_api.register(connect, user, password)
                if succ:
                    self.systemlog["text"] = "Register success."
                else:
                    self.systemlog["text"] = "Register fail."
            except:
                self.systemlog["text"] = "Register fail."
        self.userInput.delete(0, 'end')
        self.passwordInput.delete(0, 'end')
        self.passconfirmInput.delete(0, 'end')

    def login_event(self):
        succ = False
        global user, password
        global logined
        user = self.userInput.get()
        password = self.passwordInput.get()
        passconfirm = self.passconfirmInput.get()
        if password != passconfirm:
            self.systemlog["text"] = "Password differs from confirm."
        else:
            try:
                succ = client_api.login(connect, user, password)
                if succ:
                    logined = True
                    self.systemlog["text"] = "syslog :"
                    self.controller.show_frame("WelcomePage")
                else:
                    self.systemlog["text"] = "Login fail."
            except:
                self.systemlog["text"] = "Login fail."
        self.userInput.delete(0, 'end')
        self.passwordInput.delete(0, 'end')
        self.passconfirmInput.delete(0, 'end')

class WelcomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.welcome = tk.Label(self, text = "Welcome", width = 15, height = 2, font = Login_FONT)
        self.welcome.grid(row = 1, column = 0, columnspan = 20)

        self.chattarget = tk.Label(self, text = "User or Group name : ", width = 20)
        self.chattarget.grid(row = 2, column = 1)
        self.chattargetInput = tk.Entry(self)
        self.chattargetInput.grid(row = 3, column = 1)

        self.userlist = tk.Label(self, text = "users :", width = 10, height = 20)
        self.userlist.grid(row  = 3, column = 0, rowspan = 20)

        self.chatButton = tk.Button(self, text = "Chat", command = self.choosetarget_event)
        self.chatButton.grid(row = 3, column = 2)

        self.creategroupButton = tk.Button(self, text = "Create Grp", command = self.creategoup_event)
        self.creategroupButton.grid(row = 4, column = 2)

        self.systemlog = tk.Label(self, text = "syslog :")
        self.systemlog.grid(row = 21, column = 1, columnspan = 5, sticky='w')

        self.logoutButton = tk.Button(self, text = "logout", command = self.logout_event)
        self.logoutButton.grid(row = 21, column = 3)

    def creategoup_event(self):
        global group_users , group_name
        group_users = []
        group_name = ""
        self.chattargetInput.delete(0, 'end')
        self.systemlog["text"] = "syslog :"
        self.controller.show_frame("CreategroupPage")

    def choosetarget_event(self):
        valid_target = False
        target = self.chattargetInput.get()
        for user, online in users:
            if target == user:
                valid_target = True
                break;
        if valid_target:
            global chat_target, is_chatting
            chat_target = target
            is_chatting = True
            self.chattargetInput.delete(0, 'end')
            self.controller.show_frame("ChatroomPage")
            self.systemlog["text"] = "syslog :"
        else:
            self.chattargetInput.delete(0, 'end')
            self.systemlog["text"] = "user or group not exist."

    def logout_event(self):
        succ = False
        global logined
        try:
            succ = client_api.logout(connect)
            if succ:
                logined = False
                self.systemlog["text"] = "syslog :"
                self.controller.show_frame("LoginPage")
            else:
                self.systemlog["text"] = "Logout fail."
        except:
            self.systemlog["text"] = "Logout fail."


class ChatroomPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.welcome = tk.Label(self, text = "", height =1, font = Login_FONT)
        self.welcome.grid(row = 0, column = 1, columnspan = 20)

        self.chattarget = tk.Label(self)
        self.chattarget["text"] = "Talking with "  + chat_target + " ~"
        self.chattarget.grid(row = 1, column = 1)

        self.userlist = tk.Label(self, text = "users :", width = 10, height = 20)
        self.userlist.grid(row  = 2, column = 0)

        self.chatdata = tk.Label(self, text = "chatdata :", height = 20)
        self.chatdata.grid(row = 2, column = 1)

        self.downloadchatButton = tk.Button(self, text = "Dw Chat", command = self.dw_chat_event)
        self.downloadchatButton.grid(row = 21, column = 0)

        self.input = tk.Entry(self)
        self.input.grid(row = 21, column = 1)

        self.sendButton = tk.Button(self, text = "Send", height = 1, command = self.send_msg_event)
        self.sendButton.grid(row = 21, column = 2)

        self.uploadButton = tk.Button(self, text = "Upld", command = self.upload_event)
        self.uploadButton.grid(row = 21, column = 3)

        self.downloadButton = tk.Button(self, text = "Dwld", command = self.download_event)
        self.downloadButton.grid(row = 21, column = 4)

        self.systemlog = tk.Label(self, text = "syslog :")
        self.systemlog.grid(row = 22, column = 0, columnspan = 5, rowspan = 2, sticky='wn')

        self.backButton = tk.Button(self, text = "back", command = self.leave_chat_event)
        self.backButton.grid(row = 0, column = 4)

    def dw_chat_event(self):
        # TODO
        elf.systemlog["text"] = "Download chat history."

    def send_msg_event(self):
        succ = False
        msg = self.input.get()
        try:
            succ = client_api.send_msg(connect, chat_target, msg)
            if succ:
                self.systemlog["text"] = "Send message success."
            else:
                self.systemlog["text"] = "Send message fail."
        except:
            self.systemlog["text"] = "Send message fail."
        self.input.delete(0, 'end')

    def upload_event(self):
        succ = False
        filenames = self.input.get().split()
        try:
            files = [(f, open(f, "r").read()) for f in filenames]
            succ = client_api.send_files(connect, chat_target, files)
            if succ:
                self.systemlog["text"] = "Send files success."
            else:
                self.systemlog["text"] = "Send files fail."
        except:
            self.systemlog["text"] = "Send files fail."
        self.input.delete(0, 'end')

    def download_event(self):
        filename = self.input.get()
        try:
            content = client_api.recv_file(connect, chat_target, filename)
            if not content:
                self.systemlog["text"] = "Download file fail.\nPlease download by the processed name if needed."
            else:
                open(filename, 'w').write(content)
                self.systemlog["text"] = "Download file success."
        except:
            self.systemlog["text"] = "Download file fail.\nPlease download by the processed name if needed."
        self.input.delete(0, 'end')

    def leave_chat_event(self):
        self.systemlog["text"] = ""
        global chat_target, is_chatting
        chat_target = ""
        is_chatting = False
        self.controller.show_frame("WelcomePage")


def update_users():
    global users, groups
    global users_str, groups_str
    users_str = ""
    groups_str = ""
    if connect and logined:
        try:
            users = client_api.list_users(connect)
            groups = client_api.list_groups(connect)
        except:
            print "list users & groups fail."
        for user, online in users:
            if online:
                users_str += "\n+ " + user
            else:
                users_str += "\n- " + user
        groups_str = "\n  ".join(groups)

def update_msgs():
    global msgs, msgs_str
    msgs_str = ""
    msgs = []
    if connect and logined and is_chatting:
        try:
            msgs = client_api.recv_msgs(connect, chat_target)
        except:
            print "recv msgs fail."
        msgs_str = "\n".join(msgs[-15:])

def update():
    global app

    app.frames[ChatroomPage.__name__].chattarget.config(text = "Talking with "  + chat_target + " ~")

    update_users()
    app.frames[WelcomePage.__name__].userlist.config(text = "users: " + users_str + groups_str)
    app.frames[ChatroomPage.__name__].userlist.config(text = "users: " + users_str + groups_str)

    update_msgs()
    app.frames[ChatroomPage.__name__].chatdata.config(text = msgs_str)
    app.after(1000, update)

if __name__ == "__main__":
    global app
    app = Window()
    app.after(1000, update)
    app.mainloop()
