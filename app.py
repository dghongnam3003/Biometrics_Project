import tkinter as tk
import os, cv2
from PIL import Image, ImageTk
from tkinter import Frame, Entry, Button, Label, messagebox, filedialog
from tktooltip import ToolTip
import face_detector, face_train, face_recognizer

MAIN_FONT = "Microsoft YaHei UI Light"
MAIN_COLOR = "#57a1f8"
COLOR_DARK = "#0769e0"
COLOR_LIGHT = "#a8cbff"
DARD_RED = "#bd0000"
WWIDTH = 900
WHEIGHT = 500

LIMIT_CAPTURE = 32

# Create a new Tkinter window
wnd = tk.Tk()
wnd.title("Face Recognition")
wnd.geometry(str(WWIDTH)+"x"+str(WHEIGHT))
wnd.configure(bg="white")
wnd.resizable(False, False)

iLogin = tk.PhotoImage(file="res/login.png")
icContinue = tk.PhotoImage(file="res/continue.gif")
icBack = tk.PhotoImage(file="res/back.gif")
icCancel = tk.PhotoImage(file="res/cancel.gif")
icAdd = tk.PhotoImage(file="res/add.gif")
icCamera = tk.PhotoImage(file="res/camera.png")

cur_user = tk.StringVar()
cur_pswd = tk.StringVar()
is_new = False
hello = tk.StringVar()

def auth(frame: Frame, username: str, password:str =None):
    username = username.lower()
    global is_new
    def animation_fMy():
        fMy.place(x=0,y=500)
        fMy.tkraise()
        for i in range(500, 0, -1):
            fMy.place(x=0,y=i)
            wnd.update()

    if cur_user.get() != "" and cur_pswd.get() == "FACE_ID":
        # Auth by face
        print("Recognized user: ", cur_user.get(), '\nInput username: ', username)
        if username == cur_user.get():
            hello.set(f"Hello again, {username}!")
            is_new = False
            fMy.after(1000, animation_fMy)
            Label(frame, text="Login successful!    ", font=(MAIN_FONT, 10), bg="white", fg="green", bd=0).place(x=35, y=175)
            return True
    elif isUser(username):
        # Auth by password
        with open(f"data/{username}/password.txt", "r") as f:
            if f.read() == password:
                cur_user.set(username)
                hello.set(f"Hello again, {username}!")
                is_new = False
                fMy.after(1000, animation_fMy)
                Label(frame, text="Login successful!    ", font=(MAIN_FONT, 10), bg="white", fg="green", bd=0).place(x=35, y=175)
                return True
    
    Label(frame, text="Invalid credentials! ", font=(MAIN_FONT, 10), bg="white", fg=DARD_RED, bd=0).place(x=35, y=175)
    return False

def isUser(username: str):
    username = username.lower()
    if os.path.exists("data/"+username) and os.path.isdir("data/"+username):
        return True
    else:
        return False

def isValidName(username: str):
    for c in username:
        if c in '# %&\{\}\<>*?/$!\'":@+`|=^~[]()':
            return False
    return True



