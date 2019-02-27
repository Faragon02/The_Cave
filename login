import subprocess
from tkinter import *
from tkinter import messagebox
from glob import glob
import sqlite3

# Part of variable declare #
filist = glob("D:/PyProgram/Cvproject/New_account.py")
filist1 = glob("D:/PyProgram/Cvproject/R_sever")

# Part of function declare #
def login():
    strdata1, strdata2 = [], []
    log_con, log_cur = None, None
    id_data, pas_data = text_id.get(),text_pass.get()
    sql = ""
    sum1 = 0
    # account_cur.execute("CREATE TABLE usertable (ID char(15), PASSWORD char(20), Name char(10), Email char(30), Age int)")

    log_con = sqlite3.connect("D:\PyProgram\Cvproject\logDB")
    log_cur = log_con.cursor()
    log_cur.execute("select * from usertable")

    while (True):
        row = log_cur.fetchone()
        if row == None:        # 들어온 것이 없다.
            break              # 종료
        strdata1.append(row[0]);strdata2.append(row[1])
    print(strdata1)
    print(strdata2)
    if id_data in strdata1 and pas_data in strdata2:
        sum1 = 2
    elif id_data in strdata1 and pas_data not in strdata2:
            sum1 = 1
    elif id_data not in strdata1 and pas_data in strdata2:
            sum1 = 1
    elif id_data not in strdata1 and pas_data not in strdata2:
            sum1 = 0
    print(sum1)

    if sum1 ==1 or sum1 ==0:
        messagebox.showerror("Failed", "Faild login, ID,PASSWORD Check in please")
    if sum1 == 2:
        messagebox.showinfo("Succeed", "Successfully Login. Welcome")
        window.destroy()
        subprocess.call(["python.exe", filist1])
    log_con.close()

def new_account():
    subprocess.call(["python.exe",filist]) # 다른 파일을 실행시키기 위해 소환

# Part of the Main code #

if __name__ == '__main__':
    window = Tk()
    window.title("로그인")  # 제목
    window.geometry("500x600")  # 크기
    window.resizable(width=False, height=False)  # 사이즈 고정(Flase ==> True로 바꾸면 된다.)
    window.configure(background="White")  # 생성한 winform 배경색 지정 가능

    # 라벨링
    lable1 = Label(window, text="Lgoin", font=("바탕", 30), fg="blue", bg="white")
    lable2 = Label(window, text="ID :", font=("바탕", 15), fg="black"
                   , bg="white", width=30, height=5, anchor=W)
    lable3 = Label(window, text="Passward :", font=("바탕", 15), fg="black"
                   , bg="white", width=30, height=5, anchor=W)

    # Button
    log_btn = Button(window, text="Login", font=("바탕", 20), fg="black", bg="white", command=login)
    newlog_btn = Button(window, text="새계정", font=("바탕", 20), fg="black", bg="white", command=new_account)

    # textBox1
    text_id = Entry(window, width=30, textvariable=str)
    text_pass = Entry(window, width=30, textvariable=str)

    # 출력하는 팩 위치에 따라 결과가 달라짐
    lable1.pack()
    lable2.pack()
    text_id.pack()
    lable3.pack()
    text_pass.pack()

    newlog_btn.place(x=150, y=500, width=100, height=50)
    log_btn.place(x=350, y=500, width=100, height=50)
    window.mainloop()
