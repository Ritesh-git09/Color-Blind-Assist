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
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📹 Live Camera Feed")
        
        # Initialize camera state
        if 'camera_active' not in st.session_state:
            st.session_state.camera_active = False
        
        # Camera controls
        camera_col1, camera_col2, camera_col3, camera_col4 = st.columns(4)
        with camera_col1:
            if st.button("▶️ Start Camera"):
                st.session_state.camera_active = True
        with camera_col2:
            if st.button("⏹️ Stop Camera"):
                st.session_state.camera_active = False
        with camera_col3:
            if st.button("📸 Capture Frame") and st.session_state.current_frame is not None:
                st.session_state.screenshot = st.session_state.current_frame.copy()
                st.experimental_rerun()
        with camera_col4:
            detect_center = st.button("🎯 Detect Center Color")
        
        # Video display area
        video_placeholder = st.empty()
        
        # Status display
        status_placeholder = st.empty()
    
    with col2:
        st.header("🎯 Color Information")
        
        # Color display area
        color_display_placeholder = st.empty()
        
        # Instructions
        st.markdown("""
        **Instructions:**
        1. Click 'Start Camera' to begin
        2. Click 'Detect Center Color' to analyze the center pixel
        3. Use sidebar to adjust settings
        4. Choose different vision types to see how colors appear
        
        **Features:**
        - Real-time color detection
        - Voice assistance  
        - Color blindness simulation
        - Color correction (Daltonization)
        - Advanced color naming
        """)
        
        # Manual color input
        st.subheader("🎨 Manual Color Test")
        manual_color = st.color_picker("Pick a color to test", "#ff0000")
        if st.button("🔊 Speak Manual Color"):
            # Convert hex to RGB
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
            
            # Store the current frame for access outside the loop
            if 'current_frame' not in st.session_state:
                st.session_state.current_frame = None
            # Live feed loop
            while st.session_state.camera_active:
                ret, frame = cap.read()
                if not ret:
                    status_placeholder.error("Failed to read from camera.")
                    break
                frame = cv2.flip(frame, 1)
                # Apply selected view mode
                if cb_type and view_mode == "Simulated":
                    processed_frame = color_assist.simulate_color_blindness(frame, cb_type)
                    label = f"Simulated {cb_selection}"
                elif cb_type and view_mode == "Corrected (Daltonized)":
                    processed_frame = color_assist.daltonize_image(frame, cb_type)
                    label = f"Corrected {cb_selection}"
                else:
                    processed_frame = frame.copy()
                    label = "Normal View"
                # Add label to frame
                cv2.putText(processed_frame, label, (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                # Convert BGR to RGB for Streamlit
                frame_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
                # Update the current frame in session state
                st.session_state.current_frame = frame_rgb
                # Show live feed
                video_placeholder.image(frame_rgb, channels="RGB", use_column_width=True)
                time.sleep(0.03)  # ~30 FPS
            cap.release()
    else:
        status_placeholder.info("📷 Camera is inactive. Click 'Start Camera' to begin.")
    # Screenshot and pixel selection
    if st.session_state.screenshot is not None:
        st.subheader("🖼️ Captured Frame - Select Pixel to Detect Color")
        # Display screenshot and get click
        screenshot_img = Image.fromarray(st.session_state.screenshot)
        # Use Streamlit's image coordinates (simulate click detection)
        st.image(st.session_state.screenshot, channels="RGB", use_column_width=True)
        st.info("Use the table below to select a pixel and detect its color")
        
        # Button to clear screenshot and return to live view
        if st.button("Return to Live View"):
            st.session_state.screenshot = None
            st.experimental_rerun()
        # Use st.experimental_data_editor for click detection (workaround)
        # Convert image to DataFrame for click selection
        import pandas as pd
        arr = np.array(screenshot_img)
        h, w, _ = arr.shape
        # Downsample for performance
        arr_small = arr[::max(h//200,1), ::max(w//200,1)]
        df = pd.DataFrame({f"x{i}": arr_small[:,i,0] for i in range(arr_small.shape[1])})
        selected = st.experimental_data_editor(df, num_rows="dynamic", use_container_width=True)
        st.write("Select a cell in the table above to pick a pixel (row/column)")
        if selected is not None and hasattr(selected, 'iloc'):
            # Get selected cell coordinates
            sel_row = selected.index[0]
            sel_col = selected.columns.get_loc(selected.columns[0])
            # Map back to original image coordinates
            y = sel_row * max(h//200,1)
            x = sel_col * max(w//200,1)
            b, g, r = arr[y, x]
            color_name = color_assist.get_color_name_advanced((r, g, b), tolerance)
            with color_display_placeholder.container():
                st.color_picker("Detected Color", f"#{r:02x}{g:02x}{b:02x}", disabled=True)
                st.write(f"**Color Name:** {color_name}")
                st.write(f"**RGB Values:** ({r}, {g}, {b})")
                st.write(f"**Position:** ({x}, {y})")
                if voice_enabled:
                    if st.button("🔊 Speak Color", key="speak_pixel_detected"):
                        color_assist.speak_async(f"The selected color is {color_name}")
    
    # Additional features section
    st.header("📊 Additional Features")
    
    feature_col1, feature_col2, feature_col3 = st.columns(3)
    
    with feature_col1:
        st.subheader("🔬 Color Analysis")
        if st.button("Analyze Current Frame"):
            st.info("Analyzing color distribution in the current frame...")
    
    with feature_col2:
        st.subheader("📋 Session Info")
        if st.button("Show Session Stats"):
            st.info(f"""
            **Current Session:**
            - Vision Type: {cb_selection}
            - View Mode: {view_mode}
            - Voice: {'Enabled' if voice_enabled else 'Disabled'}
            - Sensitivity: {tolerance}
            """)
    
    with feature_col3:
        st.subheader("🎓 Information")
        with st.expander("Color Blindness Info"):
            st.write("""
            **Color Vision Deficiencies:**
            - **Protanopia**: Difficulty distinguishing red colors (affects ~1% of males)
            - **Deuteranopia**: Difficulty distinguishing green colors (affects ~1% of males)  
            - **Tritanopia**: Difficulty distinguishing blue colors (affects ~0.01% of population)
            
            This tool helps by:
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