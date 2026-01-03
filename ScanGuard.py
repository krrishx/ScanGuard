import cv2
from pyzbar import pyzbar
from scam_rules import analyze_qr_data
import webbrowser
import sys

APP_NAME = "ScanGuard"
last_seen_data = None
link_opened = False
app_running = True


def draw_label(frame, barcode, verdict):
    x, y, w, h = barcode.rect
    if verdict == "SAFE":
        color = (0, 255, 0)
    elif verdict == "SUSPICIOUS":
        color = (0, 255, 255)
    else:
        color = (0, 0, 255)

    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
    cv2.putText(
        frame,
        verdict,
        (x, y - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        color,
        2
    )


def open_camera():
    print("=" * 50)
    print("SEARCHING FOR CAMERAS...")
    print("=" * 50)

    for i in range(4):
        print(f"[Attempt {i+1}] Trying camera index {i}...")
        cap = cv2.VideoCapture(i)

        if cap.isOpened():
            ret, test_frame = cap.read()
            if ret:
                print(f"✓✓✓ SUCCESS! Camera {i} is working!")
                print(f"    Frame size: {test_frame.shape}")
                return cap
            else:
                print(f"✗ Camera {i} opened but can't read frames")
                cap.release()
        else:
            print(f"✗ Camera {i} failed to open")

    print("\n" + "=" * 50)
    print("ERROR: NO WORKING CAMERA FOUND")
    print("=" * 50)
    input("Press Enter to exit...")
    sys.exit(1)


def main():
    global last_seen_data, link_opened, app_running

    print("\n" + "=" * 50)
    print("STARTING SCANGUARD")
    print("=" * 50)
    print("Press 'q' in the camera window to quit\n")

    cap = open_camera()

    print("\n" + "=" * 50)
    print("CAMERA ACTIVE - SCANNING FOR QR CODES")
    print("=" * 50)
    print("Point a QR code at the camera...")

    frame_count = 0

    while app_running:
        ret, frame = cap.read()
        if not ret:
            print("WARNING: Failed to read frame")
            continue

        frame_count += 1

        if frame_count % 30 == 0:
            print(f"Running... (Frame {frame_count})")

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        barcodes = pyzbar.decode(gray)

        if not barcodes:
            last_seen_data = None
            link_opened = False
        else:
            print(f"\n>>> QR CODE DETECTED! (Found {len(barcodes)} code(s))")

        for barcode in barcodes:
            data = barcode.data.decode("utf-8").strip()
            print(f"    Data: {data}")

            verdict, reason = analyze_qr_data(data)
            print(f"    Verdict: {verdict}")
            print(f"    Reason: {reason}")

            draw_label(frame, barcode, verdict)

            if (
                app_running
                and verdict == "SAFE"
                and data.startswith(("http://", "https://"))
                and data != last_seen_data
                and not link_opened
            ):
                print(f"    >>> OPENING LINK: {data}")
                webbrowser.open(data)
                link_opened = True
                last_seen_data = data

        cv2.putText(
            frame,
            f"Frame: {frame_count} | Press Q to quit",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        cv2.imshow(APP_NAME, frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            print("\n>>> QUIT KEY PRESSED")
            app_running = False
            break

    print("\n" + "=" * 50)
    print("SHUTTING DOWN")
    print("=" * 50)
    cap.release()
    cv2.destroyAllWindows()
    print("Goodbye!")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("\n" + "=" * 50)
        print("FATAL ERROR!")
        print("=" * 50)
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
