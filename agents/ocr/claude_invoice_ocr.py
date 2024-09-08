import base64
import json
import os
import configparser
from anthropic import Anthropic
from typing import Dict, Any

def extract_text_from_image(image_path: str) -> Dict[str, Any]:
    """
    Extract text from an image using Claude 3.5 Sonnet API.

    Args:
        image_path (str): Path to the image file.

    Returns:
        Dict[str, Any]: JSON response containing extracted text and metadata.
    """
    # Read API key from config file
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config', '.anthropic_config')
    config.read(config_path)
    api_key = config['Anthropic']['api_key']

    anthropic = Anthropic(api_key=api_key)

    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

    response = anthropic.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": encoded_image
                        }
                    },
                    {
                        "type": "text",
                        "text": "This image is an invoice. Extract key invoice details in JSON format. Do not include any other text."
                    }
                ]
            }
        ]
    )

    # Parse and return the JSON response
    extracted_text = json.loads(response.content[0].text)
    
    return extracted_text

# Example usage:
# result = extract_text_from_image("path/to/your/image.jpg")
# print(result)
