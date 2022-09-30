#TO_DO

import tkinter as tk
import json

# flow:
# Check for data/credentials file
# if user/pw exists, skip entering details, otherwise pop up enter user/pw
# store values in file
# then login() button
# start_bot button, time param
# number of follows/un per hour boxes
class Gui():
    # def start():
    #     pass
        # username_info = username.get()
        # password_info = password.get()

        # file=open(username_info+".txt", "w")
        # file.write(username_info+"\n")
        # file.write(password_info)
        # file.close()

        # tk.Label(screen1, text = "Registration Sucess", fg = "green" ,font = ("calibri", 11)).pack()



    def __init__(self):
        global root 
        
    def enter_user_pw(self):
        root = tk.Tk()
        root.geometry("300x250")
        root.title("VxT InstaBot v0.5.2")
        tk.Label(text = "VxT InstaBot v0.5.2", bg = "darkgrey", width = "300", height = "2", font = ("Calibri", 13)).pack()
        # tk.Button(text = "Start Bot", height = "2", width = "30", command = self.start).pack()
        tk.Label(text = "Username", bg = "darkgrey", width = "300", height = "2", font = ("Calibri", 13)).pack()
        username = tk.StringVar()
        userEntry = tk.Entry(root, textvariable=username)
        userEntry.pack()
        tk.Label(text = "Password", bg = "darkgrey", width = "300", height = "2", font = ("Calibri", 13)).pack()
        password = tk.StringVar()
        passEntry = tk.Entry(root, textvariable=password, show='*')
        passEntry.pack() 
        # submit = tk.Button(root, text='Show Console', command=show)
        # submit.pack()      

        root.mainloop()

    def start():
        pass

    