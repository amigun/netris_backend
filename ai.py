from ultralytics import YOLO

model = YOLO('models/e100.pt')


def prediction(frame):
    return model(frame, save=False, imgsz=320, conf=0.15)