def HomePg():
    frame = Frame(wnd, width=WWIDTH, height=WHEIGHT, bg='white')
    frame.place(x=0,y=0)
    
    fLogin = Frame(frame, width=350, height=400, bg="white")
    fLogin.place(x=490, y=50)

    Label(frame, image=iLogin, bg="white").place(x=50, y=85)

    heading = Label(fLogin, text="Welcome!", font=(MAIN_FONT, 23, "bold"), bg="white", fg=COLOR_DARK, justify="center")
    heading.place(x=109, y=10)

    ############################################

    # Username Box
    user = Entry(fLogin, width=25, font=(MAIN_FONT, 11), bg="white", fg="black", bd=0)
    user.place(x=35, y=80)
    user.insert(0, "Username")
    user.bind("<FocusIn>", lambda _: user.delete('0', 'end') if user.get() == "Username" else None)
    user.bind("<FocusOut>", lambda _: user.insert('0', "Username") if user.get() == "" else None)
    Frame(fLogin, width=295, height=1, bg="gray").place(x=35, y=107)

    # Password Box
    pswd = Entry(fLogin, width=25, font=(MAIN_FONT, 11), bg="white", fg="black", bd=0)
    pswd.place(x=35, y=140)
    pswd.insert(0, "Password")
    pswd.bind("<FocusIn>", lambda _: pswd.delete('0', 'end') if pswd.get() == "Password" else None)
    pswd.bind("<FocusOut>", lambda _: pswd.insert('0', "Password") if pswd.get() == "" else None)
    pswd_bar = Frame(fLogin, width=295, height=1, bg="gray")
    pswd_bar.place(x=35, y=167)

    ############################################

    signin_btn = Button(fLogin, text="Sign In", font=(MAIN_FONT, 13, "bold"), bg=MAIN_COLOR, fg="white", command=lambda: auth(fLogin, username=user.get(), password=pswd.get()), width=26, relief="flat")
    signin_btn.place(x=35, y=220)
    Label(fLogin, text="Don't have an account?", font=(MAIN_FONT, 10), bg="white", fg="black", bd=0).place(x=35, y=315)
    status = tk.StringVar()

    def face_id():
        Label(fLogin, text="                             ", font=(MAIN_FONT, 10), bg="white", fg=DARD_RED, bd=0).place(x=35, y=175)
        signin_btn.config(state='disabled')
        signup_btn.config(state='disabled')
        faceid_btn.config(state='disabled')
        pswd.delete('0', 'end')
        pswd.config(state='disabled', fg='white')
        pswd_bar.config(width=1)
        user.config(state='readonly')

        fwhite = Frame(fLogin, width=295, height=50, bg="white")
        fwhite.place(x=35, y=135)
        fStatus = Label(fLogin, textvariable=status, font=(MAIN_FONT, 11, 'bold'), bg="white", fg='black', bd=0)
        fStatus.place(x=35, y=140)
        fCamera = Label(wnd, width=400, bg='black', height=400)
        fCamera.place(x=50, y=50)
        

        status.set('Connecting...')
        cam = cv2.VideoCapture(0)
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, 600) 
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)
        cur_code = None
        count = 0
        total_count = 0

        def reset_home():
            cam.release()
            signin_btn.config(state='normal')
            signup_btn.config(state='normal')
            faceid_btn.config(state='normal')
            pswd.config(state='normal', fg='black')
            pswd_bar.config(width=295)
            fStatus.destroy()
            fwhite.destroy()
            fCamera.destroy()
            pswd.insert(0, "Password")
            user.config(state='normal')

        def get_face(lb: Label):
            nonlocal cur_code, count, total_count
            _, img_frame = cam.read()
            cv2image = cv2.cvtColor(cv2.flip(img_frame, 1), cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            lb.imgtk = imgtk
            lb.configure(image=imgtk)
            
            code, result, __ = face_detector.extract_face(img=cv2image)
            if code == cur_code:
                count += 1
                if count >= 5:
                    count = 0
                    if code != 1:
                        status.set(result)
                        fStatus.config(fg=DARD_RED)
                    else:
                        status.set('CHECKING...')
                        fStatus.config(fg='darkgreen')
                        cur_user.set(face_recognizer.recognize_face(img=result))
                        cur_pswd.set("FACE_ID")
                        wnd.after(1000, lambda: auth(fLogin, username=user.get()))
                        wnd.after(3000, lambda: reset_home())
                        return
            else:
                cur_code = code
                count = 0
            total_count += 1
            if total_count >= 300:
                status.set('TIMEOUT')
                fStatus.config(fg=DARD_RED)
                wnd.after(3000, lambda: reset_home())
                return
            
            lb.after(10, lambda: get_face(lb))
        get_face(fCamera)
                


    faceid_btn = Button(fLogin, text="Use Face ID", font=(MAIN_FONT, 13), border=0, bg=COLOR_DARK, fg="white", width=29, relief="flat", command=face_id)
    faceid_btn.place(x=35, y=270)

    signup_btn = Button(fLogin, text="Sign Up", font=(MAIN_FONT, 10, "bold"), border=0, bg="white", fg=COLOR_DARK, width=6, cursor="hand2", command=lambda: fSignUp.tkraise())
    signup_btn.place(x=180, y=311)

    ############################################

    about = Label(fLogin, text="About us", font=(MAIN_FONT, 10, "italic"), bg="white", fg="gray", bd=0)
    about.place(x=34, y=340)
    ToolTip(about, msg="Made by Group 8\n- Nguyen Quoc Huy\n- Duong Hong Nam\n- Nguyen Hai Ninh")

    return frame


def SignUpPg():
    frame = Frame(wnd, width=WWIDTH, height=WHEIGHT, bg='white')
    frame.place(x=0,y=0)

    heading = Label(frame, text="Register", font=(MAIN_FONT, 23, "bold"), bg="white", fg=COLOR_DARK, justify="center")
    heading.place(anchor="center", relx=0.5, rely=0.15)
    Frame(frame, width=500, height=2, bg=MAIN_COLOR).place(x=200, y=110)

    fInput = Frame(frame, width=400, height=450, bg="white")
    fInput.place(x=250, y=150)

    ############################################

    # Username Box
    user = Entry(fInput, width=400, font=(MAIN_FONT, 14), bg="white", fg="black", bd=0)
    user.place(x=0, y=20)
    user.insert(0, "Username")
    user.bind("<FocusIn>", lambda _: user.delete('0', 'end') if user.get() == "Username" else None)
    def check_username(e):
        username = user.get()
        x = 0
        y = 57
        if username in ["" , "Username"]:
            Label(fInput, text="                                        ", font=(MAIN_FONT, 10), bg="white", fg="gray", bd=0).place(x=x, y=y)
            continue_btn.config(state="disabled")
        elif not isValidName(username):
            Label(fInput, text="Invalid character(s)!   ", font=(MAIN_FONT, 10), bg="white", fg=DARD_RED, bd=0).place(x=x, y=y)
            continue_btn.config(state="disabled")
        elif isUser(username):
            Label(fInput, text="Username already exists!    ", font=(MAIN_FONT, 10), bg="white", fg=DARD_RED, bd=0).place(x=x, y=y)
            continue_btn.config(state="disabled")
        else:
            Label(fInput, text="Username available!        ", font=(MAIN_FONT, 10), bg="white", fg="green", bd=0).place(x=x, y=y)
            if pswd.get() not in ['', 'Password']:
                continue_btn.config(state="normal")

    
    user.bind("<KeyRelease>", check_username)
    Frame(fInput, width=400, height=1, bg="gray").place(x=0, y=50)

    # Password Box
    pswd = Entry(fInput, width=25, font=(MAIN_FONT, 14), bg="white", fg="black", bd=0)
    pswd.place(x=0, y=100)
    pswd.insert(0, "Password")
    pswd.bind("<FocusIn>", lambda _: pswd.delete('0', 'end') if pswd.get() == "Password" else None)
    def check_password(e):
        password = pswd.get()
        if password in ['', 'Password']:
            continue_btn.config(state="disabled")
        elif not isUser(user.get()):
            continue_btn.config(state="normal")
    pswd.bind("<KeyRelease>", check_password)
    Frame(fInput, width=400, height=1, bg="gray").place(x=0, y=130)
    Label(fInput, text="* Case Sensitive", font=(MAIN_FONT, 10, 'italic'), bg="white", fg="gray", bd=0).place(x=0, y=137)

    continue_btn = Button(fInput, text="Continue ", state="disabled", font=(MAIN_FONT, 14), fg=COLOR_DARK, image=icContinue, bg="white", bd=0, cursor="hand2", compound="right", command=lambda:setFaceToCapture(username=user.get(), password=pswd.get()))
    continue_btn.place(x=269, y=170)

    back_btn = Button(fInput, text="Back ", font=(MAIN_FONT, 14), fg=DARD_RED, image=icBack, bg="white", bd=0, cursor="hand2", compound="right", command=lambda: fHome.tkraise())
    back_btn.place(x=308, y=225)

    return frame



def setFaceToCapture(username:str , password:str =None):
    global is_new
    cur_user.set(username.lower())
    if password:
        cur_pswd.set(password)
        is_new = True
    else:
        is_new = False
    fCaptureFace.tkraise()

def captureFace(frame: Frame, btn: list = None):
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 500) 
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 300)
    feed = Label(frame, width=500, bg='black', height=300)
    feed.place(x=0, y=100)

    if os.path.exists("res/temp") and os.path.isdir("res/temp"):
        for file in os.listdir("res/temp"):
            os.remove("res/temp/"+file)
    else:
        os.mkdir("res/temp")
    
    count = 0
    def show_frame(lb: Label):
        nonlocal count
        _, img_frame = cam.read()
        img_frame = cv2.flip(img_frame, 1)
        cv2image = cv2.cvtColor(img_frame, cv2.COLOR_BGR2RGB)
        code, result, faceboxes = face_detector.extract_face(img=cv2image)

        if len(faceboxes) != 0:
            for (x, y, w, h) in faceboxes:
                cv2.rectangle(cv2image, (x, y), (x+w, y+h), (255, 0, 0), 2)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        lb.imgtk = imgtk
        lb.configure(image=imgtk)
        
        if code == 1:
            count += 1
            Label(frame, text='Hold still...'+'     '*20, font=(MAIN_FONT, 10), bg="white", fg='green', bd=0).place(x=0, y=70)
            cv2.imwrite(f"res/temp/{count}.jpg", result)
        else:
            Label(frame, text=result+'     '*20, font=(MAIN_FONT, 10), bg="white", fg=DARD_RED, bd=0).place(x=0, y=70)
        if count == LIMIT_CAPTURE:
            cam.release()
            ReviewScreen()
            lb.imgtk = None
            Label(frame, text='     '*20, font=(MAIN_FONT, 10, 'bold'), bg="white", fg='green', bd=0).place(x=0, y=70)
            if btn != None:
                for b in btn:
                    b.config(state="normal")
        else:
            lb.after(10, lambda: show_frame(lb))

    show_frame(feed)

