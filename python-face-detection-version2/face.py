import cv2
import numpy as np
import face_recognition
import os

from tkinter import *
from PIL import Image, ImageTk
import subprocess
import importlib
import lowpc as low
# lỗi không đươ3jc phép import 2 lần
window = Tk()
window.title('OpenCV')
window_w, window_h = window.winfo_screenwidth(), window.winfo_screenheight()
window_height = window_h - 70
window_width = window_w + 30
window.geometry(f"{window_width}x{window_height}")
canvas = Canvas(window, width=window_width, height=window_height)
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
        tk_image = ImageTk.PhotoImage(pil_image)
        canvas.create_image(0, 0, anchor=NW, image=tk_image)
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
    


#nút bắt đầu nhận diện
button_start = Button(window, text="Bắt Đầu")
button_start.place(x=113, y=205 , width=319, height=80)
button_start.config(bg="red", borderwidth=0)
def on_click(event):
    low.cauhinh(video_thread)
button_start.bind("<Button-1>", on_click)

# đăng kí và nhập thông tin
button_login = Button(window, text="đăng kí")
button_login.place(x=112, y=359-28, width=319, height=80)
button_login.config(bg="blue", borderwidth=0)
def on_click(event):
    print("login")
button_login.bind("<Button-1>", on_click)
window.mainloop()