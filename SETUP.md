# Setup Guide - Car Damage Detection

This guide walks through setup, training, and deployment step-by-step.

## Prerequisites

- **Python**: 3.10 or higher  
  Check: `python --version`
- **GPU (optional)**: NVIDIA CUDA compute capability 3.5+  
  Check: `nvidia-smi`
- **Disk Space**: ~15 GB (dataset + model + dependencies)

---

## Step 1: Clone & Environment Setup

### 1.1 Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/car-damage-detection.git
cd car-damage-detection
```

### 1.2 Create Virtual Environment

**Windows**:
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux/Mac**:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 1.3 Verify Activation

You should see `(.venv)` at the start of your terminal prompt.

---

## Step 2: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**What's installed**:
- `ultralytics`: YOLOv8 implementation
- `streamlit`: Web application
- `torch`: Deep learning framework
- `opencv-python`: Image processing
- `numpy`: Numerical computing
- `pillow`: Image handling

**Installation time**: 5-10 minutes

---

## Step 3: Verify Installation

Run this quick test:

```bash
python -c "
import torch
import ultralytics
import streamlit
import cv2
import numpy

print('✓ All imports successful!')
print(f'Python: {torch.__version__.split('/')[0]}')
print(f'PyTorch: {torch.__version__}')
print(f'CUDA available: {torch.cuda.is_available()}')
print(f'GPUs detected: {torch.cuda.device_count()}')
"
```

**Expected output**:
```
✓ All imports successful!
Python: 2.10
PyTorch: 2.10.0+cu130
CUDA available: True
GPUs detected: 1
```

---

## Step 4: Verify Dataset

Check that training data exists:

```bash
# Windows
dir dataset\train\images | find /c /v ""
dir dataset\valid\images | find /c /v ""
dir dataset\test\images | find /c /v ""

# Linux/Mac
ls -1 dataset/train/images | wc -l
ls -1 dataset/valid/images | wc -l
ls -1 dataset/test/images | wc -l
```

**Expected counts**:
- Training images: 6000+
- Validation images: 800-1000
- Test images: 300+

---

## Step 5: Train Model

### 5.1 Quick Test (1 epoch, ~2-3 minutes)

```bash
python train.py --epochs 1 --device 0
```

This verifies:
- PyTorch/CUDA setup
- Dataset loading
- Training pipeline
- Weight saving

**Expected output**:
```
Ultralytics 8.4.15 torch-2.10.0+cu130
Starting training for 1 epochs...
Epoch 1/1 |████████████| 494/494 [1min<0s, 8.2it/s]
Optimizer stripped from best.pt
Training completed in 0.018 hours
```

### 5.2 Full Training (50 epochs, ~50-60 minutes on RTX 3050 Ti)

```bash
# Run in background or new terminal
python train.py --epochs 50 --device 0
```

**Monitoring progress**:

```bash
# Check if training is running
ps aux | grep train.py  # Linux/Mac

# Monitor GPU usage (in separate terminal)
watch -n 1 nvidia-smi  # Linux/Mac
# or
nvidia-smi  # Windows (no real-time update)
```

**Expected training metrics** (after 50 epochs):
```
mAP50: 0.5-0.7
Training time: ~1 min per epoch
Final model size: 6.2 MB
```

### 5.3 Check Training Results

```bash
# List output files
ls -la runs/detect/train/weights/

# View metrics CSV
cat runs/detect/train/results.csv  # Linux/Mac
type runs\detect\train\results.csv  # Windows
```

**Expected files**:
```
runs/detect/train/
├── weights/
│   ├── best.pt       (6.2 MB) ← use this for inference
│   └── last.pt
├── results.csv       ← metrics table
├── labels.jpg        ← dataset visualization
└── args.yaml         ← hyperparameters used
```

---

## Step 6: Run Inference

### 6.1 Command-Line Inference

```bash
# Single image
python predict.py --source dataset/test/images/000001.jpg

# Video
python predict.py --source test_video.mp4

