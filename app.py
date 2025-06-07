#!/usr/bin/env python3
"""
Flask Web Application for RemNote Flashcard Generator
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path
import zipfile
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import google.generativeai as genai
from dotenv import load_dotenv
from generate_flashcards import process_file, REMNOTE_PROMPT_TEMPLATE
import threading
import queue
import time
import logging
from datetime import datetime
import concurrent.futures
import re

# Load environment variables from .env file
load_dotenv()

# Configure comprehensive logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('flashcard_generator.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

# Supported file extensions
ALLOWED_EXTENSIONS = {'.pdf', '.jpg', '.jpeg', '.png'}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS

def process_single_file(file_path, api_key, output_dir, custom_prompt=None):
    """Process a single file with optional custom prompt"""
    logger.info(f"Starting to process file: {file_path}")
    
    # Configure the Gemini API
    genai.configure(api_key=api_key)
    
    # Initialize the Gemini model
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    file_name = os.path.basename(file_path)
    file_stem = os.path.splitext(file_name)[0]
    output_file = os.path.join(output_dir, f"{file_stem}_flashcards.txt")
    
    result = {
        "file_name": file_name,
        "file_path": file_path,
        "output_file": output_file,
        "success": False
    }
    
    # Use custom prompt if provided, otherwise use default
    prompt_to_use = custom_prompt if custom_prompt else REMNOTE_PROMPT_TEMPLATE
    logger.info(f"Using {'custom' if custom_prompt else 'default'} prompt for {file_name}")
    
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            logger.info(f"Processing attempt {retry_count + 1}/{max_retries}: {file_name}")
            
            # Upload the file to Gemini
            sample_file = genai.upload_file(path=file_path, display_name=file_name)
            logger.info(f"File uploaded to Gemini: {file_name}")
            
            # Generate flashcards using the uploaded document
            response = model.generate_content([sample_file, prompt_to_use])
            logger.info(f"AI response received for: {file_name}")
            
            # Save the generated flashcards to a text file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            result["success"] = True
            result["content"] = response.text
            
            logger.info(f"✅ Flashcards saved successfully: {output_file}")
            
            # Add a small delay to avoid rate limiting
            time.sleep(0.5)
            return result
            
        except Exception as e:
            error_msg = str(e)
            retry_count += 1
            logger.error(f"❌ Error processing {file_name} (attempt {retry_count}): {error_msg}")
            
            # Check if it's a rate limit error - use original script's sophisticated handling
            if "429" in error_msg and retry_count < max_retries:
                # Extract retry delay if available (like original script)
                retry_delay = 10  # Default delay
                if "retry_delay" in error_msg:
                    try:
                        # Try to extract the retry delay from the error message
                        delay_str = re.search(r'retry_delay\s*{\s*seconds:\s*(\d+)', error_msg)
                        if delay_str:
                            retry_delay = int(delay_str.group(1))
                    except:
                        pass
                
                logger.warning(f"Rate limit hit for {file_name}, waiting {retry_delay}s before retry...")
                time.sleep(retry_delay)
                continue
            elif retry_count < max_retries:
                logger.warning(f"Retrying in 2 seconds... (attempt {retry_count + 1}/{max_retries})")
                time.sleep(2)
                continue
            else:
                logger.error(f"❌ Failed to process {file_name} after {max_retries} attempts")
                result["error"] = error_msg
                return result
    
    return result

@app.route('/')
def index():
    """Render the main web interface"""
    logging.info("📄 Serving main web interface")
    return render_template('index.html', default_prompt=REMNOTE_PROMPT_TEMPLATE)

@app.route('/process_files', methods=['POST'])
def process_files():
    """Process uploaded files and generate flashcards"""
    logger.info("=== Starting file processing request ===")
    
    if 'files' not in request.files:
        logger.error("No files uploaded in request")
        return jsonify({'error': 'No files uploaded'}), 400
    
    files = request.files.getlist('files')
    custom_prompt = request.form.get('prompt', '').strip()
    
    logger.info(f"Received {len(files)} files")
    logger.info(f"Custom prompt provided: {'Yes' if custom_prompt else 'No'}")
    
    if custom_prompt:
        logger.info(f"Custom prompt (first 100 chars): {custom_prompt[:100]}...")
    
    if not files or all(f.filename == '' for f in files):
        logger.error("No files selected")
        return jsonify({'error': 'No files selected'}), 400
    
    # Check if API key is available
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        logger.error("Google API key not configured")
        return jsonify({'error': 'Google API key not configured. Please set GOOGLE_API_KEY environment variable.'}), 500
    
    logger.info("✅ Google API key found")
    
    # Filter valid files
    valid_files = [f for f in files if f and allowed_file(f.filename)]
    if not valid_files:
        logger.error("No valid PDF or image files found")
        return jsonify({'error': 'No valid PDF or image files found'}), 400
    
    logger.info(f"Valid files to process: {[f.filename for f in valid_files]}")
    
    # Create temporary directory for processing
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_input_dir = os.path.join(temp_dir, 'input')
        temp_output_dir = os.path.join(temp_dir, 'output')
        os.makedirs(temp_input_dir, exist_ok=True)
        os.makedirs(temp_output_dir, exist_ok=True)
        
        logger.info(f"Created temporary directories: {temp_input_dir}, {temp_output_dir}")
        
        # Save uploaded files
        saved_files = []
        for file in valid_files:
            if file:
                filename = secure_filename(file.filename)
                file_path = os.path.join(temp_input_dir, filename)
                file.save(file_path)
                saved_files.append(file_path)
                logger.info(f"Saved file: {filename} ({os.path.getsize(file_path)} bytes)")
        
        # Process files in parallel and collect results
        all_flashcards = []
        results = []
        
        # Set maximum workers (similar to original script)
        max_workers = min(5, len(saved_files))  # Max 5 workers to respect API limits
        logger.info(f"Starting parallel processing with {max_workers} workers for {len(saved_files)} files")
        
        try:
            # Use ThreadPoolExecutor for parallel processing (like original script)
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                # Create a dictionary to track which future maps to which file
                future_to_file = {}
                
                # Submit all files for processing
                for file_path in saved_files:
                    future = executor.submit(process_single_file, file_path, api_key, temp_output_dir, custom_prompt)
                    future_to_file[future] = os.path.basename(file_path)
                    logger.info(f"Submitted {os.path.basename(file_path)} for processing")
                
                # Process results as they complete
                completed_count = 0
                for future in concurrent.futures.as_completed(future_to_file):
                    file_name = future_to_file[future]
                    completed_count += 1
                    
                    try:
                        result = future.result()
                        results.append(result)
                        
                        logger.info(f"Completed {completed_count}/{len(saved_files)}: {file_name}")
                        
                        if result['success']:
                            # Read the generated flashcards
                            if 'content' in result:
                                content = result['content']
                            else:
                                # Read from output file
                                with open(result['output_file'], 'r', encoding='utf-8') as f:
                                    content = f.read()
                            
                            all_flashcards.append(f"# {result['file_name']}\n{content}\n")
                            logger.info(f"✅ Successfully processed: {result['file_name']}")
                        else:
                            logger.error(f"❌ Failed to process: {result['file_name']}")
                            
                    except Exception as exc:
                        logger.error(f"❌ {file_name} generated an exception: {exc}")
                        # Add failed result
                        results.append({
                            'file_name': file_name,
                            'success': False,
                            'error': str(exc)
                        })
        
        except Exception as e:
            logger.error(f"❌ Critical error during parallel processing: {str(e)}")
            return jsonify({'error': f'Error during parallel processing: {str(e)}'}), 500
        
        # Combine all flashcards
        combined_flashcards = '\n'.join(all_flashcards)
        
        # Calculate success metrics
        successful_files = len([r for r in results if r['success']])
        total_files = len(saved_files)
        
        logger.info(f"=== Processing complete: {successful_files}/{total_files} files successful ===")
        
        return jsonify({
            'success': True,
            'flashcards': combined_flashcards,
            'processed_files': successful_files,
            'total_files': total_files,
            'message': f'Successfully processed {successful_files}/{total_files} files'
        })

if __name__ == '__main__':
    # Check for API key
    if not os.getenv('GOOGLE_API_KEY'):
        logger.warning("⚠️  Warning: GOOGLE_API_KEY environment variable not set!")
        logger.warning("Please set your Google API key:")
        logger.warning("export GOOGLE_API_KEY='your-api-key-here'")
    else:
        logger.info("✅ Google API key found")
    
    logger.info("🚀 Starting FlashCard Generator Web Application on port 8080")
    app.run(debug=True, host='0.0.0.0', port=8080)
