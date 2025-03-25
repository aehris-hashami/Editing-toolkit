import sys
from PyPDF2 import PdfReader, PdfWriter

def split_pdf(input_pdf_path, pages_per_split):
    # Open the input PDF file
    reader = PdfReader(input_pdf_path)
    total_pages = len(reader.pages)
    
    # Calculate the number of splits needed
    num_splits = total_pages // pages_per_split
    remainder_pages = total_pages % pages_per_split

    # Split the PDF into parts
    for i in range(num_splits):
        writer = PdfWriter()
        start_page = i * pages_per_split
        end_page = start_page + pages_per_split
        
        # Add pages to the current writer
        for page_num in range(start_page, end_page):
            writer.add_page(reader.pages[page_num])
        
        # Save the current split as a new PDF file
        output_pdf_path = f"output_part_{i + 1}.pdf"
        with open(output_pdf_path, "wb") as output_pdf:
            writer.write(output_pdf)
        
        print(f"Created {output_pdf_path} (pages {start_page + 1} to {end_page})")

    # Handle remaining pages
    if remainder_pages > 0:
        writer = PdfWriter()
        start_page = num_splits * pages_per_split  # Start from the last processed page
        
        for page_num in range(start_page, total_pages):
            writer.add_page(reader.pages[page_num])

        output_pdf_path = f"output_part_{num_splits + 1}.pdf"
        with open(output_pdf_path, "wb") as output_pdf:
            writer.write(output_pdf)
        
        print(f"Created {output_pdf_path} (pages {start_page + 1} to {total_pages})")

if __name__ == "__main__":
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 3:
        print("Usage: python split_pdf.py <input_pdf> <pages_per_split>")
        sys.exit(1)
    
    # Parse command-line arguments
    input_pdf = sys.argv[1]  # Path to the input PDF file
    pages_per_split = int(sys.argv[2])  # Number of pages per split
    
    # Call the function to split the PDF
    split_pdf(input_pdf, pages_per_split)