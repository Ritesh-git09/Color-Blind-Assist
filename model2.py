import cv2
import numpy as np
import pyttsx3

# Voice Engine Setup
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# Mode Options
modes = ['normal', 'bayer', 'protanopia']
current_mode = 'normal'

# Color naming dictionary
named_colors = {
    'black': (0, 0, 0), 'white': (255, 255, 255), 'red': (255, 0, 0),
    'green': (0, 255, 0), 'blue': (0, 0, 255), 'yellow': (255, 255, 0),
    'cyan': (0, 255, 255), 'magenta': (255, 0, 255), 'gray': (128, 128, 128),
    'orange': (255, 165, 0), 'pink': (255, 192, 203), 'purple': (128, 0, 128),
    'brown': (165, 42, 42), 'navy': (0, 0, 128)
}

def speak_color(color_name):
    engine.say(f"This color is {color_name}")
    engine.runAndWait()

def closest_named_color(rgb):
    min_dist = float('inf')
    closest_name = "Unknown Color"
    for name, value in named_colors.items():
        dist = np.linalg.norm(np.array(rgb) - np.array(value))
        if dist < min_dist:
            min_dist = dist
            closest_name = name
    return closest_name

def get_color_name(b, g, r):
    return closest_named_color((r, g, b))

# Simulated Bayer filter
def apply_bayer_filter(image):
    bayer = np.zeros_like(image)
    bayer[::2, ::2, 1] = image[::2, ::2, 1]  # Green
    bayer[1::2, 1::2, 1] = image[1::2, 1::2, 1]  # Green
    bayer[::2, 1::2, 2] = image[::2, 1::2, 2]  # Red
    bayer[1::2, ::2, 0] = image[1::2, ::2, 0]  # Blue
    return bayer

# Demosaicing
def demosaic_bayer(bayer_img):
    bayer_gray = cv2.cvtColor(bayer_img, cv2.COLOR_BGR2GRAY)
    return cv2.cvtColor(bayer_gray, cv2.COLOR_BAYER_BG2BGR)

# Simulate Protanopia
def simulate_protanopia(img):
    conversion_matrix = np.array([[0.567, 0.433, 0],
                                  [0.558, 0.442, 0],
                                  [0, 0.242, 0.758]])
    return cv2.transform(img, conversion_matrix)

# Mouse event to detect color
def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        b, g, r = frame[y, x]
        color_name = get_color_name(b, g, r)
        print(f"Clicked Color at ({x},{y}): {color_name}")
        speak_color(color_name)

# Start webcam
cap = cv2.VideoCapture(0)
cv2.namedWindow("Color Blind Assist - Multi View")
cv2.setMouseCallback("Color Blind Assist - Multi View", mouse_callback)

print("Press 'n' for Normal | 'b' for Bayer | 'p' for Protanopia | 'q' to Quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)

    if current_mode == 'normal':
        display_frame = frame.copy()
        label = "Normal View"

    elif current_mode == 'bayer':
        bayer_image = apply_bayer_filter(frame)
        display_frame = demosaic_bayer(bayer_image)
        label = "Bayer Demosaiced View"

    elif current_mode == 'protanopia':
        bayer_image = apply_bayer_filter(frame)
        demosaiced = demosaic_bayer(bayer_image)
        display_frame = simulate_protanopia(demosaiced)
        label = "Protanopia Simulation (Bayer Processed)"

    # Show mode label
    cv2.putText(display_frame, label, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    cv2.imshow("Color Blind Assist - Multi View", display_frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('n'):
        current_mode = 'normal'
    elif key == ord('b'):
        current_mode = 'bayer'
    elif key == ord('p'):
        current_mode = 'protanopia'

cap.release()
cv2.destroyAllWindows()
