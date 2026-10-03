# 📱 scrcpy-v4l2-cam

<div align="center">

[![Linux](https://img.shields.io/badge/Linux-v4l2loopback-FCC624?style=for-the-badge&logo=linux&logoColor=black)](https://github.com/umlaeute/v4l2loopback)
[![scrcpy](https://img.shields.io/badge/scrcpy-2.0+-FF8C00?style=for-the-badge)](https://github.com/Genymobile/scrcpy)
[![ADB](https://img.shields.io/badge/ADB-Android%2012+-3DDC84?style=for-the-badge&logo=android&logoColor=white)](https://developer.android.com)
[![OpenCV](https://img.shields.io/badge/OpenCV-Compatible-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

<p align="center">
  <strong>Zero-latency, 60 FPS Android webcam streamer for Linux. Pipes raw sensor video over USB directly into a <code>v4l2loopback</code> node for OpenCV, FaceSwap, LivePortrait, Zoom, and OBS.</strong>
</p>

</div>

---

## 📌 Why this exists

Third-party webcam solutions (DroidCam, Iriun, Camo) have major drawbacks on Linux:
- Proprietary closed-source kernel modules or background daemons.
- Compression artifacts, watermarks, or paid paywalls for >720p or 60fps.
- Incompatible pixel formats when read by OpenCV (`cv2.VideoCapture`).

`scrcpy-v4l2-cam` leverages `scrcpy >= 2.0`'s native camera streaming directly to a `/dev/video*` loopback node over USB ADB:
- **Zero software lag** (hardware H.264/H.265 decoding).
- **No Android app installation required** (streams via native Android `Camera2` subsystem).
- **Supports full sensor resolution** (1080p, 4K, 60 FPS depending on phone hardware).

---

## 🛠 Prerequisites

Install `scrcpy` and `android-tools`:

```bash
# Arch / CachyOS / Manjaro
sudo pacman -S --needed scrcpy android-tools v4l2loopback-dkms

# Debian / Ubuntu
sudo apt install scrcpy adb v4l2loopback-dkms
```

---

## 🚀 Quick Setup

### 1. Configure the Loopback Device

Load the kernel module with device nodes:

```bash
sudo modprobe v4l2loopback devices=2 video_nr=2,3 card_label="AI Virtual Cam","Android Cam" exclusive_caps=1,1
```

*(To make persistent across reboots, add to `/etc/modules-load.d/v4l2loopback.conf`)*

### 2. Enable USB Debugging

On your Android phone:
1. *Settings -> About Phone* -> Tap **Build Number** 7 times.
2. *Developer Options* -> Enable **USB Debugging**.
3. Connect via USB and tap **Always Allow**.

### 3. Launch `camdroid`

```bash
git clone https://github.com/ProgramaGrueso/scrcpy-v4l2-cam.git
cd scrcpy-v4l2-cam

# Stream back camera at 1080p @ 30fps to /dev/video3
./bin/camdroid

# Or customize sensor, resolution and frame rate:
./bin/camdroid --facing front --size 1280x720 --fps 60 --device /dev/video3
```

---

## 🔬 Benchmark & OpenCV Integration

Verify latency and throughput with OpenCV:

```bash
python tests/test_stream.py --device /dev/video3 --frames 150
```

Example consumption in Python:

```python
import cv2

cap = cv2.VideoCapture("/dev/video3")
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    # Feed into your real-time AI pipeline (FaceSwap, LivePortrait, YOLO)
```

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.
