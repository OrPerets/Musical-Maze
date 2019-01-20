from tkinter import *
from main import main_menu
from files_functions import save_to_json, load_json, load_passwords, save_passwords
from flask import Flask
app = Flask(__name__)

Tf = ("Arial Rounded MT Bold", 20)
Bf = ("Arial Rounded MT Bold", 15)
Rf = ("Arial Rounded MT", 12)
Txf = ("Arial", 10)

users = load_json("users")
passwords = load_passwords()
current_user = None

def create_user(name, username, password, age, gender, knowledge):
    return {
        "name": name,
        "username": username,
        "password": password,
        "age": age,
        "gender": gender,
        "knowledge": knowledge
    }


def center_window(width=300, height=200):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))

@app.route('/')
def home():
    global roota

    roota = Tk()

    roota.title("Musical Maze")

    Tlabel = Label(roota, text='Login/Sign-up to start your journey!', font=Tf).grid(row=1, columnspan=2, sticky="nsew")

    flabel = Label(roota, text='Please choose the relevant option:', font=Txf).grid(row=2, columnspan=2,
                                                                                             sticky="nsew")


    img = PhotoImage(file="images/logo.png")
    panel = Label(roota, image=img).grid(row=0, columnspan=2, sticky="nsew")


    regh = Button(height=1, width=10, text="Register", relief='raised', font=Bf, fg='#1A4191',
                  command=lambda: registration())
    regh.grid(row=3, column=0, sticky="nsew")


    regl = Button(height=1, width=7, text='Login', font=Bf, fg='#1A4191', command=lambda: dlogin())
    regl.grid(row=3, column=1, sticky="nsew")
    roota.mainloop()


def registration():
    roota.destroy()
    global uname
    global pname
    global mname
    global gender
    global knowledge
    global ename
    global root

    root = Tk()
    root.title("Registration")
    center_window(360, 680)
    aimg = PhotoImage(file="images/logo.png")
    bpanel = Label(root, image=aimg).grid(row=0, columnspan=2, sticky="nsew")

    label = Label(root, text='New User Registration', font=Tf).grid(row=1, columnspan=2, sticky="nsew")

    nlabel = Label(root, text='Name', font=Txf).grid(row=2, column=0, sticky="nsew")

    ename = Entry(bd=5)
    ename.grid(row=2, column=1, sticky="nsew")
    ulabel = Label(root, text='Username', font=Txf).grid(row=3, column=0, sticky="nsew")

    uname = Entry(bd=5)
    uname.grid(row=3, column=1, sticky="nsew")

    mlabel = Label(root, text='Age', font=Txf).grid(row=4, column=0, sticky="nsew")

    mname = Entry(bd=5)
    mname.grid(row=4, column=1, sticky="nsew")
    plabel = Label(root, text='Password', font=Txf).grid(row=5, column=0, sticky="nsew")

    pname = Entry(bd=5, show="•")
    pname.grid(row=5, column=1, sticky="nsew")

    clabel = Label(root, text='Gender', font=Txf).grid(row=6, column=0, sticky="nsew")

    gender = IntVar()
    Radiobutton(root, text="Male", variable=gender, value=1).grid(row=6, column=1, sticky="nsew")
    Radiobutton(root, text="Female", variable=gender, value=2).grid(row=7, column=1, sticky="nsew")

    knowledge = IntVar()
    Checkbutton(root, text="Has knowledge in Music?", font=Rf, variable=knowledge).grid(row=8, column=0, sticky="nsew")
    reg = Button(height=1, width=10, text='Register', relief='raised', font=Bf, fg='#1A4191', command=addb)
    reg.grid(row=9, columnspan=2, sticky="nsew")
    root.mainloop()


