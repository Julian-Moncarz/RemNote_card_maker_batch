# RemNote Flashcard Generator

This command-line tool processes PDF and image files from a source folder, generates RemNote flashcards using the Google Gemini API, and saves them as text files in a structured `remnote_cards` directory.

## Prerequisites

- Python 3.9 or higher
- google-generativeai Python package
- Google Gemini API key ([Get one here](https://ai.google.dev/))

## Setup

1. Ensure you have Python 3.9 or higher installed.
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install the required dependency:
   ```bash
   pip install google-generativeai
   ```

## Usage

Run the script with the following command:

```bash
python generate_flashcards.py <source_directory> --api-key YOUR_API_KEY
```

Alternatively, you can set your API key as an environment variable:

```bash
export GOOGLE_API_KEY=your_api_key
python generate_flashcards.py <source_directory>
```

### Arguments

- `source_directory`: Directory containing PDF and image files to process
- `--api-key`: Your Google Gemini API key (optional if set as environment variable)

### Example

```bash
python generate_flashcards.py ./notes --api-key YOUR_API_KEY
```

This will process all PDF and image files in the `./notes` directory (including subdirectories) and save the generated flashcards in the `remnote_cards/notes` directory (created automatically if it doesn't exist).

## Supported File Types

- PDF files (.pdf)
- Image files (.jpg, .jpeg, .png)

## Output Format

The script generates two types of output files:

1. **Individual flashcard files**: Each processed file will have its own flashcard file saved in the `remnote_cards/[source_folder_name]` directory. Each file will be named after the original file with `_flashcards.txt` appended to it.

2. **Combined notes file**: All generated flashcards are also combined into a single file named `[source_folder_name]_notes.txt` in the same output directory, making it easy to import all flashcards at once.

The flashcards follow the RemNote format:

```
## [Object Name]

* [Question] == [Answer]  
* [Question] == [Answer]  
* [Question] == [Answer]
```

## How It Works

1. The script recursively searches the source directory for supported file types
2. Each file is uploaded to the Gemini API
3. The Gemini 2.0 Flash model processes the content with a specialized prompt that:
   - Identifies significant concepts, systems, processes, or terms as "Objects"
   - Creates atomic questions targeting the smallest meaningful units of knowledge
   - Ensures questions are deterministic and point to specific answers
   - Covers ALL information in the document
4. The generated flashcards are saved as individual text files
5. All flashcards are combined into a single notes file for easy import

## Notes

- The script uses the Gemini 2.0 Flash model, which is optimized for processing documents and images
- The API has usage limits, so be mindful of how many files you process
- Large files may take longer to process
- The script processes files recursively, so it will find files in all subdirectories of the source folder
