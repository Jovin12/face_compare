import cv2
import numpy as np
from deepface import DeepFace

def compare_id_photo(selfie_path, license_path):
    img1 = cv2.imread(selfie_path)
    img2 = cv2.imread(license_path)

    if img1 is None or img2 is None: 
        return "Error: Could not load one or both image."
    
    try: 
        result = DeepFace.verify(
            img1_path = img1, 
            img2_path = img2, 
            model_name = 'VGG-Face',
            detector_backend = 'opencv'
        )

        print(f"Match: {result['verified']}")
        print(f"Distance/similarity Score: {result['distance']:.4f}")
        return result['verified']
    except Exception as e: 
        print(f"Face verification failed: {e}")
        return False
    

if __name__ == "__main__":
    is_match = compare_id_photo("cropped_face.jpg", "cropped_face.jpg")
    print(is_match)