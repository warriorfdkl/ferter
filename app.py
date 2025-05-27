from flask import Flask, render_template, request, jsonify
import os
from PIL import Image
import io
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Translations for responses
TRANSLATIONS = {
    'en': {
        'unknown_food': 'Unknown food item',
        'calories': '300-400',
        'confidence': 'medium'
    },
    'ru': {
        'unknown_food': 'Неизвестный продукт',
        'calories': '300-400',
        'confidence': 'средняя'
    }
}

def estimate_calories(image, language='en'):
    # This is a placeholder. In a real application, you would:
    # 1. Use a food detection model to identify the food
    # 2. Use a calorie estimation API or database
    # For now, we'll return a dummy response
    return {
        "calories": TRANSLATIONS[language]['calories'],
        "food_type": TRANSLATIONS[language]['unknown_food'],
        "confidence": TRANSLATIONS[language]['confidence']
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process-image', methods=['POST'])
def process_image():
    try:
        # Get the image data and language from the request
        data = request.json
        image_data = data['image']
        language = data.get('language', 'en')
        
        # Validate language
        if language not in TRANSLATIONS:
            language = 'en'
        
        # Remove the data URL prefix
        image_data = image_data.split(',')[1]
        
        # Convert base64 to image
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        
        # Process the image and estimate calories
        result = estimate_calories(image, language)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 