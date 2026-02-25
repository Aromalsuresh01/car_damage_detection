"""Car Damage Detection Training Script Using YOLOv8.

This module implements the training pipeline for detecting car damage using
Ultralytics YOLOv8 (nano variant). The script loads a pre-trained YOLOv8n
model and performs transfer learning (fine-tuning) on a custom car damage
dataset defined in data.yaml.

Why pre-trained weights?
  - Transfer learning significantly reduces training time and improves
    accuracy on smaller datasets (our dataset has ~6800 training images)
  - The model already understands basic object detection features from
    training on COCO (1M+ images), so it needs fewer epochs to converge

Usage:
  # Train for 1 epoch on first CUDA GPU (quick test)
  python train.py --epochs 1 --device 0

  # Train for 50 epochs (production model)
  python train.py --epochs 50 --device 0

  # Train on CPU (slower, for debugging without GPU)
  python train.py --epochs 50 --device cpu

Training Flow:
  1. Initialize YOLOv8n with pre-trained COCO weights
  2. Load dataset from data.yaml (train/valid/test splits)
  3. Forward pass: convert images through model backbone, neck, and head
  4. Loss computation: combine box_loss, cls_loss, and dfl_loss
  5. Backward propagation: compute gradients via PyTorch autograd
  6. Optimizer step: SGD/Adam updates weights to minimize loss
  7. Validation: evaluate mAP50 and mAP50-95 on validation set
  8. Checkpointing: save best model when validation mAP improves

Outputs:
  - Best model weights:    runs/detect/train/weights/best.pt
  - Last epoch weights:    runs/detect/train/weights/last.pt
  - Training metrics:      runs/detect/train/results.csv
  - Validation plots:      runs/detect/train/*.jpg
  - Hyperparameter log:    runs/detect/train/args.yaml
"""

import argparse
from ultralytics import YOLO


def parse_args():
    """Parse and return command-line arguments for training configuration.
    
    Returns:
        argparse.Namespace: Parsed arguments containing:
          - epochs (int):  number of training epochs (default 1 for quick tests)
          - device (str):  compute device ('0'-'7' for GPU, 'cuda', or 'cpu')
    """
    parser = argparse.ArgumentParser(description="Train YOLOv8 on car damage data.")
    parser.add_argument(
        "--epochs",
        type=int,
        default=1,
        help="Number of epochs to run (minimal by default for quick tests).",
    )
    parser.add_argument(
        "--device",
        type=str,
        default="0",
        help="Device to train on: '0'-'7' for GPU, 'cuda', or 'cpu'.",
    )
    return parser.parse_args()


def main():
    """Main training function. Loads pre-trained YOLOv8n and begins training."""
    
    # Parse CLI arguments (epochs, device)
    args = parse_args()

    # Load the YOLOv8 nano model. The 'n' variant is the smallest, fastest
    # version suitable for rapid experiments and edge deployment. It was already
    # trained on COCO (Common Objects in Context - 1M+ images), so it has
    # learned generic object detection features. We will fine-tune it on our
    # car damage dataset instead of training from scratch.
    model = YOLO("yolov8n.pt")

    # Begin training the model using official Ultralytics API. The train()
    # method returns after all epochs complete. Parameters explained:
    #
    #   data (str): Relative path to dataset configuration YAML file.
    #     Specifies train/val/test image directories and class names.
    #
    #   epochs (int): Number of complete passes over the training dataset.
    #     User-controlled via --epochs CLI argument. Each epoch involves:
    #       1. Forward pass: images through model to get predictions
    #       2. Loss computation: compare predictions to ground truth
    #       3. Backward pass: compute gradients of loss w.r.t. weights
    #       4. Optimizer step: update weights to minimize loss
    #       5. Validation: evaluate model on held-out validation set
    #
    #   imgsz (int): Model input image size in pixels (square). YOLOv8 resizes
    #     all training/validation images to 640x640 for consistency. Larger
    #     sizes improve accuracy but increase memory and compute time.
    #
    #   batch (int): Batch size for training. Value 0 tells Ultralytics to
    #     automatically select the largest batch size that fits in GPU memory.
    #     This maximizes GPU utilization without manual tuning. Batching allows
    #     more efficient gradient computation and more stable loss estimates.
    #
    #   device (str): Which compute device to use. User passes via --device:
    #       '0' = first CUDA GPU (if available)
    #       'cuda' = any available CUDA device (automatic selection)
    #       'cpu' = CPU (slow, used for debugging or headless environments)
    #     Ultralytics automatically falls back to CPU if CUDA unavailable.
    #
    # The model.train() call internally:
    #   - Loads data from dataset directories pointing at data.yaml
    #   - Creates a DataLoader for efficient batching and augmentation
    #   - Sets up loss functions (CIoU for boxes, CrossEntropyLoss for classes)
    #   - Initializes the optimizer (SGD with momentum by default)
    #   - Runs the training loop: forward, loss, backward, step for each batch
    #   - Evaluates on validation set every epoch
    #   - Saves best model checkpoint when validation mAP improves
    #   - Logs metrics to console and results.csv for visualization
    #
    # Output locations:
    #   runs/detect/train/weights/best.pt  <- best model on validation set
    #   runs/detect/train/weights/last.pt  <- final epoch weights
    #   runs/detect/train/results.csv      <- per-epoch metrics table
    #
    model.train(
        data="data.yaml",
        epochs=args.epochs,
        imgsz=640,
        batch=0,  # automatic batch size selection for max GPU utilization
        device=args.device,
    )


if __name__ == "__main__":
    main()
