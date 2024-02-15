import tkinter as tk
from typing import Any
from video import VideoHandler
from textualizer import ContentDescriber

def setup_main_window() -> tk.Tk:
    """Initializes and returns the main Tkinter window."""
    root = tk.Tk()
    root.title("Webcam Streaming")
    return root

def setup_user_input(root: tk.Tk) -> tk.Entry:
    """Sets up a text entry for user input in the Tkinter window."""
    user_input = tk.Entry(root, width=50)
    user_input.pack()
    return user_input

def setup_canvas(root: tk.Tk, width: int = 640, height: int = 480) -> tk.Canvas:
    """Sets up a canvas for video streaming in the Tkinter window."""
    canvas = tk.Canvas(root, width=width, height=height)
    canvas.pack()
    return canvas

def create_button(root: tk.Tk, text: str, width: int, command: Any) -> None:
    """Creates and packs a button into the Tkinter window."""
    button = tk.Button(root, text=text, width=width, command=command)
    button.pack(anchor=tk.CENTER, expand=True)

def main() -> None:
    """Main function to set up the GUI and handlers."""
    root = setup_main_window()
    user_input = setup_user_input(root)
    canvas = setup_canvas(root)

    video_handler = VideoHandler(root, canvas)
    content_describer = ContentDescriber(root, user_input, video_handler)

    video_handler.content_describer = content_describer  

    create_button(root, "Stop", 50, video_handler.stop_video)
    create_button(root, "Describe the frame", 50, content_describer.threaded_describe_content)

    message_label = tk.Label(root, textvariable=content_describer.message_var, wraplength=500)
    message_label.pack()

    video_handler.start_stream()
    root.mainloop()

if __name__ == "__main__":
    main()