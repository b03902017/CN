import Tkinter as tk
import time
import client_api

Login_FONT = ("Helvetica", 18, "bold")
user = ""
password = ""
ip = ""
port = ""
chat_target = ""
adduser = ""

users = []
groups = []
connect = None

class Window(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        self.title("Client UI")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (ConnectPage , LoginPage, WelcomePage , ChatroomPage , CreategroupPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("ConnectPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class ConnectPage(tk.Frame):

    def __init__(self , parent , controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.login = tk.Label(self , text = "Connect to Server"  , height = 2, width = 15 ,font = Login_FONT)
        self.login.grid(row = 0 , column = 1 , columnspan = 20)

        self.welcome = tk.Label(self , text = "" , height = 3, font = Login_FONT)
        self.welcome.grid(row = 1 , column = 1)

        self.ip = tk.Label(self , text = "IP : ")
        self.ip.grid(row = 2 , column = 0 )
        self.ipinput = tk.Entry(self)
        self.ipinput.grid(row = 2 , column = 1  , columnspan = 20)
        self.port = tk.Label(self , text = "Port : ")
        self.port.grid(row = 3, column = 0 )
        self.portinput = tk.Entry(self)
        self.portinput.grid(row = 3 , column = 1 ,columnspan = 20)

        self.connectbutton = tk.Button(self , text = "connect" , width = 7 , command = self.connect_event)
        self.connectbutton.grid(row = 3 , column = 22)

        self.garbage = tk.Label(self , text = "" , height = 10)
        self.garbage.grid(row = 4)
        self.systemlog = tk.Label(self , text = "syslog :")
        self.systemlog.grid(row = 5 ,  column = 2 , columnspan = 10)

    def connect_event(self):
        global connect
        global ip , port
        ip = self.ipinput.get()
        port = int(self.portinput.get())
        if connect:
            conn.close()
        connect = client_api.connect(ip, port)
        if connect:
            self.controller.show_frame("LoginPage")
        else:
            self.ipinput.delete(0 , 'end')
            self.portinput.delete(0 , 'end')
            self.systemlog["text"] = "Connect fail."

class CreategroupPage(tk.Frame):

    def __init__(self , parent , controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.gar2 = tk.Label(self , text = "" , height = 3, font = Login_FONT)
        self.gar2.grid(row = 0 , column = 0)

        self.title = tk.Label(self , text = "Create Group"  , height = 2, width = 15 ,font = Login_FONT)
        self.title.grid(row = 0 , column = 1 , columnspan = 20)

        self.gar = tk.Label(self , text = "" , height = 3, font = Login_FONT)
        self.gar.grid(row = 1 , column = 1)

        self.chattarget = tk.Label(self , text = "Add User : " )
        self.chattarget.grid(row = 2 , column = 0 )
        self.chattargetinput = tk.Entry(self , width = 20)
        self.chattargetinput.grid(row = 2 , column = 1  )

        self.enterbutton = tk.Button(self , text = "add", height = 1  ,command = self.add_event)
        self.enterbutton.grid(row = 2 , column = 2 )

        self.systemlog = tk.Label(self , text = "syslog : succeess")
        self.systemlog.grid(row = 3 ,  column = 1)

        self.finishbutton = tk.Button(self , text = "finish" ,command =self.finish_creategroup)
        self.finishbutton.grid(row = 2, column = 3)

    def add_event(self):
        global adduser
        adduser += self.chattargetinput.get()
        self.chattargetinput.delete(0 , 'end')
        self.controller.show_frame("CreategroupPage")

    def finish_creategroup(self):
        global adduser
        #send
        adduser = ""
        self.controller.show_frame("WelcomePage")

class LoginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.login = tk.Label(self , text = "Welcome"  , height = 2, width = 15 ,font = Login_FONT)
        self.login.grid(row = 0 , column = 1 , columnspan = 20)

        self.welcome = tk.Label(self , text = "" , height = 3, font = Login_FONT)
        self.welcome.grid(row = 1 , column = 1)

        self.user = tk.Label(self , text = "User : ")
        self.user.grid(row = 2 , column = 0 )
        self.userinput = tk.Entry(self)
        self.userinput.grid(row = 2 , column = 1  , columnspan = 20)
        self.password = tk.Label(self , text = "Pass : ")
        self.password.grid(row = 3, column = 0 )
        self.passwordinput = tk.Entry(self)
        self.passwordinput.grid(row = 3 , column = 1 ,columnspan = 20)

        self.loginbutton = tk.Button(self , text = "login" , width = 5 , command = self.login_event)
        self.loginbutton.grid(row = 3 , column = 22)

        self.registerbutton = tk.Button(self , text = "regis" , width = 5 , command = self.register_event)
        self.registerbutton.grid(row = 2 , column = 22)

        self.garbage = tk.Label(self , text = "" , height = 10) # for UI beauty
        self.garbage.grid(row = 4)
        self.systemlog = tk.Label(self , text = "syslog :")
        self.systemlog.grid(row = 5 ,  column = 2 , columnspan = 10)

    def register_event(self):
        succ = False
        global user , password
        user = self.userinput.get()
        password = self.passwordinput.get()
        try:
            succ = client_api.register(connect, user, password)
            if not succ:
                self.systemlog["text"] = "Register fail."
        except:
            self.systemlog["text"] = "Register fail."
        self.userinput.delete(0 , 'end')
        self.passwordinput.delete(0 , 'end')
        if succ:
            self.systemlog["text"] = "Register success."

    def login_event(self):
        succ = False
        global user , password
        user = self.userinput.get()
        password = self.passwordinput.get()
        try:
            succ = client_api.login(connect, user, password)
            if not succ:
                self.systemlog["text"] = "Login fail."
        except:
            self.systemlog["text"] = "Login fail."
        self.userinput.delete(0 , 'end')
        self.passwordinput.delete(0 , 'end')
        if succ:
            self.systemlog["text"] = "syslog :"
            self.controller.show_frame("WelcomePage")

class WelcomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.welcome = tk.Label(self , text = "Welcome" , width = 15 ,  height = 2 , font = Login_FONT)
        self.welcome.grid(row = 1 , column = 0 , columnspan = 20)

        self.chattarget = tk.Label(self , text = "User or Group name : " , width = 20)
        self.chattarget.grid(row = 2 , column = 1 )
        self.chattargetinput = tk.Entry(self)
        self.chattargetinput.grid(row = 3 , column = 1  )

        self.onlineusers = tk.Label(self , text = "users : ", width = 10 , height = 20)
        self.onlineusers.grid(row  = 3 , column = 0  , rowspan = 20)

        self.update_users_button = tk.Button(self, text = "users", command = self.update_users_event)
        self.update_users_button.grid(row = 2, column = 0, )

        self.chatbutton = tk.Button(self , text = "Chat" , command = self.choosetarget_event)
        self.chatbutton.grid(row = 3 , column = 2 )

        self.creategroupbutton = tk.Button(self , text = "Create Grp" , command = self.creategoup_event)
        self.creategroupbutton.grid(row = 4 , column = 2)

        self.systemlog = tk.Label(self , text = "syslog :")
        self.systemlog.grid(row = 21 ,  column = 1)

        self.logoutbutton = tk.Button(self , text = "logout" , command = self.logout_event)
        self.logoutbutton.grid(row = 21 , column = 3)

    def update_users_event(self):
        global users , groups
        try:
            users = client_api.list_users(connect)
            print users
        except:
            print "list users fail."
        try:
            groups = client_api.list_groups(connect)
        except:
            print "list users fail."
        users_str = ""
        for user , online in users:
            if online:
                users_str += "\n+ " + user
            else:
                users_str += "\n- " + user
        self.onlineusers["text"] = "users :" + users_str

    def creategoup_event(self):
        # TODO
        self.chattargetinput.delete(0 , 'end')
        self.systemlog["text"] = "syslog :"
        self.controller.show_frame("CreategroupPage")

    def choosetarget_event(self):
        global chat_target
        chat_target = self.chattargetinput.get()
        self.chattargetinput.delete(0 , 'end')
        self.controller.show_frame("ChatroomPage")

    def logout_event(self):
        succ = False
        try:
            succ = client_api.logout(connect)
            if not succ:
                self.systemlog["text"] = "Logout fail."
        except:
            self.systemlog["text"] = "Logout fail."
        if succ:
            self.systemlog["text"] = "syslog :"
            self.controller.show_frame("LoginPage")

class ChatroomPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.welcome = tk.Label(self , text = "" , height =1 , font = Login_FONT)
        self.welcome.grid(row = 0 , column = 1 , columnspan = 20)

        global chat_target
        self.chattarget = tk.Label(self)
        self.chattarget["text"] = "Talking with "  + chat_target + " ~"
        self.chattarget.grid(row = 1 , column = 1)

        onlinepeople = "user : \n"   #data from server
        self.onlinemsg = tk.Label(self , text = onlinepeople , width = 10 , height = 20)
        self.onlinemsg.grid(row  = 2 , column = 0 )

        chatdata = ""
        self.chatdata = tk.Label(self , text = chatdata , height = 20)
        self.chatdata.grid(row = 2 , column = 1)

        self.send = tk.Button(self , text = "Send" , height = 1)
        self.send.grid(row = 21 , column = 2 )
        self.sendinput = tk.Entry(self)
        self.sendinput.grid(row = 21 , column = 1  )

        self.systemlog = tk.Label(self , text = "syslog : succeess")
        self.systemlog.grid(row = 22 ,  column = 1)

        self.upload = tk.Button(self , text = "Upld" , command = lambda : controller.show_frame("WelcomePage"))
        self.upload.grid(row = 21 , column = 3)

        self.download = tk.Button(self , text = "Dwld" , command = lambda : controller.show_frame("WelcomePage"))
        self.download.grid(row = 21 , column = 4)

        self.back = tk.Button(self , text = "back" , command = lambda : controller.show_frame("WelcomePage"))
        self.back.grid(row = 0 , column = 4)

def update():
    global chat_target , app
    app.frames[ChatroomPage.__name__].chattarget.config(text = "Talking with "  + chat_target + " ~")
    app.after(1000 , update)

if __name__ == "__main__":
    global app
    app = Window()
    app.after(1000 , update)
    app.mainloop()
