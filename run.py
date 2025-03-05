#!/usr/bin/env python
"""
Simple script to run the COM-B Framework Analyzer web application.
"""
import os
import webbrowser
import threading
import time
from app import app

def open_browser():
    """Open the browser after a short delay to ensure the server is running."""
    time.sleep(1.5)
    webbrowser.open('http://127.0.0.1:5000')

if __name__ == "__main__":
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Set larger max content length for JSON responses (to handle history)
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB
    
    # Start a thread to open the browser
    threading.Thread(target=open_browser).start()
    
    # Run the Flask app
    print("Starting COM-B Framework Analyzer web application...")
    print("Opening browser to: http://127.0.0.1:5000")
    app.run(debug=True) 