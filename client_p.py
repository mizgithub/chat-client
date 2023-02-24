
#!/usr/bin/env python3
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
from tkinter import *
from tkinter.ttk import Scale
from tkinter import colorchooser,filedialog,messagebox
import PIL.ImageGrab as ImageGrab


# def receive():
#     """Handles receiving of messages."""
#     while True:
#         try:
#             pass
#             msg = client_socket.recv(BUFSIZ).decode("utf8")
#             p.socket_paint(msg)           
#         except OSError:  
#             break


# def send(msg,event=None):  # event is passed by binders.
# #     msg = my_msg.get()
# #     my_msg.set("")  # Clears input field.
#     client_socket.send(bytes(msg, "utf8"))
#     if msg == "{quit}":
#         client_socket.close()
#         root.quit()


# def on_closing(event=None):
#     """This function is to be called when the window is closed."""
# #     my_msg.set("{quit}")
#     send()

from tkinter import *
from tkinter.ttk import Scale
from tkinter import colorchooser,filedialog,messagebox
import PIL.ImageGrab as ImageGrab


#Defining Class and constructor of the Program
class Draw():
    def __init__(self,root):

#Defining title and Size of the Tkinter Window GUI
        self.root =root
        self.root.title("Mobile Board v1.0")
#         self.root.geometry("810x530")
        self.root.configure(background="white")
#         self.root.resizable(0,0)
        self.ip = tkinter.StringVar()  # For the messages to be sent.
        self.ip.set("")
#variables for pointer and Eraser   
        self.pointer= "black"
        self.erase="white"

#Widgets for Tkinter Window
    
# Configure the alignment , font size and color of the text
        # text=Text(root)
        # text.tag_configure("tag_name", justify='center', font=('arial',25),background='#292826',foreground='orange')

# Insert a Text
        # title_txt = text.insert("1.0", "Mobile board v1.0")
        # title_txt.place(x=5,y=5,width=200,height=20)
        self.host = Entry(root,textvariable=self.ip)
        self.host.place(x=300,y=0,width=200,height=20)
        self.connect_btn= Button(self.root,text="Connect",bd=4,bg='white',command=self.connect,width=15,relief=RIDGE)
        self.connect_btn.place(x=500,y=0)

# Add the tag for following given text
        # text.tag_add("tag_name", "1.0", "end")
        # text.pack()
        
# Pick a color for drawing from color pannel
        self.pick_color = LabelFrame(self.root,text='Colors',font =('arial',15),bd=5,relief=RIDGE,bg="white")
        self.pick_color.place(x=0,y=40,width=90,height=185)

        colors = ['blue','red','green', 'orange','violet','black','yellow','purple','pink','gold','brown','indigo']
        i=j=0
        for color in colors:
            Button(self.pick_color,bg=color,bd=2,relief=RIDGE,width=3,command=lambda col=color:self.select_color(col)).grid(row=i,column=j)
            i+=1
            if i==6:
                i=0
                j=1

 # Erase Button and its properties   
        self.eraser_btn= Button(self.root,text="Eraser",bd=4,bg='white',command=self.eraser,width=9,relief=RIDGE)
        self.eraser_btn.place(x=0,y=197)

# Reset Button to clear the entire screen 
        self.clear_screen= Button(self.root,text="Clear Screen",bd=4,bg='white',command= lambda : self.background.delete('all'),width=9,relief=RIDGE)
        self.clear_screen.place(x=0,y=227)

# Save Button for saving the image in local computer
        self.save_btn= Button(self.root,text="ScreenShot",bd=4,bg='white',command=self.save_drawing,width=9,relief=RIDGE)
        self.save_btn.place(x=0,y=257)

# Background Button for choosing color of the Canvas
        self.bg_btn= Button(self.root,text="Background",bd=4,bg='white',command=self.canvas_color,width=9,relief=RIDGE)
        self.bg_btn.place(x=0,y=287)


#Creating a Scale for pointer and eraser size
        self.pointer_frame= LabelFrame(self.root,text='size',bd=5,bg='white',font=('arial',15,'bold'),relief=RIDGE)
        self.pointer_frame.place(x=0,y=320,height=200,width=70)

        self.pointer_size =Scale(self.pointer_frame,orient=VERTICAL,from_ =48 , to =0, length=168)
        self.pointer_size.set(1)
        self.pointer_size.grid(row=0,column=1,padx=15)


