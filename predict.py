"""Car Damage Detection Inference Script Using YOLOv8.

This module performs inference (prediction) on images and videos using a
trained YOLOv8 model. It loads the best weights saved during training and
runs real-time object detection to identify car damage types.

Supported damage classes:
  - scratch:      Small surface scratches on the vehicle
  - dent:         Indentations or deformations in bodywork
  - broken_glass: Cracked or shattered windows/lights
  - bumper_damage: Damage to front/rear bumpers or covers

Usage:
  # Detect damage in a single image
  python predict.py --source path/to/car.jpg

  # Detect damage in a video file
  python predict.py --source path/to/video.mp4

  # Detect damage in all images in a directory
  python predict.py --source path/to/images/

  # Real-time detection from webcam (0 = default camera)
  python predict.py --source 0

Output:
  - Annotated image/video with bounding boxes saved to runs/detect/predict/
  - Console output listing detected classes and confidence scores (0.0-1.0)
  
Inference Flow:
  1. Load pre-trained model weights from runs/detect/train/weights/best.pt
  2. Read source image/video and resize to model input size (640x640)
  3. Forward pass: image through model backbone, neck, and head
  4. Post-process: filter detections by confidence, apply NMS (non-max suppression)
  5. Annotate: draw bounding boxes, class labels, and confidence on output
  6. Save: write annotated image/video to disk
  7. Print: display detected class names and confidence values to console

About confidence scores:
  - Range: 0.0 (uncertain) to 1.0 (confident)
  - Typical production threshold: 0.5 or higher
  - Lower threshold = more detections (more false positives)
  - Higher threshold = fewer detections (more false negatives)
"""

import argparse
import os
from ultralytics import YOLO


def parse_args():
    parser = argparse.ArgumentParser(description="Run car damage detection.")
    parser.add_argument(
        "--source",
        type=str,
        required=True,
        help="Path to input image or video file",
    )
    return parser.parse_args()


def main():
    """Main inference function. Load model and run detection on source."""
    
    args = parse_args()
    src = args.source

    # Define the path to our best trained model. This file is created
    # during training and contains the weights that achieved the highest
    # validation mAP (mean Average Precision). Using relative paths ensures
    # the code works on any machine without modification.
    weights_path = os.path.join("runs", "detect", "train", "weights", "best.pt")
    
    # Verify the model file exists before attempting to load it. The user
    # must run train.py first to generate best.pt. If it's missing, provide
    # helpful error message with the expected path.
    if not os.path.isfile(weights_path):
        raise FileNotFoundError(
            f"Model weights not found at {weights_path}. Please train first with: python train.py"
        )

    # Load the trained YOLOv8 model from disk. This instantiates the model
    # architecture and populates it with saved weights. The model is now
    # ready for inference (forward pass only, no backprop needed).
    model = YOLO(weights_path)

    # Run inference on the provided source. The predict() method:
    #   1. Loads the input (image, video, or camera stream)
    #   2. Resizes to 640x640 (model input size)
    #   3. Runs forward pass through the network
    #   4. Applies post-processing: confidence filtering and NMS
    #   5. Returns Results object(s) with boxes and class predictions
    #   6. save=True writes annotated output to runs/detect/predict/
    results = model.predict(source=src, save=True)

    # Iterate through results. For image input, results is a list with
    # one element. For video input, results contains one per frame. For
    # image directories, one per image in the folder.
    for i, res in enumerate(results):
        # Display source information for clarity
        print(f"\n{'='*60}")
        print(f"Detection Result {i + 1}: {src}")
        print(f"{'='*60}")
        
        # res.boxes contains all detected bounding boxes for this result.
        # Each box holds: coordinates (xyxy format), area, confidence, class_id.
        if len(res.boxes) == 0:
            print("No damages detected in this image.")
        else:
            # Iterate through each detected box
            for box_idx, box in enumerate(res.boxes):
                # box.cls is a tensor containing the class index (0, 1, 2, or 3
                # for our 4 damage types). Extract scalar value and convert to int.
                cls = int(box.cls[0])
                
                # box.conf is a tensor containing the model's confidence that
                # this detection is correct, ranging from 0.0 to 1.0. Higher
                # values = higher confidence. Extract scalar and convert to float.
                conf = float(box.conf[0])
                
                # Look up the human-readable class name using the model's
                # names dictionary, which maps class indices to labels:
                #   0 -> 'scratch', 1 -> 'dent', 2 -> 'broken_glass',
                #   3 -> 'bumper_damage'
                name = model.names.get(cls, str(cls))
                
                # Print detection in a readable format
                print(f"  [{box_idx + 1}] {name:<16} confidence: {conf:.4f}")
        
        print(f"{'='*60}")

    # Annotated output is automatically saved by Ultralytics to:
    #   runs/detect/predict/image.jpg (or video.mp4, etc.)
    # The path is printed by Ultralytics during execution, so we don't
    # repeat it here. Users can find their results in that directory.


if __name__ == "__main__":
    main()