def addb():
    global u
    global p
    global gender
    global knowledge
    global ename

    name = ename.get()
    username = uname.get()
    password = pname.get()
    age = mname.get()
    gender = gender.get()
    knowledge = knowledge.get()

    new_user = create_user(name=name,
                             username=username,
                             password=password,
                             age=age,
                             gender=gender,
                             knowledge=knowledge)
    users.append(new_user)

    passwords[username] = password
    save_to_json(new_user, "users")
    save_passwords(passwords)
    login()


def check():
    global c
    global d
    c = unameentry.get()
    d = passentry.get()

    if passwords[c] == d:
        rootb.destroy()
        success()

    else:
        rootb.destroy()
        failed()


def dcheck():
    global e
    global f
    global current_user
    e = dunameentry.get()
    f = dpassentry.get()

    if passwords[e] == f:
        rootd.destroy()
        main_menu(e)

    else:
        rootd.destroy()
        failed()


def login():
    root.destroy()
    global rootb
    global unameentry
    global passentry

    rootb = Tk()
    rootb.title("Login")

    cimg = PhotoImage(file="images/logo.png")
    cpanel = Label(rootb, image=cimg).grid(row=0, columnspan=2, sticky="nsew")

    loglabel = Label(rootb, text='User Login', font=Tf).grid(row=1, columnspan=2, sticky="nsew")

    unamelabel = Label(rootb, text='Username', font=Txf).grid(row=2, column=0, sticky="nsew")

    unameentry = Entry(bd=5)
    unameentry.grid(row=2, column=1, sticky="nsew")

    passlabel = Label(rootb, text='Password', font=Txf).grid(row=3, column=0, sticky="nsew")

    passentry = Entry(bd=5, show="•")
    passentry.grid(row=3, column=1, sticky="nsew")

    regb = Button(height=1, width=10, text='Login', relief='raised', font=Bf, fg='#1A4191', command=check)
    regb.grid(row=4, columnspan=2, sticky="nsew")
    rootb.mainloop()


def dlogin():
    roota.destroy()
    global rootd
    global dunameentry
    global dpassentry

    rootd = Tk()
    rootd.title("Login")

    dimg = PhotoImage(file="images/logo.png")
    dpanel = Label(rootd, image=dimg).grid(row=0, columnspan=2, sticky="nsew")

    dloglabel = Label(rootd, text='User Login', font=Tf).grid(row=1, columnspan=2, sticky="nsew")

    dunamelabel = Label(rootd, text='Username', font=Txf).grid(row=2, column=0, sticky="nsew")

    dunameentry = Entry(bd=5)
    dunameentry.grid(row=2, column=1, sticky="nsew")

    dpasslabel = Label(rootd, text='Password', font=Txf).grid(row=3, column=0, sticky="nsew")

    dpassentry = Entry(bd=5, show="•")
    dpassentry.grid(row=3, column=1, sticky="nsew")

    dregb = Button(height=1, width=10, text='Login', relief='raised', font=Bf, fg='#1A4191', command=dcheck)
    dregb.grid(row=4, columnspan=2, sticky="nsew")
    rootd.mainloop()


def success(current_user):
    global roottestc
    global unameentry
    rootc = Tk()
    rootc.title("Successful Login")
    suclabel = Label(rootc, text="Successful Login", font=Tf).grid(row=0, columnspan=2)
    labelsucc = Label(rootc, text="Enjoy!", font=Tf).grid(row=1, columnspan=2)
    regb = Button(height=1, width=10, text="Home", relief='raised', font=Bf, fg='#1A4191', command=lambda: main_menu(current_user)).grid(
        row=2, columnspan=2)


def failed():
    global rootc
    rootc = Tk()
    rootc.title("Unsuccessful Login")
    suclabel = Label(rootc, text="Failed Login", font=Tf).grid(row=0, columnspan=2)
    labelsucc = Label(rootc, text="UnHappy Holidays", font=Tf).grid(row=1, columnspan=2)
    regb = Button(height=1, width=10, text="Home", relief='raised', font=Bf, fg='#1A4191', command=lambda: back()).grid(
        row=2, columnspan=2)


def back():
    rootc.destroy()
    home()


home()

