import sys
from PyPDF2 import PdfReader, PdfWriter

def extract_pages(input_pdf_path, start_page, end_page):
    try:
        # Open the input PDF file
        reader = PdfReader(input_pdf_path)
        total_pages = len(reader.pages)
        
        print(f"Total number of pages in the PDF file: {total_pages}")
        
        # Validate page range
        if start_page < 1 or end_page > total_pages or start_page > end_page:
            print(f"Error: Invalid page range. PDF has {total_pages} pages.")
            sys.exit(1)
        
        # Create a writer object and add the selected pages
        writer = PdfWriter()
        for page_num in range(start_page - 1, end_page):  # Convert to 0-based index
            writer.add_page(reader.pages[page_num])
        
        # Get output filename from user
        segment_name = input("What do you want to name the extracted PDF file (without extension): ")
        output_pdf_path = f"{segment_name}.pdf"
        
        # Save the output PDF file
        with open(output_pdf_path, "wb") as output_pdf:
            writer.write(output_pdf)
        
        print(f"Successfully created '{output_pdf_path}' (pages {start_page} to {end_page})")
    
    except FileNotFoundError:
        print(f"Error: Input file '{input_pdf_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 4:
        print(f"Received {len(sys.argv) - 1} arguments, expected 3.")
        print("Usage: python extract_pages.py <input_pdf> <start_page> <end_page>")
        print("Example: python extract_pages.py document.pdf 5 10")
        sys.exit(1)
    
    # Parse command-line arguments
    input_pdf = sys.argv[1]  # Path to the input PDF file
    try:
        start_page = int(sys.argv[2])  # Starting page number (1-based)
        end_page = int(sys.argv[3])    # Ending page number (1-based)
    except ValueError:
        print("Error: Page numbers must be integers.")
        sys.exit(1)
    
    # Call the function to extract pages
    extract_pages(input_pdf, start_page, end_page)