def CaptureFacePg():
    frame = Frame(wnd, width=WWIDTH, height=WHEIGHT, bg='white')
    frame.place(x=0,y=0)

    fCamera = Frame(frame, width=500, height=400, bg="white")
    fCamera.place(x=200, y=50)

    heading = Label(frame, text="Face Capture", font=(MAIN_FONT, 23, "bold"), bg="white", fg=COLOR_DARK, justify="center")
    heading.place(anchor="center", relx=0.5, rely=0.1)
    Frame(frame, width=500, height=2, bg=MAIN_COLOR).place(x=200, y=90)
    # Label(frame, textvariable=cur_user, font=(MAIN_FONT, 15, "bold"), bg="white", fg=MAIN_COLOR, justify="center").place(anchor="center", relx=0.5, rely=0.2)

    def cancelCapture():
        global is_new
        if is_new:
            cur_user.set("")
            cur_pswd.set("")
            fSignUp.tkraise()
            is_new = False
        else:
            fMy.tkraise()
    back_btn = Button(frame, text="Back ", font=(MAIN_FONT, 14), fg=DARD_RED, image=icBack, bg="white", bd=0, cursor="hand2", compound="right", command=cancelCapture)
    back_btn.place(x=80, y=410)

    def startCapture():
        capture_btn.config(state="disabled")
        back_btn.config(state="disabled")
        captureFace(frame=fCamera, btn=[capture_btn, back_btn])
    capture_btn = Button(frame, text="  Start", font=(MAIN_FONT, 14), fg=COLOR_DARK, image=icCamera, bg="white", bd=0, cursor="hand2", compound="left", command=startCapture)
    capture_btn.place(x=730, y=413)

    return frame


