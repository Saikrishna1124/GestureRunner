# AI-Powered Gesture-Based Subway Surfer Controller

## Project Overview
This repository contains a Python application that enables **hands‑free control** of the Subway Surfers (or similar) game using head movements detected via a webcam. It leverages **OpenCV**, **MediaPipe**, and **pynput** to translate pose landmarks into keyboard arrow key presses.

## Features
- Real‑time head pose detection using MediaPipe Pose.
- Four control zones (left, right, up, down) mapped to arrow keys.
- Simple, lightweight, and runs on any Windows machine with a webcam.
- Fully self‑contained virtual environment for easy setup.

## Setup & Installation
1. **Clone / download** this repository.
2. Open a PowerShell window and navigate to the project root:
   ```powershell
   cd "C:\Users\Hp\Downloads\AI_prwered_subway_suffer_controller_Hand_Disable_person-main\AI_prwered_subway_suffer_controller_Hand_Disable_person-main"
   ```
3. **Create and activate** the virtual environment (if not already created):
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1   # PowerShell
   # or for cmd.exe: .\.venv\Scripts\activate.bat
   ```
4. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```
5. **Run the controller**:
   ```powershell
   python src\controller.py
   ```
   A webcam window will appear. Move your head left/right/up/down to control the game. Press `q` to quit.

## Project Structure
```
AI_prwered_subway_suffer_controller_Hand_Disable_person-main/
│   README.md            # This file
│   requirements.txt     # Python dependencies
│   run.bat              # Convenience batch script to start the app
│   .gitignore           # Ignored files/folders
│
├─.venv/                 # Virtual environment (generated locally)
│
└─src/
    │   __init__.py
    │   controller.py   # Main application code
```

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
