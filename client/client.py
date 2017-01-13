import Tkinter as tk   
import time

Login_FONT = ("Helvetica", 18, "bold")
userinput = None
passwordinput = None
chatuserinput = ""

class Window(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        self.title("Client UI")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (LoginPage, PageTwo , PageThree):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class LoginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.login = tk.Label(self , text = "Login"  , height = 2, width = 15 ,font = Login_FONT)
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
        self.enterbutton = tk.Button(self , text = "enter" , width = 5 , command= self.tmp)
        self.enterbutton.grid(row = 3 , column = 22)

        self.garbage = tk.Label(self , text = "" , height = 10)
        self.garbage.grid(row = 4)  
        self.systemlog = tk.Label(self , text = "syslog : succeess")
        self.systemlog.grid(row = 5 ,  column = 2 , columnspan = 10)

    def tmp(self):
        global userinput , passwordinput
        userinput = self.userinput.get()
        passwordinput = self.passwordinput.get()
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

        onlinepeople = "user1\nuser2\nuser3\nuser1\nuser2\nuser3\nuser1\nuser2\nuser3\n"   #data from server
        self.onlinemsg = tk.Label(self , text = "user : \n" + onlinepeople , width = 10 , height = 20)
        self.onlinemsg.grid(row  = 3 , column = 0  , rowspan = 20)

        self.enterbutton = tk.Button(self , text = "enter", height = 1  ,command= self.tmp)
        self.enterbutton.grid(row = 3 , column = 2 )

        self.systemlog = tk.Label(self , text = "syslog : succeess")
        self.systemlog.grid(row = 21 ,  column = 1)

        self.backbutton = tk.Button(self , text = "back" ,command=lambda: controller.show_frame("LoginPage"))
        self.backbutton.grid(row = 21 , column = 3)

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

        onlinepeople = "user1\nuser2\n"   #data from server
        self.onlinemsg = tk.Label(self , text = onlinepeople , width = 10 , height = 20)
        self.onlinemsg.grid(row  = 2 , column = 0 )

        chatdata = "ngin shan hao sui\ngi shan hao ban\nlalalalalalall\nbababababa\ngin shan hao sui\ngi shan hao ban\nlalalalalalall\nbababababa\n"
        self.chatdata = tk.Label(self , text = chatdata , height = 20)
        self.chatdata.grid(row = 2 , column = 1) 

        self.send = tk.Button(self , text = "Send" , height = 1)
        self.send.grid(row = 21 , column = 2 )
        self.sendinput = tk.Entry(self)
        self.sendinput.grid(row = 21 , column = 1  )

        self.systemlog = tk.Label(self , text = "syslog : succeess")
        self.systemlog.grid(row = 22 ,  column = 1)

        self.upload = tk.Button(self , text = "upld" , command = lambda : controller.show_frame("PageTwo"))
        self.upload.grid(row = 21 , column = 3)

        self.download = tk.Button(self , text = "dnld" , command = lambda : controller.show_frame("PageTwo"))
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
