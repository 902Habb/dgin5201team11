# COM-B Framework Analyzer Web App

A simple web application for analyzing text using the COM-B (Capability, Opportunity, Motivation - Behavior) framework with a Llama 3.2 language model.

## Overview

This application allows users to:
- Input text through a clean, modern web interface
- Analyze the text using the COM-B framework (optimized for speed)
- View the most relevant COM-B category with confidence score and explanation
- See how long the analysis took to complete
- Access previous analyses through a history sidebar

The analysis is performed using a Llama 3.2 language model that identifies the most relevant COM-B category for the input text, focusing on high-confidence results (>60%).

## Requirements

- Python 3.8 or higher
- Virtual environment (recommended)
- Llama 3.2 model file (Llama-3.2-3B-Instruct-Q8_0.gguf)

## Setup Instructions

1. **Clone or download this repository**

2. **Set up a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ensure the database is set up**
   ```bash
   python db_setup.py
   ```

5. **Populate the database with COM-B categories and indicators (if not already done)**
   ```bash
   python populate_comb_data.py
   ```

6. **Run the application**
   ```bash
   python run.py
   ```

7. **Access the web interface**
   Open your browser and navigate to: http://127.0.0.1:5000

## Usage

1. Enter or paste text into the input box
2. Click the "Analyze Text" button
3. Wait for the analysis to complete (typically takes less than a minute)
4. View the results showing the most relevant COM-B category with confidence score and explanation
5. The analysis time is displayed at the top of the results
6. Previous analyses are saved in the sidebar for easy access

## Features

### Analysis History
- All analyses are automatically saved to the sidebar
- Click on any previous analysis to view it again
- History is stored locally in your browser
- Clear history button to remove all saved analyses

### Modern UI
- Clean, responsive design that works on desktop and mobile
- Color-coded categories for easy identification
- Collapsible sidebar on mobile devices
- Confidence bars to visually represent confidence levels

## Performance Optimizations

This application has been highly optimized for speed:

1. **Minimal Prompt Design**
   - Extremely concise prompt with only essential information
   - Only one key indicator per category
   - No examples in the prompt
   - First-sentence-only category descriptions

2. **Model Parameter Optimizations**
   - Reduced context window (1024 tokens)
   - Increased batch size (512)
   - Half-precision key/value cache
   - Limited token selection (top_k=10)
   - Reduced max tokens for generation (512)

3. **Database Optimizations**
   - Preloading all data at initialization
   - Cached category name to ID mapping
   - Simplified JSON extraction

4. **Performance Monitoring**
   - Analysis time tracking and display
   - Model loading time logging

## Files and Structure

- `app.py` - Main Flask application
- `model_handler.py` - Handles interactions with the Llama model
- `db_setup.py` - Database setup and models
- `populate_comb_data.py` - Script to populate the database with COM-B data
- `templates/index.html` - Web interface template
- `requirements.txt` - Python dependencies
- `comb_analyzer.db` - SQLite database file
- `Llama-3.2-3B-Instruct-Q8_0.gguf` - Llama model file

## Notes

- The application is optimized for speed, focusing on identifying the most relevant category
- Only categories with confidence scores above 60% are displayed
- The model uses an extremely minimal prompt to ensure faster processing times
- The model requires approximately 4GB of RAM to run efficiently
- Analysis history is stored in your browser's localStorage 
