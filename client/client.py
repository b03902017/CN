import Tkinter as tk

Login_FONT = ("Helvetica" , 18 , "bold")

class Window(tk.Frame):
	def __init__(self , master = None ):
		tk.Frame.__init__(self , master )
		self.grid()
		self.init_window()
	def init_window(self):		
		self.master.title("Client UI")
		self.login = tk.Label(self , text = "Login"  , height = 2 , font = Login_FONT)
		self.login.grid(row = 0 , column = 1)
		self.user = tk.Label(self , text = "User : ")
		self.user.grid(row = 1 , column = 0 )
		self.userinput = tk.Entry(self)
		self.userinput.grid(row = 1 , column = 1  )
		self.password = tk.Label(self , text = "Pass : ")
		self.password.grid(row = 2, column = 0 )
		self.passwordinput = tk.Entry(self)
		self.passwordinput.grid(row = 2 , column = 1 )
		self.enterbutton = tk.Button(self , text = "enter" , width = 5 , command = self.enterevent)
		self.enterbutton.grid(row = 2 , column = 2 )
		self.msg = tk.Label(self  , text = "")
		self.msg.grid(row = 3 , column = 1)
	def enterevent(self):
		if self.passwordinput.get() == "123" : 
			self.msg["text"] = "<login success>"
		else :
			self.msg["text"] = "<login fail>"

root = tk.Tk()
app = Window(master = root)
root.mainloop()