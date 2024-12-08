import os
import cv2
import time
from flask import Flask, Response
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# app = Flask(__name__)

# Folder to monitor for new images
IMAGE_FOLDER = "images"
FPS = 30

# Global list to store image paths (dynamically updated)
image_paths = []

# This function handles new image files added to the folder
class ImageHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        # Check for new image files added
        new_images = [f for f in os.listdir(IMAGE_FOLDER) if f.endswith('.jpg')]
        new_images.sort()  # Sort to keep the images in sequence
        image_paths.extend([os.path.join(IMAGE_FOLDER, img) for img in new_images])

# Set up a watchdog observer to monitor the image folder
def start_watching():
    event_handler = ImageHandler()
    observer = Observer()
    observer.schedule(event_handler, IMAGE_FOLDER, recursive=False)
    observer.start()

# Video stream generator
def generate_video():
    while True:
        if image_paths:
            # Get the next image to stream
            image_path = image_paths.pop(0)
            img = cv2.imread(image_path)
            
            # Encode the image to jpeg format
            _, buffer = cv2.imencode('.jpg', img)
            frame = buffer.tobytes()
            
            # Stream the frame as MJPEG
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            # Remove the processed image (optional)
            os.remove(image_path)

# @app.route('/video')
# def video_feed():
#     return Response(generate_video(), mimetype='multipart/x-mixed-replace; boundary=frame')

# if __name__ == "__main__":
#     # Start watching the image folder in a separate thread
#     start_watching()
    
#     # Run the Flask app
#     app.run(debug=True, port=5000)
