import streamlit as st
import cv2
import numpy as np
import pyttsx3
import threading
from PIL import Image
import webcolors
import colorsys
import time

# Configure Streamlit page
st.set_page_config(
    page_title="Advanced Color Blind Assist",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

class ColorBlindAssist:
    def __init__(self):
        self.engine = None
        self.init_voice_engine()
        
        # Enhanced color dictionary
        self.extended_colors = {
            'black': '#000000', 'white': '#ffffff', 'red': '#ff0000', 'lime': '#00ff00', 
            'blue': '#0000ff', 'yellow': '#ffff00', 'cyan': '#00ffff', 'magenta': '#ff00ff',
            'silver': '#c0c0c0', 'gray': '#808080', 'maroon': '#800000', 'olive': '#808000',
            'green': '#008000', 'purple': '#800080', 'teal': '#008080', 'navy': '#000080',
            'orange': '#ffa500', 'pink': '#ffc0cb', 'brown': '#a52a2a', 'gold': '#ffd700',
            'beige': '#f5f5dc', 'coral': '#ff7f50', 'indigo': '#4b0082', 'violet': '#ee82ee',
            'crimson': '#dc143c', 'salmon': '#fa8072', 'khaki': '#f0e68c', 'plum': '#dda0dd',
            'orchid': '#da70d6', 'tan': '#d2691e', 'azure': '#f0ffff', 'lavender': '#e6e6fa',
            'turquoise': '#40e0d0', 'chocolate': '#d2691e', 'firebrick': '#b22222'
        }
        
        # Color blindness simulation matrices
        self.color_matrices = {
            'protanopia': np.array([
                [0.56667, 0.43333, 0.00000],
                [0.55833, 0.44167, 0.00000],
                [0.00000, 0.24167, 0.75833]
            ]),
            'deuteranopia': np.array([
                [0.625, 0.375, 0.0],
                [0.7, 0.3, 0.0],
                [0.0, 0.3, 0.7]
            ]),
            'tritanopia': np.array([
                [0.95, 0.05, 0.0],
                [0.0, 0.43333, 0.56667],
                [0.0, 0.475, 0.525]
            ])
        }

    def init_voice_engine(self):
        """Initialize text-to-speech engine"""
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 150)
            self.engine.setProperty('volume', 0.9)
        except Exception as e:
            st.error(f"Voice engine initialization failed: {e}")

    def speak_async(self, text):
        """Speak text asynchronously"""
        if self.engine:
            def speak():
                try:
                    self.engine.say(text)
                    self.engine.runAndWait()
                except:
                    pass
            thread = threading.Thread(target=speak)
            thread.daemon = True
            thread.start()

    def hex_to_rgb(self, hex_color):
        """Convert hex color to RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def get_color_name_advanced(self, rgb, tolerance=50):
        """Advanced color name detection"""
        r, g, b = rgb
        
        # Try webcolors library first
        try:
            closest_name = webcolors.rgb_to_name((r, g, b))
            return closest_name
        except ValueError:
            pass
        
        # Find closest in extended dictionary
        min_distance = float('inf')
        closest_name = "Unknown Color"
        
        for name, hex_value in self.extended_colors.items():
            color_rgb = self.hex_to_rgb(hex_value)
            distance = np.sqrt(sum((a - b) ** 2 for a, b in zip(rgb, color_rgb)))
            
            if distance < min_distance and distance <= tolerance:
                min_distance = distance
                closest_name = name
        
        # Generate descriptive color name if no close match
        if closest_name == "Unknown Color" or min_distance > tolerance:
            h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
            h = h * 360
            s = s * 100
            v = v * 100
            
            if s < 20:
                if v < 30:
                    closest_name = "very dark gray"
                elif v < 70:
                    closest_name = "gray"
                else:
                    closest_name = "light gray"
            else:
                if h < 15 or h >= 345:
                    hue_name = "red"
                elif h < 45:
                    hue_name = "orange"
                elif h < 75:
                    hue_name = "yellow"
                elif h < 105:
                    hue_name = "yellow-green"
                elif h < 135:
                    hue_name = "green"
                elif h < 165:
                    hue_name = "cyan-green"
                elif h < 195:
                    hue_name = "cyan"
                elif h < 225:
                    hue_name = "blue"
                elif h < 255:
                    hue_name = "blue-violet"
                elif h < 285:
                    hue_name = "violet"
                elif h < 315:
                    hue_name = "magenta"
                else:
                    hue_name = "red-magenta"
                
                if v < 30:
                    hue_name = f"dark {hue_name}"
                elif v > 80:
                    hue_name = f"bright {hue_name}"
                
                if s < 40:
                    hue_name = f"pale {hue_name}"
                elif s > 80:
                    hue_name = f"vivid {hue_name}"
                
                closest_name = hue_name
        
        return closest_name

    def apply_color_matrix(self, img, matrix):
        """Apply color transformation matrix"""
        img_float = img.astype(float) / 255.0
        h, w, c = img_float.shape
        img_reshaped = img_float.reshape(-1, c)
        transformed = np.dot(img_reshaped, matrix.T)
        transformed = np.clip(transformed, 0, 1.0)
        result = (transformed * 255).astype(np.uint8)
        return result.reshape(h, w, c)

    def simulate_color_blindness(self, img, cb_type):
        """Simulate different types of color blindness"""
        if cb_type in self.color_matrices:
            return self.apply_color_matrix(img, self.color_matrices[cb_type])
        return img

    def daltonize_image(self, img, cb_type):
        """Apply basic daltonization correction"""
        if cb_type in self.color_matrices:
            simulated = self.simulate_color_blindness(img, cb_type)
            error = img.astype(float) - simulated.astype(float)
            corrected = img.astype(float) + error * 0.7
            return np.clip(corrected, 0, 255).astype(np.uint8)
        return img

def main():
    st.title("🎨 Advanced Color Blind Assist - Real Time Color Guide")
    st.markdown("### Comprehensive color detection and assistance for various color vision deficiencies")
    
    # Initialize the color assist system
    if 'color_assist' not in st.session_state:
        st.session_state.color_assist = ColorBlindAssist()
    color_assist = st.session_state.color_assist
    # Initialize screenshot state
    if 'screenshot' not in st.session_state:
        st.session_state.screenshot = None
    
    # Sidebar controls
    st.sidebar.header("🔧 Settings")
    
    # Color blindness type selection
    cb_options = {
        "Normal Vision": None,
        "Protanopia (Red-blind)": "protanopia",
        "Deuteranopia (Green-blind)": "deuteranopia", 
        "Tritanopia (Blue-blind)": "tritanopia"
    }
    
    cb_selection = st.sidebar.selectbox("Select Color Vision Type:", list(cb_options.keys()))
    cb_type = cb_options[cb_selection]
    
    # View mode selection
    view_mode = st.sidebar.selectbox(
        "View Mode:",
        ["Normal", "Simulated", "Corrected (Daltonized)"]
    )
    
    # Voice settings
    voice_enabled = st.sidebar.checkbox("Enable Voice Assistance", value=True)
    
    # Color detection sensitivity
    tolerance = st.sidebar.slider("Color Detection Sensitivity", 10, 100, 50)
    
    # Main interface
    st.header("📹 Live Camera Feed")
    # Initialize camera state
    if 'camera_active' not in st.session_state:
        st.session_state.camera_active = False
    # Camera controls
    camera_col1, camera_col2, camera_col3 = st.columns(3)
    with camera_col1:
        if st.button("▶️ Start Camera"):
            st.session_state.camera_active = True
    with camera_col2:
        if st.button("⏹️ Stop Camera"):
            st.session_state.camera_active = False
    with camera_col3:
        if st.button("📸 Capture Frame") and st.session_state.current_frame is not None:
            st.session_state.screenshot = st.session_state.current_frame.copy()
            st.rerun()
    # Video display area
    video_placeholder = st.empty()
    # Status display
    status_placeholder = st.empty()
    # Instructions
    st.markdown("""
    **Instructions:**
    1. Click '▶️ Start Camera' to begin live feed
    2. Click '📸 Capture Frame' to freeze and analyze any pixel
    3. Click anywhere on the captured image to detect color
    4. Adjust settings in the sidebar
    
    **Features:**
    - Real-time color detection with voice
    - Color blindness simulation & correction
    - Click-to-detect color on captured image
    - Advanced color naming system
    """)
    # Manual color input
    st.subheader("🎨 Manual Color Test")
    manual_color = st.color_picker("Pick a color to test", "#ff0000")
    if st.button("🔊 Speak Manual Color"):
        hex_color = manual_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        color_name = color_assist.get_color_name_advanced(rgb, tolerance)
        st.write(f"**Selected Color:** {color_name}")
        if voice_enabled:
            color_assist.speak_async(f"This color is {color_name}")
    
    # Fast live camera feed loop
    if st.session_state.camera_active:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            status_placeholder.error("Cannot access camera. Please check your camera connection.")
            st.session_state.camera_active = False
        else:
            status_placeholder.success("📹 Camera is active")
            frame_rgb = None
            if 'current_frame' not in st.session_state:
                st.session_state.current_frame = None
            while st.session_state.camera_active:
                ret, frame = cap.read()
                if not ret:
                    status_placeholder.error("Failed to read from camera.")
                    break
                frame = cv2.flip(frame, 1)
                if cb_type and view_mode == "Simulated":
                    processed_frame = color_assist.simulate_color_blindness(frame, cb_type)
                    label = f"Simulated {cb_selection}"
                elif cb_type and view_mode == "Corrected (Daltonized)":
                    processed_frame = color_assist.daltonize_image(frame, cb_type)
                    label = f"Corrected {cb_selection}"
                else:
                    processed_frame = frame.copy()
                    label = "Normal View"
                cv2.putText(processed_frame, label, (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                frame_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
                st.session_state.current_frame = frame_rgb
                video_placeholder.image(frame_rgb, channels="RGB", use_container_width=True)
                time.sleep(0.03)
            cap.release()
    else:
        status_placeholder.info("📷 Camera is inactive. Click 'Start Camera' to begin.")
    if st.session_state.screenshot is not None:
        st.subheader("🖼️ Captured Frame - Click Anywhere to Detect Color")
        from streamlit_image_coordinates import streamlit_image_coordinates
        screenshot_img = Image.fromarray(st.session_state.screenshot)
        
        coords = streamlit_image_coordinates(
            st.session_state.screenshot,
            key="clickable_image",
            width=700
        )
        
        # Button controls
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        with col_btn1:
            if st.button("🔙 Return to Live View", key="return_to_live"):
                st.session_state.screenshot = None
                st.rerun()
        with col_btn2:
            if st.button("🔄 Recapture Frame", key="recapture_frame") and st.session_state.current_frame is not None:
                st.session_state.screenshot = st.session_state.current_frame.copy()
                st.rerun()
        with col_btn3:
            if st.button("� Analyse Frame", key="analyse_frame"):
                arr = np.array(screenshot_img)
                avg_color = tuple(np.mean(arr.reshape(-1, 3), axis=0).astype(int))
                color_name = color_assist.get_color_name_advanced(avg_color, tolerance)
                st.success(f"Average Color: {color_name} | RGB: {avg_color}")
                unique_colors = len(np.unique(arr.reshape(-1, 3), axis=0))
                st.info(f"Unique Colors in Frame: {unique_colors}")
        
        # Show detected color below image
        if coords is not None:
            x, y = coords["x"], coords["y"]
            arr = np.array(screenshot_img)
            h, w, _ = arr.shape
            if 0 <= x < w and 0 <= y < h:
                r, g, b = arr[y, x]
                color_name = color_assist.get_color_name_advanced((r, g, b), tolerance)
                st.markdown(f"# 🎨 {color_name.upper()}")
                st.color_picker("Color Preview", f"#{r:02x}{g:02x}{b:02x}", disabled=True)
                st.write(f"**Position:** ({x}, {y}) | **RGB:** ({r}, {g}, {b}) | **Hex:** #{r:02x}{g:02x}{b:02x}")
                if voice_enabled:
                    color_assist.speak_async(f"This color is {color_name}")
        
        # Session Summary expander
        with st.expander("Session Summary"):
            if coords is not None:
                x, y = coords["x"], coords["y"]
                arr = np.array(screenshot_img)
                h, w, _ = arr.shape
                if 0 <= x < w and 0 <= y < h:
                    r, g, b = arr[y, x]
                    color_name_summary = color_assist.get_color_name_advanced((r, g, b), tolerance)
                    st.write(f"Last Detected Color: {color_name_summary} at ({x}, {y})")
                else:
                    st.write("No color detected yet.")
            else:
                st.write("No color detected yet.")
        with st.expander("Color Blindness Info"):
            st.markdown("""
**Color Vision Deficiencies:**
- **Protanopia**: Difficulty distinguishing red colors (affects ~1% of males)
- **Deuteranopia**: Difficulty distinguishing green colors (affects ~1% of males)
- **Tritanopia**: Difficulty distinguishing blue colors (affects ~0.01% of population)

**This tool helps by:**
- Providing audio descriptions of colors
- Simulating how colors appear to different vision types
- Applying correction algorithms (Daltonization)
- Using advanced color naming for better identification
            """)

    # Footer
    st.markdown("---")
    st.markdown("*Advanced Color Blind Assist v3.0 - Making colors accessible for everyone*")

if __name__ == "__main__":
    main()