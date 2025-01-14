import json
from pathlib import Path
import random

data_dir = Path.cwd() / "data"
image_dir = data_dir / "image_data"
annotation_dir = data_dir / "annotation" / "ucf101_01.json"

labels = ["noslip", "forward", "backward"]
database = {}

random.seed(10)
for class_folder in image_dir.iterdir():
    if not class_folder.is_dir():
        continue
    video_folders = [folder for folder in class_folder.iterdir() if folder.is_dir()]
    random.shuffle(video_folders)
    split = int(len(video_folders) * 0.8)
    training = video_folders[:split]
    validation = video_folders[split:]
    for folder in training:
        database[folder.name] = {
            "subset": "training",
            "annotations": {"label": class_folder.name},
        }
    for folder in validation:
        database[folder.name] = {
            "subset": "validation",
            "annotations": {"label": class_folder.name},
        }
    for folder in video_folders:
        n_frames = len(list(folder.glob("*.png")))
        with open(folder / "n_frames", "w") as fp:
            fp.write(str(n_frames))


annotation = {"labels": labels, "database": database}


with open(annotation_dir, "w") as fp:
    json.dump(annotation, fp)
