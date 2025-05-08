# Football Analysis Project

## Overview

This project implements a complete computer vision and machine learning pipeline to analyze football match videos using **YOLOv5**, **optical flow**, and **perspective transformation**. It calculates player movements, assigns teams based on jersey colors, and estimates real-world distance covered.

---

## 🖼️ Project Preview

![Football Analysis Output](./path_to_image/analysis_preview.png)  
_Replace the above path with the correct image path from your repository._

---

## 🗂️ Project Structure

```
football_analysis/
├── camera_movement_estimator/
├── development_and_analysis/
├── input_videos/
├── models/
├── output_videos/
├── player_ball_assigner/
├── speed_and_distance_estimator/
├── stubs/
├── team_assigner/
├── trackers/
├── training/
├── utils/
├── view_transformer/
├── .gitignore
├── README.md
├── main.py
├── yolo_inference.py
```

### 📁 Directory & File Descriptions

- **`camera_movement_estimator/`**: Contains modules to estimate camera movement using optical flow.
- **`development_and_analysis/`**: Includes notebooks and scripts for exploratory data analysis and development.
- **`input_videos/`**: Directory for input football match videos.
- **`models/`**: Contains trained YOLOv5 models.
- **`output_videos/`**: Stores the output videos with annotations.
- **`player_ball_assigner/`**: Modules to assign ball possession to players.
- **`speed_and_distance_estimator/`**: Scripts to calculate player speed and distance covered.
- **`stubs/`**: Contains stub files for type hinting.
- **`team_assigner/`**: Modules to assign players to teams based on jersey colors.
- **`trackers/`**: Implements tracking algorithms for players and the ball.
- **`training/`**: Scripts and data for training the YOLOv5 model.
- **`utils/`**: Utility functions used across the project.
- **`view_transformer/`**: Modules to perform perspective transformation.
- **`main.py`**: The main script to run the analysis pipeline.
- **`yolo_inference.py`**: Script to perform object detection using YOLOv5.

---

## 📦 Installation

Install the required packages with:

```bash
pip install -r requirements.txt
```

Make sure you have Python 3.x and appropriate CUDA drivers for GPU acceleration.

---

## 🚀 Usage

1. **Clone the Repository**:

```bash
git clone https://github.com/AryanS-88/football_analytics
cd football_analysis
```

2. **Add Input Video**: Place your video inside **`input_videos/`**

3. **Run Analysis**:

```bash
python main.py
```

4. **View Outputs**: Annotated outputs will be stored in **`output_videos/`**

---

## 📈 Features

- Real-time detection with **YOLOv5**
- Team classification via **KMeans clustering**
- Player tracking using **optical flow**
- **Homography-based** distance estimation
- Speed and distance metrics for each player

---

## 🛣️ Roadmap

- Add multi-camera support
- Improve tracking accuracy
- Add web-based dashboard for visualizing stats

---

## 📄 License

Licensed under the **MIT License**.
