import os
from pathlib import Path

os.environ['YOLO_CONFIG_DIR'] = str(Path.cwd())

from ultralytics import YOLO

os.environ["WANDB_DISABLED"] = "true"

project = 'blood_vessel_segmentation'

model = YOLO('yolov8n-seg.pt')

yaml_path = 'yolo_dataset.yaml'

name = 'train_50_epochs_1600_batch_9'

results = model.train(data=yaml_path,
                      project=project,
                      name=name,
                      epochs=50,
                      patience=5, 
                      batch=9,
                      imgsz=1600,
                      cache=True
                     )

model.export(imgsz=1600)