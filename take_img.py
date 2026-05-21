import cv2

def capture_license_image(save_path="full_drivers_license.jpg"):
    # 1. Initialize the webcam (0 is usually the default built-in camera)
    cam = cv2.VideoCapture(0)
    
    if not cam.isOpened():
        print("Error: Could not open webcam.")
        return False

    print("Camera opened. Position your ID in the frame.")
    print("Press [SPACE] to capture the photo, or [ESC] to exit.")

    while True:
        # 2. Read a single frame from the camera
        ret, frame = cam.read()
        if not ret:
            print("Error: Failed to grab frame.")
            break

        # 3. Display the live feed to the user
        cv2.imshow("Position your Driver's License - Press Space to Capture", frame)

        # 4. Wait for key presses (checks every 1 millisecond)
        key = cv2.waitKey(1) & 0xFF
        
        # Press Spacebar (ASCII 32) to capture
        if key == 32:
            cv2.imwrite(save_path, frame)
            print(f"Photo captured successfully and saved to {save_path}!")
            success = True
            break
            
        # Press Escape (ASCII 27) to cancel/exit
        elif key == 27:
            print("Capture cancelled by user.")
            success = False
            break

    # 5. Cleanup and release the camera resources
    cam.release()
    cv2.destroyAllWindows()
    return success


if __name__ == '__main__':
    # Usage:
    capture_license_image()