import threading
import time
from camera import CacaoDetector
from servo_controller import ServoController
import cv2

def main():
    cacao_detector = CacaoDetector()
    servo = ServoController()

    try:
        while True:
            variety, frame = cacao_detector.detect()

            if variety:
                print(f"[Camera] Detected: {variety}")
                threading.Thread(target=servo.move_to_variety, args=(variety,)).start()

            if frame is not None:
                cv2.imshow("Cacao Detection Feed", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("[System] Stopping...")

    finally:
        cacao_detector.release()
        servo.cleanup()

if __name__ == "__main__":
    main()
