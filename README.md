# nayana.ai

A smartphone-based tele-ophthalmology AI screening system for early detection of eye diseases. Built with Raspberry Pi hardware integration, PyTorch computer vision models, and Streamlit interface.

## Overview

Nayana.ai is a 3-step screening app (Symptoms → Eye Photos → Results) that combines edge hardware, deep learning, and encrypted record-keeping for remote eye disease detection.

## Core Features

- Raspberry Pi-based image capture with Camera Module V2 + LED flash
- EfficientNet-B0 model trained on ODIR-5K dataset
- OpenCV-powered anterior eye analysis
- GradCAM heatmap visualization for interpretability
- Multilingual voice input and PDF report generation
- AES-encrypted patient records

## Tech Stack

**Hardware:** Raspberry Pi 4 (Trixie 64-bit), Pi Camera Module V2, custom LED flash circuit (330Ω resistor)

**Backend:** Flask server, Python 3.10, PyTorch, timm, OpenCV, ReportLab

**Frontend:** Streamlit

**Networking:** Ngrok (secure TCP tunneling for cross-network access)

**Telehealth:** Jitsi Meet API (in-app video consultations)

**Security:** AES encryption

**Models:**
- `eye_model_v2_best.pth` — anterior/front eye classifier (6-class: cataracts, uveitis, etc.)
- `odir_model.pth` — retinal/fundus classifier (8-class multi-label, trained on ODIR-5K)

## Project Structure

```
nayana-eye-screening/
├── capture.py              # Raspberry Pi camera trigger + HTTP transmission
├── receiver.py             # Flask server (port 5000) for receiving images
├── app.py                  # Main Streamlit UI
├── doctor_dashboard.py     # Doctor interface
├── patient_records.py      # Patient record management
├── encryption.py           # AES encryption utilities
├── database.py             # SQLite database logic
├── auth.py                 # Authentication handlers
├── chatbot_flow.py         # Chatbot integration
├── voice_input.py          # Voice input processing
├── report_generator.py     # PDF report generation
└── nayana.key              # Encryption key (DO NOT COMMIT)
```

## Prerequisites

**Raspberry Pi Setup:**
- Raspberry Pi 4 with Trixie 64-bit OS
- Pi Camera Module V2 enabled (`sudo raspi-config`)
- Python 3.7+ with `picamera2`, `requests`, `RPi.GPIO`

**Laptop/Server Setup:**
- Python 3.10+
- CUDA-capable GPU (recommended, not required)
- 4GB+ RAM

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/AnaghaBL/nayana-eye-screening.git
cd nayana-eye-screening
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Raspberry Pi Setup

SSH into your Pi and install the capture script dependencies:

```bash
pip install picamera2 requests RPi.GPIO
```

Edit `capture.py` to set your laptop's local IP:

```python
SERVER_URL = "http://<YOUR_LAPTOP_IP>:5000/upload"  # Replace with actual IP
```

### 4. Download Models

Place the trained PyTorch models in the project root:
- `eye_model_v2_best.pth`
- `odir_model.pth`

## Usage

### Running the Full Pipeline

**Step 1: Start the Image Receiver (Laptop)**

```bash
python receiver.py
```

The Flask server will listen on `http://0.0.0.0:5000`.

**Step 2: Trigger Image Capture (Raspberry Pi)**

```bash
python capture.py
```

The Pi will capture an image, flash the LED, and POST it to the receiver.

**Step 3: Launch the Streamlit App (Laptop)**

```bash
streamlit run app.py
```

Navigate to `http://localhost:8501` in your browser.

**Optional: Use Ngrok for cross-network access**

If your Pi and laptop are on different networks, expose the Flask receiver via Ngrok:

```bash
ngrok http 5000
```

Then update `SERVER_URL` in `capture.py` with the Ngrok forwarding URL.

**Optional: Doctor Dashboard**

```bash
streamlit run doctor_dashboard.py
```

Doctors can review AI heatmaps, submit diagnoses, and launch Jitsi video consultations directly from the dashboard.

## Hardware Wiring

**LED Flash Circuit:**
- GPIO Pin 17 → 330Ω resistor → Red LED (gaze focus)
- GPIO Pin 27 → 330Ω resistor → White LED (flash)
- LED cathodes → GND

**Camera Module:**
- Connect Pi Camera Module V2 to CSI port
- Enable camera in `raspi-config`

## Security Notes

- **DO NOT** commit `nayana.key` to version control
- Add `nayana.key` to `.gitignore`
- Patient data is AES-encrypted at rest

## Troubleshooting

**Pi Camera Not Detected:**
```bash
sudo raspi-config
# Interface Options → Camera → Enable
sudo reboot
```

**Connection Refused (receiver.py):**
- Check firewall settings on laptop
- Verify Pi and laptop are on same network
- Test with `curl http://<LAPTOP_IP>:5000`

**Model Loading Error:**
- Ensure PyTorch version matches training environment
- Check model file paths in `app.py`

## Team

| Name | Role |
|------|------|
| **Anagha B L** | Software Implementation: Early detection & camera integration |
| **Medha Balaji** | Hardware Integration: Pi setup, device testing & capture pipeline |
| **Khushi Agarwal** | Software Implementation: Dataset training & AI integration |
| **Nisarga Hegde** | Optical Assembly: Pi setup, device testing, capture pipeline & optical assembly |