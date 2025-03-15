from ultralytics import YOLO

# Load a model
model = YOLO("yolov8n.pt")


# Perform object detection on an image
results = model("path/to/image.jpg")
results[0].show()
