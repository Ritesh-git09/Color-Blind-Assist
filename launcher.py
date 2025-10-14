import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False

def run_streamlit_app():
    """Run the Streamlit application"""
    try:
        subprocess.run(["streamlit", "run", "model3_streamlit.py"])
    except FileNotFoundError:
        print("❌ Streamlit not found. Installing requirements first...")
        if install_requirements():
            subprocess.run(["streamlit", "run", "model3_streamlit.py"])
        else:
            print("❌ Failed to install requirements. Please install manually.")

if __name__ == "__main__":
    print("🎨 Advanced Color Blind Assist Launcher")
    print("=" * 40)
    
    # Check if requirements.txt exists
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found!")
        sys.exit(1)
    
    # Check if model3_streamlit.py exists
    if not os.path.exists("model3_streamlit.py"):
        print("❌ model3_streamlit.py not found!")
        sys.exit(1)
    
    print("🚀 Starting Advanced Color Blind Assist...")
    run_streamlit_app()