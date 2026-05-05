# 🛠️ Dynamic Multi-Wave Signal Generator

---

## 📦 Project Overview
This project is a Python-based desktop application built using Tkinter, NumPy, and Matplotlib. 

It acts as a dynamic signal generator, allowing users to visually construct, combine, and manipulate complex waveforms on a master timeline. It calculates real-time RMS values and exports the final combined signal array as a formatted JSON file, which can then be fed into the main LRC simulation environment for RCD code testing.

---

## 🧰 Requirements

### ✅ Software & Libraries
- **Python:** >= 3.8
- **Required Python Packages:**
  - `numpy` (For fast mathematical array generation)
  - `matplotlib` (For rendering the real-time interactive graph)

*(Note: `tkinter` and `json` are used extensively but are included in the standard Python library by default).*

---

## 🚀 Getting Started

### 1. Install Dependencies
Before running the application, ensure you have the required mathematical and plotting libraries installed. Open your terminal or command prompt and run:

```bash
pip install numpy matplotlib

### 2. Run the Application
- Running the application can be done in two ways
  1. Via Terminal: Navigate to the directory containing the script and launch it using Python:
    Bash
    python SignalGenerator.py
  2. Via Visual Studio: Open the location of the project. Right-click inside the folder and select "Open with Visual Studio" (if it isn't listed, click on "Show more options" to reveal it). Once open, you can run the script directly from the IDE.

### 3. Usage Guide
- The application will open in a maximized window with a control panel on the left and a live graph on the right.

  1. Global Settings: Set your Sampling Frequency at the bottom of the graph. This dictates the resolution of your generated data array.

  2. Add Waves: Click the + button in the top left to add a new wave to the timeline.

  3. Configure Waves: For each wave, you can modify the following parameters in real-time:

      - Type: Sine, Square, Triangle, Positive Sine, or Peak.

      - Freq and Amp: Set the frequency and amplitude.

      - Noise: Inject random noise into the specific wave using the slider.

      - Start Time and Duration (ms): Sequence the wave perfectly on the master timeline.

  4. Export Data: Once your combined signal is perfectly shaped, click the Export JSON button on the left panel.

### 4. Output
- Clicking Export will generate a SignalData.json file in the same directory. This file contains the total RMS, the sampling frequency, and the massive array of generated mathematical data points, ready to be imported into the LRC Qt6 Simulation!

---


