# model_handler.py

import os
import json
from datetime import datetime
import uuid
from llama_cpp import Llama
from sqlalchemy.orm import Session
from db_setup import setup_database, COMBCategory, Indicator, CodingExample, AnalysisResult

class LlamaModelHandler:
    """
    Handles interactions with the Llama model for COM-B framework coding.
    """
    def __init__(self, model_path, db_session=None):
        """
        Initialize the Llama model handler.
        
        Args:
            model_path: Path to the GGUF model file
            db_session: SQLAlchemy database session
        """
        self.model_path = model_path
        
        # Set up the database session
        if db_session is None:
            self.db_session = setup_database()
        else:
            self.db_session = db_session
            
        # Load the Llama model
        # The n_ctx parameter controls the context window size
        # The n_threads parameter controls CPU parallelization
        print("Loading Llama model... This may take a moment.")
        self.model = Llama(
            model_path=model_path,
            n_ctx=4096,       # Context window size (adjust based on your needs)
            n_threads=6,      # Number of CPU threads to use
            n_gpu_layers=4  
        )
        print("Llama model loaded successfully!")
        
        # Load COM-B categories and related data
        self.categories = self._load_categories()
        self.indicators = self._load_indicators()
        self.examples = self._load_examples()
    
    def _load_categories(self):
        """Load all COM-B categories from the database."""
        categories = {}
        for category in self.db_session.query(COMBCategory).all():
            categories[category.id] = {
                'id': category.id,
                'name': category.name,
                'description': category.description
            }
        return categories
    
    def _load_indicators(self):
        """Load all indicators grouped by category."""
        indicators = {}
        for category_id in self.categories.keys():
            indicators[category_id] = {
                'positive': [],
                'negative': []
            }
            
        for indicator in self.db_session.query(Indicator).all():
            indicators[indicator.category_id][indicator.indicator_type].append(indicator.text)
            
        return indicators
    
    def _load_examples(self):
        """Load all coding examples grouped by category."""
        examples = {}
        for category_id in self.categories.keys():
            examples[category_id] = []
            
        for example in self.db_session.query(CodingExample).all():
            examples[example.category_id].append({
                'text': example.text,
                'explanation': example.explanation
            })
            
        return examples
    
    def _create_coding_prompt(self, text):
        """
        Create a simplified prompt for the Llama model to code the text.
        
        Args:
            text: The transcript text to be coded
            
        Returns:
            A formatted prompt string
        """
        # Start building the prompt - simplified for faster processing
        prompt = "You are an expert qualitative researcher coding interview transcripts using the COM-B framework. "
        prompt += "The COM-B framework consists of 6 categories:\n\n"
        
        # Add category descriptions
        for cat_id, category in self.categories.items():
            prompt += f"{category['name']}: {category['description']}\n"
        
        # Add only the most important indicators for each category
        prompt += "\nKey indicators for each category:\n\n"
        for cat_id, category in self.categories.items():
            prompt += f"{self.categories[cat_id]['name']}:\n"
            # Only include the first 3 positive indicators for brevity
            positive_indicators = self.indicators[cat_id]['positive'][:3]
            for indicator in positive_indicators:
                prompt += f"- {indicator}\n"
            prompt += "\n"
        
        # Add only 1 example per category for brevity
        prompt += "Example for each category:\n\n"
        for cat_id, category in self.categories.items():
            if self.examples[cat_id]:
                example = self.examples[cat_id][0]  # Just take the first example
                prompt += f"{self.categories[cat_id]['name']} example: \"{example['text']}\"\n\n"
        
        # Add the analysis instructions - simplified
        prompt += """
Analyze the following text and identify the TOP TWO COM-B categories it fits into. For each identified category:
1. Explain briefly why it fits that category
2. Provide a confidence level (0-100%)
3. Only include categories where your confidence is ABOVE 60%
4. Format your response as JSON with this structure:
{
    "categories": [
        {
            "category": "Category Name",
            "explanation": "Brief explanation of why it fits that category",
            "confidence": 85
        },
        // Additional categories if applicable
    ]
}

Text to analyze:
"""
        prompt += f"\"{text}\"\n"
        
        return prompt
    
    def code_text(self, text):
        """
        Use the Llama model to code a piece of text according to the COM-B framework.
        
        Args:
            text: The transcript text to be coded
            
        Returns:
            A dictionary containing the coding results
        """
        # Create a unique session ID for this analysis
        session_id = str(uuid.uuid4())
        
        # Create the prompt
        prompt = self._create_coding_prompt(text)
        
        # Generate a response from the model with optimized parameters
        response = self.model.create_completion(
            prompt,
            max_tokens=1024,  # Reduced max tokens for faster response
            temperature=0.1,  # Low temperature for more deterministic outputs
            top_p=0.9,
            stream=False,
            stop=["</s>", "Human:", "User:"]  # Stop tokens to prevent the model from continuing
        )
        
        # Extract the generated text
        generated_text = response["choices"][0]["text"].strip()
        
        # Try to extract JSON from the response
        try:
            # More robust JSON extraction
            # First, look for the last complete JSON object in the response
            # This handles cases where the model might generate multiple JSON objects
            # or include explanatory text before/after the JSON
            
            # Find all opening braces
            open_brace_indices = [i for i, char in enumerate(generated_text) if char == '{']
            
            # If no JSON structure found
            if not open_brace_indices:
                return {"error": "Could not extract valid JSON from model response", "raw_response": generated_text}
            
            # Try each potential JSON object, starting from the last one
            for start_index in reversed(open_brace_indices):
                # Track nested braces to find the matching closing brace
                brace_count = 0
                end_index = -1
                
                for i in range(start_index, len(generated_text)):
                    if generated_text[i] == '{':
                        brace_count += 1
                    elif generated_text[i] == '}':
                        brace_count -= 1
                        
                    if brace_count == 0:
                        end_index = i + 1
                        break
                
                if end_index > 0:
                    # We found a complete JSON object
                    json_str = generated_text[start_index:end_index]
                    try:
                        results = json.loads(json_str)
                        # Check if this JSON has the expected structure
                        if "categories" in results:
                            # Filter out categories with confidence <= 60%
                            if "categories" in results:
                                results["categories"] = [
                                    cat for cat in results["categories"] 
                                    if cat.get("confidence", 0) > 60
                                ]
                            
                            # Store results in the database
                            self._store_results(text, results, session_id)
                            
                            # Add the session ID to the results
                            results["session_id"] = session_id
                            
                            return results
                    except json.JSONDecodeError:
                        # This JSON object was invalid, try the next one
                        continue
            
            # If we get here, we couldn't find a valid JSON object with the expected structure
            return {"error": "Could not extract valid JSON with expected structure from model response", 
                    "raw_response": generated_text}
            
        except Exception as e:
            # If JSON parsing fails, return an error
            return {
                "error": f"Error processing model response: {str(e)}",
                "raw_response": generated_text
            }
    
    def _store_results(self, text, results, session_id):
        """
        Store coding results in the database.
        
        Args:
            text: The original text that was coded
            results: The coding results
            session_id: A unique identifier for this analysis session
        """
        # Check if results contain the expected structure
        if "categories" not in results:
            return
        
        # Get category IDs by name for easier lookup
        category_id_by_name = {category['name']: cat_id for cat_id, category in self.categories.items()}
        
        # Store each category result
        for result in results["categories"]:
            category_name = result.get("category")
            confidence = result.get("confidence", 0)
            
            # Skip if category name is not found
            if category_name not in category_id_by_name:
                continue
            
            # Create and add the analysis result
            analysis_result = AnalysisResult(
                text_quote=text,
                category_id=category_id_by_name[category_name],
                confidence=confidence,
                session_id=session_id
            )
            self.db_session.add(analysis_result)
        
        # Commit the changes to the database
        self.db_session.commit()

def test_model():
    # Path to your Llama model file
    # Use the exact filename as shown in your file structure
    model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Llama-3.2-3B-Instruct-Q8_0.gguf")
    
   # Create model handler
    handler = LlamaModelHandler(model_path)
    
    # Test text to code
    test_text = "I want to eat healthier, but I don't know how to prepare nutritious meals."
    
    # Run the coding
    results = handler.code_text(test_text)
    
    # Print results
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    test_model()