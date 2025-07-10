import json
import re
from docx import Document
from typing import List, Dict, Any

def extract_links(text: str) -> List[str]:
    """
    Extract only URLs from text.
    """
    url_pattern = r'https?://[^\s]+'
    links = re.findall(url_pattern, text)
    return list(set(links))  # Remove duplicates

def extract_qa_pairs_to_json(docx_path: str) -> List[Dict[str, Any]]:
    """
    Extract Q&A pairs from Word document and convert to JSON blocks.
    Each block will have: id, question, answer, links
    """
    try:
        # Load the document
        doc = Document(docx_path)
        
        json_blocks = []
        block_id = 1
        current_question = ""
        current_answer = ""
        in_qa_section = False
        
        for paragraph in doc.paragraphs:
            text = paragraph.text.strip()
            
            # Skip empty paragraphs
            if not text:
                continue
            
            # Check if this is a question (starts with "Q:")
            if text.startswith("Q:"):
                # If we have a previous Q&A pair, save it
                if current_question and current_answer:
                    # Extract links from both question and answer
                    question_links = extract_links(current_question)
                    answer_links = extract_links(current_answer)
                    all_links = list(set(question_links + answer_links))  # Remove duplicates
                    
                    block = {
                        "id": block_id,
                        "question": current_question,
                        "answer": current_answer,
                        "links": all_links
                    }
                    json_blocks.append(block)
                    block_id += 1
                
                # Start new Q&A pair
                current_question = text
                current_answer = ""
                in_qa_section = True
            
            # Check if this is an answer (starts with "A:")
            elif text.startswith("A:"):
                current_answer = text
                in_qa_section = True
            
            # If we're in a Q&A section and have a question but no answer yet, or if we have an answer, append to answer
            elif in_qa_section and (current_question or current_answer):
                if current_answer:
                    current_answer += " " + text
                else:
                    current_answer = text
        
        # Don't forget the last Q&A pair
        if current_question and current_answer:
            question_links = extract_links(current_question)
            answer_links = extract_links(current_answer)
            all_links = list(set(question_links + answer_links))
            
            block = {
                "id": block_id,
                "question": current_question,
                "answer": current_answer,
                "links": all_links
            }
            json_blocks.append(block)
        
        return json_blocks
    
    except Exception as e:
        print(f"Error processing document: {e}")
        return []

def main():
    # Process the Word document
    docx_file = "PMData.docx"
    json_blocks = extract_qa_pairs_to_json(docx_file)
    
    if json_blocks:
        # Save to JSON file
        output_file = "extracted_qa_content.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(json_blocks, f, indent=2, ensure_ascii=False)
        
        print(f"Successfully extracted {len(json_blocks)} Q&A blocks from {docx_file}")
        print(f"Results saved to {output_file}")
        
        # Display first few blocks as preview
        print("\nPreview of extracted Q&A content:")
        for i, block in enumerate(json_blocks[:3]):
            print(f"\nBlock {block['id']}:")
            print(f"Question: {block['question']}")
            print(f"Answer: {block['answer'][:100]}...")
            print(f"Links: {block['links']}")
        
        if len(json_blocks) > 3:
            print(f"\n... and {len(json_blocks) - 3} more Q&A blocks")
    
    else:
        print("No Q&A content extracted from the document.")

if __name__ == "__main__":
    main() 