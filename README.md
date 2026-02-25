# Car Damage Detection

A production-ready system for detecting various types of damage on cars
using Ultralytics YOLOv8. The model is trained to recognize:

- scratch
- dent
- broken_glass
- bumper_damage

## 📁 Folder Structure

```
car-damage-detection/
│
├── dataset/           # contains training/validation/test images & labels (not tracked)
├── runs/              # outputs from YOLO training and prediction (ignored)
├── train.py           # training script using YOLOv8 pretrained weights
├── predict.py         # command-line inference script
├── app.py             # Streamlit web application for demo
├── data.yaml          # dataset configuration for YOLOv8
├── requirements.txt   # Python dependencies
├── README.md          # this document
└── .gitignore         # files/folders to exclude from git
```

## 🛠 Features

- Train a YOLOv8 model on a custom car damage dataset
- Inference on images or videos via CLI
- Streamlit web app for easy image upload and visualization
- Outputs include bounding boxes, class labels, and confidence scores

## 📂 Dataset Description

The repository includes a `dataset/` directory with the following layout
required by YOLOv8:

```
dataset/
├── train/   
│   ├── images/   # training images
│   └── labels/   # corresponding YOLO-format txt annotations
├── valid/   
│   ├── images/   # validation images
│   └── labels/   # validation annotations
└── test/    
    ├── images/   # optional test set images
    └── labels/   # optional test annotations
```

`data.yaml` in the project root points to these directories using relative
paths and lists the four damage class names.

## 🚀 Training Instructions

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run training script:
   ```bash
   python train.py
   ```
   Training logs and weights will be saved under `runs/detect/train/`.
   The best model is automatically stored at
   `runs/detect/train/weights/best.pt`.

## 🔍 Inference Instructions

Use the `predict.py` script on an image or video file:

```bash
python predict.py --source path/to/image.jpg
```

Results are saved by default in `runs/detect/predict/` and the CLI prints
predicted class names with confidence scores.

## 🌐 Streamlit Web App

Run the demo application with:

```bash
streamlit run app.py
```

Upload a car image and the app will display the detection results along
with listed damage types and confidence values. If the model is missing, a
message prompts you to train first.

## 📄 Example Outputs

Training results, inference images, and Streamlit screenshots will appear in
the `runs/` directory as generated during use.

## 📦 Deployment

### Local

1. `pip install -r requirements.txt`
2. `python train.py` to train the model
3. `streamlit run app.py` to start the web interface

### Optional Cloud Deployment

- **Streamlit Cloud:** push this repository to GitHub and connect it to
  Streamlit Cloud; set `app.py` as the main file.
- **Hugging Face Spaces:** similarly, create a new Space with Streamlit
  runtime and point to this repo.

## ✅ Validation Checklist

- [ ] Dataset paths in `data.yaml` are relative and correct
- [ ] Classes listed match annotation indices
- [ ] Model path `runs/detect/train/weights/best.pt` used by scripts
- [ ] All imports are valid and use real libraries
- [ ] No fake commands or libraries introduced
- [ ] Code is modular and includes explanatory comments
- [ ] Every script runs without modification once dependencies are
      installed
- [ ] `.gitignore` excludes dataset images, runs, weights, pycache, etc.

Happy training and detection! 🚗💥