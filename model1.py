import cv2
import numpy as np
import pyttsx3

# ----------------- Voice Setup -----------------
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def speak_color(color_name):
    engine.say(f"This color is {color_name}")
    engine.runAndWait()

# ----------------- Custom CSS3 Color Dictionary -----------------
css3_colors = {
    'black': '#000000', 'white': '#ffffff', 'red': '#ff0000', 'lime': '#00ff00', 'blue': '#0000ff',
    'yellow': '#ffff00', 'cyan': '#00ffff', 'magenta': '#ff00ff', 'silver': '#c0c0c0',
    'gray': '#808080', 'maroon': '#800000', 'olive': '#808000', 'green': '#008000',
    'purple': '#800080', 'teal': '#008080', 'navy': '#000080', 'orange': '#ffa500',
    'pink': '#ffc0cb', 'brown': '#a52a2a', 'gold': '#ffd700', 'beige': '#f5f5dc',
    'coral': '#ff7f50', 'aqua': '#00ffff', 'indigo': '#4b0082', 'violet': '#ee82ee'
}

# ----------------- Helper Functions -----------------
def get_closest_color_name(requested_rgb, tolerance=60):
    """
    Get the closest color name to the requested RGB.
    The tolerance allows some color variations to be matched.
    """
    min_distance = float('inf')
    closest_name = None
    for name, hex_value in css3_colors.items():
        # Convert hex to RGB
        r_c, g_c, b_c = tuple(int(hex_value.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        
        # Calculate the Euclidean distance between the colors (with tolerance range)
        distance = np.sqrt((r_c - requested_rgb[0]) ** 2 +
                           (g_c - requested_rgb[1]) ** 2 +
                           (b_c - requested_rgb[2]) ** 2)
        
        # Compare with the minimum distance and check if it’s within the tolerance range
        if distance < min_distance and distance <= tolerance:
            min_distance = distance
            closest_name = name
    
    # If no match is found within tolerance, return a "no match" label
    if closest_name is None:
        return "Unknown Color"
    
    return closest_name

def get_color_name(b, g, r):
    """
    This function returns the closest color name for a given (r, g, b) color.
    """
    return get_closest_color_name((r, g, b))

# ----------------- Mouse Click Handler -----------------
def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        b, g, r = frame[y, x]
        color_name = get_color_name(b, g, r)
        print(f"Color at ({x},{y}): {color_name}")
        speak_color(color_name)

# ----------------- Color Blind Simulation & Correction -----------------
def simulate_protanopia(img):
    cb_mtx = np.array([
        [0.56667, 0.43333, 0],
        [0.55833, 0.44167, 0],
        [0,       0.24167, 0.75833]
    ])
    return apply_color_matrix(img, cb_mtx)

def daltonize_protanopia(img):
    sim = simulate_protanopia(img)
    error = img.astype(float) - sim.astype(float)
    corrected = img.astype(float) + error * 0.5
    return np.clip(corrected, 0, 255).astype(np.uint8)

def apply_color_matrix(img, matrix):
    img_float = img.astype(float) / 255.0
    transformed = np.dot(img_float, matrix.T)
    transformed = np.clip(transformed, 0, 1.0)
    return (transformed * 255).astype(np.uint8)

# ----------------- Main Program -----------------
cap = cv2.VideoCapture(0)
cv2.namedWindow("Color Assist (Press 's' to toggle mode)")
cv2.setMouseCallback("Color Assist (Press 's' to toggle mode)", mouse_callback)

mode = 0  # 0: Normal, 1: Simulate, 2: Daltonize

print("Press 's' to switch mode: Normal → Simulated → Daltonized")
print("Press 'q' to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    if mode == 1:
        display = simulate_protanopia(frame)
        label = "Simulated Protanopia View"
    elif mode == 2:
        display = daltonize_protanopia(frame)
        label = "Daltonized Correction View"
    else:
        display = frame.copy()
        label = "Normal Vision"

    cv2.putText(display, label, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Color Assist (Press 's' to toggle mode)", display)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):
        mode = (mode + 1) % 3
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
