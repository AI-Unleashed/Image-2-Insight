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

    tools = [
    {
        "name": "extract_invoice_info",
        "description": "Extracts key information from the invoice.",
        "input_schema": {
            "type": "object",
            "properties": {
                "invoice_number": {"type": "string", "description": "The invoice number."},
                "invoice_date": {"type": "string", "description": "The date of the invoice."},
                "total_amount": {"type": "string", "description": "The total amount on the invoice. Don't include the $ sign"},
                "vendor_name": {"type": "string", "description": "The vendor name on the invoice."},
                "vendor_address": {"type": "string", "description": "The vendor address on the invoice."},
                "payment_account_number": {"type": "string", "description": "The payment account number on the invoice."},
                "due_date": {"type": "string", "description": "The due date for payment on the invoice. if no date is present calculate it from the invoice date and the payment terms"}
            },
            "required": ["invoice_number", "invoice_date", "total_amount", "vendor_name", "vendor_address", "payment_account_number", "due_date"]
        }
    }
]

    response = anthropic.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        tools=tools,
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
                        "text": "Analyze the invoice image and extract the key data requested by the tool.Use the extract_invoice_info tool to provide the extracted information.  If the image is not an invoice or data missing still return using the tool with values of null."
                    }
                ]
            }
        ]
    )

    # Parse and return the JSON response
    for content in response.content:
        if content.type == 'tool_use':
            return content.input
    return None


# Example usage:
# result = extract_text_from_image("path/to/your/image.jpg")
# print(result)
