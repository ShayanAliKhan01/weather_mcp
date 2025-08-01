#!/usr/bin/env python3
"""
Streamlit launcher for Weather MCP Assistant
"""

import subprocess
import sys
import os

def main():
    print("🚀 Starting Weather MCP Assistant with Streamlit...")
    print("📱 Opening web interface...")
    
    # Run streamlit
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
        "--server.port", "8501",
        "--server.address", "localhost"
    ])

if __name__ == "__main__":
    main() 