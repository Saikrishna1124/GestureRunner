import cv2
import time

def test_single_cam(index):
    print(f"Testing Camera Index {index}...")
    # Try different backends
    backends = [cv2.CAP_DSHOW, cv2.CAP_MSMF, None]
    
    for backend in backends:
        backend_name = str(backend) if backend is not None else "AUTO"
        print(f"  Attempting with backend: {backend_name}")
        
        if backend is not None:
            cap = cv2.VideoCapture(index, backend)
        else:
            cap = cv2.VideoCapture(index)
            
        if cap.isOpened():
            print(f"  SUCCESS: Camera {index} opened with {backend_name}!")
            print("  Checking if we can read a frame...")
            ret, frame = cap.read()
            if ret:
                print("  SUCCESS: Read frame! Camera light should be ON.")
                cv2.imshow("Test Camera", frame)
                print("  Window should be visible. Press any key in the window to close.")
                cv2.waitKey(5000) # Show for 5 seconds
                cap.release()
                cv2.destroyAllWindows()
                return True
            else:
                print("  FAILED: cap.isOpened() was True but could not read frame.")
            cap.release()
        else:
            print(f"  FAILED: Could not open Camera {index} with {backend_name}.")
    
    return False

if __name__ == "__main__":
    found = False
    for i in range(3):
        if test_single_cam(i):
            found = True
            break
    
    if not found:
        print("\nCRITICAL: No working cameras found at all.")
        print("Please check:")
        print("1. Is your webcam plugged in?")
        print("2. Is another app (Zoom, Teams, Chrome) using it?")
        print("3. Check Privacy Settings: Start -> Settings -> Privacy -> Camera (Allow apps to access).")