def ReviewScreen():
    frame = Frame(wnd, width=WWIDTH, height=WHEIGHT, bg='white')
    frame.place(x=0,y=0)

    fGallery = Frame(frame, width=800, height=400, bg="white")
    fGallery.place(x=33, y=75)

    Label(frame, text="Remove picture(s) before adding", font=(MAIN_FONT, 12), bg="white", fg=COLOR_DARK, justify="center").place(anchor="center", relx=0.5, rely=0.074)
    Frame(frame, width=200, height=1, bg=MAIN_COLOR).place(x=350, y=47)
    Label(frame, text="User:", font=(MAIN_FONT, 11), bg="white", fg="gray").place(x=400, y=50)
    Label(frame, textvariable=cur_user, font=(MAIN_FONT, 11, 'bold'), bg="white", fg="gray").place(x=445, y=50)

    N_COLUMNS = 8
    removed = []
    btn = []
    def btnRemove(i):
        nonlocal removed
        removed.append(i)
        btn[i-1].config(state="disabled")

    total_temp = len(os.listdir(f"res/temp"))
    for i in range(1,total_temp+1):
        img = Image.open(f'res/temp/{i}.jpg')
        r, c = divmod(i-1, N_COLUMNS)
        img = img.resize((90, 90), Image.ADAPTIVE)
        img = ImageTk.PhotoImage(img)
        btn.append(Button(fGallery, image=img, bg="white", state="normal", bd=0, cursor="hand2", command=lambda j=i: btnRemove(j)))
        btn[i-1].image = img
        btn[i-1].grid(row=r, column=c, padx=5, pady=5)

    def cancelSave():
        global is_new
        if is_new:
            cur_user.set("")
            cur_pswd.set("")
            is_new = False
            fSignUp.tkraise()
        else:
            fMy.tkraise()
        if os.path.exists("res/temp") and os.path.isdir("res/temp"):
            for file in os.listdir("res/temp"):
                os.remove("res/temp/"+file)
        frame.destroy()
    cancel_btn = Button(frame, text="  Cancel", font=(MAIN_FONT, 14), fg=DARD_RED, image=icCancel, bg="white", bd=0, cursor="hand2", compound="left", command=cancelSave)
    cancel_btn.place(x=33, y=20)

    def Save():
        global is_new
        username = cur_user.get()
        if is_new:
            os.mkdir(f"data/{username}")
            os.mkdir(f"data/{username}/photo")
            with open(f"data/{username}/password.txt", "a") as f:
                f.write(f"{cur_pswd.get()}")
        for i in range(1,total_temp+1):
            if i not in removed:
                total = len(os.listdir(f"data/{username}/photo"))
                os.rename(f"res/temp/{i}.jpg", f"data/{username}/photo/{total+1}.jpg")
        for file in os.listdir("res/temp"):
            os.remove("res/temp/"+file)

        if is_new:
            cur_user.set("")
            cur_pswd.set("")
            is_new = False
            fHome.tkraise()
            messagebox.showinfo("Success", "New user saved successfully!")
        else:
            fMy.tkraise()
            messagebox.showinfo("Success", "User updated successfully!")
        face_train.train(username)
        frame.destroy()
    save_btn = Button(frame, text="Save ", font=(MAIN_FONT, 14), fg='darkgreen', image=icAdd, bg="white", bd=0, cursor="hand2", compound="right", command=Save)
    if total_temp == 0:
        save_btn.config(state="disabled")
    save_btn.place(x=750, y=20)



