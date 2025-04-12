"""
This script creates YouTube short scripts for each chapter of a dissertation.
"""

from docx.api import Document
from PyPDF2 import PdfReader
from openai import OpenAI
from dotenv import load_dotenv
import re
import os
from pathlib import Path

load_dotenv()

client = OpenAI()

# Constants
MODEL = "gpt-4o"
CHAPTER_PATTERNS = [
    r'^Chapter\s+\d+',  # Matches "Chapter 1", "Chapter 2", etc.
    r'^\d+\.\s+',       # Matches "1. ", "2. ", etc.
    r'^CHAPTER\s+\d+',  # Matches "CHAPTER 1", "CHAPTER 2", etc.
    r'^\d+\.\d+\.\s+',  # Matches "1.1. ", "1.2. ", etc.
]

def detect_chapters(text: str) -> list[tuple[str, str]]:
    """Detect chapters in the text and return them as (title, content) pairs
    
    Args:
        text (str): The full text of the document
        
    Returns:
        list[tuple[str, str]]: List of (chapter_title, chapter_content) pairs
    """
    # Split text into lines
    lines = text.split('\n')
    chapters = []
    current_chapter = []
    current_title = None
    
    for line in lines:
        # Check if this line matches any chapter pattern
        is_chapter = any(re.match(pattern, line.strip()) for pattern in CHAPTER_PATTERNS)
        
        if is_chapter:
            # If we have a previous chapter, save it
            if current_title and current_chapter:
                chapters.append((current_title, '\n'.join(current_chapter)))
            
            # Start new chapter
            current_title = line.strip()
            current_chapter = []
        else:
            current_chapter.append(line)
    
    # Add the last chapter
    if current_title and current_chapter:
        chapters.append((current_title, '\n'.join(current_chapter)))
    
    return chapters

def create_chapter_filename(chapter_title: str) -> str:
    """Create a valid filename from a chapter title
    
    Args:
        chapter_title (str): The chapter title
        
    Returns:
        str: A valid filename
    """
    # Remove special characters and replace spaces with underscores
    filename = re.sub(r'[^\w\s-]', '', chapter_title)
    filename = re.sub(r'\s+', '_', filename)
    filename = filename.lower()
    return f"{filename}.txt"

def read_word_doc(file_path: str) -> str:
    """Read content from a Word document
    
    Args:
        file_path (str): The path to the Word document
        
    Returns:
        str: The content of the Word document
    """
    doc = Document(file_path)
    text = []
    for paragraph in doc.paragraphs:
        # Normalize whitespace and remove excessive newlines
        cleaned_text = ' '.join(paragraph.text.split())
        if cleaned_text:  # Only append non-empty paragraphs
            text.append(cleaned_text)
    return '\n'.join(text)


def read_pdf(file_path: str) -> str:
    """Read content from a PDF file
    
    Args:
        file_path (str): The path to the PDF file
        
    Returns:
        str: The content of the PDF file
    """
    reader = PdfReader(file_path)
    text = []
    for page in reader.pages:
        # Normalize whitespace and handle unwanted line breaks
        page_text = page.extract_text()
        # Split on actual paragraph breaks (double newlines) and clean each paragraph
        paragraphs = [' '.join(p.split()) for p in page_text.split('\n\n')]
        # Filter out empty paragraphs and add non-empty ones
        text.extend(p for p in paragraphs if p)
    return '\n'.join(text)


def chunk_text(text: str, chunk_size: int = 2000) -> list[str]:
    """Split text into smaller chunks
    
    Args:
        text (str): The text to chunk
        chunk_size (int): The size of each chunk
        
    Returns:
        list[str]: A list of chunks
    """
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


def summarize_text(text: str) -> str:
    """Summarize text using LLM
    
    Args:
        text (str): The text to summarize
        
    Returns:
        str: The summary of the text
    """
    chunks = chunk_text(text)
    print(f"Number of chunks: {len(chunks)}")
    summaries = []

    i = 0
    
    # First round: Summarize each chunk
    for chunk in chunks:
        prompt = f"""
        Summarize the following text concisely and clearly. Improve the writing style, making it engaging, coherent, and easy to follow. Preserve all factual details accurately and avoid introducing bias or opinion. Evaluate the actions of historical figures objectively and fairly, considering the historical context without imposing modern judgments or implying sinister intentions. If describing objectionable actions, report them factually without taking sides or excusing them.

        Text:
        {chunk}

        Objective and improved summary:
        """
        messages = [
            {"role": "developer", "content": "You are a helpful assistant that creates concise, accurate summaries while preserving key information."},
            {"role": "user", "content": prompt}
        ]
        response = client.responses.create(
            model=MODEL,
            input=messages
        )
        summaries.append(response.output[0].content[0].text)
        print(f"Summary {i+1}: {summaries[-1]}")
        i += 1

    # Second round: Create final YouTube Short script
    combined_summary = "\n".join(summaries)
    messages = [
        {"role": "developer", "content": "You are an expert scriptwriter for YouTube Shorts who creates engaging, objective, and historically accurate scripts. Scripts must be concise enough to be spoken in under 60 seconds (approximately 200 words)."},
        {"role": "user", "content": f"""
        Create a concise and engaging script for a YouTube Short based on the following summaries. 

        Instructions:
        - The script should grab viewers' attention immediately.
        - Use clear and engaging language suitable for spoken delivery.
        - Preserve all factual accuracy strictly.
        - Objectively represent historical actors' actions fairly within their historical contexts. Do not judge them by modern standards or imply sinister intent unfairly.
        - If mentioning controversial or objectionable actions, present them factually without bias, justification, or condemnation.

        Summaries:
        {combined_summary}

        YouTube Short script:
        """}
    ]
    
    final_response = client.responses.create(
        model=MODEL,
        input=messages,
        max_output_tokens=500  # Approximately 200 words
    )
    
    return final_response.output[0].content[0].text


def process_document(file_path: str) -> list[str]:
    """Process document and create summaries for each chapter
    
    Args:
        file_path (str): The path to the document
        
    Returns:
        list[str]: List of paths to the summary files
    """
    # Determine file type and read content
    if file_path.lower().endswith('.docx'):
        content = read_word_doc(file_path)
    elif file_path.lower().endswith('.pdf'):
        content = read_pdf(file_path)
    else:
        raise ValueError("Unsupported file format. Please use .docx or .pdf")
    
    print(f"Content read from file: {file_path.split('/')[-1]}")
    
    # Detect chapters
    chapters = detect_chapters(content)
    print(f"Found {len(chapters)} chapters")
    
    # Create output directory if it doesn't exist
    output_dir = Path('TextSummariser/chapter_scripts')
    output_dir.mkdir(exist_ok=True)
    
    output_paths = []
    
    # Process each chapter
    for i, (title, content) in enumerate(chapters, 1):
        print(f"\nProcessing chapter {i}: {title}")
        
        # Generate summary
        summary = summarize_text(content)
        
        # Create filename and save
        filename = create_chapter_filename(title)
        output_path = output_dir / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"Chapter: {title}\n\n")
            f.write(summary)
        
        output_paths.append(str(output_path))
        print(f"Script saved to {output_path}")
    
    return output_paths


if __name__ == "__main__":
    file_path = "/Users/stephenkeeler/git/ai-diy/TextSummariser/lse_dissertation.docx"
    output_paths = process_document(file_path)
    print(f"\nAll scripts saved. Total: {len(output_paths)}")
