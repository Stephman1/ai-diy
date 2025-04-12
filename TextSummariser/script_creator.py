"""
This script creates a script for a YouTube video short based on a text input from a Word document or PDF file.
"""

from docx.api import Document
from PyPDF2 import PdfReader
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

# Constants
MODEL = "gpt-4o-2024-11-20"


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


def process_document(file_path: str) -> str:
    """Process document and create summary
    
    Args:
        file_path (str): The path to the document
        
    Returns:
        str: The path to the summary file
    """
    # Determine file type and read content
    if file_path.lower().endswith('.docx'):
        content = read_word_doc(file_path)
    elif file_path.lower().endswith('.pdf'):
        content = read_pdf(file_path)
    else:
        raise ValueError("Unsupported file format. Please use .docx or .pdf")
    
    print(f"Content read from file: {file_path.split('/')[-1]}")

    # Generate summary
    summary = summarize_text(content)
    
    # Save summary to file
    output_path = 'TextSummariser/summary_output.txt'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(summary)
    
    return output_path


if __name__ == "__main__":
    file_path = "/Users/stephenkeeler/git/ai-diy/TextSummariser/lse_dissertation.docx"  # Change this to your input file path
    output_path = process_document(file_path)
    print(f"Summary saved to {output_path}")
