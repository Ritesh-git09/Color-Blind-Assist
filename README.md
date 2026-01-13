# Advanced Color Blind Assist - Model 3

## 🎨 Overview

This is an advanced real-time color detection and assistance system designed to help people with various types of color vision deficiencies. The system provides comprehensive color identification with voice assistance, visual corrections, and interactive color analysis features.

**Version:** 3.0 (Latest Update: January 2026)

## ✨ Features

### 🔍 Enhanced Color Detection
- **Advanced color naming** with 40+ predefined colors
- **Intelligent color description** using HSV analysis
- **Adjustable sensitivity** for better accuracy (10-100 range)
- **Real-time detection** from webcam feed
- **Click-to-detect** functionality on captured frames
- **Batch frame analysis** with unique color counting

### 👁️ Color Blindness Support
- **Protanopia** (Red-blind) simulation and correction
- **Deuteranopia** (Green-blind) simulation and correction  
- **Tritanopia** (Blue-blind) simulation and correction
- **Daltonization** color correction algorithms for improved distinction
- **Scientific color transformation matrices** for accurate simulation

### 🔊 Voice Assistance
- **Text-to-speech** color announcements using pyttsx3
- **Adjustable speech rate** and volume
- **Async speech** for smooth, non-blocking user experience
- **Manual color testing** with voice feedback
- **Cross-platform** voice engine (no internet required)

### 🎛️ Multiple View Modes
- **Normal View**: Standard camera feed
- **Simulated View**: How colors appear to color blind individuals
- **Corrected View**: Daltonized correction for better color distinction
- **Frame Capture**: Freeze frames for detailed color analysis

### 📸 Camera Controls
- **Start/Stop Camera**: Control live video feed
- **Capture Frame**: Freeze current frame for analysis
- **Interactive Frame Analysis**: Click anywhere to detect color
- **Color Preview**: Visual color picker for detected colors
- **Session Summary**: Track detected colors and positions

### 🖥️ User Interface
- **Streamlit-based** modern, responsive web interface
- **Real-time camera** integration with OpenCV
- **Interactive controls** and customizable settings
- **Expandable information panels** for detailed reference
- **One-click color testing** with comprehensive feedback

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7 or higher (3.9+ recommended)
- Webcam/Camera with proper permissions
- Windows/macOS/Linux operating system
- 200MB+ disk space for dependencies

### Quick Start

1. **Clone or download** the project files to your computer
2. **Navigate to the project directory**:
   ```bash
   cd "Color Blind Assist"
   ```
3. **Run the launcher** (easiest method):
   ```bash
   python launcher.py
   ```
   
   Or run directly with Streamlit:
   ```bash
   streamlit run model3_streamlit.py
   ```

4. **Open in browser**: The application will automatically open at `http://localhost:8501`

### Automated Installation

The launcher script (`launcher.py`) will automatically:
- Check for required dependencies
- Install missing packages from `requirements.txt`
- Launch the Streamlit application

### Manual Installation

If you prefer to install packages manually:

```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install streamlit>=1.28.0 opencv-python>=4.8.0 numpy>=1.24.0 Pillow>=10.0.0 pyttsx3>=2.90 webcolors>=1.13 streamlit-image-coordinates
```

## 📖 Usage Instructions

### Getting Started
1. **Launch the application** using `python launcher.py` or Streamlit command
2. **Open your web browser** to `http://localhost:8501`
3. **Select your vision type** from the sidebar (Normal, Protanopia, Deuteranopia, or Tritanopia)
4. **Choose your view mode** (Normal, Simulated, or Corrected)
5. **Click "▶️ Start Camera"** to begin video capture

### Camera Operations
1. **Start Camera**: Click "▶️ Start Camera" to activate the webcam
2. **Capture Frame**: Click "📸 Capture Frame" to freeze the current video feed
3. **Stop Camera**: Click "⏹️ Stop Camera" to deactivate the camera
4. **Return to Live View**: Click "🔙 Return to Live View" from the captured frame to go back to live feed

