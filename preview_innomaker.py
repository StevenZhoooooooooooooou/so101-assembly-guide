import cv2


# Change only this value to your Innomaker camera's video device port.
# Windows/macOS: 0, 1, 2...; Linux: 0, 1, 2... or "/dev/video2".
CAMERA_PORT = 0

# Camera input resolution.
INPUT_WIDTH = 1920
INPUT_HEIGHT = 1080

# Preview window resolution.
DISPLAY_WIDTH = 960
DISPLAY_HEIGHT = 540

# Camera frame rate.
FPS = 30


def main() -> None:
    camera = cv2.VideoCapture(CAMERA_PORT)
    if not camera.isOpened():
        raise SystemExit(
            f"Cannot open camera port {CAMERA_PORT}. Check CAMERA_PORT and allow "
            "camera access for your terminal in your operating system's privacy settings."
        )

    camera.set(cv2.CAP_PROP_FRAME_WIDTH, INPUT_WIDTH)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, INPUT_HEIGHT)
    camera.set(cv2.CAP_PROP_FPS, FPS)

    title = "Camera Preview"
    cv2.namedWindow(title, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(title, DISPLAY_WIDTH, DISPLAY_HEIGHT)
    print("Press Q or Esc to quit.")

    try:
        while True:
            ok, frame = camera.read()
            if not ok:
                break

            cv2.imshow(title, frame)
            if cv2.waitKey(1) & 0xFF in (ord("q"), 27):
                break
    finally:
        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
