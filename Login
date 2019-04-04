import subprocess
from tkinter import *
from tkinter import messagebox
from glob import glob
import sqlite3

filist = glob("D:/Potal/New_account.py")
filist1 = glob("D:/Potal/main_sever.py")

def login():
    strdata1, strdata2 = [], []
    log_con, log_cur = None, None
    id_data, pas_data = text_id.get(),text_pass.get()
    result,sql =0,""

    log_con = sqlite3.connect("D:/Potal/semp/userDB")
    log_cur = log_con.cursor()
    log_cur.execute("select * from usertable")


    while(True):
        row = log_cur.fetchone()
        if row == None:
            break
        strdata1.append(row[0]);strdata2.append(row[1])

    for i in range(len(strdata1)):
        if strdata1[i] == id_data:
            if strdata2[i] == pas_data:
                result = 2
                break

    if result ==0:
        messagebox.showerror("Failed", "Faild login, ID,PASSWORD Check in please")
    else:
        messagebox.showinfo("Succeed", "Successfully Login. Welcome")
        logdow.destroy()
        subprocess.call(["python.exe", filist1])
    log_con.close()

def new_account():
    subprocess.call(["python.exe",filist])

if __name__ == '__main__':
    logdow = Tk()
    logdow.title("Login")
    logdow.geometry("500x600")  # 크기
    logdow.resizable(width=False, height=False)
    logdow.configure(background="White")

    # lable
    lable1 = Label(logdow, text="Lgoin", font=("바탕", 30), fg="blue", bg="white")
    lable2 = Label(logdow, text="ID :", font=("바탕", 15), fg="black"
                   , bg="white", width=30, height=5, anchor=W)
    lable3 = Label(logdow, text="Passward :", font=("바탕", 15), fg="black"
                   , bg="white", width=30, height=5, anchor=W)

    # Button
    log_btn = Button(logdow, text="Login", font=("바탕", 20), fg="black", bg="white", command=login)
    newlog_btn = Button(logdow, text="새계정", font=("바탕", 20), fg="black", bg="white", command=new_account)

    # textBox1
    text_id = Entry(logdow, width=30, textvariable=str)
    text_pass = Entry(logdow, width=30, textvariable=str)

    lable1.pack()
    lable2.pack()
    text_id.pack()
    lable3.pack()
    text_pass.pack()

    newlog_btn.place(x=150, y=500, width=100, height=50)
    log_btn.place(x=350, y=500, width=100, height=50)
    logdow.mainloop()
