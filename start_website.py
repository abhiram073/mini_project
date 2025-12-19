"""
Simple launcher for Traffic Violation Detection App
No emoji characters to avoid Windows encoding issues
"""

import os
import sys
import subprocess

def main():
    print("Traffic Violation Detection App - Launcher")
    print("=" * 50)
    
    # Get current directory
    current_dir = os.getcwd()
    print(f"Current directory: {current_dir}")
    
    # Check if main.py exists
    if not os.path.exists("main.py"):
        print("ERROR: main.py not found!")
        print("Please make sure you're in the project directory")
        input("Press Enter to exit...")
        return False
    
    print("SUCCESS: Found main.py")
    
    # Check if requirements.txt exists
    if not os.path.exists("requirements.txt"):
        print("ERROR: requirements.txt not found!")
        input("Press Enter to exit...")
        return False
    
    print("SUCCESS: Found requirements.txt")
    
    # Install dependencies
    print("\nInstalling dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("SUCCESS: Dependencies installed")
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to install dependencies: {e}")
        input("Press Enter to exit...")
        return False
    
    # Start the application
    print("\n" + "=" * 50)
    print("STARTING YOUR WEBSITE...")
    print("=" * 50)
    print("Your website will be available at:")
    print("http://localhost:5000")
    print("\nTo stop the application, press Ctrl+C")
    print("=" * 50)
    
    try:
        # Import and run the Flask app
        from main import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\nApplication stopped by user")
    except Exception as e:
        print(f"ERROR: Failed to start application: {e}")
        input("Press Enter to exit...")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