### Color Detection Methods

#### Method 1: Interactive Click Detection
1. Capture a frame using "📸 Capture Frame"
2. **Click anywhere on the captured image** to instantly detect the color at that position
3. View the color name, RGB values, and hexadecimal code
4. Voice assistance will announce the detected color (if enabled)

#### Method 2: Frame Analysis
1. Capture a frame and click "Analyse Frame"
2. View the average frame color and total unique colors in the image
3. Useful for overall color composition analysis

#### Method 3: Manual Color Testing
1. Use the color picker under "🎨 Manual Color Test" section
2. Click "🔊 Speak Manual Color" for voice feedback
3. Test specific colors without camera input

### Settings & Controls

#### Sidebar Settings
- **Color Vision Type**: Select detection and simulation mode
  - Normal Vision: Standard color perception
  - Protanopia (Red-blind): Red color blindness simulation
  - Deuteranopia (Green-blind): Green color blindness simulation
  - Tritanopia (Blue-blind): Blue color blindness simulation

- **View Mode**: Choose visualization
  - Normal: Standard camera feed
  - Simulated: View as color blind person sees
  - Corrected (Daltonized): Enhanced colors for better distinction

- **Voice Assistance**: Enable/disable audio color announcements

- **Color Detection Sensitivity**: Adjust accuracy (10-100)
  - Lower values: More strict color matching
  - Higher values: More lenient matching

### Session Features

#### Session Summary
- Tracks the last detected color and its position
- Maintains detection history during the session
- Helpful for comparing multiple colors

#### Color Blindness Information
- Detailed explanations of each color vision deficiency
- Statistics on prevalence in population
- Information on how the tool helps

## 🔧 Technical Details

### Color Detection Algorithm
1. **RGB Extraction**: Captures precise RGB values from clicked pixels
2. **Webcolors Library**: Attempts to match exact CSS/X11 color names
3. **Extended Dictionary**: Searches 40+ predefined color mappings
4. **HSV Analysis**: Converts to HSV color space for descriptive analysis
5. **Distance Calculation**: Uses Euclidean distance formula for closest match
6. **Tolerance-Based Matching**: Adjusts sensitivity based on user slider
7. **Fallback Naming**: Generates descriptive names (e.g., "pale vivid cyan") for unknown colors

**Color Naming Priority:**
- Exact webcolors match → Extended color dictionary → HSV-based description

### Color Blindness Simulation
Uses **scientifically validated transformation matrices** based on published color vision research:

- **Protanopia Matrix**: Simulates red color blindness
  - Red channel information reduced
  - Green and blue channels adjusted
  - Affects approximately 1% of males

- **Deuteranopia Matrix**: Simulates green color blindness
  - Green channel information reduced
  - Red and blue channels adjusted
  - Affects approximately 1% of males

- **Tritanopia Matrix**: Simulates blue-yellow color blindness
  - Blue channel information reduced
  - Red and green channels adjusted
  - Rare condition affecting ~0.01% of population

### Daltonization Correction Algorithm
1. **Error Calculation**: Computes difference between normal and simulated color perception
2. **Error Amplification**: Multiplies error difference by correction factor (0.7)
3. **Application**: Adds amplified error back to original image
4. **Clipping**: Constrains values to valid RGB range (0-255)

**Result**: Colors become more distinguishable for color blind individuals

### Color Space Conversions
- **RGB to HSV**: For hue-based color descriptions
- **RGB to Hex**: For web color representation
- **Hex to RGB**: For color picker compatibility

## 📁 Project Structure

