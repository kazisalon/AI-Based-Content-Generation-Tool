from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import google.generativeai as genai
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Load environment variables and configure API
def init_api():
    try:
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file")
        
        genai.configure(api_key=api_key)
        return genai.GenerativeModel('gemini-pro')
    except Exception as e:
        logger.error(f"Failed to initialize API: {str(e)}")
        raise

# Initialize the model
try:
    model = init_api()
except Exception as e:
    logger.error(f"Application startup failed: {str(e)}")
    model = None

def create_prompt(content_type, topic):
    prompts = {
        '1': {
            'text': f"Write an engaging and informative blog post about {topic}. Include an introduction, main points, and conclusion.",
            'temp': 0.7
        },
        '2': {
            'text': f"Create an attention-grabbing social media post about {topic} that will drive engagement. Include relevant hashtags.",
            'temp': 0.8
        },
        '3': {
            'text': f"Tell a funny and creative joke about {topic}. Make it original and entertaining.",
            'temp': 0.9
        },
        '4': {
            'text': f"Create a clear, step-by-step tutorial about {topic}. Include introduction, requirements, steps, and tips for success.",
            'temp': 0.6
        }
    }
    return prompts.get(content_type, {'text': '', 'temp': 0.7})

def save_content(content, content_type):
    try:
        # Create outputs directory if it doesn't exist
        os.makedirs('outputs', exist_ok=True)
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        content_types = {
            '1': 'blog',
            '2': 'social',
            '3': 'joke',
            '4': 'tutorial'
        }
        type_name = content_types.get(content_type, 'content')
        filename = f"outputs/{type_name}_{timestamp}.txt"
        
        # Save the content
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filename
    except Exception as e:
        logger.error(f"Failed to save content: {str(e)}")
        raise

@app.route('/generate', methods=['POST'])
def generate_content():
    if not model:
        return jsonify({'error': 'API not properly initialized'}), 500
    
    try:
        data = request.get_json()
        content_type = data.get('content_type')
        topic = data.get('topic')
        
        if not content_type or not topic:
            return jsonify({'error': 'Missing required fields'}), 400
        
        prompt_data = create_prompt(content_type, topic)
        if not prompt_data['text']:
            return jsonify({'error': 'Invalid content type'}), 400
        
        response = model.generate_content(
            prompt_data['text'],
            generation_config=genai.types.GenerationConfig(
                temperature=prompt_data['temp']
            )
        )
        
        return jsonify({'content': response.text})
    
    except Exception as e:
        logger.error(f"Content generation failed: {str(e)}")
        return jsonify({'error': 'Failed to generate content'}), 500

@app.route('/save', methods=['POST'])
def save_content_endpoint():
    try:
        data = request.get_json()
        content = data.get('content')
        content_type = data.get('content_type')
        
        if not content or not content_type:
            return jsonify({'error': 'Missing required fields'}), 400
        
        filename = save_content(content, content_type)
        return jsonify({'filename': filename})
    
    except Exception as e:
        logger.error(f"Content saving failed: {str(e)}")
        return jsonify({'error': 'Failed to save content'}), 500

if __name__ == '__main__':
    app.run(debug=True)