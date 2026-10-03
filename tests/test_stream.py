#!/usr/bin/env python3
"""
Test script to read from the v4l2loopback camera node, measure actual FPS, and display telemetry.
"""

import argparse
import sys
import time


def main():
    parser = argparse.ArgumentParser(description="Test v4l2loopback stream with OpenCV")
    parser.add_argument("-d", "--device", default="/dev/video3", help="Device path (default: /dev/video3)")
    parser.add_argument("--frames", type=int, default=150, help="Frames to measure (default: 150)")
    args = parser.parse_args()

    try:
        import cv2
    except ImportError:
        print("[!] OpenCV is required: pip install opencv-python")
        sys.exit(1)

    print(f"[*] Opening capture node: {args.device}...")
    cap = cv2.VideoCapture(args.device)
    if not cap.isOpened():
        print(f"[!] Failed to open {args.device}. Make sure camdroid/scrcpy is actively streaming.")
        sys.exit(1)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"[✓] Stream opened: {width}x{height}")

    print(f"[*] Measuring real throughput over {args.frames} frames...")
    start_time = time.perf_counter()
    count = 0

    while count < args.frames:
        ret, frame = cap.read()
        if not ret:
            print("[!] Dropped frame or stream ended.")
            break
        count += 1

    total_time = time.perf_counter() - start_time
    fps = count / max(total_time, 1e-6)
    print(f"[✓] Benchmark complete:")
    print(f"    - Captured: {count} frames")
    print(f"    - Elapsed:  {total_time:.2f} seconds")
    print(f"    - Real FPS: {fps:.2f} FPS")

    cap.release()


if __name__ == "__main__":
    main()
