import PyPDF2
import argparse
import os

def extract_text_from_pdf(pdf_path, output_path=None):
    """
    Extract text from PDF and save to a text file or print to console

    Args:
        pdf_path: Path to the PDF file
        output_path: Optional path to save the extracted text
    """
    if not os.path.exists(pdf_path):
        print(f"Error: File {pdf_path} not found")
        return

    print(f"Extracting text from {pdf_path}...")

    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)

            print(f"Found {num_pages} pages")
            text = ""

            for page_num in range(num_pages):
                page = reader.pages[page_num]
                text += page.extract_text() + "\n\n"
                print(f"Processed page {page_num + 1}/{num_pages}")

            if output_path:
                with open(output_path, 'w', encoding='utf-8') as out_file:
                    out_file.write(text)
                print(f"Text extracted and saved to {output_path}")
            else:
                print("\n--- EXTRACTED TEXT ---\n")
                print(text)

    except Exception as e:
        print(f"Error extracting text from PDF: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract text from a PDF file")
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument("-o", "--output", help="Output text file path (optional)")

    args = parser.parse_args()
    extract_text_from_pdf(args.pdf_path, args.output)