```
Color Blind Assist/
├── model1.py              # Original basic model
├── model2.py              # Intermediate model with Bayer filter
├── model3.py              # Advanced model (OpenCV-based)
├── model3_streamlit.py    # Advanced model (Streamlit UI)
├── launcher.py            # Easy launcher script
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🆕 Improvements over Model 1 & 2

### Enhanced Features
- **Streamlit UI** instead of OpenCV windows
- **Three types** of color blindness support (vs. 1 in previous models)
- **Advanced color naming** with 40+ colors (vs. 14-26 in previous)
- **Daltonization correction** algorithms
- **Better user interface** with real-time controls
- **Improved voice engine** with async processing

### Technical Improvements
- **More accurate** color detection algorithms
- **Scientific color matrices** for realistic simulation
- **Web-based interface** for better accessibility
- **Modular code structure** for easier maintenance
- **Error handling** and user feedback

## 🔊 Voice Engine Configuration

The voice assistance uses the **pyttsx3 library** which:
- **Works offline** (no internet connection required)
- **Cross-platform compatible** (Windows, macOS, Linux)
- **No account needed** (unlike cloud-based services)
- **Customizable rate** and volume properties
- **Async operation** for smooth user experience without blocking UI

### Voice Configuration
- **Speech Rate**: Set to 150 words per minute (adjustable in code)
- **Volume Level**: Set to 90% to ensure clarity

### Troubleshooting Voice Issues

**Voice not working?**
1. Check system volume is not muted
2. Verify speakers/headphones are connected
3. Test voice manually in sidebar: Enable "Voice Assistance"
4. Check system text-to-speech is enabled

**Linux Users:**
- Install eSpeak engine: `sudo apt-get install espeak`
- Optional: `sudo apt-get install python3-pyaudio`

**macOS Users:**
- System should have built-in text-to-speech support
- If not working, check System Preferences > Accessibility > Speech

**Windows Users:**
- Windows 10/11 includes Narrator for text-to-speech
- Check Settings > Accessibility > Text-to-speech

## 🐛 Troubleshooting Guide

### Camera Issues
**Problem**: Camera permission denied
- **Solution**: Check browser/system camera permissions
- Windows: Settings > Privacy & Security > Camera
- macOS: System Preferences > Security & Privacy > Camera
- Linux: Check permission via `ls -l /dev/video0`

**Problem**: "Cannot access camera" error
- **Solution**: 
  - Ensure webcam is connected and powered
  - Check no other application is using the camera
  - Restart the application
  - Try a different USB port (if external camera)

**Problem**: Poor video quality or lag
- **Solution**:
  - Improve lighting conditions
  - Close unnecessary applications
  - Reduce video processing complexity
  - Check CPU/RAM usage

### Installation Problems

**Problem**: "Module not found" error
- **Solution**: Run `pip install -r requirements.txt`
- If still failing: `pip install --upgrade pip` then retry

**Problem**: Permission denied during installation
- **Solution**: Use `pip install --user -r requirements.txt`
- Or use virtual environment: `python -m venv env` then activate

**Problem**: Python version incompatibility
- **Solution**: Ensure Python 3.7+ installed
- Check: `python --version`
- Install Python 3.9+: https://www.python.org/downloads/

### Performance Issues

**Problem**: Slow color detection
- **Solution**: Increase sensitivity slider (up to 100)
- Simplify the image (reduce lighting variations)
- Close other applications

**Problem**: Laggy camera feed
- **Solution**:
  - Reduce video quality/resolution
  - Close background applications
  - Check internet speed (for any remote processing)
  - Restart the application

**Problem**: High memory usage
- **Solution**:
  - Restart the application after 1-2 hours
  - Close other browser tabs
  - Limit camera resolution settings

### Color Detection Issues

**Problem**: Incorrect color names
- **Solution**: 
  - Adjust sensitivity slider (lower = stricter)
  - Improve lighting conditions
  - Move closer to the object
  - Check if color is in extended color dictionary

**Problem**: Voice not announcing colors
- **Solution**:
  - Enable "Voice Assistance" checkbox in sidebar
  - Check system volume is not muted
  - Test voice with manual color picker
  - See Voice Engine Troubleshooting section

### Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| "Cannot access camera" | Camera unavailable | Check camera connection & permissions |
| "ModuleNotFoundError" | Missing package | Run `pip install -r requirements.txt` |
| "Port 8501 already in use" | Streamlit instance running | Kill process or use `streamlit run ... --server.port 8502` |
| "Failed to read from camera" | Camera read failure | Restart app & check camera connection |

## 🔮 Future Enhancements

### Planned Features
- **Mobile app** version (iOS/Android)
- **Batch image processing** for multiple files
- **Color palette** generation from images
- **Export functionality** for detected colors (CSV/JSON)
- **Machine learning** improved color recognition
- **Multi-language** voice support
- **Dark mode** UI theme
- **Color blindness test** feature

### Advanced Features in Development
- **Object color detection** (identify colors of specific objects, not just pixels)
- **Color harmony** suggestions for design
- **Accessibility compliance** checking (WCAG standards)
- **Integration** with design software (Adobe, Figma plugins)
- **Real-time video filters** with color enhancement
- **Deep learning models** for better color recognition
- **Gesture controls** for hands-free operation
- **Multi-camera support** for simultaneous detection

## 🤝 Contributing

We welcome contributions from the community! To contribute:

1. **Fork the repository** on GitHub
2. **Create a feature branch** for your changes
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** with clear, descriptive commits
4. **Test thoroughly** 
   - Test with different vision types
   - Test with various lighting conditions
   - Verify cross-platform compatibility
5. **Submit a pull request** with detailed description of changes

### Development Setup
```bash
# Clone the repository
git clone <repository-url>
cd "Color Blind Assist"

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt

