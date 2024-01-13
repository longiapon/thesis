import cv2
import tkinter as tk
from tkinter import ttk
import customtkinter as ct
from customtkinter import CTkImage
import threading
from PIL import ImageTk, Image 
from ultralytics import YOLO
import cv2
import cvzone
import math
import time
import tkinter.messagebox as messagebox
import subprocess
import thread1
import thread2
import thread3
import importlib
import datetime
from plyer import notification
import os

notif_value = 0
index_value = 0 


class Video_Player:
        def __init__(self, root):
            self.root = root
            self.root.title("EGO-Park")
            self.root.config(bg="darkgray")
            self.root.state('zoomed')
            self.gallery_ui()
            self.new_notif_frame = ct.CTkFrame(master=self.root, width=300, height=300, fg_color="lightgray",
                                           border_width=0, border_color="gray", corner_radius=0)
            self.new_notif_frame.place(x=10, y=35)
        
            self.label_frame = tk.Frame(self.new_notif_frame, bg="#f9f9f9", height=20)
            self.label_frame.pack(side='top', padx=2)
        
            self.notification_label = tk.Label(self.label_frame, text="Notification", font=("Roboto", 11, "bold"),
                                           bg="#f9f9f9", anchor='w', width=40)
            self.notification_label.pack(side='left', padx=15)  
        
            self.canvas_notif = tk.Canvas(self.new_notif_frame, bg="white", height=300)
            self.scrollable_frame = ttk.Frame(self.canvas_notif)
        
            self.scrollbar = ttk.Scrollbar(self.new_notif_frame, orient="vertical", command=self.canvas_notif.yview)
            self.canvas_notif.configure(yscrollcommand=self.scrollbar.set)

            self.scrollbar.pack(side="left", fill="y")
            self.canvas_notif.pack(side="left", fill="both", expand=False, padx=2, pady=2)
            self.canvas_notif.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
            style = ttk.Style()
            style.configure("TFrame", background="white")
        
            self.scrollable_frame.bind("<Configure>", self.on_frame_configure)
            #canvas for video threading
            self.canvas = tk.Canvas(self.root, width=1200, height=800, bg="lightgray", bd=5)
            self.canvas.place(x=420, y=35)
            #video_thread
            self.video_canvas = tk.Canvas(self.canvas, width=500, height=300, bg="white", bd=5)
            self.video_canvas.grid(row=0, column=0, padx=15, pady=30)
            self.video_canvas1 = tk.Canvas(self.canvas, width=500, height=300, bg="white", bd=5)
            self.video_canvas1.grid(row=0, column=1, padx=15, pady=30)
            self.video_canvas2 = tk.Canvas(self.canvas, width=500, height=300, bg="white", bd=5)
            self.video_canvas2.grid(row=1, column=0, padx=15, pady=(0,30))
            self.video_canvas3 = tk.Canvas(self.canvas, width=500, height=300, bg="white", bd=5)
            self.video_canvas3.grid(row=1, column=1, padx=15, pady=(0,30))
            #button in thread1
            self.detect1 = tk.Button(self.canvas, width=10, height=1,text="Detect", bg="white", bd=0, cursor="hand2", command=self.open_new_window1)
            self.detect1.place(x=452, y=348)
            self.btn_start = tk.Button(self.canvas, width=10, height=1,text="Add Camera", bg="white", bd=0, cursor="hand2", command=self.start_video1)
            self.btn_start.place(x=350, y=348)
            self.cam_lbl1 = tk.Label(self.canvas, width=10, height=1, text="Camera 1", bg="lightgray")
            self.cam_lbl1.place(x=22, y=37)
            #button in thread2
            self.detect2 = tk.Button(self.canvas, width=10, height=1,text="Detect", bg="white", bd=0, cursor="hand2", command=self.open_new_window2)
            self.detect2.place(x=997, y=348)
            self.btn_start1 = tk.Button(self.canvas, width=10, height=1,text="Add Camera", bg="white", bd=0, cursor="hand2", command=self.start_video2)
            self.btn_start1.place(x=895, y=348)
            self.cam_lbl2 = tk.Label(self.canvas, width=10, height=1, text="Camera 2", bg="lightgray")
            self.cam_lbl2.place(x=566, y=37)
            #button in thread3
            self.detect3 = tk.Button(self.canvas, width=10, height=1,text="Detect", bg="white", bd=0, cursor="hand2", command=self.open_new_window3)
            self.detect3.place(x=452, y=692)
            self.btn_start3 = tk.Button(self.canvas, width=10, height=1,text="Add Camera", bg="white", bd=0, cursor="hand2", command=self.start_video3)
            self.btn_start3.place(x=350, y=692)
            self.cam_lbl3 = tk.Label(self.canvas, width=10, height=1, text="Camera 3", bg="lightgray")
            self.cam_lbl3.place(x=22, y=381)
            #button in thread4
            self.detect4 = tk.Button(self.canvas, width=10, height=1,text="Detect", bg="white", bd=0, cursor="hand2", command=self.open_new_window4)
            self.detect4.place(x=997, y=692)
            self.btn_start4 = tk.Button(self.canvas, width=10, height=1,text="Add Camera", bg="white", bd=0, cursor="hand2", command=self.start_video4)
            self.btn_start4.place(x=895, y=692)
            self.cam_lbl1 = tk.Label(self.canvas, width=10, height=1, text="Camera 4", bg="lightgray")
            self.cam_lbl1.place(x=566, y=381)
            #notification variable
            self.notif_value = 0
            self.index_value = 0
            self.max_notifications = 13
            self.notification_labels = []
            #capturing images variable
            self.image_paths = []
            self.frame = None
            self.lock = threading.Lock()
            #video thread variable
            self.capture = None
            self.thread1 = None
            self.capture1 = None
            self.thread2 = None
            self.capture2 = None
            self.thread3 = None
            self.capture3 = None
            self.thread4 = None

        def gallery_ui(self):
            # self.root.title("Image Capture and Notification")

            # Create the folder if it doesn't exist
            self.image_folder = "Captured_Images"
            os.makedirs(self.image_folder, exist_ok=True)

            # Capture Button
            # self.capture_button = tk.Button(self.root, text="Capture Image", command=self.capture_image)
            # self.capture_button.pack(pady=10)

            # Gallery Frame
            self.gallery_frame = ct.CTkFrame(master=self.root, width=300, height=300, fg_color="lightgray",
                                           border_width=0, border_color="gray", corner_radius=0)
            self.gallery_frame.place(x=10, y=381)
            # self.new_notif_frame = ct.CTkFrame(master=self.root, width=300, height=300, fg_color="lightgray",
            #                                border_width=0, border_color="gray", corner_radius=0)
            # self.new_notif_frame.place(x=10, y=35)

            self.captured_label_frame = tk.Frame(self.gallery_frame, bg="#f9f9f9", height=20)
            self.captured_label_frame.pack(side='top', padx=2)

            self.captured_label = tk.Label(self.captured_label_frame, text="Captured Images", font=("Roboto", 11, "bold"),
                                        bg="#f9f9f9", anchor='w', width=40)
            self.captured_label.pack(side='left', padx=15)

            self.canvas_captured = tk.Canvas(self.gallery_frame, bg="white", height=342)
            self.scrollable_captured_frame = ttk.Frame(self.canvas_captured)

            self.scrollbar_captured = ttk.Scrollbar(self.gallery_frame, orient="vertical",
                                                    command=self.canvas_captured.yview)
            self.canvas_captured.configure(yscrollcommand=self.scrollbar_captured.set)

            self.scrollbar_captured.pack(side="left", fill="y")
            self.canvas_captured.pack(side="left", fill="both", expand=True, padx=2, pady=2)
            self.canvas_captured.create_window((0, 0), window=self.scrollable_captured_frame, anchor="nw")

            self.scrollable_captured_frame.bind("<Configure>", self.on_captured_frame_configure)

        def load_existing_images(self):
            # Load existing images from the folder
            existing_images = [f for f in os.listdir(self.image_folder) if f.endswith(".jpg")]

            # Add the image paths to the list
            self.image_paths.extend([os.path.join(self.image_folder, img) for img in existing_images])

            # Display the existing images in the gallery
            for image_path in self.image_paths:
                self.display_captured_image(image_path, in_captured_frame=True)

        def capture_image(self, image):
            # Capture image using OpenCV
            # cap = cv2.VideoCapture(0)
            # ret, frame = cap.read()
            # cap.release()
            with self.lock:
                self.frame = image
            # Save the captured image
            image_path = os.path.join(self.image_folder, f"captured_image_{len(self.image_paths) + 1}.jpg")
            cv2.imwrite(image_path, self.frame)

            # Add the image path to the list
            self.image_paths.append(image_path)

            # Display the captured image on the Tkinter GUI
            self.display_captured_image(image_path, in_captured_frame=True)

            # Send notification with app icon
            notification_title = "Image Captured"
            notification_message = "Image captured successfully!"
            notification.notify(
                title=notification_title,
                message=notification_message,
                app_icon=None,
                timeout=10,  # seconds
            )
        
        def release(self):
            self.cap.release()

        def display_captured_image(self, image_path, in_captured_frame=False):
            # Open the captured image using PIL
            image = Image.open(image_path)
            image = image.resize((300, 150), Image.LANCZOS)  # Use LANCZOS for antialiasing
            photo = ImageTk.PhotoImage(image)

            # Choose the appropriate canvas and scrollable frame based on the parameter
            if in_captured_frame:
                canvas = self.canvas_captured
                scrollable_frame = self.scrollable_captured_frame
            else:
                canvas = self.canvas_notif
                scrollable_frame = self.scrollable_frame

            # Update the canvas
            canvas.create_image(0, 0, anchor="nw", image=photo)
            canvas.config(scrollregion=canvas.bbox("all"))

            # Add the captured image to the scrollable frame
            label = tk.Label(scrollable_frame, image=photo, borderwidth=2, relief="solid")
            label.image = photo
            label.pack(side=tk.TOP, padx=5, pady=5)

        def on_frame_configure(self, event):
            self.canvas_notif.configure(scrollregion=self.canvas_notif.bbox("all"))

        def on_captured_frame_configure(self, event):
            self.canvas_captured.configure(scrollregion=self.canvas_captured.bbox("all"))

        def add_notif(self, camera_name, msg):
            # self.capture_image()
            current_datetime = datetime.datetime.now()
            hour = current_datetime.hour
            minute = current_datetime.minute
            period = "AM" if hour < 12 else "PM"
            if hour > 12:
                hour -= 12
            current_time = f"{hour:02}:{minute:02} {period}"

            new_message = f"{camera_name} {msg}"

            if self.notif_value < self.max_notifications:
                # If we haven't reached the maximum number of notifications, create a new label
                scroll_label_frame = tk.Frame(self.scrollable_frame, bg="white")
                scroll_label_frame.grid(row=self.notif_value, column=0, padx=10, pady=5)

                scroll_time = tk.Label(scroll_label_frame, text=current_time, font=("Roboto", 9),
                                    bg="white", anchor='e', fg="#6f6f6f", width=27)
                scroll_time.pack(side='bottom')

                scroll_label = tk.Label(scroll_label_frame, text=new_message, wraplength=300, justify='left', anchor='w',
                                        font=("Roboto", 11), bg="white")
                scroll_label.pack(side='bottom', padx=10)

                self.notification_labels.append(scroll_label_frame)
                self.notif_value += 1
            else:
                # If we have reached the maximum number of notifications, update existing labels
                index_to_update = self.index_value % self.max_notifications
                label_to_update = self.notification_labels[index_to_update]

                # Update time label
                time_label = label_to_update.winfo_children()[0]
                time_label.config(text=current_time)

                # Update message label
                message_label = label_to_update.winfo_children()[1]
                message_label.config(text=new_message)

                # Increment the index value
                self.index_value += 1

        
        def on_frame_configure(self, event=None):
                self.canvas_notif.configure(scrollregion=self.canvas_notif.bbox("all"))

        def on_mousewheel(self, event=None):
                self.canvas_notif.yview_scroll(-1*(event.delta//120), "units")


        def open_new_window1(self):
            if self.capture is None and self.thread1 is None:
                messagebox.showerror("Error", "Camera not open!")
                return
            else:
                player_window = tk.Toplevel(self.root)
                player = VideoProcessor1(player_window, self)
                player_window.mainloop()

        def open_new_window2(self):
            if self.capture1 is None and self.thread2 is None:
                messagebox.showerror("Error", "Camera not open!")
                return
            else:
                # self.video_processor_instance = VideoProcessor2(root, self)
                # player = VideoProcessor2(tk.Toplevel(self.root, self.video_processor_instance)) 
                # player.root.mainloop()
                player_window = tk.Toplevel(self.root)
            
            # Create the VideoProcessor2 instance for the new window
                player = VideoProcessor2(player_window, self)
                video_processor = VideoProcessor2(processor)
                player_window.mainloop()

        def open_new_window3(self):
            if self.capture2 is None and self.thread3 is None:
                messagebox.showerror("Error", "Camera not open!")
                return
            else:
                player_window = tk.Toplevel(self.root)
                player = VideoProcessor3(player_window, self)
                player_window.mainloop()


        def open_new_window4(self):
            if self.capture3 is None and self.thread4 is None:
                messagebox.showerror("Error", "Camera not open!")
                return
            else:
                player_window = tk.Toplevel(self.root)
                player = VideoProcessor4(player_window, self)
                player_window.mainloop()

        def start_video1(self):
            if self.thread1 and self.thread1.is_alive():
            # If a video thread is already running, don't start a new one
                return
            # self.capture = cv2.VideoCapture('rtsp://egopark1:egopark1234@192.168.1.107:554/stream1')
            self.capture = cv2.VideoCapture(0)

            self.thread1 = threading.Thread(target=self.video_thread1)
            self.thread1.start()

        def start_video2(self):
            if self.thread2 and self.thread2.is_alive():
            # If a video thread is already running, don't start a new one
                return
            self.capture1 = cv2.VideoCapture("Videos/video5.mp4")

            self.thread2 = threading.Thread(target=self.video_thread2)
            self.thread2.start()

        def start_video3(self):
            if self.thread3 and self.thread3.is_alive():
            # If a video thread is already running, don't start a new one
                return
            self.capture2 = cv2.VideoCapture("Videos/video6.mp4")

            self.thread3 = threading.Thread(target=self.video_thread3)
            self.thread3.start()

        def start_video4(self):
            if self.thread4 and self.thread4.is_alive():
            # If a video thread is already running, don't start a new one
                return
            self.capture3 = cv2.VideoCapture(0)

            self.thread4 = threading.Thread(target=self.video_thread4)
            self.thread4.start()

        def video_thread1(self):           
            while self.capture.isOpened():
                success, img = self.capture.read()
                if not success:
                    break
                img = cv2.resize(img, (500, 300))  
                frame_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                photo = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb))
                self.video_canvas.create_image(3, 3, anchor=tk.NW, image=photo)
                self.video_canvas.image = photo
            
            if self.capture:
                self.capture.release()

        def video_thread2(self):                        
            while self.capture1.isOpened():
                success, img = self.capture1.read()
                if not success:
                    break
                img = cv2.resize(img, (500, 300))  
                frame_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                photo = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb))
                self.video_canvas1.create_image(3, 3, anchor=tk.NW, image=photo)
                self.video_canvas1.image = photo

            if self.capture1:
                self.capture1.release()

        def video_thread3(self):                        
            while self.capture2.isOpened():
                success, img = self.capture2.read()
                if not success:
                    break
                img = cv2.resize(img, (500, 300))  
                frame_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                photo = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb))
                self.video_canvas2.create_image(3, 3, anchor=tk.NW, image=photo)
                self.video_canvas2.image = photo

            if self.capture2:
                self.capture2.release()

        def video_thread4(self):                        
            while self.capture3.isOpened():
                success, img = self.capture3.read()
                if not success:
                    break
                img = cv2.resize(img, (500, 300))  
                frame_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                photo = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb))
                self.video_canvas3.create_image(3, 3, anchor=tk.NW, image=photo)
                self.video_canvas3.image = photo

            if self.capture3:
                self.capture3.release()

