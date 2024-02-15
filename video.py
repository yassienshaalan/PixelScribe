import cv2
import threading
from PIL import Image, ImageTk
import tkinter as tk
import logging
from textualizer import ContentDescriber
import time 

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class VideoHandler:
    def __init__(self, root: tk.Tk, canvas: tk.Canvas) -> None:
        """Initialize the video stream handler with the root Tkinter object and a canvas for display."""
        self.root = root
        self.canvas = canvas
        self.cap = cv2.VideoCapture(0)  # Start video capture on the default camera
        self.photo: ImageTk.PhotoImage | None = None  # Placeholder for the current photo image
        self.current_frame: cv2.Mat | None = None  # Placeholder for the current frame
        self.content_describer = None  # Reference to ContentDescriber
        self.shutdown_flag = threading.Event()  # Shutdown flag

    def video_stream(self) -> None:
        """Continuously capture frames from the webcam and display them on the Tkinter canvas."""
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                logging.info("Frame captured successfully.")
                self.current_frame = frame
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(cv2image)
                self.photo = ImageTk.PhotoImage(image=img)
                self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
                self.root.update()
            else:
                logging.warning("Failed to capture frame.")
                print("Failed to capture frame.")

    def start_stream(self) -> None:
        """Start the video stream in a separate thread."""
        logging.info("Starting video stream...")
        print("Starting video stream...")
        thread = threading.Thread(target=self.video_stream)
        thread.daemon = True  # Daemonize thread
        thread.start()

    def stop_video(self) -> None:
        """Stop the video capture and close the Tkinter window."""
        print("Initiating shutdown...")
        self.shutdown_flag.set()  # Signal all threads to shutdown

        # Wait for content description tasks to complete
        while self.content_describer is not None and self.content_describer.active_tasks > 0:
            print("Waiting for content description tasks to complete...")
            time.sleep(1)  # Wait a bit before checking again

        # Close video capture
        if self.cap.isOpened():
            self.cap.release()
        
        # Destroy the Tkinter window
        self.root.destroy()

    def get_current_frame(self) -> cv2.Mat | None:
        """Return the current frame captured by the webcam."""
        return self.current_frame