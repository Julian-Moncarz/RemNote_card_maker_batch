#!/usr/bin/env python3
"""
RemNote Flashcard Generator
--------------------------
This script processes PDF and image files from a source folder,
generates RemNote flashcards using the Gemini API, and saves them
as text files in the remnote_cards directory.
"""

import os
import sys
import argparse
from pathlib import Path
import mimetypes
import time
import re
import concurrent.futures
from tqdm import tqdm
import google.generativeai as genai

# RemNote prompt template 
REMNOTE_PROMPT_TEMPLATE = """

You are analyzing a test document. Your task is to:

1. Extract ALL test questions from the document
2. Include ALL numerical values, constants, and given data in the question portion
3. Provide the CORRECT solution/answer for each question
4. Ignore any existing student answers in the document
5. Solve problems step-by-step but provide final answers clearly
6. Focus ONLY on exam-relevant content (ignore lab procedures, general instructions, etc.)

Output ONLY in this exact format:

* question == answer
* question == answer
* question == answer

Requirements:
- Extract the EXACT question text as it appears in the test
- Include ALL given numbers, units, constants, and data in the question portion
- Make sure the question is self-contained with all information needed to solve it
- Provide complete, correct answers
- For calculations, show key steps but keep the final answer on one line
- For long answers, keep everything on a single line after the "=="
- Do not add any extra text, headers, or formatting
- Do not include non-test content like instructions or lab procedures

Example format:
* A 2μC charge is located 3m away from point P. What is the electric field at point P? == E = kq/r² = (9×10⁹)(2×10⁻⁶)/(3)² = 2000 N/C

"""

def process_file(file_path, api_key, output_dir, pbar=None):

    """Process a single file and generate flashcards."""
    # Configure the Gemini API
    genai.configure(api_key=api_key)
    
    # Initialize the Gemini model
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    file_name = os.path.basename(file_path)
    file_stem = os.path.splitext(file_name)[0]
    output_file = os.path.join(output_dir, f"{file_stem}_flashcards.txt")
    
    # Check if the output file already exists - skip if it does
    if os.path.exists(output_file):
        if pbar:
            pbar.update(1)
            pbar.set_description(f"Skipped (exists): {file_name}")
        return {
            "file_path": file_path,
            "output_file": output_file,
            "success": True,
            "skipped": True
        }
    
    result = {
        "file_path": file_path,
        "output_file": output_file,
        "success": False
    }
    
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            if pbar:
                pbar.set_description(f"Processing: {file_name}")
            
            # Upload the file to Gemini
            sample_file = genai.upload_file(path=file_path, display_name=file_name)
            
            # Generate flashcards using the uploaded document
            response = model.generate_content([sample_file, REMNOTE_PROMPT_TEMPLATE])
            
            # Save the generated flashcards to a text file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            result["success"] = True
            result["content"] = response.text
            
            if pbar:
                pbar.update(1)
                pbar.set_description(f"Completed: {file_name}")
            else:
                print(f"✅ Flashcards saved to: {output_file}")
            
            # Add a small delay to avoid rate limiting
            time.sleep(0.5)
            return result
            
        except Exception as e:
            error_msg = str(e)
            retry_count += 1
            
            # Check if it's a rate limit error
            if "429" in error_msg and retry_count < max_retries:
                # Extract retry delay if available
                retry_delay = 10  # Default delay
                if "retry_delay" in error_msg:
                    try:
                        # Try to extract the retry delay from the error message
                        delay_str = re.search(r'retry_delay\s*{\s*seconds:\s*(\d+)', error_msg)
                        if delay_str:
                            retry_delay = int(delay_str.group(1))
                    except:
                        pass
                
                if pbar:
                    pbar.set_description(f"Rate limited. Waiting {retry_delay}s before retry {retry_count}/{max_retries}")
                else:
                    print(f"Rate limited. Waiting {retry_delay}s before retry {retry_count}/{max_retries}")
                
                # Wait before retrying
                time.sleep(retry_delay)
            else:
                # Not a rate limit error or max retries reached
                result["error"] = f"Error processing {file_name}: {error_msg}"
                
                if pbar:
                    pbar.update(1)
                    pbar.set_description(f"Failed: {file_name}")
                else:
                    print(f"❌ {result['error']}")
                
                return result
    
    # If we get here, we've exhausted all retries
    result["error"] = f"Max retries reached for {file_name}"
    
    if pbar:
        pbar.update(1)
    else:
        print(f"❌ {result['error']}")
    
    return result