class VideoProcessor1:
    def __init__(self, root, video_player_instance):
        self.root = root
        self.root.title("Camera 1")
        self.root.config(bg="darkgray")
        self.root.geometry("1200x700")
        self.video_player_instance = video_player_instance
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 1200  
        window_height = 700
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        # self.root.state('zoomed')
        self.video_canvas = tk.Canvas(self.root, width=1200, height=700, bg="white", bd=5)
        self.video_canvas.pack()

        # self.capture = cv2.VideoCapture('rtsp://egopark1:egopark1234@192.168.1.107:554/stream1')
        self.capture = cv2.VideoCapture(0)
        self.model = YOLO("../yolo-weights/yolov8n.pt")  

        self.notification_sent = False
        self.last_detection_time = time.time()
        self.start_time = time.time()
        self.start_time_roi2 = None
        self.notification_interval = 21 
        self.double_notify = 50
        self.detected_roi1 = False
        self.detected_roi2 = False

        thread1 = threading.Thread(target=self.process_video)
        thread1.start()

    def process_video(self):
        classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
                        "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
                        "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
                        "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
                        "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
                        "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
                        "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "potted plant", "bed",
                        "dining table", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
                        "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
                        "teddy bear", "hair drier", "toothbrush"]
            
        area = [(690, 340), (1077, 336), (767, 595), (990, 591)]
        area1 = [(520, 400), (723, 361), (548, 598), (690, 595)]
        pt1 = area[0]
        pt2 = area[3]
        pt1_area1 = area1[0]
        pt2_area1 = area1[3]

        while True:
            success, img = self.capture.read()
            if not success:
                break

            img = cv2.resize(img, (1200, 700))
            # cv2.rectangle(img, pt1, pt2, (0, 255, 0), 2)
            # cv2.rectangle(img, pt1_area1, pt2_area1, (0, 255, 0), 2)
                
            roi_1 = img[pt1[1]:pt2[1], pt1[0]:pt2[0]]
            roi_2 = img[pt1_area1[1]:pt2_area1[1], pt1_area1[0]:pt2_area1[0]]
                
            results_1 = self.model(roi_1, stream=True)
            results_2 = self.model(roi_2, stream=True)

            for r in results_1:
                boxes = r.boxes

                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    w, h = x2 - x1, y2 - y1
                    conf = math.ceil((box.conf[0] * 100)) / 100
                    cls = int(box.cls[0])
                    self.currentClass1 = classNames[cls]

                    if self.currentClass1 in ["car", "bus", "truck", "motorbike"]:
                        # Replace this with your ROI detection logic
                        cvzone.cornerRect(roi_1, (x1, y1, w, h), l=7)
                        cvzone.putTextRect(roi_1, f'{classNames[cls]} {conf}', (max(0, x1), max(35, y1)), scale=1, thickness=1)
                        self.detected_roi1 = True  # For illustration purposes, you can adjust this based on your logic
                
            for r in results_2:
                boxes = r.boxes
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    w, h = x2 - x1, y2 - y1
                    conf = math.ceil((box.conf[0] * 100)) / 100
                    cls = int(box.cls[0])
                    self.currentClass2 = classNames[cls]
                        
                    if self.currentClass2 in ["car", "bus", "truck", "motorbike"]:
                        cvzone.cornerRect(roi_2, (x1, y1, w, h), l=7)
                        cvzone.putTextRect(roi_2, f'{classNames[cls]} {conf}', (max(0, x1), max(35, y1)), scale=1, thickness=1)
                        self.detected_roi2 = True

                        if self.start_time_roi2 is None:
                            self.start_time_roi2 = time.time()

            self.notify()  # Check for notifications based on detected ROIs
            frame_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            photo = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb))
            self.video_canvas.create_image(3, 3, anchor=tk.NW, image=photo)
            self.video_canvas.image = photo

    def notify(self):
        current_time = time.time()

            # Illegal Parking Notification
        if self.detected_roi1 and (current_time - self.start_time > self.notification_interval) and not self.notification_sent:
            messagebox.showwarning("Camera 1", "  vehicle detected in restricted area \n Parked illegal!")
            self.video_player_instance.add_notif("Camera 1", " Vehicle detected in restricted area \n Parked illegal!")
            self.notification_sent = True
            self.start_time = current_time  # Reset the timer
            self.last_notification_time = current_time

            # Double Parking Notification
        if self.detected_roi1 and self.detected_roi2 and (current_time - self.last_detection_time > self.double_notify):
                # Check if the vehicle in detected_roi2 has stayed for at least 20 seconds
            if (current_time - self.start_time_roi2) > 20:
                messagebox.showwarning("Camera 1", " Two vehicle detecteted in restricted area \n Double Parking!")
                self.video_player_instance.add_notif("Camera 1", " Two vehicle detecteted in restricted area \n Double Parking!")
                self.last_detection_time = current_time
                self.notification_sent = False  # Reset the flag after sending the notification
                self.start_time = current_time 

