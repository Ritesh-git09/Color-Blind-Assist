# Advanced Color Blind Assist - Model 3

## 🎨 Overview

This is an advanced real-time color detection and assistance system designed to help people with various types of color vision deficiencies. The system provides comprehensive color identification with voice assistance and visual corrections.

## ✨ Features

### 🔍 Enhanced Color Detection
- **Advanced color naming** with 40+ named colors
- **Intelligent color description** using HSV analysis
- **Adjustable sensitivity** for better accuracy
- **Real-time detection** from webcam feed

### 👁️ Color Blindness Support
- **Protanopia** (Red-blind) simulation and correction
- **Deuteranopia** (Green-blind) simulation and correction  
- **Tritanopia** (Blue-blind) simulation and correction
- **Daltonization** color correction algorithms

### 🔊 Voice Assistance
- **Text-to-speech** color announcements
- **Adjustable speech rate** and volume
- **Async speech** for smooth user experience
- **Manual color testing** with voice feedback

### 🎛️ Multiple View Modes
- **Normal View**: Standard camera feed
- **Simulated View**: How colors appear to color blind individuals
- **Corrected View**: Daltonized correction for better color distinction

### 🖥️ User Interface
- **Streamlit-based** modern web interface
- **Real-time camera** integration
- **Interactive controls** and settings
- **Responsive design** for different screen sizes

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7 or higher
- Webcam/Camera access
- Windows/macOS/Linux

### Quick Start

1. **Clone or download** the project files
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application**:
   ```bash
   python launcher.py
   ```
   
   Or directly with Streamlit:
   ```bash
   streamlit run model3_streamlit.py
   ```

### Manual Installation

If you prefer to install packages manually:
```bash
pip install streamlit opencv-python numpy pillow pyttsx3 webcolors
```

## 📖 Usage Instructions

### Getting Started
1. **Launch the application** using the launcher or Streamlit command
2. **Open your web browser** to the provided URL (usually http://localhost:8501)
3. **Click "Start Camera"** to begin video capture
4. **Select your vision type** from the sidebar (Normal, Protanopia, Deuteranopia, or Tritanopia)

### Color Detection
- **Center Detection**: Click "Detect Center Color" to analyze the center pixel
- **Manual Testing**: Use the color picker to test specific colors
- **Voice Feedback**: Enable voice assistance for audio color descriptions

### View Modes
- **Normal**: Standard camera view
- **Simulated**: See how colors appear to color blind individuals
- **Corrected**: Enhanced view with daltonization correction

### Settings
- **Sensitivity**: Adjust color detection accuracy (10-100)
- **Voice**: Enable/disable text-to-speech
- **Vision Type**: Select color blindness type for simulation

## 🔧 Technical Details

### Color Detection Algorithm
1. **RGB Extraction**: Captures RGB values from selected pixels
2. **Webcolors Matching**: Attempts exact color name matching
3. **Extended Dictionary**: Searches 40+ predefined colors
4. **HSV Analysis**: Generates descriptive names for unknown colors
5. **Distance Calculation**: Uses Euclidean distance for closest match

### Color Blindness Simulation
- Uses scientifically accurate **transformation matrices**
- **Protanopia Matrix**: Simulates red color blindness
- **Deuteranopia Matrix**: Simulates green color blindness  
- **Tritanopia Matrix**: Simulates blue color blindness

### Daltonization Correction
- **Error Calculation**: Finds difference between normal and simulated vision
- **Matrix Application**: Applies correction algorithms
- **Enhancement**: Improves color distinction for affected individuals

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

## 🔊 Voice Engine Notes

The voice assistance uses the `pyttsx3` library which:
- **Works offline** (no internet required)
- **Cross-platform** compatible
- **Customizable** voice properties
- **Async operation** for smooth user experience

If voice doesn't work:
1. Check if your system has text-to-speech capabilities
2. Try running: `python -c "import pyttsx3; pyttsx3.init().say('test'); pyttsx3.init().runAndWait()"`
3. On Linux, you may need to install `espeak`: `sudo apt-get install espeak`

## 🐛 Troubleshooting

### Camera Issues
- **Permission denied**: Check camera permissions in your browser/system
- **Camera not found**: Ensure webcam is connected and not used by other applications
- **Poor quality**: Adjust lighting and camera position

### Installation Problems
- **Module not found**: Run `pip install -r requirements.txt`
- **Permission errors**: Try `pip install --user -r requirements.txt`
- **Python version**: Ensure Python 3.7+ is installed

### Performance Issues
- **Slow detection**: Increase detection sensitivity in settings
- **Laggy video**: Close other applications using camera/CPU
- **Memory usage**: Restart the application periodically for long sessions

## 🔮 Future Enhancements

### Planned Features
- **Mobile app** version
- **Batch image processing**
- **Color palette** generation
- **Export functionality** for detected colors
- **Machine learning** improved color recognition
- **Multi-language** voice support

### Advanced Features
- **Object color detection** (not just pixels)
- **Color harmony** suggestions
- **Accessibility compliance** checking
- **Integration** with design software

## 🤝 Contributing

We welcome contributions! Please:
1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Test thoroughly**
5. **Submit a pull request**

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **OpenCV** for computer vision capabilities
- **Streamlit** for the excellent web framework
- **pyttsx3** for text-to-speech functionality
- **webcolors** for color naming standards
- Color blindness research community for scientific color matrices

---

*Advanced Color Blind Assist v3.0 - Making colors accessible for everyone* 🎨👁️🔊