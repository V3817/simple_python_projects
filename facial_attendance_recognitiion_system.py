"""
FACE RECOGNITION ATTENDANCE SYSTEM
==================================

This system uses computer vision and machine learning to automatically detect and recognize 
faces in real-time video, then marks attendance for recognized students.

KEY CONCEPTS:
- Face Detection: Finding faces in images/video
- Face Recognition: Identifying whose face it is
- Face Encoding: Converting face features into numerical data for comparison
- OpenCV: Computer vision library for video capture and image processing
- CSV: Simple file format to store attendance records

REQUIRED LIBRARIES:
- face_recognition: Main library for face detection and recognition
- cv2 (OpenCV): For video capture and image display
- csv: For saving attendance data
- numpy: For mathematical operations on arrays
- datetime: For timestamps
"""

import face_recognition  # Main library for face recognition
import cv2              # OpenCV for video capture and display
import csv              # For creating and writing CSV files
import numpy as np      # For numerical operations and arrays
from datetime import datetime  # For getting current date and time

# STEP 1: INITIALIZE VIDEO CAPTURE
# ================================
# VideoCapture(0) means use the default camera (usually built-in webcam)
# VideoCapture(1) would be second camera, etc.
video_capture = cv2.VideoCapture(0)

# STEP 2: LOAD AND ENCODE REFERENCE FACES
# =======================================
# This is the "training" phase where we teach the system what each person looks like

# Load first student's photo from file
# face_recognition.load_image_file() converts image file to format the library can use
my_image = face_recognition.load_image_file("faces/Aryal.jpg")

# Create "face encoding" - this converts the face into a list of 128 numbers
# These numbers represent unique facial features (distance between eyes, nose shape, etc.)
# [0] means take the first face found in the image (assuming only one person per photo)
my_encodings = face_recognition.face_encodings(my_image)[0]

# Same process for second student
newton = face_recognition.load_image_file("faces/newton.jpg")
newton_encodings = face_recognition.face_encodings(newton)[0]

# STEP 3: CREATE DATABASES OF KNOWN STUDENTS
# ==========================================
# Store student names in a list (strings, not image objects)
class_students_list_names = ["Aryal", "Newton"]

# Store corresponding face encodings (the 128-number lists)
# The order must match the names list above
class_students_list_names_encodings = [my_encodings, newton_encodings]

# Create copy for daily attendance tracking
# We'll remove names from this list as they get marked present
# This prevents marking the same person multiple times in one day
students = class_students_list_names.copy()

# STEP 4: INITIALIZE DETECTION VARIABLES
# =====================================
face_locations = []  # Will store coordinates of faces found in each video frame
face_encodings = []  # Will store encodings of faces found in each video frame

# STEP 5: SETUP DATE AND FILE MANAGEMENT
# ======================================
# Get current date and time
now = datetime.now()

# Format date as YYYY-MM-DD (e.g., "2024-03-15")
# %Y = 4-digit year, %m = 2-digit month, %d = 2-digit day
current_date = now.strftime("%Y-%m-%d")

# STEP 6: CREATE CSV FILE FOR ATTENDANCE
# =====================================
# Create CSV filename using today's date
csv_filename = f"{current_date}.csv"

# Open file for writing
# "w+" means write mode, create new file or overwrite existing
# newline="" prevents extra blank lines in CSV
f = open(csv_filename, "w+", newline="")

# Create CSV writer object to easily write rows to file
attendance_writer = csv.writer(f)

# Write header row to CSV file
attendance_writer.writerow(["Name", "Time"])

print(f"Attendance system started. Recording to: {csv_filename}")
print("Press 'q' to quit the system")

