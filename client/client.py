import Tkinter as tk   
import time

Login_FONT = ("Helvetica", 18, "bold")
userinput = ""
passwordinput = ""
ipinput = ""
portinput = ""
chatuserinput = ""
adduser = ""

class Window(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        self.title("Client UI")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (PageOne , LoginPage, PageTwo , PageThree , CreategroupPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("PageOne")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class PageOne(tk.Frame):

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

        self.connectbutton = tk.Button(self , text = "connect" , width = 7 , command= self.connectevent)
        self.connectbutton.grid(row = 3 , column = 22)

        self.garbage = tk.Label(self , text = "" , height = 10)
        self.garbage.grid(row = 4)  
        self.systemlog = tk.Label(self , text = "syslog : succeess")
        self.systemlog.grid(row = 5 ,  column = 2 , columnspan = 10)
    
    def connectevent(self):
        global ipinput , portinput
        ipinput = self.ipinput.get()
        portinput = self.portinput.get()
        self.ipinput.delete(0 , 'end')
        self.portinput.delete(0 , 'end')
        #self.systemlog["text"] = "aaaaaaaaaaaaaaaaa"
        self.controller.show_frame("LoginPage")

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

        self.chatuser = tk.Label(self , text = "Add User : " )
        self.chatuser.grid(row = 2 , column = 0 )
        self.chatuserinput = tk.Entry(self , width = 20)
        self.chatuserinput.grid(row = 2 , column = 1  )

        self.enterbutton = tk.Button(self , text = "add", height = 1  ,command= self.addevent)
        self.enterbutton.grid(row = 2 , column = 2 )

        self.systemlog = tk.Label(self , text = "syslog : succeess")
        self.systemlog.grid(row = 3 ,  column = 1)

        self.finishbutton = tk.Button(self , text = "finish" ,command=self.finish_creategroup)
        self.finishbutton.grid(row = 2, column = 3)

    def addevent(self):
        global adduser
        adduser += self.chatuserinput.get()
        self.chatuserinput.delete(0 , 'end')
        self.controller.show_frame("CreategroupPage")

    def finish_creategroup(self):
        global adduser
        #send
        adduser = ""
        self.controller.show_frame("PageTwo")



        

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

        self.loginbutton = tk.Button(self , text = "login" , width = 5 , command= self.loginevent)
        self.loginbutton.grid(row = 3 , column = 22)

        self.registerbutton = tk.Button(self , text = "regis" , width = 5 , command= self.register)
        self.registerbutton.grid(row = 2 , column = 22)

        self.garbage = tk.Label(self , text = "" , height = 10)
        self.garbage.grid(row = 4)  
        self.systemlog = tk.Label(self , text = "syslog : succeess")
        self.systemlog.grid(row = 5 ,  column = 2 , columnspan = 10)

    def register(self):
        global userinput , passwordinput
        userinput = self.userinput.get()
        passwordinput = self.passwordinput.get()
        self.userinput.delete(0 , 'end')
        self.passwordinput.delete(0 , 'end')
        #self.systemlog["text"] = "123123123123123"
        self.controller.show_frame("LoginPage")

    def loginevent(self):
        global userinput , passwordinput
        userinput = self.userinput.get()
        passwordinput = self.passwordinput.get()
        self.userinput.delete(0 , 'end')
        self.passwordinput.delete(0 , 'end')
        #self.systemlog["text"] = "aaaaaaaaaaaaaaaaa"
        self.controller.show_frame("PageTwo")

class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.welcome = tk.Label(self , text = "Welcome" , width = 15 ,  height = 2 , font = Login_FONT)
        self.welcome.grid(row = 1 , column = 0 , columnspan = 20)

        self.chatuser = tk.Label(self , text = "User or Group name : " , width = 20)
        self.chatuser.grid(row = 2 , column = 1 )
        self.chatuserinput = tk.Entry(self)
        self.chatuserinput.grid(row = 3 , column = 1  )

        onlinepeople = ""   #data from server
        self.onlinemsg = tk.Label(self , text = "user : \n" + onlinepeople , width = 10 , height = 20)
        self.onlinemsg.grid(row  = 3 , column = 0  , rowspan = 20)

        self.chatbutton = tk.Button(self , text = "Chat" ,command= self.tmp)
        self.chatbutton.grid(row = 3 , column = 2 )

        self.creategroupbutton = tk.Button(self , text = "Create Grp" ,command= self.creategoupevent)
        self.creategroupbutton.grid(row = 4 , column = 2)

        self.systemlog = tk.Label(self , text = "syslog : succeess")
        self.systemlog.grid(row = 21 ,  column = 1)

        self.backbutton = tk.Button(self , text = "logout" ,command=lambda: controller.show_frame("LoginPage"))
        self.backbutton.grid(row = 21 , column = 3)

    def creategoupevent(self):
        global chatuserinput
        chatuserinput = self.chatuserinput.get()
        self.controller.show_frame("CreategroupPage")

    def tmp(self):
        global chatuserinput
        chatuserinput = self.chatuserinput.get()
        self.controller.show_frame("PageThree")

class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.welcome = tk.Label(self , text = "" , height =1 , font = Login_FONT)
        self.welcome.grid(row = 0 , column = 1 , columnspan = 20)

        global chatuserinput
        self.chatuser = tk.Label(self)
        self.chatuser["text"] = "Talking with "  + chatuserinput + " ~"
        self.chatuser.grid(row = 1 , column = 1)

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

        self.upload = tk.Button(self , text = "Upld" , command = lambda : controller.show_frame("PageTwo"))
        self.upload.grid(row = 21 , column = 3)

        self.download = tk.Button(self , text = "Dwld" , command = lambda : controller.show_frame("PageTwo"))
        self.download.grid(row = 21 , column = 4)

        self.back = tk.Button(self , text = "back" , command = lambda : controller.show_frame("PageTwo"))
        self.back.grid(row = 0 , column = 4)

def update():
    global chatuserinput , app
    app.frames[PageThree.__name__].chatuser.config(text = "Talking with "  + chatuserinput + " ~")
    app.after(1000 , update) 

if __name__ == "__main__":
    global app
    app = Window()
    app.after(1000 , update)
    app.mainloop()