def MyPg():
    frame = Frame(wnd, width=WWIDTH, height=WHEIGHT, bg='white')
    frame.place(x=0,y=0)

    heading = Label(frame, textvariable=hello, font=(MAIN_FONT, 23, "bold"), bg="white", fg=COLOR_DARK, justify="center")
    heading.place(anchor="center", relx=0.5, rely=0.15)
    Frame(frame, width=500, height=2, bg=MAIN_COLOR).place(x=200, y=110)

    capture_photo_btn = Button(frame, text='Add Photo from Camera', font=(MAIN_FONT, 16, "bold"), bg=COLOR_DARK, fg="white", justify="center", padx=103, command=lambda: setFaceToCapture(username=cur_user.get()))
    capture_photo_btn.place(anchor="center", relx=0.5, rely=0.4)

    def import_photo():
        if os.path.exists("res/temp") and os.path.isdir("res/temp"):
            for file in os.listdir("res/temp"):
                os.remove("res/temp/"+file)
        files = filedialog.askopenfilenames(initialdir="/", title='Please select photo(s) to import', filetypes=[("Image files", ".jpg .jpeg .png")])
        if len(files) > 0:
            count = 0
            for filepath in files:
                code, result = face_detector.extract_face(PATH=filepath)
                if code == 1:
                    count += 1
                    cv2.imwrite(f"res/temp/{count}.jpg", result)
            ReviewScreen()

    import_photo_btn = Button(frame, text='Add Photo from File', font=(MAIN_FONT, 16, "bold"), bg=COLOR_DARK, fg="white", justify="center", padx=125, command=import_photo)
    import_photo_btn.place(anchor="center", relx=0.5, rely=0.55)

    def change_pass():
        miniwnd = tk.Tk()
        miniwnd.title("Change Password")
        miniwnd.geometry("250x150")
        miniwnd.configure(bg="white")
        miniwnd.resizable(True, True)
        pswd = Entry(miniwnd, width=100, font=(MAIN_FONT, 11), bg="white", fg="black", bd=0)
        pswd.place(x=35, y=35)
        pswd.insert(0, "New Password")
        pswd.bind("<FocusIn>", lambda _: pswd.delete('0', 'end') if pswd.get() == "New Password" else None)
        pswd.bind("<FocusOut>", lambda _: pswd.insert('0', "New Password") if pswd.get() == "" else None)
        Frame(miniwnd, width=180, height=1, bg="gray").place(x=35, y=65)
        def save():
            with open(f"data/{cur_user.get()}/password.txt", "w") as f:
                f.write(f"{pswd.get()}")
            messagebox.showinfo("Success", "Password changed successfully!")
            miniwnd.destroy()
        save_btn = Button(miniwnd, text="Save", font=(MAIN_FONT, 14, 'bold'), fg='white', bg=COLOR_DARK, bd=0, cursor="hand2", command=save)
        save_btn.place(x=150, y=90)
        def check_password():
            password = pswd.get()
            if password in ['', 'New Password']:
                save_btn.config(state="disabled")
            else:
                save_btn.config(state="normal")
        pswd.bind("<KeyRelease>", lambda _: check_password())
        
        miniwnd.mainloop()

    change_pass_btn = Button(frame, text='Change Password', font=(MAIN_FONT, 16, "bold"), bg=COLOR_DARK, fg="white", justify="center", padx=139, command=change_pass)
    change_pass_btn.place(anchor="center", relx=0.5, rely=0.7)

    quit_btn = Button(frame, text='Quit', font=(MAIN_FONT, 16, "bold"), bg=DARD_RED, fg="white", justify="center", padx=100, command=lambda: wnd.destroy())
    quit_btn.place(anchor="center", relx=0.5, rely=0.85)

    return frame

# Start the Tkinter event loop
fMy = MyPg()
fCaptureFace = CaptureFacePg()
fSignUp = SignUpPg()
fHome = HomePg()
wnd.mainloop()