# Multiple images
python predict.py --source dataset/test/images/
```

**Expected output**:
```
============================================================
Detection Result 1: dataset/test/images/000001.jpg
============================================================
  [1] dent              confidence: 0.7234
  [2] scratch           confidence: 0.6109
  [3] bumper_damage     confidence: 0.5891
============================================================
```

Results saved to: `runs/detect/predict/`

### 6.2 View Inference Results

```bash
# Open annotated image with default viewer
# Windows:
start runs\detect\predict\000001.jpg

# Linux:
xdg-open runs/detect/predict/000001.jpg

# Mac:
open runs/detect/predict/000001.jpg
```

---

## Step 7: Launch Web App

### 7.1 Start Streamlit Server

```bash
streamlit run app.py
```

**Expected output**:
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.100:8501
```

### 7.2 Use the App

1. Browser opens automatically to http://localhost:8501
2. Click "Browse files" to upload a car image
3. App runs inference and displays:
   - Annotated image with bounding boxes
   - Detected damages and confidence scores

### 7.3 Stop Streamlit

Press `Ctrl+C` in terminal to stop the server.

---

## Step 8: Deploy to Cloud (Optional)

### 8.1 Streamlit Cloud (Free, Easiest)

**Prerequisites**:
- GitHub account
- This repo on GitHub

**Steps**:

1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Select:
   - Repository: `your-username/car-damage-detection`
   - Branch: `main`
   - File: `app.py`
5. Click "Deploy"

**Access**: `https://your-app-name.streamlit.app` (in 3-5 minutes)

### 8.2 Hugging Face Spaces

**Steps**:

1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Select "Streamlit" runtime
4. Upload files via Git or web interface
5. Spaces auto-runs Streamlit

### 8.3 Docker (Advanced)

```bash
# Build image
docker build -t car-damage-detector:latest .

# Run container
docker run -p 8501:8501 car-damage-detector:latest

# Access: http://localhost:8501
```

---

## Troubleshooting

### Issue: CUDA not detected

**Check**:
```bash
nvidia-smi
python -c "import torch; print(torch.cuda.is_available())"
```

**Fix**:
```bash
# Reinstall PyTorch with CUDA
pip uninstall torch torchvision -y
pip install torch torchvision --extra-index-url https://download.pytorch.org/whl/cu121
```

### Issue: Model weights not found

**Check**:
```bash
ls runs/detect/train/weights/best.pt
```

**Fix**: Run training first
```bash
python train.py --epochs 50 --device 0
```

### Issue: Out of Memory

**Reduce batch size** (though `batch=0` handles this):
```bash
python train.py --epochs 50 --device 0
# OR use smaller model
# Modify train.py to load yolov8s.pt instead of yolov8n.pt
```

### Issue: Streamlit won't start

```bash
# Kill existing process
pkill -f streamlit

# Start fresh
streamlit run app.py --logger.level=debug
```

### Issue: Slow inference on CPU

**Use GPU instead**:
```bash
python predict.py --source image.jpg
# (device is hardcoded but you can modify and use --device before source)
```

---

## Performance Benchmarks

### Training (50 epochs)

| GPU | Time | Memory |
|-----|------|--------|
| RTX 3050 Ti | 50 min | 3.5 GB |
| RTX 4090 | 12 min | 12 GB |
| CPU (i7) | 8-10 hrs | 8 GB |

### Inference (per image)

| Device | Speed | Throughput |
|--------|-------|-----------|
| RTX 3050 Ti | 4 ms | 250 FPS |
| RTX 4090 | 2 ms | 500 FPS |
| CPU (i7) | 80 ms | 12 FPS |

---

## Next Steps

1. **Improve Model**: Collect more data, especially for rare classes
2. **Fine-tune**: Adjust training hyperparameters in `train.py`
3. **Integrate**: Use model in production with FastAPI, Flask, etc.
4. **Monitor**: Track model performance on real-world data
5. **Retrain**: Periodically retrain with new data

---

## Getting Help

- **Documentation**: See README.md
- **GitHub Issues**: Report bugs or request features
- **Ultralytics Docs**: https://docs.ultralytics.com
- **Streamlit Docs**: https://docs.streamlit.io

---

**Happy training! 🚗✨**