# STEP 7: MAIN RECOGNITION LOOP
# =============================
# This loop runs continuously, processing video frames one by one
while True:
    # STEP 7A: CAPTURE VIDEO FRAME
    # ----------------------------
    # Read one frame from the video camera
    # ret = True if frame captured successfully, False if failed
    # frame = the actual image data
    ret, frame = video_capture.read()
    
    # Check if frame capture was successful
    if not ret:
        print("Failed to capture video frame")
        break
    
    # STEP 7B: OPTIMIZE FRAME FOR PROCESSING
    # --------------------------------------
    # Resize frame to 1/4 size to make processing faster
    # fx=0.25, fy=0.25 means 25% of original size
    # Face recognition is computationally expensive, so smaller = faster
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    
    # Convert color format from BGR (Blue-Green-Red) to RGB (Red-Green-Blue)
    # OpenCV uses BGR by default, but face_recognition library expects RGB
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
    
    # STEP 7C: DETECT FACES IN CURRENT FRAME
    # --------------------------------------
    # Find all faces in the current frame
    # Returns list of face coordinates: [(top, right, bottom, left), ...]
    face_locations = face_recognition.face_locations(rgb_small_frame)
    
    # Create encodings for all detected faces
    # This converts each detected face into the 128-number format
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    
    # STEP 7D: RECOGNIZE EACH DETECTED FACE
    # -------------------------------------
    # Loop through each face found in the current frame
    for face_encoding in face_encodings:
        
        # STEP 7D1: COMPARE WITH KNOWN FACES
        # ----------------------------------
        # Compare current face with all known student faces
        # Returns list of True/False for each known face
        # True = faces match, False = faces don't match
        matches = face_recognition.compare_faces(class_students_list_names_encodings, face_encoding)
        
        # Calculate "distance" between current face and each known face
        # Lower distance = better match
        # Distance of 0.0 = identical faces, distance > 1.0 = very different faces
        face_distance = face_recognition.face_distance(class_students_list_names_encodings, face_encoding)
        
        # Find which known face has the smallest distance (best match)
        # np.argmin() returns the index of the smallest value
        best_match_index = np.argmin(face_distance)
        
        # STEP 7D2: VERIFY MATCH QUALITY
        # ------------------------------
        # Check if the best match is actually good enough to trust
        # matches[best_match_index] = True means face_recognition considers it a match
        if matches[best_match_index]:
            # Get the name of the matched student
            name = class_students_list_names[best_match_index]
            
            # STEP 7D3: DISPLAY RECOGNITION RESULT
            # -----------------------------------
            # Setup text properties for displaying name on video
            font = cv2.FONT_HERSHEY_SIMPLEX           # Font style
            bottomLeftCornerOfText = (10, 100)        # Position on screen (x, y)
            fontScale = 1.5                           # Text size
            fontColor = (255, 0, 0)                   # Color in BGR format (blue)
            thickness = 3                             # Text thickness
            lineType = 2                              # Line type for text
            
            # Draw the student's name on the video frame
            # This shows "Name Present" on the live video
            cv2.putText(frame, name + " Present", bottomLeftCornerOfText, 
                       font, fontScale, fontColor, thickness, lineType)
            
            # STEP 7D4: RECORD ATTENDANCE
            # --------------------------
            # Only mark attendance if student hasn't been marked today
            # This prevents duplicate entries for the same person
            if name in students:
                # Remove student from tracking list
                students.remove(name)
                
                # Get current time for attendance record
                current_time = datetime.now().strftime("%H:%M:%S")
                
                # Write attendance record to CSV file
                # Format: [Student Name, Time]
                attendance_writer.writerow([name, current_time])
                
                # Force write to file immediately (don't wait for buffer to fill)
                f.flush()
                
                # Print confirmation message
                print(f"✓ {name} marked present at {current_time}")
        
        else:
            # STEP 7D5: HANDLE UNRECOGNIZED FACES
            # ----------------------------------
            # If face is detected but not recognized, show "Unknown"
            cv2.putText(frame, "Unknown Person", (10, 100), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3, 2)
    
    # STEP 7E: DISPLAY VIDEO FRAME
    # ----------------------------
    # Show the video frame with any text overlays
    # This creates the window where you see the live video
    cv2.imshow("Attendance System", frame)
    
    # STEP 7F: CHECK FOR EXIT COMMAND
    # ------------------------------
    # Wait 1 millisecond for key press
    # & 0xFF extracts only the last 8 bits (handles different operating systems)
    # ord('q') converts letter 'q' to its ASCII number
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Exiting attendance system...")
        break

# STEP 8: CLEANUP AND SHUTDOWN
# ============================
# Release the camera so other programs can use it
video_capture.release()

# Close all OpenCV windows
cv2.destroyAllWindows()

# Close the CSV file
f.close()

# Print final summary
print(f"Attendance saved to: {csv_filename}")
print(f"Students still not marked present: {students}")
print("System shutdown complete.")

"""
DETAILED WORKFLOW EXPLANATION:
==============================

1. INITIALIZATION PHASE (Lines 1-80):
   - Import required libraries
   - Start video camera
   - Load reference photos of students
   - Convert photos to mathematical representations (encodings)
   - Create lists to store student data
   - Setup CSV file for attendance records

2. MAIN PROCESSING LOOP (Lines 81-180):
   For each video frame:
   a) Capture frame from camera
   b) Resize frame for faster processing
   c) Convert color format for face recognition library
   d) Find all faces in the frame
   e) Convert found faces to encodings
   f) Compare each found face with known students
   g) If match found: display name and record attendance
   h) If no match: display "Unknown"
   i) Show video with overlays
   j) Check if user wants to quit

3. CLEANUP PHASE (Lines 181-190):
   - Release camera resources
   - Close video windows
   - Save and close attendance file
   - Print summary

FACE RECOGNITION PROCESS:
========================

1. Face Detection: "Is there a face in this image?"
   - Uses machine learning to find face-like regions
   - Returns coordinates of face boundaries

2. Face Encoding: "What does this face look like?"
   - Measures 128 different facial features
   - Creates unique "fingerprint" for each face
   - Examples: distance between eyes, nose width, jaw shape

3. Face Recognition: "Whose face is this?"
   - Compares new face encoding with known encodings
   - Calculates similarity scores
   - If similarity is high enough, declares a match

TROUBLESHOOTING TIPS:
====================

1. If faces aren't recognized:
   - Ensure good lighting
   - Look directly at camera
   - Move closer/farther from camera
   - Check if reference photos are clear

2. If "Unknown Person" appears frequently:
   - Retake reference photos with better quality
   - Ensure only one face per reference photo
   - Try different angles in reference photos

3. If system is slow:
   - Close other programs using camera
   - Reduce video resolution
   - Use better computer hardware

4. If attendance isn't recorded:
   - Check if CSV file is created
   - Ensure you have write permissions in folder
   - Verify student names match exactly
"""