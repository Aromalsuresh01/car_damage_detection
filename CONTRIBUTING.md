# Contributing to Car Damage Detection

Thank you for your interest in contributing! This guide explains how to get started.

## 🤝 Types of Contributions

We welcome:

- **Bug Reports**: Found an issue? Open a GitHub Issue with details
- **Feature Requests**: Have an idea? Describe it in a GitHub Discussion
- **Documentation**: Improve README, comments, docstrings
- **Code**: Fix bugs, add features, improve performance
- **Data**: Contribute labeled car damage images
- **Testing**: Report edge cases or platform-specific issues

---

## 🚀 Getting Started

### 1. Fork the Repository

Visit https://github.com/YOUR_USERNAME/car-damage-detection and click "Fork"

### 2. Clone Your Fork

```bash
git clone https://github.com/YOUR_USERNAME/car-damage-detection.git
cd car-damage-detection
git remote add upstream https://github.com/YOUR_USERNAME/car-damage-detection.git
```

### 3. Create a Feature Branch

```bash
git checkout -b feature/my-feature-name
```

Use descriptive names: `feature/improved-accuracy`, `fix/gpu-detection`, etc.

### 4. Set Up Development Environment

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 5. Make Your Changes

- Edit code with clear commit messages
- Follow the code style (see below)
- Add tests if applicable
- Update documentation

### 6. Test Your Changes

```bash
# Quick sanity check
python train.py --epochs 1 --device cpu

# Test web app
streamlit run app.py

# Test inference
python predict.py --source dataset/test/images/000001.jpg
```

### 7. Commit and Push

```bash
git add .
git commit -m "Add feature: description of change"
git push origin feature/my-feature-name
```

### 8. Create a Pull Request

Visit your fork on GitHub and click "Compare & pull request"

Provide:
- Clear title and description
- Reference related issues (#123)
- Explain *why* the change is needed
- Show testing results if applicable

---

## 📝 Code Style Guidelines

### Python

- **PEP 8 compliance**: Use `black` or `autopep8` for formatting
- **Line length**: Max 88 characters (black default)
- **Comments**: Explain *why*, not *what*
- **Docstrings**: Include for all functions/classes

```python
def detect_damage(image_path: str, confidence: float = 0.5) -> dict:
    """Detect car damage in an image.
    
    This function loads the trained YOLOv8 model and runs inference
    on the provided image, filtering results by confidence threshold.
    
    Args:
        image_path: Path to input image (relative or absolute)
        confidence: Confidence threshold (0.0-1.0). Default: 0.5
    
    Returns:
        Dictionary with keys:
          - 'boxes': List of bounding boxes [x1, y1, x2, y2]
          - 'classes': List of class indices (0-3)
          - 'confidences': List of confidence scores (0.0-1.0)
    
    Raises:
        FileNotFoundError: If image or model weights not found
        ValueError: If confidence not in range [0.0, 1.0]
    """
    pass
```

### Git Commits

- **Size**: Small, focused commits (1 logical change per commit)
- **Messages**: Present tense, descriptive

```
✓ Good:
  feat: add confidence threshold parameter to inference
  fix: resolve GPU memory leak in model loading
  docs: update training time estimates

✗ Bad:
  fixed stuff
  WIP
  asdfghjkl
```

---

## 🧪 Testing

### Before Submitting

Test on multiple configurations:

```bash
# Test on CPU
python train.py --epochs 1 --device cpu

# Test on GPU (if available)
python train.py --epochs 1 --device 0

# Test inference
python predict.py --source dataset/test/images/000001.jpg

# Test web app
streamlit run app.py
# Upload test image, verify detection works
```

### Adding Unit Tests (Optional)

```python
# tests/test_inference.py
import pytest
from app import load_model

def test_model_loads():
    """Verify model loads successfully."""
    model = load_model()
    assert model is not None

def test_prediction():
    """Verify inference produces correct output format."""
    model = load_model()
    results = model.predict("dataset/test/images/000001.jpg")
    assert len(results) > 0
    assert hasattr(results[0], 'boxes')
```

Run tests:
```bash
pip install pytest
pytest tests/
```

---

## 📖 Documentation

When adding features, update:

1. **Docstrings**: Function/class documentation
2. **README.md**: User-facing features
3. **SETUP.md**: Setup/installation changes
4. **Comments**: Complex logic in code

Example:
```python
def calculate_mAP(predictions: list, ground_truth: list) -> float:
    """Calculate mean Average Precision (mAP) metric.
    
    Mean Average Precision is the standard metric for object detection models.
    It averages precision across recall levels (0-100%) and across all classes.
    
    See: https://arxiv.org/abs/1612.03144 (COCO paper)
    
    Args:
        predictions: List of predicted boxes with confidence scores
        ground_truth: List of ground truth annotations
    
    Returns:
        mAP score in range [0.0, 1.0]. Higher is better.
    """
    pass
```

---

## 🐛 Reporting Bugs

Create a GitHub Issue with:

1. **Title**: Clear, specific summary
2. **Environment**:
   ```
   - Python: 3.12.1
   - OS: Windows 11
   - GPU: RTX 3050 Ti
   - PyTorch: 2.10.0+cu130
   ```
3. **Steps to Reproduce**:
   ```
   1. Run: python train.py --epochs 1
   2. Observe: [error message]
   ```
4. **Expected Behavior**: What should happen
5. **Actual Behavior**: What actually happens
6. **Error Traces**: Full stack traces if applicable

---

## ✨ Feature Requests

Create a GitHub Discussion with:

1. **Title**: Clear feature description
2. **Motivation**: Why is this needed?
3. **Proposed Solution**: How would it work?
4. **Alternatives Considered**: Other approaches?

Example:
```
Title: Add confidence threshold adjustment in web UI

Motivation:
Currently confidence threshold is hardcoded. Users want to 
adjust it interactively in the Streamlit app.

Proposed Solution:
Add st.slider("Confidence Threshold", 0.0, 1.0, 0.5) in app.py
Pass value to model.predict(conf=threshold)

Alternative:
Command-line parameter (less user-friendly)
```

---

## 🔄 Code Review Process

1. **Automated Checks**:
   - Python syntax validation
   - Import resolution
   - Code format (if linting is set up)

2. **Manual Review**:
   - Code quality and clarity
   - Documentation completeness
   - Test coverage
   - Performance implications

3. **Feedback Loop**:
   - Reviewers comment on PR
   - Author makes requested changes
   - Reviewers approve
   - Merge to main branch

---

## 🎯 Roadmap

Areas we're actively seeking contributions:

- [ ] Model improvements (better accuracy for rare classes like broken_glass)
- [ ] Performance optimization (ONNX export, TensorRT inference)
- [ ] Deployment guides (AWS, Azure, GCP, Kubernetes)
- [ ] Data collection tools (annotation helpers, dataset utilities)
- [ ] Monitoring (model performance tracking, data drift detection)
- [ ] Multi-language documentation

---

## ❓ Questions?

- Check [README.md](README.md) and [SETUP.md](SETUP.md) first
- Open a GitHub Discussion
- Email: your.email@example.com

---

**Thank you for contributing! Happy coding! 🚗✨**
