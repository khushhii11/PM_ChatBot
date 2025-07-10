# Word Document to JSON Extractor

This script extracts text from a Word document (`PMData.docx`) and converts it into JSON blocks with the following structure:
- `id`: Unique identifier for each text block
- `content`: The extracted text content
- `links_keywords`: Array of URLs and important keywords found in the text

## Step-by-Step Instructions

### Step 1: Install Dependencies
First, install the required Python package:
```bash
pip install -r requirements.txt
```

### Step 2: Run the Extraction Script
Execute the Python script to extract content from your Word document:
```bash
python extract_docx_to_json.py
```

### Step 3: Check the Results
The script will:
1. Process the `PMData.docx` file
2. Create an `extracted_content.json` file with the results
3. Display a preview of the first few extracted blocks in the console

## Output Format

Each JSON block will have this structure:
```json
{
  "id": 1,
  "content": "Your extracted text content here...",
  "links_keywords": ["URL1", "URL2", "Keyword1", "Keyword2"]
}
```

## Features

- **Automatic URL Detection**: Finds and extracts any URLs in the text
- **Keyword Extraction**: Identifies potential keywords (capitalized words, technical terms)
- **Unique IDs**: Each text block gets a sequential unique identifier
- **UTF-8 Support**: Handles special characters and international text
- **Error Handling**: Gracefully handles document processing errors

## Customization

You can modify the `extract_links_and_keywords()` function in the script to:
- Adjust keyword detection rules
- Add more sophisticated keyword extraction logic
- Customize the filtering of common words
- Add domain-specific keyword patterns

## Troubleshooting

If you encounter any issues:
1. Make sure `PMData.docx` is in the same directory as the script
2. Verify that the document is not corrupted or password-protected
3. Check that you have write permissions in the current directory 