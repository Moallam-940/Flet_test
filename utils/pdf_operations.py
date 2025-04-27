from PyPDF2 import PdfReader, PdfWriter
import os
import subprocess
from typing import List
from tqdm import tqdm

def compress_pdf(input_pdf: str, output_pdf: str, power: int = 3) -> None:
    """
    Compress PDF file using Ghostscript while maintaining quality.
    :param input_pdf: Input PDF path.
    :param output_pdf: Output PDF path.
    :param power: Compression level (1-5):
        1: prepress (highest quality)
        2: printer (high quality)
        3: ebook (recommended balance)
        4: screen (low quality)
        5: custom (best quality/size ratio)
    """
    quality_map = {
        1: '/prepress',
        2: '/printer',
        3: '/ebook',
        4: '/screen',
        5: '/ebook'
    }
    if power not in quality_map:
        print("Invalid compression level. Using default (3 - ebook)")
        power = 3
    quality = quality_map[power]
    try:
        if not os.path.exists(input_pdf):
            raise FileNotFoundError(f"Error: Input file {input_pdf} does not exist")
        
        gs_cmd = [
            'gs',
            '-sDEVICE=pdfwrite',
            '-dCompatibilityLevel=1.5',
            '-dPDFSETTINGS=' + quality,
            '-dNOPAUSE',
            '-dQUIET',
            '-dBATCH',
            '-dAutoRotatePages=/None',
            '-sOutputFile=' + output_pdf,
            input_pdf
        ]
        if power == 5:  # Custom settings for optimal balance
            gs_cmd[3:3] = [
                '-dDetectDuplicateImages=true',
                '-dColorImageResolution=150',
                '-dGrayImageResolution=150',
                '-dMonoImageResolution=150',
                '-dDownsampleColorImages=true',
                '-dDownsampleGrayImages=true',
                '-dDownsampleMonoImages=true'
            ]
        
        print("\nCompressing PDF (this may take a while for large files)...")
        process = subprocess.Popen(gs_cmd)
        process.wait()
        
        if os.path.exists(output_pdf):
            original_size = os.path.getsize(input_pdf) / 1024
            new_size = os.path.getsize(output_pdf) / 1024
            reduction = ((original_size - new_size) / original_size) * 100
            print(f"\nSuccess: File compressed from {original_size:.2f} KB to {new_size:.2f} KB ({reduction:.1f}% reduction)")
        else:
            raise FileNotFoundError("Error: Output file was not created")
    except subprocess.CalledProcessError as e:
        print(f"Compression failed: {e}")
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"Unexpected error: {e}")

def extract_pages(input_pdf: str, output_pdf: str, page_ranges: List[str]) -> None:
    """
    Extract specified page ranges from PDF.
    :param input_pdf: Input PDF path.
    :param output_pdf: Output PDF path.
    :param page_ranges: List of page ranges (e.g., ['1-5', '8-10']).
    """
    try:
        reader = PdfReader(input_pdf)
        writer = PdfWriter()
        total_pages = sum(end - start + 1 for r in page_ranges for start, end in [map(int, r.split('-'))])
        
        with tqdm(total=total_pages, desc="Extracting pages") as pbar:
            for page_range in page_ranges:
                start, end = map(int, page_range.split('-'))
                for page_num in range(start - 1, end):
                    if page_num < len(reader.pages):
                        writer.add_page(reader.pages[page_num])
                        pbar.update(1)
                    else:
                        print(f"Warning: Page {page_num + 1} does not exist - skipping")
        
        with open(output_pdf, 'wb') as out_file:
            writer.write(out_file)
        print(f"\nSuccess: Pages extracted to {output_pdf}")
    except Exception as e:
        print(f"Error: {e}")

def merge_pdfs(input_files: List[str], output_pdf: str) -> None:
    """
    Merge multiple PDF files into one.
    :param input_files: List of input PDF paths.
    :param output_pdf: Output PDF path.
    """
    try:
        writer = PdfWriter()
        total_pages = 0
        for file in input_files:
            if os.path.exists(file):
                reader = PdfReader(file)
                total_pages += len(reader.pages)
        
        with tqdm(total=total_pages, desc="Merging PDFs") as pbar:
            for file in input_files:
                if not os.path.exists(file):
                    print(f"Warning: File {file} not found - skipping")
                    continue
                reader = PdfReader(file)
                for page in reader.pages:
                    writer.add_page(page)
                    pbar.update(1)
        
        with open(output_pdf, 'wb') as out_file:
            writer.write(out_file)
        print(f"\nSuccess: Files merged into {output_pdf}")
    except Exception as e:
        print(f"Error: {e}")

def delete_pages(input_pdf: str, output_pdf: str, page_ranges_to_delete: List[str]) -> None:
    """
    Delete specified page ranges from PDF.
    :param input_pdf: Input PDF path.
    :param output_pdf: Output PDF path.
    :param page_ranges_to_delete: List of page ranges to delete (e.g., ['1-5', '8-10']).
    """
    try:
        reader = PdfReader(input_pdf)
        writer = PdfWriter()
        total_pages = len(reader.pages)
        pages_to_exclude = set()
        for page_range in page_ranges_to_delete:
            start, end = map(int, page_range.split('-'))
            pages_to_exclude.update(range(start - 1, end))
        
        remaining_pages = total_pages - len(pages_to_exclude)
        with tqdm(total=remaining_pages, desc="Deleting pages") as pbar:
            for page_num in range(total_pages):
                if page_num not in pages_to_exclude:
                    writer.add_page(reader.pages[page_num])
                    pbar.update(1)
        
        with open(output_pdf, 'wb') as out_file:
            writer.write(out_file)
        print(f"\nSuccess: Pages deleted, saved to {output_pdf}")
    except Exception as e:
        print(f"Error: {e}")

def split_pdf(input_pdf: str, pages_per_part: int) -> None:
    """
    Split PDF into multiple parts with specified number of pages each.
    :param input_pdf: Input PDF path.
    :param pages_per_part: Number of pages per part.
    """
    try:
        reader = PdfReader(input_pdf)
        total_pages = len(reader.pages)
        num_parts = (total_pages + pages_per_part - 1) // pages_per_part
        base_name = os.path.splitext(os.path.basename(input_pdf))[0]
        output_dir = input("Enter directory to save parts (leave empty for same directory): ").strip()
        if not output_dir:
            output_dir = os.path.dirname(input_pdf)
        os.makedirs(output_dir, exist_ok=True)
        
        with tqdm(total=total_pages, desc="Splitting PDF") as pbar:
            for part_num in range(num_parts):
                start_page = part_num * pages_per_part
                end_page = min((part_num + 1) * pages_per_part, total_pages)
                writer = PdfWriter()
                for page_num in range(start_page, end_page):
                    writer.add_page(reader.pages[page_num])
                    pbar.update(1)
                
                output_pdf = os.path.join(output_dir, f"{base_name}_part{part_num + 1}.pdf")
                with open(output_pdf, 'wb') as out_file:
                    writer.write(out_file)
        
        print(f"\nSuccess: PDF split into {num_parts} parts:")
        print(f"• Saved in: {output_dir}")
        print(f"• Naming pattern: {base_name}_partX.pdf")
    except Exception as e:
        print(f"Error: {e}")

def parse_page_ranges(input_str: str) -> List[str]:
    """
    Parse page range input like '1-10,15-20' into list.
    :param input_str: Input string (e.g., '1-5,8-10').
    :return: List of page ranges (e.g., ['1-5', '8-10']).
    """
    return [r.strip() for r in input_str.split(',')]
