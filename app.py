import os
import json
import time
from flask import Flask, render_template, request, jsonify
from model_handler import LlamaModelHandler

app = Flask(__name__)

# Initialize the model handler (lazy loading - will only load when needed)
model_handler = None

def get_model_handler():
    """
    Lazy initialization of the model handler to avoid loading the model
    until it's actually needed.
    """
    global model_handler
    if model_handler is None:
        print("Initializing model handler...")
        start_time = time.time()
        model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                "Llama-3.2-3B-Instruct-Q8_0.gguf")
        model_handler = LlamaModelHandler(model_path)
        load_time = time.time() - start_time
        print(f"Model loaded in {load_time:.2f} seconds")
    return model_handler

@app.route('/')
def index():
    """Render the main page with the text input form."""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Analyze the submitted text using the Llama model and return the results.
    The model is optimized for speed and will return the most relevant category
    with confidence score above 60%.
    """
    # Get the text from the form
    text = request.form.get('text', '')
    
    if not text:
        return jsonify({'error': 'No text provided'})
    
    try:
        # Get the model handler and analyze the text
        handler = get_model_handler()
        
        # Time the analysis
        start_time = time.time()
        results = handler.code_text(text)
        analysis_time = time.time() - start_time
        
        # Add timing information to the results
        results['analysis_time'] = f"{analysis_time:.2f} seconds"
        print(f"Analysis completed in {analysis_time:.2f} seconds")
        
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': f'Error analyzing text: {str(e)}'})

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Set larger max content length for JSON responses (to handle history)
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB
    
    # Run the Flask app
    app.run(debug=True) 