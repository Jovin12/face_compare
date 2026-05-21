import cv2
from deepface import DeepFace

def crop_license_face(license_path, save_path = "cropped_face.jpg"):
    try: 
        face_objs = DeepFace.extract_faces(
            img_path = license_path, 
            detector_backend = 'opencv', 
            # target_size = (224,224)
        )

        if len(face_objs) == 0:
            print("No face detectd on driver's license")
            return None
        
        face_pixels = face_objs[0]['face']
        face_img = (face_pixels * 255).astype('uint8')
        face_img = cv2.cvtColor(face_img, cv2.COLOR_RGB2BGR)


        cv2.imwrite(save_path, face_img)
        return save_path
    except Exception as e: 
        print(f"Error cropping license: {e}")
        return None

if __name__ == "__main__":
    cropped_face_path = crop_license_face("full_drivers_license.jpg")
