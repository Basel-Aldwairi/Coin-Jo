# Jordanian Coin Detection & Sorting (Python)
### Author : Basel Al-Dwairi

This repository contains the **Python-side implementation** of a Jordanian coin detection and sorting system.  
The project integrates **computer vision, deep learning, and socket communication** to classify coin denominations and interface with embedded hardware (ESP + ESP32-CAM).

All Python code in this repository was written and maintained by me.

---

## Project Overview

The system is designed around the following workflow:

1. An **ESP** sends a trigger to the laptop.
2. The laptop requests an image from an **ESP32-CAM**.
3. The image is sent to the laptop over a socket connection.
4. A trained **CNN model** classifies the coin denomination.
5. The prediction is sent back to the ESP as an integer label for physical sorting.

The Python code handles:
- Dataset acquisition and preprocessing
- Model training and inference
- Communication with ESP and ESP32-CAM
- A Streamlit-based user interface for testing

---

## Dataset

- Original dataset sourced from **Roboflow**
- Dataset format: **COCO**
- Coins only (banknotes filtered out)
- Images cropped using bounding boxes and resized to `224×224`
- Final processed dataset uploaded separately to **Kaggle**

### Dataset Pipeline
1. Download dataset via Roboflow API
2. Parse COCO annotations
3. Crop individual coin instances
4. Resize and restructure into class-based folders
5. Save processed images for model training

---

## Model

- Architecture: **MobileNetV2 (transfer learning)**
- Framework: **TensorFlow / Keras**
- Input size: `224 × 224 × 3`
- Output classes:
  - `0.5 JD`
  - `0.25 JD`
  - `10 Piasters`
  - `5 Piasters`

### Training Details
- Base model frozen
- Global Average Pooling + Dense layers
- Optimizer: Adam
- Loss: Sparse Categorical Crossentropy
- Early stopping + checkpointing
- Final model saved as `coin_model.keras`

---

## CoinModel Interface

The `CoinModel` class provides a simple interface for inference:

- Loads the trained Keras model
- Accepts an OpenCV image
- Returns predictions as `(confidence, label)` pairs

This abstraction is used by:
- The ESP communication server
- The Streamlit user interface

---

## ESP & ESP32-CAM Communication

The laptop acts as a **central controller** using TCP sockets.

### Communication Protocol

| Step | Sender | Receiver | Description |
|------|--------|----------|-------------|
| 1    | ESP    | Laptop  | `"TAKE_PIC"` trigger |
| 2    | Laptop | ESP32-CAM | Capture command (`0x01`) |
| 3    | ESP32-CAM | Laptop | Image size + image bytes |
| 4    | Laptop | ESP | Predicted class label (int) |

- Timeouts are used to prevent blocking
- Predictions are packed using network byte order
- Designed for a local WiFi network

---

## Streamlit User Interface

A lightweight Streamlit app is included for testing and visualization:

- Upload local images or load images from URLs
- Run inference using the trained model
- Display prediction confidence
- Visualize all class probabilities as a bar chart

This interface is **independent of the ESP hardware** and is useful for debugging and demonstrations.

---

## Notes

- The embedded (ESP / ESP32-CAM) code is **not included** in this repository.
- The system assumes a stable local WiFi connection for the prototype.
- This project was developed as part of an **image processing / computer vision course**.

---