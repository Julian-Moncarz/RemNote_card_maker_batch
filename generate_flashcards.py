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
import google.generativeai as genai

# RemNote prompt template 
REMNOTE_PROMPT_TEMPLATE = """Create a comprehensive set of study flashcards covering all the content in this document.

Break content into Objects - identify all significant concepts, systems, processes or terms. Be thorough and fine-grained with your object identification but each object should still be a discrete THING (Noun). Group related objects together in logical sections when possible.

Question Formatting:

Structure your output as follows:

## [Object Name]

* [Question] == [Answer]  
* [Question] == [Answer]  
* [Question] == [Answer]

Question Construction RULES:

1. RULE 1 - ATOMIC: Each question should target the smallest meaningful unit of knowledge

2. RULE 2 - DETERMINISTIC: Questions should clearly point to a single specific answer. The answers should be VERY clear from the questions.

After following these rules, ensure your questions collectively cover ALL information in the document. A person who memorizes all answers should understand EVERYTHING in the document. ALL of the information in the document should be turned into questions.

Output Format:

* Use proper Markdown formatting  
* Create MANY flashcards - as many as needed to cover everything in the document  
* Output only the flashcards and nothing else.
"""

def process_file(file_path, api_key, output_dir):
    """Process a single file and generate flashcards."""
    # Configure the Gemini API
    genai.configure(api_key=api_key)
    
    # Initialize the Gemini model
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    file_name = os.path.basename(file_path)
    file_stem = os.path.splitext(file_name)[0]
    output_file = os.path.join(output_dir, f"{file_stem}_flashcards.txt")
    
    print(f"Processing: {file_path}")
    
    try:
        # Upload the file to Gemini
        sample_file = genai.upload_file(path=file_path, display_name=file_name)
        print(f"Uploaded file '{sample_file.display_name}' as: {sample_file.uri}")
        
        # Generate flashcards using the uploaded document
        response = model.generate_content([sample_file, REMNOTE_PROMPT_TEMPLATE])
        
        # Save the generated flashcards to a text file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        print(f"✅ Flashcards saved to: {output_file}")
        return True
    
    except Exception as e:
        print(f"❌ Error processing {file_path}: {str(e)}")
        return False

def main():
    """Main function to process files and generate flashcards."""
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Generate RemNote flashcards from PDF and image files.')
    parser.add_argument('source_dir', help='Source directory containing PDF and image files')
    parser.add_argument('--api-key', help='Google Gemini API key')
    
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
    
    # Process each file
    success_count = 0
    for file_path in files_to_process:
        if process_file(str(file_path), api_key, output_dir):
            success_count += 1
    
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
