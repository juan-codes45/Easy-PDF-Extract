import os
import argparse
from PyPDF2 import PdfReader, PdfWriter

def list_pdf_files(directory="."):
    """List all PDF files in the specified directory."""
    pdf_files = [f for f in os.listdir(directory) if f.lower().endswith('.pdf')]
    return pdf_files

def extract_pages(input_file, output_file, pages):
    """Extract specific pages from a PDF file and save to a new file."""
    try:
        reader = PdfReader(input_file)
        writer = PdfWriter()
        
        total_pages = len(reader.pages)
        print(f"Total pages in {input_file}: {total_pages}")
        
        # Validate page numbers
        valid_pages = []
        for page_num in pages:
            if 1 <= page_num <= total_pages:
                valid_pages.append(page_num)
            else:
                print(f"Warning: Page {page_num} is out of range and will be skipped.")
        
        # Add selected pages to the output
        for page_num in valid_pages:
            writer.add_page(reader.pages[page_num - 1])  # -1 because PyPDF2 is 0-indexed
            
        # Write the output file
        with open(output_file, "wb") as output:
            writer.write(output)
            
        print(f"Successfully extracted {len(valid_pages)} pages to {output_file}")
        return True
        
    except Exception as e:
        print(f"Error extracting pages: {e}")
        return False

def extract_document_range(input_files, output_file, file_ranges):
    """Extract pages from multiple PDFs and combine into one document.
    
    file_ranges is a dictionary where keys are file indices and values are lists of page numbers.
    Example: {0: [1, 2, 3], 2: [4, 5]} extracts pages 1-3 from the first file and pages 4-5 from the third file.
    """
    try:
        writer = PdfWriter()
        
        for file_idx, page_list in file_ranges.items():
            if 0 <= file_idx < len(input_files):
                reader = PdfReader(input_files[file_idx])
                total_pages = len(reader.pages)
                
                for page_num in page_list:
                    if 1 <= page_num <= total_pages:
                        writer.add_page(reader.pages[page_num - 1])
                    else:
                        print(f"Warning: Page {page_num} in file {input_files[file_idx]} is out of range and will be skipped.")
            else:
                print(f"Warning: File index {file_idx} is out of range and will be skipped.")
        
        # Write the output file
        with open(output_file, "wb") as output:
            writer.write(output)
            
        print(f"Successfully created {output_file}")
        return True
        
    except Exception as e:
        print(f"Error extracting document: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Extract pages from PDF files and create a new document")
    parser.add_argument("--dir", help="Directory containing PDF files", default=".")
    parser.add_argument("--output", help="Output PDF file name", default="extracted_document.pdf")
    parser.add_argument("--mode", choices=["interactive", "command"], default="interactive",
                        help="Run in interactive mode or command mode")
    parser.add_argument("--files", nargs="+", type=int, help="Indices of files to process (for command mode)")
    parser.add_argument("--pages", nargs="+", type=int, help="Pages to extract (for command mode)")
    
    args = parser.parse_args()
    
    pdf_files = list_pdf_files(args.dir)
    if not pdf_files:
        print(f"No PDF files found in {args.dir}")
        return
    
    # Add full paths to the PDF files
    pdf_files = [os.path.join(args.dir, f) for f in pdf_files]
    
    if args.mode == "interactive":
        interactive_mode(pdf_files, args.output)
    else:
        command_mode(pdf_files, args.output, args.files, args.pages)

def interactive_mode(pdf_files, output_file):
    """Run the program in interactive mode, allowing the user to select files and pages."""
    print("PDF Files found:")
    for i, file in enumerate(pdf_files):
        print(f"{i}: {os.path.basename(file)}")
    
    file_ranges = {}
    
    while True:
        try:
            file_idx = int(input("\nEnter the file number to extract from (or -1 to finish): "))
            if file_idx == -1:
                break
                
            if 0 <= file_idx < len(pdf_files):
                reader = PdfReader(pdf_files[file_idx])
                total_pages = len(reader.pages)
                print(f"File {os.path.basename(pdf_files[file_idx])} has {total_pages} pages.")
                
                page_input = input("Enter page numbers to extract (e.g., '1,3-5,7'): ")
                pages = parse_page_ranges(page_input, total_pages)
                
                if file_idx not in file_ranges:
                    file_ranges[file_idx] = []
                file_ranges[file_idx].extend(pages)
                
                print(f"Added {len(pages)} pages from file {file_idx} to the extraction queue.")
            else:
                print("Invalid file number!")
        except ValueError:
            print("Please enter a valid number.")
    
    if file_ranges:
        extract_document_range(pdf_files, output_file, file_ranges)
        print(f"Extraction complete. Output saved to {output_file}")
    else:
        print("No pages selected for extraction.")

def command_mode(pdf_files, output_file, file_indices, pages):
    """Run the program in command mode, using the provided file indices and page numbers."""
    if not file_indices or not pages:
        print("Error: In command mode, you must specify both --files and --pages")
        return
    
    if len(file_indices) == 1:
        # Extract pages from a single file
        extract_pages(pdf_files[file_indices[0]], output_file, pages)
    else:
        # Create a file_ranges dictionary for multiple files
        file_ranges = {}
        for idx in file_indices:
            if 0 <= idx < len(pdf_files):
                file_ranges[idx] = pages
        
        extract_document_range(pdf_files, output_file, file_ranges)

def parse_page_ranges(range_string, max_pages):
    """Parse a string like '1,3-5,7' into a list of page numbers."""
    pages = []
    
    # Split by comma
    parts = range_string.split(',')
    
    for part in parts:
        part = part.strip()
        
        # Check if it's a range (contains '-')
        if '-' in part:
            try:
                start, end = map(int, part.split('-'))
                # Ensure the range is within bounds
                start = max(1, min(start, max_pages))
                end = max(1, min(end, max_pages))
                
                # Add all pages in the range
                pages.extend(range(start, end + 1))
            except ValueError:
                print(f"Invalid range: {part}")
        else:
            # Single page number
            try:
                page = int(part)
                if 1 <= page <= max_pages:
                    pages.append(page)
                else:
                    print(f"Warning: Page {page} is out of range (1-{max_pages}) and will be skipped.")
            except ValueError:
                print(f"Invalid page number: {part}")
    
    return sorted(set(pages))  # Remove duplicates and sort

if __name__ == "__main__":
    main()