# Run the application
streamlit run model3_streamlit.py
```

### Code Style
- Follow PEP 8 guidelines
- Use descriptive variable names
- Add comments for complex logic
- Ensure code is cross-platform compatible

## 📄 License

This project is open source and available under the **MIT License**. 

**Summary**: You are free to:
- Use this software for personal or commercial purposes
- Modify and distribute the code
- Include in your own projects

**Condition**: Include the original license notice

See LICENSE file for complete details.

## 📊 Project Statistics

- **Language**: Python 3.7+
- **Framework**: Streamlit 1.28.0+
- **Lines of Code**: 400+ (main application)
- **Color Support**: 40+ named colors
- **Color Vision Types**: 3 types of color blindness
- **Vision Simulation**: Scientific transformation matrices
- **Voice Engine**: pyttsx3 (offline capable)
- **Cross-Platform**: Windows, macOS, Linux

## 🙏 Acknowledgments

This project is made possible by:

- **OpenCV** - Industrial-grade computer vision library
- **Streamlit** - Excellent web framework for data applications
- **pyttsx3** - Cross-platform text-to-speech functionality
- **webcolors** - W3C CSS color name standards
- **NumPy** - Scientific computing in Python
- **Pillow** - Python Imaging Library

### Research & References

- Color blindness research community for validated transformation matrices
- Scientific literature on color vision deficiencies
- WCAG accessibility guidelines
- Web color standards (W3C, CSS specifications)

### Special Thanks

- All users who have provided feedback and feature requests
- Contributors who have helped improve the application
- Medical and accessibility professionals for guidance

---

## 📞 Support & Contact

**Having issues?**
1. Check the [Troubleshooting Guide](#-troubleshooting-guide)
2. Review the [FAQ section](#troubleshooting-guide)
3. Check GitHub Issues for similar problems
4. Submit a new issue with:
   - Your operating system
   - Python version
   - Error message/screenshot
   - Steps to reproduce

**Want to contribute?**
- See [Contributing](#-contributing) section
- Fork the repository and submit pull requests
- Suggest features via GitHub Issues

---

*Advanced Color Blind Assist v3.0 - Making colors accessible for everyone* 

**Last Updated**: January 2026 | **Status**: Active Development | **License**: MIT