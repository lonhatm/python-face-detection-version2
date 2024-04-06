import cv2
import numpy as np
import face_recognition
import os

from tkinter import *
import tkinter.font as tkFont
from PIL import Image, ImageTk
import subprocess
import importlib
import lowpc as low

# sửa lỗi chương trình bị mờ

from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

# lỗi không đươ3jc phép import 2 lần

window = Tk()
window.title('OpenCV')
window_width, window_height  = window.winfo_screenwidth(), window.winfo_screenheight()
window.geometry("1528x816")
window.minsize(1528,816)

# giao diện

uiColor_bg = "#ffffff"
uiColor_fg = "#26282C"
uiColor_fgAlt = "#ffffff"
uiColor_label = "#898DA9"
uiColor_primary = "#4763EB"
uiColor_suface = "#DFE1EC"

window.configure(bg=uiColor_bg)

uiFont_title = tkFont.Font(family='Helvetica', size=24, weight='bold')
uiFont_btn = tkFont.Font(family='Helvetica', size=16, weight='bold')
uiFont_label = tkFont.Font(family='Helvetica', size=14)
uiFont_labelBold = tkFont.Font(family='Helvetica', size=14, weight='bold')

#

canvas = Canvas(window, width=window_width, height=window_height)
canvas.configure(bg=uiColor_bg)
canvas.grid()

detected_name = "Unknown"
folder_path = "anh_chup"
name_printed = False  
known_face_encodings = []
known_face_names = []

for filename in os.listdir(folder_path):
    image_path = os.path.join(folder_path, filename)
    if os.path.isfile(image_path):
        image = face_recognition.load_image_file(image_path)
        face_encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(face_encoding)
        known_face_names.append(os.path.splitext(filename)[0])


def detect_faces(frame):
    global detected_name, name_printed
    if detected_name == "Unknown" and not name_printed:
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
            detected_name = name
    return frame

cap = cv2.VideoCapture(0)
def video_thread():
    global name_printed
    while True:
        ret, frame = cap.read()
        processed_frame = detect_faces(frame)
        rgb_image = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_image)
        tk_image = ImageTk.PhotoImage(pil_image.resize((960, 720)))
        canvas.create_image(520, 48, anchor=NW, image=tk_image)
        canvas.image = tk_image  # Lưu trữ tham chiếu để tránh bị giải phóng bộ nhớ
        if detected_name!= "Unknown" and not name_printed:
            print("Detected name:", detected_name)
            name_printed = True
        if not window.winfo_exists():
            break
        if cv2.waitKey(1) == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

### ui linh tinh

# logo
uiImg_logo = ImageTk.PhotoImage(Image.open('D:/PROJECT/uh/pfd-ver2/assets/logo.png'))
imgLogo = Label(window, image=uiImg_logo)
imgLogo.place(x=48, y=60)
imgLogo.config(bg=uiColor_bg)

# hướng dẫn
labelGuide = Label(window, text="Bla bla cái gì đấy để ngta\nbiết mình làm gì.")
labelGuide.place(x=48, y=168)
labelGuide.config(bg=uiColor_bg, fg=uiColor_label, font=uiFont_label)

# label version ở dưới?
#labelVersion = Label(window, text="Facelog v1.0")
#labelVersion.place(x=48, y=window_height-48)
#labelVersion.config(fg="#898DA9", font=uiFont_label)


#nút bắt đầu nhận diện
uiIco_arrow = ImageTk.PhotoImage(Image.open('D:/PROJECT/uh/pfd-ver2/assets/reg.png'))

btnBatdau = Button(window, text="BẮT ĐẦU", image=uiIco_arrow, compound='left')
btnBatdau.place(x=48, y=272 , width=424, height=96)
btnBatdau.config(bg=uiColor_primary, fg=uiColor_fgAlt, borderwidth=0, font = uiFont_btn, anchor='w', padx=32)

def defBatdau(event):
    low.cauhinh(video_thread)
btnBatdau.bind("<Button-1>", defBatdau)

# đăng kí và nhập thông tin
uiIco_useradd = ImageTk.PhotoImage(Image.open('D:/PROJECT/uh/pfd-ver2/assets/useradd.png'))

btnDangky = Button(window, text="ĐĂNG KÝ", image=uiIco_useradd, compound='left')
btnDangky.place(x=48, y=392, width=424, height=96)
btnDangky.config(bg=uiColor_suface, fg=uiColor_fg, borderwidth=0, font = uiFont_btn, anchor='w', padx=32)

def defDangky(event):
    print("login")
btnDangky.bind("<Button-1>", defDangky)

# cài đặt
ui_icoSetting = ImageTk.PhotoImage(Image.open('D:/PROJECT/uh/pfd-ver2/assets/setting.png'))

btnSetting = Button(window, image=ui_icoSetting, compound='left')
btnSetting.place(x=400, y=48, width=72, height=72)
btnSetting.config(bg=uiColor_bg, fg=uiColor_bg, borderwidth=0)

def openCaidat(event):
    windowCaidat = Toplevel(window)
    windowCaidat.geometry("520x816")
    windowCaidat.minsize(520,816)
    windowCaidat.title("Cài đặt")
    windowCaidat.transient(window)
    windowCaidat.configure(bg=uiColor_bg)
    windowCaidat.grab_set()
    windowCaidat.protocol("WM_DELETE_WINDOW", lambda: close_child(windowCaidat))

    labelTitle = Label(windowCaidat, text="Cài đặt")
    labelTitle.place(x=48, y=48)
    labelTitle.config(bg=uiColor_bg, fg=uiColor_fg, font=uiFont_title, borderwidth=0)

    ## Camera

    labelCamera = Label(windowCaidat, text="Camera")
    labelCamera.place(x=48, y=172-24-12)
    labelCamera.config(bg=uiColor_bg, fg=uiColor_label, font=uiFont_label)

    # load camera hiện có xong cho vào đây?
    optionsCamera = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    clicked_optionsCamera = StringVar()
    clicked_optionsCamera.set("Monday") 

    dropdownCamera = OptionMenu(windowCaidat, clicked_optionsCamera, *optionsCamera)
    dropdownCamera.place(x=48, y=216-24-12, width=424, height=80)
    dropdownCamera.config(bg=uiColor_suface, fg=uiColor_fg, font=uiFont_labelBold, borderwidth=0)

    ## Chế độ

    labelRegMode = Label(windowCaidat, text="Chế độ nhận diện")
    labelRegMode.place(x=48, y=320-24-12)
    labelRegMode.config(bg=uiColor_bg, fg=uiColor_label, font=uiFont_label)

    optionsRegMode = ["Bình thường", "Hiệu suất", "Chính xác cao"]
    clicked_optionsRegMode = StringVar()
    clicked_optionsRegMode.set("Bình thường") 

    dropdownRegMode = OptionMenu(windowCaidat, clicked_optionsRegMode, *optionsRegMode)
    dropdownRegMode.place(x=48, y=364-24-12, width=424, height=80)
    dropdownRegMode.config(bg=uiColor_suface, fg=uiColor_fg, font=uiFont_labelBold, borderwidth=0)

def close_child(window):
    window.grab_release()
    window.destroy()

btnSetting.bind("<Button-1>", openCaidat)



window.mainloop()