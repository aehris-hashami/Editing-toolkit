import sys
import pytesseract
import cv2
import numpy as np
from pdf2image import convert_from_path
import re

def preprocess_image(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Apply adaptive thresholding
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    
    return thresh

def clean_text(text):
    # Remove extra spaces and line breaks
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Correct common OCR errors (e.g., replace '0' with 'O')
    text = text.replace('0', 'O')
    
    return text

def pdf_to_text(input_pdf_path, output_txt_path):
    images = convert_from_path(input_pdf_path, dpi=300)
    
    text = ""
    for i, img in enumerate(images):
        # Convert PIL image to OpenCV format
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        
        # Preprocess the image
        processed_img = preprocess_image(img_cv)
        
        # Extract text using Tesseract OCR
        page_text = pytesseract.image_to_string(processed_img, lang='eng', config='--oem 1 --psm 3')
        
        # Clean the extracted text
        page_text = clean_text(page_text)
        
        text += page_text + "\n"
    
    with open(output_txt_path, "w", encoding="utf-8") as output_txt:
        output_txt.write(text)
    
    print(f"PDF content successfully written to {output_txt_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python pdf_text_converter.py <input_pdf> <output_txt>")
        sys.exit(1)
    
    input_pdf = sys.argv[1]
    output_txt = sys.argv[2]
    
    pdf_to_text(input_pdf, output_txt)
    