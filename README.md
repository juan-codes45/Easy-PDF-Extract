# Easy PDF Extract

A tool to extract specific pages from multiple PDF files and combine them into a single document.

## Running the Code

1. **Save the code**: First, save the code to a file named `pdf_extractor.py`
2. **Install the required library**:
3. **Basic usage**:

This will run the tool in interactive mode by default, which is the easiest way to use it.

## Key Features

This tool has two modes:

### 1. Interactive Mode (default)
In this mode, the tool will:
* List all PDF files in the current directory
* Let you select files one by one
* For each file, specify which pages you want
* Create a combined PDF with all selected pages

### 2. Command Mode
You can also run it with specific command-line arguments

The program will:
1. Show you a list of PDFs with numbers (0, 1, 2, etc.)
2. Ask you to enter a file number
3. Show how many pages that PDF has
4. Ask you which pages you want to extract
   * You can enter individual pages like "1,3,7"
   * You can enter ranges like "1-5"
   * You can combine these like "1,3-5,7,10-12"
5. Let you select pages from multiple files
6. When done, enter "-1" to finish and create the output PDF

### Example 2: Command Mode for a Single File
To extract pages 1, 3, and 5 from the first PDF file