def main():
    """Main function to process files and generate flashcards."""
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Generate RemNote flashcards from PDF and image files.')
    parser.add_argument('source_dir', help='Source directory containing PDF and image files')
    parser.add_argument('--api-key', help='Google Gemini API key')
    parser.add_argument('--max-workers', type=int, default=5, help='Maximum number of parallel workers (default: 5)')
    parser.add_argument('--no-parallel', action='store_true', help='Disable parallel processing')
    
    args = parser.parse_args()
    
    # Check if API key is provided
    api_key = args.api_key or os.environ.get('GOOGLE_API_KEY')
    if not api_key:
        print("Error: Google Gemini API key is required.")
        print("Either provide it with --api-key or set the GOOGLE_API_KEY environment variable.")
        return 1

    # Always use 'remnote_cards/[source_folder_name]' directory for output
    source_folder_name = os.path.basename(os.path.normpath(args.source_dir))
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'remnote_cards', source_folder_name)
    os.makedirs(output_dir, exist_ok=True)
    print(f"Output directory: {output_dir}")

    # Get all PDF and image files from the source directory and its subfolders
    source_path = Path(args.source_dir)
    supported_extensions = ['.pdf', '.jpg', '.jpeg', '.png']
    files_to_process = []

    # Recursive function to find files in all subfolders
    def find_files_recursive(directory):
        files_found = []
        try:
            for item in directory.iterdir():
                if item.is_file() and item.suffix.lower() in supported_extensions:
                    files_found.append(item)
                elif item.is_dir():
                    # Recursively search in subdirectories
                    files_found.extend(find_files_recursive(item))
        except PermissionError:
            print(f"Warning: Permission denied for directory {directory}")
        return files_found

    # Find all files recursively
    files_to_process = find_files_recursive(source_path)

    if not files_to_process:
        print(f"No PDF or image files found in {args.source_dir}")
        return 1
    
    print(f"Found {len(files_to_process)} files to process")
    
    # Process files in parallel
    success_count = 0
    all_results = []
    
    # Set the maximum number of parallel workers
    # Use the user-specified value or default to 5 (for free tier limits)
    if args.no_parallel:
        max_workers = 1
    else:
        max_workers = min(args.max_workers, len(files_to_process))  # Respect user-specified limit
    
    print(f"Processing {len(files_to_process)} files with {max_workers} parallel workers...")
    
    # Use tqdm for progress tracking
    with tqdm(total=len(files_to_process), desc="Processing files", unit="file") as pbar:
        # Use ThreadPoolExecutor for parallel processing
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Create a dictionary to track which future maps to which file
            future_to_file = {}
            
            # Submit all files for processing
            for file_path in files_to_process:
                future = executor.submit(process_file, str(file_path), api_key, output_dir, pbar)
                future_to_file[future] = os.path.basename(file_path)
            
            # Process results as they complete
            for future in concurrent.futures.as_completed(future_to_file):
                file_name = future_to_file[future]
                try:
                    result = future.result()
                    all_results.append(result)
                    
                    if result["success"]:
                        success_count += 1
                        
                        # Print success message if not skipped
                        if not result.get("skipped", False):
                            print(f"✅ Flashcards saved to: {result['output_file']}")
                except Exception as exc:
                    print(f"\n❌ {file_name} generated an exception: {exc}")
    
    print(f"\nProcessing complete: {success_count}/{len(files_to_process)} files successfully processed")

    # Combine all generated flashcards into a single notes file
    notes_filename = source_folder_name + '_notes.txt'
    notes_filepath = os.path.join(output_dir, notes_filename)
    with open(notes_filepath, 'w', encoding='utf-8') as notes_file:
        for file in files_to_process:
            flashcard_file = os.path.join(output_dir, f"{file.stem}_flashcards.txt")
            if os.path.exists(flashcard_file):
                with open(flashcard_file, 'r', encoding='utf-8') as f:
                    notes_file.write(f.read())
                    notes_file.write('\n\n')
    print(f"Combined notes saved to: {notes_filepath}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
