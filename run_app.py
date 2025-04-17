#!/usr/bin/env python3

"""
Trade Tools - Runner Script

This script launches the Trade Tools Streamlit application.
"""

import os
import subprocess
import sys

def main():
    """Main entry point for the application."""
    print("Starting Trade Tools application...")
    
    # Get the path to the main application file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(current_dir, "app", "main.py")
    
    # Check if the file exists
    if not os.path.exists(app_path):
        print(f"Error: Application file not found at {app_path}")
        sys.exit(1)
    
    # Launch the Streamlit application
    try:
        subprocess.run(["streamlit", "run", app_path], check=True)
    except KeyboardInterrupt:
        print("\nApplication stopped by user.")
    except Exception as e:
        print(f"Error running application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 