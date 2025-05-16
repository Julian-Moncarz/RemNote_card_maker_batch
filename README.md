# RemNote Flashcard Generator

This command-line tool processes PDF and image files from a source folder, generates RemNote flashcards using the Google Gemini API, and saves them as text files in a `remnote_cards` directory.

## Prerequisites

- Python 3.9 or higher
- google-generativeai Python package
- Google Gemini API key ([Get one here](https://ai.google.dev/))

## Setup

1. Ensure you have Python 3.9 or higher installed.
2. Install the required dependency:
   - `google-generativeai` (use `pip install google-generativeai`)

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

This will process all PDF and image files in the `./notes` directory and save the generated flashcards as text files in the `remnote_cards` directory (created automatically if it doesn't exist).

## Supported File Types

- PDF files (.pdf)
- Image files (.jpg, .jpeg, .png)

## Output Format

The generated flashcards will be saved as text files in the `remnote_cards` directory. Each file will be named after the original file with `_flashcards.txt` appended to it.

The flashcards follow the RemNote format:

```
## [Object Name]

* [Question] == [Answer]  
* [Question] == [Answer]  
* [Question] == [Answer]
```

## Notes

- The script uses the Gemini 2.0 Flash model, which is optimized for processing documents and images.
- The API has usage limits, so be mindful of how many files you process.
- Large files may take longer to process.