class VideoProcessor2:
    def __init__(self, root, video_player_instance):
        self.root = root
        self.root.title("Camera 2")
        self.root.config(bg="darkgray")
        self.root.geometry("1200x700")
        self.video_player_instance = video_player_instance
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 1200  
        window_height = 700
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        # self.root.state('zoomed')
        self.video_canvas = tk.Canvas(self.root, width=1200, height=700, bg="white", bd=5)
        self.video_canvas.pack()

        # self.capture = cv2.VideoCapture('rtsp://egopark1:egopark1234@192.168.1.107:554/stream1')
        self.capture = cv2.VideoCapture("Videos/video5.mp4")
        self.model = YOLO("../yolo-weights/yolov8n.pt")  

        self.notification_sent = False
        self.last_detection_time = time.time()
        self.start_time = time.time()
        self.start_time_roi2 = None
        self.notification_interval = 21 
        self.double_notify = 50
        self.detected_roi1 = False
        self.detected_roi2 = False

        thread1 = threading.Thread(target=self.process_video)
        thread1.start()

    def process_video(self):
        classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
                        "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
                        "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
                        "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
                        "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
                        "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
                        "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "potted plant", "bed",
                        "dining table", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
                        "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
                        "teddy bear", "hair drier", "toothbrush"]
            
        area = [(690, 340), (1077, 336), (767, 595), (990, 591)]
        area1 = [(520, 400), (723, 361), (548, 598), (690, 595)]
        pt1 = area[0]
        pt2 = area[3]
        pt1_area1 = area1[0]
        pt2_area1 = area1[3]

        while True:
                success, img = self.capture.read()
                if not success:
                    break

                img = cv2.resize(img, (1200, 700))
                cv2.rectangle(img, pt1, pt2, (0, 255, 0), 2)
                cv2.rectangle(img, pt1_area1, pt2_area1, (0, 255, 0), 2)
                    
                roi_1 = img[pt1[1]:pt2[1], pt1[0]:pt2[0]]
                roi_2 = img[pt1_area1[1]:pt2_area1[1], pt1_area1[0]:pt2_area1[0]]
                    
                results_1 = self.model(roi_1, stream=True)
                results_2 = self.model(roi_2, stream=True)

                for r in results_1:
                    boxes = r.boxes

                    for box in boxes:
                        x1, y1, x2, y2 = box.xyxy[0]
                        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                        w, h = x2 - x1, y2 - y1
                        conf = math.ceil((box.conf[0] * 100)) / 100
                        cls = int(box.cls[0])
                        self.currentClass1 = classNames[cls]

                        if self.currentClass1 in ["car", "bus", "truck", "motorbike"]:
                            # Replace this with your ROI detection logic
                            cvzone.cornerRect(roi_1, (x1, y1, w, h), l=7)
                            cvzone.putTextRect(roi_1, f'{classNames[cls]} {conf}', (max(0, x1), max(35, y1)), scale=1, thickness=1)
                            self.detected_roi1 = True  # For illustration purposes, you can adjust this based on your logic
                    
                for r in results_2:
                    boxes = r.boxes
                    for box in boxes:
                        x1, y1, x2, y2 = box.xyxy[0]
                        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                        w, h = x2 - x1, y2 - y1
                        conf = math.ceil((box.conf[0] * 100)) / 100
                        cls = int(box.cls[0])
                        self.currentClass2 = classNames[cls]
                            
                        if self.currentClass2 in ["car", "bus", "truck", "motorbike"]:
                            cvzone.cornerRect(roi_2, (x1, y1, w, h), l=7)
                            cvzone.putTextRect(roi_2, f'{classNames[cls]} {conf}', (max(0, x1), max(35, y1)), scale=1, thickness=1)
                            self.detected_roi2 = True

                            if self.start_time_roi2 is None:
                                self.start_time_roi2 = time.time()

                self.notify(img)  # Check for notifications based on detected ROIs
                # self.video_player_instance.capture_image(img)
                frame_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                photo = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb))
                self.video_canvas.create_image(3, 3, anchor=tk.NW, image=photo)
                self.video_canvas.image = photo
    def notify(self, image):
        current_time = time.time()

            # Illegal Parking Notification
        if self.detected_roi1 and (current_time - self.start_time > self.notification_interval) and not self.notification_sent:
            messagebox.showwarning("Camera 2", "  vehicle detected in restricted area \n Parked illegal!")
            self.video_player_instance.add_notif("Camera 2", " Vehicle detected in restricted area \n Parked illegal!")
            self.video_player_instance.capture_image(image)
            self.notification_sent = True
            self.start_time = current_time  # Reset the timer
            self.last_notification_time = current_time
        elif self.notification_sent and (current_time - self.last_notification_time > 20):
            # Reset the notification flag after 20 seconds
            self.notification_sent = False

            # Double Parking Notification
        if self.detected_roi1 and self.detected_roi2 and (current_time - self.last_detection_time > self.double_notify):
                # Check if the vehicle in detected_roi2 has stayed for at least 20 seconds
            if (current_time - self.start_time_roi2) > 20:
                messagebox.showwarning("Camera 2", " Two vehicle detecteted in restricted area \n Double Parking!")
                self.video_player_instance.add_notif("Camera 2", " Two vehicle detecteted in restricted area \n Double Parking!")
                self.last_detection_time = current_time
                self.notification_sent = False  # Reset the flag after sending the notification
                self.start_time = current_time 

