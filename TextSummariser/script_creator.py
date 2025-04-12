"""
This script creates a script for a YouTube video short based on a text input from a Word document or PDF file.
"""

import os

from docx.api import Document
from PyPDF2 import PdfReader
from openai import OpenAI

# Constants
OLLAMA_API = "http://localhost:11434/api/chat"
HEADERS = {"Content-Type": "application/json"}
MODEL = "llama3.2"

def read_word_doc(file_path):
    """Read content from a Word document"""
    doc = Document(file_path)
    text = []
    for paragraph in doc.paragraphs:
        text.append(paragraph.text)
    return '\n'.join(text)

def read_pdf(file_path):
    """Read content from a PDF file"""
    reader = PdfReader(file_path)
    text = []
    for page in reader.pages:
        text.append(page.extract_text())
    return '\n'.join(text)

def chunk_text(text, chunk_size=2000):
    """Split text into smaller chunks"""
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0
    
    for word in words:
        current_length += len(word) + 1  # +1 for space
        if current_length > chunk_size:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_length = len(word)
        else:
            current_chunk.append(word)
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks

def summarize_text(text):
    """Summarize text using local Llama model via OpenAI client library"""
    
    chunks = chunk_text(text)
    print(f"Chunks: {chunks}")
    summaries = []

    ollama_via_openai = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')

    i = 0
    
    # First round: Summarize each chunk
    for chunk in chunks:
        prompt = f"Please summarize the following text concisely, focusing on the most engaging and important points:\n\n{chunk}\n\nSummary:"
        messages = [
            {"role": "system", "content": "You are a helpful assistant that creates concise, accurate summaries while preserving key information."},
            {"role": "user", "content": prompt}
        ]
        response = ollama_via_openai.chat.completions.create(
            model=MODEL,
            messages=messages
        )
        summaries.append(response.choices[0].message.content.strip())
        print(f"Summary {i+1}: {summaries[-1]}")
        i += 1

    # Second round: Create final YouTube Short script
    combined_summary = "\n".join(summaries)
    messages = [
        {"role": "system", "content": "You are a scriptwriter for YouTube Shorts. Create engaging scripts that can be spoken in under 60 seconds (approximately 150-180 words)."},
        {"role": "user", "content": f"Create an engaging script for a YouTube Short based on this content. The script should be spoken in under 60 seconds and grab viewer attention:\n\n{combined_summary}"}
    ]
    
    final_response = ollama_via_openai.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.7,
        max_tokens=250  # Approximately 180-200 words
    )
    
    return final_response.choices[0].message.content.strip()

def process_document(file_path):
    """Process document and create summary"""
    # Determine file type and read content
    if file_path.lower().endswith('.docx'):
        content = read_word_doc(file_path)
    elif file_path.lower().endswith('.pdf'):
        content = read_pdf(file_path)
    else:
        raise ValueError("Unsupported file format. Please use .docx or .pdf")
    
    print("Content read")

    # Generate summary
    summary = summarize_text(content)
    
    # Save summary to file
    output_path = 'summary_output.txt'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(summary)
    
    return output_path


if __name__ == "__main__":
    file_path = "/Users/stephenkeeler/git/ai-diy/TextSummariser/lse_dissertation.docx"  # Change this to your input file path
    output_path = process_document(file_path)
    print(f"Summary saved to {output_path}")