#Defining a background color for the Canvas 
        self.background = Canvas(self.root,bg='white',bd=5,relief=GROOVE,height=600,width=1000)
        self.background.place(x=80,y=40)


#Bind the background Canvas with mouse click
        self.background.bind("<B1-Motion>",self.paint) 


# Functions are defined here

# Paint Function for Drawing the lines on Canvas
    def receive(self):
        """Handles receiving of messages."""
        while True:
            try:
                pass
                msg = self.client_socket.recv(self.BUFSIZ).decode("utf8")
                self.socket_paint(msg)           
            except OSError:  
                break
    def send(self,msg,event=None):  # event is passed by binders.
    #     msg = my_msg.get()
    #     my_msg.set("")  # Clears input field.
        self.client_socket.send(bytes(msg, "utf8"))
        if msg == "{quit}":
            self.client_socket.close()
            root.quit()
    def on_closing(self,event=None):
        """This function is to be called when the window is closed."""
#     my_msg.set("{quit}")
        self.send()
    def connect(self):
        HOST = self.ip.get()# Enter host of the server without inverted commas 
        PORT = 33000
        self.BUFSIZ = 1024
        ADDR = (HOST, PORT)

        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(ADDR)

        receive_thread = Thread(target=self.receive)
        receive_thread.start()
        
    def paint(self,event):       
        x1,y1 = (event.x-2), (event.y-2)  
        x2,y2 = (event.x+2), (event.y+2)  

        self.background.create_oval(x1,y1,x2,y2,fill=self.pointer,outline=self.pointer,width=self.pointer_size.get())
        data = str(x1)+","+str(y1)+","+str(x2)+","+str(y2)
        self.send(data)
    def socket_paint(self,data):
        x1,y1,x2,y2 = data.split(",")
        self.background.create_oval(float(x1),float(y1),float(x2),float(y2),fill=self.pointer,outline=self.pointer,width=self.pointer_size.get())


# Function for choosing the color of pointer  
    def select_color(self,col):
        self.pointer = col

# Function for defining the eraser
    def eraser(self):
        self.pointer= self.erase

# Function for choosing the background color of the Canvas    
    def canvas_color(self):
        color=colorchooser.askcolor()
        self.background.configure(background=color[1])
        self.erase= color[1]

# Function for saving the image file in Local Computer
    def save_drawing(self):
        try:
            # self.background update()
            file_ss =filedialog.asksaveasfilename(defaultextension='jpg')
            #print(file_ss)
            x=self.root.winfo_rootx() + self.background.winfo_x()
            #print(x, self.background.winfo_x())
            y=self.root.winfo_rooty() + self.background.winfo_y()
            #print(y)

            x1= x + self.background.winfo_width() 
            #print(x1)
            y1= y + self.background.winfo_height()
            #print(y1)
            ImageGrab.grab().crop((x , y, x1, y1)).save(file_ss)
            messagebox.showinfo('Screenshot Successfully Saved as' + str(file_ss))

        except:
            print("Error in saving the screenshot")


root = Tk()
p= Draw(root)

# top = tkinter.Tk()
# top.title("Chat On!")

# messages_frame = tkinter.Frame(top)
# my_msg = root.StringVar()  # For the messages to be sent.
# my_msg.set("")
# scrollbar = tkinter.Scrollbar(messages_frame)  # To see through previous messages.
# # this will contain the messages.
# msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
# scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
# msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
# msg_list.pack()
# messages_frame.pack()

# entry_field = tkinter.Entry(top, textvariable=my_msg)
# entry_field.bind("<Return>", send)
# entry_field.pack()
# send_button = tkinter.Button(top, text="Send", command=send)
# send_button.pack()

# top.protocol("WM_DELETE_WINDOW", on_closing)

#Socket part
# HOST = input('Enter host: ') # Enter host of the server without inverted commas 
# PORT = 33000
# BUFSIZ = 1024
# ADDR = (HOST, PORT)

# client_socket = socket(AF_INET, SOCK_STREAM)
# client_socket.connect(ADDR)

# receive_thread = Thread(target=receive)
# receive_thread.start()


root.mainloop()
