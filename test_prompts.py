#!/usr/bin/env python3
"""
RemNote Flashcard Prompt Tester
------------------------------
This script tests different prompt templates from prompts.md
against the same input file and generates separate output files
for each prompt template. It also evaluates the results to identify
the top 3 prompt templates for test preparation.

Features:
- Parallel processing of multiple prompts simultaneously
- Evaluation of prompt effectiveness for test preparation
- HTML comparison of results
"""

import os
import sys
import argparse
import re
from pathlib import Path
import google.generativeai as genai
import concurrent.futures
import time
from tqdm import tqdm

def extract_prompts_from_file(prompts_file):
    """Extract prompts from the prompts.md file."""
    with open(prompts_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract sections using regex - more robust pattern to handle all prompts
    pattern = r'## ([^\n]+)\n```\n(.*?)\n```'
    matches = re.findall(pattern, content, re.DOTALL)
    
    prompts = {}
    for title, prompt_text in matches:
        prompts[title] = prompt_text.strip()
    
    print(f"Found {len(prompts)} prompts in {prompts_file}")
    # Print the first few prompt names to verify
    prompt_names = list(prompts.keys())
    if prompt_names:
        print(f"First few prompts: {', '.join(prompt_names[:5])}")
        if len(prompt_names) > 5:
            print(f"Last few prompts: {', '.join(prompt_names[-5:] if len(prompt_names) >= 5 else prompt_names)}")
    
    return prompts

def process_file_with_prompt(file_path, api_key, output_dir, prompt_name, prompt_text, pbar=None):
    """Process a single file with a specific prompt."""
    # Configure the Gemini API
    genai.configure(api_key=api_key)
    
    # Initialize the Gemini model
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    file_name = os.path.basename(file_path)
    file_stem = os.path.splitext(file_name)[0]
    
    # Create a sanitized prompt name for the filename
    sanitized_prompt_name = prompt_name.replace('/', '_').replace(' ', '_')
    output_file = os.path.join(output_dir, f"{file_stem}_{sanitized_prompt_name}_flashcards.txt")
    
    # Check if the output file already exists - skip if it does
    if os.path.exists(output_file):
        if pbar:
            pbar.update(1)
            pbar.set_description(f"Skipped (exists): {prompt_name}")
        
        # Read existing content
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return {
            "prompt_name": prompt_name,
            "file_path": file_path,
            "output_file": output_file,
            "success": True,
            "content": content,
            "skipped": True
        }
    
    result = {
        "prompt_name": prompt_name,
        "file_path": file_path,
        "output_file": output_file,
        "success": False,
        "content": ""
    }
    
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            # Upload the file to Gemini
            sample_file = genai.upload_file(path=file_path, display_name=file_name)
            
            # Generate flashcards using the uploaded document and the specific prompt
            response = model.generate_content([sample_file, prompt_text])
            
            # Save the generated flashcards to a text file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"# Flashcards generated with: {prompt_name}\n\n")
                f.write(response.text)
            
            result["success"] = True
            result["content"] = response.text
            
            if pbar:
                pbar.update(1)
                pbar.set_description(f"Processed: {prompt_name}")
            
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
                
                # Wait before retrying
                time.sleep(retry_delay)
            else:
                # Not a rate limit error or max retries reached
                result["error"] = f"❌ Error processing {prompt_name}: {error_msg}"
                
                if pbar:
                    pbar.update(1)
                    pbar.set_description(f"Failed: {prompt_name}")
                
                return result
    
    # If we get here, we've exhausted all retries
    result["error"] = f"❌ Max retries reached for {prompt_name}"
    
    if pbar:
        pbar.update(1)
    
    return result

def evaluate_flashcards(api_key, output_dir, file_stem, prompt_results):
    """Evaluate the flashcard results and identify the top 3 for test preparation."""
    # Check if evaluation file already exists
    eval_file = os.path.join(output_dir, f"{file_stem}_evaluation.txt")
    if os.path.exists(eval_file):
        print(f"\nEvaluation file already exists: {eval_file}")
        # Read existing evaluation
        with open(eval_file, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Extract the top templates
        top_templates = []
        for i in range(1, 4):
            marker = f"TOP_TEMPLATE_{i}: "
            if marker in text:
                start_idx = text.find(marker) + len(marker)
                end_idx = text.find('\n', start_idx)
                if end_idx == -1:  # If it's the last line
                    template_name = text[start_idx:].strip()
                else:
                    template_name = text[start_idx:end_idx].strip()
                top_templates.append(template_name)
        
        print(f"Evaluation complete. Top templates identified: {', '.join(top_templates)}")
        print(f"Full evaluation saved to: {eval_file}")
        
        return top_templates
    
    # Configure the Gemini API
    genai.configure(api_key=api_key)
    
    # Initialize the Gemini model
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    print("\nEvaluating flashcards to identify top templates...")
    
    # Create evaluation prompt
    evaluation_prompt = f"""
    You are an expert in educational psychology and flashcard creation. 
    I've generated flashcards using different prompt templates for studying quantum physics.
    Please analyze these flashcards and identify the TOP 3 prompt templates that would be MOST EFFECTIVE 
    for preparing for a test on this material.
    
    For each prompt template, consider:
    1. How well the flashcards cover the key concepts
    2. How effectively they test understanding rather than just memorization
    3. How well they prepare someone for exam questions
    4. The clarity and precision of the questions and answers
    5. The organization and structure of the content
    
    Here are the flashcards generated by each prompt template:
    
    {prompt_results}
    
    Please provide your TOP 3 recommendations in this exact format:
    TOP_TEMPLATE_1: [Name of the best template]
    TOP_TEMPLATE_2: [Name of the second best template]
    TOP_TEMPLATE_3: [Name of the third best template]
    REASONING: [Your detailed explanation of why these three templates are best for test preparation]
    """
    
    try:
        # Generate evaluation
        response = model.generate_content(evaluation_prompt)
        
        # Parse the response to extract the top 3 templates
        text = response.text
        top_templates = []
        
        # Extract the top templates
        for i in range(1, 4):
            marker = f"TOP_TEMPLATE_{i}: "
            if marker in text:
                start_idx = text.find(marker) + len(marker)
                end_idx = text.find('\n', start_idx)
                if end_idx == -1:  # If it's the last line
                    template_name = text[start_idx:].strip()
                else:
                    template_name = text[start_idx:end_idx].strip()
                top_templates.append(template_name)
        
        # Save the evaluation results
        eval_file = os.path.join(output_dir, f"{file_stem}_evaluation.txt")
        with open(eval_file, 'w', encoding='utf-8') as f:
            f.write(text)
        
        print(f"\nEvaluation complete. Top templates identified: {', '.join(top_templates)}")
        print(f"Full evaluation saved to: {eval_file}")
        
        return top_templates
    
    except Exception as e:
        print(f"\n❌ Error during evaluation: {str(e)}")
        return []

def main():
    """Main function to test different prompts."""
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Test different RemNote flashcard prompts on the same input file.')
    parser.add_argument('input_file', nargs='+', help='Input file(s) (PDF or image) to process')
    parser.add_argument('--api-key', help='Google Gemini API key')
    parser.add_argument('--prompts-file', default='prompts.md', help='File containing prompt templates')
    parser.add_argument('--output-dir', default='prompt_test_results', help='Directory for output files')
    
    args = parser.parse_args()
    
    # Check if API key is provided
    api_key = args.api_key or os.environ.get('GOOGLE_API_KEY')
    if not api_key:
        print("Error: Google Gemini API key is required.")
        print("Either provide it with --api-key or set the GOOGLE_API_KEY environment variable.")
        return 1
    
    # Check if input files exist
    for input_file in args.input_file:
        if not os.path.exists(input_file):
            print(f"Error: Input file {input_file} does not exist.")
            return 1
    
    # Check if prompts file exists
    prompts_file = args.prompts_file
    if not os.path.exists(prompts_file):
        print(f"Error: Prompts file {prompts_file} does not exist.")
        return 1
    
    # Create output directory
    output_dir = args.output_dir
    os.makedirs(output_dir, exist_ok=True)
    print(f"Output directory: {output_dir}")
    
    # Extract prompts from file
    prompts = extract_prompts_from_file(prompts_file)
    if not prompts:
        print(f"Error: No prompts found in {prompts_file}")
        return 1
    
    print(f"Found {len(prompts)} prompts to test")
    
    # Process each input file
    for input_file in args.input_file:
        file_stem = os.path.splitext(os.path.basename(input_file))[0]
        print(f"\n=== Processing file: {input_file} ===")
        
        # Process input file with each prompt in parallel
        success_count = 0
        prompt_results = ""
        all_results = []
        
        # Set the maximum number of parallel workers
        # Limit to 5 for free tier to avoid hitting rate limits
        max_workers = min(5, len(prompts))  # Adjusted for free tier API limits
        
        print(f"\nProcessing {len(prompts)} prompts with {max_workers} parallel workers...")
        
        # Create a progress bar
        with tqdm(total=len(prompts), desc="Processing prompts") as pbar:
            # Use ThreadPoolExecutor for parallel processing
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                # Submit all tasks
                future_to_prompt = {}
                for prompt_name, prompt_text in prompts.items():
                    future = executor.submit(
                        process_file_with_prompt, 
                        input_file, 
                        api_key, 
                        output_dir, 
                        prompt_name, 
                        prompt_text,
                        pbar
                    )
                    future_to_prompt[future] = prompt_name
                
                # Process results as they complete
                for future in concurrent.futures.as_completed(future_to_prompt):
                    prompt_name = future_to_prompt[future]
                    try:
                        result = future.result()
                        all_results.append(result)
                        
                        if result["success"]:
                            success_count += 1
                            
                            # Add the results to the evaluation text
                            content = result["content"]
                            # Limit the content to avoid token limits
                            if len(content) > 2000:
                                content = content[:2000] + "... [truncated]"
                            prompt_results += f"\n### {prompt_name}\n{content}\n\n"
                            
                            # Print success message if not skipped
                            if not result.get("skipped", False):
                                print(f"✅ Flashcards saved to: {result['output_file']}")
                    except Exception as exc:
                        print(f"\n❌ {prompt_name} generated an exception: {exc}")
        
        print(f"\nTesting complete for {input_file}: {success_count}/{len(prompts)} prompts successfully tested")
        
        # Evaluate the results to find the top 3 templates
        top_templates = evaluate_flashcards(api_key, output_dir, file_stem, prompt_results)
    
        # Create a comparison HTML file
        html_output = os.path.join(output_dir, f"{file_stem}_comparison.html")
        with open(html_output, 'w', encoding='utf-8') as f:
            f.write(f"""<!DOCTYPE html>
<html>
<head>
    <title>Flashcard Prompt Comparison - {os.path.basename(input_file)}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .container {{ display: flex; flex-wrap: wrap; }}
        .prompt-result {{ 
            flex: 1; 
            min-width: 300px; 
            margin: 10px; 
            padding: 15px; 
            border: 1px solid #ccc; 
            border-radius: 5px;
        }}
        .top-pick {{ 
            border: 3px solid #4CAF50; 
            background-color: #f8fff8; 
        }}
        .top-pick h2 {{ 
            color: #4CAF50; 
        }}
        .top-pick::before {{ 
            content: "TOP PICK FOR TEST PREP"; 
            display: block; 
            background-color: #4CAF50; 
            color: white; 
            padding: 5px 10px; 
            margin: -15px -15px 15px -15px; 
            border-radius: 5px 5px 0 0; 
            font-weight: bold; 
        }}
        h2 {{ color: #333; }}
        pre {{ white-space: pre-wrap; }}
        .evaluation-section {{ 
            margin: 20px 0; 
            padding: 15px; 
            background-color: #f5f5f5; 
            border-radius: 5px; 
        }}
    </style>
</head>
<body>
    <h1>Flashcard Prompt Comparison</h1>
    <p>Input file: {os.path.basename(input_file)}</p>
    
    <div class="evaluation-section">
        <h2>AI Evaluation for Test Preparation</h2>
        <p>The AI has evaluated all prompt templates and identified the top 3 most effective for test preparation.</p>
""")
            
            # Add the evaluation results if available
            eval_file = os.path.join(output_dir, f"{file_stem}_evaluation.txt")
            if os.path.exists(eval_file):
                with open(eval_file, 'r', encoding='utf-8') as ef:
                    eval_content = ef.read()
                    f.write(f"<pre>{eval_content}</pre>")
            
            f.write("</div>\n<div class=\"container\">\n")
        
        
            for prompt_name in prompts:
                sanitized_prompt_name = prompt_name.replace('/', '_').replace(' ', '_')
                result_file = f"{file_stem}_{sanitized_prompt_name}_flashcards.txt"
                result_path = os.path.join(output_dir, result_file)
                
                # Check if this is a top template
                is_top = prompt_name in top_templates
                div_class = 'prompt-result top-pick' if is_top else 'prompt-result'
                
                f.write(f'        <div class="{div_class}">\n')
                f.write(f'            <h2>{prompt_name}</h2>\n')
            
                if os.path.exists(result_path):
                    with open(result_path, 'r', encoding='utf-8') as rf:
                        content = rf.read()
                    f.write(f'            <pre>{content}</pre>\n')
                else:
                    f.write(f'            <p>No results available</p>\n')
                
                f.write(f'        </div>\n')
            
            f.write("""    </div>
</body>
</html>
""")
            
            print(f"HTML comparison file created: {html_output}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
