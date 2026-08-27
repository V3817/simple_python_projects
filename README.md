# 🗂 Project Collection - Internal Structure Only

This repository contains five independent Python projects. Below is a concise internal structure overview of each:

---

### 1. **Text-to-Speech Terminal App**

* **Goal**: Speak out typed text using system voice.
* **Key Component**: `os.system()` call to run PowerShell's `SpeechSynthesizer`.
* **Loop**: Runs continuously until user enters `q` or `Q`.

---

### 2. **Weather Announcer**

* **Goal**: Speak out the current temperature and condition for a city.
* **Uses**:

  * `requests` to call [WeatherAPI](https://www.weatherapi.com/).
  * `.env` file for storing `API_KEY`.
  * `os.system()` + PowerShell for voice output.

---

### 3. **Image Resizer**

* **Goal**: Resize an image to a given percentage.
* **Uses**:

  * `cv2.imread` to load image.
  * Manual percentage input to scale dimensions.
  * `cv2.resize` and `cv2.imwrite` to save resized output.

---

### 4. **PDF Merger**

* **Goal**: Merge multiple PDFs into one.
* **Uses**:

  * `PyPDF2.PdfReader` to read individual PDFs.
  * `PdfMerger` to append and combine files.
  * Outputs a single merged PDF file.

---

### 5. **Face Recognition Attendance System**

* **Goal**: Detect faces in webcam feed and manually assign attendance.
* **Uses**:

  * `cv2.CascadeClassifier` for face detection.
  * Manual keyboard input (`1` or `2`) to mark known faces.
  * Records attendance in a date-wise CSV.
  * Real-time video stream using `cv2.VideoCapture`.
