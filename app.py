import tkinter as tk
from typing import Any
from video import VideoHandler
from textualizer import ContentDescriber
from tkinter import scrolledtext 
from queue import Queue
# Initialize a global queue for UI update messages at the top of your script
message_queue = Queue()

def setup_main_window() -> tk.Tk:
    """Initializes and returns the main Tkinter window."""
    root = tk.Tk()
    root.title("Webcam Streaming")
    return root

def setup_user_input(root: tk.Tk) -> tk.Entry:
    """Sets up a text entry for user input in the Tkinter window with default text."""
    user_input = tk.Entry(root, width=50)
    default_text = "Describe the image and identify objects"
    user_input.insert(0, default_text)
    user_input.pack()
    # Bind the entry click event to clear the default text
    user_input.bind("<FocusIn>", lambda event: clear_default_text(event, user_input, default_text))
    return user_input

def clear_default_text(event, entry: tk.Entry, default_text: str) -> None:
    """Clears the default text in an entry widget when it gains focus for the first time."""
    if entry.get() == default_text:
        entry.delete(0, tk.END)

def setup_canvas(root: tk.Tk, width: int = 640, height: int = 480) -> tk.Canvas:
    """Sets up a canvas for video streaming in the Tkinter window."""
    canvas = tk.Canvas(root, width=width, height=height)
    canvas.pack()
    return canvas

def create_button(root: tk.Tk, text: str, width: int, command: Any) -> None:
    """Creates and packs a button into the Tkinter window."""
    button = tk.Button(root, text=text, width=width, command=command)
    button.pack(anchor=tk.CENTER, expand=True)

def process_queue():
    global message_box  # Declare message_box as global
    print("Processing the message box")
    while not message_queue.empty():
        message = message_queue.get()
        message_box.insert(tk.END, message + "\n")
        message_box.see(tk.END)
    root.after(100, process_queue)  # Reschedule itself
    
def main() -> None:
    """Main function to set up the GUI and handlers."""

    root = setup_main_window()
    user_input = setup_user_input(root)
    canvas = setup_canvas(root)

    video_handler = VideoHandler(root, canvas)
    content_describer = ContentDescriber(root, user_input, video_handler, message_queue)

    create_button(root, "Stop", 50, video_handler.stop_video)
    create_button(root, "Describe the frame", 50, content_describer.threaded_describe_content)

    message_box = tk.scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=10)
    message_box.pack(padx=10, pady=10)

    #content_describer.message_box = message_box

    video_handler.start_stream()

    # Start processing the queue
    root.after(100, process_queue)

    root.mainloop()

if __name__ == "__main__":
    main()