class VideoProcessor3:
    def __init__(self, root, video_player_instance):
        self.root = root
        self.root.title("Camera 3")
        self.root.config(bg="darkgray")
        self.root.geometry("1200x700")
        self.video_player_instance = video_player_instance
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 1200  
        window_height = 700
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        # self.root.state('zoomed')
        self.video_canvas = tk.Canvas(self.root, width=1200, height=700, bg="white", bd=5)
        self.video_canvas.pack()

        # self.capture = cv2.VideoCapture('rtsp://egopark1:egopark1234@192.168.1.107:554/stream1')
        self.capture = cv2.VideoCapture("Videos/video6.mp4")
        self.model = YOLO("../yolo-weights/yolov8n.pt")  

        self.notification_sent = False
        self.last_detection_time = time.time()
        self.start_time = time.time()
        self.start_time_roi2 = None
        self.notification_interval = 21 
        self.double_notify = 50
        self.detected_roi1 = False
        self.detected_roi2 = False

        thread1 = threading.Thread(target=self.process_video)
        thread1.start()

    def process_video(self):
        classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
                        "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
                        "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
                        "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
                        "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
                        "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
                        "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "potted plant", "bed",
                        "dining table", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
                        "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
                        "teddy bear", "hair drier", "toothbrush"]
            
        area = [(597, 266), (624, 591), (1001, 588), (994, 263)]
        pt1 = area[0]
        pt2 = area[2]

        while True:
            success, img = self.capture.read()
            if not success:
                break

            img = cv2.resize(img, (1200, 700))
            cv2.rectangle(img, pt1, pt2, (0, 255, 0), 2)
            # cv2.rectangle(img, pt1_area1, pt2_area1, (0, 255, 0), 2)
                
            roi_1 = img[pt1[1]:pt2[1], pt1[0]:pt2[0]]
            # roi_2 = img[pt1_area1[1]:pt2_area1[1], pt1_area1[0]:pt2_area1[0]]
                
            results_1 = self.model(roi_1, stream=True)
            # results_2 = self.model(roi_2, stream=True)

            for r in results_1:
                boxes = r.boxes

                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    w, h = x2 - x1, y2 - y1
                    conf = math.ceil((box.conf[0] * 100)) / 100
                    cls = int(box.cls[0])
                    self.currentClass1 = classNames[cls]

                    if self.currentClass1 in ["car", "bus", "truck", "motorbike"]:
                        # Replace this with your ROI detection logic
                        cvzone.cornerRect(roi_1, (x1, y1, w, h), l=7)
                        cvzone.putTextRect(roi_1, f'{classNames[cls]} {conf}', (max(0, x1), max(35, y1)), scale=1, thickness=1)
                        self.detected_roi1 = True  # For illustration purposes, you can adjust this based on your logic
                
            # for r in results_2:
            #     boxes = r.boxes
            #     for box in boxes:
            #         x1, y1, x2, y2 = box.xyxy[0]
            #         x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            #         w, h = x2 - x1, y2 - y1
            #         conf = math.ceil((box.conf[0] * 100)) / 100
            #         cls = int(box.cls[0])
            #         self.currentClass2 = classNames[cls]
                        
            #         if self.currentClass2 in ["car", "bus", "truck", "motorbike"]:
            #             cvzone.cornerRect(roi_2, (x1, y1, w, h), l=7)
            #             cvzone.putTextRect(roi_2, f'{classNames[cls]} {conf}', (max(0, x1), max(35, y1)), scale=1, thickness=1)
            #             self.detected_roi2 = True

            #             if self.start_time_roi2 is None:
            #                 self.start_time_roi2 = time.time()

            self.notify()  # Check for notifications based on detected ROIs
            frame_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            photo = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb))
            self.video_canvas.create_image(3, 3, anchor=tk.NW, image=photo)
            self.video_canvas.image = photo

    def notify(self):
        current_time = time.time()

            # Illegal Parking Notification
        if self.detected_roi1 and (current_time - self.start_time > self.notification_interval) and not self.notification_sent:
            messagebox.showwarning("Camera 3", "  vehicle detected in restricted area \n Parked illegal!")
            self.video_player_instance.add_notif("Camera 3", " Vehicle detected in restricted area \n Parked illegal!")
            self.notification_sent = True
            self.start_time = current_time  # Reset the timer
            self.last_notification_time = current_time
        elif self.notification_sent and (current_time - self.last_notification_time > 20):
            # Reset the notification flag after 20 seconds
            self.notification_sent = False

            # Double Parking Notification
        # if self.detected_roi1 and self.detected_roi2 and (current_time - self.last_detection_time > self.double_notify):
        #         # Check if the vehicle in detected_roi2 has stayed for at least 20 seconds
        #     if (current_time - self.start_time_roi2) > 20:
        #         messagebox.showwarning("Camera 3", " Two vehicle detecteted in restricted area \n Double Parking!")
                # self.video_player_instance.add_notif("Camera 3", " Two vehicle detecteted in restricted area \n Double Parking!")
        #         self.last_detection_time = current_time
        #         self.notification_sent = False  # Reset the flag after sending the notification
        #         self.start_time = current_time 
            
