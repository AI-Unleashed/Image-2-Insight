import os
from datetime import datetime
from agents.ocr.claude_ocr import extract_text_from_image

def main():
    # Specify the path to the data folder
    data_folder = "data/input_images"
    
    # Get a list of image files in the data folder
    image_files = [f for f in os.listdir(data_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
    
    if not image_files:
        print("No image files found in the data folder.")
        return
    
    # Create the output folder if it doesn't exist
    output_folder = "data/extracted_text"
    os.makedirs(output_folder, exist_ok=True)

    # Process each image file
    for image_file in image_files:
        image_path = os.path.join(data_folder, image_file)
        print(f"Processing image: {image_file}")
        
        try:
            result = extract_text_from_image(image_path)
            print("Extracted text:")
            print(result['extracted_text'])
            
            # Generate filename with datetime stamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"{timestamp}_{os.path.splitext(image_file)[0]}.txt"
            output_path = os.path.join(output_folder, output_filename)
            
            # Save extracted text to file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result['extracted_text'])
            
            print(f"Saved extracted text to: {output_path}")
            print("-" * 50)
        except Exception as e:
            print(f"Error processing {image_file}: {str(e)}")
            print("-" * 50)

if __name__ == "__main__":
    main()
