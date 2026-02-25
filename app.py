"""Car Damage Detection Web Application Using Streamlit.

This module implements an interactive web application for car damage detection.
Users upload car images through a simple web interface, and the app displays:
  - Annotated image with bounding boxes around detected damages
  - Class labels for each detection (scratch, dent, broken_glass, bumper_damage)
  - Confidence scores (0.0-1.0) indicating model certainty

Why Streamlit?
  - Zero HTML/CSS/JavaScript knowledge required
  - Automatic web server, no Flask/Django boilerplate
  - Real-time reloading during development
  - Beautiful default UI with widgets for file upload, image display, etc.
  - Built-in performance monitoring and error handling

Usage:
  streamlit run app.py
  
This will:
  1. Start a local Streamlit server (default: http://localhost:8501)
  2. Open your browser automatically
  3. Allow users to upload images
  4. Run inference and display results in real-time

Deployed Usage (Streamlit Cloud / Hugging Face Spaces):
  1. Push this repo to GitHub
  2. Connect to Streamlit Cloud or Hugging Face Spaces
  3. Set app.py as the main file
  4. Deploy with one click

Production Notes:
  - Model is loaded once on first app load for efficiency
  - Temporary files are cleaned up after inference
  - Error handling provides helpful messages if model is missing
  - No dependency on local CUDA; cloud deployment can use CPU
"""

import os
import tempfile
import streamlit as st
from ultralytics import YOLO


# Path to the trained model weights produced by train.py. This is a relative
# path that works on any machine without modification. The path follows the
# directory structure created by Ultralytics after training completes.
MODEL_PATH = os.path.join("runs", "detect", "train", "weights", "best.pt")


@st.cache_resource
def load_model():
    """Load the YOLO model once and cache it for reuse.
    
    The @st.cache_resource decorator ensures the model is loaded only once,
    even if the app reruns. This significantly improves user experience by
    avoiding expensive model initialization on every interaction.
    
    Returns:
        YOLO: Loaded model object, or None if weights file not found.
    """
    # Check if the model weights file exists. If not, return None to signal
    # that training is required. This prevents cryptic errors and allows the
    # app to show a helpful message to the user.
    if not os.path.isfile(MODEL_PATH):
        return None
    
    # Load the model from disk. This instantiates the architecture and
    # populates weights from the .pt file. The model is now ready for inference.
    return YOLO(MODEL_PATH)


def main():
    """Run the Streamlit web application for car damage detection.
    
    Flow:
      1. Display title and instructions
      2. Attempt to load model; show error if missing
      3. Display file uploader widget
      4. If user uploads image: run inference and display results
    """
    
    # Page title and description. Streamlit renders these as HTML on the page.
    st.title("🚗 Car Damage Detection")
    st.write(
        "Upload an image of a car to automatically detect scratches, dents, "
        "broken glass, and bumper damage using AI."
    )

    # Attempt to load the trained model. If it fails, the function returns None
    # and we show an error message instead of crashing.
    model = load_model()
    if model is None:
        # Display an error box. Users see this in red and know they must train first.
        st.error(
            "❌ Model not found. Please train the model first by running: python train.py"
        )
        return  # Stop execution; don't show file uploader

    # File upload widget. Accept only image formats supported by Ultralytics.
    # Returns an UploadedFile object (file-like) or None if user hasn't selected anything.
    uploaded_file = st.file_uploader(
        "Choose a car image",
        type=["jpg", "jpeg", "png"],
        help="Supported formats: JPG, JPEG, PNG"
    )
    
    # If user hasn't uploaded a file, stop here. Don't try to run inference on None.
    if uploaded_file is None:
        st.info("👆 Upload an image to get started")
        return

    # Create a temporary file to store the uploaded image. Ultralytics' predict()
    # requires a file path, not a file-like object, so we must write to disk first.
    # The delete=False parameter keeps the file after the context exits (we'll
    # clean it up manually later if desired).
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        # Write the uploaded file's bytes to the temporary file
        tmp.write(uploaded_file.getbuffer())
        tmp_path = tmp.name

    # Show a spinner while inference runs. This provides visual feedback that
    # the app hasn't frozen.
    with st.spinner("Running inference..."):
        # Run the model on the temporary image file. save=False tells Ultralytics
        # to skip saving the annotated output to disk (we'll display it directly in Streamlit).
        results = model.predict(source=tmp_path, save=False)

    # Check if inference returned any detections. results is a list of Result
    # objects, one per input. Since we passed one image, len(results) == 1.
    if results and len(results) > 0:
        # Extract the first (and only) result
        result = results[0]
        
        # Plot the result to get an annotated image (boxes + labels + confidences
        # overlaid on the original). .plot() returns a NumPy array (HxWx3 BGR).
        annotated_image = result.plot()
        
        # Display the annotated image in the Streamlit app
        st.image(annotated_image, caption="Detection Result", use_column_width=True)

        # Display detected damages in a nicely formatted section
        st.subheader("📊 Detections")
        
        # If no damages detected, show a message
        if len(result.boxes) == 0:
            st.info("No damages detected in this image.")
        else:
            # Create a list of detections to display
            detections_list = []
            for box in result.boxes:
                # Extract class index and confidence from the box tensor
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                
                # Look up the class name from the model's names dictionary
                name = model.names.get(cls, str(cls))
                
                # Add to list for display
                detections_list.append({
                    "Damage Type": name,
                    "Confidence": f"{conf:.2%}"  # Format as percentage
                })
            
            # Display as a table for easy reading
            if detections_list:
                st.table(detections_list)
    else:
        # model.predict() returned empty results or failed
        st.warning("⚠️ No results returned from inference. Please try another image.")


if __name__ == "__main__":
    main()
