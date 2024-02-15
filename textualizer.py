import threading
import cv2
from PIL import Image
import io
import os
import tkinter as tk
from typing import Optional
import logging
from dotenv import load_dotenv
import google.generativeai as genai
import google.ai.generativelanguage as glm
import time 

# Load environment variables and configure logging
load_dotenv()
logging.basicConfig(level=logging.INFO)

# Configure Google API with environment variable
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-pro-vision')

class ContentDescriber:
    def __init__(self, root: tk.Tk, user_input: tk.Entry, video_handler: 'VideoStreamHandler', message_queue:'Message Queue') -> None:
        self.root = root
        self.user_input = user_input
        self.video_handler = video_handler
        self.message_var = tk.StringVar()
        self.active_tasks = 0  # Track active description tasks
        self.message_queue = message_queue  # Store the queue as an instance variable

    def describe_content(self) -> None:
        print("Started to describe_content")
        #while not self.video_handler.shutdown_flag.is_set():  # Check if shutdown is initiated
        current_frame = self.video_handler.get_current_frame()
        if current_frame is not None:
            print("Got a frame")
            pil_image = Image.fromarray(cv2.cvtColor(current_frame, cv2.COLOR_BGR2RGB))
            img_byte_arr = io.BytesIO()
            pil_image.save(img_byte_arr, format='JPEG')
            print("Saving the image")
            blob = glm.Blob(mime_type='image/jpeg', data=img_byte_arr.getvalue())
            print("Created the blob")
            user_request = "" #self.user_input.get()
            print(user_request)
            print("Sending image and request to Google API...")
            logging.info("Sending image and request to Google API...")
            response = model.generate_content([user_request, blob], stream=True)
            for chunk in response:
                if hasattr(chunk, 'parts'):
                    # Iterate over each part in the chunk
                    for part in chunk.parts:
                        print(part.text)  
                        self.message_queue.put(part.text)  
                else:
                    print("Response format not recognized")
            
            print("Finished Description :)")
        else:
            print("No frame")
            self.root.after(0, self.update_message, "No frame available")
        # Add a small delay to prevent hogging the CPU and allow checking the shutdown flag
        time.sleep(0.1)

    def threaded_describe_content(self) -> None:
        self.active_tasks += 1  # Increment active tasks
        describe_thread = threading.Thread(target=self.describe_content)
        describe_thread.start()
        describe_thread.join()  # Ensure the main thread waits for the description thread to finish
        self.active_tasks -= 1  # Decrement active tasks when done

    def update_message(self, new_text: str) -> None:
        current_text = self.message_var.get()
        updated_text = f"{current_text}{new_text}\n"
        self.message_var.set(updated_text)

        logging.info(f"Updated message: {new_text}")
        print(f"Updated message: {new_text}")