class VideoProcessor4:
    def __init__(self, root, video_player_instance):
        self.root = root
        self.root.title("Camera 3")
        self.root.config(bg="darkgray")
        self.root.geometry("1200x700")
        self.video_player_instance = video_player_instance
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 1200  
        window_height = 700
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        # self.root.state('zoomed')
        self.video_canvas = tk.Canvas(self.root, width=1200, height=700, bg="white", bd=5)
        self.video_canvas.pack()

        # self.capture = cv2.VideoCapture('rtsp://egopark1:egopark1234@192.168.1.107:554/stream1')
        self.capture = cv2.VideoCapture(0)
        self.model = YOLO("../yolo-weights/yolov8n.pt")  

        self.notification_sent = False
        self.last_detection_time = time.time()
        self.start_time = time.time()
        self.start_time_roi2 = None
        self.notification_interval = 21 
        self.double_notify = 50
        self.detected_roi1 = False
        self.detected_roi2 = False

        thread1 = threading.Thread(target=self.process_video)
        thread1.start()

    def process_video(self):
        classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
                        "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
                        "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
                        "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
                        "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
                        "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
                        "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "potted plant", "bed",
                        "dining table", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
                        "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
                        "teddy bear", "hair drier", "toothbrush"]

        while True:
            success, img = self.capture.read()
            if not success:
                break

            img = cv2.resize(img, (1200, 700))
                
            results_1 = self.model(img, stream=True)

            for r in results_1:
                boxes = r.boxes

                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    w, h = x2 - x1, y2 - y1
                    conf = math.ceil((box.conf[0] * 100)) / 100
                    cls = int(box.cls[0])
                    self.currentClass1 = classNames[cls]

                    if self.currentClass1 in ["car", "bus", "truck", "motorbike"]:
                        # Replace this with your ROI detection logic
                        cvzone.cornerRect(img, (x1, y1, w, h), l=7)
                        cvzone.putTextRect(img, f'{classNames[cls]} {conf}', (max(0, x1), max(35, y1)), scale=1, thickness=1)

            frame_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            photo = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb))
            self.video_canvas.create_image(3, 3, anchor=tk.NW, image=photo)
            self.video_canvas.image = photo

if __name__ == "__main__":
    root = tk.Tk()
    processor = Video_Player(root)
    # app = App(root, video_player)
    root.mainloop()
