# Heart Rate Detection using Webcam

This repository contains a Python-based project for estimating heart rate using a standard webcam. The method utilizes facial detection and signal processing techniques to analyze subtle changes in skin color caused by blood flow.

---

## Features

- **Facial Detection:** Detects the face and defines a region of interest (ROI) on the forehead for analysis.
- **Color Signal Extraction:** Extracts the green channel intensity over time from the ROI.
- **Signal Filtering:** Applies high-pass and low-pass Butterworth filters to reduce noise and isolate relevant frequency components.
- **Heart Rate Estimation:** Uses Fast Fourier Transform (FFT) to estimate heart rate in beats per minute (BPM).
- **Visualization:** Plots the time-domain signal, filtered signals, and frequency spectrum for analysis.

---

## Prerequisites

To run this project, ensure you have the following installed:

### **Python Version**
- Python 3.7 or later

### **Required Libraries**
Install the required Python libraries using pip:

```bash
pip install opencv-python cvzone matplotlib scipy numpy
```

### **Hardware Requirements**
- A standard webcam with at least 720p resolution
- A stable lighting environment for accurate detection

---

## How It Works

1. **Face Detection:**
   - The `cvzone.FaceDetectionModule` is used to detect the face and define a region of interest (ROI) on the forehead.
2. **Green Channel Extraction:**
   - The mean intensity of the green channel from the ROI is recorded frame-by-frame.
3. **Signal Filtering:**
   - Low-pass and high-pass filters are applied to remove motion artifacts and lighting variations.
4. **Frequency Analysis:**
   - FFT is used to identify the dominant frequency within the range of 0.8 to 2 Hz, corresponding to 48–120 BPM.
5. **Heart Rate Calculation:**
   - The dominant frequency is converted to beats per minute (BPM).

---

## Usage

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```
2. Run the script:
   ```bash
   python <script-name>.py
   ```
3. Follow the on-screen instructions and ensure your face is visible to the webcam. Remain still during the measurement for better accuracy.

---

## Limitations

- The method is sensitive to:
  - Changes in lighting conditions
  - Head movement
  - Skin tone variations
- Works best in a controlled environment with consistent lighting.

---

## Results

The script visualizes:
- Green channel intensity over time
- Filtered signals
- Frequency spectrum with the dominant frequency highlighted

---

## Contributions

Contributions are welcome! If you find issues or have suggestions, feel free to open a pull request or create an issue.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

